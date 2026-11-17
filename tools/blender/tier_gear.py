# Silhouette pieces for the ★★ / ★★★ units of tribe3d.html (owner 2026-11-17: "ทรงมันดูไม่ต่างเลย ... ให้มันดีกว่าเปลี่ยนสี เพิ่มรายละเอียด"):
# shapes that change the outline seen from the game camera, not only colours. Modelled Z-up (Blender) -> Y-up glTF, front = -Y
# (= +Z in the game, where the characters look). Sizes in character units (a 2.0 hero is ~2.4 tall). "glow*" materials = unlit.
#   PauldronA  round gold-rimmed shoulder plate (★★ warrior)      PauldronB  big spiked shoulder plate (★★★ warrior)
#   HelmWing   feather wing for the helmet side (★★★ warrior)      Banner     back banner on a pole (★★★ warrior)
#   Mantle     feather shoulder mantle (★★ / ★★★ archer)           Antlers    antler crown (★★★ archer)
#   Halo       sun disc behind the head (★★ shaman)               HaloB      bigger glowing rune ring (★★★ shaman)
#   Orbit      three crystals on a ring, spun by the game (★★★ shaman)
#   pip install bpy ; python3 tools/blender/tier_gear.py art/tribe3d/gear/tier_gear.glb
import bpy, bmesh, math, sys
from mathutils import Vector, Matrix
OUT = sys.argv[-1] if sys.argv[-1].endswith('.glb') else 'art/tribe3d/gear/tier_gear.glb'
bpy.ops.wm.read_factory_settings(use_empty=True)
def lin(h):
    c = [((h >> s) & 255) / 255 for s in (16, 8, 0)]
    return tuple(v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in c)
def mat(name, h):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (*lin(h), 1); return m
STEEL, STEEL2, GOLD, RED, RED2, WOOD = mat('steel', 0xc8ccd4), mat('steel_dark', 0x6a6e7a), mat('gold', 0xffc83a), mat('cloth_red', 0xc8202a), mat('cloth_red2', 0x8a1018), mat('wood', 0x7a4a24)
FEA1, FEA2, FEA3, BONE = mat('feather_green', 0x3a8a3a), mat('feather_brown', 0x8a5a2a), mat('feather_white', 0xf4ecd8), mat('bone', 0xe8dcc0)
WHITE, GLOWG, GLOWC, GLOWV = mat('wing_white', 0xf6f2ea), mat('glow_gold', 0xffd860), mat('glow_cyan', 0x5af0ff), mat('glow_violet', 0xc890ff)
def obj(name):
    me = bpy.data.meshes.new(name); ob = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(ob); return ob, me
def fin(me, bm, mats):
    for m in mats: me.materials.append(m)
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = False
def setmi(geom, mi):
    for f in {f for v in geom['verts'] for f in v.link_faces}: f.material_index = mi
def xform(geom, M):
    for v in geom['verts']: v.co = M @ v.co
def tube(bm, pts, radii, sides, mi):
    rings = []
    for i, p in enumerate(pts):
        t = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized(); a = Vector((1, 0, 0)) if abs(t.x) < .9 else Vector((0, 1, 0)); u = t.cross(a).normalized(); w = t.cross(u)
        rings.append([bm.verts.new(p + (u * math.cos(k / sides * 6.283) + w * math.sin(k / sides * 6.283)) * radii[i]) for k in range(sides)])
    for r0, r1 in zip(rings, rings[1:]):
        for k in range(sides): f = bm.faces.new((r0[k], r0[(k + 1) % sides], r1[(k + 1) % sides], r1[k])); f.material_index = mi
    for r, flip in ((rings[0], True), (rings[-1], False)): f = bm.faces.new(list(reversed(r)) if flip else r); f.material_index = mi
def cone(bm, base, tip_dir, length, r, mi, seg=5):
    g = bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=0, depth=length); xform(g, Matrix.Translation((0, 0, length / 2)))
    d = Vector(tip_dir).normalized(); q = Vector((0, 0, 1)).rotation_difference(d); xform(g, Matrix.Translation(base) @ q.to_matrix().to_4x4()); setmi(g, mi)
def feather(bm, base, direction, length, width, mi, droop=.1):
    d = Vector(direction).normalized(); side = d.cross(Vector((0, 0, 1))); side = side.normalized() if side.length > .01 else Vector((1, 0, 0))
    sp = [Vector(base) + d * length * t + Vector((0, 0, -droop * t * t)) for t in (0, .3, .65, 1)]; wd = [width * .3, width, width * .8, 0]
    L = [bm.verts.new(p - side * w) for p, w in zip(sp, wd)]; R = [bm.verts.new(p + side * w) for p, w in zip(sp, wd)]
    for i in range(3):
        f = bm.faces.new((L[i], L[i + 1], R[i + 1], R[i]) if i < 2 else (L[2], L[3], R[2])); f.material_index = mi

# ---------- pauldrons (dome along +Z, centred on the shoulder; the game tilts them outward)
for name, R, spikes in (('PauldronA', .3, 0), ('PauldronB', .38, 3)):
    ob, me = obj(name); bm = bmesh.new()
    d = bmesh.ops.create_uvsphere(bm, u_segments=10, v_segments=6, radius=R)
    for v in list(d['verts']):
        if v.co.z < -.02: v.co.z = -.02
        v.co.z *= .7
    setmi(d, 0)
    rim = bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=R * 1.08, radius2=R * 1.08, depth=.06); setmi(rim, 1)
    for k in range(spikes): a = (k - 1) * .55; cone(bm, (math.sin(a) * R * .55, -math.cos(a) * R * .1, R * .45), (math.sin(a) * .9, 0, 1), .32, .07, 2)
    fin(me, bm, [STEEL, GOLD, STEEL2])
