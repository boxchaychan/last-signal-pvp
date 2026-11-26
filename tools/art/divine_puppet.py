"""Zeus as a jointed puppet for divine.html, cut from Codex's drawn puppet sheet (art/incoming/divine_game/raw/zeus_parts/exploded_guide_raw.png:
head with neck, torso with shoulder sockets, ball-jointed arms, hands, legs, bolt; transparent background). Free.
  python3 tools/art/divine_puppet.py [preview.png]
Joints are hand-set on the sheet (raw px). Each part hangs on a parent joint with a rest angle; the game turns them. Codex's own final cut
(art/divine/zeus_parts/*.png) was blocky (straight cuts), so the drawn sheet is used instead.
-> art/divine/pup_zeus_<part>.png + art/divine/puppet.json {zeus: {parts: [{n, p, lx, ly, rot, ox, oy, w, h}], h}} in the same scaled px as
   sets.json (Zeus idle body = 200), positions relative to the feet (x mid-legs, y bottom)."""
import json, math, os, sys
import numpy as np
from PIL import Image
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'); D = os.path.join(R, 'art/divine')
SRC = os.path.join(R, 'art/incoming/divine_game/raw/zeus_parts/exploded_guide_raw.png')
BOX = {'head': (590, 5, 1000, 362), 'bolt': (165, 315, 378, 790), 'torso': (625, 380, 955, 772), 'armF': (1010, 405, 1185, 612), 'armW': (412, 405, 590, 612),
       'handF': (1025, 625, 1170, 786), 'handW': (405, 635, 580, 765), 'legL': (553, 762, 736, 1012), 'legR': (834, 762, 1014, 1012)}
SC = {'head': 1.12}   # the head a little bigger: chibi proportions like Codex's idle picture
# name: (parent, attach point on the parent (raw), own joint (raw), world rest angle in degrees); draw order = list order
PUP = [   # owner "ทำไมไม่ซ่อนไว้ใต้แขน": the upper arms hang BEHIND the torso, so the ball joints hide under the shoulders;
         # owner "แขนที่มันเป็นข้อ": the hands lose their own gold cuff and tuck UNDER the arm's cuff, so the arm reads as one piece
    ('legL', 'torso', (722, 708), (645, 792), 0), ('legR', 'torso', (862, 708), (924, 792), 0),
    ('bolt', 'handW', (474, 694), (268, 558), 14), ('handW', 'armW', (460, 572), (500, 690), -40), ('armW', 'torso', (674, 520), (547, 440), 14),
    ('handF', 'armF', (1138, 572), (1090, 702), -22), ('armF', 'torso', (902, 520), (1055, 437), -10),
    ('torso', None, None, (790, 600), 0),
    ('head', 'torso', (787, 452), (790, 352), 0),
]
KEEP = {'handW': lambda x, y: x <= 503, 'handF': lambda x, y: y >= 712 - (x - 1050) * .28}   # cut the hand's own cuff away
src = np.array(Image.open(SRC).convert('RGBA')); src[src[..., 3] < 120] = 0
# the torso's shoulder sockets (brown holes) become skin, so the shoulder looks whole when the arm is tucked behind it
yy, xx = np.mgrid[0:src.shape[0], 0:src.shape[1]]; c = src[..., :3].astype(int)
for sx, sy in ((665, 513), (908, 513)):
    hole = (np.hypot(xx - sx, yy - sy) < 36) & (c[..., 0] > 60) & (c[..., 0] < 170) & (c[..., 1] < 75) & (c[..., 2] < 55) & (c[..., 0] > c[..., 1] * 1.7)
    src[hole, :3] = (253, 181, 142)
