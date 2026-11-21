# Rig a Tripo model that the owner SPLIT INTO PARTS in the Tripo app (Segment -> export GLB: one mesh + its own texture per part).
# Knowing the parts makes the rig clean where tripo_rig.py had to guess from texture islands: every part only listens to the bones it
# belongs to (the skirt never follows an arm, the bow is rigid in the left hand), and a bow / string is its own mesh the game can hide or swap.
# Steps: drop crumbs, x10, join seam-split vertices, close the holes where Tripo cut the parts (like Tripo's "Quick Cap", free), decimate a
# part when it has a budget, weights per part (heat weights on a voxel proxy limited to the part's bones, rigid, or AUTO = rigid on the bone
# nearest to the part: chain links, spikes, gems), one texture atlas for every part (base colour + normal + metal/roughness when the export
# has them), export: meshes "body" (+ "bow", "string") + an armature with the KayKit Rig_Medium names at the model's joints (the game
# re-binds them onto a KayKit skeleton: grind3d.html / tribe3d.html rigTripo, so every KayKit move plays).
#   pip install bpy
#   python3 tools/blender/tripo_parts_rig.py art/incoming/tribe3d/tripo/warrior_split_raw.glb art/grind3d/huntress.glb huntress
#   python3 tools/blender/tripo_parts_rig.py art/incoming/grind3d/knight/knight_raw.glb art/tribe3d/people/demon_knight.glb knight
#   python3 tools/blender/tripo_parts_rig.py art/incoming/winged/raw.glb art/tribe3d/people/winged_knight.glb winged
#   python3 tools/blender/tripo_parts_rig.py art/incoming/grind3d/darkknight/tripo_split_raw.glb art/grind3d/dark_knight.glb dark
#   python3 tools/blender/tripo_parts_rig.py art/incoming/grind3d/hoodknight/tripo_split_raw.glb art/grind3d/hood_knight.glb hood
#   python3 tools/blender/tripo_parts_rig.py art/incoming/tribe3d/tripo/warrior_split_raw.glb art/grind3d/outfit_archer.glb base_archer_outfit
#   python3 tools/blender/tripo_parts_rig.py art/incoming/basebody/tripo_base_v1_tex.glb art/grind3d/base_girl.glb base   (tripo_base_v1.glb = the same split without texture: flat COLORS)
# A new model: plot its parts first (front / side point plot, a grid render for the joints), then add an entry to MODELS.
import bpy, bmesh, sys, json, math
import numpy as np
from mathutils import Vector
SRC, OUT = sys.argv[1], sys.argv[2]
MODEL = sys.argv[3] if len(sys.argv) > 3 else 'huntress'
SC, VOXEL = 10, .06
# Roles: 'headblend' (head, blending to chest down the braids), 'heat:<bones>', 'rigid:<bone>', 'mix:<bone>=<w>,<bone>=<w>' (rigid, shared),
# 'bow' / 'string' (rigid on the left hand, own meshes), 'auto' (rigid on the nearest bone), 'drop'. Parts missing from ROLE take DEFAULT.
MODELS_BASE_J = {'hips': (0, .41, .05), 'spine': (0, .47, .055), 'chest': (0, .55, .055), 'head': (0, .615, .045), 'top': (0, .91, .04),
       'upperarml': (.065, .605, .035), 'lowerarml': (.14, .49, .042), 'wristl': (.195, .395, .05), 'handl': (.2, .385, .05), 'handslotl': (.222, .358, .05),
       'upperarmr': (-.065, .605, .035), 'lowerarmr': (-.14, .49, .042), 'wristr': (-.195, .395, .05), 'handr': (-.2, .385, .05), 'handslotr': (-.222, .358, .05),
       'upperlegl': (.055, .4, .055), 'lowerlegl': (.076, .21, .05), 'footl': (.095, .065, .045), 'toesl': (.105, .01, .13),
       'upperlegr': (-.055, .4, .055), 'lowerlegr': (-.076, .21, .05), 'footr': (-.095, .065, .045), 'toesr': (-.105, .01, .13)}   # the base body (2026-11-21)
