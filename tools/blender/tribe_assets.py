# Stone-age props for tribe3d.html, modelled in Blender by script (headless, runs in the cloud session).
#   pip install bpy            (Blender 5.3 as a Python module, once per session)
#   python3 tools/blender/tribe_assets.py [out folder, default art/tribe3d/models]
# Every model: low-poly, flat shaded, colours painted per face into the vertex colours (sRGB), origin on the ground,
# front = Blender -Y (= +Z in three.js), 1 unit = 1 world unit of the game (8 game pixels). Exported as .glb.
import bpy, bmesh, math, random, sys, os
from mathutils import Vector, Matrix, noise

OUT = sys.argv[1] if len(sys.argv) > 1 else 'art/tribe3d/models'
os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)

def hexc(h): return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
def mul(c, k): return tuple(max(0., min(1., v * k)) for v in c)
def mix(a, b, t): return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))
def jit(c, a): return mul(c, 1 + random.uniform(-a, a))

class Model:
    def __init__(self, name):
        self.name, self.bm = name, bmesh.new()
        self.col = self.bm.loops.layers.color.new('Col')
    def part(self, make):
        before = set(self.bm.faces); ret = make(self.bm)
        faces = [f for f in self.bm.faces if f not in before]
        verts = list({v for f in faces for v in f.verts})
        return verts, faces
    def paint(self, faces, fn):
        self.bm.normal_update()
        for f in faces:
            c = fn(f)
            for l in f.loops: l[self.col] = (c[0], c[1], c[2], 1.)
    def export(self):
        me = bpy.data.meshes.new(self.name); self.bm.normal_update(); self.bm.to_mesh(me); self.bm.free()
        for p in me.polygons: p.use_smooth = False
        ob = bpy.data.objects.new(self.name, me); bpy.context.scene.collection.objects.link(ob)
        ca = me.color_attributes
        if len(ca): ca.active_color = ca[0]; ca.render_color_index = 0
        bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True); bpy.context.view_layer.objects.active = ob
        path = os.path.join(OUT, self.name + '.glb')
        bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_vertex_color='ACTIVE', export_materials='NONE', export_normals=True, export_texcoords=False)
        bpy.data.objects.remove(ob); print(self.name, len(me.polygons), 'faces ->', path)

def lumpy(verts, centre, amp, freq, seed):
    for v in verts:
        n = (v.co - centre); n = n.normalized() if n.length > 1e-6 else Vector((0, 0, 1))
        v.co += n * noise.noise(v.co * freq + Vector((seed, seed * .7, seed * 1.3))) * amp

def shade_by_normal(base, top=1.18, bottom=.72, a=.06):
    def fn(f):
        z = f.normal.z
        k = 1 + (top - 1) * max(0, z) - (1 - bottom) * max(0, -z)
        return jit(mul(base, k), a)
    return fn

def cone(m, r1, r2, h, z0, seg, x=0, y=0, caps=True):
    return m.part(lambda bm: bmesh.ops.create_cone(bm, cap_ends=caps, cap_tris=False, segments=seg, radius1=r1, radius2=r2, depth=h, matrix=Matrix.Translation((x, y, z0 + h / 2))))
def ico(m, r, at, sub=1):
    return m.part(lambda bm: bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=r, matrix=Matrix.Translation(at)))
def box(m, sx, sy, sz, at, rot=None):
    mat = Matrix.Translation(at) @ (rot or Matrix.Identity(4)) @ Matrix.Diagonal((sx, sy, sz, 1))
    return m.part(lambda bm: bmesh.ops.create_cube(bm, size=1, matrix=mat))
def rod(m, a, b, r, seg=6):   # a cylinder from point a to point b
    a, b = Vector(a), Vector(b); d = b - a
    rot = d.to_track_quat('Z', 'Y').to_matrix().to_4x4()
    return m.part(lambda bm: bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=r, radius2=r * .85, depth=d.length, matrix=Matrix.Translation((a + b) / 2) @ rot))
