"""Geometria del circuito in rame di Metronomus: unica fonte per modello 3D, render e PDF.

Uso:  python fili/geometria.py
  - legge le misure dei moduli da fili/moduli.yaml;
  - dispone i moduli e traccia le reti con segmenti dritti (nessuna piega);
  - controlla: pezzi >= 10 mm, distanza tra fili di reti diverse, fili che attraversano le schede,
    schede che si sovrappongono (gioco 0,5 mm), reti tutte collegate;
  - scrive fili/segmenti.csv (distinta di taglio, in ordine di montaggio) e modello/metronomus.scad.

Struttura a bus: ogni scheda ha le sue discese (fili dritti dal pin fino alla quota del bus); i bus
corrono sollevati sopra la base e sporgono oltre l'ultima discesa, che si salda in T dove cade.

Assi in mm: x verso destra, y verso il retro, z verso l'alto; z = 0 è il piano della base di legno.
"""
import csv
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

QUI = Path(__file__).resolve().parent
RADICE = QUI.parent

R_FILO = 0.5
PEZZO_MIN = 10.0          # nessun pezzo più corto di 1 cm (richiesta di Fabio)
DISTANZA_MIN = 2.5        # tra gli assi di fili di reti diverse (gioco 1,5 mm; il passo dei pin è 2,54)
INFILATA_PIN = 2.5        # filo che attraversa il foro di un modulo e sporge per la saldatura
INFILATA_BASE = 5.0       # filo infilato in un foro della base di legno
GIOCO_SCHEDE = 0.5        # distanza minima tra gli ingombri di due schede (o di una scheda e un ostacolo)
TOL = 1e-6

MISURE = yaml.safe_load((QUI / "moduli.yaml").read_text(encoding="utf-8"))


# ------------------------------------------------------------------ vettori
def add(a, b): return tuple(x + y for x, y in zip(a, b))
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def mul(a, k): return tuple(x * k for x in a)
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def norma(a): return math.sqrt(dot(a, a))
def tonda(p): return tuple(round(c, 3) for c in p)


ROT = {  # assi locali x, y della scheda vista dall'alto, ruotata in senso antiorario
    0: ((1, 0, 0), (0, 1, 0)),
    90: ((0, 1, 0), (-1, 0, 0)),
    180: ((-1, 0, 0), (0, -1, 0)),
    270: ((0, -1, 0), (1, 0, 0)),
}


# ------------------------------------------------------------------ moduli
def pin_locali(chiave):
    m = MISURE[chiave]
    pin = dict(m.get("pin", {}))
    for x0, y0, verso, nomi in m.get("file", []):
        dx, dy = {"+x": (1, 0), "-x": (-1, 0), "+y": (0, 1), "-y": (0, -1)}[verso]
        for i, n in enumerate(nomi):
            pin[n] = [x0 + dx * i * m.get("passo", 2.54), y0 + dy * i * m.get("passo", 2.54)]
    return pin


@dataclass
class Modulo:
    nome: str
    chiave: str | None
    dimensioni: tuple
    u: tuple = (1, 0, 0)
    v: tuple = (0, 1, 0)
    origine: tuple = (0, 0, 0)
    spessore: float = 1.6
    altezza: float = 3.0
    sotto: float = 0.3
    pin_loc: dict = field(default_factory=dict)
    colore: str = "nero"
    stato: str = "stimato"

    @property
    def n(self):
        return cross(self.u, self.v)

    def mondo(self, p):
        return add(add(self.origine, mul(self.u, p[0])), mul(self.v, p[1]))

    def pin(self, nome):
        return tonda(self.mondo(self.pin_loc[nome]))

    def allinea(self, nome, punto):
        """Sposta il modulo in modo che il pin `nome` cada sul punto (solo le coordinate date, None = libera)."""
        attuale = self.pin(nome)
        delta = tuple(0 if p is None else p - a for p, a in zip(punto, attuale))
        self.origine = add(self.origine, delta)
        return self

    def scatola(self):
        """Ingombro allineato agli assi: (min, max)."""
        w, h = self.dimensioni
        punti = []
        for a in (0, w):
            for b in (0, h):
                for c in (-self.spessore - self.sotto, self.altezza):
                    punti.append(add(self.mondo((a, b)), mul(self.n, c)))
        return tuple(min(p[i] for p in punti) for i in range(3)), tuple(max(p[i] for p in punti) for i in range(3))


def modulo(chiave, nome, rot=0, verticale=None, colore="nero", **extra):
    m = MISURE[chiave]
    u, v = verticale if verticale else ROT[rot]
    return Modulo(nome, chiave, tuple(m["dimensioni"]), u, v, spessore=m.get("spessore", 1.6),
                  altezza=m.get("altezza", 3), sotto=m.get("sotto", 0.3), pin_loc=pin_locali(chiave),
                  colore=colore, stato=m.get("stato", "stimato"), **extra)


# ------------------------------------------------------------------ reti
@dataclass
class Rete:
    nome: str
    tratti: list = field(default_factory=list)   # liste di punti
    gruppi: list = field(default_factory=list)   # gruppo di montaggio di ogni tratto (una scheda, "bus", "struttura")
    pin: list = field(default_factory=list)      # (modulo, pin) che la rete deve toccare
    fori: list = field(default_factory=list)     # fori nella base (punti a z = 0)
    liberi: list = field(default_factory=list)   # estremità libere (attacco di un filo flessibile)
    teste: list = field(default_factory=list)    # estremità del bus oltre l'ultima discesa (nessun giunto)


RETI = {}

# Criticità trovate dai controlli, per colorarle di rosso nel modello OpenSCAD:
# pezzi (codici), oggetti (nomi di moduli o ostacoli) e zone (scatole dove gli ingombri si toccano).
CRITICITA = {"pezzi": set(), "oggetti": set(), "zone": []}


def rete(nome):
    return RETI.setdefault(nome, Rete(nome))


