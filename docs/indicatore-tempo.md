# Indicatore del tempo: il pendolo come lancetta

_Decisione di Fabio del 17 ottobre 2026._

Niente display. Il tempo impostato si legge su una **scala ad arco incisa al laser** sulla base, dietro al pendolo, come sui metronomi meccanici Wittner/Maelzel. La lancetta è il **LED a tubo** stesso.

## Comportamento

1. **In oscillazione:** il pendolo batte il tempo normalmente.
2. **Giri l'encoder:** il pendolo frena dolcemente e va a puntare sulla scala il valore BPM selezionato. Il LED resta acceso fisso e più tenue, per distinguere la "modalità impostazione".
3. **Continui a girare:** la lancetta segue il valore scatto per scatto, con movimento morbido senza sobbalzi.
4. **Lasci l'encoder per ~2 s:** il pendolo riparte dalla posizione in cui si trova, sincronizzando la prima oscillazione, e riprende a battere il nuovo tempo.

## La scala

- Valori della **scala Maelzel classica**: un clic dell'encoder corrisponde a un valore della scala.
  - 40–60 a passi di 2 · 60–72 a passi di 3 · 72–120 a passi di 4 · 120–144 a passi di 6 · 144–208 a passi di 8
  - In totale 39 posizioni.
- Accanto ai numeri, i nomi dei tempi: Largo, Larghetto, Adagio, Andante, Moderato, Allegro, Presto.
- Arco della scala: da definire con le dimensioni dell'oggetto (indicativamente ±40° dalla verticale). Lenti a sinistra, veloci a destra.
- Il file vettoriale (SVG/DXF per LightBurn) verrà generato dagli stessi dati del firmware, così scala incisa e angoli della lancetta coincidono per costruzione.

## Conseguenze tecniche

- **Serve un sensore di angolo assoluto** (encoder magnetico tipo AS5600/MT6701 con magnete diametrale sull'albero). Un Hall semplice non basta per puntare un valore preciso, a meno di affiancarlo a un azzeramento all'accensione.
- **Taratura dello zero:** l'angolo "verticale" e l'allineamento della scala si tarano una volta e si salvano in memoria non volatile (NVS) sull'ESP32.
- **Ampiezza dell'oscillazione** e **arco della scala** sono indipendenti: il pendolo può oscillare più o meno ampio dell'arco inciso. Si decide a occhio con il prototipo.
- **Gravità:** con il LED a sbalzo, tenere la lancetta ferma fuori verticale richiede una piccola coppia continua: il controllo in posizione FOC la gestisce, il consumo in modalità impostazione resta basso.
- Il LED a tubo è **dritto verso l'alto** (pendolo rovesciato come in un metronomo classico): la punta superiore è quella che indica la scala.
