# Last Signal · Step 2: merge the Mixamo downloads into one game file
# Put every FBX you downloaded from Mixamo in Downloads (one "With Skin", the rest "Without Skin"),
# then in Blender: Scripting tab > Open > this file > Run Script.
# Writes Downloads/storm_game.glb  -> send this file to Claude
import bpy, os, glob, re

DL = os.path.join(os.path.expanduser('~'), 'Downloads')
base = os.path.join(DL, 'storm_mixamo.fbx')
t0 = os.path.getmtime(base) if os.path.exists(base) else 0
files = [f for f in glob.glob(os.path.join(DL, '*.fbx'))
         if os.path.basename(f) != 'storm_mixamo.fbx' and os.path.getmtime(f) >= t0]
if not files:
    raise Exception('No Mixamo FBX files in ' + DL)
files.sort(key=os.path.getsize, reverse=True)   # the "With Skin" file is the biggest


def short(path):
    n = os.path.splitext(os.path.basename(path))[0].lower()
    for key, words in (('idle', ['idle']), ('run', ['run', 'sprint']), ('walk', ['walk']), ('shoot', ['fir', 'shoot']),
                       ('throw', ['toss', 'throw', 'grenade']), ('die', ['dying', 'death', 'die']), ('reload', ['reload']),
                       ('hit', ['hit', 'react']), ('roll', ['roll', 'dodge'])):
        if any(w in n for w in words):
            return key
    return re.sub(r'[^a-z0-9]+', '_', n).strip('_') or 'anim'


if bpy.context.object and bpy.context.object.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

char, used, acts = None, set(), []
for f in files:
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=f)
    new = [o for o in bpy.data.objects if o not in before]
    arm = next((o for o in new if o.type == 'ARMATURE'), None)
    act = arm.animation_data.action if (arm and arm.animation_data) else None
    if act:
        k, i = short(f), 2
        name = k
        while name in used:
            name = k + str(i); i += 1
        used.add(name)
        act.name = name
        act.use_fake_user = True
        acts.append(act)
        print('animation:', os.path.basename(f), '->', name)
    if char is None and arm and any(o.type == 'MESH' for o in new):
        char = arm
        continue
    for o in new:
        bpy.data.objects.remove(o, do_unlink=True)

if char is None:
    raise Exception('Could not find the "With Skin" file')
ad = char.animation_data or char.animation_data_create()
ad.action = None
for act in acts:
    tr = ad.nla_tracks.new()
    tr.name = act.name
    tr.strips.new(act.name, int(act.frame_range[0]), act)

out = os.path.join(DL, 'storm_game.glb')
kw = dict(filepath=out, export_format='GLB', export_animations=True, export_image_format='JPEG')
try:
    bpy.ops.export_scene.gltf(export_animation_mode='NLA_TRACKS', **kw)
except TypeError:
    bpy.ops.export_scene.gltf(export_nla_strips=True, **kw)
print('DONE ->', out, round(os.path.getsize(out) / 1e6, 2), 'MB')
