"""Icons for the crafted items of bag3d.html (owner 2026-11-26 "ระบบผสมไอเทม"), free: made from our own item icons.
Each crafted icon = the main ingredient's icon, colour-graded toward the recipe's element + a soft glow in that colour,
with the second ingredient's icon small in the bottom-right corner on a dark disc, and a few pixel sparkles.
Out: art/bag3d/icons_all.png = art/bag/icons.png (5 rows) + 2 rows of crafted icons (64 px cells, 8 a row), order = CRAFTED below
(the same order as the CRAFT table in bag3d.html).  usage: python3 tools/art/bag_craft_icons.py"""
from PIL import Image, ImageFilter, ImageChops
ORDER = ['dagger','sword','bow','axe','hammer','wand','poison','bomb','shield','helm','cactus','feather','apple','meat','juice','stone','glove','clover','ember','frost',
         'heart','star','pig','crown','spear','claw','scythe','shuriken','club','orb','icestaff','skull','book','meteor','plate','cloak','ring','wine','fang','hourglass']
CRAFTED = [  # result, main icon, small icon, element colour
    ('flamesword', 'sword', 'ember', (255, 120, 30)), ('venomknife', 'dagger', 'poison', (120, 255, 80)), ('frostbow', 'bow', 'frost', (110, 215, 255)),
    ('bloodaxe', 'axe', 'fang', (255, 40, 60)), ('thunderhammer', 'hammer', 'orb', (190, 140, 255)), ('archstaff', 'wand', 'book', (210, 110, 255)),
    ('vampclaw', 'claw', 'heart', (255, 40, 100)), ('comet', 'meteor', 'bomb', (255, 170, 60)), ('fortress', 'shield', 'helm', (255, 215, 110)),
    ('spikeshield', 'shield', 'cactus', (150, 255, 120)), ('feast', 'meat', 'wine', (255, 150, 80)), ('luckycoin', 'pig', 'clover', (255, 220, 80))]
SRC = Image.open('art/bag/icons.png').convert('RGBA')
def cell(k):
    i = ORDER.index(k); return SRC.crop((i % 8 * 64, i // 8 * 64, i % 8 * 64 + 64, i // 8 * 64 + 64))
def grade(im, col, amt=.38):
    r, g, b, a = im.split(); L = Image.merge('RGB', (r, g, b)).convert('L')
    tint = Image.merge('RGB', [L.point(lambda v, c=c: min(255, int(v * c / 200))) for c in col])
    out = Image.blend(Image.merge('RGB', (r, g, b)), tint, amt); out.putalpha(a); return out
def icon(main, small, col):
    m0 = grade(cell(main), col, .45).resize((52, 52), Image.LANCZOS); m = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); m.alpha_composite(m0, (5, 4)); a = m.split()[3]
    glow = a.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(2.5)).point(lambda v: min(255, int(v * 1.5)))
    base = Image.new('RGBA', (64, 64), col + (0,)); base.putalpha(glow)
    out = Image.alpha_composite(base, m)
    s = cell(small).resize((30, 30), Image.LANCZOS); disc = Image.new('RGBA', (34, 34), (0, 0, 0, 0))
    from PIL import ImageDraw
    d = ImageDraw.Draw(disc); d.ellipse((0, 0, 33, 33), fill=(20, 10, 16, 230), outline=col + (255,), width=2)
    disc.alpha_composite(s, (2, 2)); out.alpha_composite(disc, (30, 30))
    d = ImageDraw.Draw(out)
    for x, y in [(8, 8), (54, 10), (6, 40)]:
        d.point([(x, y - 1), (x - 1, y), (x, y), (x + 1, y), (x, y + 1)], fill=(255, 255, 230, 255))
    return out
sheet = Image.new('RGBA', (512, 448), (0, 0, 0, 0)); sheet.paste(SRC, (0, 0))
for n, (k, a, b, c) in enumerate(CRAFTED):
    sheet.paste(icon(a, b, c), (n % 8 * 64, 320 + n // 8 * 64))
sheet.save('art/bag3d/icons_all.png'); print('ok', len(CRAFTED))
