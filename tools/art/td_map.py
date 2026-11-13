# Walkable map 1 (owner 2026-11-11 "แมพเอาให้เสร็จก่อน1แมพละฉันจะลองเดินดู"): the mock_map2 look as a full map for map.html.
# Free (no new PixelLab jobs): raised plateaus with code-drawn cliffs (boulders on the rim, stone stairs up), a pond, the 4 big
# rocks (moss added), trees / bushes round the edges (props in an olive grade like Dimraeth).
# Ground (2026-11-13, owner "ทำแมพให้สวย"): painted flat in code in the look of art/incoming/mapgen/scene1.png, see the
# "ground painter" section: clean colour areas, crisp road with a dark lip and oval marks, bold shadows, daisies / tufts /
# stones, blue water with ripples. Geometry, props, block.png and map.json are exactly what they were before that repaint.
#   python3 tools/art/td_map.py -> art/td/map1/{ground.png, props.png, block.png, hero_*.png, mob_*.png, map.json}
#   MAP=td2 python3 tools/art/td_map.py -> art/td/map2/ (owner 2026-11-12 "ทำแมพรอไปก่อน": an autumn forest with a river and a
#   bridge, east of map 1; `exits` / `entries` in map.json join the two maps)
#   MAP=td3 python3 tools/art/td_map.py -> art/td/map3/ (2026-11-13: a cold ruined graveyard east of map 2 for stronger monsters:
#   grey dirt and stone with dead grass, a paved road, two plateaus with stairs, a murky pool, graves, ruins, dead trees.
#   Only art already in the repo, recoloured in code; td1 / td2 output is unchanged apart from map 2's new east exit)
import json, math, os, random, sys, numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0, 'tools/art'); from px_smooth import smooth_up
random.seed(7); np.random.seed(7)
W, H = 1800, 1100; DH = 62; HERO = 50
MAPID = os.environ.get('MAP', 'td1'); T2 = MAPID == 'td2'; T3 = MAPID == 'td3'
OUT = 'art/td/map3/' if T3 else 'art/td/map2/' if T2 else 'art/td/map1/'; os.makedirs(OUT, exist_ok=True)
yy, xx = np.mgrid[0:H, 0:W]

# The old painter filled the map with 32 px PixelLab tile textures here (tile_fill). The ground is now painted flat by the
# "ground painter" further down and needs no textures, but the random draws of those fills stay, in the same order, so that
# every prop placed later lands exactly where it always did (block.png / props.png / map.json must not change).
def tile_draws():
    for y in range(0, H, 32):
        for x in range(0, W, 32):
            if random.random() < .5: random.choice((0, 1, 2))
