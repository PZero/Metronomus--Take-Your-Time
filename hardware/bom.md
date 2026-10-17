# Distinta componenti (BOM)

_Da completare con i modelli esatti dopo le foto._

## Componenti che hai già

| Componente | Modello | Note |
|---|---|---|
| Microcontrollore | ESP32 — _da identificare_ | |
| Driver motore brushless | **SimpleFOC Mini v1.0 (04/22)**, chip DRV8313 | Alimentazione motore 8–30 V, max ~2,5 A di picco. Ingressi IN1/IN2/IN3 (PWM), EN, nSLP, nRT, nFT. Logica 3,3 V compatibile con ESP32. Il pin 3,3 V della scheda eroga solo ~10 mA: non usarlo per l'ESP32 |
| Motore brushless | **1503** (statore 15 mm), 7,4 V, 0,3 A, 0,5 Ω | Resistenza bassa, da drone e non da gimbal: con il driver a 12 V il firmware **deve** limitare la tensione di fase (`voltage_limit` ≈ 0,5–1 V, quindi 1–2 A). Da misurare la resistenza tra due fasi con il multimetro. In alternativa un gimbal 2204 (~10 Ω), più silenzioso e fresco |
| Batteria | **2 × 18350 Li‑ion in serie (2S)** | 6,0–8,4 V (nominale 7,4 V), circa 800–1200 mAh. Da verificare sulle celle: capacità e se sono protette |
| Modulo di ricarica USB | _da identificare_ | Se è un TP4056 non va bene per 2S: vedi sotto |
| Rotary encoder | _da identificare_ (KY‑040?) | |
| LED a tubo 5 cm | _da identificare_ | Montato sull'albero |
| Sensore magnetico + magnete | **AS5600** (encoder magnetico assoluto 12 bit, I2C, indirizzo 0x36) | Serve un magnete **diametrale** (tipico 6 × 2,5 mm) sull'albero, distanza 0,5–3 mm. Il pin DIR del modulo va collegato a GND (se resta flottante l'angolo è instabile). Supportato da SimpleFOC (`MagneticSensorI2C`) |

## Probabilmente mancanti (da confermare)

| Componente | Proposta | Perché |
|---|---|---|
| Interruttore generale | Interruttore a levetta in metallo | Estetica in tema con il rame |
| Regolatore 3,3 V | Piccolo buck 3,3 V (es. MP1584 o modulo Mini‑360) | Da 8,4 V un LDO scalderebbe e sprecherebbe energia |
| Boost per il motore | **MT3608 (disponibile)**, regolato a 12 V **prima** di collegare il driver | Con 2S la tensione scende sotto 8 V già a metà carica: il DRV8313 del SimpleFOC Mini **non funziona sotto 8 V** |
| Caricatore 2S USB‑C | Modulo con chip IP2326 (5 V → 8,4 V) | Il TP4056 carica solo celle singole |
| BMS 2S | Scheda protezione 2S (es. HX‑2S) | Sovrascarica, cortocircuito; se possibile con bilanciamento |
| MOSFET per il LED | AO3400 / IRLZ44N logic‑level | PWM del LED dal pin ESP32 |
| Partitore batteria | 2 × 100 kΩ + 100 nF | Misura carica |
| Filo flessibile per il LED | Silicone 30 AWG | Collegare il LED che oscilla |
| Piezo o altoparlante + MAX98357A | — | Suono del tic (opzionale) |
| Filo di rame | Ø 1,0 mm, rame rosso o stagnato | Il circuito |
| Vernice trasparente | Protettivo per rame | Contro l'ossidazione (opzionale) |
