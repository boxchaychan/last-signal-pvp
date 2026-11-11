# Owner 2026-11-11 "เอาที่เราเจนมาใส่ประกอบฉากด้วย เอาตัวคนที่เป็น PixelLab ย่อใส่ไปดูว่าเหมือนไหม": a Dimraeth-like top-down
# mock at the 64 canvas size (hero ~48 px), built only from what we already have: the action game's ground textures, the PixelLab
# forest props (art/side/forest + map30 tree) and the PixelLab Berserker (art/action/n128, south-east still) shrunk to 64.
# Drawn at 1 art px per game px on an 844x390 view, then x3 for a 3x phone. Day and night (Dimraeth-like glow) versions.
#   python3 tools/art/topdown_mock64.py -> art/side/td64/mock_day.png, mock_night.png
import json, random, os, numpy as np
from PIL import Image, ImageDraw, ImageFilter
OUT = 'art/side/td64/'; os.makedirs(OUT, exist_ok=True); random.seed(4)
VW, VH = 844, 390
def pshrink(im, h, cols=28):
    """shrink pixel art to height h: Lanczos, hard alpha, few colours, a 1-px dark outline"""
    im = im.convert('RGBA'); im = im.crop(im.getbbox()); k = h / im.height
    s = im.resize((max(1, round(im.width * k)), h), Image.LANCZOS); a = np.asarray(s).copy(); m = a[..., 3] > 120
    q = Image.fromarray(a[..., :3]).quantize(cols, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB')
    o = np.zeros((a.shape[0] + 2, a.shape[1] + 2, 4), np.uint8); o[1:-1, 1:-1, :3] = np.asarray(q); o[1:-1, 1:-1, 3] = m * 255
    al = o[..., 3] > 0; nb = np.zeros_like(al)
    for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)): nb |= np.roll(np.roll(al, dy, 0), dx, 1)
    o[nb & ~al] = (22, 16, 20, 255); return Image.fromarray(o)
# ground: the action game's grass + a dirt path, tiled at half size
g = Image.open('art/action/ground/grass.png').convert('RGBA'); g = g.resize((g.width // 2, g.height // 2), Image.NEAREST)
fg = Image.open('art/action/ground/flowergrass.png').convert('RGBA'); fg = fg.resize((fg.width // 2, fg.height // 2), Image.NEAREST)
dt = Image.open('art/action/ground/dirt.png').convert('RGBA'); dt = dt.resize((dt.width // 2, dt.height // 2), Image.NEAREST)
img = Image.new('RGBA', (VW, VH))
for y in range(0, VH, g.height):
    for x in range(0, VW, g.width): img.alpha_composite(g, (x, y))
path = Image.new('L', (VW, VH)); pd = ImageDraw.Draw(path)
pts = [(-20, 300), (150, 270), (330, 230), (520, 240), (700, 200), (880, 170)]
pd.line(pts, fill=255, width=46, joint='curve'); path = path.filter(ImageFilter.GaussianBlur(3)).point(lambda v: 255 if v > 128 else 0)
dl = Image.new('RGBA', (VW, VH))
for y in range(0, VH, dt.height):
    for x in range(0, VW, dt.width): dl.alpha_composite(dt, (x, y))
img = Image.composite(dl, img, path)
# props (PixelLab), sorted by their foot y
P = lambda f: Image.open(f)
props = [('art/side/map30/tree.png', 110, 120, 150), ('art/side/map30/tree.png', 96, 700, 120), ('art/side/forest/small_tree.png', 80, 40, 360),
         ('art/side/forest/small_tree.png', 70, 560, 110), ('art/side/forest/bush.png', 34, 250, 175), ('art/side/forest/bush.png', 30, 780, 330),
         ('art/side/forest/bush.png', 28, 430, 370), ('art/side/forest/rocks.png', 26, 600, 300), ('art/side/forest/rocks.png', 22, 90, 200),
         ('art/side/forest/fence.png', 30, 330, 330), ('art/side/forest/sign.png', 34, 470, 205), ('art/side/forest/flowers.png', 22, 180, 330),
         ('art/side/forest/flowers.png', 20, 650, 360), ('art/side/forest/flowers.png', 18, 380, 140)]
items = []
for f, h, x, y in props: items.append((y, pshrink(P(f), h), x))
# hero: PixelLab Berserker south-east still, figure 48
M = json.load(open('art/action/n128/berserker.json')); C = M['cell']
st = Image.open('art/action/n128/berserker_still.png').crop((C, 0, 2 * C, C)); hero = pshrink(st, 50)
items.append((268, hero, 392 - hero.width // 2))
for k, h, x, y, flip in (('wolf', 30, 520, 262, True), ('shroom', 22, 470, 300, True), ('skeleton', 40, 610, 236, True)):
    mm = json.load(open('art/action/mobs_hr/%s.json' % k)); im = Image.open('art/action/mobs_hr/%s.png' % k).crop((0, 0, mm['w'], mm['h']))
    s = pshrink(im, h); s = s.transpose(Image.FLIP_LEFT_RIGHT) if flip else s; items.append((y, s, x))
sh = Image.new('RGBA', (VW, VH)); sd = ImageDraw.Draw(sh)
for y, im, x in items: sd.ellipse((x + im.width * .15, y - 4, x + im.width * .85, y + 3), fill=(0, 0, 0, 70))
img.alpha_composite(sh)
for y, im, x in sorted(items, key=lambda t: t[0]): img.alpha_composite(im, (int(x), int(y - im.height)))
day = img.copy()
# night: blue grade, dark edges, glow round the hero
a = np.asarray(img).astype(float); a[..., 0] *= .45; a[..., 1] *= .5; a[..., 2] = a[..., 2] * .75 + 40
yy, xx = np.mgrid[0:VH, 0:VW]; d = np.hypot((xx - 410) / VW, (yy - 245) / VH)
light = np.clip(1.25 - d * 2.2, .35, 1.25)[..., None]; a[..., :3] *= light
glow = np.exp(-((xx - 410) ** 2 + (yy - 245) ** 2) / (2 * 55 ** 2))[..., None] * np.array([90, 60, 20])
a[..., :3] = np.clip(a[..., :3] + glow, 0, 255); night = Image.fromarray(a.astype(np.uint8))
for name, im in (('day', day), ('night', night)):
    im.resize((VW * 3, VH * 3), Image.NEAREST).convert('RGB').save(OUT + 'mock_%s.png' % name)
hero.resize((hero.width * 6, hero.height * 6), Image.NEAREST).save(OUT + 'hero64_x6.png')
print('hero', hero.size)
