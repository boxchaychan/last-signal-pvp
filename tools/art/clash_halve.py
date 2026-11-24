"""Shrink a CRISP pixel sprite by 2 for free (owner 2026-11-23 "ลองซัก 50" on the 99 px Pro Flash Lu Bu). 3 ways, side by side:
 A = 2 x 2 average, colours snapped back to the sprite's own palette;  B = 2 x 2 'most common colour' with dark outline pixels winning;
 C = A + a fresh 1 px dark outline (pixel_punch style).   python3 tools/art/clash_halve.py in.png out_prefix"""
import sys, numpy as np
from PIL import Image
from collections import Counter
src, pre = sys.argv[1], sys.argv[2]
im = np.asarray(Image.open(src).convert('RGBA')).astype(int); h, w = im.shape[:2]; im = np.pad(im, ((0, h % 2), (0, w % 2), (0, 0))); h, w = im.shape[:2]
op = im[..., 3] > 0; pal = np.array(sorted({tuple(p) for p in im[op][:, :3]}))
def snap(c): return pal[np.argmin(((pal - c) ** 2).sum(1))]
A = np.zeros((h // 2, w // 2, 4), np.uint8); Bm = A.copy()
for y in range(0, h, 2):
    for x in range(0, w, 2):
        blk = im[y:y + 2, x:x + 2].reshape(-1, 4); vis = blk[blk[:, 3] > 0]
        if len(vis) < 2: continue
        A[y // 2, x // 2] = (*snap(vis[:, :3].mean(0)), 255)
        dark = vis[vis[:, :3].sum(1) < 120]
        pick = Counter(map(tuple, (dark if len(dark) >= 2 else vis)[:, :3])).most_common(1)[0][0]; Bm[y // 2, x // 2] = (*pick, 255)
C = A.copy(); al = C[..., 3] > 0
edge = al & ~(np.roll(al, 1, 0) & np.roll(al, -1, 0) & np.roll(al, 1, 1) & np.roll(al, -1, 1))
C[edge, :3] = (C[edge, :3] * .3 + np.array([20, 8, 14]) * .7).astype(np.uint8)
for tag, arr in (('A', A), ('B', Bm), ('C', C)): Image.fromarray(arr).save(f'{pre}_{tag}.png')
print('ok', A.shape[1], 'x', A.shape[0])
