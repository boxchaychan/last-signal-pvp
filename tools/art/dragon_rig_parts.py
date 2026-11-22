"""Split the painted dragon into rig parts with the ORIGINAL pixels (no AI redraw) and pack them for dragonrig.html.

  python tools/art/dragon_rig_parts.py art/dragonrig

Seeds are hand-drawn lines along each shape; a watershed on the picture's outlines finds the real edge. Each part is then
under-painted: where a part in FRONT of it covers it, its own colours are extended, so no hole shows when the joint moves.
-> atlas.webp, rig.json (bones, parts in draw order), parts_map.png (each part in its own colour)
"""
import sys, os, json, colorsys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
SRC = 'art/incoming/dragon_moves/base_side.png'; CUT = 'art/incoming/dragon_mesh/dragon_side_cut_full.png'

# name, parent, x, y (picture px)
BONES = [
    ('root', None, 660, 1162), ('hips', 'root', 660, 965), ('chest', 'hips', 680, 860), ('head', 'chest', 735, 610),
    ('thigh_b', 'hips', 600, 990), ('shin_b', 'thigh_b', 598, 1062), ('foot_b', 'shin_b', 590, 1132),
    ('thigh_f', 'hips', 722, 990), ('shin_f', 'thigh_f', 726, 1062), ('foot_f', 'shin_f', 735, 1132),
    ('arm_n', 'chest', 642, 772), ('fore_n', 'arm_n', 612, 838), ('fist_n', 'fore_n', 610, 884),
    ('arm_f', 'chest', 770, 725), ('fore_f', 'arm_f', 825, 738), ('hand_f', 'fore_f', 880, 716), ('spear', 'hand_f', 908, 708),
]
CHAINS = {   # hair, cloth and flame: bones that follow through on their own
    'curl': ('head', [(366, 345), (292, 348), (242, 408), (266, 470)]), 'horn_long': ('head', [(640, 395), (486, 332), (345, 272), (280, 172)]),
    'horn_top': ('head', [(602, 322), (532, 238), (452, 205), (392, 222)]), 'ear': ('head', [(656, 342), (592, 242), (526, 150)]),
    'spikes': ('head', [(742, 372), (716, 280), (694, 222)]), 'mane_top': ('head', [(590, 472), (462, 426), (362, 396)]),
    'mane_low': ('head', [(532, 502), (424, 478), (338, 482)]), 'mane_dark': ('head', [(572, 562), (462, 536), (362, 552)]),
    'mantle': ('chest', [(704, 640), (566, 642), (436, 600)]), 'cape_red': ('chest', [(664, 690), (562, 792), (482, 902), (412, 1022), (386, 1124)]),
    'cape_tail': ('chest', [(566, 792), (432, 880), (322, 926), (250, 1006)]), 'flame': ('chest', [(492, 812), (402, 782), (332, 722), (304, 596)]),
}
for c, (par, pts) in CHAINS.items():
    for i, (x, y) in enumerate(pts[:-1]): BONES.append((f'{c}{i}', par if i == 0 else f'{c}{i - 1}', x, y))

