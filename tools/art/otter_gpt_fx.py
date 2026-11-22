"""Cut the owner's ChatGPT water sheet into moving, glowing skill effects for the otter (test link dune.html?hero=otter&wfx=3).

  python tools/art/otter_gpt_fx.py

Reads art/incoming/otter_fx2/gpt_water_sheet_v1.webp (kept as it is). Uses only the pieces without a little creature and without the ChatGPT mark:
geyser, big dome, whirl, the front of the streak, small spike. Each still is moved in code (rise, spread, spin, shimmer, dissolve), graded to the
glowing cyan set and written to art/dune/fx_gpt/ with the frame layout of the fx_w_* sheets. Adds otter_g_tornado to art/dune/sprites.json.
"""
import json, os
import numpy as np, cv2
from PIL import Image

SRC, OUT = 'art/incoming/otter_fx2/gpt_water_sheet_v1.webp', 'art/dune/fx_gpt/'; os.makedirs(OUT, exist_ok=True); A = np.array(Image.open(SRC).convert('RGB'), np.float32) / 255; BG = np.array([22, 23, 25], np.float32) / 255
STOPS = np.array([0, .2, .42, .64, .83, 1], np.float32); COLS = np.array([(5, 74, 136), (6, 116, 182), (10, 170, 226), (48, 222, 250), (166, 244, 253), (255, 255, 255)], np.float32) / 255; HALO = np.array([38, 208, 250], np.float32) / 255
def ss(a, b, v): q = np.clip((v - a) / (b - a), 0, 1); return q * q * (3 - 2 * q)
def out3(v): v = min(1, max(0, v)); return 1 - (1 - v) ** 3
def edge(h, w): return np.minimum.reduce([np.arange(h)[:, None].repeat(w, 1), np.arange(w)[None].repeat(h, 0), h - 1 - np.arange(h)[:, None].repeat(w, 1), w - 1 - np.arange(w)[None].repeat(h, 0)]).astype(np.float32)
def cut(x0, y0, x1, y1):   # dark background to transparency, then the glowing colours; returns premultiplied RGBA
    q = A[y0:y1, x0:x1]; a = np.clip((q[..., 2] - BG[2] - .035) / .44, 0, 1); rgb = np.clip((q - BG * (1 - a)[..., None]) / np.maximum(a[..., None], .06), 0, 1); L = rgb[..., 0] * .3 + rgb[..., 1] * .59 + rgb[..., 2] * .11; u = np.clip((L - .07) / .85, 0, 1) ** .74
    c = np.dstack([np.interp(u, STOPS, COLS[:, i]) for i in range(3)]).astype(np.float32); a = a * np.clip(edge(*a.shape) / 7, 0, 1); return np.dstack([c * a[..., None], a])
def place(p, W, H, tw, cx, by):
    k = tw / p.shape[1]; q = cv2.resize(p, (tw, round(p.shape[0] * k)), interpolation=cv2.INTER_AREA if k < 1 else cv2.INTER_CUBIC); q = np.clip(q, 0, 1); C = np.zeros((H, W, 4), np.float32); x = int(cx - tw / 2); y = by - q.shape[0]; x0, y0 = max(x, 0), max(y, 0); x1, y1 = min(x + tw, W), min(by, H); C[y0:y1, x0:x1] = q[y0 - y:y1 - y, x0 - x:x1 - x]; return C
GRID = {}
def grid(H, W):
    if (H, W) not in GRID: GRID[H, W] = tuple(g.astype(np.float32) for g in np.mgrid[0:H, 0:W])
    return GRID[H, W]