def arc(m, radius, tube, angle_z, at=(0, 0, 0), seg=6, steps=12, span=math.pi):   # half ring standing up (tusks, arches)
    def make(bm):
        c = bmesh.ops.create_circle(bm, cap_ends=False, segments=seg, radius=tube, matrix=Matrix.Translation((radius, 0, 0)))   # circle in XY: its normal follows the sweep round Y
        geom = c['verts'] + list({e for v in c['verts'] for e in v.link_edges})
        bmesh.ops.spin(bm, geom=geom, cent=(0, 0, 0), axis=(0, 1, 0), angle=-span, steps=steps, use_duplicate=False)
        vs = list({v for v in bm.verts if v.is_valid})
        return {}
    before_v = set(m.bm.verts)
    v, f = m.part(make)
    allv = [x for x in m.bm.verts if x not in before_v]
    rot = Matrix.Translation(at) @ Matrix.Rotation(angle_z, 4, 'Z')
    bmesh.ops.transform(m.bm, matrix=rot, verts=allv)
    bmesh.ops.reverse_faces(m.bm, faces=f)   # the sweep leaves the tube inside-out
    return allv, f

BARK, BARK2 = hexc('#7a5236'), hexc('#5e3e28')
LEAF, PINE = hexc('#5ca83f'), hexc('#2f7a55')
STRAW, STRAW2, POLE, DARK = hexc('#d1ab6c'), hexc('#b48b52'), hexc('#6b4a2e'), hexc('#24160c')
HIDE, HIDE2, IVORY, STONE = hexc('#9a7656'), hexc('#7e5c40'), hexc('#efe6cf'), hexc('#8d8984')

def tree_broad(i):
    random.seed(100 + i); m = Model(f'tree_broad_{i}')
    v, f = cone(m, .42, .24, 2.9, 0, 7)
    for x in v: x.co.x += .14 * (x.co.z / 2.9) ** 2 * (1 if i % 2 else -1)
    m.paint(f, lambda f: jit(BARK if f.normal.z < .5 else BARK2, .08))
    rv, rf = rod(m, (0, 0, 2.0), (.8, .3, 2.9), .12, 5); m.paint(rf, lambda f: jit(BARK, .08))
    blobs = [((0, 0, 3.9), 1.9), ((.95, .45, 4.8), 1.35), ((-.9, -.55, 4.4), 1.25), ((.2, -.85, 3.5), 1.15), ((-.4, .8, 3.6), 1.05)]
    for k, (c, r) in enumerate(blobs[:4 + i % 2]):
        v, f = ico(m, r, c, 1); lumpy(v, Vector(c), .22 * r, 1.1, i * 7 + k)   # 20 faces a blob: chunky + light for phones
        m.paint(f, shade_by_normal(mix(LEAF, hexc('#7cbf4a'), random.random() * .5), 1.22, .66, .07))
    return m

def tree_pine(i):
    random.seed(200 + i); m = Model(f'tree_pine_{i}')
    v, f = cone(m, .3, .2, 2.2, 0, 6); m.paint(f, lambda f: jit(BARK2, .08))
    for k in range(4):
        r, h, z = 2.35 - k * .52, 2.3 - k * .2, 1.25 + k * 1.2
        v, f = cone(m, r, .06, h, z, 9)
        for x in v:
            if x.co.z < z + .05:
                a = 1 + random.uniform(-.14, .14); x.co.x *= a; x.co.y *= a; x.co.z -= random.uniform(0, .35)
        m.paint(f, shade_by_normal(mul(PINE, 1 + k * .05), 1.25, .62, .06))
    return m

def rock(i):
    random.seed(300 + i); m = Model(f'rock_{i}')
    v, f = ico(m, 1, (0, 0, 0), 2); lumpy(v, Vector((0, 0, 0)), .32, 1.4, 30 + i)
    for x in v: x.co.x *= 1.25; x.co.z = x.co.z * .68 + .42
    moss = hexc('#6f8a4a')
    m.paint(f, lambda f: jit(mix(STONE, moss, .55) if f.normal.z > .78 and random.random() < .55 else mul(STONE, .85 + .3 * max(0, f.normal.z)), .07))
    return m