MODELS = {
  # the "tribal female warrior" split on 2026-11-17 (game coords: y up, she looks at +z, her left hand +x, 0.97 tall)
  'huntress': dict(
    ROLE={0: 'headblend', 1: 'heat:hips,spine,chest,upperlegl,upperlegr', 2: 'bow', 3: 'heat:hips,upperlegl,lowerlegl,footl,upperlegr,lowerlegr,footr',
          4: 'heat:chest,upperarmr,lowerarmr,handr', 5: 'rigid:footl', 6: 'heat:hips,spine,chest', 7: 'string', 8: 'heat:chest,upperarml,lowerarml,handl', 9: 'rigid:footr'},
    DEFAULT='drop',   # her other 30 parts are crumbs of 1-70 faces, a few millimetres each
    FACES={0: 17000, 1: 12000, 2: 4000, 3: 5000, 4: 2400, 5: 1200, 6: 2000, 7: 600, 8: 2300, 9: 1200},   # ~48k
    SHOULDER=[1],   # parts whose shoulder area follows the upper arm a little (no gap when she raises the bow)
    J={'hips': (-.035, .37, .045), 'spine': (-.03, .44, .05), 'chest': (-.025, .52, .05), 'head': (-.025, .6, .04), 'top': (-.025, .86, .03),
       'upperarml': (.06, .575, .04), 'lowerarml': (.095, .48, .045), 'wristl': (.145, .425, .05), 'handl': (.165, .418, .05), 'handslotl': (.195, .41, .05),
       'upperarmr': (-.11, .575, .04), 'lowerarmr': (-.16, .495, .045), 'wristr': (-.19, .39, .05), 'handr': (-.195, .38, .05), 'handslotr': (-.2, .36, .05),
       'upperlegl': (.015, .37, .045), 'lowerlegl': (.02, .2, .045), 'footl': (.022, .065, .03), 'toesl': (.022, .02, .1),
       'upperlegr': (-.085, .37, .045), 'lowerlegr': (-.12, .2, .045), 'footr': (-.14, .065, .03), 'toesr': (-.14, .02, .1)}),
  # the "demon knight" (GPT design -> Tripo image to 3D, quad 25k, Segment custom: 147 parts, 2026-11-17); 1.0 tall, right fist empty for a sword
  'knight': dict(
    ROLE={3: 'rigid:head', 0: 'heat:hips,spine,chest,upperlegl,upperlegr', 4: 'heat:hips,spine,chest',
          13: 'heat:chest,upperarmr,lowerarmr', 27: 'rigid:upperarml', 20: 'rigid:lowerarml', 1: 'rigid:handr', 2: 'rigid:handl',
          6: 'mix:upperarmr=.6,chest=.4', 7: 'mix:upperarml=.6,chest=.4',
          11: 'rigid:upperlegr', 12: 'rigid:upperlegl', 10: 'rigid:lowerlegr', 21: 'rigid:lowerlegl', 9: 'rigid:footr', 8: 'rigid:footl'},
    DEFAULT='auto', FACES={}, SHOULDER=[0],
    J={'hips': (0, .42, .035), 'spine': (0, .5, .035), 'chest': (0, .575, .03), 'head': (0, .64, .03), 'top': (0, .98, .03),
       'upperarml': (.11, .6, .035), 'lowerarml': (.205, .545, .045), 'wristl': (.275, .48, .05), 'handl': (.29, .465, .05), 'handslotl': (.31, .44, .055),
       'upperarmr': (-.11, .6, .035), 'lowerarmr': (-.205, .545, .045), 'wristr': (-.275, .48, .05), 'handr': (-.29, .465, .05), 'handslotr': (-.31, .445, .06),
       'upperlegl': (.055, .42, .035), 'lowerlegl': (.095, .27, .04), 'footl': (.13, .085, .04), 'toesl': (.13, .02, .13),
       'upperlegr': (-.055, .42, .035), 'lowerlegr': (-.1, .27, .04), 'footr': (-.14, .085, .04), 'toesr': (-.14, .02, .13)}),
  # the "dark knight" (owner's GPT T-pose front -> Tripo, textured, segment by prompt: 43 parts, 2026-11-18): 1.0 tall, T-pose, open hands, faces +z
  'dark': dict(
    ROLE={3: 'rigid:head', 1: 'rigid:head', 11: 'rigid:chest', 6: 'heat:spine,chest', 5: 'heat:hips,spine,chest',
          15: 'heat:hips,upperlegl,upperlegr', 23: 'rigid:hips', 20: 'mix:hips=.7,upperlegl=.15,upperlegr=.15',
          12: 'mix:hips=.45,upperlegl=.55', 4: 'mix:hips=.45,upperlegr=.55',
          7: 'heat:upperlegl,lowerlegl,footl', 8: 'heat:upperlegr,lowerlegr,footr', 9: 'rigid:footl', 10: 'rigid:footr',
          21: 'mix:upperlegl=.4,lowerlegl=.6', 22: 'mix:upperlegr=.4,lowerlegr=.6',
          18: 'mix:upperarml=.6,chest=.4', 19: 'mix:upperarmr=.6,chest=.4', 13: 'heat:chest,upperarml,lowerarml', 14: 'heat:chest,upperarmr,lowerarmr',
          16: 'heat:lowerarml,handl', 17: 'heat:lowerarmr,handr', 0: 'rigid:handl', 2: 'rigid:handr'},
    DEFAULT='auto', FACES={}, SHOULDER=[6],
    J={'hips': (0, .37, .07), 'spine': (0, .44, .07), 'chest': (0, .5, .07), 'head': (0, .565, .06), 'top': (0, 1.0, .05),
       'upperarml': (.1, .525, .08), 'lowerarml': (.215, .52, .085), 'wristl': (.295, .515, .085), 'handl': (.315, .515, .085), 'handslotl': (.36, .51, .09),
       'upperarmr': (-.1, .525, .08), 'lowerarmr': (-.215, .52, .085), 'wristr': (-.295, .515, .085), 'handr': (-.315, .515, .085), 'handslotr': (-.36, .51, .09),
       'upperlegl': (.065, .34, .08), 'lowerlegl': (.085, .195, .08), 'footl': (.1, .075, .08), 'toesl': (.1, .02, .17),
       'upperlegr': (-.065, .34, .08), 'lowerlegr': (-.085, .195, .08), 'footr': (-.1, .075, .08), 'toesr': (-.1, .02, .17)}),
  # the "hooded knight" (owner's GPT T-pose -> Tripo, textured, segment by prompt: 137 parts, 2026-11-18): 1.0 tall, T-pose, faces +z
  'hood': dict(
    ROLE={0: 'rigid:head', 9: 'rigid:head', 31: 'rigid:head', 11: 'mix:chest=.7,head=.3', 2: 'rigid:chest', 4: 'heat:spine,chest', 7: 'heat:hips,spine,chest',
          8: 'heat:hips,upperlegl,upperlegr', 30: 'rigid:hips', 25: 'rigid:hips', 1: 'rigid:hips', 17: 'rigid:hips', 18: 'rigid:hips', 19: 'rigid:hips',
          22: 'mix:hips=.7,upperlegl=.15,upperlegr=.15', 12: 'heat:hips,upperlegl,lowerlegl', 10: 'heat:hips,upperlegr,lowerlegr',
          5: 'heat:lowerlegl,footl', 13: 'heat:lowerlegr,footr', 33: 'mix:upperlegl=.4,lowerlegl=.6', 32: 'mix:upperlegr=.4,lowerlegr=.6',
          21: 'heat:chest,upperarml', 20: 'heat:chest,upperarmr', 27: 'rigid:upperarml', 26: 'rigid:upperarmr', 29: 'mix:upperarml=.6,chest=.4', 28: 'mix:upperarmr=.6,chest=.4',
          24: 'mix:upperarml=.6,chest=.4', 23: 'mix:upperarmr=.6,chest=.4', 15: 'heat:lowerarml,handl', 14: 'heat:lowerarmr,handr', 3: 'rigid:handl', 6: 'rigid:handr'},
    DEFAULT='auto', FACES={}, SHOULDER=[4, 2],
    J={'hips': (0, .43, .04), 'spine': (0, .5, .04), 'chest': (0, .57, .04), 'head': (0, .655, .03), 'top': (0, 1.0, .03),
       'upperarml': (.09, .59, .04), 'lowerarml': (.205, .59, .045), 'wristl': (.29, .585, .06), 'handl': (.31, .585, .065), 'handslotl': (.35, .58, .07),
       'upperarmr': (-.09, .59, .04), 'lowerarmr': (-.205, .59, .045), 'wristr': (-.29, .585, .06), 'handr': (-.31, .585, .065), 'handslotr': (-.35, .58, .07),
       'upperlegl': (.05, .42, .03), 'lowerlegl': (.075, .22, .03), 'footl': (.1, .07, .03), 'toesl': (.1, .02, .11),
       'upperlegr': (-.05, .42, .03), 'lowerlegr': (-.075, .22, .03), 'footr': (-.1, .07, .03), 'toesr': (-.1, .02, .11)}),
  # the "winged knight" (owner's GPT T-pose front / left / back -> Tripo multi-view, segment custom 21 names, 2026-11-18): texturing re-merged the
  # 194 parts into 140, many of them several loose pieces from all over the body, so 'auto' works per loose piece and 'main:<role>' gives
  # the biggest piece of a part the role (the rest auto). 0.97 tall, T-pose, open hands, symmetric
  'winged': dict(
    ROLE={0: 'rigid:head', 1: 'rigid:head', 9: 'rigid:head', 6: 'heat:spine,chest', 18: 'rigid:chest',
          10: 'heat:hips,upperlegl,upperlegr,lowerlegl,lowerlegr', 2: 'heat:lowerlegr,footr', 20: 'heat:lowerlegl,footl', 12: 'rigid:lowerlegr', 28: 'rigid:lowerlegl',
          15: 'rigid:handr', 78: 'main:rigid:handl', 22: 'rigid:lowerarml', 19: 'mix:upperarml=.6,chest=.4', 101: 'main:mix:upperarmr=.6,chest=.4',
          3: 'mix:spine=.5,chest=.5', 16: 'mix:spine=.5,chest=.5', 36: 'mix:spine=.5,chest=.5', 92: 'main:mix:spine=.5,chest=.5', 193: 'main:mix:spine=.5,chest=.5'},
    DEFAULT='auto', FACES={}, SHOULDER=[],
    J={'hips': (0, .36, .06), 'spine': (0, .43, .06), 'chest': (0, .5, .06), 'head': (0, .57, .05), 'top': (0, .97, .05),
       'upperarml': (.105, .51, .065), 'lowerarml': (.215, .505, .065), 'wristl': (.285, .505, .065), 'handl': (.3, .505, .065), 'handslotl': (.335, .5, .07),
       'upperarmr': (-.105, .51, .065), 'lowerarmr': (-.215, .505, .065), 'wristr': (-.285, .505, .065), 'handr': (-.3, .505, .065), 'handslotr': (-.335, .5, .07),
       'upperlegl': (.06, .335, .06), 'lowerlegl': (.075, .19, .06), 'footl': (.085, .075, .05), 'toesl': (.085, .02, .15),
       'upperlegr': (-.06, .335, .06), 'lowerlegr': (-.075, .19, .06), 'footr': (-.085, .075, .05), 'toesr': (-.085, .02, .15)}),
  # the BASE BODY (owner 2026-11-21 "ตัวเปล่า": one body for every hero, outfits worn on it): GPT turnaround -> Tripo multi-view, split: 36 parts,
  # NO texture (flat colours per part from COLORS), 1.0 tall, A-pose (arms ~57 degrees down), faces +z, her left = +x. Separate meshes: body / hair / top / shorts
  'base': dict(
    ROLE={0: 'headblend', 1: 'rigid:head', 9: 'rigid:head', 2: 'heat:chest,upperarmr,lowerarmr,handr', 3: 'heat:chest,upperarml,lowerarml,handl',
          4: 'heat:hips,upperlegl,lowerlegl,footl', 8: 'heat:hips,upperlegr,lowerlegr,footr', 5: 'heat:hips,spine,chest', 7: 'rigid:chest',
          6: 'heat:hips,upperlegl,upperlegr'},
    DEFAULT='auto', FACES={}, SHOULDER=[5], HB=(.6, .04),
    MESH={1: 'hair', 9: 'hair', 13: 'hair', 14: 'hair', 15: 'hair', 16: 'hair', 17: 'hair', 18: 'hair', 19: 'hair', 20: 'hair', 22: 'hair', 24: 'hair', 25: 'hair',
          5: 'top', 7: 'top', 6: 'shorts'},
    COLORS={0: 'f0b48c', 2: 'f0b48c', 3: 'f0b48c', 4: 'f0b48c', 8: 'f0b48c', 1: '7a3e22', 9: '7a3e22', 5: '9a9aa2', 7: '9a9aa2', 6: '3c3c44',
            10: '2a1810', 11: '2a1810', 12: 'c0605a', 21: '5a3020', 23: '5a3020', 26: 'd8342c', 27: 'd8342c', 28: 'd8342c', 29: 'd8342c',
            30: 'b01818', 31: 'b01818', 32: '2a1810', 33: '2a1810', 34: 'ffffff', 35: 'ffffff', 'default': '7a3e22'},
    J=MODELS_BASE_J),
  # OUTFIT TEST (owner 2026-11-21 "ลองเอาชุดธนูมาใส่ ... เอาแต่ชุด"): the huntress's armour / cape / fur skirt (warrior_split_raw parts 1 + 6; her arms,
  # legs, boots and head are fused with skin, so they stay out) moved from her joints to the BASE body's joints (FIT), pushed outside the base's
  # tank top / shorts (PUSH_OUT), weighted on the base joints, exported as one mesh "outfit" with its own atlas = worn on the base rig in the game
  'base_archer_outfit': dict(
    ROLE={1: 'heat:hips,spine,chest,upperlegl,upperlegr', 6: 'heat:hips,spine,chest'}, DEFAULT='drop', FACES={1: 12000, 6: 2000}, SHOULDER=[1],
    MESH={1: 'outfit', 6: 'outfit'},
    FIT=dict(src=(-.025, .37, .045), dst=(0, .41, .05), scale=(.765, .951, .92)),   # her hips -> base hips; shoulder width .17 -> .13, hips-shoulder .205 -> .195
    PUSH_OUT=('art/incoming/basebody/tripo_base_v1_tex.glb', ['tripo_part_5', 'tripo_part_7', 'tripo_part_6'], .006),
    J=MODELS_BASE_J),
}
CFG = MODELS[MODEL]; ROLE, J = CFG['ROLE'], CFG['J']
BONES = [('hips', 'spine', None), ('spine', 'chest', 'hips'), ('chest', 'head', 'spine'), ('head', 'top', 'chest'),
         ('upperarml', 'lowerarml', 'chest'), ('lowerarml', 'wristl', 'upperarml'), ('handl', 'handslotl', 'lowerarml'),
         ('upperarmr', 'lowerarmr', 'chest'), ('lowerarmr', 'wristr', 'upperarmr'), ('handr', 'handslotr', 'lowerarmr'),
         ('upperlegl', 'lowerlegl', 'hips'), ('lowerlegl', 'footl', 'upperlegl'), ('footl', 'toesl', 'lowerlegl'),
         ('upperlegr', 'lowerlegr', 'hips'), ('lowerlegr', 'footr', 'upperlegr'), ('footr', 'toesr', 'lowerlegr')]
