#!/usr/bin/env python3
"""Pixel skill effects for Babies & Beasts, drawn by code.
Owner 2026-11-05: wants skills in the style of a mobile game clip (big crescent slashes, swirling water dome,
ice crystal flowers, raining crystal blades, fire swirls, lightning), but as pixel art.

How it works: every frame is a few soft grey "light" fields (shapes drawn at SS x detail), averaged down to the
pixel grid, then a colour ramp (dark edge ... white core) puts every pixel on one of a few flat colours, the way
hand-made pixel effects are shaded. Layers are stacked back to front.

  python3 tools/art/skillfx.py <out_dir> [key ...]     -> <out_dir>/<key>.png sheets + <out_dir>/fx_new.json
"""
import sys, json, math
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter

SS = 3                     # detail per output pixel
TAU = 2 * math.pi


def hexc(h):
    h = h.lstrip('#')
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


# colour ramps, darkest edge first, white core last
RAMPS = {
    'purple': ['#8a3ce8', '#4c169a', '#8a3ce8', '#b47cff', '#e4ccff', '#ffffff'],
    'fire':   ['#ff6a1a', '#9c1a14', '#e8441a', '#ff9226', '#ffd44c', '#fff8d8'],
    'ice':    ['#3a9cf4', '#1a52b4', '#3a9cf4', '#8cd6ff', '#d8f4ff', '#ffffff'],
    'aqua':   ['#22a6f0', '#1458c0', '#22a6f0', '#5ee4ff', '#c4fbff', '#ffffff'],
    'green':  ['#20c46c', '#0e6e44', '#20c46c', '#78f0a2', '#d2ffe0', '#ffffff'],
    'gold':   ['#f0aa26', '#a85a12', '#f0aa26', '#ffd85a', '#fff2b4', '#ffffff'],
    'pink':   ['#ff5aac', '#a8206e', '#ff5aac', '#ff9cd2', '#ffd8ef', '#ffffff'],
    'dark':   ['#5a1e9a', '#1e0a36', '#44187a', '#7a34b8', '#b07cf0', '#f0dcff'],
    'bolt':   ['#ffc23a', '#ffb43a', '#ffd660', '#ffee9a', '#fffbe0', '#ffffff'],
    'smoke':  ['#3a2c2e', '#2a2024', '#40343a', '#5a4c4c', '#766a62', '#968a7c'],
}
# step 0 is a see-through glow in the effect's main colour, step 1 the deep edge, then up to the white core
TH = [0.05, 0.15, 0.30, 0.47, 0.65, 0.84]   # light needed for each ramp step
ALPHA = [0.36, 0.92, 1, 1, 1, 1]


class Frame:
    """Hi-res coordinate grid in output-pixel units + a stack of (light, ramp) layers."""

    def __init__(self, W, H):
        self.W, self.H = W, H
        xs = (np.arange(W * SS) + .5) / SS
        ys = (np.arange(H * SS) + .5) / SS
        self.X, self.Y = np.meshgrid(xs, ys)
        self.layers = []

    def zero(self):
        return np.zeros_like(self.X)

    def add(self, light, ramp, alpha=1.0):
        self.layers.append((light, ramp, alpha))

    def render(self):
        out = np.zeros((self.H, self.W, 4))
        for light, ramp, alpha in self.layers:
            L = light.reshape(self.H, SS, self.W, SS).mean(axis=(1, 3))
            lv = np.full(L.shape, -1)
            for i, t in enumerate(TH):
                lv[L >= t] = i
            cols = np.array([hexc(c) for c in RAMPS[ramp]], float) / 255
            a = np.where(lv >= 0, np.array(ALPHA)[np.clip(lv, 0, 5)], 0) * alpha
            rgb = cols[np.clip(lv, 0, 5)]
            # "over" compositing
            ao = out[..., 3:4]
            an = a[..., None]
            na = an + ao * (1 - an)
            out[..., :3] = np.where(na > 0, (rgb * an + out[..., :3] * ao * (1 - an)) / np.maximum(na, 1e-6), 0)
            out[..., 3:4] = na
        img = (np.clip(out, 0, 1) * 255 + .5).astype(np.uint8)
        img[..., 3] = np.where(img[..., 3] < 40, 0, img[..., 3])
        return Image.fromarray(img, 'RGBA')


