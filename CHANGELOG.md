# Changelog

## 2026-10-17
- Modello 3D di controllo in OpenSCAD (modello/metronomus.scad), stessa disposizione del render.
- Tolti dalla lista acquisti portapile e magnete (incluso con l'AS5600); il modulo vibrazione ha già la pull‑down su IN.
- Render con la teca di vetro (render/concept-teca.png: `python render/concept.py teca`), encoder sul bordo della base e venatura del legno migliorata.
- Confermato il motorino a vibrazione come tic: niente relè.
- Letargo con il pulsante dell'encoder al posto dell'interruttore: LDO sempre acceso, MOSFET sulla parte di potenza, pulsante su GPIO2. Schema rev. 0.2.
- Primo render di concept (render/concept.png, generato da render/concept.py).
- Primo schema elettrico (hardware/schema.pdf/png/svg, generato da schema.py) e tabella delle reti.
- Aggiunto il motorino a vibrazione per il tic (GPIO 8) e il secondo filamento LED.
- Scelto l'ESP32‑C3 SuperMini; prima bozza del pinout in hardware/pinout.md.
- LED identificato: filamento LED rigido.
- Rame: niente pieghe, solo segmenti dritti saldati. Sostituita la taratura delle pieghe con le prove di taglio e giunto.
- Componenti identificati dalle foto; BOM riscritta. Batterie in parallelo (1S) con TP4056, MT3608 a 12 V e Mini‑360 alimentato dai 12 V.
- Step‑down Mini‑360 disponibile, da tarare a 3,3 V per l'ESP32.
- Boost MT3608 disponibile, da tarare a 12 V.
- Motore 1503 (7,4 V, 0,5 Ω) confermato, con limite di tensione FOC nel firmware.
- Batteria 2 × 18350 (2S) e sensore AS5600 confermati; aggiornata la catena di alimentazione.
- Tutte le decisioni riunite nell'unico file docs/decisioni.md.
- Deciso l'indicatore del tempo: il pendolo punta su una scala Maelzel incisa al laser.
- Identificato il driver: SimpleFOC Mini v1.0 (DRV8313). Aggiunto il vincolo di alimentazione motore ≥ 8 V.
- Creato il progetto: struttura cartelle, README, ruoli dei subagenti.
- Analisi iniziale: punti critici (driver/motore per il moto a pendolo), parti mancanti, idee da aggiungere.
- Procedura di taratura della deduzione di piega per il filo da 1 mm.