def G(x, y, z): return Vector((x, -z, y)) * SC   # game (model units) -> Blender (x10)
def gpos(co): c = co / SC; return (c.x, c.z, -c.y)   # Blender -> game

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
parts = {}
for o in list(bpy.data.objects):
    if o.type != 'MESH': continue
    n = int(o.name.split('_')[-1].split('.')[0]); role = ROLE.get(n, CFG['DEFAULT'])
    if role == 'drop': bpy.data.objects.remove(o)
    else: parts[n] = o
for o in list(bpy.data.objects):
    if o.type != 'MESH': bpy.data.objects.remove(o)
def role_of(n): return ROLE.get(n, CFG['DEFAULT'])
print('parts kept', len(parts))

def only(o):
    for q in bpy.data.objects: q.select_set(False)
    bpy.context.view_layer.objects.active = o; o.select_set(True)

# ---- textures of each part (before anything renames them)
def part_images(o):
    base = norm = rm = None
    if o.active_material and o.active_material.node_tree:
        for n in o.active_material.node_tree.nodes:
            if n.type == 'TEX_IMAGE' and n.image:
                nm = n.image.name.lower()
                if 'basecolor' in nm or 'base' in nm and base is None: base = n.image
                elif 'normal' in nm: norm = n.image
                elif '_rm' in nm or 'metal' in nm: rm = n.image   # glTF metal-roughness: G roughness, B metal
    return base, norm, rm
