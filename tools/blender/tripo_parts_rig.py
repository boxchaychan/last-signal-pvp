# Rig a Tripo model that the owner SPLIT INTO PARTS in the Tripo app (Segment -> export GLB: one mesh + its own texture per part).
# Knowing the parts makes the rig clean where tripo_rig.py had to guess from texture islands: every part only listens to the bones it
# belongs to (the skirt never follows an arm, the bow is rigid in the left hand), and the bow is its own mesh the game can hide or swap.
# Steps: drop the crumbs (parts of a few faces), x10, join seam-split vertices, close the holes where Tripo cut the parts (like Tripo's
# "Quick Cap", free), decimate each part to a budget, weights per part (heat weights on a voxel proxy limited to the part's bones, or rigid),
# one texture atlas for every part (base colour + normal), export: mesh "body" + mesh "bow" + armature with the KayKit Rig_Medium names
# at HER joints (the game re-binds them onto a KayKit skeleton: tribe3d.html rigTripo, so every KayKit move plays).
#   pip install bpy ; python3 tools/blender/tripo_parts_rig.py art/incoming/tribe3d/tripo/warrior_split_raw.glb art/grind3d/huntress.glb
# Part numbers are per model: look at them first (front / side point plot of each part) and fill ROLE.
import bpy, bmesh, sys, json, math
import numpy as np
from mathutils import Vector
SRC, OUT = sys.argv[-2], sys.argv[-1]
SC, VOXEL = 10, .06
# the "tribal female warrior" split on 2026-11-17 (game coords: y up, she looks at +z, her left hand +x, 0.97 tall)
ROLE = {0: 'head', 1: 'body', 2: 'bow', 3: 'legs', 4: 'arm_r', 5: 'foot_l', 6: 'cape', 7: 'string', 8: 'arm_l', 9: 'foot_r'}
FACES = {0: 17000, 1: 12000, 2: 4000, 3: 5000, 4: 2400, 5: 1200, 6: 2000, 7: 600, 8: 2300, 9: 1200}   # ~48k: one hero can afford the detail (was 27k: spikes and folds went soft)
BONESET = {   # heat-weighted parts: the only bones that may move them
    'body': ['hips', 'spine', 'chest', 'upperlegl', 'upperlegr'],
    'cape': ['hips', 'spine', 'chest'],
    'legs': ['hips', 'upperlegl', 'lowerlegl', 'footl', 'upperlegr', 'lowerlegr', 'footr'],
    'arm_l': ['chest', 'upperarml', 'lowerarml', 'handl'],
    'arm_r': ['chest', 'upperarmr', 'lowerarmr', 'handr'],
}
J = {   # her joints (game coords, model units), read off grid renders for tripo_rig.py; the split model has the same frame
    'hips': (-.035, .37, .045), 'spine': (-.03, .44, .05), 'chest': (-.025, .52, .05), 'head': (-.025, .6, .04), 'top': (-.025, .86, .03),
    'upperarml': (.06, .575, .04), 'lowerarml': (.095, .48, .045), 'wristl': (.145, .425, .05), 'handl': (.165, .418, .05), 'handslotl': (.195, .41, .05),
    'upperarmr': (-.11, .575, .04), 'lowerarmr': (-.16, .495, .045), 'wristr': (-.19, .39, .05), 'handr': (-.195, .38, .05), 'handslotr': (-.2, .36, .05),
    'upperlegl': (.015, .37, .045), 'lowerlegl': (.02, .2, .045), 'footl': (.022, .065, .03), 'toesl': (.022, .02, .1),
    'upperlegr': (-.085, .37, .045), 'lowerlegr': (-.12, .2, .045), 'footr': (-.14, .065, .03), 'toesr': (-.14, .02, .1),
}
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
    n = int(o.name.split('_')[-1].split('.')[0])
    if n in ROLE: parts[n] = o
    else: bpy.data.objects.remove(o)   # crumbs: 30 bits of 1-70 faces, a few millimetres each
for o in list(bpy.data.objects):
    if o.type != 'MESH': bpy.data.objects.remove(o)

def only(o):
    for q in bpy.data.objects: q.select_set(False)
    bpy.context.view_layer.objects.active = o; o.select_set(True)

