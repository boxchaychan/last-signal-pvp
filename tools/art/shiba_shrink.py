# Shrinking the PixelLab shiba (owner 2026-11-12 "ถ้าย่อชิบะจะเบลอไหม" / "ลองเอามา"): free comparison.
# original 61 px | plain resize to 46 (smooth = blurry) | plain resize to 46 (nearest = broken lines) | 2x2 merge to ~31 (sharp).
#   python3 tools/art/shiba_shrink.py -> art/incoming/dogcat/shrink/{cmp_x4.png, s46_smooth.png, s46_nearest.png, s_half.png}
import numpy as np, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, 'tools/art'); from stone_px import blocks
O = 'art/incoming/dogcat/shrink/'
def half(im):   # the same 2x2 merge as pixellab_sheet.py --half: a dark outline pixel wins, else the most common colour
    a = np.array(im).astype(float); H, W = a.shape[0] // 2 * 2, a.shape[1] // 2 * 2
    b = a[:H, :W].reshape(H // 2, 2, W // 2, 2, 4).transpose(0, 2, 1, 3, 4).reshape(H // 2, W // 2, 4, 4)
    op = b[..., 3] >= 128; lum = b[..., :3] @ np.array([.299, .587, .114]); lum = np.where(op, lum, 1e9)
    dark = lum.min(-1) < 60; di = lum.argmin(-1)
    eq = (np.abs(b[:, :, :, None, :3] - b[:, :, None, :, :3]).sum(-1) < 1) & op[:, :, :, None] & op[:, :, None, :]
    mi = eq.sum(-1).argmax(-1); pick = np.where(dark, di, mi)
    out = np.take_along_axis(b, pick[..., None, None].repeat(4, -1), 2)[:, :, 0]
    out[..., 3] = np.where(op.sum(-1) >= 2, 255, 0); return Image.fromarray(out.astype(np.uint8))
S = Image.open('art/incoming/dogcat/pl/char/Idle/rotations/south.png').convert('RGBA')
S = S.crop(S.getbbox()); k = 46 / S.height; w46 = round(S.width * k)
V = [('original 61 px', S),
     ('plain resize 46 (smooth)', S.resize((w46, 46), Image.LANCZOS)),
     ('plain resize 46 (nearest)', S.resize((w46, 46), Image.NEAREST)),
     ('2x2 merge %d px' % half(S).crop(half(S).getbbox()).height, half(S).crop(half(S).getbbox()))]
V[1][1].save(O + 's46_smooth.png'); V[2][1].save(O + 's46_nearest.png'); V[3][1].save(O + 's_half.png')
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)
K = 4; cw = 70 * K; W = cw * 4; Hh = 70 * K + 40 + 150
FL = blocks(Hh, W // 2 + 2, 26, 20, [(204, 190, 160), (194, 178, 148), (212, 200, 172)], seed=5, bond=False, lip=1, mortar=(120, 104, 90))
cv = Image.new('RGBA', (W, Hh), (236, 232, 220, 255)); d = ImageDraw.Draw(cv)
small = Image.fromarray(FL[:70, :W // 2].astype(np.uint8)).convert('RGBA')        # a strip of stone floor shown at 1:1 (x2)
for i, (n, im) in enumerate(V):
    x = i * cw; d.text((x + 8, 8), n, fill=(30, 30, 30), font=F)
    big = im.resize((im.width * K, im.height * K), Image.NEAREST); cv.alpha_composite(big, (x + (cw - big.width) // 2, 30 + 70 * K - 8 - big.height))
    small.alpha_composite(im, (cw // 4 + i * (cw // 2) - im.width // 2, 66 - im.height))
cv.alpha_composite(small.resize((small.width * 2, small.height * 2), Image.NEAREST).crop((0, 0, W, 140)), (0, Hh - 140))
d.text((8, Hh - 158), 'game size (x2 for the phone)', fill=(30, 30, 30), font=F)
d.line((0, 30 + 70 * K - 4, W, 30 + 70 * K - 4), fill=(90, 90, 90), width=2)
cv.save(O + 'cmp_x4.png'); print('ok', [(n, im.size) for n, im in V])
