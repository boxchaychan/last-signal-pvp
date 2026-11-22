"""Cut the Meta AI skill icon sheet (3 x 3 on black) into the game's icon sheet.

  python tools/art/dune_skill_icons.py

Reads art/incoming/dune_icons/skills_meta_v1.webp (kept as it is), turns the black into transparency without darkening the glow,
centres every icon in a 128 px cell and writes art/dune/env/skill_icons.webp.
Order: 0 thrust, 1 sweep, 2 rise, 3 ground strike, 4 spin, 5 spear rain, 6 ultimate lance, 7 dash, 8 spear head.
"""
import numpy as np
from PIL import Image

SRC, OUT, CELL, FIT = 'art/incoming/dune_icons/skills_meta_v1.webp', 'art/dune/env/skill_icons.webp', 128, 118
X = [(21, 529), (565, 1074), (1114, 1590)]; Y = [(36, 519), (570, 1037), (1089, 1570)]   # the empty black lines between the icons
a = np.array(Image.open(SRC).convert('RGB')).astype(np.float32) / 255
S = Image.new('RGBA', (CELL * 3, CELL * 3), (0, 0, 0, 0))
for r, (y0, y1) in enumerate(Y):
    for c, (x0, x1) in enumerate(X):
        q = a[y0:y1, x0:x1]; v = q.max(2); al = np.clip((v - .04) / .18, 0, 1)
        rgb = np.clip(q / np.maximum(al[..., None], .05), 0, 1)
        im = Image.fromarray((np.dstack([rgb, al]) * 255).astype(np.uint8), 'RGBA'); box = Image.fromarray(((al > .25) * 255).astype(np.uint8)).getbbox(); im = im.crop(box)
        k = FIT / max(im.size); im = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
        S.alpha_composite(im, (c * CELL + (CELL - im.width) // 2, r * CELL + (CELL - im.height) // 2))
S.save(OUT, 'WEBP', quality=90, alpha_quality=95, method=6); print(OUT, S.size)
