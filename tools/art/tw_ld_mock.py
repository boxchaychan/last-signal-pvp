# Lucky-Defense-style board mock for dogs vs cats (owner 2026-11-12 "เป็นแมพแบบ lucky defense"): free, no jobs.
# A portrait phone screen (390 x 844): two boards stacked (top = the opponent, bottom = you); each board is a 6 x 3 grid of
# stone slots inside a dirt loop that the monsters walk round and round; summon / upgrade buttons at the bottom.
#   python3 tools/art/tw_ld_mock.py -> art/incoming/dogcat/tw_ld_mock.png (x2)
# Zoomed out (owner 2026-11-12 "ทำให้มันดูเล็กโดยซูมออก"): ZO=1.5 python3 tools/art/tw_ld_mock.py -> tw_ld_mock_zo1.5.png: the screen
# holds 1.5x more world (585 x 1266, = a 3x phone at x2 instead of x3); the layout, pedestals and HUD grow by ZO, the characters,
# monsters, props and stone blocks stay at their own pixel size, so they look smaller on the same phone.
import json, os, random, sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage
random.seed(9); np.random.seed(9)
Z = float(os.environ.get('ZO', '1')); z = lambda v: int(round(v * Z))
W, H = z(390), z(844); D = 'art/td/tiles/'; P2 = 'art/td/props/set2/cut/'; OUT = 'art/incoming/dogcat/'
yy, xx = np.mgrid[0:H, 0:W]
def tex(k, lower):
    m = json.load(open(D + k + '_meta.json'))['tileset_data']['tiles']; im = Image.open(D + k + '.png').convert('RGB')
    for t in m:
        if all((t['corners'][q] == 'lower') == lower for q in t['corners']):
            b = t['bounding_box']; return im.crop((b['x'], b['y'], b['x'] + 32, b['y'] + 32))
def tile_fill(t):
    o = Image.new('RGB', (W, H))
    for y in range(0, H, 32):
        for x in range(0, W, 32): o.paste(t.transpose(random.choice([Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM, Image.ROTATE_180])) if random.random() < .5 else t, (x, y))
    return np.asarray(o).astype(float)
