# Domande aperte

| # | Domanda | Chi risponde | Stato |
|---|---|---|---|
| 1 | Modello dell'ESP32 | Foto | ✅ ESP32‑S3 SuperMini (corretto il 18/10: 9 pin per fila e LED su GPIO48 nella foto) |
| 2 | Modello del driver brushless: ESC da drone o driver FOC/gimbal? | Fabio | ✅ SimpleFOC Mini v1.0 |
| 3 | Motore brushless | Fabio | ✅ 1503, 7,4 V, 0,5 Ω. Da misurare la resistenza fase‑fase |
| 4 | Batteria | Fabio | ✅ 2 × 18350, collegate in parallelo (1S) |
| 5 | Modulo di ricarica | Foto | ✅ TP4056 USB‑C con protezione, 1S → celle in parallelo |
| 12 | Il metronomo esposto starà sempre collegato all'USB o deve girare a batteria? (autonomia stimata 3–4 h) | Fabio | ✅ deve girare a batteria (18/10): l'autonomia conta |
| 6 | Sensore magnetico | Fabio | ✅ AS5600 |
| 7 | LED a tubo: filamento LED, tubo neon flex, altro? Tensione? | Foto | ✅ filamento LED da 3 V (18/10) |
| 8 | Il tic deve anche suonare? | Fabio | ✅ no, solo vibrazione (18/10) |
| 9 | Rame nudo da lasciare patinare, o protetto con vernice trasparente? | Fabio | rimandata: forse colorato, si decide sul prototipo |
| 10 | Hai un laser (LightBurn) o una stampante 3D per la dima? | Fabio | ✅ non indispensabile (18/10): stampa 1:1 su un piano di sughero con spilli e squadrette; per le discese fa da dima la base forata |
| 11 | Dimensioni indicative dell'oggetto (altezza, ingombro della base) | Fabio | ✅ base di legno circa 150 × 90 mm (18/10) |
| 13 | Quanto sporge l'albero del motore dal retro della base (dove va il magnete)? | Fabio | ✅ non sporge; magnete da 2 mm già fissato sulla parte che ruota (18/10) |
| 14 | Datasheet o misure del modulo AS5600 (fori, file dei pin, centro del chip) | Fabio | aperta |
| 15 | SimpleFOC Mini: ordine M1‑M2‑M3 e quale morsetto è + (serigrafia) | Fabio | ✅ dalla serigrafia della v1.0: M1‑M2‑M3 da sinistra, − verso la fila dei pin, + sotto (18/10). La v1.1 ha la fila IN invertita |
| 16 | Stop di emergenza: finecorsa meccanici in rame a ±(arco + 5°) e, in più, contatto elettrico che spegne il driver da solo (EN a massa) e avvisa l'ESP32? | Fabio | ✅ sì, meccanico + elettrico con armamento (18/10) |
| 18 | Fili flessibili verso il pendolo: con i fili che arrivano dove sono ora servono 30–36 mm (decisi 15–20). Avvicinare le uscite dei LED all'asse? E come sono fatti mozzo e collare sul pendolo? | Fabio / piano fili | ✅ ci pensa Fabio |
| 17 | Massa del motore e massa della logica separate e unite in un solo punto vicino alla batteria? Oggi l'anello è unico, con il ritorno della batteria vicino a driver e MT3608 | Fabio / elettronica | ✅ elettronica (18/10): non serve separare; foro del ritorno batteria spostato tra MT3608 e driver |
| 19 | Pannello della scala: con la base da 150 mm il pannello (170 mm) non entra nella teca. Arco ±30° invece di ±40°, pendolo più corto o base più larga? | Fabio | aperta |
