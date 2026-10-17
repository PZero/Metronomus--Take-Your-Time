# Schema elettrico

![Schema elettrico](schema.png)

File: [schema.pdf](schema.pdf) (A3, vettoriale) · [schema.svg](schema.svg) · generato da [schema.py](schema.py) con `python hardware/schema.py`.

Le etichette uguali indicano piedini collegati tra loro. Gli stessi nomi di rete si usano nel piano fili.

## Reti

| Rete | Collega | Note |
|---|---|---|
| **VBAT** | TP4056 B+ ↔ + delle due 18350 | Celle in parallelo (1S), 3,0–4,2 V |
| **VSW** | TP4056 OUT+ → SW1 → MT3608 VIN+, R1, modulo vibrazione VCC | Batteria dopo l'interruttore |
| **V12** | MT3608 VOUT+ → SimpleFOC +, Mini‑360 IN+, R6, R7 | 12,0 V |
| **3V3** | Mini‑360 OUT+ → ESP32 3V3, AS5600 VCC | 3,30 V |
| **GND** | tutte le masse, AS5600 DIR, encoder C e SW | Comune |
| PWM_A / PWM_B / PWM_C | ESP32 GPIO5 / 6 / 7 → SimpleFOC IN1 / IN2 / IN3 | |
| DRV_EN | ESP32 GPIO10 → SimpleFOC EN | |
| SDA / SCL | ESP32 GPIO20 / 21 ↔ AS5600 SDA / SCL | I2C 400 kHz |
| ENC_A / ENC_B / ENC_SW | EC11 A / B / SW → R 10 kΩ → ESP32 GPIO3 / 4 / 9 | 10 nF a GND su ogni ingresso |
| LED_PWM | ESP32 GPIO1 → 100 Ω → gate Q1 (100 kΩ a GND) | |
| LED_K | catodi LED1, LED2 → drain Q1 | Source di Q1 a GND |
| VIB_IN | ESP32 GPIO8 → modulo vibrazione IN | |
| VBAT_ADC | nodo R1/R2/C1 → ESP32 GPIO0 | Metà di VSW |
| M1 / M2 / M3 | SimpleFOC → fili del motore 1503 | L'ordine si aggiusta in firmware |

## Da verificare sul banco
- Resistenze R6/R7 dei filamenti dopo la misura della Vf.
- Se il modulo AS5600 ha già le pull‑up su SDA/SCL (altrimenti 4,7 kΩ a 3V3).
- Se il modulo vibrazione ha già la pull‑down su IN (altrimenti 100 kΩ a GND).
