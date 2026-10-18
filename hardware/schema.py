"""Schema elettrico di Metronomus (schema a moduli con etichette di rete).

Genera hardware/schema.svg, e anche schema.pdf / schema.png se cairosvg è installato.
Uso: python hardware/schema.py
I nomi delle reti sono gli stessi di hardware/pinout.md e del piano fili:
due piedini con la stessa etichetta sono collegati tra loro.
"""
from pathlib import Path

QUI = Path(__file__).parent
W, H = 1680, 1290  # circa A3 orizzontale

ROSSO, BLU, NERO, GRIGIO = "#b3261e", "#1f4e9c", "#222222", "#6b6b6b"
POTENZA = {"V12", "VSW", "3V3", "3V3_SW", "VBAT"}
el = []


def linea(x1, y1, x2, y2, c=NERO, w=2):
    el.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>')


def poli(punti, c=NERO, w=2, fill="none"):
    p = " ".join(f"{x},{y}" for x, y in punti)
    el.append(f'<polyline points="{p}" stroke="{c}" stroke-width="{w}" fill="{fill}" stroke-linejoin="round"/>')


def testo(x, y, t, c=NERO, s=14, a="start", peso="normal"):
    for i, riga in enumerate(t.split("\n")):
        el.append(f'<text x="{x}" y="{y + i * (s + 3)}" fill="{c}" font-size="{s}" text-anchor="{a}" '
                  f'font-weight="{peso}" font-family="Helvetica, Arial, sans-serif">{riga}</text>')


def punto(x, y, c=NERO):
    el.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{c}"/>')


def massa(x, y):
    """Simbolo di massa con il terminale in (x, y)."""
    linea(x, y, x, y + 12)
    for i, l in enumerate((14, 9, 4)):
        linea(x - l, y + 12 + i * 5, x + l, y + 12 + i * 5)


def resistenza(x, y, l=60, verticale=True, c=NERO):
    n, a = 6, 7
    if verticale:
        pts = [(x, y), (x, y + 10)] + [(x + (a if i % 2 == 0 else -a), y + 10 + (l - 20) * (i + 0.5) / n) for i in range(n)] + [(x, y + l - 10), (x, y + l)]
    else:
        pts = [(x, y), (x + 10, y)] + [(x + 10 + (l - 20) * (i + 0.5) / n, y + (a if i % 2 == 0 else -a)) for i in range(n)] + [(x + l - 10, y), (x + l, y)]
    poli(pts, c)


def condensatore(x, y, l=50):
    m = y + l / 2
    linea(x, y, x, m - 4)
    linea(x - 12, m - 4, x + 12, m - 4, w=3)
    linea(x - 12, m + 4, x + 12, m + 4, w=3)
    linea(x, m + 4, x, y + l)


def batteria(x, y, l=60, c=ROSSO):
    """Cella verticale, + in alto."""
    m = y + l / 2
    linea(x, y, x, m - 5, c)
    linea(x - 14, m - 5, x + 14, m - 5, c, 2)
    linea(x - 7, m + 5, x + 7, m + 5, c, 4)
    linea(x, m + 5, x, y + l, c)
    testo(x + 10, m - 10, "+", c, 12)


def interruttore(x, y, l=80, c=ROSSO):
    linea(x, y, x + 15, y, c)
    punto(x + 15, y, c)
    linea(x + 15, y, x + l - 15, y - 16, c)
    el.append(f'<circle cx="{x + l - 15}" cy="{y}" r="4" fill="white" stroke="{c}" stroke-width="2"/>')
    linea(x + l - 11, y, x + l, y, c)


def led(x, y, l=60):
    """LED verticale, anodo in alto."""
    m = y + l / 2
    linea(x, y, x, m - 10)
    poli([(x - 11, m - 10), (x + 11, m - 10), (x, m + 8), (x - 11, m - 10)], NERO, 2, "white")
    linea(x - 11, m + 8, x + 11, m + 8)
    linea(x, m + 8, x, y + l)
    for d in (0, 9):
        linea(x + 14, m - 6 + d, x + 26, m - 14 + d, NERO, 1.5)


