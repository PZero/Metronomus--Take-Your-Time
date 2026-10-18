"""Verifica del piano 1:1 in OpenSCAD: ricostruisce i fili di rame SOLO dai dati stampati nel PDF.

Uso:  python fili/verifica_scad.py                 -> modello/verifica-rame.scad (aprilo con OpenSCAD)
      python fili/verifica_scad.py alimentazione   -> modello/verifica-alimentazione.scad: tutte le schede,
                                                      solo i fili di batterie, TP4056, MT3608 e Mini-360
      python fili/verifica_scad.py esp32           -> modello/verifica-esp32.scad: segnali dall'ESP32 alle altre schede

Per ogni pezzo della distinta prende quello che c'è scritto nel PDF: coordinate dei nodi A e B, tipo delle
estremità e lunghezza di taglio. Poi mette il pezzo TAGLIATO al suo posto:
  - battuta: la testa si ferma 0,5 mm prima del nodo (appoggia sul fianco dell'altro filo);
  - passante: il filo va 0,5 mm oltre il nodo (copre il filo che arriva);
  - pin: attraversa il foro e sporge di 2,5 mm dall'altra parte della scheda;  base: entra 5 mm nel legno.
Controlla che:
  1. il pezzo così ricostruito sia lungo esattamente quanto il taglio stampato;
  2. in ogni giunto (G..) i fili si tocchino davvero (nessun vuoto da riempire di stagno);
  3. fili di reti diverse non si tocchino, contando anche le parti che sporgono (cortocircuiti);
  4. le punte che sporgono oltre i fori delle schede non entrino in un'altra scheda.
Nel modello: cursore "passo" per rivedere il montaggio gruppo per gruppo, numeri dei pezzi come nel PDF,
giunti in rosso, problemi evidenziati da sfere rosse (e scritti nella console di OpenSCAD).
"""
import math
import sys

import geometria as G
from piano_pdf import prepara

# reti di ogni verifica per gradi (python fili/verifica_scad.py alimentazione); None = tutte
GRADI = {"alimentazione": ["BATT+", "BATT-", "VBAT", "VSW", "V12", "GND", "3V3_SW"],
         "esp32": ["PWM_A", "PWM_B", "PWM_C", "PWR_EN", "LED_PWM", "VBAT_ADC", "SCL", "SDA", "STOP", "ARMA",
                   "ENC_A", "ENC_B", "ENC_SW", "VIB_IN"]}
RETI_SEL = None
CAVETTI = G.CAVETTI
NOME_FILE = "verifica-rame.scad"
CONTATTO = 2 * G.R_FILO + 0.05          # due fili Ø 1 si toccano se gli assi sono a meno di 1 mm
TOCCA_TESTA = G.R_FILO + 0.05           # una testa in battuta tocca il fianco se dista 0,5 mm dall'asse


def pezzo_tagliato(p):
    """Estremi del pezzo vero (lungo quanto il taglio), sull'asse da A a B."""
    d = G.sub(p.b, p.a)
    u = G.mul(d, 1 / G.norma(d))
    a = G.add(p.a, G.mul(u, -G.sovrappiu(p.tipo_a, p.rete)))
    b = G.add(p.b, G.mul(u, G.sovrappiu(p.tipo_b, p.rete)))
    return G.tonda(a), G.tonda(b)


