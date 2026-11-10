# Clean the leftovers of a white-background cut out of a prop picture (owner 2026-11-09 "ตัดก็ตัดไม่หมด": trees showed white
# dots round their outline and white gaps between the branches):
#  1. pale pockets enclosed by the figure (the old white background seen between branches) become see-through
#  2. pale pixels within 2 px of the edge (a cream line just inside the dark outline) take the colour of the leaves next to
#     them
# Only pale, low-saturation pixels are touched, so painted highlights (yellow-green, gold) stay.
#   python tools/art/prop_clean.py [--veg] <png> [<png> ...]      (in place; prints what changed)
# --veg (trees and plants): light tan / yellow-brown dots on the rim count as leftovers too (leaves are green there)
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

VEG = '--veg' in sys.argv
for f in [x for x in sys.argv[1:] if not x.startswith('--')]:
    a = np.array(Image.open(f).convert('RGBA')).astype(int); al = a[..., 3] > 0
    rgb = a[..., :3]; L = .3 * rgb[..., 0] + .59 * rgb[..., 1] + .11 * rgb[..., 2]; sat = rgb.max(-1) - rgb.min(-1)
    pale = al & (L > 178) & (sat < 75)
    # 1. enclosed pale pockets (not the outer background: that is already transparent)
    lab, n = ndimage.label(pale); pockets = 0
    if n:
        sz = ndimage.sum(pale, lab, range(1, n + 1))
        for i, s in enumerate(sz):
            if s >= 12:
                m = lab == i + 1; ring = ndimage.binary_dilation(m, iterations=2) & ~m
                if (L[ring & al] < 90).mean() > .25: a[m, 3] = 0; pockets += 1   # surrounded by outline: background seen through
    al = a[..., 3] > 0
    # 2. the pale line inside the outline
    near = al & ndimage.binary_dilation(~al, iterations=3)
    rim = near & pale & al
    if VEG: rim |= near & al & (L > 125) & (rgb[..., 0] >= rgb[..., 1] * .9) & (rgb[..., 0] > rgb[..., 2] + 20)
    good = al & ~pale & ~rim & (L > 70)
    fixed = 0
    if rim.any() and good.any():
        idx = ndimage.distance_transform_edt(~good, return_distances=False, return_indices=True)
        ys, xs = np.nonzero(rim); sy, sx = idx[0][ys, xs], idx[1][ys, xs]
        a[ys, xs, :3] = a[sy, sx, :3]; fixed = len(ys)
    if VEG:   # the outermost line: light olive pixels there read as pale dots on grass, make it the dark outline colour
        # GPT trees have "thin dark line, 2 px dull olive (the old white background blended in), dark line" at the edge
        edge = al & ndimage.binary_dilation(~al, iterations=4); Le = .3 * a[..., 0] + .59 * a[..., 1] + .11 * a[..., 2]; Se = a[..., :3].max(-1) - a[..., :3].min(-1)
        m = edge & (Le > 95) & (Se < 115); a[m, :3] = (16, 30, 10); fixed += int(m.sum())
    Image.fromarray(a.astype(np.uint8)).save(f, optimize=True)
    print(f, 'pockets', pockets, 'rim px', fixed)
