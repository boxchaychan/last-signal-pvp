# Tower defense map mock for the dogs-vs-cats idea (owner 2026-11-12 "จำลองแมพ TD มาก่อน ของสวยๆ เอาพื้นไปทำมา"): free, no jobs.
# One phone screen (844 x 390, 1 px = 1 CSS px), the PixelLab ground tiles laid by masks (grass with patches, a dirt road with a
# dark rim, a pond), stone tower pads along the road (some holding the lazy samurai shiba at 64 px, some empty), little monsters
# walking the road, the props set 2 round the edges, a camp as the base, a small HUD.
#   python3 tools/art/tw_mock.py -> art/incoming/dogcat/tw_mock.png (x2)
import json, random, sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage
sys.path.insert(0, 'tools/art'); from px_outline import outline
random.seed(5); np.random.seed(5)
W, H = 844, 390; D = 'art/td/tiles/'; P2 = 'art/td/props/set2/cut/'; OUT = 'art/incoming/dogcat/'
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
N8, N40, N90 = noise(8), noise(40), noise(90)
BY = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])[yy % 4, xx % 4] / 16
dil = lambda m, r: ndimage.binary_dilation(m, iterations=r)
edge = lambda m: m & ~ndimage.binary_erosion(m)
def curve(pts, n=60):
    P = []; pp = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(pp) - 2):
        p0, p1, p2, p3 = [np.array(p, float) for p in pp[i - 1:i + 3]]
        for t in np.linspace(0, 1, n, endpoint=False): P.append(.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    P.append(np.array(pts[-1], float)); return P
G = tile_fill(tex('path_pro', False)); DR = tile_fill(tex('path_pro', True)); WA = tile_fill(tex('river', True))
img = G.copy()
lv = N90 * .7 + N40 * .3 + (BY - .5) * .08
img[lv < .34] *= .9; lt = lv > .62; img[lt] = img[lt] * 1.08 + np.array([12, 8, -4])
# road
ROAD = [(-30, 262), (110, 258), (190, 205), (230, 130), (330, 100), (430, 125), (470, 205), (540, 290), (650, 300), (720, 240), (760, 175), (808, 160)]
RP = curve(ROAD); line = np.zeros((H, W), bool)
for x, y in RP:
    if 0 <= int(y) < H and 0 <= int(x) < W: line[int(y), int(x)] = True
dist = ndimage.distance_transform_edt(~line); road = dist < 20 + (N8 - .5) * 6
img[road] = DR[road]; rim = edge(dil(road, 2)) & ~road; img[rim] = img[rim] * .7 + np.array([60, 96, 36]) * .3
# pond
pond = ((xx - 95) / 78) ** 2 + ((yy - 352) / 34) ** 2 < 1 + (N8 - .5) * .2; bank = dil(pond, 5)
img[bank & ~pond] = np.array([116, 84, 54]) + (N8[bank & ~pond, None] - .5) * 26; img[pond] = WA[pond]; img[ndimage.binary_erosion(pond, iterations=10)] *= .85
img[edge(pond)] = [214, 238, 248]
base = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert('RGBA'); dr = ImageDraw.Draw(base)
# grass tufts and flowers
for _ in range(900):
    x, y = random.randrange(4, W - 4), random.randrange(34, H - 4)
    if dist[y, x] < 26 or bank[y, x]: continue
    r = random.random()
    if r < .6: c = random.choice([(52, 116, 44), (118, 178, 72), (80, 150, 56)]); [dr.line((x + d, y, x + d, y - random.randint(2, 5)), fill=c) for d in (-1, 1)]
    elif r < .85: dr.rectangle((x, y, x + 1, y + 1), fill=random.choice([(250, 236, 120), (240, 140, 170), (255, 255, 255), (170, 140, 240)]))
# props
def fit(f, h, flip=False):
    im = Image.open(f).convert('RGBA'); im = im.crop(im.getbbox()); k = h / im.height
    im = im.resize((max(1, round(im.width * k)), h), Image.NEAREST if abs(k - round(k)) < .01 and k >= 1 else Image.LANCZOS)
    a = np.asarray(im).copy(); a[..., 3] = (a[..., 3] > 110) * 255; im = Image.fromarray(a)
    return im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im
items = []
def put(im, x, y, sh=True): items.append((y, im, x - im.width // 2, sh))
free = lambda x, y, r: dist[min(H - 1, max(0, y)), min(W - 1, max(0, x))] > r and not bank[min(H - 1, y), min(W - 1, x)]
for x, y, n, h in ((30, 120, 'trees_green_0', 150), (110, 70, 'trees_green_1', 140), (560, 70, 'trees_green_3', 135), (650, 110, 'trees_green_0', 150), (820, 330, 'trees_green_1', 150),
                   (300, 390, 'trees_green_2', 130), (450, 395, 'trees_green_0', 140), (760, 400, 'trees_green_3', 130), (20, 300, 'trees_green_2', 120)):
    put(fit(P2 + n + '.png', h, random.random() < .5), x, y)
for x, y, n, h in ((180, 330, 'bushes_1', 28), (380, 230, 'bushes_6', 26), (600, 175, 'bushes_9', 22), (720, 360, 'bushes_2', 26), (470, 330, 'logs2_0', 26),
                   (260, 290, 'stones_0', 18), (520, 60, 'stones_8', 16), (350, 330, 'bushes_10', 24), (40, 210, 'stones_12', 18), (690, 60, 'bushes_4', 26)):
    if free(x, y, 26): put(fit(P2 + n + '.png', h, random.random() < .5), x, y)
for x, y, n, h in ((70, 345, 'water_0', 24), (115, 358, 'water_1', 24)): put(fit(P2 + n + '.png', h), x, y, False)
put(fit('art/td/props/rock1.png', 70, True), 880, 270); put(fit('art/td/props/rock3.png', 54), 395, 40 + 54)
# the base: a camp at the road's end
put(fit(P2 + 'camp_0.png', 70), 805, 150); put(fit(P2 + 'camp_2.png', 24), 770, 158); put(fit(P2 + 'camp_5.png', 26), 838, 172); put(fit(P2 + 'camp_1.png', 26), 790, 186)
# tower pads: round stones beside the road
SH = Image.open(OUT + 'shiba_px120_front.png'); k = 64 / SH.height
def shiba(flip):
    s = Image.open(OUT + 'shiba_gpt.webp').convert('RGB'); a = np.asarray(s).astype(int)
    bg = a.min(2) > 238; lab, n = ndimage.label(bg); ed = set(np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])) - {0}; bm = np.isin(lab, list(ed))
    sz = ndimage.sum(bg, lab, range(1, n + 1))
    for i, q in enumerate(sz):
        if i + 1 not in ed and q > 1500 and a[lab == i + 1].min() > 246: bm |= lab == i + 1
    fg = ~bm; fl, fn = ndimage.label(dil(fg, 3)); fs = ndimage.sum(fg, fl, range(1, fn + 1)); i = 1 + int(np.argsort(-fs)[:2][np.argmin([np.where(fl == j)[1].mean() for j in 1 + np.argsort(-fs)[:2]])])
    c = np.dstack([a, np.where((fl == i) & fg, 255, 0)]).astype(np.uint8); part = Image.fromarray(c); part = part.crop(part.getbbox())
    kk = 64 / part.height; s2 = part.resize((round(part.width * kk), 64), Image.BOX); b = np.asarray(s2).copy(); b[..., 3] = (b[..., 3] > 140) * 255
    rgb = Image.fromarray(b[..., :3]).quantize(24, method=Image.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB'); cc = np.dstack([np.asarray(rgb), b[..., 3]]); cc[cc[..., 3] == 0] = 0
    hh = cc.shape[0]; cc[(cc[..., :3].min(2) > 225) & (np.mgrid[0:hh, 0:cc.shape[1]][0] > hh * .86)] = 0
    im = Image.fromarray(outline(cc, pale=250, black=(30, 20, 18))); im.save(OUT + 'shiba_px64_front.png')
    return im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im
SB = shiba(False)
PADS = [(120, 205, 1), (262, 190, 1), (300, 60, 0), (400, 175, 1), (505, 235, 0), (590, 250, 1), (610, 350, 0), (700, 205, 1)]
pads = Image.new('RGBA', base.size); pd = ImageDraw.Draw(pads)
for x, y, occ in PADS:
    pd.ellipse((x - 25, y - 9, x + 25, y + 11), fill=(40, 34, 30, 255)); pd.ellipse((x - 24, y - 10, x + 24, y + 8), fill=(150, 142, 128, 255))
    pd.ellipse((x - 20, y - 8, x + 20, y + 5), fill=(186, 178, 160, 255)); pd.arc((x - 20, y - 8, x + 20, y + 5), 200, 330, fill=(220, 214, 198, 255))
    if occ: put(SB.transpose(Image.FLIP_LEFT_RIGHT) if x > 560 else SB, x, y + 3)
    else: pd.line((x - 5, y - 2, x + 5, y - 2), fill=(250, 240, 200, 255), width=2); pd.line((x, y - 7, x, y + 3), fill=(250, 240, 200, 255), width=2)
base.alpha_composite(pads)
# monsters walking the road (placeholders from the mob sheets, 34-40 px)
def mob(k, h):
    m = json.load(open('art/action/mobs_hr/%s.json' % k)); im = Image.open('art/action/mobs_hr/%s.png' % k).crop((0, 0, m['w'], m['h'])); im = im.crop(im.getbbox())
    kk = h / im.height; im = im.resize((round(im.width * kk), h), Image.LANCZOS); a = np.asarray(im).copy(); a[..., 3] = (a[..., 3] > 110) * 255; return Image.fromarray(a)
for i, (k, h) in zip((40, 70, 100, 150, 175, 205, 330, 360, 385), (('shroom', 26), ('shroom', 26), ('wolf', 30), ('wisp', 26), ('shroom', 26), ('wolf', 30), ('shroom', 26), ('wisp', 26), ('wolf', 30))):
    x, y = RP[i]; nx, ny = RP[min(len(RP) - 1, i + 3)]; im = mob(k, h); im = im if nx > x else im.transpose(Image.FLIP_LEFT_RIGHT); put(im, int(x), int(y) + 6)
# shadows, then back to front
sh = Image.new('RGBA', base.size); sd = ImageDraw.Draw(sh)
for y, im, x, s in items:
    if not s: continue
    w = im.width
    if im.height > 90: sd.ellipse((x + w * .15, y - w * .1, x + w * .95, y + w * .08), fill=(10, 24, 8, 80))
    else: sd.ellipse((x + w * .12, y - 4, x + w * .9, y + 3), fill=(10, 24, 8, 90))
base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(1.5)))
for y, im, x, s in sorted(items, key=lambda t: t[0]): base.alpha_composite(im, (int(x), int(y - im.height)))
# a soft bright grade, a light vignette
a = np.asarray(base).astype(float); g = a[..., :3].mean(2, keepdims=True); a[..., :3] = g + (a[..., :3] - g) * 1.08
a[..., :3] *= np.clip(1.12 - np.hypot((xx - W / 2) / W, (yy - H / 2) / H) * .7, .78, 1)[..., None]; base = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
# HUD: hearts, coins, wave, next-wave button
hd = ImageDraw.Draw(base); F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)
def chip(x, w, col, txt):
    hd.rounded_rectangle((x, 6, x + w, 28), 6, fill=(30, 24, 30, 220), outline=(250, 236, 200, 255), width=2)
    hd.ellipse((x + 5, 10, x + 19, 24), fill=col, outline=(30, 20, 18)); hd.text((x + 25, 8), txt, fill=(250, 240, 210), font=F)
chip(8, 70, (230, 70, 80), '20'); chip(84, 86, (250, 200, 60), '150'); chip(176, 132, (120, 190, 250), 'WAVE 3/20')
hd.rounded_rectangle((W - 92, H - 34, W - 8, H - 8), 8, fill=(250, 200, 60), outline=(30, 20, 18), width=2); hd.text((W - 80, H - 30), 'NEXT >>', fill=(30, 20, 18), font=F)
base.resize((W * 2, H * 2), Image.NEAREST).save(OUT + 'tw_mock.png'); print('ok')
