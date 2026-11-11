# Walkable map 1 (owner 2026-11-11 "แมพเอาให้เสร็จก่อน1แมพละฉันจะลองเดินดู"): the mock_map2 look as a full map for map.html.
# Free (no new PixelLab jobs): ground from the PixelLab tile textures laid by smooth masks with big grass patches, raised
# plateaus with code-drawn cliffs (rounded boulders on the rim, stone stairs up), a pond, the 4 big rocks (moss added),
# trees / bushes round the edges, an olive grade like Dimraeth. 1 map px = 1 screen px on a landscape phone (hero 50 px).
#   python3 tools/art/td_map.py -> art/td/map1/{ground.png, props.png, block.png, hero_*.png, mob_*.png, map.json}
#   MAP=td2 python3 tools/art/td_map.py -> art/td/map2/ (owner 2026-11-12 "ทำแมพรอไปก่อน": an autumn forest with a river and a
#   bridge, east of map 1; `exits` / `entries` in map.json join the two maps)
import json, math, os, random, sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
sys.path.insert(0, 'tools/art'); from px_smooth import smooth_up
random.seed(7); np.random.seed(7)
W, H = 1800, 1100; DH = 62; HERO = 50
MAPID = os.environ.get('MAP', 'td1'); T2 = MAPID == 'td2'
OUT = 'art/td/map2/' if T2 else 'art/td/map1/'; os.makedirs(OUT, exist_ok=True); D = 'art/td/tiles/'
yy, xx = np.mgrid[0:H, 0:W]

def tex(k, lower):
    m = json.load(open(D + k + '_meta.json'))['tileset_data']['tiles']; im = Image.open(D + k + '.png').convert('RGB')
    for t in m:
        if all((t['corners'][q] == 'lower') == lower for q in t['corners']):
            b = t['bounding_box']; return im.crop((b['x'], b['y'], b['x'] + 32, b['y'] + 32))
def tile_fill(t):
    out = Image.new('RGB', (W, H))
    for y in range(0, H, 32):
        for x in range(0, W, 32):
            out.paste(t.transpose(random.choice([Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM, Image.ROTATE_180])) if random.random() < .5 else t, (x, y))
    return np.asarray(out).astype(float)
