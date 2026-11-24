"""Robot recolour (owner 2026-11-24 "ช่วยทำสีใหม่สวยๆหน่อย หุ่นยนต์"), FREE: the machine sprites are mostly flat grey, so the grey METAL gets a
real colour (body hue + saturation, lightness kept), the orange warning stripes / trims move to a stripe colour and the cyan lights to a glow
colour. Schemes: A steel blue + hazard orange + cyan, B crimson mech + gold + cyan, C army green + yellow + red, D white mech + blue + red trims,
N NEON (owner "ทำให้เรืองแสงหน่อย นีออนฟ้า"): dark gunmetal body, every stripe / light turned neon blue with white-hot cores, a 1 px neon rim inside the body next to the lights.
  python3 tools/art/robot_recolor.py in.png out.png <A|B|C|D|N>"""
import sys, numpy as np
from PIL import Image
S = {'A': (212, .62, 1.3, 30, 186), 'B': (354, .78, 1.28, 46, 186), 'C': (92, .55, 1.22, 52, 2), 'D': (220, .08, 1.45, 4, 205), 'N': (222, .45, .72, 196, 196)}   # body hue, body sat, body lift, stripe hue, glow hue
def hsv2rgb(h, s, v):
    i = np.floor(h * 6).astype(int) % 6; f = h * 6 - np.floor(h * 6); p = v * (1 - s); q = v * (1 - f * s); t = v * (1 - (1 - f) * s)
    return np.stack([np.choose(i, [v, q, p, p, t, v]), np.choose(i, [t, v, v, q, p, p]), np.choose(i, [p, p, t, v, v, q])], -1)
src, dst, k = sys.argv[1], sys.argv[2], sys.argv[3]; bh, bs, lift, sh, gh = S[k]
a = np.asarray(Image.open(src).convert('RGBA')).astype(float) / 255; rgb = a[..., :3]; v = rgb.max(2); mn = rgb.min(2); s = np.where(v > 0, (v - mn) / np.maximum(v, 1e-6), 0)
mx = rgb.argmax(2); d = np.maximum(v - mn, 1e-6); h = np.where(mx == 0, ((rgb[..., 1] - rgb[..., 2]) / d) % 6, np.where(mx == 1, (rgb[..., 2] - rgb[..., 0]) / d + 2, (rgb[..., 0] - rgb[..., 1]) / d + 4)) * 60
grey = s < .2; warm = ~grey & ((h < 60) | (h > 330)); cool = ~grey & (h > 160) & (h < 260)
nh = np.where(grey, bh, np.where(warm, sh, np.where(cool, gh, h))) / 360; ns = np.where(grey, np.where(v > .08, bs * (1 - .35 * v), 0), np.minimum(1, s * 1.15))
nv = np.where(grey, np.clip(v * lift, 0, 1), np.where(cool, np.minimum(1, v * 1.08), v))
if k == 'D': nh = np.where(warm & (v < .7), 220 / 360, nh); ns = np.where(warm & (v < .7), .75, ns)   # white mech: darker trims go blue, bright ones red
if k == 'N':   # neon: lights + stripes glow, brightest become white-hot, body stays dark
    lit = warm | cool; nh = np.where(lit, 196 / 360, nh); ns = np.where(lit, np.where(v > .85, .25, .85), ns); nv = np.where(lit, np.minimum(1, .75 + v * .4), nv)
out = a.copy(); out[..., :3] = hsv2rgb(nh, ns, nv); out[..., :3] = np.where((v < .12)[..., None], rgb, out[..., :3])   # keep the dark outline
if k == 'N':
    op = a[..., 3] > .5; lit2 = (warm | cool) & op; near = np.zeros_like(lit2)
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)): near |= np.roll(np.roll(lit2, dy, 0), dx, 1)
    rim = near & ~lit2 & op & grey & (v >= .12); out[rim, :3] = out[rim, :3] * .45 + np.array([.15, .55, 1.0]) * .55
Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save(dst)
