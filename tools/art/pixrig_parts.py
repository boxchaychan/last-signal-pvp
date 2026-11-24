"""Split a 128 px PIXEL character into rig parts with its ORIGINAL pixels (free; no AI redraw) for turnrig.html.

  python3 tools/art/pixrig_parts.py art/turnrig

First test (owner 2026-11-24 "งั้นทำของเรามาดูก่อน"): the chibi swordsman's PixelLab side view (art/incoming/darkchibi/pl_char/east.png, body 124 px).
Parts come from simple rules (lines / boxes in picture pixels) because the arm and the legs touch the body in this picture. Each part is under-painted
with its own nearest colours where a part IN FRONT of it covers it, so nothing shows a hole when a joint turns a little.
-> parts.png (atlas, 1 px = 1 picture px), rig.json (parts back to front with pivots), parts_map.png (each part in its own colour, x6)
"""
import sys, os, json, colorsys
import numpy as np
from PIL import Image
from scipy import ndimage as nd

OUT = sys.argv[1] if len(sys.argv) > 1 else 'art/turnrig'; os.makedirs(OUT, exist_ok=True)
SRC = 'art/incoming/darkchibi/pl_char/east.png'
a = np.array(Image.open(SRC).convert('RGBA')); H, W = a.shape[:2]; fig = a[..., 3] > 20
yy, xx = np.mgrid[0:H, 0:W]

def seg_dist(x0, y0, x1, y1):
    dx, dy = x1 - x0, y1 - y0; t = np.clip(((xx - x0) * dx + (yy - y0) * dy) / (dx * dx + dy * dy), 0, 1)
    return np.hypot(xx - x0 - dx * t, yy - y0 - dy * t)

# pivots in picture px (x, y); parent; how far each part is under-painted where a front part covers it
# The SWORD arm is the left column (shoulder 80,87 -> fist 76,116, the guard runs up-right from the fist, the blade down-right);
# the right column (89,89 -> 89,111) is the empty arm.
PIV = {'root': (86, 152), 'legs': (85, 126), 'torso': (85, 124), 'head': (84, 79), 'cape': (75, 84), 'arm_o': (89, 90),
       'arm_s': (81, 88), 'fore_s': (79, 102), 'sword': (77, 116)}
PARENT = {'legs': 'root', 'torso': 'root', 'head': 'torso', 'cape': 'torso', 'arm_o': 'torso', 'arm_s': 'torso', 'fore_s': 'arm_s', 'sword': 'fore_s'}
ORDER = ['cape', 'legs', 'torso', 'arm_o', 'head', 'sword', 'arm_s', 'fore_s']   # back to front

lab = np.full((H, W), -1, int); L = {n: i for i, n in enumerate(ORDER)}
R, G, Bc = (a[..., k].astype(int) for k in range(3)); lum = R * .3 + G * .59 + Bc * .11
dark = fig & (lum < 34)                                   # outlines and the darkest shading: they follow their nearest coloured pixel
red = fig & (R - G > 60) & (R > 90) & (G < 70) & (Bc < 90)       # cloth red only, not the warm skin
gold = fig & (R > 180) & (G > 110) & (Bc < 120) & (R - Bc > 90)
pale = fig & (np.abs(R - Bc) < 40) & (lum > 120)          # white / grey steel
skin = fig & (R > 200) & (G > 90) & (G < 225) & (Bc > 60) & (R - Bc > 40)
def nearest_of(mask):                                      # for every pixel: is its nearest NON-dark pixel inside mask?
    idx = nd.distance_transform_edt(~(fig & ~dark), return_distances=False, return_indices=True); return mask[idx[0], idx[1]]
lab[fig] = L['torso']
lab[fig & (yy >= 125)] = L['legs']
lab[fig & (yy < 77)] = L['head']
lab[fig & (seg_dist(89, 89, 89, 111) < 3.4) & (yy >= 86)] = L['arm_o']
lab[fig & (seg_dist(81, 85, 79, 101) < 4.2) & (yy >= 81) & (xx >= 74) & ~red] = L['arm_s']
fist = fig & (xx >= 73) & (xx <= 79) & (yy >= 112) & (yy <= 118)
lab[(fig & (seg_dist(79, 101, 77, 113) < 3.8) & (yy > 101) & (xx >= 72) & ~red) | fist] = L['fore_s']
capec = red & (yy >= 78) & ((xx < 74) | ((yy >= 92) & (xx < 77))) & ~fist
lab[capec | (dark & (yy >= 78) & (xx < 78) & nearest_of(capec) & ~fist)] = L['cape']
bl, gd = seg_dist(84, 121, 108, 150), seg_dist(77, 123, 85, 115)
swc = ((pale | gold) & (bl < 3.4) & (yy >= 119)) | (gold & (gd < 2.6)) | (pale & (xx >= 81) & (xx <= 86) & (yy >= 110) & (yy <= 117))
lab[swc | (dark & ((bl < 4) & (yy >= 119) | (gd < 3)) & nearest_of(swc))] = L['sword']

