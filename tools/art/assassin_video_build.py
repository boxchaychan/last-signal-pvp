# Assassin test skin for the 2D game (owner 2026-11-11 "ใช้ 2D เลย"): the PixelLab pixel still + the Meta AI attack clip cut to
# pixel frames (tools/video/vid2px.py, PixelLab palette), feet locked to one point, the turned-away frames dropped.
#   python3 tools/art/assassin_video_build.py <frames dir from vid2px> <first,last>
#   -> art/action/assassin/still.png, attack.png (one row) + assassin.json {cw, ch, fx, fy, n}
import sys, os, json, glob, numpy as np
from PIL import Image
src = sys.argv[1]; a0, a1 = (int(v) for v in sys.argv[2].split(','))
OUT = 'art/action/assassin/'; os.makedirs(OUT, exist_ok=True)
def outline(im):
    a = np.asarray(im).copy(); m = a[..., 3] > 0; nb = np.zeros_like(m)
    for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)): nb |= np.roll(np.roll(m, dy, 0), dx, 1)
    a[nb & ~m] = (14, 6, 16, 255); return Image.fromarray(a)
def feet(im):
    a = np.asarray(im)[..., 3] > 0; ys, xs = np.nonzero(a); b = ys.max(); low = ys >= b - 5
    return float(xs[low].mean()), int(b)
fr = [outline(Image.open(f).convert('RGBA')) for f in sorted(glob.glob(src + '/p*.png'))[a0:a1 + 1]]
st = Image.open('art/incoming/action/rogue/class2/assassin_pl128_cut.png').convert('RGBA'); st = outline(st.crop(st.getbbox()))
FX, FY = 0, 0; ext = []
for im in fr + [st]: fx, fy = feet(im); ext.append((fx, fy, im))
L = max(fx for fx, fy, im in ext) + 4; R = max(im.width - fx for fx, fy, im in ext) + 4; T = max(fy for fx, fy, im in ext) + 4
cw, ch = int(L + R), int(T + 6); fx0, fy0 = int(L), int(T)
def place(fx, fy, im): c = Image.new('RGBA', (cw, ch)); c.alpha_composite(im, (round(fx0 - fx), fy0 - fy)); return c
row = Image.new('RGBA', (cw * len(fr), ch))
for i, (fx, fy, im) in enumerate(ext[:-1]): row.alpha_composite(place(fx, fy, im), (i * cw, 0))
row.save(OUT + 'attack.png'); place(*ext[-1]).save(OUT + 'still.png')
json.dump({'cw': cw, 'ch': ch, 'fx': fx0, 'fy': fy0, 'n': len(fr)}, open(OUT + 'assassin.json', 'w'))
print('cell', cw, ch, 'feet', fx0, fy0, 'frames', len(fr))
