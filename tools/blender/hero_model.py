# The red-scarf hero of tribe3d.html, modelled from scratch after the owner's design picture (art/incoming/tribe3d/hero_ref.png;
# owner 2026-11-17 on the first try built on the KayKit Knight: "ไม่เหมือนเลย"). Chibi body ~2.4 tall in the bind pose of the KayKit
# Rig_Medium skeleton, so every KayKit move still plays: each part is named "<bone>|<part>" and the game pins it to that bone, then
# merges all parts into ONE skinned mesh (vertex colours = the material colours). "RuneBlade" = the sword, in the right hand-slot space.
# Modelled Z-up -> Y-up glTF; G(x, y, z) takes GAME coordinates (y up, the hero looks at +z, his left hand is +x).
#   pip install bpy ; python3 tools/blender/hero_model.py art/tribe3d/people/hero_model.glb
import bpy, bmesh, math, sys
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
OUT = sys.argv[-1] if sys.argv[-1].endswith('.glb') else 'art/tribe3d/people/hero_model.glb'
bpy.ops.wm.read_factory_settings(use_empty=True)
def G(x, y, z): return Vector((x, -z, y))   # game -> Blender
def lin(h):
    c = [((h >> s) & 255) / 255 for s in (16, 8, 0)]
    return tuple(v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in c)
MATS = {}
def M(name, h):
    if name not in MATS:
        m = bpy.data.materials.new(name); m.use_nodes = True; m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (*lin(h), 1); MATS[name] = m
    return MATS[name]
SKIN, SKIN_D, EYE_W, IRIS, PUPIL, BROW, MOUTH = M('skin', 0xf7cfac), M('skin_dark', 0xe8a888), M('eye_white', 0xfbf6f0), M('iris', 0x5a3424), M('pupil', 0x24140e), M('brow', 0x3c2016), M('mouth', 0x6a3426)
HAIR, HAIR_L, HAIR_D = M('hair', 0x703826), M('hair_light', 0x80442e), M('hair_dark', 0x4e261a)
RED, RED_D = M('scarf', 0xd8262a), M('scarf_dark', 0x9c1820)
PURP, PURP_L, PURP_D, GAUNT = M('tunic', 0x4e4878), M('tunic_light', 0x5e588c), M('trousers', 0x37325a), M('gauntlet', 0x5a5880)
GOLD, GOLD_D, STEEL, STEEL_D = M('gold', 0xe8a630), M('gold_dark', 0xb87a22), M('steel', 0x6e717c), M('steel_dark', 0x4c4e58)
BELT, LEATH, BOOT, BOOT_L, TOE, SOLE = M('belt', 0x4e2a1a), M('leather', 0x7a4628), M('boot', 0x5e3826), M('boot_light', 0x7a4a30), M('toecap', 0x8a7e78), M('sole', 0x3a2418)
BLADE, EDGE, GRIP, GLOWR = M('blade', 0x2a2430), M('blade_edge', 0xd0d4dc), M('grip', 0x2e2026), M('glow_red', 0xff2a36)

class Part:   # one exported object: bmesh + its own material list
    def __init__(self, name, smooth=False): self.name, self.bm, self.mats, self.smooth = name, bmesh.new(), [], smooth
    def mi(self, m):
        if m not in self.mats: self.mats.append(m)
        return self.mats.index(m)
    def done(self):
        me = bpy.data.meshes.new(self.name); ob = bpy.data.objects.new(self.name, me); bpy.context.collection.objects.link(ob)
        for m in self.mats: me.materials.append(m)
        bmesh.ops.recalc_face_normals(self.bm, faces=self.bm.faces); self.bm.to_mesh(me); self.bm.free()
        for p in me.polygons: p.use_smooth = self.smooth
def setmi(geom, mi):
    for f in {f for v in geom['verts'] for f in v.link_faces}: f.material_index = mi
