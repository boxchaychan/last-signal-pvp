"""Cuts a Codex isometric sheet (flat magenta background, 4 x 3 objects) into the game atlas.
Keeps the painted pixels, removes the magenta and its fringe, and records where each object's
front ground corner is so it can stand on the map.
usage: python tools/art/nation_iso.py art/incoming/nation_iso/iso_test.png art/nation/iso.webp nation/iso_data.js"""
import json
import sys

import numpy as np
from PIL import Image, ImageFilter

src, out, js = sys.argv[1:4]
COLS, ROWS = 4, 3
a = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]
keyness = np.clip((np.minimum(r, b) - g - 42) / 70, 0, 1)
alpha = 1 - keyness
# remove the pink fringe from edge pixels
spill = np.maximum(0, np.minimum(r, b) - g) * (keyness > 0)
a[..., 0] = np.clip(r - spill * keyness, 0, 255)
a[..., 2] = np.clip(b - spill * keyness, 0, 255)
mask = alpha > .5


def biggest_box(cell):
    """Tight box round the object in this cell, ignoring specks."""
    rows = np.where(cell.sum(1) > 3)[0]
    cols = np.where(cell.sum(0) > 3)[0]
    return int(cols[0]), int(rows[0]), int(cols[-1]) + 1, int(rows[-1]) + 1


cells = []
for j in range(ROWS):
    for i in range(COLS):
        x0, x1 = W * i // COLS, W * (i + 1) // COLS
        y0, y1 = H * j // ROWS, H * (j + 1) // ROWS
        bx0, by0, bx1, by1 = biggest_box(mask[y0:y1, x0:x1])
        bx0, bx1 = bx0 + x0, bx1 + x0
        by0, by1 = by0 + y0, by1 + y0
        # the front corner of the ground tile: middle of the lowest solid rows
        low = np.where(mask[max(by0, by1 - 4):by1, bx0:bx1].any(0))[0]
        tip = bx0 + (int(low[0]) + int(low[-1])) / 2
        cells.append([bx0, by0, bx1, by1, round((tip - bx0) / max(1, bx1 - bx0), 3)])

rgba = np.dstack([np.clip(a, 0, 255).astype(np.uint8), (alpha * 255).astype(np.uint8)])
im = Image.fromarray(rgba, 'RGBA')
# soften the cut edge by one pixel without touching the painting
al = im.getchannel('A').filter(ImageFilter.GaussianBlur(.6))
im.putalpha(al)
im.save(out, 'WEBP', quality=92, alpha_quality=90, method=6, exact=True)
with open(js, 'w', encoding='utf8', newline='\n') as f:
    f.write("'use strict';\n/* made by tools/art/nation_iso.py: [x0, y0, x1, y1, front corner x] of each painted object in art/nation/iso.webp */\nconst ISO_ART = " + json.dumps({'w': W, 'h': H, 'cells': cells}) + ";\n")
print('cells', cells)
