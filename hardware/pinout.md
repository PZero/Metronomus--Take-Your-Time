# Pinout ESP32‑S3 SuperMini (bozza)

_18/10/2026 · corretto da C3 a S3 (stessa scheda del YouTube Controller); PWM spostati di un pin per le misure vere del driver. Da verificare su breadboard._

L'S3 SuperMini ha 18 piedini sul bordo, in due file da 9 (disegno quotato Nologo):

- **fila 1** (a destra con la USB in alto): 5V, GND, 3V3, GPIO 13, 12, 11, 10, 9, 8
- **fila 2** (a sinistra): TX (GPIO43), RX (GPIO44), GPIO 1, 2, 3, 4, 5, 6, 7

In tutto 15 GPIO: ne servono 14. GPIO0 (BOOT), GPIO48 (LED RGB di bordo) e i pin del retro non si usano.

| GPIO | Funzione | Collegato a | Note |
|---|---|---|---|
| 7 | PWM fase A | SimpleFOC Mini IN1 | LEDC |
| 6 | PWM fase B | SimpleFOC Mini IN2 | LEDC |
| 5 | PWM fase C | SimpleFOC Mini IN3 | LEDC |
| 4 | Accensione rail di potenza (PWR_EN) | Base Q3 2N3904 (10 kΩ + 100 kΩ a GND) | 0 = letargo |
| 2 | I2C SDA | AS5600 SDA | |
| 1 | I2C SCL | AS5600 SCL | |
| 12 | Encoder A | EC11 A | Pull‑up interna, antirimbalzo nel firmware |
| 13 | Encoder B | EC11 B | Pull‑up interna, antirimbalzo nel firmware |
| 8 | Pulsante encoder (ENC_SW) | EC11 SW | Pull‑up interna, antirimbalzo nel firmware. Risveglia dal deep sleep (sull'S3 possono tutti i GPIO RTC 0–21) |
| 10 | LED filamento | Base Q1 2N3904 (470 Ω + 100 kΩ a GND) | |
| 9 | Livello batteria | Partitore 100 k / 100 k | ADC1 (canale 8) |
| 3 | Motorino a vibrazione | Modulo vibrazione IN | Strapping JTAG: conta solo se l'eFuse è programmato (non lo è); il modulo ha già la pull‑down |
| 43 | Stop di emergenza: lettura (STOP) | EN del SimpleFOC, paletti dei finecorsa | Solo ingresso, senza pull‑up (c'è R9 sul driver). È il TX di UART0: all'avvio emette i messaggi del bootloader, quando il driver è spento |
| 44 | Stop di emergenza: armamento (ARMA) | Collare di ottone sul pendolo (filo flessibile) | Uscita a 0 appena parte il firmware; a 1 solo per staccare il pendolo dal finecorsa all'avvio |
| 11 | **libero** | — | Sotto passa il filo di PWR_EN |

Perché questa disposizione: sulla fila 2 i pin 1…7 sono in fila davanti al driver e sotto l'AS5600 (SCL, SDA, vibrazione, PWR_EN, IN3, IN2, IN1). La fila 1 sta dietro, verso la scheda servizi: 3V3, LED e ADC scendono dritti sui suoi pin. Vedi [fili/geometria.py](../fili/geometria.py).

## Alimentazione
- **3V3** ← LDO a basso consumo dalla batteria (sempre acceso). Non usare il pin 5V. Togliere il LED rosso di alimentazione.
- L'S3 SuperMini ha già un regolatore ME6217C33 tra 5V e 3V3: con il pin 5V scollegato resta a vuoto.
- **GND** comune con driver, AS5600, MT3608 e batteria.
- AS5600: VCC a 3V3_SW (Mini‑360, spento in letargo), DIR a GND.
- SimpleFOC Mini: EN alla rete STOP, con R9 10 kΩ verso il suo 3V3 al posto del ponticello (abilitato quando è alimentato e nessun finecorsa è toccato); nSP, nRT, nFT non collegati.

## Stop di emergenza
- Due paletti di rame a ±35° nel piano del pendolo (rete STOP) fanno da finecorsa meccanici; un collare di ottone sul LED (rete ARMA) li tocca per primo.
- **ARMA = 0** (normale): se il pendolo tocca un paletto, EN va a 0 V e il driver si spegne in hardware, anche se il firmware sbaglia (per esempio con l'AS5600 che legge male).
- **Avvio**: in letargo il pendolo cade su un finecorsa. Il firmware mette ARMA = 1, solleva il pendolo piano finché STOP non si apre, poi rimette ARMA = 0 prima di oscillare.
- GPIO43 legge STOP: con ARMA = 0, STOP basso = finecorsa toccato. Il firmware spegne anche PWR_EN e segnala l'errore.

## Da verificare sul banco
- Frequenza del ciclo FOC con l'AS5600 in I2C a 400 kHz (attesi alcune centinaia di Hz, sufficienti per un pendolo).
- Corrente in deep sleep con LDO esterno sul 3V3 (dichiarati ~43 µA per la scheda alimentata dal 5V).
- Che il pin di strapping GPIO3 e il LED di bordo non diano problemi all'avvio.
