# The chibi swordsman's pixel views (PixelLab B of the GPT pixel-style sheet, art/incoming/darkchibi/sword_v1/pl2_b.png) as stills for
# the map walk test (owner 2026-11-13 "ยังเก็บแมพพิกเซลที่เราเจนเยอะๆ ได้ไหม เอาตัวนี้ไปใส่ดูหน่อย"). Free.
# White joined to the border goes, tiny loose bits go (two red stubs left of the guide lines at the sword tips). 4 cells: front, 3/4, side, back.
# Also a half-size set (2x2 blocks: a dark outline pixel wins, else the most common colour) because the map's own hero is ~62 px tall.
#   python3 tools/art/chibi_map_hero.py -> art/td/map1/hero_chibi.png, hero_chibi_half.png (prints cell / feet numbers for map.html)
import sys, numpy as np
from PIL import Image
from scipy import ndimage
SRC, OUT, MINSZ = (sys.argv[1], sys.argv[2], int(sys.argv[3])) if len(sys.argv) > 3 else ('art/incoming/darkchibi/sword_v1/pl2_b.png', 'hero_chibi', 2000)   # e.g. pl3_b36.png hero_chibi36 300 (the 36 px test; cream background)
A = np.asarray(Image.open(SRC).convert('RGB')).astype(int); H, W = A.shape[:2]
white = abs(A - A[1, 1]).sum(2) < 40; lab, n = ndimage.label(white); edge = set(lab[0]) | set(lab[-1]) | set(lab[:, 0]) | set(lab[:, -1]); bg = np.isin(lab, list(edge - {0}))
fig = ~bg; lab, n = ndimage.label(fig, structure=np.ones((3, 3))); sz = ndimage.sum(fig, lab, range(1, n + 1)); big = [i + 1 for i in range(n) if sz[i] > MINSZ]
obs = ndimage.find_objects(lab); big.sort(key=lambda i: obs[i - 1][1].start); NV = len(big); assert NV in (3, 4), NV      # 3 views (front, side, back) or 4 (front, 3/4, side, back)
cells = []
for i in big:
    sl = obs[i - 1]; m = lab[sl] == i; rgba = np.dstack([A[sl], np.where(m, 255, 0)]).astype(np.uint8); ys, xs = np.where(m)
    boots = xs[(ys >= ys.max() - 3)]; body = xs[(ys > ys.max() - m.shape[0] * .3) & (ys < ys.max() - m.shape[0] * .06)]                 # feet point: under the legs, not under the sword tip
    cells.append((Image.fromarray(rgba), int(round(np.median(body))), m.shape[0]))
CW = max(c[0].width for c in cells) + (40 if MINSZ > 1000 else 14); CH = max(c[2] for c in cells) + 4; FX, FY = CW // 2, CH - 2
sheet = Image.new('RGBA', (CW * NV, CH))
for j, (im, fx, h) in enumerate(cells): sheet.alpha_composite(im, (j * CW + FX - fx, FY - h))
if len(sys.argv) > 4 and sys.argv[4] == 'halo':          # PixelLab left a pale 1 px rim round the small sprite (white background bleeding in): take it off, one pass
    q = np.asarray(sheet).copy(); op = q[..., 3] > 0; rgb = q[..., :3].astype(int); pale = op & (rgb.min(2) > 175) & (rgb.max(2) - rgb.min(2) < 34)
    out_n = ~op; near = np.zeros_like(op)
    for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)): near |= np.roll(out_n, (dy, dx), (0, 1))
    q[pale & near, 3] = 0; sheet = Image.fromarray(q)
sheet.save('art/td/map1/%s.png' % OUT)
a = np.asarray(sheet); h2, w2 = a.shape[0] // 2, a.shape[1] // 2; out = np.zeros((h2, w2, 4), np.uint8)
for y in range(h2):
    for x in range(w2):
        b = a[y * 2:y * 2 + 2, x * 2:x * 2 + 2].reshape(4, 4); op = b[b[:, 3] > 0]
        if len(op) < 2: continue
        dk = op[op[:, :3].max(1) < 50]
        if len(dk) >= 2: out[y, x] = dk[0]; continue
        u, c = np.unique(op, axis=0, return_counts=True); out[y, x] = u[np.argmax(c)]
Image.fromarray(out).save('art/td/map1/%s_half.png' % OUT); print('full', CW, CH, FX, FY, 'half', w2 // NV, h2, FX // 2, FY // 2, 'body', [c[2] for c in cells])
