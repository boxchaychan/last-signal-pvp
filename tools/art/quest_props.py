# Pack the PixelLab map objects of quest.html (trees, mushrooms, houses, rocks...) into one atlas.
#   python tools/art/quest_props.py            (reads art/incoming/quest/props/*_raw.png, writes art/quest/props.png + props.json)
# Each picture is trimmed to its drawn box, gets tools/art/pixel_punch.py (the raw files stay as they are), and is shelf-packed with a
# 1 px gap. json: name -> x, y, w, h and the foot anchor ax, ay (middle of the lowest rows, bottom row) inside its box.
import os, glob, json, subprocess, sys, tempfile
import numpy as np
from PIL import Image
SRC, OUT = 'art/incoming/quest/props', 'art/quest/props'
items = []
for f in sorted(glob.glob(os.path.join(SRC, '*_raw.png'))):
    name = os.path.basename(f)[:-8]; im = Image.open(f).convert('RGBA'); a = np.asarray(im)[..., 3] > 0
    tmp = os.path.join(tempfile.gettempdir(), 'qp_' + name + '.png')
    subprocess.check_call([sys.executable, 'tools/art/pixel_punch.py', f, tmp, '0.5', '40'])
    p = np.asarray(Image.open(tmp).convert('RGBA')).copy(); p[..., 3] = np.where(a, 255, 0); im = Image.fromarray(p).crop(im.getbbox())
    b = np.asarray(im)[..., 3] > 0; ys, xs = np.where(b); low = xs[ys >= ys.max() - 5]
    items.append({'name': name, 'im': im, 'ax': int(round((low.min() + low.max() + 1) / 2)), 'ay': im.size[1]})
items.sort(key=lambda i: -i['im'].size[1]); W = 1024; x = y = rowh = 0; meta = {}
for it in items:
    w, h = it['im'].size
    if x + w + 1 > W: x = 0; y += rowh + 1; rowh = 0
    it['x'], it['y'] = x, y; x += w + 1; rowh = max(rowh, h)
H = y + rowh; atlas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for it in items:
    atlas.paste(it['im'], (it['x'], it['y'])); meta[it['name']] = {'x': it['x'], 'y': it['y'], 'w': it['im'].size[0], 'h': it['im'].size[1], 'ax': it['ax'], 'ay': it['ay']}
os.makedirs(os.path.dirname(OUT), exist_ok=True); atlas.save(OUT + '.png'); json.dump({'W': W, 'H': H, 'items': meta}, open(OUT + '.json', 'w'), separators=(',', ':'))
print(OUT, atlas.size, len(items), 'props:', ' '.join(sorted(meta)))
