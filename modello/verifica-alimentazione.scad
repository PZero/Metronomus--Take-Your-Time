// Metronomus: VERIFICA del piano del rame 1:1, GENERATO da fili/verifica_scad.py: non modificarlo a mano.
// I fili sono i pezzi TAGLIATI come dice il PDF (lunghezza di taglio ed estremità), messi al loro posto.

/* [Montaggio] */
// gruppi montati: 1 Struttura, 2 Bus, 3 Batterie, 4 Vibrazione, 5 MT3608, 6 Mini-360, 7 Scheda servizi, 8 ESP32-S3, 9 SimpleFOC Mini, 10 AS5600
passo = 10; // [1:10]
// mostra solo il gruppo del passo (senza quelli già montati)
solo_passo = false;

/* [Vista] */
// saldature: stesso colore = fili saldati insieme (rosso = isola che non porta a niente); montaggio: rame/grigio
colori = "saldature"; // [saldature, montaggio]
schede = true;
// nome scritto su ogni scheda
nomi_schede = true;
// sui pin da collegare: nome del pin e rete
nomi_pin = true;
// base di legno: contorno (si vede tutto quello che c'è sotto e dentro), trasparente o piena
base = "contorno"; // [contorno, trasparente, piena, nascosta]
// moduli e cavetti sotto la base (TP4056, vibrazione, encoder)
sotto = true;
numeri = true;
giunti = true;
problemi = true;
// numero di un pezzo da evidenziare (0 = nessuno)
evidenzia = 0;

/* [Hidden] */
$fn = 16;
R = 0.5;
RAME = [0.85, 0.45, 0.2]; GRIGIO = [0.6, 0.6, 0.6]; ROSSO = [0.95, 0.05, 0.05];
module seg(a, b, r = R) { v = b - a; l = norm(v);
    if (l > 0) translate(a) rotate([0, acos(v[2] / l), atan2(v[1], v[0])]) cylinder(r = r, h = l); }
module cartellino(p, t, s = 1.6, col = [0.1, 0.1, 0.1]) {
    translate(p) rotate([90, 0, 0]) color(col) linear_extrude(0.2) text(t, size = s, halign = "center", valign = "center"); }
function visibile(g) = solo_passo ? g == passo : g <= passo;

echo("VERIFICA: nessun problema, i pezzi del PDF combaciano");

