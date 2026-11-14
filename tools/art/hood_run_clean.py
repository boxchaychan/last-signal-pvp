# Hooded rabbit run (PixelLab pixminimax, 2026-11-14): PixelLab drew cream dust puffs at the feet although the brief said "no dust".
# This keeps the raw frames and writes a second set without the puffs, so the owner can pick (rule: never strip without showing both).
# A puff = a light cream patch in the lower part of the frame whose edge is mostly open air (cloth flaps there are ringed by dark outline).
import sys, numpy as np
from PIL import Image
from collections import deque
src, dst = sys.argv[1], sys.argv[2]
a = np.asarray(Image.open(src).convert('RGBA')).copy(); H, W = a.shape[:2]
light = (a[..., 3] > 0) & (a[..., :3].min(2) > 195)
seen = np.zeros((H, W), bool)
for y0 in range(58, H):
    for x0 in range(W):
        if not light[y0, x0] or seen[y0, x0]: continue
        comp, q, air, dark = [], deque([(y0, x0)]), 0, 0; seen[y0, x0] = 1
        while q:
            y, x = q.popleft(); comp.append((y, x))
            for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if not (0 <= yy < H and 0 <= xx < W): air += 1; continue
                if light[yy, xx] and yy >= 58:
                    if not seen[yy, xx]: seen[yy, xx] = 1; q.append((yy, xx))
                elif a[yy, xx, 3] == 0: air += 1
                else: dark += 1
        if air > dark * .6:
            for y, x in comp: a[y, x] = 0
# loose specks left over: tiny islands away from the body
alpha = a[..., 3] > 0; lab = np.zeros((H, W), int); n = 0; sizes = {}
for y0 in range(H):
    for x0 in range(W):
        if alpha[y0, x0] and not lab[y0, x0]:
            n += 1; q = deque([(y0, x0)]); lab[y0, x0] = n; c = 0
            while q:
                y, x = q.popleft(); c += 1
                for yy in (y - 1, y, y + 1):
                    for xx in (x - 1, x, x + 1):
                        if 0 <= yy < H and 0 <= xx < W and alpha[yy, xx] and not lab[yy, xx]: lab[yy, xx] = n; q.append((yy, xx))
            sizes[n] = c
main = max(sizes, key=sizes.get)
for k, c in sizes.items():
    if k != main and c < 12: a[lab == k] = 0
Image.fromarray(a).save(dst)
