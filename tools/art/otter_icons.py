"""Cut the Meta AI otter skill icon sheet (3 x 3 on black) into the game's icon sheet.

  python tools/art/otter_icons.py

Reads art/incoming/otter_fist/icons_meta_v1.webp (kept as it is), finds the cells from the empty black lines, turns the black into
transparency without darkening the glow, centres every icon in a 128 px cell and writes art/dune/env/otter_icons.webp.
Order: 0 K step, 1 L flurry, 2 U uppercut, 3 I smash, 4 O spin, 5 P long wave, 6 R ultimate, 7 dash, 8 water orb.
"""
import numpy as np
from PIL import Image

SRC, OUT, CELL, FIT = 'art/incoming/otter_fist/icons_meta_v1.webp', 'art/dune/env/otter_icons.webp', 128, 118
a = np.array(Image.open(SRC).convert('RGB')).astype(np.float32) / 255; m = a.max(2) > .16
def spans(v, n):
    on = v > 2; out = []; st = None
    for i, b in enumerate(on):
        if b and st is None: st = i
        if not b and st is not None:
            if i - st > 40: out.append((st, i))
            st = None
    if st is not None: out.append((st, len(on)))
    while len(out) > n:   # join the two closest pieces
        g = [out[i + 1][0] - out[i][1] for i in range(len(out) - 1)]; j = int(np.argmin(g)); out[j:j + 2] = [(out[j][0], out[j + 1][1])]
    return out
Y = spans(m.sum(1), 3); X = spans(m.sum(0), 3); print('rows', Y, 'cols', X)
if len(X) != 3 or len(Y) != 3: raise SystemExit('the sheet is not a clean 3 x 3')
S = Image.new('RGBA', (CELL * 3, CELL * 3), (0, 0, 0, 0))
for r, (y0, y1) in enumerate(Y):
    for c, (x0, x1) in enumerate(X):
        q = a[y0:y1, x0:x1]; v = q.max(2); al = np.clip((v - .04) / .18, 0, 1); rgb = np.clip(q / np.maximum(al[..., None], .05), 0, 1)
        im = Image.fromarray((np.dstack([rgb, al]) * 255).astype(np.uint8), 'RGBA'); im = im.crop(Image.fromarray(((al > .25) * 255).astype(np.uint8)).getbbox())
        k = FIT / max(im.size); im = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
        S.alpha_composite(im, (c * CELL + (CELL - im.width) // 2, r * CELL + (CELL - im.height) // 2))
S.save(OUT, 'WEBP', quality=90, alpha_quality=95, method=6); print(OUT, S.size)
