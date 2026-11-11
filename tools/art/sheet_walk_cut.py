# A GPT / Meta AI sprite sheet (grid on white) -> clean frames on one ground line, one scale for every row (owner 2026-11-11
# "ประกอบดู"). Removes the white background (joined to the border, and closed white pockets between arm and body), the tan dust
# puffs at the feet, and lifts / scales every row so the figures are the same height as row 1.
#   python3 tools/art/sheet_walk_cut.py <sheet> <out dir> <cols> <rows>
import sys, os, numpy as np
from PIL import Image
from scipy import ndimage
src, od, C, R = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]); os.makedirs(od, exist_ok=True)
im = Image.open(src).convert('RGB'); W, H = im.size; cw, ch = W / C, H / R
fr = []
for r in range(R):
    for c in range(C):
        a = np.asarray(im.crop((round(c * cw), round(r * ch), round((c + 1) * cw), round((r + 1) * ch))).convert('RGBA')).astype(int).copy(); hh = a.shape[0]
        light = a[..., :3].min(2) > 230; lab, n = ndimage.label(light)
        bd = set(np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])) - {0}; bg = np.isin(lab, list(bd))
        sz = ndimage.sum(light, lab, range(1, n + 1))
        pocket = np.isin(lab, [i + 1 for i, s in enumerate(sz) if s > 25]) & (a[..., :3].min(2) > 242)   # white seen between arm and body
        a[bg | pocket] = 0
        R_, G_, B_ = a[..., 0], a[..., 1], a[..., 2]; yy = np.arange(hh)[:, None]
        dust = (a[..., 3] > 0) & (yy > hh * .72) & (((R_ > 90) & (R_ - B_ > 35) & (G_ - B_ > 12) & (R_ - G_ < 60)) |
                                                    ((R_ > 95) & (G_ > 70) & (B_ > 40) & (R_ - G_ < 55) & (R_ - B_ < 110)))
        a[dust] = 0
        edge = ndimage.binary_dilation(a[..., 3] == 0, iterations=1) & (a[..., 3] > 0) & (a[..., :3].min(2) > 215); a[edge] = 0
        m = a[..., 3] > 0; l2, n2 = ndimage.label(m, structure=np.ones((3, 3))); s2 = ndimage.sum(m, l2, range(1, n2 + 1))
        big = int(np.argmax(s2)) + 1
        for i, s in enumerate(s2):
            if i + 1 != big and s < 3000: a[l2 == i + 1] = 0   # only the figure (dust outlines, specks go)
        fr.append(Image.fromarray(a.astype(np.uint8)))
def meas(f):
    al = np.asarray(f)[..., 3] > 0; ys, xs = np.nonzero(al); return ys.max() - ys.min(), ys.max()
h1 = np.mean([meas(f)[0] for f in fr[:C]])
out = []
for r in range(R):
    hr = np.mean([meas(f)[0] for f in fr[r * C:(r + 1) * C]]); k = h1 / hr
    for f in fr[r * C:(r + 1) * C]:
        g = f.resize((round(f.width * k), round(f.height * k)), Image.LANCZOS) if abs(k - 1) > .005 else f
        _, fy = meas(g); cv = Image.new('RGBA', (round(cw * 1.2), round(ch * 1.12))); cv.alpha_composite(g, (round((cv.width - g.width) / 2), cv.height - 20 - fy)); out.append(cv)
for i, f in enumerate(out): f.save(os.path.join(od, 'f%02d.png' % i))
print('frames', len(out), 'heights', [int(meas(f)[0]) for f in out])
