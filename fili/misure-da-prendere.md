# Misure da prendere col calibro

Le posizioni dei fori dei moduli sono la base di tutto il rame: un errore di 0,5 mm su un pin si ritrova su ogni pezzo collegato. Oggi i valori in [`moduli.yaml`](moduli.yaml) sono **stimati** dalle foto; il PDF di taglio non si genera finché restano stimati.

## Come misurare
1. Metti la scheda **lato componenti in su**, orientata come scritto in `vista` per quel modulo.
2. L'origine è l'**angolo in basso a sinistra** della scheda. x verso destra, y verso l'alto.
3. Per ogni foro misura con il becco del calibro **dal bordo al bordo del foro** e aggiungi metà diametro del foro, così ottieni il centro. In alternativa infila un filo da 1 mm e misura al filo.
4. Per le file di pin a passo 2,54: misura solo il **primo** foro e controlla primo-ultimo (es. 8 pin: 17,78 mm).
5. Scrivi i numeri nella tabella qui sotto (o direttamente in `moduli.yaml`, cambiando `stato` in `misurato`).

## Tabella

| Modulo | Cosa misurare | Valore stimato (mm) | Misurato (mm) |
|---|---|---|---|
| ESP32‑C3 SuperMini | larghezza × altezza scheda | 18,0 × 22,52 | |
| | primo foro fila sinistra (5V): x, y | 1,38 · 20,15 | |
| | primo foro fila destra (GPIO5): x, y | 16,62 · 20,15 | |
| | ordine dei pin sulla serigrafia (sinistra / destra, USB in alto) | 5V…GPIO0 / GPIO5…GPIO21 | |
| SimpleFOC Mini | larghezza × altezza | 23,8 × 20,0 | |
| | foro EN (fila alta, sinistra): x, y | 3,2 · 18,45 | |
| | foro nFT (fila bassa, sinistra): x, y | 3,2 · 15,91 | |
| | foro M1: x, y | 6,2 · 1,2 | |
| | morsetto −: x, y · morsetto +: x, y | 20,4 · 14,8 · 20,1 · 9,8 | |
| | altezza del condensatore | 8,5 | |
| MT3608 | larghezza × altezza | 36,0 × 17,0 | |
| | VIN−, VIN+, VOUT−, VOUT+: x, y | 3,0·13,0 · 3,0·4,5 · 33,2·12,1 · 33,2·4,8 | |
| | altezza del trimmer | 10,0 | |
| Mini‑360 | larghezza × altezza | 17,2 × 11,2 | |
| | IN+, IN−, OUT+, OUT−: x, y (e quale angolo è quale) | 1,3·9,9 · 1,3·1,3 · 15,9·9,9 · 15,9·1,3 | |
| AS5600 | larghezza × altezza | 23,5 × 23,3 | |
| | foro VCC: x, y · foro DIR: x, y | 4,85·14,3 · 18,2·16,6 | |
| | centro del chip: x, y | 11,6 · 11,9 | |
| TP4056 | larghezza × altezza | 27,0 × 17,0 | |
| | OUT−, B−, B+, OUT+: x, y | 3,1·15,2 · 3,1·11,8 · 3,1·4,8 · 3,1·1,7 | |
| Motore 1503 | diametro campana · lunghezza base‑campana · interasse fori M2 | 19 · 15 · ? | |
| Filo di rame | diametro reale (spesso è 0,95–1,05) | 1,00 | |

## Col tester (moduli scollegati)
- AS5600: resistenza **SDA–VCC**, **SCL–VCC** (pull‑up), **DIR–GND** (se c'è una resistenza, DIR non va collegato).
- Modulo vibrazione: resistenza **IN–GND** (atteso circa 6 kΩ: 1 kΩ + 5,1 kΩ).
- Filamento LED: tensione a 20–30 mA (Vf). Con due filamenti in serie serve circa il doppio.
