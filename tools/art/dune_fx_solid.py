"""Make the black-background effect sheets readable on the bright desert (added light vanishes on orange sand).

  python tools/art/dune_fx_solid.py

Reads art/dune/fx/<key>.webp (kept as they are), turns brightness into transparency so the flames keep their real colour,
adds a soft dark red rim round the shapes, writes art/dune/fx_solid/<key>.webp and points art/dune/sprites.json at it (solid: 1).
Run it again after tools/art/dune_vfx.py.
"""
import json, os
import numpy as np, cv2
from PIL import Image

OUT = 'art/dune/fx_solid'; os.makedirs(OUT, exist_ok=True); RIM = np.array([74, 13, 5], float) / 255
sp = json.load(open('art/dune/sprites.json'))
for key, m in sp.items():
    if not key.startswith('fx_'): continue
    src = f"art/dune/fx/{key}.webp"; a = np.array(Image.open(src).convert('RGB')).astype(np.float32) / 255; w, h, cols = m['w'], m['h'], m['cols']; S = np.zeros((a.shape[0], a.shape[1], 4), np.float32)
    for i in range(m['n']):
        x, y = (i % cols) * w, (i // cols) * h; c = a[y:y + h, x:x + w]; v = c.max(2); al = np.clip((v - .045) * 1.5, 0, 1) ** .82
        if key == 'fx_thrust': e = np.clip(np.arange(w, dtype=np.float32) / (w * .34), 0, 1); al = al * (e * e * (3 - 2 * e))[None, :]   # its tail leaves the picture on the left: fade it out instead of a straight cut
        col = np.clip(c / np.maximum(v[..., None], .04), 0, 1) * np.clip(v[..., None] * 1.15 + .12, 0, 1)   # the flame's own colour, not faded by black
        g = col.mean(2, keepdims=True); col = np.clip(g + (col - g) * 1.22, 0, 1)
        blur = cv2.GaussianBlur(al, (0, 0), max(1.5, w * .016)); rim = np.clip(blur * 1.9 - al, 0, 1) * .66
        out = al + rim * (1 - al); rgb = (col * al[..., None] + RIM * (rim * (1 - al))[..., None]) / np.maximum(out[..., None], 1e-3)
        S[y:y + h, x:x + w] = np.dstack([rgb, out])
    p = f'{OUT}/{key}.webp'; Image.fromarray((np.clip(S, 0, 1) * 255).astype(np.uint8), 'RGBA').save(p, 'WEBP', quality=86, alpha_quality=90, method=6)
    m['src'] = p; m['solid'] = 1; print(f'{key}: {os.path.getsize(p) // 1024} KB')
json.dump(sp, open('art/dune/sprites.json', 'w'), separators=(',', ':'))
