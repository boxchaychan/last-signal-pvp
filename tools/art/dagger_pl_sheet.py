# The dagger girl's PixelLab clips (character ea60ebea, canvas 204) packed like chibi_pl.png so map.html plays her with the same code.
#   python3 tools/art/dagger_pl_sheet.py -> art/poses/combo/dagger_pl.png (10 columns of 204 px)
# cells: run 0-7 · slash 10-26 (cell 10 + frame) · idle 60 · hurt 70 · death 80 · roll 90 (no roll clip yet: the run frames) · run north 100 · run south 110 · spin 120 (her K skill is a dash: the run frames)
# Every frame is shifted by the same amount so her feet stand on x 103 like the swordsman's. Nothing is removed. The magenta trails PixelLab drew are
# RECOLOURED to the neon violet the owner chose for her effects (hue only; raw frames stay in art/incoming/darkchibi/dagger/pl_char/char).
import glob, numpy as np
from PIL import Image
A = glob.glob('art/incoming/darkchibi/dagger/pl_char/char/*/animations')[0] + '/'; C = 204
def fr(m, d): return [Image.open(f).convert('RGBA') for f in sorted(glob.glob(A + m + '/' + d + '/*.png'))]
def neon(im):
    a = np.asarray(im).copy(); r, g, b = [a[..., k].astype(int) for k in range(3)]; m = (a[..., 3] > 0) & (r > 190) & (g < 130) & (b > 160) & (r - g > 90)
    k = np.clip((r + b) / 510, 0, 1)[m]; a[m, 0] = (176 * k + 30).clip(0, 255); a[m, 1] = (60 * k).clip(0, 255); a[m, 2] = 255
    return Image.fromarray(a)
idle = fr('idle', 'east'); q = np.asarray(idle[0]); ys, xs = np.nonzero(q[..., 3]); feet = xs[ys >= ys.max() - 4]; dx = 103 - int(round((feet.min() + feet.max()) / 2)); dy = 174 - (int(ys.max()) + 1)
sheet = Image.new('RGBA', (C * 10, C * 14))
def put(c, im): sheet.alpha_composite(im, (c % 10 * C + dx, c // 10 * C + dy)) if dx >= 0 and dy >= 0 else sheet.paste(im, (c % 10 * C + dx, c // 10 * C + dy), im)
run = fr('run', 'east')[1:]; sl = [neon(f) for f in fr('slash', 'east')]
for i, f in enumerate(run): put(i, f); put(90 + i, f)
for i, f in enumerate(sl): put(10 + i, f)
for i, f in enumerate(idle[1:]): put(60 + i, f)
for i, f in enumerate(fr('hurt', 'east')[1:]): put(70 + i, f)
for i, f in enumerate(fr('death', 'east')[1:]): put(80 + i, f)
for i, f in enumerate(fr('run_ns', 'north')[1:]): put(100 + i, f)
for i, f in enumerate(fr('run_ns', 'south')[1:]): put(110 + i, f)
for i in range(16): put(120 + i, run[i % 8])   # the dash-through skill is played with the run frames + ghosts drawn by map.html
sheet.save('art/poses/combo/dagger_pl.png', optimize=True); print('shift', dx, dy, sheet.size)
