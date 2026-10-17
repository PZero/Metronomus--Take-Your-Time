"""Render di concept di Metronomus (Blender / bpy).

Uso:  python render/concept.py            (con il modulo bpy: pip install bpy)
  o:  blender -b -P render/concept.py
Produce render/concept.png. Misure in mm, convertite in metri.
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
    m = bpy.data.materials.new("legno")
    m.use_nodes = True
    n, l = m.node_tree.nodes, m.node_tree.links
    p = n["Principled BSDF"]
    p.inputs["Roughness"].default_value = 0.55
    coord = n.new("ShaderNodeTexCoord")
    mapping = n.new("ShaderNodeMapping")
    mapping.inputs["Scale"].default_value = (1, 1, 1)
    onde = n.new("ShaderNodeTexWave")
    onde.wave_type = "BANDS"
    onde.bands_direction = "X"
    onde.inputs["Scale"].default_value = 7.0
    onde.inputs["Distortion"].default_value = 4.0
    onde.inputs["Detail"].default_value = 4.0
    onde.inputs["Detail Scale"].default_value = 2.0
    rampa = n.new("ShaderNodeValToRGB")
    rampa.color_ramp.elements[0].color = (0.10, 0.05, 0.025, 1)
    rampa.color_ramp.elements[1].color = (0.24, 0.13, 0.065, 1)
    l.new(coord.outputs["Object"], mapping.inputs["Vector"])
    l.new(mapping.outputs["Vector"], onde.inputs["Vector"])
    l.new(onde.outputs["Fac"], rampa.inputs["Fac"])
    l.new(rampa.outputs["Color"], p.inputs["Base Color"])
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


# ------------------------------------------------------------------ scena
# pavimento e base in legno
scatola((0, 0, -21), (900, 900, 2), PAVIMENTO, "pavimento")
base = scatola((0, 5, -10), (230, 130, 20), LEGNO, "base")
bpy.ops.object.modifier_add(type="BEVEL")
base.modifiers["Bevel"].width = 2 * MM
base.modifiers["Bevel"].segments = 3

PERNO = Vector((0, -6, 78))  # asse del motore

# piedini in rame (4 colonne del telaio GND / VBAT)
for x in (-100, 100):
    for y in (-50, 60):
        pass

# telaio del motore: due colonne + traversi
for x in (-16, 16):
    filo([(x, 10, 0), (x, 10, 92)])
filo([(-16, 10, 92), (16, 10, 92)])
filo([(-16, 10, 62), (16, 10, 62)])
filo([(-16, 10, 30), (16, 10, 30)])

# motore 1503 (asse lungo y, campana verso lo spettatore)
cilindro((0, 6, 78), (0, 0, 78), 9.5, ACCIAIO_SCURO, 48, "statore")
cilindro((0, 0, 78), (0, -9, 78), 9.5, ACCIAIO, 48, "campana")
cilindro((0, -9, 78), (0, -12, 78), 3.0, ACCIAIO, 24, "mozzo")
for x, c in ((-3, (0.9, 0.9, 0.9)), (0, (0.1, 0.2, 0.8)), (3, (0.7, 0.05, 0.05))):
    pass
# AS5600 dietro al motore, scheda verticale
scheda((0, 13, 78), (23, 23, 0), PCB_VIOLA, nome="as5600")
o = bpy.data.objects["as5600"]
o.rotation_euler = (math.radians(90), 0, 0)
scatola((0, 11.6, 78), (5, 1.2, 5), CHIP)

# pendolo: due filamenti in fila, inclinati
asse = Vector((math.sin(ANGOLO_PENDOLO), 0, math.cos(ANGOLO_PENDOLO)))
p0 = PERNO + Vector((0, -13, 0))
cilindro(p0, p0 + Vector((0, 1.5, 0)), 3.5, ACCIAIO, 32, "flangia")
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

# pannello della scala (legno) sorretto da due colonne di rame
PANNELLO_Y = 26
scatola((0, PANNELLO_Y, 160), (170, 5, 70), LEGNO, "pannello")
for x in (-70, 70):
    filo([(x, PANNELLO_Y + 4, 0), (x, PANNELLO_Y + 4, 195)])
    filo([(x, PANNELLO_Y + 4, 195), (x, PANNELLO_Y - 2.5, 195)])
filo([(-70, PANNELLO_Y + 4, 195), (70, PANNELLO_Y + 4, 195)])
# tacche della scala Maelzel (39 valori) incise sul pannello
maelzel = list(range(40, 60, 2)) + list(range(60, 72, 3)) + list(range(72, 120, 4)) + list(range(120, 144, 6)) + list(range(144, 209, 8))
for i, bpm in enumerate(maelzel):
    t = math.radians(-40 + 80 * i / (len(maelzel) - 1))
    lungo = bpm in (40, 60, 72, 96, 120, 144, 176, 208)
    r1, r2 = 92, (104 if lungo else 99)
    a = Vector((PERNO.x + r1 * math.sin(t), PANNELLO_Y - 2.6, PERNO.z + r1 * math.cos(t)))
    b = Vector((PERNO.x + r2 * math.sin(t), PANNELLO_Y - 2.6, PERNO.z + r2 * math.cos(t)))
    tacca = cilindro(a, b, 0.45 if lungo else 0.3, INCISIONE, 6, "tacca")
    if lungo:
        bpy.ops.object.text_add(location=(Vector((PERNO.x + 110 * math.sin(t), PANNELLO_Y - 2.55, PERNO.z + 110 * math.cos(t))) * MM))
        tx = bpy.context.object
        tx.data.body = str(bpm)
        tx.data.size = 6 * MM
        tx.data.align_x = "CENTER"
        tx.data.extrude = 0.1 * MM
        tx.rotation_euler = (math.radians(90), -t, 0)
        tx.data.materials.append(INCISIONE)
for nome, deg in (("Largo", -33), ("Andante", -8), ("Allegro", 14), ("Presto", 33)):
    t = math.radians(deg)
    bpy.ops.object.text_add(location=(Vector((PERNO.x + 84 * math.sin(t), PANNELLO_Y - 2.55, PERNO.z + 84 * math.cos(t))) * MM))
    tx = bpy.context.object
    tx.data.body = nome
    tx.data.size = 4 * MM
    tx.data.align_x = "CENTER"
    tx.data.extrude = 0.1 * MM
    tx.rotation_euler = (math.radians(90), -t, 0)
    tx.data.materials.append(INCISIONE)

# ------------------------------------------------------------------ moduli su "palafitte" di rame
moduli = {
    # nome: (centro, dimensioni, materiale, chip)
    "esp32": ((-55, -30, 26), (18, 23), PCB_NERO, [(0, 3, 9, 9, 1.2), (0, -10, 9, 3, 3)]),
    "driver": ((52, -26, 26), (26, 21), PCB_NERO, [(-2, 0, 14, 6, 1.4), (8, 6, 6, 6, 8)]),
    "tp4056": ((-92, 8, 14), (17, 26), PCB_BLU, [(0, 2, 5, 5, 1.2), (0, 11, 9, 7, 3.2)]),
    "mt3608": ((55, 38, 16), (37, 17), PCB_BLU, [(-6, 0, 8, 8, 4), (10, 0, 7, 9, 7)]),
    "mini360": ((-40, 38, 18), (22, 17), PCB_VERDE, [(4, 0, 8, 8, 3), (-6, 0, 5, 5, 1.2)]),
}
pos = {}
for nome, (c, d, mat, chip) in moduli.items():
    scheda(c, (d[0], d[1], 0), mat, chip, nome)
    pos[nome] = Vector(c)
    # quattro piedini di rame agli angoli: sono anche i collegamenti
    for sx in (-1, 1):
        for sy in (-1, 1):
            a = (c[0] + sx * (d[0] / 2 - 1.5), c[1] + sy * (d[1] / 2 - 1.5), c[2] - 0.8)
            filo([a, (a[0], a[1], 0)])

# encoder EC11 con pomello in rame, a destra davanti
scatola((92, -40, 4), (12, 13, 8), ACCIAIO, "encoder")
cilindro((92, -40, 8), (92, -40, 15), 3.5, ACCIAIO)
cilindro((92, -40, 15), (92, -40, 30), 3.0, ACCIAIO)
pomello = cilindro((92, -40, 18), (92, -40, 31), 8, OTTONE, 48, "pomello")
for k in range(24):
    a = 2 * math.pi * k / 24
    cilindro((92 + 8 * math.cos(a), -40 + 8 * math.sin(a), 19), (92 + 8 * math.cos(a), -40 + 8 * math.sin(a), 30), 0.6, OTTONE, 6)

# batterie 18350 in parallelo (sdraiate) con fascette di rame
for y in (-12, 34):
    cilindro((-112, y, 10), (-77, y, 10), 9, BATTERIA, 48, "18350")
    cilindro((-77, y, 10), (-76, y, 10), 4, ACCIAIO)
    cilindro((-113, y, 10), (-112, y, 10), 7, ACCIAIO)
    for x in (-105, -84):
        filo([(x, y - 9.6, 0), (x, y - 9.6, 10), (x, y - 9.6, 19.6), (x, y + 9.6, 19.6), (x, y + 9.6, 0)])
filo([(-75, -12, 10), (-72, -12, 10), (-72, 34, 10), (-75, 34, 10)])
filo([(-114, -12, 10), (-117, -12, 10), (-117, 34, 10), (-114, 34, 10)])

# ------------------------------------------------------------------ collegamenti ortogonali
def pin(nome, dx, dy):
    c = pos[nome]
    return (c.x + dx, c.y + dy, c.z + 0.8)


reti = [
    # tre fasi + EN dall'ESP32 al driver, quote diverse
    (pin("esp32", 7.5, 8), pin("driver", -11.5, 7), 34),
    (pin("esp32", 7.5, 5.5), pin("driver", -11.5, 4.5), 37),
    (pin("esp32", 7.5, 3), pin("driver", -11.5, 2), 40),
    (pin("esp32", 7.5, 0.5), pin("driver", -11.5, -0.5), 43),
    # fasi motore dal driver al motore
    ((52 - 8, -26 + 9, 26.8), (-4, 8, 72), 50),
    ((52 - 4, -26 + 9, 26.8), (0, 8, 70), 54),
    ((52, -26 + 9, 26.8), (4, 8, 72), 58),
    # I2C verso l'AS5600
    (pin("esp32", -7.5, 8), (-8, 14, 70), 64),
    (pin("esp32", -7.5, 5.5), (-6, 14, 66), 68),
    # alimentazione
    (pin("mini360", 9.5, 6.5), pin("esp32", -7.5, -8), 30),
    (pin("mt3608", -16, 6.5), pin("mini360", 9.5, -6.5), 24),
    (pin("mt3608", 16, 6.5), pin("driver", 11, 8.5), 32),
    (pin("tp4056", 6.5, -11), pin("mt3608", -16, -6.5), 8),
    # encoder
    ((88, -40, 8), pin("esp32", -2, -10), 12),
    ((96, -40, 8), pin("esp32", 2, -10), 15),
    # LED: dal driver di potenza al mozzo
    (pin("driver", 11, -8.5), (6, -10, 70), 46),
]
for a, b, z in reti:
    filo(manhattan(a, b, z))

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


bpy.ops.object.light_add(type="POINT", location=(p2 + Vector((0, -6, 0))) * MM)
bpy.context.object.data.energy = 0.6
bpy.context.object.data.color = (1.0, 0.6, 0.2)
bpy.context.object.data.shadow_soft_size = 0.01
luce_area("chiave", (-260, -260, 380), (0, 0, 60), 9, 260, (1.0, 0.95, 0.9))
luce_area("riempimento", (320, -200, 160), (0, 0, 60), 2.5, 300, (0.8, 0.88, 1.0))
luce_area("controluce", (60, 350, 300), (0, 0, 100), 7, 200, (1.0, 0.85, 0.7))

bpy.ops.object.camera_add(location=Vector((-250, -470, 250)) * MM)
cam = bpy.context.object
cam.data.lens = 50
cam.data.dof.use_dof = True
cam.data.dof.focus_distance = 0.53
cam.data.dof.aperture_fstop = 5.6
cam.data.clip_start = 0.01
mira = Vector((0, 10, 92)) * MM
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
scena.view_settings.exposure = -0.3
scena.render.filepath = str(QUI / "concept.png")
bpy.ops.render.render(write_still=True)
print("Render salvato in", scena.render.filepath)
