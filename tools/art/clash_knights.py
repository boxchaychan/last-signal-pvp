#!/usr/bin/env python3
"""clash.html HUMAN tribe = the owner's 6 dark horned knights (art/incoming/clash/knights/owner_knights6.png, ChatGPT stickers:
white sticker border on black, 2 x 3). Free: cut away the black and the white sticker border (big white areas + white holes,
e.g. inside the bow), then snap to GPT's own pixel grid (CELL screen px a pixel, own phase per knight, most common colour a cell).
Writes art/clash/orig/<key>.png (cut, untouched colours) and art/clash/units/<key>.png (pixel_punch 0.6 / 40) + their sizes in
art/clash/units.json. Run: python3 tools/art/clash_knights.py"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
from scipy import ndimage as nd
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, 'art/incoming/clash/knights/owner_knights6.png'); CELL = 8.18
KEYS = ['h_k_sword', 'h_k_spear', 'h_k_axe', 'h_k_hammer', 'h_k_bow', 'h_k_mace']
A = np.asarray(Image.open(SRC).convert('RGB')).astype(int)
dark = A.max(2) < 60; labd, _ = nd.label(dark)
outside = np.isin(labd, list(set(np.unique(np.r_[labd[0], labd[-1], labd[:, 0], labd[:, -1]])) - {0}))
white = (A.min(2) > 140) & ((A.max(2) - A.min(2)) < 80); lw, nw = nd.label(white); ws = nd.sum(white, lw, range(1, nw + 1))
wmin = nd.mean(A.min(2), lw, range(1, nw + 1))
ring = np.isin(lw, [i + 1 for i, s in enumerate(ws) if s > 15000 or (s > 3500 and wmin[i] > 215)])   # border + sticker-white holes
fig = ~(outside | ring)
fig &= ~(nd.binary_dilation(ring, iterations=3) & (A.min(2) > 95)); fig &= ~nd.binary_dilation(outside, iterations=4); fig = nd.binary_opening(fig, iterations=1)
lab, n = nd.label(nd.binary_closing(~outside, iterations=2))
objs = sorted([s for s in nd.find_objects(lab) if (s[0].stop - s[0].start) * (s[1].stop - s[1].start) > 40000], key=lambda s: (s[0].start // 300, s[1].start))
assert len(objs) == 6
def spread(sub, ox, oy):
    h, w, _ = sub.shape; xs = np.floor((np.arange(w) - ox) / CELL).astype(int) + 1; ys = np.floor((np.arange(h) - oy) / CELL).astype(int) + 1
    idx = (ys[:, None] * (xs.max() + 1) + xs[None, :]).ravel(); t = 0
    for c in range(3):
        v = sub[..., c].ravel(); cnt = np.bincount(idx); s1 = np.bincount(idx, v); s2 = np.bincount(idx, v * v); t += (s2 - s1 * s1 / np.maximum(cnt, 1)).sum()
    return t
meta = json.load(open(os.path.join(ROOT, 'art/clash/units.json')))
for key, s in zip(KEYS, objs):
    sub = A[s]; f = fig[s]; h, w, _ = sub.shape
    ox, oy = min(((a, b) for a in np.arange(0, CELL, CELL / 6) for b in np.arange(0, CELL, CELL / 6)), key=lambda o: spread(sub, *o))
    xs = np.floor((np.arange(w) - ox) / CELL).astype(int) + 1; ys = np.floor((np.arange(h) - oy) / CELL).astype(int) + 1
    H, W = ys.max() + 1, xs.max() + 1; out = np.zeros((H, W, 4), np.uint8); q = (sub // 10).astype(int); kc = q[..., 0] * 4096 + q[..., 1] * 64 + q[..., 2]
    for j in range(H):
        rm = ys == j
        for i in range(W):
            cm = xs == i; bf = f[rm][:, cm]
            if bf.size == 0 or bf.mean() < .5: continue
            kk = kc[rm][:, cm][bf]; u, c = np.unique(kk, return_counts=True); out[j, i, :3] = sub[rm][:, cm][bf][kk == u[c.argmax()]].mean(0); out[j, i, 3] = 255
    al = out[..., 3] > 0; r = np.nonzero(al.any(1))[0]; c = np.nonzero(al.any(0))[0]; out = out[r[0]:r[-1] + 1, c[0]:c[-1] + 1]
    o = os.path.join(ROOT, 'art/clash/orig', key + '.png'); Image.fromarray(out).save(o)
    p = os.path.join(ROOT, 'art/clash/units', key + '.png'); subprocess.run([sys.executable, os.path.join(ROOT, 'tools/art/pixel_punch.py'), o, p, '0.6', '40'], check=True)
    meta[key] = {'w': int(out.shape[1]), 'h': int(out.shape[0])}; print(key, out.shape[1], 'x', out.shape[0])
json.dump(meta, open(os.path.join(ROOT, 'art/clash/units.json'), 'w'), indent=1)