GRASS = tile_fill(tex('path_pro', False)); DIRT = tile_fill(tex('autumn' if T2 else 'path_pro', True)); LEAF = tile_fill(tex('autumn', False)) if T2 else None; WATER = tile_fill(tex('river', True)); ROCK = tile_fill(tex('cliff', True))
def noise(cell):
    n = np.random.rand(H // cell + 2, W // cell + 2)
    return np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize(((W // cell + 2) * cell, (H // cell + 2) * cell), Image.BICUBIC)).astype(float)[:H, :W] / 255
N8, N40, N90 = noise(8), noise(40), noise(90)
BAY = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16
BY = BAY[yy % 4, xx % 4]
def dil(m, r): return ndimage.binary_dilation(m, iterations=r)
def edge(m): return m & ~ndimage.binary_erosion(m)
def band(pts, w):                       # smooth road: distance to a Catmull-Rom curve through pts < w (+ wobble)
    P = []
    pp = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(pp) - 2):
        p0, p1, p2, p3 = [np.array(p, float) for p in pp[i - 1:i + 3]]
        for t in np.linspace(0, 1, 40):
            P.append(.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    line = np.zeros((H, W), bool)
    for x, y in P:
        if 0 <= int(y) < H and 0 <= int(x) < W: line[int(y), int(x)] = True
    d = ndimage.distance_transform_edt(~line)
    return d < w + (N8 - .5) * 8 + (N40 - .5) * 8
def blob(cx, cy, rx, ry, wob=.16):
    a = np.arctan2(yy - cy, xx - cx); r = np.hypot((xx - cx) / rx, (yy - cy) / ry)
    return r < 1 + wob * np.sin(a * 3 + cx) + wob * .6 * np.sin(a * 5 + cy) + (N8 - .5) * .1

# ---- ground: grass with big light / dark patches (stepped, dithered at the edges), a few bare dirt patches
img = GRASS.copy()
if T2:   # map 2: carpets of fallen red / orange leaves over the grass, dithered edges
    lf = N90 * .6 + N40 * .4 + (BY - .5) * .1; img[lf > .45] = LEAF[lf > .45]; mix = (lf > .38) & (lf <= .45); img[mix] = img[mix] * .5 + LEAF[mix] * .5
lv = N90 * .7 + N40 * .3 + (BY - .5) * .08
img[lv < .36] *= .86; img[lv < .28] *= .9                                # darker, cooler patches
lt = lv > .66; img[lt] = img[lt] * 1.08 + np.array([10, 6, -6])         # sunny, yellowish patches
bare = (N40 > .86) & (N90 > .5) & (N8 + BY * .5 > .7)
img[bare] = img[bare] * .55 + DIRT[bare] * .45
# ---- road (Catmull-Rom) with a dark grass rim
ROADS = [[(-30, 720), (180, 700), (380, 660), (540, 590), (640, 470), (660, 380)],
         [(540, 600), (760, 650), (980, 720), (1180, 700), (1330, 640), (1400, 600)],
         [(1180, 700), (1420, 780), (1640, 800), (1840, 770)]]
if T2: ROADS = [[(-30, 770), (200, 745), (420, 695), (640, 645), (900, 625), (1120, 592), (1340, 520), (1490, 470), (1525, 372)],
                [(1120, 592), (1260, 740), (1500, 850), (1720, 900)]]
road = np.zeros((H, W), bool)
for r in ROADS: road |= band(r, 24)
img[road] = DIRT[road]
rim = edge(dil(road, 2)) & ~road; img[rim] = img[rim] * .7 + np.array([60, 96, 36]) * .3
if not T2:
    # ---- pond with a muddy bank and foam
    pond = blob(1080, 950, 190, 80); bank = dil(pond, 6)
    img[bank & ~pond] = np.array([112, 80, 52]) + (N8[bank & ~pond, None] - .5) * 30
    img[pond] = WATER[pond]; deep = ndimage.binary_erosion(pond, iterations=14); img[deep] *= .82
    img[edge(pond)] = np.array([210, 236, 250])
else:   # a river from the top to the bottom with a wooden bridge where the road crosses
    river = band([(870, -40), (850, 200), (800, 420), (825, 640), (780, 860), (805, 1140)], 40)
    deck = (xx > 742) & (xx < 892) & (yy > 600) & (yy < 654)
    bank = dil(river, 7); pond = river & ~deck
    img[bank & ~river] = np.array([118, 86, 56]) + (N8[bank & ~river, None] - .5) * 30
    img[river] = WATER[river]; deep = ndimage.binary_erosion(river, iterations=12); img[deep] *= .8
    img[edge(river)] = np.array([206, 230, 240])
    for x in range(744, 891):                                   # planks across, darker gaps, rails top and bottom
        for y in range(600, 655):
            c = np.array([150, 104, 62]) if (x - 744) % 10 else np.array([84, 56, 34])
            if y < 606 or y > 648: c = np.array([96, 64, 38]) if y in (600, 601, 653, 654) else np.array([132, 92, 54])
            img[y, x] = c * (0.94 + .06 * ((x * 7 + y * 3) % 5) / 4)
    RAIL = deck & ((yy < 606) | (yy > 648))
# ---- plateaus: footprint at ground level, top drawn DH higher, cliff face below
BOULDERS = []; UP = np.zeros((H, W), bool); FACE = np.zeros((H, W), bool); RAMP = np.zeros((H, W), bool)
def shift_up(m, k):
    o = np.zeros_like(m); o[:H - k] = m[k:]; return o
def plateau(mask, ramps):
    global UP, FACE
    up = shift_up(mask, DH); span = np.zeros_like(mask); depth = np.zeros((H, W))
    for k in range(DH + 1):
        sh = shift_up(mask, k); depth[sh & ~span] = k; span |= sh
    face = span & ~up
    foot = dil(mask, 5) & ~span; img[foot] *= .7                                   # dark shadow at the foot
    sh_k = np.clip(.55 + depth / DH * .5, .5, 1.05)[..., None]                      # darker toward the foot
    img[face] = (ROCK[face] * .62 + np.array([112, 78, 50]) * .38) * sh_k[face]
    vs = face & ((xx * 7 + (yy // 5) * 3) % 13 == 0) & (N8 > .4); img[vs] *= .72  # vertical cracks
    st = face & ((yy + (xx // 11) * 4) % 12 == 0); img[st] *= .8                   # strata
    roots = face & (N8 > .82) & (depth > DH * .55); img[roots] = np.array([70, 52, 34])
    img[up] = GRASS[up] * 1.04 + np.array([4, 4, 0])
    img[edge(up)] = np.array([150, 196, 92])                                        # sunlit rim
    img[edge(span) & ~up] = np.array([38, 26, 20])                                  # dark outline round the face
    # rounded boulders along the rim (columns: the first face pixel under the top)
    cols = np.where(face.any(0))[0]; last = -99
    for x in cols:
        if x - last < random.randint(9, 14): continue
        ys = np.nonzero(face[:, x])[0]
        if ys.size == 0: continue
        y0 = ys[0]
        if y0 < 4 or not up[y0 - 1, x] or ys[-1] - y0 < DH * .5 or not (up[y0 - 1, max(0, x - 4)] and up[y0 - 1, min(W - 1, x + 4)]): continue
        last = x; BOULDERS.append((x, y0 + random.randint(1, 4), random.randint(6, 10)))
    for x0, x1 in ramps:                                                            # stone stairs over the face
        for x in range(x0, x1):
            ys = np.nonzero(face[:, x])[0]
            if ys.size: RAMP[max(0, ys[0] - 3):ys[-1] + 3, x] = True
    UP |= up; FACE |= face
    return up
if T2: plateau(blob(1470, 220, 300, 96), [(1500, 1556)])
else:
    plateau(yy < 300 + 55 * np.sin(xx / 240) + 26 * np.sin(xx / 93 + 1) + (N40 - .5) * 30, [(632, 690)])
    plateau(blob(1460, 560, 200, 84), [(1380, 1430)])
# ---- stairs
for x in range(W):
    ys = np.nonzero(RAMP[:, x])[0]
    if not ys.size: continue
    left = not RAMP[:, x - 1].any(); right = not RAMP[:, min(W - 1, x + 1)].any()
    for y in ys:
        i = (y - ys[0]) // 7; c = np.array([150, 132, 108]) * (1 - .025 * i)
        if (y - ys[0]) % 7 == 0: c = np.array([196, 178, 146])
        if (x * 5 + i * 17) % 23 == 0: c = c * .7
        elif (y - ys[0]) % 7 == 6: c = np.array([96, 86, 76])
        img[y, x] = c
    if left or right: img[ys, x] = np.array([60, 46, 36])
img = np.clip(img, 0, 255)

# ---- props (sprites placed by their feet)
def fit(f, h, flip=False):
    im = Image.open(f).convert('RGBA'); im = im.crop(im.getbbox()); k = h / im.height
    if k >= 1: im = smooth_up(im, k)
    else: im = im.resize((max(1, round(im.width * k)), h), Image.LANCZOS)
    a = np.asarray(im).copy(); a[..., 3] = (a[..., 3] > 110) * 255
    im = Image.fromarray(a); return im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im
def mossify(im, seed):
    a = np.asarray(im).astype(float).copy(); h, w = a.shape[:2]; rs = np.random.RandomState(seed)
    n = np.asarray(Image.fromarray((rs.rand(h // 10 + 2, w // 10 + 2) * 255).astype(np.uint8)).resize((w // 10 * 10 + 20, h // 10 * 10 + 20), Image.BICUBIC)).astype(float)[:h, :w] / 255
    L = a[..., :3].mean(2); al = a[..., 3] > 0
    above = np.zeros_like(al); above[3:] = al[:-3]
    top = al & (L > np.percentile(L[al], 55))                                        # lit, upward-facing stone
    yy2 = np.mgrid[0:h, 0:w][0] / h
    m1 = top & (n + (1 - yy2) * .1 > .8) & (rs.rand(h, w) < .6); m2 = m1 & (n > .86)
    a[m1, :3] = a[m1, :3] * .5 + np.array([88, 112, 52]) * .5
    a[m2, :3] = a[m2, :3] * .4 + np.array([132, 160, 70]) * .6
    a[..., :3] *= (1.06 - yy2 * .22)[..., None]                                      # lighter top, darker foot
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
def autumn(im, seed):            # green leaves -> red / orange / yellow patches (the trunks and the rest stay)
    a = np.asarray(im.convert('RGBA')).copy(); h, w = a.shape[:2]; rs = np.random.RandomState(seed)
    hsv = np.asarray(Image.fromarray(a[..., :3]).convert('HSV')).astype(float)
    n = np.asarray(Image.fromarray((rs.rand(h // 14 + 2, w // 14 + 2) * 255).astype(np.uint8)).resize((w // 14 * 14 + 28, h // 14 * 14 + 28), Image.BICUBIC)).astype(float)[:h, :w] / 255
    g = (hsv[..., 0] > 40) & (hsv[..., 0] < 130) & (hsv[..., 1] > 50) & (a[..., 3] > 0)
    hsv[..., 0] = np.where(g, 2 + n * 24, hsv[..., 0]); hsv[..., 1] = np.where(g, np.minimum(255, hsv[..., 1] * 1.45 + 20), hsv[..., 1])
    hsv[..., 2] = np.where(g, np.minimum(255, hsv[..., 2] * 1.08 + 6), hsv[..., 2])
    rgb = np.asarray(Image.fromarray(hsv.astype(np.uint8), 'HSV').convert('RGB')); a[..., :3] = rgb; return Image.fromarray(a)
SPR = {}; PROPS = []
def sprite(key, f, h, flip=False, moss=False):
    k = (key, h, flip)
    if k not in SPR:
        im = fit(f, h, flip)
        if T2 and key.split('art/')[0] in ('tree', 'stree', 'bush'): im = autumn(im, len(SPR))
        if moss: im = mossify(im, len(SPR))
        SPR[k] = im
    return k
FP = {'tree': (.17, 11, 6), 'stree': (.14, 6, 3), 'bush': (.34, .16, 0), 'rock': (.42, .17, .12), 'pebble': (.36, .22, 0),
      'fence': (.46, 4, 0), 'sign': (.12, 3, 0), 'flowers': None, 'crown': None}
FR = 'art/side/forest/'
def put(kind, f, h, x, y, flip=False, moss=False, over=False):
    PROPS.append({'s': sprite(kind + f, f, h, flip, moss), 'x': x, 'y': y, 'kind': kind, 'over': over})
TREE = 'art/side/map30/tree.png'
if not T2:
    # forest along the top plateau, the left / right edges
    for x in range(-40, W + 60, 150):
        put('tree', TREE, random.randint(220, 270), x + random.randint(-30, 30), random.randint(110, 170), random.random() < .5)
    for x in range(60, W - 60, 230):
        if random.random() < .7: put('stree', FR + 'small_tree.png', random.randint(95, 120), x + random.randint(-40, 40), random.randint(205, 235), random.random() < .5)
    for y in range(390, H + 40, 150):
        put('tree', TREE, random.randint(220, 260), random.randint(-30, 30), y + random.randint(-20, 20), random.random() < .5)
        put('tree', TREE, random.randint(220, 260), W + random.randint(-30, 30), y + random.randint(-20, 20), random.random() < .5)
    # trees and bushes inside
    for x, y, h in ((300, 470, 240), (820, 560, 230), (1250, 420, 200), (1700, 640, 230), (470, 900, 240), (1440, 960, 220), (1660, 520, 210)):
        put('tree', TREE, h, x, y, random.random() < .5)
    for x, y in ((150, 560), (430, 520), (700, 420), (1020, 600), (1130, 480), (600, 780), (900, 850), (1300, 900), (1580, 700), (360, 820), (1700, 950), (230, 1010)):
        put('bush', FR + 'bush.png', random.randint(42, 52), x, y, random.random() < .5)
    for x, y in ((520, 740), (800, 1010), (1350, 520), (1560, 500), (180, 880)):
        put('stree', FR + 'small_tree.png', random.randint(100, 115), x, y, random.random() < .5)
    # the 4 big PixelLab rocks (Dimraeth size: ~4x the hero) + small rock piles
    for f, h, x, y, fl in (('rock0', 210, 1000, 470, False), ('rock1', 180, 260, 980, True), ('rock2', 150, 760, 900, False), ('rock3', 120, 1560, 560, False),
                           ('rock3', 110, 420, 240, True), ('rock1', 150, 1200, 260, False)):
        put('rock', 'art/td/props/%s.png' % f, h, x, y, fl, moss=True)
    for x, y in ((660, 700), (1240, 820), (90, 760), (1500, 860), (880, 300)):
        put('pebble', FR + 'rocks.png', random.randint(30, 38), x, y, random.random() < .5, moss=True)
    for x, y in ((240, 640), (690, 990), (1150, 560), (1620, 900), (980, 820), (350, 300)):
        put('flowers', FR + 'flowers.png', 20, x, y, random.random() < .5)
    put('sign', FR + 'sign.png', 42, 330, 650); put('fence', FR + 'fence.png', 34, 440, 600); put('fence', FR + 'fence.png', 34, 485, 576)
else:
    for x in range(-40, W + 60, 140):
        put('tree', TREE, random.randint(220, 270), x + random.randint(-30, 30), random.randint(100, 150), random.random() < .5)
    for y in range(330, H + 40, 150):
        for X in (random.randint(-30, 30), W + random.randint(-30, 30)):
            yy0 = y + random.randint(-20, 20)
            if abs(yy0 - 790) > 60: put('tree', TREE, random.randint(220, 260), X, yy0, random.random() < .5)   # the road gaps at both edges
    taken = dil(road, 26) | dil(bank, 20) | dil(FACE | RAMP, 14) | (yy < 230)
    def spot(n, gap, cb):
        P = []
        for _ in range(4000):
            if len(P) >= n: break
            x, y = random.randrange(90, W - 90), random.randrange(240, H - 60)
            if taken[y, x] or any(math.hypot(x - a, y - b) < gap for a, b in P + SPOTS): continue
            P.append((x, y)); cb(x, y)
        SPOTS.extend(P)
    SPOTS = [(980, 470), (300, 900), (1500, 880), (1320, 330)]   # kept open for the camps
    spot(9, 150, lambda x, y: put('tree', TREE, random.randint(200, 245), x, y, random.random() < .5))
    spot(6, 110, lambda x, y: put('stree', FR + 'small_tree.png', random.randint(100, 118), x, y, random.random() < .5))
    for f, h in (('rock0', 200), ('rock2', 150), ('rock1', 160), ('rock3', 115)):
        spot(1, 200, lambda x, y: put('rock', 'art/td/props/%s.png' % f, h, x, y, random.random() < .5, moss=True))
    spot(14, 80, lambda x, y: put('bush', FR + 'bush.png', random.randint(42, 52), x, y, random.random() < .5))
    spot(6, 70, lambda x, y: put('pebble', FR + 'rocks.png', random.randint(30, 38), x, y, random.random() < .5, moss=True))
    spot(5, 60, lambda x, y: put('flowers', FR + 'flowers.png', 20, x, y, random.random() < .5))
    put('sign', FR + 'sign.png', 42, 150, 700); put('fence', FR + 'fence.png', 34, 700, 590); put('fence', FR + 'fence.png', 34, 930, 580)
# ---- props set 2 (PixelLab 2026-11-12, 12 gen; cut by tools/art/props_cut.py into art/td/props/set2/cut/): more trees, a camp,
# village bits along the road, ruins on the plateau, logs and stumps, bushes, stones, water plants (owner "ทำฉากให้สวย")
P2 = 'art/td/props/set2/cut/'
FP.update({'tree2': (.16, 10, 6), 'solid': (.4, .16, .1), 'small': (.3, .2, 0), 'flat': None, 'water': None})
OCC = dil(road, 26) | dil(bank, 18) | dil(FACE | RAMP, 14) | (yy < 230)
NEAR = dil(road, 62) & ~dil(road, 30) & ~dil(bank, 10) & ~dil(FACE | RAMP, 10)
TAKEN = [(p['x'], p['y'], 0) for p in PROPS]; GID = [0]
def spot2(n, gap, cb, where=None, own=60):   # gap = between the pieces of this call, own = from everything else
    GID[0] += 1; g = GID[0]; got = 0
    for _ in range(8000):
        if got >= n: break
        x, y = random.randrange(80, W - 80), random.randrange(240, H - 60)
        if (where is not None and not where[y, x]) or (where is None and OCC[y, x]): continue
        if any(math.hypot(x - a, (y - b) * 1.4) < (gap if r == g else own) for a, b, r in TAKEN): continue
        cb(x, y); TAKEN.append((x, y, g)); got += 1
    if got < n: print('  only', got, 'of', n)
def P(kind, name, h, x, y): put(kind, P2 + name + '.png', h, x, y, random.random() < .5)
def camp(x, y):
    for kind, name, h, dx, dy in (('solid', 'camp_0', 95, 0, 0), ('small', 'camp_1', 50, 85, 34), ('small', 'camp_2', 44, -78, 22), ('small', 'camp_5', 48, -46, 62), ('small', 'camp_8', 40, 40, 74)):
        if not OCC[min(H - 1, y + dy), min(W - 1, x + dx)]: P(kind, name, h, x + dx, y + dy)
    TAKEN.append((x, y, -1))
pondI = ndimage.binary_erosion(pond, iterations=18)
if not T2:
    spot2(5, 170, lambda x, y: P('tree2', random.choice(['trees_green_0', 'trees_green_1', 'trees_green_2', 'trees_green_3']), random.randint(210, 250), x, y))
    spot2(1, 300, camp, None, 130)
    spot2(3, 260, lambda x, y: P('small', 'village_4', 88, x, y), NEAR)          # lamp posts by the road
    spot2(1, 200, lambda x, y: P('solid', 'village_5', 92, x, y), NEAR)          # a well
    spot2(2, 200, lambda x, y: P('small', 'village_7', 44, x, y), NEAR)          # hay
    spot2(1, 200, lambda x, y: P('small', 'village_8', 40, x, y), NEAR)          # a bench
    spot2(4, 120, lambda x, y: P('solid', random.choice(['ruins_0', 'ruins_2', 'ruins_8', 'ruins_4']), random.randint(80, 115), x, y), UP & (yy > 150) & ~dil(FACE, 30))
else:
    spot2(6, 170, lambda x, y: P('tree2', random.choice(['trees_autumn_0', 'trees_autumn_1', 'trees_autumn_2', 'trees_autumn_3']), random.randint(210, 250), x, y))
    spot2(1, 300, camp, None, 130)
    spot2(2, 260, lambda x, y: P('small', 'village_4', 88, x, y), NEAR)
    spot2(1, 200, lambda x, y: P('small', 'village_3', 58, x, y), NEAR)          # a signpost
    spot2(5, 160, lambda x, y: P('solid', random.choice(['ruins_0', 'ruins_1', 'ruins_6', 'ruins_7', 'ruins_8', 'ruins_5']), random.randint(85, 140), x, y))
    spot2(2, 120, lambda x, y: P('solid', random.choice(['ruins_0', 'ruins_8']), random.randint(90, 115), x, y), UP & (yy > 150) & ~dil(FACE, 30))
spot2(6, 130, lambda x, y: P('small', random.choice(['logs2_0', 'logs2_1', 'logs2_2', 'logs2_3', 'logs2_4', 'logs2_5']), random.randint(46, 62), x, y))
spot2(10, 90, lambda x, y: P('bush', random.choice(['bushes_%d' % i for i in range(11)]), random.randint(36, 52), x, y))
spot2(7, 80, lambda x, y: P('small', random.choice(['stones_%d' % i for i in (0, 1, 2, 4, 5, 8, 9, 10, 11, 12)]), random.randint(22, 40), x, y))
WATERP = pondI if not T2 else ndimage.binary_erosion(river, iterations=10) & ~dil(deck, 40)
spot2(4 if not T2 else 3, 70, lambda x, y: P('water', random.choice(['water_0', 'water_1']), random.randint(40, 52), x, y), WATERP, 40)
spot2(5, 70, lambda x, y: P('water', random.choice(['water_2', 'water_3', 'water_4', 'water_5']), random.randint(52, 64), x, y), edge(pond) & ~dil(deck if T2 else np.zeros_like(pond), 30), 40)
if T2: spot2(1, 200, lambda x, y: P('water', 'water_8', 64, x, y), WATERP, 40)        # a rowing boat on the river
# dark tree crowns hanging over the bottom edge (drawn over everything)
cr = fit(TREE, 300).crop((0, 0, 420, 140)); cr = autumn(cr, 99) if T2 else cr; ca = np.asarray(cr).copy(); ca[..., :3] = (ca[..., :3] * .5).astype(np.uint8); SPR[('crown', 0, 0)] = Image.fromarray(ca)
SPR[('crown', 0, 1)] = SPR[('crown', 0, 0)].transpose(Image.FLIP_LEFT_RIGHT)
for i, x in enumerate(range(-60, W + 100, 330)):
    PROPS.append({'s': ('crown', 0, i % 2), 'x': x + random.randint(-30, 30), 'y': H + 70, 'kind': 'crown', 'over': True})

# ---- prop shadows baked into the ground (to the lower right), collision footprints
blk = np.zeros((H, W), bool)
sh = np.ones((H, W))
for p in PROPS:
    im = SPR[p['s']]; w, h = im.size; x, y = p['x'], p['y']
    if p['kind'] in ('crown', 'flowers', 'flat', 'water'): continue
    if p['kind'] in ('tree', 'stree', 'tree2'):
        e = ((xx - x - w * .1) / (w * .42)) ** 2 + ((yy - y + 6) / (w * .17)) ** 2 < 1
    else:
        e = ((xx - x - w * .06) / (w * .5)) ** 2 + ((yy - y + h * .08) / (h * .16 + 3)) ** 2 < 1
    sh[e] = np.minimum(sh[e], .7)
    fp = FP[p['kind']]
    if fp:
        rx = fp[0] * w; ry = fp[1] * h if fp[1] < 1 else fp[1]; oy = fp[2] * h if fp[2] < 1 else fp[2]
        blk |= ((xx - x) / rx) ** 2 + ((yy - y + oy) / ry) ** 2 < 1
soft = sh < 1; ring = edge(soft) & (BY > .5); sh[ring] = .85
img *= sh[..., None]
base = Image.fromarray(img.astype(np.uint8)).convert('RGBA'); dr = ImageDraw.Draw(base)
for x, y, r in BOULDERS:
    dr.ellipse((x - r - 1, y - r + 2, x + r + 1, y + r + 4), fill=(40, 28, 22))
    dr.ellipse((x - r, y - r, x + r, y + r), fill=(118, 80, 52)); dr.ellipse((x - r + 2, y - r + 1, x + r - 3, y + r - 4), fill=(146, 102, 66))
    dr.ellipse((x - r + 3, y - r + 2, x - 1, y - 2), fill=(172, 128, 84))
    if random.random() < .5: dr.line((x - r + 2, y - r + 1, x + 2, y - r), fill=(110, 150, 66), width=2)
# scatter: tufts, leaves, pebbles (not on road / water / faces / stairs)
okg = ~road & ~bank & ~FACE & ~RAMP & ~blk
for _ in range(3200):
    x, y = random.randrange(4, W - 4), random.randrange(8, H - 4)
    if not okg[y, x]: continue
    r = random.random()
    if r < .55:
        c = random.choice([(46, 108, 40), (118, 176, 70), (72, 144, 52)])
        for dx in (-2, 0, 2): dr.line((x + dx, y, x + dx + random.choice((-1, 0, 1)), y - random.randint(3, 6)), fill=c)
    elif r < .78: dr.rectangle((x, y, x + 1, y + 1), fill=random.choice([(196, 72, 40), (226, 140, 52), (176, 52, 40), (230, 210, 120)]))
    else: dr.ellipse((x, y, x + 3, y + 2), fill=(146, 140, 130)); dr.point((x + 1, y), fill=(198, 194, 184))
for _ in range(500):                                       # stones on the road
    x, y = random.randrange(4, W - 4), random.randrange(4, H - 4)
    if road[y, x] and random.random() < .5: dr.ellipse((x, y, x + 2, y + 1), fill=(150, 128, 104)); dr.point((x, y), fill=(190, 170, 140))

# ---- olive grade (Dimraeth): soften saturation, warm, greens toward olive, lifted darks
def grade(a, k=1.0):
    a = a.astype(float); c = a[..., :3]; g = c.mean(2, keepdims=True)
    o = g + (c - g) * .68
    gr = np.clip((o[..., 1] - np.maximum(o[..., 0], o[..., 2])) / 50, 0, 1); o[..., 0] += gr * 30; o[..., 1] -= gr * 6; o[..., 2] -= gr * 4
    o[..., 0] *= 1.03; o[..., 2] *= .88; o = o * .92 + 9
    a[..., :3] = c + (o - c) * k; return np.clip(a, 0, 255).astype(np.uint8)
ground = Image.fromarray(grade(np.asarray(base))).convert('RGB'); ground.save(OUT + 'ground.png', optimize=True)

# ---- walk mask: water, cliff faces, the drop round a plateau top (except stairs), props, map border
drop = dil(UP, 4) & ~UP & ~FACE & ~RAMP
blk |= pond | (FACE & ~RAMP) | drop
if T2: blk |= RAIL
blk[:, :56] = blk[:, -56:] = True; blk[:140] = True; blk[-46:] = True
EXITS = [{'x0': W - 60, 'y0': 700, 'x1': W, 'y1': 860, 'to': 'td2', 'label': 'ป่าใบไม้แดง →'}] if not T2 else [{'x0': 0, 'y0': 700, 'x1': 60, 'y1': 840, 'to': 'td1', 'label': '← ป่าเนินผา'}]
ENTRIES = {'td2': [W - 100, 785]} if not T2 else {'td1': [100, 770]}
for e in EXITS: gap = road & (xx >= e['x0'] - 8) & (xx < e['x1']) & (yy >= e['y0']) & (yy < e['y1']); blk[gap] = False   # open the border where the road leaves
blk = ndimage.binary_opening(blk, iterations=1) | pond
Image.fromarray((blk[::2, ::2] * 255).astype(np.uint8)).save(OUT + 'block.png', optimize=True)

# ---- props atlas
keys = list(SPR); at = []; X = Y = rowh = 0; AW = 2048
for k in sorted(keys, key=lambda k: -SPR[k].height):
    w, h = SPR[k].size
    if X + w > AW: X = 0; Y += rowh + 2; rowh = 0
    at.append((k, X, Y)); X += w + 2; rowh = max(rowh, h)
atlas = Image.new('RGBA', (AW, Y + rowh))
pos = {}
for k, x, y in at:
    im = SPR[k]
    if k[0] != 'crown': im = Image.fromarray(grade(np.asarray(im)))
    atlas.alpha_composite(im, (x, y)); pos[k] = (x, y) + im.size
atlas.save(OUT + 'props.png', optimize=True)
props = [{'x': p['x'], 'y': p['y'], 'a': list(pos[p['s']]), 'o': 1 if p['over'] else 0} for p in PROPS]

# ---- hero and monster sheets at map size
def cells(f, C, rows, cols, k, cut=110):
    sh = Image.open(f).convert('RGBA'); c2 = round(C * k); out = Image.new('RGBA', (cols * c2, rows * c2))
    for r in range(rows):
        for i in range(cols):
            cl = sh.crop((i * C, r * C, i * C + C, r * C + C)).resize((c2, c2), Image.LANCZOS)
            a = np.asarray(cl).copy(); a[..., 3] = (a[..., 3] > cut) * 255; out.paste(Image.fromarray(a), (i * c2, r * c2))
    return out, c2
M = json.load(open('art/action/n128/berserker.json')); C = M['cell']; hk = HERO / (147 - 38)
hero = {'c': round(C * hk), 'fx': round(M['fx'] * hk), 'fy': round(M['fy'] * hk), 'dirs': M['dirs']}
for a in ('run', 'idle'):
    im, _ = cells('art/action/n128/berserker_%s.png' % a, C, 8, 8, hk); im.save(OUT + 'hero_%s.png' % a, optimize=True)
MOBS = {'wolf': .72, 'shroom': .5, 'skeleton': .98, 'boar_guard': 1.25, 'goblin_archer': .78, 'golem': 1.35, 'wisp': .62}
mobs = {}
for kk, s in MOBS.items():
    mm = json.load(open('art/action/mobs_hr/%s.json' % kk)); sh2 = Image.open('art/action/mobs_hr/%s.png' % kk).convert('RGBA')
    bb = sh2.crop((0, 0, mm['w'], mm['h'])).getbbox(); k = HERO * s / (bb[3] - bb[1])
    cw, chh = round(mm['w'] * k), round(mm['h'] * k); out = Image.new('RGBA', (cw * mm['n'], chh))
    for i in range(mm['n']):
        cl = sh2.crop((i * mm['w'], 0, (i + 1) * mm['w'], mm['h'])).resize((cw, chh), Image.LANCZOS); a = np.asarray(cl).copy(); a[..., 3] = (a[..., 3] > 110) * 255
        out.paste(Image.fromarray(a), (i * cw, 0))
    out.save(OUT + 'mob_%s.png' % kk, optimize=True); mobs[kk] = {'w': cw, 'h': chh, 'fx': round(mm['fx'] * k), 'fy': round(mm['fy'] * k), 'n': mm['n']}
SPAWN2 = [('skeleton', 980, 470), ('skeleton', 1030, 500), ('skeleton', 950, 520), ('wolf', 560, 980), ('wolf', 600, 1000), ('wolf', 520, 1010),
          ('boar_guard', 1500, 880), ('boar_guard', 1550, 900), ('golem', 1320, 330), ('goblin_archer', 1400, 160), ('goblin_archer', 1470, 180),
          ('wisp', 640, 860), ('wisp', 690, 900), ('wisp', 600, 920), ('shroom', 480, 470), ('shroom', 520, 500)]
SPAWN = [('wolf', 980, 650), ('wolf', 1030, 690), ('wolf', 950, 700), ('shroom', 640, 820), ('shroom', 700, 850), ('shroom', 590, 860),
         ('skeleton', 1320, 760), ('skeleton', 1370, 800), ('boar_guard', 1470, 520), ('goblin_archer', 900, 200), ('goblin_archer', 960, 230),
         ('wolf', 1600, 960), ('shroom', 300, 560)]
json.dump({'w': W, 'h': H, 'start': [120, 770] if T2 else [200, 705], 'props': props, 'hero': hero, 'mobs': mobs, 'spawn': SPAWN2 if T2 else SPAWN, 'bk': 2,
           'exits': EXITS, 'entries': ENTRIES}, open(OUT + 'map.json', 'w'))
# preview of the whole map
pv = ground.convert('RGBA')
for p in sorted(PROPS, key=lambda p: (p['over'], p['y'])):
    x, y, w, h = pos[p['s']]; pv.alpha_composite(atlas.crop((x, y, x + w, y + h)), (int(p['x'] - w / 2), int(p['y'] - h)))
pv.convert('RGB').save('art/td/%s_preview.png' % ('map2' if T2 else 'map1'))
print('ok', len(PROPS), 'props', atlas.size, 'boulders', len(BOULDERS))
