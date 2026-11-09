# Recolour an effect sheet in fx/ to one hero's tone (owner 2026-11-09: each class has its own colour; the archer green
# "ปรับโดนให้สีเขียว", the rogue black-purple). Brightness is mapped onto a ramp from dark to light, a soft glow of the
# middle colour is added behind it, and the copy gets its own fx/manifest.json entry.
#   python tools/art/fx_tint.py <src key> <dst key> <dark,mid,light,white hex ramp> [pad px=10] [glow strength=1] [gamma=1]
#   e.g. python tools/art/fx_tint.py pfx_skyarrow pfx_skyarrow_g 0b3a1a,2fae4f,8af07a,f4ffe8
import json, sys
import numpy as np
from PIL import Image, ImageFilter

src, dst, ramp = sys.argv[1], sys.argv[2], sys.argv[3]
pad = int(sys.argv[4]) if len(sys.argv) > 4 else 10
gk = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
gam = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0   # >1 pushes white cores down into the colour
RAMP = np.array([[int(h[i:i + 2], 16) for i in (0, 2, 4)] for h in ramp.split(',')], float)
MID = RAMP[len(RAMP) // 2]

def tint(c):
    a = np.array(c).astype(float); v = (a[..., :3].max(-1) / 255) ** gam * (len(RAMP) - 1)
    i = np.clip(v.astype(int), 0, len(RAMP) - 2); f = (v - i)[..., None]
    a[..., :3] = RAMP[i] * (1 - f) + RAMP[i + 1] * f
    out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    if gk <= 0: return out
    al = a[..., 3] * (np.array(c)[..., :3].max(-1) / 255)
    g = np.zeros(a.shape); g[..., :3] = MID; g[..., 3] = np.clip(al * 1.5 * gk, 0, 255)
    gi = Image.fromarray(g.astype(np.uint8)).filter(ImageFilter.GaussianBlur(6)); gi.alpha_composite(out); return gi

man = json.load(open('fx/manifest.json')); m = man[src]; im = Image.open('fx/' + src + '.png').convert('RGBA')
w, h, cols, n = m['w'], m['h'], m.get('cols') or m['n'], m['n']; W, H = w + 2 * pad, h + 2 * pad
out = Image.new('RGBA', (cols * W, -(-n // cols) * H))
for i in range(n):
    c = Image.new('RGBA', (W, H)); c.alpha_composite(im.crop(((i % cols) * w, (i // cols) * h, (i % cols + 1) * w, (i // cols + 1) * h)), (pad, pad))
    out.alpha_composite(tint(c), ((i % cols) * W, (i // cols) * H))
out.save('fx/' + dst + '.png', optimize=True)
man[dst] = dict(m, w=W, h=H, cols=cols, ax=m['ax'] + pad, ay=m['ay'] + pad, src=m.get('src', src).split(' (')[0] + f' (tinted {ramp}, tools/art/fx_tint.py)')
json.dump(man, open('fx/manifest.json', 'w'), separators=(',', ':')); print(dst, out.size)
