# .gltf with embedded base64 buffers -> binary .glb (same content, ~25% smaller, faster to load). No Blender needed.
#   python3 tools/assets/gltf2glb.py in.gltf out.glb
import json, base64, struct, sys
src, dst = sys.argv[1], sys.argv[2]
g = json.load(open(src, encoding='utf-8'))
assert len(g['buffers']) == 1, 'one buffer expected'
uri = g['buffers'][0].pop('uri'); data = base64.b64decode(uri.split(',', 1)[1])
g['buffers'][0]['byteLength'] = len(data)
js = json.dumps(g, separators=(',', ':')).encode(); js += b' ' * (-len(js) % 4); data += b'\0' * (-len(data) % 4)
with open(dst, 'wb') as f:
    f.write(struct.pack('<III', 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(data)))
    f.write(struct.pack('<II', len(js), 0x4E4F534A)); f.write(js)
    f.write(struct.pack('<II', len(data), 0x004E4942)); f.write(data)
print(dst, len(js) + len(data), 'bytes')