rgb = a[..., :3]
tiles = []
for i, n in enumerate(ORDER):
    m = lab == i
    c = rgb.copy(); al = np.where(m, 255, 0).astype(np.uint8)
    front = fig & (lab > i)
    reach = {'torso': 10, 'legs': 5, 'cape': 6, 'arm_o': 0, 'arm_s': 3, 'head': 0, 'sword': 0, 'fore_s': 0}[n]
    def hull(mask):                                       # fill only between the part's own left and right edge on each row
        h = np.zeros_like(mask)
        for r in np.where(mask.any(1))[0]: xs_ = np.where(mask[r])[0]; h[r, xs_.min():xs_.max() + 1] = True
        return h
    if n == 'torso': front = front | (fig & (lab == L['head']) & (yy >= 70)); front &= hull(np.isin(lab, [L['torso'], L['arm_s'], L['fore_s'], L['arm_o']])) & (yy < 127)
    if n == 'legs': front &= hull(m) & (yy >= 119)
    if n == 'cape': front &= (yy >= 78) & (xx <= 81)
    if n == 'arm_s': front &= lab == L['fore_s']
    if reach:
        ext = nd.binary_dilation(m, iterations=reach, mask=m | front) & front
        ext &= nd.binary_opening(ext | m, iterations=1)             # no 1 px whiskers
        core = m & nd.binary_erosion(m, iterations=1); core = core if core.sum() > 20 else m
        ni = nd.distance_transform_edt(~core, return_distances=False, return_indices=True)
        c[ext] = rgb[ni[0], ni[1]][ext]; al[ext] = 255
    cl, cn = nd.label(al > 0, structure=np.ones((3, 3)))
    if cn > 1:                                                    # loose specks away from the part go
        cs = nd.sum(al > 0, cl, range(1, cn + 1)); drop = np.where(cs < 8)[0] + 1; al[np.isin(cl, drop)] = 0
    ys, xs = np.where(al > 0); x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    tiles.append({'name': n, 'x': int(x0), 'y': int(y0), 'w': int(x1 - x0), 'h': int(y1 - y0), 'px': np.dstack([c, al])[y0:y1, x0:x1]})

AW = 256; x = y = rowh = 0
for t in sorted(tiles, key=lambda q: -q['h']):
    if x + t['w'] + 2 > AW: x = 0; y += rowh + 2; rowh = 0
    t['ax'], t['ay'] = x, y; x += t['w'] + 2; rowh = max(rowh, t['h'])
AH = y + rowh; atlas = Image.new('RGBA', (AW, AH), (0, 0, 0, 0))
for t in tiles: atlas.paste(Image.fromarray(t['px'], 'RGBA'), (t['ax'], t['ay']))
atlas.save(f'{OUT}/parts.png')
over = a.copy()
for i, n in enumerate(ORDER):
    col = np.array(colorsys.hsv_to_rgb(i * .618 % 1, .8, 1)) * 255; m = lab == i; over[m, :3] = (over[m, :3] * .35 + col * .65).astype(np.uint8)
Image.fromarray(over).crop((40, 20, 125, 156)).resize((85 * 6, 136 * 6), Image.NEAREST).save(f'{OUT}/parts_map.png')
rig = {'src': SRC, 'foot': PIV['root'], 'w': AW, 'h': AH,
       'parts': [{k: t[k] for k in ('name', 'x', 'y', 'w', 'h', 'ax', 'ay')} | {'px': PIV[t['name']][0], 'py': PIV[t['name']][1], 'parent': PARENT[t['name']]} for t in tiles]}
json.dump(rig, open(f'{OUT}/rig.json', 'w'), indent=1)
back = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for t in tiles: back.alpha_composite(Image.fromarray(t['px'], 'RGBA'), (t['x'], t['y']))
e = np.abs(np.array(back).astype(int) - a.astype(int))[fig].max(1)
print(len(tiles), 'parts; atlas', AW, AH, '; rest differs on', round(float((e > 0).mean() * 100), 3), '% of pixels')