def blob(P, c, r, m, p=2.0, segs=(16, 10), squash=None, keep=None):
    """ellipsoid / rounded box (exponent p) centred at game point c with game radii r; squash(v_game) -> new game point; keep(v_game) -> drop faces"""
    bm = P.bm; g = bmesh.ops.create_uvsphere(bm, u_segments=segs[0], v_segments=segs[1], radius=1)
    for v in g['verts']:
        n = Vector((v.co.x, v.co.z, -v.co.y))   # unit sphere in game axes
        k = (abs(n.x) ** p + abs(n.y) ** p + abs(n.z) ** p) ** (1 / p) or 1
        q = Vector((n.x / k * r[0], n.y / k * r[1], n.z / k * r[2])) + Vector(c)
        if squash: q = squash(q)
        v.co = G(*q)
    setmi(g, P.mi(m))
    if keep:
        dead = [f for f in {f for v in g['verts'] for f in v.link_faces} if not keep(Vector((f.calc_center_median().x, f.calc_center_median().z, -f.calc_center_median().y)))]
        bmesh.ops.delete(bm, geom=dead, context='FACES')
    return g
def tube(P, pts, rad, m, sides=8, side=None, flat=1.0):
    """tube through game points; rad = radius per point (or (width, thickness)); side = game vector the width lies along"""
    bm = P.bm; mi = P.mi(m); pts = [Vector(p) for p in pts]; rings = []
    for i, p in enumerate(pts):
        t = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        s = Vector(side) if side is not None else (Vector((1, 0, 0)) if abs(t.x) < .9 else Vector((0, 0, 1)))
        s = (s - t * s.dot(t)); s = s.normalized() if s.length > 1e-4 else t.orthogonal().normalized(); w = t.cross(s)
        rw, rt = (rad[i], rad[i] * flat) if not isinstance(rad[i], tuple) else rad[i]
        rings.append([bm.verts.new(G(*(p + s * math.cos(k / sides * 6.283) * rw + w * math.sin(k / sides * 6.283) * rt))) for k in range(sides)])
    for r0, r1 in zip(rings, rings[1:]):
        for k in range(sides): bm.faces.new((r0[k], r0[(k + 1) % sides], r1[(k + 1) % sides], r1[k])).material_index = mi
    for r, flip in ((rings[0], True), (rings[-1], False)): bm.faces.new(list(reversed(r)) if flip else r).material_index = mi
def slab(P, pts2d, origin, ax, ay, az, depth, m):
    """flat polygon (2-D points on the ax / ay plane, game vectors) extruded along az, centred"""
    bm = P.bm; mi = P.mi(m); o, ax, ay, az = Vector(origin), Vector(ax), Vector(ay), Vector(az)
    top = [bm.verts.new(G(*(o + ax * x + ay * y + az * depth / 2))) for x, y in pts2d]; bot = [bm.verts.new(G(*(o + ax * x + ay * y - az * depth / 2))) for x, y in pts2d]
    bm.faces.new(top).material_index = mi; bm.faces.new(list(reversed(bot))).material_index = mi
    n = len(pts2d)
    for k in range(n): bm.faces.new((bot[k], bot[(k + 1) % n], top[(k + 1) % n], top[k])).material_index = mi
def ribbon(P, pts, half, side, thick, m, fork=0):
    """cloth strip along game points, half-widths per point along `side`, closed with thickness; fork = torn two-point end"""
    bm = P.bm; mi = P.mi(m); pts = [Vector(p) for p in pts]; s = Vector(side).normalized()
    nrm = [((pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).cross(s)).normalized() * thick / 2 for i in range(len(pts))]
    def layer(sign):
        L = [bm.verts.new(G(*(p - s * h + n * sign))) for p, h, n in zip(pts, half, nrm)]; R = [bm.verts.new(G(*(p + s * h + n * sign))) for p, h, n in zip(pts, half, nrm)]; return L, R
    (L1, R1), (L2, R2) = layer(1), layer(-1)
    for i in range(len(pts) - 1):
        for q in ((L1[i], L1[i + 1], R1[i + 1], R1[i]), (L2[i], R2[i], R2[i + 1], L2[i + 1]), (L1[i], L2[i], L2[i + 1], L1[i + 1]), (R1[i], R1[i + 1], R2[i + 1], R2[i])): bm.faces.new(q).material_index = mi
    for q in ((L1[0], R1[0], R2[0], L2[0]),): bm.faces.new(q).material_index = mi
    d = (pts[-1] - pts[-2]).normalized()
    if fork:   # torn end: two points and a notch
        for sign, (A, B) in ((1, (L1, R1)), (-1, (L2, R2))):
            n = nrm[-1] * sign; mid = bm.verts.new(G(*(pts[-1] - d * fork * .3 + n))); t1 = bm.verts.new(G(*(pts[-1] - s * half[-1] * .6 + d * fork + n))); t2 = bm.verts.new(G(*(pts[-1] + s * half[-1] * .5 + d * fork * .7 + n)))
            for q in ((A[-1], t1, mid), (mid, t2, B[-1]), (A[-1], mid, B[-1])): bm.faces.new(q if sign > 0 else tuple(reversed(q))).material_index = mi
    else: bm.faces.new((L1[-1], L2[-1], R2[-1], R1[-1])).material_index = mi
