"""A character sheet on a flat GREEN screen (an assembled front view + the same character as separate pieces) -> a rig for rig.html / rig2d/bones.js.
Nothing is redrawn: every pixel is the sheet's own. First used for the owner's Poseidon sheet (2026-11-28, "ใช้ทูลทำท่าโจมตีให้ดู ใช้ทูลนะ").
  1. green taken out (soft edge, green spill removed), pieces found as separate islands;
  2. each piece placed on the assembled front view by a masked match (turn / size / place, searched in its own area of the picture);
  3. the rig: roles, parents, turning points, back-to-front order, the front view as the reference + its figure mask.
  The tool then refines the places (rig.html "จัดทุกชิ้น" = Bones2D.autofit) and checks them (tools/qa/rig_check.js).
  python3 tools/art/rig_from_sheet.py poseidon      (pip install pillow numpy scipy opencv-python-headless)"""
import json, os, sys
import numpy as np, cv2
from PIL import Image
from scipy import ndimage as nd
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
# per character: the sheet, which island is which piece (by a point inside it), roles, parents, turning points (as a share of the piece box: 0..1), search area in the front view
CHARS = {
  'poseidon': dict(sheet='art/incoming/poseidon/owner_sheet_raw.png', title='โพไซดอน (จากแผ่นของคุณ)', front=(240, 520), flip=True,
    parts=dict(   # name: (point inside on the sheet, role, parent, turning point (fx, fy) of the piece box, Thai, search box in the front view (x0, y0, x1, y1) as shares, turn range)
      cape=((1370, 200), 'cape', 'torso', (.5, .06), 'ผ้าคลุม', (.1, .35, .9, .85), 12),
      thigh_r=((538, 780), 'legF', 'torso', (.5, .08), 'ต้นขาขวา', (.2, .65, .55, .95), 15), thigh_l=((656, 780), 'legB', 'torso', (.5, .08), 'ต้นขาซ้าย', (.45, .65, .8, .95), 15),
      shin_r=((779, 800), 'shinF', 'thigh_r', (.5, .1), 'แข้งขวา', (.2, .7, .55, 1), 15), shin_l=((885, 800), 'shinB', 'thigh_l', (.5, .1), 'แข้งซ้าย', (.45, .7, .8, 1), 15),
      foot_r=((1018, 830), 'none', 'shin_r', (.5, .15), 'เท้าขวา', (.15, .8, .55, 1), 10), foot_l=((1180, 830), 'none', 'shin_l', (.5, .15), 'เท้าซ้าย', (.45, .8, .85, 1), 10),
      skirt=((1113, 300), 'none', 'torso', (.5, .1), 'กระโปรง', (.2, .5, .8, .85), 8),
      torso=((888, 280), 'body', '', (.5, .92), 'ลำตัว', (.2, .35, .8, .75), 8),
      trident=((1384, 800), 'weapon', 'fist_r', (.5, .62), 'สามง่าม', None, 0),
      uarm_r=((537, 530), 'armF', 'torso', (.5, .12), 'แขนบนขวา', (0, .38, .45, .75), 50), uarm_l=((661, 530), 'armB', 'torso', (.5, .12), 'แขนบนซ้าย', (.55, .38, 1, .75), 50),
      fore_r=((786, 540), 'foreF', 'uarm_r', (.5, .14), 'แขนล่างขวา', (0, .45, .45, .8), 50), fore_l=((900, 540), 'foreB', 'uarm_l', (.5, .14), 'แขนล่างซ้าย', (.55, .45, 1, .8), 50),
      fist_r=((1040, 540), 'none', 'fore_r', (.5, .25), 'มือขวา', (0, .55, .4, .9), 50), fist_l=((1176, 540), 'none', 'fore_l', (.5, .25), 'มือซ้าย', (.6, .55, 1, .9), 50),
      head=((622, 250), 'head', 'torso', (.5, .9), 'หัว', (.15, 0, .85, .55), 8)),
    order=['cape', 'trident', 'thigh_r', 'thigh_l', 'shin_r', 'shin_l', 'foot_r', 'foot_l', 'skirt', 'uarm_r', 'uarm_l', 'torso', 'fist_r', 'fore_r', 'fist_l', 'fore_l', 'head'],
    front_box=(14, 160, 464, 895)),
}
name = sys.argv[1] if len(sys.argv) > 1 else 'poseidon'; C = CHARS[name]; OUT = os.path.join(R, 'art/rigs', name); os.makedirs(OUT, exist_ok=True)
A = np.asarray(Image.open(os.path.join(R, C['sheet'])).convert('RGB')).astype(np.float32); r, g, b = A[..., 0], A[..., 1], A[..., 2]
greenness = g - np.maximum(r, b); BG = (greenness > 60) & (g > 150); FG = nd.binary_opening(~BG, iterations=1); LAB, _ = nd.label(FG)
def rgba(mask, box):
    """the piece as RGBA: soft edge from how green the edge pixel is, green spill on the edge pulled back to the neighbours' colour"""
    x0, y0, x1, y1 = box; m = mask[y0:y1, x0:x1]; a = A[y0:y1, x0:x1].copy(); gr = greenness[y0:y1, x0:x1]
    edge = m & ~nd.binary_erosion(m, iterations=2); al = m.astype(np.float32); al[edge] = np.clip(1 - (gr[edge] - 10) / 90, 0, 1)
    sp = edge & (gr > 0); a[..., 1][sp] = np.maximum(a[..., 0], a[..., 2])[sp] * 1.0   # no green halo
    return Image.fromarray(np.dstack([a, al * 255]).clip(0, 255).astype(np.uint8), 'RGBA')