# back to front: name, bone (or chain), seed lines, how far it is under-painted
PARTS = [
    ('spear', 'spear', [[(912, 170), (912, 500), (908, 640)], [(908, 780), (908, 1000), (908, 1130)]], 40),
    ('flame', 'flame', [[(330, 640), (300, 720), (372, 762), (442, 802), (340, 832)]], 30),
    ('cape_tail', 'cape_tail', [[(268, 972), (330, 912), (420, 882), (500, 846)]], 46),
    ('cape_red', 'cape_red', [[(394, 1110), (420, 1010), (482, 902), (560, 792), (654, 696)], [(552, 952), (574, 900)]], 54),
    ('arm_f', 'arm_f', [[(778, 742), (818, 734)]], 34),
    ('fore_f', 'fore_f', [[(832, 742), (856, 736)]], 22),
    ('hand_f', 'hand_f', [[(874, 704), (922, 716)]], 12),
    ('shin_b', 'shin_b', [[(586, 1078), (580, 1140)], [(620, 1140)]], 24),
    ('thigh_b', 'thigh_b', [[(566, 1016), (630, 1030)]], 40),
    ('shin_f', 'shin_f', [[(714, 1084), (730, 1140)], [(770, 1140)]], 24),
    ('thigh_f', 'thigh_f', [[(690, 1030), (760, 1020)]], 40),
    ('torso', 'chest', [[(704, 700), (690, 772)], [(650, 790), (750, 786)], [(722, 826), (742, 880), (750, 908)], [(660, 930), (646, 900)], [(786, 900), (806, 950)]], 40),
    ('arm_n', 'arm_n', [[(628, 790), (612, 834)]], 24),
    ('fore_n', 'fore_n', [[(578, 850), (630, 846)]], 12),
    ('fist_n', 'fist_n', [[(592, 884), (632, 900)]], 12),
    ('mantle', 'mantle', [[(420, 590), (520, 604), (622, 620)], [(472, 690), (560, 702), (650, 682)], [(722, 646)]], 34),
    ('mane_dark', 'mane_dark', [[(366, 552), (450, 528), (540, 552)], [(420, 498), (500, 512)]], 36),
    ('mane_low', 'mane_low', [[(344, 482), (410, 472), (500, 492)]], 30),
    ('curl', 'curl', [[(352, 338), (292, 346), (244, 398), (256, 452), (298, 488)]], 22),
    ('horn_long', 'horn_long', [[(284, 175), (326, 256), (416, 306), (520, 346), (636, 384)]], 34),
    ('horn_top', 'horn_top', [[(398, 226), (460, 204), (530, 232), (592, 306)]], 30),
    ('spikes', 'spikes', [[(700, 232), (724, 292), (744, 352)], [(632, 232), (672, 268), (700, 330)]], 30),
    ('ear', 'ear', [[(526, 152), (580, 232), (636, 306), (654, 336)]], 30),
    ('mane_top', 'mane_top', [[(362, 398), (450, 424), (552, 462)]], 32),
    ('face', 'head', [[(585, 395), (700, 430), (800, 515), (852, 544)], [(610, 505), (690, 560), (770, 582)], [(800, 400), (826, 462)]], 0),
]

rgb = np.array(Image.open(SRC).convert('RGB')); alpha = np.array(Image.open(CUT).convert('RGBA'))[..., 3]; H, W = alpha.shape
dark = 255 - rgb.mean(2)
grad = np.max([np.hypot(nd.sobel(rgb[..., c].astype(float), 0), nd.sobel(rgb[..., c].astype(float), 1)) for c in range(3)], 0)
cost = np.clip(dark * .55 + grad * .55, 0, 255).astype(np.uint8)
seed = Image.new('I', (W, H), 0); d = ImageDraw.Draw(seed)
for i, p in enumerate(PARTS):
    for l in p[2]:
        if len(l) > 1: d.line(l, fill=i + 1, width=5)
        else: d.ellipse([l[0][0] - 3, l[0][1] - 3, l[0][0] + 3, l[0][1] + 3], fill=i + 1)
mk = np.array(seed).astype(np.int16); BG = len(PARTS) + 1; mk[alpha < 16] = BG
lab = nd.watershed_ift(cost, mk, structure=np.ones((3, 3), int)).astype(np.int16); lab[alpha < 16] = 0
# the pants are one black shape: split them at the crotch line
TB, TF = [i + 1 for i, p in enumerate(PARTS) if p[0] == 'thigh_b'][0], [i + 1 for i, p in enumerate(PARTS) if p[0] == 'thigh_f'][0]
pants = np.isin(lab, [TB, TF]); xx = np.arange(W)[None, :].repeat(H, 0); lab[pants & (xx < 657)] = TB; lab[pants & (xx >= 657)] = TF
# stray specks (an outline that leaked along a neighbour) go to the nearest real part
keep = np.zeros_like(lab, bool); seeds = np.array(seed).astype(np.int16)
for i in range(1, len(PARTS) + 1):
    m = nd.binary_opening(lab == i, iterations=3) | ((lab == i) & (seeds == i))   # thin strands = an outline that leaked along a neighbour
    l, n = nd.label(m, structure=np.ones((3, 3)))
    if n:
        cs = nd.sum(m, l, range(1, n + 1)); ok = {int(q) for q in set(np.unique(l[(seeds == i) & m])) - {0} if cs[int(q) - 1] >= 800}; ok.add(int(np.argmax(cs)) + 1)   # a small loose island belongs to the neighbour it touches
        keep |= np.isin(l, list(ok))
fig = alpha >= 16; idx = nd.distance_transform_edt(~keep, return_distances=False, return_indices=True)
lab[fig] = lab[idx[0], idx[1]][fig]; lab[~fig] = 0
for _ in range(2):   # a small island (a tip's outline) joins the part it actually touches
    for i in range(1, len(PARTS) + 1):
        l, n = nd.label(lab == i, structure=np.ones((3, 3)))
        if n < 2: continue
        cs = nd.sum(lab == i, l, range(1, n + 1))
        for q in np.where(cs < 800)[0] + 1:
            if q == int(np.argmax(cs)) + 1: continue
            c = l == q; ring = nd.binary_dilation(c, iterations=2) & ~c; v = lab[ring]; v = v[(v > 0) & (v != i)]
            if len(v): lab[c] = np.bincount(v).argmax()

