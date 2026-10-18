"""Piano di montaggio del rame in PDF, in scala 1:1.

Uso:  python fili/piano_pdf.py            -> produzione/piano-rame.pdf
      python fili/piano_pdf.py --bozza    -> genera anche con misure stimate o errori (pagine marcate BOZZA)

Legge la geometria da fili/geometria.py (stesse misure, stessi controlli) e scrive, senza librerie esterne:
  1. copertina: righello di controllo da 100 mm, riepilogo, legenda delle estremità;
  2. dima di foratura della base (vista dall'alto, 1:1) con la tabella dei fori;
  3. per ogni gruppo di montaggio: viste 1:1 dall'alto, dal fronte e da destra, con i pezzi del gruppo
     in rame, quelli già montati in grigio, le schede e i giunti numerati;
  4. distinta di taglio in ordine di saldatura: per ogni pezzo codice, rete, taglio, estremità, giunti
     e il pezzo disegnato in scala reale (ci si appoggia il filo e si taglia).
Stampa SEMPRE al 100 % ("dimensioni effettive"): controlla il righello prima di tagliare.
"""
import sys
from datetime import date
from pathlib import Path

import geometria as G

MM = 72 / 25.4
A4 = (210.0, 297.0)
MARGINE = 10.0
RAME = (0.80, 0.42, 0.18)
GRIGIO = (0.72, 0.72, 0.72)
GRIGIO_SCURO = (0.35, 0.35, 0.35)
ROSSO = (0.85, 0.1, 0.1)
NERO = (0, 0, 0)
NOMI_ESTREMI = {"pin": "pin", "base": "base", "passante": "passante", "battuta": "battuta",
                "libero": "libero", "testa": "testa", "?": "?"}


# ================================================================== PDF minimale
def _testo_pdf(s):
    s = s.encode("cp1252", "replace")
    return s.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")


def larghezza_testo(t, corpo):
    return 0.52 * corpo * len(t)


class Pagina:
    """Una pagina; coordinate in mm con origine in basso a sinistra."""

    def __init__(self, w, h):
        self.w, self.h, self.ops = w, h, []

    def _col(self, col, riemp=False):
        return f"{col[0]:.3f} {col[1]:.3f} {col[2]:.3f} {'rg' if riemp else 'RG'}"

    def linea(self, a, b, sp=0.2, col=NERO, tratt=None):
        d = f"[{tratt[0]} {tratt[1]}] 0 d" if tratt else "[] 0 d"
        self.ops.append(f"{self._col(col)} {sp:.3f} w {d} 1 J {a[0]:.3f} {a[1]:.3f} m {b[0]:.3f} {b[1]:.3f} l S")

    def rett(self, x, y, w, h, sp=0.2, col=NERO, riemp=None, tratt=None):
        d = f"[{tratt[0]} {tratt[1]}] 0 d" if tratt else "[] 0 d"
        op = "B" if riemp and col else ("f" if riemp else "S")
        f = self._col(riemp, True) if riemp else ""
        self.ops.append(f"{self._col(col or NERO)} {f} {sp:.3f} w {d} {x:.3f} {y:.3f} {w:.3f} {h:.3f} re {op}")

    def cerchio(self, x, y, r, sp=0.2, col=NERO, riemp=None):
        k = 0.5523 * r
        p = (f"{x + r:.3f} {y:.3f} m {x + r:.3f} {y + k:.3f} {x + k:.3f} {y + r:.3f} {x:.3f} {y + r:.3f} c "
             f"{x - k:.3f} {y + r:.3f} {x - r:.3f} {y + k:.3f} {x - r:.3f} {y:.3f} c "
             f"{x - r:.3f} {y - k:.3f} {x - k:.3f} {y - r:.3f} {x:.3f} {y - r:.3f} c "
             f"{x + k:.3f} {y - r:.3f} {x + r:.3f} {y - k:.3f} {x + r:.3f} {y:.3f} c")
        op = "B" if riemp and col else ("f" if riemp else "S")
        f = self._col(riemp, True) if riemp else ""
        self.ops.append(f"{self._col(col or NERO)} {f} {sp:.3f} w [] 0 d {p} {op}")

    def testo(self, x, y, t, corpo=2.5, allinea="s", col=NERO, grassetto=False):
        if allinea == "c":
            x -= larghezza_testo(t, corpo) / 2
        elif allinea == "d":
            x -= larghezza_testo(t, corpo)
        self.ops.append((f"BT {self._col(col, True)} /{'F2' if grassetto else 'F1'} {corpo:.2f} Tf "
                         f"{x:.3f} {y:.3f} Td (").encode() + _testo_pdf(t) + b") Tj ET")

    def ritaglio(self, x, y, w, h):
        self.ops.append(f"q {x:.3f} {y:.3f} {w:.3f} {h:.3f} re W n")

    def fine_ritaglio(self):
        self.ops.append("Q")

    def contenuto(self):
        righe = [f"{MM:.6f} 0 0 {MM:.6f} 0 0 cm".encode()]
        righe += [o if isinstance(o, bytes) else o.encode() for o in self.ops]
        return b"\n".join(righe)


