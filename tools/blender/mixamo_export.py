# A Tripo GLB (split into parts, textured) -> one FBX for Mixamo's auto-rigger (owner 2026-11-21 "เอาไฟล์ต้นแบบมา ฉันไปเอาท่า mixamo").
# All parts joined into ONE mesh (Mixamo rigs one mesh most reliably), transforms applied, textures EMBEDDED in the FBX, facing the front.
# Also writes an OBJ + MTL + textures zip (Mixamo takes that too, if the FBX textures do not show).
#   pip install bpy
#   python3 tools/blender/mixamo_export.py art/incoming/basebody/tripo_base_v1_tex.glb art/incoming/basebody/mixamo/base_girl_mixamo
import bpy, sys, os, zipfile, glob
SRC, OUT = sys.argv[1], sys.argv[2]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
meshes = [o for o in bpy.data.objects if o.type == 'MESH']
for o in meshes: o.parent = None
for o in bpy.data.objects:
    if o.type != 'MESH': bpy.data.objects.remove(o)
for q in bpy.data.objects: q.select_set(False)
for o in meshes: o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.object.join(); body = bpy.context.view_layer.objects.active; body.name = body.data.name = 'base_girl'
print('faces', len(body.data.polygons), 'materials', len(body.data.materials))
d = OUT + '_obj'; os.makedirs(d, exist_ok=True)
for i, img in enumerate(bpy.data.images):   # textures come packed inside the GLB: write them out so the FBX can embed them and the OBJ can point at them
    if img.size[0] == 0: continue
    fn = os.path.join(d, 'tex_%02d.jpg' % i); img.filepath_raw = fn; img.file_format = 'JPEG'; img.save(); img.unpack(method='USE_ORIGINAL') if img.packed_file else None
print('textures written', len(os.listdir(d)))
bpy.ops.export_scene.fbx(filepath=OUT + '.fbx', use_selection=True, object_types={'MESH'}, path_mode='COPY', embed_textures=True, apply_unit_scale=True, add_leaf_bones=False)
bpy.ops.wm.obj_export(filepath=os.path.join(d, 'base_girl.obj'), export_selected_objects=True, path_mode='COPY', export_materials=True)
with zipfile.ZipFile(OUT + '_obj.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for f in glob.glob(os.path.join(d, '*')): z.write(f, os.path.basename(f))
print('wrote', OUT + '.fbx', OUT + '_obj.zip')
