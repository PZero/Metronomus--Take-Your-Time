# Pinout ESP32‑C3 SuperMini (bozza)

_17/10/2026 · prima proposta, da verificare su breadboard._

Il C3 SuperMini ha 16 piedini, tutti sul bordo: 5V, GND, 3V3, GPIO 0–10, 20, 21. Ne servono 12 su 13.

| GPIO | Funzione | Collegato a | Note |
|---|---|---|---|
| 5 | PWM fase A | SimpleFOC Mini IN1 | LEDC |
| 6 | PWM fase B | SimpleFOC Mini IN2 | LEDC |
| 7 | PWM fase C | SimpleFOC Mini IN3 | LEDC |
| 10 | Accensione rail di potenza (PWR_EN) | Gate Q3 (100 Ω + 100 kΩ a GND) | 0 = letargo |
| 20 | I2C SDA | AS5600 SDA | Pin UART0 RX: il debug passa dalla USB nativa |
| 21 | I2C SCL | AS5600 SCL | Pin UART0 TX |
| 3 | Encoder A | EC11 A | Pull‑up interna + RC |
| 4 | Encoder B | EC11 B | Pull‑up interna + RC |
| 9 | **libero** | — | Tasto BOOT di bordo, strapping: niente pull‑down |
| 1 | LED filamento | Gate MOSFET (100 Ω + 100 kΩ a GND) | |
| 0 | Livello batteria | Partitore 100 k / 100 k | ADC1 |
| 2 | Pulsante encoder (ENC_SW) | EC11 SW | Pull‑up interna + RC. Risveglia dal deep sleep (solo GPIO 0–5 possono) |
| 8 | Motorino a vibrazione | Modulo vibrazione IN | Ha il LED blu di bordo; strapping (conta solo in modalità download con BOOT premuto) |

## Alimentazione
- **3V3** ← LDO a basso consumo dalla batteria (sempre acceso). Non usare il pin 5V. Togliere il LED rosso di alimentazione.
- **GND** comune con driver, AS5600, MT3608 e batteria.
- AS5600: VCC a 3V3_SW (Mini‑360, spento in letargo), DIR a GND.
- SimpleFOC Mini: EN collegato al suo pin 3V3 (abilitato quando è alimentato); nSP, nRT, nFT non collegati.

## Da verificare sul banco
- Frequenza del ciclo FOC con l'AS5600 in I2C a 400 kHz (attesi alcune centinaia di Hz, sufficienti per un pendolo).
- Che il LED di bordo e i pin di strapping non diano problemi all'avvio.
