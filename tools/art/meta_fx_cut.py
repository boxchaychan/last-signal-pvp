#!/usr/bin/env python3
# Cut an effect GIF that Meta AI drew on its grey grid preview into a transparent sprite sheet (nothing of the effect is removed).
#   python3 tools/art/meta_fx_cut.py <in.gif> <out.png> <key> [empty frames for the background, e.g. 0,9,10,11,12]
# Background = per-pixel median of frames where the effect hardly covers anything; alpha from how far a pixel is from it
# (the effect has dark smoke on a grey ground, so it is a real alpha cut, not an additive one); colours un-premultiplied.
# Adds / replaces <key> in fx/manifest.json (cell size, frames, fps from the GIF, anchor = middle of the cell).
import sys, json
import numpy as np
from PIL import Image, ImageSequence
src, out, key = sys.argv[1:4]; empty = [int(v) for v in (sys.argv[4] if len(sys.argv) > 4 else '0,-1,-2,-3,-4').split(',')]
im = Image.open(src); ms = im.info.get('duration', 40)
A = np.stack([np.asarray(f.convert('RGB')).astype(np.float32) for f in ImageSequence.Iterator(im)]); n = len(A)
bg = np.median(A[[e % n for e in empty]], axis=0)
d = np.abs(A - bg).max(axis=-1); al = np.clip((d - 8) / 28, 0, 1)
col = np.clip((A - (1 - al[..., None]) * bg) / np.maximum(al[..., None], 1e-3), 0, 255)
ys, xs = np.where(al.max(axis=0) > .05); p = 4
y0, y1, x0, x1 = max(0, ys.min() - p), min(A.shape[1], ys.max() + p), max(0, xs.min() - p), min(A.shape[2], xs.max() + p)
w, h = int(x1 - x0), int(y1 - y0); sheet = Image.new('RGBA', (w * n, h))
for i in range(n):
    rgba = np.dstack([col[i, y0:y1, x0:x1], al[i, y0:y1, x0:x1] * 255]).astype(np.uint8); sheet.paste(Image.fromarray(rgba, 'RGBA'), (i * w, 0))
sheet.save(out, optimize=True)
m = json.load(open('fx/manifest.json'))
m[key] = {'w': w, 'h': h, 'n': n, 'cols': n, 'fps': round(1000 / ms), 'ax': w // 2, 'ay': h // 2, 'src': 'owner, Meta AI gif (' + src + '); grey grid taken out by tools/art/meta_fx_cut.py, normal alpha'}
json.dump(m, open('fx/manifest.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print(key, w, h, n, 'fps', round(1000 / ms), 'crop', x0, y0, x1, y1)
