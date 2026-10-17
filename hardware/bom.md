# Distinta componenti (BOM)

_Aggiornata il 17/10/2026 con le foto in [`foto/`](../foto)._

## Componenti disponibili

| Componente | Modello | Foto | Note |
|---|---|---|---|
| Microcontrollore | **ESP32‑C3 SuperMini** (lo stesso del YouTube Controller) | [foto](../foto/esp32-c3-supermini.jpg) | RISC‑V 160 MHz, USB‑C, 16 piedini sul bordo, 13 GPIO (ne servono 11). Pinout in [pinout.md](pinout.md) |
| Microcontrollore (riserva) | ESP32 D1 Mini con modulo WROOM‑32 | [foto](../foto/esp32-d1-mini-wroom.jpg) | Più potente e con più pin, ma 40 piedini su doppia fila: scomodo da cablare in rame. Tenuto come alternativa |
| Driver motore | **SimpleFOC Mini v1.0** (rev. 2024‑05‑13), chip DRV8313 | [foto](../foto/driver-simplefoc-mini.jpg) | Motore 8–35 V (serigrafia), condensatore 100 µF 35 V già montato. Pin: IN1, IN2, IN3, EN, GND (fila 1) · nFT, nSP (sleep), nRT (reset), GND, 3V3 (fila 2). Uscite M1/M2/M3. Il pin 3V3 eroga solo ~10 mA: non alimenta l'ESP32 |
| Motore | **Outrunner 1503**, 7,4 V, 0,3 A, 0,5 Ω, 3 fili (bianco/blu/rosso) | [foto](../foto/motore-1503.jpg) | Base con 2 fori filettati M2 + 2 fori. L'estremità dell'albero sporge al centro della base: lì va incollato il magnete dell'AS5600, con il sensore dietro al motore. Il LED si monta sulla campana, davanti. Bassa resistenza: `voltage_limit` FOC ≈ 0,5–1 V |
| Sensore di posizione | **AS5600** (modulo viola, 7 pin: VCC, OUT, GND, DIR, SCL, SDA, GPO) | [foto](../foto/sensore-as5600.jpg) | I2C 0x36, 12 bit. DIR a GND, GPO a GND o libero. Magnete diametrale 6 × 2,5 mm (incluso, confermato da Fabio), distanza 0,5–3 mm, centrato ±0,5 mm |
| Rotary encoder | **EC11 nudo** (senza scheda), con pulsante, albero zigrinato 20 mm, filetto per dado a pannello | [foto](../foto/encoder-ec11.jpg) | 3 pin A‑C‑B + 2 pin pulsante + 2 linguette di fissaggio. Pull‑up interne dell'ESP32, debounce RC consigliato. I piedini si saldano bene al filo di rame |
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
| MOSFET N di comando | AO3400 + 100 Ω + 100 kΩ (lo stesso dei LED) | Comanda il gate dell'AO3401 |
| MOSFET per il LED | AO3400 / IRLZ44N logic‑level + 100 Ω gate + 100 kΩ pull‑down | PWM del LED dal pin ESP32 |
| Partitore batteria | 2 × 100 kΩ + 100 nF | Misura del livello di carica |
| Debounce encoder | 3 × 10 kΩ + 3 × 10 nF | Letture pulite di A, B e pulsante |
| Filo flessibile per il LED | Silicone 30 AWG | Collegare il LED che oscilla |
| Filo di rame | Ø 1,0 mm | Il circuito (quantità dopo il layout) |
| Vernice trasparente | Protettivo per rame | Contro l'ossidazione (opzionale) |

## Non più necessari
- Caricatore 2S e BMS 2S: con le celle in parallelo bastano il TP4056 e la sua protezione.
- Condensatore bulk esterno sul driver: il SimpleFOC Mini ha già 100 µF a bordo.
