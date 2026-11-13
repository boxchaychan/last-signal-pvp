# Swordsman (class 1) cut into parts for OUR bone moves (owner 2026-11-13 "เอาดาบมาทำก็ได้ คลาส 1"). Free, no jobs.
# From his PixelLab east still: head (not rotated in the rig, only moved) and torso + scarf + belt (sheared with the lean, so
# pixels stay crisp); sword from attack frame 6 (the only frame where the whole sword shows), mirrored to point right.
# Arms and legs are hidden / merged in the still, so the rig draws them as pixel capsules in his colours (combo.html `HERO`).
#   python3 tools/art/rig_parts.py -> art/poses/combo/swordsman_parts.png + .json (rect + pivot per part) + _check.png
import json, numpy as np
from PIL import Image
B = 'art/incoming/action/swordsman/pl_dl/Idle/'; O = 'art/poses/combo/swordsman_parts'
E = np.asarray(Image.open(B + 'rotations/east.png').convert('RGBA')).copy(); yy, xx = np.mgrid[0:128, 0:128]
red = (E[..., 0] > 120) & (E[..., 1] < 80)
head = E.copy(); head[~((yy <= 41) & ((xx >= 56) | (yy < 35)) & ~((xx < 58) & (yy >= 36)))] = 0
head[(yy >= 36) & red] = 0
tor = E.copy(); keep = (yy >= 40) & (yy <= 92) & (xx <= 80) & ~((xx < 56) & (yy < 52) & ~red)          # no blade, no hilt / hands in front
keep &= ~((yy <= 41) & ~red); tor[~keep] = 0
tor[head[..., 3] > 0] = 0
S = Image.open(B + 'animations/attack/east/frame_006.png').convert('RGBA').crop((0, 74, 58, 102)).transpose(Image.FLIP_LEFT_RIGHT)
parts = {}; W = 0; ims = []
def add(name, arr_or_im, pivot):
    global W
    im = Image.fromarray(arr_or_im) if isinstance(arr_or_im, np.ndarray) else arr_or_im; bb = im.getbbox(); im = im.crop(bb)
    parts[name] = {'x': W, 'y': 0, 'w': im.width, 'h': im.height, 'px': pivot[0] - bb[0], 'py': pivot[1] - bb[1]}; ims.append((W, im)); W += im.width + 2
add('head', head, (68, 42)); add('torso', tor, (66, 90)); add('sword', S, (3, 14))
def flush(O):
    global parts, W, ims
    A = Image.new('RGBA', (W, max(i.height for _, i in ims)))
    for x, i in ims: A.alpha_composite(i, (x, 0))
    A.save(O + '.png'); json.dump(parts, open(O + '.json', 'w'))
    c = Image.new('RGBA', A.size, (214, 226, 190, 255)); c.alpha_composite(A); c.resize((A.width * 4, A.height * 4), Image.NEAREST).save(O + '_check.png'); print(parts); parts = {}; W = 0; ims = []
flush(O)
# Samurai shiba 2 stars (owner "ไอ้ตัวชิบะที่ทำกระดูกมาทำได้ไหมท่านี้"): head (+ topknot) and body (+ tail, robe, feet) from his east still,
# the katana from south-east attack frame 2 (held upright there), turned to point right. Arm and legs = capsules in the rig.
D = 'art/incoming/dogcat/pl2s/char/Idle/'; E = np.asarray(Image.open(D + 'rotations/east.png').convert('RGBA')).copy(); yy, xx = np.mgrid[0:80, 0:80]
navy = (E[..., 2].astype(int) > E[..., 0].astype(int) + 10)
back = (xx < 33) & (yy >= 40) & (yy <= 45) & (E[..., 2] > 90)                 # the sheathed sword tip behind him
E[back] = 0; E[(yy >= 30) & (yy <= 36) & (xx >= 56)] = 0                    # + the breath puff
head = E.copy(); hm = (yy <= 46) & ~navy & ~((yy >= 44) & (xx < 34)); head[~hm] = 0
tor = E.copy(); tor[hm | (yy < 40)] = 0
K = Image.open(D + 'animations/attack_se/south-east/frame_002.png').convert('RGBA').crop((19, 12, 34, 48)); k = np.asarray(K).copy(); ky, kx = np.mgrid[0:36, 0:15]
k[(ky >= 32) & (kx < 5)] = 0; K = Image.fromarray(k).transpose(Image.ROTATE_270)
from scipy import ndimage
def biggest(a):
    lab, n = ndimage.label(a[..., 3] > 0); sz = ndimage.sum(a[..., 3] > 0, lab, range(1, n + 1)); a[lab != np.argmax(sz) + 1] = 0; return a
head[(xx < 26) & (yy >= 38)] = 0; tor[yy >= 70] = 0; tor[(yy <= 43)] = 0                   # leftovers of the back sword; his painted feet + shadow line (the rig draws the feet)
head = biggest(head); tor = biggest(tor)
add('head', head, (42, 46)); add('torso', tor, (40, 70)); add('sword', K, (2, 11)); flush('art/poses/combo/shiba2_parts')

