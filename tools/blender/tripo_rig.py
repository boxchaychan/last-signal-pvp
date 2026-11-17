# Rig a static Tripo model (one fused mesh, no skeleton) for tribe3d.html: the owner's "tribal female warrior" (Tripo AI app, 2026-11-17).
# 1. joins the vertices Tripo split at texture seams (UVs stay per corner), 2. decimates to a game budget, 3. builds an armature whose bones
# carry the KayKit Rig_Medium names at HER joints, 4. automatic (heat) weights + fixes (bow -> left hand, braids / cape -> body),
# 5. textures down to 1024, 6. exports a skinned GLB. The game re-binds it onto a KayKit skeleton (see loadPeople: rigTripo) so every KayKit move plays.
# Joints were read off grid renders of the model (game coords: y up, she looks at +z, her left hand +x; model units, 0.97 tall).
#   pip install bpy ; python3 tools/blender/tripo_rig.py <in.glb> art/tribe3d/people/warrior_f.glb
import bpy, bmesh, sys, math
from mathutils import Vector
SRC, OUT = sys.argv[-2], sys.argv[-1]
DECIMATE, FACES, TEX, VOXEL, SC, BOW_X, ARM_R, LEG_R = .4, 24000, 1024, .06, 10, .2, .055, .075
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
ob = [o for o in bpy.data.objects if o.type == 'MESH'][0]
for o in bpy.data.objects:
    if o is not ob: bpy.data.objects.remove(o)
ob.parent = None
bpy.context.view_layer.objects.active = ob; ob.select_set(True)
ob.scale = (SC, SC, SC)   # Blender's heat weighting fails on tiny models (she is under 1 unit tall): work x10, the game rescales anyway
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
me = ob.data
# the bow + string: whole texture islands (Tripo keeps the bow's islands apart from the body's) found by where they sit; they will follow the
# left hand rigidly (heat weights alone tear the bow between the hand and the leg)
def is_bow(cx, cy, cz, mxx, zs, rgb):   # where her bow lies (rest pose, left side; the boot wing ends at x .1, the skirt at .145)
    if cz < -.06: return False   # behind her
    string = cx > .1 and min(zs) > .04 and max(zs) - min(zs) < .02 and rgb[2] > rgb[0] + .15   # the thin blue string
    return cx > BOW_X or (cy < .22 and cx > .105) or (cy < .42 and cx > .145) or string   # limbs, tips, string
img = [i for i in bpy.data.images if 'olor' in i.name][0]; TW_, TH_ = img.size; TPX = img.pixels[:]
def texcol(u, v):
    x = min(TW_ - 1, max(0, int(u * TW_))); y = min(TH_ - 1, max(0, int(v * TH_))); i = (y * TW_ + x) * 4; return TPX[i:i + 3]
bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table(); uvl = bm.loops.layers.uv.active; seen = set(); bow = []; hood = []
for v in bm.verts:
    if v.index in seen: continue
    stack = [v]; seen.add(v.index); ids = []
    while stack:
        a = stack.pop(); ids.append(a.index)
        for e in a.link_edges:
            b = e.other_vert(a)
            if b.index not in seen: seen.add(b.index); stack.append(b)
    g = [(bm.verts[i].co.x / SC, bm.verts[i].co.z / SC, -bm.verts[i].co.y / SC) for i in ids]
    cx, cy, cz = (sum(q[k] for q in g) / len(g) for k in range(3)); zs = [q[2] for q in g]; mxx = max(q[0] for q in g)
    cs = [texcol(*bm.verts[i].link_loops[0][uvl].uv) for i in ids[:150] if bm.verts[i].link_loops]; rgb = [sum(q[k] for q in cs) / max(1, len(cs)) for k in range(3)]
    if is_bow(cx, cy, cz, mxx, zs, rgb): bow += ids
    elif cy > .58 and abs(cx + .03) > .17: hood += ids   # feathers / gold discs hanging off the hood: with the head
