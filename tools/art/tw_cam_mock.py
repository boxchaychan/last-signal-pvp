# Dogs vs cats: one Lucky-Defense-style board seen from 4 camera angles, side by side (owner 2026-11-12
# "ลองใช้มุมกล้องหลายๆแบบให้ฉันเทียบดู"). Free, no jobs. The ground is painted flat (seen from straight above) in world units,
# then each camera squashes / turns it; the characters always stand upright at their own pixel size (60 px), only their feet
# move with the camera. Slots are drawn after the camera as stone discs with a front face (thicker when the camera is lower).
#   python3 tools/art/tw_cam_mock.py -> art/incoming/dogcat/tw_cam_mock.png (x2)
import json, math, random, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
random.seed(4); np.random.seed(4)
D = 'art/td/tiles/'; P2 = 'art/td/props/set2/cut/'; OUT = 'art/incoming/dogcat/'
WW, WH = 390, 252                                  # the board in world units (1 unit = 1 screen px across)
GX, GY, CS = 51, 54, 48                            # 6 x 3 grid of 48-unit cells
LO = (15, 18, 375, 234); RW = 28                   # the loop road's outer edge and width
def tex(k, lower):
    m = json.load(open(D + k + '_meta.json'))['tileset_data']['tiles']; im = Image.open(D + k + '.png').convert('RGB')
    for t in m:
        if all((t['corners'][q] == 'lower') == lower for q in t['corners']):
            b = t['bounding_box']; return im.crop((b['x'], b['y'], b['x'] + 32, b['y'] + 32))
def tile_fill(t, w, h):
    o = Image.new('RGB', (w, h))
    for y in range(0, h, 32):
        for x in range(0, w, 32): o.paste(t.transpose(random.choice([Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM, Image.ROTATE_180])) if random.random() < .5 else t, (x, y))
    return np.asarray(o).astype(float)
# --- the flat world ground (with a wide grass margin so turned cameras never show an edge)
M = 360; FW, FH = WW + 2 * M, WH + 2 * M
yy, xx = np.mgrid[0:FH, 0:FW]
def rrect(x0, y0, x1, y1, r):
    x0 += M; x1 += M; y0 += M; y1 += M
    cx = np.clip(xx, x0 + r, x1 - r); cy = np.clip(yy, y0 + r, y1 - r); return np.hypot(xx - cx, yy - cy) <= r
