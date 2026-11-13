# A big-pixel picture on a flat (dark) background -> the true small sprite (owner 2026-11-13 "ลองแปลงดู", the 24 px wolf test).
# Finds the pixel size and offset from the colour edges, takes the middle colour of every block, removes the background, merges near-identical shades.
#   python3 tools/art/tiny_snap.py <in.png> <out.png> [min block 6] [max block 24]
import sys, numpy as np
from PIL import Image
src, out = sys.argv[1], sys.argv[2]; lo, hi = (float(sys.argv[3]), float(sys.argv[4])) if len(sys.argv) > 4 else (6, 24)
a = np.asarray(Image.open(src).convert('RGB')).astype(int); bg = np.median(a.reshape(-1, 3), axis=0); m = abs(a - bg).sum(2) > 45
ys, xs = np.where(m); x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
def grid(ax):
    sub = a[y0:y1, x0:x1]; g = (abs(np.diff(sub, axis=ax)).sum(2) > 40).sum(1 - ax).astype(float); best = (0, 0, 0)
    for p in np.arange(lo, hi, .02):
        ph = np.arange(len(g)) % p
        for k in np.arange(0, p, .5):
            sc = g[(ph >= k) & (ph < k + 1.5)].mean()
            if sc > best[0]: best = (sc, p, k)
    return best[1], best[2]
(px, kx), (py, ky) = grid(1), grid(0); p = (px + py) / 2
ox = x0 + kx + 1 - p * np.ceil((kx + 1) / p + 1); oy = y0 + ky + 1 - p * np.ceil((ky + 1) / p + 1)
W, H = int((x1 - ox) / p) + 2, int((y1 - oy) / p) + 2; o = np.zeros((H, W, 4), np.uint8)
for j in range(H):
    for i in range(W):
        cy0, cx0 = oy + j * p, ox + i * p; b = a[int(max(0, cy0 + p * .3)):int(cy0 + p * .7) + 1, int(max(0, cx0 + p * .3)):int(cx0 + p * .7) + 1].reshape(-1, 3)
        if not len(b): continue
        c = np.median(b, axis=0)
        if abs(c - bg).sum() > 45: o[j, i] = (*c.astype(np.uint8), 255)
im = Image.fromarray(o); im = im.crop(im.getbbox()); q = np.asarray(im).copy(); op = q[..., 3] > 0
pal = Image.fromarray(q[..., :3]).quantize(12, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB'); q[..., :3] = np.asarray(pal); q[~op] = 0
Image.fromarray(q).save(out); print('block %.2f x %.2f' % (px, py), 'sprite', Image.fromarray(q).size, 'colours', len(np.unique(q[op][:, :3], axis=0)))
