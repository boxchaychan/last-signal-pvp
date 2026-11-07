# Cut the plain white background of a generated picture -> see-through PNG, without eating white or silver parts of the figure
# (owner 2026-11-07, Artemis: silver hair and a white dress on a white background, so a colour threshold alone would punch holes).
#   python3 tools/art/white_cut.py <in.png> <out.png>
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
pure = (mn >= 244) & (mx - mn <= 8) & ~bg
lab2, n2 = ndimage.label(pure)
if n2:
    sz = ndimage.sum(np.ones(pure.shape), lab2, range(1, n2 + 1)); bg |= np.isin(lab2, 1 + np.where(sz >= 150)[0])
# soften nothing: hard alpha, and a 1 px trim of the light fringe left round the outside
fr = ndimage.binary_dilation(bg) & ~bg & (mn >= 215) & (mx - mn <= 20)
a[..., 3] = np.where(bg | fr, 0, 255)
Image.fromarray(a).save(sys.argv[2], optimize=True)
print('background', int(bg.sum()), 'fringe', int(fr.sum()))
