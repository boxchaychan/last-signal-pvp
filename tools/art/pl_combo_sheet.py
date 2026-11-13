# The chibi swordsman's PixelLab clips (character 6d57e54b, east, canvas 204) packed for combo.html / map.html. Nothing removed:
# PixelLab's slash arcs and run dust stay as drawn.
#   python3 tools/art/pl_combo_sheet.py -> art/poses/combo/chibi_pl.png (10 columns: row 0 = run 1-8, rows 1-5 = combo3 0-40) + .json
import glob, json, numpy as np
from PIL import Image
D = 'art/incoming/darkchibi/pl_char/char/Idle/animations/'; C = 204
run = sorted(glob.glob(D + 'run/east/*.png'))[1:]; cb = sorted(glob.glob(D + 'combo3/east/*.png'))
EXTRA = [('idle', 'east', 60), ('hurt', 'east', 70), ('death', 'east', 80), ('roll', 'east', 90), ('run_ns', 'north', 100), ('run_ns', 'south', 110), ('spin', 'east', 120)]   # move, direction, first cell (the reference frame 0 of each is skipped)
sheet = Image.new('RGBA', (C * 10, C * 14))
for i, f in enumerate(run): sheet.alpha_composite(Image.open(f).convert('RGBA'), (i * C, 0))
for i, f in enumerate(cb): sheet.alpha_composite(Image.open(f).convert('RGBA'), (i % 10 * C, (1 + i // 10) * C))
for mv, dr, c0 in EXTRA:
    for i, f in enumerate(sorted(glob.glob(D + mv + '/' + dr + '/*.png'))[1:]): sheet.alpha_composite(Image.open(f).convert('RGBA'), ((c0 + i) % 10 * C, (c0 + i) // 10 * C))
a = np.asarray(Image.open(cb[0]).convert('RGBA')); ys, xs = np.where(a[..., 3] > 0); feet = xs[ys >= ys.max() - 3]
meta = {'cell': C, 'cols': 10, 'fx': int(round((feet.min() + feet.max()) / 2)), 'fy': int(ys.max()) + 1, 'h0': int(ys.max() - ys.min() + 1), 'run': [0, len(run)], 'combo': [10, len(cb)], 'idle': [60, 8], 'hurt': [70, 4], 'death': [80, 8], 'roll': [90, 8], 'run_n': [100, 8], 'run_s': [110, 8], 'spin': [120, 16]}
sheet.save('art/poses/combo/chibi_pl.png', optimize=True); json.dump(meta, open('art/poses/combo/chibi_pl.json', 'w')); print(meta, sheet.size)
