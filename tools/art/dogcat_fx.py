# Dogs vs cats: attack effects drawn in code (owner 2026-11-12 "ปรับเอฟเฟกต์ตัวละครด้วย อันไหนทำเองได้ ทำสวยๆ"): free, no jobs.
# Every effect is a brightness field per frame (soft shapes + smooth noise), stepped onto a colour ramp from a dark rim to a
# white-hot core, so it comes out as clean pixel art on the same 1 px grid as the characters. Three tiers per character
# (1 / 2 / 3 stars): bigger, more colours, more sparks.
#   python3 tools/art/dogcat_fx.py -> art/incoming/dogcat/fx/<key>.png (one row of frames) + fx.json + preview.gif
import json, math, os, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
O = 'art/incoming/dogcat/fx/'; os.makedirs(O, exist_ok=True)
R = np.random.RandomState(7)
def field(n, c):                      # smooth noise 0..1
    return ndimage.zoom(R.rand(n // c + 2, n // c + 2), c, order=3)[:n, :n]
def ramp(I, cols, lo=.16):
    """I 0..1 -> RGBA: below lo see-through, then the colours in equal steps (the first one = the dark rim)"""
    I = np.clip(I, 0, 1); k = np.clip(((I - lo) / (1 - lo) * len(cols)).astype(int), 0, len(cols) - 1)
    out = np.zeros(I.shape + (4,), np.uint8); out[..., :3] = np.array(cols)[k]; out[..., 3] = (I >= lo) * 255; return out
def grid(n):
    y, x = np.mgrid[0:n, 0:n].astype(float); return x - n / 2 + .5, y - n / 2 + .5
ease = lambda t: 1 - (1 - t) ** 3
def sparks(a, pts, col, core=(255, 255, 255)):
    for x, y, s in pts:
        x, y = int(x), int(y)
        if 1 <= x < a.shape[1] - 1 and 1 <= y < a.shape[0] - 1:
            a[y, x] = core + (255,)
            if s > 1:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)): a[y + dy, x + dx] = col + (255,)
    return a
# ---------- sword slash: a crescent that sweeps round in front of the fighter (facing right)
def slash(n, cols, R0, wid, frames=7, sp=0, a0=-115, a1=80):
    x, y = grid(n); r = np.hypot(x + n * .18, y); th = np.degrees(np.arctan2(y, x + n * .18)); nz = field(n, 6); out = []
    pts = [(R.uniform(a0, a1), R.uniform(.9, 1.25), R.uniform(.2, .9)) for _ in range(sp)]
    for f in range(frames):
        t = (f + 1) / (frames + 1); head = a0 + (a1 - a0) * ease(min(1, t * 1.9)); tail = a0 + (a1 - a0) * ease(max(0, t * 1.5 - .5))
        u = np.clip((th - tail) / max(1, head - tail), 0, 1); ins = (th >= tail) & (th <= head)
        w = wid * (u ** .7) * (1 - .4 * t)                                     # thick at the leading end, a thin tail
        prof = np.clip(1 - np.abs(r - (R0 - w / 2)) / np.maximum(w / 2, .01), 0, 1)
        I = ins * prof ** .6 * (.45 + .55 * u) * (1.05 - .5 * t) + (nz - .5) * .12 * ins
        I = np.where(r > R0 - 1.2, np.minimum(I, .3) * (r < R0 + .4), I)         # a hard outer edge with a dark rim
        a = ramp(I, cols)
        a = sparks(a, [(n / 2 - n * .18 + math.cos(math.radians(an)) * R0 * (rr + t * .35), n / 2 + math.sin(math.radians(an)) * R0 * (rr + t * .35), 2 if ph > .5 else 1)
                       for an, rr, ph in pts if tail - 20 < an < head and t > ph * .5 and t < ph * .5 + .55], cols[-2])
        out.append(a)
    return out
