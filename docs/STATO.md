# Stato del progetto

_Aggiornato il 18/10/2026 (fine sessione)._

## Fase attuale
Fase 3 · disposizione del circuito in rame: la geometria passa tutti i controlli, ma 5 moduli sono ancora su misure stimate. In parallelo la fase 1 (parti da comprare).

## Fatto finora
- Componenti e BOM ([hardware/bom.md](../hardware/bom.md)): **ESP32‑S3 SuperMini**, SimpleFOC Mini v1.0, motore 1503, AS5600, EC11, TP4056 USB‑C, MT3608, Mini‑360, 2 × 18350 in parallelo, 2 filamenti LED da 3 V, motorino a vibrazione (solo il tic, niente suono). Deve girare a batteria.
- Pinout ([hardware/pinout.md](../hardware/pinout.md)): PWM 7/6/5, I2C SCL 1 / SDA 2, PWR_EN 4, vibrazione 3, encoder 12/13/8, LED 10, ADC 9, stop 43 (STOP) / 44 (ARMA). Schema rev. 0.2.2, aggiornato solo l'SVG.
- Indicatore del tempo: il pendolo punta su una scala Maelzel su **±30°**; tic con motorino a vibrazione sotto la base; base di legno **150 × 90 mm** in una teca di vetro.
- **Stop di emergenza**: paletti di rame a ±35° (finecorsa meccanici) e collare di ottone sul pendolo; con ARMA = 0 il contatto spegne il driver in hardware (EN a massa, R9 10 kΩ), ARMA = 1 solo all'avvio.
- Rame **a bus** ([fili/geometria.py](../fili/geometria.py)): discese per scheda, bus sollevati con 3 mm di sporgenza per il gioco di montaggio, distinta in ordine di montaggio. 93 pezzi, 3,16 m, **zero errori** (pezzi ≥ 10 mm, assi ≥ 2,5 mm, nessun filo attraverso le schede, schede senza sovrapposizioni, tutto dentro la teca).
- AS5600 e magnete risolti: magnete da 2 mm a filo del motore, sensore a 1 mm. Driver v1.0 confermato dalla serigrafia (M1‑M2‑M3 da sinistra).
- Masse: anello unico, foro del ritorno batteria tra MT3608 e driver (parere del ruolo elettronica). Modello OpenSCAD con criticità in rosso e cartellini.

## Prossimi passi
1. Misure reali dei moduli col calibro (AS5600 senza datasheet, Mini‑360 e MT3608 per le piazzole, spessore PCB dell'S3, diametro del filo, fori del motore): [fili/misure-da-prendere.md](../fili/misure-da-prendere.md).
2. Schema rev. 0.3: filamenti in serie (via R7), scheda servizi, DIR dell'AS5600, i condensatori 220–470 µF e 100 nF già scritti in schema.md; rigenerare PDF/PNG (serve cairosvg).
3. Ordinare le parti mancanti (LDO, AO3401/AO3400, resistenza R9, condensatori, prolunga USB‑C, filo di rame, ottone per il collare).
4. Pagine del PDF 1:1 per ogni gruppo di montaggio; poi montaggio una scheda alla volta, alimentazione per prima.
5. Firmware su breadboard: SimpleFOC in posizione, pendolo, scala Maelzel, letargo, armamento dello stop.

## In attesa da Fabio
- Domanda 14: datasheet o misure dell'AS5600; interasse dei fori M2 del motore.
- Misure di Mini‑360 e MT3608; spessore del PCB dell'S3; diametro reale del filo.
- Modulo vibrazione (pin header a passo 2,54).
- Col tester: pull‑up SDA/SCL e DIR dell'AS5600; Vf dei filamenti LED.
- Fili flessibili verso il pendolo (29–35 mm) e mozzo/collare: li progetta Fabio.

## Problemi aperti
- Moduli ancora su misure stimate: AS5600, ESP32‑S3, MT3608, Mini‑360, SimpleFOC Mini. Il PDF di produzione non si genera finché lo sono.
- Render in `render/` e schema PDF/PNG fermi alla versione C3: servono `bpy` e `cairosvg`.
- Rigidità del telaio del motore in filo da 1 mm: forse serve filo più grosso o ottone.
- GPIO43 (TX di UART0) usato per STOP: da provare su breadboard che l'avvio non disturbi il driver.