order = [p[0] for p in PUP]; spec = {p[0]: p[1:] for p in PUP}; world = {}
def rot(v, a): c, s = math.cos(a), math.sin(a); return (v[0] * c - v[1] * s, v[0] * s + v[1] * c)
for n in ['torso', 'legL', 'legR', 'armF', 'handF', 'head', 'armW', 'handW', 'bolt']:   # parents first
    par, att, own, deg = spec[n]; a = math.radians(deg)
    if par is None: world[n] = (own, a); continue
    pj, pa = world[par]; pown = spec[par][2]; d = rot((att[0] - pown[0], att[1] - pown[1]), pa); world[n] = ((pj[0] + d[0], pj[1] + d[1]), a)
# world bounds of the assembled puppet -> feet anchor and scale
pts = []
for n in order:
    x0, y0, x1, y1 = BOX[n]; (jx, jy), a = world[n]; own = spec[n][2]
    for cx, cy in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)): d = rot((cx - own[0], cy - own[1]), a); pts.append((jx + d[0], jy + d[1]))
ys = [p[1] for p in pts]; FY = max(ys); FX = (world['legL'][0][0] + world['legR'][0][0]) / 2; TOP = min(ys)
K = 322 * (200 / 322) / (FY - TOP)   # whole puppet as tall as Zeus's idle picture in game px (200)
out = []
for n in order:
    par, att, own, deg = spec[n]; x0, y0, x1, y1 = BOX[n]; (jx, jy), a = world[n]
    if par is None: lx, ly, r = (jx - FX) * K, (jy - FY) * K, a
    else: pj, pa = world[par]; d = rot((jx - pj[0], jy - pj[1]), -pa); lx, ly, r = d[0] * K, d[1] * K, a - pa
    sc = SC.get(n, 1); part = src[y0:y1, x0:x1].copy()
    if n in KEEP: gy, gx = np.mgrid[y0:y1, x0:x1]; part[~KEEP[n](gx, gy)] = 0
    im = Image.fromarray(part); w, h = max(1, round(im.width * K * sc)), max(1, round(im.height * K * sc)); im.resize((w, h), Image.LANCZOS).save(os.path.join(D, f'pup_zeus_{n}.png'))
    out.append({'n': n, 'p': par, 'lx': round(lx, 2), 'ly': round(ly, 2), 'rot': round(r, 4), 'ox': round((x0 - own[0]) * K * sc, 2), 'oy': round((y0 - own[1]) * K * sc, 2), 'w': w, 'h': h})
json.dump({'zeus': {'parts': out, 'h': 200}}, open(os.path.join(D, 'puppet.json'), 'w'), indent=1)
if len(sys.argv) > 1:   # preview at 3x the game size, next to Codex's idle picture
    Z = 3; W = H = int(260 * Z); can = Image.new('RGBA', (W * 2, H), (110, 120, 110, 255)); fx, fy = W // 2, H - 20
    T = {}; byn = {p['n']: p for p in out}
    for p in [byn[n] for n in ['torso', 'legL', 'legR', 'armF', 'handF', 'head', 'armW', 'handW', 'bolt']]:
        if p['p'] is None: T[p['n']] = (fx / Z + p['lx'], fy / Z + p['ly'], p['rot'])
        else: px, py, pr = T[p['p']]; d = rot((p['lx'], p['ly']), pr); T[p['n']] = (px + d[0], py + d[1], pr + p['rot'])
    for p in out:
        x, y, r = T[p['n']]; im = Image.open(os.path.join(D, f"pup_zeus_{p['n']}.png")).resize((p['w'] * Z, p['h'] * Z), Image.LANCZOS)
        big = Image.new('RGBA', (W, H)); big.alpha_composite(im, (int(x * Z + p['ox'] * Z), int(y * Z + p['oy'] * Z)))
        big = big.rotate(-math.degrees(r), center=(x * Z, y * Z), resample=Image.BICUBIC); can.alpha_composite(big)
    idle = Image.open(os.path.join(D, 'zeus_idle.png')).convert('RGBA'); idle = idle.resize((idle.width * Z, idle.height * Z), Image.LANCZOS); can.alpha_composite(idle, (W + W // 2 - int(idle.width * .541), fy - idle.height))
    can.save(sys.argv[1]); print('preview', sys.argv[1])
print(json.dumps(out)[:200])
