# Pieces of the red-scarf hero of tribe3d.html (owner's design picture 2026-11-17, art/incoming/tribe3d/hero_ref.png), on the KayKit
# Knight body (tools/art/hero_build.mjs). Fitted to that body: the script loads Knight.glb and casts rays at its head / body, so the hair,
# headband and scarf sit on the surface. Modelled Z-up -> Y-up glTF; G(x, y, z) takes GAME coordinates (bind pose, y up, the hero looks
# at +z). The body pieces are in the hero's root space (the game attaches them to a bone keeping their place); the sword is in the
# right-hand slot's space (blade along +y, like the KayKit swords). "glow*" materials are drawn unlit by the game.
#   HeroHair  spiky anime hair      HeroBand  red headband + knot tails     HeroScarf  red scarf, tails flying back
#   HeroPad   steel shoulder pad with gold rims (dome along +Z, placed like PauldronA)     HeroBadge  gold chevron on the chest
#   HeroPouch belt pouch            RuneBlade dark broad sword, gold guard, red glowing runes
#   pip install bpy ; python3 tools/blender/hero_gear.py art/incoming/kaykit/adventurers_2.0/characters/Knight.glb art/tribe3d/gear/hero_gear.glb
import bpy, bmesh, math, sys
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
KNIGHT, OUT = sys.argv[-2], sys.argv[-1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=KNIGHT)
def bvh_of(names):
    V, P = [], []
    for ob in bpy.data.objects:
        if ob.type != 'MESH' or ob.name.split('.')[0] not in names: continue
        b = len(V); V += [ob.matrix_world @ v.co for v in ob.data.vertices]; P += [[b + i for i in p.vertices] for p in ob.data.polygons]
    return BVHTree.FromPolygons(V, P)
HEAD, BODY = bvh_of(['Knight_Head']), bvh_of(['Knight_Body'])
for ob in list(bpy.data.objects): bpy.data.objects.remove(ob)
def G(x, y, z): return Vector((x, -z, y))   # game -> Blender
def hit(tree, o, d, push=0):
    loc, n, i, dist = tree.ray_cast(o, d.normalized())
    return (loc + d.normalized() * push) if loc else None
def lin(h):
    c = [((h >> s) & 255) / 255 for s in (16, 8, 0)]
    return tuple(v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in c)
def mat(name, h):
    m = bpy.data.materials.new(name); m.use_nodes = True; m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (*lin(h), 1); return m
HAIR, HAIR_D, HAIR_L = mat('hair', 0x7c3520), mat('hair_dark', 0x521f10), mat('hair_light', 0x96462a)
RED, RED_D = mat('cloth_red', 0xd8222c), mat('cloth_red2', 0x8e1420)
STEEL, STEEL_D, GOLD, GOLD_D = mat('steel', 0x8a909c), mat('steel_dark', 0x5a5e6a), mat('gold', 0xffc43a), mat('gold_dark', 0xc88a1c)
LEATH, BLADE, EDGE, GRIP, GLOWR = mat('leather', 0x6a3e24), mat('blade', 0x2c2630), mat('blade_edge', 0xd4d8e0), mat('grip', 0x3a2420), mat('glow_red', 0xff2638)
def obj(name):
    me = bpy.data.meshes.new(name); ob = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(ob); return ob, me
def fin(me, bm, mats, smooth=False):
    for m in mats: me.materials.append(m)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = smooth   # hair / cloth smooth (soft like the owner's picture), metal flat
def setmi(geom, mi):
    for f in {f for v in geom['verts'] for f in v.link_faces}: f.material_index = mi
def xform(geom, M):
    for v in geom['verts']: v.co = M @ v.co