def scrivi_pdf(pagine, percorso):
    oggetti = [b"<< /Type /Catalog /Pages 2 0 R >>", None,
               b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
               b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"]
    figli = []
    for p in pagine:
        c = p.contenuto()
        oggetti.append(b"<< /Length %d >>\nstream\n" % len(c) + c + b"\nendstream")
        n_cont = len(oggetti)
        oggetti.append((f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {p.w * MM:.2f} {p.h * MM:.2f}] "
                        f"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents {n_cont} 0 R >>").encode())
        figli.append(f"{len(oggetti)} 0 R")
    oggetti[1] = f"<< /Type /Pages /Kids [{' '.join(figli)}] /Count {len(pagine)} >>".encode()
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    pos = []
    for i, o in enumerate(oggetti, 1):
        pos.append(len(out))
        out += b"%d 0 obj\n" % i + o + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(oggetti) + 1)
    for p in pos:
        out += b"%010d 00000 n \n" % p
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(oggetti) + 1, xref)
    percorso.parent.mkdir(exist_ok=True)
    percorso.write_bytes(bytes(out))


# ================================================================== dati
def prepara():
    pezzi, errori, avvisi = G.analizza()
    pezzi = sorted(pezzi, key=lambda p: G.GRUPPI.index(p.gruppo))     # stabile: ordine della distinta
    # giunti rame-rame: estremità passanti o in battuta, numerate nell'ordine di montaggio
    punti = []
    for p in pezzi:
        for e, t in ((p.a, p.tipo_a), (p.b, p.tipo_b)):
            if t in ("battuta", "passante") and e not in punti:
                punti.append(e)
    giunti = {pt: f"G{i + 1:02d}" for i, pt in enumerate(punti)}
    for n, p in enumerate(pezzi, 1):
        p.n = n                                       # numero d'ordine: etichetta nei disegni e riga della distinta
        p.giunti = [g for pt, g in giunti.items() if pt in (p.a, p.b) or G.sul_segmento(pt, p.a, p.b)]
    return pezzi, giunti, errori, avvisi


# ================================================================== viste 1:1
VISTE = {"alto": (0, 1, "Vista dall'alto (fronte in basso)"),
         "fronte": (0, 2, "Vista dal fronte"),
         "destra": (1, 2, "Vista da destra (fronte a sinistra)")}


def proietta(p, vista):
    i, j, _ = VISTE[vista]
    return p[i], p[j]


class Etichette:
    """Posiziona le etichette evitando (se può) di sovrapporle."""

    def __init__(self):
        self.occupate = []

    def libera(self, r):
        return all(r[0] + r[2] < o[0] or o[0] + o[2] < r[0] or r[1] + r[3] < o[1] or o[1] + o[3] < r[1]
                   for o in self.occupate)

    def metti(self, pag, candidati, testo, corpo, col):
        w, h = larghezza_testo(testo, corpo), corpo * 0.8
        scelta = None
        for (x, y) in candidati:
            r = (x - 0.3, y - 0.3, w + 0.6, h + 0.6)
            if self.libera(r):
                scelta = (x, y, r)
                break
        if scelta is None:
            x, y = candidati[0]
            scelta = (x, y, (x, y, w, h))
        self.occupate.append(scelta[2])
        x, y, _ = scelta
        pag.rett(x - 0.3, y - 0.4, w + 0.6, h + 0.7, sp=0, col=None, riemp=(1, 1, 1))
        pag.testo(x, y, testo, corpo, col=col, grassetto=True)


def ingombro_vista(gruppo, pezzi, vista):
    pts = [proietta(e, vista) for p in pezzi if p.gruppo == gruppo for e in (p.a, p.b)]
    if gruppo in G.MODULI:
        lo, hi = G.MODULI[gruppo].scatola()
        pts += [proietta(lo, vista), proietta(hi, vista)]
    if vista != "alto":
        pts.append((pts[0][0], 0.0))                      # sempre il piano della base
    u0 = min(p[0] for p in pts) - 10
    u1 = max(p[0] for p in pts) + 10
    v0 = min(p[1] for p in pts) - 10
    v1 = max(p[1] for p in pts) + 10
    arr = lambda a, f: 5 * f(a / 5)
    import math
    return arr(u0, math.floor), arr(v0, math.floor), arr(u1, math.ceil), arr(v1, math.ceil)