# ---------- explosion: flash, fireball with a ragged edge, then a ring of smoke puffs
def boom(n, fire, smoke, R0, frames=11, rays=0, puffs=7):
    x, y = grid(n); r = np.hypot(x, y); th = np.arctan2(y, x); nz = field(n, 5); nz2 = field(n, 9); out = []
    for f in range(frames):
        t = f / (frames - 1); a = np.zeros((n, n, 4), np.uint8)
        if t > .3:                                                               # smoke puffs drifting out and up
            ts = (t - .3) / .7; S = np.zeros((n, n))
            for i in range(puffs):
                an = i * 2 * math.pi / puffs + .4; d = R0 * (.55 + .5 * ease(ts)); cx, cy = math.cos(an) * d, math.sin(an) * d * .8 - ts * R0 * .25
                S = np.maximum(S, 1 - np.hypot(x - cx, y - cy) / (R0 * (.42 - .26 * ts)))
            S = np.clip(S + (nz - .5) * .25, 0, 1) * (1.15 - ts * .75); a = ramp(S, smoke, lo=.3)
        if t < .75:                                                              # the fireball
            tf = t / .75; rad = R0 * (.35 + .65 * ease(tf)) * (1 + (nz2 - .5) * .5)
            I = np.clip(1 - r / rad, 0, 1) ** (.45 + tf) * (1.25 - tf * .9) + (nz - .5) * .15 * (r < rad)
            hole = np.clip((tf - .45) / .55, 0, 1) * R0 * .9; I = np.where(r < hole * (1 + (nz - .5) * .6), I * .2, I)      # it opens from the middle
            fb = ramp(I, fire); m = fb[..., 3] > 0; a[m] = fb[m]
        if rays and t < .5:
            for i in range(rays):
                an = i * 2 * math.pi / rays + .26; l0 = R0 * (.5 + t * 1.6); l1 = l0 + R0 * (.5 - t)
                for d in np.arange(l0, l1, .7):
                    px, py = int(n / 2 + math.cos(an) * d), int(n / 2 + math.sin(an) * d)
                    if 0 <= px < n and 0 <= py < n: a[py, px] = fire[-1] + (255,) if d < (l0 + l1) / 2 else fire[-3] + (255,)
        if f == 0: a = ramp(np.clip(1.2 - r / (R0 * .5), 0, 1), [fire[-2], fire[-1], (255, 255, 255)], lo=.2)   # first frame: a white flash
        out.append(a)
    return out
# ---------- impact spark: a four-point star + a ring that snaps out
def hit(n, cols, R0, frames=6):
    x, y = grid(n); r = np.hypot(x, y); out = []
    for f in range(frames):
        t = f / (frames - 1); L = R0 * (.5 + .9 * ease(t)); wdt = R0 * .3 * (1 - t) + .8
        star = np.maximum(np.clip(1 - np.abs(y) / wdt, 0, 1) * np.clip(1 - np.abs(x) / L, 0, 1) ** .5, np.clip(1 - np.abs(x) / wdt, 0, 1) * np.clip(1 - np.abs(y) / L, 0, 1) ** .5)
        xr, yr = (x + y) / 1.414, (x - y) / 1.414; L2 = L * .62
        star = np.maximum(star, .8 * np.maximum(np.clip(1 - np.abs(yr) / (wdt * .7), 0, 1) * np.clip(1 - np.abs(xr) / L2, 0, 1) ** .5, np.clip(1 - np.abs(xr) / (wdt * .7), 0, 1) * np.clip(1 - np.abs(yr) / L2, 0, 1) ** .5))
        ring = np.clip(1 - np.abs(r - R0 * (.3 + .8 * ease(t))) / (2.6 - t * 1.4), 0, 1) * (.8 - t * .55)
        out.append(ramp(np.maximum(star * (1.2 - t * .8), ring), cols, lo=.22))
    return out
