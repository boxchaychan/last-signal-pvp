# Quaternius "Ultimate Stylized Nature" (CC0, art/incoming/quaternius/nature) -> light game copies for tribe3d.html.
#   pip install bpy            (Blender 5.3 as a Python module, once per session)
#   python3 tools/blender/nature_pack.py [out folder, default art/tribe3d/nature]
# For each chosen model: import (glTF or FBX), split by material, thin out the bark (decimate; the pixel look hides it),
# keep leaf / flower / grass cards as they are, put the base on the ground (y = 0), export a .glb WITHOUT images
# (geometry, UVs and material names only). The game loads the small textures from <out>/tex/ itself (made below with Pillow:
# 128-256 px, enough for the 1 render pixel = 1/8 unit look). Normal maps are dropped.
import bpy, bmesh, sys, os, random
from mathutils import Vector
from PIL import Image

SRC = 'art/incoming/quaternius/nature'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'art/tribe3d/nature'
os.makedirs(os.path.join(OUT, 'tex'), exist_ok=True)

# name, bark decimate ratio (1 = untouched); leaf cards are not decimated: a share of whole cards is dropped instead (LEAF_KEEP)
# and the cards left are enlarged a little around their own middle, so the crown keeps its outline with fewer triangles
LEAF_KEEP, LEAF_GROW = .6, 1.18
PICK = [(f'MapleTree_{i}', .12) for i in range(1, 6)] + [(f'BirchTree_{i}', .12) for i in range(1, 6)] + \
       [(f'NormalTree_{i}', .12) for i in range(1, 6)] + [(f'PineTree_{i}', .2) for i in range(1, 6)] + \
       [(f'DeadTree_{i}', .25) for i in (1, 3, 5, 6, 9)] + \
       [(n, 1) for n in ('Bush', 'Bush_Flowers', 'Bush_Large', 'Bush_Large_Flowers', 'Bush_Small', 'Bush_Small_Flowers',
                         'Flower_1_Clump', 'Flower_2_Clump', 'Flower_3_Clump', 'Flower_4_Clump', 'Flower_5_Clump',
                         'Grass_Small', 'Grass_Large', 'Plant_1', 'Plant_2', 'Plant_Flowers')] + \
       [(f'Rock_{i}', .5) for i in range(1, 6)]
# NP_PICK="PalmTree_1:1,PalmTree_2:.4" = convert only these (name:bark ratio), e.g. the palms for pixgrind.html
if os.environ.get('NP_PICK'): PICK = [(n, float(r)) for n, r in (x.split(':') for x in os.environ['NP_PICK'].split(','))]
CARD = ('Leaves', 'Flowers', 'Grass', 'Petal', 'Plant')   # material names that are cut-out cards

def is_card(name): return any(k.lower() in name.lower() for k in CARD)

def load(name):
    g, f = os.path.join(SRC, 'gltf', name + '.gltf'), os.path.join(SRC, 'fbx', name + '.fbx')
    if os.path.exists(g): bpy.ops.import_scene.gltf(filepath=g)
    elif os.path.exists(f): bpy.ops.import_scene.fbx(filepath=f)
    else: raise FileNotFoundError(name)

report = []
for name, ratio in PICK:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    try: load(name)
    except Exception as e: print('skip', name, e); continue
    obs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    # apply transforms (FBX comes in at 0.01 scale with a rotation), then split every mesh by material
    bpy.ops.object.select_all(action='DESELECT')
    for o in obs: o.select_set(True)
    bpy.context.view_layer.objects.active = obs[0]
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    if len(obs) > 1: bpy.ops.object.join()
    ob = bpy.context.view_layer.objects.active
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.mesh.separate(type='MATERIAL'); bpy.ops.object.mode_set(mode='OBJECT')
    parts = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    tris = 0
    for o in parts:
        mname = o.active_material.name if o.active_material else ''
        if ratio < 1 and not is_card(mname):
            m = o.modifiers.new('dec', 'DECIMATE'); m.ratio = ratio
            bpy.context.view_layer.objects.active = o; bpy.ops.object.modifier_apply(modifier='dec')
        elif ratio < 1 and 'Leaves' in mname:   # tree crown: drop whole cards (islands of linked faces), grow the rest
            rnd = random.Random(name); bm = bmesh.new(); bm.from_mesh(o.data); bm.faces.ensure_lookup_table()
            seen, drop = set(), []
            for f in bm.faces:
                if f.index in seen: continue
                isl, stack = [], [f]; seen.add(f.index)
                while stack:
                    g = stack.pop(); isl.append(g)
                    for e in g.edges:
                        for h in e.link_faces:
                            if h.index not in seen: seen.add(h.index); stack.append(h)
                if rnd.random() > LEAF_KEEP: drop.extend(isl)
                else:
                    vs = {v for g in isl for v in g.verts}; c = sum((v.co for v in vs), Vector()) / len(vs)
                    for v in vs: v.co = c + (v.co - c) * LEAF_GROW
            bmesh.ops.delete(bm, geom=drop, context='FACES'); bm.to_mesh(o.data); bm.free()
        o.data.calc_loop_triangles(); tris += len(o.data.loop_triangles)
    # base on the ground: lowest point of the non-card parts (bushes / grass: of everything), centred in x / y
    zs = [(o.matrix_world @ v.co) for o in parts for v in o.data.vertices]
    minz = min(v.z for v in zs)
    for o in parts:
        for v in o.data.vertices: v.co.z -= minz
    bpy.ops.object.select_all(action='DESELECT')
    for o in parts: o.select_set(True)
    path = os.path.join(OUT, name + '.glb')
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_materials='EXPORT', export_image_format='NONE',
                              export_normals=True, export_texcoords=True, export_apply=True)
    mats = sorted({o.active_material.name for o in parts if o.active_material})
    h = max(v.z for v in zs) - minz
    report.append(f'{name:22s} {tris:5d} tris  h {h:.2f}  {mats}')
    print(report[-1])

# small textures (colour only); leaves keep their alpha
TEX = {'MapleTree_Leaves.png': 256, 'BirchTree_Leaves.png': 256, 'NormalTree_Leaves.png': 256, 'PineTree_Leaves.png': 256, 'Bush_Leaves.png': 256,
       'Flowers.png': 256, 'Grass.png': 64, 'MapleTree_Bark.jpg': 64, 'BirchTree_Bark.jpg': 64, 'NormalTree_Bark.jpg': 64, 'PineTree_Bark.jpg': 64, 'Rocks.jpg': 64, 'Leaves_BW.png': 256, 'PalmTree_Leaves.png': 256, 'PalmTree_Trunk.jpg': 64}
for f, s in TEX.items():
    p = os.path.join(SRC, 'gltf', f)
    if not os.path.exists(p): print('no texture', f); continue
    im = Image.open(p); im = im.convert('RGBA' if im.mode == 'RGBA' else 'RGB').resize((s, s), Image.LANCZOS)
    im.save(os.path.join(OUT, 'tex', f.rsplit('.', 1)[0] + '.png'))
print('\n'.join(report))