def controlla(pezzi, giunti):
    problemi = []                             # (testo, punto)
    vero = {p.codice: pezzo_tagliato(p) for p in pezzi}

    # 1. lunghezze: ricostruito contro taglio stampato (il PDF arrotonda a 0,1 mm)
    for p in pezzi:
        a, b = vero[p.codice]
        l = G.norma(G.sub(b, a))
        if abs(l - round(p.taglio, 1)) > 0.051:
            problemi.append((f"{p.n} {p.codice}: ricostruito {l:.2f} mm, stampato {p.taglio:.1f} mm", a))

    # 2. giunti: i pezzi che si incontrano devono toccarsi
    for pt, g in giunti.items():
        chi = [p for p in pezzi if g in p.giunti]
        if len(chi) < 2:
            problemi.append((f"{g}: un solo pezzo ({chi[0].codice if chi else '-'})", pt))
            continue
        for i, p in enumerate(chi):
            vicini = [G.distanza_segmenti(*vero[p.codice], *vero[q.codice]) for q in chi if q is not p]
            if min(vicini) > CONTATTO:
                problemi.append((f"{g}: {p.codice} non tocca gli altri (vuoto di {min(vicini) - 2 * G.R_FILO:.2f} mm)", pt))

    # 3. cortocircuiti tra reti diverse, con i pezzi veri (punte sotto le schede comprese)
    for i, p in enumerate(pezzi):
        for q in pezzi[i + 1:]:
            if p.rete == q.rete:
                continue
            d = G.distanza_segmenti(*vero[p.codice], *vero[q.codice])
            if d < CONTATTO:
                a, b = vero[p.codice]
                problemi.append((f"CORTO {p.codice} ({p.rete}) e {q.codice} ({q.rete}): assi a {d:.2f} mm",
                                 G.tonda(G.mul(G.add(a, b), 0.5))))

    # 3b. batterie: la barra BATT+ deve toccare il polo + (fronte) di ogni cella, la BATT- il polo - (retro)
    for i, bt in enumerate(G.BATTERIE, 1):
        cx, cy, cz = bt["centro"]
        for nome, polo in (("BATT+", (cx, cy - bt["lunghezza"] / 2, cz)), ("BATT-", (cx, cy + bt["lunghezza"] / 2, cz))):
            barre = [p for p in pezzi if p.rete == nome]
            if not barre:
                continue
            d = min(G.distanza_segmenti(*vero[p.codice], polo, G.add(polo, (0, 0, 1e-3))) for p in barre)
            if d > G.R_FILO + 0.05:
                problemi.append((f"cella {i}: {nome} non tocca il polo (vuoto di {d - G.R_FILO:.2f} mm): serve il contatto a molla", polo))

    # 4. punte oltre i fori: non devono entrare in un'altra scheda
    for p in pezzi:
        a, b = vero[p.codice]
        for lato, tipo, punta, nodo in (("A", p.tipo_a, a, p.a), ("B", p.tipo_b, b, p.b)):
            if tipo != "pin":
                continue
            for m in G.MODULI.values():
                lo, hi = m.scatola()
                if G.segmento_in_scatola(nodo, punta, lo, hi, G.R_FILO) and not any(
                        G.norma(G.sub(m.pin(n), nodo)) < 1e-3 for n in m.pin_loc):
                    problemi.append((f"{p.codice}: la punta oltre il pin ({lato}) entra in {m.nome}", punta))
    return vero, problemi


def isole_saldate(pezzi):
    """Raggruppa i pezzi saldati tra loro (che condividono un giunto). Ritorna {codice: indice} e le isole."""
    padre = {p.codice: p.codice for p in pezzi}
    def radice(c):
        while padre[c] != c:
            padre[c] = padre[padre[c]]
            c = padre[c]
        return c
    per_giunto = {}
    for p in pezzi:
        for g in p.giunti:
            per_giunto.setdefault(g, []).append(p.codice)
    for chi in per_giunto.values():
        for c in chi[1:]:
            padre[radice(c)] = radice(chi[0])
    # cavetti sotto la base: saldati al rame che sporge dal foro da cui partono
    for i, c in enumerate(CAVETTI):
        padre[f"cavetto {i}"] = f"cavetto {i}"
        for p in pezzi:
            for e, t in ((p.a, p.tipo_a), (p.b, p.tipo_b)):
                if t == "base" and p.rete == c["rete"] and any(G.norma(G.sub(e[:2], f)) < 1e-3
                                                              for f in (c["da"], c.get("a_foro", c["da"]))):
                    padre[radice(f"cavetto {i}")] = radice(p.codice)
    gruppi = {}
    for p in pezzi:
        gruppi.setdefault(radice(p.codice), []).append(p)
    cav_isola = {}
    for i, c in enumerate(CAVETTI):
        cav_isola.setdefault(radice(f"cavetto {i}"), []).append(i)
    pin_mondo = {m.pin(n): f"{m.nome} {n}" for m in G.MODULI.values() for n in m.pin_loc}
    isole, comp = [], {}
    for k, sel in enumerate(sorted(gruppi.values(), key=lambda s: s[0].n)):
        arrivi, cavi = [], cav_isola.get(radice(sel[0].codice), [])
        for i in cavi:
            comp[f"cavetto {i}"] = k
            arrivi.append(CAVETTI[i]["a"] + " (cavetto sotto la base)")
        for p in sel:
            for e, t in ((p.a, p.tipo_a), (p.b, p.tipo_b)):
                if t == "pin":
                    arrivi.append(pin_mondo.get(e, "pin"))
                elif t == "libero":
                    arrivi.append("filo flessibile")
                elif t == "base" and p.rete not in G.RETI_ANCORATE and not cavi:
                    arrivi.append("SCENDE NELLA BASE MA NESSUN CAVETTO")
                elif t == "base":
                    arrivi.append("ancorato nella base" if p.rete in G.RETI_ANCORATE else "foro passante")
            comp[p.codice] = k
        reti = sorted({p.rete for p in sel})
        utile = (any(a not in ("foro passante", "ancorato nella base") for a in arrivi) or reti[0] in ("TELAIO", "PANNELLO"))             and not any("NESSUN CAVETTO" in a for a in arrivi)
        h = (k * 0.618034) % 1.0                       # tinte ben distanziate (rapporto aureo)
        rgb = hsv(h, 0.7, 0.9) if utile else [1.0, 0.0, 0.0]
        isole.append({"colore": [round(c, 3) for c in rgb],
                      "descrizione": f"{'/'.join(reti)}, {len(sel)} pezzi ({sel[0].n}..{sel[-1].n}) -> "
                                     + (", ".join(sorted(set(arrivi))) if arrivi else
                                        ("struttura" if utile else "NON ARRIVA A NIENTE"))})
    return comp, isole


