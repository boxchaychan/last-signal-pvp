#!/usr/bin/env python3
"""An animation GIF (white or see-through background, a "pixel art" character resized to a non-whole scale, e.g. the owner's
Cleopatra_Attack_4_Directions_GIF) -> one strip of true pixel frames for the game.

  python3 -I tools/art/gif_anim.py <in.gif> <out.png> [grid range, default 1.8,4] [light cut, default 200]

- the background (near-white, joined to the border) is cut from every frame; white clothes inside the outline stay
- ONE pixel grid is found for the whole animation (edge profile summed over all frames, same method as gptpx.py),
  so every frame snaps the same way and the animation does not wobble
- every cell takes the most common colour of its middle, near-identical shades are merged over all frames,
  a 1-px dark outline is added, frames are cropped to their common box (feet stay where they are) and put side by side
Prints the numbers for FANIM in bb.html: n, cw, ch (cell), fx, fy (feet in the cell), h0 (height of frame 1's figure).
"""
import sys, json
import numpy as np
from PIL import Image, ImageSequence
from scipy import ndimage as nd

src, out = sys.argv[1], sys.argv[2]
GR = [float(v) for v in (sys.argv[3] if len(sys.argv) > 3 else '1.8,4').split(',')]
LIGHT = int(sys.argv[4]) if len(sys.argv) > 4 else 200   # white-background cut: lighter than this (old rule: 226)
raw = [np.array(f.convert('RGBA')).astype(int) for f in ImageSequence.Iterator(Image.open(src))]
# a see-through background (e.g. Wukong's GIF) is used as it is; the colours sit on white for the grid search
CLEAR = all((r[:, :, 3] < 128).mean() > .2 for r in raw)
frames = [np.where(r[:, :, 3:] > 127, r[:, :, :3], 255) for r in raw]
H, W, _ = frames[0].shape


def figure(A, R):
    if CLEAR:
        return keep_big(R[:, :, 3] > 127)
    # light grey joined to the border = background + its soft fringe (else white specks ring the outline)
    near = (A.min(2) > LIGHT) & (A.max(2) - A.min(2) < 30)
    lab, n = nd.label(near)
    edge = set(np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])) - {0}
    fig = ~np.isin(lab, list(edge))
    # background caught inside the figure (between an arm and a hammer): exactly the border colour and not tiny
    bg = np.median(np.r_[A[0], A[-1], A[:, 0], A[:, -1]], 0)
    hole = fig & (np.abs(A - bg).max(2) <= 5)
    hl, hn = nd.label(hole)
    if hn:
        hs = nd.sum(hole, hl, range(1, hn + 1))
        fig &= ~np.isin(hl, np.where(hs > 120)[0] + 1)
    return keep_big(fig)


def keep_big(fig):
    fl, fn = nd.label(fig)
    if fn:
        fs = nd.sum(fig, fl, range(1, fn + 1))
        keep = fs > fs.max() * .004          # keep small sparks near the staff, drop single specks
        fig = np.isin(fl, np.where(keep)[0] + 1)
    return fig


figs = [figure(A, R) for A, R in zip(frames, raw)]


def fit(ax):
    prof = None
    for A in frames:
        d = np.abs(np.diff(A, axis=ax)).sum(2) > 60
        p = d.sum(axis=1 - ax).astype(float)
        prof = p if prof is None else prof + p
    xs = np.arange(len(prof)) + 1
    best = None
    for per in np.arange(GR[0], GR[1], 0.005):
        z = (prof * np.exp(2j * np.pi * xs / per)).sum()
        s = abs(z) * (per ** .5)              # small lean to the bigger period (half-periods also ring)
        if best is None or s > best[0]:
            best = (s, per, (np.angle(z) / (2 * np.pi) * per) % per)
    return best[1], best[2]