X, Y, Z = Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))

# ================= HEAD (bone head, pivot y 1.24) =================
HC, HR = Vector((0, 1.665, 0)), (.44, .43, .41)
def jaw(q):   # narrower, rounder lower face (chibi cheeks to a soft chin)
    t = max(0, (HC.y - q.y) / HR[1])
    return Vector((q.x * (1 - .2 * t * t), q.y, q.z * (1 - .08 * t) + .02 * t))
P = Part('head|skull', smooth=True); blob(P, HC, HR, SKIN, p=2.3, segs=(28, 18), squash=jaw)
bvh = BVHTree.FromBMesh(P.bm)   # in Blender space
def face_pt(x, y, off):   # point on the front of the skull at game (x, y), pushed out along +z
    loc, n, i, d = bvh.ray_cast(G(x, y, 0), G(0, 0, 1))
    return Vector((loc.x, loc.z, -loc.y)) + Z * off if loc else Vector((x, y, .4 + off))
for sx in (1, -1):   # ears
    blob(P, (sx * .425, 1.6, -.03), (.06, .095, .085), SKIN, segs=(10, 8))
    blob(P, (sx * .45, 1.6, -.02), (.025, .055, .045), SKIN_D, segs=(8, 6))
blob(P, face_pt(0, 1.465, -.01), (.026, .022, .024), SKIN_D, segs=(8, 6))   # tiny nose
P.done()
def decal(name, pts, cx, cy, off, m, thick=.012, sx=1):
    """a shape (2-D points around (cx, cy), x mirrored by sx) laid on the face surface"""
    P = Part(name); bm = P.bm; mi = P.mi(m)
    front = [bm.verts.new(G(*face_pt(cx + sx * u, cy + v, off))) for u, v in pts]; back = [bm.verts.new(G(*face_pt(cx + sx * u, cy + v, off - thick))) for u, v in pts]
    if sx < 0: front.reverse(); back.reverse()
    bm.faces.new(front).material_index = mi; bm.faces.new(list(reversed(back))).material_index = mi
    n = len(pts)
    for k in range(n): bm.faces.new((back[k], back[(k + 1) % n], front[(k + 1) % n], front[k])).material_index = mi
    P.done()
def ell(rx, ry, cx=0, cy=0, n=14, top=None):
    out = []
    for k in range(n):
        a = k / n * 6.283; x, y = cx + math.cos(a) * rx, cy + math.sin(a) * ry
        if top: y = min(y, top(x) - .006)
        out.append((x, y))
    return out
EX, EY = .165, 1.535   # eye centres (x mirrored); u > 0 = toward the ear
lid = lambda u: .052 + (u + .075) * .2   # angry slant: inner corner low, outer high
for sx, tag in ((1, 'L'), (-1, 'R')):
    sclera = [(-.078, lid(-.078)), (-.02, lid(-.02)), (.04, lid(.04)), (.083, lid(.083)), (.088, .02), (.072, -.045), (.035, -.08), (-.01, -.088), (-.05, -.07), (-.075, -.03)]
    decal(f'head|eye{tag}', sclera, sx * EX, EY, .006, EYE_W, sx=sx)
    decal(f'head|iris{tag}', ell(.05, .078, -.008, -.008, 16, top=lid), sx * EX, EY, .010, IRIS, sx=sx)
    decal(f'head|pupil{tag}', ell(.028, .046, -.008, -.012, 12, top=lid), sx * EX, EY, .013, PUPIL, sx=sx)
    decal(f'head|glint{tag}', ell(.017, .017, .012, .03, 8), sx * EX, EY, .016, EYE_W, sx=sx)
    decal(f'head|lid{tag}', [(-.084, lid(-.084) - .012), (.095, lid(.095) - .012), (.1, lid(.1) + .016), (-.084, lid(-.084) + .014)], sx * EX, EY, .015, PUPIL, sx=sx)
    decal(f'head|brow{tag}', [(-.07, .1), (.1, .145), (.106, .185), (-.075, .143)], sx * EX, EY, .03, BROW, thick=.035, sx=sx)