# ---- textures of each part (before anything renames them)
def part_images(o):
    base = norm = rm = None
    for n in o.active_material.node_tree.nodes:
        if n.type == 'TEX_IMAGE' and n.image:
            nm = n.image.name.lower()
            if 'basecolor' in nm: base = n.image
            elif 'normal' in nm: norm = n.image
            elif '_rm' in nm: rm = n.image   # glTF metal-roughness: G roughness, B metal (the gold trims shine with an environment light)
    return base, norm, rm
IMG = {n: part_images(o) for n, o in parts.items()}

# ---- geometry: x10, join seams, cap the cut holes, decimate
for n, o in parts.items():
    o.parent = None; only(o); o.scale = (SC, SC, SC); bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
    edges = [e for e in bm.edges if e.is_boundary]
    if edges:
        r = bmesh.ops.holes_fill(bm, edges=edges, sides=0)
        bmesh.ops.triangulate(bm, faces=r['faces'])
        caps = len(r['faces'])
    else: caps = 0
    bm.to_mesh(o.data); bm.free()
    f0 = len(o.data.polygons)
    if f0 > FACES[n]:
        d = o.modifiers.new('dec', 'DECIMATE'); d.ratio = FACES[n] / f0; bpy.ops.object.modifier_apply(modifier='dec')
    print('part', n, ROLE[n], 'cap faces', caps, 'faces', f0, '->', len(o.data.polygons))

# ---- armature at her joints
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
    # anything the heat solve left empty: nearest allowed bone
    fill = 0
    for v in o.data.vertices:
        if not [g for g in v.groups if g.weight > 1e-4]:
            o.vertex_groups[nearest_bone(gpos(v.co), names)].add([v.index], 1, 'REPLACE'); fill += 1
    print('  heat', o.name, 'bones', names, 'proxy unweighted', miss, 'filled', fill)

for n, o in parts.items():
    role = ROLE[n]
    if role in BONESET: heat(o, BONESET[role])
    elif role in ('bow', 'string'): set_w(o, [{'handl': 1}] * len(o.data.vertices))
    elif role == 'foot_l': set_w(o, [{'footl': 1}] * len(o.data.vertices))
    elif role == 'foot_r': set_w(o, [{'footr': 1}] * len(o.data.vertices))
    elif role == 'head':   # face + mane with the head; the hanging braids blend down to the chest (they hang from the shoulders)
        ws = []
        for v in o.data.vertices:
            x, y, z = gpos(v.co); t = max(0, min(1, (y - .5) / .12)); ws.append({'head': t, 'chest': 1 - t})
        set_w(o, ws)

# the shoulder of the dress follows the arm a little, so a raised arm does not open a gap at the shoulder
body = [o for n, o in parts.items() if ROLE[n] == 'body'][0]
for side in 'lr':
    sh = Vector(J['upperarm' + side]); g_ua = body.vertex_groups['upperarm' + side]
    for v in body.data.vertices:
        p = Vector(gpos(v.co)); d = (p - sh).length
        if d < .06 and p.y > .5:
            w = .6 * (1 - d / .06)
            ws = {body.vertex_groups[g.group].name: g.weight * (1 - w) for g in v.groups}; ws['upperarm' + side] = ws.get('upperarm' + side, 0) + w
            for nm, ww in ws.items(): body.vertex_groups[nm].add([v.index], ww, 'REPLACE')

# ---- one atlas for every part: base colour (2048 x 1536) + normal (half size), each part's own 0-1 UVs squeezed into its tile
SLOTS = {0: (0, 0, 1024), 1: (1024, 0, 1024), 2: (0, 1024, 512), 3: (512, 1024, 512), 4: (1024, 1024, 256), 5: (1280, 1024, 256),
         6: (1536, 1024, 256), 8: (1792, 1024, 256), 9: (1024, 1280, 256), 7: (1280, 1280, 128)}