# ---------- projectiles (spin frames, facing right)
def shuriken(n, body, edge, glow=None, frames=4):
    out = []
    for f in range(frames):
        c = Image.new('RGBA', (n * 4, n * 4)); d = ImageDraw.Draw(c); m = n * 2; a0 = f * 90 / frames
        if glow: d.ellipse((m - n * 1.7, m - n * 1.7, m + n * 1.7, m + n * 1.7), fill=glow + (255,))
        for i in range(4):
            an = math.radians(a0 + i * 90); t1 = (m + math.cos(an) * n * 1.7, m + math.sin(an) * n * 1.7)
            l = (m + math.cos(an + 1.0) * n * .55, m + math.sin(an + 1.0) * n * .55); r_ = (m + math.cos(an - .9) * n * .55, m + math.sin(an - .9) * n * .55)
            d.polygon([t1, l, (m, m), r_], fill=body + (255,)); d.line([t1, r_], fill=edge + (255,), width=3)
        d.ellipse((m - n * .28, m - n * .28, m + n * .28, m + n * .28), fill=(40, 34, 46, 255))
        im = c.resize((n, n), Image.BOX); a = np.asarray(im).copy(); a[..., 3] = (a[..., 3] > 120) * 255
        ring = ndimage.binary_dilation(a[..., 3] > 0) & ~(a[..., 3] > 0); a[ring] = (34, 28, 40, 255); out.append(a)
    return out
def ball(n, col, hi, frames=2):
    out = []
    for f in range(frames):
        x, y = grid(n); r = np.hypot(x, y); a = np.zeros((n, n, 4), np.uint8); a[r < n * .36] = col + (255,); a[np.hypot(x + n * .1, y + n * .1) < n * .14] = hi + (255,)
        a[(r >= n * .36) & (r < n * .36 + 1.1)] = (34, 28, 40, 255); out.append(a)
    return out
INK = (34, 28, 40)
FX = {
 # the shiba's slashes
 'shiba1_slash': slash(72, [(120, 84, 56), (196, 150, 96), (240, 214, 160), (255, 250, 230)], 27, 12, sp=3),
 'shiba2_slash': slash(88, [(60, 90, 150), (120, 170, 230), (190, 226, 255), (255, 255, 255)], 34, 18, sp=8),
 'shiba3_slash': slash(112, [(150, 70, 20), (236, 150, 30), (255, 214, 80), (255, 246, 190), (255, 255, 255)], 44, 26, sp=16, a0=-130, a1=100),
 # the corgi's shells and blasts
 'corgi_ball': ball(12, (52, 48, 60), (150, 150, 170)),
 'corgi1_boom': boom(64, [(110, 50, 30), (214, 110, 40), (250, 190, 70), (255, 244, 190)], [(96, 90, 96), (150, 144, 146), (200, 196, 194)], 20, puffs=5),
 'corgi2_boom': boom(88, [(120, 40, 30), (226, 90, 36), (250, 170, 50), (255, 226, 110), (255, 255, 230)], [(80, 76, 86), (136, 130, 138), (196, 192, 194)], 29, rays=8),
 'corgi3_boom': boom(120, [(110, 30, 40), (214, 60, 40), (248, 130, 40), (255, 200, 70), (255, 240, 150), (255, 255, 255)], [(70, 60, 80), (122, 110, 128), (180, 170, 180), (226, 220, 222)], 42, frames=13, rays=12, puffs=9),
 # the cat's throws
 'cat1_fish': shuriken(14, (176, 132, 84), (226, 190, 130)),
 'cat2_star': shuriken(16, (176, 184, 200), (240, 244, 255)),
 'cat3_star': shuriken(22, (250, 200, 60), (255, 246, 180), glow=(170, 80, 230)),
 'cat1_hit': hit(40, [(150, 110, 70), (240, 214, 160), (255, 255, 255)], 13),
 'cat2_hit': hit(52, [(110, 70, 190), (190, 150, 255), (240, 230, 255), (255, 255, 255)], 18),
 'cat3_hit': hit(72, [(120, 50, 180), (200, 110, 250), (255, 200, 90), (255, 246, 190), (255, 255, 255)], 26, frames=7),
}
meta = {}
for k, fr in FX.items():
    n = fr[0].shape[0]; st = Image.new('RGBA', (n * len(fr), n))
    for i, a in enumerate(fr): st.alpha_composite(Image.fromarray(a), (i * n, 0))
    st.save(O + k + '.png'); meta[k] = {'w': n, 'h': n, 'n': len(fr), 'fps': 14 if 'boom' in k else 16}
