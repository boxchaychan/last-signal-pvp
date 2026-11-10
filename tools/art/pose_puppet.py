# Animate our own sprite into an example's poses WITHOUT any generator (owner 2026-11-10 "ให้ครอสทำเอง ไม่ใช่ PixelLab"):
# a pixel-art puppet. Every opaque pixel of our still is given to the nearest bone of OUR skeleton (head, torso, upper /
# lower arms, thighs / shins; the weapon goes with the hand that holds it), then each frame moves every bone rigidly onto
# the target skeleton (rotation about its parent joint + the joint's new place) and draws the parts back to front
# (far limbs, torso, head, near limbs) with nearest-pixel sampling, so pixels stay crisp, no blur and no new colours.
#   python tools/art/pose_puppet.py <skeletons.json from pose_copy.py> <our still.png> <out dir> [near=right|left] [fps]
# skeletons.json holds {"ours": {...}, "target": [{...}, ...]} with joints in our still's pixels (pose_copy.py --dry
# writes it; the joints can also be tapped by hand in posecopy.html, so no credits at all).
import sys, os, json, math
import numpy as np
from PIL import Image

SEG = {   # bone: (joint a, joint b) on the skeleton
 'torso': ('ROOT', 'NECK'), 'head': ('NECK', 'NOSE'),
 'r_up': ('RIGHT SHOULDER', 'RIGHT ELBOW'), 'r_lo': ('RIGHT ELBOW', 'RIGHT ARM'),
 'l_up': ('LEFT SHOULDER', 'LEFT ELBOW'), 'l_lo': ('LEFT ELBOW', 'LEFT ARM'),
 'r_th': ('RIGHT HIP', 'RIGHT KNEE'), 'r_sh': ('RIGHT KNEE', 'RIGHT LEG'),
 'l_th': ('LEFT HIP', 'LEFT KNEE'), 'l_sh': ('LEFT KNEE', 'LEFT LEG')}

def root(s): return ((s['RIGHT HIP'][0] + s['LEFT HIP'][0]) / 2, (s['RIGHT HIP'][1] + s['LEFT HIP'][1]) / 2)
def P(s, j): return root(s) if j == 'ROOT' else tuple(s[j])

def seg_dist(px, py, a, b):
    ax, ay = a; bx, by = b; dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy or 1
    t = np.clip(((px - ax) * dx + (py - ay) * dy) / L2, 0, 1)
    return np.hypot(px - (ax + t * dx), py - (ay + t * dy)), t

def assign(img, sk):
    a = img[..., 3] > 0; H, W = a.shape; yy, xx = np.mgrid[0:H, 0:W].astype(float)
    names = list(SEG); D = []
    for n in names:
        d, t = seg_dist(xx, yy, P(sk, SEG[n][0]), P(sk, SEG[n][1]))
        if n == 'head': d = d * .55            # the head is a big round blob round a short bone: let it win nearby
        if n == 'torso': d = d * .8
        if n.endswith('_lo'):                  # a hand's weapon reaches past the wrist: pixels beyond it stay with the forearm
            pass
        D.append(d)
    lab = np.argmin(np.stack(D), 0); lab[~a] = -1
    return names, lab

def rigid(sk_from, sk_to, n):
    a0, b0 = P(sk_from, SEG[n][0]), P(sk_from, SEG[n][1]); a1, b1 = P(sk_to, SEG[n][0]), P(sk_to, SEG[n][1])
    th = math.atan2(b1[1] - a1[1], b1[0] - a1[0]) - math.atan2(b0[1] - a0[1], b0[0] - a0[0])
    return a0, a1, th

def render(img, names, lab, ours, tgt, order):
    H, W = lab.shape; out = np.zeros_like(img); yy, xx = np.mgrid[0:H, 0:W].astype(float)
    for n in order:
        k = names.index(n); a0, a1, th = rigid(ours, tgt, n); c, s = math.cos(-th), math.sin(-th)
        dx, dy = xx - a1[0], yy - a1[1]; sx = np.rint(a0[0] + dx * c - dy * s).astype(int); sy = np.rint(a0[1] + dx * s + dy * c).astype(int)
        ok = (sx >= 0) & (sy >= 0) & (sx < W) & (sy < H); m = np.zeros((H, W), bool)
        m[ok] = lab[sy[ok], sx[ok]] == k
        out[m] = img[sy[m], sx[m]]
    return out