AW, AH, PAD = 2048, 1536, 2
def tile(img, size, half=False):
    a = np.empty(img.size[0] * img.size[1] * 4, np.float32); img.pixels.foreach_get(a); a = a.reshape(img.size[1], img.size[0], 4)
    if img.size[0] != size:   # resample (nearest is fine: the sources are already this size or bigger)
        ys = (np.arange(size) * img.size[1] / size).astype(int); xs = (np.arange(size) * img.size[0] / size).astype(int); a = a[ys][:, xs]
    if half: a = a[::2, ::2]
    return a
def build_atlas(which, half):
    s = 2 if half else 1; A = np.zeros((AH // s, AW // s, 4), np.float32); A[..., 3] = 1
    if which == 1: A[..., 0:3] = (.5, .5, 1)   # flat normal where nothing is
    if which == 2: A[..., 0:3] = (1, .65, 0)   # rough, not metal
    for n, (x0, y0, sz) in SLOTS.items():
        img = IMG[n][which]
        if img is None: continue
        t = tile(img, sz, half); A[y0 // s:y0 // s + t.shape[0], x0 // s:x0 // s + t.shape[1]] = t
    im = bpy.data.images.new('atlas_' + ('base', 'normal', 'rm')[which], AW // s, AH // s, alpha=False)
    im.colorspace_settings.name = 'Non-Color' if which else 'sRGB'; im.pixels.foreach_set(A.ravel()); im.update(); im.pack()
    print('atlas', im.name, im.size[:], 'mean', A.reshape(-1, 4).mean(0).round(3)); return im
BASE, NORM, RMI = build_atlas(0, False), build_atlas(1, True), build_atlas(2, True)
for n, o in parts.items():
    x0, y0, sz = SLOTS[n]; uv = o.data.uv_layers.active.data
    for l in uv:
        u = min(1, max(0, l.uv.x)); v = min(1, max(0, l.uv.y))
        l.uv.x = (x0 + PAD + u * (sz - 2 * PAD)) / AW; l.uv.y = (y0 + PAD + v * (sz - 2 * PAD)) / AH
mat = bpy.data.materials.new('huntress'); mat.use_nodes = True; nt = mat.node_tree; bsdf = nt.nodes['Principled BSDF']
tb = nt.nodes.new('ShaderNodeTexImage'); tb.image = BASE; nt.links.new(tb.outputs['Color'], bsdf.inputs['Base Color'])
tn = nt.nodes.new('ShaderNodeTexImage'); tn.image = NORM; nm_ = nt.nodes.new('ShaderNodeNormalMap'); nt.links.new(tn.outputs['Color'], nm_.inputs['Color']); nt.links.new(nm_.outputs['Normal'], bsdf.inputs['Normal'])
tr = nt.nodes.new('ShaderNodeTexImage'); tr.image = RMI; sp = nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(tr.outputs['Color'], sp.inputs['Color'])
nt.links.new(sp.outputs['Green'], bsdf.inputs['Roughness']); nt.links.new(sp.outputs['Blue'], bsdf.inputs['Metallic'])
for o in parts.values(): o.data.materials.clear(); o.data.materials.append(mat)

# ---- join: "body" = every part but the bow, "bow", "string" (the game can pull the string to the hand while she draws); all skinned on the rig
def join(objs, name):
    for q in bpy.data.objects: q.select_set(False)
    for q in objs: q.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]; bpy.ops.object.join(); objs[0].name = name; objs[0].data.name = name; return objs[0]
bodyo = join([o for n, o in sorted(parts.items()) if ROLE[n] not in ('bow', 'string')], 'body')
bowo = join([o for n, o in sorted(parts.items()) if ROLE[n] == 'bow'], 'bow')
stro = join([o for n, o in sorted(parts.items()) if ROLE[n] == 'string'], 'string')
for o in (bodyo, bowo, stro):
    o.parent = rig; m = o.modifiers.new('rig', 'ARMATURE'); m.object = rig
    print(o.name, 'faces', len(o.data.polygons), 'verts', len(o.data.vertices))
rig['joints'] = json.dumps({k: [round(c * SC, 4) for c in v] for k, v in J.items()})   # the game re-binds on these (glTF extras)
for q in bpy.data.objects: q.select_set(False)
for q in (bodyo, bowo, stro, rig): q.select_set(True)
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True, export_image_format='JPEG', export_jpeg_quality=86, export_animations=False, export_extras=True)
print('wrote', OUT)
