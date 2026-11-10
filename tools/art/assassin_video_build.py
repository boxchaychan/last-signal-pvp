# Assassin skin for the 2D game (owner 2026-11-11 "ใช้ 2D เลย"): the PixelLab pixel still + the owner's Meta AI clips cut to
# pixel frames (tools/video/vid2px.py with the PixelLab still as palette). Every frame gets a dark outline and its feet are
# locked to one point; all moves share one cell size.
#   python3 tools/art/assassin_video_build.py name=<frames dir>:<first,last> [name=...]   (attack, attack2, run, hurt, death)
#   -> art/action/assassin/still.png, <name>.png (one row each) + assassin.json {cw, ch, fx, fy, n: {name: frames}}
import sys, os, json, glob, numpy as np
from PIL import Image
OUT = 'art/action/assassin/'; os.makedirs(OUT, exist_ok=True)

def outline(im):
    a = np.asarray(im).copy(); m = a[..., 3] > 0; nb = np.zeros_like(m)
    for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)): nb |= np.roll(np.roll(m, dy, 0), dx, 1)
    a[nb & ~m] = (14, 6, 16, 255); return Image.fromarray(a)

def feet(im):   # middle of the lowest 6 rows of the figure
    a = np.asarray(im)[..., 3] > 0; ys, xs = np.nonzero(a); b = ys.max(); low = ys >= b - 5
    return float(xs[low].mean()), int(b)

JOBS = []
for arg in sys.argv[1:]:
    name, rest = arg.split('=', 1); d, rng = rest.rsplit(':', 1); a0, a1 = (int(v) for v in rng.split(','))
    JOBS.append((name, [outline(Image.open(f).convert('RGBA')) for f in sorted(glob.glob(d + '/p*.png'))[a0:a1 + 1]]))
st = Image.open('art/incoming/action/rogue/class2/assassin_pl128_cut.png').convert('RGBA'); st = outline(st.crop(st.getbbox()))
allim = [im for _, fr in JOBS for im in fr] + [st]
ext = [(*feet(im), im) for im in allim]
L = max(fx for fx, fy, im in ext) + 4; R = max(im.width - fx for fx, fy, im in ext) + 4; T = max(fy for fx, fy, im in ext) + 4
cw, ch, fx0, fy0 = int(L + R), int(T + 6), int(L), int(T)

def place(im):
    fx, fy = feet(im); c = Image.new('RGBA', (cw, ch)); c.alpha_composite(im, (round(fx0 - fx), fy0 - fy)); return c

N = {}
for name, fr in JOBS:
    row = Image.new('RGBA', (cw * len(fr), ch))
    for i, im in enumerate(fr): row.alpha_composite(place(im), (i * cw, 0))
    row.save(OUT + name + '.png'); N[name] = len(fr)
place(st).save(OUT + 'still.png')
json.dump({'cw': cw, 'ch': ch, 'fx': fx0, 'fy': fy0, 'n': N}, open(OUT + 'assassin.json', 'w'))
print('cell', cw, ch, 'feet', fx0, fy0, N)
