// Metronomus: modello 3D di controllo (OpenSCAD)
// Stessa disposizione di render/concept.py, misure in mm, z verso l'alto.
// È ancora indicativa: la geometria definitiva verrà da fili/geometria.yaml.
// Apri il file in OpenSCAD e premi F5; i parametri si cambiano dal Customizer.

/* [Vista] */
teca = true;            // teca di vetro, base più grande, encoder sul bordo
mostra_vetro = true;    // nasconde il vetro per guardare dentro
angolo_pendolo = -14;   // gradi
mostra_scala = true;

$fn = 24;
R_FILO = 0.5;           // filo di rame Ø 1 mm

C_RAME = [0.85, 0.45, 0.25];
C_STAGNO = [0.75, 0.75, 0.72];
C_LEGNO = [0.55, 0.33, 0.17];
C_NERO = [0.1, 0.1, 0.1];
C_BLU = [0.1, 0.25, 0.7];
C_VERDE = [0.05, 0.45, 0.2];
C_VIOLA = [0.5, 0.3, 0.75];
C_ACCIAIO = [0.75, 0.75, 0.78];
C_FILAMENTO = [1.0, 0.75, 0.25];

PERNO = [0, -6, 78];    // asse del motore
PANNELLO_Y = 26;

// ------------------------------------------------------------ primitive
module segmento(a, b, r = R_FILO) {
    v = b - a;
    l = norm(v);
    if (l > 0)
        translate(a)
            rotate([0, acos(v[2] / l), atan2(v[1], v[0])])
                cylinder(r = r, h = l, $fn = 12);
}

// filo di rame a segmenti dritti, con una goccia di stagno a ogni giunto
module filo(punti) {
    color(C_RAME)
        for (i = [0 : len(punti) - 2]) segmento(punti[i], punti[i + 1]);
    color(C_STAGNO)
        for (i = [0 : len(punti) - 1])
            translate(punti[i]) sphere(r = R_FILO * 1.4, $fn = 12);
}

// percorso ortogonale da a a b passando alla quota z
function manhattan(a, b, z) = [a, [a[0], a[1], z], [b[0], a[1], z], [b[0], b[1], z], b];

module scheda(c, d, col, chip = []) {
    color(col) translate(c) cube([d[0], d[1], 1.6], center = true);
    color(C_NERO)
        for (k = chip)
            translate([c[0] + k[0], c[1] + k[1], c[2] + 0.8 + k[4] / 2])
                cube([k[2], k[3], k[4]], center = true);
}

// ------------------------------------------------------------ base
module base() {
    color(C_LEGNO)
        if (teca) translate([0, 5, -11]) cube([270, 170, 22], center = true);
        else translate([0, 5, -10]) cube([230, 130, 20], center = true);
}

// ------------------------------------------------------------ motore, sensore, pendolo
module motore() {
    // telaio: due colonne e tre traversi
    for (x = [-16, 16]) filo([[x, 10, 0], [x, 10, 92]]);
    for (z = [30, 62, 92]) filo([[-16, 10, z], [16, 10, z]]);
    // motore 1503, asse lungo y
    color([0.15, 0.15, 0.16]) segmento([0, 6, 78], [0, 0, 78], 9.5);
    color(C_ACCIAIO) segmento([0, 0, 78], [0, -9, 78], 9.5);
    color(C_ACCIAIO) segmento([0, -9, 78], [0, -12, 78], 3);
    // AS5600 dietro al motore
    color(C_VIOLA) translate([0, 13, 78]) cube([23, 1.6, 23], center = true);
    color(C_NERO) translate([0, 11.6, 78]) cube([5, 1.2, 5], center = true);
}

module pendolo() {
    p0 = PERNO + [0, -13, 0];
    translate(p0) rotate([0, angolo_pendolo, 0]) {
        color(C_ACCIAIO) rotate([-90, 0, 0]) cylinder(r = 3.5, h = 1.5);
        color(C_RAME) cylinder(r = 0.9, h = 6);
        color(C_FILAMENTO) translate([0, 0, 6]) cylinder(r = 1.1, h = 50);
        color(C_STAGNO) translate([0, 0, 56]) cylinder(r = 0.9, h = 2);
        color(C_FILAMENTO) translate([0, 0, 58]) cylinder(r = 1.1, h = 50);
        color(C_RAME) translate([2.2, 0, 0]) cylinder(r = 0.18, h = 109, $fn = 8);
    }
}