IMG = {n: part_images(o) for n, o in parts.items()}

# ---- outfit models: move the parts from their own body's joints onto another body's (game units, before x10), then push them outside that body
if 'FIT' in CFG:
    F = CFG['FIT']; (cx, cy, cz), (dx, dy, dz), (sx, sy, sz) = F['src'], F['dst'], F['scale']
    for n, o in parts.items():
        o.parent = None; only(o); bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        for v in o.data.vertices:
            gx, gy, gz = v.co.x, v.co.z, -v.co.y
            nx, ny, nz = dx + (gx - cx) * sx, dy + (gy - cy) * sy, dz + (gz - cz) * sz
            v.co = Vector((nx, -nz, ny))
# ---- geometry: x10, join seams, cap the cut holes, decimate when the part has a budget
for n, o in parts.items():
    o.parent = None; only(o); o.scale = (SC, SC, SC); bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
    edges = [e for e in bm.edges if e.is_boundary]
    if edges: r = bmesh.ops.holes_fill(bm, edges=edges, sides=0); bmesh.ops.triangulate(bm, faces=r['faces'])
    bm.to_mesh(o.data); bm.free()
    f0, fb = len(o.data.polygons), CFG['FACES'].get(n)
    if fb and f0 > fb:
        d = o.modifiers.new('dec', 'DECIMATE'); d.ratio = fb / f0; bpy.ops.object.modifier_apply(modifier='dec')
