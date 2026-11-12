# Bag art for dogcat.html, drawn in code (owner 2026-11-13 "ทำให้ดูดี" about the bag): free, no jobs.
#   python3 tools/art/dogcat_bag.py -> art/dogcat/bag/{panel.png, bone,collar,bowl,leash,tag,treat}.png
# panel.png = the leather backpack (573 x 404): stitched edge, flap with a buckle, 7 x 4 inset pockets, 3 tray pockets, a bin.
# Items are pixel sprites on the 1 px grid, sized to their cells (56 px each) at rotation 0; the game turns them in 90° steps.
import os, sys, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
sys.path.insert(0, 'tools/art'); from px_outline import outline
O = 'art/dogcat/bag/'; os.makedirs(O, exist_ok=True); INK = (34, 28, 40); R = np.random.RandomState(4)
def fin(c): return Image.fromarray(outline(np.asarray(c), pale=999, black=INK).astype(np.uint8))
# ---------- panel
PW, PH = 573, 404; a = np.zeros((PH, PW, 3)); yy, xx = np.mgrid[0:PH, 0:PW]
n = ndimage.zoom(R.rand(PH // 6 + 2, PW // 6 + 2), 6, order=1)[:PH, :PW]; a[:] = np.array([124, 82, 52]) + (n[..., None] - .5) * 16
a[R.rand(PH, PW) < .05] *= .92
im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA'); d = ImageDraw.Draw(im)
d.rounded_rectangle((0, 0, PW - 1, PH - 1), 12, outline=INK, width=3); d.rounded_rectangle((3, 3, PW - 4, PH - 4), 10, outline=(168, 118, 76), width=2); d.rounded_rectangle((5, 5, PW - 6, PH - 6), 9, outline=(92, 58, 38), width=1)
for x in range(14, PW - 14, 10): d.line((x, 10, x + 5, 10), fill=(232, 204, 150)); d.line((x, PH - 11, x + 5, PH - 11), fill=(232, 204, 150))
for y in range(14, PH - 14, 10): d.line((10, y, 10, y + 5), fill=(232, 204, 150)); d.line((PW - 11, y, PW - 11, y + 5), fill=(232, 204, 150))
d.rounded_rectangle((14, 16, PW - 15, 70), 8, fill=(104, 66, 42), outline=INK); d.line((18, 19, PW - 19, 19), fill=(150, 104, 68)); d.line((18, 67, PW - 19, 67), fill=(70, 44, 30))      # the flap
for x in range(22, PW - 22, 9): d.line((x, 64, x + 4, 64), fill=(214, 184, 132))
bx = PW - 70; d.rounded_rectangle((bx, 26, bx + 44, 60), 4, fill=(226, 186, 76), outline=INK); d.rectangle((bx + 8, 33, bx + 36, 53), fill=(104, 66, 42), outline=INK); d.rectangle((bx + 20, 30, bx + 24, 56), fill=(250, 226, 130), outline=INK); d.line((bx + 3, 29, bx + 41, 29), fill=(255, 240, 170))
def pocket(x, y, w, h, base=(78, 50, 34)):
    d.rounded_rectangle((x, y, x + w - 1, y + h - 1), 4, fill=INK); d.rounded_rectangle((x + 1, y + 1, x + w - 2, y + h - 2), 3, fill=base)
    d.line((x + 3, y + 2, x + w - 4, y + 2), fill=tuple(int(v * .62) for v in base)); d.line((x + 2, y + 3, x + 2, y + h - 4), fill=tuple(int(v * .62) for v in base)); d.line((x + 3, y + 3, x + w - 4, y + 3), fill=tuple(int(v * .78) for v in base))
    d.line((x + 3, y + h - 3, x + w - 4, y + h - 3), fill=tuple(min(255, int(v * 1.3)) for v in base)); d.line((x + w - 3, y + 3, x + w - 3, y + h - 4), fill=tuple(min(255, int(v * 1.3)) for v in base))
GX, GY, S = 16, 84, 56                                   # grid origin inside the panel (the game: BAG.x = 6 + 16, BAG.y = 716 + 84)
for r in range(4):
    for c in range(7): pocket(GX + c * S, GY + r * S, S, S, (84, 54, 36) if (r + c) % 2 else (92, 60, 40))
for i in range(3): pocket(432, 84 + i * 72, 126, 66, (70, 46, 32))
d.rounded_rectangle((432, 302, 557, 365), 5, fill=INK); d.rounded_rectangle((434, 304, 555, 363), 4, fill=(112, 60, 54)); d.line((437, 306, 552, 306), fill=(160, 96, 86))
tx, ty = 452, 318; d.rectangle((tx, ty + 6, tx + 22, ty + 34), fill=(210, 200, 196), outline=INK); d.rectangle((tx - 3, ty + 1, tx + 25, ty + 6), fill=(236, 228, 224), outline=INK); d.rectangle((tx + 7, ty - 3, tx + 15, ty + 1), fill=(236, 228, 224), outline=INK)
for x in (tx + 6, tx + 11, tx + 16): d.line((x, ty + 11, x, ty + 30), fill=(130, 120, 120))
im.save(O + 'panel.png')
# ---------- items
def bone(c, x0, y0, x1, y1, t, col=(250, 240, 214), sh=(214, 196, 160)):
    d = ImageDraw.Draw(c); d.rectangle((x0, y0 + t // 2, x1, y1 - t // 2), fill=col)
    for x in (x0, x1):
        for y in (y0 + t // 2, y1 - t // 2): d.ellipse((x - t, y - t, x + t, y + t), fill=col)
    d.line((x0 - 2, y1 - t // 2 + t - 3, x1 + 2, y1 - t // 2 + t - 3), fill=sh); d.line((x0, y1 - t // 2, x1, y1 - t // 2), fill=sh); d.line((x0 - 4, y0 + t // 2 - t + 3, x0 + 2, y0 + t // 2 - t + 3), fill=(255, 255, 255)); d.line((x0, y0 + t // 2 + 1, x1, y0 + t // 2 + 1), fill=(255, 255, 255))
c = Image.new('RGBA', (112, 56)); bone(c, 28, 22, 84, 34, 9); fin(c).save(O + 'bone.png')
c = Image.new('RGBA', (56, 56)); d = ImageDraw.Draw(c)
d.ellipse((7, 16, 49, 44), fill=(196, 44, 52)); d.ellipse((7, 14, 49, 40), fill=(226, 70, 70)); d.ellipse((15, 20, 41, 34), fill=(0, 0, 0, 0)); d.arc((9, 15, 47, 38), 200, 320, fill=(255, 150, 140))
for sx in (12, 21, 28, 35, 44): d.polygon([(sx - 4, 17), (sx, 6), (sx + 4, 17)], fill=(214, 220, 230)); d.line((sx - 1, 9, sx - 2, 15), fill=(255, 255, 255))
d.ellipse((22, 38, 34, 50), fill=(250, 204, 70)); d.ellipse((25, 41, 29, 45), fill=(255, 240, 160)); fin(c).save(O + 'collar.png')
c = Image.new('RGBA', (112, 112)); d = ImageDraw.Draw(c)
d.polygon([(12, 50), (100, 50), (90, 98), (22, 98)], fill=(214, 60, 58)); d.polygon([(64, 50), (100, 50), (90, 98), (60, 98)], fill=(182, 44, 50)); d.rectangle((22, 92, 90, 98), fill=(150, 34, 44))
d.ellipse((8, 30, 104, 66), fill=(160, 38, 46)); d.ellipse((14, 34, 98, 60), fill=(140, 88, 52)); d.arc((10, 31, 102, 64), 190, 340, fill=(246, 130, 110))
for i in range(26):
    kx, ky = 22 + R.randint(0, 68), 38 + R.randint(0, 16)
    if ((kx - 56) / 42) ** 2 + ((ky - 47) / 13) ** 2 < .8: d.ellipse((kx - 3, ky - 2, kx + 3, ky + 2), fill=[(196, 138, 84), (176, 118, 68), (214, 160, 100)][i % 3])
bone(c, 42, 72, 70, 80, 5, (255, 236, 220), (236, 200, 190)); d.line((20, 54, 26, 90), fill=(250, 150, 130)); fin(c).save(O + 'bowl.png')
c = Image.new('RGBA', (168, 56)); d = ImageDraw.Draw(c)
pts = [(40 + i * 4, 28 + int(round(6 * np.sin(i * .5)))) for i in range(26)]
d.line(pts, fill=(52, 110, 196), width=9); d.line([(x, y - 2) for x, y in pts], fill=(110, 170, 240), width=2); d.line([(x, y + 3) for x, y in pts], fill=(36, 80, 150), width=1)
d.ellipse((6, 10, 46, 46), fill=(52, 110, 196)); d.ellipse((15, 18, 37, 38), fill=(0, 0, 0, 0)); d.arc((8, 12, 44, 44), 190, 300, fill=(140, 190, 250))
d.rectangle((138, 22, 150, 34), fill=(200, 206, 216)); d.ellipse((146, 16, 164, 40), fill=(200, 206, 216)); d.ellipse((151, 21, 159, 35), fill=(0, 0, 0, 0)); d.line((139, 23, 149, 23), fill=(255, 255, 255)); fin(c).save(O + 'leash.png')
c = Image.new('RGBA', (112, 112)); d = ImageDraw.Draw(c)
for y in range(8, 72, 12): d.ellipse((22, y, 34, y + 14), fill=(190, 196, 208)); d.ellipse((25, y + 3, 31, y + 11), fill=(0, 0, 0, 0))
d.ellipse((24, 70, 48, 94), fill=(190, 196, 208)); d.ellipse((29, 75, 43, 89), fill=(0, 0, 0, 0))
d.ellipse((42, 56, 106, 108), fill=(214, 160, 40)); d.ellipse((42, 52, 106, 104), fill=(250, 204, 70)); d.ellipse((48, 58, 100, 98), fill=(240, 186, 52)); d.arc((45, 54, 103, 100), 190, 290, fill=(255, 244, 180), width=2)
bone(c, 62, 74, 86, 82, 5, (255, 244, 190), (214, 160, 40)); fin(c).save(O + 'tag.png')
c = Image.new('RGBA', (56, 56)); bone(c, 18, 24, 38, 34, 8, (190, 128, 72), (150, 96, 54)); d = ImageDraw.Draw(c)
for px, py in ((22, 27), (28, 31), (34, 27)): d.rectangle((px, py, px + 1, py + 1), fill=(120, 76, 44))
d.polygon([(44, 6), (46, 12), (52, 14), (46, 16), (44, 22), (42, 16), (36, 14), (42, 12)], fill=(255, 226, 90)); fin(c).save(O + 'treat.png')
print('ok')
