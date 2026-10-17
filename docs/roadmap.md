# Roadmap

## Fase 0 · Avvio ✅
- [x] Cartella di progetto, repository git, ruoli dei subagenti
- [x] Analisi iniziale ([analisi-iniziale.md](analisi-iniziale.md))

## Fase 1 · Componenti
- [ ] Identificare i modelli dalle foto (`foto/`)
- [ ] Decidere driver/motore/sensore (FOC o no)
- [ ] Completare la BOM con le parti mancanti
- [ ] Ordinare quello che manca

## Fase 2 · Elettronica e firmware su breadboard
- [ ] Schema a blocchi e schema elettrico
- [ ] Pinout ESP32
- [ ] Firmware: motore in posizione con SimpleFOC
- [ ] Firmware: pendolo sinusoidale a BPM variabili
- [ ] Firmware: modalità impostazione (pendolo come lancetta sulla scala)
- [ ] Firmware: encoder, pulsante, LED sincronizzato, batteria
- [ ] Prove di consumo e autonomia

## Fase 3 · Design del circuito in rame
- [ ] Disposizione dei moduli nello spazio (layout 3D)
- [ ] Geometria dei fili (`fili/geometria.yaml`)
- [ ] Prove di taglio e giunti saldati (`fili/prove-giunti.md`)
- [ ] Distinta di taglio e sequenza di montaggio
- [ ] Dima per laser/stampa 3D
- [ ] Scala Maelzel da incidere al laser (SVG generato dai dati del firmware)

## Fase 4 · Produzione
- [ ] PDF 1:1 di taglio e saldatura dei segmenti (`produzione/`)
- [ ] Montaggio e saldatura
- [ ] Taratura finale e protezione del rame
- [ ] Foto finali nel README