px, ox = fit(1)
py, oy = fit(0)
print('grid x %.3f+%.2f  y %.3f+%.2f' % (px, ox, py, oy), file=sys.stderr)
xs = np.arange(ox - px, W, px)
ys = np.arange(oy - py, H, py)
BIN = None
cells = []
for A, fig in zip(frames, figs):
    binv = (A[:, :, 0] // 16) * 289 + (A[:, :, 1] // 16) * 17 + (A[:, :, 2] // 16)
    img = np.zeros((len(ys), len(xs), 4), np.uint8)
    for j, y0 in enumerate(ys):
        a0, a1 = max(0, int(round(y0 + py * .25))), min(H, int(round(y0 + py * .75)) + 1)
        if a1 <= a0:
            continue
        for i, x0 in enumerate(xs):
            b0, b1 = max(0, int(round(x0 + px * .25))), min(W, int(round(x0 + px * .75)) + 1)
            if b1 <= b0:
                continue
            m = fig[a0:a1, b0:b1]
            if m.mean() < .5:
                continue
            v = binv[a0:a1, b0:b1][m]
            c = np.bincount(v).argmax()
            img[j, i, :3] = A[a0:a1, b0:b1][m][v == c].mean(0).round()
            img[j, i, 3] = 255
    cells.append(img)

# white background: light grey cells just outside a dark outline are the old soft edge, not the figure
if not CLEAR:
    N4 = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    for c in cells:
        for _ in range(2):
            al = c[:, :, 3] > 0
            rgb = c[:, :, :3].astype(int)
            edge = al & nd.binary_dilation(~al, structure=N4)
            grey = (rgb.max(2) - rgb.min(2) < 28) & (rgb.mean(2) > 120)
            dark = al & (rgb.mean(2) < 75)
            near_dark = nd.binary_dilation(dark, structure=np.ones((3, 3)))
            cut = edge & grey & near_dark
            if not cut.any():
                break
            c[cut] = 0

# merge near-identical shades over the whole animation (most common first)
allc = np.concatenate([c[c[:, :, 3] > 0][:, :3] for c in cells])
cols, cnt = np.unique(allc, axis=0, return_counts=True)
pal, mp = [], {}
for i in np.argsort(-cnt):
    c = cols[i].astype(int)
    hit = next((p for p in pal if ((p - c) ** 2).sum() < 14 * 14), None)
    if hit is None:
        pal.append(c)
        hit = c
    mp[tuple(cols[i])] = hit
for c in cells:
    m = c[:, :, 3] > 0
    for y, x in zip(*np.where(m)):
        c[y, x, :3] = mp[tuple(c[y, x, :3])]
print('colours', len(pal), file=sys.stderr)

# 1-px dark outline, then the common box
out_cells = []
for c in cells:
    h, w = c.shape[:2]
    pad = np.zeros((h + 2, w + 2, 4), np.uint8)
    pad[1:-1, 1:-1] = c
    al = pad[:, :, 3] > 0
    ring = nd.binary_dilation(al, structure=[[0, 1, 0], [1, 1, 1], [0, 1, 0]]) & ~al
    pad[ring] = (26, 18, 22, 255)
    out_cells.append(pad)
u = None
for c in out_cells:
    yy, xx = np.where(c[:, :, 3] > 0)
    b = (xx.min(), yy.min(), xx.max() + 1, yy.max() + 1)
    u = b if u is None else (min(u[0], b[0]), min(u[1], b[1]), max(u[2], b[2]), max(u[3], b[3]))
cw, ch = u[2] - u[0], u[3] - u[1]
strip = np.zeros((ch, cw * len(out_cells), 4), np.uint8)
for i, c in enumerate(out_cells):
    strip[:, i * cw:(i + 1) * cw] = c[u[1]:u[3], u[0]:u[2]]
Image.fromarray(strip, 'RGBA').save(out, optimize=True)
# feet: bottom of frame 1's figure; x: middle of frame 1's lower body
f0 = strip[:, :cw, 3] > 0
yy, xx = np.where(f0)
fy = int(yy.max()) + 1
low = xx[yy > yy.min() + (yy.max() - yy.min()) * .6]
fx = int(round((low.min() + low.max()) / 2))
# strike frame guess: the first frame whose figure reaches (almost) as far forward as any frame
reach = [int(np.where((strip[:, i * cw:(i + 1) * cw, 3] > 0).any(0))[0].max()) for i in range(len(out_cells))]
hit = next(i for i, r in enumerate(reach) if r >= max(reach) - 2)
print(json.dumps({'n': len(out_cells), 'cw': int(cw), 'ch': int(ch), 'fx': fx, 'fy': fy, 'h0': int(yy.max() - yy.min() + 1), 'hit': max(1, hit)}))
