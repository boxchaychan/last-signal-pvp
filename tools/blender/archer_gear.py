# Gear for the "นักธนู ★★" (2-star archer) of tribe3d.html, modelled in Blender by script (headless, cloud session):
# longbow (wood limbs, recurve tips with gold caps, leather grip, string), quiver with 5 feathered arrows and a gold rim,
# a red + white feather plume for the hood, a studded leather shoulder pad. Flat colours, low poly like the game.
# Sizes are in KayKit character units (a character is 2.4 tall). Each piece has its origin where it attaches:
#   Bow = grip (limbs along +-Y, the belly bends toward -Z), Quiver = middle (opening at +Y), Plume = base, Pad = shoulder.
#   pip install bpy ; python3 tools/blender/archer_gear.py art/tribe3d/gear/archer_gear.glb
import bpy, bmesh, math, sys
from mathutils import Vector, Matrix
OUT = sys.argv[-1] if sys.argv[-1].endswith('.glb') else 'art/tribe3d/gear/archer_gear.glb'
bpy.ops.wm.read_factory_settings(use_empty=True)

def lin(h):   # sRGB hex -> linear (the game turns glTF colours back to sRGB like its other packs)
    c = [((h >> s) & 255) / 255 for s in (16, 8, 0)]
    return tuple(v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in c)
MATS = {}
def mat(name, h, rough=.75, metal=0.):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*lin(h), 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    MATS[name] = m; return m
WOOD, WOOD2, GRIP, GOLD, STRING = mat('wood', 0xb8803e), mat('wood_dark', 0x8a5a2c), mat('grip', 0x3a2414), mat('gold', 0xf0c040, .35, .6), mat('string', 0xf2ead6)
LEATHER, LEATHER2, RED, WHITE = mat('leather', 0x7a4422), mat('leather_dark', 0x4e2a14), mat('feather_red', 0xd83a24), mat('feather_white', 0xf6f0e4)

def new_obj(name):
    me = bpy.data.meshes.new(name); ob = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(ob); return ob, me
def tube(bm, pts, radii, sides, mi):   # rings swept along points (flat shaded low poly)
    rings = []
    for i, p in enumerate(pts):
        t = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        a = Vector((1, 0, 0)) if abs(t.x) < .9 else Vector((0, 0, 1)); u = t.cross(a).normalized(); w = t.cross(u)
        rings.append([bm.verts.new(p + (u * math.cos(k / sides * 6.283) + w * math.sin(k / sides * 6.283)) * radii[i]) for k in range(sides)])
    for r0, r1 in zip(rings, rings[1:]):
        for k in range(sides): f = bm.faces.new((r0[k], r0[(k + 1) % sides], r1[(k + 1) % sides], r1[k])); f.material_index = mi
    for r, flip in ((rings[0], True), (rings[-1], False)):
        f = bm.faces.new(list(reversed(r)) if flip else r); f.material_index = mi
def blob(bm, c, r, mi, seg=6, ring=4, sc=(1, 1, 1)):
    m = bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=ring, radius=r)
    for v in m['verts']: v.co = Vector((v.co.x * sc[0], v.co.y * sc[1], v.co.z * sc[2])) + Vector(c)
    for f in {f for v in m['verts'] for f in v.link_faces}: f.material_index = mi
def finish(ob, me, bm, mats):
    for m in mats: me.materials.append(m)
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = False

# ---------- longbow
ob, me = new_obj('Bow'); bm = bmesh.new()
N = 18; pts, rad = [], []
for i in range(N + 1):
    t = -1 + 2 * i / N; y = .72 * t; a = abs(t)
    z = -.17 * t * t + (.10 * ((a - .82) / .18) ** 2 if a > .82 else 0)   # bends toward the archer, recurve tips flick out
    pts.append(Vector((0, y, z))); rad.append(.05 - .03 * a)