def disegna_vista(pag, ox, oy, gruppo, pezzi, giunti, vista, box):
    """Disegna la vista con l'angolo (u0, v0) del box nel punto (ox, oy) della pagina."""
    u0, v0, u1, v1 = box
    w, h = u1 - u0, v1 - v0
    P = lambda q: (ox + q[0] - u0, oy + q[1] - v0)
    idx = G.GRUPPI.index(gruppo)
    prima = [p for p in pezzi if G.GRUPPI.index(p.gruppo) < idx]
    questi = [p for p in pezzi if p.gruppo == gruppo]
    _, _, titolo = VISTE[vista]
    pag.testo(ox, oy + h + 2.5, titolo + "  ·  scala 1:1, quote in mm", 2.6, grassetto=True)

    # cornice con le tacche delle coordinate (ogni 5 mm, numeri ogni 10)
    pag.rett(ox, oy, w, h, sp=0.15, col=GRIGIO_SCURO)
    nomi_assi = "xyz"
    i, j, _ = VISTE[vista]
    for k in range(int(u0), int(u1) + 1, 5):
        x = ox + k - u0
        lung = 2.0 if k % 10 == 0 else 1.0
        pag.linea((x, oy), (x, oy + lung), 0.12)
        pag.linea((x, oy + h), (x, oy + h - lung), 0.12)
        if k % 10 == 0:
            pag.testo(x, oy - 2.6, str(k), 1.8, "c", GRIGIO_SCURO)
    for k in range(int(v0), int(v1) + 1, 5):
        y = oy + k - v0
        lung = 2.0 if k % 10 == 0 else 1.0
        pag.linea((ox, y), (ox + lung, y), 0.12)
        pag.linea((ox + w, y), (ox + w - lung, y), 0.12)
        if k % 10 == 0:
            pag.testo(ox - 0.8, y - 0.6, str(k), 1.8, "d", GRIGIO_SCURO)
    pag.testo(ox + w, oy - 5.2, f"{nomi_assi[i]} (mm)", 1.8, "d", GRIGIO_SCURO)
    pag.testo(ox - 0.8, oy + h + 0.4, f"{nomi_assi[j]}", 1.8, "d", GRIGIO_SCURO)

    pag.ritaglio(ox, oy, w, h)
    # base di legno (fronte/destra: piano z = 0; alto: contorno della base e della teca)
    if vista == "alto":
        lo, hi = G.BASE["min"], G.BASE["max"]
        a, b = P((lo[0], lo[1])), P((hi[0], hi[1]))
        pag.rett(a[0], a[1], b[0] - a[0], b[1] - a[1], 0.3, (0.55, 0.33, 0.17))
        t = G.TECA_BORDO
        a, b = P((lo[0] + t, lo[1] + t)), P((hi[0] - t, hi[1] - t))
        pag.rett(a[0], a[1], b[0] - a[0], b[1] - a[1], 0.15, (0.4, 0.6, 0.8), tratt=(1.5, 1))
    else:
        a, b = P((u0, 0)), P((u1, 0))
        pag.rett(a[0], a[1] - 3, b[0] - a[0], 3, 0, None, riemp=(0.93, 0.87, 0.78))
        pag.linea(a, b, 0.3, (0.55, 0.33, 0.17))

    # schede: già montate tratteggiate, quella del gruppo piena; pin usati con il nome
    for chiave, m in G.MODULI.items():
        if chiave not in G.GRUPPI or G.GRUPPI.index(chiave) > idx:
            continue
        lo, hi = m.scatola()
        a, b = P(proietta(lo, vista)), P(proietta(hi, vista))
        if chiave == gruppo:
            pag.rett(a[0], a[1], b[0] - a[0], b[1] - a[1], 0.25, (0.1, 0.3, 0.6), riemp=(0.88, 0.92, 0.98))
        else:
            pag.rett(a[0], a[1], b[0] - a[0], b[1] - a[1], 0.15, GRIGIO, tratt=(1, 1))
    if gruppo in G.MODULI:
        a = P(proietta(G.MODULI[gruppo].scatola()[0], vista))
        pag.testo(a[0] + 1, a[1] + 1, G.MODULI[gruppo].nome, 2.0, col=(0.1, 0.3, 0.6), grassetto=True)

    # pezzi già montati (grigi), poi i pezzi del gruppo (rame, larghi 1 mm come il filo)
    for p in prima:
        a, b = P(proietta(p.a, vista)), P(proietta(p.b, vista))
        if abs(a[0] - b[0]) < 1e-6 and abs(a[1] - b[1]) < 1e-6:
            pag.cerchio(a[0], a[1], 0.5, 0, None, riemp=GRIGIO)
        else:
            pag.linea(a, b, 1.0, GRIGIO)
    for p in questi:
        a, b = P(proietta(p.a, vista)), P(proietta(p.b, vista))
        if abs(a[0] - b[0]) < 1e-6 and abs(a[1] - b[1]) < 1e-6:
            pag.cerchio(a[0], a[1], 0.5, 0, None, riemp=RAME)
        else:
            pag.linea(a, b, 1.0, RAME)
            pag.linea(a, b, 0.1, (0.45, 0.2, 0.05))           # asse del filo

    # pin della scheda del gruppo, se la scheda è vista di faccia
    if gruppo in G.MODULI:
        m = G.MODULI[gruppo]
        if abs(m.n[3 - i - j]) > 0.5:                 # asse perpendicolare alla vista
            usati = {pn for r in G.RETI.values() for c, pn in r.pin if c == gruppo}
            for pn in m.pin_loc:
                q = P(proietta(m.pin(pn), vista))
                pag.cerchio(q[0], q[1], 0.45, 0.12, (0.1, 0.3, 0.6) if pn in usati else GRIGIO)
    pag.fine_ritaglio()

    # etichette: numero d'ordine del pezzo (legenda in testa alla pagina) e giunti
    et = Etichette()
    for p in questi:
        a, b = P(proietta(p.a, vista)), P(proietta(p.b, vista))
        corto = str(p.n)
        if abs(a[0] - b[0]) < 1e-6 and abs(a[1] - b[1]) < 1e-6:
            c = [(a[0] + 1.2, a[1] + 0.8), (a[0] + 1.2, a[1] - 2.2), (a[0] - 1.2 - larghezza_testo(corto, 2), a[1] + 0.8),
                 (a[0] - 1.2 - larghezza_testo(corto, 2), a[1] - 2.2)]
        else:
            c = []
            for t in (0.5, 0.3, 0.7, 0.15, 0.85):
                mx, my = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
                if abs(a[1] - b[1]) < 1e-6:          # orizzontale: sopra o sotto
                    c += [(mx - larghezza_testo(corto, 2) / 2, my + 1.0), (mx - larghezza_testo(corto, 2) / 2, my - 2.6)]
                else:                                # verticale: a destra o a sinistra
                    c += [(mx + 1.0, my - 0.7), (mx - 1.0 - larghezza_testo(corto, 2), my - 0.7)]
        et.metti(pag, c, corto, 2.0, (0.45, 0.2, 0.05))
    visti = set()
    for p in questi:
        for e in (p.a, p.b):
            g = giunti.get(e)
            if g and g not in visti:
                visti.add(g)
                q = P(proietta(e, vista))
                pag.cerchio(q[0], q[1], 0.9, 0.18, ROSSO)
                et.metti(pag, [(q[0] + 1.1, q[1] + 1.0), (q[0] + 1.1, q[1] - 2.3), (q[0] - 5.5, q[1] + 1.0),
                               (q[0] - 5.5, q[1] - 2.3)], g, 1.7, ROSSO)


