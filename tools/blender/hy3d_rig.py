# Rig a Tencent HY 3D model (hy3d.tencent.ai 3D Studio: one fused 500k mesh, PBR texture, no skeleton; its own bone binding timed out)
# for the same KayKit re-bind as tripo_rig.py (grind3d.html / pixmap.html rigTripo): bones carry the KayKit Rig_Medium names at THIS model's
# joints, heat weights solved on a voxel proxy, then fixes by region (everything above the neck = rigid head: helmet, wings, hair;
# the cape behind the body follows the spine, never the legs or arms), decimate to a game budget, 1024 textures, skinned GLB.
# Blender (not pip bpy): blender -b --python tools/blender/hy3d_rig.py -- <in.fbx> <out.glb> [model]
#   blender -b --python tools/blender/hy3d_rig.py -- art/incoming/human_sword/hy3d_raw/sword_textured_500k.fbx art/grind3d/hy3d_sword.glb sword
# Joints were read off grid renders (front / side) of the model. Game coords: y up, looks at +z, left hand +x, model units (0.98 tall).
import bpy, bmesh, sys, json
from mathutils import Vector
A = sys.argv[sys.argv.index('--') + 1:]; SRC, OUT = A[0], A[1]; MODEL = A[2] if len(A) > 2 else 'sword'
SC, VOXEL, TEX = 10, float(__import__("os").environ.get("VOXEL", .12)), 1024
MODELS = {
  # black-red winged swordsman (ChatGPT design sheet -> HY 3D multi-view front + back, 2026-11-25): chibi, arms hanging by the body, long cape
  'sword': dict(FACES=30000, NECK=.47, ARM_R=.075, LEG_R=.075, CAPE_Z=.035,
    J={'hips': (0, .23, .02), 'spine': (0, .30, .02), 'chest': (0, .38, .02), 'head': (0, .47, .01), 'top': (0, .95, 0),
       'upperarml': (.14, .44, .02), 'lowerarml': (.19, .35, .03), 'wristl': (.21, .28, .04), 'handl': (.212, .27, .04), 'handslotl': (.215, .23, .05),
       'upperarmr': (-.14, .44, .02), 'lowerarmr': (-.19, .35, .03), 'wristr': (-.21, .28, .04), 'handr': (-.212, .27, .04), 'handslotr': (-.215, .23, .05),
       'upperlegl': (.07, .22, .02), 'lowerlegl': (.08, .12, .03), 'footl': (.09, .045, .02), 'toesl': (.09, .0, .12),
       'upperlegr': (-.07, .22, .02), 'lowerlegr': (-.08, .12, .03), 'footr': (-.09, .045, .02), 'toesr': (-.09, .0, .12)}),
}
M = MODELS[MODEL]; J = M['J']
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=SRC)
ob = [o for o in bpy.data.objects if o.type == 'MESH'][0]
for o in list(bpy.data.objects):
    if o is not ob: bpy.data.objects.remove(o)
ob.parent = None; bpy.context.view_layer.objects.active = ob; ob.select_set(True)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
ob.scale = (SC, SC, SC); bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)   # heat weights fail on tiny models: work x10
me = ob.data
bm = bmesh.new(); bm.from_mesh(me); n0 = len(bm.verts); bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5); bm.to_mesh(me); bm.free(); print('joined seams', n0, '->', len(me.vertices))
mod = ob.modifiers.new('dec', 'DECIMATE'); mod.ratio = min(1, 90000 / len(me.polygons)); bpy.ops.object.modifier_apply(modifier='dec'); print('faces after decimate', len(me.polygons))

