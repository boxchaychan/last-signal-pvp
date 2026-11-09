# Swordsman E (owner 2026-11-09 "พายุดาบ เปลี่ยนโทนส้ม นีออนดำ แบบพวกมีด ธนู"): the owner's pasted tornado sheet (9 x 8 = 72 frames on
# black) came with its soft glow flattened into solid red / yellow / orange / pink bands. Those bands are flat colour, the tornado
# is textured: a pixel is kept when its 5x5 neighbourhood varies (local std), the flat bands go. What is kept becomes black ink
# with a neon orange rim and an orange glow, like the rogue's purple and the archer's green.
#   python3 tools/art/sword_storm_fx.py  -> fx/pfx_swstorm_k.png + manifest
import json
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

SRC, KEY, C, R, K = 'art/incoming/pfx/sword-storm-sheet.png', 'pfx_swstorm_k', 9, 8, .5
RIM, INK, GLOW = [255, 140, 30], [14, 6, 2], [255, 110, 20]
a = np.array(Image.open(SRC).convert('RGB')).astype(float); H, W = a.shape[:2]; cw, ch = W / C, H / R
ow, oh = round(cw * K), round(ch * K); out = Image.new('RGBA', (8 * ow, -(-C * R // 8) * oh))
for i in range(C * R):
    x0, y0 = round(i % C * cw), round(i // C * ch); q = a[y0:y0 + round(ch), x0:x0 + round(cw)]
    sd = 0
    for c in range(3):   # fast local std: sqrt(E[x^2] - E[x]^2) over 5x5
        u = ndimage.uniform_filter(q[..., c], 5); sd = sd + np.sqrt(np.maximum(0, ndimage.uniform_filter(q[..., c] ** 2, 5) - u * u))
    band = np.zeros(q.shape[:2], bool)   # the flattened glow: solid yellow, red, orange, pink, white (and their seams)
    for col in ([255, 255, 0], [255, 0, 0], [255, 130, 0], [255, 130, 130], [255, 255, 255], [255, 255, 130]):
        band |= np.abs(q - col).max(-1) < 34
    near = ndimage.binary_dilation(band, iterations=4)
    dark = q.max(-1) < 125
    m = (dark & (q.max(-1) > 25)) | (~near & (sd > 26))
    m = ndimage.binary_opening(m, iterations=1); lab, n = ndimage.label(m)
    if n: sz = ndimage.sum(m, lab, range(1, n + 1)); m = np.isin(lab, 1 + np.nonzero(sz >= 40)[0])
    img = Image.fromarray((m * 255).astype(np.uint8)).resize((ow, oh), Image.BOX); mm = np.array(img) > 110
    edge = ndimage.binary_dilation(mm, iterations=2) & ~mm
    o = np.zeros((oh, ow, 4), np.uint8); o[edge] = RIM + [255]; o[mm] = INK + [235]
    g = np.zeros((oh, ow, 4), np.uint8); g[..., :3] = GLOW; g[..., 3] = ndimage.binary_dilation(mm, iterations=3) * 170
    c = Image.fromarray(g).filter(ImageFilter.GaussianBlur(6)); c.alpha_composite(Image.fromarray(o))
    out.alpha_composite(c, (i % 8 * ow, i // 8 * oh))
out.save('fx/' + KEY + '.png', optimize=True)
man = json.load(open('fx/manifest.json'))
man[KEY] = {'w': ow, 'h': oh, 'n': C * R, 'cols': 8, 'fps': 30, 'ax': ow // 2, 'ay': round(oh * .78), 'src': "owner's pasted sword storm sheet, black + neon orange (tools/art/sword_storm_fx.py)"}
json.dump(man, open('fx/manifest.json', 'w'), separators=(',', ':')); print(KEY, out.size, man[KEY])
