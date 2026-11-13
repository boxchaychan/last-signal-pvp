#!/usr/bin/env python3
"""Violet copies of effects we already own (owner 2026-11-13 "ไปเอาที่มีอยู่มาแปลงเอา": the old rogue's cyan cuts for the dagger girl).
usage: fx_violet.py [key ...]   -> fx/<key>_v.png + a manifest entry <key>_v (same cells, anchor and fps). The originals are not touched.
Colour: hue set to violet, saturation kept (lifted a little), brightness kept, so white cores stay white and dark rims stay dark."""
import sys, json, numpy as np
from PIL import Image
KEYS = sys.argv[1:] or ['dslash%d' % i for i in range(8)] + ['dslashl%d' % i for i in range(8)] + ['dslashs%d' % i for i in range(8)] + ['xcut', 'bigcut0', 'woundcut_m', 'dashhit']
m = json.load(open('fx/manifest.json'))
for k in KEYS:
    if k not in m: print('skip', k); continue
    im = Image.open('fx/%s.png' % k).convert('RGBA'); a = im.split()[3]
    h, s, v = [np.asarray(c).astype(float) / 255 for c in im.convert('RGB').convert('HSV').split()]
    h2 = np.full_like(h, .765); s2 = np.clip(s * 1.05 + .1 * (s > .08), 0, 1) * (s > .03)
    rgb = Image.merge('HSV', [Image.fromarray((c * 255).astype(np.uint8)) for c in (h2, s2, v)]).convert('RGB')
    Image.merge('RGBA', (*rgb.split(), a)).save('fx/%s_v.png' % k, optimize=True)
    d = dict(m[k]); d['src'] = 'violet copy of %s (tools/art/fx_violet.py)' % k; m[k + '_v'] = d
json.dump(m, open('fx/manifest.json', 'w'), ensure_ascii=False, separators=(',', ':')); print('made', len(KEYS))