decal('head|mouth', [(-.045, -.012), (0, .006), (.045, -.012), (.045, -.002), (0, .016), (-.045, -.002)], 0, 1.375, .008, MOUTH)

# ---------- hair: a shell over the skull + big smooth leaf-like clumps (bangs, crown sweeping up and back, side fans)
HHC, HHR = Vector((0, 1.7, -.03)), (.52, .49, .52)   # a full mass, well outside the skull
def hairline(q):
    t = (q.z - HHC.z) / HHR[2]
    return q.y > 1.55 + .3 * max(t, 0) - .25 * max(-t, 0)
P = Part('head|hair', smooth=True); blob(P, HHC, HHR, HAIR, segs=(28, 18), keep=hairline)
def surf(d):   # point on the hair shell in direction d (game)
    d = Vector(d).normalized(); t = 1 / math.sqrt((d.x / HHR[0]) ** 2 + (d.y / HHR[1]) ** 2 + (d.z / HHR[2]) ** 2); return HHC + d * t, d
CLUMPS = [   # aim (root on the shell), grow, length, width, thickness, curl, colour: few BIG soft clumps like the picture
    # bangs: wide clumps from the top front, hanging over the headband down to the brows; the middle-right one longest
    ((-.27, .75, .62), (-.12, -.92, .38), .44, .16, .07, (-.05, -.15, .02), HAIR), ((-.03, .8, .6), (-.05, -.92, .4), .52, .17, .075, (0, -.15, .02), HAIR_L),
    ((.2, .78, .6), (.06, -.92, .38), .44, .16, .07, (.05, -.15, .02), HAIR), ((.42, .65, .6), (.22, -.93, .3), .38, .15, .065, (.05, -.15, 0), HAIR_L),
    ((-.45, .65, .6), (-.22, -.93, .3), .38, .15, .065, (-.05, -.15, 0), HAIR),
    ((-.95, .15, .32), (-.2, -1, .1), .3, .11, .055, (0, -.1, .1), HAIR_D), ((.95, .15, .32), (.2, -1, .1), .3, .11, .055, (0, -.1, .1), HAIR_D),   # locks before the ears
    # crown: tufts sweeping up and back, overlapping into one mass
    ((.08, 1, .2), (.45, .85, -.2), .28, .24, .11, (.2, -.25, -.2), HAIR_L), ((-.25, 1, .1), (-.4, .8, -.4), .28, .24, .11, (-.1, -.3, -.25), HAIR),
    ((.32, .95, -.05), (.6, .65, -.45), .28, .22, .1, (.1, -.3, -.2), HAIR), ((0, .9, -.35), (0, .5, -.85), .32, .24, .11, (0, -.35, -.1), HAIR),
    ((-.08, 1, -.05), (.05, .75, -.65), .26, .22, .1, (0, -.3, -.2), HAIR_L),
    # sides: clumps hanging out and DOWN (not a mane), layered
    ((-.9, .6, .1), (-.85, -.25, -.2), .36, .2, .095, (-.05, -.2, 0), HAIR), ((-.85, .3, -.3), (-.8, -.45, -.4), .34, .2, .095, (0, -.2, 0), HAIR_D),
    ((.9, .6, .05), (.85, -.25, -.25), .34, .2, .095, (.05, -.2, 0), HAIR), ((.85, .3, -.35), (.8, -.45, -.45), .32, .19, .09, (0, -.2, 0), HAIR_D),
    ((-.75, .85, -.2), (-.9, .2, -.5), .34, .2, .095, (0, -.3, 0), HAIR), ((.75, .85, -.2), (.9, .2, -.5), .32, .2, .095, (0, -.3, 0), HAIR),
    # back
    ((-.35, .3, -.9), (-.3, -.55, -.75), .32, .22, .1, (0, -.2, 0), HAIR_D), ((.35, .3, -.9), (.3, -.55, -.75), .3, .22, .1, (0, -.2, 0), HAIR_D), ((0, 0, -1), (0, -.7, -.7), .28, .22, .1, (0, -.1, 0), HAIR_D),
]
for aim, grow, L, w, t, curl, col in CLUMPS:
    p0, n = surf(aim); g = Vector(grow).normalized(); cv = Vector(curl)
    side = g.cross(n); side = side.normalized() if side.length > .15 else g.cross(Y).normalized()
    pts = [p0 - n * .07, p0 + g * L * .22, p0 + g * L * .5 + cv * L * .1, p0 + g * L * .78 + cv * L * .25, p0 + g * L + cv * L * .42]
    tube(P, pts, [(w * .8, t * .8), (w, t), (w * .85, t * .85), (w * .5, t * .55), (.006, .006)], col, sides=8, side=side)
