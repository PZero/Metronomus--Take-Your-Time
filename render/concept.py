"""Render di concept di Metronomus (Blender / bpy).

Uso:  python render/concept.py [teca] [campioni]   (con il modulo bpy: pip install bpy)
  o:  blender -b -P render/concept.py -- [teca] [campioni]
Produce render/concept.png, oppure render/concept-teca.png con la teca di vetro,
l'encoder sul bordo anteriore della base e la USB‑C sul retro. Misure in mm, convertite in metri.
È un'immagine indicativa: la disposizione reale verrà da fili/geometria.yaml.
"""
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

QUI = Path(__file__).resolve().parent
MM = 0.001
CAMPIONI = int(sys.argv[-1]) if sys.argv[-1].isdigit() else 96
TECA = "teca" in sys.argv
VICINO = "vicino" in sys.argv   # primo piano dei collegamenti, senza teca
ANGOLO_PENDOLO = math.radians(-14)

bpy.ops.wm.read_factory_settings(use_empty=True)
scena = bpy.context.scene


# ------------------------------------------------------------------ materiali
def materiale(nome, colore, metallo=0.0, ruvidita=0.5, emissione=None, forza=0.0):
    m = bpy.data.materials.new(nome)
    m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*colore, 1)
    p.inputs["Metallic"].default_value = metallo
    p.inputs["Roughness"].default_value = ruvidita
    if emissione:
        p.inputs["Emission Color"].default_value = (*emissione, 1)
        p.inputs["Emission Strength"].default_value = forza
    return m


def legno():
    """Noce: venature lunghe lungo x (rumore stirato) più fibre fini."""
    m = bpy.data.materials.new("legno")
    m.use_nodes = True
    n, l = m.node_tree.nodes, m.node_tree.links
    p = n["Principled BSDF"]
    p.inputs["Roughness"].default_value = 0.5
    coord = n.new("ShaderNodeTexCoord")
    mapping = n.new("ShaderNodeMapping")
    mapping.inputs["Scale"].default_value = (0.6, 14, 14)
    venature = n.new("ShaderNodeTexNoise")
    venature.inputs["Scale"].default_value = 3.0
    venature.inputs["Detail"].default_value = 6.0
    venature.inputs["Roughness"].default_value = 0.55
    venature.inputs["Distortion"].default_value = 0.6
    fibre = n.new("ShaderNodeTexWave")
    fibre.wave_type = "BANDS"
    fibre.bands_direction = "Y"
    fibre.wave_profile = "SAW"
    fibre.inputs["Scale"].default_value = 6.0
    fibre.inputs["Distortion"].default_value = 6.0
    fibre.inputs["Detail"].default_value = 3.0
    rampa = n.new("ShaderNodeValToRGB")
    rampa.color_ramp.elements[0].position = 0.3
    rampa.color_ramp.elements[0].color = (0.085, 0.042, 0.02, 1)
    rampa.color_ramp.elements[1].position = 0.7
    rampa.color_ramp.elements[1].color = (0.20, 0.105, 0.05, 1)
    mix = n.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.blend_type = "MULTIPLY"
    mix.inputs["Factor"].default_value = 0.25
    l.new(coord.outputs["Object"], mapping.inputs["Vector"])
    l.new(mapping.outputs["Vector"], venature.inputs["Vector"])
    l.new(mapping.outputs["Vector"], fibre.inputs["Vector"])
    l.new(venature.outputs["Fac"], rampa.inputs["Fac"])
    l.new(rampa.outputs["Color"], mix.inputs["A"])
    l.new(fibre.outputs["Color"], mix.inputs["B"])
    l.new(mix.outputs["Result"], p.inputs["Base Color"])
    return m


def vetro():
    m = bpy.data.materials.new("vetro")
    m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (0.95, 1.0, 0.98, 1)
    p.inputs["Roughness"].default_value = 0.0
    p.inputs["IOR"].default_value = 1.5
    p.inputs["Transmission Weight"].default_value = 1.0
    return m


