"""Make every move of a frame-sheet character the same body size and stand in the same place.

  python tools/art/dune_fit.py <folder with the skill strips>

AI sheets draw the character a little bigger or smaller per move. The head is the part that keeps its shape, so it is found in every
frame by template matching at many scales; each move is then rescaled to the idle size and its start lined up with idle.
Rewrites the hero_* sheets in art/dune/hero/ and their entries in art/dune/sprites.json, and prints the table.
"""
import sys, json, subprocess
import numpy as np, cv2
from PIL import Image

SK = sys.argv[1]; BASE = .82
MOVES = {'hero_idle': 'art/pixmap/dragon/idle', 'hero_run': 'art/pixmap/dragon/run', 'hero_attack1': 'art/pixmap/dragon/attack1', 'hero_attack2': 'art/pixmap/dragon/attack2', 'hero_attack3': 'art/pixmap/dragon/attack3',
         'hero_skill_dash': 'art/pixmap/dragon/skill_dash', 'hero_hurt': 'art/pixmap/dragon/hurt', 'hero_death': 'art/pixmap/dragon/death', 'hero_s_dragon': f'{SK}/hero_skill_dragon', 'hero_s_meteor': f'{SK}/hero_skill_meteor', 'hero_s_cyclone': f'{SK}/hero_skill_cyclone', 'hero_s_ult': f'{SK}/hero_skill_ult',
         'hero_s_sweep': f'{SK}/hero_skill_sweep', 'hero_s_rise': f'{SK}/hero_skill_rise', 'hero_s_rain': f'{SK}/hero_skill_rain'}
UPRIGHT = {'hero_attack1', 'hero_skill_dash', 'hero_hurt', 'hero_death', 'hero_s_dragon', 'hero_s_meteor', 'hero_s_cyclone', 'hero_s_ult', 'hero_s_sweep', 'hero_s_rise', 'hero_s_rain'}   # these sheets open in the same standing pose as idle
ONLY = set(sys.argv[2].split(',')) if len(sys.argv) > 2 else None   # optional: refit just these moves, the others stay as they are
STEADY = {'hero_s_sweep', 'hero_s_rise', 'hero_s_rain'}
def feet_mid(a, sole, S=1):   # middle of the two boots: a wide flat opening drops the thin spear butt, and anything far from the torso (a low spear tip) is ignored
    u = a.astype(np.uint8); core = np.where(cv2.erode(u, np.ones((int(21 * S), int(21 * S)), np.uint8)).any(0))[0]
    xs = np.where(cv2.morphologyEx(u[max(0, sole - int(20 * S)):sole + 1], cv2.MORPH_OPEN, np.ones((3, int(17 * S)), np.uint8)).any(0))[0]
    if len(core): xs = xs[np.abs(xs - core.mean()) < 85 * S]
    return (xs.min() + xs.max()) / 2 if len(xs) >= 12 * S else np.nan
def frames(stem):
    m = json.load(open(stem + '.json')); a = np.array(Image.open(stem + '.png').convert('RGBA')).astype(float); rgb = a[..., :3] * (a[..., 3:] / 255) + 128 * (1 - a[..., 3:] / 255); g = cv2.cvtColor(rgb.astype(np.uint8), cv2.COLOR_RGB2GRAY); al = a[..., 3] > 90
    return m, [g[:, i * m['w']:(i + 1) * m['w']] for i in range(m['n'])], [al[:, i * m['w']:(i + 1) * m['w']] for i in range(m['n'])]
def stand(al):   # height of the standing figure with its upright spear, and the sole of the feet (the spear column is left out)
    ys, xs = np.where(al); x0, x1 = xs.min(), xs.max(); body = al[:, x0:x0 + int((x1 - x0) * .72)]; return ys.max() - ys.min() + 1, int(np.where(body.any(1))[0].max())
mi, fi, ai = frames(MOVES['hero_idle']); H0, _ = stand(ai[0]); D = .5; T = cv2.resize(fi[0][52:116, 88:156], None, fx=D, fy=D, interpolation=cv2.INTER_AREA); SC = np.arange(.72, 1.36, .02); ROT = np.arange(-30, 31, 7.5)
TS = []
for s in SC:
    t = cv2.resize(T, None, fx=s, fy=s, interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC); h, w = t.shape
    for r in ROT:
        M = cv2.getRotationMatrix2D((w / 2, h / 2), float(r), 1); TS.append((float(s), cv2.warpAffine(t, M, (w, h), borderValue=128)))
