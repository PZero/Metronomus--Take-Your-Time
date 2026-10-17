# Taratura della deduzione di piega

Serve a sapere di quanto "si accorcia" il filo a ogni piega a 90° con **la tua pinza e il tuo metodo**. Va fatta una volta, con lo stesso filo che userai.

## Procedura
1. Raddrizza e taglia 5 spezzoni da esattamente **100,0 mm**.
2. Segna su ciascuno il punto a 50,0 mm.
3. Piega a 90° sul segno, sempre con lo stesso attrezzo e lo stesso lato della pinza.
4. Misura con il calibro i due bracci dal vertice esterno fino all'estremità: `a` e `b`.
5. Calcola per ogni spezzone `deduzione_esterna = a + b − 100`, poi fai la media.

## Come si usa
- Lunghezza di taglio = somma delle quote esterne − (numero di pieghe × deduzione_esterna).
- Il valore misurato va scritto qui sotto e in `fili/geometria.yaml` (`deduzione_piega_mm`).

| Data | Attrezzo | Media deduzione (mm) | Note |
|---|---|---|---|
| — | — | — | da misurare |

Valore teorico di riferimento (raggio interno 0,5 mm, Ø 1 mm): circa 1,43 mm misurando sui bordi esterni, circa 0,43 mm misurando sugli assi.
