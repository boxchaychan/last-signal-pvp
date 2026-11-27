"""Icons for the crafted items of bag3d.html (owner 2026-11-26 "ระบบผสมไอเทม"), free: made from our own item icons.
Each crafted icon = the main ingredient's icon, colour-graded toward the recipe's element + a soft glow in that colour,
with the second ingredient's icon small in the bottom-right corner on a dark disc, and a few pixel sparkles.
Out: art/bag3d/icons_all.png = art/bag/icons.png (5 rows) + 2 rows of crafted icons (64 px cells, 8 a row), order = CRAFTED below
(the same order as the CRAFT table in bag3d.html).  usage: python3 tools/art/bag_craft_icons.py
   --sheet <png> [cols 4] [rows 3]: use the owner's ChatGPT sheet instead (12 icons in a grid on flat magenta, PROMPT in
   art/incoming/bag3d/PROMPT_craft_icons.txt): each cell is keyed off magenta, trimmed, fitted into 60 px (nearest step-down to keep
   it crisp) and centred in its 64 px cell; cells it cannot read fall back to the code-made icon. The raw sheet stays in art/incoming/bag3d/."""
import sys, glob, os, shutil
from PIL import Image, ImageFilter, ImageChops
ORDER = ['dagger','sword','bow','axe','hammer','wand','poison','bomb','shield','helm','cactus','feather','apple','meat','juice','stone','glove','clover','ember','frost',
         'heart','star','pig','crown','spear','claw','scythe','shuriken','club','orb','icestaff','skull','book','meteor','plate','cloak','ring','wine','fang','hourglass']
CRAFTED = [  # result, main icon, small icon, element colour
    ('flamesword', 'sword', 'ember', (255, 120, 30)), ('venomknife', 'dagger', 'poison', (120, 255, 80)), ('frostbow', 'bow', 'frost', (110, 215, 255)),
    ('bloodaxe', 'axe', 'fang', (255, 40, 60)), ('thunderhammer', 'hammer', 'orb', (190, 140, 255)), ('archstaff', 'wand', 'book', (210, 110, 255)),
    ('vampclaw', 'claw', 'heart', (255, 40, 100)), ('comet', 'meteor', 'bomb', (255, 170, 60)), ('fortress', 'shield', 'helm', (255, 215, 110)),
    ('spikeshield', 'shield', 'cactus', (150, 255, 120)), ('feast', 'meat', 'wine', (255, 150, 80)), ('luckycoin', 'pig', 'clover', (255, 220, 80))]
# 24 shop items added 2026-11-26 ("เพิ่มของไปอีก"): code-made from our icons until the owner's ChatGPT sheets come
# ('var', src, tint, amount, rotate deg, scale, flip) or ('pair', src a, src b, tint) = two icons crossed
NEWITEMS = [('twinblades', 'pair', 'dagger', 'dagger', (190, 200, 255)), ('rapier', 'var', 'sword', (235, 240, 255), .3, -18, .9, False), ('greatsword', 'var', 'sword', (150, 70, 220), .55, 0, 1.0, True),
    ('katana', 'var', 'sword', (150, 225, 255), .45, 28, .95, False), ('javelin', 'var', 'spear', (255, 220, 150), .35, -12, 1.0, False), ('chakram', 'var', 'shuriken', (255, 130, 40), .6, 20, 1.0, False),
    ('holytome', 'var', 'book', (255, 225, 130), .6, 0, 1.0, False), ('voidorb', 'var', 'orb', (110, 40, 170), .6, 0, 1.0, False), ('buckler', 'var', 'shield', (215, 150, 80), .5, 0, .78, False),
    ('towershield', 'var', 'shield', (170, 200, 230), .45, 0, 1.0, False), ('boots', 'var', 'feather', (110, 230, 210), .55, 35, 1.0, False), ('amulet', 'var', 'heart', (255, 215, 110), .6, 0, .9, False),
    ('bread', 'var', 'apple', (215, 160, 80), .65, 0, .95, False), ('potion', 'var', 'wine', (255, 60, 80), .4, 0, 1.05, False), ('honey', 'var', 'juice', (255, 175, 40), .65, 0, 1.0, False),
    ('elixir', 'var', 'juice', (255, 225, 110), .6, 0, 1.05, True), ('furyrune', 'var', 'ember', (255, 50, 40), .5, 0, 1.0, False), ('venomgland', 'var', 'poison', (90, 200, 60), .55, 0, 1.0, True),
    ('thunderstone', 'var', 'stone', (170, 130, 255), .65, 0, 1.0, False), ('holyseal', 'var', 'star', (255, 240, 170), .5, 0, 1.0, False), ('ragemask', 'var', 'fang', (255, 40, 40), .55, 0, 1.0, True),
    ('wardrum', 'var', 'bomb', (200, 130, 70), .6, 0, 1.0, False), ('lantern', 'var', 'hourglass', (255, 190, 90), .5, 0, 1.0, False), ('goldbag', 'var', 'pig', (255, 210, 60), .7, 0, 1.0, True)]
