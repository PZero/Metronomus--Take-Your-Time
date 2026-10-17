# Changelog

## 2026-10-17
- Step‑down Mini‑360 disponibile, da tarare a 3,3 V per l'ESP32.
- Boost MT3608 disponibile, da tarare a 12 V.
- Motore 1503 (7,4 V, 0,5 Ω) confermato, con limite di tensione FOC nel firmware.
- Batteria 2 × 18350 (2S) e sensore AS5600 confermati; aggiornata la catena di alimentazione.
- Tutte le decisioni riunite nell'unico file docs/decisioni.md.
- Deciso l'indicatore del tempo: il pendolo punta su una scala Maelzel incisa al laser.
- Identificato il driver: SimpleFOC Mini v1.0 (DRV8313). Aggiunto il vincolo di alimentazione motore ≥ 8 V.
- Creato il progetto: struttura cartelle, README, ruoli dei subagenti.
- Analisi iniziale: punti critici (driver/motore per il moto a pendolo), parti mancanti, idee da aggiungere.
- Procedura di taratura della deduzione di piega per il filo da 1 mm.
