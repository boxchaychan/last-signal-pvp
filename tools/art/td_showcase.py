# Two hand-composed showcase scenes with props set 2 (owner 2026-11-12 "ประกอบมาให้ดูหน่อยขอสวยๆ"): free, no new jobs.
# A = a green forest camp by a pond at dusk light, B = an autumn river with a bridge and ruins. Same scale as the maps (hero 50 px).
#   python3 tools/art/td_showcase.py -> art/td/showcase_a.png, showcase_b.png (x2)
import json, math, random, sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
sys.path.insert(0, 'tools/art'); from px_smooth import smooth_up
W, H = 900, 420; D = 'art/td/tiles/'; P2 = 'art/td/props/set2/cut/'
yy, xx = np.mgrid[0:H, 0:W]

def tex(k, lower):
    m = json.load(open(D + k + '_meta.json'))['tileset_data']['tiles']; im = Image.open(D + k + '.png').convert('RGB')
    for t in m:
        if all((t['corners'][q] == 'lower') == lower for q in t['corners']):
            b = t['bounding_box']; return im.crop((b['x'], b['y'], b['x'] + 32, b['y'] + 32))
def tile_fill(t):
    out = Image.new('RGB', (W, H))
    for y in range(0, H, 32):
        for x in range(0, W, 32): out.paste(t.transpose(random.choice([Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM, Image.ROTATE_180])) if random.random() < .5 else t, (x, y))
    return np.asarray(out).astype(float)