print('faces', sum(len(o.data.polygons) for o in parts.values()))
if 'PUSH_OUT' in CFG:   # nothing of the outfit inside the body it is worn on (its tank top / shorts would poke through)
    path, names, off = CFG['PUSH_OUT']; before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path); new = [o for o in bpy.data.objects if o not in before]; newn = [o.name for o in new]; tg = [o for o in new if o.type == 'MESH' and o.name.split('.')[0] in names]
    for o in tg:
        o.parent = None; only(o); o.scale = (SC, SC, SC); bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    for q in bpy.data.objects: q.select_set(False)
    for o in tg: o.select_set(True)
    bpy.context.view_layer.objects.active = tg[0]; bpy.ops.object.join(); tgt = tg[0]
    for n, o in parts.items():
        only(o); m = o.modifiers.new('push', 'SHRINKWRAP'); m.target = tgt; m.wrap_method = 'NEAREST_SURFACEPOINT'; m.wrap_mode = 'OUTSIDE'; m.offset = off * SC
        bpy.ops.object.modifier_apply(modifier='push')
    print('pushed outside', tgt.name)
    for nm in newn:
        if nm in bpy.data.objects: bpy.data.objects.remove(bpy.data.objects[nm])

# ---- armature at the model's joints
arm = bpy.data.armatures.new('rig'); rig = bpy.data.objects.new('rig', arm); bpy.context.collection.objects.link(rig)
only(rig); bpy.ops.object.mode_set(mode='EDIT')
for name, tail, parent in BONES:
    b = arm.edit_bones.new(name); b.head = G(*J[name]); t = G(*J[tail])
    if name in ('handl', 'handr'): b.head = G(*J['wrist' + name[-1]])
    if (t - b.head).length < 1e-2: t = b.head + Vector((0, 0, .3))
    b.tail = t
