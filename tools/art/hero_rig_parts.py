"""The Eclipse Knight as rig parts: EVERY body part is cut from one picture (hero_base.png), the blade from hero_blade.png.

  python tools/art/hero_rig_parts.py <folder with the pictures> art/dune/hero_rig

Hand-drawn seed lines + a watershed on the outlines find each part. Colours are extended only under the parts drawn in front,
so the standing pose is unchanged and no hole opens at a joint. -> atlas.webp, rig.json, parts_map.png
"""
import sys, os, json, colorsys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd

SRC, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True); KEEP = .42          # atlas scale
D = lambda x, y: (x / .625, y / .625)                                                       # coordinates read off the review picture
L = lambda *q: [D(*p) for p in q]
J = {'root': D(335, 865), 'hips': D(335, 545), 'chest': D(340, 470), 'head': D(335, 368), 'thigh_f': D(290, 562), 'shin_f': D(278, 682), 'foot_f': D(262, 802), 'thigh_b': D(375, 562), 'shin_b': D(382, 680), 'foot_b': D(388, 802),
     'arm_w': D(420, 402), 'fore_w': D(437, 490), 'hand_w': D(480, 560), 'blade': D(484, 592), 'arm_n': D(246, 402), 'fore_n': D(208, 490), 'hand_n': D(166, 560)}
PARENT = {'root': None, 'hips': 'root', 'chest': 'hips', 'head': 'chest', 'thigh_f': 'hips', 'shin_f': 'thigh_f', 'foot_f': 'shin_f', 'thigh_b': 'hips', 'shin_b': 'thigh_b', 'foot_b': 'shin_b',
          'arm_w': 'chest', 'fore_w': 'arm_w', 'hand_w': 'fore_w', 'blade': 'hand_w', 'arm_n': 'chest', 'fore_n': 'arm_n', 'hand_n': 'fore_n'}
PARTS = [  # back to front
    ('thigh_b', [L((372, 585), (388, 650)), L((352, 600), (402, 620))]), ('shin_b', [L((388, 680), (375, 760)), L((362, 690), (412, 690)), L((360, 735), (395, 735)), L((372, 652), (410, 652))]), ('foot_b', [L((365, 835), (440, 850)), L((360, 800), (415, 802)), L((400, 835))]),
    ('thigh_f', [L((292, 585), (278, 650)), L((262, 610), (312, 610))]), ('shin_f', [L((278, 680), (250, 760)), L((252, 685), (302, 690)), L((232, 735), (270, 735)), L((250, 652), (300, 652))]), ('foot_f', [L((225, 835), (300, 850)), L((222, 800), (276, 802)), L((262, 835))]),
    ('hips', [L((285, 530), (336, 528), (392, 535)), L((262, 568), (300, 552)), L((405, 572), (375, 552)), L((336, 548), (340, 565))]),
    ('chest', [L((300, 420), (360, 430), (405, 425)), L((330, 490), (352, 480)), L((360, 405), (300, 395)), L((292, 392), (340, 386), (392, 388)), L((280, 420), (292, 455)), L((400, 455), (392, 420)), L((378, 398), (392, 412))]),
    ('scarf', [L((285, 352), (335, 368), (382, 368))]),
    ('head', [L((205, 200), (330, 170), (445, 235)), L((165, 270), (300, 300)), L((330, 332), (405, 340), (390, 410)), L((245, 300), (270, 320)), L((280, 325), (300, 345)), L((130, 245), (190, 240)), L((470, 240))]),
    ('arm_w', [L((418, 395), (432, 462)), L((405, 385), (450, 420)), L((418, 440), (440, 470))]), ('fore_w', [L((437, 492), (465, 530)), L((445, 480), (475, 548))]), ('hand_w', [L((472, 585), (498, 598)), L((480, 608))]),
    ('arm_n', [L((245, 395), (222, 462)), L((192, 415), (262, 395)), L((252, 435), (222, 470))]), ('fore_n', [L((208, 492), (175, 530)), L((160, 548), (192, 552))]), ('hand_n', [L((150, 590), (182, 598)), L((165, 610))]),
]
A = np.array(Image.open(f'{SRC}/hero_base.png').convert('RGB')).astype(float); H, W = A.shape[:2]
def key(a):
    m = np.minimum(a[..., 0], a[..., 2]) - a[..., 1]; al = 1 - np.clip((m - 62) / 118, 0, 1); q = np.clip(al, .08, 1)[..., None]; c = np.clip((a - (1 - q) * np.array([255., 0, 255])) / q, 0, 255); e = (al > 0) & (al < .98); c[e, 2] = np.minimum(c[e, 2], np.maximum(c[e, 0], c[e, 1]) * 1.04); return c.astype(np.uint8), (al * 255).astype(np.uint8)
rgb, alpha = key(A); fig = alpha >= 16
dark = 255 - rgb.mean(2); grad = np.max([np.hypot(nd.sobel(rgb[..., c].astype(float), 0), nd.sobel(rgb[..., c].astype(float), 1)) for c in range(3)], 0); cost = np.clip(dark * .42 + grad * .62, 0, 255).astype(np.uint8)
seed = Image.new('I', (W, H), 0); d = ImageDraw.Draw(seed)
for i, (_, ls) in enumerate(PARTS):
    for l in ls:
        if len(l) > 1: d.line(l, fill=i + 1, width=7)
        else: d.ellipse([l[0][0] - 5, l[0][1] - 5, l[0][0] + 5, l[0][1] + 5], fill=i + 1)