def tratto(nome_rete, *punti, gruppo="bus"):
    pts = [tonda(p) for p in punti]
    # unisce i punti allineati (un pezzo dritto resta un pezzo solo)
    pulito = [pts[0]]
    for p in pts[1:]:
        if p == pulito[-1]:
            continue
        if len(pulito) >= 2:
            d1 = sub(pulito[-1], pulito[-2])
            d2 = sub(p, pulito[-1])
            if norma(cross(d1, d2)) < TOL and dot(d1, d2) > 0:
                pulito[-1] = p
                continue
        pulito.append(p)
    rete(nome_rete).tratti.append(pulito)
    rete(nome_rete).gruppi.append(gruppo)
    return pulito


# Struttura a bus (decisione del 18/10/2026): ogni scheda ha le sue DISCESE, fili dritti dal pin
# fino alla quota del bus; i BUS corrono sollevati sopra la base e proseguono di SPORGENZA oltre
# l'ultima discesa, così ogni discesa si salda in T dove cade davvero (gioco di montaggio).
SPORGENZA = 3.0


def discesa(chiave, pin, nome_rete, z, *piede):
    """Filo dritto dal pin fino alla quota z; `piede` = eventuali punti successivi fino al bus."""
    rete(nome_rete).pin.append((chiave, pin))
    p = MODULI[chiave].pin(pin)
    return tratto(nome_rete, p, (p[0], p[1], z), *piede, gruppo=chiave)


def bus(nome_rete, *punti, sporgenze=(SPORGENZA, SPORGENZA)):
    """Linea del bus tra i punti dati, allungata alle due estremità (0 = estremità su un giunto)."""
    pts = [tonda(p) for p in punti]
    for i, (k, vicino) in enumerate(((0, 1), (-1, -2))):
        if sporgenze[i]:
            d = sub(pts[k], pts[vicino])
            pts[k] = tonda(add(pts[k], mul(d, sporgenze[i] / norma(d))))
            rete(nome_rete).teste.append(pts[k])
    return tratto(nome_rete, *pts, gruppo="bus")


# ================================================================== DISPOSIZIONE
DECK = 30.0                      # piano delle schede orizzontali (lato componenti in su)
ASSE = (0.0, 9.0, 72.0)          # punto dell'asse motore sul retro del motore (x, y, z)
Y_AS = 11.0                      # piano dell'AS5600, componenti verso il motore

MODULI = {}

# --- AS5600 verticale dietro al motore: fila DIR/SCL/SDA/GPO in alto, orizzontale.
#     Locale x -> su (+z), locale y -> verso -x: il lato componenti guarda il motore (-y).
MODULI["as5600"] = modulo("as5600", "AS5600", verticale=((0, 0, 1), (-1, 0, 0)), colore="bianco")
MODULI["as5600"].allinea("CHIP", (ASSE[0], Y_AS, ASSE[2]))
AS = MODULI["as5600"]

# --- ESP32-S3 sul ponte, ruotato di 90 gradi: fila TX/RX/GPIO1..7 davanti, fila 5V..GPIO8 dietro.
#     GPIO1 (SCL) e GPIO2 (SDA) sotto i fili che scendono dall'AS5600.
Y_ESP_FRONTE = Y_AS + 14.0
MODULI["esp32"] = modulo("esp32s3", "ESP32-S3", rot=90, colore="nero")
ESP = MODULI["esp32"]
ESP.origine = (0, 0, DECK)
ESP.allinea("GPIO1", (AS.pin("SCL")[0], Y_ESP_FRONTE, DECK))

# --- Driver davanti all'ESP32: IN1..IN3 sotto GPIO7..5, collegati a U (un passo più a destra
#     di GPIO6..4: con le misure vere il driver toccherebbe il Mini-360).
MODULI["driver"] = modulo("simplefoc_mini", "SimpleFOC Mini", rot=0, colore="nero")
DRV = MODULI["driver"]
DRV.origine = (0, 0, DECK)
DRV.allinea("IN1", (ESP.pin("GPIO7")[0], Y_ESP_FRONTE - 11.0, DECK))

# --- Mini-360 a sinistra: OUT+ esattamente sotto la discesa del VCC dell'AS5600.
Y_DISCESA_AS = Y_AS + 10.0       # i fili VCC e GND dell'AS5600 corrono 10 mm verso il retro e scendono
MODULI["mini360"] = modulo("mini360", "Mini-360", rot=0, colore="verde")
MINI = MODULI["mini360"]
MINI.origine = (0, 0, DECK)
MINI.allinea("OUT+", (AS.pin("VCC")[0], Y_DISCESA_AS, DECK))

# --- MT3608 a destra del driver, ruotato di 270: VOUT davanti, sulla stessa y del + del driver.
MODULI["mt3608"] = modulo("mt3608", "MT3608", rot=270, colore="blu")
MT = MODULI["mt3608"]
MT.origine = (0, 0, DECK)
MT.allinea("VOUT+", (38.0 + 4.8, DRV.pin("PWR+")[1], DECK))

# --- Scheda servizi (millefori a passo 2,54, da tagliare): LDO, MOSFET del letargo e del LED,
#     resistenze. I suoi pin sono sulla stessa griglia dei pin dell'ESP32.
#     Griglia contata dal pin 5V dell'S3 (k = 0), verso +x: 3V3 = 2, GPIO11 = 5, GPIO10 = 6, GPIO9 = 7.
#     PWR_EN passa dritto sotto GPIO11, che resta libero.
Y_SERVIZI = ESP.pin("5V")[1] + 12.26
X0 = ESP.pin("5V")[0]             # griglia x dei pin: X0 + 2,54 k
def gx(k): return round(X0 + 2.54 * k, 3)


PIN_SERVIZI = {
    "3V3": gx(2), "PWR_EN": gx(5), "LED_PWM": gx(6), "ADC": gx(7), "LED_K": gx(9), "LED_A": gx(10),
    "VBAT": gx(11), "GND": gx(12), "V12": gx(14), "VSW": gx(15), "VSW_VIB": gx(16),
}
servizi = Modulo("Scheda servizi", None, (gx(16) - gx(2) + 2 * 1.8, 10.16), origine=(gx(2) - 1.8, Y_SERVIZI - 5.08, DECK),
                 spessore=1.6, altezza=6.0, sotto=1.0, colore="millefori", stato="progetto")
servizi.pin_loc = {k: [x - servizi.origine[0], 5.08] for k, x in PIN_SERVIZI.items()}
MODULI["servizi"] = servizi
SRV = servizi