P.done()
# headband round the hair line + knot and tails at the back
P = Part('head|band', smooth=True); YB = 1.77; N = 28; ring = []
for k in range(N + 1):
    a = k / N * 6.283; dy = (YB - HHC.y) / HHR[1]; s = math.sqrt(max(.05, 1 - dy * dy))
    dyk = (YB - HC.y) / HR[1]; sk = math.sqrt(max(.05, 1 - dyk * dyk)); front = max(0, math.cos(a))   # on the forehead skin in front, over the hair behind
    rx, rz = HR[0] * sk * 1.05 * front + HHR[0] * s * 1.02 * (1 - front), HR[2] * sk * 1.06 * front + HHR[2] * s * 1.02 * (1 - front)
    ring.append(Vector((math.sin(a) * rx, YB + .02 * math.cos(a), (HC.z if front else HHC.z) + math.cos(a) * rz)))
tube(P, ring, [(.035, .018)] * len(ring), RED, sides=6, side=Y)
kn = Vector((0, YB, HHC.z - HHR[2] * .93))
blob(P, kn + Vector((.05, 0, -.03)), (.055, .045, .04), RED_D, segs=(8, 6)); blob(P, kn + Vector((-.05, 0, -.03)), (.055, .045, .04), RED_D, segs=(8, 6))
ribbon(P, [kn + Vector((.03, -.02, -.03)), kn + Vector((.08, -.15, -.12)), kn + Vector((.12, -.32, -.17)), kn + Vector((.14, -.48, -.18))], [.04, .045, .042, .04], X, .02, RED, fork=.05)
ribbon(P, [kn + Vector((-.03, -.02, -.03)), kn + Vector((-.07, -.14, -.1)), kn + Vector((-.1, -.28, -.14)), kn + Vector((-.11, -.42, -.15))], [.038, .042, .04, .037], X, .02, RED_D, fork=.05)
P.done()

# ================= NECK + SCARF (bone chest) =================
P = Part('chest|neck', smooth=True); tube(P, [(0, 1.1, 0), (0, 1.32, 0)], [.12, .12], SKIN, sides=10); P.done()
P = Part('chest|scarf', smooth=True)
for yc, rx, rz, r, col, tilt in ((1.2, .27, .25, .09, RED, .05), (1.265, .245, .22, .08, RED, .04)):
    pts = [Vector((math.sin(k / 24 * 6.283) * rx, yc - tilt * math.cos(k / 24 * 6.283), math.cos(k / 24 * 6.283) * rz)) for k in range(25)]
    tube(P, pts, [r] * len(pts), col, sides=8)
blob(P, (.2, 1.2, -.14), (.1, .09, .09), RED, segs=(10, 8))   # the knot behind his left shoulder, where the tails start
for (x0, y0, z0), L, h, col in (((.16, 1.2, -.18), .8, .14, RED), ((.12, 1.12, -.2), .62, .12, RED_D)):   # tails blown back over his left shoulder, sagging
    pts = [Vector((x0, y0, z0)), Vector((x0 + .22 * L, y0 - .1 * L, z0 - .22 * L)), Vector((x0 + .45 * L, y0 - .3 * L, z0 - .3 * L)), Vector((x0 + .64 * L, y0 - .52 * L, z0 - .28 * L)), Vector((x0 + .78 * L, y0 - .72 * L, z0 - .22 * L))]
    ribbon(P, pts, [h * .75, h, h * 1.15, h * 1.15, h * 1.05], Vector((.55, .55, .3)), .035, col, fork=.13)
P.done()

