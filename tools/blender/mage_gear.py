# Gear for the "หมอผี ★★" (2-star shaman) of tribe3d.html, modelled in Blender by script (headless, cloud session), so the
# upgraded shaman looks clearly stronger than the ★ one (owner 2026-11-16: the first ★★ shaman looked weaker):
#   HatStar = a gold five-point star with a glowing gem, for the front of the hat (faces +Z in the game)
#   Crystal = a cluster of glowing violet crystals in a gold ring, for the staff head
#   Collar  = a gold mantle collar with points, round the neck (lies flat)
# Modelled Z-up (Blender) so it arrives Y-up in glTF; sizes in KayKit character units (a character is 2.4 tall).
# Materials whose name starts with "glow" are drawn unlit (glowing) by the game.
#   pip install bpy ; python3 tools/blender/mage_gear.py art/tribe3d/gear/mage_gear.glb
import bpy, bmesh, math, sys
from mathutils import Vector
OUT = sys.argv[-1] if sys.argv[-1].endswith('.glb') else 'art/tribe3d/gear/mage_gear.glb'
bpy.ops.wm.read_factory_settings(use_empty=True)
def lin(h):
    c = [((h >> s) & 255) / 255 for s in (16, 8, 0)]
    return tuple(v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in c)
def mat(name, h, rough=.5, metal=0.):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*lin(h), 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal; return m
GOLD, GOLD2, GEM, CRY, CRY2 = mat('gold', 0xffcf3a, .3, .7), mat('gold_dark', 0xc08a1a, .4, .6), mat('glow_gem', 0x6af0ff), mat('glow_crystal', 0xc07aff), mat('glow_crystal2', 0xff9ae8)
def obj(name):
    me = bpy.data.meshes.new(name); ob = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(ob); return ob, me
def finish(me, bm, mats):
    for m in mats: me.materials.append(m)
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = False

# ---------- star (in the XZ plane, thickness along Y; front = -Y in Blender = +Z in the game)
ob, me = obj('HatStar'); bm = bmesh.new()
R1, R2, T = .2, .085, .05
ring = [Vector((math.sin(i / 10 * 6.283) * (R1 if i % 2 == 0 else R2), 0, math.cos(i / 10 * 6.283) * (R1 if i % 2 == 0 else R2))) for i in range(10)]
front = [bm.verts.new(p + Vector((0, -T, 0))) for p in ring]; back = [bm.verts.new(p + Vector((0, T, 0))) for p in ring]
cf = bm.verts.new((0, -T * 2.2, 0)); cb = bm.verts.new((0, T * 1.4, 0))
for i in range(10):
    j = (i + 1) % 10
    bm.faces.new((front[i], front[j], cf)); bm.faces.new((back[j], back[i], cb)); bm.faces.new((front[j], front[i], back[i], back[j]))
gem = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=.055)
for v in gem['verts']: v.co += Vector((0, -T * 2.4, 0))
for f in {f for v in gem['verts'] for f in v.link_faces}: f.material_index = 1
finish(me, bm, [GOLD, GEM])

# ---------- crystal cluster in a gold ring (stands up along Z)
ob, me = obj('Crystal'); bm = bmesh.new()
def crystal(bm, base, axis, length, r, mi):
    axis = Vector(axis).normalized(); side = axis.cross(Vector((1, 0, 0))) if abs(axis.x) < .9 else axis.cross(Vector((0, 1, 0))); side.normalize(); s2 = axis.cross(side)
    mid = [bm.verts.new(Vector(base) + axis * length * .35 + (side * math.cos(a) + s2 * math.sin(a)) * r) for a in [k / 6 * 6.283 for k in range(6)]]
    top = bm.verts.new(Vector(base) + axis * length); bot = bm.verts.new(Vector(base) - axis * length * .15)
    for i in range(6):
        j = (i + 1) % 6; f = bm.faces.new((mid[i], mid[j], top)); f.material_index = mi; g = bm.faces.new((mid[j], mid[i], bot)); g.material_index = mi
crystal(bm, (0, 0, 0), (0, 0, 1), .42, .09, 1)
crystal(bm, (.05, .02, -.02), (.5, .2, 1), .28, .06, 2)
crystal(bm, (-.05, -.03, -.02), (-.45, -.3, 1), .26, .055, 1)
crystal(bm, (.0, -.05, -.03), (.1, -.6, 1), .22, .05, 2)
tor = bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=.13, radius2=.16, depth=.07)
for v in tor['verts']: v.co += Vector((0, 0, -.02))
for f in {f for v in tor['verts'] for f in v.link_faces}: f.material_index = 0
finish(me, bm, [GOLD, CRY, CRY2])

# ---------- gold collar (flat ring of points round the neck, centre = neck)
ob, me = obj('Collar'); bm = bmesh.new()
N = 14; inner, outer = .26, .4
for i in range(N):
    a0, a1, am = i / N * 6.283, (i + 1) / N * 6.283, (i + .5) / N * 6.283
    v = [bm.verts.new((math.cos(a0) * inner, math.sin(a0) * inner, 0)), bm.verts.new((math.cos(a1) * inner, math.sin(a1) * inner, 0)),
         bm.verts.new((math.cos(am) * outer, math.sin(am) * outer, -.07)), bm.verts.new((math.cos(a0) * inner, math.sin(a0) * inner, .06)), bm.verts.new((math.cos(a1) * inner, math.sin(a1) * inner, .06))]
    f = bm.faces.new((v[0], v[2], v[1])); f.material_index = i % 2; g = bm.faces.new((v[3], v[4], v[2])); g.material_index = i % 2
    h = bm.faces.new((v[0], v[3], v[2])); h.material_index = 1; k = bm.faces.new((v[1], v[2], v[4])); k.material_index = 1
for a in (0, 2.09, 4.19):   # three gems on the collar
    gm = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=.04)
    for vv in gm['verts']: vv.co += Vector((math.cos(a + 1.57) * .34, math.sin(a + 1.57) * .34, .0))
    for f in {f for vv in gm['verts'] for f in vv.link_faces}: f.material_index = 2
finish(me, bm, [GOLD, GOLD2, GEM])

bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', export_apply=True)
print('wrote', OUT, [o.name for o in bpy.data.objects])
