# Ground textures from the owner's painted tile sheet (2026-11-12 "เอาไปทำพื้นฉาก": art/incoming/dogcat/floor/tiles_src.webp,
# 1024x1024, stone / grass / dirt patches on dark grey). Free, no jobs. Each patch is cut, shrunk (box filter) to the scene's pixel
# size and cut down to a few colours so it reads as pixel art next to the PixelLab characters.
import numpy as np
from PIL import Image
SRC = 'art/incoming/dogcat/floor/tiles_src.webp'
CROPS = {'road': (566, 30, 742, 258), 'grass': (745, 690, 985, 812), 'grass2': (568, 520, 730, 640), 'dirt': (800, 300, 990, 470),
         'f23': (26, 667, 214, 822), 'f29': (24, 838, 216, 1000), 'f12': (562, 285, 750, 482),
         'f34': (246, 846, 380, 1004), 'f25': (236, 668, 380, 815), 'f8': (26, 300, 188, 428),
         'b22': (311, 569, 382, 651), 'b16': (243, 448, 307, 542), 'b17': (317, 450, 378, 544), 'b31': (491, 837, 570, 920),
         'bush33': (911, 829, 1000, 914), 'bush36': (497, 930, 568, 1004), 'bush37': (919, 927, 1000, 1011), 'bush30': (387, 834, 494, 924)}
_S = None
def crop(n):
    global _S
    if _S is None: _S = Image.open(SRC).convert('RGB')
    return _S.crop(CROPS[n])
def px(im, k=.45, size=None, colours=28, lift=1.08, sat=1.12):
    """shrink to the pixel grid, a touch brighter and more colourful than the painting, few colours"""
    im = im.resize(size or (max(1, round(im.width * k)), max(1, round(im.height * k))), Image.BOX)
    a = np.asarray(im.convert('RGB')).astype(float); g = a.mean(2, keepdims=True); a = (g + (a - g) * sat) * lift
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return im.quantize(colours, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB')
def mirror_tile(im, W, H):
    """seamless fill: the patch, its mirror to the right, below and both"""
    a = np.asarray(im); b = np.concatenate([np.concatenate([a, a[:, ::-1]], 1), np.concatenate([a[::-1], a[::-1, ::-1]], 1)], 0)
    ry, rx = -(-H // b.shape[0]), -(-W // b.shape[1])
    return np.tile(b, (ry, rx, 1))[:H, :W].astype(float)
def patchwork(names, W, H, cw, ch, x0=0, y0=0, seed=3, k=None):
    """slab groups laid edge to edge on a cw x ch grid starting at (x0, y0) (one group per slot cell), random pick and mirror"""
    r = np.random.RandomState(seed); P = [px(crop(n), size=(cw, ch)) for n in names]
    out = np.zeros((H, W, 3)); sx = x0 % cw - cw; sy = y0 % ch - ch
    for y in range(sy, H, ch):
        for x in range(sx, W, cw):
            p = np.asarray(P[r.randint(len(P))]); p = p[:, ::-1] if r.rand() < .5 else p
            ys, xs = max(0, y), max(0, x); ye, xe = min(H, y + ch), min(W, x + cw)
            if ye > ys and xe > xs: out[ys:ye, xs:xe] = p[ys - y:ye - y, xs - x:xe - x]
    return out
def sprite(n, w, squash=1.0):
    """a single block / bush cut out of the dark sheet background, w px wide (height x squash), see-through around it"""
    im = crop(n); a = np.asarray(im).astype(int)
    bg = np.abs(a - np.array([74, 75, 72])).sum(2) < 26
    from scipy import ndimage
    lab, nn = ndimage.label(bg); edge = set(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]]) - {0}
    out = np.dstack([a, np.where(np.isin(lab, list(edge)), 0, 255)]).astype(np.uint8)
    k = w / im.width; sz = (w, max(1, round(im.height * k * squash)))
    rgb = px(Image.fromarray(out[..., :3]), size=sz); al = np.asarray(Image.fromarray(out[..., 3]).resize(sz, Image.BOX)) > 140
    return Image.fromarray(np.dstack([np.asarray(rgb), al * 255]).astype(np.uint8))
def splat(names, W, H, n=None, seed=5, k=.45):
    """grass without a visible grid: the average colour, then many patches pasted at random spots with soft round edges"""
    r = np.random.RandomState(seed); P = [np.asarray(px(crop(m), k=k, colours=64)).astype(float) for m in names]
    out = np.zeros((H, W, 3)) + np.mean([p.reshape(-1, 3).mean(0) for p in P], 0); n = n or int(W * H / 1800)
    for _ in range(n):
        p = P[r.randint(len(P))]; p = p[:, ::-1] if r.rand() < .5 else p; ph, pw = p.shape[:2]
        yy, xx = np.mgrid[0:ph, 0:pw]; d = np.hypot((yy - ph / 2) / (ph / 2), (xx - pw / 2) / (pw / 2)); al = np.clip((1 - d) * 2.2, 0, 1)[..., None]
        y, x = r.randint(-ph // 2, H - ph // 2), r.randint(-pw // 2, W - pw // 2)
        ys, xs, ye, xe = max(0, y), max(0, x), min(H, y + ph), min(W, x + pw)
        out[ys:ye, xs:xe] = out[ys:ye, xs:xe] * (1 - al[ys - y:ye - y, xs - x:xe - x]) + p[ys - y:ye - y, xs - x:xe - x] * al[ys - y:ye - y, xs - x:xe - x]
    im = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).quantize(32, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB')
    return np.asarray(im).astype(float)
