# The archer's effects in the rogue's style (owner 2026-11-09 "สกิลโทนเขียว ... ให้มันคล้ายๆ กับสกิลโทนสีของมีด"): the rogue's
# skills are black strokes with a neon purple rim and a purple glow (tools/art/rogue_dash_fx.py); the archer gets the same
# with neon green. Black also reads on the green grass, where the pale green copies (fx_tint) disappeared.
#   python tools/art/archer_fx.py            -> every sheet below, fx/<key>_k.png + fx/manifest.json entries
#   python tools/art/archer_fx.py <key> ...  -> only those
import json, sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

RIM, INK, GLOW = [70, 255, 125], [2, 18, 8], [40, 225, 95]

def shadow(c, a_min=110, v_min=90, rim=2, keep_white=0):
    # strokes (opaque + bright enough) -> black, a neon green rim round them, a soft green light behind;
    # keep_white > 0: the hottest pixels (white cores) stay white-green so a flash still flashes
    a = np.array(c).astype(float); v = a[..., :3].max(-1); m = (a[..., 3] > a_min) & (v > v_min)
    edge = ndimage.binary_dilation(m, iterations=rim) & ~m
    o = np.zeros(a.shape, np.uint8)
    o[edge] = RIM + [255]; o[m, :3] = INK; o[m, 3] = np.clip(a[m, 3] * 1.3, 0, 255).astype(np.uint8)
    if keep_white:
        hot = m & (a[..., :3].min(-1) > keep_white) & (a[..., 3] > 200)
        hot &= ndimage.binary_erosion(m, iterations=rim)          # only well inside a stroke, the black still frames it
        o[hot, :3] = [215, 255, 225]
    g = np.zeros(a.shape, np.uint8); g[..., :3] = GLOW; g[..., 3] = (ndimage.binary_dilation(m, iterations=rim + 1) * 190).astype(np.uint8)
    out = Image.fromarray(g).filter(ImageFilter.GaussianBlur(6)); out.alpha_composite(Image.fromarray(o)); return out

def remake(src, dst, pad, **kw):
    man = json.load(open('fx/manifest.json')); m = man[src]; im = Image.open('fx/' + src + '.png').convert('RGBA')
    w, h, cols, n = m['w'], m['h'], m.get('cols') or m['n'], m['n']; W, H = w + 2 * pad, h + 2 * pad
    out = Image.new('RGBA', (cols * W, -(-n // cols) * H))
    for i in range(n):
        c = Image.new('RGBA', (W, H)); c.alpha_composite(im.crop(((i % cols) * w, (i // cols) * h, (i % cols + 1) * w, (i // cols + 1) * h)), (pad, pad))
        out.alpha_composite(shadow(c, **kw), ((i % cols) * W, (i // cols) * H))
    out.save('fx/' + dst + '.png', optimize=True)
    man[dst] = dict(m, w=W, h=H, ax=m['ax'] + pad, ay=m['ay'] + pad, src=m['src'].split(' (')[0] + ' (archer black + neon green, tools/art/archer_fx.py)')
    json.dump(man, open('fx/manifest.json', 'w'), separators=(',', ':')); print(dst, out.size)

JOBS = {
    'pfx_rapier': dict(pad=10, a_min=30, v_min=60),                      # Q rapier flurry (owner's sheet); low limits: its streaks are soft
    'pfx_chargeshot': dict(pad=10, a_min=28, v_min=70),                  # R charged shot (owner's sheet, gold); the faint charge rings too
    'pfx_skyarrow': dict(pad=12, a_min=90, v_min=90),                    # E thunder javelin
    'pfx_dashstrike': dict(pad=14, a_min=110, v_min=90),                 # the hit flash on her arrows
    'pfx_vine': dict(pad=10, a_min=60, v_min=40),                        # Z thorn vine trap (owner's sheet)
}
for k in (sys.argv[1:] or JOBS):
    j = dict(JOBS[k]); remake(k, k + '_k', j.pop('pad'), **j)