RAME = materiale("rame", (0.93, 0.52, 0.33), 1.0, 0.22)
STAGNO = materiale("stagno", (0.75, 0.75, 0.72), 1.0, 0.35)
LEGNO = legno()
PCB_NERO = materiale("pcb_nero", (0.02, 0.02, 0.02), 0.0, 0.35)
PCB_BLU = materiale("pcb_blu", (0.02, 0.10, 0.35), 0.0, 0.35)
PCB_VERDE = materiale("pcb_verde", (0.01, 0.22, 0.08), 0.0, 0.35)
PCB_VIOLA = materiale("pcb_viola", (0.22, 0.10, 0.40), 0.0, 0.35)
CHIP = materiale("chip", (0.015, 0.015, 0.015), 0.0, 0.45)
ACCIAIO = materiale("acciaio", (0.8, 0.8, 0.82), 1.0, 0.18)
ACCIAIO_SCURO = materiale("acciaio_scuro", (0.12, 0.12, 0.13), 1.0, 0.3)
BATTERIA = materiale("batteria", (0.05, 0.25, 0.65), 0.0, 0.25)
FILAMENTO = materiale("filamento", (1.0, 0.75, 0.25), 0.0, 0.4, (1.0, 0.5, 0.1), 22.0)
INCISIONE = materiale("incisione", (0.85, 0.75, 0.6), 0.0, 0.7)
PAVIMENTO = materiale("pavimento", (0.035, 0.035, 0.04), 0.0, 0.6)
OTTONE = materiale("pomello", (0.85, 0.5, 0.3), 1.0, 0.35)
VETRO = vetro()


# ------------------------------------------------------------------ primitive (mm)
def scatola(c, d, mat, nome="scatola", rot=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=Vector(c) * MM)
    o = bpy.context.object
    o.name = nome
    o.scale = Vector(d) * MM
    if rot:
        o.rotation_euler = rot
    o.data.materials.append(mat)
    return o


def cilindro(p1, p2, r, mat, vertici=24, nome="cilindro"):
    p1, p2 = Vector(p1), Vector(p2)
    v = p2 - p1
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertici, radius=r * MM, depth=v.length * MM,
                                        location=(p1 + v / 2) * MM)
    o = bpy.context.object
    o.name = nome
    o.rotation_euler = v.to_track_quat("Z", "Y").to_euler()
    o.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    return o


def sfera(c, r, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=r * MM, location=Vector(c) * MM)
    o = bpy.context.object
    o.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    return o


def filo(punti, r=0.5):
    """Filo di rame Ø 1 mm a segmenti dritti con giunto stagnato a ogni angolo."""
    for a, b in zip(punti, punti[1:]):
        cilindro(a, b, r, RAME, 12, "rame")
    for p in punti[1:-1]:
        sfera(p, r * 1.35, STAGNO)
    for p in (punti[0], punti[-1]):
        sfera(p, r * 1.5, STAGNO)


def manhattan(a, b, z):
    """Percorso ortogonale da a a b passando alla quota z."""
    return [a, (a[0], a[1], z), (b[0], a[1], z), (b[0], b[1], z), b]


def scheda(c, d, mat, chip=(), nome="scheda"):
    s = scatola(c, (d[0], d[1], 1.6), mat, nome)
    for (dx, dy, w, h, t) in chip:
        scatola((c[0] + dx, c[1] + dy, c[2] + 0.8 + t / 2), (w, h, t), CHIP)
    return s


# ------------------------------------------------------------------ geometria (fili/geometria.py)
sys.path.insert(0, str(QUI.parent / "fili"))
_argv = sys.argv
sys.argv = [sys.argv[0]]
import geometria as G  # noqa: E402
sys.argv = _argv
PEZZI, _errori, _avvisi = G.analizza()
from mathutils import Matrix  # noqa: E402


