# Distinta componenti (BOM)

_Aggiornata il 18/10/2026: la scheda ESP32 è una S3, non una C3 (foto in [`foto/`](../foto))._

## Componenti disponibili

| Componente | Modello | Foto | Note |
|---|---|---|---|
| Microcontrollore | **ESP32‑S3 SuperMini** (lo stesso del YouTube Controller; fino al 17/10 indicato per errore come C3) | [foto](../foto/esp32-s3-supermini.jpg) | Xtensa dual‑core 240 MHz, USB‑C nativa, 18 piedini sul bordo in 2 file da 9, 15 GPIO (ne servono 12). PCB 23,50 × 18,00 dal disegno quotato Nologo; regolatore ME6217C33 a bordo; LED RGB su GPIO48. Pinout in [pinout.md](pinout.md) |
| Microcontrollore (riserva) | ESP32 D1 Mini con modulo WROOM‑32 | [foto](../foto/esp32-d1-mini-wroom.jpg) | Più potente e con più pin, ma 40 piedini su doppia fila: scomodo da cablare in rame. Tenuto come alternativa |
| Driver motore | **SimpleFOC Mini v1.0** (rev. 2024‑05‑13), chip DRV8313 | [foto](../foto/driver-simplefoc-mini.jpg) | Motore 8–35 V (serigrafia), condensatore 100 µF 35 V già montato. Pin: IN1, IN2, IN3, EN, GND (fila 1) · nFT, nSP (sleep), nRT (reset), GND, 3V3 (fila 2). Uscite M1/M2/M3. Il pin 3V3 eroga solo ~10 mA: non alimenta l'ESP32 |
| Motore | **Outrunner 1503**, 7,4 V, 0,3 A, 0,5 Ω, 3 fili (bianco/blu/rosso) | [foto](../foto/motore-1503.jpg) | Base con 2 fori filettati M2 + 2 fori. L'estremità dell'albero sporge al centro della base: lì va incollato il magnete dell'AS5600, con il sensore dietro al motore. Il LED si monta sulla campana, davanti. Bassa resistenza: `voltage_limit` FOC ≈ 0,5–1 V |
| Sensore di posizione | **AS5600** (modulo viola, 7 pin: VCC, OUT, GND, DIR, SCL, SDA, GPO) | [foto](../foto/sensore-as5600.jpg) | I2C 0x36, 12 bit. DIR a GND, GPO a GND o libero. Magnete diametrale 6 × 2,5 mm (incluso, confermato da Fabio), distanza 0,5–3 mm, centrato ±0,5 mm |
| Rotary encoder | **EC11 nudo** (senza scheda), con pulsante, albero zigrinato 20 mm, filetto per dado a pannello | [foto](../foto/encoder-ec11.jpg) | 3 pin A‑C‑B + 2 pin pulsante + 2 linguette di fissaggio. Pull‑up interne dell'ESP32, antirimbalzo nel firmware. I piedini si saldano bene al filo di rame |
| Caricatore | **TP4056 USB‑C con protezione** (DW01 + doppio MOSFET) | [foto](../foto/caricatore-tp4056-usbc.jpg) | **Una sola cella (1S)**, max 1 A. Morsetti B+/B− (cella) e OUT+/OUT− (carico, protetto) |
| Batterie | **2 × 18350 Li‑ion** | — | Collegate **in parallelo** (1S), solo dopo averle portate alla stessa tensione |
| Boost | **MT3608** (trimmer multigiro 3296) | [foto](../foto/boost-mt3608.jpg) | Ingresso 2–24 V. Tarato a **12 V prima** di collegare il driver |
| Step‑down | **MH Mini‑360** (MP2307) | [foto](../foto/stepdown-mini360.jpg) | Ingresso 4,75–23 V: alimentato dai 12 V del boost. Tarato a **3,3 V prima** di collegarlo, uscita al pin 3V3 dell'ESP32 |
| Modulo vibrazione | **Motorino a moneta ~Ø10 mm (prob. 1027, 3 V)** su modulo GND/VCC/IN con transistor e diodo — lo stesso del YouTube Controller | [foto](../foto/modulo-vibrazione.jpg) | Fissato rigido sotto la base di legno per fare il "tic". VCC dalla batteria, IN da GPIO 8. Dal YouTube Controller: impulsi a piena potenza da **almeno 60 ms** (sotto ~30 ms non parte). Condensatori 47–100 µF + 100 nF su VCC. Dalla foto: transistor SOT‑23, resistenze 1001 (1 kΩ, in serie alla base) e 512 (5,1 kΩ, probabilmente base‑GND), nessun LED di bordo, quindi la pull‑down su IN c'è già (da confermare col tester) |
| LED a tubo 5 cm | **Filamento LED rigido** (fosforo giallo, terminali metallici alle due estremità) — da confermare lunghezza e tensione | [foto](../foto/led-filamento-prova.jpg) | Tipicamente ~3 V, 20–100 mA, polarizzato (il + è di solito l'estremità con il foro o il segno). Un terminale sta sul mozzo, l'altro in punta: serve un filo sottile di ritorno lungo il filamento. Pilotaggio: MOSFET low‑side + resistenza da dimensionare dopo aver misurato la Vf |

## Da comprare

| Componente | Proposta | Perché |
|---|---|---|
| LDO 3,3 V a basso consumo | RT9080‑33 (600 mA, Iq 2 µA) o MCP1700‑3302 (250 mA, solo con WiFi spento) | ESP32 sempre alimentato per il letargo |
| MOSFET P per il letargo | AO3401 + 100 kΩ gate‑source | Spegne tutta la parte di potenza |
| Transistor di comando (Q3) | **2N3904** NPN TO‑92, **già in casa** (kit TO‑92 del YouTube Controller) + 10 kΩ in base + 100 kΩ a GND | Comanda il gate dell'AO3401: corrente di collettore 42 µA. Equivalenti nel kit: S8050, S9013, S9014, C1815, C945, 2N2222 |
| Transistor del LED (Q1) | **2N3904** NPN TO‑92, **già in casa** + 470 Ω in base + 100 kΩ a GND | PWM del LED: con ~5 mA di base resta saturo fino a ~100 mA (Vce ≈ 0,2 V). Se i filamenti chiedono più di 100 mA serve S8050 (500 mA) dallo stesso kit |
| Partitore batteria | 2 × 100 kΩ + 100 nF | Misura del livello di carica |
| Scheda servizi | Millefori passo 2,54 (17 × 6 fori), 1 adattatore SOT‑23 → 3 piedini in fila (solo per l'AO3401), 2 × 1 µF + 100 nF ceramici, resistenze 470 Ω × 1, 10 kΩ × 1 e 100 kΩ × 5 | Disposizione in [fili/millefori.py](../fili/millefori.py) e nel PDF 1:1 |
| ~~Debounce encoder~~ | ~~3 × 10 kΩ + 3 × 10 nF~~ | Non serve: antirimbalzo nel firmware (18/10). Solo se le prove sul banco lo richiedono |
| Filo flessibile per il LED | Silicone 30 AWG | Collegare il LED che oscilla e il collare del finecorsa (3 fili) |
| Condensatori | Elettrolitico 220–470 µF 25 V + ceramico 100 nF | Ai morsetti del driver e all'AS5600 |
| Stop di emergenza | Resistenza 10 kΩ (R9, al posto del ponticello EN–3V3 del driver) + collare di ottone Ø 6 × 10 mm, isolato dal filo di ritorno del LED | Il pendolo che tocca un paletto spegne il driver |
| Filo di rame | Ø 1,0 mm | Il circuito (quantità dopo il layout) |
| Vernice trasparente | Protettivo per rame | Contro l'ossidazione (opzionale) |

## Non più necessari
- Caricatore 2S e BMS 2S: con le celle in parallelo bastano il TP4056 e la sua protezione.
- Condensatore bulk esterno sul driver: il SimpleFOC Mini ha già 100 µF a bordo.