def hut_cone():
    random.seed(400); m = Model('hut_cone')
    v, f = cone(m, 3.1, .25, 5.3, 0, 12)
    m.paint(f, lambda f: jit(STRAW if int(f.calc_center_median().z / .9) % 2 else STRAW2, .06))
    for (z, r1, r2, h) in [(.05, 3.32, 2.55, 1.45), (1.55, 2.6, 1.72, 1.35), (2.95, 1.78, .95, 1.2)]:   # thatch layers with ragged bottoms
        v, f = cone(m, r1, r2, h, z, 12, caps=False)
        for x in v:
            if x.co.z < z + .05: x.co.z -= random.uniform(0, .3); s = 1 + random.uniform(-.06, .08); x.co.x *= s; x.co.y *= s
        m.paint(f, lambda f: jit(STRAW, .08))
    for a in (0, 1.6, 3.2, 4.7):   # crossed poles at the top
        _, f = rod(m, (math.cos(a) * .2, math.sin(a) * .2, 4.3), (math.cos(a) * .9, math.sin(a) * .9, 6.4), .09, 5); m.paint(f, lambda f: jit(POLE, .08))
    _, f = box(m, 1.35, .9, 2.0, (0, -2.35, 1.0)); m.paint(f, lambda f: DARK)                       # doorway
    for sx in (-.78, .78): _, f = rod(m, (sx, -2.55, 0), (sx * .8, -2.4, 2.3), .11, 5); m.paint(f, lambda f: jit(POLE, .06))
    _, f = box(m, .7, .08, 1.5, (.45, -2.72, 1.15), Matrix.Rotation(.25, 4, 'Z')); m.paint(f, lambda f: jit(hexc('#c08a5a'), .05))   # hide flap
    for k in range(12):
        a = k / 12 * math.tau
        if abs(math.sin(a) + 1) < .35: continue   # gap at the door
        _, f = ico(m, .32 + random.random() * .12, (math.cos(a) * 3.15, math.sin(a) * 3.15, .15), 1); m.paint(f, lambda f: jit(STONE, .1))
    return m

def hut_bone():
    random.seed(500); m = Model('hut_bone')
    v, f = m.part(lambda bm: bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=8, radius=3.0))
    bmesh.ops.delete(m.bm, geom=[x for x in v if x.co.z < -.01], context='VERTS')
    f = [x for x in f if x.is_valid]
    m.paint(f, lambda f: jit(HIDE if noise.noise(f.calc_center_median() * .9 + Vector((3, 1, 2))) > -.1 else HIDE2, .07))
    for a in (-.75, 0, .75):    # mammoth tusks arching over the dome
        _, f = arc(m, 3.15, .2, math.pi / 2 + a, steps=14); m.paint(f, lambda f: jit(IVORY, .05))
    _, f = arc(m, 1.15, .17, 0, at=(0, -2.85, 0), steps=10); m.paint(f, lambda f: jit(IVORY, .05))   # entrance arch
    _, f = box(m, 1.4, 1.0, 1.8, (0, -2.6, .9)); m.paint(f, lambda f: DARK)
    _, f = box(m, .9, .6, .55, (0, -.4, 3.05)); m.paint(f, lambda f: jit(IVORY, .04))                   # skull on top
    return m

def campfire():
    random.seed(600); m = Model('campfire')
    for k in range(10):
        a = k / 10 * math.tau
        v, f = ico(m, .42 + random.random() * .12, (math.cos(a) * 2.0, math.sin(a) * 2.0, .2), 1); lumpy(v, Vector((math.cos(a) * 2.0, math.sin(a) * 2.0, .2)), .1, 2, k)
        m.paint(f, lambda f: jit(STONE, .1))
    for k in range(5):
        a = k / 5 * math.tau
        _, f = rod(m, (math.cos(a) * 1.25, math.sin(a) * 1.25, .1), (math.cos(a) * .15, math.sin(a) * .15, 1.4), .17, 6)
        m.paint(f, lambda f: jit(hexc('#e0c090') if abs(f.normal.z) > .8 else BARK, .06))
    v, f = m.part(lambda bm: bmesh.ops.create_circle(bm, cap_ends=True, segments=12, radius=1.5, matrix=Matrix.Translation((0, 0, .03))))
    m.paint(f, lambda f: hexc('#3a3330'))
    return m