def nmos(x, y):
    """MOSFET N: drain in (x, y), source in (x, y + 60), gate in (x - 30, y + 30)."""
    linea(x, y, x, y + 18)
    linea(x, y + 18, x - 12, y + 18)
    linea(x, y + 42, x - 12, y + 42)
    linea(x, y + 42, x, y + 60)
    linea(x - 12, y + 12, x - 12, y + 48, w=3)
    linea(x - 18, y + 16, x - 18, y + 44)
    linea(x - 30, y + 30, x - 18, y + 30)
    poli([(x - 10, y + 42), (x - 3, y + 38), (x - 3, y + 46), (x - 10, y + 42)], fill=NERO)


def pmos(x, y):
    """MOSFET P orizzontale: source in (x, y), drain in (x + 60, y), gate in (x + 30, y + 30)."""
    poli([(x, y), (x + 18, y), (x + 18, y + 12)], ROSSO)
    poli([(x + 60, y), (x + 42, y), (x + 42, y + 12)], ROSSO)
    linea(x + 12, y + 12, x + 48, y + 12, NERO, 3)
    linea(x + 16, y + 18, x + 44, y + 18)
    linea(x + 30, y + 18, x + 30, y + 30)
    poli([(x + 18, y + 4), (x + 14, y + 10), (x + 22, y + 10), (x + 18, y + 4)], fill=NERO)


def etichetta_rete(x, y, nome, lato):
    if nome == "GND":
        massa(x, y)
    elif nome == "n.c.":
        testo(x + (-6 if lato == "sx" else 6), y + 5, "n.c.", GRIGIO, 12, "end" if lato == "sx" else "start")
    else:
        c = ROSSO if nome in POTENZA else BLU
        testo(x + (-6 if lato == "sx" else 6), y + 5, nome, c, 13, "end" if lato == "sx" else "start", "bold")


def modulo(x, y, w, h, titolo, sx=(), dx=(), passo=40, stub=50):
    """Riquadro di un modulo. sx/dx: lista di (pin, rete); rete '' = solo terminale libero.
    Restituisce pin -> coordinate dell'estremità del terminale."""
    el.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fbf7f0" stroke="{NERO}" stroke-width="2.2" rx="4"/>')
    righe = titolo.count("\n")
    testo(x + w / 2, y + h / 2 - 8 * righe, titolo, NERO, 15, "middle", "bold")
    pos = {}
    for lato, lista in (("sx", sx), ("dx", dx)):
        for i, (p, rete) in enumerate(lista):
            py = y + 30 + i * passo
            if lato == "sx":
                testo(x + 8, py + 5, p, NERO, 13)
                linea(x - stub, py, x, py)
                pos[p] = (x - stub, py)
            else:
                testo(x + w - 8, py + 5, p, NERO, 13, "end")
                linea(x + w, py, x + w + stub, py)
                pos[p] = (x + w + stub, py)
            if rete:
                etichetta_rete(*pos[p], rete, lato)
    return pos


def sezione(x, y, w, h, titolo, c):
    el.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{c}" stroke-width="1.2" stroke-dasharray="6 5" rx="8"/>')
    testo(x + 12, y + 22, titolo, c, 15, "start", "bold")


# ------------------------------------------------------------------ cartiglio
testo(40, 48, "METRONOMUS · schema elettrico", NERO, 26, "start", "bold")
testo(40, 74, "rev. 0.2.1 · 18/10/2026 · ESP32-S3 · bozza da verificare su breadboard · "
      "le etichette uguali indicano piedini collegati tra loro", GRIGIO, 14)

# ------------------------------------------------------------------ ALIMENTAZIONE
sezione(30, 95, 1620, 485, "ALIMENTAZIONE", ROSSO)

tp = modulo(110, 140, 220, 240, "TP4056\nUSB-C\n+ protezione", sx=[("USB-C", "")],
            dx=[("B+", ""), ("B−", ""), ("OUT+", ""), ("OUT−", "")], passo=55, stub=40)
