# Lucky-Defense-style board mock for dogs vs cats (owner 2026-11-12 "เป็นแมพแบบ lucky defense"): free, no jobs.
# A portrait phone screen (390 x 844): two boards stacked (top = the opponent, bottom = you); each board is a 6 x 3 grid of
# stone slots inside a dirt loop that the monsters walk round and round; summon / upgrade buttons at the bottom.
#   python3 tools/art/tw_ld_mock.py -> art/incoming/dogcat/tw_ld_mock.png (x2)
import json, random, sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage
random.seed(9); np.random.seed(9)
W, H = 390, 844; D = 'art/td/tiles/'; P2 = 'art/td/props/set2/cut/'; OUT = 'art/incoming/dogcat/'
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
BOARDS = [(46, 'top'), (466, 'me')]          # board top edges
BW, BH, PW = 358, 300, 30                     # board size, loop width
X0 = (W - BW) // 2
def rrect(x0, y0, x1, y1, r):
    cx = np.clip(xx, x0 + r, x1 - r); cy = np.clip(yy, y0 + r, y1 - r); return np.hypot(xx - cx, yy - cy) <= r
road = np.zeros((H, W), bool); LOOPS = []
for y0, who in BOARDS:
    outer = rrect(X0, y0, X0 + BW, y0 + BH, 26); inner = rrect(X0 + PW, y0 + PW, X0 + BW - PW, y0 + BH - PW, 10)
    road |= outer & ~inner
    # the loop's middle line, for placing the walkers
    a, b, c, d = X0 + PW / 2, y0 + PW / 2, X0 + BW - PW / 2, y0 + BH - PW / 2
    per = 2 * (c - a + d - b); pts = []
    for s in np.linspace(0, per, 400, endpoint=False):
        if s < c - a: pts.append((a + s, b))
        elif s < c - a + d - b: pts.append((c, b + s - (c - a)))
        elif s < 2 * (c - a) + d - b: pts.append((c - (s - (c - a + d - b)), d))
        else: pts.append((a, d - (s - (2 * (c - a) + d - b))))
    LOOPS.append(pts)
img[road] = DR[road]
rim = road ^ ndimage.binary_dilation(road, iterations=2); img[rim] = img[rim] * .68 + np.array([60, 96, 36]) * .32
inn = ndimage.binary_erosion(road, iterations=1) ^ road; img[inn & road] *= .8
base = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert('RGBA'); dr = ImageDraw.Draw(base)
for _ in range(500):
    x, y = random.randrange(2, W - 2), random.randrange(2, H - 2)
    if road[y, x]: continue
    if random.random() < .6: c = random.choice([(52, 116, 44), (118, 178, 72)]); dr.line((x, y, x, y - random.randint(2, 4)), fill=c)
    else: dr.rectangle((x, y, x + 1, y + 1), fill=random.choice([(250, 236, 120), (240, 140, 170), (255, 255, 255)]))
# slots: 6 x 3 stone tiles inside each loop
CW, CHh = 46, 62
def fit(f, h, flip=False):
    im = Image.open(f).convert('RGBA'); im = im.crop(im.getbbox()); k = h / im.height
    im = im.resize((max(1, round(im.width * k)), h), Image.LANCZOS); a = np.asarray(im).copy(); a[..., 3] = (a[..., 3] > 110) * 255; im = Image.fromarray(a)
    return im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im
