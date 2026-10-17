# Distinta componenti (BOM)

_Da completare con i modelli esatti dopo le foto._

## Componenti che hai già

| Componente | Modello | Note |
|---|---|---|
| Microcontrollore | ESP32 — _da identificare_ | |
| Driver motore brushless | _da identificare_ | Critico: deve permettere controllo in posizione |
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
| Boost per il motore | MT3608 (se batteria 1S) | Il motore gimbal vuole 7–12 V |
| MOSFET per il LED | AO3400 / IRLZ44N logic‑level | PWM del LED dal pin ESP32 |
| Partitore batteria | 2 × 100 kΩ + 100 nF | Misura carica |
| Filo flessibile per il LED | Silicone 30 AWG | Collegare il LED che oscilla |
| Piezo o altoparlante + MAX98357A | — | Suono del tic (opzionale) |
| Filo di rame | Ø 1,0 mm, rame rosso o stagnato | Il circuito |
| Vernice trasparente | Protettivo per rame | Contro l'ossidazione (opzionale) |