def tube(bm, pts, radii, sides, mi, flat=1.0, up=None):
    """a tube through pts; flat < 1 squashes the section along `up` (a world vector) -> a blade-like spike"""
    rings = []
    for i, p in enumerate(pts):
        t = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        a = up if up is not None and t.cross(up).length > .3 else (Vector((1, 0, 0)) if abs(t.x) < .9 else Vector((0, 1, 0)))
        u = t.cross(a).normalized(); w = t.cross(u)
        rings.append([bm.verts.new(p + (u * math.cos(k / sides * 6.283) + w * math.sin(k / sides * 6.283) * flat) * radii[i]) for k in range(sides)])
    for r0, r1 in zip(rings, rings[1:]):
        for k in range(sides): f = bm.faces.new((r0[k], r0[(k + 1) % sides], r1[(k + 1) % sides], r1[k])); f.material_index = mi
    for r, flip in ((rings[0], True), (rings[-1], False)): f = bm.faces.new(list(reversed(r)) if flip else r); f.material_index = mi
def slab(bm, pts2d, origin, ax, ay, az, depth, mi):
    """a flat polygon (2-D points in the ax / ay plane) extruded along az by depth (centred)"""
    top = [bm.verts.new(origin + ax * x + ay * y + az * depth / 2) for x, y in pts2d]
    bot = [bm.verts.new(origin + ax * x + ay * y - az * depth / 2) for x, y in pts2d]
    f = bm.faces.new(top); f.material_index = mi; f = bm.faces.new(list(reversed(bot))); f.material_index = mi
    n = len(pts2d)
    for k in range(n): f = bm.faces.new((bot[k], bot[(k + 1) % n], top[(k + 1) % n], top[k])); f.material_index = mi
def ribbon(bm, pts, widths, side, thick, mi, fork=0):
    """a cloth strip along pts (width along `side`), with thickness; fork > 0 = torn two-point end"""
    sv = [Vector(side).normalized()] * len(pts)
    L = [p - s * w for p, s, w in zip(pts, sv, widths)]; R = [p + s * w for p, s, w in zip(pts, sv, widths)]
    for off, flip in ((thick / 2, False), (-thick / 2, True)):
        nrm = (pts[1] - pts[0]).cross(sv[0]).normalized() * off
        l = [bm.verts.new(v + nrm) for v in L]; r = [bm.verts.new(v + nrm) for v in R]
        for i in range(len(pts) - 1):
            q = (l[i], l[i + 1], r[i + 1], r[i]); f = bm.faces.new(tuple(reversed(q)) if flip else q); f.material_index = mi
        if fork:
            m = bm.verts.new((L[-1] + R[-1]) / 2 + (pts[-1] - pts[-2]).normalized() * -fork + nrm)
            t1 = bm.verts.new(L[-1] + (pts[-1] - pts[-2]).normalized() * fork + nrm); t2 = bm.verts.new(R[-1] + (pts[-1] - pts[-2]).normalized() * fork * .6 + nrm)
            for q in ((l[-1], t1, m), (m, t2, r[-1]), (l[-1], m, r[-1])):
                f = bm.faces.new(tuple(reversed(q)) if flip else q); f.material_index = mi

