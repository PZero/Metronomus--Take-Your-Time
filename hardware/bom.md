# Distinta componenti (BOM)

_Da completare con i modelli esatti dopo le foto._

## Componenti che hai già

| Componente | Modello | Note |
|---|---|---|
| Microcontrollore | ESP32 — _da identificare_ | |
| Driver motore brushless | **SimpleFOC Mini v1.0 (04/22)**, chip DRV8313 | Alimentazione motore 8–30 V, max ~2,5 A di picco. Ingressi IN1/IN2/IN3 (PWM), EN, nSLP, nRT, nFT. Logica 3,3 V compatibile con ESP32. Il pin 3,3 V della scheda eroga solo ~10 mA: non usarlo per l'ESP32 |
| Motore brushless | _da identificare_ | Ideale un gimbal 2204/2804 |
| Batteria | _da identificare_ | |
| Modulo di ricarica USB | _da identificare_ (TP4056?) | |
| Rotary encoder | _da identificare_ (KY‑040?) | |
| LED a tubo 5 cm | _da identificare_ | Montato sull'albero |
| Sensore magnetico + magnete | _da identificare_ | AS5600 o Hall |

## Probabilmente mancanti (da confermare)

| Componente | Proposta | Perché |
|---|---|---|
| Interruttore generale | Interruttore a levetta in metallo | Estetica in tema con il rame |
| Regolatore 3,3 V | MCP1700‑3302 / AP2112K‑3.3 | Alimentare l'ESP32 dalla batteria |
| Boost per il motore | MT3608 o simile, regolato a ~10–12 V (solo se batteria 1S) | Il DRV8313 del SimpleFOC Mini **non funziona sotto 8 V** |
| MOSFET per il LED | AO3400 / IRLZ44N logic‑level | PWM del LED dal pin ESP32 |
| Partitore batteria | 2 × 100 kΩ + 100 nF | Misura carica |
| Filo flessibile per il LED | Silicone 30 AWG | Collegare il LED che oscilla |
| Piezo o altoparlante + MAX98357A | — | Suono del tic (opzionale) |
| Filo di rame | Ø 1,0 mm, rame rosso o stagnato | Il circuito |
| Vernice trasparente | Protettivo per rame | Contro l'ossidazione (opzionale) |