testo(58, 160, "5 V", GRIGIO, 12, "end")
# celle in parallelo tra B+ e B−
bx, yp, yn = tp["B+"][0], tp["B+"][1], tp["B−"][1]
linea(bx, yp, bx + 130, yp, ROSSO)
linea(bx, yn, bx + 130, yn)
for cx in (bx + 60, bx + 120):
    punto(cx, yp, ROSSO)
    punto(cx, yn)
    batteria(cx, yp, yn - yp)
testo(bx + 145, yp + 20, "2 × 18350\nin parallelo (1S)", GRIGIO, 12)
# OUT+ = VBAT (sempre presente) → interruttore elettronico Q2/Q3 → VSW
ox, oy = tp["OUT+"]
linea(ox, oy, 440, oy, ROSSO)
punto(385, oy, ROSSO)
testo(385, oy - 10, "VBAT", ROSSO, 14, "middle", "bold")
punto(410, oy, ROSSO)
pmos(440, oy)
testo(470, oy - 14, "Q2 AO3401 (P)", NERO, 12, "middle")
# R8 tra source e gate di Q2
linea(410, oy, 410, oy + 50)
resistenza(410, oy + 50, 50, verticale=False)
testo(435, oy + 75, "R8 100 kΩ", NERO, 12, "middle")
linea(460, oy + 50, 470, oy + 50)
linea(470, oy + 30, 470, oy + 50)
punto(470, oy + 50)
poli([(470, oy + 50), (530, oy + 50), (530, oy + 70)])
nmos(530, oy + 70)
testo(542, oy + 110, "Q3 AO3400", NERO, 12)
massa(530, oy + 130)
resistenza(440, oy + 100, 60, verticale=False)
testo(470, oy + 125, "100 Ω", NERO, 12, "middle")
punto(440, oy + 100)
resistenza(440, oy + 100, 45)
massa(440, oy + 145)
testo(432, oy + 128, "100 kΩ", NERO, 12, "end")
linea(440, oy + 100, 420, oy + 100, BLU)
testo(416, oy + 105, "PWR_EN", BLU, 13, "end", "bold")
vsw = (ox + 300, oy)
linea(500, oy, vsw[0], oy, ROSSO)
punto(*vsw, ROSSO)
testo(vsw[0] + 8, vsw[1] - 10, "VSW", ROSSO, 14, "start", "bold")
massa(*tp["OUT−"])
# LDO sempre acceso per l'ESP32
poli([(385, oy), (385, 520), (860, 520)], ROSSO)
ldo = modulo(900, 490, 170, 80, "LDO 3,3 V\nbasso consumo", sx=[("IN", ""), ("GND", "GND")],
             dx=[("OUT", "3V3")], passo=40, stub=40)

# partitore batteria da VSW
x_, y_ = vsw
linea(x_, y_, x_, y_ + 20, ROSSO)
resistenza(x_, y_ + 20, 55)
testo(x_ + 14, y_ + 52, "R1 100 kΩ", NERO, 12)
adc = (x_, y_ + 95)
linea(x_, y_ + 75, *adc)
punto(*adc)
resistenza(x_, adc[1], 55)
testo(x_ + 14, adc[1] + 32, "R2 100 kΩ", NERO, 12)
massa(x_, adc[1] + 55)
linea(x_, adc[1], x_ + 90, adc[1])
condensatore(x_ + 90, adc[1], 55)
testo(x_ + 108, adc[1] + 32, "C1 100 nF", NERO, 12)
massa(x_ + 90, adc[1] + 55)
testo(x_ + 45, adc[1] - 8, "VBAT_ADC", BLU, 13, "middle", "bold")

# MT3608
mt = modulo(800, 230, 170, 110, "MT3608\nboost → 12 V", sx=[("VIN+", ""), ("VIN−", "GND")],
            dx=[("VOUT+", ""), ("VOUT−", "GND")], passo=50, stub=40)
