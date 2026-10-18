# Changelog

## 2026-10-18 (sera)
- **Q1 e Q3 diventano 2N3904** del kit già in casa (al posto degli AO3400): millefori ridisposta e controllata, schema (simbolo NPN, solo SVG), pinout e BOM aggiornati, PDF 1:1 rigenerato. Da comprare resta solo l'AO3401.
- Misure col calibro di ESP32, AS5600, MT3608, Mini‑360, SimpleFOC, TP4056, celle e filo in fili/moduli.yaml.
- **PDF 1:1 del rame** (produzione/piano-rame.pdf, da fili/piano_pdf.py): righello, dima di foratura con fori passanti e ciechi, viste 1:1 per gruppo, pagina della millefori, giunti, distinta con i pezzi in scala reale.
- **Verifiche OpenSCAD** (fili/verifica_scad.py): pezzi tagliati ricostruiti dai dati del PDF, controlli di lunghezze, giunti, corti e contatto delle celle; colori per isole saldate; nomi di schede e pin; verifiche per gradi `alimentazione` ed `esp32`.
- Sotto la base: TP4056 ed encoder in scassi, cavetti in canaline, rame elettrico passante. Modulo vibrazione sopra la base. Barre delle batterie saldate sui poli (celle 35 × 18).
- Scheda servizi su millefori 17 × 6 (fili/millefori.py, con controllo della netlist). Encoder senza RC: antirimbalzo nel firmware.
- Geometria: 95 pezzi, 3,36 m, zero errori.

## 2026-10-18
- Scala su ±30° (finecorsa ±35°): pannello e colonne ricavati dall'arco, larghi 124 mm. Base 150 × 90 mm: geometria senza errori (93 pezzi, 3,16 m).
- Risposte di Fabio registrate (domande 7–18). Base 150 × 90 mm con controllo della teca; magnete da 2 mm a filo, AS5600 arretrato: risolti i contatti con motore e magnete. Driver v1.0 confermato dalla serigrafia. Ritorno di massa spostato vicino a driver e MT3608 (ruolo elettronica), condensatori aggiuntivi. Resta il pannello della scala, troppo largo (domanda 19).
- Stop di emergenza: paletti di rame a ±45° (finecorsa meccanici, rete STOP verso EN del driver e GPIO43) e collare di ottone sul pendolo (rete ARMA da GPIO44). Schema rev. 0.2.2 (solo SVG), pinout, BOM, rame (93 pezzi, 3,19 m) e modello 3D aggiornati.
- Rame a bus: geometria.py divisa in bus (sollevati, con 3 mm di sporgenza per il gioco di montaggio) e discese per scheda; distinta segmenti.csv in ordine di montaggio (colonna `gruppo`). 84 pezzi, 2,72 m.
- Decisioni: AS5600 collegato direttamente, filamenti LED con 15–20 mm di filo flessibile. Nuove domande: stop di emergenza, masse separate.
- Fine sessione: STATO riscritto, nuove domande aperte (sporgenza dell'albero, AS5600, serigrafia del SimpleFOC).
- Modello OpenSCAD: cartellini con il nome di schede e componenti (interruttore `etichette`).
- Modello assegnato a ogni ruolo e comando (Opus per l'elettronica, Sonnet per coordinatore, piano fili e /fine-sessione, Haiku per git-readme e /stato).
- La scheda ESP32 è una **S3 SuperMini** (non una C3): moduli.yaml con le misure del disegno quotato Nologo (23,50 × 18,00, 2 file da 9 pin), nuovo pinout, schema rev. 0.2.1, BOM e foto rinominate.
- Rame: S3 ruotata di 90°, scheda servizi riordinata; geometria rilanciata: 84 pezzi, 2,67 m, tutti i controlli superati.
- TP4056: piazzole e dimensioni dalla foto quotata del venditore (26,1 × 17,4).
- Modello OpenSCAD: criticità in rosso (pezzi, schede e ostacoli coinvolti, volumi rossi sulle zone di contatto, elenco nella console), interruttore `criticita`; aggiunto il magnete dell'AS5600 (sporgenza dell'albero in moduli.yaml, `sporgenza_albero`, per ora 0).
- geometria.py: nuovo controllo sulle schede che si sovrappongono (tra loro e con motore, batterie e pannello, gioco 0,5 mm). Segnala AS5600 e motore a 0,2 mm: il magnete non è ancora nel modello.
- SimpleFOC Mini dal disegno quotato del produttore (26 × 21,5, fori Ø2 a 22 × 17,5). Toccava il Mini‑360: driver spostato di un passo, PWM su GPIO7/6/5, PWR_EN su 4, pulsante su 8.

## 2026-10-17
- Comandi di Claude Code `/stato` e `/fine-sessione` (come nel YouTube Controller), stato del progetto in docs/STATO.md, ruoli copiati in .claude/agents/.
- Disposizione compatta: misure dei moduli in fili/moduli.yaml, geometria unica in fili/geometria.py con i controlli (pezzi ≥ 10 mm, distanze, schede attraversate), distinta fili/segmenti.csv. Modello OpenSCAD e render ora generati dalla stessa geometria.
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
