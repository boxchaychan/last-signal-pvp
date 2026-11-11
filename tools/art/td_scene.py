# Top-down map + hero proportion mock (owner 2026-11-11 "ลองจำลองแมพละตัวละครมา ... เจนพื้น PixelLab อนุญาต 20 เครดิต"):
# PixelLab Wang tilesets (art/td/tiles: path_pro = grass/dirt (pro), river = grass/water, cliff = grass/rock, autumn = leaves/dirt;
# in every set the feature is the LOWER terrain) autotiled from vertex masks, the grass of the other sets colour-matched to the
# pro grass, our PixelLab props and the Berserker at the chosen size (64 canvas, figure ~50) on an 844x390 view, x3 for a phone.
#   python3 tools/art/td_scene.py -> art/td/mock_map.png
import json, math, random, sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, 'tools/art'); from px_smooth import smooth_up; from vivid import vivid
T = 32; W, H = 27, 13; VW, VH = W * T - 20, H * T - 26          # 844 x 390 view
D = 'art/td/tiles/'; random.seed(7)
def load(k):
    im = Image.open(D + k + '.png').convert('RGBA'); m = json.load(open(D + k + '_meta.json'))['tileset_data']['tiles']
    lut = {}
    for t in m:
        c = t['corners']; b = t['bounding_box']; key = tuple(c[q] == 'lower' for q in ('NW', 'NE', 'SW', 'SE'))
        lut.setdefault(key, []).append(im.crop((b['x'], b['y'], b['x'] + b['width'], b['y'] + b['height'])))
    return lut
def grass_px(lut):
    a = np.asarray(lut[(False,) * 4][0]).astype(float); return a[..., :3].reshape(-1, 3)
SETS = {k: load(k) for k in ('path_pro', 'river', 'cliff', 'autumn')}
ref = grass_px(SETS['path_pro']); rm, rs = ref.mean(0), ref.std(0) + 1
def match(lut, src_feature_dark=False):   # move this set's grass colours onto the pro grass
    g = grass_px(lut); gm, gs = g.mean(0), g.std(0) + 1
    out = {}
    for key, tiles in lut.items():
        nt = []
        for t in tiles:
            a = np.asarray(t).astype(float); rgb = a[..., :3]
            d = np.linalg.norm(rgb - gm, axis=-1); w = np.clip(1.6 - d / 55, 0, 1)[..., None]   # how grass-like a pixel is
            mapped = (rgb - gm) / gs * rs + rm
            a[..., :3] = np.clip(rgb * (1 - w) + mapped * w, 0, 255); nt.append(Image.fromarray(a.astype(np.uint8)))
        out[key] = nt
    return out
for k in ('river', 'cliff'): SETS[k] = match(SETS[k])
# vertex masks (W+1 x H+1): which feature sits on each vertex
V = np.zeros((H + 1, W + 1), 'U5'); V[:] = 'g'
def blob(cx, cy, rx, ry, tag):
    for y in range(H + 1):
        for x in range(W + 1):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 < 1 + .25 * math.sin(x * 1.3 + y): V[y, x] = tag
pts = [(0, 9.6), (4, 9.0), (8, 8.2), (11, 7.2), (14, 7.0), (17, 7.4), (20, 6.6), (24, 5.6), (28, 5.2)]           # dirt road
for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
    for s in np.linspace(0, 1, 40):
        x, y = x0 + (x1 - x0) * s, y0 + (y1 - y0) * s
        for yy in range(H + 1):
            for xx in range(W + 1):
                if (yy - y) ** 2 / 1.3 + (xx - x) ** 2 / 1.0 < 1: V[yy, xx] = 'd'
blob(23.5, 11.6, 3.6, 1.8, 'w')                                                   # pond / stream bend bottom right
blob(9.5, 2.2, 2.2, 1.4, 'r')                                                        # rocky patch top left
blob(19, 1.4, 2.6, 1.3, 'r')
SET_OF = {'d': 'path_pro', 'w': 'river', 'r': 'cliff'}
img = Image.new('RGBA', (W * T, H * T))
for y in range(H):
    for x in range(W):
        c = [V[y, x], V[y, x + 1], V[y + 1, x], V[y + 1, x + 1]]; feat = [t for t in c if t != 'g']
        tag = max(set(feat), key=feat.count) if feat else 'd'
        lut = SETS[SET_OF[tag]]; key = tuple(t == tag for t in c)
        img.alpha_composite(random.choice(lut[key]), (x * T, y * T))