# ---------- spiky hair: curved, slightly flat spikes rooted on the Knight's head (rays from the head centre)
ob, me = obj('HeroHair'); bm = bmesh.new()
C = G(0, 1.8, 0.02)
SPIKES = [   # aim (where the root is), grow direction, length, root radius, material (0 mid, 1 dark under-layer, 2 light top), curl (bend of the tip, game coords)
    # owner's picture: one soft mass of thick clumps (not needles), sweeping up and back
    ((0, 1, .1), (0, 1, -.2), .22, .34, 0, (0, -.2, -.3)), ((-.4, 1, -.2), (-.4, .8, -.4), .2, .32, 0, (0, -.2, -.3)), ((.4, 1, -.2), (.4, .8, -.4), .2, .32, 0, (0, -.2, -.3)),   # volume
    ((0, 1, .25), (.2, 1, -.05), .42, .27, 2, (.3, -.2, -.3)), ((-.38, 1, .02), (-.7, .8, -.15), .4, .26, 0, (-.2, -.4, -.2)), ((.4, 1, -.04), (.75, .75, -.2), .4, .26, 2, (.2, -.4, -.2)),
    ((0, 1, -.4), (0, .65, -.85), .46, .28, 0, (0, -.4, -.3)), ((-.25, .95, -.2), (-.35, .85, -.6), .38, .24, 0, (0, -.3, -.3)), ((.22, .95, -.25), (.3, .85, -.6), .38, .24, 0, (0, -.3, -.3)),
    ((-1, .5, .05), (-1, .25, -.1), .34, .25, 0, (0, -.4, -.2)), ((1, .5, .05), (1, .25, -.1), .34, .25, 0, (0, -.4, -.2)),
    ((-.9, .7, -.45), (-.85, .3, -.7), .36, .25, 1, (0, -.4, 0)), ((.9, .7, -.45), (.85, .3, -.7), .36, .25, 1, (0, -.4, 0)),
    ((0, .35, -1), (0, -.05, -1), .38, .27, 1, (0, -.4, 0)), ((-.45, .1, -.9), (-.4, -.5, -.8), .3, .23, 1, (0, -.2, 0)), ((.45, .1, -.9), (.4, -.5, -.8), .3, .23, 1, (0, -.2, 0)),
    # bangs over the forehead (the face is +z), the middle one longer, and locks in front of the ears
    ((-.42, .5, 1), (-.3, -.9, .35), .28, .18, 0, (0, -.05, .15)), ((-.14, .56, 1), (-.04, -.95, .4), .34, .19, 2, (0, -.05, .15)), ((.14, .56, 1), (.12, -.95, .4), .3, .18, 0, (0, -.05, .15)),
    ((.42, .5, 1), (.35, -.85, .35), .28, .18, 2, (0, -.05, .15)), ((-.98, .15, .5), (-.3, -1, .15), .32, .16, 1, (0, 0, .1)), ((.98, .15, .5), (.3, -1, .15), .32, .16, 1, (0, 0, .1)),
]
for aim, grow, L, r, mi, curl in SPIKES:
    d = G(*aim); p0 = hit(HEAD, C, d)
    if p0 is None: print('miss', aim); continue
    g = G(*grow).normalized(); cv = G(*curl)
    root = p0 - d.normalized() * r * .55
    pts = [root, p0 + g * L * .35, p0 + g * L * .7 + cv * L * .12, p0 + g * L + cv * L * .3]
    tube(bm, pts, [r, r * .85, r * .45, .01], 6, mi, flat=.5, up=d.normalized())   # squashed along the head normal -> wide, flat spikes
fin(me, bm, [HAIR, HAIR_D, HAIR_L], True)

# ---------- headband: a band on the forehead line all round the head, knot + two tails at the back
ob, me = obj('HeroBand'); bm = bmesh.new()
YB, HB, N = 1.93, .055, 32
outer, inner = [], []
for k in range(N):
    a = k / N * 6.283; d = G(math.sin(a), 0, math.cos(a)); c0 = G(0, YB, 0)
    p = hit(HEAD, c0, d)
    if p is None: p = c0 + d * .55
    outer.append(p + d.normalized() * .045); inner.append(p - d.normalized() * .005)
ring = lambda pts, dy: [bm.verts.new(p + Vector((0, 0, dy))) for p in pts]
ot, ob_, it, ib = ring(outer, HB), ring(outer, -HB), ring(inner, HB), ring(inner, -HB)
for k in range(N):
    j = (k + 1) % N
    for q in ((ot[k], ot[j], ob_[j], ob_[k]), (it[j], it[k], ib[k], ib[j]), (ot[j], ot[k], it[k], it[j]), (ob_[k], ob_[j], ib[j], ib[k])): bm.faces.new(q).material_index = 0
