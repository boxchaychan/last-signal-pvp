# Map mock v2 (owner 2026-11-11 "แมพเรียบแบบนี้ไม่ได้ มันมีสูงต่ำ"): free, no new jobs. Ground from the PixelLab tile textures but
# laid by smooth pixel masks (no stair-step road), raised plateaus with code-drawn cliff faces (rock texture from the cliff set,
# shaded, top rim, dark foot), a stone ramp, scattered tufts / leaves / pebbles, props and characters at the 64 size.
#   python3 tools/art/td_scene2.py -> art/td/mock_map2.png
import json, math, random, sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, 'tools/art'); from px_smooth import smooth_up; from vivid import vivid
random.seed(3); np.random.seed(3)
VW, VH = 844, 390; D = 'art/td/tiles/'
def tex(k, lower):
    m = json.load(open(D + k + '_meta.json'))['tileset_data']['tiles']; im = Image.open(D + k + '.png').convert('RGB')
    for t in m:
        if all((t['corners'][q] == 'lower') == lower for q in t['corners']):
            b = t['bounding_box']; return im.crop((b['x'], b['y'], b['x'] + 32, b['y'] + 32))
def tile_fill(t):
    out = Image.new('RGB', (VW, VH))
    for y in range(0, VH, 32):
        for x in range(0, VW, 32): out.paste(t.transpose(random.choice([Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM, Image.ROTATE_180])) if random.random() < .5 else t, (x, y))
    return np.asarray(out).astype(float)
