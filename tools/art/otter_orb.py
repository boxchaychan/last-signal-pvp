"""Paint the otter's water orb in code: a clear glass-like ball with water turning inside it, 12 looping frames.

  python tools/art/otter_orb.py

Writes art/dune/otter/orb.webp and the otter_orb entry of art/dune/sprites.json.
"""
import json
import numpy as np, cv2
from PIL import Image

CELL, SS, N = 96, 4, 12; S = CELL * SS; y, x = np.mgrid[0:S, 0:S].astype(np.float32); x = (x + .5) / S * 2 - 1; y = (y + .5) / S * 2 - 1; r = np.hypot(x, y); th = np.arctan2(y, x)
NAVY, DEEP, BLUE, CYAN, PALE, WHITE = [np.array(c, np.float32) / 255 for c in ((10, 44, 128), (10, 92, 214), (20, 150, 245), (86, 224, 255), (196, 248, 255), (255, 255, 255))]
def ss(a, b, v): q = np.clip((v - a) / (b - a), 0, 1); return q * q * (3 - 2 * q)
def mix(rgb, col, k): return rgb * (1 - k[..., None]) + col * k[..., None]
R = .86; ball = 1 - ss(R - .012, R + .012, r); u = np.clip(r / R, 0, 1)
sheet = np.zeros((CELL, CELL * N, 4), np.float32)
for f in range(N):
    ph = f / N * 2 * np.pi
    rgb = mix(np.broadcast_to(CYAN, (S, S, 3)).copy(), BLUE, ss(.25, .72, u)); rgb = mix(rgb, DEEP, ss(.66, 1, u))            # clear blue in the middle, deep at the edge
    al = .46 + .5 * ss(.3, .98, u)
    arm = np.sin(2 * th + 6.0 * u - ph); band = ss(.12, .3, u) * (1 - ss(.74, .92, u))                                       # two soft arms of water turning inside
    rgb = mix(rgb, CYAN, ss(.05, .55, arm) * band * .9); al = al + ss(.05, .55, arm) * band * .3
    rgb = mix(rgb, PALE, ss(.62, .92, arm) * band); al = al + ss(.62, .92, arm) * band * .2
    core = 1 - ss(.07, .17, u); rgb = mix(rgb, PALE, core); al = al + core * .35
    d = np.hypot(x + .05, y + .17); cres = ss(.67, .75, d) * ss(.02, .3, y) * ball; rgb = mix(rgb, PALE, cres * .85); al = al + cres * .3   # light caught along the bottom
    e = ((x + .33) * .82 + (y + .38) * .57) ** 2 / .042 + ((x + .33) * -.57 + (y + .38) * .82) ** 2 / .012; hi = 1 - ss(.75, 1.1, e)    # the big shine stays still
    dot = (1 - ss(.04, .058, np.hypot(x + .02, y + .6))) + (1 - ss(.028, .044, np.hypot(x - .4, y - .34)))
    rgb = mix(rgb, WHITE, np.clip(hi + dot, 0, 1)); al = np.clip(al + hi + dot, 0, 1) * ball
    rim = ss(R - .055, R - .012, r) * (1 - ss(R + .022, R + .05, r)); rgb = mix(rgb, NAVY, rim * .95); al = np.maximum(al, rim * .92)   # a thin dark edge so it reads on bright sand
    glow = (1 - ss(R, .995, r)) * (r > R) * .3; out = al + glow * (1 - al); rgb = (rgb * al[..., None] + CYAN * (glow * (1 - al))[..., None]) / np.maximum(out[..., None], 1e-3)
    pm = np.dstack([rgb * out[..., None], out]); sm = cv2.resize(pm, (CELL, CELL), interpolation=cv2.INTER_AREA); a = sm[..., 3:]; sheet[:, f * CELL:(f + 1) * CELL] = np.dstack([np.clip(sm[..., :3] / np.maximum(a, 1e-3), 0, 1), a])
OUT = 'art/dune/otter/orb.webp'; Image.fromarray((np.clip(sheet, 0, 1) * 255 + .5).astype(np.uint8), 'RGBA').save(OUT, 'WEBP', quality=92, alpha_quality=96, method=6)
sp = json.load(open('art/dune/sprites.json')); sp['otter_orb'] = {'src': OUT, 'n': N, 'w': CELL, 'h': CELL, 'cols': N}; json.dump(sp, open('art/dune/sprites.json', 'w'), separators=(',', ':')); print(OUT, sheet.shape)