// isole di rame saldate insieme (colori = saldature):
echo("ISOLA 1: GND, 19 pezzi (15..89) -> AS5600 GND, ESP32-S3 GND, Encoder EC11 C (cavetto sotto la base), Encoder EC11 SW2 (cavetto sotto la base), MT3608 VOUT-, Mini-360 OUT-, Scheda servizi GND, SimpleFOC Mini PWR-, TP4056 OUT- (cavetto sotto la base), Vibrazione GND, foro GND (2.4, 19.9) (cavetto sotto la base), foro passante");
echo("ISOLA 2: V12, 7 pezzi (20..82) -> MT3608 VOUT+, Mini-360 IN+, Scheda servizi V12, SimpleFOC Mini PWR+");
echo("ISOLA 3: VSW, 4 pezzi (30..57) -> MT3608 VIN+, Scheda servizi VSW");
echo("ISOLA 4: BATT+, 3 pezzi (35..37) -> TP4056 B+ (cavetto sotto la base), foro passante");
echo("ISOLA 5: BATT-, 3 pezzi (38..40) -> TP4056 B- (cavetto sotto la base), foro passante");
echo("ISOLA 6: VSW, 2 pezzi (42..58) -> Scheda servizi VSW_VIB, Vibrazione VCC, foro VSW (2.4, 22.5) (cavetto sotto la base), foro passante");
echo("ISOLA 7: VBAT, 1 pezzi (59..59) -> Scheda servizi VBAT, TP4056 OUT+ (cavetto sotto la base), foro passante");
echo("ISOLA 8: 3V3_SW, 2 pezzi (94..95) -> AS5600 VCC, Mini-360 OUT+");
PEZZI = [
  [15, 2, [-22.5, 0.0, 6.0], [38.0, 0.0, 6.0], "GND-01", 60.5, [-22.0, 0.0, 6.0], [37.5, 0.0, 6.0], [0.9, 0.27, 0.27]],
  [16, 2, [37.5, 0.5, 6.0], [37.5, 30.0, 6.0], "GND-02", 29.5, [37.5, 0.0, 6.0], [37.5, 29.5, 6.0], [0.9, 0.27, 0.27]],
  [17, 2, [37.0, 29.5, 6.0], [-22.5, 29.5, 6.0], "GND-03", 59.5, [37.5, 29.5, 6.0], [-22.0, 29.5, 6.0], [0.9, 0.27, 0.27]],
  [18, 2, [-22.0, 29.0, 6.0], [-22.0, 0.5, 6.0], "GND-04", 28.5, [-22.0, 29.5, 6.0], [-22.0, 0.0, 6.0], [0.9, 0.27, 0.27]],
  [19, 2, [37.5, 6.72, 5.5], [37.5, 6.72, -20.0], "GND-05", 25.5, [37.5, 6.72, 6.0], [37.5, 6.72, 0.0], [0.9, 0.27, 0.27]],
  [20, 2, [45.8, 4.12, 14.0], [-18.33, 4.12, 14.0], "V12-01", 64.1, [45.8, 4.12, 14.0], [-17.83, 4.12, 14.0], [0.27, 0.454, 0.9]],
  [21, 2, [-17.83, 4.62, 14.0], [-17.83, 24.0, 14.0], "V12-02", 19.4, [-17.83, 4.12, 14.0], [-17.83, 24.0, 14.0], [0.27, 0.454, 0.9]],
  [22, 2, [27.77, 4.62, 14.0], [27.77, 56.26, 14.0], "V12-03", 51.6, [27.77, 4.12, 14.0], [27.77, 56.26, 14.0], [0.27, 0.454, 0.9]],
  [30, 2, [30.31, 56.26, 18.0], [30.31, 36.12, 18.0], "VSW-01", 20.1, [30.31, 56.26, 18.0], [30.31, 36.62, 18.0], [0.638, 0.9, 0.27]],
  [31, 2, [30.81, 36.62, 18.0], [45.8, 36.62, 18.0], "VSW-02", 15.0, [30.31, 36.62, 18.0], [45.8, 36.62, 18.0], [0.638, 0.9, 0.27]],
  [35, 3, [-35.0, 1.5, -20.0], [-35.0, 1.5, 9.5], "BATT+-01", 29.5, [-35.0, 1.5, 0.0], [-35.0, 1.5, 9.0], [0.9, 0.27, 0.821]],
  [36, 3, [-35.5, 1.5, 9.0], [-56.5, 1.5, 9.0], "BATT+-02", 21.0, [-35.0, 1.5, 9.0], [-56.0, 1.5, 9.0], [0.9, 0.27, 0.821]],
  [37, 3, [-56.0, 1.5, 8.5], [-56.0, 1.5, -20.0], "BATT+-03", 28.5, [-56.0, 1.5, 9.0], [-56.0, 1.5, 0.0], [0.9, 0.27, 0.821]],
  [38, 3, [-35.0, 37.5, -20.0], [-35.0, 37.5, 9.5], "BATT--01", 29.5, [-35.0, 37.5, 0.0], [-35.0, 37.5, 9.0], [0.27, 0.9, 0.795]],
  [39, 3, [-35.5, 37.5, 9.0], [-56.5, 37.5, 9.0], "BATT--02", 21.0, [-35.0, 37.5, 9.0], [-56.0, 37.5, 9.0], [0.27, 0.9, 0.795]],
  [40, 3, [-56.0, 37.5, 8.5], [-56.0, 37.5, -20.0], "BATT--03", 28.5, [-56.0, 37.5, 9.0], [-56.0, 37.5, 0.0], [0.27, 0.9, 0.795]],
  [41, 4, [2.37, 19.92, 3.8], [2.37, 19.92, -20.0], "GND-14", 23.8, [2.37, 19.92, 1.3], [2.37, 19.92, 0.0], [0.9, 0.27, 0.27]],
  [42, 4, [2.37, 22.46, 3.8], [2.37, 22.46, -20.0], "VSW-06", 23.8, [2.37, 22.46, 1.3], [2.37, 22.46, 0.0], [0.9, 0.611, 0.27]],
  [43, 5, [52.8, 4.12, 32.5], [52.8, 4.12, 5.5], "GND-06", 27.0, [52.8, 4.12, 30.0], [52.8, 4.12, 6.0], [0.9, 0.27, 0.27]],
  [44, 5, [52.3, 4.12, 6.0], [38.0, 4.12, 6.0], "GND-07", 14.3, [52.8, 4.12, 6.0], [37.5, 4.12, 6.0], [0.9, 0.27, 0.27]],
  [45, 5, [42.8, 4.12, 32.5], [42.8, 4.12, 14.5], "V12-04", 18.0, [42.8, 4.12, 30.0], [42.8, 4.12, 14.0], [0.27, 0.454, 0.9]],
  [46, 5, [42.8, 36.62, 32.5], [42.8, 36.62, 18.5], "VSW-03", 14.0, [42.8, 36.62, 30.0], [42.8, 36.62, 18.0], [0.638, 0.9, 0.27]],
  [47, 6, [-2.83, 11.0, 32.5], [-2.83, 11.0, 5.5], "GND-08", 27.0, [-2.83, 11.0, 30.0], [-2.83, 11.0, 6.0], [0.9, 0.27, 0.27]],
  [48, 6, [-2.83, 10.5, 6.0], [-2.83, 0.5, 6.0], "GND-09", 10.0, [-2.83, 11.0, 6.0], [-2.83, 0.0, 6.0], [0.9, 0.27, 0.27]],
  [49, 6, [-17.83, 21.0, 32.5], [-17.83, 21.0, 14.5], "V12-05", 18.0, [-17.83, 21.0, 30.0], [-17.83, 21.0, 14.0], [0.27, 0.454, 0.9]],
  [50, 7, [22.69, 53.26, 32.5], [22.69, 53.26, 5.5], "GND-10", 27.0, [22.69, 53.26, 30.0], [22.69, 53.26, 6.0], [0.9, 0.27, 0.27]],
  [51, 7, [22.69, 52.76, 6.0], [22.69, 30.0, 6.0], "GND-11", 22.8, [22.69, 53.26, 6.0], [22.69, 29.5, 6.0], [0.9, 0.27, 0.27]],
  [52, 7, [27.77, 53.26, 32.5], [27.77, 53.26, 14.5], "V12-06", 18.0, [27.77, 53.26, 30.0], [27.77, 53.26, 14.0], [0.27, 0.454, 0.9]],
  [57, 7, [30.31, 53.26, 32.5], [30.31, 53.26, 18.5], "VSW-04", 14.0, [30.31, 53.26, 30.0], [30.31, 53.26, 18.0], [0.638, 0.9, 0.27]],
  [58, 7, [32.85, 53.26, 32.5], [32.85, 53.26, -20.0], "VSW-05", 52.5, [32.85, 53.26, 30.0], [32.85, 53.26, 0.0], [0.9, 0.611, 0.27]],
  [59, 7, [20.15, 53.26, 32.5], [20.15, 53.26, -20.0], "VBAT-01", 52.5, [20.15, 53.26, 30.0], [20.15, 53.26, 0.0], [0.427, 0.27, 0.9]],
  [64, 8, [-5.25, 41.0, 32.5], [-5.25, 41.0, 5.5], "GND-12", 27.0, [-5.25, 41.0, 30.0], [-5.25, 41.0, 6.0], [0.9, 0.27, 0.27]],
  [65, 8, [-5.25, 40.5, 6.0], [-5.25, 30.0, 6.0], "GND-13", 10.5, [-5.25, 41.0, 6.0], [-5.25, 29.5, 6.0], [0.9, 0.27, 0.27]],
  [80, 9, [22.58, 9.32, 32.5], [22.58, 9.32, 5.5], "GND-15", 27.0, [22.58, 9.32, 30.0], [22.58, 9.32, 6.0], [0.9, 0.27, 0.27]],
  [81, 9, [23.08, 9.32, 6.0], [37.0, 9.32, 6.0], "GND-16", 13.9, [22.58, 9.32, 6.0], [37.5, 9.32, 6.0], [0.9, 0.27, 0.27]],
  [82, 9, [22.58, 4.12, 32.5], [22.58, 4.12, 14.5], "V12-07", 18.0, [22.58, 4.12, 30.0], [22.58, 4.12, 14.0], [0.27, 0.454, 0.9]],
  [87, 10, [2.25, 11.3, 65.75], [2.25, 21.5, 65.75], "GND-17", 10.2, [2.25, 13.8, 65.75], [2.25, 21.0, 65.75], [0.9, 0.27, 0.27]],
  [88, 10, [2.25, 21.0, 65.25], [2.25, 21.0, 5.5], "GND-18", 59.8, [2.25, 21.0, 65.75], [2.25, 21.0, 6.0], [0.9, 0.27, 0.27]],
  [89, 10, [2.25, 20.5, 6.0], [2.25, 0.5, 6.0], "GND-19", 20.0, [2.25, 21.0, 6.0], [2.25, 0.0, 6.0], [0.9, 0.27, 0.27]],
  [94, 10, [-2.83, 11.3, 65.75], [-2.83, 21.5, 65.75], "3V3_SW-01", 10.2, [-2.83, 13.8, 65.75], [-2.83, 21.0, 65.75], [0.297, 0.9, 0.27]],
  [95, 10, [-2.83, 21.0, 65.25], [-2.83, 21.0, 27.5], "3V3_SW-02", 37.8, [-2.83, 21.0, 65.75], [-2.83, 21.0, 30.0], [0.297, 0.9, 0.27]]
];
for (p = PEZZI) if (visibile(p[1])) {
    col = p[0] == evidenzia ? [0.1, 0.8, 0.2] : colori == "saldature" ? p[8] : (p[1] == passo ? RAME : GRIGIO);
    color(col) seg(p[2], p[3], p[0] == evidenzia ? R * 1.5 : R);
    if (numeri && p[1] == passo) { m = (p[6] + p[7]) / 2; cartellino(m + [1.6, -1.2, 0.8], str(p[0])); }
}
GIUNTI = [
  ["G09", 2, [-22.0, 0.0, 6.0]],
  ["G10", 2, [37.5, 0.0, 6.0]],
  ["G11", 2, [37.5, 29.5, 6.0]],
  ["G12", 2, [-22.0, 29.5, 6.0]],
  ["G13", 2, [37.5, 6.72, 6.0]],
  ["G14", 2, [-17.83, 4.12, 14.0]],
  ["G15", 2, [27.77, 4.12, 14.0]],
  ["G16", 2, [30.31, 36.62, 18.0]],
  ["G21", 3, [-35.0, 1.5, 9.0]],
  ["G22", 3, [-56.0, 1.5, 9.0]],
  ["G23", 3, [-35.0, 37.5, 9.0]],
  ["G24", 3, [-56.0, 37.5, 9.0]],
  ["G25", 5, [52.8, 4.12, 6.0]],
  ["G26", 5, [37.5, 4.12, 6.0]],
  ["G27", 5, [42.8, 4.12, 14.0]],
  ["G28", 5, [42.8, 36.62, 18.0]],
  ["G29", 6, [-2.83, 11.0, 6.0]],
  ["G30", 6, [-2.83, 0.0, 6.0]],
  ["G31", 6, [-17.83, 21.0, 14.0]],
  ["G32", 7, [22.69, 53.26, 6.0]],
  ["G33", 7, [22.69, 29.5, 6.0]],
  ["G34", 7, [27.77, 53.26, 14.0]],
  ["G39", 7, [30.31, 53.26, 18.0]],
  ["G42", 8, [-5.25, 41.0, 6.0]],
  ["G43", 8, [-5.25, 29.5, 6.0]],
  ["G53", 9, [22.58, 9.32, 6.0]],
  ["G54", 9, [37.5, 9.32, 6.0]],
  ["G55", 9, [22.58, 4.12, 14.0]],
  ["G60", 10, [2.25, 21.0, 65.75]],
  ["G61", 10, [2.25, 21.0, 6.0]],
  ["G62", 10, [2.25, 0.0, 6.0]],
  ["G65", 10, [-2.83, 21.0, 65.75]]
];
if (giunti) for (g = GIUNTI) if (visibile(g[1])) {
    color([1, 0.1, 0.1, 0.55]) translate(g[2]) sphere(r = R * 1.5);
    if (numeri && g[1] == passo) cartellino(g[2] + [-2.4, -1.2, 1.4], g[0], 1.2, ROSSO);
}
if (schede) {
  if (visibile(10)) color([0.2, 0.35, 0.7, 0.35]) multmatrix([[0, -1, 0, 11.25], [0, 0, -1, 13.8], [1, 0, 0, 60.75], [0, 0, 0, 1]]) translate([0, 0, -1.6]) cube([22.5, 22.5, 1.6]);  // AS5600
  if (visibile(10)) color([0.9, 0.8, 0.3]) translate([0.0, 13.8, 72.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(10)) color([0.9, 0.8, 0.3]) translate([-2.83, 13.8, 65.75]) sphere(r = 0.35, $fn = 8);
  if (visibile(10)) color([0.9, 0.8, 0.3]) translate([-0.29, 13.8, 65.75]) sphere(r = 0.35, $fn = 8);
  if (visibile(10)) color([0.9, 0.8, 0.3]) translate([2.25, 13.8, 65.75]) sphere(r = 0.35, $fn = 8);
  if (visibile(10)) color([0.9, 0.8, 0.3]) translate([-5.25, 13.8, 78.25]) sphere(r = 0.35, $fn = 8);
  if (visibile(10)) color([0.9, 0.8, 0.3]) translate([-2.71, 13.8, 78.25]) sphere(r = 0.35, $fn = 8);
  if (visibile(10)) color([0.9, 0.8, 0.3]) translate([-0.17, 13.8, 78.25]) sphere(r = 0.35, $fn = 8);
  if (visibile(10)) color([0.9, 0.8, 0.3]) translate([2.37, 13.8, 78.25]) sphere(r = 0.35, $fn = 8);
  if (visibile(10)) multmatrix([[0, -1, 0, 11.25], [0, 0, -1, 13.8], [1, 0, 0, 60.75], [0, 0, 0, 1]]) translate([0, 0, 0.05]) {
    if (nomi_schede) color([0.05, 0.15, 0.45]) translate([11.25, -1.0]) rotate(0) linear_extrude(0.2) text("AS5600", size = 2.00, halign = "center", valign = "top");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([5.900, 14.080, 0]) rotate(0) linear_extrude(0.2) text("VCC", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([4.100, 14.080, 0]) rotate(0) linear_extrude(0.2) text("3V3_SW", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([5.900, 9.000, 0]) rotate(0) linear_extrude(0.2) text("GND", size = 0.8, halign = "left", valign = "center");
  }
  if (visibile(8)) color([0.2, 0.35, 0.7, 0.35]) multmatrix([[0, -1, 0, 13.73], [1, 0, 0, 24.0], [0, 0, 1, 30.0], [0, 0, 0, 1]]) translate([0, 0, -3.0]) cube([18.0, 24.0, 3.0]);  // ESP32-S3
  if (visibile(8)) color([0.9, 0.8, 0.3]) translate([-7.79, 25.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(8)) color([0.9, 0.8, 0.3]) translate([-5.25, 25.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(8)) color([0.9, 0.8, 0.3]) translate([-2.71, 25.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(8)) color([0.9, 0.8, 0.3]) translate([-0.17, 25.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(8)) color([0.9, 0.8, 0.3]) translate([2.37, 25.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(8)) color([0.9, 0.8, 0.3]) translate([4.91, 25.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(8)) color([0.9, 0.8, 0.3]) translate([7.45, 25.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(8)) color([0.9, 0.8, 0.3]) translate([9.99, 25.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(8)) color([0.9, 0.8, 0.3]) translate([12.53, 25.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(8)) color([0.9, 0.8, 0.3]) translate([-7.79, 41.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(8)) color([0.9, 0.8, 0.3]) translate([-5.25, 41.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(8)) color([0.9, 0.8, 0.3]) translate([-2.71, 41.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(8)) color([0.9, 0.8, 0.3]) translate([-0.17, 41.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(8)) color([0.9, 0.8, 0.3]) translate([2.37, 41.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(8)) color([0.9, 0.8, 0.3]) translate([4.91, 41.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(8)) color([0.9, 0.8, 0.3]) translate([7.45, 41.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(8)) color([0.9, 0.8, 0.3]) translate([9.99, 41.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(8)) color([0.9, 0.8, 0.3]) translate([12.53, 41.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(8)) multmatrix([[0, -1, 0, 13.73], [1, 0, 0, 24.0], [0, 0, 1, 30.0], [0, 0, 0, 1]]) translate([0, 0, 0.05]) {
    if (nomi_schede) color([0.05, 0.15, 0.45]) translate([9.0, -1.0]) rotate(0) linear_extrude(0.2) text("ESP32-S3", size = 2.00, halign = "center", valign = "top");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([16.100, 18.980, 0]) rotate(0) linear_extrude(0.2) text("GND", size = 0.8, halign = "right", valign = "center");
  }
  if (visibile(9)) color([0.2, 0.35, 0.7, 0.35]) multmatrix([[1, 0, 0, -0.16999999999999993], [0, 1, 0, -6.199999999999999], [0, 0, 1, 30.0], [0, 0, 0, 1]]) translate([0, 0, -1.6]) cube([26.0, 21.5, 1.6]);  // SimpleFOC Mini
  if (visibile(9)) color([0.9, 0.8, 0.3]) translate([22.58, 9.32, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(9)) color([0.9, 0.8, 0.3]) translate([22.58, 4.12, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(9)) color([0.9, 0.8, 0.3]) translate([4.91, 14.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(9)) color([0.9, 0.8, 0.3]) translate([7.45, 14.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(9)) color([0.9, 0.8, 0.3]) translate([9.99, 14.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(9)) color([0.9, 0.8, 0.3]) translate([12.53, 14.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(9)) color([0.9, 0.8, 0.3]) translate([15.07, 14.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(9)) color([0.9, 0.8, 0.3]) translate([4.91, 11.46, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(9)) color([0.9, 0.8, 0.3]) translate([7.45, 11.46, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(9)) color([0.9, 0.8, 0.3]) translate([9.99, 11.46, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(9)) color([0.9, 0.8, 0.3]) translate([12.53, 11.46, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(9)) color([0.9, 0.8, 0.3]) translate([15.07, 11.46, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(9)) color([0.9, 0.8, 0.3]) translate([8.16, -4.98, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(9)) color([0.9, 0.8, 0.3]) translate([10.7, -4.98, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(9)) color([0.9, 0.8, 0.3]) translate([13.24, -4.98, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(9)) multmatrix([[1, 0, 0, -0.16999999999999993], [0, 1, 0, -6.199999999999999], [0, 0, 1, 30.0], [0, 0, 0, 1]]) translate([0, 0, 0.05]) {
    if (nomi_schede) color([0.05, 0.15, 0.45]) translate([13.0, -1.0]) rotate(0) linear_extrude(0.2) text("SimpleFOC Mini", size = 2.00, halign = "center", valign = "top");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([21.850, 15.520, 0]) rotate(0) linear_extrude(0.2) text("PWR-", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([23.650, 15.520, 0]) rotate(0) linear_extrude(0.2) text("GND", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([21.850, 10.320, 0]) rotate(0) linear_extrude(0.2) text("PWR+", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([23.650, 10.320, 0]) rotate(0) linear_extrude(0.2) text("V12", size = 0.8, halign = "left", valign = "center");
  }
  if (visibile(6)) color([0.2, 0.35, 0.7, 0.35]) multmatrix([[1, 0, 0, -19.33], [0, 1, 0, 10.0], [0, 0, 1, 30.0], [0, 0, 0, 1]]) translate([0, 0, -1.0]) cube([18.0, 12.0, 1.0]);  // Mini-360
  if (visibile(6)) color([0.9, 0.8, 0.3]) translate([-17.83, 21.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(6)) color([0.9, 0.8, 0.3]) translate([-17.83, 11.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(6)) color([0.9, 0.8, 0.3]) translate([-2.83, 21.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(6)) color([0.9, 0.8, 0.3]) translate([-2.83, 11.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(6)) multmatrix([[1, 0, 0, -19.33], [0, 1, 0, 10.0], [0, 0, 1, 30.0], [0, 0, 0, 1]]) translate([0, 0, 0.05]) {
    if (nomi_schede) color([0.05, 0.15, 0.45]) translate([9.0, -1.0]) rotate(0) linear_extrude(0.2) text("Mini-360", size = 2.00, halign = "center", valign = "top");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([1.500, 10.100, 0]) rotate(90) linear_extrude(0.2) text("IN+", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([1.500, 11.900, 0]) rotate(90) linear_extrude(0.2) text("V12", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([16.500, 10.100, 0]) rotate(90) linear_extrude(0.2) text("OUT+", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([16.500, 11.900, 0]) rotate(90) linear_extrude(0.2) text("3V3_SW", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([16.500, 1.900, 0]) rotate(90) linear_extrude(0.2) text("OUT-", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([16.500, 0.100, 0]) rotate(90) linear_extrude(0.2) text("GND", size = 0.8, halign = "right", valign = "center");
  }
  if (visibile(5)) color([0.2, 0.35, 0.7, 0.35]) multmatrix([[0, 1, 0, 38.8], [-1, 0, 0, 39.12], [0, 0, 1, 30.0], [0, 0, 0, 1]]) translate([0, 0, -1.6]) cube([37.5, 18.0, 1.6]);  // MT3608
  if (visibile(5)) color([0.9, 0.8, 0.3]) translate([52.8, 36.62, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(5)) color([0.9, 0.8, 0.3]) translate([42.8, 36.62, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(5)) color([0.9, 0.8, 0.3]) translate([52.8, 4.12, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(5)) color([0.9, 0.8, 0.3]) translate([42.8, 4.12, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(5)) multmatrix([[0, 1, 0, 38.8], [-1, 0, 0, 39.12], [0, 0, 1, 30.0], [0, 0, 0, 1]]) translate([0, 0, 0.05]) {
    if (nomi_schede) color([0.05, 0.15, 0.45]) translate([18.75, 19.0]) rotate(0) linear_extrude(0.2) text("MT3608", size = 2.00, halign = "center", valign = "bottom");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([3.400, 4.000, 0]) rotate(0) linear_extrude(0.2) text("VIN+", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([1.600, 4.000, 0]) rotate(0) linear_extrude(0.2) text("VSW", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([34.100, 14.000, 0]) rotate(0) linear_extrude(0.2) text("VOUT-", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([35.900, 14.000, 0]) rotate(0) linear_extrude(0.2) text("GND", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([34.100, 4.000, 0]) rotate(0) linear_extrude(0.2) text("VOUT+", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([35.900, 4.000, 0]) rotate(0) linear_extrude(0.2) text("V12", size = 0.8, halign = "left", valign = "center");
  }
  if (visibile(7)) color([0.2, 0.35, 0.7, 0.35]) multmatrix([[1, 0, 0, -4.51], [0, 1, 0, 48.18], [0, 0, 1, 30.0], [0, 0, 0, 1]]) translate([0, 0, -1.6]) cube([39.160000000000004, 10.16, 1.6]);  // Scheda servizi
  if (visibile(7)) color([0.9, 0.8, 0.3]) translate([-2.71, 53.26, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(7)) color([0.9, 0.8, 0.3]) translate([4.91, 53.26, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(7)) color([0.9, 0.8, 0.3]) translate([7.45, 53.26, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(7)) color([0.9, 0.8, 0.3]) translate([9.99, 53.26, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(7)) color([0.9, 0.8, 0.3]) translate([15.07, 53.26, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(7)) color([0.9, 0.8, 0.3]) translate([17.61, 53.26, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(7)) color([0.9, 0.8, 0.3]) translate([20.15, 53.26, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(7)) color([0.9, 0.8, 0.3]) translate([22.69, 53.26, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(7)) color([0.9, 0.8, 0.3]) translate([27.77, 53.26, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(7)) color([0.9, 0.8, 0.3]) translate([30.31, 53.26, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(7)) color([0.9, 0.8, 0.3]) translate([32.85, 53.26, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(7)) multmatrix([[1, 0, 0, -4.51], [0, 1, 0, 48.18], [0, 0, 1, 30.0], [0, 0, 0, 1]]) translate([0, 0, 0.05]) {
    if (nomi_schede) color([0.05, 0.15, 0.45]) translate([19.580000000000002, -1.0]) rotate(0) linear_extrude(0.2) text("Scheda servizi", size = 2.00, halign = "center", valign = "top");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([24.660, 4.180, 0]) rotate(90) linear_extrude(0.2) text("VBAT", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([27.200, 4.180, 0]) rotate(90) linear_extrude(0.2) text("GND", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([32.280, 4.180, 0]) rotate(90) linear_extrude(0.2) text("V12", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([35.720, 5.080, 0]) rotate(0) linear_extrude(0.2) text("VSW", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([38.260, 5.080, 0]) rotate(0) linear_extrude(0.2) text("VSW_VIB VSW", size = 0.8, halign = "left", valign = "center");
  }
  if (visibile(4)) color([0.2, 0.35, 0.7, 0.35]) multmatrix([[1, 0, 0, 1.1], [0, 1, 0, 17.92], [0, 0, 1, 1.3], [0, 0, 0, 1]]) translate([0, 0, -1.0]) cube([15.0, 10.0, 1.0]);  // Vibrazione
  if (visibile(4)) color([0.9, 0.8, 0.3]) translate([2.37, 19.92, 1.3]) sphere(r = 0.35, $fn = 8);
  if (visibile(4)) color([0.9, 0.8, 0.3]) translate([2.37, 22.46, 1.3]) sphere(r = 0.35, $fn = 8);
  if (visibile(4)) color([0.9, 0.8, 0.3]) translate([2.37, 25.0, 1.3]) sphere(r = 0.35, $fn = 8);
  if (visibile(4)) multmatrix([[1, 0, 0, 1.1], [0, 1, 0, 17.92], [0, 0, 1, 1.3], [0, 0, 0, 1]]) translate([0, 0, 0.05]) {
    if (nomi_schede) color([0.05, 0.15, 0.45]) translate([7.5, 11.0]) rotate(0) linear_extrude(0.2) text("Vibrazione", size = 2.00, halign = "center", valign = "bottom");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([2.170, 2.000, 0]) rotate(0) linear_extrude(0.2) text("GND", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([2.170, 4.540, 0]) rotate(0) linear_extrude(0.2) text("VCC", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([0.370, 4.540, 0]) rotate(0) linear_extrude(0.2) text("VSW", size = 0.8, halign = "right", valign = "center");
  }
  color([0.75, 0.75, 0.78, 0.5]) seg([0.0, 9.0, 72.0], [0.0, -6.0, 72.0], 9.5);  // motore
  color([0.25, 0.55, 0.95, 0.4]) seg([-35.0, 2.0, 9.0], [-35.0, 37.0, 9.0], 9.0);  // 18350
  color([0.25, 0.55, 0.95, 0.4]) seg([-56.0, 2.0, 9.0], [-56.0, 37.0, 9.0], 9.0);  // 18350
}
if (base == "piena" || base == "trasparente") color([0.55, 0.33, 0.17, base == "piena" ? 1 : 0.25]) translate([-75.0, -22.0, -22.0]) cube([150.0, 90.0, 22.0]);
if (base == "contorno") color([0.55, 0.33, 0.17]) { seg([-75.0, -22.0, -22.0], [75.0, -22.0, -22.0], 0.3); seg([-75.0, -22.0, 0.0], [75.0, -22.0, 0.0], 0.3); seg([-75.0, 68.0, -22.0], [75.0, 68.0, -22.0], 0.3); seg([-75.0, 68.0, 0.0], [75.0, 68.0, 0.0], 0.3); seg([-75.0, -22.0, -22.0], [-75.0, 68.0, -22.0], 0.3); seg([-75.0, -22.0, 0.0], [-75.0, 68.0, 0.0], 0.3); seg([75.0, -22.0, -22.0], [75.0, 68.0, -22.0], 0.3); seg([75.0, -22.0, 0.0], [75.0, 68.0, 0.0], 0.3); seg([-75.0, -22.0, -22.0], [-75.0, -22.0, 0.0], 0.3); seg([-75.0, 68.0, -22.0], [-75.0, 68.0, 0.0], 0.3); seg([75.0, -22.0, -22.0], [75.0, -22.0, 0.0], 0.3); seg([75.0, 68.0, -22.0], [75.0, 68.0, 0.0], 0.3); }
if (sotto) {
  color([0.15, 0.2, 0.35, 0.7]) translate([-28.0, 35.9, -21.8]) cube([17.4, 26.1, 4.6]);  // TP4056
  if (nomi_schede) cartellino([-19.3, 35.7, -23.3], "TP4056", 1.8, [0.05, 0.15, 0.45]);
  color([0.9, 0.8, 0.3]) translate([-12.3, 37.3, -18.5]) sphere(r = 0.45, $fn = 8);
  if (nomi_pin) translate([-12.3, 37.3, -19.7]) rotate([180, 0, 0]) color([0.6, 0.05, 0.05]) linear_extrude(0.2) text("OUT-", size = 0.9, halign = "center", valign = "center");
  color([0.9, 0.8, 0.3]) translate([-15.55, 37.3, -18.5]) sphere(r = 0.45, $fn = 8);
  if (nomi_pin) translate([-15.55, 37.3, -19.7]) rotate([180, 0, 0]) color([0.6, 0.05, 0.05]) linear_extrude(0.2) text("B-", size = 0.9, halign = "center", valign = "center");
  color([0.9, 0.8, 0.3]) translate([-23.05, 37.3, -18.5]) sphere(r = 0.45, $fn = 8);
  if (nomi_pin) translate([-23.05, 37.3, -19.7]) rotate([180, 0, 0]) color([0.6, 0.05, 0.05]) linear_extrude(0.2) text("B+", size = 0.9, halign = "center", valign = "center");
  color([0.9, 0.8, 0.3]) translate([-26.3, 37.3, -18.5]) sphere(r = 0.45, $fn = 8);
  if (nomi_pin) translate([-26.3, 37.3, -19.7]) rotate([180, 0, 0]) color([0.6, 0.05, 0.05]) linear_extrude(0.2) text("OUT+", size = 0.9, halign = "center", valign = "center");
  color([0.9, 0.8, 0.3]) translate([-12.3, 60.6, -18.5]) sphere(r = 0.45, $fn = 8);
  if (nomi_pin) translate([-12.3, 60.6, -19.7]) rotate([180, 0, 0]) color([0.6, 0.05, 0.05]) linear_extrude(0.2) text("IN-", size = 0.9, halign = "center", valign = "center");
  color([0.9, 0.8, 0.3]) translate([-26.3, 60.6, -18.5]) sphere(r = 0.45, $fn = 8);
  if (nomi_pin) translate([-26.3, 60.6, -19.7]) rotate([180, 0, 0]) color([0.6, 0.05, 0.05]) linear_extrude(0.2) text("IN+", size = 0.9, halign = "center", valign = "center");
  color([0.15, 0.2, 0.35, 0.7]) translate([39.0, -20.5, -17.0]) cube([12.0, 12.0, 12.0]);  // Encoder EC11
  if (nomi_schede) cartellino([45.0, -20.7, -18.5], "Encoder EC11", 1.8, [0.05, 0.15, 0.45]);
  color([0.9, 0.8, 0.3]) translate([42.5, -10.0, -17.0]) sphere(r = 0.45, $fn = 8);
  if (nomi_pin) translate([42.5, -10.0, -18.2]) rotate([180, 0, 0]) color([0.6, 0.05, 0.05]) linear_extrude(0.2) text("A", size = 0.9, halign = "center", valign = "center");
  color([0.9, 0.8, 0.3]) translate([45.0, -10.0, -17.0]) sphere(r = 0.45, $fn = 8);
  if (nomi_pin) translate([45.0, -10.0, -18.2]) rotate([180, 0, 0]) color([0.6, 0.05, 0.05]) linear_extrude(0.2) text("C", size = 0.9, halign = "center", valign = "center");
  color([0.9, 0.8, 0.3]) translate([47.5, -10.0, -17.0]) sphere(r = 0.45, $fn = 8);
  if (nomi_pin) translate([47.5, -10.0, -18.2]) rotate([180, 0, 0]) color([0.6, 0.05, 0.05]) linear_extrude(0.2) text("B", size = 0.9, halign = "center", valign = "center");
  color([0.9, 0.8, 0.3]) translate([42.5, -19.0, -17.0]) sphere(r = 0.45, $fn = 8);
  if (nomi_pin) translate([42.5, -19.0, -18.2]) rotate([180, 0, 0]) color([0.6, 0.05, 0.05]) linear_extrude(0.2) text("SW1", size = 0.9, halign = "center", valign = "center");
  color([0.9, 0.8, 0.3]) translate([47.5, -19.0, -17.0]) sphere(r = 0.45, $fn = 8);
  if (nomi_pin) translate([47.5, -19.0, -18.2]) rotate([180, 0, 0]) color([0.6, 0.05, 0.05]) linear_extrude(0.2) text("SW2", size = 0.9, halign = "center", valign = "center");
  color([0.75, 0.75, 0.78]) seg([45.0, -20.5, -11.0], [45.0, -36.5, -11.0], 3);  // albero e pomello dell'encoder
  color([0.3, 0.3, 0.3]) translate([-25.0, 64.0, -20.0]) cube([11.5, 4.0, 8.0]);  // presa USB-C da pannello
  color([0.9, 0.27, 0.821]) seg([-35.0, 1.5, -20.0], [-23.05, 1.5, -20.0], 0.4);  // cavetto BATT+ -> TP4056 B+
  color([0.9, 0.27, 0.821]) seg([-23.05, 1.5, -20.0], [-23.05, 37.3, -20.0], 0.4);  // cavetto BATT+ -> TP4056 B+
  color([0.9, 0.27, 0.821]) seg([-23.05, 37.3, -20.0], [-23.05, 37.3, -18.5], 0.4);  // cavetto BATT+ -> TP4056 B+
  color([0.9, 0.27, 0.821]) translate([-35.0, 1.5, -20.0]) sphere(r = 0.7);
  color([0.27, 0.9, 0.795]) seg([-35.0, 37.5, -20.0], [-35.0, 30.0, -20.0], 0.4);  // cavetto BATT- -> TP4056 B-
  color([0.27, 0.9, 0.795]) seg([-35.0, 30.0, -20.0], [-15.55, 30.0, -20.0], 0.4);  // cavetto BATT- -> TP4056 B-
  color([0.27, 0.9, 0.795]) seg([-15.55, 30.0, -20.0], [-15.55, 37.3, -20.0], 0.4);  // cavetto BATT- -> TP4056 B-
  color([0.27, 0.9, 0.795]) seg([-15.55, 37.3, -20.0], [-15.55, 37.3, -18.5], 0.4);  // cavetto BATT- -> TP4056 B-
  color([0.27, 0.9, 0.795]) translate([-35.0, 37.5, -20.0]) sphere(r = 0.7);
  color([0.427, 0.27, 0.9]) seg([20.15, 53.26, -20.0], [20.15, 32.0, -20.0], 0.4);  // cavetto VBAT -> TP4056 OUT+
  color([0.427, 0.27, 0.9]) seg([20.15, 32.0, -20.0], [-26.3, 32.0, -20.0], 0.4);  // cavetto VBAT -> TP4056 OUT+
  color([0.427, 0.27, 0.9]) seg([-26.3, 32.0, -20.0], [-26.3, 37.3, -20.0], 0.4);  // cavetto VBAT -> TP4056 OUT+
  color([0.427, 0.27, 0.9]) seg([-26.3, 37.3, -20.0], [-26.3, 37.3, -18.5], 0.4);  // cavetto VBAT -> TP4056 OUT+
  color([0.427, 0.27, 0.9]) translate([20.15, 53.26, -20.0]) sphere(r = 0.7);
  color([0.9, 0.27, 0.27]) seg([37.5, 6.72, -20.0], [37.5, 34.0, -20.0], 0.4);  // cavetto GND -> TP4056 OUT-
  color([0.9, 0.27, 0.27]) seg([37.5, 34.0, -20.0], [-12.3, 34.0, -20.0], 0.4);  // cavetto GND -> TP4056 OUT-
  color([0.9, 0.27, 0.27]) seg([-12.3, 34.0, -20.0], [-12.3, 37.3, -20.0], 0.4);  // cavetto GND -> TP4056 OUT-
  color([0.9, 0.27, 0.27]) seg([-12.3, 37.3, -20.0], [-12.3, 37.3, -18.5], 0.4);  // cavetto GND -> TP4056 OUT-
  color([0.9, 0.27, 0.27]) translate([37.5, 6.72, -20.0]) sphere(r = 0.7);
  color([0.9, 0.611, 0.27]) seg([32.85, 53.26, -20.0], [32.85, 45.0, -20.0], 0.4);  // cavetto VSW -> foro VSW (2.4, 22.5)
  color([0.9, 0.611, 0.27]) seg([32.85, 45.0, -20.0], [10.0, 45.0, -20.0], 0.4);  // cavetto VSW -> foro VSW (2.4, 22.5)
  color([0.9, 0.611, 0.27]) seg([10.0, 45.0, -20.0], [10.0, 22.46, -20.0], 0.4);  // cavetto VSW -> foro VSW (2.4, 22.5)
  color([0.9, 0.611, 0.27]) seg([10.0, 22.46, -20.0], [2.37, 22.46, -20.0], 0.4);  // cavetto VSW -> foro VSW (2.4, 22.5)
  color([0.9, 0.611, 0.27]) translate([32.85, 53.26, -20.0]) sphere(r = 0.7);
  color([0.9, 0.27, 0.27]) seg([37.5, 6.72, -20.0], [12.0, 6.72, -20.0], 0.4);  // cavetto GND -> foro GND (2.4, 19.9)
  color([0.9, 0.27, 0.27]) seg([12.0, 6.72, -20.0], [12.0, 19.92, -20.0], 0.4);  // cavetto GND -> foro GND (2.4, 19.9)
  color([0.9, 0.27, 0.27]) seg([12.0, 19.92, -20.0], [2.37, 19.92, -20.0], 0.4);  // cavetto GND -> foro GND (2.4, 19.9)
  color([0.9, 0.27, 0.27]) translate([37.5, 6.72, -20.0]) sphere(r = 0.7);
  color([0.9, 0.27, 0.27]) seg([37.5, 6.72, -20.0], [37.5, -8.0, -20.0], 0.4);  // cavetto GND -> Encoder EC11 C
  color([0.9, 0.27, 0.27]) seg([37.5, -8.0, -20.0], [45.0, -8.0, -20.0], 0.4);  // cavetto GND -> Encoder EC11 C
  color([0.9, 0.27, 0.27]) seg([45.0, -8.0, -20.0], [45.0, -10.0, -20.0], 0.4);  // cavetto GND -> Encoder EC11 C
  color([0.9, 0.27, 0.27]) seg([45.0, -10.0, -20.0], [45.0, -10.0, -17.0], 0.4);  // cavetto GND -> Encoder EC11 C
  color([0.9, 0.27, 0.27]) translate([37.5, 6.72, -20.0]) sphere(r = 0.7);
  color([0.9, 0.27, 0.27]) seg([37.5, 6.72, -20.0], [50.0, 6.72, -20.0], 0.4);  // cavetto GND -> Encoder EC11 SW2
  color([0.9, 0.27, 0.27]) seg([50.0, 6.72, -20.0], [50.0, -19.0, -20.0], 0.4);  // cavetto GND -> Encoder EC11 SW2
  color([0.9, 0.27, 0.27]) seg([50.0, -19.0, -20.0], [47.5, -19.0, -20.0], 0.4);  // cavetto GND -> Encoder EC11 SW2
  color([0.9, 0.27, 0.27]) seg([47.5, -19.0, -20.0], [47.5, -19.0, -17.0], 0.4);  // cavetto GND -> Encoder EC11 SW2
  color([0.9, 0.27, 0.27]) translate([37.5, 6.72, -20.0]) sphere(r = 0.7);
}
