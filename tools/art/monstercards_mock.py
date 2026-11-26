# python3 tools/art/monstercards_mock.py -> art/incoming/monstercards/mock_lanes_v1.png (needs the Loma Thai font)
# mock-up picture of the monster card game (lanes), real pixel monsters, free
from PIL import Image, ImageDraw, ImageFont
import json, math
M = json.load(open('art/horde/mobs/index.json'))['mobs']
def mob(k, half=False):
    m = M[k]; im = Image.open(m['f']).convert('RGBA').crop((0, 0, m['w'], m['h']))
    im = im.resize((m['w'] // 2, m['h'] // 2), Image.NEAREST)   # image is art x2 -> art x1
    fx, fy = m['fx'] // 2, m['fy'] // 2
    if half: im = im.resize((im.width // 2, im.height // 2), Image.NEAREST); fx //= 2; fy //= 2
    bb = im.getbbox(); return im, fx, fy
W, H = 844, 390
img = Image.new('RGBA', (W, H), (226, 170, 116, 255)); d = ImageDraw.Draw(img)
# sand ripples
for y in range(H):
    for x in range(0, W, 2):
        v = math.sin(x * .05 + y * .16 + math.sin(x * .013) * 2.2)
        if v > .82: d.point((x, y), (210, 152, 102, 255)); d.point((x + 1, y), (210, 152, 102, 255))
# stone table / lanes
BX0, BX1, LY0, LH, N = 150, 694, 30, 52, 5
d.rectangle((BX0 - 8, LY0 - 8, BX1 + 8, LY0 + LH * N + 6), fill=(120, 84, 70, 255))
for i in range(N):
    y0 = LY0 + i * LH
    for j, (x0, x1) in enumerate(((BX0, (BX0 + BX1) // 2 - 2), ((BX0 + BX1) // 2 + 2, BX1))):
        c = (196, 160, 122, 255) if (i + j) % 2 == 0 else (186, 150, 114, 255)
        d.rectangle((x0, y0 + 2, x1, y0 + LH - 2), fill=c); d.line((x0, y0 + LH - 2, x1, y0 + LH - 2), fill=(150, 112, 88, 255))
    d.line(((BX0 + BX1) // 2, y0 + 2, (BX0 + BX1) // 2, y0 + LH - 2), fill=(232, 210, 160, 255))
SLOT = {0: 300, 1: 545}   # our slot x, enemy slot x
def put(k, lane, side, half=False):
    im, fx, fy = mob(k, half)
    if side == 0: im = im.transpose(Image.FLIP_LEFT_RIGHT); fx = im.width - fx
    x = SLOT[side] - fx; y = LY0 + lane * LH + LH - 6 - fy
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((SLOT[side] - 22, LY0 + lane * LH + LH - 10, SLOT[side] + 22, LY0 + lane * LH + LH - 3), fill=(90, 50, 60, 90))
    img.alpha_composite(sh); img.alpha_composite(im, (x, y))
# summoners
hero = Image.open('art/incoming/pixgrind/chibi/chibi_native.png').convert('RGBA').transpose(Image.FLIP_LEFT_RIGHT)
img.alpha_composite(hero, (40, LY0 + 2 * LH + LH - 6 - hero.height + 20))
boss, bfx, bfy = mob('boss_desert_tomb_king', half=True)
img.alpha_composite(boss, (W - 30 - boss.width, LY0 + 2 * LH + LH - boss.height + 30))
# lanes, drawn top to bottom so lower monsters overlap upper ones
order = [(0, 'mob_desert_stingclaw_scorpion', 0, False), (0, 'mob_desert_linenwalker', 1, False),
         (1, 'mob_desert_spinewalker', 0, False),
         (2, 'mob_desert_dune_viper', 1, False),
         (3, 'mob_desert_fortress_tortoise', 0, False), (3, 'mob_desert_sandstone_colossus', 1, True)]
for lane, k, side, half in order: put(k, lane, side, half)
# effects: clash in lane 1, cactus hits the enemy summoner (empty lane 2), viper hits us (empty lane 3)
def star(cx, cy, r, col):
    pts = [(cx + math.cos(a * math.pi / 5) * (r if a % 2 == 0 else r * .45), cy + math.sin(a * math.pi / 5) * (r if a % 2 == 0 else r * .45)) for a in range(10)]
    d.polygon(pts, fill=col)
star(423, LY0 + 26, 11, (255, 240, 170, 255)); star(423, LY0 + 26, 6, (255, 255, 255, 255))
for x in range(330, 760, 14): d.line((x, LY0 + LH + 30, x + 8, LY0 + LH + 30), fill=(255, 236, 150, 255), width=2)
d.polygon([(764, LY0 + LH + 24), (776, LY0 + LH + 30), (764, LY0 + LH + 36)], fill=(255, 236, 150, 255))
for x in range(520, 110, -14): d.line((x, LY0 + 2 * LH + 30, x - 8, LY0 + 2 * LH + 30), fill=(255, 150, 140, 255), width=2)
d.polygon([(104, LY0 + 2 * LH + 24), (92, LY0 + 2 * LH + 30), (104, LY0 + 2 * LH + 36)], fill=(255, 150, 140, 255))
# empty lane 5: glowing slot where the dragged card goes
gx = SLOT[0]; gy = LY0 + 4 * LH
d.rectangle((gx - 34, gy + 5, gx + 34, gy + LH - 5), outline=(120, 240, 255, 255), width=2)
img.save('/tmp/monstercards_mock_base.png')
# ---- x2, then cards + text at full resolution
Z = 2; big = img.resize((W * Z, H * Z), Image.NEAREST); d = ImageDraw.Draw(big)
F = lambda s: ImageFont.truetype('/usr/share/fonts/opentype/tlwg/Loma-Bold.otf', s)
def txt(x, y, s, size, col=(255, 248, 230), stroke=(50, 28, 20), anchor='la'):
    d.text((x, y), s, font=F(size), fill=col, stroke_width=3, stroke_fill=stroke, anchor=anchor)
def card(x, y, k, cost, atk, hp, name, frame, lift=0, glow=False, rot=0):
    cw, ch = 132, 176; c = Image.new('RGBA', (cw, ch), (0, 0, 0, 0)); cd = ImageDraw.Draw(c)
    cd.rounded_rectangle((0, 0, cw - 1, ch - 1), 12, fill=frame)
    cd.rounded_rectangle((8, 8, cw - 9, ch - 40), 8, fill=(46, 58, 78, 255))
    if k:
        im, fx, fy = mob(k); s = min((cw - 24) / im.width, (ch - 60) / im.height); s = max(1, int(s)) if s >= 1 else .5
        im2 = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.NEAREST).transpose(Image.FLIP_LEFT_RIGHT)
        c.alpha_composite(im2, ((cw - im2.width) // 2, ch - 44 - im2.height))
    cd.ellipse((-4, -4, 36, 36), fill=(60, 120, 230, 255), outline=(220, 240, 255, 255), width=3); cd.text((16, 16), str(cost), font=F(22), fill='white', anchor='mm')
    if atk is not None:
        cd.ellipse((4, ch - 38, 38, ch - 4), fill=(200, 60, 50, 255), outline=(255, 220, 200, 255), width=2); cd.text((21, ch - 21), str(atk), font=F(20), fill='white', anchor='mm')
        cd.ellipse((cw - 38, ch - 38, cw - 4, ch - 4), fill=(60, 160, 70, 255), outline=(220, 255, 220, 255), width=2); cd.text((cw - 21, ch - 21), str(hp), font=F(20), fill='white', anchor='mm')
    cd.text((cw // 2, ch - 30), name, font=F(15), fill=(255, 248, 230), anchor='mm', stroke_width=2, stroke_fill=(40, 24, 20))
    if rot: c = c.rotate(rot, resample=Image.BICUBIC, expand=True)
    if glow:
        g = Image.new('RGBA', (c.width + 16, c.height + 16), (0, 0, 0, 0)); ImageDraw.Draw(g).rounded_rectangle((0, 0, g.width - 1, g.height - 1), 16, fill=(120, 240, 255, 150)); big.alpha_composite(g, (x - 8, y - lift - 8))
    big.alpha_composite(c, (x, y - lift))
GOLD, SILV, STONE = (214, 168, 70, 255), (176, 182, 196, 255), (132, 118, 104, 255)
card(330, 610, 'mob_desert_dune_wolf', 2, 3, 2, 'หมาป่าเนินทราย', SILV, rot=6)
card(470, 600, None, 3, None, None, 'ลูกไฟ', GOLD, rot=2)
card(760, 598, 'mob_desert_jackal_priest', 5, 4, 6, 'นักบวชหมาใน', GOLD, rot=-3)
card(900, 606, 'mob_desert_dune_viper', 1, 1, 2, 'งูพิษ', STONE, rot=-7)
card(690, 560, 'mob_desert_strider_bird', 2, 2, 3, 'นกเท้าไว', SILV, lift=0, glow=True)   # the card being dragged
d = ImageDraw.Draw(big)
# fireball icon on the spell card
d.ellipse((520, 650, 568, 698), fill=(255, 140, 40, 255)); d.ellipse((532, 662, 556, 686), fill=(255, 230, 120, 255))
# drag arrow from the lifted card to lane 5's glowing slot
d.line((700, 566, 650, 540), fill=(120, 240, 255, 255), width=5); d.polygon([(660, 528), (636, 532), (650, 552)], fill=(120, 240, 255, 255))
# top bar + summoner HP + mana + end turn
txt(30, 10, 'ผู้อัญเชิญ   HP 28', 26); txt(W * Z - 30, 10, 'ราชาสุสาน   HP 27', 26, anchor='ra')
for i in range(7): d.polygon([(40 + i * 30, 740), (52 + i * 30, 722), (64 + i * 30, 740), (52 + i * 30, 758)], fill=(80, 170, 255, 255) if i < 5 else (70, 70, 90, 255), outline=(220, 240, 255, 255))
txt(40, 690, 'มานา 5/7', 24)
d.rounded_rectangle((W * Z - 230, 690, W * Z - 40, 760), 18, fill=(200, 80, 50, 255), outline=(255, 220, 180, 255), width=4); d.text((W * Z - 135, 725), 'จบตา', font=F(30), fill='white', anchor='mm')
# explanations
txt(846, 48, 'ตีตัวตรงหน้า', 22, col=(255, 240, 170)); txt(1300, 170, '-3', 34, col=(255, 236, 150)); txt(120, 220, '-2', 34, col=(255, 160, 150))
txt(1060, 152, 'เลนว่าง = ตีผู้อัญเชิญตรงๆ', 22, col=(255, 236, 150)); txt(840, 520, 'ลากการ์ดลงเลน', 22, col=(150, 245, 255))
for i in range(N): txt(BX0 * Z - 34, (LY0 + i * LH) * Z + 40, f'เลน {i + 1}', 18, col=(255, 230, 200))
big.convert('RGB').save('art/incoming/monstercards/mock_lanes_v1.png'); print(big.size)
