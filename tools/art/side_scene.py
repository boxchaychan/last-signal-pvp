# First side-view map mock (owner 2026-11-11 "แมพแรก", "160 x1 ก่อน"): the PixelLab sidescroller tileset (art/side/tiles/grass_wang.png,
# 32 px corner-Wang sheet; its top-left 3x3 block is a complete platform: corners, edges, fill) built into platforms at 1 art px per
# screen px on a 3x landscape phone (2532x1170), the v5 Berserker side view at body 160, monsters scaled to him.
#   python3 tools/art/side_scene.py  -> art/side/mock_map1.png
import json, math, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
T = 32; ts = Image.open('art/side/tiles/grass_wang.png').convert('RGBA')
tile = lambda c, r: ts.crop((c * T, r * T, c * T + T, r * T + T))
TL, TOP, TR = tile(0, 0), tile(1, 0), tile(2, 0); L, F, R = tile(0, 1), tile(1, 1), tile(2, 1); BL, B, BR = tile(0, 2), tile(1, 2), tile(2, 2); F2 = tile(0, 3)
SW, SH = 2532, 1170
img = Image.new('RGBA', (SW, SH)); d = ImageDraw.Draw(img)
for y in range(SH):
    t = y / SH; d.line((0, y, SW, y), fill=(int(120 + 110 * t), int(190 + 55 * t), 255))
for col, top, amp, ph in (((170, 205, 235), 470, 150, 1), ((134, 186, 140), 680, 110, 2), ((98, 156, 100), 820, 70, 3)):
    d.polygon([(0, SH)] + [(x, int(top - amp * (.5 + .3 * math.sin(x / 260 + ph) + .2 * math.sin(x / 90 + ph * 2)))) for x in range(0, SW + 10, 10)] + [(SW, SH)], fill=col)
def platform(x, y, n, rows):
    """x, y = top-left in px; n tiles wide; rows tiles tall (>=2). The tiles' outer half is empty (corner Wang), so shift by half a tile."""
    for r in range(rows):
        for c in range(n):
            t = (TL if c == 0 else TR if c == n - 1 else TOP) if r == 0 else (BL if c == 0 else BR if c == n - 1 else B) if r == rows - 1 else (L if c == 0 else R if c == n - 1 else (F if (c + r) % 3 else F2))
            img.alpha_composite(t, (x + c * T, y + r * T))
FLOOR = SH - 4 * T
platform(-T // 2, FLOOR - T // 2, SW // T + 2, 6)                    # the ground, running off both sides
platform(140, FLOOR - 260, 14, 2); platform(1250, FLOOR - 300, 20, 2); platform(760, FLOOR - 560, 12, 2); platform(1900, FLOOR - 560, 14, 2)
def cut(im):
    a = np.asarray(im.convert('RGBA')).copy(); bg = (a[..., :3].min(2) > 225) | (a[..., 3] < 20)
    lab, _ = ndimage.label(bg); bd = set(np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])) - {0}; a[np.isin(lab, list(bd))] = 0
    a[(a[..., :3].min(2) > 238)] = 0; return Image.fromarray(a)
def figs(im):
    a = np.asarray(im)[..., 3] > 0; lab, n = ndimage.label(ndimage.binary_dilation(a, iterations=2))
    ob = sorted([s for s in ndimage.find_objects(lab) if s and s[0].stop - s[0].start > 40], key=lambda s: s[1].start)
    return [im.crop((s[1].start, s[0].start, s[1].stop, s[0].stop)) for s in ob]
hero = figs(cut(Image.open('art/incoming/action/berserker/v5_style/out_basic.png')))[1]
ground = FLOOR - T // 2 + 10                                          # the grass line inside the top tiles
img.alpha_composite(hero, (640, ground - hero.height))
def mob(k):
    m = json.load(open('art/action/mobs_hr/%s.json' % k)); im = Image.open('art/action/mobs_hr/%s.png' % k).convert('RGBA')
    c = im.crop((0, 0, m['w'], m['h'])); return c.crop(c.getbbox())
mobs = [mob(k) for k in ('skeleton', 'wolf', 'shroom', 'boar_guard')]; sc = hero.height * .8 / mobs[0].height
for m, (x, y) in zip(mobs, ((1150, ground), (1500, FLOOR - 300 + 10), (1000, FLOOR - 560 + 10), (2150, ground))):
    M = m.resize((int(m.width * sc), int(m.height * sc)), Image.NEAREST).transpose(Image.FLIP_LEFT_RIGHT); img.alpha_composite(M, (x, y - M.height))
ov = Image.new('RGBA', (SW, SH)); o = ImageDraw.Draw(ov)
o.rectangle((0, SH - 70, SW, SH), fill=(0, 0, 0, 150)); o.rectangle((40, SH - 52, 520, SH - 22), fill=(196, 30, 42, 255)); o.rectangle((560, SH - 52, 1040, SH - 22), fill=(30, 86, 196, 255)); o.rectangle((0, SH - 12, SW, SH), fill=(224, 176, 32, 255))
for (x, y, r) in ((2380, 900, 90), (2210, 1010, 62), (2210, 830, 62), (2330, 700, 62)): o.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, 40), outline=(255, 255, 255, 150), width=6)
o.ellipse((60, 760, 300, 1000), fill=(255, 255, 255, 30), outline=(255, 255, 255, 130), width=6)
img.alpha_composite(ov); img.convert('RGB').save('art/side/mock_map1.png'); print('hero', hero.size)