for name, tail, parent in BONES:
    if parent: arm.edit_bones[name].parent = arm.edit_bones[parent]
bpy.ops.object.mode_set(mode='OBJECT')
ALL = [b[0] for b in BONES]

def seg_dist(p, a, b):
    a, b, q = Vector(a), Vector(b), Vector(p); ab = b - a; t = max(0, min(1, (q - a).dot(ab) / max(1e-9, ab.dot(ab)))); return (q - (a + ab * t)).length
SEGS = {n: (J[n] if n not in ('handl', 'handr') else J['wrist' + n[-1]], J[t]) for n, t, _ in BONES}
def nearest_bone(p, names): return min(names, key=lambda n: seg_dist(p, *SEGS[n]))

def set_w(o, ws_per_vertex):
    for nm in ALL:
        if nm not in o.vertex_groups: o.vertex_groups.new(name=nm)
    for vi, ws in enumerate(ws_per_vertex):
        tot = sum(ws.values()) or 1
        for nm, w in ws.items():
            if w / tot > 1e-3: o.vertex_groups[nm].add([vi], w / tot, 'REPLACE')

def heat(o, names):
    """heat weights on a watertight voxel copy, only `names` deform, copied to the real part by nearest surface"""
    for b in arm.bones: b.use_deform = b.name in names
    px = o.copy(); px.data = o.data.copy(); px.name = 'proxy'; bpy.context.collection.objects.link(px); px.vertex_groups.clear(); px.modifiers.clear()
    only(px); r = px.modifiers.new('rm', 'REMESH'); r.mode = 'VOXEL'; r.voxel_size = VOXEL; bpy.ops.object.modifier_apply(modifier='rm')
    if len(px.data.polygons) > 30000:
        d = px.modifiers.new('dec', 'DECIMATE'); d.ratio = 30000 / len(px.data.polygons); bpy.ops.object.modifier_apply(modifier='dec')
    for q in bpy.data.objects: q.select_set(False)
    px.select_set(True); rig.select_set(True); bpy.context.view_layer.objects.active = rig
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    miss = sum(1 for v in px.data.vertices if not v.groups)
    for nm in ALL:
        if nm not in o.vertex_groups: o.vertex_groups.new(name=nm)
    only(o); dt = o.modifiers.new('dt', 'DATA_TRANSFER'); dt.object = px; dt.use_vert_data = True; dt.data_types_verts = {'VGROUP_WEIGHTS'}
    dt.vert_mapping = 'POLYINTERP_NEAREST'; dt.layers_vgroup_select_src = 'ALL'; dt.layers_vgroup_select_dst = 'NAME'
    bpy.ops.object.modifier_apply(modifier='dt'); bpy.data.objects.remove(px)
    for b in arm.bones: b.use_deform = True
    fill = 0
    for v in o.data.vertices:   # anything the heat solve left empty: nearest allowed bone
        if not [g for g in v.groups if g.weight > 1e-4]:
            o.vertex_groups[nearest_bone(gpos(v.co), names)].add([v.index], 1, 'REPLACE'); fill += 1
    print('  heat', n, 'bones', names, 'proxy unweighted', miss, 'filled', fill)