def render_lbs(img, ours, tgt, near='right'):
    # smooth skinning: every pixel moves with a weighted blend of the bones near it (weights fall off with distance, the
    # torso and head reach further), splatted forward at 2x so no holes open; where two pixels land on one spot the one
    # nearer the camera wins (near arm > head > torso > far arm), then single-pixel gaps are filled from their neighbours
    H, W = img.shape[:2]; a = img[..., 3] > 0; ys, xs = np.nonzero(a); px, py = xs.astype(float), ys.astype(float)
    names = list(SEG); far = 'l' if near == 'right' else 'r'
    ZS = {n: (3 if n.startswith(('r_' if near == 'right' else 'l_')) else 0 if n.startswith(far + '_') else 2 if n == 'head' else 1) for n in names}
    wts, X, Y, Z = [], 0, 0, 0
    for n in names:
        d, _ = seg_dist(px, py, P(ours, SEG[n][0]), P(ours, SEG[n][1])); sc = {'torso': 10, 'head': 16}.get(n, 4)
        w = np.exp(-(d / sc) ** 2)
        if n == 'torso': w = w + .02            # anything far from every bone (cape, loose hair) follows the body
        if n == 'head': w = w * (py < P(ours, 'NECK')[1] + 4) + 1e-6   # the hair and headband above the neck go with the head
        wts.append(w)
    Wt = np.stack(wts); Wt = Wt ** 2; Wt /= Wt.sum(0) + 1e-9   # mostly one bone, a soft blend only at the joints
    for k, n in enumerate(names):
        a0, a1, th = rigid(ours, tgt, n); c, s_ = math.cos(th), math.sin(th); dx, dy = px - a0[0], py - a0[1]
        X = X + Wt[k] * (a1[0] + dx * c - dy * s_); Y = Y + Wt[k] * (a1[1] + dx * s_ + dy * c); Z = Z + Wt[k] * ZS[n]
    out = np.zeros_like(img); zb = np.full((H, W), -9.0)
    for ox in (0, .5):
        for oy in (0, .5):
            tx = np.rint(X + ox - .25).astype(int); ty = np.rint(Y + oy - .25).astype(int); ok = (tx >= 0) & (ty >= 0) & (tx < W) & (ty < H)
            for i in np.argsort(Z[ok], kind='stable'):
                j = np.nonzero(ok)[0][i]; x, y = tx[j], ty[j]
                if Z[j] >= zb[y, x]: zb[y, x] = Z[j]; out[y, x] = img[ys[j], xs[j]]
    hole = (out[..., 3] == 0)
    nb = sum(np.roll(np.roll(out[..., 3] > 0, dy, 0), dx, 1) for dy in (-1, 0, 1) for dx in (-1, 0, 1))
    fill = hole & (nb >= 6)
    for y, x in zip(*np.nonzero(fill)):
        for dy, dx in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            if 0 <= y + dy < H and 0 <= x + dx < W and out[y + dy, x + dx, 3]: out[y, x] = out[y + dy, x + dx]; break
    return out

if __name__ == '__main__':
    a = sys.argv[1:]; js, still, outd = a[:3]; near = a[3] if len(a) > 3 else 'right'; fps = int(a[4]) if len(a) > 4 else 12
    J = json.load(open(js)); ours = J['ours']; tg = J['target']; img = np.array(Image.open(still).convert('RGBA'))
    names, lab = assign(img, ours)
    far, nr = ('l', 'r') if near == 'right' else ('r', 'l')
    order = [far + '_th', far + '_sh', far + '_up', far + '_lo', 'torso', nr + '_th', nr + '_sh', 'head', nr + '_up', nr + '_lo']
    os.makedirs(outd, exist_ok=True); frames = []
    for i, t in enumerate(tg):
        f = Image.fromarray(render_lbs(img, ours, t, near) if '--cut' not in sys.argv else render(img, names, lab, ours, t, order)); f.save(os.path.join(outd, 'p%02d.png' % i)); frames.append(f)
    # parts map for checking
    pal = np.array([[230, 80, 80], [250, 200, 80], [80, 200, 250], [40, 120, 220], [120, 250, 120], [40, 160, 60], [250, 120, 220], [170, 60, 160], [250, 250, 250], [140, 140, 140]], np.uint8)
    pm = np.zeros(img.shape, np.uint8); m = lab >= 0; pm[m, :3] = pal[lab[m]]; pm[m, 3] = 255; Image.fromarray(pm).save(os.path.join(outd, 'parts.png'))
    bg = [Image.alpha_composite(Image.new('RGBA', f.size, (79, 122, 60, 255)), f).resize((f.width * 2, f.height * 2), Image.NEAREST).convert('RGB') for f in frames]
    bg[0].save(os.path.join(outd, 'puppet.gif'), save_all=True, append_images=bg[1:], duration=int(1000 / fps), loop=0)
    print(len(frames), 'frames ->', outd)
