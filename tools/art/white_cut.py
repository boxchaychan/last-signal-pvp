# Cut the plain white background of a generated picture -> see-through PNG, without eating white or silver parts of the figure
# (owner 2026-11-07, Artemis: silver hair and a white dress on a white background, so a colour threshold alone would punch holes).
#   python3 tools/art/white_cut.py <in.png> <out.png> [--edge-only] [--no-ring]
#   --no-ring   skips the dark-ring rule below, for gold / orange characters (Apollo 2026-11-07): the rule takes the min
#               channel as darkness, so saturated gold counts as dark outline and eye highlights, skirt whites and the
#               cape lining were cut. With it the gaps in Apollo's lyre stay white (they read as a glowing lyre).
#   --edge-only skips step 2, for very white characters (Artemis's back view: her hair has pure-white patches over 100 px);
#               white and light grey joined to the outside in the lowest 16% of each figure (the gap between the legs behind
#               the ground shadow) still go, and 1 px wide tall lines left by the generator's cell cutting
# 1. white joined to the picture border (flood fill over near-white, untinted pixels) goes;
# 2. inside the figure only big patches of PURE untinted white go (background seen between legs, arm and bow);
#    tinted whites and light greys (hair, cloth, fur) stay.
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

im = Image.open(sys.argv[1]).convert('RGBA'); a = np.array(im); rgb = a[..., :3].astype(int)
mx, mn = rgb.max(2), rgb.min(2)
nearw = (mn >= 232) & (mx - mn <= 14) | (a[..., 3] < 128)
lab, n = ndimage.label(nearw)
edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
bg = np.isin(lab, list(edge))
pure = (mn >= 244) & (mx - mn <= 8) & ~bg & ('--edge-only' not in sys.argv)
lab2, n2 = ndimage.label(pure)
if n2:
    sz = ndimage.sum(np.ones(pure.shape), lab2, range(1, n2 + 1)); bg |= np.isin(lab2, 1 + np.where(sz >= 150)[0])
if '--edge-only' in sys.argv:
    # the gap between the legs is shut off by the grey ground shadow: in the lowest 16% of each figure, light grey and white
    # that join the outside background go too (the skirt and hair higher up stay)
    figs, nf = ndimage.label(~bg); band = np.zeros(bg.shape, bool)
    for o in ndimage.find_objects(figs):
        h = o[0].stop - o[0].start
        if h >= 40: band[o[0].start + int(h * .84):o[0].stop, o[1]] = True
    pas = band & (mn >= 185) & (mx - mn <= 16) & ~bg
    l3, n3 = ndimage.label(pas | bg)
    keep = set(np.unique(l3[bg])) - {0}
    bg |= pas & np.isin(l3, list(keep))
    # background seen inside the bow / between arm and body: a pure-white patch walled by dark outline pixels. White hair
    # highlights sit inside lighter hair strands (almost no dark pixels round them), so they stay (owner 2026-11-07 "แก้ด่วน")
    pw = (mn >= 246) & (mx - mn <= 8) & ~bg; l4, n4 = ndimage.label(pw)
    for i, o in enumerate([] if '--no-ring' in sys.argv else ndimage.find_objects(l4)):
        m = np.zeros(bg.shape, bool); m[o] = l4[o] == i + 1
        if m.sum() < 40: continue
        ring = ndimage.binary_dilation(m, iterations=2) & ~m & ~bg
        if ring.any() and (mn[ring] < 120).mean() >= .15: bg |= m
    # 1 px wide tall lines left at the cell edges by the generator's cutting
    op = ~bg
    for x in range(1, op.shape[1] - 1):
        col = op[:, x] & ~op[:, x - 1] & ~op[:, x + 1]
        if col.sum() >= 40: bg[:, x] |= col
# soften nothing: hard alpha, and a 1 px trim of the light fringe left round the outside
fr = ndimage.binary_dilation(bg) & ~bg & (mn >= 215) & (mx - mn <= 20)
a[..., 3] = np.where(bg | fr, 0, 255)
Image.fromarray(a).save(sys.argv[2], optimize=True)
print('background', int(bg.sum()), 'fringe', int(fr.sum()))