G = tile_fill(tex('path_pro', False), FW, FH); DR = tile_fill(tex('path_pro', True), FW, FH)
n40 = np.asarray(Image.fromarray((np.random.rand(FH // 40 + 2, FW // 40 + 2) * 255).astype(np.uint8)).resize(((FW // 40 + 2) * 40, (FH // 40 + 2) * 40), Image.BICUBIC)).astype(float)[:FH, :FW] / 255
img = G.copy(); img[n40 < .35] *= .9; lt = n40 > .65; img[lt] = img[lt] * 1.07 + np.array([10, 6, -4])
road = rrect(*LO, 24) & ~rrect(LO[0] + RW, LO[1] + RW, LO[2] - RW, LO[3] - RW, 8)
img[road] = DR[road]
rim = road ^ ndimage.binary_dilation(road, iterations=2); img[rim] = img[rim] * .68 + np.array([60, 96, 36]) * .32
inn = ndimage.binary_erosion(road, iterations=1) ^ road; img[inn & road] *= .8
GROUND = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert('RGBA'); gd = ImageDraw.Draw(GROUND)
for _ in range(4200):
    x, y = random.randrange(2, FW - 2), random.randrange(2, FH - 2)
    if road[y, x]: continue
    if random.random() < .6: gd.rectangle((x, y, x, y + 1), fill=random.choice([(52, 116, 44), (118, 178, 72)]))
    else: gd.rectangle((x, y, x + 1, y + 1), fill=random.choice([(250, 236, 120), (240, 140, 170), (255, 255, 255)]))
# loop middle line (world units)
a, b, c, d = LO[0] + RW / 2, LO[1] + RW / 2, LO[2] - RW / 2, LO[3] - RW / 2
per = 2 * (c - a + d - b); LOOP = []
for s in np.linspace(0, per, 400, endpoint=False):
    if s < c - a: LOOP.append((a + s, b))
    elif s < c - a + d - b: LOOP.append((c, b + s - (c - a)))
    elif s < 2 * (c - a) + d - b: LOOP.append((c - (s - (c - a + d - b)), d))
    else: LOOP.append((a, d - (s - (2 * (c - a) + d - b))))
# --- sprites
def solid(im):
    a = np.asarray(im.convert('RGBA')).copy(); a[..., 3] = (a[..., 3] > 110) * 255; return Image.fromarray(a)
SH = solid(Image.open(OUT + 'pl/pl_b64_front_clean.png'))                       # PixelLab B shiba, 61 px, as is
MOBS = {}
for k2 in ('shroom', 'wisp', 'wolf'):
    m = json.load(open('art/action/mobs_hr/%s.json' % k2)); im = Image.open('art/action/mobs_hr/%s.png' % k2).crop((0, 0, m['w'], m['h'])); im = im.crop(im.getbbox())
    h = 34 if k2 != 'wolf' else 36; MOBS[k2] = solid(im.resize((round(im.width * h / im.height), h), Image.LANCZOS))
def fit(f, h):
    im = Image.open(f).convert('RGBA'); im = im.crop(im.getbbox()); return solid(im.resize((max(1, round(im.width * h / im.height)), h), Image.LANCZOS))
PROPS = [(-6, 120, fit(P2 + 'trees_green_1.png', 74)), (396, 110, fit(P2 + 'trees_green_3.png', 70)), (8, 262, fit(P2 + 'bushes_1.png', 22)), (384, 258, fit(P2 + 'bushes_6.png', 22))]
OCC = {(0, 1), (1, 1), (2, 0), (2, 2), (3, 1), (4, 0), (5, 2), (1, 2), (4, 2)}
MOBI = list(range(0, 400, 16)); MOBK = [random.choice(list(MOBS)) for _ in MOBI]
# --- cameras: forward 2x3 affine world -> screen (before the panel offset)
CAMS = [('A  TOP-DOWN 90', 1.0, 0), ('B  HIGH 3/4  (~50)', .75, 0), ('C  LOW 3/4  (~30)', .5, 0), ('D  ISOMETRIC', .5, 45)]
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 14)
def panel(name, sy, rot):
    th = math.radians(rot); cx, cy = WW / 2, WH / 2
    k = 1.0
    if rot:   # the turned board is wider than the phone: shrink it to fit 390
        k = (WW - 6) / ((WW * math.cos(th) + WH * math.sin(th)))
    def fwd(x, y):
        u = (x - cx) * math.cos(th) - (y - cy) * math.sin(th); v = (x - cx) * math.sin(th) + (y - cy) * math.cos(th)
        return u * k, v * k * sy
    corners = [fwd(x, y) for x, y in ((0, 0), (WW, 0), (WW, WH), (0, WH))]
    top = 70; PH = int(max(p[1] for p in corners) - min(p[1] for p in corners)) + top + 24; PW_ = 390
    ox = PW_ / 2; oy = top - min(p[1] for p in corners)
    S = lambda x, y: (fwd(x, y)[0] + ox, fwd(x, y)[1] + oy)
    # affine for the ground image: screen -> flat ground pixel (inverse of S, with the margin M)
    A = np.array([[k * math.cos(th), -k * math.sin(th)], [k * sy * math.sin(th), k * sy * math.cos(th)]]); Ai = np.linalg.inv(A)
    t0 = np.array([ox, oy]) - A @ np.array([cx, cy])
    coef = (Ai[0, 0], Ai[0, 1], -(Ai[0] @ t0) + M, Ai[1, 0], Ai[1, 1], -(Ai[1] @ t0) + M)
    pan = GROUND.transform((PW_, PH), Image.AFFINE, coef, Image.NEAREST)
    dr = ImageDraw.Draw(pan); items = []
    rx = 19 * k; ry = 19 * k * sy; tk = round(7 * math.sqrt(max(0, 1 - sy * sy)))      # disc radius and front-face height
    for cc in range(6):
        for r in range(3):
            x, y = S(GX + cc * CS + CS / 2, GY + r * CS + CS / 2)
            dr.ellipse((x - rx - 1, y - ry + tk - 1, x + rx + 1, y + ry + tk + 2), fill=(44, 38, 34))
            dr.rectangle((x - rx, y, x + rx, y + tk), fill=(112, 104, 94)); dr.ellipse((x - rx, y - ry + tk, x + rx, y + ry + tk), fill=(112, 104, 94))
            dr.ellipse((x - rx, y - ry, x + rx, y + ry), fill=(172, 162, 144), outline=(60, 52, 46))
            dr.arc((x - rx + 4, y - ry + 2, x + rx - 4, y + ry - 2), 200, 330, fill=(214, 206, 188))
            if (cc, r) in OCC: items.append((y + 2, SH, x - SH.width / 2))
    for i, kk in zip(MOBI, MOBK):
        x, y = S(*LOOP[i]); nx, _ = S(*LOOP[(i + 6) % 400]); im = MOBS[kk] if nx >= x else MOBS[kk].transpose(Image.FLIP_LEFT_RIGHT)
        items.append((y + 3, im, x - im.width / 2))
    for px, py, im in PROPS:
        x, y = S(px, py); items.append((y, im, x - im.width / 2))
    sh = Image.new('RGBA', pan.size); sd = ImageDraw.Draw(sh)
    for y, im, x in items: sd.ellipse((x + im.width * .18, y - 3, x + im.width * .82, y + 2), fill=(10, 24, 8, 100))
    pan.alpha_composite(sh)
    for y, im, x in sorted(items, key=lambda t: t[0]): pan.alpha_composite(im, (round(x), round(y - im.height)))
    hd = ImageDraw.Draw(pan); hd.rounded_rectangle((6, 6, PW_ - 6, 30), 7, fill=(30, 24, 30, 225), outline=(250, 236, 200), width=2)
    hd.text((14, 10), name, fill=(255, 226, 150), font=F)
    return pan
pans = [panel(*c) for c in CAMS]
H = max(p.height for p in pans); out = Image.new('RGBA', (sum(p.width for p in pans) + 12 * (len(pans) - 1), H), (24, 20, 24, 255)); x = 0
for p in pans: out.alpha_composite(p, (x, 0)); x += p.width + 12
out.resize((out.width * 2, out.height * 2), Image.NEAREST).save(OUT + 'tw_cam_mock.png'); print('ok', out.size, [p.size for p in pans])
