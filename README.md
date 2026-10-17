# Metronomus · Take Your Time

> Un metronomo artistico: un pendolo di luce mosso da un motore brushless, governato da un ESP32, con il circuito esposto in filo di rame da 1 mm piegato ad angoli retti.

**Stato:** 🟡 Fase 1 · identificazione dei componenti (vedi [roadmap](docs/roadmap.md))

---

## Indice
1. [Il concept](#il-concept)
2. [Come funziona](#come-funziona)
3. [Componenti](#componenti)
4. [Schema a blocchi](#schema-a-blocchi)
5. [Elettronica](#elettronica)
6. [Firmware](#firmware)
7. [Il circuito in rame](#il-circuito-in-rame)
8. [Produzione: PDF 1:1](#produzione-pdf-11)
9. [Uso](#uso)
10. [Struttura del repository](#struttura-del-repository)
11. [Come lavoriamo: i ruoli](#come-lavoriamo-i-ruoli)
12. [Roadmap e decisioni](#roadmap-e-decisioni)

---

## Il concept

Un metronomo che è anche una scultura. Al posto dell'asta con il peso c'è un **tubo LED da 5 cm** fissato all'albero di un **motore brushless**, che oscilla come un pendolo e si accende a ogni battito. Tutta l'elettronica è a vista: i collegamenti non stanno su un circuito stampato ma sono **fili di rame da Ø 1 mm** piegati a 90° con precisione millimetrica, che fanno anche da struttura.

## Come funziona

- **Ruoti l'encoder** → cambia il tempo (BPM): il pendolo si ferma e fa da lancetta su una scala Maelzel incisa al laser sulla base. Quando lasci l'encoder riparte a battere il nuovo tempo. Niente display ([dettagli](docs/indicatore-tempo.md)).
- **L'ESP32** calcola la traiettoria del pendolo e comanda il **driver** del motore.
- **Il sensore magnetico** legge la posizione dell'albero, così il pendolo sa dove si trova e quando invertire.
- **Il LED** si accende o pulsa sul battito.
- **La batteria** si ricarica dalla presa USB.

Il movimento ideale è sinusoidale, come un pendolo vero: `θ(t) = A · sin(π · BPM/60 · t)`. Ogni estremo dell'oscillazione è un battito.

## Componenti

Elenco completo e modelli in [hardware/bom.md](hardware/bom.md).

| Componente | Modello | Stato |
|---|---|---|
| ESP32 | da identificare | ✅ disponibile |
| Driver brushless | SimpleFOC Mini v1.0 (DRV8313, 8–30 V) | ✅ disponibile |
| Motore brushless | da identificare | ✅ disponibile |
| Batteria | da identificare | ✅ disponibile |
| Caricatore USB | da identificare | ✅ disponibile |
| Rotary encoder | da identificare | ✅ disponibile |
| LED a tubo 5 cm | da identificare | ✅ disponibile |
| Sensore magnetico | da identificare | ✅ disponibile |
| Regolatore 3,3 V, interruttore, MOSFET LED, partitore | proposti | ❓ da confermare |

## Schema a blocchi

```
 USB ──► [Caricatore] ──► [Batteria] ──► [Interruttore] ─┬─► [Regolatore 3,3 V] ──► ESP32
                                                         └─► [Boost?] ──► [Driver BLDC] ──► Motore
                                                                                               │
 [Rotary encoder] ──► ESP32 ◄── [Sensore magnetico] ◄── magnete sull'albero ◄───────────────────┤
                       │                                                                       │
                       └──► [MOSFET] ──► LED a tubo (sull'albero) ◄────────────────────────────┘
```

## Elettronica

**Driver:** SimpleFOC Mini v1.0, basato su DRV8313. Il motore va alimentato a 8–30 V (consigliati 10–12 V), la logica è a 3,3 V e si collega direttamente all'ESP32 con 3 PWM (IN1–IN3) più EN.

_Il resto è in definizione._ Analisi di partenza, punti critici e parti mancanti: [docs/analisi-iniziale.md](docs/analisi-iniziale.md).
Qui andranno: schema elettrico, pinout ESP32, alimentazione e autonomia.

## Firmware

_Da scrivere._ Base prevista: Arduino/PlatformIO + libreria [SimpleFOC](https://simplefoc.com) per il controllo del brushless.
Funzioni previste: BPM 40–208 sulla scala Maelzel (39 posizioni), modalità impostazione con il pendolo come lancetta, start/stop e tap tempo dal pulsante dell'encoder, LED sincronizzato, accento, misura batteria, auto‑spegnimento.

## Il circuito in rame

- Filo di rame Ø 1,0 mm, raddrizzato in trazione, solo tratti dritti e pieghe a 90°.
- Ogni filo è una rete elettrica (GND, VBAT, 3V3, segnali…) e ha un codice.
- Le lunghezze di taglio tengono conto della deduzione di piega, tarata con pieghe di prova: [fili/taratura.md](fili/taratura.md).
- Reti diverse corrono su piani separati (≥ 3 mm in aria) e si scavalcano senza toccarsi.
- Una dima incisa al laser tiene i fili in posizione durante la saldatura.

### Attrezzi
Pinza a becchi piatti (o piegatrice per filo), calibro, tronchesino a taglio piano, saldatore e stagno, morsa per raddrizzare, dima.

## Produzione: PDF 1:1

Quando il progetto sarà definito, in `produzione/` ci sarà un PDF da stampare **al 100%** (controllare il righello di 100 mm in prima pagina) con, per ogni filo: codice, rete, lunghezza di taglio, disegno in scala reale con i punti di piega numerati e la direzione, ordine di montaggio e punti di saldatura.

## Uso

_Da scrivere quando il firmware è pronto._

## Struttura del repository

```
Metronomus/
├── README.md              questa pagina
├── CHANGELOG.md           storico delle modifiche
├── CLAUDE.md              istruzioni per Claude in questo progetto
├── agenti/                i 4 ruoli (coordinatore, git-readme, elettronica, piano-fili)
├── docs/                  analisi, decisioni, roadmap, domande aperte
├── hardware/              BOM, schema, pinout
├── firmware/              codice ESP32
├── fili/                  geometria del circuito in rame, taratura
├── foto/                  foto dei componenti e del prototipo
└── produzione/            PDF 1:1 di taglio, piegatura e saldatura
```

## Come lavoriamo: i ruoli

Il progetto è organizzato in quattro ruoli, definiti in `agenti/`. Per usarli come subagenti di Claude Code basta copiare quei file in `.claude/agents/`.

| Ruolo | Si occupa di |
|---|---|
| **coordinatore** | Priorità, decisioni, roadmap, smistamento del lavoro |
| **git-readme** | README sempre completo, CHANGELOG, commit |
| **elettronica** | Componenti, schema, pinout, alimentazione, firmware |
| **piano-fili** | Geometria dei fili, distinta di taglio, piegature, dima, PDF 1:1 |

## Roadmap e decisioni

- [Roadmap](docs/roadmap.md)
- [Registro delle decisioni](docs/decisioni.md)
- [Domande aperte](docs/domande-aperte.md)
