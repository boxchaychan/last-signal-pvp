# The ADVENTURER of the bag game (owner 2026-11-27 "ทำโมเดลสวยเท่ๆรักผจญภัย", then "ฉันไม่ได้จะใช้ Tripo"): modelled from scratch in code after
# the owner's own picture art/incoming/pixgrind/v4/hero_v4_owner.png (auburn high ponytail, teal scarf, cream blouse, brown bodice, belt +
# pouch, teal tabard, wrapped gloves, fur-top boots) + a small backpack with a bedroll. Free: no Tripo, no PixelLab.
# Output = the same kind of file tools/blender/tripo_parts_rig.py writes, so the games load it with rigTripo() and every KayKit / UAL move plays:
#   meshes "body", "sword" (right hand slot), "bow" (left hand slot), one texture atlas (colours + baked soft shadows + a painted face),
#   an armature with the KayKit Rig_Medium names at HER joints, extras "joints" (rigTripo re-binds on these) and "chains" (ponytail and scarf
#   bones the game swings with springs: bag3d/spring.js).
# Game coordinates everywhere: y up, she looks at +z, her left hand is +x, 2.45 tall.
#   pip install bpy pillow ; python3 tools/blender/adventurer_model.py art/bag3d/adventurer.glb [--preview=/tmp/adv.png] [--fast]
#   --fast = no texture: only the preview picture, painted with the plain part colours (for shaping)
import bpy, bmesh, math, sys, json, os
import numpy as np
from mathutils import Vector, Matrix
from PIL import Image, ImageDraw, ImageFilter
ARGS = sys.argv[1:]
OUT = next((a for a in ARGS if a.endswith('.glb')), 'art/bag3d/adventurer.glb')
PREVIEW = next((a.split('=', 1)[1] for a in ARGS if a.startswith('--preview=')), None)
FAST = '--fast' in ARGS
SRC = 'art/incoming/bag3d/adventurer'   # the atlas and the face picture are kept here
TAU = math.tau
bpy.ops.wm.read_factory_settings(use_empty=True)
def G(x, y, z): return Vector((x, -z, y))   # game -> Blender
def Gi(v): return Vector((v.x, v.z, -v.y))   # Blender -> game
def lin(h): return tuple(v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in [((h >> s) & 255) / 255 for s in (16, 8, 0)])
def C(h): return (*lin(h), 1.0)
def mix(a, b, t): return tuple(a[i] * (1 - t) + b[i] * t for i in range(4))
def ss(a, b, x): t = min(1, max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t)
def grad(top, bot, y1, y0): return lambda p: mix(bot, top, ss(y0, y1, p.y))   # colour by height
X, Y, Z = Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))

# ---------------- colours
SKIN, SKIN_D = C(0xfbdcc0), C(0xf0b999)
HAIR, HAIR_L, HAIR_D = C(0x8e4526), C(0xbe6c3c), C(0x5a2a18)
TEAL, TEAL_L, TEAL_D = C(0x2c8f8c), C(0x55b8ac), C(0x1c6468)
CREAM, CREAM_D, FUR = C(0xf4e7cc), C(0xd8c39c), C(0xfaf0dc)
LEATH, LEATH_L, LEATH_D, BELT = C(0x7c4a2c), C(0x9c6438), C(0x57321e), C(0x4c2a1a)
GOLD, GOLD_D = C(0xf0b43c), C(0xb87a22)
SHORTS, SOLE = C(0x35333e), C(0x33221a)
STEEL, STEEL_L, STEEL_D = C(0xc4ccd8), C(0xeef2f8), C(0x8590a4)
WOOD, WOOD_D = C(0x8a5a34), C(0x5e3a22)

# ---------------- her joints (the KayKit names); arms hang 42 degrees below level
TH = math.radians(42)
def arm_axes(sx): return Vector((sx * math.cos(TH), -math.sin(TH), 0)), Vector((sx * math.sin(TH), math.cos(TH), 0))   # along the arm, across it (up and out)
def SH(sx): return Vector((sx * .215, 1.47, 0))
def A(sx, u, v=0, w=0): a, n = arm_axes(sx); return SH(sx) + a * u + n * v + Z * w   # arm space: u from the shoulder, v up and out, w forward
LE, LW, LHN = .30, .57, .62   # elbow, wrist, hand joint along the arm
SLOT = (.70, -.048)   # the hand slot (where a weapon's grip sits), in arm space
KNEE = .53
J = {'hips': (0, 1.0, 0), 'spine': (0, 1.13, 0), 'chest': (0, 1.31, 0), 'head': (0, 1.57, 0), 'top': (0, 2.36, 0)}
for sx, s in ((1, 'l'), (-1, 'r')):
    J['upperarm' + s], J['lowerarm' + s], J['wrist' + s], J['hand' + s], J['handslot' + s] = tuple(A(sx, 0)), tuple(A(sx, LE)), tuple(A(sx, LW)), tuple(A(sx, LHN)), tuple(A(sx, *SLOT))
    J['upperleg' + s], J['lowerleg' + s], J['foot' + s], J['toes' + s] = (sx * .105, .97, 0), (sx * .11, KNEE, .01), (sx * .115, .15, -.01), (sx * .12, .03, .13)
BONES = [('hips', 'spine', None), ('spine', 'chest', 'hips'), ('chest', 'head', 'spine'), ('head', 'top', 'chest')]
for s in 'lr': BONES += [('upperarm' + s, 'lowerarm' + s, 'chest'), ('lowerarm' + s, 'wrist' + s, 'upperarm' + s), ('hand' + s, 'handslot' + s, 'lowerarm' + s), ('handslot' + s, None, 'hand' + s),
                         ('upperleg' + s, 'lowerleg' + s, 'hips'), ('lowerleg' + s, 'foot' + s, 'upperleg' + s), ('foot' + s, 'toes' + s, 'lowerleg' + s), ('toes' + s, None, 'foot' + s)]
# spring chains (not KayKit bones: the game adds them under their parent and swings them): joints + the free end
PONY = [Vector(p) for p in ((0, 2.31, -.2), (0, 2.4, -.47), (0, 2.12, -.7), (0, 1.8, -.69), (0, 1.52, -.6))]
SCARF = [Vector(p) for p in ((.13, 1.58, -.17), (.33, 1.56, -.4), (.55, 1.47, -.62), (.76, 1.36, -.86))]
CHAINS = [dict(b=['pony1', 'pony2', 'pony3', 'pony4'], pts=PONY, parent='head', k=26, d=.9, g=.35), dict(b=['scarf1', 'scarf2', 'scarf3'], pts=SCARF, parent='chest', k=14, d=.86, g=.1)]
for c in CHAINS:
    for i, n in enumerate(c['b']): BONES.append((n, None, c['b'][i - 1] if i else c['parent'])); J[n] = tuple(c['pts'][i])
ALLB = [b[0] for b in BONES]

# ---------------- weights: every part names the bones it follows as a function of the point
def w_torso(p):
    ws, wc, wh = ss(1.06, 1.2, p.y), ss(1.24, 1.38, p.y), ss(1.5, 1.62, p.y)
    return {'hips': 1 - ws, 'spine': ws * (1 - wc), 'chest': wc * (1 - wh), 'head': wc * wh}
def w_arm(sx):
    s = 'l' if sx > 0 else 'r'; a, n = arm_axes(sx)
    def f(p):
        u = (p - SH(sx)).dot(a); wl, wh, wc = ss(LE - .055, LE + .055, u), ss(LW - .03, LW + .03, u), (1 - ss(-.06, .07, u)) * .9
        return {'chest': wc, 'upperarm' + s: (1 - wc) * (1 - wl), 'lowerarm' + s: (1 - wc) * wl * (1 - wh), 'hand' + s: (1 - wc) * wl * wh}
    return f