def tube(m, pts, radii, seg=6, cap=True):   # a ring at every point, joined into a bent tapered tube (trunks, tusks, tails)
    bm = m.bm; before = set(bm.faces); rings = []; pts = [Vector(p) for p in pts]
    for i, p in enumerate(pts):
        d = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        up = Vector((0, 0, 1)) if abs(d.z) < .9 else Vector((1, 0, 0))
        a = d.cross(up).normalized(); b = d.cross(a).normalized()
        rings.append([bm.verts.new(p + (a * math.cos(t) + b * math.sin(t)) * radii[i]) for t in [k / seg * math.tau for k in range(seg)]])
    for i in range(len(rings) - 1):
        r0, r1 = rings[i], rings[i + 1]
        for k in range(seg): bm.faces.new((r0[k], r0[(k + 1) % seg], r1[(k + 1) % seg], r1[k]))
    if cap: bm.faces.new(list(reversed(rings[0]))); bm.faces.new(rings[-1])
    faces = [f for f in bm.faces if f not in before]
    bmesh.ops.recalc_face_normals(bm, faces=faces)
    return [v for r in rings for v in r], faces
def scaled_ico(m, r, at, sc, sub=2, amp=0., seed=0):
    v, f = ico(m, r, (0, 0, 0), sub)
    if amp: lumpy(v, Vector((0, 0, 0)), amp, 1.6, seed)
    for x in v: x.co = Vector((x.co.x * sc[0], x.co.y * sc[1], x.co.z * sc[2])) + Vector(at)
    return v, f
GRASS1, GRASS2, WOOD, WOOD2, ROPE = hexc('#8fae4c'), hexc('#7a9a3e'), hexc('#8a6238'), hexc('#6e4a2a'), hexc('#c9b07a')

def ragged(v, z, drop=.3, s=.07):
    for x in v:
        if x.co.z < z + .05: x.co.z -= random.uniform(0, drop); k = 1 + random.uniform(-s, s); x.co.x *= k; x.co.y *= k

def hut_dome():
    random.seed(700); m = Model('hut_dome')
    v, f = m.part(lambda bm: bmesh.ops.create_uvsphere(bm, u_segments=14, v_segments=8, radius=2.9))
    bmesh.ops.delete(m.bm, geom=[x for x in v if x.co.z < -.01], context='VERTS'); f = [x for x in f if x.is_valid]
    m.paint(f, lambda f: jit(GRASS2, .06))
    for (z, r1, r2, h) in [(.05, 3.2, 2.75, 1.25), (1.15, 2.85, 2.05, 1.1), (2.1, 2.15, .95, .95)]:
        v, f = cone(m, r1, r2, h, z, 14, caps=False); ragged(v, z, .28)
        m.paint(f, lambda f: jit(GRASS1 if random.random() < .6 else GRASS2, .07))
    v, f = cone(m, .45, .1, .9, 2.9, 6); m.paint(f, lambda f: jit(ROPE, .05))
    _, f = box(m, 1.3, .9, 1.75, (0, -2.45, .87)); m.paint(f, lambda f: DARK)
    for sx in (-.75, .75): _, f = rod(m, (sx, -2.75, 0), (sx * .85, -2.55, 1.95), .1, 5); m.paint(f, lambda f: jit(POLE, .06))
    return m