# the front view = the reference and the rig's space
fx0, fy0, fx1, fy1 = C['front_box']; fid = LAB[C['front'][1], C['front'][0]]; FM = (LAB == fid)
REFIMG = rgba(FM, C['front_box']); W, H = REFIMG.size; REFIMG.save(os.path.join(OUT, 'ref.png')); Image.fromarray((FM[fy0:fy1, fx0:fx1] * 255).astype(np.uint8)).save(os.path.join(OUT, 'ref_mask.png'))
REF = np.asarray(REFIMG).astype(np.float32); REFM = REF[..., 3] > 128; ys, xs = np.nonzero(REFM); FEET = [float(xs[ys > ys.max() - 8].mean()), float(ys.max())]
IMG, PV = {}, {}
for k, (pt, role, par, pv, n, area, tr) in C['parts'].items():
    i = LAB[pt[1], pt[0]]; assert i and i != fid, (k, 'no piece at', pt); m = LAB == i; yy, xx = np.nonzero(m); box = (xx.min() - 3, yy.min() - 3, xx.max() + 4, yy.max() + 4)
    IMG[k] = rgba(m, box); IMG[k].save(os.path.join(OUT, k + '.png')); w, h = IMG[k].size; PV[k] = [round(pv[0] * w, 1), round(pv[1] * h, 1)]
