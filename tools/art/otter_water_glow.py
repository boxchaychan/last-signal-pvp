"""Regrade the otter's own water effects into a glowing cyan look (deep teal, bright cyan, white foam, soft halo).

  python tools/art/otter_water_glow.py

Reads our Meta AI effect sheets (art/dune/fx_solid/fx_w_*.webp and the water fist / kick), leaves them untouched, and writes the graded copies
to art/dune/fx_kit/<key>.webp with the same layout, so dune.html can swap the whole set with &wfx=2. The owner's reference picture is another
artist's signed work: only its mood was looked at, it is not read or stored here.
"""
import json, os
import numpy as np, cv2
from PIL import Image

OUT = 'art/dune/fx_kit/'; os.makedirs(OUT, exist_ok=True); sp = json.load(open('art/dune/sprites.json'))
KEYS = ['fx_w_punch', 'fx_w_crown', 'fx_w_wave', 'fx_w_spin', 'fx_w_geyser', 'otter_wfist', 'otter_wkick']
STOPS = np.array([0, .2, .42, .64, .83, 1], np.float32); COLS = np.array([(3, 52, 104), (5, 100, 158), (8, 160, 216), (42, 218, 248), (156, 242, 252), (255, 255, 255)], np.float32) / 255; HALO = np.array([38, 208, 250], np.float32) / 255
BRIGHT = np.array([(8, 122, 196), (16, 168, 232), (40, 212, 250), (104, 236, 254), (196, 250, 255), (255, 255, 255)], np.float32) / 255   # the fist and the kick: no dark edge, so they read as light
def grade(f, gamma=.92, cols=COLS):
    rgb, a = f[..., :3], f[..., 3]; L = rgb[..., 0] * .3 + rgb[..., 1] * .59 + rgb[..., 2] * .11; u = np.clip((L - .07) / .85, 0, 1) ** gamma; c = np.dstack([np.interp(u, STOPS, cols[:, i]) for i in range(3)]).astype(np.float32)
    h, w = a.shape; e = np.minimum.reduce([np.arange(h)[:, None].repeat(w, 1), np.arange(w)[None].repeat(h, 0), h - 1 - np.arange(h)[:, None].repeat(w, 1), w - 1 - np.arange(w)[None].repeat(h, 0)]); k = w / 300   # the halo must fade before the cell edge
    glow = np.clip((cv2.GaussianBlur(a, (0, 0), 11 * k) * .75 + cv2.GaussianBlur(a, (0, 0), 3.5 * k) * .35) * 1.1, 0, 1) * .66 * np.clip(e / (14 * k), 0, 1); out = a + glow * (1 - a)
    pm = c * a[..., None] + HALO * (glow * (1 - a))[..., None]; return np.dstack([np.clip(pm / np.maximum(out[..., None], 1e-3), 0, 1), out])
NEW = {}
for key in KEYS:
    m = sp[key]; A = np.array(Image.open(m['src']).convert('RGBA'), np.float32) / 255; B = np.zeros_like(A); c = m.get('cols', m['n'])
    for i in range(m['n']):
        x, y = (i % c) * m['w'], (i // c) * m['h']; B[y:y + m['h'], x:x + m['w']] = grade(A[y:y + m['h'], x:x + m['w']], *((.74, BRIGHT) if key.startswith('otter_') else ()))
    p = f'{OUT}{key}.webp'; Image.fromarray((B * 255 + .5).astype(np.uint8), 'RGBA').save(p, 'WEBP', quality=86, alpha_quality=90, method=6); print(p, m['n'], os.path.getsize(p) // 1024, 'KB')
    if key.startswith('otter_'):   # the art fills its cell, so its light gets its own sheet: one cell = twice the width and height of the fist, same centre
        w = m['w']; G = np.zeros((w, w * m['n'], 4), np.float32); G[..., :3] = np.array([44, 216, 252], np.float32) / 255
        for i in range(m['n']):
            q = np.zeros((w * 2, w * 2), np.float32); q[w // 2:w // 2 + w, w // 2:w // 2 + w] = B[:w, i * w:(i + 1) * w, 3]; h = np.clip((cv2.GaussianBlur(q, (0, 0), 26) * 1.1 + cv2.GaussianBlur(q, (0, 0), 9) * .8) * 1.15, 0, .94); e = np.minimum.reduce([np.arange(w * 2)[:, None].repeat(w * 2, 1), np.arange(w * 2)[None].repeat(w * 2, 0), w * 2 - 1 - np.arange(w * 2)[:, None].repeat(w * 2, 1), w * 2 - 1 - np.arange(w * 2)[None].repeat(w * 2, 0)]); G[:w, i * w:(i + 1) * w, 3] = cv2.resize(h * np.clip(e / 34, 0, 1), (w, w), interpolation=cv2.INTER_AREA)
        g = f'{OUT}{key}_glow.webp'; Image.fromarray((G * 255 + .5).astype(np.uint8), 'RGBA').save(g, 'WEBP', quality=80, alpha_quality=88, method=6); NEW[key + '_glow'] = {'src': g, 'n': m['n'], 'w': w, 'h': w, 'cols': m['n']}; print(g, os.path.getsize(g) // 1024, 'KB')
sp.update(NEW); json.dump(sp, open('art/dune/sprites.json', 'w'), separators=(',', ':'))
