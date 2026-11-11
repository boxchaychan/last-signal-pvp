# The v5 Berserker's back sword: GPT / Codex draw the hilt + crossguard tilted ~25 degrees while the blade below hangs straight down,
# so the sword looks bent at the red orb (owner 2026-11-11 "ดาบเบี้ยว", "เหลือแต่ดาบเอง"). For every frame: find the red orb, cut the
# hilt + guard (a strip along the line pommel -> orb and a disc round the orb, left of the head), rotate it upright about the orb and
# put it back BEHIND the body.  python3 tools/art/sword_straighten.py <in.gif> <out.gif> [disc radius px=46]
import sys, math, numpy as np
from PIL import Image
from scipy import ndimage
src, dst = sys.argv[1], sys.argv[2]; RAD = int(sys.argv[3]) if len(sys.argv) > 3 else 46
g = Image.open(src); out = []; durs = []
for i in range(getattr(g, 'n_frames', 1)):
    g.seek(i); f = g.convert('RGBA'); a = np.asarray(f).copy(); H, W = a.shape[:2]
    r, gg, b, al = [a[..., k].astype(int) for k in range(4)]
    hot = (al > 0) & (r > 200) & (gg < 90) & (b < 90); hot[:, W // 2 + 30:] = False; hot[H // 2 + 20:] = False   # the orb sits upper left
    lab, n = ndimage.label(hot); sz = ndimage.sum(hot, lab, range(1, n + 1)); k = int(np.argmax(sz)) + 1
    oy, ox = ndimage.center_of_mass(hot, lab, k)
    # pommel = the top-most opaque pixel up-left of the orb
    ys, xs = np.nonzero(al[:int(oy) - 20, :int(ox)] > 0); j = np.argmin(ys); py, px = ys[j], xs[j]
    ang = math.degrees(math.atan2(ox - px, oy - py))
    yy, xx = np.mgrid[0:H, 0:W]; L = math.hypot(ox - px, oy - py); ux, uy = (ox - px) / L, (oy - py) / L
    t = (xx - px) * ux + (yy - py) * uy; d = np.abs((xx - px) * uy - (yy - py) * ux)
    strip = (t > -10) & (t < L) & (d < 19)
    disc = ((xx - ox) ** 2 + (yy - oy) ** 2 < RAD ** 2) & (xx < ox + RAD * .55)
    m = (strip | disc) & (al > 0)
    part = np.zeros_like(a); part[m] = a[m]; a[m] = 0
    rot = Image.fromarray(part).rotate(-ang, resample=Image.BICUBIC, center=(ox, oy))
    fin = Image.new('RGBA', (W, H)); fin.alpha_composite(rot); fin.alpha_composite(Image.fromarray(a))
    fa = np.asarray(fin).copy(); m2 = fa[..., 3] > 0
    fi = fa.astype(int); gr = (fi[..., 1] > fi[..., 0] + 40) & (fi[..., 1] > fi[..., 2] + 40) & m2   # int maths: uint8 + 40 wrapped round and blackened the white highlights; fa[gr, :3] = (46, 30, 36)   # green key spill
    l2, n2 = ndimage.label(m2, structure=np.ones((3, 3))); s2 = ndimage.sum(m2, l2, range(1, n2 + 1))
    for q, v in enumerate(s2):
        if v < 60: fa[l2 == q + 1] = 0                                                                                    # specks left behind
    fin = Image.fromarray(fa)
    out.append(fin); durs.append(g.info.get('duration', 100)); print(i, 'orb', int(ox), int(oy), 'lean', round(ang, 1))
# master frames as PNG (a GIF palette can turn the bright reds see-through: PIL picks the transparent index among the reds)
import os
od = os.path.splitext(dst)[0]; os.makedirs(od, exist_ok=True)
for i, f in enumerate(out): f.save(os.path.join(od, 'f%02d.png' % i))
def gifsafe(f):   # 255 colours for the picture, index 255 = see-through only where alpha is 0
    rgb = f.convert('RGB').quantize(255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    idx = np.asarray(rgb).copy(); idx[np.asarray(f)[..., 3] < 128] = 255
    p = Image.fromarray(idx.astype(np.uint8), 'P'); pal = rgb.getpalette()[:765] + [0, 0, 0]; p.putpalette(pal); return p
gs = [gifsafe(f) for f in out]
gs[0].save(dst, save_all=True, append_images=gs[1:], duration=durs, loop=0, disposal=2, transparency=255)
