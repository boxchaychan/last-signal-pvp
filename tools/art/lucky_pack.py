# Pack the PixelLab art of lucky.html ("ผู้กล้าเสี่ยงดวง").
#   python tools/art/lucky_pack.py
# heroes: art/incoming/lucky/heroes/<name>_raw.png (48 x 48 each, front view) -> art/lucky/heroes.png (one row of 48 px cells, in
#         name order) + heroes.json: name -> i (cell), ax / ay (foot point: middle of the lowest rows, bottom row), top (first drawn row).
# scene:  art/incoming/lucky/bg/<name>_raw.png -> art/lucky/bg_<name>.png
# Every picture gets tools/art/pixel_punch.py (heroes .5 / 32 colours, scenes .35 / 96); the raw files stay as they are.
import os, glob, json, subprocess, sys, tempfile
import numpy as np
from PIL import Image
SRC, OUT, C = 'art/incoming/lucky', 'art/lucky', 48
os.makedirs(OUT, exist_ok=True)
def punch(f, s, n):
    tmp = os.path.join(tempfile.gettempdir(), 'lk_' + os.path.basename(f)); subprocess.check_call([sys.executable, 'tools/art/pixel_punch.py', f, tmp, s, n])
    a = np.asarray(Image.open(f).convert('RGBA')); p = np.asarray(Image.open(tmp).convert('RGBA')).copy(); p[..., 3] = np.where(a[..., 3] > 0, 255, 0); return Image.fromarray(p)
files = sorted(glob.glob(os.path.join(SRC, 'heroes', '*_raw.png'))); strip = Image.new('RGBA', (C * len(files), C), (0, 0, 0, 0)); meta = {}
for i, f in enumerate(files):
    name = os.path.basename(f)[:-8]; im = punch(f, '0.5', '32'); a = np.asarray(im)[..., 3] > 0; ys, xs = np.where(a); low = xs[ys >= ys.max() - 2]
    strip.paste(im, (i * C + (C - im.size[0]) // 2, C - im.size[1])); oy = C - im.size[1]; ox = (C - im.size[0]) // 2
    meta[name] = {'i': i, 'ax': int(round((low.min() + low.max() + 1) / 2)) + ox, 'ay': int(ys.max()) + 1 + oy, 'top': int(ys.min()) + oy}
strip.save(os.path.join(OUT, 'heroes.png')); json.dump({'cell': C, 'heroes': meta}, open(os.path.join(OUT, 'heroes.json'), 'w'), separators=(',', ':'))
print('heroes', strip.size, ' '.join(meta))
for f in sorted(glob.glob(os.path.join(SRC, 'bg', '*_raw.png'))):
    name = os.path.basename(f)[:-8]
    try: im = punch(f, '0.35', '96')
    except Exception as e: print('skip', name, e); continue
    im.convert('RGB').save(os.path.join(OUT, 'bg_' + name + '.png')); print('bg', name, im.size)
