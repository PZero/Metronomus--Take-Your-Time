# Stato del progetto

_Aggiornato il 18/10/2026._

## Fase attuale
Fase 3 · disposizione del circuito in rame, in attesa delle misure reali dei moduli. In parallelo la fase 1 (parti da comprare).

## Fatto finora
- Componenti e BOM ([hardware/bom.md](../hardware/bom.md)): **ESP32‑S3 SuperMini** (non C3, corretto il 18/10), SimpleFOC Mini, motore 1503, AS5600, EC11, TP4056 USB‑C, MT3608, Mini‑360, 2 × 18350 in parallelo, 2 filamenti LED, motorino a vibrazione.
- Pinout dell'S3 ([hardware/pinout.md](../hardware/pinout.md)): PWM 7/6/5, I2C SCL 1 / SDA 2, PWR_EN 4, vibrazione 3, encoder 12/13/8, LED 10, ADC 9, stop 43 (STOP) / 44 (ARMA). Schema rev. 0.2.2 (aggiornato solo l'SVG).
- Indicatore del tempo: il pendolo punta su una scala Maelzel incisa. Tic: motorino a vibrazione sotto la base. Base di legno in una teca di vetro.
- Misure dai disegni quotati: ESP32‑S3 (Nologo), SimpleFOC Mini (produttore), TP4056 (foto quotata del venditore), in [fili/moduli.yaml](../fili/moduli.yaml).
- Rame **a bus** (decisione del 18/10): discese per scheda e bus sollevati con 3 mm di sporgenza per il gioco; distinta in ordine di montaggio. [fili/geometria.py](../fili/geometria.py), 93 pezzi, 3,16 m, zero errori. Stop di emergenza con paletti a ±35° e collare armato da GPIO44 (schema rev. 0.2.2). Controlli: pezzi ≥ 10 mm, assi ≥ 2,5 mm, nessun filo attraverso le schede, **schede che non si sovrappongono** (gioco 0,5 mm, anche con motore, magnete, batterie e pannello).
- Modello OpenSCAD ([modello/metronomus.scad](../modello/metronomus.scad)): criticità in rosso e cartellini con i nomi (interruttori `criticita` ed `etichette`); anteprima in `modello/criticita.png`.
- Ruoli con il modello adatto: elettronica Opus, coordinatore e piano‑fili Sonnet, git‑readme Haiku.

## Prossimi passi
0. Montaggio una scheda alla volta, alimentazione per prima: pagina del PDF 1:1 per ogni gruppo (struttura, bus, batterie, MT3608, Mini‑360, servizi, ESP32, driver, AS5600).
1. Misure reali dei moduli col calibro: oggi la geometria è senza errori, ma ancora su misure stimate.
2. Misure mancanti: AS5600 (nessun datasheet), Mini‑360 e MT3608 (piazzole), diametro reale del filo, fori della base del motore ([fili/misure-da-prendere.md](../fili/misure-da-prendere.md)).
3. Schema rev. 0.3: filamenti in serie (via R7), scheda servizi, DIR dell'AS5600; rigenerare PDF/PNG (serve cairosvg).
4. Ordinare le parti mancanti (LDO, AO3401/AO3400, prolunga USB‑C, filo di rame).
5. Firmware su breadboard: SimpleFOC in posizione, pendolo, scala Maelzel, letargo.

## In attesa da Fabio
- Interasse dei fori M2 del motore.
- Datasheet o misure di AS5600, Mini‑360, MT3608; spessore del PCB dell'S3; diametro reale del filo.
- Modulo vibrazione (pin header standard a passo 2,54).
- Col tester: pull‑up SDA/SCL e DIR dell'AS5600; Vf dei filamenti LED.

## Problemi aperti
- `geometria.py` senza errori (base 150 × 90, scala ±30°), ma con 5 moduli ancora su misure stimate.
- Render in `render/` e schema PDF/PNG fermi alla versione C3: servono `bpy` e `cairosvg`.
- Rigidità del telaio del motore in filo da 1 mm: forse serve filo più grosso o ottone.
- Ponticello EN–3V3 del driver fatto sulla scheda (pezzo sotto i 10 mm, unica eccezione).