# masked match of each piece on the front view (coarse then fine), inside its own search area
REFB = cv2.GaussianBlur(REF[..., :3], (0, 0), 1.0)
def fit(k, area, tr):
    im = np.asarray(IMG[k]).astype(np.float32); rgb, al = im[..., :3], im[..., 3] / 255; pv = PV[k]; best = None; X0, Y0, X1, Y1 = int(area[0] * W), int(area[1] * H), int(area[2] * W), int(area[3] * H)
    def one(a, s):
        h, w = al.shape; M = cv2.getRotationMatrix2D((float(pv[0]), float(pv[1])), -a, s); cs = np.array([[0, 0, 1], [w, 0, 1], [0, h, 1], [w, h, 1]], np.float32) @ M.T; mn = np.floor(cs.min(0)) - 1; mx = np.ceil(cs.max(0)) + 1
        M[:, 2] -= mn; W2, H2 = int(mx[0] - mn[0]), int(mx[1] - mn[1]); t = cv2.warpAffine(rgb, M, (W2, H2)); mk = (cv2.warpAffine(al, M, (W2, H2)) > .6).astype(np.float32)
        reg = REFB[Y0:Y1, X0:X1]
        if reg.shape[0] <= H2 or reg.shape[1] <= W2: return None
        rr = cv2.matchTemplate(np.ascontiguousarray(reg), np.ascontiguousarray(t), cv2.TM_SQDIFF, mask=np.dstack([mk, mk, mk])) / max(1, mk.sum()); v, _, loc, _ = cv2.minMaxLoc(rr); px, py = M @ np.array([pv[0], pv[1], 1], np.float32)
        return v, a, s, (X0 + loc[0] + px, Y0 + loc[1] + py)
    for a in np.arange(-tr, tr + .1, max(3, tr / 6)):
        for s in (np.arange(.75, 1.46, .05) if k == 'cape' else np.arange(.85, 1.16, .05)):
            o = one(a, s)
            if o and (best is None or o[0] < best[0]): best = o
    v, a0, s0, _ = best
    for a in np.arange(a0 - 4, a0 + 4.1, 1):
        for s in np.arange(s0 - .04, s0 + .041, .01):
            o = one(a, s)
            if o and o[0] < best[0]: best = o
    v, a, s, (x, y) = best; print(f'  {k:8s} turn {a:6.1f} size {s:4.2f} at ({x:6.1f},{y:6.1f}) error {v ** .5 / 2.55:5.1f}'); return dict(at=[round(float(x), 1), round(float(y), 1)], r=round(float(a), 1), s=round(float(s), 3))
F = {}
for k, (pt, role, par, pv, n, area, tr) in C['parts'].items():
    if area: F[k] = fit(k, area, tr)
# the weapon: not in the front view, held upright in the weapon hand (its grip on the fist's middle)
fk = 'fist_r'; f = F[fk]; fw, fh = IMG[fk].size; c, s_ = np.cos(np.radians(f['r'])) * f['s'], np.sin(np.radians(f['r'])) * f['s']; lx, ly = fw / 2 - PV[fk][0], fh * .5 - PV[fk][1]
F['trident'] = dict(at=[round(f['at'][0] + c * lx - s_ * ly, 1), round(f['at'][1] + s_ * lx + c * ly, 1)], r=0, s=round(f['s'], 3))
# ---- NO JOINT LINES (the Zeus recipe, made general): every closed area of the front view goes to the piece whose fitted picture covers it most,
#      outlines go with the areas they border. Each piece = its front-view pixels on top ("fv_") and its own sheet picture, moved onto the front view,
#      hidden underneath ("u_") on the same canvas and bone, which fills whatever opens when it moves. Hands: the open hand of the front view at rest,
#      the sheet's fist (same canvas) in the fist moves.
def warped(k):
    im = np.asarray(IMG[k]).astype(np.float32); f = F[k]; pv = PV[k]; c, s_ = np.cos(np.radians(f['r'])) * f['s'], np.sin(np.radians(f['r'])) * f['s']
    M = np.array([[c, -s_, f['at'][0] - (c * pv[0] - s_ * pv[1])], [s_, c, f['at'][1] - (s_ * pv[0] + c * pv[1])]], np.float32); return cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_LINEAR)
WP = {k: warped(k) for k in F if k != 'trident'}; KEYS = list(WP)
L = REF[..., :3] @ np.array([.299, .587, .114], np.float32); DARK = (L < 70) & REFM
inner = REFM & ~DARK; lab, n = nd.label(inner); OWN = {k: np.zeros(REFM.shape, bool) for k in KEYS}; VOTE = {k: nd.binary_dilation(WP[k][..., 3] > 128, iterations=2) for k in KEYS}
pri = {k: C['order'].index(k) for k in KEYS}   # a tie goes to the piece drawn in front
for i in range(1, n + 1):
    m = lab == i; v = {k: (VOTE[k] & m).sum() for k in KEYS}; best = max(KEYS, key=lambda k: (v[k], pri[k]))
    if v[best] == 0: cy, cx = np.argwhere(m).mean(0); best = min(KEYS, key=lambda k: np.hypot(*(np.argwhere(VOTE[k]).mean(0) - [cy, cx])) if VOTE[k].any() else 1e9)
    OWN[best] |= m
