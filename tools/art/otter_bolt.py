"""Turn the owner's small projectile picture into a crisp moving water shot for skill P.

  python tools/art/otter_bolt.py

Reads art/incoming/otter_fx2/projectile_ref_v1.png (kept as it is; the owner said "p เปลี่ยนเป็นอันนี้", its source is unknown: replace it before a commercial release if it is someone else's work).
Takes the shape from that picture, enlarges it, redraws its tones as clean flat layers, moves the tail in code and writes art/dune/fx_gpt/otter_g_bolt.webp (24 frames, flying right).
"""
import json
import numpy as np, cv2
from PIL import Image

SRC, OUT = 'art/incoming/otter_fx2/projectile_ref_v1.png', 'art/dune/fx_gpt/otter_g_bolt.webp'; W, H, SS, N, COLS = 320, 180, 2, 24, 6; W2, H2 = W * SS, H * SS
STOPS = np.array([0, .2, .42, .64, .83, 1], np.float32); PAL = np.array([(5, 74, 136), (6, 116, 182), (10, 170, 226), (48, 222, 250), (166, 244, 253), (255, 255, 255)], np.float32) / 255; GLOW = np.array([38, 208, 250], np.float32) / 255   # the same colours as the rest of the otter's water set
def ss(a, b, v): q = np.clip((v - a) / (b - a), 0, 1); return q * q * (3 - 2 * q)
A = np.array(Image.open(SRC).convert('RGB'), np.float32) / 255; h, w = A.shape[:2]; x0, y0, x1, y1 = 26, 24, 230, 141; C = A[y0:y1, x0:x1]; UP = 5
C = cv2.resize(C, None, fx=UP, fy=UP, interpolation=cv2.INTER_CUBIC); C = cv2.GaussianBlur(C, (0, 0), UP * .42); R, G, B = C[..., 0], C[..., 1], C[..., 2]; V = C.max(2); L = R * .3 + G * .59 + B * .11
body = np.maximum(ss(.08, .17, B - R) * ss(.27, .38, V), ss(.5, .62, V)); n, lab, st, _ = cv2.connectedComponentsWithStats((body > .5).astype(np.uint8), 8); keep = np.isin(lab, [i for i in range(1, n) if st[i, 4] > UP * UP * 2]); body = body * cv2.GaussianBlur(keep.astype(np.float32), (0, 0), 1.2)
ys, xs = np.where(body > .5); bx0, bx1, by0, by1 = xs.min(), xs.max(), ys.min(), ys.max(); print('source shape', (bx1 - bx0) / UP, (by1 - by0) / UP); k = 545 / (bx1 - bx0); pad = 12
def fit(q): return cv2.resize(q[max(0, by0 - pad):by1 + pad, max(0, bx0 - pad):bx1 + pad], None, fx=k, fy=k, interpolation=cv2.INTER_CUBIC)
b, l = fit(body), fit(L); ph, pw = b.shape; ox, oy = W2 - 34 - pw, (H2 - ph) // 2; BODY = np.zeros((H2, W2), np.float32); LUM = np.zeros((H2, W2), np.float32); yy0, xx0 = max(oy, 0), max(ox, 0); BODY[yy0:oy + ph, xx0:ox + pw] = np.clip(b[yy0 - oy:yy0 - oy + min(H2 - yy0, ph - (yy0 - oy)), xx0 - ox:xx0 - ox + min(W2 - xx0, pw - (xx0 - ox))], 0, 1); LUM[yy0:oy + ph, xx0:ox + pw] = l[yy0 - oy:yy0 - oy + min(H2 - yy0, ph - (yy0 - oy)), xx0 - ox:xx0 - ox + min(W2 - xx0, pw - (xx0 - ox))]
BODY = ss(.42, .58, cv2.GaussianBlur(BODY, (0, 0), 1.6)); LUM = cv2.GaussianBlur(LUM, (0, 0), 1.2); U = np.clip((LUM - .07) / .85, 0, 1) ** .86; TONE = np.dstack([np.interp(U, STOPS, PAL[:, i]) for i in range(3)]).astype(np.float32); pm = np.dstack([TONE * BODY[..., None], BODY])
NOSE = float(np.where(BODY.max(0) > .5)[0].max()); yy, xx = np.mgrid[0:H2, 0:W2].astype(np.float32); q0 = cv2.GaussianBlur(np.random.default_rng(5).random((H2, W2), np.float32), (0, 0), 6); a0, b0 = np.percentile(q0, [1, 99]); NOISE = np.clip((q0 - a0) / (b0 - a0), 0, 1); D = np.clip((NOSE - xx) / 545, 0, 1)
def frame(f):
    t = f / 12 * 6.2832; g = .32 + .68 * (1 - (1 - min(1, (f + 1) / 4)) ** 3); sx = g * (1 + .035 * np.sin(t)); mx = NOSE + (xx - NOSE) / (1 + (sx - 1) * ss(.02, .4, D)) + np.sin(yy * .032 - t) * 5 * D; my = yy + np.sin(xx * .021 + t) * (2 + 15 * D) * D ** 1.15; c = cv2.remap(pm, mx.astype(np.float32), my.astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0); e = max(0, (f - 17) / 6) * 1.1
    if e > 0: c = c * ss(e - .12, e + .05, NOISE)[..., None]
    halo = np.clip(cv2.GaussianBlur(c[..., 3], (0, 0), 20) * .85 + cv2.GaussianBlur(c[..., 3], (0, 0), 7) * .4, 0, .7); return c + np.dstack([GLOW * (halo * (1 - c[..., 3]))[..., None], halo * (1 - c[..., 3])])
S = np.zeros((((N + COLS - 1) // COLS) * H, COLS * W, 4), np.float32); e = np.minimum.reduce([np.arange(H)[:, None].repeat(W, 1), np.arange(W)[None].repeat(H, 0), H - 1 - np.arange(H)[:, None].repeat(W, 1), W - 1 - np.arange(W)[None].repeat(H, 0)]).astype(np.float32)
for f in range(N):
    q = np.clip(cv2.resize(frame(f), (W, H), interpolation=cv2.INTER_AREA), 0, 1); S[(f // COLS) * H:(f // COLS + 1) * H, (f % COLS) * W:(f % COLS + 1) * W] = np.dstack([np.clip(q[..., :3] / np.maximum(q[..., 3:], 1e-3), 0, 1), q[..., 3] * np.clip(e / 10, 0, 1)])
Image.fromarray((np.clip(S, 0, 1) * 255 + .5).astype(np.uint8), 'RGBA').save(OUT, 'WEBP', quality=90, alpha_quality=92, method=6)
sp = json.load(open('art/dune/sprites.json')); sp['otter_g_bolt'] = {'src': OUT, 'n': N, 'w': W, 'h': H, 'cols': COLS, 'fx': 1, 'solid': 1}; json.dump(sp, open('art/dune/sprites.json', 'w'), separators=(',', ':')); print(OUT, N)
