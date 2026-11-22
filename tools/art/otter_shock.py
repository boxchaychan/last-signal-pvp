"""Paint the otter's punch-through shock in code: torn rings travelling out of the enemy's back, white shards of water, flying flecks.

  python tools/art/otter_shock.py

Writes art/dune/fx_gpt/otter_g_shock.webp (16 frames, punch goes to the right) and its entry in art/dune/sprites.json.
The owner's anime frame was only looked at for the idea; it is not read, stored or traced here.
"""
import json
import numpy as np, cv2
from PIL import Image

CELL, SS, COLS, N = 420, 2, 4, 16; S = CELL * SS; OUT = 'art/dune/fx_gpt/otter_g_shock.webp'; CX, CY, TILT = 280., 420., np.radians(-24)
yy, xx = np.mgrid[0:S, 0:S].astype(np.float32); UX = (xx - CX) * np.cos(TILT) + (yy - CY) * np.sin(TILT); VY = -(xx - CX) * np.sin(TILT) + (yy - CY) * np.cos(TILT); DIST = np.hypot(xx - CX, yy - CY)
RING, WHITE, BLUE, CYAN = [np.array(c, np.float32) / 255 for c in ((196, 226, 252), (255, 255, 255), (24, 112, 236), (46, 202, 250))]
def ss(a, b, v): q = np.clip((np.asarray(v, np.float32) - a) / (b - a), 0, 1); return q * q * (3 - 2 * q)
def out3(v): v = min(1, max(0, v)); return 1 - (1 - v) ** 3
TABLE = [np.random.default_rng(40 + i).uniform(-1, 1, 512).astype(np.float32) for i in range(8)]
def jag(ang, seed):   # a torn edge: coarse and fine teeth round the ring
    k = (ang + np.pi) / 6.2832; a = TABLE[seed % 8][(k * 56).astype(np.int32) % 512]; b = TABLE[(seed + 3) % 8][(k * 170).astype(np.int32) % 512]; return a * .68 + b * .32
def ring(R, w, d, seed, alpha):
    if alpha <= .01: return np.zeros((S, S), np.float32)
    u = (UX - d) / .44; r = np.hypot(u, VY); ang = np.arctan2(VY, u); wid = w * (.42 + .9 * (.5 + .5 * np.cos(ang - .6))); outer = R + jag(ang, seed) * (6 + R * .055); inner = R - wid + jag(ang, seed + 1) * (6 + R * .07); return ss(outer + 2, outer - 2, r) * ss(inner - 2, inner + 2, r) * alpha
r0 = np.random.default_rng(9); SHARDS = []
for i in range(14):
    fwd = i < 9; SHARDS.append((float(r0.uniform(-.92, .92) if fwd else r0.choice([-1, 1]) * r0.uniform(2.1, 3.05)), float(r0.uniform(230, 405) if fwd else r0.uniform(120, 240)), float(r0.uniform(4.5, 12) if fwd else r0.uniform(3.5, 8)), float(r0.uniform(0, .1)), float(r0.uniform(-34, 34)), r0.uniform(-1, 1, 14).astype(np.float32)))
FLECKS = [(float(r0.uniform(-.85, .85) if r0.random() < .75 else r0.uniform(1.9, 4.3)), float(r0.uniform(90, 250)), float(r0.uniform(190, 430)), float(r0.uniform(5, 15)), float(r0.uniform(1.6, 3.4)), float(r0.uniform(0, .18))) for _ in range(30)]
def shard(m, th, L, wid, t0, bend, wob, t):
    q = (t - t0) / (1 - t0)
    if q <= 0: return
    s1 = L * out3(q / .3) * (1 + .22 * q); s0 = L * .95 * float(ss(.24, .86, q))
    if s1 - s0 < 4: return
    k = np.linspace(0, 1, 14); s = s0 + (s1 - s0) * k; h = wid * (1 - float(ss(.55, .95, q)) * .7) * np.sin(np.pi * np.clip(k, .02, .98)) ** .7; off = bend * np.sin(np.pi * k) * (s1 / L); tilt = TILT + th; dx, dy = np.cos(tilt), np.sin(tilt); nx, ny = -dy, dx
    top = np.c_[CX + dx * s + nx * (off + h * (1 + wob * .4)), CY + dy * s + ny * (off + h * (1 + wob * .4))]; low = np.c_[CX + dx * s + nx * (off - h * (1 - wob[::-1] * .4)), CY + dy * s + ny * (off - h * (1 - wob[::-1] * .4))]; cv2.fillPoly(m, [np.round(np.r_[top, low[::-1]]).astype(np.int32)], 255, cv2.LINE_AA)
