# Dogs vs cats: the "beautiful scene" mock (owner 2026-11-12 "ทำฉากให้สวยๆ"): free, no jobs.
# One portrait phone screen (585 x 1266 world px = zoom-out 1.5, saved x2): your stone board (7 x 4 round paw pedestals inside
# the monster loop) and, below it, the dogs' yard: a wooden bench strip, the dog house (drawn in code), campfire, well, trees,
# fences, a lily pond. What makes it read as pixel art (the owner's village reference): every sprite on ONE pixel grid (props
# shrunk by whole numbers with reduce(): a dark outline pixel wins, else the most common colour), calm flat ground, dark lines
# between shapes, and one sun from the upper left: every sprite casts a sheared shadow to the lower right.
#   python3 tools/art/tw_scene.py -> art/incoming/dogcat/tw_scene.png
import json, math, random, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
sys.path.insert(0, 'tools/art'); from stone_px import blocks; from px_outline import outline
random.seed(21); np.random.seed(21)
W, H = 585, 1266; DC = 'art/incoming/dogcat/'; P2 = 'art/td/props/set2/cut/'; TL = 'art/td/tiles/'
yy, xx = np.mgrid[0:H, 0:W]
INK = (34, 28, 40)

def reduce(im, n):
    if n == 1: return im.convert('RGBA')
    a = np.asarray(im.convert('RGBA')); h, w = a.shape[0] // n * n, a.shape[1] // n * n
    b = a[:h, :w].reshape(h // n, n, w // n, n, 4).transpose(0, 2, 1, 3, 4).reshape(h // n, w // n, n * n, 4).astype(int)
    op = b[..., 3] >= 128; lum = (b[..., :3] * [.299, .587, .114]).sum(-1); lum = np.where(op, lum, 1e9)
    dark = (lum < 58).sum(-1) >= max(1, n * n // 4); di = lum.argmin(-1)
    key = np.where(op, (b[..., 0] >> 3) * 1024 + (b[..., 1] >> 3) * 32 + (b[..., 2] >> 3), -1)
    mi = ((key[..., :, None] == key[..., None, :]) & op[..., :, None]).sum(-1).argmax(-1)
    out = np.take_along_axis(b, np.where(dark, di, mi)[..., None, None].repeat(4, -1), 2)[:, :, 0]
    out[..., 3] = np.where(op.sum(-1) * 2 >= n * n, 255, 0); return Image.fromarray(out.astype(np.uint8))
def crop(im): im = im.convert('RGBA'); return im.crop(im.getbbox())
def prop(n, k): return crop(reduce(crop(Image.open(P2 + n + '.png')), k))
def flip(im): return im.transpose(Image.FLIP_LEFT_RIGHT)
def feet(im):
    al = np.asarray(im)[..., 3] > 0; ys = np.where(al.any(1))[0]; y1 = ys[-1]; xs = np.where(al[max(0, y1 - 5):y1 + 1].any(0))[0]
    return (xs[0] + xs[-1]) // 2, y1, ys[0]

# ---------- ground: calm grass with tone patches, a dirt yard
def tex(k, lower):
    m = json.load(open(TL + k + '_meta.json'))['tileset_data']['tiles']; im = Image.open(TL + k + '.png').convert('RGB')
    for t in m:
        if all((t['corners'][q] == 'lower') == lower for q in t['corners']):
            b = t['bounding_box']; return im.crop((b['x'], b['y'], b['x'] + 32, b['y'] + 32))
def fill(t):
    o = Image.new('RGB', (W, H))
    for y in range(0, H, 32):
        for x in range(0, W, 32): o.paste(t.transpose(random.choice([Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM, Image.ROTATE_180])) if random.random() < .5 else t, (x, y))
    a = np.asarray(o).astype(float); m = a.reshape(-1, 3).mean(0); return m + (a - m) * .55          # calmer: less speckle
def noise(c):
    n = np.random.rand(H // c + 3, W // c + 3)
    return np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize(((W // c + 3) * c, (H // c + 3) * c), Image.BICUBIC)).astype(float)[:H, :W] / 255
N60, N24, N9 = noise(60), noise(24), noise(9)
img = fill(tex('path_pro', False)) * np.array([.96, 1.0, .9])
img[N60 < .34] *= .9; lt = N60 > .68; img[lt] = img[lt] * 1.05 + np.array([10, 8, -2])
DIRT = fill(tex('path_pro', True)) * np.array([1.04, 1.0, .94])
def blob(cx, cy, rx, ry): return ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 + (N24 - .5) * .5 + (N9 - .5) * .22 < 1
def seg(x0, y0, x1, y1, r):
    dx, dy = x1 - x0, y1 - y0; t = np.clip(((xx - x0) * dx + (yy - y0) * dy) / (dx * dx + dy * dy), 0, 1)
    return np.hypot(xx - (x0 + t * dx), yy - (y0 + t * dy)) + (N24 - .5) * 16 + (N9 - .5) * 6 < r
import os; HOUSE = os.environ.get('HOUSE') == '1'; BGM = os.environ.get('BG') == '1'   # BG=1: the empty scene for the game (art/dogcat/bg.png + geo.json)
HX, HY = 292, 918                                                   # the dog house's door step
dirt = (blob(HX, HY + 26, 150, 78) if HOUSE else blob(HX, HY + 40, 60, 30)) | seg(HX, HY + 40, HX - 10, 1130, 26) | seg(HX - 120, HY + 30, 0, HY + 70, 20) | seg(HX + 120, HY + 30, W, HY + 10, 20)
img[dirt] = DIRT[dirt]
e = dirt & ~ndimage.binary_erosion(dirt, iterations=2); img[e] *= .8
e = ndimage.binary_dilation(dirt, iterations=2) & ~dirt; img[e] = img[e] * .7 + np.array([52, 92, 40]) * .3
# ---------- the board: a raised stone platform
BX, BY, BW, BH, PW = 8, 152, 569, 418, 44; CW, CH = 66, 78; GX, GY = BX + (BW - 7 * CW) // 2, BY + (BH - 4 * CH) // 2
def rrect(x0, y0, x1, y1, r):
    cx = np.clip(xx, x0 + r, x1 - r); cy = np.clip(yy, y0 + r, y1 - r); return np.hypot(xx - cx, yy - cy) <= r
def down(m, n):
    o = np.zeros_like(m)
    for k in range(1, n + 1): o[k:] |= m[:-k]
    return o
def right(m, n):
    o = np.zeros_like(m)
    for k in range(1, n + 1): o[:, k:] |= m[:, :-k]
    return o
plat = rrect(BX, BY, BX + BW, BY + BH, 30); inner = rrect(BX + PW, BY + PW, BX + BW - PW, BY + BH - PW, 12); ring = plat & ~inner
ROAD = blocks(H, W, 15, 11, [(126, 132, 150), (112, 120, 140), (140, 144, 158), (118, 116, 132)], seed=3, moss=.05, mortar=(52, 52, 70))
FLOOR = blocks(H, W, 33, 26, [(226, 208, 170), (214, 196, 158), (234, 218, 184), (206, 188, 154)], seed=5, bond=False, lip=1, x0=-(GX % 33), y0=-(GY % 26), mortar=(150, 126, 104))
WALL = blocks(H, W, 17, 8, [(92, 96, 116), (82, 86, 106), (100, 100, 118)], seed=7, lip=0, mortar=(40, 38, 52), moss=.16)
KERB = blocks(H, W, 12, 30, [(176, 178, 190), (162, 166, 182)], seed=9, lip=0, mortar=(70, 70, 88))
# owner 2026-11-12 "เอาพื้นไปใส่สวยๆ" (the painted tile sheet, tools/art/floor_sheet.py): grey slab groups for the loop, warm slab
# groups for the dais (one group per half cell, so the joints follow the slots), each cut to few colours with more contrast
if os.environ.get('TEX', 'sheet') == 'sheet':
    import floor_sheet as FS
    def punch(a, k=1.28, lift=1.0, tint=(1, 1, 1)):
        m = a.reshape(-1, 3).mean(0); a = (m + (a - m) * k) * lift * np.array(tint)
        return np.asarray(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).quantize(14, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB')).astype(float)
    ROAD = punch(FS.patchwork(['f23', 'f29', 'f12'], W, H, 48, 44, x0=BX, y0=BY, seed=4), 1.3, .86, (.94, .97, 1.1))
    FLOOR = punch(FS.patchwork(['f34', 'f25', 'f8'], W, H, CW, CH // 2, x0=GX, y0=GY, seed=6), 1.25, 1.2, (1.04, 1.0, .9))
    WALL = punch(FS.mirror_tile(FS.px(FS.crop('road')), W, H), 1.2, .6, (.9, .92, 1.1))
    DIRT2 = punch(FS.mirror_tile(FS.px(FS.crop('dirt').crop((0, 0, 190, 60))), W, H), 1.0, 1.02); img[dirt & ndimage.binary_erosion(dirt, iterations=2)] = DIRT2[dirt & ndimage.binary_erosion(dirt, iterations=2)]
wall = down(plat, 13) & ~plat
sh = (down(right(plat | wall, 12), 12)) & ~plat & ~wall; img[sh] = img[sh] * np.array([.62, .68, .74])     # the platform's shadow on the grass
img[ring] = ROAD[ring]; img[inner] = FLOOR[inner]; img[wall] = WALL[wall]
kerb = plat & ~ndimage.binary_erosion(plat, iterations=5); img[kerb] = KERB[kerb]                           # a pale kerb round the edge
img[plat & ~ndimage.binary_erosion(plat, iterations=1)] = INK; img[kerb & ~ndimage.binary_erosion(kerb | ~plat, iterations=1) & ndimage.binary_erosion(plat, iterations=4)] *= .62
# the middle is a dais 5 px above the road: light top edge, a lip under its front edge, its shadow on the road
lipm = down(inner, 5) & ring; img[lipm] = np.array([168, 146, 118]); img[down(lipm, 1) & ring & ~lipm] = (60, 54, 66)
shd = down(right(inner | lipm, 5), 4) & ring & ~lipm; img[shd] *= .72
img[inner & ~ndimage.binary_erosion(inner, iterations=1)] = (120, 100, 86); img[inner & ~down(inner, 1) & ndimage.binary_erosion(inner | down(inner, 1), iterations=1)] = (250, 240, 214)
img[down(wall, 1) & ~wall & ~plat] = INK
base = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert('RGBA'); dr = ImageDraw.Draw(base)
# grass details: tufts and flower patches (not on stone or dirt)
solid = plat | wall | dirt
for _ in range(900):
    x, y = random.randrange(3, W - 3), random.randrange(110, H - 3)
    if solid[y, x]: continue
    dr.line((x, y, x, y - random.randint(2, 3)), fill=random.choice([(58, 122, 50), (130, 190, 84)]))
for _ in range(26):
    cx, cy = random.randrange(10, W - 10), random.randrange(600, 1120); col = random.choice([(255, 244, 150), (255, 170, 200), (255, 255, 255), (190, 170, 255)])
    for _ in range(random.randint(4, 8)):
        x, y = cx + random.randint(-12, 12), cy + random.randint(-8, 8)
        if 0 < x < W - 2 and not solid[y, x]: dr.rectangle((x, y, x + 1, y + 1), fill=col); dr.point((x, y + 2), fill=(50, 110, 46))
for _ in range(40):                                                   # pebbles on the dirt
    x, y = random.randrange(10, W - 10), random.randrange(820, 1120)
    if dirt[y, x]: dr.rectangle((x, y, x + 2, y + 1), fill=random.choice([(150, 128, 100), (196, 170, 130)])); dr.point((x + 1, y + 2), fill=(96, 74, 60))

# ---------- sprites drawn in code
def kennel():
    c = Image.new('RGBA', (140, 124)); d = ImageDraw.Draw(c)
    d.polygon([(98, 58), (124, 49), (124, 104), (98, 114)], fill=(140, 98, 66))                      # side wall
    for x in (106, 115): d.line((x, 58 - (x - 98) // 3, x, 113 - (x - 98) // 3), fill=(108, 74, 52))
    d.polygon([(18, 114), (18, 58), (58, 18), (98, 58), (98, 114)], fill=(206, 156, 98))            # front
    for i, x in enumerate(range(18, 98, 10)):
        if i % 2: d.rectangle((x, 20, x + 9, 114), fill=(192, 142, 88))
        d.line((x, 20, x, 114), fill=(138, 96, 62))
    d.polygon([(18, 58), (58, 18), (98, 58), (98, 0), (18, 0)], fill=(0, 0, 0, 0)); d.polygon([(19, 58), (58, 19), (97, 58)], fill=(214, 166, 106))
    for y in range(26, 58, 8): d.line((58 - (y - 19), y, 58 + (y - 19), y), fill=(168, 122, 78))
    d.rectangle((18, 58, 98, 64), fill=(150, 104, 68))                                               # the roof's shadow on the wall
    d.pieslice((40, 66, 76, 102), 180, 360, fill=(226, 184, 122)); d.rectangle((40, 84, 76, 114), fill=(226, 184, 122))   # door frame
    d.pieslice((44, 70, 72, 98), 180, 360, fill=(52, 36, 34)); d.rectangle((44, 84, 72, 114), fill=(52, 36, 34))
    d.polygon([(44, 114), (44, 92), (56, 114)], fill=(34, 24, 26))
    d.polygon([(58, 8), (86, 0), (134, 48), (106, 58)], fill=(176, 52, 46))                          # right roof plane
    for t in (.25, .5, .75):
        d.line((58 + 48 * t, 8 + 50 * t, 86 + 48 * t, 0 + 48 * t), fill=(132, 36, 40))
    for t, s in ((.12, 8), (.37, 18), (.62, 6), (.87, 16)): d.line((58 + 48 * t + s, 8 + 50 * t - s * .29, 58 + 48 * (t + .13) + s, 8 + 50 * (t + .13) - s * .29), fill=(132, 36, 40))
    d.line((58, 8, 86, 0), fill=(236, 110, 84), width=2)
    d.line((10, 62, 58, 12), fill=(214, 70, 56), width=7); d.line((58, 12, 106, 60), fill=(214, 70, 56), width=7)      # the roof's front edge
    d.line((11, 58, 57, 10), fill=(246, 132, 100), width=2); d.line((60, 16, 104, 60), fill=(150, 42, 44), width=2)
    bx, by = 58, 46; d.rectangle((bx - 9, by - 2, bx + 9, by + 2), fill=(250, 240, 214))             # bone sign
    for sx in (-10, 10):
        for sy in (-3, 3): d.ellipse((bx + sx - 3, by + sy - 3, bx + sx + 3, by + sy + 3), fill=(250, 240, 214))
    d.rectangle((14, 112, 100, 116), fill=(120, 84, 58))
    return Image.fromarray(outline(np.asarray(c), pale=999, black=INK).astype(np.uint8))
def flag(col=(64, 124, 226)):
    c = Image.new('RGBA', (34, 56)); d = ImageDraw.Draw(c)
    d.rectangle((3, 4, 5, 54), fill=(150, 108, 70)); d.rectangle((3, 4, 3, 54), fill=(196, 150, 100)); d.ellipse((1, 0, 7, 6), fill=(250, 214, 90))
    d.polygon([(6, 8), (31, 12), (24, 18), (31, 26), (6, 28)], fill=col); d.line((6, 9, 28, 12), fill=tuple(min(255, v + 50) for v in col))
    d.ellipse((12, 17, 18, 23), fill=(255, 255, 255))
    for px, py in ((11, 14), (14, 12), (18, 13)): d.rectangle((px, py, px + 1, py + 1), fill=(255, 255, 255))
    return Image.fromarray(outline(np.asarray(c), pale=999, black=INK).astype(np.uint8))
def bowl():
    c = Image.new('RGBA', (26, 16)); d = ImageDraw.Draw(c)
    d.polygon([(2, 5), (23, 5), (20, 14), (5, 14)], fill=(214, 70, 60)); d.ellipse((2, 1, 23, 9), fill=(150, 42, 44)); d.ellipse((4, 2, 21, 8), fill=(150, 98, 60))
    for px in (7, 11, 15, 17): d.point((px, 4 + px % 2), fill=(206, 150, 96))
    d.line((5, 11, 20, 11), fill=(250, 220, 200))
    return Image.fromarray(outline(np.asarray(c), pale=999, black=INK).astype(np.uint8))
def bone():
    c = Image.new('RGBA', (20, 10)); d = ImageDraw.Draw(c); d.rectangle((4, 4, 15, 5), fill=(250, 240, 214))
    for sx in (3, 15):
        for sy in (2, 6): d.ellipse((sx - 1, sy - 1, sx + 2, sy + 2), fill=(250, 240, 214))
    return Image.fromarray(outline(np.asarray(c), pale=999, black=INK).astype(np.uint8))
def star(n):
    c = Image.new('RGBA', (n * 11 + 1, 12)); d = ImageDraw.Draw(c)
    for i in range(n):
        x = i * 11 + 5; d.polygon([(x, 0), (x + 2, 3), (x + 5, 4), (x + 3, 7), (x + 3, 10), (x, 8), (x - 3, 10), (x - 3, 7), (x - 5, 4), (x - 2, 3)], fill=(255, 214, 64)); d.point((x - 1, 3), fill=(255, 250, 200))
    return Image.fromarray(outline(np.asarray(c), pale=999, black=INK).astype(np.uint8))

# ---------- slots: round stone pedestals with a paw
items = []      # (feet y, image, left x, cast a shadow?)
def put(im, fx_, fy_, sh=True, anchor=None):
    ax, ay, _ = anchor or feet(im); items.append((fy_, im, fx_ - ax, fy_ - ay, sh))
def pedestal(cx, cy, empty):
    rx, ry, t = 25, 11, 7
    dr.ellipse((cx - rx - 1, cy - ry + t - 1, cx + rx + 1, cy + ry + t + 1), fill=INK); dr.rectangle((cx - rx - 1, cy, cx + rx + 1, cy + t), fill=INK)
    dr.ellipse((cx - rx, cy - ry + t, cx + rx, cy + ry + t), fill=(120, 116, 132)); dr.rectangle((cx - rx, cy, cx + rx, cy + t), fill=(120, 116, 132))
    dr.rectangle((cx - rx, cy + 1, cx - rx + 5, cy + t + 3), fill=(146, 142, 156)); dr.rectangle((cx + rx - 9, cy + 1, cx + rx, cy + t + 2), fill=(96, 92, 112))
    dr.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(204, 204, 214), outline=INK); dr.arc((cx - rx + 2, cy - ry + 2, cx + rx - 2, cy + ry - 2), 150, 300, fill=(240, 240, 246))
    dr.arc((cx - rx + 2, cy - ry + 2, cx + rx - 2, cy + ry - 2), 330, 100, fill=(168, 168, 184))
    if empty:
        pc = (160, 162, 180); dr.ellipse((cx - 6, cy - 2, cx + 6, cy + 5), fill=pc)
        for px, py in ((-10, -3), (-4, -7), (3, -7), (9, -3)): dr.ellipse((cx + px - 2, cy + py - 1, cx + px + 2, cy + py + 2), fill=pc)
def rot(d_, s, v='south'): return crop(Image.open(DC + '%s/char/Idle/rotations/%s.png' % (d_, v)))
SHIBA = {1: 'pl1s', 2: 'pl2s', 3: 'pl3'}
def unit(kind, s, pose):
    """-> (image, anchor (x, y, top)) ; pose: idle | atk (a mid-attack frame, facing right)"""
    if kind == 'shiba':
        if pose == 'idle': im = rot(SHIBA[s], s); return im, feet(im)
        A = DC + SHIBA[s] + '/char/Idle/animations/attack_se/south-east/frame_%03d.png'; f0 = Image.open(A % 0).convert('RGBA'); f = Image.open(A % {1: 4, 2: 3, 3: 3}[s]).convert('RGBA')
        return f, feet(f0)
    idle = Image.open(DC + 'corgi/game/s%d_idle.png' % s).convert('RGBA')
    if pose == 'idle': return idle, feet(idle)
    st = Image.open(DC + 'corgi/game/s%d_attack.png' % s).convert('RGBA'); k = {1: 1, 2: 2, 3: 2}[s]; return st.crop((k * 104, 0, k * 104 + 104, 104)), feet(idle)
U = {(0, 0): ('shiba', 2, 'atkL'), (2, 0): ('corgi', 1, 'idle'), (3, 0): ('shiba', 3, 'idle'), (5, 0): ('corgi', 2, 'idle'),
     (1, 1): ('shiba', 1, 'idle'), (4, 1): ('shiba', 2, 'idle'), (6, 1): ('corgi', 3, 'atk'),
     (0, 2): ('corgi', 1, 'idleL'), (2, 2): ('shiba', 1, 'idle'), (3, 2): ('corgi', 2, 'idle'), (5, 2): ('shiba', 1, 'idle'),
     (1, 3): ('shiba', 2, 'idle'), (4, 3): ('corgi', 1, 'idle'), (6, 3): ('shiba', 3, 'atk')}
if BGM: U = {}
stars = []
for c in range(7):
    for r in range(4):
        cx, cy = GX + c * CW + CW // 2, GY + r * CH + CH - 22; pedestal(cx, cy, (c, r) not in U)
        if (c, r) in U:
            kind, s, pose = U[(c, r)]; im, an = unit(kind, s, pose.rstrip('L'))
            if pose.endswith('L'): im = flip(im); an = (im.width - 1 - an[0], an[1], an[2])
            put(im, cx, cy + 3, anchor=an); stars.append((cx, cy + 3 - (an[1] - an[2]) - 13, s))
# ---------- monsters on the loop
a_, b_, c_, d_ = BX + PW / 2, BY + PW / 2 + 2, BX + BW - PW / 2, BY + BH - PW / 2 + 2; per = 2 * (c_ - a_ + d_ - b_); LOOP = []
for s in np.linspace(0, per, 400, endpoint=False):
    if s < c_ - a_: LOOP.append((a_ + s, b_))
    elif s < c_ - a_ + d_ - b_: LOOP.append((c_, b_ + s - (c_ - a_)))
    elif s < 2 * (c_ - a_) + d_ - b_: LOOP.append((c_ - (s - (c_ - a_ + d_ - b_)), d_))
    else: LOOP.append((a_, d_ - (s - (2 * (c_ - a_) + d_ - b_))))
MOB = {}
for k, n in (('shroom', 2), ('wisp', 2), ('wolf', 2), ('kappa', 2), ('kasa_obake', 2), ('paper_doll', 2)):
    m = json.load(open('art/action/mobs_hr/%s.json' % k)); MOB[k] = crop(reduce(crop(Image.open('art/action/mobs_hr/%s.png' % k).crop((0, 0, m['w'], m['h']))), n))
for i in ([] if BGM else list(range(8, 400, 19))):
    if 318 < i < 345 or 96 < i < 112: continue                                        # room for the swoosh and the cannon blast
    px, py = LOOP[i]; nx, _ = LOOP[(i + 5) % 400]; im = MOB[random.choice(list(MOB))]; put(im if nx >= px else flip(im), int(px) + random.randint(-3, 3), int(py) + 12 + random.randint(-3, 3))
# flags on the two back corners, bench strip with three dogs waiting
put(flag(), BX + 30, BY + 22); put(flip(flag()), BX + BW - 30, BY + 22)
BN, BWd = 8, 60; bx0 = (W - BN * BWd) // 2; byy = 640
dr.rectangle((bx0 - 5, byy - 3, bx0 + BN * BWd + 4, byy + 51), fill=INK); dr.rectangle((bx0 - 4, byy + 40, bx0 + BN * BWd + 3, byy + 50), fill=(112, 76, 54))
for i in range(BN):
    x = bx0 + i * BWd; dr.rectangle((x, byy - 2, x + BWd - 2, byy + 39), fill=(196, 146, 94) if i % 2 else (184, 134, 84))
    for yv in (byy + 11, byy + 25): dr.line((x, yv, x + BWd - 2, yv), fill=(150, 104, 68))
    dr.line((x, byy - 2, x + BWd - 2, byy - 2), fill=(232, 190, 130)); dr.rectangle((x + BWd - 1, byy - 2, x + BWd - 1, byy + 39), fill=(110, 76, 54))
    dr.line((x, byy + 40, x + BWd - 2, byy + 40), fill=(150, 104, 68))
    for px in (x + 5, x + BWd - 8): dr.rectangle((px, byy + 3, px + 1, byy + 4), fill=(110, 76, 54))
for i, (kind, s) in (() if BGM else ((0, ('shiba', 1)), (1, ('shiba', 1)), (3, ('corgi', 1)))):
    im, an = unit(kind, s, 'idle'); cx = bx0 + i * BWd + BWd // 2 - 1; put(im, cx, byy + 30, anchor=an); stars.append((cx, byy + 30 - (an[1] - an[2]) - 13, s))
# ---------- the yard
# owner "เอาบ้านมาทำไม" + a painted swamp sheet "เอาไปตกแต่ง" (art/incoming/dogcat/swamp/, cut by swamp boxes): no dog house; the big old tree
# on its sandy mound is the yard's centrepiece, the lily ponds and moss lie on the grass (reduce() by whole numbers, 1 px ink line)
def swamp(n, k): return Image.fromarray(outline(np.asarray(crop(reduce(Image.open(DC + 'swamp/' + n + '.png'), k))), pale=999, black=INK).astype(np.uint8))
if HOUSE: put(kennel(), HX + 10, HY); put(flag(), HX - 62, HY - 6); put(bowl(), HX - 86, HY + 34, sh=False)
else:
    t_ = swamp('tree', 3); put(t_, HX, HY + 44, anchor=(t_.width // 2, t_.height - 30, 0))
    for n, k, x, y in (('lily_dark', 3, 452, 1096), ('pond_blue', 2, 96, 1066), ('moss', 2, 520, 962), ('lily_patch', 3, 150, 792), ('stump', 3, 60, 930), ('pond_rock', 2, 496, 846)):
        im = swamp(n, k); items.append((y - im.height // 2 - 400, im, x - im.width // 2, y - im.height, False))
YARD = [('trees_green_2', 2, 60, 870), ('trees_green_1', 2, 536, 800), ('trees_green_3', 2, 500, 1118), ('trees_green_2', 2, 70, 1180), ('trees_green_1', 2, 14, 1010),
        ('village_1', 2, 30, 742), ('village_1', 2, 82, 742), ('village_1', 2, 134, 742), ('village_1', 2, 452, 742), ('village_1', 2, 504, 742), ('village_1', 2, 556, 742),
        ('camp_1', 3, 408, 968), ('logs2_0', 3, 470, 990), ('logs2_1', 3, 372, 1012), ('camp_7', 3, 30, 836),
        ('village_3', 2, 330, 1090), ('village_4', 2, 236, 1070), ('camp_5', 2, 150, 1040),
        ('water_3', 3, 384, 1084), ('water_4', 3, 512, 1042), ('logs2_3', 3, 200, 1010), ('stones_9', 3, 566, 960), ('stones_1', 3, 24, 900),
        ('bushes_1', 3, 28, 772), ('bushes_3', 3, 176, 760), ('bushes_0', 3, 418, 764), ('bushes_5', 3, 562, 780), ('bushes_9', 3, 250, 1118), ('bushes_1', 3, 548, 870),
        ('bushes_6', 3, 204, 1004), ('bushes_10', 3, 40, 1090), ('bushes_3', 3, 350, 1124), ('bushes_0', 3, 30, 616), ('bushes_5', 3, 558, 620), ('bushes_1', 3, 300, 134), ('bushes_9', 3, 60, 138), ('bushes_3', 3, 520, 140)]
for n, k, x, y in YARD:
    im = prop(n, k); put(flip(im) if (x * 7 + y) % 3 == 0 else im, x, y, sh=not n.startswith('water'), anchor=(im.width // 2, im.height - 1 - (im.height // 3 if n.startswith('water_0') else 0), 0))
# ---------- shadows (sun from the upper left), then the sprites back to front
shm = np.zeros((H, W), bool)
for fy_, im, x0, y0, sh in items:
    if not sh: continue
    al = np.asarray(im)[..., 3] > 0; ax, ay, _ = feet(im); hh = al.shape[0]
    for r in range(min(ay + 1, hh)):
        dy = ay - r; ys = y0 + ay + int(dy * .16); xs = x0 + int(dy * .55)
        if 0 <= ys < H:
            lo, hi = max(0, xs), min(W, xs + al.shape[1])
            if hi > lo: shm[ys, lo:hi] |= al[r, lo - xs:hi - xs]
g = np.asarray(base).astype(float); g[shm, :3] *= np.array([.66, .7, .8]); base = Image.fromarray(g.astype(np.uint8))
for fy_, im, x0, y0, sh in sorted(items, key=lambda t: t[0]): base.alpha_composite(im, (x0, y0)) if x0 >= 0 and y0 >= 0 else base.alpha_composite(im.crop((max(0, -x0), max(0, -y0), im.width, im.height)), (max(0, x0), max(0, y0)))
for cx, ty, s in stars: st = star(s); base.alpha_composite(st, (cx - st.width // 2, max(0, ty)))
# light: warm upper left, cooler lower right, a soft vignette; butterflies
g = np.asarray(base).astype(float); t = (xx / W * .45 + yy / H * .55)[..., None]
g[..., :3] = g[..., :3] * (np.array([1.07, 1.05, .98]) * (1 - t) + np.array([.92, .95, 1.03]) * t)
v = np.hypot((xx - W / 2) / (W * .75), (yy - H / 2) / (H * .7))[..., None]; g[..., :3] *= 1 - np.clip(v - .55, 0, 1) * .35
base = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)); dr = ImageDraw.Draw(base)
for x, y, col in ((210, 700, (255, 255, 255)), (420, 720, (255, 236, 120)), (120, 1010, (255, 190, 220)), (540, 1000, (255, 255, 255))):
    dr.rectangle((x, y, x + 1, y + 1), fill=col); dr.rectangle((x + 3, y - 1, x + 4, y), fill=col); dr.point((x + 2, y + 1), fill=INK)
if BGM:
    os.makedirs('art/dogcat', exist_ok=True); base.convert('RGB').save('art/dogcat/bg.png')
    json.dump({'w': W, 'h': H, 'slots': [[GX + c * CW + CW // 2, GY + r * CH + CH - 19] for r in range(4) for c in range(7)], 'cols': 7, 'rows': 4, 'cw': CW, 'ch': CH,
               'loop': [a_, b_ + 12, c_, d_ + 12], 'bench': [[bx0 + i * BWd + BWd // 2 - 1, byy + 30] for i in range(BN)]}, open('art/dogcat/geo.json', 'w'))
    print('bg ok'); sys.exit()
# ---------- HUD
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 14); FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22); FS = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 11)
def panel(x0, y0, x1, y1, fill=(36, 30, 46)):
    dr.rounded_rectangle((x0, y0, x1, y1), 8, fill=INK); dr.rounded_rectangle((x0 + 2, y0 + 2, x1 - 2, y1 - 2), 7, fill=(246, 206, 110)); dr.rounded_rectangle((x0 + 4, y0 + 4, x1 - 4, y1 - 4), 5, fill=fill)
def coin(x, y, r=6):
    dr.ellipse((x - r - 1, y - r - 1, x + r + 1, y + r + 1), fill=INK); dr.ellipse((x - r, y - r, x + r, y + r), fill=(250, 200, 60)); dr.ellipse((x - r + 2, y - r + 2, x + 1, y + 1), fill=(255, 236, 140))
def txt(x, y, s, f=F, col=(250, 240, 214)): dr.text((x + 1, y + 1), s, fill=INK, font=f); dr.text((x, y), s, fill=col, font=f)
panel(8, 6, W - 8, 44); cat = crop(Image.open(DC + 'cat/char_s2/Idle/rotations/south.png')).crop((6, 0, 46, 30)); base.alpha_composite(cat, (16, 10))
txt(64, 16, 'CATS', F, (255, 190, 220)); txt(120, 16, 'monsters 31 / 100'); dr.rectangle((330, 20, 560, 30), fill=(70, 50, 60)); dr.rectangle((330, 20, 330 + int(230 * .31), 30), fill=(236, 110, 150))
panel(8, 48, W - 8, 104); txt(22, 62, 'WAVE 12', FB); txt(150, 68, '00:24', F, (255, 226, 150)); dg = crop(Image.open(DC + 'pl2s/char/Idle/rotations/south.png')).crop((6, 6, 48, 40)); base.alpha_composite(dg, (212, 58))
txt(262, 60, 'DOGS', F, (150, 200, 255)); txt(318, 60, 'monsters 47 / 100'); dr.rectangle((262, 82, 560, 92), fill=(70, 50, 60)); dr.rectangle((262, 82, 262 + int(298 * .47), 92), fill=(236, 84, 84))
panel(4, 1124, W - 4, H - 4)
for i, (t, cst, col) in enumerate((('REROLL', 2, (98, 170, 240)), ('LEVEL UP', 4, (250, 196, 70)))):
    y = 1136 + i * 60; dr.rounded_rectangle((14, y, 102, y + 50), 6, fill=INK); dr.rounded_rectangle((16, y + 2, 100, y + 44), 5, fill=col); dr.rounded_rectangle((16, y + 2, 100, y + 8), 5, fill=tuple(min(255, v + 40) for v in col))
    dr.text((22, y + 10), t, fill=INK, font=FS); coin(30, y + 33, 5); dr.text((40, y + 26), str(cst), fill=INK, font=F)
SHOP = [('shiba', 1, 'SHIBA', 1, (150, 158, 172)), ('corgi', 1, 'CORGI', 2, (104, 190, 120)), ('shiba', 1, 'SHIBA', 1, (150, 158, 172)), ('corgi', 1, 'CORGI', 2, (104, 190, 120)), ('shiba', 1, 'SHIBA', 1, (150, 158, 172))]
for i, (kind, s, nm, cst, col) in enumerate(SHOP):
    x = 110 + i * 93; dr.rounded_rectangle((x, 1136, x + 87, 1250), 6, fill=INK); dr.rounded_rectangle((x + 2, 1138, x + 85, 1248), 5, fill=col)
    dr.rounded_rectangle((x + 5, 1141, x + 82, 1218), 4, fill=(232, 222, 196)); dr.rectangle((x + 5, 1196, x + 82, 1218), fill=(150, 196, 110))
    im, an = unit(kind, s, 'idle'); im = im.crop((max(0, an[0] - 38), max(0, an[2] - 4), an[0] + 38, an[1] + 2)); base.alpha_composite(im, (x + 44 - im.width // 2, 1214 - im.height))
    dr.text((x + 7, 1226), nm, fill=INK, font=FS); coin(x + 66, 1234, 5); dr.text((x + 74, 1226), str(cst), fill=INK, font=F)
panel(W - 118, 1088, W - 6, 1122); coin(W - 100, 1105, 7); txt(W - 86, 1096, '14', F, (255, 226, 150)); txt(W - 58, 1096, 'Lv 5', F)
base.resize((W * 2, H * 2), Image.NEAREST).save(DC + 'tw_scene.png'); print('ok', len(items))