def longhouse():
    random.seed(800); m = Model('longhouse')
    for side in (-1, 1):                                     # log walls
        for k, z in enumerate((.4, 1.15, 1.9)):
            _, f = rod(m, (side * 2.9, -5.4, z), (side * 2.9, 5.4, z), .4, 7); m.paint(f, lambda f: jit(hexc('#d9b98a') if abs(f.normal.y) > .8 else (WOOD if k % 2 else WOOD2), .07))
    for end in (-1, 1):                                      # plank ends
        for k in range(7):
            x = -2.6 + k * .87
            if end < 0 and abs(x) < .6: continue
            _, f = box(m, .8, .25, 2.4 + (1.6 - abs(x) * .55), (x, end * 5.4, (2.4 + (1.6 - abs(x) * .55)) / 2)); m.paint(f, lambda f: jit(WOOD if k % 2 else WOOD2, .06))
    _, f = box(m, 1.3, .4, 2.0, (0, -5.35, 1.0)); m.paint(f, lambda f: DARK)
    for side in (-1, 1):                                     # thatch roof slabs with ragged eaves
        rot = Matrix.Rotation(side * math.radians(40), 4, 'Y')
        v, f = box(m, 4.4, 12.2, .4, (side * 1.55, 0, 3.85), rot)
        for x in v:
            if x.co.z < 3.0: x.co.z -= random.uniform(0, .25)
        m.paint(f, lambda f: jit(STRAW if int((f.calc_center_median().y + 6) / 1.3) % 2 else STRAW2, .06))
    _, f = rod(m, (0, -6.2, 5.25), (0, 6.2, 5.25), .2, 6); m.paint(f, lambda f: jit(POLE, .05))
    for end in (-1, 1):
        for sx in (-1, 1): _, f = rod(m, (0, end * 6.0, 5.0), (sx * .9, end * 6.1, 6.2), .1, 5); m.paint(f, lambda f: jit(POLE, .05))
    return m

def totem():
    random.seed(900); m = Model('totem')
    cols = [hexc('#b5523b'), hexc('#e0b04a'), hexc('#3f8f7a'), hexc('#7a3fb0')]
    for i, c in enumerate(cols):
        z = .05 + i * 1.32; r = .78 - i * .06
        _, f = cone(m, r, r * .92, 1.25, z, 8); m.paint(f, lambda f, c=c: jit(mul(c, .8) if abs(f.normal.z) > .8 else c, .05))
        _, f = cone(m, r * 1.04, r * 1.04, .12, z + 1.18, 8); m.paint(f, lambda f: hexc('#2a1a10'))
        for sx in (-.3, .3):
            _, f = box(m, .26, .12, .2, (sx, -r * .97, z + .8)); m.paint(f, lambda f: hexc('#f4efe2'))
            _, f = box(m, .12, .1, .12, (sx, -r * 1.03, z + .8)); m.paint(f, lambda f: hexc('#140c08'))
        _, f = box(m, .3, .4 + (i == 3) * .4, .25, (0, -r - .15 - (i == 3) * .2, z + .45)); m.paint(f, lambda f, c=c: jit(mul(c, .75), .04))
    _, f = box(m, 4.2, .35, .8, (0, 0, 5.6)); m.paint(f, lambda f: jit(cols[1], .05))
    for sx in (-1.9, -1.3, 1.3, 1.9): _, f = box(m, .4, .3, .5, (sx, 0, 5.05)); m.paint(f, lambda f: jit(cols[0], .05))
    return m

def watchtower():
    random.seed(1000); m = Model('watchtower')
    for (a, b) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        _, f = rod(m, (a * 1.65, b * 1.65, 0), (a * 1.35, b * 1.35, 7.0), .2, 6); m.paint(f, lambda f: jit(WOOD2, .06))
    for (p, q) in (((-1.6, -1.6, .6), (1.4, -1.4, 6.0)), ((1.6, -1.6, .6), (-1.4, -1.4, 6.0)), ((-1.6, 1.6, .6), (1.4, 1.4, 6.0)), ((1.6, 1.6, .6), (-1.4, 1.4, 6.0))):
        _, f = rod(m, p, q, .09, 5); m.paint(f, lambda f: jit(WOOD, .06))
    for k in range(6): _, f = box(m, 3.7, .6, .25, (0, -1.55 + k * .62, 7.05)); m.paint(f, lambda f, k=k: jit(WOOD if k % 2 else WOOD2, .05))
    for (a, b) in ((-1, -1), (1, -1), (-1, 1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)):
        _, f = rod(m, (a * 1.7, b * 1.7, 7.1), (a * 1.7, b * 1.7, 8.0), .07, 4); m.paint(f, lambda f: jit(WOOD2, .05))
    for (p, q) in (((-1.7, -1.7, 7.9), (1.7, -1.7, 7.9)), ((-1.7, 1.7, 7.9), (1.7, 1.7, 7.9)), ((-1.7, -1.7, 7.9), (-1.7, 1.7, 7.9)), ((1.7, -1.7, 7.9), (1.7, 1.7, 7.9))):
        _, f = rod(m, p, q, .07, 4); m.paint(f, lambda f: jit(ROPE, .05))
    for (z, r1, r2, h) in [(8.6, 2.9, 1.6, 1.0), (9.4, 1.8, .2, 1.6)]:
        v, f = cone(m, r1, r2, h, z, 10, caps=(z > 9)); ragged(v, z, .25); m.paint(f, lambda f: jit(STRAW, .07))
    for (a, b) in ((-1, -1), (1, -1), (-1, 1), (1, 1)): _, f = rod(m, (a * 1.6, b * 1.6, 7.1), (a * 1.6, b * 1.6, 8.7), .08, 4); m.paint(f, lambda f: jit(WOOD2, .05))
    for sx in (-.45, .45): _, f = rod(m, (sx, -2.6, 0), (sx, -1.75, 7.0), .07, 4); m.paint(f, lambda f: jit(WOOD, .05))
    for k in range(9):
        t = (k + .5) / 9; _, f = rod(m, (-.45, -2.6 + .85 * t, 7 * t), (.45, -2.6 + .85 * t, 7 * t), .05, 4); m.paint(f, lambda f: jit(WOOD, .05))
    return m