# ================================================================== pagine
def piede(pag, n, tot, bozza):
    pag.testo(MARGINE, 5.5, f"Metronomus · piano del rame 1:1 · {date.today().strftime('%d/%m/%Y')}"
              + ("  ·  BOZZA" if bozza else ""), 2.2, col=GRIGIO_SCURO)
    pag.testo(pag.w - MARGINE, 5.5, f"pagina {n} di {tot}", 2.2, "d", GRIGIO_SCURO)
    # barretta di controllo da 50 mm su ogni pagina
    x0 = pag.w / 2 - 25
    pag.linea((x0, 6.3), (x0 + 50, 6.3), 0.2)
    for k in (0, 10, 20, 30, 40, 50):
        pag.linea((x0 + k, 5.3), (x0 + k, 7.3), 0.15)
    pag.testo(x0 + 25, 3.0, "controllo: 50 mm", 1.8, "c", GRIGIO_SCURO)
    if bozza:
        pag.testo(pag.w / 2, pag.h - 6, "BOZZA: misure stimate o errori nei controlli, non tagliare", 3.0, "c", ROSSO, True)


def copertina(pezzi, giunti, avvisi, errori):
    pag = Pagina(*A4)
    y = A4[1] - 25
    pag.testo(MARGINE, y, "Metronomus · piano del circuito in rame", 7, grassetto=True)
    y -= 8
    pag.testo(MARGINE, y, "Filo di rame Ø 1,0 mm, solo pezzi dritti saldati ad angolo retto. Scala 1:1.", 3.2)
    y -= 14
    pag.testo(MARGINE, y, "1. Prima di tutto: controlla la stampa", 4, grassetto=True)
    y -= 6
    pag.testo(MARGINE, y, "Stampa al 100 % (\"dimensioni effettive\", NON \"adatta alla pagina\"). Il righello deve misurare 100 mm.", 3)
    y -= 12
    pag.linea((MARGINE, y), (MARGINE + 100, y), 0.3)
    for k in range(0, 101):
        lung = 5 if k % 10 == 0 else (3.5 if k % 5 == 0 else 2)
        pag.linea((MARGINE + k, y), (MARGINE + k, y + lung), 0.12 if k % 10 else 0.25)
        if k % 10 == 0:
            pag.testo(MARGINE + k, y + 6, str(k), 2.4, "c")
    pag.testo(MARGINE + 104, y + 1, "mm", 2.6)
    pag.rett(A4[0] - MARGINE - 50, 16, 50, 50, 0.25)
    pag.testo(A4[0] - MARGINE - 25, 40, "50 x 50 mm", 3, "c")
    y -= 22
    pag.testo(MARGINE, y, "2. Riepilogo", 4, grassetto=True)
    y -= 6
    righe = [
        f"{len(pezzi)} pezzi, {sum(p.taglio for p in pezzi) / 1000:.2f} m di filo (più il 10 % di scorta), "
        f"pezzo più corto {min(p.taglio for p in pezzi):.1f} mm, {len(giunti)} giunti rame-rame.",
        "Ordine di montaggio: " + ", ".join(f"{k + 1}. {G.NOMI_GRUPPI[g]}" for k, g in enumerate(G.GRUPPI)) + ".",
        "Assi: x verso destra, y verso il retro, z verso l'alto. Origine: x = 0 sull'asse del motore, z = 0 sul legno.",
    ]
    for r in righe:
        for pezzo in spezza(r, 100):
            pag.testo(MARGINE, y, pezzo, 3)
            y -= 4.8
    y -= 6
    pag.testo(MARGINE, y, "3. Estremità dei pezzi (la lunghezza di taglio ne tiene già conto)", 4, grassetto=True)
    y -= 6
    leg = [("battuta", "la testa appoggia sul fianco di un altro filo: taglio = interasse - 0,5 mm"),
           ("passante", "arriva fino al bordo esterno del giunto d'angolo: + 0,5 mm"),
           ("pin", f"attraversa il foro della scheda e sporge dall'altra parte per la saldatura: + {G.INFILATA_PIN:.1f} mm"),
           ("base", f"struttura: foro cieco, + {G.INFILATA_BASE:.0f} mm; elettrici: attraversa la base e sporge nella canalina, + {-G.Z_CANALINE:.0f} mm"),
           ("testa", "estremità libera del bus, oltre l'ultima discesa (gioco di montaggio)"),
           ("libero", "qui si salda il filo flessibile verso il pendolo")]
    for nome, d in leg:
        pag.testo(MARGINE + 2, y, nome, 3, grassetto=True)
        pag.testo(MARGINE + 22, y, d, 3)
        y -= 4.8
    y -= 6
    pag.testo(MARGINE, y, "4. Come si usa", 4, grassetto=True)
    y -= 6
    passi = [
        "Fora la base con la dima (pagina 2), punta da 1,1-1,2 mm, fori dritti e perpendicolari: passanti quelli elettrici, ciechi da 6 mm quelli della struttura. Sotto: scassi per TP4056, vibrazione ed encoder e canaline da 4 mm per i cavetti.",
        "Taglia i pezzi di un gruppo alla volta appoggiando il filo sul disegno 1:1 della distinta di taglio.",
        "Fissa la vista 1:1 del gruppo su sughero con spilli e squadrette; salda i giunti (cerchi rossi G..) "
        "nell'ordine della distinta. In grigio i pezzi già montati, in rame quelli del gruppo.",
        "Prima l'alimentazione, poi una scheda alla volta: prova ogni gruppo col tester prima del successivo.",
    ]
    for k, s in enumerate(passi, 1):
        for i, pezzo in enumerate(spezza(s, 98)):
            pag.testo(MARGINE + (0 if i == 0 else 4), y, (f"{k}. " if i == 0 else "") + pezzo, 3)
            y -= 4.8
    if avvisi or errori:
        y -= 6
        pag.testo(MARGINE, y, "Attenzione", 4, col=ROSSO, grassetto=True)
        y -= 6
        for a in list(errori) + list(avvisi):
            pag.testo(MARGINE, y, a, 3, col=ROSSO)
            y -= 4.8
    return pag