def scheda_orientata(m, mat):
    """Scheda di un modulo con i suoi assi u, v, n e un blocco scuro per i componenti."""
    u, v, n = Vector(m.u), Vector(m.v), Vector(m.n)
    w, h = m.dimensioni
    o = Vector(m.origine)
    for (dx, dy, dz, sx, sy, sz, materiale_) in ((w / 2, h / 2, -m.spessore / 2, w, h, m.spessore, mat),
                                                 (w / 2, h / 2, m.altezza / 2, w * 0.45, h * 0.4, m.altezza, CHIP)):
        c = o + u * dx + v * dy + n * dz
        bpy.ops.mesh.primitive_cube_add(size=1)
        ob = bpy.context.object
        ob.name = m.nome
        k = MM
        ob.matrix_world = Matrix(((u.x * sx * k, v.x * sy * k, n.x * sz * k, c.x * k),
                                  (u.y * sx * k, v.y * sy * k, n.y * sz * k, c.y * k),
                                  (u.z * sx * k, v.z * sy * k, n.z * sz * k, c.z * k), (0, 0, 0, 1)))
        ob.data.materials.append(materiale_)


MAT_SCHEDA = {"nero": PCB_NERO, "blu": PCB_BLU, "verde": PCB_VERDE, "bianco": materiale("pcb_bianco", (0.85, 0.85, 0.82), 0.0, 0.4),
              "millefori": materiale("millefori", (0.55, 0.38, 0.15), 0.0, 0.45)}

# base in legno (dimensioni da geometria)
scatola((0, 0, lo_z - 1), (1200, 1200, 2), PAVIMENTO, "pavimento") if (lo_z := G.BASE["min"][2]) else None
lo, hi = G.BASE["min"], G.BASE["max"]
base = scatola(tuple((lo[i] + hi[i]) / 2 for i in range(3)), tuple(hi[i] - lo[i] for i in range(3)), LEGNO, "base")
bpy.ops.object.modifier_add(type="BEVEL")
base.modifiers["Bevel"].width = 2 * MM
base.modifiers["Bevel"].segments = 3

# moduli
for m in G.MODULI.values():
    scheda_orientata(m, MAT_SCHEDA[m.colore])

# fili di rame: un cilindro per pezzo, una goccia di stagno per giunto
for p in PEZZI:
    cilindro(p.a, p.b, G.R_FILO, RAME, 12, p.codice)
for g in {pt for p in PEZZI for pt in (p.a, p.b)}:
    if g[2] > 0.1:
        sfera(g, G.R_FILO * 1.35, STAGNO)

# motore 1503 (asse lungo y, campana verso lo spettatore)
ax, ay, az = G.MOTORE["asse"]
rm, lm = G.MOTORE["diametro"] / 2, G.MOTORE["lunghezza"]
scatola((ax, ay + 0.5, az), (25, 1, 25), OTTONE, "piastra motore")
cilindro((ax, ay, az), (ax, ay - 4, az), rm, ACCIAIO_SCURO, 48, "statore")
cilindro((ax, ay - 4, az), (ax, ay - lm, az), rm, ACCIAIO, 48, "campana")
cilindro((ax, ay - lm, az), (ax, ay - lm - 4, az), 3.0, ACCIAIO, 24, "mozzo")
PERNO = Vector((ax, ay - lm - 4, az))

# pendolo: due filamenti in serie, inclinati
asse = Vector((math.sin(ANGOLO_PENDOLO), 0, math.cos(ANGOLO_PENDOLO)))
p0 = PERNO + Vector((0, -1.5, 0))
cilindro(PERNO, p0, 3.5, ACCIAIO, 32, "flangia")
p1 = p0 + asse * 6
p2 = p1 + asse * 50
p3 = p2 + asse * 2
p4 = p3 + asse * 50
cilindro(p0, p1, 0.9, RAME)
cilindro(p1, p2, 1.1, FILAMENTO, 24, "filamento1")
cilindro(p2, p3, 0.9, STAGNO)
cilindro(p3, p4, 1.1, FILAMENTO, 24, "filamento2")
sfera(p4, 1.1, STAGNO)
laterale = Vector((math.cos(ANGOLO_PENDOLO), 0, -math.sin(ANGOLO_PENDOLO))) * 2.2
cilindro(p0 + laterale, p4 + laterale + asse * 1, 0.18, RAME, 8, "ritorno")
cilindro(p4, p4 + laterale + asse * 1, 0.18, RAME, 8, "ritorno")

