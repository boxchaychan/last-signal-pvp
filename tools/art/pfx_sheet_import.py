# ParticleFX Studio "PNG spritesheet" export (a grid of equal frames on transparency) -> fx/<key>.png + fx/manifest.json.
# Owner 2026-11-09: effects from particlefx.studio (library downloads and the agent's builds; licence allows commercial use).
#   python tools/art/pfx_sheet_import.py <sheet.png> <key> <cols>x<rows> [size=widest frame in game px] [fps=30] [anchor=c|g] [n=frames]
# Frames are cropped to the ink of all frames together, scaled so the widest is <size> px (soft, the effects are HD glows),
# empty frames at the end dropped, laid out 12 per row so the sheet stays under 4096 px for phones.
import json, sys
import numpy as np
from PIL import Image

src, key, grid = sys.argv[1], sys.argv[2], sys.argv[3]
size = int(sys.argv[4]) if len(sys.argv) > 4 else 0
fps = int(sys.argv[5]) if len(sys.argv) > 5 else 30
anchor = sys.argv[6] if len(sys.argv) > 6 else 'c'
nmax = int(sys.argv[7]) if len(sys.argv) > 7 else 0
cols, rows = (int(v) for v in grid.split('x'))
import os, glob
if os.path.isdir(src):   # a folder of PNG frames (ParticleFX "PNG frames" export); the grid argument is ignored
    fr = [np.array(Image.open(f).convert('RGBA')) for f in sorted(glob.glob(os.path.join(src, '*.png')))]
else:
    im = Image.open(src).convert('RGBA'); W, H = im.size; cw, ch = W / cols, H / rows
    fr = [np.array(im.crop((round(c * cw), round(r * ch), round((c + 1) * cw), round((r + 1) * ch)))) for r in range(rows) for c in range(cols)]
h0, w0 = min(f.shape[0] for f in fr), min(f.shape[1] for f in fr); fr = [f[:h0, :w0] for f in fr]
while len(fr) > 1 and (fr[-1][..., 3] > 8).sum() < 20: fr.pop()
if nmax: fr = fr[:nmax]
A = np.stack([f[..., 3] for f in fr]).astype(float); m = A.max(0) > 8; ys, xs = np.nonzero(m)
y0, y1, x0, x1 = max(0, ys.min() - 2), min(h0, ys.max() + 3), max(0, xs.min() - 2), min(w0, xs.max() + 3)
s = size / (x1 - x0) if size else 1
w, h = max(1, round((x1 - x0) * s)), max(1, round((y1 - y0) * s))
small = [Image.fromarray(f[y0:y1, x0:x1]).resize((w, h), Image.LANCZOS) for f in fr]
n = len(small); C = min(12, n); R = (n + C - 1) // C
sheet = Image.new('RGBA', (w * C, h * R), (0, 0, 0, 0))
for i, f in enumerate(small): sheet.paste(f, ((i % C) * w, (i // C) * h))
S = np.stack([np.array(f)[..., 3] for f in small]).astype(float).sum(0); yy, xx = np.mgrid[0:h, 0:w]; tw = S.sum()
ax = (S * xx).sum() / tw
if anchor == 'b': ax, ay = w / 2, h / 2   # centre of the box (a ring of arcs turned round the hero)
elif anchor == 'c': ay = (S * yy).sum() / tw
else: r_ = S.sum(1); ay = int(np.nonzero(r_ > r_.max() * .05)[0].max())
sheet.save(f'fx/{key}.png', optimize=True)
man = json.load(open('fx/manifest.json'))
man[key] = {'w': w, 'h': h, 'n': n, 'cols': C, 'fps': fps, 'ax': int(round(ax)), 'ay': int(round(ay)), 'src': f'ParticleFX Studio {src.split("/")[-1]}'}
json.dump(man, open('fx/manifest.json', 'w'), separators=(',', ':'))
print(key, n, 'frames', w, 'x', h, 'sheet', sheet.size, 'anchor', man[key]['ax'], man[key]['ay'])
