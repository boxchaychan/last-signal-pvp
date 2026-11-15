# Contact sheet of the stone-age city starter set (art/incoming/citytest/starter/sheet.png). Run inside that folder.
from PIL import Image, ImageDraw, ImageFont
F = ImageFont.truetype('../../../../art/gem/font/kanit-thai-600-normal.woff2', 22)
BG = (231, 184, 110)   # sandy ground of scene3
INK = (70, 40, 20)
S = 3
rows = [
    ('ไทล์พื้น', ['tile_grass', 'tile_dirt', 'tile_rock', 'tile_water', 'tile_cliff']),
    ('อาคาร', ['obj_hut2', 'obj_hut', 'obj_leanto', 'obj_campfire', 'obj_totem', 'obj_rack', 'obj_fence']),
    ('ของประกอบ', ['prop_tree', 'prop_firewood', 'prop_flint', 'prop_pots', 'prop_skull']),
]
names = {'tile_grass': 'หญ้า', 'tile_dirt': 'ดินทราย', 'tile_rock': 'พื้นหิน', 'tile_water': 'น้ำตื้น', 'tile_cliff': 'หน้าผา',
         'obj_hut2': 'กระท่อมงาช้าง', 'obj_hut': 'กระท่อม ลองแรก', 'obj_leanto': 'เพิงใบไม้', 'obj_campfire': 'กองไฟ',
         'obj_totem': 'เสาโทเท็ม', 'obj_rack': 'ราวตากหนัง', 'obj_fence': 'รั้วไม้แหลม', 'prop_tree': 'ต้นไม้ใหญ่',
         'prop_firewood': 'กองฟืน', 'prop_flint': 'กองหินเหล็กไฟ', 'prop_pots': 'หม้อดิน', 'prop_skull': 'หัวกะโหลก'}
pad = 24
blocks = []
for title, ks in rows:
    ims = [Image.open(k + '.png').convert('RGBA') for k in ks]
    h = max(i.height for i in ims) * S
    w = sum(max(i.width * S, 170) for i in ims) + pad * (len(ims) + 1)
    blocks.append((title, ks, ims, w, h))
mapW, mapH = 380, 290
W = max(max(b[3] for b in blocks) + 40, mapW * 2 + 40)
H = sum(b[4] + 90 for b in blocks) + 34 + mapH * 2 - 40
out = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(out)
y = 20
for title, ks, ims, w, h in blocks:
    d.text((20, y), title, font=F, fill=INK); y += 34
    x = 20 + pad
    for k, im in zip(ks, ims):
        cw = max(im.width * S, 170)
        big = im.resize((im.width * S, im.height * S), Image.NEAREST)
        out.paste(big, (x + (cw - big.width) // 2, y + h - big.height), big)
        d.text((x + cw // 2, y + h + 6), names[k], font=F, fill=INK, anchor='ma')
        x += cw + pad
    y += h + 56

# quick layout test: iso grid of the tiles + objects (not a game map, just to see them together), shown x2
d.text((20, y), 'ลองวางรวมกัน ขยายสองเท่า', font=F, fill=INK); y += 34
m = Image.new('RGBA', (mapW, mapH), BG + (255,))
tiles = {k: Image.open(k + '.png').convert('RGBA') for k in ['tile_grass', 'tile_dirt', 'tile_rock', 'tile_water', 'tile_cliff']}
N = 10
def kind(i, j):
    if i + j >= 15: return 'tile_water'
    if i + j == 14: return 'tile_rock'
    if 3 <= i <= 6 and 3 <= j <= 6: return 'tile_dirt'
    if (i, j) in [(1, 7), (2, 8), (8, 1), (7, 2), (8, 2)]: return 'tile_rock'
    return 'tile_grass'
ox, oy = mapW // 2 - 16, 90
for s in range(2 * N):
    for i in range(N):
        j = s - i
        if 0 <= j < N:
            m.alpha_composite(tiles[kind(i, j)], (ox + (i - j) * 16, oy + (i + j) * 8))
def put(k, i, j):
    im = Image.open(k + '.png').convert('RGBA')
    bb = im.getbbox()
    cx = ox + (i - j) * 16 + 16
    cy = oy + (i + j) * 8 + 8
    m.alpha_composite(im, (cx - im.width // 2, cy - bb[3] + 6))
PL = [('prop_tree', 0, 0), ('prop_tree', 9, 0), ('obj_totem', 1, 3), ('obj_hut2', 3, 0), ('obj_leanto', 0, 6),
      ('obj_rack', 7, 2), ('obj_hut', 8, 5), ('prop_pots', 2, 8), ('obj_campfire', 4, 4), ('prop_firewood', 6, 4),
      ('prop_flint', 6, 8), ('prop_skull', 3, 6), ('obj_fence', 0, 9)]
for k, i, j in sorted(PL, key=lambda e: e[1] + e[2]):
    put(k, i, j)
out.paste(m.resize((mapW * 2, mapH * 2), Image.NEAREST), (20, y))
out.save('sheet.png')
print(out.size)
