# 30-credit PixelLab map test (owner 2026-11-11 "ลองจำกัดซัก 30 เครดิต"): pro sidescroller tileset (15) + Pro Flash parallax
# background 256x144 (9) + one big tree 200x200 (6), assembled on a 3x landscape phone screen with the v6 painted hero at x1.
#   python3 tools/art/side_map30.py -> art/side/map30/mock.png
import glob, os, sys, numpy as np
sys.path.insert(0, 'tools/art'); SMOOTH = os.environ.get('SMOOTH') == '1'
from px_smooth import smooth_up
from vivid import vivid
from PIL import Image, ImageDraw
D = 'art/side/map30/'; SW, SH = 2532, 1170
T = 32; ts = Image.open(D + 'tiles_wang.png').convert('RGBA'); K = 2          # tiles drawn 2x (64 px)
tile = lambda c, r: (smooth_up(ts.crop((c * T, r * T, c * T + T, r * T + T)), K) if SMOOTH else ts.crop((c * T, r * T, c * T + T, r * T + T)).resize((T * K, T * K), Image.NEAREST))
TL, TOP, TR, L, F, R, BL, B, BR, F2 = tile(0, 0), tile(1, 0), tile(2, 0), tile(0, 1), tile(1, 1), tile(2, 1), tile(0, 2), tile(1, 2), tile(2, 2), tile(0, 3)
img = Image.new('RGBA', (SW, SH)); d = ImageDraw.Draw(img)
bg = Image.open(D + 'bg.png').convert('RGBA'); KB = 6
B6 = smooth_up(bg, KB) if SMOOTH else bg.resize((bg.width * KB, bg.height * KB), Image.NEAREST); top = bg.getpixel((2, 2))
top = bg.getpixel((bg.width // 2, 1))[:3]; y0 = SH - 150 - B6.height + 120
for y in range(y0 + 2):                                                   # sky above the picture: the picture's top blue, deeper upwards
    k = y / max(1, y0); d.line((0, y, SW, y), fill=tuple(int(c * (.78 + .22 * k)) for c in top))
x = -300; flip = False
while x < SW:
    img.alpha_composite(B6.transpose(Image.FLIP_LEFT_RIGHT) if flip else B6, (x, SH - 150 - B6.height + 120)); x += B6.width; flip = not flip
t2 = T * K
def platform(x, y, n, rows):
    for r in range(rows):
        for c in range(n):
            t = (TL if c == 0 else TR if c == n - 1 else TOP) if r == 0 else (BL if c == 0 else BR if c == n - 1 else B) if r == rows - 1 else (L if c == 0 else R if c == n - 1 else (F if (c + r) % 3 else F2))
            img.alpha_composite(t, (x + c * t2, y + r * t2))
FLOOR = SH - 3 * t2
tree = Image.open(D + 'tree.png').convert('RGBA'); tree = tree.crop(tree.getbbox()); tree = smooth_up(tree, 3) if SMOOTH else tree.resize((tree.width * 3, tree.height * 3), Image.NEAREST)
img.alpha_composite(tree, (1500, FLOOR - t2 // 2 + 20 - tree.height + 18))
PROPS = os.environ.get('PROPS') == '1'
def prop(name, k, x, base, flip=False):
    im = Image.open('art/side/forest/' + name + '.png').convert('RGBA'); im = im.crop(im.getbbox())
    im = smooth_up(im, k) if SMOOTH else im.resize((im.width * k, im.height * k), Image.NEAREST)
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    img.alpha_composite(im, (x, base - im.height + 6))
gl = FLOOR - t2 // 2 + 20
if PROPS:                                                     # behind the ground line: trees, fence, sign
    prop('small_tree', 3, 80, gl); prop('small_tree', 2, 2200, gl, True); prop('fence', 3, 980, gl); prop('sign', 3, 560, gl)
platform(-t2 // 2, FLOOR - t2 // 2, SW // t2 + 2, 4)
if PROPS:                                                     # on the grass: bushes, rocks, flowers, and a few on the platforms
    prop('bush', 3, 300, gl + 8); prop('bush', 2, 1320, gl + 8, True); prop('rocks', 3, 1900, gl + 8); prop('flowers', 3, 1180, gl + 10)
    prop('flowers', 2, 2350, gl + 10, True); prop('rocks', 2, 640, gl + 8, True)
platform(260, FLOOR - 330, 6, 2); platform(1050, FLOOR - 560, 7, 2); platform(2050, FLOOR - 360, 5, 2)
if PROPS:
    prop('bush', 2, 300, FLOOR - 330 + 22); prop('flowers', 2, 1150, FLOOR - 560 + 24); prop('sign', 2, 2120, FLOOR - 360 + 22)
ground = FLOOR - t2 // 2 + 20
hero = Image.open(sorted(glob.glob('art/incoming/side/berserker/v6/walk/f*.png'))[0]); hk = .42
hero = hero.resize((round(hero.width * hk), round(hero.height * hk)), Image.LANCZOS)
img.alpha_composite(hero, (720, ground - round((hero.height / hk - 20) * hk)))
ov = Image.new('RGBA', (SW, SH)); o = ImageDraw.Draw(ov)
o.rectangle((0, SH - 70, SW, SH), fill=(0, 0, 0, 150)); o.rectangle((40, SH - 52, 520, SH - 22), fill=(196, 30, 42, 255)); o.rectangle((560, SH - 52, 1040, SH - 22), fill=(30, 86, 196, 255))
for (cx, cy, r) in ((2380, 900, 90), (2210, 1010, 62), (2210, 830, 62), (2330, 700, 62)): o.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 40), outline=(255, 255, 255, 150), width=6)
o.ellipse((60, 760, 300, 1000), fill=(255, 255, 255, 30), outline=(255, 255, 255, 130), width=6)
img = vivid(img, 1.0) if SMOOTH else img
img.alpha_composite(ov); img.convert('RGB').save(D + ('mock_props.png' if PROPS else 'mock_smooth.png' if SMOOTH else 'mock.png')); print('ok')