def w_leg(sx):
    s = 'l' if sx > 0 else 'r'
    def f(p):
        wk, wf, wh = 1 - ss(KNEE - .06, KNEE + .06, p.y), 1 - ss(.1, .22, p.y), ss(.9, 1.02, p.y); wt = ss(.07, .17, p.z) * (1 - ss(.1, .2, p.y)) * .7
        return {'hips': wh, 'upperleg' + s: (1 - wh) * (1 - wk), 'lowerleg' + s: wk * (1 - wf), 'foot' + s: wk * wf * (1 - wt), 'toes' + s: wk * wf * wt}
    return f
def w_pelvis(p):
    wh, l, ws = ss(.84, 1.0, p.y), ss(-.05, .05, p.x), ss(1.06, 1.2, p.y)
    return {'hips': wh * (1 - ws), 'spine': wh * ws, 'upperlegl': (1 - wh) * l, 'upperlegr': (1 - wh) * (1 - l)}
def w_skirt(k):   # cloth hanging from the belt: lower down it follows the thigh on its side
    def f(p):
        g, l = k * ss(1.04, .76, p.y), ss(-.1, .1, p.x); return {'hips': 1 - g, 'upperlegl': g * l, 'upperlegr': g * (1 - l)}
    return f
def w_chain(c):   # along a spring chain: each stretch follows its own bone, shared round the joints
    names, pts, parent = c['b'], c['pts'], c['parent']
    def f(p):
        best = None
        for i in range(len(pts) - 1):
            a, b = pts[i], pts[i + 1]; ab = b - a; t = max(0, min(1, (p - a).dot(ab) / ab.dot(ab))); d = (p - (a + ab * t)).length
            if best is None or d < best[0]: best = (d, i, t)
        _, i, t = best
        if t < .3: k = .5 * (1 - t / .3); return {names[i]: 1 - k, (names[i - 1] if i else parent): k}
        if t > .7 and i + 1 < len(names): k = .5 * (t - .7) / .3; return {names[i]: 1 - k, names[i + 1]: k}
        return {names[i]: 1}
    return f
def rigid(b): return lambda p: {b: 1}

# ---------------- building: a Part = one bmesh, corner colours "Col", weights from its skin function
PARTS = []
class Part:
    def __init__(self, name, skin, sharp=42, mesh='body', xf=None):
        self.name, self.skin, self.sharp, self.mesh, self.xf = name, skin, math.radians(sharp), mesh, xf
        self.bm = bmesh.new(); self.cl = self.bm.loops.layers.float_color.new('Col'); self.uvm = self.bm.faces.layers.int.new('uvm'); self.wl = {}
    def V(self, p):
        p = Vector(p); v = self.bm.verts.new(G(*(self.xf(p) if self.xf else p))); return v
    def paint(self, faces, col):
        for f in faces:
            for l in f.loops: l[self.cl] = col(Gi(l.vert.co)) if callable(col) else col
    def F(self, vs, col):
        try: f = self.bm.faces.new(vs)
        except ValueError: return None
        if col is not None: self.paint([f], col)
        return f
    def done(self):
        bm = self.bm; bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        for f in bm.faces: f.smooth = True
        for e in bm.edges:
            if len(e.link_faces) == 2 and e.calc_face_angle(0) > self.sharp: e.smooth = False
        me = bpy.data.meshes.new(self.name); bm.to_mesh(me); bm.free(); ob = bpy.data.objects.new(self.name, me); bpy.context.collection.objects.link(ob)
        for b in ALLB: ob.vertex_groups.new(name=b)
        for v in me.vertices:
            w = self.skin(Gi(v.co)); w = {b: x for b, x in w.items() if x > 2e-3}; s = sum(w.values())
            for b, x in w.items(): ob.vertex_groups[b].add([v.index], x / s, 'REPLACE')
        ob['mesh'] = self.mesh; PARTS.append(ob); return ob

def blob(P, c, r, col, p=2.0, segs=(16, 10), squash=None, keep=None):
    """ellipsoid / rounded box (exponent p) at c with radii r; squash(point) -> point; keep(face centre) -> bool"""
    g = bmesh.ops.create_uvsphere(P.bm, u_segments=segs[0], v_segments=segs[1], radius=1)
    for v in g['verts']:
        n = Vector((v.co.x, v.co.z, -v.co.y)); k = (abs(n.x) ** p + abs(n.y) ** p + abs(n.z) ** p) ** (1 / p) or 1
        q = Vector((n.x / k * r[0], n.y / k * r[1], n.z / k * r[2])) + Vector(c)
        if squash: q = squash(q)
        v.co = G(*(P.xf(q) if P.xf else q))
    faces = list({f for v in g['verts'] for f in v.link_faces})
    if keep:
        dead = [f for f in faces if not keep(Gi(f.calc_center_median()))]; faces = [f for f in faces if f not in set(dead)]; bmesh.ops.delete(P.bm, geom=dead, context='FACES')
    P.paint(faces, col); return faces
def tube(P, pts, rad, col, sides=10, side=None, cols=None, closed=False, caps=True):
    """tube through points; rad = radius per point or (width, thickness); side = the direction the width lies along (one vector or one per point);
    cols = a colour per point (hair locks); closed = a ring"""
    pts = [Vector(p) for p in pts]; n = len(pts); rings = []; ring_of = {}
    for i, p in enumerate(pts):
        t = ((pts[(i + 1) % n] - pts[(i - 1) % n]) if closed else (pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)])).normalized()
        s = side[i] if isinstance(side, list) else side
        s = Vector(s) if s is not None else (Vector((1, 0, 0)) if abs(t.x) < .9 else Vector((0, 0, 1)))
        s = s - t * s.dot(t); s = s.normalized() if s.length > 1e-4 else t.orthogonal().normalized(); w = t.cross(s)
        rw, rt = rad[i] if isinstance(rad[i], tuple) else (rad[i], rad[i])
        ring = [P.V(p + s * math.cos(k / sides * TAU) * rw + w * math.sin(k / sides * TAU) * rt) for k in range(sides)]
        for v in ring: ring_of[v] = i
        rings.append(ring)
    faces = []
    for i in range(n if closed else n - 1):
        r0, r1 = rings[i], rings[(i + 1) % n]
        for k in range(sides): faces.append(P.F((r0[k], r0[(k + 1) % sides], r1[(k + 1) % sides], r1[k]), None))
    if caps and not closed: faces += [P.F(list(reversed(rings[0])), None), P.F(rings[-1], None)]
    for f in faces:
        if f is None: continue
        for l in f.loops: l[P.cl] = cols[ring_of[l.vert]] if cols else (col(Gi(l.vert.co)) if callable(col) else col)
    return rings
def sheet(P, grid, thick, col, out, closed=False, rowcols=None):
    """a cloth surface with thickness: grid[j][i] = points (j down the cloth, i across / around); out(p) = roughly outward; rowcols = colour per row"""
    nj, ni = len(grid), len(grid[0]); g = [[Vector(p) for p in row] for row in grid]; top, bot = [], []; row_of = {}
    for j in range(nj):
        ta, tb = [], []
        for i in range(ni):
            du = g[j][(i + 1) % ni if closed else min(i + 1, ni - 1)] - g[j][(i - 1) % ni if closed else max(i - 1, 0)]; dv = g[min(j + 1, nj - 1)][i] - g[max(j - 1, 0)][i]
            n = du.cross(dv); n = n.normalized() if n.length > 1e-9 else Vector(out(g[j][i])).normalized()
            if n.dot(out(g[j][i])) < 0: n = -n
            a, b = P.V(g[j][i] + n * thick / 2), P.V(g[j][i] - n * thick / 2); row_of[a] = row_of[b] = j; ta.append(a); tb.append(b)
        top.append(ta); bot.append(tb)
    faces = []; q = lambda *vs: faces.append(P.F(vs, None))
    for j in range(nj - 1):
        for i in range(ni if closed else ni - 1):
            i2 = (i + 1) % ni; q(top[j][i], top[j][i2], top[j + 1][i2], top[j + 1][i]); q(bot[j][i], bot[j + 1][i], bot[j + 1][i2], bot[j][i2])
        if not closed: q(top[j][0], top[j + 1][0], bot[j + 1][0], bot[j][0]); q(top[j][-1], bot[j][-1], bot[j + 1][-1], top[j + 1][-1])
    for i in range(ni if closed else ni - 1):
        i2 = (i + 1) % ni; q(top[0][i], bot[0][i], bot[0][i2], top[0][i2]); q(top[-1][i], top[-1][i2], bot[-1][i2], bot[-1][i])
    for f in faces:
        if f is None: continue
        for l in f.loops: l[P.cl] = rowcols[row_of[l.vert]] if rowcols else (col(Gi(l.vert.co)) if callable(col) else col)
