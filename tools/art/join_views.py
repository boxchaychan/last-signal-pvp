# Three separate view pictures (front / side facing right / back, each from its own GPT run, white background already cut)
# -> one turnaround strip for turn128.py, every view scaled to the same BODY height (feet to the top of the head right above
# the feet, so a sword raised over the head does not count). Berserker 2026-11-09: front_v2, side_v4_fix, back_v2 came at
# different sizes.
#   python3 tools/art/white_cut.py <view.png> <view_cut.png> --no-ring        (each of the three)
#   python3 tools/art/join_views.py <front_cut> <side_cut> <back_cut> <out.png> [body px=900]
#   python3 tools/art/turn128.py <out.png> <dir> 128 32
import sys
import numpy as np
from PIL import Image

H = int(sys.argv[5]) if len(sys.argv) > 5 else 900
figs = []
for f in sys.argv[1:4]:
    im = Image.open(f).convert('RGBA'); a = np.array(im)[..., 3] > 128
    ys, xs = np.where(a); y0, y1 = ys.min(), ys.max()
    feet = np.where(a[y1 - int((y1 - y0) * .12):y1 + 1].any(0))[0]; cx = (feet.min() + feet.max()) // 2
    top = np.where(a[:, max(0, cx - 60):cx + 60].any(1))[0].min()   # head top in a narrow band over the feet
    k = H / (y1 - top)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS); im = im.crop(im.getbbox()); figs.append(im)
    print(f, 'body', y1 - top, '-> scale', round(k, 4), im.size)
gap = 80
c = Image.new('RGBA', (sum(f.width for f in figs) + gap * 4, max(f.height for f in figs) + 40), (0, 0, 0, 0)); x = gap
for f in figs: c.alpha_composite(f, (x, c.height - 20 - f.height)); x += f.width + gap
c.save(sys.argv[4]); print(sys.argv[4], c.size)
