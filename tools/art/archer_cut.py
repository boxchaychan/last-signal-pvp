# Sky Huntress (painted 2D archer) for hoodfall.html: cut Codex's 14 move sheets (art/incoming/archer/<move>.png,
# 1536x1024, 4 x 3 cells, flat green #00B140, a dark ground line in every cell, side view facing right) into ONE packed sheet.
#   python tools/art/archer_cut.py            -> art/sidegame/archer.webp + archer.json
# - green keyed out with a soft edge + despill; the ground line removed (dark, flat rows near the cell bottom)
# - feet = the ground line of each cell, x anchor = the cell centre (Codex draws the body centred in its cell)
# - scaled so the standing body is BODY px tall x OUT_K (drawn at 1/OUT_K world size on the full-res canvas, stays sharp)
# - SKIP drops frames per move (shot2 frames 2, 3 = 0-based: she turned her back; owner asked Codex to redraw them)
import json, os, sys
import numpy as np
from PIL import Image
SRC, DST = 'art/incoming/archer', 'art/sidegame'
MOVES = ['idle', 'run', 'shot1', 'shot2', 'shot3', 'jump', 'hurt', 'death', 'skill_rain', 'skill_gale', 'skill_fan', 'skill_frost', 'skill_flip', 'skill_wolf']
SKIP = {'shot2': [2, 3]} if not os.environ.get('NOSKIP') else {}
BODY, OUT_K = 80, 3          # world px tall (the rabbit is ~75), stored 3x
def key(rgb):
    r, g, b = [rgb[..., i].astype(float) for i in range(3)]
    m = np.maximum(r, b); gr = g - m                      # how much greener than the other channels
    a = np.clip(1 - (gr - 25) / 45, 0, 1)                 # >70 greener = background, <25 = body
    out = rgb.astype(float).copy(); out[..., 1] = np.minimum(g, m + 12)   # despill
    return out, a
def ground_line(a, rgb):
    h, w = a.shape; lum = rgb.mean(2)
    dark = (a > .5) & (lum < 70)
    best = None
    for y in range(int(h * .7), h - 2):
        n = dark[y].sum()
        if n > w * .3 and (best is None or n > best[1]): best = (y, n)
    return best[0] if best else int(h * .9)
cells = []
for mv in MOVES:
    im = np.asarray(Image.open(f'{SRC}/{mv}.png').convert('RGB')); H, W = im.shape[:2]
    cw, ch = W / 4, H / 3; k = 0
    for r in range(3):
        for c in range(4):
            x0, y0 = round(c * cw), round(r * ch); cell = im[y0:round(y0 + ch), x0:round(x0 + cw)]
            rgb, a = key(cell); gy = ground_line(a, cell)
            lum = cell.mean(2)
            for y in range(gy - 3, min(a.shape[0], gy + 4)):          # line pixels: dark, with background a few rows above
                above = a[max(0, y - 6)]
                a[y][(lum[y] < 90) & (above < .3)] = 0
            a[gy + 4:] = 0                                          # nothing under the ground line
            if k not in SKIP.get(mv, []): cells.append((mv, k, rgb, a, gy, cell.shape[1] / 2))
            k += 1
# scale from the idle frames' standing height
hs = []
for mv, k, rgb, a, gy, cx in cells:
    if mv == 'idle': ys = np.where(a.max(1) > .5)[0]; hs.append(gy - ys.min())
S = BODY * OUT_K / np.median(hs)
# common box around the anchor (feet), over all frames
L = T = Rr = 0
for mv, k, rgb, a, gy, cx in cells:
    ys, xs = np.where(a > .1); L = min(L, xs.min() - cx); Rr = max(Rr, xs.max() - cx); T = min(T, ys.min() - gy)
B = 6 / S
fw, fh = int(np.ceil((Rr - L) * S)) + 4, int(np.ceil((-T + B) * S)) + 4
fx, fy = int(np.ceil(-L * S)) + 2, int(np.ceil(-T * S)) + 2
rows = {}; per = {}
for mv, k, rgb, a, gy, cx in cells: per.setdefault(mv, []).append((k, rgb, a, gy, cx))
ncol = max(len(v) for v in per.values())
sheet = Image.new('RGBA', (fw * ncol, fh * len(MOVES)), (0, 0, 0, 0))
for ri, mv in enumerate(MOVES):
    rows[mv] = {'row': ri, 'n': len(per[mv])}
    for ci, (k, rgb, a, gy, cx) in enumerate(per[mv]):
        rgba = np.dstack([rgb, a * 255]).clip(0, 255).astype(np.uint8)
        im = Image.fromarray(rgba, 'RGBA')
        # premultiplied resize so keyed edges do not pick up green / dark fringes
        sw, sh = max(1, round(im.width * S)), max(1, round(im.height * S))
        pm = np.asarray(im).astype(float); pm[..., :3] *= pm[..., 3:4] / 255
        rs = np.asarray(Image.fromarray(pm.clip(0, 255).astype(np.uint8), 'RGBA').resize((sw, sh), Image.LANCZOS)).astype(float)
        al = rs[..., 3:4]; rs[..., :3] = np.where(al > 0, rs[..., :3] * 255 / np.maximum(al, 1), 0)
        im = Image.fromarray(rs.clip(0, 255).astype(np.uint8), 'RGBA')
        px, py = round(fx - cx * S), round(fy - gy * S)
        frame = Image.new('RGBA', (fw, fh), (0, 0, 0, 0)); frame.paste(im, (px, py), im)
        sheet.alpha_composite(frame, (ci * fw, ri * fh))
sheet.save(f'{DST}/archer.webp', quality=90, method=6)
meta = {'w': fw, 'h': fh, 'fx': fx, 'fy': fy, 'k': OUT_K, 'rows': rows, 'skip': SKIP}
json.dump(meta, open(f'{DST}/archer.json', 'w'))
print(meta, sheet.size, os.path.getsize(f'{DST}/archer.webp'))