def slab(P, pts2d, origin, ax, ay, az, depth, col):
    """a flat polygon (2-D points on the ax / ay plane) with thickness along az"""
    o, ax, ay, az = Vector(origin), Vector(ax), Vector(ay), Vector(az); n = len(pts2d)
    top = [P.V(o + ax * x + ay * y + az * depth / 2) for x, y in pts2d]; bot = [P.V(o + ax * x + ay * y - az * depth / 2) for x, y in pts2d]
    P.F(top, col); P.F(list(reversed(bot)), col)
    for k in range(n): P.F((bot[k], bot[(k + 1) % n], top[(k + 1) % n], top[k]), col)
def crv(pts, n):   # a smooth curve through the points, n samples
    q = [Vector(p) for p in pts]; q = [q[0] * 2 - q[1]] + q + [q[-1] * 2 - q[-2]]; segs = len(q) - 3; out = []
    for k in range(n):
        u = k / (n - 1) * segs; i = min(int(u), segs - 1); t = u - i; p0, p1, p2, p3 = q[i:i + 4]
        out.append(.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    return out
LEAF = (.5, .88, 1, .97, .86, .7, .5, .28, .03)
def lock(P, ctrl, w, t, cols, n=10, centre=None, sidev=None, prof=LEAF, sides=8):
    """a leaf of hair / cloth along a curve: flat (width w, thickness t), the flat face turned away from `centre`; cols(0..1) = colour along it"""
    pts = crv(ctrl, n); pr = [np.interp(i / (n - 1), np.linspace(0, 1, len(prof)), prof) for i in range(n)]; sv = []
    for i, p in enumerate(pts):
        tan = (pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)]).normalized(); o = (p - Vector(centre)).normalized() if centre is not None else Vector(sidev)
        s = tan.cross(o); sv.append(s.normalized() if s.length > .05 else (sv[-1] if sv else X))
    tube(P, pts, [(w * f, t * min(1, f * 1.25)) for f in pr], None, sides=sides, side=sv, cols=[cols(i / (n - 1)) for i in range(n)])
def ring_pts(c, rx, rz, n, tilt=0, yw=0, ph=0):   # an ellipse round the y axis at c: tilt = front lower / back higher, yw = a soft wave
    return [Vector((c[0] + math.sin(k / n * TAU) * rx, c[1] - tilt * math.cos(k / n * TAU) + yw * math.sin(k / n * TAU * 3 + ph), c[2] + math.cos(k / n * TAU) * rz)) for k in range(n)]

# ================= HEAD =================
HC, HR = Vector((0, 1.93, .02)), (.385, .375, .365)
def jaw(q):   # soft cheeks into a small chin
    t = max(0, (HC.y - q.y) / HR[1]); return Vector((q.x * (1 - .3 * t * t), q.y, q.z * (1 - .1 * t) + .03 * t))
FX0, FX1, FY0, FY1, FS = -.34, .34, 1.56, 2.16, 1100   # the painted face: this front rectangle of the skull, pixels per unit
P = Part('skull', rigid('head'), sharp=80)
blob(P, HC, HR, SKIN, p=2.25, segs=(48, 32), squash=jaw)
for f in P.bm.faces:
    ps = [Gi(v.co) for v in f.verts]
    if all(q.z > .13 and FX0 + .012 < q.x < FX1 - .012 and FY0 + .012 < q.y < FY1 - .012 for q in ps): f[P.uvm] = 1
def head_z(x, y, off=0.0):   # the front surface of the skull at (x, y), pushed out by off
    lo, hi = 0.0, .6
    for _ in range(30):
        m = (lo + hi) / 2; n = Vector(((x) / (HR[0]), (y - HC.y) / HR[1], m / HR[2]))   # invert the squash roughly: solve on the squashed surface
        t = max(0, (HC.y - y) / HR[1]); xs = x / (1 - .3 * t * t); zs = (m - .03 * t) / (1 - .1 * t)
        inside = (abs(xs / HR[0]) ** 2.25 + abs((y - HC.y) / HR[1]) ** 2.25 + abs((zs - HC.z) / HR[2]) ** 2.25) < 1
        lo, hi = (m, hi) if inside else (lo, m)
    return lo + off
def onhead(x, y, off=0.0): return Vector((x, y, head_z(x, y, off)))
blob(P, onhead(0, 1.752, -.012), (.022, .02, .024), SKIN, segs=(8, 6))   # a tiny nose
for sx in (1, -1): blob(P, (sx * .372, 1.87, -.02), (.05, .085, .07), SKIN, segs=(10, 8)); blob(P, (sx * .392, 1.87, -.012), (.02, .05, .04), SKIN_D, segs=(8, 6))   # ears
P.done()
P = Part('neck', w_torso); tube(P, [(0, 1.46, -.01), (0, 1.63, .0)], [.078, .074], SKIN_D, sides=12); P.done()

# ---------- hair: a cap over the skull, swept bangs, long side locks, a big high ponytail on its own spring bones
def hc(k): return mix(HAIR_D, HAIR_L, ss(0, .4, k)) if k < .4 else mix(HAIR_L, HAIR, ss(.4, .85, k))   # dark root, a light band, auburn tip
def hc2(k): return mix(HAIR_D, HAIR, ss(0, .5, k)) if k < .5 else mix(HAIR, HAIR_D, ss(.6, 1, k) * .5)
HHC, HHR = Vector((0, 1.955, -.025)), (.425, .415, .43)
def hairline(q):
    t = (q.z - HHC.z) / HHR[2]; return q.y > 1.63 + .47 * ss(.05, .8, t)
P = Part('hair', rigid('head'), sharp=70)
blob(P, HHC, HHR, lambda p: mix(HAIR_D, HAIR, ss(1.6, 2.3, p.y)), segs=(40, 26), keep=hairline)
def bang(x0, y0, x1, y1, x2, y2, w, cf=hc, off=(.045, .05, .04), t=.035):
    lock(P, [onhead(x0, y0, off[0]), onhead((x0 + x1) / 2, (y0 + y1) / 2 + .02, off[0] + .012), onhead(x1, y1, off[1]), onhead(x2, y2, off[2])], w, t, cf, n=10, centre=HC + Vector((0, 0, -.1)))
