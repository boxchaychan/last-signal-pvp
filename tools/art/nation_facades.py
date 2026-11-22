"""Cuts the 8 flat building fronts from the Codex sheet into the game atlas.
Keeps the painting untouched, fills the green around each front with its own edge colours,
and stores a window mask in alpha so windows can light up at night.
usage: python tools/art/nation_facades.py art/incoming/nation_facades/facades_test.png art/nation/facades.webp nation/facade_data.js"""
import json, sys
import numpy as np
from PIL import Image

src, out, js = sys.argv[1:4]
a = np.asarray(Image.open(src).convert('RGB')).astype(np.int32)
H, W = a.shape[:2]
green = (a[..., 1] > 170) & (a[..., 0] < 110) & (a[..., 2] < 110)
solid = ~green

def spans(line, thr, gap=10):
    idx = np.where(line > thr)[0]
    if not len(idx): return []
    out, s, p = [], idx[0], idx[0]
    for i in idx[1:]:
        if i - p > gap: out.append((int(s), int(p) + 1)); s = i
        p = i
    out.append((int(s), int(p) + 1))
    return [q for q in out if q[1] - q[0] > 60]

rows = spans(solid.sum(1), 40)
assert len(rows) == 2, rows
cells = []
for r0, r1 in rows:
    cols = spans(solid[r0:r1].sum(0), 40)
    assert len(cols) == 4, cols
    for c0, c1 in cols:
        s = solid[r0:r1, c0:c1]
        ys = np.where(s.sum(1) > s.shape[1] * .97)[0]
        y0, y1 = r0 + int(ys[0]), r0 + int(ys[-1]) + 1
        s2 = solid[y0:y1, c0:c1]
        xs = np.where(s2.sum(0) > s2.shape[0] * .985)[0]
        x0, x1 = c0 + int(xs[0]), c0 + int(xs[-1]) + 1
        cells.append([x0 + 1, y0 + 1, x1 - 1, y1 - 1])

rgb = np.full((H, W, 3), 200, np.uint8)
alpha = np.zeros((H, W), np.uint8)
PAD = 10
for x0, y0, x1, y1 in cells:
    crop = a[y0:y1, x0:x1].astype(np.uint8)
    top, left = min(PAD, y0), min(PAD, x0)
    bottom, right = min(PAD, H - y1), min(PAD, W - x1)
    rgb[y0 - top:y1 + bottom, x0 - left:x1 + right] = np.pad(crop, ((top, bottom), (left, right), (0, 0)), mode='edge')
    r, g, b = [crop[..., i].astype(np.int32) for i in range(3)]
    win = (np.maximum(b, g) > r + 16) & (r < 175)
    alpha[y0:y1, x0:x1] = win.astype(np.uint8) * 255
rgb[:16, :16] = 255
alpha[:16, :16] = 0
Image.fromarray(np.dstack([rgb, alpha]), 'RGBA').save(out, 'WEBP', quality=92, alpha_quality=80, method=6, exact=True)
with open(js, 'w', encoding='utf8', newline='\n') as f:
    f.write("'use strict';\n/* made by tools/art/nation_facades.py: where each painted building front sits in art/nation/facades.webp */\nconst FACADE = " + json.dumps({'w': W, 'h': H, 'cells': cells}) + ";\n")
print('cells', cells)
