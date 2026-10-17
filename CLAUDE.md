# Metronomus · istruzioni per Claude

Metronomo artistico: ESP32 + motore brushless che fa oscillare un LED a tubo da 5 cm, sensore magnetico di posizione, rotary encoder per i BPM, batteria con ricarica USB. Circuito esposto in filo di rame Ø 1 mm: segmenti dritti tagliati e saldati ad angolo retto, nessuna piega, precisione molto alta.

- Scrivi sempre in italiano (README, documenti, commit).
- Usa i ruoli definiti in `agenti/` (copiati in `.claude/agents/` per Claude Code): `coordinatore`, `git-readme`, `elettronica`, `piano-fili`.
- I nomi delle reti elettriche sono condivisi tra `hardware/` e `fili/`: cambiarne uno significa aggiornare entrambi.
- Dopo ogni modifica significativa: aggiorna README e CHANGELOG, poi commit (ruolo `git-readme`).
- **Tutte** le decisioni vanno nell'unico file `docs/decisioni.md` (riga nella tabella + eventuale sezione di dettaglio): mai un file .md per singola decisione. Domande per Fabio in `docs/domande-aperte.md`.