bang(-.02, 2.3, -.1, 2.12, -.035, 1.925, .082)   # the long lock between the eyes
bang(.07, 2.3, .13, 2.13, .2, 1.985, .09, hc2)
bang(.15, 2.28, .25, 2.11, .305, 1.955, .08)
bang(-.1, 2.3, -.2, 2.12, -.245, 1.975, .085, hc2)
bang(-.17, 2.27, -.29, 2.08, -.325, 1.93, .07)
bang(.0, 2.31, .03, 2.2, .1, 2.05, .07, hc, off=(.05, .075, .07))   # a second layer on top
bang(-.06, 2.31, -.16, 2.2, -.2, 2.07, .065, hc2, off=(.05, .075, .07))
for sx in (1, -1):   # side locks before the ears, down to the scarf
    lock(P, [(sx * .3, 2.16, .2), (sx * .375, 1.98, .17), (sx * .385, 1.8, .15), (sx * .355, 1.63, .17), (sx * .31, 1.52, .2)], .07, .034, hc, n=11, centre=(0, 1.9, -.1))
    lock(P, [(sx * .36, 2.1, .08), (sx * .42, 1.94, .04), (sx * .425, 1.78, .02), (sx * .4, 1.66, .0)], .06, .03, hc2, n=9, centre=(0, 1.9, 0))
    lock(P, [(sx * .2, 2.3, -.12), (sx * .34, 2.25, -.2), (sx * .44, 2.12, -.3), (sx * .5, 2.02, -.4)], .07, .04, hc, n=8, centre=HHC)   # a tuft sticking out at the back
P.done()
P = Part('ponytail', w_chain(CHAINS[0]), sharp=70)
PB = PONY[0]
lock(P, [PB + Vector((0, -.03, .03)), (0, 2.43, -.36), (0, 2.37, -.57), (0, 2.14, -.69), (0, 1.9, -.68), (0, 1.72, -.63)], .15, .11, hc2, n=12, sidev=X, prof=(.5, .85, 1, 1, .9, .7, .4, .1), sides=10)   # the mass
for ox, top, mid, tipy, fx, fz, w, cf in ((-.17, 0, -.02, 1.74, -.2, -.1, .075, hc), (-.1, .03, .02, 1.58, -.08, -.02, .085, hc2), (-.03, .05, .04, 1.48, -.02, .05, .09, hc), (.05, .05, .04, 1.55, .06, .0, .09, hc2),
                                         (.12, .03, .02, 1.66, .14, -.08, .085, hc), (.18, 0, -.02, 1.82, .24, -.14, .07, hc2), (.0, .08, .08, 1.68, .0, -.2, .08, hc), (-.07, -.05, -.1, 1.9, -.16, .12, .06, hc2), (.08, -.05, -.1, 1.96, .18, .1, .06, hc)):
    lock(P, [PB + Vector((ox * .3, 0, 0)), (ox * .8, 2.42 + top, -.37), (ox * 1.15, 2.36 + top, -.58 - mid), (ox * 1.3, 2.13 + top * .5, -.7 - mid), (ox * 1.35 + fx * .4, (2.13 + tipy) / 2, -.7 - mid + fz * .4), (ox * 1.4 + fx, tipy, -.63 + fz)],
         w, .04, cf, n=12, centre=(0, 2.0, -.45))
tube(P, [PB + Vector((math.sin(k / 14 * TAU) * .092, math.cos(k / 14 * TAU) * .075 * .8 + .012, math.cos(k / 14 * TAU) * .075 * .6 - .035)) for k in range(14)], [.032] * 14, CREAM, sides=8, closed=True)   # the tie
P.done()

# ================= SCARF: two loose wraps round the neck, a knot behind her left shoulder, two tails blown back (spring bones) =================
P = Part('scarf', rigid('chest'), sharp=60)
tube(P, ring_pts((0, 1.5, .0), .225, .185, 28, tilt=.03, yw=.012), [(.075, .062)] * 28, lambda p: mix(TEAL_D, TEAL, ss(1.42, 1.56, p.y)), sides=10, side=Y, closed=True)
tube(P, ring_pts((0, 1.578, -.005), .185, .158, 28, tilt=.035, yw=.01, ph=1.3), [(.06, .052)] * 28, lambda p: mix(TEAL, TEAL_L, ss(1.55, 1.64, p.y)), sides=10, side=Y, closed=True)
blob(P, SCARF[0] + Vector((-.01, -.01, .01)), (.075, .07, .07), TEAL_D, segs=(10, 8))
P.done()
P = Part('scarf_tails', w_chain(CHAINS[1]), sharp=60)
def tail(pts, half, col, col2, fork):   # a cloth strip: sheet 3 wide with a forked torn end
    c = crv(pts, 12); side = Vector((.25, .93, .28)).normalized(); grid = []
    for i, p in enumerate(c):
        h = half * (.6 + .5 * ss(0, .45, i / 11)); wob = Vector((0, .018 * math.sin(i * 1.4), .03 * math.sin(i * 1.1 + 1)))
        grid.append([p + wob - side * h, p + wob * 1.6 + (c[min(i + 1, 11)] - c[max(i - 1, 0)]).normalized().cross(side) * h * .22, p + wob + side * h])
    d = (c[-1] - c[-2]).normalized(); grid.append([c[-1] - side * half * .85 + d * fork, c[-1] + d * fork * .25, c[-1] + side * half * .7 + d * fork * .75])
    sheet(P, grid, .022, None, lambda p: (-.5, .2, -.8), rowcols=[mix(col, col2, ss(0, 12, j)) for j in range(13)])
tail([SCARF[0], SCARF[1] + Vector((0, .03, 0)), SCARF[2] + Vector((0, .02, 0)), SCARF[3]], .1, TEAL, TEAL_L, .1)
tail([SCARF[0] + Vector((-.02, -.05, 0)), SCARF[1] + Vector((-.03, -.1, .03)), SCARF[2] + Vector((-.08, -.17, .07)), SCARF[3] + Vector((-.2, -.2, .16))], .085, TEAL_D, TEAL, .09)
P.done()

# ================= BODY =================
TOR = ((1.0, .168, .128, 0), (1.07, .152, .116, 0), (1.14, .145, .11, 0), (1.22, .156, .118, .005), (1.3, .172, .13, .012), (1.38, .185, .138, .016), (1.44, .19, .134, .01), (1.5, .168, .115, 0), (1.545, .105, .088, -.005), (1.575, .07, .07, -.01))
def tor_at(y):   # half width, half depth, z offset of the torso at height y
    ys = [r[0] for r in TOR]; return tuple(float(np.interp(y, ys, [r[k] for r in TOR])) for k in (1, 2, 3))
P = Part('blouse', w_torso, sharp=60)
tube(P, [(0, y, zo) for y, _, _, zo in TOR], [(hx, hz) for _, hx, hz, _ in TOR], grad(CREAM, CREAM_D, 1.5, 1.1), sides=20, side=X)
P.done()
P = Part('bodice', w_torso, sharp=50)   # the brown leather bodice with gold buttons
ys = [1.1, 1.14, 1.2, 1.26, 1.32, 1.38, 1.43]
tube(P, [(0, y, tor_at(y)[2]) for y in ys], [(tor_at(y)[0] + .016, tor_at(y)[1] + .016) for y in ys], grad(LEATH_L, LEATH, 1.43, 1.12), sides=20, side=X)
for y in (1.105, 1.425): tube(P, ring_pts((0, y, tor_at(y)[2]), tor_at(y)[0] + .02, tor_at(y)[1] + .02, 24), [.012] * 24, LEATH_D, sides=6, closed=True)   # rolled edges
slab(P, [(-.022, 1.11), (.022, 1.11), (.022, 1.42), (-.022, 1.42)], (0, 0, tor_at(1.3)[1] + tor_at(1.3)[2] + .012), X, Y, Z, .02, LEATH_D)   # the button band
for y in (1.185, 1.265, 1.345): blob(P, (0, y, tor_at(y)[1] + tor_at(y)[2] + .03), (.02, .02, .012), GOLD, segs=(10, 6))
for sx in (1, -1):   # side seams
    tube(P, [(sx * (tor_at(y)[0] * .72 + .012), y, tor_at(y)[2] + tor_at(y)[1] * .72 + .014) for y in ys], [.006] * len(ys), LEATH_D, sides=5)