CRAFTED2 = [('stormblades', 'twinblades', 'feather', (150, 220, 255)), ('luckrapier', 'rapier', 'clover', (140, 255, 120)), ('executioner', 'greatsword', 'fang', (255, 50, 60)),
    ('frostlance', 'javelin', 'frost', (120, 215, 255)), ('divinetome', 'holytome', 'ring', (255, 235, 140)), ('parrybuckler', 'buckler', 'glove', (255, 200, 110)),
    ('honeybread', 'bread', 'juice', (255, 190, 70)), ('soullantern', 'lantern', 'skull', (190, 90, 255))]
SRC = Image.open('art/bag/icons.png').convert('RGBA')
MADE = {}
def cell(k):
    if k in MADE: return MADE[k].copy()
    i = ORDER.index(k); return SRC.crop((i % 8 * 64, i // 8 * 64, i % 8 * 64 + 64, i // 8 * 64 + 64))
def var(src, col, amt, rot, sc, flip):
    m = grade(cell(src), col, amt)
    if flip: m = m.transpose(Image.FLIP_LEFT_RIGHT)
    if rot: m = m.rotate(rot, Image.BICUBIC, expand=False)
    if sc != 1: w = max(8, round(64 * sc)); m2 = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); m2.alpha_composite(m.resize((w, w), Image.LANCZOS), ((64 - w) // 2, (64 - w) // 2)); m = m2
    return m
def pair(a, b, col):
    out = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    for src, rot, dx in ((a, 28, -6), (b, -28, 6)):
        m = grade(cell(src), col, .35).resize((52, 52), Image.LANCZOS).rotate(rot, Image.BICUBIC, expand=False)
        out.alpha_composite(m, (6 + dx, 6))
    return out
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
def from_sheet(path, cols=4, rows=3):
    im = Image.open(path).convert('RGBA'); W, H = im.size; out = []
    for n in range(cols * rows):
        c = im.crop((n % cols * W // cols, n // cols * H // rows, (n % cols + 1) * W // cols, (n // cols + 1) * H // rows)); px = c.load()
        for y in range(c.height):
            for x in range(c.width):
                r, g, b, a = px[x, y]
                if r > 150 and b > 150 and g < 110 and abs(r - b) < 90: px[x, y] = (0, 0, 0, 0)   # flat magenta key
                elif r > 120 and b > 120 and g < r * .55 and g < b * .55: px[x, y] = (r, g, b, int(a * .25))   # magenta fringe
        bb = c.getbbox()
        if not bb or (bb[2] - bb[0]) < 8: out.append(None); continue
        c = c.crop(bb); k = 60 / max(c.size); w, h = max(1, round(c.width * k)), max(1, round(c.height * k))
        big = c.resize((w * 4, h * 4), Image.LANCZOS); c = big.resize((w, h), Image.NEAREST)
        cell = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); cell.alpha_composite(c, ((64 - w) // 2, (64 - h) // 2)); out.append(cell)
    return out
# the order of the IT table in bag3d.html after the 40 originals: CRAFTED, NEWITEMS, CRAFTED2
ALL = [k for k, *_ in CRAFTED] + [k for k, *_ in NEWITEMS] + [k for k, *_ in CRAFTED2]
for k, op, *a in NEWITEMS: MADE[k] = var(a[0], *a[1:]) if op == 'var' else pair(a[0], a[1], a[2])
code = {k: icon(a, b, c) for k, a, b, c in CRAFTED}; code.update({k: MADE[k] for k, *_ in NEWITEMS}); code.update({k: icon(a, b, c) for k, a, b, c in CRAFTED2})
# PixelLab icons (art/incoming/bag3d/gen.py, the same recipe as the 40 originals, used raw like them) replace the code-made ones
for k in ALL:
    f = f'art/incoming/bag3d/pl/{k}.png'
    if os.path.exists(f): code[k] = Image.open(f).convert('RGBA').resize((64, 64), Image.NEAREST)
# owner's ChatGPT sheets that already came in (art/incoming/bag3d/sheet_<first id>_<cols>x<rows>.png, kept and re-used), then a new one:
#   python3 tools/art/bag_craft_icons.py --sheet <png> <first id> [cols 4] [rows 3]
if len(sys.argv) > 3 and sys.argv[1] == '--sheet':
    c, r = (int(v) for v in (sys.argv[4:6] if len(sys.argv) > 5 else (4, 3))); dst = f'art/incoming/bag3d/sheet_{sys.argv[3]}_{c}x{r}.png'
    if os.path.abspath(sys.argv[2]) != os.path.abspath(dst): shutil.copy(sys.argv[2], dst)
sheets = sorted(glob.glob('art/incoming/bag3d/sheet_*_*x*.png'))
for sh in sheets:
    first, grid = os.path.basename(sh)[6:-4].rsplit('_', 1); c, r = (int(v) for v in grid.split('x'))
    for n, im in enumerate(from_sheet(sh, c, r)):
        j = ALL.index(first) + n
        if im is not None and j < len(ALL): code[ALL[j]] = im
rows = (40 + len(ALL) + 7) // 8
sheet = Image.new('RGBA', (512, rows * 64), (0, 0, 0, 0)); sheet.paste(SRC, (0, 0))
for n, k in enumerate(ALL): sheet.paste(code[k], ((40 + n) % 8 * 64, (40 + n) // 8 * 64))
sheet.save('art/bag3d/icons_all.png'); print('ok', len(ALL), 'icons,', rows, 'rows, sheets used:', len(sheets))