def over(base, rgb, a): return base * (1 - a[..., None]) + np.dstack([rgb[..., 0] * a, rgb[..., 1] * a, rgb[..., 2] * a, a]) if rgb.ndim == 3 else base * (1 - a[..., None]) + np.dstack([rgb[0] * a, rgb[1] * a, rgb[2] * a, a])
def frame(t):
    q2 = max(0, (t - .08) / .92); q3 = max(0, (t - .2) / .8)
    R = np.maximum.reduce([ring(60 + 205 * out3(t / .55), 112 * (1 - .72 * t) + 10, 10 + 40 * t, 0, float(1 - ss(.55, .95, t))), ring(30 + 232 * out3(q2 / .6), 60 * (1 - .75 * q2) + 6, 50 + 150 * out3(q2), 2, float(ss(0, .1, q2) * (1 - ss(.5, .92, q2)))), ring(20 + 182 * out3(q3 / .6), 40 * (1 - .7 * q3) + 5, 120 + 215 * out3(q3), 5, float(ss(0, .12, q3) * (1 - ss(.48, .9, q3))))])
    m = np.zeros((S, S), np.uint8)
    for sh in SHARDS: shard(m, *sh, t)
    for th, a, b, z, rt, t0 in FLECKS:
        q = (t - t0) / (1 - t0)
        if 0 < q < .92:
            d = a + (b - a) * out3(q / .8); x, y = CX + np.cos(TILT + th) * d, CY + np.sin(TILT + th) * d; zz = z * (1 - q * .5); c, s = np.cos(TILT + th), np.sin(TILT + th); cv2.fillPoly(m, [np.round(np.array([[x + c * zz * rt, y + s * zz * rt], [x - s * zz * .36, y + c * zz * .36], [x - c * zz * rt * .7, y - s * zz * rt * .7], [x + s * zz * .42, y - c * zz * .42]])).astype(np.int32)], 255, cv2.LINE_AA)
    W = cv2.GaussianBlur(m, (0, 0), .9).astype(np.float32) / 255; core = (1 - ss(10, 42 + 70 * t, DIST)) * float(1 - ss(.08, .3, t)); W = np.maximum(W, core); B = np.maximum(R, W); glow = np.clip(cv2.GaussianBlur(B, (0, 0), 25) * .85, 0, .62); edge = np.clip(cv2.GaussianBlur(B, (0, 0), 8) * 1.9, 0, .86); disc = (1 - ss(0, 170 + 300 * t, DIST)) * .46 * float(1 - ss(.1, .58, t))
    c = np.zeros((S, S, 4), np.float32); c = over(c, CYAN, glow); c = over(c, BLUE, np.maximum(edge, disc)); c = over(c, RING, R * .92); return over(c, WHITE, W)
A = np.zeros((((N + COLS - 1) // COLS) * CELL, COLS * CELL, 4), np.float32); e = np.minimum.reduce([np.arange(CELL)[:, None].repeat(CELL, 1), np.arange(CELL)[None].repeat(CELL, 0), CELL - 1 - np.arange(CELL)[:, None].repeat(CELL, 1), CELL - 1 - np.arange(CELL)[None].repeat(CELL, 0)]).astype(np.float32)
for f in range(N):
    q = np.clip(cv2.resize(frame(f / (N - 1)), (CELL, CELL), interpolation=cv2.INTER_AREA), 0, 1); a = q[..., 3] * np.clip(e / 12, 0, 1); A[(f // COLS) * CELL:(f // COLS + 1) * CELL, (f % COLS) * CELL:(f % COLS + 1) * CELL] = np.dstack([np.clip(q[..., :3] / np.maximum(q[..., 3:], 1e-3), 0, 1), a])
Image.fromarray((np.clip(A, 0, 1) * 255 + .5).astype(np.uint8), 'RGBA').save(OUT, 'WEBP', quality=86, alpha_quality=90, method=6)
sp = json.load(open('art/dune/sprites.json')); sp.pop('otter_g_jet', None); sp['otter_g_shock'] = {'src': OUT, 'n': N, 'w': CELL, 'h': CELL, 'cols': COLS, 'fx': 1, 'solid': 1}; json.dump(sp, open('art/dune/sprites.json', 'w'), separators=(',', ':')); print(OUT, N, A.shape)