P.done()
P = Part('belt', w_torso, sharp=50)
tube(P, [(0, 1.03, 0), (0, 1.075, 0), (0, 1.115, 0)], [(.183, .143), (.176, .137), (.168, .13)], BELT, sides=22, side=X)
slab(P, [(-.062, -.05), (.062, -.05), (.062, .05), (-.062, .05)], (0, 1.074, .146), X, Y, Z, .028, GOLD)   # buckle
slab(P, [(-.036, -.026), (.036, -.026), (.036, .026), (-.036, .026)], (0, 1.074, .158), X, Y, Z, .012, BELT)
slab(P, [(-.008, -.03), (.008, -.03), (.008, .03), (-.008, .03)], (.0, 1.074, .166), X, Y, Z, .008, GOLD_D)
for sx in (1, -1): slab(P, [(-.012, -.045), (.012, -.045), (.012, .045), (-.012, .045)], (sx * .105, 1.074, .121), Vector((1, 0, -sx * .45)).normalized(), Y, Vector((sx * .45, 0, 1)).normalized(), .012, LEATH_D)   # belt loops
P.done()
P = Part('pouch', rigid('hips'), sharp=50)   # on her right hip
PC = Vector((-.19, .955, .055))
blob(P, PC, (.062, .072, .05), LEATH_L, p=3.2, segs=(14, 10)); blob(P, PC + Vector((-.004, .03, .004)), (.067, .05, .054), LEATH, p=3.2, segs=(14, 8))
blob(P, PC + Vector((-.03, -.01, .05)), (.016, .02, .01), GOLD, p=3, segs=(8, 6))
tube(P, [PC + Vector((0, .06, -.01)), PC + Vector((.01, .1, -.02))], [(.022, .008), (.022, .008)], LEATH_D, sides=6, side=Z)
P.done()
P = Part('shorts', w_pelvis, sharp=60)
blob(P, (0, .955, 0), (.178, .12, .14), SHORTS, p=2.6, segs=(20, 12))
P.done()
P = Part('skirt', w_skirt(.5), sharp=50)   # a short flared cream skirt, open in front where the tabard hangs
NI, grid, rowc = 44, [], []
for j in range(7):
    v = j / 6; row = []
    for i in range(NI + 1):
        ph = math.radians(30 + 300 * i / NI); pl = 1 + .05 * v * math.cos(ph * 8); rx, rz = (.176 + .1 * v ** .85) * pl, (.138 + .1 * v ** .85) * pl
        row.append((math.sin(ph) * rx, 1.05 - .255 * v + .014 * v * math.cos(ph * 8 + 1), math.cos(ph) * rz - .01 * v))
    grid.append(row); rowc.append(mix(CREAM, CREAM_D, v * .5) if j < 6 else LEATH)
sheet(P, grid, .016, None, lambda p: (p.x, 0, p.z), rowcols=rowc)
P.done()
P = Part('tabard', w_skirt(.38), sharp=50)   # the teal pointed tabard with a cream border
for hw, tip, zo, col, th in ((.108, .6, .0, CREAM, .014), (.082, .645, .012, None, .014)):
    grid = []
    for j in range(8):
        y = 1.05 - (1.05 - tip) * j / 7; k = min(1, (y - tip) / .13); w = hw * (k if k < 1 else 1) + .003
        grid.append([(w * (i / 3 - 1), y, .136 + (1.05 - y) * .2 + zo - .5 * (w * (i / 3 - 1)) ** 2) for i in range(7)])
    sheet(P, grid, th, col or grad(TEAL_L, TEAL_D, 1.05, .62), lambda p: (0, .2, 1))
P.done()
P = Part('pack', lambda p: {'chest': .8, 'spine': .2}, sharp=45)   # a small leather backpack with a bedroll on top
BC = Vector((0, 1.265, -.24))
blob(P, BC, (.15, .165, .105), grad(LEATH_L, LEATH, 1.4, 1.12), p=3.4, segs=(20, 14))
blob(P, BC + Vector((0, .075, -.008)), (.158, .1, .112), LEATH, p=3.4, segs=(20, 10))   # the flap
slab(P, [(-.018, -.07), (.018, -.07), (.018, .05), (-.018, .05)], BC + Vector((0, .02, -.117)), X, Y, Z, .012, LEATH_D)   # its strap and buckle
slab(P, [(-.03, -.026), (.03, -.026), (.03, .026), (-.03, .026)], BC + Vector((0, -.045, -.124)), X, Y, Z, .012, GOLD)
for sx in (1, -1): blob(P, BC + Vector((sx * .155, -.06, 0)), (.04, .075, .07), LEATH, p=3, segs=(10, 8))   # side pockets
tube(P, [(-.19, 1.475, -.235), (.19, 1.475, -.235)], [.06, .06], lambda p: mix(TEAL_D, TEAL, ss(1.42, 1.53, p.y)), sides=14)   # the bedroll
for sx in (1, -1):
    tube(P, [(sx * .19, 1.475, -.235), (sx * .2, 1.475, -.235)], [.05, .03], CREAM_D, sides=14)
    tube(P, [Vector((sx * .1, 1.475 + math.cos(k / 12 * TAU) * .066, -.235 + math.sin(k / 12 * TAU) * .066)) for k in range(12)], [(.014, .008)] * 12, LEATH_D, sides=6, side=X, closed=True)
    # shoulder straps: over the shoulder and down the front to the bodice
    sp = [(sx * .1, 1.4, -.14), (sx * .115, 1.535, -.09), (sx * .125, 1.555, .02), (sx * .135, 1.49, .105), (sx * .145, 1.4, .135), (sx * .15, 1.3, .13)]
    lock(P, sp, .024, .012, lambda k: LEATH_D, n=14, centre=(0, 1.38, 0), prof=(1, 1, 1, 1), sides=6)
P.done()