def rack():
    random.seed(1100); m = Model('rack')
    for sx in (-1.7, 1.7):
        _, f = rod(m, (sx, 0, 0), (sx, 0, 2.6), .12, 5); m.paint(f, lambda f: jit(WOOD2, .05))
        _, f = rod(m, (sx, 0, 2.3), (sx + (.25 if sx > 0 else -.25), 0, 2.8), .08, 4); m.paint(f, lambda f: jit(WOOD2, .05))
    _, f = rod(m, (-1.9, 0, 2.55), (1.9, 0, 2.55), .09, 5); m.paint(f, lambda f: jit(WOOD, .05))
    for k, (x, c) in enumerate(((-.95, '#c08a5a'), (0, '#9a6a44'), (.95, '#d8b48a'))):
        v, f = box(m, .85, .08, 1.5, (x, 0, 1.75))
        for q in v:
            if q.co.z < 1.1: q.co.z -= random.uniform(0, .25)
        m.paint(f, lambda f, c=c: jit(hexc(c), .07))
    for x in (-1.35, 1.35):
        _, f = scaled_ico(m, .3, (x, 0, 1.9), (.35, .5, 1.3), 1); m.paint(f, lambda f: jit(hexc('#9ab0b8'), .08))
    return m

def woodpile():
    random.seed(1200); m = Model('woodpile')
    for row in range(3):
        for k in range(4 - row):
            x = (k - (3 - row) / 2) * .62; z = .3 + row * .52
            _, f = rod(m, (x, -1.2, z), (x, 1.2, z), .29, 7); m.paint(f, lambda f: jit(hexc('#e3c79a') if abs(f.normal.y) > .8 else (WOOD if k % 2 else WOOD2), .07))
    _, f = rod(m, (1.6, -.6, 0), (1.3, -.5, 1.4), .06, 4); m.paint(f, lambda f: jit(WOOD, .05))
    _, f = scaled_ico(m, .22, (1.3, -.5, 1.4), (1.6, .6, .9), 1); m.paint(f, lambda f: jit(STONE, .05))
    return m

def stonepile():
    random.seed(1300); m = Model('stonepile')
    for k, (x, y, z, r) in enumerate(((-.6, 0, .3, .55), (.5, .2, .3, .6), (0, -.6, .3, .5), (.1, .5, .3, .45), (-.1, 0, .85, .5), (.55, -.4, .75, .35), (-.55, .45, .7, .35))):
        v, f = scaled_ico(m, r, (x, y, z), (1.2, 1, .8), 1, .08, k); m.paint(f, lambda f: jit(mul(STONE, .9 + .2 * max(0, f.normal.z)), .08))
    return m

def palisade_log():
    random.seed(1400); m = Model('palisade_log')
    _, f = cone(m, .42, .4, 3.4, 0, 7); m.paint(f, lambda f: jit(WOOD2 if random.random() < .5 else WOOD, .06))
    _, f = cone(m, .4, .03, 1.0, 3.4, 7); m.paint(f, lambda f: jit(hexc('#d9b98a'), .05))
    _, f = cone(m, .44, .44, .18, 2.6, 7, caps=False); m.paint(f, lambda f: jit(ROPE, .04))
    return m