tube(bm, pts, rad, 6, 0)
tube(bm, [Vector((0, -.11, .0)), Vector((0, .11, .0))], [.062, .062], 6, 2)                       # leather grip wrap
for s in (-1, 1):
    tip = pts[0] if s < 0 else pts[-1]; blob(bm, tip, .045, 3)                                        # gold caps on the tips
    tube(bm, [Vector((0, s * .58, -.17 * .8 ** 2 + .0)), Vector((0, s * .62, -.17 * .86 ** 2))], [.04, .04], 6, 1)   # dark nock bands
tube(bm, [pts[1] + Vector((0, 0, -.01)), pts[-2] + Vector((0, 0, -.01))], [.008, .008], 4, 4)      # string
finish(ob, me, bm, [WOOD, WOOD2, GRIP, GOLD, STRING])

# ---------- quiver with arrows
ob, me = new_obj('Quiver'); bm = bmesh.new()
tube(bm, [Vector((0, -.3, 0)), Vector((0, .28, 0))], [.1, .135], 8, 0)                           # leather body, wider at the mouth
tube(bm, [Vector((0, .25, 0)), Vector((0, .32, 0))], [.148, .148], 8, 3)                           # gold rim
tube(bm, [Vector((0, -.32, 0)), Vector((0, -.24, 0))], [.11, .11], 8, 1)                         # dark bottom band
tube(bm, [Vector((0, .02, 0)), Vector((0, .08, 0))], [.122, .122], 8, 1)                           # strap band
for k, (ox, oz, h) in enumerate([(-.05, .04, .26), (.05, .045, .34), (0, -.04, .3), (-.06, -.045, .22), (.065, -.03, .28)]):
    top = Vector((ox, .3 + h, oz)); tube(bm, [Vector((ox, .1, oz)), top], [.022, .022], 4, 4)     # shaft
    for sgn in (-1, 1):   # two fletchings per arrow
        v0 = bm.verts.new(top + Vector((0, -.02, 0))); v1 = bm.verts.new(top + Vector((sgn * .085, -.04, 0))); v2 = bm.verts.new(top + Vector((sgn * .085, -.19, 0))); v3 = bm.verts.new(top + Vector((0, -.17, 0)))
        f = bm.faces.new((v0, v1, v2, v3)); f.material_index = 5 if k % 2 == 0 else 6   # one-sided: the game draws gear double-sided
finish(ob, me, bm, [LEATHER, LEATHER2, GRIP, GOLD, WOOD2, RED, WHITE])

# ---------- feather plume (two feathers + a gold clasp)
ob, me = new_obj('Plume'); bm = bmesh.new()
def feather(bm, base, direction, length, width, mi, bend):
    d = Vector(direction).normalized(); side = d.cross(Vector((0, 0, 1))).normalized() if abs(d.z) < .9 else Vector((1, 0, 0))
    spine = [Vector(base) + d * length * t + Vector((0, 0, -bend * t * t)) for t in (0, .25, .5, .75, 1)]
    wid = [0, width * .8, width, width * .7, 0]
    L = [bm.verts.new(p - side * w) for p, w in zip(spine, wid)]; R = [bm.verts.new(p + side * w) for p, w in zip(spine, wid)]
    for i in range(4):
        f = bm.faces.new((L[i], L[i + 1], R[i + 1], R[i]) if i else (L[0], L[1], R[1])); f.material_index = mi
feather(bm, (0, 0, 0), (.25, 1, 0), .42, .07, 0, .12)
feather(bm, (.02, 0, -.02), (.55, 1, 0), .34, .06, 1, .1)
blob(bm, (0, .02, 0), .045, 2)
finish(ob, me, bm, [RED, WHITE, GOLD])

# ---------- studded shoulder pad
ob, me = new_obj('Pad'); bm = bmesh.new()
blob(bm, (0, 0, 0), .2, 0, seg=8, ring=5, sc=(1, .6, 1.05))
tube(bm, [Vector((0, -.03, 0)), Vector((0, .01, 0))], [.205, .205], 8, 1)
for a in (-.6, 0, .6): blob(bm, (math.sin(a) * .13, .1, math.cos(a) * .13), .03, 2, seg=5, ring=3)
finish(ob, me, bm, [LEATHER, LEATHER2, GOLD])

bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', export_apply=True)
print('wrote', OUT, [o.name for o in bpy.data.objects])
