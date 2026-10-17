# Analisi iniziale: cosa manca e cosa si potrebbe aggiungere

_17 ottobre 2026 · prima stesura, prima di aver visto le foto dei componenti._

## 1. Il punto critico: il driver del motore

> **Aggiornamento 17/10:** il driver è un **SimpleFOC Mini v1.0** (DRV8313). Problema risolto: è un driver FOC, adatto al controllo in posizione. Vincolo nuovo: alimentazione motore **8–30 V**.

Il pendolo deve **oscillare**: rallentare, fermarsi all'estremo, invertire, accelerare. È il contrario di quello per cui sono fatti molti brushless.

| Se il driver è… | Funziona per il pendolo? |
|---|---|
| Un **ESC da drone/aereo** (es. 20–30 A, BLHeli) | Male. Non gira piano, di solito non inverte (serve modalità 3D), non tiene una posizione. Sconsigliato. |
| Un **driver FOC per motori gimbal** (SimpleFOC Mini, DRV8313, L6234, B-G431B) | Ottimo. Con un encoder magnetico muove il motore in posizione, lento e fluido, come un pendolo vero. |

E il motore: un **motore gimbal** (es. 2204/2804, alta resistenza di avvolgimento) è l'ideale. Un motore da drone a bassa velocità "scatta" (cogging).

**Proposta:** controllo FOC in posizione con la libreria SimpleFOC. L'angolo segue una sinusoide `θ(t) = A · sin(π · BPM/60 · t)`: ogni estremo dell'oscillazione è un battito. Il movimento sarà identico a quello di un metronomo meccanico.

## 2. Il sensore magnetico

Due possibilità, le foto diranno quale hai:

- **Encoder magnetico assoluto** (AS5600, AS5048A, MT6701): chip sotto l'albero + magnete diametrale incollato sull'albero. Conosce l'angolo in ogni istante. È ciò che serve per il FOC. **Consigliato.**
- **Sensore Hall semplice** (A3144, KY-003) + magnete: dà solo un segnale on/off quando il magnete passa. Basta per sapere "sono al centro" o "sono all'estremo", non per un moto fluido. Utile come finecorsa/azzeramento in aggiunta.

## 3. Alimentazione: cosa manca

Batteria + caricatore USB (probabilmente un TP4056) non bastano da soli:

- **Interruttore** generale (oppure spegnimento software con deep sleep).
- **Regolatore 3,3 V** per l'ESP32 se la batteria è una Li‑ion 1S (3,0–4,2 V). Un LDO a bassa caduta (MCP1700, HT7333, AP2112) o un buck‑boost.
- **Tensione del motore**: il SimpleFOC Mini (DRV8313) richiede **almeno 8 V**, e i motori gimbal lavorano bene a 10–12 V. Con una 1S servono un **boost** (MT3608 o simile) oppure una batteria 2S con caricatore 2S USB‑C.
- **Protezione batteria** (sovrascarica/cortocircuito): i moduli TP4056 "con protezione" hanno il DW01, quelli base no.
- **Misura della batteria**: partitore resistivo verso un ingresso ADC dell'ESP32 per avvisare quando è scarica.
- **Load sharing**: con il TP4056 il metronomo non dovrebbe funzionare mentre ricarica senza un piccolo circuito di condivisione (MOSFET P + diodo Schottky).

## 4. Il LED a tubo sull'albero

- Il motore **oscilla**, non gira in continuo: bastano due fili molto flessibili (silicone 28–30 AWG) con un'ansa morbida, niente contatti striscianti.
- Va pilotato da un MOSFET logic‑level comandato in PWM dall'ESP32: così può **lampeggiare sul battito**, sfumare, segnare l'accento.
- Se è un "filamento LED" (tipo lampadina Edison) serve una limitazione di corrente: lo dimensioniamo con le foto.
- Bilanciamento: il LED a sbalzo crea una coppia di gravità. Va considerato nel controllo (o bilanciato con un contrappeso, anche decorativo).

## 5. Rotary encoder

- Rotazione: BPM, da 40 a 208 (scala Maelzel classica), con accelerazione se giri veloce.
- **Pulsante** (quasi tutti gli encoder lo hanno): start/stop con un click, "tap tempo" battendo il ritmo, pressione lunga per menu (accento, suddivisioni).
- Conviene un debounce hardware (RC 10 kΩ + 10 nF) oltre a quello software.

## 6. Cose che si potrebbero aggiungere

1. **Suono del tic** (il metronomo oggi è muto): un piezo passivo è minimo; un piccolo altoparlante con amplificatore I2S MAX98357A suona molto meglio e permette un "tic" e un "toc" diversi per l'accento.
2. **Accento sul primo battito** (2/4, 3/4, 4/4, 6/8): il LED cambia intensità o colore.
3. ✅ _Scelto: vedi [indicatore-tempo.md](indicatore-tempo.md)._ **Indicatore discreto dei BPM**: niente display per non rovinare l'estetica; si può mostrare il valore con il pendolo stesso (si ferma e "indica" una scala incisa sulla base) o con una app.
4. **Wi‑Fi/Bluetooth**: l'ESP32 li ha già. Una piccola pagina web o BLE MIDI per sincronizzarsi con una DAW.
5. **Auto‑spegnimento** dopo X minuti fermo, deep sleep, risveglio con il click dell'encoder.
6. ✅ _Inclusa nell'indicatore del tempo._ **Scala graduata** incisa al laser sulla base dietro il pendolo, come i metronomi Wittner.

## 7. Il circuito in rame da 1 mm

- **Ossidazione**: il rame nudo scurisce in poche settimane. Opzioni: filo stagnato, vernice trasparente (protettivo per rame o lacca nitro) a fine montaggio, oppure lasciarlo patinare volutamente.
- **Raddrizzare il filo**: tirarlo in trazione (un capo in morsa, l'altro con una pinza o un trapano) lo raddrizza e lo incrudisce. Così i tratti sono perfettamente dritti e le pieghe stanno ferme.
- **Precisione delle pieghe**: le lunghezze di taglio terranno conto della deduzione di piega (circa 0,4 mm a piega con raggio interno 0,5 mm), ma il valore vero va **misurato con pieghe di prova** con la tua pinza.
- **Dima**: hai LightBurn, quindi probabilmente un laser. Una base in multistrato o acrilico con le scanalature incise in scala 1:1 tiene i fili in posizione mentre saldi. È il modo per avere precisione "molto molto alta".
- **Collegamento ai moduli**: i fori dei pin header sono da circa 1,0 mm, quindi il filo da 1 mm entra a fatica o non entra. Meglio saldare il filo di lato al pin (o usare header lunghi e saldare sopra) oppure assottigliare la punta. Da decidere dopo aver visto i moduli.
- **Isolamento in aria**: le reti diverse corrono su piani paralleli separati (almeno 3 mm), gli incroci si fanno scavalcando su un altro livello. GND e VBAT conviene usarli come "telaio" strutturale.
- **Correnti**: 1 mm di rame regge diversi ampere, nessun problema per il motore.

## 8. Meccanica

- Base pesante e stabile (il pendolo scuote), staffa per il motore, posizione dell'encoder magnetico centrata sotto l'albero (tolleranza ±0,5 mm per l'AS5600).
- La struttura in rame può essere anche il supporto dei moduli.

## 9. Cosa mi serve da te

Vedi [domande-aperte.md](domande-aperte.md). Le foto risolvono la maggior parte delle domande.