# ---------- helpers ----------
def sstep(a, b, x):
    t = np.clip((x - a) / (b - a + 1e-9), 0, 1)
    return t * t * (3 - 2 * t)


def ease_out(t):
    t = min(max(t, 0), 1)
    return 1 - (1 - t) ** 3


def ease_in(t):
    t = min(max(t, 0), 1)
    return t * t


def win(t, a, b):
    """0..1 progress of t inside [a,b]"""
    return min(max((t - a) / (b - a), 0), 1)


def noise(shape, sigma, seed):
    r = np.random.default_rng(seed).random(shape)
    n = gaussian_filter(r, sigma, mode='wrap')
    n = (n - n.min()) / (n.max() - n.min() + 1e-9)
    return n


def polar(F, cx, cy, sq=1.0, rot=0.0):
    dx = F.X - cx
    dy = (F.Y - cy) / sq
    if rot:
        c, s = math.cos(-rot), math.sin(-rot)
        dx, dy = dx * c - dy * s, dx * s + dy * c
    return np.hypot(dx, dy), np.arctan2(dy, dx)


def crescent(F, cx, cy, R, a_tail, a_head, W, sq=1.0, rot=0.0, glow=.35, inner=.25):
    """Slash arc on a circle (or a flat ellipse with sq<1): thin tail, thick near the head, sharp tip,
    brightest along the outer edge. Angles in radians; head may be smaller than tail (other direction)."""
    span = a_head - a_tail
    if abs(span) < 1e-3 or W <= 0:
        return F.zero()
    r, th = polar(F, cx, cy, sq, rot)
    d = np.mod((th - a_tail) * math.copysign(1, span), TAU)
    u = d / abs(span)
    inside = u <= 1
    uc = np.clip(u, 0, 1)
    k = (uc ** 0.9) * ((1 - uc) ** 0.55)
    k = k / 0.43
    w = W * k + 1e-6
    s = (R - r) / w
    band = np.where((s >= 0) & (s <= 1), (1 - np.clip(s, 0, 1)) ** .55, 0)
    out = np.where((s < 0), np.exp(-((r - R) / (0.45 * W + 1.5)) ** 2) * glow * k, 0)
    inn = np.where(s > 1, np.exp(-np.clip(s - 1, 0, 50) * 2.5) * inner * k, 0)
    return np.where(inside, np.maximum(band, out + inn), 0)


def chord_arc(p0, p1, bulge):
    """circle through p0 and p1 whose middle sticks out by `bulge` px (sign = side). -> (cx, cy, R, a0, a1)"""
    (x0, y0), (x1, y1) = p0, p1
    c = math.hypot(x1 - x0, y1 - y0)
    b = abs(bulge) + 1e-6
    R = (c * c / 4 + b * b) / (2 * b)
    mx_, my_ = (x0 + x1) / 2, (y0 + y1) / 2
    nx, ny = -(y1 - y0) / c, (x1 - x0) / c
    sg = 1 if bulge > 0 else -1
    cx, cy = mx_ - nx * sg * (R - b), my_ - ny * sg * (R - b)
    a0 = math.atan2(y0 - cy, x0 - cx)
    a1 = math.atan2(y1 - cy, x1 - cx)
    # go the short way round (the side that bulges)
    d = (a1 - a0 + math.pi) % TAU - math.pi
    return cx, cy, R, a0, a0 + d


def slash(F, p0, p1, bulge, W, t, st, dur=.24, glow=.5):
    """a crescent slash sweeping from p0 to p1 starting at time st"""
    k = win(t, st, st + dur)
    if k <= 0:
        return F.zero()
    cx, cy, R, a0, a1 = chord_arc(p0, p1, bulge)
    head = a0 + (a1 - a0) * ease_out(k)
    tail = a0 + (a1 - a0) * ease_in(win(t, st + dur * .45, st + dur * 2.1))
    thin = 1 - ease_in(win(t, st + dur * 1.1, st + dur * 2.4))
    if thin <= 0 or abs(head - tail) < .03:
        return F.zero()
    return crescent(F, cx, cy, R, tail, head, W * thin, glow=glow)


def ring(F, cx, cy, R, W, sq=1.0, power=1.0):
    r, _ = polar(F, cx, cy, sq)
    return np.clip(1 - np.abs(r - R) / (W + 1e-6), 0, 1) ** power


def disc(F, cx, cy, R, sq=1.0, power=1.5):
    r, _ = polar(F, cx, cy, sq)
    return np.clip(1 - r / (R + 1e-6), 0, 1) ** power