# ------------------------------------------------------------------ motore e telaio
MOTORE = {"asse": ASSE, "diametro": MISURE["motore_1503"]["diametro_campana"],
          "lunghezza": MISURE["motore_1503"]["lunghezza"]}
# Magnete diametrale dell'AS5600 incollato sull'estremità dell'albero, dietro al motore.
# sporgenza = quanto l'albero esce dal retro della base (da misurare: per ora a filo).
MAGNETE = {"diametro": 6.0, "spessore": 2.5, "sporgenza": MISURE["motore_1503"].get("sporgenza_albero", 0.0)}
Y_TELAIO_RETRO, Y_TELAIO_FRONTE, X_TELAIO = 8.5, -8.0, 11.5

# ------------------------------------------------------------------ pendolo e finecorsa
Y_PENDOLO = ASSE[1] - MOTORE["lunghezza"] - 5.5     # piano in cui oscilla il pendolo
Y_FLESSIBILI = Y_PENDOLO + 8.0                      # dove finisce il rame e comincia il filo flessibile
ANGOLO_FC = 45.0                                    # arco della scala ±40°, finecorsa 5° oltre
R_COLLARE = 3.0                                     # collare di ottone sul LED: tocca il paletto per primo
X_FC = 20.0
# la cima del paletto tocca il collare quando il pendolo è a ANGOLO_FC
_a = math.radians(ANGOLO_FC)
Z_FC = round(ASSE[2] + (X_FC * math.cos(_a) - R_COLLARE - R_FILO) / math.sin(_a), 1)
R_CONTATTO = round(X_FC * math.sin(_a) + (Z_FC - ASSE[2]) * math.cos(_a), 1)   # raggio del collare
Z_TELAIO_ALTO, Z_TELAIO_BASSO = 84.0, 60.0

# ------------------------------------------------------------------ pannello della scala
PANNELLO = {"centro": (0.0, -5.0, 160.0), "dimensioni": (170.0, 5.0, 70.0)}
X_COLONNE_PANNELLO, Y_COLONNE_PANNELLO, Z_COLONNE_PANNELLO = 72.0, -1.5, 195.0

# ------------------------------------------------------------------ batterie 18350 in parallelo
BATTERIE = [{"centro": (x, 19.5, 9.15), "diametro": 18.3, "lunghezza": 35.0} for x in (-35.0, -56.0)]

# ------------------------------------------------------------------ base
BASE = {"min": (-95.0, -25.0, -22.0), "max": (95.0, 65.0, 0.0)}

# ================================================================== RETI
# Quote dei bus sopra la base (sollevati dal legno): massa, 12 V, segnali.
Z_ANELLO, Z_DORSALE, Z_PONTI, Z_LED = 6.0, 14.0, 18.0, 95.0
ANELLO = {"x": (-22.0, 37.5), "y": (1.0, ESP.pin("GND")[1] - 11.5)}
ax0, ax1 = ANELLO["x"]
ay0, ay1 = ANELLO["y"]

# ------------------------------------------------------------------ bus
# GND: anello chiuso vicino alla base; il ritorno della batteria scende nella base vicino al driver
# e al MT3608 (le correnti del motore non passano sotto la logica).
tratto("GND", (ax0, ay0, Z_ANELLO), (ax1, ay0, Z_ANELLO), (ax1, ay1, Z_ANELLO), (ax0, ay1, Z_ANELLO), (ax0, ay0, Z_ANELLO))
foro_gnd = (ax0, (ay0 + ay1) / 2, 0.0)
tratto("GND", (ax0, foro_gnd[1], Z_ANELLO), foro_gnd)            # al TP4056 OUT- sotto la base
rete("GND").fori.append(foro_gnd)

# V12: dorsale lungo il fronte dal MT3608 al Mini-360, ramo verso la scheda servizi
Y_DORSALE = MT.pin("VOUT+")[1]
X_RAMO_V12 = SRV.pin("V12")[0]
bus("V12", (MT.pin("VOUT+")[0], Y_DORSALE, Z_DORSALE), (MINI.pin("IN+")[0], Y_DORSALE, Z_DORSALE),
    (MINI.pin("IN+")[0], MINI.pin("IN+")[1], Z_DORSALE))
bus("V12", (X_RAMO_V12, Y_DORSALE, Z_DORSALE), (X_RAMO_V12, SRV.pin("V12")[1], Z_DORSALE), sporgenze=(0, SPORGENZA))

# Segnali tra ESP32 e driver / scheda servizi: linee lungo y sotto i pin allineati
for nome, a, b in (("PWM_A", DRV.pin("IN1"), ESP.pin("GPIO7")), ("PWM_B", DRV.pin("IN2"), ESP.pin("GPIO6")),
                   ("PWM_C", DRV.pin("IN3"), ESP.pin("GPIO5")), ("PWR_EN", ESP.pin("GPIO4"), SRV.pin("PWR_EN")),
                   ("3V3", ESP.pin("3V3"), SRV.pin("3V3")), ("LED_PWM", ESP.pin("GPIO10"), SRV.pin("LED_PWM")),
                   ("VBAT_ADC", ESP.pin("GPIO9"), SRV.pin("ADC"))):
    bus(nome, (a[0], a[1], Z_PONTI), (b[0], b[1], Z_PONTI))

# VSW: dalla scheda servizi lungo y fino all'altezza del MT3608, poi lungo x sotto il suo VIN+
a, b = SRV.pin("VSW"), MT.pin("VIN+")
bus("VSW", (a[0], a[1], Z_PONTI), (a[0], b[1], Z_PONTI), (b[0], b[1], Z_PONTI))

# ------------------------------------------------------------------ discese, scheda per scheda
# MT3608
discesa("mt3608", "VOUT+", "V12", Z_DORSALE)
discesa("mt3608", "VIN+", "VSW", Z_PONTI)
p = MT.pin("VOUT-")
discesa("mt3608", "VOUT-", "GND", Z_ANELLO, (ax1, p[1], Z_ANELLO))