bm.free(); vg = ob.vertex_groups.new(name='bowsel'); vg.add(bow, 1.0, 'REPLACE'); vg = ob.vertex_groups.new(name='hoodsel'); vg.add(hood, 1.0, 'REPLACE')
print('bow vertices', len(bow), 'hood ornaments', len(hood))
bm = bmesh.new(); bm.from_mesh(me); n0 = len(bm.verts)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5); bm.to_mesh(me); bm.free(); print('joined seams', n0, '->', len(me.vertices))
mod = ob.modifiers.new('dec', 'DECIMATE'); mod.ratio = DECIMATE; bpy.ops.object.modifier_apply(modifier='dec'); print('faces after decimate', len(me.polygons))

def G(x, y, z): return Vector((x, -z, y)) * SC   # game (model units) -> Blender (x10)
J = {   # her joints (game coords, model units)
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
arm = bpy.data.armatures.new('rig'); rig = bpy.data.objects.new('rig', arm); bpy.context.collection.objects.link(rig)
bpy.context.view_layer.objects.active = rig; bpy.ops.object.mode_set(mode='EDIT')
for name, tail, parent in BONES:
    b = arm.edit_bones.new(name); b.head = G(*J[name]); t = G(*J[tail])
    if name in ('handl', 'handr'): b.head = G(*J['wrist' + name[-1]])
    if (t - b.head).length < 1e-2: t = b.head + Vector((0, 0, .3))
    b.tail = t
for name, tail, parent in BONES:
    if parent: arm.edit_bones[name].parent = arm.edit_bones[parent]
bpy.ops.object.mode_set(mode='OBJECT')
# heat weights fail on Tripo's fused, self-crossing mesh, so they are solved on a clean watertight PROXY (voxel remesh of a copy)
# and copied to the real mesh by nearest-surface interpolation
px = ob.copy(); px.data = ob.data.copy(); px.name = 'proxy'; bpy.context.collection.objects.link(px); px.vertex_groups.clear()
for o in bpy.data.objects: o.select_set(False)
bpy.context.view_layer.objects.active = px; px.select_set(True)
r = px.modifiers.new('rm', 'REMESH'); r.mode = 'VOXEL'; r.voxel_size = VOXEL; bpy.ops.object.modifier_apply(modifier='rm')
d = px.modifiers.new('dec', 'DECIMATE'); d.ratio = min(1, 40000 / max(1, len(px.data.polygons))); bpy.ops.object.modifier_apply(modifier='dec')
print('proxy faces', len(px.data.polygons))
for o in bpy.data.objects: o.select_set(False)
px.select_set(True); rig.select_set(True); bpy.context.view_layer.objects.active = rig
bpy.ops.object.parent_set(type='ARMATURE_AUTO')
print('proxy unweighted', sum(1 for v in px.data.vertices if not v.groups), 'of', len(px.data.vertices))
for vg in px.vertex_groups:
    if vg.name not in ob.vertex_groups: ob.vertex_groups.new(name=vg.name)
for o in bpy.data.objects: o.select_set(False)
bpy.context.view_layer.objects.active = ob; ob.select_set(True)
dt = ob.modifiers.new('dt', 'DATA_TRANSFER'); dt.object = px; dt.use_vert_data = True; dt.data_types_verts = {'VGROUP_WEIGHTS'}
dt.vert_mapping = 'POLYINTERP_NEAREST'; dt.layers_vgroup_select_src = 'ALL'; dt.layers_vgroup_select_dst = 'NAME'
bpy.ops.object.modifier_apply(modifier='dt')
bpy.data.objects.remove(px)
am = ob.modifiers.new('rig', 'ARMATURE'); am.object = rig; ob.parent = rig
groups = {vg.name: vg for vg in ob.vertex_groups}
print('groups', sorted(groups))
def gpos(v): c = v.co / SC; return (c.x, c.z, -c.y)   # Blender -> game (model units)
def setonly(v, name, mix=1.0):
    """move the weight of vertex v toward bone `name` (mix 1 = only that bone)"""
    ws = {g.group: g.weight for g in v.groups}; tot = sum(ws.values()) or 1
    for gi in list(ws): ws[gi] = ws[gi] / tot * (1 - mix)
    gi = groups[name].index; ws[gi] = ws.get(gi, 0) + mix
    for vg in ob.vertex_groups:
        w = ws.get(vg.index, 0)
        if w > 1e-4: vg.add([v.index], w, 'REPLACE')
        else: vg.remove([v.index])
def seg_dist(p, pts):
    best = 9
    for a, b in zip(pts, pts[1:]):
        a, b, q = Vector(a), Vector(b), Vector(p); ab = b - a; t = max(0, min(1, (q - a).dot(ab) / max(1e-9, ab.dot(ab)))); best = min(best, (q - (a + ab * t)).length)
    return best
def name_w(v, names): return sum(g.weight for g in v.groups if ob.vertex_groups[g.group].name in names)
def drop(v, names):
    for n in names: groups[n].remove([v.index])
fix = {'bow': 0, 'hood': 0, 'braid': 0, 'limb': 0, 'none': 0}; bi, hi = groups['bowsel'].index, groups['hoodsel'].index
for v in me.vertices:
    x, y, z = gpos(v)
    if any(g.group == bi and g.weight > .5 for g in v.groups): setonly(v, 'handl'); fix['bow'] += 1; continue   # the bow moves with her left hand, rigid
    if any(g.group == hi and g.weight > .5 for g in v.groups): setonly(v, 'head'); fix['hood'] += 1; continue
    # an arm / leg bone only moves what is really ON that limb (a capsule round its joints): the cape flap by her right hand, braids and
    # skirt edges stay with the body instead of being dragged (heat weights spill onto anything close)
    for side in 'lr':
        for limb, R in (('arm', ARM_R), ('leg', LEG_R)):
            names = [n + side for n in (('upperarm', 'lowerarm', 'hand') if limb == 'arm' else ('upperleg', 'lowerleg', 'foot'))]
            if limb == 'arm' and name_w(v, names) > 0 and seg_dist((x, y, z), [J[n + side] for n in ('upperarm', 'lowerarm', 'wrist', 'handslot')]) > R: drop(v, names); fix['limb'] += 1
            if limb == 'leg' and name_w(v, names) > 0 and seg_dist((x, y, z), [J[n + side] for n in ('upperleg', 'lowerleg', 'foot', 'toes')]) > R: drop(v, names); fix['limb'] += 1
    if not [g for g in v.groups if g.group not in (bi, hi) and g.weight > 1e-4]: setonly(v, 'chest' if y > .5 else 'spine' if y > .42 else 'hips'); fix['none'] += 1; continue
    if abs(x - (-.03)) > .15 and y > .38 and z < -.015:   # braids and the cape behind the arms: with the body, not the arms
        setonly(v, 'head' if y > .62 else 'chest', .9 if y > .45 else .75); fix['braid'] += 1
print('fixes', fix); ob.vertex_groups.remove(groups['bowsel']); ob.vertex_groups.remove(groups['hoodsel'])
# the heat solve only works on the proxy made from the 40% mesh, so the game budget comes from a SECOND decimate here (weights interpolate)
for o in bpy.data.objects: o.select_set(False)
bpy.context.view_layer.objects.active = ob; ob.select_set(True)
d2 = ob.modifiers.new('dec2', 'DECIMATE'); d2.ratio = min(1, FACES / len(me.polygons)); bpy.ops.object.modifier_move_to_index(modifier='dec2', index=0)
bpy.ops.object.modifier_apply(modifier='dec2'); print('final faces', len(ob.data.polygons))
# smaller textures (the game shows her ~100 px tall); no metal / roughness map (without an environment map metal reads black)
for m in ob.data.materials:
    for n in list(m.node_tree.nodes):
        if n.type == 'TEX_IMAGE' and n.image and 'metallic' in n.image.name.lower(): m.node_tree.nodes.remove(n)
    bsdf = m.node_tree.nodes.get('Principled BSDF')
    if bsdf: bsdf.inputs['Metallic'].default_value = 0; bsdf.inputs['Roughness'].default_value = .65
for im in list(bpy.data.images):
    if im.users == 0: bpy.data.images.remove(im); continue
    if im.size[0] > TEX: im.scale(TEX, TEX); print('texture', im.name, '->', TEX)
import json
rig['joints'] = json.dumps({k: [round(c * SC, 4) for c in v] for k, v in J.items()})   # the game re-binds on these (glTF extras)
bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True); rig.select_set(True)
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True, export_image_format='JPEG', export_jpeg_quality=88, export_animations=False, export_extras=True)
print('wrote', OUT)
