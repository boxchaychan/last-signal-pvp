# Hooded rabbit attack sheet (owner's Meta / GPT picture 2026-11-14, 3 rows x 4 frames on transparency, drawn ~4.2x our 59x75 sprite)
# -> 12 frames back on our own pixel grid, feet lined up with the run, effects KEPT as drawn (rule: never strip without asking).
# Grid: period P = idle-frame height / 75; the phase is found per frame (cells should be flat inside), then each cell's centre is sampled.
import sys, json, numpy as np
from PIL import Image
# v1 = first sheet (horizontal swing / overhead smash / thrust); v2 = second sheet (big arcs, owner 2026-11-14 "ภาพมันกระโดด เอาอันนี้แทน").
# v2 also lines frames up by the glowing EYES (head steady, only the blade and effects move) instead of the feet alone: v1 jumped up to 30 px.
V = sys.argv[1] if len(sys.argv) > 1 else 'v2'
SHEETS = {
  'v1': ('art/incoming/hood/attack/sheet_raw.webp', 'art/sidegame/rabbit_attack_v1.png', [(40, 410), (410, 885), (885, 1260)],
         [[(72, 320), (428, 953), (1003, 1402), (1466, 1906)], [(72, 326), (396, 941), (1017, 1429), (1521, 1908)], [(37, 512), (512, 1040), (1040, 1460), (1562, 1821)]], False),
  'v2': ('art/incoming/hood/attack/sheet2_raw.webp', 'art/sidegame/rabbit_attack.png', [(20, 410), (425, 845), (860, 1265)],
         [[(88, 324), (511, 894), (981, 1456), (1532, 1920)], [(31, 414), (462, 904), (991, 1443), (1482, 1901)], [(28, 408), (476, 930), (996, 1504), (1560, 1815)]], True)}
SHEETS['v3'] = ('art/incoming/hood/attack/sheet3_raw.webp', 'art/sidegame/rabbit_attack3.png', [(10, 250), (262, 510), (520, 765), (795, 1020)],
         [[(99, 267), (471, 696), (848, 1097), (1230, 1494)], [(81, 353), (468, 739), (852, 1137), (1232, 1518)],
          [(80, 359), (469, 740), (841, 1121), (1223, 1492)], [(69, 323), (455, 682), (853, 1037), (1241, 1420)]], True)   # 16 in-between frames, owner 2026-11-14
SRC, OUT, ROWS, CELLS, BY_EYES = SHEETS[V]
A = np.asarray(Image.open(SRC).convert('RGBA')).astype(float)
P = {'v3': 207 / 75}.get(V, 315 / 75)   # the idle frame's height over our sprite's 75 px
def snap(c):
    H, W = c.shape[:2]; best = None
    for oy in np.arange(0, P, P / 6):
        for ox in np.arange(0, P, P / 6):
            ys = np.arange(oy + P / 2, H - 1, P); xs = np.arange(ox + P / 2, W - 1, P)
            Y, X = np.meshgrid(ys, xs, indexing='ij'); cost = 0
            for dy, dx in ((-P * .3, 0), (P * .3, 0), (0, -P * .3), (0, P * .3)):
                a = c[np.clip((Y + dy).round().astype(int), 0, H - 1), np.clip((X + dx).round().astype(int), 0, W - 1)]
                b = c[Y.round().astype(int), X.round().astype(int)]; cost += np.abs(a - b).sum()
            if best is None or cost < best[0]: best = (cost, Y.round().astype(int), X.round().astype(int))
    o = c[best[1], best[2]].copy(); o[..., 3] = np.where(o[..., 3] > 110, 255, 0); return o.astype(np.uint8)
def feet(o):   # anchor = mean x of the dark (boot / body) pixels in the lowest 4 rows that have any, and that lowest row
    dark = (o[..., 3] > 0) & (o[..., :3].max(2) < 110); ys = np.where(dark.any(1))[0]; yb = ys[-1]
    return float(np.where(dark[yb - 3:yb + 1].any(0))[0].mean()), int(yb)
def eyes(o):   # the two glowing orange eyes inside the black face: bright orange pixels with plenty of near-black around them
    m = (o[..., 3] > 0) & (o[..., 0] > 220) & (o[..., 1] > 110) & (o[..., 1] < 210) & (o[..., 2] < 90); dark = (o[..., 3] > 0) & (o[..., :3].max(2) < 60)
    pts = [(y, x) for y, x in zip(*np.where(m)) if 2 < y < o.shape[0] - 3 and 2 < x < o.shape[1] - 3 and dark[y - 2:y + 3, x - 2:x + 3].sum() > 8]
    return (float(np.mean([p[1] for p in pts])), float(np.mean([p[0] for p in pts]))) if len(pts) >= 2 else None
run0 = np.asarray(Image.open('art/sidegame/rabbit_run.png').convert('RGBA'))[:, :128]
RX, RY = feet(run0); FEET_RUN = (50, 92)   # the run's own feet point in the game
frames = []
for r, (y0, y1) in enumerate(ROWS):
    for (x0, x1) in CELLS[r]:
        o = snap(A[y0:y1, x0:x1]); fx, fy = feet(o)
        if BY_EYES:   # keep the feet row, but put the eyes where the run's stance has them (x only: the head may dip in a swing)
            e, er = eyes(o), eyes(run0)
            if e and er: fx = e[0] - (er[0] - RX)
        frames.append((o, fx, fy))
# where the run's dark-feet anchor sits relative to the game feet point
dx_run, dy_run = RX - FEET_RUN[0], RY - FEET_RUN[1]
L = max(fx - dx_run for o, fx, fy in frames); R = max(o.shape[1] - (fx - dx_run) for o, fx, fy in frames)
U = max(fy - dy_run for o, fx, fy in frames); D = max(o.shape[0] - (fy - dy_run) for o, fx, fy in frames)
CW, CH = int(np.ceil(L + R)) + 2, int(np.ceil(U + D)) + 2; FX, FY = int(np.ceil(L)) + 1, int(np.ceil(U)) + 1
sheet = Image.new('RGBA', (CW * len(frames), CH), (0, 0, 0, 0))
for i, (o, fx, fy) in enumerate(frames):
    px, py = FX - int(round(fx - dx_run)), FY - int(round(fy - dy_run)); sheet.alpha_composite(Image.fromarray(o), (i * CW + px, py))
sheet.save(OUT); json.dump({'cw': CW, 'ch': CH, 'feet': [FX, FY], 'frames': len(frames)}, open(OUT.replace('.png', '.json'), 'w'))
print('cell', CW, CH, 'feet', FX, FY, [f[0].shape[:2] for f in frames])
