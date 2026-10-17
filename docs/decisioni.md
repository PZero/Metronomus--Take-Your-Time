# Registro delle decisioni

Tutte le decisioni del progetto stanno in questo file: la tabella è l'indice, i dettagli sono nelle sezioni sotto.

| Data | Decisione | Motivo | Alternative scartate |
|---|---|---|---|
| 2026-10-17 | Filo di rame Ø 1,0 mm, solo pieghe a 90° | Scelta estetica di Fabio | — |
| 2026-10-17 | Lunghezze dei fili misurate sull'asse del filo, con deduzione di piega tarata | Precisione ripetibile | Misura sui bordi esterni |
| 2026-10-17 | Controllo FOC in posizione con libreria SimpleFOC, driver SimpleFOC Mini v1.0 | Il driver di Fabio è nato per questo; moto sinusoidale fluido come un pendolo vero | ESC da drone; avanti/indietro con finecorsa Hall |
| 2026-10-17 | Indicatore del tempo: il pendolo si ferma e punta su una scala Maelzel incisa al laser ([dettagli](#indicatore-del-tempo-il-pendolo-come-lancetta)) | Estetica pulita, zero componenti in più | Display 3 cifre, strumento ad ago, Nixie, arco di LED |
| 2026-10-17 | Alimentazione motore ≥ 8 V (boost da 1S) | Limite minimo del DRV8313 | Motore alimentato direttamente da 1S |
| 2026-10-17 | ~~2 × 18350 in serie (2S)~~ → **2 × 18350 in parallelo (1S)**, ricarica con il TP4056 USB‑C, MT3608 a 12 V per il motore, Mini‑360 da 12 V a 3,3 V per l'ESP32 | Usa solo componenti già disponibili: il TP4056 è per una cella e il Mini‑360 non funziona sotto 4,75 V, quindi lo si alimenta dai 12 V del boost | 2S con caricatore e BMS 2S da comprare |
| 2026-10-17 | Sensore di posizione AS5600 | Angolo assoluto, necessario per il pendolo FOC e per l'indicatore del tempo | Hall semplice |
| 2026-10-17 | Motore 1503 (7,4 V, 0,5 Ω) con limite di tensione FOC basso nel firmware | Motore già disponibile, carico leggero (LED da 5 cm) | Motore gimbal 2204: da valutare se il 1503 scalda o scatta troppo |

---

## Dettagli

### Indicatore del tempo: il pendolo come lancetta

_17 ottobre 2026, scelta di Fabio._

Niente display. Il tempo impostato si legge su una **scala ad arco incisa al laser** sulla base, dietro al pendolo, come sui metronomi meccanici Wittner/Maelzel. La lancetta è il **LED a tubo** stesso.

#### Comportamento

1. **In oscillazione:** il pendolo batte il tempo normalmente.
2. **Giri l'encoder:** il pendolo frena dolcemente e va a puntare sulla scala il valore BPM selezionato. Il LED resta acceso fisso e più tenue, per distinguere la "modalità impostazione".
3. **Continui a girare:** la lancetta segue il valore scatto per scatto, con movimento morbido senza sobbalzi.
4. **Lasci l'encoder per ~2 s:** il pendolo riparte dalla posizione in cui si trova, sincronizzando la prima oscillazione, e riprende a battere il nuovo tempo.

#### La scala

- Valori della **scala Maelzel classica**: un clic dell'encoder corrisponde a un valore della scala.
  - 40–60 a passi di 2 · 60–72 a passi di 3 · 72–120 a passi di 4 · 120–144 a passi di 6 · 144–208 a passi di 8
  - In totale 39 posizioni.
- Accanto ai numeri, i nomi dei tempi: Largo, Larghetto, Adagio, Andante, Moderato, Allegro, Presto.
- Arco della scala: da definire con le dimensioni dell'oggetto (indicativamente ±40° dalla verticale). Lenti a sinistra, veloci a destra.
- Il file vettoriale (SVG/DXF per LightBurn) verrà generato dagli stessi dati del firmware, così scala incisa e angoli della lancetta coincidono per costruzione.

#### Conseguenze tecniche

- **Sensore di angolo assoluto:** AS5600 con magnete diametrale sull'albero (confermato).
- **Taratura dello zero:** l'angolo "verticale" e l'allineamento della scala si tarano una volta e si salvano in memoria non volatile (NVS) sull'ESP32.
- **Ampiezza dell'oscillazione** e **arco della scala** sono indipendenti: il pendolo può oscillare più o meno ampio dell'arco inciso. Si decide a occhio con il prototipo.
- **Gravità:** con il LED a sbalzo, tenere la lancetta ferma fuori verticale richiede una piccola coppia continua: il controllo in posizione FOC la gestisce, il consumo in modalità impostazione resta basso.
- Il LED a tubo è **dritto verso l'alto** (pendolo rovesciato come in un metronomo classico): la punta superiore è quella che indica la scala.