def xf(c, ox, oy, sx, sy, dx=0, dy=0):
    yy, xx = grid(*c.shape[:2]); return cv2.remap(c, (ox + (xx - ox) / sx + dx).astype(np.float32), (oy + (yy - oy) / sy + dy).astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
NOISE = {}
def noise(H, W):
    if (H, W) not in NOISE: q = cv2.GaussianBlur(np.random.default_rng(7).random((H, W), np.float32), (0, 0), 9); a, b = np.percentile(q, [1, 99]); NOISE[H, W] = np.clip((q - a) / (b - a), 0, 1)
    return NOISE[H, W]
def keep(c, e): return c if e <= 0 else c * ss(e - .12, e + .05, noise(*c.shape[:2]))[..., None]
W2 = 600
GEY = place(cut(700, 238, 986, 531), W2, W2, 510, 300, 562)
DOME = place(cut(355, 552, 1022, 931), W2, W2, 580, 300, 432)
STREAK = place(cut(372, 85, 612, 222), W2, W2, 560, 300, 460)
SPIKE = place(cut(182, 1330, 312, 1500), W2, W2, 290, 300, 500)
TW, TH = 640, 340; TOR = place(cut(410, 938, 1012, 1252), TW, TH, 640, 320, 336); TCX, TCY, TR = 347, 107, .32
def geyser(f, n):
    t = f / (n - 1); r = out3((f - 5) / 7) if f >= 5 else 0; sy = .1 + .9 * r; yy, xx = grid(W2, W2); dx = np.sin(yy * .018 + t * 26) * 7 * (562 - yy) / 520 * r; c = xf(GEY, 300, 562, .82 + .18 * r, max(.04, sy), dx); return keep(c, ss(.62, 1, t) * 1.08) * min(1, f / 3 + .15)
def crown(f, n):
    t = f / (n - 1); G = out3(t / .2); yy, xx = grid(W2, W2); dx = np.sin(yy * .02 + t * 18) * 4 * (1 - G * .4); dy = np.sin(xx * .016 - t * 16) * 4; k = .3 + .7 * G + .06 * t; c = xf(DOME, 300, 432, k, (.16 + .84 * G) * (1 + .05 * t), dx, dy); return keep(c, ss(.52, 1, t) * 1.08)
def wave(f, n):
    t = f / (n - 1); G = out3(t / .18); yy, xx = grid(W2, W2); dy = np.sin(xx * .05 - t * 34) * 4; L = 40 + 520 * G; c = xf(STREAK, 560, 390, 1, .82 + .18 * G, 0, dy) * ss(560 - L, 600 - L, xx)[..., None]; return keep(c, ss(.56, 1, t) * 1.08)
def punch(f, n):
    t = f / (n - 1); G = out3(t / .24); yy, xx = grid(W2, W2); dx = np.sin(yy * .03 + t * 20) * 3; return keep(xf(SPIKE, 300, 500, .6 + .4 * G, .18 + .82 * G, dx), ss(.42, 1, t) * 1.08)
def tornado(f, n):   # flow, not a rigid turn: two short turns cross-fade forever, so the ring's shape and its hole stay where GPT drew them
    a = f / n * 6.283; yy, xx = grid(TH, TW); u = xx - 335; v = (yy - 125) / .34; mask = (1 - ss(286, 326, np.hypot(u, v)))[..., None]; ring = 0
    for q in (f / n, (f / n + .5) % 1):
        th = (q - .5) * .72; ca, sa = np.cos(th), np.sin(th); ring = ring + (1 - abs(2 * q - 1)) * cv2.remap(TOR * mask, (335 + u * ca + v * sa).astype(np.float32), (125 + (-u * sa + v * ca) * .34).astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    stem = xf(TOR * (1 - mask), 320, 336, 1, 1, np.sin(yy * .03 + a * 2) * 5 * (336 - yy) / 230); return stem + ring * (1 - stem[..., 3:])
def finish(c, w, h):
    q = np.clip(cv2.resize(c, (w, h), interpolation=cv2.INTER_AREA), 0, 1); a = q[..., 3]; k = w / 300; g = np.clip((cv2.GaussianBlur(a, (0, 0), 11 * k) * .8 + cv2.GaussianBlur(a, (0, 0), 3.5 * k) * .4) * 1.15, 0, 1) * .7 * np.clip(edge(h, w) / (14 * k), 0, 1); o = a + g * (1 - a); pm = q[..., :3] + HALO * (g * (1 - a))[..., None]; return np.dstack([np.clip(pm / np.maximum(o[..., None], 1e-3), 0, 1), o])
def sheet(fn, n, w, h, cols, name):
    S = np.zeros((((n + cols - 1) // cols) * h, cols * w, 4), np.float32)
    for f in range(n): S[(f // cols) * h:(f // cols + 1) * h, (f % cols) * w:(f % cols + 1) * w] = finish(fn(f, n), w, h)
    p = f'{OUT}{name}.webp'; Image.fromarray((np.clip(S, 0, 1) * 255 + .5).astype(np.uint8), 'RGBA').save(p, 'WEBP', quality=86, alpha_quality=90, method=6); print(p, n, os.path.getsize(p) // 1024, 'KB'); return p
for name, fn, n in (('fx_w_geyser', geyser, 30), ('fx_w_crown', crown, 23), ('fx_w_wave', wave, 26), ('fx_w_punch', punch, 20)): sheet(fn, n, 300, 300, 6, name)
p = sheet(tornado, 24, 320, 170, 6, 'otter_g_tornado'); sp = json.load(open('art/dune/sprites.json')); sp['otter_g_tornado'] = {'src': p, 'n': 24, 'w': 320, 'h': 170, 'cols': 6}; json.dump(sp, open('art/dune/sprites.json', 'w'), separators=(',', ':'))
