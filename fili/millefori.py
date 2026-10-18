"""Scheda servizi su millefori (passo 2,54): disposizione dei componenti, collegamenti e controllo delle reti.

Uso:  python fili/millefori.py      -> controlla che i collegamenti realizzino esattamente le reti dello schema

Griglia: colonna k (x = gx(k), la stessa griglia dei pin dell'ESP32) e riga r (r = 0 è la fila dei pin di
uscita, dove arriva il rame; r > 0 verso il retro, r < 0 verso il fronte). Vista dal lato componenti, fronte in basso.
  - COLLEGAMENTI: sul lato saldature, filo nudo (o ponte di stagno) che passa per i fori elencati, in fila o in colonna;
  - PONTICELLI: sul lato componenti, filo isolato tra due fori (anche in diagonale).
La pagina del PDF la disegna fili/piano_pdf.py.
"""
import sys

RIGHE = range(-3, 3)          # da -3 (fronte) a +2 (retro)
COLONNE = range(0, 17)

# fila dei pin di uscita (r = 0): qui entra il rame dal basso
USCITE = {"3V3": 2, "PWR_EN": 5, "LED_PWM": 6, "ADC": 7, "LED_K": 9, "LED_A": 10, "VBAT": 11, "GND": 12,
          "V12": 14, "VSW": 15, "VSW_VIB": 16}

# componenti: sigla -> (tipo, valore, {piedino: (k, r)})
COMPONENTI = {
    "U1": ("TO-92", "MCP1700-3302E (LDO 3,3 V), lato piatto verso il fronte", {"GND": (1, 1), "IN": (2, 1), "OUT": (3, 1)}),
    "C2": ("C", "1 µF ceramico (ingresso LDO)", {"+": (0, 2), "-": (0, 1)}),
    "C3": ("C", "1 µF ceramico (uscita LDO)", {"+": (3, 0), "-": (3, -1)}),
    "Q3": ("TO-92", "2N3904 NPN (comando del letargo), in colonna, lato piatto verso destra, E sul fronte",
           {"E": (4, -3), "B": (4, -2), "C": (4, -1)}),
    "R3": ("R in piedi", "10 kΩ (base di Q3)", {"1": (5, -1), "2": (5, -2)}),
    "R4": ("R in piedi", "100 kΩ", {"1": (3, -2), "2": (3, -3)}),
    "Q2": ("SOT-23", "AO3401 su adattatore SOT-23 (interruttore del letargo)", {"G": (13, 1), "S": (14, 1), "D": (15, 1)}),
    "R8": ("R in piedi", "100 kΩ", {"1": (12, 1), "2": (12, 2)}),
    "Q1": ("TO-92", "2N3904 NPN (LED), in colonna, lato piatto verso destra, E sul fronte",
           {"E": (8, -3), "B": (8, -2), "C": (8, -1)}),
    "R5": ("R in piedi", "470 Ω (base di Q1)", {"1": (6, -1), "2": (7, -1)}),
    "R10": ("R in piedi", "100 kΩ", {"1": (6, -2), "2": (6, -3)}),
    "R6": ("R sdraiata", "resistenza dei filamenti (valore dopo la misura della Vf)", {"1": (10, -1), "2": (14, -1)}),
    "R1": ("R in piedi", "100 kΩ (partitore della batteria)", {"1": (16, -1), "2": (16, -2)}),
    "R2": ("R in piedi", "100 kΩ (partitore della batteria)", {"1": (15, -2), "2": (15, -3)}),
    "C1": ("C", "100 nF (filtro dell'ADC)", {"1": (14, -2), "2": (14, -3)}),
}

# lato saldature: percorsi di filo nudo (ogni foro attraversato è collegato)
COLLEGAMENTI = [
    [(0, 2), (14, 2)],                      # linea VBAT (retro)
    [(0, -3), (16, -3)],                    # linea GND (fronte)
    [(2, 1), (2, 2)],                       # U1 IN -> VBAT
    [(1, 1), (1, -3)],                      # U1 GND -> GND
    [(3, 1), (3, 0), (2, 0)],               # U1 OUT -> pin 3V3
    [(0, 1), (1, 1)],                       # C2 -> GND
    [(3, -1), (2, -1), (2, -3)],            # C3 -> GND
    [(5, 0), (5, -1)],                      # pin PWR_EN -> R3
    [(3, -2), (4, -2), (5, -2)],            # R4 e R3 -> base di Q3 (emettitore già sulla linea GND)
    [(4, -1), (4, 0)],                      # collettore di Q3 -> ponticello J1
    [(13, 0), (13, 1)],                     # ponticello J1 -> gate di Q2
    [(12, 1), (13, 1)],                     # R8 -> gate di Q2
    [(14, 1), (14, 2)],                     # Q2 S -> VBAT
    [(15, 1), (15, 0), (16, 0), (16, -1)],  # Q2 D -> pin VSW, VSW_VIB e R1
    [(11, 0), (11, 2)],                     # pin VBAT -> linea VBAT
    [(12, 0), (12, -3)],                    # pin GND -> linea GND
    [(8, -1), (9, -1), (9, 0)],             # collettore di Q1 -> pin LED_K (emettitore già sulla linea GND)
    [(6, 0), (6, -1)],                      # pin LED_PWM -> R5
    [(7, -1), (7, -2), (8, -2)],            # R5 -> base di Q1
    [(6, -2), (7, -2)],                     # R10 -> base di Q1
    [(10, 0), (10, -1)],                    # pin LED_A -> R6
    [(14, 0), (14, -1)],                    # pin V12 -> R6
    [(16, -2), (14, -2)],                   # nodo del partitore: R1, R2, C1
    [(13, -2), (14, -2)],                   # nodo del partitore -> ponticello J2
    [(7, 1), (7, 0)],                       # ponticello J2 -> pin ADC
]