# ================= BODY =================
P = Part('chest|torso', smooth=True)
blob(P, (0, 1.0, 0), (.3, .25, .215), PURP, p=3.2, segs=(18, 12), squash=lambda q: Vector((q.x * (1 + .06 * (q.y - .9) / .3), q.y, q.z)))
fz = lambda y: .214   # front surface of the torso (flat-ish rounded box)
slab(P, [(-.1, .78), (.1, .78), (.11, 1.1), (-.11, 1.1)], (0, 0, .205), X, Y, Z, .03, PURP_L)   # lighter front panel
slab(P, [(-.17, 1.2), (-.07, 1.2), (0, 1.12), (.07, 1.2), (.17, 1.2), (.09, 1.1), (0, 1.0), (-.09, 1.1)], (0, 0, .225), X, Y, Z, .035, GOLD)   # gold chevron emblem
P.done()
P = Part('spine|waist', smooth=True)
blob(P, (0, .7, 0), (.27, .12, .2), PURP, p=3, segs=(16, 10))
blob(P, (0, .645, 0), (.29, .045, .222), BELT, p=4, segs=(18, 8))
slab(P, [(-.075, -.06), (.075, -.06), (.075, .06), (-.075, .06)], (0, .645, .235), X, Y, Z, .03, GOLD)   # buckle frame
slab(P, [(-.04, -.028), (.04, -.028), (.04, .028), (-.04, .028)], (0, .645, .25), X, Y, Z, .012, BELT)
P.done()
P = Part('hips|pelvis', smooth=True)
blob(P, (0, .5, 0), (.255, .1, .185), PURP_D, p=3, segs=(16, 10))
for sx in (1, -1):   # tunic flaps under the belt: front split in two, gold edges
    fl = [(sx * .01, .62), (sx * .23, .62), (sx * .24, .42), (sx * .13, .37), (sx * .01, .41)]
    slab(P, fl if sx > 0 else list(reversed(fl)), (0, 0, .2), X, Y, Z, .03, PURP)
    tr = [(sx * .24, .44), (sx * .13, .39), (sx * .01, .43), (sx * .01, .395), (sx * .13, .35), (sx * .245, .405)]
    slab(P, tr if sx > 0 else list(reversed(tr)), (0, 0, .214), X, Y, Z, .02, GOLD)
slab(P, [(-.24, .62), (.24, .62), (.25, .42), (-.25, .42)], (0, 0, -.2), X, Y, Z, .03, PURP)   # back flap
blob(P, (.27, .57, .08), (.055, .07, .06), LEATH, p=3, segs=(10, 8))   # pouch on his left hip
blob(P, (.27, .615, .085), (.06, .028, .065), BELT, p=3, segs=(10, 6))
blob(P, (.27, .6, .15), (.014, .014, .01), GOLD, segs=(6, 4))
P.done()

for sx, s in ((1, 'l'), (-1, 'r')):
    # shoulder pad (two layered steel plates, gold rims), pinned to the upper arm
    P = Part(f'upperarm{s}|pad')
    blob(P, (sx * .3, 1.17, 0), (.2, .13, .19), STEEL, segs=(8, 5), keep=lambda q: q.y > 1.12)
    tube(P, [Vector((sx * .3 + math.sin(k / 12 * 6.283) * .2, 1.125, math.cos(k / 12 * 6.283) * .19)) for k in range(13)], [.03] * 13, GOLD, sides=5)
    blob(P, (sx * .4, 1.1, 0), (.15, .1, .165), STEEL_D, segs=(8, 5), keep=lambda q: q.y > 1.05)
    tube(P, [Vector((sx * .4 + math.sin(k / 12 * 6.283) * .15, 1.055, math.cos(k / 12 * 6.283) * .165)) for k in range(13)], [.025] * 13, GOLD, sides=5)
    P.done()
    P = Part(f'upperarm{s}|sleeve', smooth=True)
    blob(P, (sx * .25, 1.11, 0), (.1, .1, .1), PURP_D, segs=(10, 8)); tube(P, [(sx * .24, 1.11, 0), (sx * .47, 1.11, 0)], [.092, .086], PURP_D, sides=10); P.done()
    P = Part(f'lowerarm{s}|gauntlet', smooth=True)
    tube(P, [(sx * .45, 1.11, 0), (sx * .58, 1.11, 0), (sx * .73, 1.11, 0)], [.1, .115, .128], GAUNT, sides=8)
    tube(P, [(sx * .465, 1.11, 0), (sx * .515, 1.11, 0)], [.118, .118], GOLD, sides=8); tube(P, [(sx * .67, 1.11, 0), (sx * .735, 1.11, 0)], [.14, .14], GOLD, sides=8)
    P.done()
    P = Part(f'hand{s}|fist', smooth=True)
    blob(P, (sx * .815, 1.1, 0), (.072, .078, .082), SKIN, p=3, segs=(10, 8)); blob(P, (sx * .79, 1.13, .075), (.035, .03, .03), SKIN, segs=(8, 6)); P.done()
    # legs
    P = Part(f'upperleg{s}|thigh', smooth=True)
    blob(P, (sx * .16, .49, 0), (.1, .1, .1), PURP_D, segs=(10, 8)); tube(P, [(sx * .17, .52, 0), (sx * .17, .3, 0)], [.1, .094], PURP_D, sides=10); P.done()
    P = Part(f'lowerleg{s}|shin', smooth=True)
    tube(P, [(sx * .17, .3, 0), (sx * .17, .15, 0)], [.088, .085], PURP_D, sides=10)
    tube(P, [(sx * .17, .335, 0), (sx * .17, .255, 0)], [.12, .12], GOLD, sides=12)   # big gold knee band
    tube(P, [(sx * .17, .225, -.005), (sx * .17, .15, -.005)], [.112, .108], BOOT_L, sides=10)   # boot cuff
    P.done()
    P = Part(f'foot{s}|boot', smooth=True)
    blob(P, (sx * .17, .09, -.01), (.098, .09, .12), BOOT, p=3, segs=(12, 8)); blob(P, (sx * .17, .018, .02), (.104, .02, .155), SOLE, p=4, segs=(12, 6)); P.done()
    P = Part(f'toes{s}|toecap', smooth=True)
    blob(P, (sx * .17, .07, .12), (.104, .068, .085), TOE, p=2.4, segs=(12, 8)); P.done()

