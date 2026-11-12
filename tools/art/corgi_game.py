# Boom Corgi frames for the game (owner 2026-11-12 "ปืนหันผิดทางหรือเปล่า" -> "แก้เลย"): free, no jobs.
# The GPT design carries the cannon with the muzzle BEHIND his head, so the PixelLab standing views and frame 0 / 7 / 8 of each
# south-east shot point backwards, and the 1-star shot even swings it back while the blast goes off in front (frames 4-6).
# Fix: he stands in the AIMING pose (the cannon pointing forward) and the shot starts and ends there.
#   1 star: aim f2, fire f3, then the blasts PixelLab drew in f4-f6 (every piece apart from the body) put in front of the aiming
#           body, pushed back 3 / 2 / 1 px for the recoil, then aim again
#   2 stars: aim f2, f3-f6 as drawn, aim      3 stars: aim f1, f2-f6 as drawn, aim
#   python3 tools/art/corgi_game.py -> art/incoming/dogcat/corgi/game/{s1,s2,s3}_{idle,attack}.png + corgi.json + preview.gif
import os, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
B = 'art/incoming/dogcat/corgi/'; O = B + 'game/'; os.makedirs(O, exist_ok=True)
def fr(s, i): return Image.open(B + 'char_s%s/Idle/animations/attack_se/south-east/frame_%03d.png' % (s, i)).convert('RGBA')
def body_and_rest(im):
    """split a frame into the biggest piece (the corgi) and everything else (blast, sparks)"""
    a = np.asarray(im).copy(); m = a[..., 3] > 0; lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    if n == 0: return im, Image.new('RGBA', im.size)
    sz = ndimage.sum(m, lab, range(1, n + 1)); big = np.argmax(sz) + 1
    body = a.copy(); body[lab != big] = 0; rest = a.copy(); rest[lab == big] = 0
    return Image.fromarray(body), Image.fromarray(rest)
def shift(im, dx):
    c = Image.new('RGBA', im.size); c.alpha_composite(im, (dx, 0)) if dx >= 0 else c.alpha_composite(im.crop((-dx, 0, im.width, im.height)), (0, 0)); return c
SEQ = {}
aim1 = fr(1, 2); f3 = fr(1, 3); seq = [aim1, f3]
for i, dx in ((4, -3), (5, -2), (6, -1)):
    _, blast = body_and_rest(fr(1, i)); c = shift(aim1, dx); c.alpha_composite(blast); seq.append(c)
SEQ['1'] = (aim1, seq + [aim1])
SEQ['2'] = (fr(2, 2), [fr(2, i) for i in (2, 3, 4, 5, 6)] + [fr(2, 2)])
SEQ['3'] = (fr(3, 1), [fr(3, i) for i in (1, 2, 3, 4, 5, 6)] + [fr(3, 1)])
meta = {}
for s, (idle, att) in SEQ.items():
    idle.save(O + 's%s_idle.png' % s); w, h = idle.size
    strip = Image.new('RGBA', (w * len(att), h))
    for i, f in enumerate(att): strip.alpha_composite(f, (i * w, 0))
    strip.save(O + 's%s_attack.png' % s); meta[s] = {'cw': w, 'ch': h, 'n': len(att), 'fps': 12, 'hit': 1}
json.dump(meta, open(O + 'corgi.json', 'w'))
# preview: aim for 0.5 s, shot, aim; right-facing and mirrored, the three levels side by side
K = 3; F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16); g = []
w, h = SEQ['1'][0].size
for t in range(14):
    c = Image.new('RGBA', (w * K * 6 + 50, h * K + 26), (214, 226, 190, 255)); d = ImageDraw.Draw(c)
    for j, s in enumerate('123'):
        idle, att = SEQ[s]; f = idle if t < 6 else att[min(t - 6, len(att) - 1)]
        x = j * (w * K * 2 + 25)
        c.alpha_composite(f.resize((w * K, h * K), Image.NEAREST), (x, 26)); c.alpha_composite(f.transpose(Image.FLIP_LEFT_RIGHT).resize((w * K, h * K), Image.NEAREST), (x + w * K - 40, 26))
        d.text((x + 8, 4), '%s star' % s, fill=(30, 30, 30), font=F)
    g.append(c.convert('RGB'))
g[0].save(O + 'preview.gif', save_all=True, append_images=g[1:], duration=[90] * 14, loop=0)
print(meta)