def best(f):
    f = cv2.resize(f, None, fx=D, fy=D, interpolation=cv2.INTER_AREA); top = (-1, 1, 0, 0)
    for s, t in TS:
        if t.shape[0] >= f.shape[0] or t.shape[1] >= f.shape[1]: continue
        _, v, _, loc = cv2.minMaxLoc(cv2.matchTemplate(f, t, cv2.TM_CCOEFF_NORMED))
        if v > top[0]: top = (v, s, (loc[0] + t.shape[1] / 2) / D, (loc[1] + t.shape[0] / 2) / D)
    return top
idle0 = best(fi[0]); dxi = idle0[2] - mi['w'] / 2; sp = json.load(open('art/dune/sprites.json')); print(f"{'move':16} size vs idle  how")
for key, stem in MOVES.items():
    if ONLY and key not in ONLY: continue
    m, fs, als = frames(stem); h0, sole = stand(als[0]); R = [best(f) for f in (fs if key not in UPRIGHT and key != 'hero_idle' else fs[:2])]; good = sorted(R, key=lambda r: -r[0])[:7]
    if key == 'hero_idle': s, how = 1., 'base'
    elif key in UPRIGHT: s, how = h0 / H0, 'standing height'
    else: s, how = float(np.median([r[1] for r in good])), f'head match {np.mean([r[0] for r in good]):.2f}'
    k = BASE / s; out = sp.get(key, {}).get('src', f'art/dune/hero/{key[5:]}.webp'); q = json.loads(subprocess.run(['python', 'tools/art/dune_pack.py', stem + '.png', out, f'{k:.4f}'], capture_output=True, text=True, check=True).stdout); q['src'] = out; q['foot'] = int(round(q['foot'] + (sole + 1 - m['foot']) * k))
    first = max(R[:2], key=lambda r: r[0]); dx = (first[2] - m['w'] / 2) / s
    if key != 'hero_idle' and first[0] >= .4 and abs(dx - dxi) < 70: q['cx'] = int(round(q['cx'] + (dx - dxi) * BASE))
    # keep the feet on the ground in EVERY frame: the lowest solid part of the body (the thin spear is ignored) goes to the ground line
    K3 = np.ones((9, 9), np.uint8); soles = []
    for a in als:
        o = cv2.morphologyEx(a.astype(np.uint8), cv2.MORPH_OPEN, K3); y = np.where(o.any(1))[0]; soles.append(int(y.max()) if len(y) else sole)
    limit = 9 if key in ('hero_attack3', 'hero_s_meteor', 'hero_s_rise') else 26; base = soles[0]; q['foot'] = int(round(q['foot'] + (base - sole) * k)); q['dy'] = [int(round((base - v) * k)) if abs(base - v) <= limit else 0 for v in soles]
    if key in STEADY:   # the sheet draws the body a little left or right per cell: keep the middle of the two feet on one spot (frames in the air follow their neighbours)
        mid = np.array([feet_mid(a, v) if abs(base - v) <= limit else np.nan for a, v in zip(als, soles)]); ok = ~np.isnan(mid); mid = np.interp(np.arange(len(mid)), np.where(ok)[0], mid[ok]); q['dx'] = [int(round(np.clip((mid[0] - v) * k, -100, 100))) for v in mid]
    if key == 'hero_run': lo = [np.where(a[int(a.shape[0] * .8):].any(0))[0] for a in als]; rr = [int(x.max()) for x in lo if len(x)]; q['stride'] = round((max(rr) - min(rr)) * k * .5, 1)
    sp[key] = q; print(f"{key:16} {s:8.3f}  {how}  foot moved up to {max(abs(v) for v in q['dy'])} px" + (f"  stride {q['stride']}" if 'stride' in q else ''))
json.dump(sp, open('art/dune/sprites.json', 'w'), separators=(',', ':'))
