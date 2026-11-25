"""Cut the moon blade's Meta AI effect videos (black background, 1280x720) into solid-colour frame sheets for dune.html.

  python tools/art/moon_vfx.py [raw folder]      (default art/incoming/moon_vfx/; the .mp4 are git-ignored, they live in the main folder)

Per effect: picks frames, lifts the video's black haze, crops to the area the effect really uses (keeps its shape, no squashing),
fades the last pixels by the video border (an arc that touches the border dissolves instead of ending in a straight line),
turns brightness into transparency with the effect's own colour and a dark violet rim (readable on the orange desert,
the lesson of tools/art/dune_fx_solid.py), writes art/dune/fx_moon/<key>.webp and the fx_m_* entries of art/dune/sprites.json.
Prompts: art/incoming/moon_vfx/PROMPTS_META.txt.
"""
import json, os, sys
import numpy as np, cv2
from PIL import Image

RAW = sys.argv[1] if len(sys.argv) > 1 else 'art/incoming/moon_vfx/'; OUT = 'art/dune/fx_moon'; os.makedirs(OUT, exist_ok=True)
RIM = np.array([34, 8, 58], np.float32) / 255; LONG = 360; COLS = 8
def span(a, b, n): return [int(round(v)) for v in np.linspace(a, b, n)]
FX = {   # key: (video, frames, frames that fade out at the end)
    'fx_m_c1': ('fx_m_combo', span(12, 44, 9), 3),        # combo hit 1: slash from top-left down to the right
    'fx_m_c2': ('fx_m_combo', span(52, 76, 8), 3),        # combo hit 2: rising slash
    'fx_m_c3': ('fx_m_combo', span(112, 172, 12), 4),     # combo hit 3: wide horizontal slash
    'fx_m_wave': ('fx_m_wave', span(2, 40, 8) + span(46, 168, 14) + span(172, 196, 6), 5),   # K: crescent wave flying right
    'fx_m_flurry': ('fx_m_flurry', span(24, 156, 26), 4), # rapid multi-hit cuts
    'fx_m_spin': ('fx_m_spin', span(4, 140, 24), 4),      # ring of crescents spinning round the body
    'fx_m_fall': ('fx_m_fall', span(0, 40, 10) + span(44, 190, 14), 5),   # blade falls, moon circle on the ground
    'fx_m_moon': ('fx_m_moon', span(0, 84, 14), 0),       # the full moon of the ultimate (the blade rain is drawn in code)
}
def read(name):
    c = cv2.VideoCapture(RAW + name + '.mp4'); out = []
    while True:
        ok, f = c.read()
        if not ok: return out
        out.append(f)
cache = {}; sp = json.load(open('art/dune/sprites.json'))
for key, (video, idx, tail) in FX.items():
    if not os.path.exists(RAW + video + '.mp4'): print(key, 'video missing'); continue
    fr = cache.setdefault(video, read(video)); H, W = fr[0].shape[:2]; idx = [min(i, len(fr) - 1) for i in idx]
    yy, xx = np.mgrid[0:H, 0:W]; e = np.clip(np.minimum.reduce([xx, W - 1 - xx, yy, H - 1 - yy]) / 26, 0, 1); edge = (e * e * (3 - 2 * e))[..., None]
    fs = [np.clip((fr[i][..., ::-1].astype(np.float32) - 12) / 243, 0, 1) * edge for i in idx]
    on = cv2.dilate((np.max([f.max(2) for f in fs], 0) > .2).astype(np.uint8), np.ones((9, 9), np.uint8)); n_, lab, st, _ = cv2.connectedComponentsWithStats(on, 8); keep = [i for i in range(1, n_) if st[i, 4] > 600]; on = np.isin(lab, keep); ys, xs = np.where(on); pad = 22   # the bright shapes, not the faint spark dust
    x0, x1, y0, y1 = max(0, xs.min() - pad), min(W, xs.max() + pad), max(0, ys.min() - pad), min(H, ys.max() + pad)
    k = LONG / max(x1 - x0, y1 - y0); w, h = max(8, round((x1 - x0) * k)), max(8, round((y1 - y0) * k)); cols = min(COLS, len(fs)); rows = (len(fs) + cols - 1) // cols
    S = np.zeros((rows * h, cols * w, 4), np.float32)
    for n, f in enumerate(fs):
        c = cv2.resize(f[y0:y1, x0:x1], (w, h), interpolation=cv2.INTER_AREA)
        if tail and n >= len(fs) - tail: c = c * ((len(fs) - n) / (tail + 1))   # dies out smoothly
        v = c.max(2); al = np.clip((v - .045) * 1.6, 0, 1) ** .8
        col = np.clip(c / np.maximum(v[..., None], .04), 0, 1) * np.clip(v[..., None] * 1.15 + .12, 0, 1); g = col.mean(2, keepdims=True); col = np.clip(g + (col - g) * 1.2, 0, 1)
        blur = cv2.GaussianBlur(al, (0, 0), max(1.4, LONG * .006)); rim = np.clip(blur * 1.9 - al, 0, 1) * .7
        o = al + rim * (1 - al); rgb = (col * al[..., None] + RIM * (rim * (1 - al))[..., None]) / np.maximum(o[..., None], 1e-3)
        S[(n // cols) * h:(n // cols + 1) * h, (n % cols) * w:(n % cols + 1) * w] = np.dstack([rgb, o])
    out = f'{OUT}/{key}.webp'; Image.fromarray((S * 255).astype(np.uint8), 'RGBA').save(out, 'WEBP', quality=88, alpha_quality=90, method=6)
    sp[key] = {'src': out, 'n': len(fs), 'cols': cols, 'w': w, 'h': h, 'fx': 1, 'solid': 1, 'cx': (W / 2 - x0) * k, 'foot': (H / 2 - y0) * k}   # cx / foot = where the VIDEO centre lands in the cell
    print(f'{key}: {len(fs)} frames {w}x{h}, crop x {x0}-{x1} y {y0}-{y1}, {os.path.getsize(out) // 1024} KB')
json.dump(sp, open('art/dune/sprites.json', 'w'), separators=(',', ':'))
