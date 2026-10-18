# Stato del progetto

_Aggiornato il 18/10/2026._

## Fase attuale
Fase 3 · disposizione del circuito in rame, in attesa delle misure reali dei moduli. In parallelo la fase 1 (parti da comprare).

## Fatto finora
- Componenti identificati dalle foto e BOM ([hardware/bom.md](../hardware/bom.md)): ESP32‑S3 SuperMini (corretto il 18/10, era indicata come C3), SimpleFOC Mini, motore 1503, AS5600, EC11, TP4056 USB‑C, MT3608, Mini‑360, 2 × 18350 in parallelo, 2 filamenti LED, motorino a vibrazione.
- Schema elettrico rev. 0.2.1 (GPIO dell'S3; il PDF/PNG va rigenerato con cairosvg, aggiornato solo l'SVG) con letargo sul pulsante dell'encoder ([hardware/schema.pdf](../hardware/schema.pdf)), pinout ([hardware/pinout.md](../hardware/pinout.md)).
- Indicatore del tempo: il pendolo punta su una scala Maelzel incisa. Tic: motorino a vibrazione sotto la base.
- Base di legno dentro una teca di vetro; encoder sul bordo anteriore, prolunga USB‑C sul retro.
- Rame: misure dei moduli in [fili/moduli.yaml](../fili/moduli.yaml) (ancora **stimate** dalle foto), geometria in [fili/geometria.py](../fili/geometria.py) con controlli (pezzi ≥ 10 mm, assi ≥ 2,5 mm, nessun filo attraverso le schede). Disposizione compatta: 84 pezzi, circa 2,67 m di filo (con l'S3).
- Modello OpenSCAD e render generati dalla stessa geometria ([modello/](../modello), [render/](../render)).

## Prossimi passi
1. Fabio misura i moduli col calibro ([fili/misure-da-prendere.md](../fili/misure-da-prendere.md)); si aggiorna `moduli.yaml` e si rilancia la geometria.
2. Aggiornare lo schema elettrico: filamenti in serie con una sola resistenza (R7 via), scheda servizi, DIR dell'AS5600.
3. Ordinare le parti mancanti (LDO, AO3401/AO3400, prolunga USB‑C da pannello, filo di rame).
4. Firmware su breadboard: SimpleFOC in posizione, pendolo sinusoidale, scala Maelzel, letargo.
5. Generatore del PDF 1:1 di taglio (solo con misure tutte "misurate").

## In attesa da Fabio
- Misure col calibro di ESP32, driver, MT3608, Mini‑360, AS5600, TP4056, motore e diametro reale del filo.
- Col tester: pull‑up SDA/SCL e resistenza su DIR dell'AS5600; Vf dei filamenti LED.

## Problemi aperti
- Rigidità del telaio del motore in filo da 1 mm: forse serve filo più grosso o ottone.
- Ponticello EN–3V3 del driver fatto sulla scheda (pezzo sotto i 10 mm, unica eccezione).
