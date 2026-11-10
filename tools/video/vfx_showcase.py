# Every cut Berserker effect playing at once next to the hero at game scale (owner 2026-11-10 "ทำมาให้ฉันดูสกิลทั้งหมด").
#   python3 tools/video/vfx_showcase.py <out.gif>
import json, sys
from PIL import Image, ImageDraw, ImageFont
Z = 1.5                                   # picture px per world px (the hero's own pixel size)
F = ImageFont.truetype('/usr/share/fonts/opentype/tlwg/Loma-Bold.otf', 22)
# key, Thai label, where: front = in front of him on the ground, on = centred on him, ground squash for flat (top view) effects
L = [('vfx_bzswing', 'ตีธรรมดา · รอยดาบ', 'front', 1), ('vfx_bzchainall', 'Q โซ่ดึงรอบตัว', 'on', .6), ('vfx_bzchainring', 'Q วงฟันรอบตัว', 'on', .6),
     ('vfx_bztriple', 'E ฟาดสามยมทูต', 'front', 1), ('vfx_bzslam', 'R/F ระเบิดทุบพื้น', 'front', 1), ('vfx_bzslamring', 'R/F คลื่นวงบนพื้น', 'front', .6),
     ('vfx_bzcrack', 'R รอยแตกพุ่ง', 'front', 1), ('vfx_bzhook', 'F โซ่กระชาก', 'hand', 1), ('vfx_bzshackle', 'Z ตรวนนรก', 'front', .6),
     ('vfx_bzrage', 'X ออร่าคลั่ง', 'on', 1), ('vfx_bzwave', 'X คลื่นฟัน', 'front', 1)]
man = json.load(open('fx/manifest.json'))
hero = Image.open('art/incoming/action/berserker/pl_dl_paid/Idle/rotations/south-east.png').convert('RGBA'); hero = hero.crop(hero.getbbox())
PW, PH, COLS = 520, 400, 4; ROWS = -(-len(L) // COLS); T = 72   # 3 s at 24 fps
sheets = {k: Image.open(f'fx/{k}.png').convert('RGBA') for k, *_ in L}
def cell(k, i):
    m = man[k]; c = m.get('cols', m['n']); f = sheets[k].crop(((i % c) * m['w'], (i // c) * m['h'], (i % c + 1) * m['w'], (i // c + 1) * m['h'])); return f, m
frames = []
for t in range(T):
    G = Image.new('RGBA', (PW * COLS, PH * ROWS), (30, 30, 30, 255))
    for j, (k, lab, where, sq) in enumerate(L):
        P = Image.new('RGBA', (PW, PH), (92, 150, 62, 255)); hx, hy = 150, PH - 70
        m = man[k]; i = t % (m['n'] + 10); f, _ = cell(k, min(i, m['n'] - 1)); vis = i < m['n'] or k == 'vfx_bzrage'
        if k == 'vfx_bzrage': f, _ = cell(k, t % m['n'])
        f = f.resize((round(m['w'] * Z), round(m['h'] * Z * sq)), Image.LANCZOS); ax, ay = m['ax'] * Z, m['ay'] * Z * sq
        if where == 'on': ex, ey = hx, hy
        elif where == 'hand': ex, ey = hx + 20, hy - 50
        else: ex, ey = hx + 170, hy
        behind = k in ('vfx_bzchainall', 'vfx_bzchainring', 'vfx_bzslamring', 'vfx_bzshackle', 'vfx_bzrage')   # the aura burns behind him
        if behind and vis: P.alpha_composite(f, (round(ex - ax), round(ey - ay)))
        P.alpha_composite(hero, (hx - hero.width // 2, hy - hero.height))
        if not behind and vis: P.alpha_composite(f, (round(ex - ax), round(ey - ay)))
        d = ImageDraw.Draw(P); d.rectangle((0, 0, PW, 34), fill=(0, 0, 0, 190)); d.text((10, 4), lab, font=F, fill=(255, 225, 120, 255))
        G.alpha_composite(P, ((j % COLS) * PW, (j // COLS) * PH))
    frames.append(G.resize((G.width * 3 // 4, G.height * 3 // 4), Image.LANCZOS).convert('RGB').quantize(200, dither=Image.Dither.NONE))
frames[0].save(sys.argv[1], save_all=True, append_images=frames[1:], duration=42, loop=0); print(sys.argv[1], len(frames))