# ================= SWORD (right hand-slot space: grip at 0, blade along +y, guard along x, flat faces +-z) =================
P = Part('RuneBlade')
tube(P, [(0, -.3, 0), (0, .07, 0)], [.045, .045], GRIP, sides=8)
for y in (-.22, -.12, -.02): tube(P, [(0, y, 0), (0, y + .025, 0)], [.05, .05], GOLD_D, sides=8)
blob(P, (0, -.335, 0), (.06, .045, .06), GOLD, segs=(10, 6))
blob(P, (0, .1, 0), (.21, .055, .055), GOLD, p=3.5, segs=(16, 8))   # guard: a fat gold bar with rounded ends
blob(P, (0, .1, .05), (.035, .035, .015), GLOWR, segs=(8, 6)); blob(P, (0, .1, -.05), (.035, .035, .015), GLOWR, segs=(8, 6))
slab(P, [(-.14, .14), (-.13, 1.1), (.14, 1.42), (.14, .14)], (0, 0, 0), X, Y, Z, .05, EDGE)   # bright metal (shows at the edges)
slab(P, [(-.1, .14), (-.095, 1.08), (.095, 1.3), (.095, .14)], (0, 0, 0), X, Y, Z, .07, BLADE)   # dark core
slab(P, [(-.14, .2), (-.12, .2), (-.11, 1.08), (.12, 1.37), (.14, 1.42), (-.13, 1.1)], (0, 0, 0), X, Y, Z, .055, GLOWR)   # red glowing lower edge + tip
for sz in (1, -1):   # runes on both faces: "<<" toward the tip, "<o>" near the guard
    o = Vector((0, 0, sz * .037))
    for y0 in (.86, .99):
        slab(P, [(.03, y0 + .045), (-.03, y0), (.03, y0 - .045), (.05, y0 - .045), (-.005, y0), (.05, y0 + .045)], o, X, Y, Z, .01, GLOWR)
    slab(P, [(-.02, .44), (-.065, .4), (-.02, .36), (-.005, .36), (-.045, .4), (-.005, .44)], o, X, Y, Z, .01, GLOWR)
    slab(P, [(.035, .44), (.075, .4), (.035, .36), (.0, .4)], o, X, Y, Z, .01, GLOWR)
    slab(P, [(.035, .42), (.055, .4), (.035, .38), (.017, .4)], o + Vector((0, 0, sz * .003)), X, Y, Z, .01, BLADE)
P.done()

HS = 1.08   # the picture's head is a touch bigger than the KayKit people's
for ob in bpy.data.objects:
    if ob.name.startswith('head|'): ob.data.transform(Matrix.Translation(G(0, 1.24, 0)) @ Matrix.Scale(HS, 4) @ Matrix.Translation(-G(0, 1.24, 0)))
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', export_apply=True)
print('wrote', OUT, len(bpy.data.objects), 'parts')
