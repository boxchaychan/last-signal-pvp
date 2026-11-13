#!/usr/bin/env python3
"""Purple - gold - white "light" copies of effects we already own (owner 2026-11-13: "ม่วงทองขาว", "แบบแสง", "ทุกท่าเลยที่เป็นม่วงดำ").
usage: [LOOK=neon|gold] fx_goldlight.py [key ...]  -> fx/<key>_n.png (neon violet + white, the default, the look the owner chose) or <key>_g.png (purple - gold - white) + a manifest entry (same cells / anchor / fps, add: 1 = draw with 'lighter').
Colour by a gradient map on brightness x (1 - 0.62 x saturation): the coloured body turns violet, pale parts gold, the white core stays white.
A soft violet halo is added round each frame (inside its own cell). The originals and the plain violet copies (_v) are not touched."""
import sys, json, numpy as np
from PIL import Image, ImageFilter
KEYS = sys.argv[1:] or ['dslash%d' % i for i in range(8)] + ['dslashl%d' % i for i in range(8)] + ['dslashs%d' % i for i in range(8)] + ['xcut', 'bigcut0', 'woundcut_m', 'dashhit']
import os
GOLD = [(0, (40, 14, 80)), (.25, (96, 36, 180)), (.45, (150, 76, 240)), (.62, (200, 140, 255)), (.78, (255, 196, 90)), (.92, (255, 232, 170)), (1, (255, 255, 255))]
NEON = [(0, (44, 0, 110)), (.25, (110, 20, 235)), (.5, (176, 60, 255)), (.72, (214, 130, 255)), (.88, (240, 205, 255)), (1, (255, 255, 255))]   # owner: "ม่วงนีออน ขาวพอ ไม่ต้องใส่ทอง"
LOOK = os.environ.get('LOOK', 'neon'); STOPS, SUF, HALO = (GOLD, '_g', (150, 76, 240)) if LOOK == 'gold' else (NEON, '_n', (176, 60, 255))
m = json.load(open('fx/manifest.json'))
for k in KEYS:
    if k not in m: print('skip', k); continue
    d = m[k]; im = Image.open('fx/%s.png' % k).convert('RGBA'); a0 = np.asarray(im.split()[3]).astype(float) / 255
    rgb = np.asarray(im.convert('RGB')).astype(float) / 255; v = rgb.max(2); s = (v - rgb.min(2)) / np.maximum(v, 1e-6); t = v * (1 - .62 * s)
    out = np.dstack([np.interp(t, [p for p, _ in STOPS], [c[i] for _, c in STOPS]) for i in range(3)])
    al = a0 * np.clip((v - .12) / .5, 0, 1) ** .7
    res = Image.new('RGBA', im.size, (0, 0, 0, 0)); w, h = d['w'], d['h']; R = max(2, round(min(w, h) / 22))
    for i in range(d['n']):
        x, y = i % d['cols'] * w, i // d['cols'] * h; pm = np.dstack([out[y:y + h, x:x + w] * al[y:y + h, x:x + w, None], al[y:y + h, x:x + w] * 255])
        bl = np.asarray(Image.fromarray(pm.astype(np.uint8), 'RGBA').filter(ImageFilter.GaussianBlur(R))).astype(float)
        halo = bl * (.8 if LOOK == 'neon' else .55) * (1 - pm[..., 3:4] / 255); halo[..., :3] = halo[..., 3:4] * np.array(HALO) / 255      # the halo is violet whatever it comes from
        o = pm + halo; aa = np.clip(o[..., 3], 0, 255); col = np.where(aa[..., None] > 0, o[..., :3] / np.maximum(aa[..., None], 1) * 255, 0)
        res.paste(Image.fromarray(np.dstack([np.clip(col, 0, 255), aa]).astype(np.uint8), 'RGBA'), (x, y))
    res.save('fx/%s%s.png' % (k, SUF), optimize=True); e = dict(d); e['src'] = '%s light copy of %s (tools/art/fx_goldlight.py)' % (LOOK, k); e['add'] = 1; m[k + SUF] = e
json.dump(m, open('fx/manifest.json', 'w'), ensure_ascii=False, separators=(',', ':')); print('made', len(KEYS))
