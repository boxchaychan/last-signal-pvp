# The 1.5x versions of the props that are not straight out of a sheet (owner 2026-11-10 "เอาฉากให้คม"), after
# `PROP_K=1.5 python tools/art/thai_props.py` has made props_hr/wall_sema.png and t_fort.png:
#   wall_front  = the same tile cut from the 1.5x wall_sema (thai_wall.py's columns x 1.5)
#   wall_side   = thai_wall.py's code-drawn piece, scaled 1.5 (flat bands, nearest)
#   t_fort_w    = thai_wall.py's plaster recolour on the 1.5x t_fort
#   t_fort_wl/r = t_fort_w with the same parts cut as in the low-res pictures (their removed pixels, scaled up)
# The side gates t_gate_l / _r come from props_px.py on the cut art/incoming/maps/thai_gate_4view.png at 0=570.
#   python tools/art/props_hr_extra.py
import numpy as np
from PIL import Image

P, H, K = 'art/action/props/', 'art/action/props_hr/', 1.5
ld = lambda f: np.array(Image.open(f).convert('RGBA'))

a = ld(H + 'wall_sema.png')
x0 = round(57 * K); w = round(54 * K); t = a[:, x0:x0 + w].copy()
r0 = round(80 * K); t[r0:, round(43 * K):w] = a[r0:, round(64 * K):round(64 * K) + w - round(43 * K)]   # the bush at the right end
Image.fromarray(t).save(H + 'wall_front.png')

s = Image.open(P + 'wall_side.png'); s.resize((round(s.width * K), round(s.height * K)), Image.NEAREST).save(H + 'wall_side.png')

OUT, DARK, MID, LIGHT, TOP = (58, 40, 38), (168, 126, 108), (212, 180, 158), (236, 214, 196), (250, 238, 226)
f = ld(H + 't_fort.png').astype(float)
r, g, b = f[..., 0], f[..., 1], f[..., 2]; L = r * .3 + g * .59 + b * .11
brick = (r > g + 18) & (r > b + 25) & (f[..., 3] > 0)
roof = np.zeros_like(brick); roof[:round(125 * K)] = True
ramp = np.array([OUT, DARK, MID, LIGHT, TOP], float); lv = np.array([22, 62, 92, 122, 158], float)
idx = np.clip(np.searchsorted(lv, L), 1, 4); lo, hi = lv[idx - 1], lv[idx]; k = np.clip((L - lo) / (hi - lo), 0, 1)[..., None]
col = ramp[idx - 1] * (1 - k) + ramp[idx] * k
m = brick & ~roof; f[m, :3] = col[m]
fw = f.clip(0, 255).astype(np.uint8); Image.fromarray(fw).save(H + 't_fort_w.png')

base = ld(P + 't_fort_w.png')[..., 3] > 0
for n in ('t_fort_wl', 't_fort_wr'):
    cut = base & ~(ld(P + n + '.png')[..., 3] > 0)
    big = np.array(Image.fromarray(cut.astype(np.uint8) * 255).resize((fw.shape[1], fw.shape[0]), Image.NEAREST)) > 0
    o = fw.copy(); o[big, 3] = 0; Image.fromarray(o).save(H + n + '.png'); print(n, int(cut.sum()), 'px cut')
print('done')