# ---------- helmet wing (flat fan in the x = 0 plane, pointing up and back)
ob, me = obj('HelmWing'); bm = bmesh.new()
for k in range(5): a = .25 + k * .22; feather(bm, (0, 0, 0), (0, math.sin(a) * .9, math.cos(a)), .55 - k * .05, .07, 0 if k % 2 == 0 else 1, .02)
fin(me, bm, [WHITE, GOLD])
# ---------- back banner: pole along +Z, flag to the side, gold tip
ob, me = obj('Banner'); bm = bmesh.new()
tube(bm, [Vector((0, 0, 0)), Vector((0, 0, 2.1))], [.035, .035], 6, 0)
cone(bm, (0, 0, 2.1), (0, 0, 1), .22, .06, 1)
tube(bm, [Vector((-.02, 0, 1.95)), Vector((.62, 0, 1.95))], [.025, .025], 5, 0)
fl = [Vector((0, 0, 1.92)), Vector((.6, 0, 1.92)), Vector((.6, 0, 1.2)), Vector((.3, 0, 1.05)), Vector((0, 0, 1.2))]
for side in (-.012, .012):
    vs = [bm.verts.new(p + Vector((0, side, 0))) for p in fl]; f = bm.faces.new(vs if side < 0 else list(reversed(vs))); f.material_index = 2
for side in (-.02, .02):   # gold stripe
    vs = [bm.verts.new(Vector((x, side, z))) for x, z in ((.05, 1.62), (.55, 1.62), (.55, 1.52), (.05, 1.52))]; f = bm.faces.new(vs if side < 0 else list(reversed(vs))); f.material_index = 1
fin(me, bm, [WOOD, GOLD, RED])
# ---------- feather mantle: feathers fanned round the neck, splayed outward and down
ob, me = obj('Mantle'); bm = bmesh.new()
N = 14
for k in range(N):
    a = k / N * 6.283
    if abs(math.sin(a)) > .9 and math.cos(a) < 0: pass
    feather(bm, (math.sin(a) * .22, -math.cos(a) * .22, 0), (math.sin(a), -math.cos(a), -.45), .42, .08, k % 3, .05)
fin(me, bm, [FEA1, FEA2, FEA3])
# ---------- antler crown (two branching antlers, symmetric)
ob, me = obj('Antlers'); bm = bmesh.new()
for sx in (1, -1):
    b0 = Vector((sx * .18, 0, 0)); m1 = Vector((sx * .38, .05, .32)); t1 = Vector((sx * .5, .12, .62))
    tube(bm, [b0, m1, t1], [.045, .035, .02], 5, 0)
    tube(bm, [m1, Vector((sx * .28, -.05, .55))], [.03, .015], 4, 0)
    tube(bm, [Vector((sx * .44, .09, .48)), Vector((sx * .68, .05, .62))], [.025, .012], 4, 0)
    tube(bm, [Vector((sx * .3, .03, .2)), Vector((sx * .5, -.02, .28))], [.025, .012], 4, 0)
band = bmesh.ops.create_cone(bm, cap_ends=False, segments=10, radius1=.24, radius2=.22, depth=.06); setmi(band, 1)
fin(me, bm, [BONE, GOLD])
# ---------- halos (vertical ring in the XZ plane = faces the front)
for name, R, M2, rays in (('Halo', .42, GLOWG, 12), ('HaloB', .55, GLOWC, 16)):
    ob, me = obj(name); bm = bmesh.new(); N2 = 24
    inner = [bm.verts.new((math.cos(k / N2 * 6.283) * R * .8, 0, math.sin(k / N2 * 6.283) * R * .8)) for k in range(N2)]
    outer = [bm.verts.new((math.cos(k / N2 * 6.283) * R, 0, math.sin(k / N2 * 6.283) * R)) for k in range(N2)]
    for k in range(N2): j = (k + 1) % N2; bm.faces.new((inner[k], inner[j], outer[j], outer[k]))
    for k in range(rays):
        a = k / rays * 6.283; c, s = math.cos(a), math.sin(a); w = .05
        v1 = bm.verts.new((c * R, 0, s * R)); v2 = bm.verts.new((c * R * 1.28, 0, s * R * 1.28)); v3 = bm.verts.new((c * R - s * w, 0, s * R + c * w)); bm.faces.new((v3, v1, v2))
    for f in bm.faces: f.material_index = 0
    fin(me, bm, [M2])
# ---------- orbit: three crystals on a ring (the game spins this object)
ob, me = obj('Orbit'); bm = bmesh.new()
for k in range(3):
    a = k / 3 * 6.283; c = Vector((math.cos(a) * .95, math.sin(a) * .95, 0))
    g = bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=.1, radius2=0, depth=.32); xform(g, Matrix.Translation(c + Vector((0, 0, .16)))); setmi(g, k % 2)
    g = bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=.1, radius2=0, depth=.2); xform(g, Matrix.Translation(c - Vector((0, 0, .1))) @ Matrix.Rotation(math.pi, 4, 'X')); setmi(g, k % 2)
fin(me, bm, [GLOWC, GLOWV])
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', export_apply=True)
print('wrote', OUT, sorted(o.name for o in bpy.data.objects))
