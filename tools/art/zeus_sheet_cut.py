"""The owner's own Zeus sheet (GPT, 2026-11-27: art/incoming/zeus_sheet/owner_sheet_raw.png) cut into the pieces of a rig, WITHOUT redrawing anything
(owner: a GPT redraw changed his build, "ฉันต้องการคงเดิมไว้"). Every pixel is the sheet's own.
  - the pieces box (top right): torso, skirt, 2 upper arms, 2 forearms with fists, 2 thighs, 2 feet -> dark-outline flood from the box border;
  - the 6 faces row: 6 whole heads on ONE canvas size, chins lined up, so a move can swap the face;
  - the bolt (no dark outline): by colour;
  - the front view (top left) = the faint reference picture and the rig's own space (380 x 426, feet at 182, 418).
  - the two open hands = cut from the front view itself; the forearms get a fist-less copy (they swap by move);
  - FIT: every piece turned / sized / moved by a masked match until it lies on the front view = the rest pose.
-> art/rigs/zeusgpt/*.png + art/rigs/zeusgpt.json (rig.html?char=zeusgpt, rig2d/bones.js).     pip install pillow numpy scipy opencv-python-headless ; python3 tools/art/zeus_sheet_cut.py"""
import json, os
import numpy as np
from PIL import Image
from scipy import ndimage as nd
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'); OUT = os.path.join(R, 'art/rigs/zeusgpt'); os.makedirs(OUT, exist_ok=True)
A = np.asarray(Image.open(os.path.join(R, 'art/incoming/zeus_sheet/owner_sheet_raw.png')).convert('RGB'), np.float32); LUM = A @ np.array([.299, .587, .114], np.float32); M = 3
def pieces(box, thr=62):
    """whole pieces inside a box: everything the background cannot reach from the box border without crossing a dark outline"""
    x0, y0, x1, y1 = box; L = LUM[y0:y1, x0:x1]; B = L < thr; Bd = nd.binary_dilation(B); lab, n = nd.label(~Bd)
    edge = (set(lab[0]) | set(lab[-1]) | set(lab[:, 0]) | set(lab[:, -1])) - {0}; bg = np.isin(lab, list(edge)); pc = ~bg; pc &= ~(Bd & ~B & nd.binary_dilation(bg)); lab2, n2 = nd.label(pc); out = []
    for i, sl in enumerate(nd.find_objects(lab2)):
        m = lab2[sl] == i + 1
        if m.sum() >= 120: out.append((sl[1].start + x0, sl[0].start + y0, m))
    return out
