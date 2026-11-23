#!/usr/bin/env python3
"""clash.html units: cut the owner's ChatGPT sheet (art/incoming/clash/gpt_style12.png, 12 sprites on flat magenta, 4 x 3)
into TRUE pixel sprites (one art pixel per GPT "pixel"), free, no PixelLab.
GPT's pixels are not square in this copy (the 1536 x 1024 picture came back as 1448 x 1086), so the cell is CX x CY screen px;
each sprite gets its own grid phase (the one with the least colour spread inside cells), each cell takes its most common colour.
Writes art/clash/orig/<key>.png (untouched cut), art/clash/units/<key>.png (pixel_punch colour recipe), art/clash/units.json.
Run: python3 tools/art/clash_cut.py"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
from scipy import ndimage as nd
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, 'art/incoming/clash/gpt_style12.png'); OUT = os.path.join(ROOT, 'art/clash')
CX, CY = 7.54, 8.48
KEYS = ['m_saw', 'm_shield', 'a_wolf', 'a_rhino', 'e_psychic', 'e_jelly', 'h_spear', 'h_archer', 'd_imp', 'd_brute', 'g_angel', 'g_titan']
A = np.array(Image.open(SRC).convert('RGB')).astype(float)
mag = (np.abs(A[..., 0] - 255) + A[..., 1] + np.abs(A[..., 2] - 255)) < 140
fig = ~mag
lab, n = nd.label(nd.binary_dilation(fig, iterations=6))
objs = [s for s in nd.find_objects(lab) if (s[0].stop - s[0].start) * (s[1].stop - s[1].start) > 3000]
objs.sort(key=lambda s: (round(s[0].stop / 350), s[1].start))
assert len(objs) == 12, len(objs)

def cells(h, w, ox, oy):
    xs = np.floor((np.arange(w) - ox) / CX).astype(int) + 1; ys = np.floor((np.arange(h) - oy) / CY).astype(int) + 1
    return ys, xs

def spread(sub, f, ox, oy):
    h, w, _ = sub.shape; ys, xs = cells(h, w, ox, oy); W = xs.max() + 1; idx = (ys[:, None] * W + xs[None, :]).ravel()
    t = 0
    for c in range(3):
        v = sub[..., c].ravel(); cnt = np.bincount(idx); s1 = np.bincount(idx, v); s2 = np.bincount(idx, v * v)
        t += (s2 - s1 * s1 / np.maximum(cnt, 1)).sum()
    return t

meta = {}
for key, s in zip(KEYS, objs):
    y0, y1, x0, x1 = s[0].start - 4, s[0].stop + 4, s[1].start - 4, s[1].stop + 4
    sub = A[y0:y1, x0:x1]; f = fig[y0:y1, x0:x1]; h, w, _ = sub.shape
    ox, oy = min(((ox, oy) for ox in np.arange(0, CX, CX / 6) for oy in np.arange(0, CY, CY / 6)), key=lambda o: spread(sub, f, *o))
    ys, xs = cells(h, w, ox, oy); H, W = ys.max() + 1, xs.max() + 1
    out = np.zeros((H, W, 4), np.uint8)
    q = (sub // 12).astype(int); keyc = q[..., 0] * 4096 + q[..., 1] * 64 + q[..., 2]
    for j in range(H):
        rm = ys == j
        for i in range(W):
            cm = xs == i; bf = f[rm][:, cm]
            if bf.size == 0 or bf.mean() < .5: continue
            kk = keyc[rm][:, cm][bf]; u, c = np.unique(kk, return_counts=True); best = u[c.argmax()]
            out[j, i, :3] = sub[rm][:, cm][bf][kk == best].mean(0); out[j, i, 3] = 255
    al = out[..., 3] > 0; rows = np.nonzero(al.any(1))[0]; cols = np.nonzero(al.any(0))[0]
    out = out[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]
    o = os.path.join(OUT, 'orig', key + '.png'); Image.fromarray(out, 'RGBA').save(o)
    p = os.path.join(OUT, 'units', key + '.png'); subprocess.run([sys.executable, os.path.join(ROOT, 'tools/art/pixel_punch.py'), o, p, '0.6', '40'], check=True)
    meta[key] = {'w': int(out.shape[1]), 'h': int(out.shape[0])}
    print(key, out.shape[1], 'x', out.shape[0])
json.dump(meta, open(os.path.join(OUT, 'units.json'), 'w'), indent=1)
