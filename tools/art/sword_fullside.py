# Owner 2026-11-11 "แก้ภาพด้านข้างให้ดาบเต็ม": the v5 side view hides the blade behind the cape (only the hilt shows). Cut the
# whole blade from the back view (where it lies on top of his back, art/incoming/side/berserker/REF_back_full_sword.png), turn it
# upright, scale it to the side picture and lay it over the cape under the straightened crossguard, clipped at his back.
#   python3 tools/art/sword_fullside.py -> art/incoming/side/berserker/REF_side_512_fullsword(.png|_white.png)
import math, numpy as np
from PIL import Image
D = 'art/incoming/side/berserker/'
back = Image.open(D + 'REF_back_full_sword.png').convert('RGBA'); b = np.asarray(back).copy(); H, W = b.shape[:2]
gx, gy, tx, ty, HW = 385, 205, 148, 532, 44          # back view: blade top (under the guard), tip, half width
L = math.hypot(tx - gx, ty - gy); ux, uy = (tx - gx) / L, (ty - gy) / L
yy, xx = np.mgrid[0:H, 0:W]; t = (xx - gx) * ux + (yy - gy) * uy; d = (xx - gx) * uy - (yy - gy) * ux
# the blade tapers to the point over its last 60 px
hw = np.where(t > L - 60, HW * np.clip((L - t) / 60, 0, 1), HW)
m = (t > 0) & (t < L + 4) & (np.abs(d) < hw)
blade = np.zeros_like(b); blade[m] = b[m]; blade[m, 3] = 255
ang = math.degrees(math.atan2(-(tx - gx), ty - gy))   # lean of the blade from straight down
bi = Image.fromarray(blade).rotate(ang, resample=Image.BICUBIC, center=(gx, gy), expand=False)
bi = bi.crop(bi.getbbox())
side = Image.open(D + 'REF_side_512_straight.png').convert('RGBA')
K = 0.62; bi = bi.resize((round(bi.width * K), round(bi.height * K)), Image.LANCZOS)
ox, oy = 236, 196                                      # side view: under the red orb
lay = Image.new('RGBA', side.size); lay.alpha_composite(bi, (ox - bi.width // 2, oy))
la = np.asarray(lay).copy(); la[:, 262:] = 0          # behind his back: nothing past the back line
out = side.copy(); out.alpha_composite(Image.fromarray(la))
# the crossguard + hilt go back on top of the blade's top end
s = np.asarray(side); top = np.zeros_like(s); top[:oy + 22] = s[:oy + 22]; top[oy + 22:] = 0
out.alpha_composite(Image.fromarray(top))
out.save(D + 'REF_side_512_fullsword.png')
w = Image.new('RGBA', out.size, (255, 255, 255, 255)); w.alpha_composite(out); w.convert('RGB').save(D + 'REF_side_512_fullsword_white.png')
print('blade', bi.size, 'lean', round(ang, 1))