def noise(cell):
    n = np.random.rand(H // cell + 2, W // cell + 2)
    return np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize(((W // cell + 2) * cell, (H // cell + 2) * cell), Image.BICUBIC)).astype(float)[:H, :W] / 255
def band(pts, w, N):
    P = []; pp = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(pp) - 2):
        p0, p1, p2, p3 = [np.array(p, float) for p in pp[i - 1:i + 3]]
        for t in np.linspace(0, 1, 40): P.append(.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    line = np.zeros((H, W), bool)
    for x, y in P:
        if 0 <= int(y) < H and 0 <= int(x) < W: line[int(y), int(x)] = True
    return ndimage.distance_transform_edt(~line) < w + (N - .5) * 8
def blob(cx, cy, rx, ry, N, wob=.14):
    a = np.arctan2(yy - cy, xx - cx); r = np.hypot((xx - cx) / rx, (yy - cy) / ry)
    return r < 1 + wob * np.sin(a * 3 + cx) + wob * .6 * np.sin(a * 5 + cy) + (N - .5) * .1
dil = lambda m, r: ndimage.binary_dilation(m, iterations=r)
edge = lambda m: m & ~ndimage.binary_erosion(m)
def grade(a):
    a = a.astype(float); c = a[..., :3]; g = c.mean(2, keepdims=True); o = g + (c - g) * .72
    gr = np.clip((o[..., 1] - np.maximum(o[..., 0], o[..., 2])) / 50, 0, 1); o[..., 0] += gr * 26; o[..., 1] -= gr * 5; o[..., 2] -= gr * 4
    o[..., 0] *= 1.03; o[..., 2] *= .9; o = o * .93 + 8; a[..., :3] = o; return np.clip(a, 0, 255).astype(np.uint8)
def fit(f, h, flip=False):
    im = Image.open(f).convert('RGBA'); im = im.crop(im.getbbox()); k = h / im.height
    im = smooth_up(im, k) if k >= 1 else im.resize((max(1, round(im.width * k)), h), Image.LANCZOS)
    a = np.asarray(im).copy(); a[..., 3] = (a[..., 3] > 110) * 255; im = Image.fromarray(grade(a))
    return im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im
def autumn(im, seed):
    a = np.asarray(im.convert('RGBA')).copy(); h, w = a.shape[:2]; rs = np.random.RandomState(seed)
    hsv = np.asarray(Image.fromarray(a[..., :3]).convert('HSV')).astype(float)
    n = np.asarray(Image.fromarray((rs.rand(h // 14 + 2, w // 14 + 2) * 255).astype(np.uint8)).resize((w // 14 * 14 + 28, h // 14 * 14 + 28), Image.BICUBIC)).astype(float)[:h, :w] / 255
    g = (hsv[..., 0] > 40) & (hsv[..., 0] < 130) & (hsv[..., 1] > 50) & (a[..., 3] > 0)
    hsv[..., 0] = np.where(g, 2 + n * 24, hsv[..., 0]); hsv[..., 1] = np.where(g, np.minimum(255, hsv[..., 1] * 1.45 + 20), hsv[..., 1])
    a[..., :3] = np.asarray(Image.fromarray(hsv.astype(np.uint8), 'HSV').convert('RGB')); return Image.fromarray(a)

def scene(name, seed, autumnal):
    random.seed(seed); np.random.seed(seed)
    N8, N40, N90 = noise(8), noise(40), noise(90); BY = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])[yy % 4, xx % 4] / 16
    G = tile_fill(tex('path_pro', False)); DR = tile_fill(tex('autumn' if autumnal else 'path_pro', True)); WA = tile_fill(tex('river', True))
    img = G.copy()
    if autumnal: L = tile_fill(tex('autumn', False)); lf = N90 * .6 + N40 * .4 + (BY - .5) * .1; img[lf > .44] = L[lf > .44]
    lv = N90 * .7 + N40 * .3 + (BY - .5) * .08; img[lv < .34] *= .87; lt = lv > .66; img[lt] = img[lt] * 1.07 + np.array([10, 6, -6])
    items = []; glows = []
    def put(f, h, x, y, flip=None, aut=False, over=False):
        im = fit(f, h, random.random() < .5 if flip is None else flip)
        if aut: im = autumn(im, int(x + y))
        items.append((y, im, x - im.width // 2, over))
    if not autumnal:
        road = band([(-20, 400), (180, 360), (380, 345), (560, 350), (740, 330), (920, 300)], 22, N8)
        pond = blob(760, 205, 105, 44, N8); bank = dil(pond, 5)
        img[road] = DR[road]; rim = edge(dil(road, 2)) & ~road; img[rim] = img[rim] * .72 + np.array([60, 96, 36]) * .28
        img[bank & ~pond] = np.array([112, 80, 52]) + (N8[bank & ~pond, None] - .5) * 28; img[pond] = WA[pond]
        img[ndimage.binary_erosion(pond, iterations=12)] *= .82; img[edge(pond)] = [210, 236, 248]
        img[(np.hypot(xx - 330, (yy - 250) * 1.6) < 95) & (N8 > .35)] *= .93          # trodden ground round the camp
        # back row of forest, framing trees
        for x in range(-30, W + 60, 105): put('art/side/map30/tree.png', random.randint(210, 250), x + random.randint(-15, 15), random.randint(40, 75))
        put(P2 + 'trees_green_0.png', 235, 95, 300, False); put(P2 + 'trees_green_1.png', 230, 545, 150); put(P2 + 'trees_green_3.png', 205, 880, 255, True)
        put(P2 + 'trees_green_2.png', 205, 640, 130, False); put('art/side/forest/small_tree.png', 105, 210, 150)
        # the camp
        put(P2 + 'camp_0.png', 92, 300, 222, False); put(P2 + 'camp_1.png', 48, 372, 262); glows.append((372, 248, 70, (255, 150, 60)))
        put(P2 + 'camp_2.png', 40, 238, 238); put(P2 + 'camp_5.png', 44, 226, 268); put(P2 + 'camp_8.png', 36, 270, 280)
        put(P2 + 'village_8.png', 38, 430, 300, True); put(P2 + 'logs2_0.png', 42, 330, 300)
        put(P2 + 'village_4.png', 86, 470, 338, False); glows.append((478, 268, 46, (255, 210, 120)))
        put(P2 + 'village_4.png', 86, 690, 318, True); glows.append((682, 248, 46, (255, 210, 120)))
        put(P2 + 'village_3.png', 54, 150, 372); put(P2 + 'village_7.png', 40, 600, 262)
        put(P2 + 'village_5.png', 88, 470, 210)
        # ruins at the back, the pond
        put(P2 + 'ruins_0.png', 96, 430, 135); put(P2 + 'ruins_8.png', 100, 740, 118)
        for x, y, k in ((730, 205, 'water_0'), (800, 215, 'water_1'), (772, 186, 'water_0')): put(P2 + k + '.png', 40, x, y)
        for x, y, k in ((672, 214, 'water_2'), (850, 196, 'water_4'), (700, 246, 'water_3')): put(P2 + k + '.png', 52, x, y)
        # ground clutter
        for x, y, k, h in ((40, 205, 'bushes_1', 46), (175, 300, 'bushes_6', 46), (520, 230, 'bushes_2', 44), (620, 300, 'bushes_9', 34), (860, 360, 'bushes_0', 46),
                           (560, 390, 'stones_0', 32), (110, 240, 'stones_8', 28), (790, 380, 'stones_12', 34), (24, 330, 'logs2_1', 48), (280, 380, 'bushes_10', 40),
                           (560, 300, 'logs2_3', 40), (395, 175, 'bushes_7', 40), (880, 160, 'bushes_4', 44)): put(P2 + k + '.png', h, x, y)
        hero = (395, 300, False); mobs = [('wolf', .72, 640, 362, -1), ('wolf', .72, 700, 384, -1), ('wolf', .72, 600, 404, -1)]
    else:
        river = band([(560, -20), (548, 120), (515, 230), (528, 330), (500, 440)], 36, N8)
        road = band([(-20, 300), (180, 285), (360, 255), (470, 240), (600, 235), (760, 205), (920, 190)], 20, N8)
        deck = (xx > 466) & (xx < 590) & (yy > 214) & (yy < 262)
        bank = dil(river, 6); img[road & ~river] = DR[road & ~river]
        img[bank & ~river] = np.array([118, 86, 56]) + (N8[bank & ~river, None] - .5) * 28; img[river] = WA[river]
        img[ndimage.binary_erosion(river, iterations=10)] *= .8; img[edge(river)] = [206, 230, 240]
        for x in range(467, 590):
            for y in range(214, 262):
                c = np.array([150, 104, 62]) if (x - 467) % 10 else np.array([84, 56, 34])
                if y < 219 or y > 256: c = np.array([96, 64, 38]) if y in (214, 215, 260, 261) else np.array([132, 92, 54])
                img[y, x] = c
        for x in range(-30, W + 60, 105): put('art/side/map30/tree.png', random.randint(210, 250), x + random.randint(-15, 15), random.randint(40, 75), aut=True)
        put(P2 + 'trees_autumn_0.png', 235, 120, 250, False); put(P2 + 'trees_autumn_1.png', 225, 330, 150); put(P2 + 'trees_autumn_2.png', 220, 760, 150, True)
        put(P2 + 'trees_autumn_3.png', 190, 860, 370, True)
        put(P2 + 'ruins_1.png', 140, 680, 280, False); put(P2 + 'ruins_7.png', 70, 610, 360); put(P2 + 'ruins_5.png', 72, 760, 330, True)
        put(P2 + 'ruins_6.png', 100, 255, 345); put(P2 + 'ruins_8.png', 104, 420, 150)
        put(P2 + 'water_8.png', 60, 530, 360, False);
        for x, y, k in ((555, 120, 'water_3'), (488, 300, 'water_2'), (470, 410, 'water_5')): put(P2 + k + '.png', 52, x, y)
        put(P2 + 'logs2_3.png', 42, 300, 230); put(P2 + 'logs2_0.png', 46, 180, 330); put(P2 + 'logs2_2.png', 48, 60, 380)
        put(P2 + 'village_4.png', 86, 420, 230, False); glows.append((428, 160, 46, (255, 210, 120)))
        put(P2 + 'camp_1.png', 44, 820, 250); glows.append((820, 238, 64, (255, 150, 60)))
        for x, y, k, h in ((40, 230, 'bushes_2', 44), (210, 400, 'bushes_1', 46), (380, 330, 'bushes_6', 44), (640, 230, 'stones_0', 30), (880, 255, 'bushes_9', 34),
                           (720, 395, 'stones_11', 30), (320, 395, 'bushes_10', 38), (100, 170, 'stones_8', 28)): put(P2 + k + '.png', h, x, y, aut=k.startswith('bushes'))
        hero = (520, 245, False); mobs = [('skeleton', .98, 640, 300, -1), ('skeleton', .98, 700, 330, -1), ('skeleton', .98, 610, 330, -1)]
    # shadows, then sprites back to front, hero and monsters
    base = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert('RGBA')
    sh = Image.new('RGBA', base.size); sd = ImageDraw.Draw(sh)
    for y, im, x, o in items:
        w = im.width
        if im.height > 140: sd.ellipse((x + w * .12, y - w * .14, x + w * 1.02, y + w * .1), fill=(10, 20, 6, 70))
        else: sd.ellipse((x + w * .08, y - 6, x + w * .98, y + 6), fill=(10, 20, 6, 80))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)))
    M = json.load(open('art/action/n128/berserker.json')); C = M['cell']; hk = 50 / (147 - 38)
    hst = Image.open('art/action/n128/berserker_still.png').crop((C, 0, 2 * C, C)); hst = hst.crop(hst.getbbox()); hst = hst.resize((round(hst.width * hk), 50), Image.LANCZOS)
    ha = np.asarray(hst).copy(); ha[..., 3] = (ha[..., 3] > 110) * 255; hst = Image.fromarray(ha)
    items.append((hero[1], hst, hero[0] - hst.width // 2, False))
    for k, s, x, y, face in mobs:
        mm = json.load(open('art/action/mobs_hr/%s.json' % k)); im = Image.open('art/action/mobs_hr/%s.png' % k).crop((0, 0, mm['w'], mm['h'])); im = im.crop(im.getbbox())
        kk = 50 * s / im.height; im = im.resize((round(im.width * kk), round(im.height * kk)), Image.LANCZOS); a = np.asarray(im).copy(); a[..., 3] = (a[..., 3] > 110) * 255
        im = Image.fromarray(a); im = im.transpose(Image.FLIP_LEFT_RIGHT) if face < 0 else im; items.append((y, im, x - im.width // 2, False))
    s2 = Image.new('RGBA', base.size); d2 = ImageDraw.Draw(s2)
    for y, im, x, o in items[-1 - len(mobs):]: d2.ellipse((x + im.width * .15, y - 4, x + im.width * .85, y + 4), fill=(0, 0, 0, 90))
    base.alpha_composite(s2.filter(ImageFilter.GaussianBlur(1.5)))
    for y, im, x, o in sorted(items, key=lambda t: t[0]): base.alpha_composite(im, (int(x), int(y - im.height)))
    # light: warm glows (fire, lamps), a soft late-afternoon tint, vignette, dark crowns in the foreground
    a = np.asarray(base).astype(float)
    for gx, gy, r, c in glows:
        g = np.clip(1 - np.hypot(xx - gx, (yy - gy) * 1.3) / r, 0, 1) ** 2 * .55; a[..., :3] += g[..., None] * np.array(c) * .6
    tint = np.array([1.04, 1.0, .9]) if not autumnal else np.array([1.05, .98, .88]); a[..., :3] *= tint
    vig = np.clip(1.15 - np.hypot((xx - W / 2) / W, (yy - H / 2) / H) * 1.05, .5, 1); a[..., :3] *= vig[..., None]
    base = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    cr = fit('art/side/map30/tree.png', 300).crop((0, 0, 420, 140)); cr = autumn(cr, 5) if autumnal else cr
    c2 = np.asarray(cr).copy(); c2[..., :3] = (c2[..., :3] * .42).astype(np.uint8); cr = Image.fromarray(c2)
    base.alpha_composite(cr, (-120, H - 62)); base.alpha_composite(cr.transpose(Image.FLIP_LEFT_RIGHT), (W - 300, H - 54))
    base.resize((W * 2, H * 2), Image.NEAREST).convert('RGB').save('art/td/showcase_%s.png' % name); print(name, 'ok')

scene('a', 11, False); scene('b', 23, True)