kn = hit(HEAD, G(0, YB, 0), G(0, 0, -1), .07)
g = bmesh.ops.create_cube(bm, size=1); xform(g, Matrix.Translation(kn) @ Matrix.Diagonal((.16, .1, .13, 1))); setmi(g, 1)
ribbon(bm, [kn + G(.04, 0, 0), kn + G(.08, -.12, -.16), kn + G(.12, -.3, -.24), kn + G(.14, -.5, -.27)], [.055, .06, .055, .05], G(1, 0, 0), .025, 0, fork=.07)
ribbon(bm, [kn + G(-.03, 0, 0), kn + G(-.06, -.16, -.12), kn + G(-.08, -.36, -.17), kn + G(-.09, -.54, -.19)], [.05, .055, .05, .045], G(1, 0, 0), .025, 1, fork=.06)
fin(me, bm, [RED, RED_D])

# ---------- scarf: a fat roll round the neck, a knot at the front, two long torn tails flying back to the hero's left (+x)
ob, me = obj('HeroScarf'); bm = bmesh.new()
YS, N = 1.21, 20
pts = []
for k in range(N):
    a = k / N * 6.283; d = G(math.sin(a), 0, math.cos(a)); p = hit(BODY, G(0, YS, 0), d)
    if p is None: p = hit(HEAD, G(0, YS + .06, 0), d)
    if p is None: p = G(0, YS, 0) + d * .36
    pts.append(p + d.normalized() * .07)
pts.append(pts[0]); pts.append(pts[1])
tube(bm, pts, [.105] * len(pts), 6, 0)
front = hit(BODY, G(-.12, YS - .06, 0), G(-.25, 0, 1), .08)
g = bmesh.ops.create_cube(bm, size=1); xform(g, Matrix.Translation(front) @ Matrix.Rotation(.3, 4, 'Z') @ Matrix.Diagonal((.18, .14, .16, 1))); setmi(g, 1)
ribbon(bm, [front + G(0, -.05, .02), front + G(-.04, -.22, .03), front + G(-.02, -.38, .02)], [.075, .08, .07], G(1, 0, 0), .03, 0, fork=.06)   # short front drape
back = hit(BODY, G(.18, YS, 0), G(.5, 0, -1), .08)
for dy, L, mi in ((0, 1.0, 0), (-.12, .78, 1)):   # tails blown back and to the side, sagging
    t = [back + G(0, dy, 0), back + G(.2 * L, dy - .12 * L, -.25 * L), back + G(.42 * L, dy - .26 * L, -.38 * L), back + G(.64 * L, dy - .32 * L, -.42 * L), back + G(.86 * L, dy - .3 * L, -.38 * L)]
    ribbon(bm, t, [.12, .13, .12, .1, .09], G(0, 1, .25), .035, mi, fork=.1)
fin(me, bm, [RED, RED_D], True)

# ---------- shoulder pad: steel dome, gold rim, a second layered plate (dome along +Z like PauldronA)
ob, me = obj('HeroPad'); bm = bmesh.new()
for R, z0, zk, mi in ((.3, 0, .62, 0), (.22, .1, .7, 1)):
    d = bmesh.ops.create_uvsphere(bm, u_segments=10, v_segments=6, radius=R)
    for v in list(d['verts']):
        if v.co.z < -.02: v.co.z = -.02
        v.co.z = v.co.z * zk + z0
    setmi(d, mi)
rim = bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=.33, radius2=.33, depth=.06); setmi(rim, 2)
rim2 = bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=.245, radius2=.245, depth=.05); xform(rim2, Matrix.Translation((0, 0, .1))); setmi(rim2, 2)
fin(me, bm, [STEEL, STEEL_D, GOLD])

# ---------- chest badge: gold chevron on the tunic front
ob, me = obj('HeroBadge'); bm = bmesh.new()
cf = hit(BODY, G(0, 1.05, 0), G(0, 0, 1), .012)
slab(bm, [(-.17, .09), (-.1, .09), (0, -.03), (.1, .09), (.17, .09), (0, -.15)], cf, G(1, 0, 0), G(0, 1, 0), G(0, 0, 1), .035, 0)
g = bmesh.ops.create_cone(bm, cap_ends=True, segments=4, radius1=.05, radius2=.05, depth=.04); xform(g, Matrix.Translation(cf + G(0, .1, .005)) @ Matrix.Rotation(math.pi / 2, 4, 'X')); setmi(g, 1)
fin(me, bm, [GOLD, GLOWR])

