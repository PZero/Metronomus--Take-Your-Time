# Pinout ESP32‑C3 SuperMini (bozza)

_17/10/2026 · prima proposta, da verificare su breadboard._

Il C3 SuperMini ha 16 piedini, tutti sul bordo: 5V, GND, 3V3, GPIO 0–10, 20, 21. Ne servono 11 su 13.

| GPIO | Funzione | Collegato a | Note |
|---|---|---|---|
| 5 | PWM fase A | SimpleFOC Mini IN1 | LEDC |
| 6 | PWM fase B | SimpleFOC Mini IN2 | LEDC |
| 7 | PWM fase C | SimpleFOC Mini IN3 | LEDC |
| 10 | Abilitazione driver | SimpleFOC Mini EN | |
| 20 | I2C SDA | AS5600 SDA | Pin UART0 RX: il debug passa dalla USB nativa |
| 21 | I2C SCL | AS5600 SCL | Pin UART0 TX |
| 3 | Encoder A | EC11 A | Pull‑up interna + RC |
| 4 | Encoder B | EC11 B | Pull‑up interna + RC |
| 9 | Pulsante encoder | EC11 SW | È anche il tasto BOOT: va bene, purché non sia premuto all'accensione |
| 1 | LED filamento | Gate MOSFET (100 Ω + 100 kΩ a GND) | |
| 0 | Livello batteria | Partitore 100 k / 100 k | ADC1 |
| 2 | **libero** | — | Strapping: non mettere pull‑down (niente MOSFET qui). Riservato al buzzer |
| 8 | **libero** | — | Ha il LED blu di bordo; strapping |

## Alimentazione
- **3V3** ← uscita del Mini‑360 tarato a 3,3 V. Non usare il pin 5V.
- **GND** comune con driver, AS5600, MT3608 e batteria.
- AS5600: VCC a 3V3, DIR a GND.
- SimpleFOC Mini: nSP (sleep) e nRT (reset) hanno già pull‑up sulla scheda; nFT (fault) eventualmente su GPIO 8.

## Da verificare sul banco
- Frequenza del ciclo FOC con l'AS5600 in I2C a 400 kHz (attesi alcune centinaia di Hz, sufficienti per un pendolo).
- Che il LED di bordo e i pin di strapping non diano problemi all'avvio.
