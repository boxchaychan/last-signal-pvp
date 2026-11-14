#!/usr/bin/env python3
# Cut the GPT parts sheet of the painted chibi dagger girl into transparent parts for bone animation (side2d.html).
#   python3 tools/art/side2d_cut.py   -> art/side2d/dagger/<part>.png + parts.json (size of each part)
# Background: near-white pixels connected to the box border; edge pixels get a soft alpha from how white they are
# (the white hair is never connected to the border through near-white pixels, so it stays). Nothing is redrawn.
import json
import numpy as np
from PIL import Image
SRC = 'art/incoming/side2d/dagger_parts_raw.webp'; OUT = 'art/side2d/dagger/'
BOX = {'full': (294, 18, 744, 609), 'ponytail': (282, 654, 474, 1008), 'head': (12, 690, 264, 942), 'cape': (696, 711, 993, 990), 'torso': (498, 735, 651, 975),
       'uarm_f': (27, 1032, 144, 1191), 'uarm_b': (513, 1035, 624, 1188), 'farm_f': (216, 1080, 426, 1185), 'farm_b': (696, 1080, 906, 1185),
       'thigh_f': (30, 1263, 138, 1440), 'thigh_b': (372, 1266, 474, 1437), 'shin_f': (183, 1269, 306, 1524), 'shin_b': (528, 1269, 654, 1524),
       'dagger_1': (708, 1284, 996, 1377), 'dagger_2': (711, 1413, 996, 1506)}
im = np.asarray(Image.open(SRC).convert('RGB')).astype(int); meta = {}
for k, (x0, y0, x1, y1) in BOX.items():
    x0, y0, x1, y1 = x0 - 6, y0 - 6, x1 + 6, y1 + 6; a = im[y0:y1, x0:x1]; H, W = a.shape[:2]; mn = a.min(axis=-1)
    near = mn >= 236; bg = np.zeros((H, W), bool); st = [(y, x) for y in range(H) for x in (0, W - 1)] + [(y, x) for x in range(W) for y in (0, H - 1)]
    while st:
        y, x = st.pop()
        if 0 <= y < H and 0 <= x < W and near[y, x] and not bg[y, x]: bg[y, x] = True; st += [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
    al = np.where(bg, 0, 255).astype(float)
    edge = ~bg & (np.roll(bg, 1, 0) | np.roll(bg, -1, 0) | np.roll(bg, 1, 1) | np.roll(bg, -1, 1))
    soft = np.clip((255 - mn) / 70, 0, 1); al[edge] = 255 * soft[edge]
    rgb = a.astype(float); f = np.maximum(al / 255, 1e-3)[..., None]; rgb = np.where(edge[..., None], np.clip((rgb - (1 - f) * 255) / f, 0, 255), rgb)
    out = np.dstack([rgb, al]).astype(np.uint8); img = Image.fromarray(out, 'RGBA'); bb = img.getbbox(); img = img.crop(bb)
    img.save(OUT + k + '.png', optimize=True); meta[k] = [img.width, img.height]
json.dump(meta, open(OUT + 'parts.json', 'w')); print(meta)