json.dump(meta, open(O + 'fx.json', 'w'))
# ---------- preview: every effect looping on grass, x3
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13)
keys = list(FX); cols_ = 5; cw, ch = 128, 140; rows = -(-len(keys) // cols_); g = []
for t in range(26):
    c = Image.new('RGBA', (cols_ * cw, rows * ch), (96, 150, 76, 255)); d = ImageDraw.Draw(c)
    for i, k in enumerate(keys):
        fr = FX[k]; n = fr[0].shape[0]; x, y = (i % cols_) * cw, (i // cols_) * ch
        f = t % (len(fr) + 4) if len(fr) > 4 else t % len(fr)
        if f < len(fr): c.alpha_composite(Image.fromarray(fr[f]), (x + (cw - n) // 2, y + 16 + (120 - n) // 2))
        d.text((x + 4, y + 2), k, fill=(20, 30, 20), font=F)
    g.append(c.resize((c.width * 2, c.height * 2), Image.NEAREST).convert('RGB'))
g[0].save(O + 'preview.gif', save_all=True, append_images=g[1:], duration=70, loop=0)
print(meta)

# ---------- demo: each 3-star character attacking a monster with its effect, x3
DC = 'art/incoming/dogcat/'; mj = json.load(open('art/action/mobs_hr/wolf.json')); wolf = Image.open('art/action/mobs_hr/wolf.png').crop((0, 0, mj['w'], mj['h'])); wolf = wolf.resize((wolf.width // 2, wolf.height // 2), Image.NEAREST).transpose(Image.FLIP_LEFT_RIGHT)
def fr_(path, i): return Image.open(path % i).convert('RGBA')
SH = [fr_(DC + 'pl3/char/Idle/animations/attack_se/south-east/frame_%03d.png', i) for i in (0, 1, 2, 0, 0, 0, 0, 0, 0)]      # wind-up, then our own slash instead of the drawn one
cg = Image.open(DC + 'corgi/game/s3_attack.png').convert('RGBA'); CG = [cg.crop((i * 104, 0, i * 104 + 104, 104)) for i in (0, 0, 1, 0, 0, 0, 0, 0, 0)]
CT = [fr_(DC + 'cat/char_s3/Idle/animations/attack_se/south-east/frame_%03d.png', i) for i in (0, 1, 2, 3, 4, 5, 6, 7, 8)]
def at(c, a, cx, cy): im = Image.fromarray(a); c.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
g = []
for t in range(22):
    c = Image.new('RGBA', (300, 360), (96, 150, 76, 255)); d = ImageDraw.Draw(c); k = min(t, 8)
    for row, (name, frames) in enumerate((('SHIBA 3', SH), ('CORGI 3', CG), ('CAT 3', CT))):
        y = row * 120; d.text((6, y + 4), name, fill=(20, 30, 20), font=F); hurt = (row == 0 and 3 <= t <= 6) or (row == 1 and 7 <= t <= 10) or (row == 2 and 9 <= t <= 12)
        c.alpha_composite(wolf, (190 + (4 if hurt else 0), y + 44)); c.alpha_composite(frames[k], (20, y + 10))
        if row == 0 and 3 <= t < 3 + 7: at(c, FX['shiba3_slash'][t - 3], 178, y + 70)
        if row == 1:
            if 2 <= t < 7: at(c, FX['corgi_ball'][t % 2], 110 + (t - 2) * 24, y + 66)
            if 7 <= t < 20: at(c, FX['corgi3_boom'][t - 7], 222, y + 66)
        if row == 2:
            if 5 <= t < 9: at(c, FX['cat3_star'][t % 4], 100 + (t - 5) * 30, y + 62)
            if 9 <= t < 16: at(c, FX['cat3_hit'][t - 9], 220, y + 64)
    g.append(c.resize((900, 1080), Image.NEAREST).convert('RGB'))
g[0].save(O + 'demo.gif', save_all=True, append_images=g[1:], duration=80, loop=0)
