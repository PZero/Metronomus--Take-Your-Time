# Stato del progetto

_Aggiornato il 18/10/2026 (fine sessione, sera)._

## Fase attuale
Fase 3 · piano del rame **pronto in PDF 1:1** (bozza solo per il modulo vibrazione, ancora da misurare). In parallelo la fase 1: parti da comprare.

## Fatto finora
- Componenti e BOM ([hardware/bom.md](../hardware/bom.md)): ESP32‑S3 SuperMini, SimpleFOC Mini v1.0, motore 1503, AS5600, EC11, TP4056 USB‑C, MT3608, Mini‑360, 2 × 18350 in parallelo, filamenti LED, modulo vibrazione.
- **Misure col calibro** in [fili/moduli.yaml](../fili/moduli.yaml): ESP32 (18 × 24, file a 16 mm), AS5600 (22,5², chip al centro), MT3608 (37,5 × 18), Mini‑360 (18 × 12), SimpleFOC (26 × 21,5), TP4056 (interassi), celle 35 × 18, filo 1,0.
- Geometria ([fili/geometria.py](../fili/geometria.py)): 95 pezzi, 3,36 m, zero errori.
- **PDF 1:1** ([produzione/piano-rame.pdf](../produzione/piano-rame.pdf), da `fili/piano_pdf.py`, 24 pagine): righello, dima di foratura (fori passanti/ciechi), viste 1:1 per gruppo, millefori, giunti, distinta con i pezzi in scala reale.
- **Verifiche in OpenSCAD** (`fili/verifica_scad.py`): ricostruiscono i pezzi tagliati dai dati del PDF e controllano lunghezze, giunti, corti, contatto delle celle; colori per isole saldate; per gradi: `alimentazione`, `esp32` (modello/verifica-*.scad).
- **Sotto la base**: TP4056 ed encoder in scassi, cavetti isolati in canaline da 4 mm; il rame elettrico attraversa la base e sporge 2 mm nella canalina.
- Modulo vibrazione **sopra** la base, incollato al legno, IN sotto il GPIO3.
- Batterie: barre di rame **saldate direttamente** sui poli.
- **Scheda servizi** su millefori 17 × 6 fori ([fili/millefori.py](../fili/millefori.py), netlist controllata): LDO MCP1700 TO‑92, Q1 e Q3 2N3904 TO‑92 (già in casa), AO3401 su adattatore SOT‑23, 2 ponticelli.
- Encoder senza RC: antirimbalzo nel firmware.

## Prossimi passi
1. Misure del modulo vibrazione → PDF definitivo (non più bozza).
2. Schema rev. 0.3: filamenti in serie (R6), scheda servizi con le sigle di millefori.py, DIR dell'AS5600, condensatori; rigenerare PDF/PNG (serve cairosvg).
3. Ordinare: MCP1700‑3302E TO‑92, AO3401 + 1 adattatore SOT‑23 (i 2N3904 ci sono già), resistenze (470 Ω, 10 kΩ, 100 kΩ), 1 µF × 2, 100 nF, R9, millefori, prolunga USB‑C, filo, ottone.
4. Prove: stampa del PDF al 100 %, giunti di prova, poi montaggio per gruppi (alimentazione per prima).
5. Firmware su breadboard: SimpleFOC in posizione, pendolo, scala Maelzel, letargo, stop, encoder a stati.

## In attesa da Fabio
- Modulo vibrazione: dimensioni, centro dei fori GND/VCC/IN, altezza col motorino.
- Col tester: continuità VIN−/VOUT− (MT3608) e IN−/OUT− (Mini‑360); pull‑up SDA/SCL e DIR dell'AS5600; Vf dei filamenti.
- Ricontrollo: spessore del PCB dell'ESP32 (3 mm misurati, atteso 1–1,2) e interasse VIN−/VIN+ dell'MT3608 (10 mm, la foto dava ~8,5).
- Misure dell'encoder EC11 (oggi tipiche) e interasse dei fori M2 del motore.

## Problemi aperti
- Saldatura diretta sulle celle: rapida, celle a ~3,6 V e alla stessa tensione (vedi decisioni).
- Render in `render/` e schema PDF/PNG fermi alla versione C3: servono `bpy` e `cairosvg`.
- Rigidità del telaio del motore in filo da 1 mm.
- GPIO43 (TX di UART0) per STOP: da provare che l'avvio non disturbi il driver.
- Il modello principale `modello/metronomus.scad` non mostra ancora cosa c'è sotto la base: usare i modelli di verifica.