// ------------------------------------------------------------ scala Maelzel
MAELZEL = concat([for (b = [40 : 2 : 58]) b], [for (b = [60 : 3 : 69]) b],
                 [for (b = [72 : 4 : 116]) b], [for (b = [120 : 6 : 138]) b],
                 [for (b = [144 : 8 : 208]) b]);
LUNGHI = [40, 60, 72, 96, 120, 144, 176, 208];

module scala() {
    color(C_LEGNO) translate([0, PANNELLO_Y, 160]) cube([170, 5, 70], center = true);
    for (x = [-70, 70]) {
        filo([[x, PANNELLO_Y + 4, 0], [x, PANNELLO_Y + 4, 195]]);
        filo([[x, PANNELLO_Y + 4, 195], [x, PANNELLO_Y - 2.5, 195]]);
    }
    filo([[-70, PANNELLO_Y + 4, 195], [70, PANNELLO_Y + 4, 195]]);
    if (mostra_scala) {
        n = len(MAELZEL);
        for (i = [0 : n - 1]) {
            t = -40 + 80 * i / (n - 1);
            lungo = len(search(MAELZEL[i], LUNGHI)) > 0;
            r2 = lungo ? 104 : 99;
            color("white")
                segmento([PERNO[0] + 92 * sin(t), PANNELLO_Y - 2.6, PERNO[2] + 92 * cos(t)],
                         [PERNO[0] + r2 * sin(t), PANNELLO_Y - 2.6, PERNO[2] + r2 * cos(t)],
                         lungo ? 0.45 : 0.3);
            if (lungo)
                color("white")
                    translate([PERNO[0] + 110 * sin(t), PANNELLO_Y - 2.6, PERNO[2] + 110 * cos(t)])
                        rotate([90, 0, 0]) rotate([0, 0, -t])
                            linear_extrude(0.2) text(str(MAELZEL[i]), size = 6, halign = "center", valign = "center");
        }
    }
}

// ------------------------------------------------------------ moduli su piedini di rame
// nome, centro, dimensioni, colore, chip [dx, dy, larghezza, profondità, altezza]
MODULI = [
    ["esp32",   [-55, -30, 26], [18, 23], C_NERO,  [[0, 3, 9, 9, 1.2], [0, -10, 9, 3, 3]]],
    ["driver",  [52, -26, 26],  [26, 21], C_NERO,  [[-2, 0, 14, 6, 1.4], [8, 6, 6, 6, 8]]],
    ["tp4056",  [-92, 8, 14],   [17, 26], C_BLU,   [[0, 2, 5, 5, 1.2], [0, 11, 9, 7, 3.2]]],
    ["mt3608",  [55, 38, 16],   [37, 17], C_BLU,   [[-6, 0, 8, 8, 4], [10, 0, 7, 9, 7]]],
    ["mini360", [-40, 38, 18],  [22, 17], C_VERDE, [[4, 0, 8, 8, 3], [-6, 0, 5, 5, 1.2]]],
];

function centro(nome) = MODULI[search([nome], MODULI)[0]][1];
function pin(nome, dx, dy) = let(c = centro(nome)) [c[0] + dx, c[1] + dy, c[2] + 0.8];

module moduli() {
    for (m = MODULI) {
        c = m[1]; d = m[2];
        scheda(c, d, m[3], m[4]);
        for (sx = [-1, 1], sy = [-1, 1]) {
            a = [c[0] + sx * (d[0] / 2 - 1.5), c[1] + sy * (d[1] / 2 - 1.5), c[2] - 0.8];
            filo([a, [a[0], a[1], 0]]);
        }
    }
}

// ------------------------------------------------------------ encoder
FRONTE = 5 - 85;
ENCODER_A = teca ? [88, -50, 0] : [88, -40, 8];
ENCODER_B = teca ? [96, -50, 0] : [96, -40, 8];

