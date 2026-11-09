# Thai city wall pieces (owner 2026-11-09 "แมพไทยไม่สวย กำแพง"): the old wall_sema picture had bushes painted on both ends
# and was stamped round an ellipse, so the sides piled up. Writes:
#   art/action/props/wall_front.png  a seamless 54 px tile cut from wall_sema (two merlon periods, two windows, no bushes)
#   art/action/props/wall_side.png   a 28 px piece of a wall running north-south seen from above: the walkway between two
#                                    rows of merlons, raised as high as the front wall (tiles straight down)
#   art/action/props/t_fort_w.png    the corner fort with its red brick turned to the same whitewashed plaster (roof kept)
#   python tools/art/thai_wall.py
import numpy as np
from PIL import Image

P = 'art/action/props/'
a = np.array(Image.open(P + 'wall_sema.png').convert('RGBA'))
x0, x1 = 57, 111                                  # merlons every 27 px; windows at 66 and 102 stay whole
t = a[:, x0:x1].copy()
t[80:, 43:54] = a[80:, 64:75]                     # the right bush reaches in at the bottom: copy clean base stones over it
Image.fromarray(t).save(P + 'wall_front.png')

# colours of the plaster, from light to dark, plus the outline
op = a[..., 3] > 200; px = a[op][:, :3].astype(int); lum = px.sum(1)
def pick(lo, hi):
    m = (lum >= lo) & (lum < hi); return tuple(np.median(px[m], 0).astype(int)) if m.any() else (200, 190, 180)
OUT, DARK, MID, LIGHT, TOP = (58, 40, 38), (168, 126, 108), (212, 180, 158), (236, 214, 196), (250, 238, 226)   # the wall's warm plaster (the median picks caught moss)
W, SEG, H = 34, 28, 80                            # wall thickness, piece length, raised height (the front wall's face)
img = np.zeros((SEG + H, W, 4), np.uint8)
def rect(x, y, w, h, c): img[y:y + h, x:x + w, :3] = c; img[y:y + h, x:x + w, 3] = 255
rect(0, 0, W, SEG, MID)                           # walkway
rect(3, 0, W - 6, SEG, LIGHT)
for y in range(0, SEG, 14): rect(4, y, W - 8, 1, MID)   # stone joints
rect(W // 2, 7, 1, 7, MID); rect(W // 2 - 6, 21, 1, 7, MID)
for x in (0, W - 7):                              # merlons on both edges, raised: a lit top and a darker lip
    for y in range(1, SEG, 14):
        rect(x, y, 7, 9, TOP); rect(x, y + 9, 7, 2, DARK); rect(x, y, 7, 1, LIGHT)
img[:SEG, 0, :3] = OUT; img[:SEG, W - 1, :3] = OUT  # outline down both sides
img[:SEG, W - 2, :3] = DARK                       # the east side a step darker (light from the left)
# the body under the walkway is hidden by the walkway of the piece in front (pieces overlap), only a faint shadow strip
rect(0, SEG, W, 2, DARK); img[SEG:SEG + 2, :, 3] = 90
Image.fromarray(img).save(P + 'wall_side.png')

# the fort: brick reds -> plaster by brightness, the tiled roof (orange-red, top part) kept
f = np.array(Image.open(P + 't_fort.png').convert('RGBA')).astype(float)
r, g, b = f[..., 0], f[..., 1], f[..., 2]; L = (r * .3 + g * .59 + b * .11)
brick = (r > g + 18) & (r > b + 25) & (f[..., 3] > 0)
roof = np.zeros_like(brick); roof[:125] = True
ramp = np.array([OUT, DARK, MID, LIGHT, TOP], float); lv = np.array([22, 62, 92, 122, 158], float)   # the bricks are dark: spread them up into the plaster
idx = np.clip(np.searchsorted(lv, L) , 1, 4); lo, hi = lv[idx - 1], lv[idx]; k = np.clip((L - lo) / (hi - lo), 0, 1)[..., None]
col = ramp[idx - 1] * (1 - k) + ramp[idx] * k
m = brick & ~roof
f[m, :3] = col[m]
Image.fromarray(f.clip(0, 255).astype(np.uint8)).save(P + 't_fort_w.png')
print('colours', OUT, DARK, MID, LIGHT, TOP)
