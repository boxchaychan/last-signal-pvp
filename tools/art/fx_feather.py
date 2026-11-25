"""Fade the cut edges of effect sheets (owner 2026-11-25: "ภาพสกิลยังไม่เต็ม", "ระวังล้นกรอบ": no effect may end in a straight line).

  python tools/art/fx_feather.py [key ...]      (default: every fx_m_* sheet in art/dune/sprites.json)

The Meta videos sometimes drew a ring or a slash bigger than the video frame, so the cut sheet has a flat edge where the frame ended.
For every side of a sheet where ANY frame reaches the cell border (alpha in the outer 4 px), all frames of that sheet get a soft
smoothstep fade over 15 % of the cell on that side (same on every frame, so nothing flickers); sides that never touch are untouched.
Run it after tools/art/moon_vfx.py. The sheets before this step are in git history (commit ea2994b); the raw videos are on the owner's PC.
"""
import json, sys
import numpy as np
from PIL import Image

sp = json.load(open('art/dune/sprites.json')); keys = sys.argv[1:] or [k for k in sp if k.startswith('fx_m_')]
def ramp(n, f):   # 0 at the border -> 1 after f px, smoothstep
    u = np.clip(np.arange(n) / max(1, f), 0, 1); return u * u * (3 - 2 * u)
for key in keys:
    v = sp[key]; S = np.array(Image.open(v['src']).convert('RGBA')).astype(np.float32); w, h, c, n = v['w'], v['h'], v['cols'], v['n']
    cells = [(i, (i // c) * h, (i % c) * w) for i in range(n)]; touch = {'l': 0, 'r': 0, 't': 0, 'b': 0}
    for i, y, x in cells:
        a = S[y:y + h, x:x + w, 3]
        touch['l'] = max(touch['l'], a[:, :4].max()); touch['r'] = max(touch['r'], a[:, -4:].max()); touch['t'] = max(touch['t'], a[:4].max()); touch['b'] = max(touch['b'], a[-4:].max())
    sides = [s for s, m in touch.items() if m > 25]
    if not sides: print(f'{key}: whole, nothing to do'); continue
    mx = np.ones(w, np.float32); my = np.ones(h, np.float32); fx, fy = w * .15, h * .15
    if 'l' in sides: mx *= ramp(w, fx)
    if 'r' in sides: mx *= ramp(w, fx)[::-1]
    if 't' in sides: my *= ramp(h, fy)
    if 'b' in sides: my *= ramp(h, fy)[::-1]
    M = my[:, None] * mx[None, :]
    for i, y, x in cells: S[y:y + h, x:x + w, 3] *= M
    Image.fromarray(np.clip(S, 0, 255).astype(np.uint8), 'RGBA').save(v['src'], 'WEBP', quality=88, alpha_quality=90, method=6)
    print(f'{key}: faded {"".join(sides)} (max edge alpha before {int(max(touch.values()))})')