def G(x, y, z): return Vector((x, -z, y)) * SC   # game -> Blender (x10)
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
# weights from distance to each bone (Blender's heat solver failed on this fused, self-crossing mesh, even on a voxel proxy):
# each vertex takes its 2 nearest ALLOWED bones by 1/d^4; arm / leg bones are only allowed inside a capsule round that limb,
# everything above the neck is the rigid head (helmet, wings, hair), the cape behind the body follows the spine bones only
import numpy as np
am = ob.modifiers.new('rig', 'ARMATURE'); am.object = rig; ob.parent = rig
NECK = M['NECK']; DEF = [b[0] for b in BONES]; SEGS = {}
for n, tail, _ in BONES: SEGS[n] = (np.array(J['wrist' + n[-1]] if n in ('handl', 'handr') else J[n]), np.array(J[tail]))
P = np.array([(v.co.x, v.co.z, -v.co.y) for v in me.vertices]) / SC
def segd(a, b):
    ab = b - a; t = np.clip(((P - a) @ ab) / max(1e-9, ab @ ab), 0, 1); return np.linalg.norm(P - (a + t[:, None] * ab), axis=1)
D = np.stack([segd(*SEGS[n]) for n in DEF], 1)
ok = np.ones_like(D, bool); x, y, z = P[:, 0], P[:, 1], P[:, 2]
for side in 'lr':
    ac = np.min(np.stack([segd(np.array(J[a + side]), np.array(J[b + side])) for a, b in (('upperarm', 'lowerarm'), ('lowerarm', 'wrist'), ('wrist', 'handslot'))], 1), 1)
    lc = np.min(np.stack([segd(np.array(J[a + side]), np.array(J[b + side])) for a, b in (('upperleg', 'lowerleg'), ('lowerleg', 'foot'), ('foot', 'toes'))], 1), 1)
    for n in ('upperarm', 'lowerarm', 'hand'): ok[:, DEF.index(n + side)] &= ac < M['ARM_R']
    for n in ('upperleg', 'lowerleg', 'foot'): ok[:, DEF.index(n + side)] &= lc < M['LEG_R']
cape = (z < -M['CAPE_Z']) & (y < NECK)
for n in DEF:
    if n not in ('hips', 'spine', 'chest'): ok[cape, DEF.index(n)] = False
ok[:, DEF.index('head')] &= y > NECK - .03
W = np.where(ok, 1 / (D + .01) ** 4, 0); top2 = np.argsort(-W, 1)[:, :2]; W2 = np.take_along_axis(W, top2, 1); W2 /= W2.sum(1, keepdims=True) + 1e-12
hd = y > NECK + .03; groups = {n: ob.vertex_groups.new(name=n) for n in DEF}
for i in range(len(P)):
    if hd[i]: groups['head'].add([i], 1.0, 'REPLACE'); continue
    for k in range(2):
        if W2[i, k] > .01: groups[DEF[top2[i, k]]].add([i], float(W2[i, k]), 'REPLACE')
print('weights: head', int(hd.sum()), 'cape', int(cape.sum()), 'of', len(P))
for o in bpy.data.objects: o.select_set(False)
bpy.context.view_layer.objects.active = ob; ob.select_set(True)
d2 = ob.modifiers.new('dec2', 'DECIMATE'); d2.ratio = min(1, M['FACES'] / len(me.polygons)); bpy.ops.object.modifier_move_to_index(modifier='dec2', index=0)
bpy.ops.object.modifier_apply(modifier='dec2'); print('final faces', len(ob.data.polygons))
for m in ob.data.materials:
    if not m.use_nodes: continue
    for n in list(m.node_tree.nodes):
        if n.type == 'TEX_IMAGE' and n.image and 'metallic' in n.image.name.lower(): m.node_tree.nodes.remove(n)
    bsdf = m.node_tree.nodes.get('Principled BSDF')
    if bsdf: bsdf.inputs['Metallic'].default_value = 0
for im in list(bpy.data.images):
    if im.users == 0: bpy.data.images.remove(im); continue
    if im.size[0] > TEX: im.scale(TEX, TEX); print('texture', im.name, '->', TEX)
ob.name = 'body'
rig['joints'] = json.dumps({k: [round(c * SC, 4) for c in v] for k, v in J.items()})   # the game re-binds on these (glTF extras)
bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True); rig.select_set(True)
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True, export_image_format='JPEG', export_jpeg_quality=88, export_animations=False, export_extras=True)
print('wrote', OUT)