# Mini-360 (OUT+ va dritto all'AS5600: vedi sotto)
discesa("mini360", "IN+", "V12", Z_DORSALE)
p = MINI.pin("OUT-")
discesa("mini360", "OUT-", "GND", Z_ANELLO, (p[0], ay0, Z_ANELLO))

# Scheda servizi
discesa("servizi", "V12", "V12", Z_DORSALE)
discesa("servizi", "VSW", "VSW", Z_PONTI)
for nome, ps in (("PWR_EN", "PWR_EN"), ("3V3", "3V3"), ("LED_PWM", "LED_PWM"), ("VBAT_ADC", "ADC")):
    discesa("servizi", ps, nome, Z_PONTI)
p = SRV.pin("GND")
discesa("servizi", "GND", "GND", Z_ANELLO, (p[0], ay1, Z_ANELLO))
for nome, ps in (("VBAT", "VBAT"), ("VSW", "VSW_VIB")):          # nella base: TP4056 e motorino a vibrazione
    discesa("servizi", ps, nome, 0.0)
    rete(nome).fori.append(tonda((SRV.pin(ps)[0], SRV.pin(ps)[1], 0.0)))
# LED: due fili salgono fin sopra il motore; da lì 15-20 mm di filo flessibile fino ai filamenti
for nome in ("LED_A", "LED_K"):
    p = SRV.pin(nome)
    fine = (p[0], Y_FLESSIBILI, Z_LED)
    discesa("servizi", nome, nome, Z_LED, fine)
    rete(nome).liberi.append(tonda(fine))

# ESP32-S3
for nome, pe in (("PWM_A", "GPIO7"), ("PWM_B", "GPIO6"), ("PWM_C", "GPIO5"), ("PWR_EN", "GPIO4"),
                 ("3V3", "3V3"), ("LED_PWM", "GPIO10"), ("VBAT_ADC", "GPIO9")):
    discesa("esp32", pe, nome, Z_PONTI)
p = ESP.pin("GND")
discesa("esp32", "GND", "GND", Z_ANELLO, (p[0], ay1, Z_ANELLO))
for nome, pe in (("ENC_SW", "GPIO8"), ("ENC_A", "GPIO12"), ("ENC_B", "GPIO13"), ("VIB_IN", "GPIO3")):
    discesa("esp32", pe, nome, 0.0)                                # nella base: encoder e motorino
    rete(nome).fori.append(tonda((ESP.pin(pe)[0], ESP.pin(pe)[1], 0.0)))

# SimpleFOC Mini
for nome, pd in (("PWM_A", "IN1"), ("PWM_B", "IN2"), ("PWM_C", "IN3")):
    discesa("driver", pd, nome, Z_PONTI)
discesa("driver", "PWR+", "V12", Z_DORSALE)
p = DRV.pin("PWR-")
discesa("driver", "PWR-", "GND", Z_ANELLO, (ax1, p[1], Z_ANELLO))

# AS5600: collegamenti diretti, senza bus (I2C corto, lontano dalle fasi del motore)
for nome, pa, pe in (("SCL", "SCL", "GPIO1"), ("SDA", "SDA", "GPIO2")):
    rete(nome).pin += [("as5600", pa), ("esp32", pe)]
    p, q = AS.pin(pa), ESP.pin(pe)
    tratto(nome, p, (p[0], q[1], p[2]), q, gruppo="as5600")
rete("3V3_SW").pin += [("as5600", "VCC"), ("mini360", "OUT+")]
p = AS.pin("VCC")
tratto("3V3_SW", p, (p[0], Y_DISCESA_AS, p[2]), MINI.pin("OUT+"), gruppo="as5600")
p = AS.pin("GND")
discesa("as5600", "GND", "GND", p[2], (p[0], Y_DISCESA_AS, p[2]), (p[0], Y_DISCESA_AS, Z_ANELLO), (p[0], ay0, Z_ANELLO))

# Finecorsa (stop di emergenza): due paletti verticali nel piano del pendolo a ±ANGOLO_FC, uniti
# dal bus STOP, che va all'EN del driver e a GPIO43. Il collare di ottone del pendolo (rete ARMA,
# GPIO44 con filo flessibile) tocca la cima del paletto: il paletto è anche il finecorsa meccanico.
for nome, x in (("STOP", -X_FC), ("STOP", X_FC)):
    tratto(nome, (x, Y_PENDOLO, 0.0), (x, Y_PENDOLO, Z_FC), gruppo="struttura")
    rete(nome).fori.append((x, Y_PENDOLO, 0.0))
    rete(nome).teste.append(tonda((x, Y_PENDOLO, Z_FC)))
bus("STOP", (-X_FC, Y_PENDOLO, Z_PONTI), (X_FC, Y_PENDOLO, Z_PONTI), sporgenze=(0, 0))
for chiave, pin in (("driver", "EN"), ("esp32", "GPIO43")):
    p = MODULI[chiave].pin(pin)
    bus("STOP", (p[0], p[1], Z_PONTI), (p[0], Y_PENDOLO, Z_PONTI), sporgenze=(SPORGENZA, 0))
    discesa(chiave, pin, "STOP", Z_PONTI)

# Fili verso il pendolo: salgono a Z_LED e arrivano 8 mm dietro al piano del pendolo; da lì filo flessibile.
p = ESP.pin("GPIO44")
discesa("esp32", "GPIO44", "ARMA", Z_LED, (p[0], Y_FLESSIBILI, Z_LED))
rete("ARMA").liberi.append(tonda((p[0], Y_FLESSIBILI, Z_LED)))

# --- struttura (non è una rete elettrica): telaio del motore e colonne del pannello
xt, yr, yf, za, zb = X_TELAIO, Y_TELAIO_RETRO, Y_TELAIO_FRONTE, Z_TELAIO_ALTO, Z_TELAIO_BASSO
for x, y in ((-xt, yr), (-xt, yf), (xt, yf)):
    tratto("TELAIO", (x, y, 0.0), (x, y, za), gruppo="struttura")
    rete("TELAIO").fori.append((x, y, 0.0))
