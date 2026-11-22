"""Turn the Meta AI effect videos (black background) into small frame sheets for dune.html, without a hard cut at the picture edge.

  python tools/art/dune_vfx.py

Picks the frames of each effect, lifts the video's near-black haze, softly fades the last pixels by the picture border (a flame
that reaches the border dissolves instead of ending in a straight line) and packs a WebP grid. The raw videos stay in art/incoming/dragon_vfx_meta/.
Updates the fx_* entries of art/dune/sprites.json.
"""
import json, os
import numpy as np, cv2
from PIL import Image

RAW = 'art/incoming/dragon_vfx_meta/'; CELL = 300; COLS = 6
def span(a, b, n): return [int(round(v)) for v in np.linspace(a, b, n)]
FX = {
    'fx_sweep': ('fx_sweep', span(2, 44, 17) + span(112, 158, 9), 8, 22),      # grows, then turns and dies out (the video's long still middle is skipped)
    'fx_thrust': ('fx_thrust', span(3, 24, 7) + span(30, 96, 5) + span(104, 152, 8) + span(158, 186, 6), 0, 22),   # the tail leaves on the left, where the hero's hands are
    'fx_spear_fall': ('fx_spear', span(56, 80, 9), 0, 22),                     # the whole spear; the game moves it down from the sky
    'fx_spear_burst': ('fx_spear', span(86, 158, 25), 0, 36),
    'fx_slam': ('fx_slam', span(1, 24, 10) + span(30, 112, 7), 5, 26),         # ground strike: the burst and twin flames (feet of the flames go on the ground)
    'fx_slam_ring': ('fx_slam', span(120, 182, 14), 3, 26),                    # its shock ring, placed separately so the ring lies on the ground
    'fx_spin': ('fx_spin', span(8, 40, 8) + span(44, 132, 15) + span(150, 198, 7), 0, 34),   # spinning spear
    'fx_lance': ('fx_lance', span(30, 62, 8) + span(66, 150, 12) + span(156, 196, 9), 0, 30),   # the ultimate: the tail leaves on the left, where the hero's hands are
}
def read(name):
    c = cv2.VideoCapture(RAW + name + '.mp4'); out = []
    while True:
        ok, f = c.read()
        if not ok: return out
        out.append(f)
cache = {}; sp = json.load(open('art/dune/sprites.json'))
for key, (video, idx, tail, feather) in FX.items():
    fr = cache.setdefault(video, read(video)); H, W = fr[0].shape[:2]; yy, xx = np.mgrid[0:H, 0:W]; d = np.minimum.reduce([xx, W - 1 - xx, yy, H - 1 - yy]) / feather; e = np.clip(d, 0, 1); edge = (e * e * (3 - 2 * e))[..., None]
    cells = []
    for n, i in enumerate(idx):
        f = np.clip((fr[i].astype(float) - 12) * 255 / 243, 0, 255) * edge
        if tail and n >= len(idx) - tail: f *= (len(idx) - n) / (tail + 1)   # dies out smoothly
        cells.append(cv2.resize(f.astype(np.uint8), (CELL, CELL), interpolation=cv2.INTER_AREA))
    cols = min(COLS, len(cells)); rows = (len(cells) + cols - 1) // cols; S = np.zeros((rows * CELL, cols * CELL, 3), np.uint8)
    for n, c in enumerate(cells): S[(n // cols) * CELL:(n // cols + 1) * CELL, (n % cols) * CELL:(n % cols + 1) * CELL] = c
    out = f'art/dune/fx/{key}.webp'; Image.fromarray(S[..., ::-1]).save(out, 'WEBP', quality=84, method=6)
    sp[key] = {'src': out, 'n': len(cells), 'cols': cols, 'w': CELL, 'h': CELL, 'fx': 1}
    m = max(int(max(c[:2].max(), c[-2:].max(), c[:, :2].max(), c[:, -2:].max())) for c in cells); print(f'{key}: {len(cells)} frames, brightest pixel on the very edge {m}')
for key, src in {'fx_pillar': 'art/incoming/dune_fx_pillar/fx_pillar.png'}.items():   # effects drawn as a 4 x 4 black sheet instead of a video
    if not os.path.exists(src): continue
    a = np.array(Image.open(src).convert('RGB')); H, W = a.shape[:2]; cw, ch = W // 4, H // 4; yy, xx = np.mgrid[0:ch, 0:cw]; e = np.clip(np.minimum.reduce([xx, cw - 1 - xx, yy, ch - 1 - yy]) / 7, 0, 1); edge = (e * e * (3 - 2 * e))[..., None]
    S = np.zeros((3 * CELL, COLS * CELL, 3), np.uint8)
    for n in range(16):
        c = cv2.resize((a[(n // 4) * ch:(n // 4 + 1) * ch, (n % 4) * cw:(n % 4 + 1) * cw] * edge).astype(np.uint8), (CELL, CELL), interpolation=cv2.INTER_CUBIC); S[(n // COLS) * CELL:(n // COLS + 1) * CELL, (n % COLS) * CELL:(n % COLS + 1) * CELL] = c
    out = f'art/dune/fx/{key}.webp'; Image.fromarray(S).save(out, 'WEBP', quality=84, method=6); sp[key] = {'src': out, 'n': 16, 'cols': COLS, 'w': CELL, 'h': CELL, 'fx': 1}; print(f'{key}: 16 frames from {src}')
json.dump(sp, open('art/dune/sprites.json', 'w'), separators=(',', ':'))
