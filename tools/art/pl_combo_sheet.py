# The chibi swordsman's PixelLab clips (character 6d57e54b, east, canvas 204) packed for combo.html / map.html. Nothing removed:
# PixelLab's slash arcs and run dust stay as drawn.
#   python3 tools/art/pl_combo_sheet.py -> art/poses/combo/chibi_pl.png (10 columns: row 0 = run 1-8, rows 1-5 = combo3 0-40) + .json
import glob, json, numpy as np
from PIL import Image
D = 'art/incoming/darkchibi/pl_char/char/Idle/animations/'; C = 204
run = sorted(glob.glob(D + 'run/east/*.png'))[1:]; cb = sorted(glob.glob(D + 'combo3/east/*.png'))
sheet = Image.new('RGBA', (C * 10, C * 6))
for i, f in enumerate(run): sheet.alpha_composite(Image.open(f).convert('RGBA'), (i * C, 0))
for i, f in enumerate(cb): sheet.alpha_composite(Image.open(f).convert('RGBA'), (i % 10 * C, (1 + i // 10) * C))
a = np.asarray(Image.open(cb[0]).convert('RGBA')); ys, xs = np.where(a[..., 3] > 0); feet = xs[ys >= ys.max() - 3]
meta = {'cell': C, 'cols': 10, 'fx': int(round((feet.min() + feet.max()) / 2)), 'fy': int(ys.max()) + 1, 'h0': int(ys.max() - ys.min() + 1), 'run': [0, len(run)], 'combo': [10, len(cb)]}
sheet.save('art/poses/combo/chibi_pl.png', optimize=True); json.dump(meta, open('art/poses/combo/chibi_pl.json', 'w')); print(meta, sheet.size)
