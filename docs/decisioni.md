# Registro delle decisioni

Tutte le decisioni del progetto stanno in questo file: la tabella è l'indice, i dettagli sono nelle sezioni sotto.

| Data | Decisione | Motivo | Alternative scartate |
|---|---|---|---|
| 2026-10-17 | Filo di rame Ø 1,0 mm, geometria solo ad angoli retti | Scelta estetica di Fabio | — |
| 2026-10-17 | **Niente pieghe**: solo segmenti dritti tagliati a misura e saldati agli angoli (giunti a L e a T) | Scelta di Fabio: le pieghe vengono traballanti, i tagli sono più precisi | Fili piegati a 90° con deduzione di piega |
| 2026-10-17 | Lunghezze calcolate sull'asse, −0,5 mm per ogni estremità in battuta, corrette con giunti di prova ([prove-giunti.md](../fili/prove-giunti.md)) | Precisione ripetibile | Misura sui bordi esterni |
| 2026-10-17 | Controllo FOC in posizione con libreria SimpleFOC, driver SimpleFOC Mini v1.0 | Il driver di Fabio è nato per questo; moto sinusoidale fluido come un pendolo vero | ESC da drone; avanti/indietro con finecorsa Hall |
| 2026-10-17 | Indicatore del tempo: il pendolo si ferma e punta su una scala Maelzel incisa al laser ([dettagli](#indicatore-del-tempo-il-pendolo-come-lancetta)) | Estetica pulita, zero componenti in più | Display 3 cifre, strumento ad ago, Nixie, arco di LED |
| 2026-10-17 | Alimentazione motore ≥ 8 V (boost da 1S) | Limite minimo del DRV8313 | Motore alimentato direttamente da 1S |
| 2026-10-17 | ~~2 × 18350 in serie (2S)~~ → **2 × 18350 in parallelo (1S)**, ricarica con il TP4056 USB‑C, MT3608 a 12 V per il motore, Mini‑360 da 12 V a 3,3 V per l'ESP32 | Usa solo componenti già disponibili: il TP4056 è per una cella e il Mini‑360 non funziona sotto 4,75 V, quindi lo si alimenta dai 12 V del boost | 2S con caricatore e BMS 2S da comprare |
| 2026-10-17 | Sensore di posizione AS5600 | Angolo assoluto, necessario per il pendolo FOC e per l'indicatore del tempo | Hall semplice |
| 2026-10-17 | Motore 1503 (7,4 V, 0,5 Ω) con limite di tensione FOC basso nel firmware | Motore già disponibile, carico leggero (LED da 5 cm) | Motore gimbal 2204: da valutare se il 1503 scalda o scatta troppo |
| 2026-10-17 | ~~Microcontrollore ESP32‑C3 SuperMini~~ (era una S3: vedi 18/10), pinout in [pinout.md](../hardware/pinout.md) | Piccolo, piedini tutti sul bordo (facile in rame), GPIO sufficienti, già usato da Fabio | ESP32 D1 Mini WROOM (40 pin su doppia fila) |
| 2026-10-17 | Tic con motorino a vibrazione fissato sotto la base (impulsi ≥ 60 ms), su GPIO 8 | Suono meccanico del battito senza altoparlante, componente già disponibile | Piezo, altoparlante I2S |
| 2026-10-17 | Due filamenti LED in parallelo sullo stesso MOSFET, ognuno con la sua resistenza | Più luce senza usare altri pin | Un solo filamento; due canali separati |
| 2026-10-17 | **Niente interruttore**: 3 s sul pulsante dell'encoder mettono in letargo (deep sleep + rail di potenza spento da MOSFET), altri 3 s risvegliano. Pulsante su GPIO2, PWR_EN su GPIO10, LDO sempre acceso per l'ESP32, EN del driver al suo 3V3 | Idea di Fabio; consumo in letargo di decine di µA invece di decine di mA | Interruttore a levetta; relè Relpol RSM850B (monostabile, bobina 6 V) |
| 2026-10-17 | Il metronomo starà su una base di legno dentro una piccola teca di vetro: encoder sul bordo della base (pomello fuori dal vetro), USB‑C sul retro, tic con il motorino a vibrazione sotto la base | Il clic di un relè sotto vetro si sentirebbe appena; la vibrazione passa dalla base | Relè a vista per il tic |
| 2026-10-17 | Confermato il motorino a vibrazione come unico tic, niente relè | Fabio: i moduli relè recuperati (Songle JQC‑3FF‑S‑Z 5 V) non sono belli da vedere; la bobina da 5 V non scatta con la sola batteria 1S | Relè Songle dissaldato, alimentato dai 12 V con resistenza in serie |
| 2026-10-17 | Niente portapile: le 18350 si tengono con un supporto in filo di rame saldato e colla a caldo | Scelta di Fabio, coerente con il circuito in rame a vista | Portapile commerciale |
| 2026-10-17 | **Disposizione compatta**: geometria unica in `fili/geometria.py`, misure dei moduli in `fili/moduli.yaml` (stimato/misurato). Nessun pezzo di rame sotto 10 mm, assi di reti diverse ad almeno 2,5 mm | Richiesta di Fabio: pezzi corti difficili da tenere e incollare; lavorare sui fori reali dei moduli | Disposizione a occhio del primo concept |
| 2026-10-17 | Prolunga USB‑C da pannello sul retro della base; TP4056, encoder (sul bordo anteriore) e motorino a vibrazione stanno sotto la base | USB usabile senza toccare la teca; meno fili a vista | TP4056 a vista con la presa dentro la teca |
| 2026-10-17 | Filamenti LED **in serie** con una sola resistenza (R7 eliminata): servono solo due fili verso il pendolo | Il pendolo ha già il filo di ritorno lungo i filamenti; stessa corrente in entrambi | Due filamenti in parallelo con due resistenze |
| 2026-10-17 | LDO, MOSFET del letargo e del LED e resistenze su una **scheda servizi** (millefori a passo 2,54) dietro all'ESP32 | I componenti SMD piccoli non si saldano bene sul filo da 1 mm; i pin della scheda stanno sulla griglia dei pin dell'ESP32 | Componenti volanti sul rame |
| 2026-10-17 | Masse su un **anello di rame** a 6 mm dalla base; 12 V su una dorsale a 14 mm; ponti a U a 18 mm | Ogni modulo scende sul proprio piano senza incroci | Masse a stella |
| 2026-10-17 | Motore su una piastrina di ottone saldata a un telaio quadro di rame, AS5600 dietro la piastrina; ESP32 messo in modo che SDA/SCL dell'AS5600 scendano dritti sui suoi pin | Ottone e rame non disturbano il magnete; I2C con due soli pezzi per filo | Motore sorretto dai soli fili |
| 2026-10-18 | La scheda è un'**ESP32‑S3 SuperMini**, non una C3: misure dal disegno quotato Nologo (23,50 × 18,00, 2 file da 9 pin). Nuovo pinout: PWM 6/5/4, I2C SCL 1 / SDA 2, PWR_EN 7, vibrazione 3, encoder 12/13/11, LED 10, ADC 9. Sul rame l'S3 è ruotata di 90° (fila 1…7 verso il driver, fila 5V…8 verso la scheda servizi) e la scheda servizi è riordinata | La foto mostra 9 pin per fila e la serigrafia "48" del LED RGB; il YouTube Controller usa la stessa scheda | Tenere il pinout C3 (pin inesistenti sull'S3) |
| 2026-10-18 | TP4056: piazzole e dimensioni dalla foto quotata del venditore (HW‑107, 26,1 × 17,4) | Stessa disposizione delle piazzole della versione USB‑C | Stima dalla foto di Fabio senza scala |

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
