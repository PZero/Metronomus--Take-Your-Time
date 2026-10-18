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
echo("ISOLA 1: STOP, 7 pezzi (1..86) -> ESP32-S3 GPIO43, SimpleFOC Mini EN, ancorato nella base");
echo("ISOLA 2: PWM_A, 3 pezzi (23..83) -> ESP32-S3 GPIO7, SimpleFOC Mini IN1");
echo("ISOLA 3: PWM_B, 3 pezzi (24..84) -> ESP32-S3 GPIO6, SimpleFOC Mini IN2");
echo("ISOLA 4: PWM_C, 3 pezzi (25..85) -> ESP32-S3 GPIO5, SimpleFOC Mini IN3");
echo("ISOLA 5: PWR_EN, 3 pezzi (26..69) -> ESP32-S3 GPIO4, Scheda servizi PWR_EN");
echo("ISOLA 6: LED_PWM, 3 pezzi (28..71) -> ESP32-S3 GPIO10, Scheda servizi LED_PWM");
echo("ISOLA 7: VBAT_ADC, 3 pezzi (29..72) -> ESP32-S3 GPIO9, Scheda servizi ADC");
echo("ISOLA 8: VIB_IN, 1 pezzi (73..73) -> ESP32-S3 GPIO3, Vibrazione IN");
echo("ISOLA 9: ENC_SW, 1 pezzi (74..74) -> ESP32-S3 GPIO8, Encoder EC11 SW1 (cavetto sotto la base), foro passante");
echo("ISOLA 10: ENC_A, 1 pezzi (75..75) -> ESP32-S3 GPIO12, Encoder EC11 A (cavetto sotto la base), foro passante");
echo("ISOLA 11: ENC_B, 1 pezzi (76..76) -> ESP32-S3 GPIO13, Encoder EC11 B (cavetto sotto la base), foro passante");
echo("ISOLA 12: ARMA, 2 pezzi (78..79) -> ESP32-S3 GPIO44, filo flessibile");
echo("ISOLA 13: SCL, 2 pezzi (90..91) -> AS5600 SCL, ESP32-S3 GPIO1");
echo("ISOLA 14: SDA, 2 pezzi (92..93) -> AS5600 SDA, ESP32-S3 GPIO2");
PEZZI = [
  [1, 1, [-20.0, -11.5, -5.0], [-20.0, -11.5, 94.5], "STOP-01", 99.5, [-20.0, -11.5, 0.0], [-20.0, -11.5, 94.5], [0.9, 0.27, 0.27]],
  [2, 1, [20.0, -11.5, -5.0], [20.0, -11.5, 94.5], "STOP-02", 99.5, [20.0, -11.5, 0.0], [20.0, -11.5, 94.5], [0.9, 0.27, 0.27]],
  [23, 2, [12.53, 11.0, 18.0], [12.53, 28.0, 18.0], "PWM_A-01", 17.0, [12.53, 11.0, 18.0], [12.53, 28.0, 18.0], [0.27, 0.454, 0.9]],
  [24, 2, [9.99, 11.0, 18.0], [9.99, 28.0, 18.0], "PWM_B-01", 17.0, [9.99, 11.0, 18.0], [9.99, 28.0, 18.0], [0.638, 0.9, 0.27]],
  [25, 2, [7.45, 11.0, 18.0], [7.45, 28.0, 18.0], "PWM_C-01", 17.0, [7.45, 11.0, 18.0], [7.45, 28.0, 18.0], [0.9, 0.27, 0.821]],
  [26, 2, [4.91, 22.0, 18.0], [4.91, 56.26, 18.0], "PWR_EN-01", 34.3, [4.91, 22.0, 18.0], [4.91, 56.26, 18.0], [0.27, 0.9, 0.795]],
  [28, 2, [7.45, 38.0, 18.0], [7.45, 56.26, 18.0], "LED_PWM-01", 18.3, [7.45, 38.0, 18.0], [7.45, 56.26, 18.0], [0.9, 0.611, 0.27]],
  [29, 2, [9.99, 38.0, 18.0], [9.99, 56.26, 18.0], "VBAT_ADC-01", 18.3, [9.99, 38.0, 18.0], [9.99, 56.26, 18.0], [0.427, 0.27, 0.9]],
  [32, 2, [-19.5, -11.5, 18.0], [19.5, -11.5, 18.0], "STOP-03", 39.0, [-20.0, -11.5, 18.0], [20.0, -11.5, 18.0], [0.9, 0.27, 0.27]],
  [33, 2, [4.91, 17.0, 18.0], [4.91, -11.0, 18.0], "STOP-04", 28.0, [4.91, 17.0, 18.0], [4.91, -11.5, 18.0], [0.9, 0.27, 0.27]],
  [34, 2, [-7.79, 28.0, 18.0], [-7.79, -11.0, 18.0], "STOP-06", 39.0, [-7.79, 28.0, 18.0], [-7.79, -11.5, 18.0], [0.9, 0.27, 0.27]],
  [53, 7, [4.91, 53.26, 32.5], [4.91, 53.26, 18.5], "PWR_EN-02", 14.0, [4.91, 53.26, 30.0], [4.91, 53.26, 18.0], [0.27, 0.9, 0.795]],
  [55, 7, [7.45, 53.26, 32.5], [7.45, 53.26, 18.5], "LED_PWM-02", 14.0, [7.45, 53.26, 30.0], [7.45, 53.26, 18.0], [0.9, 0.611, 0.27]],
  [56, 7, [9.99, 53.26, 32.5], [9.99, 53.26, 18.5], "VBAT_ADC-02", 14.0, [9.99, 53.26, 30.0], [9.99, 53.26, 18.0], [0.427, 0.27, 0.9]],
  [66, 8, [12.53, 25.0, 32.5], [12.53, 25.0, 18.5], "PWM_A-02", 14.0, [12.53, 25.0, 30.0], [12.53, 25.0, 18.0], [0.27, 0.454, 0.9]],
  [67, 8, [9.99, 25.0, 32.5], [9.99, 25.0, 18.5], "PWM_B-02", 14.0, [9.99, 25.0, 30.0], [9.99, 25.0, 18.0], [0.638, 0.9, 0.27]],
  [68, 8, [7.45, 25.0, 32.5], [7.45, 25.0, 18.5], "PWM_C-02", 14.0, [7.45, 25.0, 30.0], [7.45, 25.0, 18.0], [0.9, 0.27, 0.821]],
  [69, 8, [4.91, 25.0, 32.5], [4.91, 25.0, 18.5], "PWR_EN-03", 14.0, [4.91, 25.0, 30.0], [4.91, 25.0, 18.0], [0.27, 0.9, 0.795]],
  [71, 8, [7.45, 41.0, 32.5], [7.45, 41.0, 18.5], "LED_PWM-03", 14.0, [7.45, 41.0, 30.0], [7.45, 41.0, 18.0], [0.9, 0.611, 0.27]],
  [72, 8, [9.99, 41.0, 32.5], [9.99, 41.0, 18.5], "VBAT_ADC-03", 14.0, [9.99, 41.0, 30.0], [9.99, 41.0, 18.0], [0.427, 0.27, 0.9]],
  [73, 8, [2.37, 25.0, 32.5], [2.37, 25.0, -1.2], "VIB_IN-01", 33.7, [2.37, 25.0, 30.0], [2.37, 25.0, 1.3], [0.297, 0.9, 0.27]],
  [74, 8, [12.53, 41.0, 32.5], [12.53, 41.0, -20.0], "ENC_SW-01", 52.5, [12.53, 41.0, 30.0], [12.53, 41.0, 0.0], [0.9, 0.27, 0.481]],
  [75, 8, [2.37, 41.0, 32.5], [2.37, 41.0, -20.0], "ENC_A-01", 52.5, [2.37, 41.0, 30.0], [2.37, 41.0, 0.0], [0.27, 0.664, 0.9]],
  [76, 8, [-0.17, 41.0, 32.5], [-0.17, 41.0, -20.0], "ENC_B-01", 52.5, [-0.17, 41.0, 30.0], [-0.17, 41.0, 0.0], [0.848, 0.9, 0.27]],
  [77, 8, [-7.79, 25.0, 32.5], [-7.79, 25.0, 18.5], "STOP-07", 14.0, [-7.79, 25.0, 30.0], [-7.79, 25.0, 18.0], [0.9, 0.27, 0.27]],
  [78, 8, [-5.25, 25.0, 27.5], [-5.25, 25.0, 95.5], "ARMA-01", 68.0, [-5.25, 25.0, 30.0], [-5.25, 25.0, 95.0], [0.768, 0.27, 0.9]],
  [79, 8, [-5.25, 24.5, 95.0], [-5.25, -3.5, 95.0], "ARMA-02", 28.0, [-5.25, 25.0, 95.0], [-5.25, -3.5, 95.0], [0.768, 0.27, 0.9]],
  [83, 9, [12.53, 14.0, 32.5], [12.53, 14.0, 18.5], "PWM_A-03", 14.0, [12.53, 14.0, 30.0], [12.53, 14.0, 18.0], [0.27, 0.454, 0.9]],
  [84, 9, [9.99, 14.0, 32.5], [9.99, 14.0, 18.5], "PWM_B-03", 14.0, [9.99, 14.0, 30.0], [9.99, 14.0, 18.0], [0.638, 0.9, 0.27]],
  [85, 9, [7.45, 14.0, 32.5], [7.45, 14.0, 18.5], "PWM_C-03", 14.0, [7.45, 14.0, 30.0], [7.45, 14.0, 18.0], [0.9, 0.27, 0.821]],
  [86, 9, [4.91, 14.0, 32.5], [4.91, 14.0, 18.5], "STOP-05", 14.0, [4.91, 14.0, 30.0], [4.91, 14.0, 18.0], [0.9, 0.27, 0.27]],
  [90, 10, [-2.71, 11.3, 78.25], [-2.71, 25.5, 78.25], "SCL-01", 14.2, [-2.71, 13.8, 78.25], [-2.71, 25.0, 78.25], [0.27, 0.9, 0.584]],
  [91, 10, [-2.71, 25.0, 77.75], [-2.71, 25.0, 27.5], "SCL-02", 50.2, [-2.71, 25.0, 78.25], [-2.71, 25.0, 30.0], [0.27, 0.9, 0.584]],
  [92, 10, [-0.17, 11.3, 78.25], [-0.17, 25.5, 78.25], "SDA-01", 14.2, [-0.17, 13.8, 78.25], [-0.17, 25.0, 78.25], [0.9, 0.4, 0.27]],
  [93, 10, [-0.17, 25.0, 77.75], [-0.17, 25.0, 27.5], "SDA-02", 50.2, [-0.17, 25.0, 78.25], [-0.17, 25.0, 30.0], [0.9, 0.4, 0.27]]
];
for (p = PEZZI) if (visibile(p[1])) {
    col = p[0] == evidenzia ? [0.1, 0.8, 0.2] : colori == "saldature" ? p[8] : (p[1] == passo ? RAME : GRIGIO);
    color(col) seg(p[2], p[3], p[0] == evidenzia ? R * 1.5 : R);
    if (numeri && p[1] == passo) { m = (p[6] + p[7]) / 2; cartellino(m + [1.6, -1.2, 0.8], str(p[0])); }
}
GIUNTI = [
  ["G17", 2, [-20.0, -11.5, 18.0]],
  ["G18", 2, [20.0, -11.5, 18.0]],
  ["G19", 2, [4.91, -11.5, 18.0]],
  ["G20", 2, [-7.79, -11.5, 18.0]],
  ["G35", 7, [4.91, 53.26, 18.0]],
  ["G37", 7, [7.45, 53.26, 18.0]],
  ["G38", 7, [9.99, 53.26, 18.0]],
  ["G44", 8, [12.53, 25.0, 18.0]],
  ["G45", 8, [9.99, 25.0, 18.0]],
  ["G46", 8, [7.45, 25.0, 18.0]],
  ["G47", 8, [4.91, 25.0, 18.0]],
  ["G49", 8, [7.45, 41.0, 18.0]],
  ["G50", 8, [9.99, 41.0, 18.0]],
  ["G51", 8, [-7.79, 25.0, 18.0]],
  ["G52", 8, [-5.25, 25.0, 95.0]],
  ["G56", 9, [12.53, 14.0, 18.0]],
  ["G57", 9, [9.99, 14.0, 18.0]],
  ["G58", 9, [7.45, 14.0, 18.0]],
  ["G59", 9, [4.91, 14.0, 18.0]],
  ["G63", 10, [-2.71, 25.0, 78.25]],
  ["G64", 10, [-0.17, 25.0, 78.25]]
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
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([16.600, 13.960, 0]) rotate(0) linear_extrude(0.2) text("SCL", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([16.600, 11.420, 0]) rotate(0) linear_extrude(0.2) text("SDA", size = 0.8, halign = "right", valign = "center");
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
    if (nomi_schede) color([0.05, 0.15, 0.45]) translate([9.0, 25.0]) rotate(0) linear_extrude(0.2) text("ESP32-S3", size = 2.00, halign = "center", valign = "bottom");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([1.900, 21.520, 0]) rotate(0) linear_extrude(0.2) text("GPIO43", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([0.100, 21.520, 0]) rotate(0) linear_extrude(0.2) text("STOP", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([1.900, 18.980, 0]) rotate(0) linear_extrude(0.2) text("GPIO44", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([0.100, 18.980, 0]) rotate(0) linear_extrude(0.2) text("ARMA", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([1.900, 16.440, 0]) rotate(0) linear_extrude(0.2) text("GPIO1", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([0.100, 16.440, 0]) rotate(0) linear_extrude(0.2) text("SCL", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([1.900, 13.900, 0]) rotate(0) linear_extrude(0.2) text("GPIO2", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([0.100, 13.900, 0]) rotate(0) linear_extrude(0.2) text("SDA", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([1.900, 11.360, 0]) rotate(0) linear_extrude(0.2) text("GPIO3", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([0.100, 11.360, 0]) rotate(0) linear_extrude(0.2) text("VIB_IN", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([1.900, 8.820, 0]) rotate(0) linear_extrude(0.2) text("GPIO4", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([0.100, 8.820, 0]) rotate(0) linear_extrude(0.2) text("PWR_EN", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([1.900, 6.280, 0]) rotate(0) linear_extrude(0.2) text("GPIO5", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([0.100, 6.280, 0]) rotate(0) linear_extrude(0.2) text("PWM_C", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([1.900, 3.740, 0]) rotate(0) linear_extrude(0.2) text("GPIO6", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([0.100, 3.740, 0]) rotate(0) linear_extrude(0.2) text("PWM_B", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([1.900, 1.200, 0]) rotate(0) linear_extrude(0.2) text("GPIO7", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([0.100, 1.200, 0]) rotate(0) linear_extrude(0.2) text("PWM_A", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([16.100, 13.900, 0]) rotate(0) linear_extrude(0.2) text("GPIO13", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([17.900, 13.900, 0]) rotate(0) linear_extrude(0.2) text("ENC_B", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([16.100, 11.360, 0]) rotate(0) linear_extrude(0.2) text("GPIO12", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([17.900, 11.360, 0]) rotate(0) linear_extrude(0.2) text("ENC_A", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([16.100, 6.280, 0]) rotate(0) linear_extrude(0.2) text("GPIO10", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([17.900, 6.280, 0]) rotate(0) linear_extrude(0.2) text("LED_PWM", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([16.100, 3.740, 0]) rotate(0) linear_extrude(0.2) text("GPIO9", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([17.900, 3.740, 0]) rotate(0) linear_extrude(0.2) text("VBAT_ADC", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([16.100, 1.200, 0]) rotate(0) linear_extrude(0.2) text("GPIO8", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([17.900, 1.200, 0]) rotate(0) linear_extrude(0.2) text("ENC_SW", size = 0.8, halign = "left", valign = "center");
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
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([5.080, 19.300, 0]) rotate(90) linear_extrude(0.2) text("EN", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([5.080, 21.100, 0]) rotate(90) linear_extrude(0.2) text("STOP", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([7.620, 21.100, 0]) rotate(90) linear_extrude(0.2) text("IN3 PWM_C", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([10.160, 21.100, 0]) rotate(90) linear_extrude(0.2) text("IN2 PWM_B", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([12.700, 21.100, 0]) rotate(90) linear_extrude(0.2) text("IN1 PWM_A", size = 0.8, halign = "left", valign = "center");
  }
  if (visibile(6)) color([0.2, 0.35, 0.7, 0.35]) multmatrix([[1, 0, 0, -19.33], [0, 1, 0, 10.0], [0, 0, 1, 30.0], [0, 0, 0, 1]]) translate([0, 0, -1.0]) cube([18.0, 12.0, 1.0]);  // Mini-360
  if (visibile(6)) color([0.9, 0.8, 0.3]) translate([-17.83, 21.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(6)) color([0.9, 0.8, 0.3]) translate([-17.83, 11.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(6)) color([0.9, 0.8, 0.3]) translate([-2.83, 21.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(6)) color([0.9, 0.8, 0.3]) translate([-2.83, 11.0, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(6)) multmatrix([[1, 0, 0, -19.33], [0, 1, 0, 10.0], [0, 0, 1, 30.0], [0, 0, 0, 1]]) translate([0, 0, 0.05]) {
    if (nomi_schede) color([0.05, 0.15, 0.45]) translate([9.0, -1.0]) rotate(0) linear_extrude(0.2) text("Mini-360", size = 2.00, halign = "center", valign = "top");
  }
  if (visibile(5)) color([0.2, 0.35, 0.7, 0.35]) multmatrix([[0, 1, 0, 38.8], [-1, 0, 0, 39.12], [0, 0, 1, 30.0], [0, 0, 0, 1]]) translate([0, 0, -1.6]) cube([37.5, 18.0, 1.6]);  // MT3608
  if (visibile(5)) color([0.9, 0.8, 0.3]) translate([52.8, 36.62, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(5)) color([0.9, 0.8, 0.3]) translate([42.8, 36.62, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(5)) color([0.9, 0.8, 0.3]) translate([52.8, 4.12, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(5)) color([0.9, 0.8, 0.3]) translate([42.8, 4.12, 30.0]) sphere(r = 0.35, $fn = 8);
  if (visibile(5)) multmatrix([[0, 1, 0, 38.8], [-1, 0, 0, 39.12], [0, 0, 1, 30.0], [0, 0, 0, 1]]) translate([0, 0, 0.05]) {
    if (nomi_schede) color([0.05, 0.15, 0.45]) translate([18.75, -1.0]) rotate(0) linear_extrude(0.2) text("MT3608", size = 2.00, halign = "center", valign = "top");
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
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([9.420, 4.180, 0]) rotate(90) linear_extrude(0.2) text("PWR_EN", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([11.960, 4.180, 0]) rotate(90) linear_extrude(0.2) text("LED_PWM", size = 0.8, halign = "right", valign = "center");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([14.500, 4.180, 0]) rotate(90) linear_extrude(0.2) text("ADC VBAT_ADC", size = 0.8, halign = "right", valign = "center");
  }
  if (visibile(4)) color([0.2, 0.35, 0.7, 0.35]) multmatrix([[1, 0, 0, 1.1], [0, 1, 0, 17.92], [0, 0, 1, 1.3], [0, 0, 0, 1]]) translate([0, 0, -1.0]) cube([15.0, 10.0, 1.0]);  // Vibrazione
  if (visibile(4)) color([0.9, 0.8, 0.3]) translate([2.37, 19.92, 1.3]) sphere(r = 0.35, $fn = 8);
  if (visibile(4)) color([0.9, 0.8, 0.3]) translate([2.37, 22.46, 1.3]) sphere(r = 0.35, $fn = 8);
  if (visibile(4)) color([0.9, 0.8, 0.3]) translate([2.37, 25.0, 1.3]) sphere(r = 0.35, $fn = 8);
  if (visibile(4)) multmatrix([[1, 0, 0, 1.1], [0, 1, 0, 17.92], [0, 0, 1, 1.3], [0, 0, 0, 1]]) translate([0, 0, 0.05]) {
    if (nomi_schede) color([0.05, 0.15, 0.45]) translate([7.5, -1.0]) rotate(0) linear_extrude(0.2) text("Vibrazione", size = 2.00, halign = "center", valign = "top");
    if (nomi_pin) color([0.6, 0.05, 0.05]) translate([2.170, 7.080, 0]) rotate(0) linear_extrude(0.2) text("IN", size = 0.8, halign = "left", valign = "center");
    if (nomi_pin) color([0.05, 0.25, 0.6]) translate([0.370, 7.080, 0]) rotate(0) linear_extrude(0.2) text("VIB_IN", size = 0.8, halign = "right", valign = "center");
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
  color([0.27, 0.664, 0.9]) seg([2.37, 41.0, -20.0], [5.0, 41.0, -20.0], 0.4);  // cavetto ENC_A -> Encoder EC11 A
  color([0.27, 0.664, 0.9]) seg([5.0, 41.0, -20.0], [5.0, -12.0, -20.0], 0.4);  // cavetto ENC_A -> Encoder EC11 A
  color([0.27, 0.664, 0.9]) seg([5.0, -12.0, -20.0], [42.5, -12.0, -20.0], 0.4);  // cavetto ENC_A -> Encoder EC11 A
  color([0.27, 0.664, 0.9]) seg([42.5, -12.0, -20.0], [42.5, -10.0, -20.0], 0.4);  // cavetto ENC_A -> Encoder EC11 A
  color([0.27, 0.664, 0.9]) seg([42.5, -10.0, -20.0], [42.5, -10.0, -17.0], 0.4);  // cavetto ENC_A -> Encoder EC11 A
  color([0.27, 0.664, 0.9]) translate([2.37, 41.0, -20.0]) sphere(r = 0.7);
  color([0.848, 0.9, 0.27]) seg([-0.17, 41.0, -20.0], [-0.17, -14.0, -20.0], 0.4);  // cavetto ENC_B -> Encoder EC11 B
  color([0.848, 0.9, 0.27]) seg([-0.17, -14.0, -20.0], [47.5, -14.0, -20.0], 0.4);  // cavetto ENC_B -> Encoder EC11 B
  color([0.848, 0.9, 0.27]) seg([47.5, -14.0, -20.0], [47.5, -10.0, -20.0], 0.4);  // cavetto ENC_B -> Encoder EC11 B
  color([0.848, 0.9, 0.27]) seg([47.5, -10.0, -20.0], [47.5, -10.0, -17.0], 0.4);  // cavetto ENC_B -> Encoder EC11 B
  color([0.848, 0.9, 0.27]) translate([-0.17, 41.0, -20.0]) sphere(r = 0.7);
  color([0.9, 0.27, 0.481]) seg([12.53, 41.0, -20.0], [12.53, -17.0, -20.0], 0.4);  // cavetto ENC_SW -> Encoder EC11 SW1
  color([0.9, 0.27, 0.481]) seg([12.53, -17.0, -20.0], [42.5, -17.0, -20.0], 0.4);  // cavetto ENC_SW -> Encoder EC11 SW1
  color([0.9, 0.27, 0.481]) seg([42.5, -17.0, -20.0], [42.5, -19.0, -20.0], 0.4);  // cavetto ENC_SW -> Encoder EC11 SW1
  color([0.9, 0.27, 0.481]) seg([42.5, -19.0, -20.0], [42.5, -19.0, -17.0], 0.4);  // cavetto ENC_SW -> Encoder EC11 SW1
  color([0.9, 0.27, 0.481]) translate([12.53, 41.0, -20.0]) sphere(r = 0.7);
}
