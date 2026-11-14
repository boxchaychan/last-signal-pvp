#!/usr/bin/env python3
# The 180 Swordtember swords (TheWiseHedgehog, CC BY 4.0, see vendor/swordtember/NOTICE.md) packed for the games.
#   python3 tools/art/sword_pack.py   -> art/swords/swords.png (6 x 30 cells of 32x32: sheet n = rows 5n..5n+4, as the packs come)
#                                        art/swords/swords.json (per sword: cell, grip = the handle end, tip = the blade end, length in px)
# All swords are drawn the same way, handle at the bottom left and tip at the top right, so the grip is the opaque pixel nearest the
# bottom-left corner and the tip the one nearest the top-right corner. The pictures are copied unchanged.
import json
import numpy as np
from PIL import Image
out = Image.new('RGBA', (192, 960), (0, 0, 0, 0)); meta = []
for n in range(6):
    sh = Image.open('art/incoming/swords/raw/sheet%d.png' % (n + 1)).convert('RGBA'); out.paste(sh, (0, n * 160))
    a = np.asarray(sh)[..., 3]
    for r in range(5):
        for c in range(6):
            cell = a[r * 32:r * 32 + 32, c * 32:c * 32 + 32]; ys, xs = np.nonzero(cell > 40)
            g = int(np.argmax(ys - xs)); t = int(np.argmax(xs - ys))
            meta.append({'i': len(meta), 'pack': n + 1, 'cell': [c, n * 5 + r], 'grip': [int(xs[g]), int(ys[g])], 'tip': [int(xs[t]), int(ys[t])],
                         'len': round(float(np.hypot(xs[t] - xs[g], ys[t] - ys[g])), 1)})
out.save('art/swords/swords.png', optimize=True)
json.dump({'cell': 32, 'cols': 6, 'credit': 'Swords: Hedgy\'s Swordtember packs by TheWiseHedgehog (thewisehedgehog.itch.io), CC BY 4.0', 'swords': meta},
          open('art/swords/swords.json', 'w'), separators=(',', ':'))
print(len(meta), 'swords; length min / max', min(m['len'] for m in meta), max(m['len'] for m in meta))