tratto("TELAIO", (-xt, yr, za), (xt, yr, za), (xt, yr, zb), (-xt, yr, zb), gruppo="struttura")
tratto("TELAIO", (-xt, yr, za), (-xt, yf, za), (xt, yf, za), (xt, yr, za), gruppo="struttura")
for x in (-X_COLONNE_PANNELLO, X_COLONNE_PANNELLO):
    tratto("PANNELLO", (x, Y_COLONNE_PANNELLO, 0.0), (x, Y_COLONNE_PANNELLO, Z_COLONNE_PANNELLO), gruppo="struttura")
    rete("PANNELLO").fori.append((x, Y_COLONNE_PANNELLO, 0.0))
tratto("PANNELLO", (-X_COLONNE_PANNELLO, Y_COLONNE_PANNELLO, Z_COLONNE_PANNELLO),
       (X_COLONNE_PANNELLO, Y_COLONNE_PANNELLO, Z_COLONNE_PANNELLO), gruppo="struttura")

# --- portabatterie in rame: barra del + davanti, barra del - dietro, scendono nella base
for nome, y in (("BATT+", 19.5 - 17.5 - 1.0), ("BATT-", 19.5 + 17.5 + 1.0)):
    xa, xb = BATTERIE[0]["centro"][0], BATTERIE[1]["centro"][0]
    tratto(nome, (xa, y, 0.0), (xa, y, 9.15), (xb, y, 9.15), (xb, y, 0.0), gruppo="alimentazione")
    rete(nome).fori += [(xa, y, 0.0), (xb, y, 0.0)]

# Ordine di montaggio: struttura e bus sulla dima, poi una scheda alla volta, alimentazione per prima.
GRUPPI = ["struttura", "bus", "alimentazione", "mt3608", "mini360", "servizi", "esp32", "driver", "as5600"]
NOMI_GRUPPI = {"struttura": "Struttura", "bus": "Bus", "alimentazione": "Batterie"} | {k: m.nome for k, m in MODULI.items()}


# ================================================================== CONTROLLI
@dataclass
class Pezzo:
    codice: str
    rete: str
    a: tuple
    b: tuple
    tipo_a: str = ""
    tipo_b: str = ""
    gruppo: str = ""

    @property
    def lunghezza(self):
        return norma(sub(self.b, self.a))

    @property
    def asse(self):
        d = sub(self.b, self.a)
        return "XYZ"[max(range(3), key=lambda i: abs(d[i]))]

    @property
    def taglio(self):
        extra = {"pin": INFILATA_PIN, "base": INFILATA_BASE, "passante": R_FILO, "battuta": -R_FILO,
                 "libero": 0.0, "testa": 0.0, "?": 0.0}
        return self.lunghezza + extra[self.tipo_a] + extra[self.tipo_b]


def sul_segmento(p, a, b):
    ab, ap = sub(b, a), sub(p, a)
    l2 = dot(ab, ab)
    t = dot(ap, ab) / l2
    return TOL < t < 1 - TOL and norma(sub(ap, mul(ab, t))) < 1e-3


def distanza_segmenti(p1, q1, p2, q2):
    """Distanza minima tra due segmenti 3D."""
    d1, d2, r = sub(q1, p1), sub(q2, p2), sub(p1, p2)
    a, e, f = dot(d1, d1), dot(d2, d2), dot(d2, r)
    c, b = dot(d1, r), dot(d1, d2)
    den = a * e - b * b
    s = min(max((b * f - c * e) / den, 0), 1) if den > TOL else 0.0
    t = (b * s + f) / e
    if t < 0:
        t, s = 0.0, min(max(-c / a, 0), 1)
    elif t > 1:
        t, s = 1.0, min(max((b - c) / a, 0), 1)
    return norma(sub(add(p1, mul(d1, s)), add(p2, mul(d2, t))))


def segmento_in_scatola(a, b, lo, hi, margine):
    """Vero se il segmento (asse) entra nella scatola allargata del raggio del filo."""
    t0, t1 = 0.0, 1.0
    for i in range(3):
        d = b[i] - a[i]
        l, h = lo[i] - margine, hi[i] + margine
        if abs(d) < TOL:
            if a[i] <= l or a[i] >= h:
                return False
        else:
            ta, tb = sorted(((l - a[i]) / d, (h - a[i]) / d))
            t0, t1 = max(t0, ta), min(t1, tb)
            if t0 >= t1:
                return False
    return True


def ostacoli():
    """Ingombri solidi da cui i fili devono stare lontani (oltre ai moduli)."""
    ax, ay, az = MOTORE["asse"]
    r = MOTORE["diametro"] / 2
    yield "motore", (ax - r, ay - MOTORE["lunghezza"] - 4, az - r), (ax + r, ay, az + r)
    rm, sm = MAGNETE["diametro"] / 2, MAGNETE["spessore"]
    yield "magnete", (ax - rm, ay + MAGNETE["sporgenza"], az - rm), (ax + rm, ay + MAGNETE["sporgenza"] + sm, az + rm)
    for i, bt in enumerate(BATTERIE):
        cx, cy, cz = bt["centro"]
        r, l = bt["diametro"] / 2, bt["lunghezza"] / 2
        yield f"batteria {i + 1}", (cx - r, cy - l, cz - r), (cx + r, cy + l, cz + r)
    c, d = PANNELLO["centro"], PANNELLO["dimensioni"]
    yield "pannello", tuple(c[i] - d[i] / 2 for i in range(3)), tuple(c[i] + d[i] / 2 for i in range(3))