# pannello della scala
c, d = G.PANNELLO["centro"], G.PANNELLO["dimensioni"]
scatola(c, d, LEGNO, "pannello")
PANNELLO_Y = c[1] + d[1] / 2
FRONTE_PANNELLO = c[1] - d[1] / 2 - 0.1
maelzel = list(range(40, 60, 2)) + list(range(60, 72, 3)) + list(range(72, 120, 4)) + list(range(120, 144, 6)) + list(range(144, 209, 8))
for i, bpm in enumerate(maelzel):
    t = math.radians(-40 + 80 * i / (len(maelzel) - 1))
    lungo = bpm in (40, 60, 72, 96, 120, 144, 176, 208)
    r1, r2 = 92, (104 if lungo else 99)
    a_ = Vector((PERNO.x + r1 * math.sin(t), FRONTE_PANNELLO, PERNO.z + r1 * math.cos(t)))
    b_ = Vector((PERNO.x + r2 * math.sin(t), FRONTE_PANNELLO, PERNO.z + r2 * math.cos(t)))
    cilindro(a_, b_, 0.45 if lungo else 0.3, INCISIONE, 6, "tacca")
    if lungo:
        bpy.ops.object.text_add(location=(Vector((PERNO.x + 110 * math.sin(t), FRONTE_PANNELLO, PERNO.z + 110 * math.cos(t))) * MM))
        tx = bpy.context.object
        tx.data.body = str(bpm)
        tx.data.size = 6 * MM
        tx.data.align_x = "CENTER"
        tx.data.extrude = 0.1 * MM
        tx.rotation_euler = (math.radians(90), -t, 0)
        tx.data.materials.append(INCISIONE)
for nome, deg in (("Largo", -33), ("Andante", -8), ("Allegro", 14), ("Presto", 33)):
    t = math.radians(deg)
    bpy.ops.object.text_add(location=(Vector((PERNO.x + 84 * math.sin(t), FRONTE_PANNELLO, PERNO.z + 84 * math.cos(t))) * MM))
    tx = bpy.context.object
    tx.data.body = nome
    tx.data.size = 4 * MM
    tx.data.align_x = "CENTER"
    tx.data.extrude = 0.1 * MM
    tx.rotation_euler = (math.radians(90), -t, 0)
    tx.data.materials.append(INCISIONE)

# batterie 18350
for bt in G.BATTERIE:
    cx, cy, cz = bt["centro"]
    l2 = bt["lunghezza"] / 2
    cilindro((cx, cy - l2, cz), (cx, cy + l2, cz), bt["diametro"] / 2, BATTERIA, 48, "18350")
    cilindro((cx, cy - l2 - 1, cz), (cx, cy - l2, cz), 4, ACCIAIO)

# encoder sul bordo anteriore, prolunga USB-C sul retro
FRONTE = lo[1]
XE, ZE = 60.0, (lo[2] + hi[2]) / 2
cilindro((XE, FRONTE, ZE), (XE, FRONTE - 6, ZE), 4.5, ACCIAIO, 32)
cilindro((XE, FRONTE - 3, ZE), (XE, FRONTE - 16, ZE), 8, OTTONE, 48, "pomello")
for k in range(24):
    a = 2 * math.pi * k / 24
    cilindro((XE + 8 * math.cos(a), FRONTE - 4, ZE + 8 * math.sin(a)),
             (XE + 8 * math.cos(a), FRONTE - 15, ZE + 8 * math.sin(a)), 0.6, OTTONE, 6)
scatola((-60, hi[1], ZE), (9.5, 1.5, 3.6), CHIP, "usb_c")