# lato componenti: fili isolati
PONTICELLI = {"J1": ((4, 0), (13, 0)),      # gate di Q2 (collettore di Q3)
              "J2": ((13, -2), (7, 1))}     # partitore -> ADC

# reti attese: (componente, piedino) e pin di uscita
RETI = {
    "GND": [("U1", "GND"), ("C2", "-"), ("C3", "-"), ("Q3", "E"), ("R4", "2"), ("R10", "2"), ("Q1", "E"),
            ("R2", "2"), ("C1", "2"), "GND"],
    "VBAT": [("U1", "IN"), ("C2", "+"), ("R8", "2"), ("Q2", "S"), "VBAT"],
    "3V3": [("U1", "OUT"), ("C3", "+"), "3V3"],
    "PWR_EN": [("R3", "1"), "PWR_EN"],
    "Q3_BASE": [("R3", "2"), ("Q3", "B"), ("R4", "1")],
    "Q2_GATE": [("Q3", "C"), ("Q2", "G"), ("R8", "1")],
    "VSW": [("Q2", "D"), ("R1", "1"), "VSW", "VSW_VIB"],
    "VBAT_ADC": [("R1", "2"), ("R2", "1"), ("C1", "1"), "ADC"],
    "LED_PWM": [("R5", "1"), "LED_PWM"],
    "Q1_BASE": [("R5", "2"), ("Q1", "B"), ("R10", "1")],
    "LED_K": [("Q1", "C"), "LED_K"],
    "LED_A": [("R6", "1"), "LED_A"],
    "V12": [("R6", "2"), "V12"],
}


def fori_del_percorso(percorso):
    fori = []
    for (k0, r0), (k1, r1) in zip(percorso, percorso[1:]):
        if k0 != k1 and r0 != r1:
            raise ValueError(f"collegamento non in fila o in colonna: {(k0, r0)} -> {(k1, r1)}")
        n = max(abs(k1 - k0), abs(r1 - r0))
        dk, dr = (k1 - k0) // n if n else 0, (r1 - r0) // n if n else 0
        fori += [(k0 + i * dk, r0 + i * dr) for i in range(n + 1)]
    return fori


def controlla():
    """Ritorna la lista dei problemi (vuota se le reti tornano)."""
    problemi = []
    padre = {}
    def radice(f):
        padre.setdefault(f, f)
        while padre[f] != f:
            f = padre[f]
        return f
    def unisci(a, b):
        padre[radice(a)] = radice(b)
    for p in COLLEGAMENTI:
        fori = fori_del_percorso(p)
        for f in fori:
            if f[0] not in COLONNE or f[1] not in RIGHE:
                problemi.append(f"foro fuori dalla scheda: {f}")
        for a, b in zip(fori, fori[1:]):
            unisci(a, b)
    for a, b in PONTICELLI.values():
        unisci(a, b)
    # un solo piedino per foro; niente piedini sui fori del rame
    occupati = {}
    for sigla, (_, _, piedini) in COMPONENTI.items():
        for pd, f in piedini.items():
            if f in occupati:
                problemi.append(f"{sigla}.{pd} e {occupati[f]} nello stesso foro {f}")
            occupati[f] = f"{sigla}.{pd}"
    for nome, k in USCITE.items():
        if (k, 0) in occupati:
            problemi.append(f"il foro del pin {nome} è occupato da {occupati[(k, 0)]}")
    # ogni rete tutta collegata, reti diverse separate
    def foro(x):
        return (USCITE[x], 0) if isinstance(x, str) else COMPONENTI[x[0]][2][x[1]]
    radici = {}
    for nome, membri in RETI.items():
        rr = {radice(foro(m)) for m in membri}
        if len(rr) > 1:
            problemi.append(f"rete {nome} spezzata: " + ", ".join(m if isinstance(m, str) else ".".join(m) for m in membri))
        for r in rr:
            if r in radici and radici[r] != nome:
                problemi.append(f"CORTO tra {nome} e {radici[r]}")
            radici[r] = nome
    # tutti i piedini dei componenti stanno in una rete
    in_rete = {m for membri in RETI.values() for m in membri if not isinstance(m, str)}
    for sigla, (_, _, piedini) in COMPONENTI.items():
        for pd in piedini:
            if (sigla, pd) not in in_rete:
                problemi.append(f"{sigla}.{pd} non è in nessuna rete")
    return problemi


if __name__ == "__main__":
    pr = controlla()
    for p in pr:
        print("PROBLEMA:", p)
    print("millefori: " + ("reti corrette, nessun corto" if not pr else f"{len(pr)} problemi"))
    sys.exit(1 if pr else 0)
