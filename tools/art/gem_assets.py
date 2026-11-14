#!/usr/bin/env python3
# Art in use by gem.html, built from the raw PixelLab pictures in art/incoming/gem/raw/ (see gen.py there):
#   python3 tools/art/gem_assets.py        -> art/gem/bg_<k>.png (6 backgrounds), art/gem/icons.png (9 icons of 32 px in a row),
#                                             art/gem/emblem.png, art/gem/app192.png + app512.png (home-screen icon), and prints
#                                             the light table for gem.html (fires / lanterns found by colour: [x, y, radius, 'colour'])
# Nothing is redrawn or cleaned: the pictures are copied as they came (the icon sheet only puts them side by side).
import json, sys
from PIL import Image
import numpy as np
RAW, OUT = 'art/incoming/gem/raw/', 'art/gem/'
ICONS = ['lock', 'skull', 'swords', 'gear', 'speaker', 'note', 'map', 'chest', 'book']
def lights(im):
    a = np.asarray(im.convert('RGB')).astype(int); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    out = []
    for name, mask, col in (('fire', (r > 235) & (g > 150) & (b < 140), '#ff9a3a'), ('blue', (b > 235) & (g > 150) & (r < 140), '#6ab8ff')):
        seen = np.zeros(mask.shape, bool); H, W = mask.shape
        for y in range(H):
            for x in range(W):
                if mask[y, x] and not seen[y, x]:
                    st = [(y, x)]; seen[y, x] = True; pts = []
                    while st:
                        cy, cx = st.pop(); pts.append((cy, cx))
                        for dy in (-2, -1, 0, 1, 2):
                            for dx in (-2, -1, 0, 1, 2):
                                ny, nx = cy + dy, cx + dx
                                if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not seen[ny, nx]: seen[ny, nx] = True; st.append((ny, nx))
                    if len(pts) >= 5: ys = [p[0] for p in pts]; xs = [p[1] for p in pts]; out.append([round(sum(xs) / len(xs)), round(sum(ys) / len(ys)), min(60, 18 + int(len(pts) ** .5 * 3)), col])
    return out
tab = {}
for k in ['siam', 'china', 'japan', 'egypt', 'norse', 'camp']:
    im = Image.open(RAW + k + '.png').convert('RGB'); im.save(OUT + 'bg_' + k + '.png', optimize=True); tab[k] = lights(im)
tab['moon'] = lights(Image.open('art/bag/arena.png'))
sheet = Image.new('RGBA', (32 * len(ICONS), 32), (0, 0, 0, 0))
for i, k in enumerate(ICONS): sheet.paste(Image.open(RAW + k + '.png').convert('RGBA'), (i * 32, 0))
sheet.save(OUT + 'icons.png', optimize=True)
em = Image.open(RAW + 'emblem.png').convert('RGBA'); em.save(OUT + 'emblem.png', optimize=True)
for n in (192, 512):                                        # the home-screen icon: the emblem, whole pixels, on the game's dark purple
    k = max(1, int(n * .92) // em.width); e2 = em.resize((em.width * k, em.height * k), Image.NEAREST); ic = Image.new('RGBA', (n, n), (26, 19, 50, 255))
    for y in range(n):
        t = y / n; c = (int(40 - 22 * t), int(28 - 16 * t), int(78 - 40 * t), 255)
        for x in range(n): ic.putpixel((x, y), c)
    ic.alpha_composite(e2, ((n - e2.width) // 2, (n - e2.height) // 2)); ic.convert('RGB').save(OUT + 'app%d.png' % n, optimize=True)
print(json.dumps(tab))
