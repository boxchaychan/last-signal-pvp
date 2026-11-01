"""Spider-queen Flow clips -> feet-anchored frame strips (AX/AY/H0 below are measured from frame 0 by `analyse`; re-measure for new clips).
usage: sqproc.py analyse | build
All four clips start from the same input picture, so frame 0 of each clip gives a shared scale and anchor."""
import sys, json, subprocess
import numpy as np
from PIL import Image
from scipy import ndimage

import os
D = os.environ.get('SQ_DIR', 'vid/sq/')  # folder with v1.mp4..v4.mp4 (cast, walk, attack, idle)
OUT = os.environ.get('ART_OUT', 'art/')
W, H = 1280, 720


def load(i):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', D + 'v%d.mp4' % i, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)


def key(fr):
    f = fr.astype(np.int16)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    mx = np.maximum(r, b)
    d = g - mx
    a = np.clip((150 - d) / 90.0, 0, 1)
    a[(g > 150) & (d > 90)] = 0
    g2 = np.where(d > 0, mx, g)  # despill: no pixel keeps more green than its red/blue
    rgb = np.stack([r, g2, b], -1).clip(0, 255).astype(np.uint8)
    al = (a * 255).astype(np.uint8)
    m = al > 40
    lab, n = ndimage.label(m)
    if n > 1:
        sizes = ndimage.sum(m, lab, range(1, n + 1))
        big = sizes.max()
        keep = np.zeros(n + 1, bool)
        keep[1:] = sizes >= max(400, big * .004)
        al[~keep[lab]] = 0
    rgb[al == 0] = 0
    return np.dstack([rgb, al])


def bbox(al, th=100):
    ys, xs = np.where(al > th)
    return xs.min(), ys.min(), xs.max(), ys.max()


def body_x(al):
    # x centre of the opaque mass in the upper 60% (body + queen), ignores leg tips
    ys, xs = np.where(al > 128)
    top, bot = ys.min(), ys.max()
    sel = ys < top + (bot - top) * .6
    return xs[sel].mean()


def loop_pair(small, lo, hi, a=0, b=None):
    b = len(small) if b is None else b
    best = (1e9, 0, 0)
    for i in range(a, b):
        for j in range(i + lo, min(b, i + hi + 1)):
            d = np.abs(small[i] - small[j]).mean()
            if d < best[0]:
                best = (d, i, j)
    return best


def thumbs(frames):
    out = []
    for fr in frames:
        im = Image.fromarray(fr).resize((160, 90), Image.BILINEAR)
        out.append(np.asarray(im, np.float32))
    return np.array(out)


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'analyse':
        res = {}
        for i in (1, 2, 3, 4):
            v = load(i)
            k0 = key(v[0])
            x0, y0, x1, y1 = bbox(k0[..., 3])
            res[i] = dict(n=len(v), bbox=[int(x0), int(y0), int(x1), int(y1)], bx=float(body_x(k0[..., 3])))
            if i in (2, 4):
                th = thumbs(v)
                lo, hi = (18, 60) if i == 2 else (40, 140)
                res[i]['loop'] = [float(x) for x in loop_pair(th, lo, hi, 4, len(v) - 4)]
                # also report the best few periods
            print(i, res[i], flush=True)
        json.dump(res, open(D + 'an.json', 'w'))


def build(clip, idx, name, drift=None, CH=260, pad=6):
    v = load(clip)
    AX, AY, H0 = 640.5, 643.0, 527.0
    s = CH / H0
    ks = [key(v[i]) for i in idx]
    dx = [0.0] * len(ks)
    if drift:  # linear drift removal so the loop closes: body x at the two loop ends
        i0, i1 = drift
        b0, b1 = body_x(key(v[i0])[..., 3]), body_x(key(v[i1])[..., 3])
        dx = [(b1 - b0) * (i - i0) / (i1 - i0) for i in idx]
    L = T = R = B = 0
    for k, d in zip(ks, dx):
        x0, y0, x1, y1 = bbox(k[..., 3], 8)
        L = max(L, AX + d - x0); R = max(R, x1 - AX - d); T = max(T, AY - y0); B = max(B, y1 - AY)
    L, R, T, B = [int(np.ceil(q)) + pad for q in (L, R, T, B)]
    fw0, fh0 = L + R, T + B
    fw, fh = round(fw0 * s), round(fh0 * s)
    strip = Image.new('RGBA', (fw * len(ks), fh), (0, 0, 0, 0))
    for n, (k, d) in enumerate(zip(ks, dx)):
        ox = int(round(AX + d - L)); oy = int(round(AY - T))
        cv = np.zeros((fh0, fw0, 4), np.uint8)
        sx0, sy0 = max(0, ox), max(0, oy); sx1, sy1 = min(W, ox + fw0), min(H, oy + fh0)
        cv[sy0 - oy:sy1 - oy, sx0 - ox:sx1 - ox] = k[sy0:sy1, sx0:sx1]
        im = Image.fromarray(cv, 'RGBA').convert('RGBa').resize((fw, fh), Image.LANCZOS).convert('RGBA')
        strip.paste(im, (n * fw, 0))
    q = strip.quantize(256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
    q.save(OUT + name, optimize=True)
    bg = Image.new('RGBA', strip.size, (70, 90, 70, 255)); bg.alpha_composite(strip)
    bg.convert('RGB').save(D + name.replace('.png', '_prev.jpg'), quality=80)
    meta = dict(n=len(ks), fw=fw, fh=fh, fax=round(L * s, 1), fay=round(T * s, 1), ch=CH)
    print(name, meta, flush=True)
    return meta


if __name__ == '__main__' and sys.argv[1] == 'build':
    an = json.load(open(D + 'an.json'))
    w0, w1 = int(an['2']['loop'][1]), int(an['2']['loop'][2])
    i0, i1 = int(an['4']['loop'][1]), int(an['4']['loop'][2])
    M = {}
    walk_idx = [round(w0 + (w1 - w0) * k / 13) for k in range(13)]
    M['walk'] = build(2, walk_idx, 'z_queen_walk.png', drift=(w0, w1))
    idle_idx = [round(i0 + (i1 - i0) * k / 16) for k in range(16)]
    M['idle'] = build(4, idle_idx, 'z_queen_idle.png', drift=(i0, i1))
    atk_idx = [round(14 + (72 - 14) * k / 11) for k in range(12)]
    M['atk'] = build(3, atk_idx, 'z_queen_attack.png')
    cast_idx = [round(24 + (150 - 24) * k / 15) for k in range(16)]
    M['cast'] = build(1, cast_idx, 'z_queen_cast.png')
    M['_loops'] = dict(walk=[w0, w1], idle=[i0, i1])
    json.dump(M, open(D + 'meta.json', 'w'))
