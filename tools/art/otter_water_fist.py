"""Cut the Meta AI water fists (2 x 2 on black) into one small sheet for the otter's rapid punches.

  python tools/art/otter_water_fist.py

Reads art/incoming/otter_fist/water_fists_meta_v1.webp (kept as it is), turns the black into transparency without darkening the water,
puts each fist with its knuckles at the same place in a 128 px cell, writes art/dune/otter/water_fist.webp and adds otter_wfist to sprites.json.
"""
import json
import numpy as np
from PIL import Image

SRC, OUT, CELL = 'art/incoming/otter_fist/water_fists_meta_v1.webp', 'art/dune/otter/water_fist.webp', 128
a = np.array(Image.open(SRC).convert('RGB')).astype(np.float32) / 255; H, W = a.shape[:2]; S = Image.new('RGBA', (CELL * 4, CELL), (0, 0, 0, 0))
for n in range(4):
    x0, y0 = (n % 2) * W // 2, (n // 2) * H // 2; q = a[y0:y0 + H // 2, x0:x0 + W // 2]; v = q.max(2); al = np.clip((v - .05) / .16, 0, 1); e = np.minimum.reduce(np.mgrid[0:q.shape[0], 0:q.shape[1]].tolist() + [q.shape[0] - 1 - np.mgrid[0:q.shape[0], 0:q.shape[1]][0], q.shape[1] - 1 - np.mgrid[0:q.shape[0], 0:q.shape[1]][1]]); al *= np.clip(e / 12, 0, 1)
    rgb = np.clip(q / np.maximum(al[..., None], .05), 0, 1); im = Image.fromarray((np.dstack([rgb, al]) * 255).astype(np.uint8), 'RGBA'); im = im.crop(Image.fromarray(((al > .3) * 255).astype(np.uint8)).getbbox()); k = 118 / max(im.size); im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    S.alpha_composite(im, (n * CELL + CELL - 5 - im.width, (CELL - im.height) // 2))
S.save(OUT, 'WEBP', quality=90, alpha_quality=95, method=6)
sp = json.load(open('art/dune/sprites.json')); sp['otter_wfist'] = {'src': OUT, 'n': 4, 'w': CELL, 'h': CELL, 'cols': 4}; json.dump(sp, open('art/dune/sprites.json', 'w'), separators=(',', ':')); print(OUT, S.size)
