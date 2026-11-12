# Game-ready sprites for dogcat.html (free): python3 tools/art/dogcat_assets.py -> art/dogcat/{units,mobs}/*.png + sprites.json
# (the background art/dogcat/bg.png + geo.json come from: BG=1 python3 tools/art/tw_scene.py)
# Units: the PixelLab south-east attack clips, untouched (frame 0 = the standing pose); corgi = the aiming strips of corgi_game.py.
import json, os, sys, numpy as np
from PIL import Image
sys.path.insert(0, 'tools/art')
DC = 'art/incoming/dogcat/'; O = 'art/dogcat/'; os.makedirs(O + 'units', exist_ok=True); os.makedirs(O + 'mobs', exist_ok=True)
def feet(im):
    al = np.asarray(im)[..., 3] > 0; ys = np.where(al.any(1))[0]; y1 = ys[-1]; xs = np.where(al[max(0, y1 - 5):y1 + 1].any(0))[0]; return int((xs[0] + xs[-1]) // 2), int(y1), int(ys[0])
def reduce2(im):
    a = np.asarray(im.convert('RGBA')); h, w = a.shape[0] // 2 * 2, a.shape[1] // 2 * 2
    b = a[:h, :w].reshape(h // 2, 2, w // 2, 2, 4).transpose(0, 2, 1, 3, 4).reshape(h // 2, w // 2, 4, 4).astype(int)
    op = b[..., 3] >= 128; lum = (b[..., :3] * [.299, .587, .114]).sum(-1); lum = np.where(op, lum, 1e9); dark = lum.min(-1) < 58; di = lum.argmin(-1)
    key = np.where(op, (b[..., 0] >> 3) * 1024 + (b[..., 1] >> 3) * 32 + (b[..., 2] >> 3), -1); mi = ((key[..., :, None] == key[..., None, :]) & op[..., :, None]).sum(-1).argmax(-1)
    out = np.take_along_axis(b, np.where(dark, di, mi)[..., None, None].repeat(4, -1), 2)[:, :, 0]; out[..., 3] = np.where(op.sum(-1) >= 2, 255, 0); return Image.fromarray(out.astype(np.uint8))
S = {'units': {}, 'mobs': {}}
SH = {1: 'pl1s', 2: 'pl2s', 3: 'pl3'}
for s in (1, 2, 3):
    fr = [Image.open(DC + SH[s] + '/char/Idle/animations/attack_se/south-east/frame_%03d.png' % i).convert('RGBA') for i in range(9)]
    st = Image.new('RGBA', (104 * 9, 104))
    for i, f in enumerate(fr): st.alpha_composite(f, (i * 104, 0))
    st.save(O + 'units/shiba%d.png' % s); fx, fy, top = feet(fr[0]); S['units']['shiba%d' % s] = {'w': 104, 'h': 104, 'n': 9, 'fx': fx, 'fy': fy, 'top': top, 'hit': 3}
    st = Image.open(DC + 'corgi/game/s%d_attack.png' % s).convert('RGBA'); st.save(O + 'units/corgi%d.png' % s); fx, fy, top = feet(st.crop((0, 0, 104, 104)))
    S['units']['corgi%d' % s] = {'w': 104, 'h': 104, 'n': st.width // 104, 'fx': fx, 'fy': fy, 'top': top, 'hit': 1}
# idle clips (PixelLab pixminimax, 8 frames + the start frame; owner 2026-11-13 "เอา 1 ดาวมาก่อน"): units/<key>_idle.png, same cell and feet as the attack strip
import glob
for key, pat in (('shiba1', DC + 'pl1s/char/Idle/animations/idle_se/south-east/*.png'), ('corgi1', DC + 'corgi/char_s1/Idle/animations/idle_aim*/south-east/*.png')):
    fs = sorted(glob.glob(pat))[1:]
    if not fs: continue
    st = Image.new('RGBA', (104 * len(fs), 104))
    for i, f in enumerate(fs): st.alpha_composite(Image.open(f).convert('RGBA'), (i * 104, 0))
    st.save(O + 'units/%s_idle.png' % key); S['units'][key]['idle'] = len(fs)
for k in ('shroom', 'wisp', 'wolf', 'kappa', 'kasa_obake', 'paper_doll', 'monkey', 'goblin_archer'):
    m = json.load(open('art/action/mobs_hr/%s.json' % k)); im = Image.open('art/action/mobs_hr/%s.png' % k).convert('RGBA'); w, h, n = m['w'], m['h'], m['n']; r = m['rows']['walk']
    fr = [reduce2(im.crop((i * w, r * h, i * w + w, r * h + h))) for i in range(n)]; cw, ch = fr[0].size; st = Image.new('RGBA', (cw * n, ch))
    for i, f in enumerate(fr): st.alpha_composite(f, (i * cw, 0))
    st.save(O + 'mobs/%s.png' % k); S['mobs'][k] = {'w': cw, 'h': ch, 'n': n, 'fx': m['fx'] // 2, 'fy': m['fy'] // 2}
json.dump(S, open(O + 'sprites.json', 'w')); print(S)
