# Last Signal · Step 1: make the Meshy model light and ready for Mixamo
# Blender: Scripting tab > Open > this file > Run Script (the play button)
# Uses the newest .glb in your Downloads folder.
# Writes Downloads/storm_mixamo.fbx (upload this to mixamo.com) and Downloads/storm_basecolor.png
import bpy, os, glob

TARGET_FACES = 20000      # low poly for phones
TEX_SIZE = 1024           # texture size
HEIGHT = 1.8              # metres

DL = os.path.join(os.path.expanduser('~'), 'Downloads')
glbs = glob.glob(os.path.join(DL, '*.glb'))
if not glbs:
    raise Exception('No .glb file in ' + DL)
src = max(glbs, key=os.path.getmtime)
print('source:', src)

if bpy.context.object and bpy.context.object.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

bpy.ops.import_scene.gltf(filepath=src)
meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
if not meshes:
    raise Exception('No mesh in ' + src)
for o in bpy.context.scene.objects:
    o.select_set(o in meshes)
bpy.context.view_layer.objects.active = meshes[0]
bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
if len(meshes) > 1:
    bpy.ops.object.join()
ob = bpy.context.view_layer.objects.active
for o in list(bpy.data.objects):
    if o is not ob:
        bpy.data.objects.remove(o, do_unlink=True)
ob.select_set(True)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# fewer polygons
n = len(ob.data.polygons)
if n > TARGET_FACES:
    m = ob.modifiers.new('LS_decimate', 'DECIMATE')
    m.ratio = TARGET_FACES / n
    bpy.ops.object.modifier_apply(modifier=m.name)
print('faces:', n, '->', len(ob.data.polygons))

# standing on the floor, centred, 1.8 m tall
xs = [v.co.x for v in ob.data.vertices]
ys = [v.co.y for v in ob.data.vertices]
zs = [v.co.z for v in ob.data.vertices]
k = HEIGHT / (max(zs) - min(zs))
cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
ob.scale = (k, k, k)
ob.location = (-cx * k, -cy * k, -min(zs) * k)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# keep only the colour texture, shrink it, save it next to the FBX
mat = ob.active_material
if mat and mat.use_nodes:
    tree = mat.node_tree
    bsdf = next((nd for nd in tree.nodes if nd.type == 'BSDF_PRINCIPLED'), None)
    base = None
    for l in tree.links:
        if bsdf and l.to_node == bsdf and l.to_socket.name == 'Base Color' and l.from_node.type == 'TEX_IMAGE':
            base = l.from_node
    for nd in list(tree.nodes):
        if nd is not base and nd.type in ('TEX_IMAGE', 'NORMAL_MAP', 'SEPARATE_COLOR', 'SEPRGB', 'SEPARATE_RGB'):
            tree.nodes.remove(nd)
    if bsdf:
        bsdf.inputs['Metallic'].default_value = 0.0
        bsdf.inputs['Roughness'].default_value = 0.8
    if base and base.image:
        img = base.image
        w, h = img.size
        if w > TEX_SIZE:
            img.scale(TEX_SIZE, max(1, round(TEX_SIZE * h / w)))
        bpy.context.scene.view_settings.view_transform = 'Standard'
        out = os.path.join(DL, 'storm_basecolor.png')
        img.save_render(out)
        base.image = bpy.data.images.load(out, check_existing=False)
        print('texture:', out)

for o in bpy.data.objects:
    o.select_set(o is ob)
fbx = os.path.join(DL, 'storm_mixamo.fbx')
bpy.ops.export_scene.fbx(filepath=fbx, use_selection=True, object_types={'MESH'},
                         path_mode='COPY', embed_textures=True, apply_scale_options='FBX_SCALE_UNITS')
print('DONE ->', fbx, round(os.path.getsize(fbx) / 1e6, 2), 'MB')
