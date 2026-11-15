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
        v, f = ico(m, r, c, 2); lumpy(v, Vector(c), .3 * r, 1.1, i * 7 + k)
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

for mk in [lambda: tree_broad(0), lambda: tree_broad(1), lambda: tree_broad(2), lambda: tree_pine(0), lambda: tree_pine(1), lambda: rock(0), lambda: rock(1), lambda: rock(2), hut_cone, hut_bone, campfire]:
    mk().export()
