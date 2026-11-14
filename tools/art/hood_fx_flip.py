# Owner 2026-11-14 "567 กลับเอฟเฟกต์มาอีกฝั่ง": in attack frames 5, 6, 7 (indices 4-6 of rabbit_attack.png) the big arc is drawn BEHIND the rabbit (left);
# move it to the front: the arc pixels (bright orange / yellow / white, no dark outline, big patches) are mirrored about the head line
# and laid UNDER the body. The unflipped sheet is kept as rabbit_attack_noflip.png.
import json, numpy as np
from PIL import Image
from scipy import ndimage as nd
SRC = 'art/sidegame/rabbit_attack.png'; J = json.load(open(SRC.replace('.png', '.json'))); CW, CH = J['cw'], J['ch']; FX = J['feet'][0]
import os
NF = SRC.replace('.png', '_noflip.png')
if not os.path.exists(NF): Image.open(SRC).save(NF)
im = Image.open(NF).convert('RGBA')   # always start from the unflipped sheet
a = np.asarray(im).copy()
for i in (4, 5, 6):
    c = a[:, i * CW:(i + 1) * CW].copy(); rgb = c[..., :3].astype(int); al = c[..., 3] > 0
    mx, mn = rgb.max(2), rgb.min(2)
    glow = al & (mx > 200) & ((rgb[..., 0] > 200) & (rgb[..., 2] < 200) | (mn > 215))   # orange / yellow / near-white
    # the rabbit itself is ringed by a dark outline: close it, fill it, and never take pixels from inside it
    dark = al & (mx < 90); body_m = nd.binary_fill_holes(nd.binary_closing(dark, np.ones((3, 3)), 2)); body_m = nd.binary_dilation(body_m, iterations=1)
    head = np.abs(np.arange(CW)[None, :] - FX) <= 17; near_line = nd.binary_dilation(dark, iterations=3)
    glow &= ~body_m & ~(head & near_line)   # ears: thin, their outline is not always closed, so near-outline pixels in the head zone stay
    lab, n = nd.label(glow, np.ones((3, 3)))
    fx = np.zeros_like(al)
    for k in range(1, n + 1):
        m = lab == k; ys, xs = np.where(m)
        if xs.mean() < FX - 6 and (m.sum() > 60 or xs.max() < FX - 20): fx |= m
    # sparkles / specks left of the body go with the arc
    fx |= al & ~body_m & (mx > 150) & (np.arange(CW)[None, :] < FX - 30)
    body = c.copy(); body[fx] = 0
    eff = np.zeros_like(c); eff[fx] = c[fx]
    eff = eff[:, ::-1]; sh = 2 * FX - (CW - 1)   # mirror about x = FX
    eff = np.roll(eff, sh, axis=1)
    if sh > 0: eff[:, :sh] = 0
    elif sh < 0: eff[:, sh:] = 0
    out = Image.fromarray(eff); out.alpha_composite(Image.fromarray(body)); a[:, i * CW:(i + 1) * CW] = np.asarray(out)
# Owner "ขาหาย ต่อขากลับมา": in frames 5 and 6 the original arc covered the legs, so once the arc moved there were none.
# The legs of frame 7 (index 6, same stance) are laid UNDER those two frames.
LEGS = a[J['feet'][1] - 24:J['feet'][1] + 2, 6 * CW + FX - 30:6 * CW + FX + 24].copy()
for i in (4, 5):
    y0, x0 = J['feet'][1] - 24, i * CW + FX - 30
    under = Image.fromarray(np.zeros_like(a[:, i * CW:(i + 1) * CW])); under.paste(Image.fromarray(LEGS), (FX - 30, y0))
    under.alpha_composite(Image.fromarray(a[:, i * CW:(i + 1) * CW].copy())); a[:, i * CW:(i + 1) * CW] = np.asarray(under)
Image.fromarray(a).save(SRC)