def noise(c):
    n = np.random.rand(H // c + 2, W // c + 2)
    return np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize(((W // c + 2) * c, (H // c + 2) * c), Image.BICUBIC)).astype(float)[:H, :W] / 255
N8, N40 = noise(8), noise(40)
G = tile_fill(tex('path_pro', False)); DR = tile_fill(tex('path_pro', True))
img = G.copy(); img[N40 < .35] *= .9; lt = N40 > .65; img[lt] = img[lt] * 1.07 + np.array([10, 6, -4])
BOARDS = [(z(46), 'top'), (z(434), 'me')]          # board top edges
BW, BH, PW = z(380), z(278), z(30)   # owner "ทำให้มันสมส่วนหน่อย": units fill their slots, monsters ~2/3 of a unit, a tighter loop                     # board size, loop width
X0 = (W - BW) // 2
def rrect(x0, y0, x1, y1, r):
    cx = np.clip(xx, x0 + r, x1 - r); cy = np.clip(yy, y0 + r, y1 - r); return np.hypot(xx - cx, yy - cy) <= r
road = np.zeros((H, W), bool); plat = np.zeros((H, W), bool); floor = np.zeros((H, W), bool); LOOPS = []
for y0, who in BOARDS:
    outer = rrect(X0, y0, X0 + BW, y0 + BH, z(26)); inner = rrect(X0 + PW, y0 + PW, X0 + BW - PW, y0 + BH - PW, z(10))
    road |= outer & ~inner; plat |= outer; floor |= inner
    # the loop's middle line, for placing the walkers
    a, b, c, d = X0 + PW / 2, y0 + PW / 2, X0 + BW - PW / 2, y0 + BH - PW / 2
    per = 2 * (c - a + d - b); pts = []
    for s in np.linspace(0, per, 400, endpoint=False):
        if s < c - a: pts.append((a + s, b))
        elif s < c - a + d - b: pts.append((c, b + s - (c - a)))
        elif s < 2 * (c - a) + d - b: pts.append((c - (s - (c - a + d - b)), d))
        else: pts.append((a, d - (s - (2 * (c - a) + d - b))))
    LOOPS.append(pts)
# owner 2026-11-12 "ทำพื้นเป็นบล็อกหิน": the board is a raised stone platform: grey cobble blocks for the loop, light sandstone
# slabs (lined up with the slot grid) for the middle, a stone wall face under the front edge, a low step where the middle meets the road
sys.path.insert(0, 'tools/art'); from stone_px import blocks
def down(m, n):
    o = np.zeros_like(m)
    for k in range(1, n + 1): o[k:] |= m[:-k]
    return o
ROAD = blocks(H, W, 14, 10, [(132, 134, 146), (118, 122, 136), (146, 146, 152), (124, 118, 126)], seed=3, moss=.07)
FLOOR = blocks(H, W, 26, 20, [(204, 190, 160), (194, 178, 148), (212, 200, 172), (186, 172, 146)], seed=5, bond=False, lip=1, x0=13, mortar=(120, 104, 90))
STEP = blocks(H, W, 13, 5, [(150, 134, 112), (140, 124, 104)], seed=6, lip=0, mortar=(84, 70, 62))
WALL = blocks(H, W, 16, 9, [(96, 98, 112), (86, 88, 102), (104, 102, 112)], seed=7, lip=0, mortar=(38, 34, 42), moss=.12)
wall = down(plat, 9) & ~plat; step = down(floor, 4) & road & ~floor
img[road] = ROAD[road]; img[floor] = FLOOR[floor]; img[step] = STEP[step]; img[wall] = WALL[wall]
edge = floor ^ ndimage.binary_erosion(floor, iterations=1); img[edge & ~down(floor, 1)] *= .72      # the middle's rim, not its bottom
ped = plat ^ ndimage.binary_erosion(plat, iterations=1); img[ped] *= .7
img[down(wall, 1) & ~wall & ~plat] = (40, 36, 44)                                                    # the wall's foot
sh = down(plat | wall, 5) & ~plat & ~wall; img[sh] *= .7                                              # its shadow on the grass
rim = (plat | wall) ^ ndimage.binary_dilation(plat | wall, iterations=2); img[rim & ~sh] = img[rim & ~sh] * .78 + np.array([40, 70, 30]) * .22
road = plat | wall
base = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert('RGBA'); dr = ImageDraw.Draw(base)
for _ in range(z(z(500))):
    x, y = random.randrange(2, W - 2), random.randrange(2, H - 2)
    if road[y, x]: continue
    if random.random() < .6: c = random.choice([(52, 116, 44), (118, 178, 72)]); dr.line((x, y, x, y - random.randint(2, 4)), fill=c)
    else: dr.rectangle((x, y, x + 1, y + 1), fill=random.choice([(250, 236, 120), (240, 140, 170), (255, 255, 255)]))
# slots: 6 x 3 stone tiles inside each loop
CW, CHh = z(52), z(70)
def fit(f, h, flip=False):
    im = Image.open(f).convert('RGBA'); im = im.crop(im.getbbox()); k = h / im.height
    im = im.resize((max(1, round(im.width * k)), h), Image.LANCZOS); a = np.asarray(im).copy(); a[..., 3] = (a[..., 3] > 110) * 255; im = Image.fromarray(a)
    return im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im
SB = Image.open(OUT + 'pl/char/Idle/rotations/south.png').convert('RGBA'); SB = SB.crop(SB.getbbox())   # the PixelLab character (2026-11-12), 1:1
a = np.asarray(SB).copy(); a[..., 3] = (a[..., 3] > 110) * 255; SB = Image.fromarray(a)
grey = np.asarray(SB).astype(float).copy(); g = grey[..., :3].mean(2, keepdims=True); grey[..., :3] = g * np.array([.95, .97, 1.08]) * 1.05; GREY = Image.fromarray(np.clip(grey, 0, 255).astype(np.uint8))
items = []
for (y0, who), pts in zip(BOARDS, LOOPS):
    gx = X0 + (BW - 6 * CW) // 2; gy = y0 + (BH - 3 * CHh) // 2
    occ = {(0, 1), (1, 1), (2, 0), (2, 2), (3, 1), (4, 0), (5, 2), (1, 2), (4, 2)} if who == 'me' else {(0, 0), (1, 2), (3, 1), (4, 1), (5, 0), (2, 1)}
    for c in range(6):
        for r in range(3):
            x, y = gx + c * CW, gy + r * CHh
            # a raised stone pedestal per slot: top face (4 small tiles) + a front face of 2 blocks
            P = Z ** .35                      # pedestals stay about the character's width when zoomed out (not x Z)
            fb = y + CHh - z(13); l, rr = x + CW // 2 - round(20 * P), x + CW // 2 + round(20 * P); t = fb - round(17 * P); tp = (150, 154, 168) if who == 'me' else (140, 140, 150)
            dr.rectangle((l - 1, t - 1, rr + 1, fb + round(8 * P) + 1), fill=(34, 30, 38))
            dr.rectangle((l, t, rr, fb), fill=tp); mx, my = (l + rr) // 2, (t + fb) // 2
            dr.line((l, t, rr, t), fill=tuple(min(255, int(v * 1.2)) for v in tp)); dr.line((l, t, l, fb), fill=tuple(int(v * 1.08) for v in tp))
            dr.line((mx, t + 1, mx, fb), fill=tuple(int(v * .7) for v in tp)); dr.line((l + 1, my, rr, my), fill=tuple(int(v * .7) for v in tp))
            dr.line((mx + 1, t + 1, mx + 1, fb), fill=tuple(min(255, int(v * 1.1)) for v in tp))
            fc = tuple(int(v * .62) for v in tp); dr.rectangle((l, fb + 1, rr, fb + round(8 * P)), fill=fc)
            dr.line((l, fb + 1, rr, fb + 1), fill=tuple(int(v * .8) for v in tp)); dr.line((mx - 3, fb + 2, mx - 3, fb + round(8 * P)), fill=(34, 30, 38))
            if (c, r) in occ: items.append(((t + fb) // 2 + 3, SB if who == 'me' else GREY, x + CW // 2 - SB.width // 2))
    # monsters on the loop
    for i in range(0, 400, 15 if who == 'me' else 21):
        px, py = pts[(i + (0 if who == 'me' else 50)) % 400]; k2 = random.choice(['shroom', 'wisp', 'wolf'])
        m = json.load(open('art/action/mobs_hr/%s.json' % k2)); im = Image.open('art/action/mobs_hr/%s.png' % k2).crop((0, 0, m['w'], m['h'])); im = im.crop(im.getbbox())
        h = 36 if k2 != 'wolf' else 38; kk = h / im.height; im = im.resize((round(im.width * kk), h), Image.LANCZOS); a = np.asarray(im).copy(); a[..., 3] = (a[..., 3] > 110) * 255
        nx, ny = pts[(i + 5 + (0 if who == 'me' else 50)) % 400]; im = Image.fromarray(a); im = im if nx >= px else im.transpose(Image.FLIP_LEFT_RIGHT)
        items.append((int(py) + 12, im, int(px) - im.width // 2))
# small trees / rocks in the margins and the middle strip
for x, y, n, h in ((30, 840, 'bushes_1', 26), (360, 842, 'bushes_6', 26), (200, 842, 'stones_0', 14)):
    items.append((z(y), fit(P2 + n + '.png', h, random.random() < .5), z(x) - 20))
sh = Image.new('RGBA', base.size); sd = ImageDraw.Draw(sh)
for y, im, x in items: sd.ellipse((x + im.width * .15, y - 3, x + im.width * .85, y + 3), fill=(10, 24, 8, 90))
base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(1)))
for y, im, x in sorted(items, key=lambda t: t[0]): base.alpha_composite(im, (x, y - im.height))
# HUD
hd = ImageDraw.Draw(base); F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', z(13)); FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', z(17))
def bar(y, txt, col):
    hd.rounded_rectangle((z(8), z(y), W - z(8), z(y + 26)), z(7), fill=(30, 24, 30, 225), outline=(250, 236, 200), width=z(2)); hd.text((z(16), z(y + 5)), txt, fill=col, font=F)
bar(10, 'CATS  (opponent)      monsters 31/100', (255, 210, 230))
hd.rounded_rectangle((z(8), z(332), W - z(8), z(426)), z(10), fill=(30, 24, 30, 200), outline=(250, 236, 200), width=z(2))
hd.text((z(20), z(340)), 'WAVE 12      00:24', fill=(250, 240, 210), font=FB); hd.text((z(20), z(364)), 'monsters 47/100', fill=(255, 140, 140), font=F)
hd.rectangle((z(20), z(384), z(370), z(394)), fill=(60, 40, 40)); hd.rectangle((z(20), z(384), z(20 + 350 * .47), z(394)), fill=(230, 80, 80))
hd.text((z(20), z(402)), 'DOGS  (you)', fill=(255, 220, 140), font=F)
hd.rounded_rectangle((z(8), z(748), W - z(8), z(808)), z(10), fill=(30, 24, 30, 225), outline=(250, 236, 200), width=z(2))
for i, (t, c, col) in enumerate((('SUMMON', '20', (250, 200, 60)), ('UPGRADE', '50', (120, 200, 250)), ('LUCKY', '1', (200, 140, 250)))):
    x = 16 + i * 122; hd.rounded_rectangle((z(x), z(756), z(x + 114), z(800)), z(8), fill=col, outline=(30, 20, 18), width=z(2))
    hd.text((z(x + 10), z(760)), t, fill=(30, 20, 18), font=FB); hd.text((z(x + 10), z(780)), '@ ' + c, fill=(30, 20, 18), font=F)
hd.text((z(300), z(724)), 'gold 140', fill=(255, 220, 120), font=F)
base.resize((W * 2, H * 2), Image.NEAREST).save(OUT + ('tw_ld_mock.png' if Z == 1 else 'tw_ld_mock_zo%g.png' % Z)); print('ok', W, H)