def analizza():
    pezzi, errori, avvisi = [], [], []
    pin_mondo = {}
    for chiave, m in MODULI.items():
        for nome in m.pin_loc:
            pin_mondo[m.pin(nome)] = (chiave, nome)

    # pezzi e tipo delle estremità
    for nome, r in RETI.items():
        segs = []
        for k, t in enumerate(r.tratti):
            for i in range(len(t) - 1):
                segs.append((k, i, t[i], t[i + 1]))
        for k, i, a, b in segs:
            d = sub(b, a)
            if sum(1 for c in d if abs(c) > TOL) != 1:
                errori.append(f"{nome}: segmento non parallelo a un asse {a} -> {b}")
        for k, i, a, b in segs:
            p = Pezzo(f"{nome}-{len([q for q in pezzi if q.rete == nome]) + 1:02d}", nome, a, b, gruppo=r.gruppi[k])
            t = r.tratti[k]
            for lato, punto, vicino in (("a", a, i - 1 if i > 0 else None), ("b", b, i + 1 if i + 1 < len(t) - 1 else None)):
                tipo = None
                chiuso = t[0] == t[-1]
                if lato == "a" and i > 0:
                    tipo = "battuta"
                elif lato == "b" and i < len(t) - 2:
                    tipo = "passante"
                elif chiuso:
                    tipo = "battuta" if lato == "b" else "passante"
                elif punto in pin_mondo:
                    tipo = "pin"
                elif abs(punto[2]) < TOL and punto in [tonda(f) for f in r.fori]:
                    tipo = "base"
                elif punto in [tonda(f) for f in r.liberi]:
                    tipo = "libero"
                elif punto in r.teste:
                    tipo = "testa"
                else:
                    for k2, i2, a2, b2 in segs:
                        if (k2, i2) != (k, i) and (sul_segmento(punto, a2, b2) or punto in (a2, b2)):
                            tipo = "battuta"
                            break
                if tipo is None:
                    errori.append(f"{nome}: estremità scoperta in {punto}")
                    tipo = "?"
                setattr(p, "tipo_" + lato, tipo)
            pezzi.append(p)

    # lunghezza minima
    for p in pezzi:
        if p.taglio < PEZZO_MIN - TOL:
            errori.append(f"{p.codice}: pezzo da {p.taglio:.1f} mm (minimo {PEZZO_MIN:.0f})")
            CRITICITA["pezzi"].add(p.codice)

    # distanze tra reti diverse
    for i, p in enumerate(pezzi):
        for q in pezzi[i + 1:]:
            if p.rete == q.rete:
                continue
            d = distanza_segmenti(p.a, p.b, q.a, q.b)
            if d < DISTANZA_MIN - 1e-3:
                errori.append(f"{p.codice} e {q.codice}: assi a {d:.2f} mm (minimo {DISTANZA_MIN})")
                CRITICITA["pezzi"].update((p.codice, q.codice))

    # attraversamenti di schede e ingombri
    for p in pezzi:
        for chiave, m in MODULI.items():
            lo, hi = m.scatola()
            if not segmento_in_scatola(p.a, p.b, lo, hi, R_FILO):
                continue
            ok = False
            for e in (p.a, p.b):
                if pin_mondo.get(e, (None,))[0] == chiave:
                    d = sub(p.b, p.a)
                    ok = norma(cross(d, m.n)) < TOL
            if not ok:
                errori.append(f"{p.codice} attraversa {m.nome}")
                CRITICITA["pezzi"].add(p.codice)
                CRITICITA["oggetti"].add(m.nome)
        for nome_o, lo, hi in ostacoli():
            if segmento_in_scatola(p.a, p.b, lo, hi, R_FILO):
                if p.rete.startswith("BATT") and nome_o.startswith("batteria"):
                    continue
                errori.append(f"{p.codice} tocca {nome_o}")
                CRITICITA["pezzi"].add(p.codice)
                CRITICITA["oggetti"].add(nome_o)

    # schede che si sovrappongono (ingombri allargati di GIOCO_SCHEDE)
    def sovrapposte(a, b):
        return all(a[0][i] < b[1][i] + GIOCO_SCHEDE and b[0][i] < a[1][i] + GIOCO_SCHEDE for i in range(3))

    def segnala(na, sa, nb, sb):
        errori.append(f"{na} e {nb}: ingombri a meno di {GIOCO_SCHEDE} mm")
        CRITICITA["oggetti"].update((na, nb))
        # zona del contatto: intersezione delle scatole allargate del gioco
        lo = tuple(max(sa[0][i], sb[0][i]) - GIOCO_SCHEDE for i in range(3))
        hi = tuple(min(sa[1][i], sb[1][i]) + GIOCO_SCHEDE for i in range(3))
        CRITICITA["zone"].append((f"{na} / {nb}", lo, hi))
    elenco = [(m.nome, m.scatola()) for m in MODULI.values()]
    for i, (na, sa) in enumerate(elenco):
        for nb, sb in elenco[i + 1:]:
            if sovrapposte(sa, sb):
                segnala(na, sa, nb, sb)
        for nome_o, lo, hi in ostacoli():
            if sovrapposte(sa, (lo, hi)):
                segnala(na, sa, nome_o, (lo, hi))

    # ogni rete tocca tutti i suoi pin ed è tutta collegata
    for nome, r in RETI.items():
        estremi = {pt for t in r.tratti for pt in t}
        for chiave, pn in r.pin:
            if MODULI[chiave].pin(pn) not in estremi:
                errori.append(f"{nome}: non arriva a {MODULI[chiave].nome} {pn}")
        segs = [(a, b) for t in r.tratti for a, b in zip(t, t[1:])]
        gruppi = list(range(len(segs)))
        def radice(i):
            while gruppi[i] != i:
                i = gruppi[i]
            return i
        for i, (a, b) in enumerate(segs):
            for j, (c, d) in enumerate(segs[:i]):
                if a in (c, d) or b in (c, d) or sul_segmento(a, c, d) or sul_segmento(b, c, d) \
                        or sul_segmento(c, a, b) or sul_segmento(d, a, b):
                    gruppi[radice(i)] = radice(j)
        # due pin della stessa rete sullo stesso modulo sono già collegati dentro la scheda
        for c1, p1 in r.pin:
            for c2, p2 in r.pin:
                if c1 == c2 and p1 != p2:
                    i1 = [i for i, (a, b) in enumerate(segs) if MODULI[c1].pin(p1) in (a, b)]
                    i2 = [i for i, (a, b) in enumerate(segs) if MODULI[c2].pin(p2) in (a, b)]
                    if i1 and i2:
                        gruppi[radice(i1[0])] = radice(i2[0])
        if len({radice(i) for i in range(len(segs))}) > 1:
            errori.append(f"{nome}: la rete è spezzata in più parti")

    stimati = sorted({m.nome for m in MODULI.values() if m.stato == "stimato"})
    if stimati:
        avvisi.append("misure ancora stimate: " + ", ".join(stimati))
    return pezzi, errori, avvisi


