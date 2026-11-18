# Cut wearable pieces (helmet, shoulder pads, ...) out of a Tripo model the owner SPLIT INTO PARTS in the Tripo app, for a KayKit body to wear
# (owner 2026-11-17 "แบบนี้พวกที่ฉันแยกพาสออกมาเอาไปใส่ kay kit ได้ถูกไหม" -> "ทำเลย"). Each piece = the listed parts joined, centred on its own
# middle (the original middle is kept in the extras as "center"), in model units (the Tripo model ~1.0 tall), its own small textures
# (each part keeps its picture, shrunk by how big the part is: no atlas). The game pins a piece to a bone like any other gear (tribe3d.html addGear).
# Find the part numbers first: tools/art/tripo_part_view.js renders groups of parts.
#   pip install bpy
#   python3 tools/blender/tripo_gear.py art/incoming/grind3d/knight/knight_raw.glb art/tribe3d/gear/knight_parts.glb DemonHelm=3,111,141,142 DemonPadL=7 DemonPadR=6
#   python3 tools/blender/tripo_gear.py art/incoming/winged/raw.glb art/tribe3d/gear/winged_parts.glb 'WingHelm=*@y>.585!x>-.1&x<.1&z>.12&y<.7~0,9' 'WingPadL=19' 'WingPadR=101@y>.45' 'WingKneeL=28' 'WingKneeR=12'
import bpy, sys, json, math
from mathutils import Vector
SRC, OUT = sys.argv[1], sys.argv[2]
# a piece = part numbers, or * for every part; then optionally @<conditions> on each loose piece's middle (x / y / z, model units, glTF axes:
# +x = his left, y up, +z front) and ~<part numbers> to leave out, e.g. WingHelm=*@y>.585~0,9 = every loose piece above the neck but the hair
# and the face (Tripo's texturing re-merged parts of the winged knight into loose bits from all over the body); !<conditions> = leave out the pieces
# meeting all of them (the eyebrows: !x>-.1&x<.1&z>.12&y<.7). The model must be standing on 0.
import re
def spec(v):
    m = re.match(r'^([*\d,]+)(?:@([^!~]+))?(?:!([^~]+))?(?:~([\d,]+))?$', v); ids, cond, nocond, ex = m.groups(); C = lambda c: re.findall(r'([xyz])([<>])(-?[\d.]+)', c or '')
    return dict(ids=None if ids == '*' else [int(x) for x in ids.split(',')], cond=C(cond), no=C(nocond), ex=[int(x) for x in ex.split(',')] if ex else [])
SETS = {k: spec(v) for k, v in (a.split('=', 1) for a in sys.argv[3:])}
TEX = 512   # the biggest part's picture; smaller parts get less (by the square root of their face share), at least 64

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
bpy.context.view_layer.update()
parts = {}
for o in list(bpy.data.objects):
    n = int(o.name.split('_')[-1].split('.')[0]) if o.type == 'MESH' else -1
    if n >= 0 and any((S['ids'] is None or n in S['ids']) and n not in S['ex'] for S in SETS.values()): parts[n] = o
for o in parts.values():   # out of the hierarchy, world transform applied (Blender z up; glTF export turns it back to y up)
    mw = o.matrix_world.copy(); o.parent = None; o.matrix_world = mw
for o in list(bpy.data.objects):
    if o not in parts.values(): bpy.data.objects.remove(o)
for o in parts.values():
    for q in bpy.data.objects: q.select_set(False)
    bpy.context.view_layer.objects.active = o; o.select_set(True); bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

fmax = max(len(o.data.polygons) for o in parts.values()); done = set()
for n, o in parts.items():   # shrink each part's pictures (normal maps half size)
    s = max(64, min(TEX, 2 ** round(math.log2(TEX * math.sqrt(len(o.data.polygons) / fmax)))))
    for m in o.data.materials:
        if not m or not m.node_tree: continue
        for nd in m.node_tree.nodes:
            if nd.type == 'TEX_IMAGE' and nd.image and nd.image.name not in done and nd.image.size[0] > 0:
                k = s // 2 if 'normal' in nd.image.name.lower() else s
                if nd.image.size[0] > k: nd.image.scale(k, k)
                nd.image.pack(); done.add(nd.image.name)
    print('part', n, len(o.data.polygons), 'faces, picture', s)

import bmesh
def pick(o, S):   # a copy of part o holding only the loose pieces whose middle meets the conditions (None if none)
    q = o.copy(); q.data = o.data.copy(); bpy.context.collection.objects.link(q)
    if not S['cond'] and not S['no']: return q
    bm = bmesh.new(); bm.from_mesh(q.data); bm.verts.ensure_lookup_table(); seen, drop = set(), []
    for v in bm.verts:
        if v.index in seen: continue
        st, comp = [v], []; seen.add(v.index)
        while st:
            a = st.pop(); comp.append(a)
            for e in a.link_edges:
                b = e.other_vert(a)
                if b.index not in seen: seen.add(b.index); st.append(b)
        c = sum((a.co for a in comp), Vector()) / len(comp); g = {'x': c.x, 'y': c.z, 'z': -c.y}
        ok = lambda L: all((g[k] > float(t)) if op == '>' else (g[k] < float(t)) for k, op, t in L)
        if not ok(S['cond']) or (S['no'] and ok(S['no'])): drop += comp
    bmesh.ops.delete(bm, geom=drop, context='VERTS'); bm.to_mesh(q.data); bm.free()
    if not q.data.polygons: bpy.data.objects.remove(q); return None
    return q
outs = []
for name, S in SETS.items():
    objs = [q for q in (pick(o, S) for n, o in sorted(parts.items()) if (S['ids'] is None or n in S['ids']) and n not in S['ex']) if q]
    for q in bpy.data.objects: q.select_set(False)
    for q in objs: q.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]; bpy.ops.object.join(); o = objs[0]; o.name = o.data.name = name
    vs = [v.co for v in o.data.vertices]; c = Vector([(min(p[i] for p in vs) + max(p[i] for p in vs)) / 2 for i in range(3)])
    for v in o.data.vertices: v.co -= c
    o.location = (0, 0, 0); o['center'] = json.dumps([round(c.x, 4), round(c.z, 4), round(-c.y, 4)])   # glTF coords (y up, +z front)
    size = [round(max(p[i] for p in vs) - min(p[i] for p in vs), 4) for i in (0, 2, 1)]; o['size'] = json.dumps(size)
    print(name, len(o.data.polygons), 'faces, centre', o['center'], 'size', size); outs.append(o)
for q in list(bpy.data.objects):
    if q not in outs: bpy.data.objects.remove(q)
for q in bpy.data.objects: q.select_set(True)
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True, export_image_format='JPEG', export_jpeg_quality=86, export_animations=False, export_extras=True)
print('wrote', OUT)
