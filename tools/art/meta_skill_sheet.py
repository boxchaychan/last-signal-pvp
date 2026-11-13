#!/usr/bin/env python3
"""Cut a Meta AI / GPT skill sheet on a magenta background into game cells for bag.html.
usage: meta_skill_sheet.py <sheet> <cols> <rows> <body height px in game> <out.png> [preview.png]
Cells of 204 px, feet line at y 174, frame 1's feet centre at x 100 (the same shift for every frame, so the motion inside the sheet is kept).
Nothing drawn by the AI is removed except the flat background."""
import sys
from PIL import Image
import numpy as np
from scipy import ndimage
src, cols, rows, body, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
im = Image.open(src).convert('RGB'); a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
key = (r > 150) & (b > 150) & (g < 110) & (abs(r - b) < 90)          # magenta
alpha = np.where(key, 0, 255).astype(np.uint8)
# soften the pink fringe: pixels next to the background that are still pinkish
pink = (r - g > 60) & (b - g > 60) & ~key
nb = np.zeros_like(key); nb[1:] |= key[:-1]; nb[:-1] |= key[1:]; nb[:, 1:] |= key[:, :-1]; nb[:, :-1] |= key[:, 1:]
alpha[pink & nb] = 0
rgba = np.dstack([a.astype(np.uint8), alpha]); im = Image.fromarray(rgba, 'RGBA')
cw, ch = im.width / cols, im.height / rows
# every connected blob goes to ONE cell: big blobs by their centre, small ones (sparks, streaks) to the nearest big blob, so an effect that spills over a cell edge stays with its own frame
# a glowing effect of a lower frame can reach up and touch the feet of the frame above: light blue-ish pixels just above a row line are held back from the labelling and given to the lower frame afterwards
cut = np.zeros_like(key)
for r_ in range(1, rows):
    y = round(r_ * ch); band = slice(max(0, y - int(ch * .2)), y + 2)
    blue = (b[band] > r[band] + 18) & (g[band] > r[band] + 8); white = (r[band] > 200) & (g[band] > 200) & (b[band] > 200)
    cut[band] = (blue | (white & ndimage.binary_dilation(blue, iterations=8))) & (alpha[band] > 0)
lab, n = ndimage.label((alpha > 0) & ~cut, structure=np.ones((3, 3)))
sl = ndimage.find_objects(lab); area = ndimage.sum(alpha > 0, lab, range(1, n + 1))
big = [i for i in range(n) if area[i] > 4000]; cen = {}
for i in big:
    ys, xs = np.nonzero(lab[sl[i]] == i + 1); cen[i] = (xs.mean() + sl[i][1].start, ys.mean() + sl[i][0].start)
owner = {}; bcell = {}
if len(big) == cols * rows:      # one body per cell: match bodies to cells one-to-one (a tall effect can pull a body's centre over the row line)
    from scipy.optimize import linear_sum_assignment
    cost = np.array([[(cen[i][0] - (k % cols + .5) * cw) ** 2 + (cen[i][1] - (k // cols + .5) * ch) ** 2 for k in range(cols * rows)] for i in big])
    for a_, k in zip(*linear_sum_assignment(cost)): bcell[big[a_]] = k
else:
    for i in big: bcell[i] = int(cen[i][1] // ch) * cols + int(cen[i][0] // cw)
for i in range(n):
    if i in cen: owner[i] = bcell[i]
    else:
        mx, my = (sl[i][1].start + sl[i][1].stop) / 2, (sl[i][0].start + sl[i][0].stop) / 2
        j = min(big, key=lambda k: max(sl[k][1].start - mx, mx - sl[k][1].stop, 0) ** 2 + max(sl[k][0].start - my, my - sl[k][0].stop, 0) ** 2); owner[i] = bcell[j]
omap = np.zeros(n + 1, int); 
for i in range(n): omap[i + 1] = owner[i] + 1
own = omap[lab]
for y, x in zip(*np.nonzero(cut)):
    below = [k for k in big if cen[k][1] > y]
    j = min(below or big, key=lambda k: max(sl[k][1].start - x, x - sl[k][1].stop, 0) ** 2 + max(sl[k][0].start - y, y - sl[k][0].stop, 0) ** 2); own[y, x] = bcell[j] + 1
M = int(max(cw, ch) * .5); cells = []
for k in range(cols * rows):
    c, r_ = k % cols, k // cols; x0, y0 = round(c * cw) - M, round(r_ * ch) - M; x1, y1 = round((c + 1) * cw) + M, round((r_ + 1) * ch) + M
    cell = np.zeros((y1 - y0, x1 - x0, 4), np.uint8); sx0, sy0, sx1, sy1 = max(0, x0), max(0, y0), min(im.width, x1), min(im.height, y1)
    part = rgba[sy0:sy1, sx0:sx1].copy(); part[..., 3] = np.where(own[sy0:sy1, sx0:sx1] == k + 1, part[..., 3], 0)
    cell[sy0 - y0:sy1 - y0, sx0 - x0:sx1 - x0] = part; cells.append(Image.fromarray(cell, 'RGBA'))
bb = cells[0].getbbox(); sc = body / (bb[3] - bb[1])
C = 204; sheet = Image.new('RGBA', (cols * C, rows * C), (0, 0, 0, 0))
fa = np.asarray(cells[0])[..., 3]; ys = np.where(fa.any(1))[0]; ground = ys.max() + 1
xs = np.where(fa[ground - 12:ground].any(0))[0]; fx = (xs.min() + xs.max()) / 2
for i, c in enumerate(cells):
    w, h = round(c.width * sc), round(c.height * sc)
    s = c.resize((w, h), Image.BOX)
    al = s.split()[3].point(lambda v: 255 if v > 110 else 0); s.putalpha(al)
    cell = Image.new('RGBA', (C, C), (0, 0, 0, 0))
    cell.alpha_composite(s, (max(0, round(100 - fx * sc)), 0) if False else (0, 0)) if False else None
    ox, oy = round(100 - fx * sc), round(174 - ground * sc)
    tmp = Image.new('RGBA', (C * 3, C * 3), (0, 0, 0, 0)); tmp.alpha_composite(s, (C + ox, C + oy))
    cell = tmp.crop((C, C, 2 * C, 2 * C))
    sheet.alpha_composite(cell, (i % cols * C, i // cols * C))
sheet.save(out, optimize=True); print(out, sheet.size, 'scale %.3f' % sc)
if len(sys.argv) > 6:
    p = Image.new('RGBA', sheet.size, (40, 40, 50, 255)); p.alpha_composite(sheet); p.save(sys.argv[6])