def spezza(s, n):
    parole, righe, r = s.split(), [], ""
    for p in parole:
        if len(r) + len(p) + 1 > n:
            righe.append(r)
            r = p
        else:
            r = (r + " " + p).strip()
    return righe + [r]


def dima_base():
    pag = Pagina(*A4)
    lo, hi = G.BASE["min"], G.BASE["max"]
    fori = []
    for nome, r in G.RETI.items():
        for f in r.fori:
            f = G.tonda(f)
            if (f[0], f[1]) not in [(q[1], q[2]) for q in fori]:
                fori.append((nome, f[0], f[1]))
    fori.sort(key=lambda q: (-q[2], q[1]))
    ox, oy = (A4[0] - (hi[0] - lo[0])) / 2, A4[1] - 40 - (hi[1] - lo[1])
    P = lambda x, y: (ox + x - lo[0], oy + y - lo[1])
    pag.testo(MARGINE, A4[1] - 18, "Dima di foratura della base (vista dall'alto, 1:1)", 5, grassetto=True)
    pag.testo(MARGINE, A4[1] - 25, f"Ritaglia sul bordo, appoggiala sulla base {hi[0] - lo[0]:.0f} x {hi[1] - lo[1]:.0f} mm "
              "col FRONTE in basso, fissala e fora al centro delle croci.", 3)
    a, b = P(lo[0], lo[1]), P(hi[0], hi[1])
    pag.rett(a[0], a[1], b[0] - a[0], b[1] - a[1], 0.35, (0.55, 0.33, 0.17))
    t = G.TECA_BORDO
    a2, b2 = P(lo[0] + t, lo[1] + t), P(hi[0] - t, hi[1] - t)
    pag.rett(a2[0], a2[1], b2[0] - a2[0], b2[1] - a2[1], 0.15, (0.4, 0.6, 0.8), tratt=(1.5, 1))
    pag.testo((a[0] + b[0]) / 2, a[1] - 4, "FRONTE", 3, "c", grassetto=True)
    pag.testo(a2[0] + 1, b2[1] - 3, "interno della teca", 2, col=(0.4, 0.6, 0.8))
    c = P(0, 0)
    pag.linea((c[0], a[1]), (c[0], a[1] + 3), 0.2)
    pag.linea((c[0], b[1]), (c[0], b[1] - 3), 0.2)
    pag.testo(c[0], b[1] + 1.5, "x = 0 (asse del motore)", 2, "c", GRIGIO_SCURO)
    et = Etichette()
    for k, (nome, x, y) in enumerate(fori, 1):
        q = P(x, y)
        pag.linea((q[0] - 2, q[1]), (q[0] + 2, q[1]), 0.12)
        pag.linea((q[0], q[1] - 2), (q[0], q[1] + 2), 0.12)
        pag.cerchio(q[0], q[1], 0.6, 0.15, ROSSO)
        et.metti(pag, [(q[0] + 1.3, q[1] + 0.6), (q[0] + 1.3, q[1] - 2.2), (q[0] - 4.5, q[1] + 0.6), (q[0] - 4.5, q[1] - 2.2)],
                 f"F{k}", 1.8, ROSSO)
    # tabella
    y = oy - 14
    pag.testo(MARGINE, y, "Fori (coordinate dal centro: x dall'asse del motore, y dal fronte della base)", 3.2, grassetto=True)
    y -= 6
    col = [MARGINE, MARGINE + 10, MARGINE + 33, MARGINE + 47, MARGINE + 68]
    for blocco in range(2):
        for i, t2 in enumerate(("foro", "rete", "x", "y dal fronte", "tipo")):
            pag.testo(col[i] + blocco * 95, y, t2, 2.6, grassetto=True)
    y -= 4.5
    meta = (len(fori) + 1) // 2
    for k, (nome, x, yy) in enumerate(fori):
        blocco, riga = divmod(k, meta)
        yr = y - riga * 4.2
        dx = blocco * 95
        pag.testo(col[0] + dx, yr, f"F{k + 1}", 2.6)
        pag.testo(col[1] + dx, yr, nome, 2.6)
        pag.testo(col[2] + dx, yr, f"{x:+.1f}".replace(".", ","), 2.6)
        pag.testo(col[3] + dx, yr, f"{yy - lo[1]:.1f}".replace(".", ","), 2.6)
        pag.testo(col[4] + dx, yr, "cieco 6 mm" if nome in G.RETI_ANCORATE else "passante", 2.6,
                  grassetto=nome not in G.RETI_ANCORATE)
    return pag


