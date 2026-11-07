# PixelLab character download (owner 2026-11-07, Wukong: "Chibi_Sun_Wukong_the_Mon-Idle.zip") -> one legend sheet for the game.
# The zip holds <state>/rotations/<dir>.png (8 still directions, 256x256, native pixel art) and
# <state>/animations/<action name>/<dir>/frame_NNN.png (up to 40 frames, PixMiniMax).
#   python3 tools/art/pixellab_char.py <unzipped dir> <out.png> attack=<action folder | still> [skill=<action folder | file.gif | attack>] [--sub=2] [--hit=N] [--views=east,south-east,north-east]
#   --views = the PixelLab directions for the game's 3 row blocks: side (target level), toward the camera (target below, and resting),
#             away (target above). Default east,south-east,north-east: the owner prefers the diagonal views (2026-11-07 "ทำไมเราไม่ใช้เฉียง").
#             A block whose direction has no animation of its own swings with the east one (a still while attacking looked stiff:
#             the demons often pass above a slot); its idle stays its own still.
# Rows like the other legend sheets: east_idle / east_attack / east_skill, south_*, north_* (the game mirrors east for west).
# A direction without an animation gets its still in every cell (the game adds breathing, lean and lunge in code).
# PixelLab drifted Wukong's colours toward red in the middle of the attack (skin and hair red): a frame whose mean red is
# well above the first frame's gets its channels histogram-matched to the first frame, then snapped to its colours.
# --sub=2 keeps every 2nd frame (41 -> 21); --hit = frame (after sub) where the blow lands (default: the widest frame).
# Prints the LEGA numbers (cw ch fx fy h0 na hit).
import sys, os, glob, json
import numpy as np
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
opt = dict(a.split('=', 1) for a in sys.argv[3:] if '=' in a and not a.startswith('--'))
sub = int(next((a[6:] for a in sys.argv[3:] if a.startswith('--sub=')), '2'))
hit_arg = next((int(a[6:]) for a in sys.argv[3:] if a.startswith('--hit=')), None)
views = next((a[8:] for a in sys.argv[3:] if a.startswith('--views=')), 'east,south-east,north-east').split(',')
state = next(d for d in glob.glob(os.path.join(src, '*')) if os.path.isdir(os.path.join(d, 'rotations')))

def load(f): return np.array(Image.open(f).convert('RGBA')).astype(float)
def still(d): return load(os.path.join(state, 'rotations', d + '.png'))
def anim(name, d):
    if name.lower().endswith('.gif'):   # a PixelLab GIF download (one direction, east): skill=<path to gif>
        if d != 'east' or not os.path.exists(name): return None
        from PIL import ImageSequence
        return [np.array(f.convert('RGBA')).astype(float) for f in ImageSequence.Iterator(Image.open(name))][::sub]
    fs = sorted(glob.glob(os.path.join(state, 'animations', name, d, 'frame_*.png')))
    return [load(f) for f in fs][::sub] if fs else None

def fix_colours(frames):
    ref = frames[0]; R = ref[ref[..., 3] > 0][:, :3]; r0 = R[:, 0].mean()
    pal = np.unique(R.astype(np.uint8), axis=0)
    p = Image.new('P', (1, 1)); flat = list(pal.flatten())[:765]; p.putpalette(flat + [0] * (768 - len(flat)))
    out = []
    for a in frames:
        m = a[..., 3] > 0; X = a[m][:, :3]
        if X[:, 0].mean() - r0 > 15:
            for c in range(3):
                s_idx = np.argsort(X[:, c]); r = np.sort(R[:, c])
                v = np.empty(len(X)); v[s_idx] = np.interp(np.linspace(0, 1, len(X)), np.linspace(0, 1, len(r)), r); X[:, c] = v
            a = a.copy(); a[m, :3] = X
            q = np.array(Image.fromarray(a[..., :3].astype(np.uint8)).quantize(palette=p, dither=Image.Dither.NONE).convert('RGB'))
            a[..., :3] = q
        out.append(a)
    return out

act = opt.get('attack'); sk = opt.get('skill', 'attack')
rows = []
for d in views:
    st = still(d)
    A = (anim(act, d) or anim(act, 'east')) if act and act != 'still' else None
    A = fix_colours(A) if A else [st]
    S = A if sk == 'attack' else (fix_colours(anim(sk, d) or anim(sk, 'east')) if (anim(sk, d) or anim(sk, 'east')) else [st])
    rows += [[st], A, S]
# one cell for everything: the union of all frames, feet point from the east still
al = [(f[..., 3] > 0) for r in rows for f in r]
ys = [np.where(m.any(1))[0] for m in al if m.any()]; xs = [np.where(m.any(0))[0] for m in al if m.any()]
X0, X1 = min(x[0] for x in xs), max(x[-1] for x in xs) + 1; Y0, Y1 = min(y[0] for y in ys), max(y[-1] for y in ys) + 1
e = rows[0][0][..., 3] > 0; ey = np.where(e.any(1))[0]; gy = ey[-1]   # feet point from the side view's still
feet = np.where(e[gy - 4])[0]; fx = (feet[0] + feet[-1]) / 2
pad = 2; CW, CH = X1 - X0 + 2 * pad, Y1 - Y0 + 2 * pad
NA = max(len(r) for r in rows)
sheet = np.zeros((CH * len(rows), CW * NA, 4), np.uint8)
for ri, r in enumerate(rows):
    for ci in range(NA):
        f = r[min(ci, len(r) - 1)].astype(np.uint8)   # short rows repeat their last frame
        sheet[ri * CH + pad:ri * CH + pad + (Y1 - Y0), ci * CW + pad:ci * CW + pad + (X1 - X0)] = f[Y0:Y1, X0:X1]
sheet[..., 3] = np.where(sheet[..., 3] >= 128, 255, 0)
Image.fromarray(sheet).save(out, optimize=True)
na = len(rows[1])
if hit_arg is None:   # the frame reaching furthest to the right (the blow)
    reach = [np.where((f[..., 3] > 0).any(0))[0][-1] for f in rows[1]]; hit_arg = int(np.argmax(reach))
info = dict(cw=int(CW), ch=int(CH), fx=int(round(fx - X0 + pad)), fy=int(gy + 1 - Y0 + pad), h0=int(gy + 1 - ey[0]), na=int(na), hit=int(hit_arg), cols=int(NA))
print(json.dumps(info))
json.dump(dict(info, rows=['east_idle', 'east_attack', 'east_skill', 'south_idle', 'south_attack', 'south_skill', 'north_idle', 'north_attack', 'north_skill']),
          open(os.path.splitext(out)[0] + '.json', 'w'))