def cut(x, y, m, canvas=None, anchor=None):
    """one piece as RGBA with a soft 1-pixel edge; canvas = (w, h) + anchor = where the piece's bottom-centre goes (faces share one canvas)"""
    h, w = m.shape; y0, x0 = y - M, x - M; mm = np.zeros((h + 2 * M, w + 2 * M), bool); mm[M:-M, M:-M] = m; rgb = A[y0:y0 + mm.shape[0], x0:x0 + mm.shape[1]].copy(); L = LUM[y0:y0 + mm.shape[0], x0:x0 + mm.shape[1]]
    ring = nd.binary_dilation(mm) & ~mm; far = ~nd.binary_dilation(mm, iterations=3); bgl = nd.uniform_filter(np.where(far, L, 0), 15) / np.maximum(nd.uniform_filter(far.astype(np.float32), 15), 1e-3)
    a = mm.astype(np.float32); a[ring] = np.clip((bgl[ring] - L[ring]) / np.maximum(bgl[ring] - 30, 20), 0, 1) * .85; dark = rgb[mm & (L < 62)].mean(0) if (mm & (L < 62)).any() else np.array([30, 20, 14]); rgb[ring] = dark
    im = Image.fromarray(np.dstack([rgb, a * 255]).clip(0, 255).astype(np.uint8), 'RGBA')
    if canvas: c = Image.new('RGBA', canvas, (0, 0, 0, 0)); c.alpha_composite(im, (anchor[0] - im.width // 2, anchor[1] - im.height)); im = c
    return im
def at(ps, px, py): return next(p for p in ps if p[0] <= px < p[0] + p[2].shape[1] and p[1] <= py < p[1] + p[2].shape[0] and p[2][py - p[1], px - p[0]])
P = pieces((872, 4, 1532, 436)); IMG = {}
for name, (px, py) in dict(torso=(960, 215), skirt=(960, 330), uarm_r=(1080, 195), uarm_l=(1185, 195), fore_r=(1080, 265), fore_l=(1183, 265), thigh_r=(1076, 338), thigh_l=(1156, 338), foot_r=(1066, 410), foot_l=(1168, 410)).items():
    IMG[name] = cut(*at(P, px, py))   # _r = HIS right = the left of the picture (the weapon side)
F = sorted(pieces((8, 444, 1010, 580)), key=lambda p: p[0]); FW, FH = max(p[2].shape[1] for p in F) + 2 * M + 2, max(p[2].shape[0] for p in F) + 2 * M + 2
for i, p in enumerate(F): IMG[f'face{i}'] = cut(*p, canvas=(FW, FH), anchor=(FW // 2, FH))   # 0 smirk, 1 shout, 2 teeth, 3 eyes shut, 4 "o", 5 frown
# the bolt: bright white core, gold and blue rim, no dark outline -> by colour inside its own box; the soft glow that melts into the backdrop stays behind
bx0, by0, bx1, by1 = 1452, 132, 1534, 336; a = A[by0:by1, bx0:bx1] / 255; mx, mn = a.max(2), a.min(2); sat = (mx - mn) / np.maximum(mx, 1e-3)
m = ((sat > .5) & (mx > .55)) | ((mx > .93) & (sat < .25)); m = nd.binary_fill_holes(nd.binary_closing(m, iterations=2)); lab, n = nd.label(m); m = lab == (np.bincount(lab.ravel())[1:].argmax() + 1); ys, xs = np.nonzero(m)
IMG['bolt'] = cut(bx0 + xs.min(), by0 + ys.min(), m[ys.min():ys.max() + 1, xs.min():xs.max() + 1])
REF = A[6:432, 20:400]; RX, RY = 20, 6   # the front view = the rig's space and the target every piece is fitted onto
Image.fromarray(REF.astype(np.uint8), 'RGB').save(os.path.join(OUT, 'ref.png'))

# ---- hands: the open hands of the front view itself (they show whole, under the cuff), so the rest pose is HIS hands
GOLD = lambda a: (a[..., 0] > 170) & (a[..., 1] > 120) & (a[..., 2] < 110) & (a[..., 0] - a[..., 2] > 90)
HMASK = []
def hand_from_front(box, inside):
    """the hand under a cuff: the part of the box the background cannot reach, the component under `inside`; dark lines kept only near its own skin"""
    x0, y0, x1, y1 = box; L = LUM[y0:y1, x0:x1]; B = L < 62; Bd = nd.binary_dilation(B); lab, n = nd.label(~Bd)
    edge = (set(lab[0]) | set(lab[-1]) | set(lab[:, 0]) | set(lab[:, -1])) - {0}; core = ~np.isin(lab, list(edge)) & ~Bd & ~GOLD(A[y0:y1, x0:x1])
    lab2, _ = nd.label(core); keep = lab2 == lab2[inside[1] - y0, inside[0] - x0]; keep = nd.binary_fill_holes(nd.binary_dilation(keep, iterations=1) | (nd.binary_fill_holes(keep | (B & nd.binary_dilation(keep, iterations=5)))))
    keep &= (B & nd.binary_dilation(keep & ~B, iterations=5)) | ~B; keep &= ~GOLD(A[y0:y1, x0:x1]); ys, xs = np.nonzero(keep)
    g = GOLD(A[y0:y1, x0:x1]) & nd.binary_dilation(keep, iterations=4); gy, gx = np.nonzero(g & ~keep); hy, hx = np.nonzero(keep & nd.binary_dilation(g, iterations=4))
    wrist = (x0 + hx.mean(), y0 + hy.mean()); sub = keep[ys.min():ys.max() + 1, xs.min():xs.max() + 1]; ox, oy = x0 + xs.min(), y0 + ys.min()
    full = np.zeros(LUM.shape, bool); full[y0:y1, x0:x1] = keep; HMASK.append(full)
    return cut(ox, oy, sub), (wrist[0] - ox + M, wrist[1] - oy + M), (wrist[0] - RX, wrist[1] - RY)
IMG['hand_r'], HPV_R, HAT_R = hand_from_front((36, 244, 122, 300), (60, 280))   # his right = left of the picture (the bolt hand)
IMG['hand_l'], HPV_L, HAT_L = hand_from_front((276, 244, 362, 300), (338, 280))

# ---- the forearm pieces end in a fist: a copy with the fist taken off below the cuff (same canvas, so the two swap); the open hand goes under the cuff
def unfist(im, elbow):
    a = np.asarray(im).copy(); al = a[..., 3] > 40; c = a[..., :3].astype(np.float32); g = (c[..., 0] > 190) & (c[..., 1] > 140) & (c[..., 2] < 90) & (c[..., 0] - c[..., 2] > 130) & al; lab, n = nd.label(nd.binary_closing(g, iterations=2)); g = lab == (np.bincount(lab.ravel())[1:].argmax() + 1)     # the cuff: the biggest strongly gold patch (skin shading is orange too)
    ys, xs = np.nonzero(al); far = np.argmax((xs - elbow[0]) ** 2 + (ys - elbow[1]) ** 2)
    ax = np.array([xs[far] - elbow[0], ys[far] - elbow[1]], np.float32); ax /= np.linalg.norm(ax); yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]; pr = (xx - elbow[0]) * ax[0] + (yy - elbow[1]) * ax[1]
    end = pr[g].max(); a[pr > end + 2.5, 3] = 0; return Image.fromarray(a, 'RGBA')
IMG['fore_r_open'] = unfist(IMG['fore_r'], (17, 15)); IMG['fore_l_open'] = unfist(IMG['fore_l'], (IMG['fore_l'].width - 17, 15))
IMG['none'] = Image.new('RGBA', (2, 2), (0, 0, 0, 0))
for k, im in IMG.items(): im.save(os.path.join(OUT, k + '.png'))
S = {k: im.size for k, im in IMG.items()}

# ---- FIT: every piece is turned / sized / moved until it lies best on the front view (OpenCV masked match, coarse then fine),
#      searched near a rough first guess so a left piece never lands on the right
import cv2
REFF = cv2.GaussianBlur(REF, (0, 0), 1.0)
def fit(key, pv, guess, ang, scl, win=46):
    im = np.asarray(IMG[key]).astype(np.float32); rgb, al = im[..., :3], im[..., 3] / 255; best = None
    def tryone(a, s):
        h, w = al.shape; Mx = cv2.getRotationMatrix2D((float(pv[0]), float(pv[1])), -a, s); cs = np.array([[0, 0, 1], [w, 0, 1], [0, h, 1], [w, h, 1]], np.float32) @ Mx.T; mn = np.floor(cs.min(0)) - 1; mx = np.ceil(cs.max(0)) + 1
        Mx[:, 2] -= mn; W2, H2 = int(mx[0] - mn[0]), int(mx[1] - mn[1]); t = cv2.warpAffine(rgb, Mx, (W2, H2)); m = cv2.warpAffine(al, Mx, (W2, H2)); m = (m > .6).astype(np.float32)
        px, py = Mx @ np.array([pv[0], pv[1], 1], np.float32); gx, gy = guess; x0, y0 = int(gx - px - win), int(gy - py - win); x0 = max(0, x0); y0 = max(0, y0)
        reg = REFF[y0:min(REF.shape[0], y0 + H2 + 2 * win), x0:min(REF.shape[1], x0 + W2 + 2 * win)]
        if reg.shape[0] < H2 + 1 or reg.shape[1] < W2 + 1: return None
        r = cv2.matchTemplate(np.ascontiguousarray(reg), np.ascontiguousarray(t), cv2.TM_SQDIFF, mask=np.dstack([m, m, m])) / max(1, m.sum()); v, _, loc, _ = cv2.minMaxLoc(r)
        return v, a, s, (x0 + loc[0] + px, y0 + loc[1] + py)
    for a in ang:
        for s in scl:
            o = tryone(a, s)
            if o and (best is None or o[0] < best[0]): best = o
    v, a0, s0, _ = best
    for a in np.arange(a0 - 3, a0 + 3.01, 1):
        for s in np.arange(s0 - .04, s0 + .041, .01):
            o = tryone(a, s)
            if o and o[0] < best[0]: best = o
    v, a, s, (x, y) = best; print(f'  fit {key:12s} turn {a:6.1f}  size {s:4.2f}  at ({x:6.1f},{y:6.1f})  error {v ** .5 / 255 * 100:4.1f}%'); return dict(at=[round(float(x), 1), round(float(y), 1)], r=round(float(a), 1), s=round(float(s), 3))
R3 = lambda a, b, st: list(np.arange(a, b + .01, st)); w = lambda k: S[k][0]; h = lambda k: S[k][1]
PV = dict(torso=[w('torso') / 2, h('torso') - 9], skirt=[w('skirt') / 2, 12], head=[w('face0') / 2, h('face0') - 12], uarm_r=[w('uarm_r') - 17, 15], uarm_l=[17, 15], fore_r_open=[17, 15], fore_l_open=[w('fore_l') - 17, 15],
          thigh_r=[w('thigh_r') / 2, 9], thigh_l=[w('thigh_l') / 2, 9], foot_r=[w('foot_r') - 23, 10], foot_l=[23, 10], bolt=[w('bolt') / 2, h('bolt') * .55])
F = {}
F['torso'] = fit('torso', PV['torso'], (181, 268), R3(-6, 6, 3), R3(.85, 1.05, .04))
F['skirt'] = fit('skirt', PV['skirt'], (181, 268), R3(-6, 6, 3), R3(.92, 1.12, .04))
F['head'] = fit('face0', PV['head'], (179, 178), R3(-6, 6, 3), R3(1.36, 1.6, .04))
for sd, sg, gx in (('r', 1, 141), ('l', -1, 222)):
    pass   # the arms come from the front view itself (below)

    F['thigh_' + sd] = fit('thigh_' + sd, PV['thigh_' + sd], (gx + sg * 4, 320), R3(-12, 12, 4), R3(.85, 1.05, .05))
    F['foot_' + sd] = fit('foot_' + sd, PV['foot_' + sd], (gx, 364), R3(-8, 8, 4), R3(.9, 1.1, .05))
F['bolt'] = dict(at=[round(HAT_R[0] - 10, 1), round(HAT_R[1] + 14, 1)], r=10, s=.62)   # the front view has no bolt: held upright in his right hand, like the first pose of the owner's attack row
print({k: v for k, v in S.items()})

# ---- ARMS from the front view itself: shoulder to cuff in ONE piece (his arms have no elbow line), cut at the shoulder inside the part the torso covers;
#      what lies under the torso is the chest skin of the front view, so a turning arm never opens a hole. The hand stays its own piece under the cuff.
from PIL import ImageDraw
def front_piece(poly, minus):
    x0, y0, x1, y1 = 8, 0, 392, 436; L = LUM[y0:y1, x0:x1]; B = L < 62; Bd = nd.binary_dilation(B); lab, n = nd.label(~Bd); edge = (set(lab[0]) | set(lab[-1]) | set(lab[:, 0]) | set(lab[:, -1])) - {0}
    body = np.zeros(LUM.shape, bool); body[y0:y1, x0:x1] = ~np.isin(lab, list(edge)); body &= ~(nd.binary_dilation(~body) & ~(LUM < 62))   # the whole figure, outlines kept
    pm = Image.new('L', (LUM.shape[1], LUM.shape[0]), 0); ImageDraw.Draw(pm).polygon([(x + RX, y + RY) for x, y in poly], fill=1); m = body & np.asarray(pm).astype(bool) & ~nd.binary_dilation(minus, iterations=1)
    lab2, _ = nd.label(m); m = lab2 == (np.bincount(lab2.ravel())[1:].argmax() + 1); ys, xs = np.nonzero(m); ox, oy = xs.min(), ys.min(); return cut(ox, oy, m[oy:ys.max() + 1, ox:xs.max() + 1]), (ox - M - RX, oy - M - RY)
IMG['arm_r'], ORIG_R = front_piece([(143, 180), (141, 214), (129, 244), (110, 260), (86, 274), (30, 244), (58, 208), (104, 186)], HMASK[0])   # his right arm (left of the picture)
IMG['arm_l'], ORIG_L = front_piece([(226, 186), (226, 262), (252, 266), (300, 270), (336, 250), (310, 212), (262, 192)], HMASK[1])
# fists for the fist moves: the sheet's loose fists on the SAME canvas as the open hand, wrist on the wrist (the two pictures swap)
FISTS = sorted([p for p in pieces((1030, 470, 1200, 566))], key=lambda p: p[0])
def on_canvas(base, pv, im, centre):
    cw, ch = base.size; c = Image.new('RGBA', (cw + 40, ch + 40), (0, 0, 0, 0)); c.alpha_composite(base, (20, 20)); f = Image.new('RGBA', c.size, (0, 0, 0, 0)); f.alpha_composite(im, (int(round(centre[0] + 20 - im.width / 2)), int(round(centre[1] + 20 - im.height / 2)))); return c, f, (pv[0] + 20, pv[1] + 20)
for sd, (hk, hpv), fp in (('r', ('hand_r', HPV_R), FISTS[0]), ('l', ('hand_l', HPV_L), FISTS[1])):
    a = np.asarray(IMG[hk])[..., 3] > 40; ys, xs = np.nonzero(a); cen = np.array([xs.mean(), ys.mean()]); d = cen - np.array(hpv); fist = cut(*fp)
    IMG[hk], IMG['fist_' + sd], newpv = on_canvas(IMG[hk], hpv, fist, np.array(hpv) + d * .75)
    if sd == 'r': HPV_R = newpv
    else: HPV_L = newpv
for k in ('arm_r', 'arm_l', 'hand_r', 'hand_l', 'fist_r', 'fist_l'): IMG[k].save(os.path.join(OUT, k + '.png'))
S = {k: im.size for k, im in IMG.items()}

# ---- LOOK LIKE BEFORE RIGGING (owner 2026-11-27 "ประกอบไม่ถูก มันไม่ชิด", "ประกอบเสร็จก็ลบเส้นออกด้วยสิ ทำให้เหมือนตอนยังไม่ต่อกระดูก"):
#      the box's torso, skirt, legs and sandals are drawn a little narrower than the front view, so their joints show lines the drawing does not have.
#      Each of them gets TWO layers on the same bone: on top the front view's own pixels of that part (every closed area of the front view goes to the piece
#      whose fitted box picture covers it most, outlines go with the areas they border), and under ALL top layers the fitted box picture, which fills
#      whatever opens when a part moves. At rest the hero is pixel for pixel the front view.
def fitted_mask(key, f, pv):
    al = np.asarray(IMG[key])[..., 3].astype(np.float32) / 255; c, s_ = np.cos(np.radians(f['r'])) * f['s'], np.sin(np.radians(f['r'])) * f['s']
    Mx = np.array([[c, -s_, f['at'][0] - (c * pv[0] - s_ * pv[1])], [s_, c, f['at'][1] - (s_ * pv[0] + c * pv[1])]], np.float32); return cv2.warpAffine(al, Mx, (REF.shape[1], REF.shape[0])) > .5
REFL = LUM[RY:RY + REF.shape[0], RX:RX + REF.shape[1]]; DARK = REFL < 62
fl_ = ~nd.binary_dilation(DARK); lab, n = nd.label(fl_); edge = (set(lab[0]) | set(lab[-1]) | set(lab[:, 0]) | set(lab[:, -1])) - {0}; BODY = ~np.isin(lab, list(edge)); BODY &= ~(nd.binary_dilation(~BODY) & ~DARK)
# the background of the front view is a dark brown gradient (dark like the outlines at the top corners): take it out by its own colour, row by row,
# from the picture's border, so no piece ever carries background (the head did: "a box round the head")
_bgrow = np.median(np.concatenate([REF[:, :14], REF[:, -14:]], 1).astype(np.float32), 1)[:, None, :]; _near = np.abs(REF.astype(np.float32) - _bgrow).sum(2) < 42
_lab, _n = nd.label(_near); _edge = (set(_lab[0]) | set(_lab[-1]) | set(_lab[:, 0]) | set(_lab[:, -1])) - {0}; _bg = np.isin(_lab, list(_edge)); _bg = nd.binary_opening(_bg, iterations=1)
BODY &= ~_bg; Image.fromarray((BODY * 255).astype(np.uint8)).save(os.path.join(OUT, 'ref_mask.png'))   # the figure of the reference, for the checks
TAKEN = np.zeros(BODY.shape, bool)
for k, orig in (('arm_r', ORIG_R), ('arm_l', ORIG_L)): a_ = np.asarray(IMG[k])[..., 3] > 40; ys, xs = np.nonzero(a_); TAKEN[ys + orig[1], xs + orig[0]] = True
for hm in HMASK: TAKEN |= hm[RY:RY + REF.shape[0], RX:RX + REF.shape[1]]
HEADM = fitted_mask('face0', F['head'], PV['head']); TAKEN |= BODY & (nd.binary_dilation(HEADM, iterations=8) | (np.arange(REF.shape[0])[:, None] < 178))   # the head stays the sheet's face picture (it swaps faces)
BOXK = ['torso', 'skirt', 'thigh_r', 'thigh_l', 'foot_r', 'foot_l']; FM = {k: nd.binary_dilation(fitted_mask(k, F[k], PV[k]), iterations=2) for k in BOXK}
inner = BODY & ~DARK & ~TAKEN; lab, n = nd.label(inner); OWN = {k: np.zeros(BODY.shape, bool) for k in BOXK}
for i in range(1, n + 1):
    m = lab == i; votes = [(FM[k] & m).sum() for k in BOXK]
    if max(votes) == 0: cy, cx = np.argwhere(m).mean(0); k = min(BOXK, key=lambda k: np.hypot(*(np.argwhere(FM[k]).mean(0) - [cy, cx])))
    else: k = BOXK[int(np.argmax(votes))]
    OWN[k] |= m
for k in BOXK:
    lab3, n3 = nd.label(nd.binary_dilation(OWN[k], iterations=3))   # stray specks out: keep the main area and what touches it
    if n3 > 1: big = np.bincount(lab3[OWN[k]].ravel(), minlength=n3 + 1); big[0] = 0; OWN[k] &= lab3 == big.argmax()
    OWN[k] |= DARK & BODY & ~TAKEN & nd.binary_dilation(OWN[k], iterations=4)   # the outlines it borders
CHEST = np.zeros(BODY.shape, bool); CHEST[172:262, 128:240] = True   # leftovers only count on the chest / neck, never round the hands or legs
COVER = HEADM.copy()   # whatever of the front view no piece shows (next to the neck, under the chin) goes to the torso layer, so no hole shows at rest
for k, orig in (('arm_r', ORIG_R), ('arm_l', ORIG_L)): a_ = np.asarray(IMG[k])[..., 3] > 40; ys, xs = np.nonzero(a_); COVER[ys + orig[1], xs + orig[0]] = True
for hm in HMASK: COVER |= hm[RY:RY + REF.shape[0], RX:RX + REF.shape[1]]
for k in BOXK: COVER |= OWN[k]
left = BODY & ~COVER; lab4, n4 = nd.label(left)
for i in range(1, n4 + 1):
    m = lab4 == i
    if (nd.binary_dilation(m, iterations=3) & (OWN['torso'] | COVER & ~HEADM)).any() and np.argwhere(m)[:, 0].mean() > 170: OWN['torso'] |= m & CHEST   # only next to the body, below the chin (hair specks stay out)
OWN['torso'] |= BODY & nd.binary_dilation(OWN['torso'], iterations=3) & ~nd.binary_dilation(HEADM, iterations=1) & CHEST & ~(TAKEN & DARK)   # a little over the soft cut edge of the arms (the torso is drawn above them), so no thin line shows
# under the arms: the torso the drawing never showed (the arms lie over it) is painted with the torso's own nearest skin / cloth colours, inside the
# box torso's shape, so a raised arm uncovers a clean body and no line (owner: "ลดรอยออก ทำให้เนียน")
ARMS = np.zeros(BODY.shape, bool)
for k, orig in (('arm_r', ORIG_R), ('arm_l', ORIG_L)): a_ = np.asarray(IMG[k])[..., 3] > 40; ys, xs = np.nonzero(a_); ARMS[ys + orig[1], xs + orig[0]] = True
for hm in HMASK: ARMS |= hm[RY:RY + REF.shape[0], RX:RX + REF.shape[1]]
UNDER = nd.binary_dilation(ARMS, iterations=3) & nd.binary_dilation(OWN['torso'] | fitted_mask('torso', F['torso'], PV['torso']), iterations=6) & CHEST & ~nd.binary_dilation(HEADM, iterations=2)
SRC = OWN['torso'] & ~DARK & (REFL > 120); _, (iy, ix) = nd.distance_transform_edt(~SRC, return_indices=True); FILL = REF.copy(); FILL[UNDER] = REF[iy[UNDER], ix[UNDER]]
FILL[UNDER] = nd.uniform_filter(FILL.astype(np.float32), size=(5, 5, 1))[UNDER]; CH = (UNDER | OWN['torso']); RIM = CH & ~nd.binary_erosion(CH, iterations=2) & ~nd.binary_dilation(OWN['torso'] & ~DARK, iterations=1); FILL[RIM & UNDER] = (24, 16, 12); print('  under the arms painted', int(UNDER.sum()), 'px')   # a hidden chest layer UNDER the arms (rest pose unchanged)
ys, xs = np.nonzero(CH); cy0, cy1, cx0, cx1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1; CHIM = Image.fromarray(np.dstack([FILL[cy0:cy1, cx0:cx1], CH[cy0:cy1, cx0:cx1] * 255]).astype(np.uint8), 'RGBA'); CHIM.save(os.path.join(OUT, 'u_chest.png'))
FVO = {}
for k in BOXK:
    m = OWN[k]; ys, xs = np.nonzero(m); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1; a_ = m[y0:y1, x0:x1].astype(np.float32)
    im = Image.fromarray(np.dstack([REF[y0:y1, x0:x1], a_ * 255]).astype(np.uint8), 'RGBA'); IMG['fv_' + k] = im; im.save(os.path.join(OUT, 'fv_' + k + '.png')); FVO[k] = (x0, y0); print('  front-view layer', k, im.size)
S = {k: im.size for k, im in IMG.items()}

# ---- the rig: the rest pose IS the owner's front view (arms and hands at their own places, the rest fitted); joints hidden under the torso / cuffs
SHO = {'r': (133, 205), 'l': (231, 209)}   # shoulder turning points (under the torso)
def placed(k, orig, pvw): return dict(pv=[round(pvw[0] - orig[0], 1), round(pvw[1] - orig[1], 1)], at=[pvw[0], pvw[1]], r=0, s=1)
A_R, A_L = placed('arm_r', ORIG_R, SHO['r']), placed('arm_l', ORIG_L, SHO['l']); H_R = dict(pv=list(HPV_R), at=[round(HAT_R[0], 1), round(HAT_R[1], 1)], r=0, s=1); H_L = dict(pv=list(HPV_L), at=[round(HAT_L[0], 1), round(HAT_L[1], 1)], r=0, s=1)
def part(img, n, role, fit_, p='', pv=None, **kw): q = dict(img=img + '.png', n=n, role=role, p=p, **kw); q.update(fit_); q['pv'] = [round(float(v), 1) for v in (pv if pv is not None else q['pv'])]; return q
PARTS = {
  'thigh_r': part('thigh_r', 'ขาขวา (ซ้ายของรูป)', 'legF', F['thigh_r'], 'torso', PV['thigh_r']), 'thigh_l': part('thigh_l', 'ขาซ้าย', 'legB', F['thigh_l'], 'torso', PV['thigh_l']),
  'foot_r': part('foot_r', 'เท้าขวา', 'shinF', F['foot_r'], 'thigh_r', PV['foot_r']), 'foot_l': part('foot_l', 'เท้าซ้าย', 'shinB', F['foot_l'], 'thigh_l', PV['foot_l']),
  'bolt': part('bolt', 'สายฟ้า', 'weapon', F['bolt'], 'hand_r', PV['bolt']),
  'hand_r': part('hand_r', 'มือขวา (ถืออาวุธ)', 'foreF', H_R, 'arm_r', g=.35), 'arm_r': part('arm_r', 'แขนขวา', 'armF', A_R, 'torso', g=.9),
  'hand_l': part('hand_l', 'มือซ้าย', 'foreB', H_L, 'arm_l', g=.35), 'arm_l': part('arm_l', 'แขนซ้าย', 'armB', A_L, 'torso', g=.9),
  'torso': part('torso', 'ลำตัว', 'body', F['torso'], '', PV['torso']), 'skirt': part('skirt', 'กระโปรง', 'none', F['skirt'], 'torso', PV['skirt']), 'head': part('face0', 'หัว', 'head', F['head'], 'torso', PV['head']),
}
FIST = ('attack', 'shoot', 'cast', 'cheer', 'throw')   # moves that clench the fists
SW = {'head': dict(idle='face0', throw='face1', attack='face1', shoot='face1', cast='face2', hit='face4', die='face3', spawn='face0', cheer='face3')}
for sd in 'rl': SW['hand_' + sd] = {mv: 'fist_' + sd for mv in FIST} | dict(idle='hand_' + sd)
for k in BOXK:   # the front-view layer on top, the fitted box picture as its filler underneath (same bone)
    q = PARTS[k]; pvw = q['at']; ox, oy = FVO[k]; PARTS['u_' + k] = dict(q, n=q['n'] + ' (ชั้นรอง)', role='none', p=k)
    PARTS[k] = dict(q, img='fv_' + k + '.png', pv=[round(pvw[0] - ox, 1), round(pvw[1] - oy, 1)], at=pvw, r=0, s=1)
hq = PARTS['head']; c_, s_ = np.cos(np.radians(hq['r'])) * hq['s'], np.sin(np.radians(hq['r'])) * hq['s']; fw, fh = IMG['face0'].size
yy, xx = np.mgrid[0:fh, 0:fw].astype(np.float32); X = c_ * (xx - hq['pv'][0]) - s_ * (yy - hq['pv'][1]) + hq['at'][0]; Yv = s_ * (xx - hq['pv'][0]) + c_ * (yy - hq['pv'][1]) + hq['at'][1]
HEADFV = BODY & (nd.binary_dilation(HEADM, iterations=6) | (np.arange(REF.shape[0])[:, None] < 176)) & ~ARMS & (np.arange(REF.shape[0])[:, None] < 196) & ~CHEST | (BODY & HEADM & ~ARMS & (np.arange(REF.shape[0])[:, None] < 190))
lab5, n5 = nd.label(HEADFV); HEADFV = lab5 == (np.bincount(lab5.ravel())[1:].argmax() + 1)
X = X.astype(np.float32); Yv = Yv.astype(np.float32); rgbH = np.dstack([cv2.remap(REF[..., i].astype(np.float32), X, Yv, cv2.INTER_LINEAR) for i in range(3)]); aH = cv2.remap(HEADFV.astype(np.float32), X, Yv, cv2.INTER_LINEAR)
aH *= nd.binary_dilation(np.asarray(IMG['face0'])[..., 3] > 40, iterations=3)   # 2026-11-28: the junky mask let background blobs round the hair in (a brown box round the head); keep only the head's own outline + 3 px
Image.fromarray(np.dstack([rgbH, aH * 255]).clip(0, 255).astype(np.uint8), 'RGBA').save(os.path.join(OUT, 'face_fv.png')); PARTS['head']['img'] = 'face_fv.png'; SW['head']['idle'] = 'face_fv'
# under the skirt: the dark inside of the skirt between the thighs, hidden at rest, planted like the legs (a squashed body never opens a gap there)
sk = OWN['skirt']; sy_ = np.nonzero(sk.any(1))[0]; hem = int(np.percentile(np.nonzero(sk)[0], 97)); legs = OWN['thigh_r'] | OWN['thigh_l']
zone = np.zeros(BODY.shape, bool); zone[hem - 30:hem + 4, :] = True; hull = np.zeros(BODY.shape, np.uint8); pts = np.argwhere(legs & zone)[:, ::-1].astype(np.int32); cv2.fillConvexPoly(hull, cv2.convexHull(pts), 1)   # between the thighs only, never wider than the legs
HIP = hull.astype(bool) & zone & nd.binary_erosion(nd.binary_fill_holes(sk | legs), iterations=2); gray = REF[sk & (REFL > 90) & (REFL < 190) & (np.abs(REF[..., 0].astype(int) - REF[..., 2]) < 25)]
col = np.median(gray, 0) if len(gray) else np.array([150, 150, 160]); ys, xs = np.nonzero(HIP); hy0, hx0 = ys.min(), xs.min(); hip = np.zeros((ys.max() - hy0 + 1, xs.max() - hx0 + 1, 4), np.uint8); hip[ys - hy0, xs - hx0, :3] = col * .8; hip[ys - hy0, xs - hx0, 3] = 255
Image.fromarray(hip, 'RGBA').save(os.path.join(OUT, 'u_hips.png'))
PARTS['u_hips'] = dict(img='u_hips.png', n='ใต้กระโปรง (ชั้นรอง)', role='none', p='skirt', pv=[round(PARTS['torso']['at'][0] - hx0, 1), round(PARTS['torso']['at'][1] - hy0, 1)], at=PARTS['torso']['at'], r=0, s=1)
PARTS['u_chest'] = dict(img='u_chest.png', n='อกใต้แขน (ชั้นรอง)', role='none', p='torso', pv=[round(PARTS['torso']['at'][0] - cx0, 1), round(PARTS['torso']['at'][1] - cy0, 1)], at=PARTS['torso']['at'], r=0, s=1)
ORDER = ['u_hips', 'u_torso', 'u_chest', 'u_thigh_r', 'u_thigh_l', 'u_foot_r', 'u_foot_l', 'u_skirt',   # fillers first: at rest nothing of them shows
         'thigh_r', 'thigh_l', 'foot_r', 'foot_l', 'bolt', 'hand_r', 'arm_r', 'hand_l', 'arm_l', 'torso', 'skirt', 'head']   # hands under the cuffs, arms under the torso
CLIPS = {'throw2': dict(dir='throw/', frames=[f't{i:02d}.png' for i in range(16)], durs=[80, 90, 80, 80, 90, 80, 80, 90, 80, 80, 90, 80, 80, 90, 80, 80], foot=[188, 463], figH=311, ev=[[.56, 'release']], release=[400, 303], dirx=1, boltScale=.5, n='ปาสายฟ้า')}   # the owner's GPT throw (art/incoming/zeus_sheet/gpt_throw_reference.gif split into art/rigs/zeusgpt/throw/), drawn frames
rig = dict(v=2, name='zeusgpt', title='ซุส (จากแผ่นของคุณ)', dir='art/rigs/zeusgpt/', ref='ref.png', size=[380, 426], feet=[182, 418], view='front', flip=True, figH=410, refMask='ref_mask.png', parts=PARTS, order=ORDER, swaps=SW, clips=CLIPS)
json.dump(rig, open(os.path.join(R, 'art/rigs/zeusgpt.json'), 'w'), ensure_ascii=False, indent=1); print('art/rigs/zeusgpt.json', len(PARTS), 'pieces')