poli([vsw, (720, vsw[1]), (720, mt["VIN+"][1]), mt["VIN+"]], ROSSO)
linea(720, mt["VIN+"][1], 720, 165, ROSSO)
punto(720, mt["VIN+"][1], ROSSO)
testo(720, 155, "VSW → modulo vibrazione", ROSSO, 13, "middle", "bold")
v12 = (mt["VOUT+"][0] + 60, mt["VOUT+"][1])
linea(*mt["VOUT+"], *v12, ROSSO)
punto(*v12, ROSSO)
linea(v12[0], v12[1], v12[0], 165, ROSSO)
testo(v12[0], 155, "V12 → driver, filamenti LED", ROSSO, 13, "middle", "bold")

# Mini-360
mn = modulo(1180, 230, 170, 110, "Mini-360\nstep-down → 3,3 V", sx=[("IN+", ""), ("IN−", "GND")],
            dx=[("OUT+", "3V3_SW"), ("OUT−", "GND")], passo=50, stub=50)
linea(*v12, *mn["IN+"], ROSSO)

testo(1190, 500, "Tarare MT3608 a 12,0 V e Mini-360 a 3,30 V PRIMA di collegare i carichi.\n"
      "Mettere le celle in parallelo solo quando hanno la stessa tensione.\n"
      "In letargo PWR_EN = 0: Q2 spegne boost, driver, LED, AS5600 e vibrazione.\n"
      "Restano accesi solo LDO + ESP32 in deep sleep (decine di µA).", ROSSO, 13)

# ------------------------------------------------------------------ CONTROLLO
INIZIO_CONTROLLO = len(el)
sezione(30, 495, 1620, 670, "CONTROLLO E ATTUATORI", BLU)

esp = modulo(740, 560, 230, 360, "ESP32-S3\nSuperMini",
             sx=[("5V", "n.c."), ("GND", "GND"), ("3V3", "3V3"), ("GPIO13", "ENC_B"), ("GPIO12", "ENC_A"),
                 ("GPIO11", "n.c."), ("GPIO10", "LED_PWM"), ("GPIO9", "VBAT_ADC"), ("GPIO8", "ENC_SW")],
             dx=[("TX", "n.c."), ("RX", "n.c."), ("GPIO1", "SCL"), ("GPIO2", "SDA"), ("GPIO3", "VIB_IN"),
                 ("GPIO4", "PWR_EN"), ("GPIO5", "PWM_C"), ("GPIO6", "PWM_B"), ("GPIO7", "PWM_A")],
             passo=37, stub=60)
testo(855, 945, "GPIO8 = pulsante, risveglia dal letargo · GPIO3 = strapping JTAG (innocuo)\nTogliere il LED rosso di alimentazione della SuperMini", GRIGIO, 12, "middle")

drv = modulo(1200, 560, 200, 380, "SimpleFOC\nMini v1.0\n(DRV8313)",
             sx=[("IN1", "PWM_A"), ("IN2", "PWM_B"), ("IN3", "PWM_C"), ("EN", "DRV_3V3"), ("GND", "GND"),
                 ("nFT", "n.c."), ("nSP", "n.c."), ("nRT", "n.c."), ("3V3", "DRV_3V3")],
             dx=[("+", "V12"), ("−", "GND"), ("M1", ""), ("M2", ""), ("M3", "")], passo=42, stub=40)
mx, my = 1540, drv["M2"][1]
el.append(f'<circle cx="{mx}" cy="{my}" r="42" fill="#fbf7f0" stroke="{NERO}" stroke-width="2.2"/>')
testo(mx, my - 2, "M", NERO, 20, "middle", "bold")
testo(mx, my + 18, "3~", NERO, 13, "middle")
for p, d in (("M1", -28), ("M2", 0), ("M3", 28)):
    x0, y0 = drv[p]
    xe = mx - (42 ** 2 - d ** 2) ** 0.5
    poli([(x0, y0), (x0 + 30, y0), (x0 + 30, my + d), (xe, my + d)])
testo(mx, my + 62, "Motore 1503\n0,5 Ω · voltage_limit ≈ 0,5–1 V", GRIGIO, 12, "middle")