ANY = np.zeros(REFM.shape, bool)
for k in KEYS: ANY |= OWN[k]
_, (iy, ix) = nd.distance_transform_edt(~ANY, return_indices=True); owner = np.full(REFM.shape, -1); 
for j, k in enumerate(KEYS): owner[OWN[k]] = j
NEAR = owner[iy, ix]   # every outline / dark pixel (brows, beard lines, eyes) goes to the piece of the nearest coloured area ...
for j, k in enumerate(KEYS): OWN[k] |= (DARK & (NEAR == j)) | (DARK & nd.binary_dilation(OWN[k], iterations=4))   # ... and joint outlines to both sides
LEFT = REFM & ~ANY & ~DARK
for j, k in enumerate(KEYS): OWN[k] |= LEFT & (NEAR == j)
CAN = {}
for k in KEYS:
    um = WP[k][..., 3] > 10; allm = um | OWN[k]; ys_, xs_ = np.nonzero(allm); x0, y0, x1, y1 = max(0, xs_.min() - 2), max(0, ys_.min() - 2), xs_.max() + 3, ys_.max() + 3
    Image.fromarray(np.dstack([REF[y0:y1, x0:x1, :3], OWN[k][y0:y1, x0:x1] * 255]).astype(np.uint8), 'RGBA').save(os.path.join(OUT, 'fv_' + k + '.png'))
    u = WP[k][y0:y1, x0:x1].copy(); u[..., 3] *= nd.binary_dilation(REFM, iterations=1)[y0:y1, x0:x1]   # the filler never shows past the figure's outline at rest
    Image.fromarray(u.clip(0, 255).astype(np.uint8), 'RGBA').save(os.path.join(OUT, 'u_' + k + '.png')); CAN[k] = (x0, y0)
PARTS = {}
for k, (pt, role, par, pv, n_, area, tr) in C['parts'].items():
    if k == 'trident': PARTS[k] = dict(img=k + '.png', n=n_, role=role, p=par, pv=PV[k], **F[k]); continue
    x0, y0 = CAN[k]; at = F[k]['at']; q = dict(img='fv_' + k + '.png', n=n_, role=role, p=par, pv=[round(at[0] - x0, 1), round(at[1] - y0, 1)], at=at, r=0, s=1); PARTS[k] = q
    if not k.startswith('fist'): PARTS['u_' + k] = dict(q, img='u_' + k + '.png', n=n_ + ' (ชั้นรอง)', role='none', p=k)
for k in ('uarm_r', 'uarm_l', 'fore_r', 'fore_l'): PARTS[k]['g'] = .9
PARTS['cape']['g'] = .5
FIST = ('attack', 'shoot', 'cast', 'cheer', 'throw', 'thrust')
SW = {f'fist_{sd}': {**{mv: f'u_fist_{sd}' for mv in FIST}, 'idle': f'fv_fist_{sd}'} for sd in 'rl'}
ORDER = ['u_' + k for k in C['order'] if 'u_' + k in PARTS] + C['order']
rig = dict(v=2, name=name, title=C['title'], dir=f'art/rigs/{name}/', ref='ref.png', refMask='ref_mask.png', size=[W, H], feet=[round(FEET[0], 1), round(FEET[1], 1)], view='front', flip=C['flip'], figH=round(float(ys.max() - ys.min()), 1), parts=PARTS, order=ORDER, swaps=SW, checks=dict(throw=False))   # the bolt-throw test is for a bolt, not a trident
json.dump(rig, open(os.path.join(R, f'art/rigs/{name}.json'), 'w'), ensure_ascii=False, indent=1); print(f'art/rigs/{name}.json', len(PARTS), 'pieces', 'size', W, H)