# ================================================================== USCITE
def scrivi_csv(pezzi):
    with open(QUI / "segmenti.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["gruppo", "codice", "rete", "asse", "lunghezza_assi_mm", "taglio_mm", "estremo_A", "estremo_B",
                    "A_x", "A_y", "A_z", "B_x", "B_y", "B_z"])
        for p in sorted(pezzi, key=lambda p: GRUPPI.index(p.gruppo)):
            w.writerow([NOMI_GRUPPI[p.gruppo], p.codice, p.rete, p.asse, f"{p.lunghezza:.1f}", f"{p.taglio:.1f}", p.tipo_a, p.tipo_b,
                        *p.a, *p.b])


COLORI_SCAD = {"nero": [0.1, 0.1, 0.1], "blu": [0.1, 0.25, 0.7], "verde": [0.05, 0.45, 0.2],
               "bianco": [0.92, 0.92, 0.9], "millefori": [0.75, 0.6, 0.3]}


ROSSO = [0.9, 0.05, 0.05]


def scrivi_scad(pezzi, errori=()):
    r = []
    rosso = lambda nome, col: f'(criticita ? {ROSSO} : {col})' if nome in CRITICITA["oggetti"] else str(col)
    r.append("// Metronomus: modello 3D di controllo, GENERATO da fili/geometria.py: non modificarlo a mano.")
    r.append("// Misure dei moduli in fili/moduli.yaml. Assi in mm, z = 0 piano della base.\n")
    r.append("/* [Vista] */\nteca = true;\nmostra_vetro = true;\nmostra_scala = true;\nangolo_pendolo = -14;\n"
             "// criticità (errori dei controlli) in rosso, con le zone di contatto evidenziate\ncriticita = true;\n"
             "// nomi delle schede e dei componenti, su cartellini rivolti verso il fronte\netichette = true;\n")
    r.append("// " + (f"{len(errori)} criticità:" if errori else "nessuna criticità"))
    for e in errori:
        r.append(f"//   - {e}")
        r.append(f'if (criticita) echo("CRITICITÀ: {e}");')
    r.append("")
    r.append("$fn = 24;\nR = %.2f;\n" % R_FILO)
    r.append("""module seg(a, b, r = R) { v = b - a; l = norm(v);
    if (l > 0) translate(a) rotate([0, acos(v[2] / l), atan2(v[1], v[0])]) cylinder(r = r, h = l, $fn = 12); }
module etichetta(punto, testo, alto, dx = 0) {  // cartellino rivolto verso il fronte (-y): filo guida su di alto, poi di lato di dx
    color([0.2, 0.2, 0.2]) { seg(punto, punto + [0, 0, alto], 0.25); seg(punto + [0, 0, alto], punto + [dx, 0, alto], 0.25); }
    translate(punto + [dx, 0, alto]) rotate([90, 0, 0]) {
        color("white") translate([-len(testo) * 1.45 - 1, -1.2, -0.3]) cube([len(testo) * 2.9 + 2, 6.4, 0.3]);
        color([0.1, 0.1, 0.1]) linear_extrude(0.4) text(testo, size = 4, halign = "center", font = "Liberation Sans:style=Bold");
    } }
module scheda(o, u, v, n, d, sp, alt, col) {
    color(col) multmatrix([[u[0], v[0], n[0], o[0]], [u[1], v[1], n[1], o[1]], [u[2], v[2], n[2], o[2]], [0, 0, 0, 1]]) {
        translate([0, 0, -sp]) cube([d[0], d[1], sp]);
        color([0.15, 0.15, 0.15]) translate([d[0] * 0.3, d[1] * 0.3, 0]) cube([d[0] * 0.4, d[1] * 0.4, alt]);
    } }
""")
    # base e teca
    lo, hi = BASE["min"], BASE["max"]
    r.append(f"color([0.55, 0.33, 0.17]) translate({list(lo)}) cube({[hi[i] - lo[i] for i in range(3)]});")
    r.append(f"if (teca && mostra_vetro) color([0.8, 0.95, 1.0, 0.15]) translate([{lo[0] + 5}, {lo[1] + 5}, 0]) "
             f"difference() {{ cube([{hi[0] - lo[0] - 10}, {hi[1] - lo[1] - 10}, 220]); "
             f"translate([3, 3, -1]) cube([{hi[0] - lo[0] - 16}, {hi[1] - lo[1] - 16}, 218]); }}")
    # moduli
    for m in MODULI.values():
        col = rosso(m.nome, COLORI_SCAD[m.colore])
        r.append(f"scheda({list(m.origine)}, {list(m.u)}, {list(m.v)}, {list(m.n)}, {list(m.dimensioni)}, "
                 f"{m.spessore}, {m.altezza}, {col});  // {m.nome}")
    # motore, pendolo, batterie, pannello
    ax, ay, az = MOTORE["asse"]
    rr, ll = MOTORE["diametro"] / 2, MOTORE["lunghezza"]
    r.append(f"color({rosso('motore', [0.75, 0.75, 0.78])}) seg([{ax}, {ay}, {az}], [{ax}, {ay - ll}, {az}], {rr});")
    ym = ay + MAGNETE["sporgenza"]
    r.append(f"color({rosso('magnete', [0.35, 0.35, 0.4])}) seg([{ax}, {ym}, {az}], [{ax}, {ym + MAGNETE['spessore']}, {az}], "
             f"{MAGNETE['diametro'] / 2});  // magnete dell'AS5600")
    r.append(f"color([0.75, 0.75, 0.78]) seg([{ax}, {ay - ll}, {az}], [{ax}, {ay - ll - 4}, {az}], 3);")
    yp = ay - ll - 5.5
    r.append(f"translate([{ax}, {yp}, {az}]) rotate([0, angolo_pendolo, 0]) {{ color([1, 0.75, 0.25]) "
             f"cylinder(r = 1.1, h = 108); color([0.85, 0.45, 0.25]) translate([2.2, 0, 0]) cylinder(r = 0.2, h = 108); "
             f"color([0.8, 0.65, 0.3]) translate([0, 0, {R_CONTATTO - 5}]) cylinder(r = {R_COLLARE}, h = 10); }}  // collare ARMA")
    for i, bt in enumerate(BATTERIE):
        cx, cy, cz = bt["centro"]
        r.append(f"color({rosso(f'batteria {i + 1}', [0.25, 0.55, 0.95])}) seg([{cx}, {cy - bt['lunghezza'] / 2}, {cz}], "
                 f"[{cx}, {cy + bt['lunghezza'] / 2}, {cz}], {bt['diametro'] / 2});")
    c, d = PANNELLO["centro"], PANNELLO["dimensioni"]
    r.append(f"color({rosso('pannello', [0.6, 0.38, 0.2])}) translate({[c[i] - d[i] / 2 for i in range(3)]}) cube({list(d)});")
    r.append(f"""if (mostra_scala) for (i = [0 : 38]) {{ t = -40 + 80 * i / 38; l = (i % 5 == 0) ? 104 : 99;
    color("white") seg([{ax} + 92 * sin(t), {c[1] - d[1] / 2 - 0.1}, {az} + 92 * cos(t)], [{ax} + l * sin(t), {c[1] - d[1] / 2 - 0.1}, {az} + l * cos(t)], 0.4); }}""")
    # fili
    colori_rete = {"TELAIO": [0.7, 0.45, 0.3], "PANNELLO": [0.7, 0.45, 0.3]}
    for p in pezzi:
        col = colori_rete.get(p.rete, [0.85, 0.45, 0.25])
        if p.codice in CRITICITA["pezzi"]:
            r.append(f"color(criticita ? {ROSSO} : {col}) seg({list(p.a)}, {list(p.b)}, criticita ? R * 1.6 : R);  // {p.codice} CRITICO")
        else:
            r.append(f"color({col}) seg({list(p.a)}, {list(p.b)});  // {p.codice}")
    giunti = sorted({pt for p in pezzi for pt in (p.a, p.b)})
    r.append("color([0.75, 0.75, 0.72]) for (g = " + str([list(g) for g in giunti]) + ") translate(g) sphere(r = R * 1.4, $fn = 12);")
    # etichette: sopra il centro di ogni scheda, altezze sfalsate per non coprirsi
    # (alto, spostamento laterale): i cartellini escono da dietro al motore e non si coprono
    posti = {"AS5600": (20, 0), "ESP32-S3": (76, 36), "SimpleFOC Mini": (16, 0), "Mini-360": (12, -28),
             "MT3608": (14, 0), "Scheda servizi": (42, 0)}
    for m in MODULI.values():
        lo, hi = m.scatola()
        punto = [round((lo[0] + hi[0]) / 2, 2), round(lo[1], 2), round(hi[2], 2)]
        alto, dx = posti.get(m.nome, (20, 0))
        r.append(f'if (etichette) etichetta({punto}, "{m.nome}", {alto}, {dx});')
    r.append(f'if (etichette) etichetta([{ax - rr - 2}, {ay - ll / 2}, {az + rr}], "Motore 1503", 12);')
    r.append(f'if (etichette) etichetta([{ax}, {ay + MAGNETE["sporgenza"]}, {az - MAGNETE["diametro"] / 2}], "magnete", -12, -30);')
    for i, bt in enumerate(BATTERIE):
        cx, cy, cz = bt["centro"]
        r.append(f'if (etichette) etichetta([{cx}, {cy - bt["lunghezza"] / 2}, {cz + bt["diametro"] / 2}], "18350", 8);')
    r.append(f'if (etichette) etichetta([{BASE["min"][0] + 55}, {BASE["min"][1]}, 0], "TP4056, encoder e vibrazione sotto la base", 6);')
    for nome, lo, hi in CRITICITA["zone"]:
        r.append(f"if (criticita) color([1, 0, 0, 0.45]) translate({[round(c, 3) for c in lo]}) "
                 f"cube({[round(hi[i] - lo[i], 3) for i in range(3)]});  // contatto {nome}")
    (RADICE / "modello").mkdir(exist_ok=True)
    (RADICE / "modello" / "metronomus.scad").write_text("\n".join(r) + "\n", encoding="utf-8")


