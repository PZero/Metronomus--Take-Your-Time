---
description: Salva lo stato della sessione nei documenti del progetto
---

Chiudiamo la sessione. Senza rileggere file che non servono:

1. Aggiorna `docs/STATO.md`: data di oggi, fase attuale, cosa è stato fatto in questa sessione, prossimi passi, problemi aperti e cosa aspettiamo da Fabio. **Riscrivi** il file tenendolo sotto le 60 righe: è una fotografia dello stato, non un diario.
2. Aggiungi a `docs/decisioni.md` le decisioni prese oggi (una riga nella tabella: data, decisione, motivazione, alternative scartate). Non riscrivere quelle vecchie e non creare altri file di decisioni.
3. Aggiorna `docs/domande-aperte.md`: chiudi le domande risolte, aggiungi quelle nuove.
4. Se sono cambiati componenti, pin o misure, verifica che siano allineati `hardware/bom.md`, `hardware/pinout.md`, `hardware/schema.md` e `fili/moduli.yaml` (i nomi delle reti sono condivisi tra `hardware/` e `fili/`).
5. Se è cambiata la geometria del rame, lancia `python fili/geometria.py`: deve finire senza errori (pezzi ≥ 10 mm, distanze, schede attraversate) e rigenerare `fili/segmenti.csv` e `modello/metronomus.scad`.
6. Aggiorna `README.md` (vetrina su GitHub) se sono cambiati stato, componenti, foto (`foto/`, senza metadati EXIF/GPS) o render (`render/`): solo sintesi e link ai documenti di dettaglio. Aggiungi la voce di oggi in `CHANGELOG.md`.
7. Prima del commit controlla che nei file non ci siano chiavi, token o password.
8. Fai un commit con un messaggio in italiano che riassume la sessione.
9. Rispondimi con 5 righe al massimo: cosa è stato salvato e da dove ripartire la prossima volta.

Dopo questo comando posso chiudere la chat o usare `/clear`.
