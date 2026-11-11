# Cut the objects out of a PixelLab picture with several props on a plain (or softly shaded) background
# (owner 2026-11-12 props set 2): background = pixels close to the border colour AND joined to the border (a magic wand that
# follows a soft gradient: each pixel is compared with the blurred background around it), then one PNG per object.
#   python3 tools/art/props_cut.py <raw.png> <out dir> <name> [--tol=34] [--min=500] [--grid=CxR]
#   --grid: split by the picture's grid cells instead of by touching pixels (leaf litter / ground patches joined some objects)
#   light-grey flat shadows drawn under objects on a light background become see-through dark shadows
import sys, os, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
def opt(n, d):
    for a in sys.argv:
        if a.startswith('--' + n + '='): return float(a.split('=', 1)[1])
    return d
src, out, name = sys.argv[1:4]; tol, mn = opt('tol', 34), opt('min', 500); os.makedirs(out, exist_ok=True)
im = Image.open(src).convert('RGB'); a = np.asarray(im).astype(float); H, W = a.shape[:2]
# background estimate: median of the border, refined by a big blur of the pixels that look like it
b = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]]); bg0 = np.median(b, 0)
near = np.abs(a - bg0).max(2) < tol * 1.6
fill = a.copy(); fill[~near] = bg0
bg = np.asarray(Image.fromarray(fill.astype(np.uint8)).filter(ImageFilter.GaussianBlur(24))).astype(float)
cand = np.abs(a - bg).max(2) < tol
lab, n = ndimage.label(cand); edge = set(np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])) - {0}
bgm = np.isin(lab, list(edge))
fg = ~bgm; fg = ndimage.binary_opening(fg, iterations=1); fg = ndimage.binary_fill_holes(fg) & ~(bgm & ~ndimage.binary_fill_holes(fg)) | (fg)
grid = next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--grid=')), None)
if grid:
    C, R = map(int, grid.split('x')); lab2 = np.zeros((H, W), int)
    for r in range(R):
        for c in range(C): lab2[r * H // R:(r + 1) * H // R, c * W // C:(c + 1) * W // C] = r * C + c + 1
    lab2[~fg] = 0
else: lab2, n2 = ndimage.label(ndimage.binary_dilation(fg, iterations=2), structure=np.ones((3, 3)))
objs = [(s, i + 1) for i, s in enumerate(ndimage.find_objects(lab2)) if s is not None and ((lab2[s] == i + 1) & (rgba[s][..., 3] > 200 if False else True)).sum() >= mn]
objs.sort(key=lambda t: ((t[0][0].start + t[0][0].stop) // 2 // (H // 4), t[0][1].start))
rgba = np.dstack([a, np.where(fg, 255, 0)]).astype(np.uint8)
if bg0.mean() > 140:   # flat light-grey shadow areas -> dark see-through shadow
    V = a.mean(2); low = (a.max(2) - a.min(2)) < 16
    m1 = ndimage.uniform_filter(low.astype(float), 9) > .97; mu = ndimage.uniform_filter(V, 9); sd = np.sqrt(np.maximum(0, ndimage.uniform_filter(V * V, 9) - mu * mu))
    shd = fg & low & m1 & (sd < 9) & (V > 110)
    rgba[shd] = [12, 18, 8, 90]
k = 0
for s, i in objs:
    m = (lab2[s] == i) & fg[s]; c = rgba[s].copy(); c[..., 3] = np.where(m, c[..., 3], 0)
    e = m & ~ndimage.binary_erosion(m)                                   # soften the background colour left on the rim
    c[e, :3] = (c[e, :3].astype(float) * .7).astype(np.uint8)
    t = Image.fromarray(c); t = t.crop(t.getbbox()); t.save(os.path.join(out, '%s_%d.png' % (name, k))); k += 1
print(name, k, 'objects')
