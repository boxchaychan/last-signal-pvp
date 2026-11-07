# Turn a back-to-front arrow round in every frame of a GIF (owner 2026-11-07, Artemis from PixelLab: "ลูกธนูกลับหัวปะ"):
# the nocked arrow had its white feathers at the FRONT end and no head. In each frame the longest horizontal run of
# shaft colours (dark brown wood) is the arrow; the light pixels round its front end (the feather vanes above and below
# the shaft) go, and a small silver arrowhead pointing forward is drawn at the tip. Frames without a long horizontal
# shaft (the arrow pulled from the quiver, after the release) are left alone.
#   python3 tools/art/arrow_fix.py <in.gif> <out.gif> [min shaft length, default 14]
import sys
import numpy as np
from PIL import Image, ImageSequence

src, out = sys.argv[1], sys.argv[2]
MINL = int(sys.argv[3]) if len(sys.argv) > 3 else 14
im = Image.open(src); dur = im.info.get('duration', 100)
frames = [np.array(f.convert('RGBA')) for f in ImageSequence.Iterator(im)]
OUTL, HEAD, HI, SH = (46, 23, 34), (177, 170, 201), (254, 254, 254), (132, 124, 162)

def wood(a):
    r, g, b = [a[..., i].astype(int) for i in range(3)]
    return (a[..., 3] > 0) & (r > g + 25) & (g >= b) & (r < 190) & (r > 60)   # brown shaft

fixed = 0
for a in frames:
    w = wood(a); best = None
    for y in range(a.shape[0]):
        xs = np.where(w[y])[0]
        if len(xs) < MINL: continue
        runs = np.split(xs, np.where(np.diff(xs) > 2)[0] + 1)
        for r in runs:
            if len(r) >= MINL and (best is None or len(r) > best[2]): best = (y, r[-1], len(r))
    if not best: continue
    y0, xe, _ = best
    # the shaft is 1-2 rows thick; the front end = the right-most opaque pixel on the shaft row
    row = np.where(a[y0, :, 3] > 0)[0]; tip = row[row >= xe].max() if (row >= xe).any() else xe
    light = (a[..., :3].min(2) >= 195) & (a[..., 3] > 0)
    for y in range(y0 - 5, y0 + 6):          # feather vanes round the front end
        for x in range(tip - 11, tip + 2):
            if 0 <= y < a.shape[0] and 0 <= x < a.shape[1] and abs(y - y0) >= 2 and light[y, x]:
                a[y, x, 3] = 0
    for x in range(tip - 11, tip + 1):        # the shaft runs to the tip in wood colours
        if a[y0, x, 3] == 0 or light[y0, x]: a[y0, x] = (167, 117, 74, 255)
    # silver arrowhead: 6 px long, 5 px tall at its back, pointing right, dark outline
    hx = tip + 1
    shape = {0: (-2, 2), 1: (-2, 2), 2: (-1, 1), 3: (-1, 1), 4: (0, 0), 5: (0, 0)}
    for i, (lo, hi) in shape.items():
        x = hx - 3 + i
        for dy in range(lo - 1, hi + 2):
            yy = y0 + dy
            if 0 <= yy < a.shape[0] and 0 <= x < a.shape[1]:
                a[yy, x] = (*(OUTL if dy < lo or dy > hi else HI if dy == lo else SH if dy == hi else HEAD), 255)
    if 0 <= hx + 3 < a.shape[1]: a[y0, hx + 3] = (*OUTL, 255)
    fixed += 1
ims = [Image.fromarray(a) for a in frames]
ims[0].save(out, save_all=True, append_images=ims[1:], duration=dur, loop=0, disposal=2)
print('frames', len(frames), 'arrows turned', fixed)
