# Schema elettrico

![Schema elettrico](schema.png)

File: [schema.pdf](schema.pdf) (A3, vettoriale) · [schema.svg](schema.svg) · generato da [schema.py](schema.py) con `python hardware/schema.py`.

Le etichette uguali indicano piedini collegati tra loro. Gli stessi nomi di rete si usano nel piano fili.

## Reti

| Rete | Collega | Note |
|---|---|---|
| **VBAT** | TP4056 B+/OUT+ ↔ + delle due 18350 → source Q2, R8, LDO IN | Sempre presente, 3,0–4,2 V |
| **VSW** | drain Q2 → MT3608 VIN+, R1, modulo vibrazione VCC | Batteria dopo l'interruttore elettronico: spenta in letargo |
| PWR_EN | ESP32 GPIO7 → 100 Ω → gate Q3 (100 kΩ a GND) | Q3 tira giù il gate di Q2 (R8 100 kΩ verso VBAT) |
| **V12** | MT3608 VOUT+ → SimpleFOC +, Mini‑360 IN+, R6, R7 | 12,0 V |
| **3V3** | LDO OUT → ESP32 3V3 | Sempre acceso (anche in letargo) |
| **3V3_SW** | Mini‑360 OUT+ → AS5600 VCC | Spento in letargo |
| DRV_3V3 | SimpleFOC 3V3 → SimpleFOC EN | Driver abilitato quando è alimentato |
| **GND** | tutte le masse, AS5600 DIR, encoder C e SW | Comune |
| PWM_A / PWM_B / PWM_C | ESP32 GPIO6 / 5 / 4 → SimpleFOC IN1 / IN2 / IN3 | |
| SDA / SCL | ESP32 GPIO2 / 1 ↔ AS5600 SDA / SCL | I2C 400 kHz |
| ENC_A / ENC_B / ENC_SW | EC11 A / B / SW → R 10 kΩ → ESP32 GPIO12 / 13 / 11 | 10 nF a GND su ogni ingresso. GPIO11 risveglia dal deep sleep |
| LED_PWM | ESP32 GPIO10 → 100 Ω → gate Q1 (100 kΩ a GND) | |
| LED_K | catodi LED1, LED2 → drain Q1 | Source di Q1 a GND |
| VIB_IN | ESP32 GPIO3 → modulo vibrazione IN | |
| VBAT_ADC | nodo R1/R2/C1 → ESP32 GPIO9 | Metà di VSW |
| M1 / M2 / M3 | SimpleFOC → fili del motore 1503 | L'ordine si aggiusta in firmware |

## Da verificare sul banco
- Resistenze R6/R7 dei filamenti dopo la misura della Vf.
- Se il modulo AS5600 ha già le pull‑up su SDA/SCL (altrimenti 4,7 kΩ a 3V3).
- Modulo vibrazione: dalla foto ha già 5,1 kΩ tra base e GND, quindi niente pull‑down esterna (conferma col tester).

## Letargo (al posto dell'interruttore)
- Pressione di 3 s sul pulsante dell'encoder: il firmware ferma il pendolo, porta PWR_EN a 0 (Q2 spegne boost, driver, LED, AS5600 e vibrazione), mette SDA/SCL in alta impedenza e manda l'ESP32 in deep sleep con risveglio su GPIO11 basso.
- Al risveglio il firmware controlla che il pulsante resti premuto per 3 s; se viene lasciato prima, torna a dormire.
- Restano alimentati solo l'LDO e l'ESP32: consumo atteso di qualche decina di µA (da misurare). Togliere il LED rosso di alimentazione della SuperMini.
- Sull'ESP32‑S3 tutti i GPIO RTC (0–21) svegliano dal deep sleep: il pulsante è su GPIO11.
