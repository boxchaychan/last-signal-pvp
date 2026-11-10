# usage: python3 tools/video/vid2px.py <folder of f001.png.. from ffmpeg> <out dir> <figure height px> <palette png> [frame step]
# (owner 2026-11-10: Meta AI videos on flat green, locked camera, e.g. the Berserker slash combo)
# video on flat green -> pixel frames at game size (locked camera: one shared scale + crop for every frame)
import sys, glob, numpy as np
from PIL import Image
src, out, H0, pal_png = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
step = int(sys.argv[5]) if len(sys.argv) > 5 else 2
fs = sorted(glob.glob(src + '/f*.png'))[::step]
def key(im):
    f = np.asarray(im.convert('RGB')).astype(np.int16); r, g, b = f[..., 0], f[..., 1], f[..., 2]; mx = np.maximum(r, b); d = g - mx
    a = np.clip((120 - d) / 70.0, 0, 1); a[(g > 140) & (d > 80)] = 0
    g2 = np.where(d > 0, mx, g); return np.dstack([r, g2, b, (a * 255).astype(np.int16)]).clip(0, 255).astype(np.uint8)
K = [key(Image.open(f)) for f in fs]
# shared box over all frames; the scale comes from frame 0's figure height
al = np.stack([k[..., 3] > 128 for k in K]); any_ = al.any(0); ys, xs = np.nonzero(any_)
y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
r0 = np.nonzero(al[0].any(1))[0]; h0 = r0.max() - r0.min() + 1; s = H0 / h0
print('frames', len(K), 'h0', h0, 'scale', round(s, 3), 'box', x0, y0, x1, y1)
pal = Image.open(pal_png).convert('RGBA'); pa = np.asarray(pal).reshape(-1, 4); pa = pa[pa[:, 3] > 200][:, :3]
P = np.unique(pa, axis=0).astype(float)
W2, H2 = int((x1 - x0) * s + .5), int((y1 - y0) * s + .5)
res = []
for k in K:
    im = Image.fromarray(k[y0:y1, x0:x1]); im = im.resize((W2, H2), Image.BOX); a = np.asarray(im).copy()
    m = a[..., 3] > 110; rgb = a[..., :3].astype(float)
    d = ((rgb[:, :, None, :] - P[None, None]) ** 2).sum(-1); idx = d.argmin(-1)
    o = np.zeros_like(a); o[m, :3] = P[idx[m]].astype(np.uint8); o[m, 3] = 255; res.append(Image.fromarray(o))
import os; os.makedirs(out, exist_ok=True)
for i, r in enumerate(res): r.save(out + '/p%03d.png' % i)
bg = (96, 140, 70, 255)
g = [Image.alpha_composite(Image.new('RGBA', r.size, bg), r).resize((r.width * 3, r.height * 3), Image.NEAREST).convert('RGB') for r in res]
g[0].save(out + '/anim.gif', save_all=True, append_images=g[1:], duration=int(1000 / 24 * step), loop=0)
print('size', W2, H2)