for sx, s in ((1, 'l'), (-1, 'r')):
    a, n = arm_axes(sx)
    P = Part('arm' + s, w_arm(sx), sharp=60)
    tube(P, [A(sx, u) for u in (-.02, .1, .2, LE, .37)], [.064, .062, .058, .055, .056], SKIN, sides=12, side=Z)
    blob(P, A(sx, .06, .012), (.125, .118, .118), grad(CREAM, CREAM_D, 1.56, 1.36), segs=(16, 12), squash=lambda q, sx=sx: SH(sx) + (q - SH(sx)) if True else q)   # the puff sleeve
    tube(P, [A(sx, .178), A(sx, .215)], [.078, .07], CREAM_D, sides=12, side=Z)   # its gathered cuff
    us = (.35, .4, .46, .52, LW, .6)
    tube(P, [A(sx, u) for u in us], [.07, .066, .062, .058, .056, .058], grad(LEATH_L, LEATH, 1.3, 1.0), sides=12, side=Z)   # the long glove
    tube(P, [A(sx, .345), A(sx, .365)], [.076, .075], LEATH_D, sides=12, side=Z)
    for u in (.41, .47, .53): tube(P, [A(sx, u - .011), A(sx, u + .011)], [.0705 - (u - .35) * .07] * 2, LEATH_D, sides=12, side=Z)   # wraps
    P.done()
    P = Part('hand' + s, rigid('hand' + s), sharp=60)   # a soft fist round the hand slot: glove over the palm, bare fingers
    blob(P, A(sx, .655, -.012), (.062, .06, .064), LEATH, p=2.6, segs=(12, 10), squash=None)
    blob(P, A(sx, .7, -.05, .0), (.05, .046, .062), SKIN, p=2.6, segs=(12, 10))
    blob(P, A(sx, .668, -.04, .066), (.034, .034, .03), SKIN, segs=(8, 6))   # thumb
    P.done()
    P = Part('leg' + s, w_leg(sx), sharp=60)
    tube(P, [(sx * .105, 1.0, 0), (sx * .106, .9, 0), (sx * .108, .76, .004), (sx * .11, .6, .008), (sx * .11, KNEE, .01), (sx * .112, .42, -.004), (sx * .114, .3, -.01)], [.1, .106, .098, .084, .078, .08, .07], SKIN, sides=14, side=X)
    tube(P, [(sx * .106, .97, 0), (sx * .107, .9, 0), (sx * .108, .8, .003)], [.112, .114, .108], SHORTS, sides=14, side=X)   # shorts leg
    tube(P, [(sx * .108, .805, .003), (sx * .108, .785, .003)], [.112, .11], C(0x4a4856), sides=14, side=X)
    if sx < 0:   # a strap with a gold buckle on her right thigh
        tube(P, [(sx * .109, .715, .005), (sx * .109, .675, .005)], [.103, .1], LEATH_D, sides=14, side=X)
        slab(P, [(-.026, -.024), (.026, -.024), (.026, .024), (-.026, .024)], (sx * .12, .695, .106), X, Y, Z, .014, GOLD)
        slab(P, [(-.013, -.012), (.013, -.012), (.013, .012), (-.013, .012)], (sx * .12, .695, .114), X, Y, Z, .006, LEATH_D)
    # boot: shaft, a thick fur cuff, a chunky foot with a toe cap, heel and sole, a buckled ankle strap
    tube(P, [(sx * .111, .47, .0), (sx * .112, .38, -.004), (sx * .114, .26, -.01), (sx * .115, .15, -.012)], [.098, .093, .085, .084], grad(LEATH_L, LEATH, .5, .15), sides=14, side=X)
    for k in range(9): blob(P, (sx * .111 + math.sin(k / 9 * TAU) * .085, .478 + .012 * math.sin(k * 2.3), math.cos(k / 9 * TAU) * .085), (.052, .046, .052), FUR if k % 2 else mix(FUR, CREAM_D, .35), segs=(8, 6))
    tube(P, [(sx * .114, .225, -.01), (sx * .114, .19, -.011)], [.094, .093], LEATH_D, sides=14, side=X)
    slab(P, [(-.024, -.022), (.024, -.022), (.024, .022), (-.024, .022)], (sx * .114 + sx * .096, .2075, -.008), Z, Y, X * sx, .014, GOLD)
    slab(P, [(-.011, -.01), (.011, -.01), (.011, .01), (-.011, .01)], (sx * .114 + sx * .104, .2075, -.008), Z, Y, X * sx, .006, LEATH_D)
    blob(P, (sx * .117, .09, .03), (.092, .085, .15), LEATH, p=2.5, segs=(14, 10), keep=lambda q: q.y > .02)
    blob(P, (sx * .118, .075, .125), (.094, .07, .085), LEATH_L, p=2.3, segs=(14, 10), keep=lambda q: q.y > .02)   # toe cap
    blob(P, (sx * .117, .028, .035), (.1, .03, .168), SOLE, p=3.5, segs=(14, 6)); blob(P, (sx * .116, .05, -.075), (.082, .05, .06), SOLE, p=3.5, segs=(10, 6))
    P.done()

# ================= WEAPONS: built in hand-slot space (grip at 0; KayKit: slot x = world -x, slot y = forward, slot z = up in the bind pose) =================
def slot_xf(s):   # the same re-binding the game does (rigTripo): KayKit's hand -> slot direction turned onto hers
    sx = 1 if s == 'l' else -1; kd = Vector((sx * .096, -.058, 0)).normalized(); md = (Vector(J['handslot' + s]) - Vector(J['hand' + s])).normalized()
    R = kd.rotation_difference(md).to_matrix(); KK = Matrix(((-1, 0, 0), (0, 0, 1), (0, 1, 0)))   # columns: slot x, y, z in game axes
    return lambda p: Vector(J['handslot' + s]) + R @ (KK @ Vector(p))
P = Part('sword', rigid('handslotr'), sharp=25, mesh='sword', xf=slot_xf('r'))   # blade along slot +y, guard along x, flat faces +-z
tube(P, [(0, -.105, 0), (0, .075, 0)], [.021, .021], LEATH_D, sides=8)
for y in (-.07, -.03, .01, .05): tube(P, [(0, y - .008, 0), (0, y + .008, 0)], [.0245, .0245], LEATH, sides=8)
blob(P, (0, -.13, 0), (.034, .032, .034), GOLD, segs=(10, 8))
blob(P, (0, .095, 0), (.125, .026, .03), GOLD, p=3, segs=(16, 8));
for sxx in (1, -1): blob(P, (sxx * .125, .105, 0), (.03, .034, .03), GOLD_D, segs=(8, 6))
for sz in (1, -1): blob(P, (0, .095, sz * .028), (.022, .022, .012), TEAL_L, segs=(8, 6))
def blade(P, y0, y1, ytip, w0, w1, th, edge, core):   # a diamond-section blade with a bright bevel
    prof = [(y0, w0), ((y0 + y1) / 2, (w0 + w1) / 2 * 1.02), (y1, w1), (ytip, .002)]; L, R_, T, B = [], [], [], []
    for y, w in prof: L.append(P.V((-w, y, 0))); R_.append(P.V((w, y, 0))); T.append(P.V((0, y, th * (w / w0) ** .5))); B.append(P.V((0, y, -th * (w / w0) ** .5)))
    for i in range(len(prof) - 1):
        for a_, b_, c in ((L, T, edge), (T, R_, core), (R_, B, edge), (B, L, core)): P.F((a_[i], b_[i], b_[i + 1], a_[i + 1]), c)
    P.F((L[0], B[0], R_[0], T[0]), core)
blade(P, .11, .74, .9, .058, .044, .017, STEEL_L, STEEL)
slab(P, [(-.012, .13), (.012, .13), (.008, .66), (-.008, .66)], (0, 0, 0), X, Y, Z, .04, STEEL_D)   # the fuller
P.done()
P = Part('bow', rigid('handslotl'), sharp=40, mesh='bow', xf=slot_xf('l'))   # KayKit bow: long axis = slot z, the string on the -x side
def limb(sgn):
    c = crv([(0, 0, sgn * .07), (.035, 0, sgn * .26), (.0, 0, sgn * .52), (-.13, 0, sgn * .76), (-.2, 0, sgn * .84)], 12)
    tube(P, c, [(.03 - .016 * i / 11, .024 - .01 * i / 11) for i in range(12)], None, sides=8, side=Y, cols=[mix(WOOD, WOOD_D, ss(0, 11, i)) if i < 10 else GOLD for i in range(12)])
limb(1); limb(-1)
tube(P, [(0, 0, -.085), (0, 0, .085)], [.03, .03], TEAL_D, sides=10, side=Y)
for z in (-.09, .09): tube(P, [(0, 0, z - .012), (0, 0, z + .012)], [.034, .034], GOLD, sides=10, side=Y)
tube(P, [(-.2, 0, -.84), (-.2, 0, .84)], [.005, .005], C(0xf4ead0), sides=5, side=Y)   # the string
P.done()

# ================= one mesh, the atlas, the bake =================
for o in bpy.data.objects: o.select_set(False)
for o in PARTS: o.select_set(True)
MID = {'body': 0, 'sword': 1, 'bow': 2}
for o in PARTS:   # remember which output mesh a face belongs to
    a = o.data.attributes.new('mid', 'INT', 'FACE'); a.data.foreach_set('value', [MID[o['mesh']]] * len(o.data.polygons))
bpy.context.view_layer.objects.active = PARTS[0]; bpy.ops.object.join(); ALL = PARTS[0]; ALL.name = 'all'; me = ALL.data
print('joined:', len(me.vertices), 'verts', len(me.polygons), 'faces')
paint = bpy.data.materials.new('paint'); paint.use_nodes = True; nt = paint.node_tree; bsdf = nt.nodes['Principled BSDF']; bsdf.inputs['Roughness'].default_value = .75
att = nt.nodes.new('ShaderNodeAttribute'); att.attribute_name = 'Col'; nt.links.new(att.outputs['Color'], bsdf.inputs['Base Color'])
me.materials.append(paint)

