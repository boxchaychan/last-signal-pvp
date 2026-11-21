"""Paint out colour that a removed piece left on a neighbour's texture (owner 2026-11-21: "ลบรอยที่ค้างด้วย" after the quiver was dropped:
Tripo had painted the quiver's brown / red onto the wolf pelt behind it).

For each given part: every texel whose 3D point (found by rasterising the part's triangles in UV space) lies inside the box AND whose colour
is "not like the part" (saturated red / orange / brown, while fur is grey / white) is masked and in-painted from the texels round it.
The GLB is rewritten with the new pictures (every other byte kept).

python3 tools/art/glb_texclean.py <in.glb> <out.glb> <part>:<xmin>,<xmax>,<ymin>,<ymax>,<zmin>,<zmax>[:<min saturation 0-255, default 60>] [...]
  e.g. python3 tools/art/glb_texclean.py art/incoming/basebody/tripo_wolf_v1_tex.glb art/incoming/basebody/tripo_wolf_v1_tex_clean.glb 0:-.4,0,.3,.8,-.4,-.02
Coordinates = the GLB's own (y up). Needs: pip install opencv-python-headless
"""
import io
import json
import struct
import sys

import cv2
import numpy as np
from PIL import Image


def read_glb(p):
    b = open(p, 'rb').read()
    n = struct.unpack('<I', b[12:16])[0]
    j = json.loads(b[20:20 + n])
    off = 20 + n
    bl = struct.unpack('<I', b[off:off + 4])[0]
    return j, bytearray(b[off + 8:off + 8 + bl])


def write_glb(p, j, views):   # views: list of bytes per bufferView, packed in order (4-byte aligned)
    out = bytearray()
    for i, v in enumerate(views):
        while len(out) % 4: out.append(0)
        j['bufferViews'][i]['byteOffset'] = len(out); j['bufferViews'][i]['byteLength'] = len(v); out += v
    while len(out) % 4: out.append(0)
    j['buffers'][0]['byteLength'] = len(out)
    js = json.dumps(j, separators=(',', ':')).encode()
    while len(js) % 4: js += b' '
    total = 12 + 8 + len(js) + 8 + len(out)
    with open(p, 'wb') as f:
        f.write(struct.pack('<III', 0x46546C67, 2, total)); f.write(struct.pack('<II', len(js), 0x4E4F534A)); f.write(js)
        f.write(struct.pack('<II', len(out), 0x004E4942)); f.write(out)


def accessor(j, binb, i):
    a = j['accessors'][i]; bv = j['bufferViews'][a['bufferView']]
    comp = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}[a['componentType']]
    nc = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4}[a['type']]
    o = bv.get('byteOffset', 0) + a.get('byteOffset', 0); st = bv.get('byteStride', 0) or nc * np.dtype(comp).itemsize
    raw = np.frombuffer(bytes(binb[o:o + st * a['count']]), dtype=np.uint8).reshape(a['count'], st)
    return raw[:, :nc * np.dtype(comp).itemsize].copy().view(comp).reshape(a['count'], nc)


def main():
    src, dst, jobs = sys.argv[1], sys.argv[2], sys.argv[3:]
    j, binb = read_glb(src)
    views = [bytes(binb[v.get('byteOffset', 0):v.get('byteOffset', 0) + v['byteLength']]) for v in j['bufferViews']]
    node_of = {nd['name']: nd for nd in j['nodes'] if 'mesh' in nd}
    for job in jobs:
        bits = job.split(':'); part, box = bits[0], bits[1]; smin = int(bits[2]) if len(bits) > 2 else 60; x0, x1, y0, y1, z0, z1 = map(float, box.split(','))
        pr = j['meshes'][node_of['tripo_part_' + part]['mesh']]['primitives'][0]
        P = accessor(j, binb, pr['attributes']['POSITION']); UV = accessor(j, binb, pr['attributes']['TEXCOORD_0'])
        I = accessor(j, binb, pr['indices']).reshape(-1, 3)
        tex = j['materials'][pr['material']]['pbrMetallicRoughness']['baseColorTexture']['index']; img_i = j['textures'][tex]['source']
        bvi = j['images'][img_i]['bufferView']
        im = np.array(Image.open(io.BytesIO(views[bvi])).convert('RGB')); H, W = im.shape[:2]
        zone = np.zeros((H, W), bool)
        for t in I:
            p = P[t]
            if p[:, 0].min() > x1 or p[:, 0].max() < x0 or p[:, 1].min() > y1 or p[:, 1].max() < y0 or p[:, 2].min() > z1 or p[:, 2].max() < z0: continue
            uv = UV[t] * [W, H]; mn = np.floor(uv.min(0)).astype(int); mx = np.ceil(uv.max(0)).astype(int)
            mn = np.clip(mn, 0, [W - 1, H - 1]); mx = np.clip(mx, 0, [W - 1, H - 1])
            xs, ys = np.meshgrid(np.arange(mn[0], mx[0] + 1) + .5, np.arange(mn[1], mx[1] + 1) + .5)
            a, b, c = uv; v0, v1 = b - a, c - a; d = v0[0] * v1[1] - v1[0] * v0[1]
            if abs(d) < 1e-9: continue
            px, py = xs - a[0], ys - a[1]; l1 = (px * v1[1] - v1[0] * py) / d; l2 = (v0[0] * py - px * v0[1]) / d; l0 = 1 - l1 - l2
            inside = (l0 >= -.02) & (l1 >= -.02) & (l2 >= -.02)
            q = l0[..., None] * p[0] + l1[..., None] * p[1] + l2[..., None] * p[2]
            ok = inside & (q[..., 0] >= x0) & (q[..., 0] <= x1) & (q[..., 1] >= y0) & (q[..., 1] <= y1) & (q[..., 2] >= z0) & (q[..., 2] <= z1)
            zone[(ys[ok] - .5).astype(int), (xs[ok] - .5).astype(int)] = True
        hsv = cv2.cvtColor(im, cv2.COLOR_RGB2HSV).astype(int)   # OpenCV hue 0-179
        h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
        bad = zone & (s > smin) & ((h < 28) | (h > 165)) & (v > 12)   # red / orange / brown; the fur is grey-violet and pale
        bad = cv2.dilate(bad.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
        bad &= cv2.dilate(zone.astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
        fixed = cv2.inpaint(im, bad.astype(np.uint8) * 255, 7, cv2.INPAINT_TELEA)
        buf = io.BytesIO(); Image.fromarray(fixed).save(buf, 'JPEG', quality=92); views[bvi] = buf.getvalue()
        j['images'][img_i]['mimeType'] = 'image/jpeg'
        print('part', part, 'texture', W, 'x', H, 'zone texels', int(zone.sum()), 'painted out', int(bad.sum()))
    write_glb(dst, j, views); print('wrote', dst)


if __name__ == '__main__':
    main()