def spiral(F, cx, cy, r0, r1, arms, twist, phase, sq=1.0, sharp=3.0):
    r, th = polar(F, cx, cy, sq)
    r = r + 1e-6
    a = arms * (th - twist * np.log(r) - phase)
    band = (0.5 + 0.5 * np.cos(a)) ** sharp
    env = sstep(r0 * .5, r0, r) * (1 - sstep(r1 * .75, r1, r))
    return band * env


def star(F, cx, cy, L, w=.9, diag=.45):
    """4-point twinkle (plus short diagonal arms)"""
    dx = np.abs(F.X - cx)
    dy = np.abs(F.Y - cy)

    def arm(a, b, LL, ww):
        t = np.clip(1 - a / (LL + 1e-6), 0, 1)
        return np.clip(1 - b / (ww * t + .05), 0, 1) * t ** .5
    o = np.maximum(arm(dx, dy, L, w), arm(dy, dx, L, w))
    if diag > 0:
        p = (dx + dy) / 1.4142
        q = np.abs(dx - dy) / 1.4142
        o = np.maximum(o, .8 * arm(p, q, L * diag, w * .8))
    return o


def kite(F, base, tip, wd, split=.38, light=(.74, .5)):
    """Crystal blade: diamond from base to tip, widest at `split`, left facet light, right facet darker,
    white ridge. Drawn as polygons at full detail."""
    bx, by = base
    tx, ty = tip
    L = math.hypot(tx - bx, ty - by) + 1e-6
    ux, uy = (tx - bx) / L, (ty - by) / L
    nx, ny = -uy, ux
    mx, my = bx + ux * L * split, by + uy * L * split
    A = (bx, by)
    B = (mx + nx * wd, my + ny * wd)
    C = (tx, ty)
    D = (mx - nx * wd, my - ny * wd)
    im = Image.new('L', (F.W * SS, F.H * SS), 0)
    g = ImageDraw.Draw(im)
    sc = lambda p: (p[0] * SS, p[1] * SS)
    g.polygon([sc(A), sc(B), sc(C)], fill=int(255 * light[0]))
    g.polygon([sc(A), sc(D), sc(C)], fill=int(255 * light[1]))
    g.line([sc(A), sc(C)], fill=255, width=max(1, SS // 2))
    a = np.asarray(im, float) / 255
    return a


def lines(F, pts, width, val=1.0):
    im = Image.new('L', (F.W * SS, F.H * SS), 0)
    g = ImageDraw.Draw(im)
    g.line([(x * SS, y * SS) for x, y in pts], fill=int(255 * val), width=max(1, int(width * SS)), joint='curve')
    return np.asarray(im, float) / 255


def blur(a, px):
    return gaussian_filter(a, px * SS)


def bolt(rng, x0, y0, x1, y1, rough, depth=5):
    pts = [(x0, y0), (x1, y1)]
    for _ in range(depth):
        nxt = [pts[0]]
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            L = math.hypot(bx - ax, by - ay)
            mx, my = (ax + bx) / 2, (ay + by) / 2
            nx, ny = -(by - ay) / (L + 1e-6), (bx - ax) / (L + 1e-6)
            o = rng.normal() * rough * L
            nxt += [(mx + nx * o, my + ny * o), (bx, by)]
        pts = nxt
    return pts


def mx(*a):
    o = a[0]
    for b in a[1:]:
        o = np.maximum(o, b)
    return o


# ---------- effects ----------
# each: (W, H, ax, ay, n, fps, fn(F, t, i, rng))
FX = {}


def effect(key, W, H, ax, ay, n, fps):
    def deco(fn):
        FX[key] = (W, H, ax, ay, n, fps, fn)
        return fn
    return deco


@effect('nslash', 96, 80, 48, 44, 18, 30)
def nslash(F, t, i, rng):
    """Nin: two purple crescent slashes cross on the target, a white star flash, flying shards, gold twinkles."""
    cx, cy = 48, 44
    back, front, gold = F.zero(), F.zero(), F.zero()
    front = mx(front, slash(F, (cx - 34, cy - 28), (cx + 30, cy + 26), 12, 12, t, 0.0))
    front = mx(front, slash(F, (cx + 33, cy - 24), (cx - 30, cy + 28), -11, 11, t, 0.13))
    gold = mx(gold, slash(F, (cx - 26, cy - 30), (cx + 34, cy + 16), 16, 3.2, t, 0.05, glow=.2) * .9)
    # hit flash
    f = win(t, .16, .46)
    if 0 < f < 1:
        e = math.sin(math.pi * min(1, f * 1.6))
        front = mx(front, star(F, cx, cy, 30 * e, 2.6 * e, .5) * 1.1, disc(F, cx, cy, 9 * e) * 1.2)
        back = mx(back, ring(F, cx, cy, 8 + 30 * ease_out(f), 3.2 * (1 - f) + .4, sq=.6) * (1 - f * .5))
    # shards
    for j in range(11):
        a = rng.uniform(0, TAU)
        sp = rng.uniform(22, 40)
        st = .2 + rng.uniform(0, .12)
        k = win(t, st, st + .5)
        if 0 < k < 1:
            d = 6 + sp * ease_out(k)
            x, y = cx + math.cos(a) * d, cy + math.sin(a) * d * .8
            ln = 7 * (1 - k) + 2
            back = mx(back, kite(F, (x - math.cos(a) * ln, y - math.sin(a) * ln * .8), (x, y), 1.8 * (1 - k * .5)) * (1 - k * .25))
    # gold twinkles
    for j, (dx, dy, st) in enumerate([(-16, -18, .22), (20, -8, .32), (-6, 18, .42), (24, 16, .5)]):
        k = win(t, st, st + .34)
        if 0 < k < 1:
            gold = mx(gold, star(F, cx + dx, cy + dy, 9 * math.sin(math.pi * k), 1.1))
    F.add(back, 'purple')
    F.add(front, 'purple')
    F.add(gold, 'gold')


def flame(F, x, y, h, w, t, seed, lean=0.0):
    """rising flame tongue: wide soft base, wavy pointed top, noise that scrolls upward"""
    dx = F.X - x
    dy = y - F.Y                       # height above the base
    v = np.clip(dy / (h + 1e-6), -1, 2)
    off = lean * v * h + np.sin(v * 6 + t * 18 + seed) * w * .25 * v
    half = w * np.clip(1 - v, 0, 1) ** .7 * np.clip(v * 4 + .4, 0, 1)
    body = np.clip(1 - np.abs(dx - off) / (half + 1e-6), 0, 1) * (v >= -.05) * (v <= 1)
    return body ** .8 * (1.05 - v * .45)


def scroll_noise(F, sigma, seed, dy):
    n = noise((F.H * SS + 64, F.W * SS), sigma * SS, seed)
    o = int(dy * SS) % 64
    return n[o:o + F.H * SS, :]


def dissolve(a, n, thr):
    """eat the light away where the noise is below thr (pixel-style fade out)"""
    return a * np.clip((n - thr) * 6, 0, 1)


@effect('fswirl', 136, 104, 68, 70, 20, 28)
def fswirl(F, t, i, rng):
    """Tan's landing: fire swirls round the impact, flame crescents spin out, flames and embers shoot up, then smoke."""
    cx, cy = 68, 70
    smoke, ground, front, emb = F.zero(), F.zero(), F.zero(), F.zero()
    n1 = noise((F.H * SS, F.W * SS), 2.2 * SS, 7)
    grow = ease_out(win(t, 0, .45))
    fade = win(t, .5, 1)
    # ground fire spiral
    sp = spiral(F, cx, cy, 6, 18 + 46 * grow, 3, 1.9, t * 9, sq=.42, sharp=2.2) * (0.55 + 0.6 * n1)
    sp = mx(sp, disc(F, cx, cy, 20 + 30 * grow, sq=.42) * .55 * (1 - grow * .6))
    ground = dissolve(sp, n1, fade * 1.1)
    # spinning flame crescents on the ellipse
    for j in range(3):
        a0 = j * TAU / 3 + t * 8.5
        R = 22 + 40 * grow
        W = 9 * (1 - ease_in(fade)) + .5
        c = crescent(F, cx, cy - 4, R, a0, a0 + 2.0, W, sq=.45, glow=.6)
        front = mx(front, dissolve(c, n1, fade))
    # flash
    f = win(t, 0, .22)
    if f < 1:
        front = mx(front, disc(F, cx, cy - 10, 10 + 36 * ease_out(f), sq=.75) * (1 - f) * 1.3)
    # flames shooting up round the ring
    for j in range(7):
        a = j * TAU / 7 + rng.uniform(-.3, .3)
        st = rng.uniform(.05, .25)
        hh = rng.uniform(26, 44)
        k = win(t, st, st + .55)
        if 0 < k < 1:
            R = 14 + 30 * grow
            x, y = cx + math.cos(a) * R, cy + math.sin(a) * R * .42
            front = mx(front, flame(F, x, y, hh * math.sin(math.pi * k ** .7), 9 * (1 - k * .5), t, j, lean=math.cos(a) * .25))
    # centre fire column
    k = win(t, .02, .6)
    if 0 < k < 1:
        front = mx(front, flame(F, cx, cy, 64 * math.sin(math.pi * k ** .6), 17 * (1 - k * .4), t, 9))
    # embers
    for j in range(16):
        a = rng.uniform(-math.pi, 0)
        spd = rng.uniform(30, 60)
        st = rng.uniform(.1, .35)
        k = win(t, st, st + .6)
        if 0 < k < 1:
            x = cx + math.cos(a) * spd * k * 1.2
            y = cy - 8 + math.sin(a) * spd * k * .9 + 30 * k * k
            emb = mx(emb, star(F, x, y, 3.2 * (1 - k) + .8, .7, 0))
    # smoke at the end
    for j in range(6):
        a = j * TAU / 6 + .4
        k = win(t, .45, 1)
        if k > 0:
            x, y = cx + math.cos(a) * 34, cy + math.sin(a) * 15 - 16 * k
            smoke = mx(smoke, disc(F, x, y, 9 + 8 * k, power=1) * (1 - k) * 1.1)
    smoke = dissolve(smoke, n1, win(t, .7, 1) * .9)
    F.add(smoke, 'smoke')
    F.add(ground, 'fire')
    F.add(front, 'fire')
    F.add(emb, 'gold')


@effect('gburst', 120, 112, 60, 78, 20, 28)
def gburst(F, t, i, rng):
    """Fah: a green crescent ring sweeps round the target, crystal blades burst out of the ground, then shatter."""
    cx, cy = 60, 78
    back, ring_, crys, sh, tw = F.zero(), F.zero(), F.zero(), F.zero(), F.zero()
    # sweeping ring (front + back halves of an ellipse)
    k = win(t, 0, .32)
    if k > 0:
        head = -2.2 + TAU * 1.05 * ease_out(k)
        tail = -2.2 + TAU * 1.05 * ease_in(win(t, .12, .55))
        thin = 1 - ease_in(win(t, .35, .6))
        if thin > 0 and head - tail > .05:
            ring_ = crescent(F, cx, cy - 10, 40, tail, head, 9 * thin, sq=.42, glow=.6)
    # flash
    f = win(t, .18, .42)
    if 0 < f < 1:
        e = math.sin(math.pi * f)
        ring_ = mx(ring_, star(F, cx, cy - 22, 30 * e, 2.4 * e, .4), disc(F, cx, cy - 20, 10 * e))
    # crystal blades
    blades = [(-.5, 40, 5.5), (.45, 44, 6), (-1.0, 30, 4.5), (1.0, 32, 4.5), (-.15, 50, 6.5), (.2, 36, 5), (-1.35, 22, 3.5), (1.4, 24, 3.5)]
    for j, (lean, L, wd) in enumerate(blades):
        st = .18 + j * .025
        g = ease_out(win(t, st, st + .16))
        br = win(t, .66 + j * .012, .8 + j * .012)
        bx = cx + lean * 18
        by = cy - 6 + abs(lean) * 4
        if g > 0 and br < 1:
            tip = (bx + math.sin(lean) * L * g, by - math.cos(lean) * L * g)
            crys = mx(crys, kite(F, (bx, by), tip, wd * g, .3) * (1 - br))
        if br > 0:
            # shatter: shards fly out from along the blade
            for q in range(3):
                a = lean - math.pi / 2 + rng.uniform(-1.2, 1.2)
                v = rng.uniform(14, 30)
                if br < 1:
                    hx = bx + math.sin(lean) * L * (q + 1) / 4
                    hy = by - math.cos(lean) * L * (q + 1) / 4
                    x, y = hx + math.cos(a) * v * br, hy + math.sin(a) * v * br + 18 * br * br
                    sh = mx(sh, kite(F, (x, y + 3), (x + 1, y - 3), 1.6) * (1 - br))
        else:
            for q in range(3):
                rng.uniform(-1.2, 1.2); rng.uniform(14, 30)
    for j, (dx, dy, st) in enumerate([(-30, -36, .3), (26, -48, .38), (34, -18, .5), (-20, -10, .6), (4, -60, .7)]):
        k = win(t, st, st + .3)
        if 0 < k < 1:
            tw = mx(tw, star(F, cx + dx, cy + dy, 8 * math.sin(math.pi * k), 1))
    F.add(ring_ * .0 + back, 'green')
    F.add(crys, 'green')
    F.add(ring_, 'green')
    F.add(sh, 'green')
    F.add(tw, 'gold')


@effect('ibloom', 96, 96, 48, 64, 18, 28)
def ibloom(F, t, i, rng):
    """Ratri: an ice crystal flower bursts open where the comet lands, frost ring, then the crystals shatter."""
    cx, cy = 48, 64
    frost, crys, flash, sh = F.zero(), F.zero(), F.zero(), F.zero()
    g = ease_out(win(t, .0, .22))
    br = win(t, .62, .86)
    # frost ring on the ground
    k = win(t, 0, .6)
    frost = mx(frost, ring(F, cx, cy, 8 + 32 * ease_out(k), 3.5 * (1 - k) + .6, sq=.42) * (1 - k * .5) * (1 - win(t, .55, .8)))
    frost = mx(frost, disc(F, cx, cy, 26 * g, sq=.42) * .45 * (1 - win(t, .4, .9)))
    # radial crystals, upper half fan + a few low ones
    spikes = [(-90, 40, 6.5), (-62, 32, 5.5), (-118, 32, 5.5), (-38, 24, 4.5), (-142, 24, 4.5), (-14, 16, 3.5), (-166, 16, 3.5), (-76, 22, 3.5), (-104, 22, 3.5)]
    for j, (ang, L, wd) in enumerate(spikes):
        a = math.radians(ang)
        st = j * .015
        gg = ease_out(win(t, st, st + .2))
        if gg > 0 and br < 1:
            b0 = (cx, cy - 8)
            tip = (cx + math.cos(a) * L * gg, cy - 8 + math.sin(a) * L * gg)
            crys = mx(crys, kite(F, b0, tip, wd * gg, .35, (.86, .56)) * (1 - br))
        for q in range(2):
            v = rng.uniform(18, 34)
            da = rng.uniform(-.3, .3)
            if 0 < br < 1:
                d = L * (.5 + q * .4) + v * br
                x, y = cx + math.cos(a + da) * d, cy - 8 + math.sin(a + da) * d + 20 * br * br
                sh = mx(sh, kite(F, (x - math.cos(a) * 3, y - math.sin(a) * 3), (x + math.cos(a) * 3, y + math.sin(a) * 3), 1.7) * (1 - br))
    f = win(t, 0, .3)
    if f < 1:
        e = math.sin(math.pi * min(1, f * 1.5))
        flash = mx(flash, disc(F, cx, cy - 12, 14 * e) * 1.3, star(F, cx, cy - 12, 34 * e, 2.4 * e, .5))
    for j, (dx, dy, st) in enumerate([(-24, -40, .25), (22, -34, .35), (30, -6, .48), (-30, -12, .55)]):
        k = win(t, st, st + .3)
        if 0 < k < 1:
            flash = mx(flash, star(F, cx + dx, cy + dy, 7 * math.sin(math.pi * k), 1))
    F.add(frost, 'ice')
    F.add(crys, 'ice')
    F.add(sh, 'ice')
    F.add(flash, 'ice')


@effect('adome', 208, 160, 104, 112, 24, 26)
def adome(F, t, i, rng):
    """Ratri gold / Merlin: a dome of swirling water ribbons with lightning running through it."""
    cx, cy = 104, 112
    back, front, zap = F.zero(), F.zero(), F.zero()
    grow = ease_out(win(t, 0, .3))
    fade = win(t, .7, 1)
    n1 = noise((F.H * SS, F.W * SS), 2.5 * SS, 3)
    ground = spiral(F, cx, cy, 10, 30 + 64 * grow, 4, 1.6, -t * 7, sq=.36, sharp=3) * (.6 + .5 * n1)
    back = mx(back, dissolve(ground, n1, fade))
    rib = [(0, 84, .36, 0.0, 9), (-18, 76, .40, 1.3, 8), (-36, 64, .44, 2.6, 8), (-52, 48, .5, 3.9, 7), (-64, 30, .6, 5.2, 6),
           (-8, 80, .36, 3.2, 6), (-28, 70, .42, 4.6, 6), (-46, 56, .48, .7, 5)]
    for j, (h, R, sq, a0, W) in enumerate(rib):
        sp = (7.5 if j % 2 == 0 else -6.5) * (1 + .1 * j)
        a = a0 + t * sp
        L = 2.4 + .4 * math.sin(j)
        c = crescent(F, cx, cy + h * grow, R * (.35 + .65 * grow), a, a + (L if sp > 0 else -L), W * (1 - ease_in(fade)) + .3, sq=sq, glow=.5)
        front = mx(front, dissolve(c, n1, fade * .9))
    # lightning squiggles inside the dome
    if 4 <= i <= 19 and i % 2 == 0:
        for q in range(3):
            r2 = np.random.default_rng(50 + i * 7 + q)
            x0, y0 = cx + r2.uniform(-60, 60), cy + r2.uniform(-80, -10)
            x1, y1 = x0 + r2.uniform(-50, 50), y0 + r2.uniform(-10, 40)
            pts = bolt(r2, x0, y0, x1, y1, .22, 4)
            zap = mx(zap, lines(F, pts, 1.1), blur(lines(F, pts, 1.5), 1.2) * .6)
    f = win(t, 0, .25)
    if f < 1:
        front = mx(front, disc(F, cx, cy - 30, 30 * ease_out(f), sq=.9) * (1 - f))
    F.add(back, 'aqua')
    F.add(front, 'aqua')
    F.add(zap, 'ice')


@effect('pswirl', 128, 140, 64, 112, 24, 26)
def pswirl(F, t, i, rng):
    """Chan's party: pink ribbons spiral up round the bunny, a gold ring on the ground, stars pop."""
    cx, cy = 64, 112
    ground, rib, stars = F.zero(), F.zero(), F.zero()
    grow = ease_out(win(t, 0, .25))
    fade = win(t, .72, 1)
    n1 = noise((F.H * SS, F.W * SS), 2 * SS, 5)
    ground = mx(ring(F, cx, cy, 44 * grow, 2.2, sq=.4), ring(F, cx, cy, 34 * grow, 1.2, sq=.4) * .8)
    for j in range(8):
        a = j * TAU / 8 + t * 3
        ground = mx(ground, star(F, cx + math.cos(a) * 39 * grow, cy + math.sin(a) * 39 * .4 * grow, 3.5, .9, 0))
    ground = dissolve(ground, n1, fade)
    for j in range(12):
        st = j * .045
        k = win(t, st, st + .5)
        if 0 < k < 1:
            h = 4 + 96 * ease_out(k)
            R = 44 * (1 - .6 * k) + 4
            a = j * 2.4 + t * 11
            W = 9 * math.sin(math.pi * k) ** .7 + .4
            rib = mx(rib, crescent(F, cx, cy - h, R, a, a + 3.0, W, sq=.38, glow=.6))
    rib = mx(rib, dissolve(spiral(F, cx, cy, 6, 40 * grow, 3, 1.8, t * 8, sq=.4, sharp=3) * .7, n1, fade))
    for j in range(10):
        x = cx + rng.uniform(-50, 50)
        y = cy - rng.uniform(10, 120)
        st = rng.uniform(.1, .7)
        k = win(t, st, st + .25)
        if 0 < k < 1:
            stars = mx(stars, star(F, x, y, 8 * math.sin(math.pi * k), 1.1))
    F.add(ground, 'gold')
    F.add(rib, 'pink')
    F.add(stars, 'gold')


@effect('ddome', 128, 120, 64, 88, 22, 26)
def ddome(F, t, i, rng):
    """Mok's curse: a dark purple dome swells up, bright rim, curse crescents fly up out of it, then it melts away."""
    cx, cy = 64, 88
    smoke, dome, cres, tw = F.zero(), F.zero(), F.zero(), F.zero()
    grow = ease_out(win(t, 0, .3))
    fade = win(t, .6, 1)
    n1 = noise((F.H * SS, F.W * SS), 2 * SS, 11)
    R = 8 + 40 * grow
    dx = F.X - cx
    dy = F.Y - cy
    r = np.hypot(dx, dy * 1.05)
    up = dy <= 4
    rim = np.clip(r / (R + 1e-6), 0, 1)
    body = np.where(up & (r < R), .1 + .9 * rim ** 4, 0)
    swirl = spiral(F, cx, cy - R * .5, 2, R, 3, 2.2, -t * 6, sharp=2) * .5 * (r < R) * up
    dome = mx(body, swirl, ring(F, cx, cy, R * 1.02, 2.2, sq=.32))
    dome = dissolve(dome, n1, fade * 1.05)
    smoke = dissolve(disc(F, cx, cy, R * 1.3, sq=.35, power=.8) * .8, n1, fade * .9)
    for j in range(7):
        st = .18 + j * .05
        k = win(t, st, st + .42)
        if 0 < k < 1:
            ang = -math.pi / 2 + (j - 3) * .32
            d = R * .7 + 46 * ease_out(k)
            x, y = cx + math.cos(ang) * d, cy - 6 + math.sin(ang) * d
            c = crescent(F, x, y + 14, 15, ang - 1.1, ang + 1.1, 6 * math.sin(math.pi * k) ** .6 + .3, glow=.6)
            cres = mx(cres, c)
    f = win(t, .12, .4)
    if 0 < f < 1:
        tw = mx(tw, star(F, cx, cy - R, 26 * math.sin(math.pi * f), 2, .5))
    F.add(smoke, 'dark', .85)
    F.add(dome, 'dark', .85)
    F.add(cres, 'purple')
    F.add(tw, 'purple')


@effect('glight', 80, 208, 40, 192, 14, 24)
def glight(F, t, i, rng):
    """gold lightning bolt from the sky, impact flash, sparks"""
    cx, cy = 40, 192
    bo, gl, fl = F.zero(), F.zero(), F.zero()
    if i < 9:
        r2 = np.random.default_rng(900 + i // 2)
        pts = bolt(r2, cx + r2.uniform(-10, 10), 0, cx, cy - 4, .16, 6)
        w = 2.4 if i < 5 else 1.6
        core = lines(F, pts, w)
        for q in range(2):
            j0 = int(r2.uniform(.25, .7) * len(pts))
            x0, y0 = pts[j0]
            br = bolt(r2, x0, y0, x0 + r2.uniform(-34, 34), y0 + r2.uniform(20, 50), .2, 4)
            core = mx(core, lines(F, br, 1.1) * .9)
        bo = mx(core, blur(core, 1.6) * 1.1, blur(core, 4) * .55)
    k = win(t, .05, .6)
    if 0 < k < 1:
        fl = mx(fl, disc(F, cx, cy - 6, 6 + 24 * ease_out(k), sq=.6) * (1 - k) * 1.3, ring(F, cx, cy, 6 + 34 * ease_out(k), 2.5 * (1 - k) + .3, sq=.4))
        fl = mx(fl, star(F, cx, cy - 8, 30 * math.sin(math.pi * k), 2.2, .5))
    for j in range(10):
        a = rng.uniform(-math.pi, 0)
        v = rng.uniform(20, 44)
        k = win(t, .1, .8)
        if 0 < k < 1:
            x, y = cx + math.cos(a) * v * k, cy - 6 + math.sin(a) * v * k * .8 + 30 * k * k
            fl = mx(fl, star(F, x, y, 3 * (1 - k) + .8, .7, 0))
    F.add(fl, 'gold')
    F.add(bo, 'bolt')


def build(key, outdir):
    W, H, ax, ay, n, fps, fn = FX[key]
    cols = min(n, 6)
    rows = (n + cols - 1) // cols
    sheet = Image.new('RGBA', (W * cols, H * rows), (0, 0, 0, 0))
    for i in range(n):
        F = Frame(W, H)
        rng = np.random.default_rng(1000 + sum(map(ord, key)))
        fn(F, i / (n - 1), i, rng)
        sheet.paste(F.render(), ((i % cols) * W, (i // cols) * H))
    sheet.save(f'{outdir}/{key}.png', optimize=True)
    return {'w': W, 'h': H, 'fps': fps, 'n': n, 'cols': cols, 'ax': ax, 'ay': ay}


if __name__ == '__main__':
    out = sys.argv[1]
    keys = sys.argv[2:] or list(FX)
    man = {}
    for k in keys:
        man[k] = build(k, out)
        print(k, man[k])
    json.dump(man, open(f'{out}/fx_new.json', 'w'))
