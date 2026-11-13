# The chibi swordsman's pixel views (PixelLab B of the GPT pixel-style sheet, art/incoming/darkchibi/sword_v1/pl2_b.png) as stills for
# the map walk test (owner 2026-11-13 "ยังเก็บแมพพิกเซลที่เราเจนเยอะๆ ได้ไหม เอาตัวนี้ไปใส่ดูหน่อย"). Free.
# White joined to the border goes, tiny loose bits go (two red stubs left of the guide lines at the sword tips). 4 cells: front, 3/4, side, back.
# Also a half-size set (2x2 blocks: a dark outline pixel wins, else the most common colour) because the map's own hero is ~62 px tall.
#   python3 tools/art/chibi_map_hero.py -> art/td/map1/hero_chibi.png, hero_chibi_half.png (prints cell / feet numbers for map.html)
import numpy as np
from PIL import Image
from scipy import ndimage
A = np.asarray(Image.open('art/incoming/darkchibi/sword_v1/pl2_b.png').convert('RGB')).astype(int); H, W = A.shape[:2]
white = A.min(2) > 236; lab, n = ndimage.label(white); edge = set(lab[0]) | set(lab[-1]) | set(lab[:, 0]) | set(lab[:, -1]); bg = np.isin(lab, list(edge - {0}))
fig = ~bg; lab, n = ndimage.label(fig, structure=np.ones((3, 3))); sz = ndimage.sum(fig, lab, range(1, n + 1)); big = [i + 1 for i in range(n) if sz[i] > 2000]
obs = ndimage.find_objects(lab); big.sort(key=lambda i: obs[i - 1][1].start); assert len(big) == 4, len(big)
cells = []
for i in big:
    sl = obs[i - 1]; m = lab[sl] == i; rgba = np.dstack([A[sl], np.where(m, 255, 0)]).astype(np.uint8); ys, xs = np.where(m)
    boots = xs[(ys >= ys.max() - 3)]; body = xs[(ys > ys.max() - 40) & (ys < ys.max() - 8)]                 # feet point: under the legs, not under the sword tip
    cells.append((Image.fromarray(rgba), int(round(np.median(body))), m.shape[0]))
CW = max(c[0].width for c in cells) + 40; CH = max(c[2] for c in cells) + 4; FX, FY = CW // 2, CH - 2
sheet = Image.new('RGBA', (CW * 4, CH))
for j, (im, fx, h) in enumerate(cells): sheet.alpha_composite(im, (j * CW + FX - fx, FY - h))
sheet.save('art/td/map1/hero_chibi.png')
a = np.asarray(sheet); h2, w2 = a.shape[0] // 2, a.shape[1] // 2; out = np.zeros((h2, w2, 4), np.uint8)
for y in range(h2):
    for x in range(w2):
        b = a[y * 2:y * 2 + 2, x * 2:x * 2 + 2].reshape(4, 4); op = b[b[:, 3] > 0]
        if len(op) < 2: continue
        dk = op[op[:, :3].max(1) < 50]
        if len(dk) >= 2: out[y, x] = dk[0]; continue
        u, c = np.unique(op, axis=0, return_counts=True); out[y, x] = u[np.argmax(c)]
Image.fromarray(out).save('art/td/map1/hero_chibi_half.png'); print('full', CW, CH, FX, FY, 'half', w2 // 4, h2, FX // 2, FY // 2, 'body', [c[2] for c in cells])
