# Cut the owner's Tripo huntress (already rigged by tripo_rig.py) into pieces worn by a KayKit body (owner 2026-11-17 "เอานักธนู KayKit
# มาทับ" -> "ผสมกัน": KayKit archer body + her hood and bow). Faces are sorted by where they sit, their bone weights and their texture colour:
#   TripoHood = the skull-fur hood with horns, gold discs, red feathers (her face, brown hair, braids and scarf are dropped)
#   TripoBow  = her bow + string (everything that follows her left hand, minus the hand itself)
# The pieces keep her coordinates (x10 model units, glTF y up); her joints go into the extras so the game can read them in her bone frames
# and put them on the same bones of any KayKit body (tribe3d.html: tripoParts).
#   pip install bpy ; python3 tools/blender/tripo_parts.py art/tribe3d/people/warrior_f.glb art/tribe3d/gear/huntress_parts.glb
import bpy, bmesh, sys, json
SRC, OUT = sys.argv[-2], sys.argv[-1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
rig = [o for o in bpy.data.objects if o.type == 'ARMATURE'][0]; joints = rig.get('joints')
ob = max([o for o in bpy.data.objects if o.type == 'MESH'], key=lambda o: len(o.data.polygons)); me = ob.data
im = [i for i in bpy.data.images if i.size[0] > 0 and 'ormal' not in i.name][0]; W, H = im.size; PX = im.pixels[:]
uv = me.uv_layers.active.data; gn = {g.index: g.name for g in ob.vertex_groups}

def label(x, y, z, r, g, b, w):
    if w.get('handl', 0) > .95 and not (1.0 < x < 2.05 and 3.75 < y < 4.55):   # her left hand holds the bow: keep the bow, not the hand
        return 'bow' if x > 1.0 or y < 3.0 or y > 5.0 else None
    if y < 6.3: return None
    l = .3 * r + .59 * g + .11 * b
    if l < .3 and y < 6.9: return None   # dark collar under the chin
    skin = r > .7 and .16 < r - b < .5 and .02 < g - b < .22 and g > .5 and l > .55 and y < 8.2 and abs(x) < 1.4
    brown = l < .38 and r >= b - .02 and (y < 8.0 and z > -.7 and abs(x) < 1.55 or y < 6.9)   # hair / braids (the dark inside of the hood stays)
    blue = b > r + .12 and y < 6.7   # the scarf (blue gems on the hood stay)
    face = abs(x) < 1.3 and 6.2 < y < 7.75 and z > .25
    return None if face or skin or brown or blue else 'hood'

lab = []
for p in me.polygons:
    c = ob.matrix_world @ p.center
    u = sum(uv[l].uv.x for l in p.loop_indices) / p.loop_total; v = sum(uv[l].uv.y for l in p.loop_indices) / p.loop_total
    i = (min(H - 1, int(v * H)) * W + min(W - 1, int(u * W))) * 4
    w = {}
    for vi in p.vertices:
        for g in me.vertices[vi].groups: w[gn[g.group]] = w.get(gn[g.group], 0) + g.weight / p.loop_total
    lab.append(label(c.x, c.z, -c.y, *PX[i:i + 3], w))
print({k: lab.count(k) for k in set(lab)})
ob.modifiers.clear(); ob.parent = None; ob.vertex_groups.clear()
outs = []
for name in ('hood', 'bow'):
    o = ob.copy(); o.data = me.copy(); o.name = 'Tripo' + name.capitalize(); o.data.name = o.name; bpy.context.collection.objects.link(o)
    bm = bmesh.new(); bm.from_mesh(o.data); bm.faces.ensure_lookup_table()
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if lab[f.index] != name], context='FACES'); bm.to_mesh(o.data); bm.free()
    print(o.name, len(o.data.polygons), 'faces'); outs.append(o)
for o in list(bpy.data.objects):
    if o not in outs: bpy.data.objects.remove(o)
outs[0]['joints'] = joints
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True, export_image_format='JPEG', export_jpeg_quality=88, export_animations=False, export_extras=True, export_skins=False)
print('wrote', OUT)