def cave_mouth():
    random.seed(1500); m = Model('cave_mouth')
    _, f = box(m, 6.2, 1.6, 4.6, (0, .9, 2.3)); m.paint(f, lambda f: hexc('#0c0806'))
    for k in range(11):
        t = k / 10 * math.pi; x, z = math.cos(t) * 3.6, math.sin(t) * 3.9 + .3
        v, f = scaled_ico(m, .85 + random.random() * .35, (x, -.1, z), (1, .9, 1), 1, .18, k); m.paint(f, lambda f: jit(mul(STONE, .8 + .25 * max(0, f.normal.z)), .08))
    for x in (-4.4, 4.6):
        v, f = scaled_ico(m, 1.3, (x, .1, .8), (1, .9, .9), 2, .3, int(x)); m.paint(f, lambda f: jit(mix(STONE, hexc('#6f8a4a'), .5) if f.normal.z > .75 else STONE, .08))
    return m

def mammoth():
    random.seed(1600); m = Model('mammoth')
    FUR, FUR2, FUR3, FEET = hexc('#8a5230'), hexc('#6a3c22'), hexc('#a86a3c'), hexc('#3a2a20')
    furfn = lambda f: jit(FUR3 if f.normal.z > .55 else FUR2 if f.normal.z < -.3 else (FUR if random.random() < .7 else FUR2), .07)
    _, f = scaled_ico(m, 1, (0, .3, 3.2), (1.55, 2.3, 1.45), 2, .08, 1); m.paint(f, furfn)
    _, f = scaled_ico(m, 1, (0, -.7, 4.25), (1.2, 1.1, 1.0), 2, .06, 2); m.paint(f, furfn)
    _, f = scaled_ico(m, 1, (0, -2.25, 4.0), (1.0, .95, 1.1), 2, .05, 3); m.paint(f, furfn)
    _, f = scaled_ico(m, 1, (0, -2.1, 5.0), (.75, .7, .55), 1, 0, 4); m.paint(f, furfn)          # head dome
    for sx in (-1, 1): _, f = scaled_ico(m, .6, (sx * .95, -1.9, 4.05), (.25, .7, .85), 1); m.paint(f, lambda f: jit(FUR2, .06))
    for sx in (-1, 1):
        _, f = box(m, .14, .1, .12, (sx * .55, -3.05, 4.35)); m.paint(f, lambda f: hexc('#140c08'))
    _, f = tube(m, [(0, -3.0, 3.75), (0, -3.6, 3.1), (0, -3.75, 2.1), (0, -3.55, 1.1), (0, -3.15, .7)], [.42, .36, .28, .22, .18], 7); m.paint(f, lambda f: jit(FUR2, .06))
    for sx in (-1, 1):
        _, f = tube(m, [(sx * .5, -2.95, 3.1), (sx * .75, -3.7, 2.3), (sx * .7, -4.35, 2.4), (sx * .35, -4.35, 3.15)], [.17, .15, .11, .05], 6); m.paint(f, lambda f: jit(IVORY, .04))
    for (x, y) in ((-.85, -1.25), (.85, -1.25), (-.8, 1.55), (.8, 1.55)):
        _, f = cone(m, .5, .45, 2.4, .2, 7, x, y); m.paint(f, furfn)
        _, f = cone(m, .55, .55, .25, 0, 7, x, y); m.paint(f, lambda f: jit(FEET, .05))
    _, f = tube(m, [(0, 2.55, 3.7), (0, 2.95, 3.1), (0, 3.0, 2.5)], [.14, .1, .06], 5); m.paint(f, lambda f: jit(FUR2, .05))
    return m

for mk in [lambda: tree_broad(0), lambda: tree_broad(1), lambda: tree_broad(2), lambda: tree_pine(0), lambda: tree_pine(1), lambda: rock(0), lambda: rock(1), lambda: rock(2), hut_cone, hut_bone, campfire, hut_dome, longhouse, totem, watchtower, rack, woodpile, stonepile, palisade_log, cave_mouth, mammoth]:
    mk().export()