# ---------- belt pouch on the right hip
ob, me = obj('HeroPouch'); bm = bmesh.new()
hp = hit(BODY, G(-.2, .6, 0), G(-.75, 0, .6), .03)
g = bmesh.ops.create_cube(bm, size=1); xform(g, Matrix.Translation(hp) @ Matrix.Rotation(-.9, 4, 'Z') @ Matrix.Diagonal((.16, .1, .17, 1))); setmi(g, 0)
g = bmesh.ops.create_cube(bm, size=1); xform(g, Matrix.Translation(hp + G(0, .06, 0)) @ Matrix.Rotation(-.9, 4, 'Z') @ Matrix.Diagonal((.17, .115, .06, 1))); setmi(g, 1)
fin(me, bm, [LEATH, GOLD_D])

# ---------- rune blade (hand-slot space: grip at 0, blade up +y = Blender +Z, guard along x, flat faces toward +-z = Blender -+y)
ob, me = obj('RuneBlade'); bm = bmesh.new()
X, Y, Z = Vector((1, 0, 0)), Vector((0, 0, 1)), Vector((0, -1, 0))   # Blender vectors for game x, y (blade), z (face normal)
tube(bm, [Vector((0, 0, -.34)), Vector((0, 0, .1))], [.05, .05], 6, 3)   # grip
g = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=.075); xform(g, Matrix.Translation((0, 0, -.38))); setmi(g, 4)   # pommel
slab(bm, [(-.32, .1), (-.26, .12), (.26, .12), (.32, .1), (.25, -.02), (.08, .0), (0, -.04), (-.08, .0), (-.25, -.02)], Vector((0, 0, .1)), X, Y, Z, .13, 4)   # guard
g = bmesh.ops.create_cone(bm, cap_ends=True, segments=4, radius1=.055, radius2=.055, depth=.15); xform(g, Matrix.Translation((0, 0, .14)) @ Matrix.Rotation(math.pi / 2, 4, 'X')); setmi(g, 5)   # red gem in the guard
blade = [(-.17, .2), (-.165, 1.2), (0, 1.52), (.165, 1.2), (.17, .2)]
slab(bm, blade, Vector((0, 0, 0)), X, Y, Z, .055, 1)   # light steel edge (full width)
core = [(-.11, .2), (-.105, 1.14), (0, 1.36), (.105, 1.14), (.11, .2)]
slab(bm, core, Vector((0, 0, 0)), X, Y, Z, .085, 0)   # dark core (thicker, narrower)
for sgn in (1, -1):   # runes on both faces
    off = Z * sgn * .046
    for y0 in (.42, .6):
        slab(bm, [(-.05, y0 + .05), (.0, y0), (-.05, y0 - .05), (-.075, y0 - .05), (-.025, y0), (-.075, y0 + .05)], off, X, Y, Z, .012, 2)
        slab(bm, [(.04, y0 + .05), (.09, y0), (.04, y0 - .05), (.015, y0 - .05), (.065, y0), (.015, y0 + .05)], off, X, Y, Z, .012, 2)
    slab(bm, [(0, .84), (.07, .92), (0, 1.0), (-.07, .92)], off, X, Y, Z, .012, 2)
    slab(bm, [(0, .875), (.035, .92), (0, .965), (-.035, .92)], off + Z * sgn * .004, X, Y, Z, .012, 0)
slab(bm, [(.12, 1.0), (.17, 1.0), (.165, 1.2), (0, 1.52), (-.02, 1.47), (.13, 1.19)], Vector((0, 0, 0)), X, Y, Z, .062, 2)   # glowing edge near the tip
fin(me, bm, [BLADE, EDGE, GLOWR, GRIP, GOLD, GLOWR])

bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', export_apply=True)
print('wrote', OUT, sorted(o.name for o in bpy.data.objects))
