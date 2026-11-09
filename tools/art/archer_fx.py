# The archer's effects in the rogue's style (owner 2026-11-09 "สกิลโทนเขียว ... ให้มันคล้ายๆ กับสกิลโทนสีของมีด"): the rogue's
# skills are black strokes with a neon purple rim and a purple glow (tools/art/rogue_dash_fx.py); the archer gets the same
# with neon green. Black also reads on the green grass, where the pale green copies (fx_tint) disappeared.
#   python tools/art/archer_fx.py            -> every sheet below, fx/<key>_k.png + fx/manifest.json entries
#   python tools/art/archer_fx.py <key> ...  -> only those
#   python tools/art/archer_fx.py --tone=red <key> ...  -> the Berserker's black + neon red (docs/berserker.md), fx/<key>_r.png;
#        a key not in JOBS uses dict(pad=10, a_min=60, v_min=60)
import json, sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

RIM, INK, GLOW = [70, 255, 125], [2, 18, 8], [40, 225, 95]
HOT = [215, 255, 225]; SUF, TAG = '_k', 'archer black + neon green'
ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
if '--tone=red' in sys.argv:
    RIM, INK, GLOW, HOT, SUF, TAG = [255, 42, 58], [18, 2, 4], [224, 16, 42], [255, 225, 220], '_r', 'berserker black + neon red'

def shadow(c, a_min=110, v_min=90, rim=2, keep_white=0, w_min=0, thin=0, hollow=0):
    # strokes (opaque + bright enough) -> black, a neon green rim round them, a soft green light behind;
    # keep_white > 0: the hottest pixels (white cores) stay white-green so a flash still flashes
    a = np.array(c).astype(float); v = a[..., :3].max(-1); m = (a[..., 3] > a_min) & (v > v_min) & (a[..., :3].min(-1) > w_min)   # w_min: only near-white parts (skips a coloured haze)
    if thin: m = ndimage.binary_erosion(m, iterations=thin)   # thin: strokes eroded so a wide glow does not turn into a fat black stake
    edge = ndimage.binary_dilation(m, iterations=rim) & ~m
    o = np.zeros(a.shape, np.uint8)
    o[edge] = RIM + [255]; o[m, :3] = INK; o[m, 3] = np.clip(a[m, 3] * 1.3, 0, 255).astype(np.uint8)
    if hollow:                      # big shapes (landing splashes, the orb): see-through inside a black band, a neon line on both sides
        inner = ndimage.binary_erosion(m, iterations=hollow); o[inner] = 0; o[m & ndimage.binary_dilation(inner, iterations=1) & ~inner] = RIM + [255]
    if keep_white:
        hot = m & (a[..., :3].min(-1) > keep_white) & (a[..., 3] > 200)
        hot &= ndimage.binary_erosion(m, iterations=rim)          # only well inside a stroke, the black still frames it
        o[hot, :3] = HOT
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
    man[dst] = dict(m, w=W, h=H, ax=m['ax'] + pad, ay=m['ay'] + pad, src=m['src'].split(' (')[0] + f' ({TAG}, tools/art/archer_fx.py)')
    json.dump(man, open('fx/manifest.json', 'w'), separators=(',', ':')); print(dst, out.size)

JOBS = {
    'pfx_rapier': dict(pad=10, a_min=30, v_min=60),                      # Q rapier flurry (owner's sheet); low limits: its streaks are soft
    'pfx_chargeshot': dict(pad=10, a_min=28, v_min=70),                  # R charged shot (owner's sheet, gold); the faint charge rings too
    'pfx_skyarrow': dict(pad=12, a_min=90, v_min=90),                    # E thunder javelin
    'pfx_dashstrike': dict(pad=14, a_min=110, v_min=90),                 # the hit flash on her arrows
    'pfx_vine': dict(pad=10, a_min=60, v_min=40),
    'pfx_starfall_c': dict(pad=10, a_min=120, v_min=110, w_min=205, thin=2, hollow=3),                 # X star rain: the original ParticleFX sheet with its haze faded (owner: "ในต้นแบบมันไม่ได้เป็นแบบนั้น")                        # Z thorn vine trap (owner's sheet)
}
for k in (ARGS or JOBS):
    j = dict(JOBS.get(k) or dict(pad=10, a_min=60, v_min=60)); remake(k, k + SUF, j.pop('pad'), **j)