def fili_flessibili():
    """Lunghezza consigliata dei fili flessibili: distanza massima tra la fine del rame e l'attacco
    sul pendolo nell'arco ±ANGOLO_FC, più 5 mm di lasco. LED attaccati alla base del tubo (raggio 8),
    ARMA al collare (raggio R_CONTATTO)."""
    ax, _, az = ASSE
    out = {}
    for nome in ("LED_A", "LED_K", "ARMA"):
        fine = rete(nome).liberi[0]
        raggio = R_CONTATTO if nome == "ARMA" else 8.0
        dmax = max(norma(sub(fine, (ax + raggio * math.sin(math.radians(t)), Y_PENDOLO, az + raggio * math.cos(math.radians(t)))))
                   for t in range(-int(ANGOLO_FC), int(ANGOLO_FC) + 1))
        out[nome] = math.ceil(dmax + 5)
    return out


def costruisci():
    return analizza()


if __name__ == "__main__":
    pezzi, errori, avvisi = analizza()
    scrivi_csv(pezzi)
    scrivi_scad(pezzi, errori)
    reti_el = [n for n in RETI if n not in ("TELAIO", "PANNELLO")]
    giunti = len({pt for p in pezzi for pt in (p.a, p.b)})
    print(f"{len(pezzi)} pezzi ({sum(1 for p in pezzi if p.rete in reti_el)} elettrici), "
          f"{sum(p.taglio for p in pezzi) / 1000:.2f} m di filo, pezzo più corto "
          f"{min(p.taglio for p in pezzi):.1f} mm, {len(reti_el)} reti")
    for g in GRUPPI:
        sel = [p for p in pezzi if p.gruppo == g]
        print(f"  {NOMI_GRUPPI[g]:<16} {len(sel):3d} pezzi  {sum(p.taglio for p in sel) / 10:6.1f} cm")
    print("  fili flessibili (mm): " + ", ".join(f"{k} {v}" for k, v in fili_flessibili().items())
          + f"; finecorsa a ±{ANGOLO_FC:.0f}°, paletti alti {Z_FC} mm, collare a {R_CONTATTO} mm dall'asse")
    for a in avvisi:
        print("AVVISO:", a)
    for e in errori:
        print("ERRORE:", e)
    sys.exit(1 if errori else 0)
