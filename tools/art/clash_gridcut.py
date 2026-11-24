#!/usr/bin/env python3
"""Cut a ChatGPT / Meta 'pixel art' sheet on flat magenta into TRUE pixel sprites, FREE (no PixelLab): the size of the drawn pixel is
measured from the picture itself (autocorrelation of colour edges, x and y apart, so stretched copies work), then every sprite gets its own
grid phase (least colour spread inside cells) and each cell takes its most common colour (clash_cut.py's method, now with the grid found by itself).
  python3 tools/art/clash_gridcut.py <sheet.png> <out dir> <prefix> [count=12]
-> <out>/<prefix>_<nn>.png (untouched true-pixel cut), <prefix>_<nn>_p.png (pixel_punch), <out>/<prefix>_sheet.png (preview, 6x on grass)"""
import os, subprocess, sys
import numpy as np
from PIL import Image
from scipy import ndimage as nd
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src, out, pre = sys.argv[1], sys.argv[2], sys.argv[3]; N = int(sys.argv[4]) if len(sys.argv) > 4 else 12
A = np.array(Image.open(src).convert('RGB')).astype(float)
mag = (np.abs(A[..., 0] - 255) + A[..., 1] + np.abs(A[..., 2] - 255)) < 170; fig = ~mag
def period(axis):
    g = np.abs(np.diff(A, axis=axis)).sum(2); m = fig & np.roll(fig, -1, axis=axis); m = m[:-1] if axis == 0 else m[:, :-1]
    s = (g * m).sum(1 - axis); s = s - s.mean(); ac = np.correlate(s, s, 'full')[len(s) - 1:]; lags = np.arange(len(ac))
    best = max(range(5, 17), key=lambda L: ac[L]); fine = np.arange(best - .9, best + .9, .02)          # sub-pixel refine over many periods
    sc = [sum(np.interp(k * f, lags, ac) for k in range(1, 9)) for f in fine]; return float(fine[int(np.argmax(sc))])
CX, CY = period(1), period(0); print('drawn pixel', round(CX, 2), 'x', round(CY, 2), 'screen px')
lab, n = nd.label(nd.binary_dilation(fig, iterations=2)); objs = [s for s in nd.find_objects(lab) if (s[0].stop - s[0].start) * (s[1].stop - s[1].start) > 6000]
objs.sort(key=lambda s: (s[0].start + s[0].stop) / 2); rows = []
for s in objs:
    if rows and abs((s[0].start + s[0].stop) / 2 - (rows[-1][0][0].start + rows[-1][0][0].stop) / 2) < 120: rows[-1].append(s)
    else: rows.append([s])
objs = [s for r in rows for s in sorted(r, key=lambda s: s[1].start)]; print('sprites', len(objs)); assert len(objs) == N, len(objs)
def cells(h, w, ox, oy): return np.floor((np.arange(h) - oy) / CY).astype(int) + 1, np.floor((np.arange(w) - ox) / CX).astype(int) + 1
def spread(sub, ox, oy):
    h, w, _ = sub.shape; ys, xs = cells(h, w, ox, oy); W = xs.max() + 1; idx = (ys[:, None] * W + xs[None, :]).ravel(); t = 0
    for c in range(3):
        v = sub[..., c].ravel(); cnt = np.bincount(idx); s1 = np.bincount(idx, v); s2 = np.bincount(idx, v * v); t += (s2 - s1 * s1 / np.maximum(cnt, 1)).sum()
    return t
os.makedirs(out, exist_ok=True); res = []
for n_, s in enumerate(objs, 1):
    y0, y1, x0, x1 = max(0, s[0].start - 4), s[0].stop + 4, max(0, s[1].start - 4), s[1].stop + 4
    sub = A[y0:y1, x0:x1]; f = fig[y0:y1, x0:x1]; h, w, _ = sub.shape
    ox, oy = min(((ox, oy) for ox in np.arange(0, CX, CX / 8) for oy in np.arange(0, CY, CY / 8)), key=lambda o: spread(sub, *o))
    ys, xs = cells(h, w, ox, oy); H, W = ys.max() + 1, xs.max() + 1; o = np.zeros((H, W, 4), np.uint8)
    q = (sub // 12).astype(int); keyc = q[..., 0] * 4096 + q[..., 1] * 64 + q[..., 2]
    for j in range(H):
        rm = ys == j
        for i in range(W):
            cm = xs == i; bf = f[rm][:, cm]
            if bf.size == 0 or bf.mean() < .5: continue
            kk = keyc[rm][:, cm][bf]; u, c = np.unique(kk, return_counts=True); o[j, i, :3] = sub[rm][:, cm][bf][kk == u[c.argmax()]].mean(0); o[j, i, 3] = 255
    al = o[..., 3] > 0; r_ = np.nonzero(al.any(1))[0]; c_ = np.nonzero(al.any(0))[0]; o = o[r_[0]:r_[-1] + 1, c_[0]:c_[-1] + 1]
    fo = os.path.join(out, f'{pre}_{n_:02d}.png'); Image.fromarray(o, 'RGBA').save(fo); fp = os.path.join(out, f'{pre}_{n_:02d}_p.png')
    subprocess.run([sys.executable, os.path.join(ROOT, 'tools/art/pixel_punch.py'), fo, fp, '0.6', '40'], check=True); res.append(Image.open(fp).convert('RGBA')); print(n_, o.shape[1], 'x', o.shape[0])
Z = 6; Wd = sum(t.width * Z + 16 for t in res) + 16; Hd = max(t.height for t in res) * Z + 30; sh = Image.new('RGBA', (Wd, Hd), (92, 120, 60, 255)); x = 16
for t in res: sh.alpha_composite(t.resize((t.width * Z, t.height * Z), Image.NEAREST), (x, Hd - 15 - t.height * Z)); x += t.width * Z + 16
sh.save(os.path.join(out, f'{pre}_sheet.png'))
