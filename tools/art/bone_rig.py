# A tiny cut-out ("bone") rig for our pixel characters (owner 2026-11-13: wants our own bone tool instead of PixelLab for every
# move; first test "ลองดูก่อน"): free, no jobs. A character still is split into parts by masks; every part has a pivot, a parent and
# a motion (angle / dx / dy as sine waves over the loop); frames are rendered with nearest-pixel sampling so the pixels stay hard.
# Parts keep an "underlay" in the body so no holes open where a part moves away.
#   python3 tools/art/bone_rig.py -> art/incoming/dogcat/rig/shiba2_idle.png (16 frames, 104 px cells) + preview gif
import math, os, numpy as np
from PIL import Image
O = 'art/incoming/dogcat/rig/'; os.makedirs(O, exist_ok=True)
def rig(still, parts, n=16):
    """parts: list of dict(name, mask(bool array), pivot(x,y), parent(index or -1), a, dx, dy, ph) with a/dx/dy = amplitudes;
    drawn in list order. -> n RGBA frames"""
    a = np.asarray(still.convert('RGBA')); H, W = a.shape[:2]; frames = []
    layers = []
    for p in parts:
        l = a.copy(); l[~p['mask']] = 0; layers.append(Image.fromarray(l))
    for f in range(n):
        t = f / n * 2 * math.pi; mats = []; out = Image.new('RGBA', (W, H))
        for p, layer in zip(parts, layers):
            ang = math.radians(p.get('a', 0) * math.sin(t * p.get('fa', 1) + p.get('ph', 0)))
            dx = round(p.get('dx', 0) * math.sin(t * p.get('fx', 1) + p.get('ph', 0))); dy = round(p.get('dy', 0) * (.5 - .5 * math.cos(t * p.get('fy', 1) + p.get('ph', 0))))
            px, py = p['pivot']; c, s = math.cos(ang), math.sin(ang); tx, ty = px + dx - c * px + s * py, py + dy - s * px - c * py
            pc, ps, x0, y0 = (1, 0, 0, 0) if p['parent'] < 0 else mats[p['parent']]
            m = (pc * c - ps * s, ps * c + pc * s, pc * tx - ps * ty + x0, ps * tx + pc * ty + y0); mats.append(m)
            C, S, TX, TY = m; inv = (C, S, -(C * TX + S * TY), -S, C, S * TX - C * TY)
            out.alpha_composite(layer.transform((W, H), Image.Transform.AFFINE, inv, Image.Resampling.NEAREST))
        frames.append(out)
    return frames
if __name__ == '__main__':
    st = Image.open('art/dogcat/units/shiba2.png').convert('RGBA').crop((0, 0, 104, 104)); a = np.asarray(st); op = a[..., 3] > 0
    yy, xx = np.mgrid[0:104, 0:104]
    knot = op & (yy < 35) & (xx < 56)                                     # the topknot
    head = op & (yy < 58) & (xx >= 37) & ~((yy > 54) & (xx < 44))         # head with ears (the topknot rides on it)
    tail = op & (xx < 40) & (yy >= 66) & (yy <= 80)                       # the curled tail on the left
    body = op & ~head & ~tail | (op & (yy >= 52) & (yy < 58) & (xx >= 40)) | (tail & (xx >= 36))   # + underlays: the chin rows and the tail's root
    parts = [dict(name='tail', mask=tail, pivot=(40, 75), parent=-1, a=13, fa=2, dy=1),
             dict(name='body', mask=body, pivot=(52, 86), parent=-1),
             dict(name='head', mask=head & ~knot, pivot=(52, 57), parent=-1, dy=1.2, ph=.6, a=1.5),
             dict(name='knot', mask=knot, pivot=(48, 34), parent=2, a=7, ph=1.2)]
    fr = rig(st, parts, 16); strip = Image.new('RGBA', (104 * 16, 104))
    for i, f in enumerate(fr): strip.alpha_composite(f, (i * 104, 0))
    strip.save(O + 'shiba2_idle.png')
    g = []
    for i in range(16):
        c = Image.new('RGBA', (104 * 2 + 10, 104), (214, 226, 190, 255)); c.alpha_composite(st, (0, 0)); c.alpha_composite(fr[i], (114, 0)); g.append(c.resize((c.width * 4, c.height * 4), Image.NEAREST).convert('RGB'))
    g[0].save(O + 'shiba2_idle_cmp.gif', save_all=True, append_images=g[1:], duration=95, loop=0)
    big = Image.new('RGBA', (104 * 8, 104 * 2), (214, 226, 190, 255))
    for i, f in enumerate(fr): big.alpha_composite(f, (i % 8 * 104, i // 8 * 104))
    big.crop((0, 20, 832, 208)).resize((1664, 376), Image.NEAREST).save('/tmp/claude-0/-home-user-last-signal-pvp/be576c95-f8fc-5b1b-80a5-8423c4aa1256/scratchpad/rig.png'); print('ok')