# teca di vetro appoggiata nella scanalatura della base
if TECA:
    S, M_ = 3, 5
    LX, LY, H = hi[0] - lo[0] - 2 * M_ - 2 * S, hi[1] - lo[1] - 2 * M_ - 2 * S, 225
    CX, CY = (lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2
    lastre = [
        ((CX, CY - LY / 2 - S / 2, H / 2), (LX + 2 * S, S, H)),
        ((CX, CY + LY / 2 + S / 2, H / 2), (LX + 2 * S, S, H)),
        ((CX - LX / 2 - S / 2, CY, H / 2), (S, LY, H)),
        ((CX + LX / 2 + S / 2, CY, H / 2), (S, LY, H)),
        ((CX, CY, H + S / 2), (LX + 2 * S, LY + 2 * S, S)),
    ]
    for c_, d_ in lastre:
        o = scatola(c_, d_, VETRO, "vetro")
        o.visible_shadow = False
    for c_, d_ in lastre[:4]:
        scatola((c_[0], c_[1], 0.15), (d_[0] + 1, d_[1] + 1, 0.4), CHIP, "scanalatura")

# ------------------------------------------------------------------ luci e camera
mondo = bpy.data.worlds.new("mondo")
scena.world = mondo
mondo.use_nodes = True
mondo.node_tree.nodes["Background"].inputs["Color"].default_value = (0.012, 0.012, 0.015, 1)


def luce_area(nome, loc, mira, forza, dim, colore=(1, 1, 1)):
    bpy.ops.object.light_add(type="AREA", location=Vector(loc) * MM)
    l = bpy.context.object
    l.name = nome
    l.data.energy = forza
    l.data.size = dim * MM
    l.data.color = colore
    l.rotation_euler = (Vector(mira) * MM - l.location).to_track_quat("-Z", "Y").to_euler()
    l.visible_camera = False
    l.visible_glossy = not TECA  # niente rettangoli bianchi riflessi nel vetro
    l.visible_transmission = not TECA


bpy.ops.object.light_add(type="POINT", location=(p2 + Vector((0, -6, 0))) * MM)
bpy.context.object.data.energy = 0.6
bpy.context.object.data.color = (1.0, 0.6, 0.2)
bpy.context.object.data.shadow_soft_size = 0.01
bpy.context.object.visible_camera = False
bpy.context.object.visible_transmission = False
luce_area("chiave", (-260, -260, 380), (0, 0, 60), 9, 260, (1.0, 0.95, 0.9))
luce_area("riempimento", (320, -200, 160), (0, 0, 60), 2.5, 300, (0.8, 0.88, 1.0))
luce_area("controluce", (60, 350, 300), (0, 0, 100), 7, 200, (1.0, 0.85, 0.7))

bpy.ops.object.camera_add(location=Vector((-120, -175, 120) if VICINO else (-230, -440, 230) if TECA else (-200, -380, 210)) * MM)
cam = bpy.context.object
cam.data.lens = 50
cam.data.dof.use_dof = True
cam.data.dof.focus_distance = 0.21 if VICINO else 0.52 if TECA else 0.45
cam.data.dof.aperture_fstop = 11 if VICINO else 5.6
cam.data.clip_start = 0.01
mira = Vector((6, 18, 38) if VICINO else (0, 15, 90)) * MM
cam.rotation_euler = (mira - cam.location).to_track_quat("-Z", "Y").to_euler()
scena.camera = cam

scena.render.engine = "CYCLES"
scena.cycles.device = "CPU"
scena.cycles.samples = CAMPIONI
scena.cycles.use_denoising = True
scena.render.resolution_x = 1600
scena.render.resolution_y = 1200
scena.view_settings.view_transform = "AgX"
scena.view_settings.look = "AgX - Medium High Contrast"
scena.view_settings.exposure = -0.9 if TECA else -0.3
scena.cycles.max_bounces = 16
scena.cycles.transmission_bounces = 16
scena.render.filepath = str(QUI / ("concept-vicino.png" if VICINO else "concept-teca.png" if TECA else "concept.png"))
bpy.ops.render.render(write_still=True)
print("Render salvato in", scena.render.filepath)