tiles = []; over = rgb.astype(float).copy()
for i, (n, b, _, reach) in enumerate(PARTS):
    m = lab == i + 1; col = np.array(colorsys.hsv_to_rgb(i * .618 % 1, .8, 1)) * 255; over[m] = over[m] * .35 + col * .65
    a = np.where(m, alpha, 0).astype(np.uint8); c = rgb.copy()
    if reach:
        front = fig & (lab > i + 1)
        if n in ('thigh_b', 'shin_b'): front &= ~np.isin(lab, [q + 1 for q, r in enumerate(PARTS) if r[0] in ('thigh_f', 'shin_f')])   # the back leg never hides pixels under the front leg: they would show as scraps when the legs part
        ext = nd.binary_dilation(m, iterations=reach, mask=m | front) & front
        ext = nd.binary_opening(ext | m, iterations=4) & ext                  # no thin spikes
        ll, _ = nd.label(ext | m, structure=np.ones((3, 3))); ext &= np.isin(ll, list(set(np.unique(ll[m])) - {0}))   # no scraps cut off from the part
        core = nd.binary_erosion(m, iterations=4); core = core if core.sum() > 40 else m
        ni = nd.distance_transform_edt(~core, return_distances=False, return_indices=True)
        c[ext] = rgb[ni[0], ni[1]][ext]; soft = nd.gaussian_filter(c.astype(float), (2, 2, 0)); c[ext] = soft[ext].astype(np.uint8); a[ext] = 255
    cl, cn = nd.label(a > 0, structure=np.ones((3, 3)))
    if cn > 1:   # a few loose specks of the old background cut would float away from the body
        cs = nd.sum(a > 0, cl, range(1, cn + 1)); drop = np.where(cs < max(140, cs.max() * .004))[0] + 1
        if len(drop): print('  ', n, 'specks removed:', len(drop), int(cs[drop - 1].sum()), 'px'); a[np.isin(cl, drop)] = 0
    ys, xs = np.where(a > 0); x0, y0, x1, y1 = max(0, xs.min() - 2), max(0, ys.min() - 2), min(W, xs.max() + 3), min(H, ys.max() + 3)
    tiles.append({'name': n, 'bone': b, 'x': int(x0), 'y': int(y0), 'w': int(x1 - x0), 'h': int(y1 - y0), 'px': np.dstack([c, a])[y0:y1, x0:x1], 'color': [int(v) for v in col]})

AW = 2048; x = y = rowh = 0
for t in sorted(tiles, key=lambda q: -q['h']):
    if x + t['w'] + 4 > AW: x = 0; y += rowh + 4; rowh = 0
    t['ax'], t['ay'] = x, y; x += t['w'] + 4; rowh = max(rowh, t['h'])
AH = y + rowh; atlas = Image.new('RGBA', (AW, AH), (0, 0, 0, 0))
for t in tiles: atlas.paste(Image.fromarray(t['px'], 'RGBA'), (t['ax'], t['ay']))
atlas.save(f'{OUT}/atlas.webp', 'WEBP', quality=93, alpha_quality=100, method=6)
Image.fromarray(over.astype(np.uint8)).crop((200, 100, 1000, 1190)).save(f'{OUT}/parts_map.png')
rig = {'w': AW, 'h': AH, 'bones': [{'n': b[0], 'p': b[1], 'x': b[2], 'y': b[3]} for b in BONES],
       'chains': {c: {'n': len(p[1]) - 1, 'end': p[1][-1]} for c, p in CHAINS.items()},
       'parts': [{k: t[k] for k in ('name', 'bone', 'x', 'y', 'w', 'h', 'ax', 'ay', 'color')} for t in tiles]}
json.dump(rig, open(f'{OUT}/rig.json', 'w'), separators=(',', ':'))
# the parts put back together at rest must equal the picture
back = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for t in tiles: back.alpha_composite(Image.fromarray(t['px'], 'RGBA'), (t['x'], t['y']))
b = np.array(back).astype(int); e = np.abs(b[..., :3] - rgb.astype(int)).max(2)[alpha > 200]
print(len(tiles), 'parts', len(BONES), 'bones, atlas', AW, AH, os.path.getsize(f'{OUT}/atlas.webp') // 1024, 'KB; rest error: mean', round(float(e.mean()), 2), 'over 12:', round(float((e > 12).mean() * 100), 3), '%')