def pagine_gruppi(pezzi, giunti):
    """Viste 1:1 di ogni gruppo, impilate su pagine A4 verticali (orizzontali se una vista è troppo larga)."""
    pagine = []
    for k, g in enumerate(G.GRUPPI, 1):
        sel = [p for p in pezzi if p.gruppo == g]
        if not sel:
            continue
        viste = [(v, ingombro_vista(g, pezzi, v)) for v in ("alto", "fronte", "destra")]
        titolo = f"Gruppo {k} · {G.NOMI_GRUPPI[g]} · {len(sel)} pezzi, " + f"{sum(p.taglio for p in sel) / 10:.1f}".replace(".", ",") + " cm"
        pag, y = None, 0
        for v, box in viste:
            w, h = box[2] - box[0], box[3] - box[1]
            largo = w > A4[0] - 2 * MARGINE - 8
            dim = (A4[1], A4[0]) if largo else A4
            serve = h + 14
            if pag is None or largo or pag.w != dim[0] or y - serve < 14:
                pag = Pagina(*dim)
                pagine.append(pag)
                pag.testo(MARGINE, dim[1] - 14, titolo, 3.6, grassetto=True)
                # legenda: numero nei disegni -> codice, taglio, giunti
                colonne = int((dim[0] - 2 * MARGINE) // 62)
                righe = -(-len(sel) // colonne)
                for i, p in enumerate(sel):
                    c, r = divmod(i, righe)
                    x, yy = MARGINE + c * 62, dim[1] - 21 - r * 3.6
                    pag.testo(x, yy, str(p.n), 2.4, "s", (0.45, 0.2, 0.05), True)
                    pag.testo(x + 6, yy, f"{p.codice}  {p.taglio:.1f}".replace(".", ",") + " mm", 2.4)
                    pag.testo(x + 40, yy, " ".join(p.giunti), 2.0, col=ROSSO)
                y = dim[1] - 21 - righe * 3.6
            ox = MARGINE + 8
            disegna_vista(pag, ox, y - 6 - h, g, pezzi, giunti, v, box)
            y -= serve
    return pagine


def pagine_distinta(pezzi, giunti):
    """Distinta di taglio, A4 orizzontale: una riga per pezzo con il pezzo disegnato 1:1."""
    W, H = A4[1], A4[0]
    pagine = []
    col = [MARGINE, MARGINE + 9, MARGINE + 31, MARGINE + 53, MARGINE + 69, MARGINE + 86, MARGINE + 103]
    x_barra = MARGINE + 140
    pag, y = None, 0

    def nuova():
        p = Pagina(W, H)
        pagine.append(p)
        p.testo(MARGINE, H - 14, "Distinta di taglio, in ordine di saldatura (pezzi disegnati 1:1: appoggia il filo e taglia)",
                3.6, grassetto=True)
        for i, t in enumerate(("n.", "codice", "rete", "taglio", "estremo A", "estremo B", "giunti")):
            p.testo(col[i], H - 21, t, 2.6, grassetto=True)
        p.testo(x_barra, H - 21, "pezzo in scala 1:1 (da A a B)", 2.6, grassetto=True)
        p.linea((MARGINE, H - 22.5), (W - MARGINE, H - 22.5), 0.2)
        return p, H - 28

    gruppo = None
    for n, p in enumerate(pezzi, 1):
        lungo = x_barra + p.taglio > W - MARGINE
        serve = 7.5 + (5 if lungo else 0) + (7 if p.gruppo != gruppo else 0)
        if pag is None or y - serve < 14:
            pag, y = nuova()
            gruppo = None
        if p.gruppo != gruppo:
            gruppo = p.gruppo
            pag.rett(MARGINE, y - 1.6, W - 2 * MARGINE, 5.2, 0, None, riemp=(0.93, 0.93, 0.93))
            pag.testo(MARGINE + 1, y, f"Gruppo {G.GRUPPI.index(gruppo) + 1} · {G.NOMI_GRUPPI[gruppo]}", 3, grassetto=True)
            y -= 7
        pag.testo(col[0], y, str(n), 2.8)
        pag.testo(col[1], y, p.codice, 2.8, grassetto=True)
        pag.testo(col[2], y, p.rete, 2.8)
        pag.testo(col[3], y, f"{p.taglio:.1f}".replace(".", ",") + " mm", 2.8, grassetto=True)
        pag.testo(col[4], y, NOMI_ESTREMI[p.tipo_a], 2.8)
        pag.testo(col[5], y, NOMI_ESTREMI[p.tipo_b], 2.8)
        pag.testo(col[6], y, " ".join(p.giunti) or "-", 2.4, col=ROSSO)
        # barra 1:1, larga 1 mm come il filo
        xb, yb = (x_barra, y + 0.9) if not lungo else (MARGINE + 9, y - 4.1)
        pag.rett(xb, yb - 0.5, p.taglio, 1.0, 0, None, riemp=RAME)
        for x in (xb, xb + p.taglio):
            pag.linea((x, yb - 1.6), (x, yb + 1.6), 0.15)
        pag.testo(xb - 2.4, yb - 0.8, "A", 2, col=GRIGIO_SCURO)
        pag.testo(xb + p.taglio + 0.8, yb - 0.8, "B", 2, col=GRIGIO_SCURO)
        y -= 7.5 + (5 if lungo else 0)
        pag.linea((MARGINE, y + 3.6), (W - MARGINE, y + 3.6), 0.05, GRIGIO)
    return pagine


def pagina_millefori():
    """Scheda servizi: lato componenti e lato saldature (specchiato) in scala 4:1, sagoma 1:1, elenco componenti."""
    import millefori as MF
    S, P = 4.0, 2.54
    k0, k1, r0, r1 = min(MF.COLONNE), max(MF.COLONNE), min(MF.RIGHE), max(MF.RIGHE)
    nk, nr = k1 - k0 + 1, r1 - r0 + 1
    W, H = nk * P * S, nr * P * S
    pag = Pagina(*A4)
    pag.testo(MARGINE, A4[1] - 16, "Scheda servizi su millefori (passo 2,54)", 5, grassetto=True)
    pag.testo(MARGINE, A4[1] - 22.5, f"Taglia una millefori di {nk} x {nr} fori a metà tra i fori ({nk * P:.1f} x {nr * P:.1f} mm). "
              "Fronte in basso. Disegni in scala 4:1.", 3)
    rame_k = {k: n for n, k in MF.USCITE.items()}
    BLU, GRIGIO_L = (0.1, 0.25, 0.6), (0.45, 0.45, 0.45)

    def vista(oy, specchio, titolo):
        ox = (A4[0] - W) / 2
        def F(k, r):
            kk = (k1 - k + k0) if specchio else k
            return ox + (kk - k0 + 0.5) * P * S, oy + (r - r0 + 0.5) * P * S
        pag.testo(ox, oy + H + 2.5, titolo, 3, grassetto=True)
        pag.rett(ox, oy, W, H, 0.3, (0.55, 0.4, 0.2), riemp=(0.97, 0.93, 0.85))
        for k in MF.COLONNE:
            for r in MF.RIGHE:
                x, y = F(k, r)
                if r == 0 and k in rame_k:
                    pag.cerchio(x, y, 1.6, 0.3, RAME, riemp=(1.0, 0.85, 0.7))
                else:
                    pag.cerchio(x, y, 0.9, 0.15, GRIGIO_L)
        # nomi del rame sotto la scheda, colonna per colonna
        for k, n in rame_k.items():
            x, _ = F(k, 0)
            pag.testo(x, oy - 3.5 - (2.6 if k % 2 else 0), n, 1.9, "c", (0.5, 0.25, 0.05), True)
        # collegamenti sul lato saldature
        for perc in MF.COLLEGAMENTI:
            for a, b in zip(perc, perc[1:]):
                pag.linea(F(*a), F(*b), 1.4 if specchio else 0.5, (0.55, 0.55, 0.6) if specchio else (0.75, 0.75, 0.8),
                          tratt=None if specchio else (1.2, 0.8))
        if specchio:
            for sigla, (_, _, piedini) in MF.COMPONENTI.items():
                for pd, f in piedini.items():
                    x, y = F(*f)
                    pag.testo(x + 1.2, y + 1.0, f"{sigla}.{pd}", 1.6, col=BLU)
            return
        # componenti
        for sigla, (tipo, _, piedini) in MF.COMPONENTI.items():
            pts = [F(*f) for f in piedini.values()]
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
            if tipo in ("TO-92", "SOT-23"):
                pag.rett(min(xs) - 3.5, min(ys) - 3.2, max(xs) - min(xs) + 7, max(ys) - min(ys) + 6.4, 0.35, BLU)
                for pd, f in piedini.items():
                    x, y = F(*f)
                    pag.testo(x, y - 2.9, pd, 1.6, "c", BLU, True)
                pag.testo(cx, max(ys) + 3.8, sigla, 2.4, "c", BLU, True)
            elif tipo == "R sdraiata":
                pag.linea(pts[0], pts[1], 0.35, BLU)
                lx, ly = abs(pts[1][0] - pts[0][0]), abs(pts[1][1] - pts[0][1])
                if lx >= ly:
                    pag.rett(cx - lx * 0.3, cy - 2.2, lx * 0.6, 4.4, 0.35, BLU, riemp=(0.85, 0.9, 1.0))
                else:
                    pag.rett(cx - 2.2, cy - ly * 0.3, 4.4, ly * 0.6, 0.35, BLU, riemp=(0.85, 0.9, 1.0))
                pag.testo(cx, cy - 0.8, sigla, 2.2, "c", BLU, True)
            elif tipo == "R in piedi":
                pag.linea(pts[0], pts[1], 0.35, BLU)
                pag.cerchio(pts[0][0], pts[0][1], 2.6, 0.35, BLU, riemp=(0.85, 0.9, 1.0))
                pag.testo(pts[0][0], pts[0][1] - 0.8, sigla, 1.9, "c", BLU, True)
            else:                                        # condensatore
                pag.linea(pts[0], pts[1], 0.35, BLU)
                horiz = abs(pts[1][0] - pts[0][0]) > abs(pts[1][1] - pts[0][1])
                pag.rett(cx - (3 if horiz else 2), cy - (2 if horiz else 3), 6 if horiz else 4, 4 if horiz else 6, 0.35, BLU,
                         riemp=(1.0, 0.95, 0.8))
                pag.testo(cx, cy - 0.8, sigla, 1.9, "c", BLU, True)
        for nome, (a, b) in MF.PONTICELLI.items():
            pa, pb = F(*a), F(*b)
            pag.linea(pa, pb, 0.6, (0.1, 0.55, 0.2))
            pag.testo((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2 + 1, nome, 2.2, "c", (0.1, 0.55, 0.2), True)

    y1 = A4[1] - 36 - H
    vista(y1, False, "Lato componenti (sopra). Tratteggio grigio: collegamenti sotto. Verde: ponticelli isolati sopra.")
    y2 = y1 - 20 - H
    vista(y2, True, "Lato saldature (sotto, SPECCHIATO): fili nudi o ponti di stagno tra i fori")
    # sagoma 1:1 ed elenco
    y3 = y2 - 16
    pag.testo(MARGINE, y3, "Sagoma 1:1", 3, grassetto=True)
    pag.rett(MARGINE, y3 - 4 - nr * P, nk * P, nr * P, 0.25)
    for k in MF.COLONNE:
        for r in MF.RIGHE:
            pag.cerchio(MARGINE + (k - k0 + 0.5) * P, y3 - 4 - nr * P + (r - r0 + 0.5) * P, 0.4, 0.1, GRIGIO_L)
    x, y = MARGINE + 55, y3
    pag.testo(x, y, "Componenti", 3, grassetto=True)
    for sigla, (tipo, val, _) in MF.COMPONENTI.items():
        y -= 3.8
        pag.testo(x, y, sigla, 2.4, grassetto=True)
        pag.testo(x + 9, y, val, 2.4)
    y -= 5
    pag.testo(x, y, "Il rame entra dal basso nei fori marrone (fila dei pin) e sporge di 2,5 mm sopra.", 2.4)
    pag.testo(x, y - 3.8, "SOT-23 su adattatore (G-S-D); 2N3904 TO-92: E-B-C guardando il lato piatto. Controllo: python fili/millefori.py", 2.4)
    return pag


def pagina_giunti(pezzi, giunti):
    pag = Pagina(*A4)
    pag.testo(MARGINE, A4[1] - 18, "Giunti rame-rame (in ordine di saldatura)", 5, grassetto=True)
    pag.testo(MARGINE, A4[1] - 25, "Per ogni giunto: i pezzi che si toccano; il primo è quello già montato.", 3)
    y = A4[1] - 34
    x = MARGINE
    for pt, g in giunti.items():
        chi = [p.codice for p in pezzi if g in p.giunti]
        s = f"{g}: " + ", ".join(chi)
        pag.testo(x, y, s, 2.6)
        y -= 4.0
        if y < 16:
            y, x = A4[1] - 34, x + 64
    return pag


def main():
    bozza = "--bozza" in sys.argv
    pezzi, giunti, errori, avvisi = prepara()
    if (errori or avvisi) and not bozza:
        for e in errori + avvisi:
            print("ERRORE:" if e in errori else "AVVISO:", e)
        print("PDF non generato: correggi la geometria o le misure (oppure usa --bozza).")
        sys.exit(1)
    pagine = [copertina(pezzi, giunti, avvisi, errori), dima_base()]
    pagine += pagine_gruppi(pezzi, giunti)
    pagine.append(pagina_millefori())
    pagine.append(pagina_giunti(pezzi, giunti))
    pagine += pagine_distinta(pezzi, giunti)
    for n, p in enumerate(pagine, 1):
        piede(p, n, len(pagine), bozza and bool(errori or avvisi))
    out = G.RADICE / "produzione" / "piano-rame.pdf"
    scrivi_pdf(pagine, out)
    print(f"{out.relative_to(G.RADICE)}: {len(pagine)} pagine, {len(pezzi)} pezzi, {len(giunti)} giunti")


if __name__ == "__main__":
    main()