GRASS = tile_fill(tex('path_pro', False)); DIRT = tile_fill(tex('path_pro', True)); WATER = tile_fill(tex('river', True)); ROCK = tile_fill(tex('cliff', True))
yy, xx = np.mgrid[0:VH, 0:VW]
noise = np.asarray(Image.fromarray((np.random.rand(VH // 8 + 1, VW // 8 + 1) * 255).astype(np.uint8)).resize((VW, VH), Image.BICUBIC)).astype(float) / 255
def band(pts, w):                                      # distance to a smooth polyline < w (+ wobble)
    d = np.full((VH, VW), 1e9)
    P = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        for s in np.linspace(0, 1, 30): P.append((x0 + (x1 - x0) * s, y0 + (y1 - y0) * s))
    for x, y in P: d = np.minimum(d, np.hypot(xx - x, (yy - y) * 1.15))
    return d < w + (noise - .5) * 10
def blob(cx, cy, rx, ry, wob=.18):
    a = np.arctan2(yy - cy, xx - cx); r = np.hypot((xx - cx) / rx, (yy - cy) / ry)
    return r < 1 + wob * np.sin(a * 3 + cx) + wob * .6 * np.sin(a * 5 + cy) + (noise - .5) * .12
def outline(m):
    e = m & ~np.asarray(Image.fromarray(m.astype(np.uint8) * 255).filter(ImageFilter.MinFilter(3))).astype(bool); return e
img = GRASS.copy()
# road
road = band([(-20, 330), (120, 300), (260, 268), (360, 262), (470, 262), (560, 250), (660, 214), (760, 196), (870, 190)], 22)
dark = np.array([70, 110, 40]); img[road] = DIRT[road]
rim = outline(road) | outline(np.asarray(Image.fromarray(road.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(3))).astype(bool))
img[rim & ~road] = img[rim & ~road] * .7 + dark * .3
# pond with muddy bank
pond = blob(760, 350, 120, 60); bank = np.asarray(Image.fromarray(pond.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(11))).astype(bool)
img[bank & ~pond] = np.array([116, 82, 52]) + (noise[bank & ~pond, None] - .5) * 30
img[pond] = WATER[pond]; img[outline(pond)] = np.array([210, 240, 255])
# plateaus (raised ground): footprint at ground level, drawn DH higher, cliff face below
DH = 34
def plateau(mask):
    up = np.zeros_like(mask); up[:-DH] = mask[DH:]                               # the top surface, shifted up
    span = np.zeros_like(mask)
    for k in range(DH + 1): sh = np.zeros_like(mask); sh[:VH - k] = mask[k:]; span |= sh
    face = span & ~up
    # foot shadow on the ground
    foot = np.asarray(Image.fromarray(mask.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(9))).astype(bool) & ~span
    img[foot] *= .72
    depth = np.zeros((VH, VW))
    for k in range(DH + 1): sh = np.zeros_like(mask); sh[:VH - k] = mask[k:]; depth[sh & face & (depth == 0)] = k + 1
    sh_k = np.clip(1 - (DH - depth) / DH * .55, .45, 1)[..., None]               # darker toward the foot
    img[face] = (ROCK[face] * .9 + np.array([90, 62, 40]) * .1) * sh_k[face]
    lines = face & ((yy + (xx // 9) * 3) % 11 == 0); img[lines] *= .7               # rock strata
    img[up] = GRASS[up] * 1.06
    e = outline(up); img[e] = np.array([150, 205, 90])                            # sunlit rim
    fe = outline(span) & ~up; img[fe] = np.array([40, 26, 20])                     # dark outline round the face
    # rounded earth boulders along the top of the face (the reference's cliff rim)
    ys, xs = np.nonzero(fe)
    order = np.argsort(xs); last = -99
    for i in order[::1]:
        x, y = xs[i], ys[i]
        if x - last < 11: continue
        last = x; r = random.randint(7, 10); cy = y - DH + random.randint(4, 10)
        if cy < 0 or not up[min(VH - 1, cy - 2), x]: continue
        BOULDERS.append((x, cy, r))
    return up
BOULDERS = []
up1 = plateau(blob(150, 140, 170, 70)); up2 = plateau(blob(640, 75, 230, 70))
# a stone ramp up to the left plateau
ramp = (xx > 250) & (xx < 300) & (yy > 168) & (yy < 214)
for i, y0 in enumerate(range(172, 214, 7)):
    st = ramp & (yy >= y0) & (yy < y0 + 7); img[st] = np.array([150, 140, 125]) * (1 - .05 * i); img[st & (yy == y0)] = np.array([200, 192, 176])
img = np.clip(img, 0, 255).astype(np.uint8); base = Image.fromarray(img).convert('RGBA'); d = ImageDraw.Draw(base)
for x, y, r in BOULDERS:
    d.ellipse((x - r, y - r + 3, x + r, y + r + 6), fill=(46, 30, 22))
    d.ellipse((x - r, y - r, x + r, y + r), fill=(120, 76, 46)); d.ellipse((x - r + 2, y - r + 1, x + r - 4, y + r - 5), fill=(150, 98, 58))
    d.ellipse((x - r + 4, y - r + 2, x, y - 1), fill=(176, 122, 76))
# scatter: tufts, leaves, pebbles (not on road / water / cliff faces)
okg = ~road & ~bank
for _ in range(420):
    x, y = random.randrange(4, VW - 4), random.randrange(4, VH - 4)
    if not okg[y, x]: continue
    r = random.random()
    if r < .55:
        c = random.choice([(46, 112, 40), (120, 190, 70), (70, 150, 52)])
        for dx in (-2, 0, 2): d.line((x + dx, y, x + dx + random.choice((-1, 0, 1)), y - random.randint(3, 6)), fill=c)
    elif r < .8:
        d.rectangle((x, y, x + 1, y + 1), fill=random.choice([(200, 70, 40), (230, 140, 50), (180, 50, 40)]))
    else:
        d.ellipse((x, y, x + 3, y + 2), fill=(150, 145, 135)); d.point((x + 1, y), fill=(200, 196, 188))
# props + characters
HERO = 50
def fit(f, h):
    im = Image.open(f).convert('RGBA'); im = im.crop(im.getbbox()); k = h / im.height
    if k >= 1: return smooth_up(im, k)
    s = im.resize((max(1, round(im.width * k)), h), Image.LANCZOS); a = np.asarray(s).copy(); a[..., 3] = (a[..., 3] > 110) * 255; return Image.fromarray(a)
items = []
def put(f, h, x, y, flip=False):
    im = fit(f, h); im = im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im; items.append((y, im, x - im.width // 2))
F = 'art/side/forest/'
put('art/side/map30/tree.png', int(HERO * 4.6), 90, 140); put('art/side/map30/tree.png', int(HERO * 4.2), 560, 70, True)
put(F + 'small_tree.png', int(HERO * 2.2), 790, 90); put(F + 'small_tree.png', int(HERO * 2), 360, 385, True)
put(F + 'bush.png', int(HERO * 1.0), 230, 120); put(F + 'bush.png', int(HERO * .9), 480, 380, True); put(F + 'bush.png', int(HERO * .9), 700, 60)
put(F + 'rocks.png', int(HERO * .7), 640, 330)
put('art/td/props/rock0.png', int(HERO * 3.2), 330, 215); put('art/td/props/rock1.png', int(HERO * 2.6), 700, 300); put('art/td/props/rock3.png', int(HERO * 1.8), 520, 385); put(F + 'flowers.png', int(HERO * .4), 150, 330)
M = json.load(open('art/action/n128/berserker.json')); C = M['cell']
hero = Image.open('art/action/n128/berserker_still.png').crop((C, 0, 2 * C, C)); hero = hero.crop(hero.getbbox())
k = HERO / hero.height; hero = hero.resize((round(hero.width * k), HERO), Image.LANCZOS); ha = np.asarray(hero).copy(); ha[..., 3] = (ha[..., 3] > 110) * 255
items.append((280, Image.fromarray(ha), 410 - hero.width // 2))
for kk, h, x, y in (('wolf', int(HERO * .7), 520, 270), ('shroom', int(HERO * .5), 470, 320), ('skeleton', int(HERO * .95), 610, 252), ('boar_guard', int(HERO * 1.2), 160, 150)):
    mm = json.load(open('art/action/mobs_hr/%s.json' % kk)); im = Image.open('art/action/mobs_hr/%s.png' % kk).crop((0, 0, mm['w'], mm['h'])); im = im.crop(im.getbbox())
    k2 = h / im.height; s = im.resize((round(im.width * k2), h), Image.LANCZOS).transpose(Image.FLIP_LEFT_RIGHT); a = np.asarray(s).copy(); a[..., 3] = (a[..., 3] > 110) * 255
    items.append((y, Image.fromarray(a), x - s.width // 2))
sh = Image.new('RGBA', base.size); sd = ImageDraw.Draw(sh)
for y, im, x in items: sd.ellipse((x + im.width * .18, y - 5, x + im.width * .82, y + 4), fill=(0, 0, 0, 85))
base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(1.5)))
for y, im, x in sorted(items, key=lambda t: t[0]): base.alpha_composite(im, (int(x), int(y - im.height)))
a = np.asarray(base).astype(float); g = a[..., :3].mean(2, keepdims=True)
a[..., :3] = g + (a[..., :3] - g) * .78; a[..., 0] *= 1.04; a[..., 2] *= .86; a[..., :3] = a[..., :3] * .92 + 8
vig = np.clip(1.15 - np.hypot((xx - VW / 2) / VW, (yy - VH / 2) / VH) * 1.1, .55, 1)[..., None]; a[..., :3] *= vig
base = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
crown = fit('art/side/map30/tree.png', 260).crop((0, 0, 400, 130)); cr = np.asarray(crown).copy(); cr[..., :3] = (cr[..., :3] * .55).astype(np.uint8); crown = Image.fromarray(cr)
for cx in (-40, 210): base.alpha_composite(crown, (cx, VH - 70))
o = ImageDraw.Draw(base); o.ellipse((470, 248, 560, 284), outline=(255, 80, 60, 220), width=2)
base.resize((VW * 3, VH * 3), Image.NEAREST).convert('RGB').save(__import__('os').environ.get('OUT','art/td/mock_map2.png')); print('ok')