def islands(o):   # the loose pieces of a part (vertex index lists, biggest first)
    nb = [[] for _ in o.data.vertices]
    for e in o.data.edges: a, b = e.vertices; nb[a].append(b); nb[b].append(a)
    seen, out = [False] * len(nb), []
    for v in range(len(nb)):
        if seen[v]: continue
        st, comp = [v], []; seen[v] = True
        while st:
            a = st.pop(); comp.append(a)
            for b in nb[a]:
                if not seen[b]: seen[b] = True; st.append(b)
        out.append(comp)
    return sorted(out, key=len, reverse=True)
def fixed(role):   # rigid / mix role -> one weight dict
    if role.startswith('rigid:'): return {role[6:]: 1}
    return {k: float(w) for k, w in (q.split('=') for q in role[4:].split(','))}
auto = {}
def auto_w(o, ws, comps):   # a small rigid piece (chain link, spike, gem, buckle) follows the bone nearest to its middle: per loose piece
    for comp in comps:
        c = gpos(sum((o.data.vertices[i].co for i in comp), Vector()) / len(comp))
        b = 'head' if c[1] > J['head'][1] + .02 else nearest_bone(c, ALL); auto[b] = auto.get(b, 0) + 1   # above the neck = the head (helmet discs beside a big chibi head are nearer the shoulder bone)
        for i in comp: ws[i] = {b: 1}
for n, o in parts.items():
    role = role_of(n); nv = len(o.data.vertices)
    if role.startswith('heat:'): heat(o, role[5:].split(','))
    elif role.startswith('rigid:') or role.startswith('mix:'): set_w(o, [fixed(role)] * nv)
    elif role.startswith('main:'):
        comps = islands(o); ws = [None] * nv
        for i in comps[0]: ws[i] = fixed(role[5:])
        auto_w(o, ws, comps[1:]); set_w(o, ws)
    elif role in ('bow', 'string'): set_w(o, [{'handl': 1}] * nv)
    elif role == 'headblend':   # face + mane with the head; hanging braids blend down to the chest
        ws = []
        for v in o.data.vertices:
            x, y, z = gpos(v.co); hb = CFG.get('HB', (.5, .12)); t = max(0, min(1, (y - hb[0]) / hb[1])); ws.append({'head': t, 'chest': 1 - t})
        set_w(o, ws)
    else:   # auto
        ws = [None] * nv; auto_w(o, ws, islands(o)); set_w(o, ws)
print('auto parts per bone', auto)

for n in CFG['SHOULDER']:   # the shoulder of the body part follows the upper arm a little, so a raised arm does not open a gap
    if n not in parts: continue
    body = parts[n]
    for side in 'lr':
        sh = Vector(J['upperarm' + side])
        for v in body.data.vertices:
            p = Vector(gpos(v.co)); d = (p - sh).length
            if d < .06 and p.y > sh.y - .08:
                w = .6 * (1 - d / .06)
                ws = {body.vertex_groups[g.group].name: g.weight * (1 - w) for g in v.groups}; ws['upperarm' + side] = ws.get('upperarm' + side, 0) + w
                for nm, ww in ws.items(): body.vertex_groups[nm].add([v.index], ww, 'REPLACE')

# ---- one atlas for every part, packed in shelves: each part's own 0-1 UVs squeezed into its tile; sizes scaled so all fit
AW = AH = 2048 if any(IMG[n][0] for n in parts) else 512; PAD = 2   # flat-colour models need only a small atlas
SIZE = {n: (IMG[n][0].size[0] if IMG[n][0] else 32) for n in parts}
area = sum(s * s for s in SIZE.values()); f = min(1, math.sqrt(.82 * AW * AH / max(1, area)))
def packit(f):
    tiles = sorted(((max(16, int(SIZE[n] * f)), n) for n in parts), reverse=True); x = y = rowh = 0; out = {}
    for s, n in tiles:
        if x + s > AW: x = 0; y += rowh; rowh = 0
        if y + s > AH: return None
        out[n] = (x, y, s); x += s; rowh = max(rowh, s)
    return out
SLOTS = packit(f)
while SLOTS is None: f *= .94; SLOTS = packit(f)
print('atlas scale %.2f' % f, 'biggest tile', max(s for _, _, s in SLOTS.values()))
def tile(img, size, half=False):
    a = np.empty(img.size[0] * img.size[1] * 4, np.float32); img.pixels.foreach_get(a); a = a.reshape(img.size[1], img.size[0], 4)
    ys = (np.arange(size) * img.size[1] / size).astype(int); xs = (np.arange(size) * img.size[0] / size).astype(int); a = a[ys][:, xs]
    if half: a = a[::2, ::2]
    return a