img = img.crop((10, 13, 10 + VW, 13 + VH))
# props and characters (foot y in view px)
def fit(f, h):
    im = Image.open(f).convert('RGBA'); im = im.crop(im.getbbox()); k = h / im.height
    if k >= 1: return smooth_up(im, k)
    s = im.resize((max(1, round(im.width * k)), h), Image.LANCZOS); a = np.asarray(s).copy(); a[..., 3] = (a[..., 3] > 110) * 255
    return Image.fromarray(a)
HERO = 50
items = []
def put(f, h, x, y, flip=False):
    im = fit(f, h); im = im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im; items.append((y, im, x - im.width // 2))
F = 'art/side/forest/'
put('art/side/map30/tree.png', int(HERO * 4.6), 120, 150); put('art/side/map30/tree.png', int(HERO * 4.2), 640, 175, True)
put(F + 'small_tree.png', int(HERO * 2.3), 820, 260); put(F + 'small_tree.png', int(HERO * 2), 330, 380, True)
put(F + 'bush.png', int(HERO * 1.1), 260, 170); put(F + 'bush.png', int(HERO * .9), 470, 365, True); put(F + 'bush.png', int(HERO * 1), 820, 120)
put(F + 'rocks.png', int(HERO * .8), 700, 330); put(F + 'fence.png', int(HERO * .8), 560, 300); put(F + 'sign.png', int(HERO * 1.1), 300, 250)
put(F + 'flowers.png', int(HERO * .45), 200, 330); put(F + 'flowers.png', int(HERO * .4), 560, 170, True)
M = json.load(open('art/action/n128/berserker.json')); C = M['cell']
hero = Image.open('art/action/n128/berserker_still.png').crop((C, 0, 2 * C, C)); hero = hero.crop(hero.getbbox())
k = HERO / hero.height; hero = hero.resize((round(hero.width * k), HERO), Image.LANCZOS); ha = np.asarray(hero).copy(); ha[..., 3] = (ha[..., 3] > 110) * 255
items.append((262, Image.fromarray(ha), 420 - hero.width // 2))
for kk, h, x, y in (('wolf', int(HERO * .7), 520, 250), ('shroom', int(HERO * .5), 470, 300), ('skeleton', int(HERO * .95), 600, 236), ('boar_guard', int(HERO * 1.2), 350, 210)):
    mm = json.load(open('art/action/mobs_hr/%s.json' % kk)); im = Image.open('art/action/mobs_hr/%s.png' % kk).crop((0, 0, mm['w'], mm['h'])); im = im.crop(im.getbbox())
    kk2 = h / im.height; s = im.resize((round(im.width * kk2), h), Image.LANCZOS).transpose(Image.FLIP_LEFT_RIGHT); a = np.asarray(s).copy(); a[..., 3] = (a[..., 3] > 110) * 255
    items.append((y, Image.fromarray(a), x - s.width // 2))
sh = Image.new('RGBA', img.size); sd = ImageDraw.Draw(sh)
for y, im, x in items: sd.ellipse((x + im.width * .18, y - 5, x + im.width * .82, y + 4), fill=(0, 0, 0, 80))
img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(1.5)))
for y, im, x in sorted(items, key=lambda t: t[0]): img.alpha_composite(im, (int(x), int(y - im.height)))
# HUD hints: bars, ground-target circle in front of the hero
ov = Image.new('RGBA', img.size); o = ImageDraw.Draw(ov)
o.ellipse((470, 226, 560, 262), outline=(255, 80, 60, 200), width=2); o.ellipse((474, 228, 556, 260), fill=(255, 60, 40, 40))
o.rectangle((8, VH - 18, 170, VH - 10), fill=(196, 30, 42, 255)); o.rectangle((178, VH - 18, 300, VH - 10), fill=(30, 86, 196, 255))
img = vivid(img, .6); img.alpha_composite(ov)
img.resize((VW * 3, VH * 3), Image.NEAREST).convert('RGB').save('art/td/mock_map.png')
tiles = Image.new('RGBA', (4 * 128 + 30, 128), (40, 40, 40, 255))
for i, kk in enumerate(['path_pro', 'cliff', 'river', 'autumn']): tiles.alpha_composite(Image.open(D + kk + '.png').convert('RGBA'), (i * 138, 0))
tiles.resize((tiles.width * 2, tiles.height * 2), Image.NEAREST).save('art/td/tiles_sheets_x2.png'); print('ok', img.size)
