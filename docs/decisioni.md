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
| 2026-10-18 | La scheda è un'**ESP32‑S3 SuperMini**, non una C3: misure dal disegno quotato Nologo (23,50 × 18,00, 2 file da 9 pin). Nuovo pinout: PWM 7/6/5, I2C SCL 1 / SDA 2, PWR_EN 4, vibrazione 3, encoder 12/13/8, LED 10, ADC 9. Sul rame l'S3 è ruotata di 90° (fila 1…7 verso il driver, fila 5V…8 verso la scheda servizi) e la scheda servizi è riordinata | La foto mostra 9 pin per fila e la serigrafia "48" del LED RGB; il YouTube Controller usa la stessa scheda | Tenere il pinout C3 (pin inesistenti sull'S3) |
| 2026-10-18 | TP4056: piazzole e dimensioni dalla foto quotata del venditore (HW‑107, 26,1 × 17,4) | Stessa disposizione delle piazzole della versione USB‑C | Stima dalla foto di Fabio senza scala |
| 2026-10-18 | SimpleFOC Mini dal disegno quotato del produttore: 26 × 21,5, 4 fori Ø2 a 22 × 17,5, alto 11 con i pin. Con le misure vere toccava il Mini‑360: driver spostato di un passo a destra (PWM su GPIO7/6/5, PWR_EN su 4, pulsante dell'encoder su 8) | La stima dalla foto (23,8 × 20) era troppo piccola | Spostare il Mini‑360 (tocca batteria e telaio) |
| 2026-10-18 | Modello per ruolo: `elettronica` Opus (errori di progetto costosi), `coordinatore` e `piano-fili` Sonnet (la geometria è controllata dallo script), `git-readme` Haiku; comandi `/stato` Haiku e `/fine-sessione` Sonnet | Richiesta di Fabio: ridurre il consumo di token | Tutto sul modello della chat |
| 2026-10-18 | Controllo delle sovrapposizioni tra schede (gioco 0,5 mm) e magnete dell'AS5600 nel modello; criticità ed etichette visibili nello script OpenSCAD | Il contatto driver/Mini‑360 non era stato visto; serve leggere il modello a colpo d'occhio | Controllo a vista sul render |
| 2026-10-18 | **Circuito a bus**: ogni scheda ha le sue *discese* (fili dritti dal pin fino alla quota del bus); i bus corrono sollevati sopra la base (massa a 6 mm, 12 V a 14 mm, segnali a 18 mm) e sporgono 3 mm oltre l'ultima discesa, che si salda in T dove cade davvero. Montaggio a gruppi: struttura e bus sulla dima, poi una scheda alla volta, l'alimentazione per prima | Proposta di Fabio: gioco di montaggio, una scheda alla volta, correzioni sul bus se una misura non torna | Collegamenti a U chiusi tra i pin (nessun gioco) |
| 2026-10-18 | AS5600 collegato **direttamente** all'ESP32 (SCL, SDA) e al Mini‑360 (VCC), fuori dai bus | I2C corto e lontano dalle fasi del motore | I2C nel bus con massa in mezzo |
| 2026-10-18 | I filamenti LED che oscillano si collegano con 15–20 mm di filo flessibile, fermato prima della saldatura | Il pendolo si muove: il filo flessibile lavora al posto del giunto | Rame rigido fino al LED |
| 2026-10-18 | **Stop di emergenza**: due paletti di rame a ±35° (prima ±45°) nel piano del pendolo (finecorsa meccanici, rete STOP verso l'EN del driver con R9 10 kΩ di pull‑up e verso GPIO43) e collare di ottone sul pendolo (rete ARMA da GPIO44, filo flessibile). Con ARMA = 0 il contatto spegne il driver in hardware; ARMA = 1 solo all'avvio | In letargo il pendolo rovesciato cade su un finecorsa: con il percussore a massa il driver non potrebbe più ripartire | Percussore a massa (blocco al risveglio); solo firmware; solo finecorsa meccanici |
| 2026-10-18 | Base di legno **150 × 90 mm**; nuovo controllo: tutto dentro la teca (vetro a 5 mm dal bordo, spesso 3) | Risposta di Fabio (15 × 8–10 cm) | Base da 190 mm |
| 2026-10-18 | Magnete da 2 mm a filo del retro del motore; AS5600 con i componenti a 1 mm dal magnete (chip a circa 1–2 mm). ESP32 e Mini‑360 restano dove sono | L'albero non sporge (Fabio); spostando tutto, la dorsale del 12 V toccava il telaio | Arretrare anche le schede |
| 2026-10-18 | **Masse non separate**: anello unico, con il foro del ritorno batteria a metà tra MT3608 VOUT‑ e driver PWR‑. In più 220–470 µF ai morsetti del driver e 100 nF su 3V3_SW all'AS5600 | Ruolo elettronica: le correnti del motore restano tra driver e motore; 1–2 mV tra le masse contro 1 V di soglia I2C | Masse di potenza e logica separate |
| 2026-10-18 | Niente dima dedicata: stampa 1:1 su sughero con spilli e squadrette, la base forata tiene le discese | Tutti pezzi dritti (Fabio: la dima non è indispensabile) | Dima incisa al laser o stampata |
| 2026-10-18 | **Scala su ±30°**, finecorsa a ±35° (paletti alti 94,5 mm, collare a 30 mm dall'asse), pannello largo 124 mm ricavato dall'arco; tutto entra nella base da 150 mm | Fabio: adattare la larghezza alle necessità. ±30° è circa l'oscillazione di un metronomo meccanico; 39 tacche a 2,7 mm l'una restano leggibili | ±40° con base da 175 mm; ±35° con base da 160 mm |
| 2026-10-18 | **Encoder senza filtro RC**: A e B letti con decodifica in quadratura a stati, pulsante con antirimbalzo software di 20–30 ms, pull‑up interne dell'ESP32 | Le linee dell'encoder non passano dalla millefori; la decodifica a stati annulla da sola i rimbalzi. Se sul banco le letture sono sporche, si aggiunge un RC (10 kΩ + 10 nF) su una millefori minuscola sotto la base, vicino all'encoder | RC sulla scheda servizi (più rame e giunti); RC sotto la base subito |
| 2026-10-18 | **Barre BATT+ e BATT− saldate direttamente sui poli delle 18350** (a contatto, al centro del polo) | Scelta di Fabio: niente molle né linguette, coerente col rame a vista. Saldatura rapida: polo carteggiato, flussante, saldatore potente ben caldo, contatto di 2–3 s, celle scariche a circa 3,6 V | Molla + piastrina; linguette a puntatrice |
| 2026-10-18 | **Moduli misurati col calibro** (centro dei fori): ESP32 18 × 24 (25 con USB), AS5600 22,5 × 22,5 con chip al centro, MT3608 37,5 × 18, Mini‑360 18 × 12, SimpleFOC 26 × 21,5, filo 1,0; anello di massa 1 mm più avanti per tenere il pezzo sotto il Mini‑360 ≥ 10 mm | Le stime dalle foto non bastavano per il PDF di produzione | Restare sulle stime |
| 2026-10-18 | **MT3608 e Mini‑360 con un solo filo di massa** (VOUT− e OUT−) | VIN−/VOUT− e IN−/OUT− sono la stessa massa sulla scheda: un secondo filo aggiunge pezzi e giunti senza effetto (da verificare col tester) | Filo anche sul quarto piedino |
| 2026-10-18 | **Sotto la base**: TP4056 ed encoder in scassi, cavetti isolati in canaline da 4 mm; il rame elettrico attraversa la base (fori passanti) e sporge 2 mm nella canalina dove si salda il cavetto; struttura e paletti in fori ciechi da 5 mm | Senza questo le batterie e il caricatore non erano collegati a niente; i cavetti sotto restano invisibili | Rame rigido anche sotto; fori ciechi e fili flessibili dall'alto |
| 2026-10-18 | **Modulo vibrazione sopra la base**, incollato al legno, con IN esattamente sotto il GPIO3 (filo dritto); VCC e GND scendono nella base e arrivano coi cavetti | Scelta di Fabio; verso l'anello i pezzi sarebbero stati di 5 mm | Modulo sotto la base |
| 2026-10-18 | **Scheda servizi: millefori 17 × 6 fori** (fili/millefori.py, netlist controllata): MCP1700‑3302E TO‑92, AO3400/AO3401 su adattatori SOT‑23, resistenze in piedi, R6 sdraiata, 2 ponticelli isolati, linee VBAT dietro e GND davanti | Componenti saldabili a mano; fila dei pin di uscita invariata, quindi il rame non cambia | Componenti volanti sul rame; moduli già pronti |
| 2026-10-18 | **PDF 1:1 generato** (fili/piano_pdf.py, senza librerie) e **verifiche OpenSCAD per gradi** (fili/verifica_scad.py: tutto, alimentazione, esp32) che ricostruiscono i pezzi tagliati dai dati del PDF | Controllare che lunghezze ed estremità stampate combacino davvero prima di tagliare | Fidarsi solo dei controlli della geometria |
| 2026-10-18 | **Q1 (LED) e Q3 (comando del letargo) sono 2N3904 NPN TO‑92** del kit già in casa, al posto degli AO3400: base con 470 Ω (Q1) e 10 kΩ (Q3), pull‑down 100 kΩ invariate; sulla millefori in colonna, emettitore sulla linea GND. **Q2 resta AO3401** | Fabio: usare quello che ha nella scatola. Q3 porta solo 42 µA e Q1 al massimo ~100 mA, il 2N3904 basta; per Q2 un PNP del kit (S8550/S9012, 0,5 A) perderebbe 0,2–0,5 V sulla batteria e chiederebbe 20–50 mA di base fissi, quindi resta il MOSFET P | AO3400 ×2 da comprare; S8550 anche per Q2 |

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
- Arco della scala: **±30° dalla verticale** (decisione del 18/10, base da 150 mm), tacche tra 92 e 104 mm dall'asse; pannello largo 124 mm. Lenti a sinistra, veloci a destra.
- Il file vettoriale (SVG/DXF per LightBurn) verrà generato dagli stessi dati del firmware, così scala incisa e angoli della lancetta coincidono per costruzione.

#### Conseguenze tecniche

- **Sensore di angolo assoluto:** AS5600 con magnete diametrale sull'albero (confermato).
- **Taratura dello zero:** l'angolo "verticale" e l'allineamento della scala si tarano una volta e si salvano in memoria non volatile (NVS) sull'ESP32.
- **Ampiezza dell'oscillazione** e **arco della scala** sono indipendenti: il pendolo può oscillare più o meno ampio dell'arco inciso. Si decide a occhio con il prototipo.
- **Gravità:** con il LED a sbalzo, tenere la lancetta ferma fuori verticale richiede una piccola coppia continua: il controllo in posizione FOC la gestisce, il consumo in modalità impostazione resta basso.
- Il LED a tubo è **dritto verso l'alto** (pendolo rovesciato come in un metronomo classico): la punta superiore è quella che indica la scala.