seeds = np.array(seed).astype(np.int16); mk = seeds.copy(); mk[alpha < 16] = len(PARTS) + 1
lab = nd.watershed_ift(cost, mk, structure=np.ones((3, 3), int)).astype(np.int16); lab[~fig] = 0
keep = np.zeros_like(lab, bool)
for i in range(1, len(PARTS) + 1):
    m = nd.binary_opening(lab == i, iterations=3) | ((lab == i) & (seeds == i)); l, n = nd.label(m, structure=np.ones((3, 3)))
    if n: cs = nd.sum(m, l, range(1, n + 1)); ok = {int(q) for q in set(np.unique(l[(seeds == i) & m])) - {0} if cs[int(q) - 1] >= 400}; ok.add(int(np.argmax(cs)) + 1); keep |= np.isin(l, list(ok))
idx = nd.distance_transform_edt(~keep, return_distances=False, return_indices=True); lab[fig] = lab[idx[0], idx[1]][fig]; lab[~fig] = 0
for _ in range(2):
    for i in range(1, len(PARTS) + 1):
        l, n = nd.label(lab == i, structure=np.ones((3, 3)))
        if n < 2: continue
        cs = nd.sum(lab == i, l, range(1, n + 1))
        for q in np.where(cs < 500)[0] + 1:
            if q == int(np.argmax(cs)) + 1: continue
            c = l == q; ring = nd.binary_dilation(c, iterations=2) & ~c; v = lab[ring]; v = v[(v > 0) & (v != i)]
            if len(v): lab[c] = np.bincount(v).argmax()
tiles = []; over = rgb.astype(float).copy()
for i, (n, _) in enumerate(PARTS):
    m = lab == i + 1; col = np.array(colorsys.hsv_to_rgb(i * .618 % 1, .8, 1)) * 255; over[m] = over[m] * .35 + col * .65; a = np.where(m, alpha, 0).astype(np.uint8); c = rgb.copy(); front = fig & (lab > i + 1)
    if n != 'head':
        ext = nd.binary_dilation(m, iterations=30, mask=m | front) & front & ~m; ext = nd.binary_opening(ext | m, iterations=3) & ext; ll, _ = nd.label(ext | m, structure=np.ones((3, 3))); ext &= np.isin(ll, list(set(np.unique(ll[m])) - {0}))
        core = nd.binary_erosion(m, iterations=5); core = core if core.sum() > 60 else m; ni = nd.distance_transform_edt(~core, return_distances=False, return_indices=True); c[ext] = rgb[ni[0], ni[1]][ext]; a[ext] = 255
    ys, xs = np.where(a > 0); x0, y0, x1, y1 = max(0, xs.min() - 3), max(0, ys.min() - 3), min(W, xs.max() + 4), min(H, ys.max() + 4)
    tiles.append({'name': n, 'bone': n if n not in ('scarf',) else 'chest', 'x': int(x0), 'y': int(y0), 'w': int(x1 - x0), 'h': int(y1 - y0), 'px': np.dstack([c, a])[y0:y1, x0:x1]})
# the blade: its own picture, grip on the hand joint; about .94 x the picture scale
B = np.array(Image.open(f'{SRC}/hero_blade.png').convert('RGB')).astype(float); bc, ba = key(B); ys, xs = np.where(ba > 40); bx0, by0, bx1, by1 = xs.min() - 3, ys.min() - 3, xs.max() + 4, ys.max() + 4; BK = .94; bim = Image.fromarray(np.dstack([bc, ba])[by0:by1, bx0:bx1], 'RGBA'); bim = bim.resize((round(bim.width * BK), round(bim.height * BK)), Image.LANCZOS)
gx, gy = (512 - bx0) * BK, (752 - by0) * BK; jb = J['blade']; tiles.insert([t['name'] for t in tiles].index('hand_w'), {'name': 'blade', 'bone': 'blade', 'x': int(round(jb[0] - gx)), 'y': int(round(jb[1] - gy)), 'w': bim.width, 'h': bim.height, 'px': np.array(bim), 'upright': 1})
AW = 2048; x = y = rowh = 0
for t in sorted(tiles, key=lambda q: -q['h']):
    t['aw'], t['ah'] = max(1, round(t['w'] * KEEP)), max(1, round(t['h'] * KEEP))
    if x + t['aw'] + 4 > AW: x = 0; y += rowh + 4; rowh = 0
    t['ax'], t['ay'] = x, y; x += t['aw'] + 4; rowh = max(rowh, t['ah'])
atlas = Image.new('RGBA', (AW, y + rowh), (0, 0, 0, 0))
for t in tiles: atlas.paste(Image.fromarray(t['px'], 'RGBA').resize((t['aw'], t['ah']), Image.LANCZOS), (t['ax'], t['ay']))
atlas.save(f'{OUT}/atlas.webp', 'WEBP', quality=93, alpha_quality=100, method=6)
Image.fromarray(over.astype(np.uint8)).crop((150, 70, 860, 1420)).save(f'{OUT}/parts_map.png')
json.dump({'bones': {k: {'p': PARENT[k], 'x': round(J[k][0], 1), 'y': round(J[k][1], 1)} for k in J}, 'parts': [{k: t[k] for k in ('name', 'bone', 'x', 'y', 'w', 'h', 'ax', 'ay', 'aw', 'ah')} for t in tiles]}, open(f'{OUT}/rig.json', 'w'), separators=(',', ':'))
back = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for t in tiles:
    if t['name'] != 'blade': back.alpha_composite(Image.fromarray(t['px'], 'RGBA'), (t['x'], t['y']))
e = np.abs(np.array(back).astype(int)[..., :3] - rgb.astype(int)).max(2)[alpha > 200]
print(len(tiles), 'parts, atlas', AW, y + rowh, os.path.getsize(f'{OUT}/atlas.webp') // 1024, 'KB; rest error mean', round(float(e.mean()), 2), 'over 12:', round(float((e > 12).mean() * 100), 3), '%')