for _ in range(5 if T2 else 4): tile_draws()                 # grass, dirt, (map 2: leaves), water, rock
def noise(cell):
    n = np.random.rand(H // cell + 2, W // cell + 2)
    return np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize(((W // cell + 2) * cell, (H // cell + 2) * cell), Image.BICUBIC)).astype(float)[:H, :W] / 255
N8, N40, N90 = noise(8), noise(40), noise(90)
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

# ---- the big light / dark patches (N90 / N40) and, on map 3, the stone / dead-grass patches (M90 / M40) are laid by the painter
if T3: M90, M40 = noise(90), noise(40)
# ---- road (Catmull-Rom), water: masks only, the painter draws them
ROADS = [[(-30, 720), (180, 700), (380, 660), (540, 590), (640, 470), (660, 380)],
         [(540, 600), (760, 650), (980, 720), (1180, 700), (1330, 640), (1400, 600)],
         [(1180, 700), (1420, 780), (1640, 800), (1840, 770)]]
if T2: ROADS = [[(-30, 770), (200, 745), (420, 695), (640, 645), (900, 625), (1120, 592), (1340, 520), (1490, 470), (1525, 372)],
                [(1120, 592), (1260, 740), (1500, 850), (1720, 900)]]
if T3: ROADS = [[(-30, 610), (200, 600), (420, 560), (640, 590), (880, 640), (1100, 650), (1290, 690), (1400, 680), (1432, 630)],
                [(640, 590), (660, 480), (615, 372)],
                [(880, 640), (850, 800), (700, 900), (560, 930)],
                [(1100, 650), (1180, 480), (1330, 330), (1540, 292)]]
road = np.zeros((H, W), bool)
for r in ROADS: road |= band(r, 24)
if T3:   # a murky pool in the south-east
    pond = blob(1420, 955, 150, 58); bank = dil(pond, 6); river = pond; deck = np.zeros((H, W), bool)
elif not T2:   # a pond
    pond = blob(1080, 950, 190, 80); bank = dil(pond, 6); river = pond; deck = np.zeros((H, W), bool)
else:   # a river from the top to the bottom with a wooden bridge where the road crosses
    river = band([(870, -40), (850, 200), (800, 420), (825, 640), (780, 860), (805, 1140)], 40)
    deck = (xx > 742) & (xx < 892) & (yy > 600) & (yy < 654)
    bank = dil(river, 7); pond = river & ~deck
    RAIL = deck & ((yy < 606) | (yy > 648))
# ---- plateaus: footprint at ground level, top drawn DH higher, cliff face below
BOULDERS = []; UP = np.zeros((H, W), bool); FACE = np.zeros((H, W), bool); RAMP = np.zeros((H, W), bool); FOOT = np.zeros((H, W), bool)
def shift_up(m, k):
    o = np.zeros_like(m); o[:H - k] = m[k:]; return o
def plateau(mask, ramps):
    global UP, FACE, FOOT
    up = shift_up(mask, DH); span = np.zeros_like(mask)
    for k in range(DH + 1): span |= shift_up(mask, k)
    face = span & ~up
    FOOT |= dil(mask, 5) & ~span                                                    # the shadow at the foot
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
elif T3:
    plateau(blob(560, 225, 330, 92), [(588, 644)])
    plateau(blob(1500, 545, 215, 86), [(1406, 1458)])
else:
    plateau(yy < 300 + 55 * np.sin(xx / 240) + 26 * np.sin(xx / 93 + 1) + (N40 - .5) * 30, [(632, 690)])
    plateau(blob(1460, 560, 200, 84), [(1380, 1430)])
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
def wither(im, seed):            # green leaves -> dark, cold grey-green (a dead forest); trunks a little greyer
    a = np.asarray(im.convert('RGBA')).copy(); hsv = np.asarray(Image.fromarray(a[..., :3]).convert('HSV')).astype(float)
    g = (hsv[..., 0] > 40) & (hsv[..., 0] < 130) & (hsv[..., 1] > 50) & (a[..., 3] > 0)
    hsv[..., 0] = np.where(g, 96, hsv[..., 0]); hsv[..., 1] = np.where(g, hsv[..., 1] * .3, hsv[..., 1] * .75); hsv[..., 2] = np.where(g, hsv[..., 2] * .62, hsv[..., 2] * .9)
    a[..., :3] = np.asarray(Image.fromarray(hsv.astype(np.uint8), 'HSV').convert('RGB')); return Image.fromarray(a)
SPR = {}; PROPS = []
def sprite(key, f, h, flip=False, moss=False):
    k = (key, h, flip)
    if k not in SPR:
        im = fit(f, h, flip)
        if T2 and key.split('art/')[0] in ('tree', 'stree', 'bush'): im = autumn(im, len(SPR))
        if T3 and (key.split('art/')[0] in ('tree', 'stree', 'bush') or 'bushes_' in key): im = wither(im, len(SPR))
        if moss: im = mossify(im, len(SPR))
        SPR[k] = im
    return k
FP = {'tree': (.17, 11, 6), 'stree': (.14, 6, 3), 'bush': (.34, .16, 0), 'rock': (.42, .17, .12), 'pebble': (.36, .22, 0),
      'fence': (.46, 4, 0), 'sign': (.12, 3, 0), 'flowers': None, 'crown': None}
FR = 'art/side/forest/'
def put(kind, f, h, x, y, flip=False, moss=False, over=False):
    PROPS.append({'s': sprite(kind + f, f, h, flip, moss), 'x': x, 'y': y, 'kind': kind, 'over': over})
TREE = 'art/side/map30/tree.png'
if T3:   # the edge forest only (withered); the inside is placed by hand below
    for x in range(-40, W + 60, 150):
        put('tree', TREE, random.randint(220, 270), x + random.randint(-30, 30), random.randint(100, 150), random.random() < .5)
    for y in range(330, H + 40, 150):
        for X, gy in ((random.randint(-30, 30), 625), (W + random.randint(-30, 30), -999)):
            yy0 = y + random.randint(-20, 20)
            if abs(yy0 - gy) > 75: put('tree', TREE, random.randint(220, 260), X, yy0, random.random() < .5)      # the road gap on the west edge
elif not T2:
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
if T3: spot2 = lambda *a, **k: None          # map 3 has no random pass: everything inside is placed by hand
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
SPAWN2 = [('skeleton', 980, 470), ('skeleton', 1030, 500), ('skeleton', 950, 520), ('wolf', 560, 980), ('wolf', 600, 1000), ('wolf', 520, 1010),
          ('boar_guard', 1500, 880), ('boar_guard', 1550, 900), ('golem', 1320, 330), ('goblin_archer', 1400, 160), ('goblin_archer', 1470, 180),
          ('wisp', 640, 860), ('wisp', 690, 900), ('wisp', 600, 920), ('shroom', 480, 470), ('shroom', 520, 500)]
SPAWN3 = [('skeleton', 330, 860), ('skeleton', 400, 900), ('skeleton', 300, 940), ('skeleton', 440, 830),              # the graveyard
          ('boar_guard', 1040, 800), ('boar_guard', 1100, 840), ('boar_guard', 1000, 860),                                # south of the crossroads
          ('golem', 1500, 500), ('golem', 1570, 530), ('golem', 420, 220), ('skeleton', 700, 215), ('skeleton', 760, 235),   # the two plateaus
          ('wisp', 1250, 900), ('wisp', 1300, 860), ('wisp', 1590, 900), ('wisp', 1220, 960),                             # round the pool
          ('wisp', 960, 330), ('wisp', 1010, 360), ('wisp', 920, 380), ('boar_guard', 1500, 240), ('boar_guard', 1580, 330),
          ('skeleton', 1640, 760), ('skeleton', 1690, 800), ('golem', 250, 420)]
SPAWN = [('wolf', 980, 650), ('wolf', 1030, 690), ('wolf', 950, 700), ('shroom', 640, 820), ('shroom', 700, 850), ('shroom', 590, 860),
         ('skeleton', 1320, 760), ('skeleton', 1370, 800), ('boar_guard', 1470, 520), ('goblin_archer', 900, 200), ('goblin_archer', 960, 230),
         ('wolf', 1600, 960), ('shroom', 300, 560)]
# ---- hand-placed layout (owner 2026-11-12 "ของจริงใส่มั่วไปหมด"): only the edge forest stays from the code above; everything inside
# the map is placed by hand in themed groups (a camp, a village corner at the crossroads, a fishing pond, ruins on the high
# ground, a grove of logs and mushrooms). A piece that lands on the road, water, a cliff or a monster camp is nudged a little,
# or dropped (printed).
PROPS[:] = [p for p in PROPS if p['kind'] == 'tree' and (p['y'] < 200 or p['x'] < 70 or p['x'] > W - 70)]
SPW = SPAWN3 if T3 else SPAWN2 if T2 else SPAWN
BAD = dil(road, 18) | dil(bank, 8) | dil(FACE | RAMP, 10) | (yy < 150) | (yy > H - 40)
if T2: BAD |= dil(deck, 6)
for k_, x_, y_ in SPW: BAD |= ((xx - x_) / 46) ** 2 + ((yy - y_) / 32) ** 2 < 1
WATERS = (pond if not T2 else river & ~deck)
NUD = [(0, 0)] + [(round(math.cos(a) * r), round(math.sin(a) * r * .7)) for r in (14, 28, 42, 56) for a in np.linspace(0, 6.28, 12, endpoint=False)]
# owner 2026-11-12: no village things in the wild (lamps, benches, wells, hay, tents, crates, signs: they look usable and do not
# belong in a forest), no stone stairs without a hill, no reeds in the water (they read as bushes)
SKIP = lambda n: n.startswith(('camp_', 'village_')) or n in ('ruins_7', 'water_2', 'water_3', 'water_4', 'water_5')
def H_(kind, name, h, x, y, flip=None, wet=False):
    if SKIP(name): return
    f = name if name.startswith('art/') else P2 + name + '.png'
    for dx, dy in NUD:
        X, Y = x + dx, y + dy
        if not (0 < X < W and 0 < Y < H): continue
        ok = WATERS[Y, X] if wet else not BAD[Y, X] and not WATERS[Y, X]
        if ok:
            put(kind, f, h, X, Y, (random.random() < .5) if flip is None else flip)
            if not wet: BAD[max(0, Y - 10):Y + 6, max(0, X - 14):X + 14] = True
            return
    print('  dropped', name, x, y)
TR = 'art/side/map30/tree.png'; ST = 'art/side/forest/small_tree.png'; RK = 'art/td/props/'
if T3:
    DT = 'trees_autumn_3'
    # dead trees that frame the clearings
    for h, x, y in ((230, 180, 470), (205, 840, 450), (220, 1010, 530), (215, 1130, 1010), (200, 850, 1045), (220, 150, 1040),
                    (205, 1720, 1000), (215, 1110, 250), (190, 1240, 885)):
        H_('tree2', DT, h, x, y)
    # the graveyard in the south-west: rows of headstones, a broken arch at the end of the road, statues, a low wall
    for r_, y in enumerate((800, 868, 936, 1004)):
        for c_ in range(5):
            x = 232 + c_ * 62 + (r_ % 2) * 14
            if (r_, c_) in ((1, 3), (2, 1), (3, 4)): H_('small', 'stones_%d' % (10, 8, 9)[r_ - 1], 30, x, y)      # a fallen one
            else: H_('small', 'ruins_8', random.randint(54, 62), x + random.randint(-4, 4), y + random.randint(-4, 4))
    for k, n, h, x, y in (('solid', 'ruins_1', 140, 610, 868), ('solid', 'ruins_5', 76, 200, 740), ('solid', 'ruins_4', 76, 560, 760), ('solid', 'ruins_6', 96, 130, 900),
                          ('solid', 'ruins_2', 92, 600, 1010), ('small', 'stones_4', 34, 520, 990), ('small', 'logs2_4', 40, 170, 990)):
        H_(k, n, h, x, y)
    # the west plateau: a ruined shrine
    for k, n, h, x, y in (('solid', 'ruins_1', 132, 500, 190), ('solid', 'ruins_0', 92, 330, 215), ('solid', 'ruins_0', 86, 690, 180), ('solid', 'ruins_6', 96, 820, 215),
                          ('solid', 'ruins_4', 72, 590, 240), ('small', 'ruins_8', 60, 400, 262), ('small', 'ruins_8', 60, 760, 268)):
        H_(k, n, h, x, y)
    # the east plateau: broken pillars round the golems
    for k, n, h, x, y in (('solid', 'ruins_0', 96, 1400, 478), ('solid', 'ruins_0', 90, 1640, 500), ('solid', 'ruins_2', 96, 1560, 440), ('solid', 'ruins_5', 72, 1450, 545),
                          ('small', 'stones_2', 34, 1620, 560)):
        H_(k, n, h, x, y)
    # the shrine at the end of the north-east road
    for k, n, h, x, y in (('solid', 'ruins_1', 136, 1640, 262), ('solid', 'ruins_5', 72, 1560, 222), ('small', 'ruins_8', 60, 1690, 330)): H_(k, n, h, x, y)
    # big rocks and rock piles
    for f, h, x, y, fl in (('rock0', 200, 330, 520, False), ('rock1', 170, 1010, 1000, True), ('rock2', 150, 1500, 760, False), ('rock3', 120, 1330, 210, True),
                           ('rock3', 110, 760, 960, False), ('rock1', 150, 1010, 215, False)):
        H_('rock', RK + f + '.png', h, x, y, fl)
    for n, h, x, y in (('stones_0', 38, 470, 480), ('stones_1', 40, 1180, 420), ('stones_10', 40, 780, 700), ('stones_11', 38, 1600, 380), ('stones_12', 36, 960, 760),
                       ('stones_5', 34, 250, 660), ('stones_2', 34, 1340, 760), ('stones_4', 34, 1230, 1040), ('stones_9', 36, 520, 420), ('stones_8', 30, 1420, 260),
                       ('stones_1', 36, 90, 700), ('stones_0', 34, 1660, 1030), ('stones_10', 36, 900, 1020), ('stones_5', 32, 1440, 380)):
        H_('small', n, h, x, y)
    # dead wood, dry grass clumps
    for n, h, x, y in (('logs2_4', 46, 980, 440), ('logs2_5', 52, 1140, 900), ('logs2_1', 52, 730, 380), ('logs2_0', 46, 1600, 660), ('logs2_5', 48, 300, 330),
                       ('logs2_4', 42, 1380, 1050), ('logs2_2', 46, 880, 900), ('logs2_1', 50, 1760, 860)):
        H_('small', n, h, x, y)
    for n, h, x, y in (('bushes_6', 44, 120, 560), ('bushes_3', 44, 560, 660), ('bushes_7', 40, 1040, 720), ('bushes_8', 40, 1270, 620), ('bushes_6', 46, 1560, 1010),
                       ('bushes_3', 42, 1250, 300), ('bushes_7', 40, 420, 620), ('bushes_8', 38, 850, 560), ('bushes_6', 44, 1690, 400), ('bushes_3', 40, 700, 820),
                       ('bushes_7', 38, 1500, 880), ('bushes_8', 40, 1330, 1010), ('bushes_6', 42, 1180, 740), ('bushes_3', 40, 240, 1050)):
        H_('bush', n, h, x, y)
elif not T2:
    # trees that frame the clearings
    for n, h, x, y in (('trees_green_0', 240, 300, 470), ('trees_green_1', 225, 840, 520), ('trees_green_2', 215, 1250, 430), ('trees_green_0', 235, 1690, 660),
                       ('trees_green_3', 215, 1300, 925), ('trees_green_1', 220, 120, 1000), ('trees_green_3', 205, 470, 905), ('trees_green_2', 205, 1560, 1010)):
        H_('tree2', n, h, x, y)
    for x, y in ((700, 400), (1120, 470), (1610, 700), (560, 1000)): H_('stree', ST, 105, x, y)
    # the camp south-west of the road
    for k, n, h, x, y in (('solid', 'camp_0', 96, 255, 830), ('small', 'camp_1', 50, 335, 862), ('small', 'camp_2', 44, 182, 846), ('small', 'camp_3', 46, 176, 896),
                          ('small', 'camp_5', 48, 222, 918), ('small', 'camp_8', 40, 270, 935), ('small', 'logs2_0', 44, 350, 915), ('small', 'camp_6', 56, 400, 845),
                          ('fence', 'village_1', 40, 120, 800), ('small', 'logs2_2', 46, 110, 900)):
        H_(k, n, h, x, y)
    # where the camp was: a fallen-tree corner
    for k, n, h, x, y in (('small', 'logs2_0', 50, 250, 850), ('small', 'logs2_3', 46, 320, 880), ('bush', 'bushes_6', 46, 200, 900), ('small', 'stones_5', 34, 290, 930)):
        H_(k, n, h, x, y)
    # the crossroads: lamps, a signpost, a well, hay, a bench
    for k, n, h, x, y in (('small', 'village_4', 88, 470, 668), ('small', 'village_4', 88, 628, 560), ('small', 'village_2', 56, 515, 652), ('solid', 'village_5', 92, 735, 560),
                          ('small', 'village_7', 44, 790, 585), ('small', 'village_8', 40, 575, 662), ('bush', 'bushes_1', 46, 690, 590), ('bush', 'bushes_9', 34, 412, 610)):
        H_(k, n, h, x, y)
    # the fishing pond
    for n, x, y in (('water_0', 1040, 960), ('water_1', 1130, 940), ('water_0', 1170, 995), ('water_1', 990, 990)): H_('water', n, 44, x, y, wet=True)
    for n, x, y in (('water_2', 905, 935), ('water_4', 1255, 985), ('water_3', 1210, 890), ('water_5', 960, 900)): H_('water', n, 58, x, y, wet=True)
    for k, n, h, x, y in (('small', 'village_8', 40, 990, 850), ('small', 'village_4', 88, 1170, 860), ('bush', 'bushes_6', 46, 870, 880), ('bush', 'bushes_3', 44, 1270, 1040)):
        H_(k, n, h, x, y)
    # ruins on the island plateau and along the north ridge
    for k, n, h, x, y in (('solid', 'ruins_8', 104, 1450, 452), ('solid', 'ruins_0', 92, 1360, 492), ('solid', 'ruins_5', 70, 1555, 500),
                          ('solid', 'ruins_2', 92, 420, 232), ('solid', 'ruins_0', 90, 1240, 205), ('solid', 'ruins_6', 96, 1600, 220)):
        H_(k, n, h, x, y)
    # big rocks
    for f, h, x, y, fl in (('rock0', 210, 1000, 470, False), ('rock1', 170, 1430, 790, True), ('rock2', 140, 520, 980, False), ('rock3', 110, 1760, 520, True)):
        H_('rock', RK + f + '.png', h, x, y, fl)
    # the grove of logs and mushrooms in the south-east
    for k, n, h, x, y in (('small', 'logs2_1', 56, 1690, 880), ('small', 'logs2_3', 46, 1740, 930), ('small', 'logs2_4', 40, 1650, 940), ('small', 'logs2_5', 52, 1720, 1000),
                          ('bush', 'bushes_7', 40, 1630, 880), ('small', 'stones_2', 30, 1690, 960)):
        H_(k, n, h, x, y)
    # small bits along the road and in the meadow
    for k, n, h, x, y in (('bush', 'bushes_0', 46, 210, 655), ('flowers', 'art/side/forest/flowers.png', 20, 245, 640), ('bush', 'bushes_2', 44, 880, 700),
                          ('small', 'stones_0', 32, 930, 760), ('bush', 'bushes_5', 46, 1220, 760), ('small', 'stones_8', 28, 1350, 700), ('bush', 'bushes_10', 40, 760, 790),
                          ('small', 'stones_12', 34, 640, 960), ('bush', 'bushes_4', 46, 1500, 640), ('flowers', 'art/side/forest/flowers.png', 20, 1150, 760)):
        H_(k, n, h, x, y)
else:
    for n, h, x, y in (('trees_autumn_0', 240, 470, 330), ('trees_autumn_1', 230, 160, 990), ('trees_autumn_2', 220, 1650, 620), ('trees_autumn_0', 230, 1250, 1020),
                       ('trees_autumn_1', 225, 620, 470), ('trees_autumn_2', 215, 1090, 300), ('trees_autumn_3', 190, 1180, 420), ('trees_autumn_3', 180, 380, 1030),
                       ('trees_autumn_0', 225, 1700, 1010), ('trees_autumn_1', 220, 980, 1040)):
        H_('tree2', n, h, x, y)
    # the north-west clearing: mushrooms and stumps
    for k, n, h, x, y in (('small', 'logs2_3', 46, 290, 490), ('small', 'logs2_2', 50, 360, 530), ('bush', 'bushes_2', 44, 230, 520), ('small', 'stones_9', 32, 320, 570)):
        H_(k, n, h, x, y)
    # camp in the north-west clearing
    for k, n, h, x, y in (('solid', 'camp_0', 96, 290, 480), ('small', 'camp_1', 50, 370, 512), ('small', 'camp_2', 44, 215, 500), ('small', 'camp_7', 50, 232, 546),
                          ('small', 'camp_8', 40, 300, 560), ('small', 'logs2_0', 44, 380, 566), ('small', 'village_3', 58, 150, 712)):
        H_(k, n, h, x, y)
    # the bridge: lamps at both ends, reeds and lily pads along the river, a rowing boat
    for k, n, h, x, y in (('small', 'village_4', 88, 722, 598), ('small', 'village_4', 88, 925, 582)): H_(k, n, h, x, y)
    for n, h, x, y in (('water_2', 58, 790, 420), ('water_4', 58, 860, 300), ('water_3', 58, 780, 960), ('water_5', 58, 840, 700), ('water_0', 44, 850, 180),
                       ('water_1', 44, 800, 1040), ('water_8', 64, 812, 820), ('water_0', 44, 830, 520)):
        H_('water', n, h, x, y, wet=True)
    # the old temple ruins round the south road
    for k, n, h, x, y in (('solid', 'ruins_1', 140, 1010, 800), ('solid', 'ruins_7', 72, 1090, 900), ('solid', 'ruins_5', 72, 1190, 870), ('solid', 'ruins_6', 100, 1300, 960),
                          ('solid', 'ruins_0', 92, 950, 930), ('small', 'stones_4', 32, 1150, 960)):
        H_(k, n, h, x, y)
    # ruins on the plateau
    for k, n, h, x, y in (('solid', 'ruins_8', 104, 1330, 190), ('solid', 'ruins_0', 92, 1600, 175)): H_(k, n, h, x, y)
    # dead wood east of the river
    for k, n, h, x, y in (('small', 'logs2_1', 56, 1000, 380), ('small', 'logs2_5', 52, 1080, 420), ('small', 'logs2_3', 44, 950, 340), ('small', 'logs2_2', 46, 640, 330)):
        H_(k, n, h, x, y)
    for f, h, x, y, fl in (('rock0', 200, 520, 820, False), ('rock2', 150, 1500, 690, False), ('rock1', 160, 140, 380, True), ('rock3', 115, 1750, 380, True)):
        H_('rock', RK + f + '.png', h, x, y, fl)
    for k, n, h, x, y in (('bush', 'bushes_2', 44, 560, 620), ('bush', 'bushes_9', 34, 470, 700), ('bush', 'bushes_1', 46, 1250, 650), ('small', 'stones_0', 32, 1370, 600),
                          ('bush', 'bushes_6', 46, 260, 820), ('bush', 'bushes_0', 46, 1560, 900), ('small', 'stones_8', 28, 700, 760), ('bush', 'bushes_10', 40, 1020, 560),
                          ('small', 'stones_12', 34, 1620, 780), ('bush', 'bushes_5', 46, 430, 900)):
        H_(k, n, h, x, y)
# dark tree crowns hanging over the bottom edge (drawn over everything)
cr = fit(TREE, 300).crop((0, 0, 420, 140)); cr = autumn(cr, 99) if T2 else wither(cr, 99) if T3 else cr; ca = np.asarray(cr).copy(); ca[..., :3] = (ca[..., :3] * .5).astype(np.uint8); SPR[('crown', 0, 0)] = Image.fromarray(ca)
SPR[('crown', 0, 1)] = SPR[('crown', 0, 0)].transpose(Image.FLIP_LEFT_RIGHT)
for i, x in enumerate(range(-60, W + 100, 330)):
    PROPS.append({'s': ('crown', 0, i % 2), 'x': x + random.randint(-30, 30), 'y': H + 70, 'kind': 'crown', 'over': True})

# ---- collision footprints of the props, and their shadow shapes (to the lower right) for the ground painter
blk = np.zeros((H, W), bool); SHAD = np.zeros((H, W), bool)
for p in PROPS:
    im = SPR[p['s']]; w, h = im.size; x, y = p['x'], p['y']
    if p['kind'] in ('crown', 'flowers', 'flat', 'water'): continue
    if p['kind'] in ('tree', 'stree', 'tree2'):
        SHAD |= ((xx - x - w * .1) / (w * .42)) ** 2 + ((yy - y + 6) / (w * .17)) ** 2 < 1
    else:
        SHAD |= ((xx - x - w * .06) / (w * .5)) ** 2 + ((yy - y + h * .08) / (h * .16 + 3)) ** 2 < 1
    fp = FP[p['kind']]
    if fp:
        rx = fp[0] * w; ry = fp[1] * h if fp[1] < 1 else fp[1]; oy = fp[2] * h if fp[2] < 1 else fp[2]
        blk |= ((xx - x) / rx) ** 2 + ((yy - y + oy) / ry) ** 2 < 1
MOSSY = [random.random() < .5 for _ in BOULDERS]      # which rim boulders carry moss: the last draws from the seeded generator

# ============================================================================================================================
# ---- ground painter (owner 2026-11-13 "ทำแมพให้สวย"): the look of art/incoming/mapgen/scene1.png. Flat colour areas in a small
# palette per material, hard steps, crisp outlined edges, bold shadows, small hand-drawn decals: no texture tiles, no noise
# speckle, no dithering, no olive grade. Painted at half size and doubled: one art pixel = 2 x 2 map pixels (the grid of
# block.png), which next to the trees is as chunky as the reference. The geometry comes from the masks above and is not touched
# (the road edge is only tidied by a 5 px median and grows grass teeth a few pixels long); the big light / dark patches, the
# leaf carpets of map 2 and the rock / dead-grass patches of map 3 lie where the old map had them (same noise fields).
# Own random generators (RG / RR): nothing here draws from the seeded `random` / `np.random` that place the props.
GW, GH = W // 2, H // 2; gy, gx = np.mgrid[0:GH, 0:GW]
RG = np.random.default_rng(1113); RR = random.Random(1113)
def lo(m): return np.ascontiguousarray(m[::2, ::2])                         # a map-size mask / field at art size
def qt(a, q): return float(np.quantile(a, q))
def mv(m, dy, dx=0):                                                        # the mask moved dy down and dx right
    o = np.zeros_like(m)
    o[max(0, dy):GH + min(0, dy), max(0, dx):GW + min(0, dx)] = m[max(0, -dy):GH + min(0, -dy), max(0, -dx):GW + min(0, -dx)]; return o
def n4(m): return m | mv(m, 1) | mv(m, -1) | mv(m, 0, 1) | mv(m, 0, -1)     # the mask and its 4 neighbours
def runpos(m):                                                              # 1, 2, 3 ... down every vertical run of the mask
    c = np.cumsum(m, 0); return (c - np.maximum.accumulate(np.where(m, 0, c), 0)) * m
def streak(L):                # rows of dashes L px long, shifted row by row: a smooth field + this, thresholded = a brushed edge
    v = np.repeat(RG.random((GH, GW // L + 3)), L, axis=1); o = RG.integers(0, L, GH)
    return np.stack([v[y, o[y]:o[y] + GW] for y in range(GH)])
def wide(cy, cx):             # smooth noise stretched sideways (cells cy x cx): thresholded = flat horizontal blotches
    n = (RG.random((GH // cy + 3, GW // cx + 3)) * 255).astype(np.uint8)
    return np.asarray(Image.fromarray(n).resize(((GW // cx + 3) * cx, (GH // cy + 3) * cy), Image.BICUBIC)).astype(float)[:GH, :GW] / 255
def tones(p, f, qs=(.34, .28, .91), f2=None):   # 4 flat tones: p[0] base, p[1] darker patches, p[2] dark clumps inside them, p[3] sunny patches
    o = np.empty((GH, GW, 3), np.uint8); o[:] = p[0]; f2 = F2 if f2 is None else f2
    m1 = f < qt(f, qs[0]); o[m1] = p[1]; o[m1 & (f < qt(f, qs[0] * .8)) & (f2 < qt(f2, qs[1]))] = p[2]; o[f > qt(f, qs[2])] = p[3]; return o
PAL = dict(   # map 1: the greens, the dirt road and the blue water of the reference
    soft=[(123, 139, 55), (94, 122, 55), (73, 102, 57), (147, 158, 63)], top=[(131, 147, 59), (102, 130, 57), (81, 110, 59), (155, 166, 67)],
    tl=(166, 170, 78), td=(60, 84, 56), ts=(78, 104, 60), out=(44, 64, 54), rim=(170, 178, 84),
    rl=(182, 146, 84), rm=(150, 108, 62), rd=(112, 70, 48), rr=(128, 84, 54),
    bm=(124, 78, 52), bd=(72, 44, 46), wm=(66, 137, 157), wd=(54, 106, 140), wp=(50, 76, 108), wl=(131, 214, 216),
    k=[(152, 110, 66), (130, 86, 56), (108, 66, 50), (90, 54, 48)], kj=(64, 38, 46), ko=(48, 30, 40),
    sl=(204, 188, 152), sm=(166, 148, 118), sd=(112, 96, 84), so=(62, 48, 46),
    pl=(160, 158, 140), pm=(114, 112, 108), pd=(76, 74, 88), po=(44, 46, 54), moss=(104, 130, 58),
    shk=(.40, .46, .62), shb=(4, 6, 20))
if T2: PAL.update(   # map 2: autumn: yellower grass, carpets of orange / red / yellow leaves, a slightly cooler dirt road
    soft=[(134, 136, 58), (106, 120, 56), (84, 100, 56), (156, 152, 66)], top=[(142, 142, 60), (114, 128, 58), (92, 108, 58), (164, 158, 70)],
    leaf=[(200, 114, 50), (168, 78, 44), (138, 58, 44), (222, 154, 62)], lout=(98, 48, 42), tl=(176, 170, 80),
    rl=(178, 142, 90), rm=(146, 106, 68), rd=(106, 68, 50), rr=(122, 82, 58))
if T3: PAL.update(   # map 3: cold and dark: blue-grey dirt, broken flagstones, grey-green dead grass, a pale paved road, a murky pool
    soft=[(84, 80, 94), (74, 72, 88), (64, 64, 82), (94, 90, 102)], slab=[(72, 78, 98), (62, 68, 90), (82, 88, 108)], sj=(44, 48, 66),
    dead=[(82, 96, 88), (72, 84, 82), (62, 74, 78), (98, 110, 94)], top=[(92, 106, 96), (80, 92, 88), (70, 80, 84), (108, 120, 100)],
    tl=(150, 148, 108), td=(46, 50, 58), ts=(84, 92, 88), out=(34, 36, 50), rim=(140, 146, 114),
    pave=[(150, 154, 164), (128, 132, 146), (108, 112, 128)], pj=(74, 78, 96),
    bm=(74, 68, 70), bd=(44, 40, 50), wm=(58, 88, 86), wd=(46, 72, 78), wp=(36, 54, 66), wl=(134, 166, 150),
    k=[(116, 118, 132), (98, 100, 116), (82, 84, 102), (68, 70, 88)], kj=(48, 48, 64), ko=(32, 32, 46),
    sl=(170, 174, 184), sm=(134, 138, 152), sd=(92, 94, 110), so=(44, 44, 58),
    pl=(150, 154, 164), pm=(110, 114, 126), pd=(74, 76, 94), po=(34, 36, 50), moss=(84, 96, 84),
    shk=(.58, .6, .68), shb=(0, 2, 8))
PAL = {k_: (np.array(v_, np.uint8) if isinstance(v_[0], int) else [np.array(c_, np.uint8) for c_ in v_]) if k_ not in ('shk', 'shb') else np.array(v_, float) for k_, v_ in PAL.items()}
def shade(c): return np.clip(c * PAL['shk'] + PAL['shb'], 0, 255).astype(np.uint8)

# -- 1. the cover: big flat patches in the places the old map had its light / dark patches, brushed edges
lv = lo(N90) * .7 + lo(N40) * .3; lf = lo(N90) * .6 + lo(N40) * .4; F6 = (streak(5) - .5) * .034; F2 = wide(16, 22) + F6 * 2
g = tones(PAL['soft'], lv + F6)
cov = np.zeros((GH, GW), np.uint8)             # what lies on the soft ground: 0 grass (map 3: grey dirt), 1 leaves, 2 rock slab, 3 dead grass
if T2:   # carpets of fallen leaves where the old map had them
    lm = lf + (streak(4) - .5) * .05 > .45
    g[lm] = tones(PAL['leaf'], lo(N40) * .6 + wide(10, 18) * .4 + F6, (.30, .22, .88))[lm]; cov[lm] = 1
    g[lm & ~mv(lm, -1)] = PAL['lout']                                       # the carpet has a little thickness: a dark lower rim
if T3:   # areas of broken flagstones (a light upper edge, a dark lower edge), then patches of dead grass
    sm_ = lo(M90) * .65 + lo(M40) * .35 + F6 > .6
    seeds = np.zeros((GH, GW), bool)                                        # broken flagstones: cells round scattered seeds, dark joints
    for cy in range(0, GH - 8, 9):
        for cx in range(0, GW - 14, 15): seeds[cy + RR.randrange(8), cx + RR.randrange(14)] = True
    _, (iy, ix) = ndimage.distance_transform_edt(~seeds, return_indices=True, sampling=(1.5, 1)); lab = iy * GW + ix
    g[sm_] = np.array(PAL['slab'])[RG.choice(3, GH * GW, p=(.5, .3, .2))[lab]][sm_]; cov[sm_] = 2
    g[sm_ & ((lab != np.roll(lab, 1, 0)) | (lab != np.roll(lab, 1, 1)))] = PAL['sj']
    g[sm_ & ~mv(sm_, 1)] = PAL['slab'][2] + 12; g[sm_ & ~mv(sm_, -1)] = PAL['out']
    dm = lf + F6 > .56
    g[dm] = tones(PAL['dead'], lv + F6)[dm]; cov[dm] = 3
# -- 2. road, bank, water (fills), then the cover grows over their edges
vroad = ndimage.median_filter(lo(road).astype(np.uint8), size=5) > 0
water = lo(river); deck_a = lo(deck); bank_a = lo(bank) & ~water; up_a, face_a, ramp_a = lo(UP), lo(FACE), lo(RAMP)
if T3:   # an old paved road: slabs in running bond, three pale tones, dark joints, dirt showing where it is worn
    row = gy // 8; off = (row * 5) % 12; col = (gx + off) // 12
    g[vroad] = np.array(PAL['pave'])[RG.choice(3, (GH // 8 + 2, GW // 12 + 3), p=(.25, .55, .2))[row, col]][vroad]
    g[vroad & ((gy % 8 == 0) | ((gx + off) % 12 == 0))] = PAL['pj']
    wn = wide(5, 9); worn = vroad & (lo(N40) > .7) & (wn > .56); g[worn] = PAL['soft'][1]
else:    # a dirt road: light inside, a darker band along the edges, flat darker blotches
    din = ndimage.distance_transform_edt(vroad)
    g[vroad] = PAL['rl']
    wn = wide(5, 16); g[vroad & (wn > qt(wn, .70))] = PAL['rm']
    g[vroad & (din < 2.4 + (lo(N8) - .5) * 2)] = PAL['rm']
if T2: bank_a &= ~(vroad & ndimage.binary_dilation(deck_a, iterations=12))    # the road runs onto the bridge: no bank strip across it
g[bank_a] = PAL['bm']
g[water] = PAL['wm']
wn = wide(6, 22); g[water & (wn > qt(wn, .60))] = PAL['wd']
g[water & (mv(~water, 1) | mv(~water, 2) | mv(~water, 3))] = PAL['wp']     # the north bank throws a shadow on the water
soft = ~(vroad | bank_a | water | deck_a | face_a | ramp_a)
def blades(soil, src, dens, lmax):   # the cover grows over the edge of `soil` from the `src` pixels touching it: blades 1 px wide
    _, (iy, ix) = ndimage.distance_transform_edt(~soil, return_indices=True); live = soil.copy()
    by, bx = np.nonzero(src & ~soil & n4(soil)); cl = wide(7, 7)
    for y, x in zip(by.tolist(), bx.tolist()):
        if RR.random() > dens * (.3 + 1.4 * cl[y, x]): continue
        dy, dx = int(np.sign(iy[y, x] - y)), int(np.sign(ix[y, x] - x)); c = g[y, x].copy(); lean = RR.choice((-1, 0, 0, 1)); L = RR.randint(1, lmax)
        for k in range(1, L + 1):
            Y, X = y + dy * k + (dx != 0) * lean * (k > 1), x + dx * k + (dy != 0) * lean * (k > 1)
            if not (0 <= Y < GH and 0 <= X < GW) or not soil[Y, X]: break
            g[Y, X] = c; live[Y, X] = False; cov[Y, X] = cov[y, x]
            Y2, X2 = Y + (dx != 0) * (lean or 1), X + (dy != 0) * (lean or 1)                   # a long blade is 2 px wide at its foot
            if k == 1 and L > 1 and 0 <= Y2 < GH and 0 <= X2 < GW and soil[Y2, X2]: g[Y2, X2] = c; live[Y2, X2] = False; cov[Y2, X2] = cov[y, x]
    return live
live = blades(vroad | bank_a, soft, 0 if T3 else .5, 3)
soft2 = soft | ((vroad | bank_a) & ~live); vroad2 = vroad & live; bank2 = bank_a & live
oe = soft2 & n4(live); g[oe] = PAL['out']                                   # the dark rim of the cover along road and bank
if T2: g[oe & (cov == 1)] = PAL['lout']
if not T3: g[vroad2 & mv(soft2, 1)] = PAL['rd']                             # a dark lip where the cover hangs over the road
g[bank2 & mv(soft2, 1)] = PAL['bd']; g[bank2 & n4(water)] = PAL['bd']
g[water & n4(~water)] = PAL['wl']                                           # a light line along the bank
def ell(cx, cy, rx, ry):             # the pixels of a small ellipse
    return [(y, x) for y in range(int(cy - ry - 1), int(cy + ry + 2)) for x in range(int(cx - rx - 1), int(cx + rx + 2))
            if 0 <= y < GH and 0 <= x < GW and ((x - cx) / (rx + .35)) ** 2 + ((y - cy) / (ry + .35)) ** 2 <= 1]
def ring(px): s_ = set(px); return [(y, x) for y, x in px if not {(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)} <= s_]
def spots(mask, n, gap=0):           # up to n random pixels of the mask, at least `gap` apart
    ys, xs = np.nonzero(mask); out = []
    for _ in range(n * 8 if len(ys) else 0):
        if len(out) >= n: break
        i = RR.randrange(len(ys)); x, y = int(xs[i]), int(ys[i])
        if gap and any(abs(x - a) < gap and abs(y - b) < gap * .6 for a, b in out): continue
        out.append((x, y))
    return out
if not T3:   # oval marks on the road: a thin darker ring, some filled with the other tone
    core = ndimage.binary_erosion(vroad2, iterations=4)
    for x, y in spots(core, int(core.sum()) // 110, 12):
        rx_ = RR.randint(3, 7); px = ell(x, y, rx_, RR.choice((1.6, 2, 2.4)) + (rx_ > 5) * .6)
        if not all(core[q] for q in px): continue
        if RR.random() < .5:
            f = PAL['rm'] if tuple(g[y, x]) == tuple(PAL['rl']) else PAL['rl']
            for q in px: g[q] = f
        for q in ring(px): g[q] = PAL['rr']
    for x, y in spots(core, int(core.sum()) // 420, 6):                     # a few pebbles
        g[y, x:x + 2] = PAL['pl']; g[y + 1, x:x + 2] = PAL['rr']; g[y, x + 1 + RR.randint(0, 1)] = PAL['pm']
inner = ndimage.binary_erosion(water & ~deck_a, iterations=3)               # ripple strokes
for x, y in spots(inner, int(inner.sum()) // 100, 6):
    L = RR.randint(3, 8); c = PAL['wl'] if RR.random() < .7 else PAL['wp']; kink = RR.randrange(1, L); d = RR.choice((-1, 1))
    for k in range(L):
        X, Y = x + k, y + (d if k >= kink and L > 4 else 0)
        if X < GW and inner[Y, X]: g[Y, X] = c
for p in PROPS:   # the lily pads and the boat (props) carry a round patch of grey water: a dark ring and a light ripple arc tie it into the pond
    if p['kind'] != 'water': continue
    w_, h_ = SPR[p['s']].size; cx, cy, r_ = p['x'] / 2, (p['y'] - h_ / 2) / 2, w_ / 4
    for q in ell(cx, cy, r_ + 1.2, r_ + 1.2):
        if water[q] and not deck_a[q]: g[q] = PAL['wp']
    for qy, qx in ring(ell(cx, cy + 1.5, r_ + 3.6, r_ + 2.6)):
        if qy > cy + 2 and water[qy, qx] and not deck_a[qy, qx] and (qx + qy) % 9 > 1: g[qy, qx] = PAL['wl']
if not T3:   # a few small lily pads away from the big ones (props)
    far = inner & ndimage.binary_erosion(inner, iterations=4)
    for p in PROPS:
        if p['kind'] == 'water': far &= np.hypot(gx - p['x'] / 2, gy - (p['y'] - 20) / 2) > 26
    for x, y in spots(far, 5 if T2 else 3, 28):
        px = ell(x, y, 3, 1.7)
        for q in ell(x, y, 4, 2.7): g[q] = (40, 78, 100)
        for q in px: g[q] = (112, 146, 74)
        g[y, x + 1:x + 4] = (40, 78, 100); g[y - 1, x - 2:x + 1] = (146, 172, 88)
if T2:   # the wooden bridge: planks across with dark gaps, a rail (blocked) along both sides, its shadow on the water
    dy0, dy1 = np.nonzero(deck_a.any(1))[0][[0, -1]]; dx0, dx1 = np.nonzero(deck_a.any(0))[0][[0, -1]]
    g[water & ~deck_a & (mv(deck_a, 1) | mv(deck_a, 2) | mv(deck_a, 3))] = PAL['wp']
    WOOD = [np.array(c_, np.uint8) for c_ in ((168, 118, 70), (150, 102, 62), (134, 90, 56))]
    for x in range(dx0, dx1 + 1):
        i = x - dx0; t = WOOD[(i // 5 * 7 + i // 5 // 3) % 3]
        for y in range(dy0, dy1 + 1):
            c = t if i % 5 != 4 else np.array((78, 50, 40), np.uint8)
            if i % 5 != 4 and (i * 7 + y * 13) % 31 == 0: c = WOOD[2] - 14
            if y - dy0 < 2 or dy1 - y < 2: c = np.array(((186, 136, 82), (96, 62, 44))[(y - dy0) % 2 if y - dy0 < 2 else 1 - (dy1 - y)], np.uint8)
            g[y, x] = c
    for x in (dx0, dx0 + 24, dx0 + 49, dx1 - 2):                                   # posts
        for y0_ in (dy0 - 1, dy1 - 2):
            g[y0_:y0_ + 3, x:x + 3] = (112, 74, 50); g[y0_, x:x + 3] = (196, 148, 92); g[y0_ + 3, x:x + 3] = (60, 40, 36)
# -- 3. plateaus: the top in a slightly sunnier set of tones, a wall of rock columns under it, the cover hanging over the wall
top = tones(PAL['top'], lv + F6); g[up_a] = top[up_a]; cov[up_a] = 3 if T3 else 0
if T2: g[up_a & lm] = tones(PAL['leaf'], lo(N40) * .6 + wide(10, 18) * .4 + F6, (.30, .22, .88))[up_a & lm]; cov[up_a & lm] = 1
g[up_a & n4(~up_a)] = PAL['rim']                                            # sunlit rim
g[~up_a & n4(up_a) & ~face_a & ~ramp_a] = PAL['out']                        # the far edge of the top against the low ground behind
fd = runpos(face_a)                                                        # 1 on the first wall row under the top, counting down
cb = np.cumsum(RG.integers(7, 15, GW // 7 + 2)); ci = np.searchsorted(cb, gx[0], side='right')      # rock columns 7-14 px wide
split = RG.integers(8, 20, ci.max() + 1)[ci][None, :]; jog = RG.integers(-2, 3, ci.max() + 1); lowt = RG.integers(1, 3, ci.max() + 1)[ci][None, :]
upt = (RG.random(ci.max() + 1) < .3).astype(int)[ci][None, :]
ki = np.where(fd <= split, upt, lowt); ki = np.where(fd > 26, 3, ki)        # a lighter upper facet, a darker lower one, a dark base
g[face_a] = np.array(PAL['k'])[ki][face_a]
g[face_a & (fd == split + 1) & (RG.random(ci.max() + 1) < .6)[ci][None, :]] = PAL['kj']             # the ledge between two facets
crack = np.zeros((GH, GW), bool)
for c_ in range(1, ci.max() + 1):                                           # cracks between the columns, jogging at the ledge
    x0_ = int(cb[c_ - 1]); x1_ = min(GW - 1, max(0, x0_ + int(jog[c_])))
    if x0_ + 2 < GW: crack[:, x0_] |= fd[:, x0_] <= split[0, x0_]; crack[:, x1_] |= fd[:, x1_] > split[0, x0_]
g[face_a & crack] = PAL['kj']
g[face_a & n4(~(face_a | up_a | ramp_a))] = PAL['ko']
flive = blades(face_a & ~ramp_a, up_a, .6, 3)
g[flive & mv(~flive & (up_a | face_a), 1) & face_a] = PAL['ko']             # the shadow line under the overhanging cover
r6 = (runpos(ramp_a) - 1) % 6                                               # stairs, steps 6 px tall: a lit edge, the tread, a darker riser, a shadow line
g[ramp_a] = PAL['sm']; g[ramp_a & (r6 == 0)] = PAL['sl']; g[ramp_a & (r6 >= 3)] = PAL['sd']; g[ramp_a & (r6 == 5)] = PAL['so']
g[ramp_a & ~(mv(ramp_a, 0, 1) & mv(ramp_a, 0, -1))] = PAL['so']
# -- 4. bold flat shadows: under every prop (the same ellipses as before) and at the foot of the walls
shd = (lo(SHAD) & ~face_a & ~ramp_a & ~deck_a) | lo(FOOT)
shd |= n4(shd) & (RG.random((GH, GW)) < .22) & ~face_a & ~ramp_a & ~deck_a                # a few teeth on the edge
g[shd & ~water] = shade(g[shd & ~water]); g[shd & water] = (g[shd & water] * np.array((.7, .74, .82))).astype(np.uint8)
# -- 5. small life on the soft ground (never on road / water / walls / stairs, not under a blocking prop)
def stamp(rows, key, x, y, outline=None):     # a tiny hand-drawn sprite; (x, y) = the middle of its bottom row
    h_, w_ = len(rows), len(rows[0]); x0, y0 = x - w_ // 2, y - h_ + 1
    full = lambda j, i: 0 <= j < h_ and 0 <= i < w_ and rows[j][i] != '.'
    for j in range(-1, h_ + 1):
        for i in range(-1, w_ + 1):
            if full(j, i): g[y0 + j, x0 + i] = key[rows[j][i]]
            elif outline is not None and (full(j + 1, i) or full(j - 1, i) or full(j, i + 1) or full(j, i - 1)): g[y0 + j, x0 + i] = outline
okd = ndimage.binary_erosion(soft2, iterations=3) & ~lo(blk) & (gx > 8) & (gx < GW - 9) & (gy > 14) & (gy < GH - 6)
TUFTS = (("a..a..a", ".a.a.a.", ".a.a.a."), ("a...a", ".a.a.", ".a.a."), ("..a..", "a.a.a", "a.a.a"), ("...a...", "a..a..a", ".a.a.a.", ".a.a.a."))
BIGTUFTS = ((".a...a...a.", ".a.a.a.a.a.", "..aa.a.aa..", "..bbabbab.."), ("a...a..a.", "a.a.a.a..", ".aa.aa.a.", ".babbabb."), ("..a...a..", "a.a.a.a.a", ".aababaa.", "..bbbbb.."))
STONES = ((".LLM.", "LLMMD", "MMMDD"), (".LL.", "LMMD", "MMDD"), ("LLM", "MDD"), (".LL....", "LLMM.LM", "MMMD.MD"))
SKEY = {'L': PAL['pl'], 'M': PAL['pm'], 'D': PAL['pd']}
LIGHTER = {}; DARKER = {}
for p_ in ('soft', 'top', 'dead'):
    if p_ in PAL:
        LIGHTER.update({tuple(PAL[p_][0]): PAL[p_][3], tuple(PAL[p_][1]): PAL[p_][0], tuple(PAL[p_][2]): PAL[p_][1], tuple(PAL[p_][3]): PAL['tl']})
        DARKER.update({tuple(PAL[p_][0]): PAL[p_][1], tuple(PAL[p_][1]): PAL[p_][2], tuple(PAL[p_][3]): PAL[p_][0]})
grassy = okd & ((cov == 0) | (cov == 3))
for x, y in spots(grassy & ~shd, int(grassy.sum()) // 1500, 8):             # brushed light dashes, 2-3 stacked
    c = LIGHTER.get(tuple(g[y, x]))
    if c is None: continue
    for j in range(RR.randint(2, 3)):
        x0 = x + RR.randint(-2, 2); L = RR.randint(3, 5)
        for i in range(L):
            if grassy[y - j * 2, x0 + i]: g[y - j * 2, x0 + i] = c
for x, y in spots(grassy & ~shd & ndimage.binary_erosion(okd, iterations=4), int(grassy.sum()) // 5200, 30):    # darker grass clumps with a spiky top
    c = DARKER.get(tuple(g[y, x])); w_ = RR.randint(4, 7)
    if c is None: continue
    for i in range(-w_, w_ + 1):
        for j in range(max(1, round((1 - (i / (w_ + .5)) ** 2) ** .5 * w_ * .5) + RR.randint(0, 2) - i % 2)): g[y - j, x + i] = c
    for i in range(-w_ + 1, w_, 3): g[y - RR.randint(0, 1), x + i] = PAL['td']
    stamp(RR.choice(TUFTS), {'a': PAL['tl']}, x + RR.randint(-2, 2), y - 2)
for x, y in spots(grassy, int(grassy.sum()) // 360, 7):                     # tufts: light or dark blades, mid green in the shade
    c = PAL['ts'] if shd[y, x] else PAL['tl'] if RR.random() < .62 else PAL['td']
    if RR.random() < .22 and not shd[y, x]: stamp(RR.choice(BIGTUFTS), {'a': PAL['tl'], 'b': PAL['td']}, x, y)
    else: stamp(RR.choice(TUFTS), {'a': c}, x, y)
if not T3:   # tufts standing at the lower edge of the road, their blades over it
    under = oe & mv(vroad2, 1) & (gx > 8) & (gx < GW - 9) & ~shd
    for x, y in spots(under, int(under.sum()) // 9, 8): stamp(RR.choice(TUFTS), {'a': PAL['tl'] if RR.random() < .7 else PAL['soft'][0]}, x, y)
if T2:   # fallen leaves (single ones, also out on the grass), a few mushrooms
    LEAFC = [np.array(c_, np.uint8) for c_ in ((182, 62, 40), (226, 134, 48), (238, 196, 84), (132, 70, 44), (206, 96, 44))]
    LEAVES = (("ab.", ".aa"), ("a.", "aa", ".b"), (".aa", "ab."), ("ab", "a."), ("aa", ".b"))
    BIGLEAVES = ((".aa.", "aaab", ".ab."), ("aa..", "aaab", ".aab"), ("..aa", "baaa", "baa."), (".a.", "aaa", "aab", ".b."))
    LK = {tuple(PAL['leaf'][0]): (PAL['leaf'][3], PAL['leaf'][1]), tuple(PAL['leaf'][1]): (PAL['leaf'][0], PAL['leaf'][2]), tuple(PAL['leaf'][3]): (PAL['leaf'][0], np.array((244, 200, 96), np.uint8))}
    carpet = okd & (cov == 1)
    for x, y in spots(carpet, int(carpet.sum()) // 85, 5):                  # leaf shapes in the neighbouring tones: the carpet reads as leaves
        c = LK.get(tuple(g[y, x]))
        if c is not None: c = RR.choice(c); stamp(RR.choice(BIGLEAVES + LEAVES), {'a': c, 'b': (c * .8).astype(np.uint8)}, x, y)
    for x, y in spots(okd & (cov != 1), int((okd & (cov != 1)).sum()) // 300, 4):          # single leaves out on the grass
        c = RR.choice(LEAFC)
        if shd[y, x]: c = shade(c.astype(float) * 1.5)
        stamp(RR.choice(LEAVES), {'a': c, 'b': (c * .72).astype(np.uint8)}, x, y)
    for x, y in spots(okd & ~shd, 16, 30):
        stamp((".RRR.", "RWRRR", "RRRWR", ".CC.."), {'R': (196, 60, 44), 'W': (240, 232, 210), 'C': (226, 208, 170)}, x, y, PAL['out'])
if not T3:   # daisies in small clusters (map 2: fewer, cream)
    DK = {'W': (243, 242, 223), 'w': (196, 198, 172), 'Y': (236, 172, 62), 's': PAL['out'], 'l': (52, 82, 56)}
    if T2: DK.update(W=(246, 232, 190), w=(206, 186, 140), Y=(214, 110, 50))
    BIG = ("..WWW..", "W.WWW.W", "WWYYYWW", "WWYYYWw", ".WW.ww.", ".WW.ww."); MED = ("WW.WW", "WWWWW", ".WYW.", "WWWww", "WW.ww"); SML = (".W.", "WYW", ".w.")
    for x, y in spots(grassy & ndimage.binary_erosion(okd, iterations=5), 22 if T2 else 76, 24):
        for k in range(RR.choice((1, 1, 2, 2, 3, 3, 4))):
            X, Y = x + RR.randint(-9, 9) * (k > 0), y + RR.randint(-5, 5) * (k > 0); d = RR.choice((BIG, MED, MED, SML))
            if not okd[Y, X]: continue
            if d is not SML: stamp(("...s...", ".l.s.l.", "lllslll", ".ll.ll.") if d is BIG else ("..s..", "l.s.l", "lllll"), DK, X, Y + (4 if d is BIG else 3))
            stamp(d, DK, X, Y, PAL['out'])
for x, y in spots(okd, 70 if T3 else 44, 22): stamp(RR.choice(STONES), SKEY, x, y, PAL['po'])        # small stones
if T3:   # cracks in the rock slabs and the dry dirt
    for x, y in spots(okd & (cov != 3), 150, 12):
        c = PAL['out'] if cov[y, x] == 2 else PAL['soft'][2]
        for k in range(RR.randint(5, 10)):
            if 0 < x < GW and 0 < y < GH and okd[y, x] and cov[y, x] != 3: g[y, x] = c
            x += RR.choice((1, 1, 1, 0)); y += RR.choice((-1, 0, 0, 1, 1))
# -- 6. the boulders along the rim of the walls: grey stones with a dark outline, some with moss on top
for (x, y, r), moss in zip(BOULDERS, MOSSY):
    cx, cy, ra = x // 2, y // 2, max(2, round(r / 2)); px = ell(cx, cy, ra, ra - 1); s_ = set(px)
    for q in ell(cx, cy, ra + 1, ra): g[q] = PAL['po']
    for qy, qx in px: g[qy, qx] = PAL['pd'] if qy - cy > ra * .35 or qx - cx > ra * .7 else PAL['pm']
    for q in ell(cx - 1, cy - 1, ra - 1.6, ra - 2.2):
        if q in s_: g[q] = PAL['moss'] if moss else PAL['pl']
ground = Image.fromarray(g).resize((W, H), Image.NEAREST); ground.save(OUT + 'ground.png', optimize=True)

# ---- olive grade (Dimraeth) for the PROPS only: soften saturation, warm, greens toward olive, lifted darks (the ground is
# painted in its final colours)
def grade(a, k=1.0):
    a = a.astype(float); c = a[..., :3]; g = c.mean(2, keepdims=True)
    o = g + (c - g) * .68
    gr = np.clip((o[..., 1] - np.maximum(o[..., 0], o[..., 2])) / 50, 0, 1); o[..., 0] += gr * 30; o[..., 1] -= gr * 6; o[..., 2] -= gr * 4
    o[..., 0] *= 1.03; o[..., 2] *= .88; o = o * .92 + 9
    if T3:   # cold night-ish grade: greyer, blue in the darks, a little darker
        g = o.mean(2, keepdims=True); o = g + (o - g) * .72; o[..., 0] *= .9; o[..., 1] *= .97; o[..., 2] *= 1.16; o = o * .93 + np.array([2, 5, 12])
    a[..., :3] = c + (o - c) * k; return np.clip(a, 0, 255).astype(np.uint8)

# ---- walk mask: water, cliff faces, the drop round a plateau top (except stairs), props, map border
drop = dil(UP, 4) & ~UP & ~FACE & ~RAMP
blk |= pond | (FACE & ~RAMP) | drop
if T2: blk |= RAIL
blk0 = blk.copy()
blk[:, :56] = blk[:, -56:] = True; blk[:140] = True; blk[-46:] = True
EXITS = [{'x0': W - 60, 'y0': 700, 'x1': W, 'y1': 860, 'to': 'td2', 'label': 'ป่าใบไม้แดง →'}] if not T2 else [{'x0': 0, 'y0': 700, 'x1': 60, 'y1': 840, 'to': 'td1', 'label': '← ป่าเนินผา'}]
ENTRIES = {'td2': [W - 100, 785]} if not T2 else {'td1': [100, 770]}
if T3: EXITS = [{'x0': 0, 'y0': 540, 'x1': 60, 'y1': 680, 'to': 'td2', 'label': '← ป่าใบไม้แดง'}]; ENTRIES = {'td2': [100, 606]}
for e in EXITS: gap = road & (xx >= e['x0'] - 8) & (xx < e['x1']) & (yy >= e['y0']) & (yy < e['y1']); blk[gap] = False   # open the border where the road leaves
if T2:   # the south road stops just short of the east edge (the ground is not redrawn: td.html uses it): open the border there
    e = {'x0': W - 60, 'y0': 850, 'x1': W, 'y1': 950, 'to': 'td3', 'label': 'สุสานซากหิน →'}; EXITS.append(e); ENTRIES['td3'] = [W - 100, 900]
    gap = (xx >= e['x0'] - 12) & (yy >= e['y0']) & (yy < e['y1']); blk[gap] = blk0[gap]
blk = ndimage.binary_opening(blk, iterations=1) | pond
Image.fromarray((blk[::2, ::2] * 255).astype(np.uint8)).save(OUT + 'block.png', optimize=True)

# ---- props atlas
keys = list(SPR) if not T3 else [k for k in SPR if any(p['s'] == k for p in PROPS)]; at = []; X = Y = rowh = 0; AW = 2048
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
# the old hero sheets were removed 2026-11-13 (owner: old characters out); map.html draws the chibi swordsman from hero_chibi*.png (tools/art/chibi_map_hero.py)
hero = {'c': 79, 'fx': 39, 'fy': 67, 'dirs': ['east', 'south-east', 'south', 'south-west', 'west', 'north-west', 'north', 'north-east']}
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
J = {'w': W, 'h': H, 'start': [100, 606] if T3 else [120, 770] if T2 else [200, 705], 'props': props, 'hero': hero, 'mobs': mobs, 'spawn': SPW, 'bk': 2,
     'exits': EXITS, 'entries': ENTRIES}
if T3:
    J['hpk'] = 1.8                                         # map.html: monster HP / damage / XP multiplier of this zone
    for k_, x_, y_ in SPW:
        if blk[y_, x_]: print('  spawn on a blocked spot', k_, x_, y_)
json.dump(J, open(OUT + 'map.json', 'w'))
# preview of the whole map
pv = ground.convert('RGBA')
for p in sorted(PROPS, key=lambda p: (p['over'], p['y'])):
    x, y, w, h = pos[p['s']]; pv.alpha_composite(atlas.crop((x, y, x + w, y + h)), (int(p['x'] - w / 2), int(p['y'] - h)))
pv.convert('RGB').save('art/td/%s_preview.png' % ('map3' if T3 else 'map2' if T2 else 'map1'))
print('ok', len(PROPS), 'props', atlas.size, 'boulders', len(BOULDERS))