asx = modulo(1515, 880, 120, 260, "AS5600",
             sx=[("VCC", "3V3_SW"), ("GND", "GND"), ("DIR", "GND"), ("SDA", "SDA"), ("SCL", "SCL"),
                 ("GPO", "n.c."), ("OUT", "n.c.")], passo=34, stub=40)

vib = modulo(1150, 1000, 170, 120, "Modulo\nvibrazione", sx=[("VCC", "VSW"), ("IN", "VIB_IN"), ("GND", "GND")],
             passo=34, stub=40)
testo(1050, 1150, "47–100 µF + 100 nF su VCC · impulsi ≥ 60 ms · magnete AS5600 diametrale 6×2,5 mm a 0,5–3 mm", GRIGIO, 12)

# filamenti LED
testo(60, 540, "Filamenti LED (×2) sul pendolo", NERO, 14, "start", "bold")
for k, x in enumerate((130, 230)):
    testo(x, 572, "V12", ROSSO, 13, "middle", "bold")
    linea(x, 580, x, 595, ROSSO)
    resistenza(x, 595, 60)
    testo(x + 14, 630, f"R{6 + k}*", NERO, 12)
    led(x, 655, 60)
    testo(x + 30, 690, f"LED{k + 1}", NERO, 12)
    linea(x, 715, x, 740)
linea(130, 740, 230, 740)
punto(180, 740)
linea(180, 740, 180, 760)
nmos(180, 760)
testo(192, 795, "Q1 AO3400", NERO, 12)
massa(180, 820)
resistenza(90, 790, 60, verticale=False)
testo(122, 815, "100 Ω", NERO, 12, "middle")
punto(90, 790)
resistenza(90, 790, 50)
testo(80, 822, "100 kΩ", NERO, 12, "end")
massa(90, 840)
linea(90, 790, 60, 790, BLU)
testo(56, 795, "LED_PWM", BLU, 13, "end", "bold") if False else testo(75, 772, "LED_PWM", BLU, 13, "middle", "bold")
testo(60, 900, "* R6, R7 = (12 V − Vf) / I, da calcolare dopo\naver misurato la Vf del filamento (≈ 300 Ω, 0,5 W).\n"
      "Il filo di ritorno corre lungo il filamento.", GRIGIO, 12)

# encoder EC11 con antirimbalzo
testo(360, 540, "Encoder EC11 + antirimbalzo", NERO, 14, "start", "bold")
for i, (pin_, rete, rn) in enumerate((("A", "ENC_A", "R3"), ("B", "ENC_B", "R4"), ("SW", "ENC_SW", "R5"))):
    y = 595 + i * 100
    testo(380, y + 5, pin_, NERO, 14, "end", "bold")
    linea(385, y, 400, y)
    resistenza(400, y, 70, verticale=False)
    testo(435, y - 14, f"{rn} 10 kΩ", NERO, 12, "middle")
    punto(490, y)
    linea(470, y, 540, y, BLU)
    testo(546, y + 5, rete, BLU, 13, "start", "bold")
    condensatore(490, y, 45)
    testo(504, y + 30, "10 nF", NERO, 12)
    massa(490, y + 45)
testo(360, 920, "C (comune) e secondo piedino del pulsante a GND.\nPull-up interne dell'ESP32 attive.", GRIGIO, 12)

el[INIZIO_CONTROLLO:] = ['<g transform="translate(0,100)">'] + el[INIZIO_CONTROLLO:] + ["</g>"]
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
       f'<rect width="{W}" height="{H}" fill="white"/>' + "\n".join(el) + "</svg>")
(QUI / "schema.svg").write_text(svg, encoding="utf-8")

try:
    import cairosvg
    cairosvg.svg2pdf(url=str(QUI / "schema.svg"), write_to=str(QUI / "schema.pdf"))
    cairosvg.svg2png(url=str(QUI / "schema.svg"), write_to=str(QUI / "schema.png"), scale=1.5)
except ImportError:
    pass