def hsv(h, s, v):
    i = int(h * 6) % 6
    f = h * 6 - int(h * 6)
    p, q, t = v * (1 - s), v * (1 - f * s), v * (1 - (1 - f) * s)
    return [(v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)][i]


def scrivi(pezzi, giunti, vero, problemi):
    gi = {g: i + 1 for i, g in enumerate(G.GRUPPI)}
    r = ["// Metronomus: VERIFICA del piano del rame 1:1, GENERATO da fili/verifica_scad.py: non modificarlo a mano.",
         "// I fili sono i pezzi TAGLIATI come dice il PDF (lunghezza di taglio ed estremità), messi al loro posto.",
         "", "/* [Montaggio] */",
         f"// gruppi montati: {', '.join(f'{gi[g]} {G.NOMI_GRUPPI[g]}' for g in G.GRUPPI)}",
         f"passo = {len(G.GRUPPI)}; // [1:{len(G.GRUPPI)}]",
         "// mostra solo il gruppo del passo (senza quelli già montati)", "solo_passo = false;",
         "", "/* [Vista] */",
         "// saldature: stesso colore = fili saldati insieme (rosso = isola che non porta a niente); montaggio: rame/grigio",
         'colori = "saldature"; // [saldature, montaggio]', "schede = true;", "// nome scritto su ogni scheda", "nomi_schede = true;",
         "// sui pin da collegare: nome del pin e rete", "nomi_pin = true;",
         "// base di legno: contorno (si vede tutto quello che c'è sotto e dentro), trasparente o piena",
         'base = "contorno"; // [contorno, trasparente, piena, nascosta]',
         "// moduli e cavetti sotto la base (TP4056, vibrazione, encoder)", "sotto = true;", "numeri = true;", "giunti = true;",
         "problemi = true;", "// numero di un pezzo da evidenziare (0 = nessuno)", "evidenzia = 0;",
         "", "/* [Hidden] */", "$fn = 16;", f"R = {G.R_FILO};",
         "RAME = [0.85, 0.45, 0.2]; GRIGIO = [0.6, 0.6, 0.6]; ROSSO = [0.95, 0.05, 0.05];",
         "module seg(a, b, r = R) { v = b - a; l = norm(v);",
         "    if (l > 0) translate(a) rotate([0, acos(v[2] / l), atan2(v[1], v[0])]) cylinder(r = r, h = l); }",
         "module cartellino(p, t, s = 1.6, col = [0.1, 0.1, 0.1]) {",
         "    translate(p) rotate([90, 0, 0]) color(col) linear_extrude(0.2) text(t, size = s, halign = \"center\", valign = \"center\"); }",
         "function visibile(g) = solo_passo ? g == passo : g <= passo;", ""]
    if problemi:
        r.append(f"echo(\"VERIFICA: {len(problemi)} problemi\");")
        for t, _ in problemi:
            r.append(f'echo("PROBLEMA: {t}");')
    else:
        r.append('echo("VERIFICA: nessun problema, i pezzi del PDF combaciano");')
    r.append("")

    # isole di rame: pezzi saldati tra loro (stesso colore); un'isola che non arriva a nessun pin, foro della base
    # o filo flessibile non serve a niente e diventa rossa
    comp, isole = isole_saldate(pezzi)
    r.append("// isole di rame saldate insieme (colori = saldature):")
    for k, isola in enumerate(isole):
        r.append(f'echo("ISOLA {k + 1}: {isola["descrizione"]}");')

    # pezzi: [n, gruppo, A, B, codice, taglio, nodoA, nodoB, colore dell'isola]
    righe = []
    for p in pezzi:
        a, b = vero[p.codice]
        col = isole[comp[p.codice]]["colore"]
        righe.append(f'  [{p.n}, {gi[p.gruppo]}, {list(a)}, {list(b)}, "{p.codice}", {p.taglio:.1f}, {list(p.a)}, {list(p.b)}, {col}]')
    r.append("PEZZI = [\n" + ",\n".join(righe) + "\n];")
    r.append("""for (p = PEZZI) if (visibile(p[1])) {
    col = p[0] == evidenzia ? [0.1, 0.8, 0.2] : colori == "saldature" ? p[8] : (p[1] == passo ? RAME : GRIGIO);
    color(col) seg(p[2], p[3], p[0] == evidenzia ? R * 1.5 : R);
    if (numeri && p[1] == passo) { m = (p[6] + p[7]) / 2; cartellino(m + [1.6, -1.2, 0.8], str(p[0])); }
}""")
    gr = []
    for pt, g in giunti.items():
        grp = max(gi[p.gruppo] for p in pezzi if g in p.giunti)     # si salda quando arriva l'ultimo pezzo
        gr.append(f'  ["{g}", {grp}, {list(pt)}]')
    r.append("GIUNTI = [\n" + ",\n".join(gr) + "\n];")
    r.append("""if (giunti) for (g = GIUNTI) if (visibile(g[1])) {
    color([1, 0.1, 0.1, 0.55]) translate(g[2]) sphere(r = R * 1.5);
    if (numeri && g[1] == passo) cartellino(g[2] + [-2.4, -1.2, 1.4], g[0], 1.2, ROSSO);
}""")

    # schede e ingombri (solo contesto)
    collegati = {(c, pn): nome for nome, rt in G.RETI.items() for c, pn in rt.pin if RETI_SEL is None or nome in RETI_SEL}
    r.append("if (schede) {")
    for chiave, m in G.MODULI.items():
        g = gi.get(chiave, 1)
        o, u, v, n = m.origine, m.u, m.v, m.n
        w, h = m.dimensioni
        mat = [[u[0], v[0], n[0], o[0]], [u[1], v[1], n[1], o[1]], [u[2], v[2], n[2], o[2]], [0, 0, 0, 1]]
        r.append(f"  if (visibile({g})) color([0.2, 0.35, 0.7, 0.35]) multmatrix({mat}) "
                 f"translate([0, 0, {-m.spessore}]) cube([{w}, {h}, {m.spessore}]);  // {m.nome}")
        for pn in m.pin_loc:
            q = m.pin(pn)
            r.append(f"  if (visibile({g})) color([0.9, 0.8, 0.3]) translate({list(q)}) sphere(r = 0.35, $fn = 8);")
        # nome della scheda e pin da collegare, scritti sulla faccia dei componenti (sistema locale della scheda)
        r.append(f"  if (visibile({g})) multmatrix({mat}) translate([0, 0, 0.05]) {{")
        usati = [(pn, xy) for pn, xy in m.pin_loc.items() if (chiave, pn) in collegati]
        # nome della scheda fuori dal bordo con meno pin collegati vicini, scritto lungo il bordo
        bordi = {"sotto": lambda x, y: y, "sopra": lambda x, y: h - y, "sinistra": lambda x, y: x, "destra": lambda x, y: w - x}
        bordo = min(bordi, key=lambda b: sum(1 for _, (x, y) in usati if bordi[b](x, y) < 5))
        corpo = min(2.0, max(w, h) / (0.75 * len(m.nome)))
        pos_nome = {"sotto": ([w / 2, -1.0], 0, "top"), "sopra": ([w / 2, h + 1.0], 0, "bottom"),
                    "sinistra": ([-1.0, h / 2], 90, "bottom"), "destra": ([w + 1.0, h / 2], 90, "top")}[bordo]
        r.append(f'    if (nomi_schede) color([0.05, 0.15, 0.45]) translate({pos_nome[0]}) rotate({pos_nome[1]}) '
                 f'linear_extrude(0.2) text("{m.nome}", size = {corpo:.2f}, halign = "center", valign = "{pos_nome[2]}");')
        # pin collegati: "PIN RETE" verso l'interno della scheda se ci sta senza coprire altri pin,
        # altrimenti verso il bordo più vicino (fuori dalla scheda)
        CORPO = 0.8
        def scritta(x, y, d, testo, col):
            ruota, alli = {(1, 0): (0, "left"), (-1, 0): (0, "right"), (0, 1): (90, "left"), (0, -1): (90, "right")}[d]
            r.append(f'    if (nomi_pin) color({col}) translate([{x + 0.9 * d[0]:.3f}, {y + 0.9 * d[1]:.3f}, 0]) '
                     f'rotate({ruota}) linear_extrude(0.2) text("{testo}", size = {CORPO}, halign = "{alli}", valign = "center");')
        for pn, (x, y) in usati:
            rete_pin = collegati[(chiave, pn)]
            dist = {(0, -1): y, (0, 1): h - y, (-1, 0): x, (1, 0): w - x}
            fuori = min(dist, key=dist.get)
            dentro = (-fuori[0], -fuori[1])
            def libero(d, testo):
                lungo = 0.95 * CORPO * len(testo) + 1.0
                return not any(0.4 < (x2 - x) * d[0] + (y2 - y) * d[1] < lungo and abs((x2 - x) * d[1] - (y2 - y) * d[0]) < 1.0
                               for p2, (x2, y2) in m.pin_loc.items() if p2 != pn)
            entra = lambda testo: libero(dentro, testo) and dist[dentro] / 2 > 0.95 * CORPO * len(testo) + 1.0
            if pn == rete_pin:
                scritta(x, y, dentro if entra(pn) else fuori, pn, "[0.6, 0.05, 0.05]")
            elif entra(pn) and libero(fuori, rete_pin):
                # nome del pin dentro la scheda, rete fuori (in blu)
                scritta(x, y, dentro, pn, "[0.6, 0.05, 0.05]")
                scritta(x, y, fuori, rete_pin, "[0.05, 0.25, 0.6]")
            else:
                testo = f"{pn} {rete_pin}"
                scritta(x, y, fuori if libero(fuori, testo) else dentro, testo, "[0.6, 0.05, 0.05]")
        r.append("  }")
    ax, ay, az = G.MOTORE["asse"]
    rr, ll = G.MOTORE["diametro"] / 2, G.MOTORE["lunghezza"]
    r.append(f"  color([0.75, 0.75, 0.78, 0.5]) seg([{ax}, {ay}, {az}], [{ax}, {ay - ll}, {az}], {rr});  // motore")
    for bt in G.BATTERIE:
        cx, cy, cz = bt["centro"]
        r.append(f"  color([0.25, 0.55, 0.95, 0.4]) seg([{cx}, {cy - bt['lunghezza'] / 2}, {cz}], "
                 f"[{cx}, {cy + bt['lunghezza'] / 2}, {cz}], {bt['diametro'] / 2});  // 18350")
    r.append("}")
    lo, hi = G.BASE["min"], G.BASE["max"]
    dim = [hi[i] - lo[i] for i in range(3)]
    r.append(f"if (base == \"piena\" || base == \"trasparente\") color([0.55, 0.33, 0.17, base == \"piena\" ? 1 : 0.25]) "
             f"translate({list(lo)}) cube({dim});")
    spigoli = []
    for i in range(3):                       # 12 spigoli della base
        for u in (0, 1):
            for v in (0, 1):
                p = [lo[0], lo[1], lo[2]]
                j, l = [x for x in range(3) if x != i]
                p[j] = (lo, hi)[u][j]
                p[l] = (lo, hi)[v][l]
                q = list(p)
                q[i] = hi[i]
                spigoli.append(f"seg({p}, {q}, 0.3)")
    r.append(f"if (base == \"contorno\") color([0.55, 0.33, 0.17]) {{ {' '.join(s + ';' for s in spigoli)} }}")
    # sotto la base: moduli negli scassi, cavetti isolati nelle canaline (colore dell'isola a cui sono saldati)
    r.append("if (sotto) {")
    for m in G.SOTTO.values():
        a, b = m.scatola()
        r.append(f"  color([0.15, 0.2, 0.35, 0.7]) translate({list(a)}) cube({[round(b[i] - a[i], 3) for i in range(3)]});  // {m.nome}")
        centro = [round((a[0] + b[0]) / 2, 2), round(a[1] - 0.2, 2), round(a[2] - 1.5, 2)]
        r.append(f'  if (nomi_schede) cartellino({centro}, "{m.nome}", 1.8, [0.05, 0.15, 0.45]);')
        for pn in m.pin_loc:
            q = m.pin(pn)
            r.append(f"  color([0.9, 0.8, 0.3]) translate({list(q)}) sphere(r = 0.45, $fn = 8);")
            r.append(f'  if (nomi_pin) translate({list(G.add(q, (0, 0, -1.2)))}) rotate([180, 0, 0]) color([0.6, 0.05, 0.05]) '
                         f'linear_extrude(0.2) text("{pn}", size = 0.9, halign = "center", valign = "center");')
    (p0, lung) = G.ALBERO_ENCODER
    r.append(f"  color([0.75, 0.75, 0.78]) seg({list(p0)}, {list(G.add(p0, (0, -lung, 0)))}, 3);  // albero e pomello dell'encoder")
    a, b = G.PROLUNGA_USB
    r.append(f"  color([0.3, 0.3, 0.3]) translate({list(a)}) cube({[round(b[i] - a[i], 3) for i in range(3)]});  // presa USB-C da pannello")
    for i, c in enumerate(CAVETTI):
        col = isole[comp[f"cavetto {i}"]]["colore"] if f"cavetto {i}" in comp else [1, 0, 0]
        for p, q in zip(c["punti"], c["punti"][1:]):
            r.append(f"  color({col}) seg({list(p)}, {list(q)}, 0.4);  // cavetto {c['rete']} -> {c['a']}")
        r.append(f"  color({col}) translate({list(c['punti'][0])}) sphere(r = 0.7);")
    r.append("}")
    if problemi:
        r.append("if (problemi) {")
        for t, pt in problemi:
            r.append(f"  color([1, 0, 0, 0.35]) translate({list(pt)}) sphere(r = 2.5);  // {t}")
        r.append("}")
    out = G.RADICE / "modello" / NOME_FILE
    out.write_text("\n".join(r) + "\n", encoding="utf-8")
    return out


def main():
    global RETI_SEL, CAVETTI, NOME_FILE
    pezzi, giunti, errori, avvisi = prepara()
    if len(sys.argv) > 1:
        grado = sys.argv[1]
        if grado not in GRADI:
            sys.exit(f"gradi disponibili: {', '.join(GRADI)}")
        RETI_SEL = set(GRADI[grado])
        NOME_FILE = f"verifica-{grado}.scad"
        pezzi = [p for p in pezzi if p.rete in RETI_SEL]
        giunti = {pt: g for pt, g in giunti.items() if any(g in p.giunti for p in pezzi)}
        CAVETTI = [c for c in G.CAVETTI if c["rete"] in RETI_SEL]
    vero, problemi = controlla(pezzi, giunti)
    out = scrivi(pezzi, giunti, vero, problemi)
    print(f"{out.relative_to(G.RADICE)}: {len(pezzi)} pezzi tagliati come da PDF, {len(giunti)} giunti")
    for e in errori + avvisi:
        print("GEOMETRIA:", e)
    if problemi:
        for t, _ in problemi:
            print("PROBLEMA:", t)
    else:
        print("nessun problema: lunghezze, giunti e distanze tornano")


if __name__ == "__main__":
    main()
