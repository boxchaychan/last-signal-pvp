# Owner's Meta AI sprite SHEET of the samurai shiba (2026-11-13, made with ref3_shiba2_magenta.png: 3 rows x 7 figures, 2000x1691,
# see-through background; this time he matches OUR shiba). Raw: art/incoming/dogcat/meta/shiba_sheet_v1.png. Nothing is removed:
# slash arcs, speed lines, sparkles, spin rings and the ground line under the feet stay as drawn.
# Figures are not on a grid and some swords reach into the next figure, so every frame has its own cut rule (x range + exceptions).
# Each frame is pinned by the middle of its ground line. Size x0.4 (box) with hard alpha -> figure ~120 px. Cell 280x180, feet 120,172.
#   python3 tools/art/meta_sheet.py -> art/poses/combo/shiba_sheet_frames.png (7 columns x 3 rows, same order as the sheet) + _check.png
import numpy as np
from PIL import Image
A = np.asarray(Image.open('art/incoming/dogcat/meta/shiba_sheet_v1.png').convert('RGBA')); H, W = A.shape[:2]; yy, xx = np.mgrid[0:H, 0:W]
R = [(220, 560), (740, 1120), (1320, 1625)]
def band(r, x0, x1, extra=None, drop=None):
    y0, y1 = R[r]; m = (yy >= y0) & (yy < y1) & (xx >= x0) & (xx < x1)
    if extra is not None: m |= extra
    if drop is not None: m &= ~drop
    return m
def box(r, x0, x1, ya, yb): return (xx >= x0) & (xx < x1) & (yy >= R[r][0] + ya) & (yy < R[r][0] + yb)
F = [band(0, 0, 272), band(0, 272, 535), band(0, 535, 835), band(0, 835, 1140, box(0, 1140, 1240, 165, 205)), band(0, 1140, 1398, box(0, 1398, 1548, 160, 205), box(0, 1140, 1153, 0, 165)),
     band(0, 1398, 1722, None, box(0, 1398, 1548, 160, 205) & (xx < 1470)), band(0, 1722, 2000),
     band(1, 0, 305), band(1, 305, 540), band(1, 540, 790, box(1, 790, 810, 250, 290)), band(1, 772, 1070, None, box(1, 772, 810, 250, 290) | (xx < 772)),
     band(1, 1080, 1352, box(1, 1352, 1380, 300, 380)), band(1, 1352, 1675, None, box(1, 1352, 1380, 300, 380)), band(1, 1680, 2000),
     band(2, 0, 260), band(2, 260, 480), band(2, 480, 680), band(2, 680, 992), band(2, 992, 1296), band(2, 1296, 1688), band(2, 1688, 2000)]
CW, CH, FX, FY, K = 280, 180, 120, 172, .4
sheet = Image.new('RGBA', (CW * 7, CH * 3))
for i, m in enumerate(F):
    a = A.copy(); a[~m] = 0; ys, xs = np.where(a[..., 3] > 40); y1 = ys.max(); gx = xs[ys >= y1 - 3]; ax = (gx.min() + gx.max()) / 2      # ground line = the bottom rows
    x0, x1, y0 = xs.min(), xs.max() + 1, ys.min(); im = Image.fromarray(a[y0:y1 + 1, x0:x1])
    im = im.resize((max(1, round(im.width * K)), max(1, round(im.height * K))), Image.BOX); p = np.asarray(im).copy(); p[..., 3] = np.where(p[..., 3] > 110, 255, 0); im = Image.fromarray(p)
    sheet.alpha_composite(im, (i % 7 * CW + FX - round((ax - x0) * K), i // 7 * CH + FY - im.height))
sheet.save('art/poses/combo/shiba_sheet_frames.png', optimize=True)
c = Image.new('RGBA', sheet.size, (120, 160, 120, 255)); c.alpha_composite(sheet); c.save('art/poses/combo/shiba_sheet_frames_check.png'); print(sheet.size)
