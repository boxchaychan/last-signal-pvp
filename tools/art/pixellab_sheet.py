# PixelLab character download (unzipped) -> ONE animation sheet for pack.html's LANIM (rows idle / walk / attack / skill, wrapped
# into a fixed number of columns so the picture stays phone-friendly).
# Every PixelLab animation comes on its own canvas, but each one's frame_000 is the same standing reference, so the rows are lined
# up by the feet in their own frame_000 (lowest opaque row, middle of the pixels near it). Frames keep their drawn offsets inside a
# row (jumps, steps). Owner 2026-11-08: Wukong made in PixelLab from our own turnaround (front/side/back imported, nothing redrawn),
# moves made with PixMiniMax (text), which beat the skeleton mode on the same move.
#   python3 -I tools/art/pixellab_sheet.py <unzipped dir> <out.png> <row>=<animation folder>:<first>-<last> ... [--cols=13] [--dir=east]
# Prints the layout JSON (rows {r,n}, cols, nr, cw, ch, fx, fy, h0) and writes it next to the picture.
import sys, json, glob, os
import numpy as np
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
opts = dict(a[2:].split('=', 1) for a in sys.argv[3:] if a.startswith('--'))
COLS, DIR = int(opts.get('cols', 13)), opts.get('dir', 'east')
specs = []
for a in sys.argv[3:]:
    if a.startswith('--'): continue
    name, rest = a.split('=', 1); folder, rng = rest.rsplit(':', 1); f0, f1 = map(int, rng.split('-'))
    specs.append((name, folder, f0, f1))

def frames_of(folder):
    fs = sorted(glob.glob(os.path.join(src, '*', 'animations', folder, DIR, 'frame_*.png')))
    if not fs: raise SystemExit('no frames for ' + folder)
    return [Image.open(f).convert('RGBA') for f in fs]

def feet(im):
    al = np.array(im)[..., 3] > 40; ys = np.where(al.any(1))[0]; y1 = ys[-1]
    xs = np.where(al[max(0, y1 - 6):y1 + 1].any(0))[0]; return (xs[0] + xs[-1]) / 2, y1, ys[0]

rows = []
for name, folder, f0, f1 in specs:
    fr = frames_of(folder); ref = fr[0]; fx, fy, top = feet(ref)
    rows.append((name, fr[f0:f1 + 1], fx, fy, fy - top))
h0 = int(rows[0][4])
# one cell big enough for every frame once all rows share the feet point
L = max(r[2] for r in rows); T = max(r[3] for r in rows)
Rr = max(r[1][0].width - r[2] for r in rows); B = max(r[1][0].height - r[3] for r in rows)
cw, ch = int(np.ceil(L + Rr)), int(np.ceil(T + B)); FX, FY = int(round(L)), int(round(T))
nr = sum((len(r[1]) + COLS - 1) // COLS for r in rows)
sheet = Image.new('RGBA', (COLS * cw, nr * ch), (0, 0, 0, 0)); meta = {}; r0 = 0
for name, fr, fx, fy, _ in rows:
    for i, im in enumerate(fr):
        sheet.alpha_composite(im, ((i % COLS) * cw + int(round(FX - fx)), (r0 + i // COLS) * ch + int(round(FY - fy))))
    meta[name] = dict(r=r0, n=len(fr)); r0 += (len(fr) + COLS - 1) // COLS
sheet.save(out, optimize=True)
info = dict(rows=meta, cols=COLS, nr=nr, cw=cw, ch=ch, fx=FX, fy=FY, h0=h0)
json.dump(info, open(os.path.splitext(out)[0] + '.json', 'w'))
print(json.dumps(info))
