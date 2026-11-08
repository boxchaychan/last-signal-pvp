# GPT turnaround (front / side / back on white) -> three pixel-art views on one canvas size, ready for PixelLab create_character v3
# (south = front as the reference, east = side, north = back as direction_images). Owner 2026-11-08: dagger rogue at 128.
#   python3 tools/art/turn128.py <cut.png> <out dir> [canvas=128] [colours=32]
#   <cut.png> = the turnaround with its white background already cut: tools/art/white_cut.py <in> <cut.png> --edge-only --no-ring
# All three views share ONE scale (the tallest figure fills canvas-10 px) and one palette; feet sit 4 px above the bottom edge,
# each figure centred on its own width. A 1 px dark outline goes round the outside. Writes south.png east.png north.png + preview.png.
import sys, os
import numpy as np
from PIL import Image
from scipy import ndimage

src, out = sys.argv[1], sys.argv[2]
C = int(sys.argv[3]) if len(sys.argv) > 3 else 128
NC = int(sys.argv[4]) if len(sys.argv) > 4 else 32
os.makedirs(out, exist_ok=True)
im = Image.open(src).convert('RGBA'); a = np.array(im)
solid = a[..., 3] > 128
# split into figures by empty columns
cols = solid.any(0); runs = []; x = 0
while x < len(cols):
    if cols[x]:
        s = x
        while x < len(cols) and cols[x]: x += 1
        runs.append((s, x))
    x += 1
runs = [r for r in runs if r[1] - r[0] > 20]
# join runs closer than 12 px (a dagger tip or headband tail split off its figure)
merged = []
for r in runs:
    if merged and r[0] - merged[-1][1] < 12: merged[-1] = (merged[-1][0], r[1])
    else: merged.append(r)
assert len(merged) == 3, f'expected 3 figures, found {len(merged)}: {merged}'
figs = []
for x0, x1 in merged:
    sub = im.crop((x0, 0, x1, im.height)); figs.append(sub.crop(sub.getbbox()))
k = (C - 10) / max(f.height for f in figs)

def shrink(f):
    w, h = max(1, round(f.width * k)), max(1, round(f.height * k))
    p = np.array(f).astype(float) / 255; p[..., :3] *= p[..., 3:4]
    q = np.array(Image.fromarray((p * 255).astype(np.uint8)).resize((w, h), Image.BOX)).astype(float)
    al = q[..., 3:4] / 255
    rgb = np.where(al > 0, q[..., :3] / np.maximum(al, 1e-6), 0).clip(0, 255)
    return rgb.astype(np.uint8), al[..., 0] > .5

small = [shrink(f) for f in figs]
# one shared palette from all opaque pixels
allpx = np.concatenate([r[m] for r, m in small])[None]
pal = Image.fromarray(allpx).quantize(NC, method=Image.Quantize.MEDIANCUT)
views = []
for (rgb, m), name in zip(small, ['south', 'east', 'north']):
    q = np.array(Image.fromarray(rgb).quantize(palette=pal, dither=Image.Dither.NONE).convert('RGB'))
    can = np.zeros((C, C, 4), np.uint8); h, w = m.shape
    ox, oy = (C - w) // 2, C - 4 - h
    can[oy:oy + h, ox:ox + w, :3] = q; can[oy:oy + h, ox:ox + w, 3] = m * 255
    mm = can[..., 3] > 0; ring = ndimage.binary_dilation(mm) & ~mm
    can[ring] = (30, 20, 24, 255)
    v = Image.fromarray(can); v.save(os.path.join(out, name + '.png')); views.append(v)
    print(name, 'figure', w, 'x', h)
pv = Image.new('RGBA', (C * 3 * 3 + 40, C * 3 + 20), (126, 170, 92, 255))
for i, v in enumerate(views): pv.alpha_composite(v.resize((C * 3, C * 3), Image.NEAREST), (10 + i * (C * 3 + 10), 10))
pv.save(os.path.join(out, 'preview.png')); print('scale', round(k, 4), 'colours', NC)
