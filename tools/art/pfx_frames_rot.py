# ParticleFX "PNG frames" export (one PNG per frame) -> fx/<key><deg>.png turned copies + manifest (HD, soft alpha kept).
#   python tools/art/pfx_frames_rot.py <frames dir> <key> <size> [step=45] [fps=30] [flat=1]
# The effect is drawn facing right; each copy is turned on the full picture, then cropped to the ink of all its frames and
# scaled so the effect's long side is <size> game px. flat < 1 squashes the vertical (a top-down ground look).
import glob, json, sys, math
import numpy as np
from PIL import Image

d, key, size = sys.argv[1], sys.argv[2], int(sys.argv[3])
step = int(sys.argv[4]) if len(sys.argv) > 4 else 45
fps = int(sys.argv[5]) if len(sys.argv) > 5 else 30
flat = float(sys.argv[6]) if len(sys.argv) > 6 else 1
fr = [Image.open(f).convert('RGBA') for f in sorted(glob.glob(d + '/*.png'))]
while len(fr) > 1 and (np.array(fr[-1])[..., 3] > 8).sum() < 30: fr.pop()
A = np.stack([np.array(f)[..., 3] for f in fr]).max(0) > 8; ys, xs = np.nonzero(A)
s = size / max(xs.max() - xs.min() + 1, ys.max() - ys.min() + 1)
cx0, cy0 = fr[0].width / 2, fr[0].height / 2     # turn round the frame centre (the hero's swing centre)
man = json.load(open('fx/manifest.json'))
for deg in range(0, 360, step):
    tf = [f.rotate(-deg, resample=Image.BICUBIC, expand=True) for f in fr]
    if flat != 1: tf = [f.resize((f.width, max(1, round(f.height * flat))), Image.BICUBIC) for f in tf]
    W, H = tf[0].size
    M = np.stack([np.array(f)[..., 3] for f in tf]).max(0) > 8; ys, xs = np.nonzero(M)
    x0, x1, y0, y1 = max(0, xs.min() - 2), min(W, xs.max() + 3), max(0, ys.min() - 2), min(H, ys.max() + 3)
    w, h = max(1, round((x1 - x0) * s)), max(1, round((y1 - y0) * s))
    small = [f.crop((x0, y0, x1, y1)).resize((w, h), Image.LANCZOS) for f in tf]
    n = len(small); C = min(12, n); R = (n + C - 1) // C
    sheet = Image.new('RGBA', (w * C, h * R), (0, 0, 0, 0))
    for i, f in enumerate(small): sheet.paste(f, ((i % C) * w, (i // C) * h))
    name = f'{key}{deg}'; sheet.save(f'fx/{name}.png', optimize=True)
    # anchor = the frame centre (where the hero stands), mapped through the turn, crop and scale
    ax, ay = (W / 2 - x0) * s, (H / 2 - y0) * s
    man[name] = {'w': w, 'h': h, 'n': n, 'cols': C, 'fps': fps, 'ax': int(round(ax)), 'ay': int(round(ay)), 'src': f'ParticleFX Studio frames {d.split("/")[-1]} turned {deg}'}
    print(name, n, 'frames', w, 'x', h)
json.dump(man, open('fx/manifest.json', 'w'), separators=(',', ':'))