SB = Image.open(OUT + 'shiba_px64_front.png').convert('RGBA'); k = 46 / SB.height; SB = SB.resize((round(SB.width * k), 46), Image.LANCZOS)
a = np.asarray(SB).copy(); a[..., 3] = (a[..., 3] > 110) * 255; SB = Image.fromarray(a)
grey = np.asarray(SB).astype(float).copy(); g = grey[..., :3].mean(2, keepdims=True); grey[..., :3] = g * np.array([.95, .97, 1.08]) * 1.05; GREY = Image.fromarray(np.clip(grey, 0, 255).astype(np.uint8))
items = []
for (y0, who), pts in zip(BOARDS, LOOPS):
    gx = X0 + (BW - 6 * CW) // 2; gy = y0 + (BH - 3 * CHh) // 2 + 4
    occ = {(0, 1), (1, 1), (2, 0), (2, 2), (3, 1), (4, 0), (5, 2), (1, 2), (4, 2)} if who == 'me' else {(0, 0), (1, 2), (3, 1), (4, 1), (5, 0), (2, 1)}
    for c in range(6):
        for r in range(3):
            x, y = gx + c * CW, gy + r * CHh
            dr.rounded_rectangle((x + 3, y + 3, x + CW - 3, y + CHh - 3), 6, fill=(60, 52, 44, 255))
            dr.rounded_rectangle((x + 4, y + 4, x + CW - 4, y + CHh - 6), 6, fill=(160, 150, 132, 255) if who == 'me' else (142, 136, 128, 255))
            dr.line((x + 8, y + 6, x + CW - 8, y + 6), fill=(206, 198, 180, 255))
            if (c, r) in occ: items.append((y + CHh - 6, SB if who == 'me' else GREY, x + CW // 2 - SB.width // 2))
    # monsters on the loop
    for i in range(0, 400, 17 if who == 'me' else 23):
        px, py = pts[(i + (0 if who == 'me' else 50)) % 400]; k2 = random.choice(['shroom', 'wisp', 'wolf'])
        m = json.load(open('art/action/mobs_hr/%s.json' % k2)); im = Image.open('art/action/mobs_hr/%s.png' % k2).crop((0, 0, m['w'], m['h'])); im = im.crop(im.getbbox())
        h = 22 if k2 != 'wolf' else 24; kk = h / im.height; im = im.resize((round(im.width * kk), h), Image.LANCZOS); a = np.asarray(im).copy(); a[..., 3] = (a[..., 3] > 110) * 255
        nx, ny = pts[(i + 5 + (0 if who == 'me' else 50)) % 400]; im = Image.fromarray(a); im = im if nx >= px else im.transpose(Image.FLIP_LEFT_RIGHT)
        items.append((int(py) + 8, im, int(px) - im.width // 2))
# small trees / rocks in the margins and the middle strip
for x, y, n, h in ((10, 470, 'trees_green_1', 70), (380, 470, 'trees_green_3', 64), (12, 46, 'trees_green_0', 62), (378, 48, 'trees_green_2', 60),
                   (40, 432, 'bushes_1', 20), (350, 436, 'bushes_6', 20), (200, 440, 'stones_0', 12)):
    items.append((y, fit(P2 + n + '.png', h, random.random() < .5), x - 20))
sh = Image.new('RGBA', base.size); sd = ImageDraw.Draw(sh)
for y, im, x in items: sd.ellipse((x + im.width * .15, y - 3, x + im.width * .85, y + 3), fill=(10, 24, 8, 90))
base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(1)))
for y, im, x in sorted(items, key=lambda t: t[0]): base.alpha_composite(im, (x, y - im.height))
# HUD
hd = ImageDraw.Draw(base); F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13); FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
def bar(y, txt, col):
    hd.rounded_rectangle((8, y, W - 8, y + 26), 7, fill=(30, 24, 30, 225), outline=(250, 236, 200), width=2); hd.text((16, y + 5), txt, fill=col, font=F)
bar(10, 'CATS  (opponent)      monsters 31/100', (255, 210, 230))
hd.rounded_rectangle((8, 360, W - 8, 452), 10, fill=(30, 24, 30, 200), outline=(250, 236, 200), width=2)
hd.text((20, 368), 'WAVE 12      00:24', fill=(250, 240, 210), font=FB); hd.text((20, 392), 'monsters 47/100', fill=(255, 140, 140), font=F)
hd.rectangle((20, 412, 370, 422), fill=(60, 40, 40)); hd.rectangle((20, 412, 20 + int(350 * .47), 422), fill=(230, 80, 80))
hd.text((20, 428), 'DOGS  (you)', fill=(255, 220, 140), font=F)
hd.rounded_rectangle((8, 776, W - 8, 836), 10, fill=(30, 24, 30, 225), outline=(250, 236, 200), width=2)
for i, (t, c, col) in enumerate((('SUMMON', '20', (250, 200, 60)), ('UPGRADE', '50', (120, 200, 250)), ('LUCKY', '1', (200, 140, 250)))):
    x = 16 + i * 122; hd.rounded_rectangle((x, 784, x + 114, 828), 8, fill=col, outline=(30, 20, 18), width=2)
    hd.text((x + 10, 788), t, fill=(30, 20, 18), font=FB); hd.text((x + 10, 808), '@ ' + c, fill=(30, 20, 18), font=F)
hd.text((300, 752), 'gold 140', fill=(255, 220, 120), font=F)
base.resize((W * 2, H * 2), Image.NEAREST).save(OUT + 'tw_ld_mock.png'); print('ok')
