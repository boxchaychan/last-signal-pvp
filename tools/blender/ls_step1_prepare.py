# Last Signal · Step 1: make the Meshy/Tripo model light and ready for Mixamo
# Blender: Scripting tab > Open > this file > Run Script (the play button)
#   or headless: blender -b --factory-startup --python tools/blender/ls_step1_prepare.py
# Uses the newest .glb in your Downloads folder.
# Writes Downloads/storm_mixamo.fbx (upload this to mixamo.com) and Downloads/storm_basecolor.png
#
# How: the model is joined, cleaned (stray objects and any rig that came with it are dropped, Mixamo
# rigs it again), scaled to 1.8 m, then a low-poly copy gets fresh UVs and its colours are baked from
# the full model. Plain decimation on the original UVs cracks the texture (dark lines along UV seams).
import bpy, bmesh, os, glob, math
import numpy as np

TARGET_FACES = 20000      # low poly for phones
TEX_SIZE = 1024           # texture size
HEIGHT = 1.8              # metres

DL = os.path.join(os.path.expanduser('~'), 'Downloads')
glbs = glob.glob(os.path.join(DL, '*.glb'))
if not glbs:
    raise Exception('No .glb file in ' + DL)
src = max(glbs, key=os.path.getmtime)
print('source:', src, flush=True)

sc = bpy.context.scene
if bpy.context.object and bpy.context.object.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

bpy.ops.import_scene.gltf(filepath=src)
meshes = [o for o in sc.objects if o.type == 'MESH']
if not meshes:
    raise Exception('No mesh in ' + src)

# drop stray bits (helper spheres etc.): no material, or tiny next to the biggest mesh
big = max(len(o.data.polygons) for o in meshes)
keep = [o for o in meshes if len(o.data.polygons) >= big * 0.01 and any(o.data.materials)]
if not keep:
    keep = [max(meshes, key=lambda o: len(o.data.polygons))]
print('meshes:', [o.name for o in meshes], '-> keep', [o.name for o in keep], flush=True)
for o in keep:
    for m in list(o.modifiers):
        if m.type == 'ARMATURE':
            o.modifiers.remove(m)
for o in sc.objects:
    o.select_set(o in keep)
bpy.context.view_layer.objects.active = keep[0]
bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
if len(keep) > 1:
    bpy.ops.object.join()
hi = bpy.context.view_layer.objects.active
for o in list(bpy.data.objects):
    if o is not hi:
        bpy.data.objects.remove(o, do_unlink=True)
hi.select_set(True)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# standing on the floor, centred, 1.8 m tall
co = np.empty(len(hi.data.vertices) * 3)
hi.data.vertices.foreach_get('co', co)
co = co.reshape(-1, 3)
lo_, hi_ = co.min(0), co.max(0)
k = HEIGHT / (hi_[2] - lo_[2])
hi.scale = (k, k, k)
hi.location = (-(lo_[0] + hi_[0]) / 2 * k, -(lo_[1] + hi_[1]) / 2 * k, -lo_[2] * k)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# Meshy/Tripo split the mesh along every UV seam; weld it back, or decimation tears holes in it
bm = bmesh.new()
bm.from_mesh(hi.data)
nv = len(bm.verts)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
print('welded verts:', nv, '->', len(bm.verts), flush=True)
bm.to_mesh(hi.data)
bm.free()

# full colour for the bake: no metal (metal has no diffuse colour)
for mat in hi.data.materials:
    if not (mat and mat.node_tree):
        continue
    tree = mat.node_tree
    for l in [l for l in tree.links if l.to_node.type == 'BSDF_PRINCIPLED' and l.to_socket.name == 'Metallic']:
        tree.links.remove(l)
    for nd in tree.nodes:
        if nd.type == 'BSDF_PRINCIPLED':
            nd.inputs['Metallic'].default_value = 0.0

# low-poly copy
lo = hi.copy()
lo.data = hi.data.copy()
lo.name = lo.data.name = 'storm'
sc.collection.objects.link(lo)
n = len(lo.data.polygons)
for o in sc.objects:
    o.select_set(o is lo)
bpy.context.view_layer.objects.active = lo
if n > TARGET_FACES:
    m = lo.modifiers.new('LS_decimate', 'DECIMATE')
    m.ratio = TARGET_FACES / n
    bpy.ops.object.modifier_apply(modifier=m.name)
    # fresh UVs for the low-poly mesh
    while lo.data.uv_layers:
        lo.data.uv_layers.remove(lo.data.uv_layers[0])
    lo.data.uv_layers.new(name='UVMap')
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.004)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()
print('faces:', n, '->', len(lo.data.polygons), flush=True)

# new material: one colour texture
img = bpy.data.images.new('storm_basecolor', TEX_SIZE, TEX_SIZE, alpha=False)
mat = bpy.data.materials.new('storm')
try:
    mat.use_nodes = True
except Exception:
    pass
tree = mat.node_tree
bsdf = next(nd for nd in tree.nodes if nd.type == 'BSDF_PRINCIPLED')
bsdf.inputs['Metallic'].default_value = 0.0
bsdf.inputs['Roughness'].default_value = 0.8
tex = tree.nodes.new('ShaderNodeTexImage')
tex.image = img
tree.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
for nd in tree.nodes:
    nd.select = False
tex.select = True
tree.nodes.active = tex
lo.data.materials.clear()
lo.data.materials.append(mat)

# bake the colours of the full model onto the low-poly one
sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = 1
bk = sc.render.bake
bk.use_pass_direct = False
bk.use_pass_indirect = False
bk.use_pass_color = True
bk.margin = 8
for o in sc.objects:
    o.select_set(o in (hi, lo))
bpy.context.view_layer.objects.active = lo
bpy.ops.object.bake(type='DIFFUSE', pass_filter={'COLOR'}, use_selected_to_active=True,
                    cage_extrusion=0.015, max_ray_distance=0.04, margin=8)
out = os.path.join(DL, 'storm_basecolor.png')
img.filepath_raw = out
img.file_format = 'PNG'
img.save()
print('texture:', out, flush=True)

bpy.data.objects.remove(hi, do_unlink=True)
for o in sc.objects:
    o.select_set(o is lo)
fbx = os.path.join(DL, 'storm_mixamo.fbx')
bpy.ops.export_scene.fbx(filepath=fbx, use_selection=True, object_types={'MESH'},
                         path_mode='COPY', embed_textures=True, apply_scale_options='FBX_SCALE_UNITS')
print('DONE ->', fbx, round(os.path.getsize(fbx) / 1e6, 2), 'MB', flush=True)