def face_picture():
    """her face, painted flat (the skull's front rectangle): big amber eyes with dark lashes, brows, blush, a small smile"""
    K = 3; W_, H_ = int((FX1 - FX0) * FS) * K, int((FY1 - FY0) * FS) * K; im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0))
    px = lambda x, y: ((x - FX0) * FS * K, (FY1 - y) * FS * K); u = FS * K
    blush = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(blush)
    for sx in (1, -1):
        cx, cy = px(sx * .222, 1.752); d.ellipse((cx - .075 * u, cy - .036 * u, cx + .075 * u, cy + .036 * u), fill=(255, 128, 118, 105))
    im.alpha_composite(blush.filter(ImageFilter.GaussianBlur(.02 * u)))
    for sx in (1, -1):
        S = int(.36 * u); e = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(e); c = S / 2; rx, ry = .07 * u, .098 * u
        ell = lambda cx, cy, a, b, **k: d.ellipse((cx - a, cy - b, cx + a, cy + b), **k)
        ell(c, c, rx, ry, fill=(255, 250, 244, 255))   # white
        iris = Image.new('RGBA', (S, S), (0, 0, 0, 0)); g = np.zeros((S, S, 4), np.uint8); yy = np.linspace(0, 1, S)[:, None]; t = np.clip((yy * S - (c - ry)) / (2 * ry), 0, 1)
        top, botc = np.array((62, 28, 16)), np.array((236, 150, 62)); g[..., :3] = (top * (1 - t ** 1.5) + botc * t ** 1.5)[:, None, :].repeat(S, 1).reshape(S, S, 3) if False else (top[None, None, :] * (1 - t[..., None] ** 1.5) + botc[None, None, :] * t[..., None] ** 1.5).repeat(S, 1)
        g[..., 3] = 255; iris = Image.fromarray(g, 'RGBA'); m = Image.new('L', (S, S), 0); md = ImageDraw.Draw(m); md.ellipse((c - rx * .86, c - ry * .9 + ry * .06, c + rx * .86, c + ry * .98), fill=255)
        wm = Image.new('L', (S, S), 0); ImageDraw.Draw(wm).ellipse((c - rx, c - ry, c + rx, c + ry), fill=255); m = Image.composite(m, Image.new('L', (S, S), 0), wm)
        ring = Image.new('RGBA', (S, S), (58, 26, 14, 255)); rm = Image.new('L', (S, S), 0); ImageDraw.Draw(rm).ellipse((c - rx * .93, c - ry * .9 + ry * .06 - rx * .07, c + rx * .93, c + ry * .98 + rx * .07), fill=255); rm = Image.composite(rm, Image.new('L', (S, S), 0), wm)
        e.paste(ring, (0, 0), rm); e.paste(iris, (0, 0), m); d = ImageDraw.Draw(e)
        ell(c, c - ry * .08, rx * .4, ry * .42, fill=(34, 14, 8, 255))   # pupil
        glow = Image.new('RGBA', (S, S), (0, 0, 0, 0)); ImageDraw.Draw(glow).ellipse((c - rx * .5, c + ry * .4, c + rx * .5, c + ry * .9), fill=(255, 214, 130, 150)); glow = glow.filter(ImageFilter.GaussianBlur(.008 * u)); e.alpha_composite(Image.composite(glow, Image.new('RGBA', (S, S), (0, 0, 0, 0)), m)); d = ImageDraw.Draw(e)
        ell(c + rx * .34, c - ry * .42, rx * .3, rx * .3, fill=(255, 255, 255, 255)); ell(c - rx * .36, c + ry * .3, rx * .14, rx * .14, fill=(255, 255, 255, 235))   # glints (same side on both eyes)
        lash = (40, 18, 12, 255); pts_o, pts_i = [], []   # the upper lash: a thick band along the top, a flick at the outer corner
        for k in range(25):
            a_ = math.pi * (1.06 - 1.12 * k / 24); th = .2 + .1 * math.sin(k / 24 * math.pi)
            pts_o.append((c + math.cos(a_) * rx * 1.1 * sx * -1 * -1, c - math.sin(a_) * ry * (1.02 + th * .5))); pts_i.append((c + math.cos(a_) * rx * 1.02, c - math.sin(a_) * ry * (.98 - th * .5)))
        d.polygon(pts_o + pts_i[::-1], fill=lash)
        ox = c + sx * rx * 1.02; d.polygon([(ox - sx * rx * .1, c - ry * .2), (ox + sx * rx * .42, c - ry * .5), (ox + sx * rx * .04, c + ry * .1)], fill=lash)   # outer flick
        d.arc((c - rx, c - ry, c + rx, c + ry), 20 if sx > 0 else 100, 80 if sx > 0 else 160, fill=(120, 62, 44, 255), width=int(.007 * u))   # a short lower line at the outer side
        e = e.rotate(sx * 5, resample=Image.BICUBIC); cx, cy = px(sx * .158, 1.862); im.alpha_composite(e, (int(cx - c), int(cy - c)))
    d = ImageDraw.Draw(im); brow = (92, 44, 26, 255)
    for sx in (1, -1):   # brows: thin, a confident tilt
        p = [px(sx * .075, 2.005), px(sx * .16, 2.03), px(sx * .245, 2.012), px(sx * .245, 2.0), px(sx * .16, 2.012), px(sx * .078, 1.99)]; d.polygon(p, fill=brow)
    m0, m1, m2 = px(-.042, 1.668), px(0, 1.652), px(.05, 1.676)   # a small smile, one corner higher
    d.line([m0, px(-.02, 1.657), m1, px(.028, 1.66), m2], fill=(150, 62, 48, 255), width=int(.0085 * u), joint='curve')
    d.ellipse((m2[0] - .006 * u, m2[1] - .006 * u, m2[0] + .006 * u, m2[1] + .006 * u), fill=(150, 62, 48, 255)); d.ellipse((m0[0] - .005 * u, m0[1] - .005 * u, m0[0] + .005 * u, m0[1] + .005 * u), fill=(150, 62, 48, 255))
    return im.resize((W_ // K, H_ // K), Image.LANCZOS)

def setup_render(views, size=(520, 680)):
    sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 24; sc.cycles.use_denoising = False
    w = bpy.data.worlds.get('pw') or bpy.data.worlds.new('pw'); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes['Background']; bg.inputs[0].default_value = (.42, .5, .62, 1); bg.inputs[1].default_value = .85
    sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN')); sun.data.energy = 2.2; sun.data.angle = .3; sun.rotation_euler = (math.radians(50), 0, math.radians(35)); sc.collection.objects.link(sun)
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); cam.data.type = 'ORTHO'; sc.collection.objects.link(cam); sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = size; sc.render.film_transparent = False; tiles = []
    for name, ang, el, ctr, scale in views:
        cam.data.ortho_scale = scale; d = Vector((math.sin(math.radians(ang)) * math.cos(math.radians(el)), math.sin(math.radians(el)), math.cos(math.radians(ang)) * math.cos(math.radians(el))))
        cam.location = G(*(Vector(ctr) + d * 8)); cam.rotation_euler = (G(*d)).to_track_quat('Z', 'Y').to_euler()
        sc.render.filepath = f'/tmp/_adv_{name}.png'; bpy.ops.render.render(write_still=True); tiles.append(Image.open(sc.render.filepath).convert('RGB'))
    bpy.data.objects.remove(sun); bpy.data.objects.remove(cam); return tiles
VIEWS = [('front', 0, 8, (0, 1.25, 0), 2.9), ('q', 38, 14, (0, 1.25, 0), 2.9), ('side', 90, 8, (0, 1.25, -.1), 2.9), ('back', 205, 14, (0, 1.25, -.1), 2.9), ('face', 12, 4, (0, 1.9, 0), 1.25)]
def montage(tiles, path):
    W_ = sum(t.width for t in tiles); im = Image.new('RGB', (W_, tiles[0].height)); x = 0
    for t in tiles: im.paste(t, (x, 0)); x += t.width
    im.save(path); print('preview', path)

if FAST:
    if PREVIEW: montage(setup_render(VIEWS), PREVIEW)
    sys.exit(0)

# ---- UVs: the face rectangle straight from the front, everything else unwrapped into the rest of the atlas
TS = 2048; FU0, FV1 = 6 / TS, 1 - 6 / TS; FW, FH = (FX1 - FX0) * FS / TS, (FY1 - FY0) * FS / TS; REST = FV1 - FH - 10 / TS   # the face block sits top left, the rest fills the band under it
me.uv_layers.new(name='UVMap'); bpy.context.view_layer.objects.active = ALL; bpy.ops.object.mode_set(mode='EDIT'); bm = bmesh.from_edit_mesh(me); uvm = bm.faces.layers.int['uvm']
for f in bm.faces: f.select = f[uvm] == 0
bmesh.update_edit_mesh(me)
bpy.ops.uv.smart_project(angle_limit=math.radians(62), island_margin=.0025, area_weight=0, correct_aspect=False, scale_to_bounds=False)
bm = bmesh.from_edit_mesh(me); uvl = bm.loops.layers.uv.verify(); uvm = bm.faces.layers.int['uvm']
for f in bm.faces:
    if f[uvm] == 0:
        for l in f.loops: l[uvl].uv.y /= REST   # stretch, pack into the square without turning, squeeze back = islands keep their shape inside the band
bmesh.update_edit_mesh(me); bpy.ops.uv.pack_islands(rotate=False, margin=.0025)
bm = bmesh.from_edit_mesh(me); uvl = bm.loops.layers.uv.verify(); uvm = bm.faces.layers.int['uvm']
for f in bm.faces:
    for l in f.loops:
        if f[uvm] == 0: l[uvl].uv.y *= REST
        else: q = Gi(l.vert.co); l[uvl].uv = (FU0 + (q.x - FX0) / (FX1 - FX0) * FW, FV1 - FH + (q.y - FY0) / (FY1 - FY0) * FH)
bmesh.update_edit_mesh(me); bpy.ops.object.mode_set(mode='OBJECT')

sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.use_denoising = False
w = bpy.data.worlds.new('w'); sc.world = w; w.light_settings.distance = .3
img = bpy.data.images.new('bake', TS, TS, alpha=False, float_buffer=True); tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = img; nt.nodes.active = tex
for o in bpy.data.objects: o.select_set(False)
ALL.select_set(True); bpy.context.view_layer.objects.active = ALL; sc.render.bake.margin = 10; sc.render.bake.use_clear = True
def baked(kind, samples, **kw):
    sc.cycles.samples = samples; bpy.ops.object.bake(type=kind, **kw); a = np.empty(TS * TS * 4, np.float32); img.pixels.foreach_get(a); return a.reshape(TS, TS, 4)[::-1, :, :3].copy()
col = baked('DIFFUSE', 1, pass_filter={'COLOR'}); ao = baked('AO', 96)[..., 0]
srgb = lambda a: np.where(a <= .0031308, a * 12.92, 1.055 * np.clip(a, 0, 1) ** (1 / 2.4) - .055)
colim = Image.fromarray((np.clip(srgb(col), 0, 1) * 255).astype(np.uint8), 'RGB').convert('RGBA')
face = face_picture(); os.makedirs(SRC, exist_ok=True); face.save(f'{SRC}/face.png'); colim.alpha_composite(face, (int(FU0 * TS), int((1 - FV1) * TS)))
aoim = np.asarray(Image.fromarray((np.clip(ao, 0, 1) * 255).astype(np.uint8), 'L').filter(ImageFilter.GaussianBlur(1.6)), np.float32) / 255
k = np.clip((aoim - .08) / .8, 0, 1) ** .9; shade = np.array((.5, .36, .46), np.float32)   # shadows lean to a warm violet, not grey
out = np.asarray(colim.convert('RGB'), np.float32) / 255 * (shade[None, None, :] + (1 - shade[None, None, :]) * k[..., None])
Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), 'RGB').save(f'{SRC}/atlas.png'); print('atlas', f'{SRC}/atlas.png')