HAS = [any(IMG[n][k] for n in parts) for k in range(3)]
def build_atlas(which, half):
    s = 2 if half else 1; A = np.zeros((AH // s, AW // s, 4), np.float32); A[..., 3] = 1
    if which == 1: A[..., 0:3] = (.5, .5, 1)   # flat normal where nothing is
    if which == 2: A[..., 0:3] = (1, .65, 0)   # rough, not metal
    for n, (x0, y0, sz) in SLOTS.items():
        img = IMG[n][which]
        if img is None and which == 0 and 'COLORS' in CFG:   # no texture in the export: a flat colour tile (sRGB byte image = display values)
            hx = CFG['COLORS'].get(n, CFG['COLORS'].get('default', '808080')); A[y0 // s:y0 // s + sz // s, x0 // s:x0 // s + sz // s, 0:3] = [int(hx[i:i + 2], 16) / 255 for i in (0, 2, 4)]; continue
        if img is None: continue
        t = tile(img, sz, half); A[y0 // s:y0 // s + t.shape[0], x0 // s:x0 // s + t.shape[1]] = t
    im = bpy.data.images.new('atlas_' + ('base', 'normal', 'rm')[which], AW // s, AH // s, alpha=False)
    im.colorspace_settings.name = 'Non-Color' if which else 'sRGB'; im.pixels.foreach_set(A.ravel()); im.update(); im.pack()
    print('atlas', im.name, im.size[:], 'mean', A.reshape(-1, 4).mean(0).round(3)); return im
BASE = build_atlas(0, False); NORM = build_atlas(1, True) if HAS[1] else None; RMI = build_atlas(2, True) if HAS[2] else None
for n, o in parts.items():
    x0, y0, sz = SLOTS[n]
    if not o.data.uv_layers: o.data.uv_layers.new()
    for l in o.data.uv_layers.active.data:
        u = min(1, max(0, l.uv.x)); v = min(1, max(0, l.uv.y))
        l.uv.x = (x0 + PAD + u * (sz - 2 * PAD)) / AW; l.uv.y = (y0 + PAD + v * (sz - 2 * PAD)) / AH
mat = bpy.data.materials.new(MODEL); mat.use_nodes = True; nt = mat.node_tree; bsdf = nt.nodes['Principled BSDF']
tb = nt.nodes.new('ShaderNodeTexImage'); tb.image = BASE; nt.links.new(tb.outputs['Color'], bsdf.inputs['Base Color'])
if NORM: tn = nt.nodes.new('ShaderNodeTexImage'); tn.image = NORM; nm_ = nt.nodes.new('ShaderNodeNormalMap'); nt.links.new(tn.outputs['Color'], nm_.inputs['Color']); nt.links.new(nm_.outputs['Normal'], bsdf.inputs['Normal'])
if RMI:
    tr = nt.nodes.new('ShaderNodeTexImage'); tr.image = RMI; sp = nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(tr.outputs['Color'], sp.inputs['Color'])
    nt.links.new(sp.outputs['Green'], bsdf.inputs['Roughness']); nt.links.new(sp.outputs['Blue'], bsdf.inputs['Metallic'])
else: bsdf.inputs['Metallic'].default_value = 0; bsdf.inputs['Roughness'].default_value = .6
for o in parts.values(): o.data.materials.clear(); o.data.materials.append(mat)

# ---- join: "body" = every part but the bow, "bow", "string" (the game can pull the string to the hand while she draws); all skinned on the rig
def join(objs, name):
    if not objs: return None
    for q in bpy.data.objects: q.select_set(False)
    for q in objs: q.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]; bpy.ops.object.join(); objs[0].name = name; objs[0].data.name = name; return objs[0]
MESHN = CFG.get('MESH', {})
outs = [join([o for n, o in sorted(parts.items()) if role_of(n) not in ('bow', 'string') and n not in MESHN], 'body')] + [join([o for n, o in sorted(parts.items()) if MESHN.get(n) == nm], nm) for nm in sorted(set(MESHN.values()))] + [
        join([o for n, o in sorted(parts.items()) if role_of(n) == 'bow'], 'bow'),
        join([o for n, o in sorted(parts.items()) if role_of(n) == 'string'], 'string')]
outs = [o for o in outs if o]
for o in outs:
    o.parent = rig; m = o.modifiers.new('rig', 'ARMATURE'); m.object = rig
    print(o.name, 'faces', len(o.data.polygons), 'verts', len(o.data.vertices))
rig['joints'] = json.dumps({k: [round(c * SC, 4) for c in v] for k, v in J.items()})   # the game re-binds on these (glTF extras)
for q in bpy.data.objects: q.select_set(False)
for q in outs + [rig]: q.select_set(True)
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True, export_image_format='JPEG', export_jpeg_quality=86, export_animations=False, export_extras=True)
print('wrote', OUT)