module encoder() {
    if (teca) {
        // sul bordo anteriore: corpo incassato, asse orizzontale, pomello fuori dalla teca
        color(C_ACCIAIO) segmento([92, FRONTE, -11], [92, FRONTE - 9, -11], 3);
        color([0.8, 0.5, 0.3]) segmento([92, FRONTE - 3, -11], [92, FRONTE - 16, -11], 8);
        color(C_NERO) translate([-92, 5 + 85, -11]) cube([9.5, 1.5, 3.6], center = true); // USB-C
    } else {
        color(C_ACCIAIO) translate([92, -40, 4]) cube([12, 13, 8], center = true);
        color(C_ACCIAIO) segmento([92, -40, 8], [92, -40, 30], 3);
        color([0.8, 0.5, 0.3]) segmento([92, -40, 18], [92, -40, 31], 8);
    }
}

// ------------------------------------------------------------ batterie 18350 in parallelo
module batterie() {
    for (y = [-12, 34]) {
        color([0.25, 0.55, 0.95]) segmento([-112, y, 10], [-77, y, 10], 9);
        color(C_ACCIAIO) segmento([-77, y, 10], [-76, y, 10], 4);
        color(C_ACCIAIO) segmento([-113, y, 10], [-112, y, 10], 7);
        for (x = [-105, -84])
            filo([[x, y - 9.6, 0], [x, y - 9.6, 10], [x, y - 9.6, 19.6], [x, y + 9.6, 19.6], [x, y + 9.6, 0]]);
    }
    filo([[-75, -12, 10], [-72, -12, 10], [-72, 34, 10], [-75, 34, 10]]);
    filo([[-114, -12, 10], [-117, -12, 10], [-117, 34, 10], [-114, 34, 10]]);
}

// ------------------------------------------------------------ collegamenti
// [inizio, fine, quota del tratto orizzontale]
RETI = [
    [pin("esp32", 7.5, 8),   pin("driver", -11.5, 7),    34],  // PWM A
    [pin("esp32", 7.5, 5.5), pin("driver", -11.5, 4.5),  37],  // PWM B
    [pin("esp32", 7.5, 3),   pin("driver", -11.5, 2),    40],  // PWM C
    [pin("esp32", 7.5, 0.5), pin("driver", -11.5, -0.5), 43],
    [[44, -17, 26.8], [-4, 8, 72], 50],                        // fasi del motore
    [[48, -17, 26.8], [0, 8, 70], 54],
    [[52, -17, 26.8], [4, 8, 72], 58],
    [pin("esp32", -7.5, 8),   [-8, 14, 70], 64],               // I2C AS5600
    [pin("esp32", -7.5, 5.5), [-6, 14, 66], 68],
    [pin("mini360", 9.5, 6.5), pin("esp32", -7.5, -8), 30],    // alimentazione
    [pin("mt3608", -16, 6.5),  pin("mini360", 9.5, -6.5), 24],
    [pin("mt3608", 16, 6.5),   pin("driver", 11, 8.5), 32],
    [pin("tp4056", 6.5, -11),  pin("mt3608", -16, -6.5), 8],
    [ENCODER_A, pin("esp32", -2, -10), 12],                    // encoder
    [ENCODER_B, pin("esp32", 2, -10), 15],
    [pin("driver", 11, -8.5), [6, -10, 70], 46],               // LED
];

module reti() {
    for (r = RETI) filo(manhattan(r[0], r[1], r[2]));
}

// ------------------------------------------------------------ teca
module vetro() {
    LX = 240; LY = 140; H = 225; S = 3; CY = 5;
    color([0.8, 0.95, 1.0, 0.18]) {
        translate([0, CY - LY / 2 - S / 2, H / 2]) cube([LX + 2 * S, S, H], center = true);
        translate([0, CY + LY / 2 + S / 2, H / 2]) cube([LX + 2 * S, S, H], center = true);
        translate([-LX / 2 - S / 2, CY, H / 2]) cube([S, LY, H], center = true);
        translate([LX / 2 + S / 2, CY, H / 2]) cube([S, LY, H], center = true);
        translate([0, CY, H + S / 2]) cube([LX + 2 * S, LY + 2 * S, S], center = true);
    }
}

// ------------------------------------------------------------ assieme
base();
motore();
pendolo();
scala();
moduli();
encoder();
batterie();
reti();
if (teca && mostra_vetro) vetro();   // per ultimo: la trasparenza funziona meglio