final = bpy.data.materials.new('adventurer'); final.use_nodes = True; fnt = final.node_tree; fb = fnt.nodes['Principled BSDF']; fb.inputs['Roughness'].default_value = .7; fb.inputs['Metallic'].default_value = 0
ft = fnt.nodes.new('ShaderNodeTexImage'); ft.image = bpy.data.images.load(os.path.abspath(f'{SRC}/atlas.png')); fnt.links.new(ft.outputs['Color'], fb.inputs['Base Color'])
me.materials.clear(); me.materials.append(final); me.color_attributes.remove(me.color_attributes['Col'])
if PREVIEW: montage(setup_render(VIEWS), PREVIEW)

# ---- split into the output meshes, the armature at her joints, export
outs = []
for name, mid in MID.items():
    o = ALL.copy(); o.data = ALL.data.copy(); o.name = name; o.data.name = name; bpy.context.collection.objects.link(o); b2 = bmesh.new(); b2.from_mesh(o.data); lay = b2.faces.layers.int['mid']
    bmesh.ops.delete(b2, geom=[f for f in b2.faces if f[lay] != mid], context='FACES'); bmesh.ops.delete(b2, geom=[v for v in b2.verts if not v.link_faces], context='VERTS'); b2.to_mesh(o.data); b2.free()
    for an in ('mid', 'uvm'):
        if an in o.data.attributes: o.data.attributes.remove(o.data.attributes[an])
    outs.append(o); print(name, len(o.data.vertices), 'verts', len(o.data.polygons), 'faces')
bpy.data.objects.remove(ALL)
arm = bpy.data.armatures.new('rig'); rig = bpy.data.objects.new('rig', arm); bpy.context.collection.objects.link(rig)
for o in bpy.data.objects: o.select_set(False)
rig.select_set(True); bpy.context.view_layer.objects.active = rig; bpy.ops.object.mode_set(mode='EDIT')
TIP = {c['b'][i]: c['pts'][i + 1] for c in CHAINS for i in range(len(c['b']))}
for name, tail, parent in BONES:
    b = arm.edit_bones.new(name); b.head = G(*J[name]); t = G(*J[tail]) if tail else (G(*TIP[name]) if name in TIP else b.head + Vector((0, 0, .08)))
    if name in ('handl', 'handr'): b.head = G(*J['wrist' + name[-1]])
    if (t - b.head).length < 1e-3: t = b.head + Vector((0, 0, .08))
    b.tail = t
for name, tail, parent in BONES:
    if parent: arm.edit_bones[name].parent = arm.edit_bones[parent]
bpy.ops.object.mode_set(mode='OBJECT')
for o in outs: o.parent = rig; m = o.modifiers.new('rig', 'ARMATURE'); m.object = rig
rig['joints'] = json.dumps({k: [round(c, 4) for c in v] for k, v in J.items()})
rig['chains'] = json.dumps([dict(b=c['b'], tip=[round(v, 4) for v in c['pts'][-1]], k=c['k'], d=c['d'], g=c['g']) for c in CHAINS])
for o in bpy.data.objects: o.select_set(False)
for o in outs + [rig]: o.select_set(True)
props = bpy.ops.export_scene.gltf.get_rna_type().properties.keys(); kw = dict(filepath=OUT, export_format='GLB', use_selection=True, export_image_format='JPEG', export_animations=False, export_extras=True)
kw['export_image_quality' if 'export_image_quality' in props else 'export_jpeg_quality'] = 90
if 'export_vertex_color' in props: kw['export_vertex_color'] = 'NONE'
bpy.ops.export_scene.gltf(**kw); print('wrote', OUT, os.path.getsize(OUT) // 1024, 'KB')
