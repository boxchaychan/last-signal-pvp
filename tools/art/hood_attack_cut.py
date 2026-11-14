# Hooded rabbit attack sheet (owner's Meta / GPT picture 2026-11-14, 3 rows x 4 frames on transparency, drawn ~4.2x our 59x75 sprite)
# -> 12 frames back on our own pixel grid, feet lined up with the run, effects KEPT as drawn (rule: never strip without asking).
# Grid: period P = idle-frame height / 75; the phase is found per frame (cells should be flat inside), then each cell's centre is sampled.
import sys, json, numpy as np
from PIL import Image
SRC, OUT = 'art/incoming/hood/attack/sheet_raw.webp', 'art/sidegame/rabbit_attack.png'
A = np.asarray(Image.open(SRC).convert('RGBA')).astype(float)
CELLS = [[(72, 320), (428, 953), (1003, 1402), (1466, 1906)], [(72, 326), (396, 941), (1017, 1429), (1521, 1908)], [(37, 512), (512, 1040), (1040, 1460), (1562, 1821)]]
ROWS = [(40, 410), (410, 885), (885, 1260)]
P = 315 / 75
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
run0 = np.asarray(Image.open('art/sidegame/rabbit_run.png').convert('RGBA'))[:, :128]
RX, RY = feet(run0); FEET_RUN = (50, 92)   # the run's own feet point in the game
frames = []
for r, (y0, y1) in enumerate(ROWS):
    for (x0, x1) in CELLS[r]:
        o = snap(A[y0:y1, x0:x1]); fx, fy = feet(o); frames.append((o, fx, fy))
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
