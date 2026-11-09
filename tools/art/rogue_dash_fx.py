# The rogue's new skill 4 look (owner 2026-11-09, approved "เออสวย" on the demo GIF): six Dash Strike dashes in a deep
# black with a neon purple rim (colours from the owner's neon samurai picture), each with Dash Strike's own hit flash,
# and the closing X (twin fang) the same: black from its first frame with the purple rim; the monster's hit flash violet. Makes the two effect sheets:
#   python tools/art/rogue_dash_fx.py   -> fx/pfx_dashstrike_v.png, fx/pfx_twinfang_k.png + their fx/manifest.json entries
# Timing from the demo: one dash 0.2 s (the game's SK4.cut was 0.12), Dash Strike played at 20 fps (made at 30), she holds
# the dash row's frame 6 with a violet glow until the X ends. Not in the game yet: the owner will say when.
import json
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

RAMP = np.array([[30, 12, 70], [80, 32, 170], [129, 60, 225], [170, 90, 245], [214, 140, 253]], float)

def tint(c):                        # brightness -> the violet ramp
    a = np.array(c).astype(float); v = (a[..., :3].max(-1) / 255) ** 1.25 * (len(RAMP) - 1)
    i = np.clip(v.astype(int), 0, len(RAMP) - 2); f = (v - i)[..., None]
    a[..., :3] = RAMP[i] * (1 - f) + RAMP[i + 1] * f; return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def glowy(c, r=7):                  # a soft violet light behind it
    a = np.array(c).astype(float); al = a[..., 3] * (a[..., :3].max(-1) / 255)
    g = np.zeros_like(a); g[..., :3] = [120, 50, 230]; g[..., 3] = np.clip(al * 1.6, 0, 255)
    out = Image.fromarray(g.astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)); out.alpha_composite(c); return out

def shadow_x(c):                    # black strokes, a 2 px neon purple rim, a purple glow
    a = np.array(c).astype(float); m = (a[..., 3] > 110) & (a[..., :3].max(-1) > 90)
    rim = ndimage.binary_dilation(m, iterations=2) & ~m
    o = np.zeros(a.shape, np.uint8)
    o[rim] = [150, 60, 240, 255]; o[m, :3] = [10, 0, 16]; o[m, 3] = np.clip(a[m, 3] * 1.3, 0, 255).astype(np.uint8)
    g = np.zeros(a.shape, np.uint8); g[..., :3] = [120, 50, 230]; g[..., 3] = (ndimage.binary_dilation(m, iterations=3) * 200).astype(np.uint8)
    out = Image.fromarray(g).filter(ImageFilter.GaussianBlur(6)); out.alpha_composite(Image.fromarray(o)); return out

def remake(src, dst, fn, pad):
    man = json.load(open('fx/manifest.json')); m = man[src]; im = Image.open('fx/' + src + '.png').convert('RGBA')
    w, h, cols, n = m['w'], m['h'], m['cols'], m['n']; W, H = w + 2 * pad, h + 2 * pad
    out = Image.new('RGBA', (cols * W, -(-n // cols) * H))
    for i in range(n):
        c = Image.new('RGBA', (W, H)); c.alpha_composite(im.crop(((i % cols) * w, (i // cols) * h, (i % cols + 1) * w, (i // cols + 1) * h)), (pad, pad))
        out.alpha_composite(fn(c), ((i % cols) * W, (i // cols) * H))
    out.save('fx/' + dst + '.png', optimize=True)
    man[dst] = dict(m, w=W, h=H, ax=m['ax'] + pad, ay=m['ay'] + pad, src=m['src'] + ' (rogue skill 4 look, tools/art/rogue_dash_fx.py)')
    json.dump(man, open('fx/manifest.json', 'w'), separators=(',', ':')); print(dst, out.size)

remake('pfx_dashstrike', 'pfx_dashstrike_v', shadow_x, 14)   # owner "Dash Strike โทนเดียวกันได้ไหม": black + purple rim like the X (the glowing violet one was lambda c: glowy(tint(c)))
remake('pfx_twinfang', 'pfx_twinfang_k', shadow_x, 10)
