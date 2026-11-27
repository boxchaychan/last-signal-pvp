"""The owner's own Zeus sheet (GPT, 2026-11-27: art/incoming/zeus_sheet/owner_sheet_raw.png) cut into the pieces of a rig, WITHOUT redrawing anything
(owner: a GPT redraw changed his build, "ฉันต้องการคงเดิมไว้"). Every pixel is the sheet's own.
  - the pieces box (top right): torso, skirt, 2 upper arms, 2 forearms with fists, 2 thighs, 2 feet -> dark-outline flood from the box border;
  - the 6 faces row: 6 whole heads on ONE canvas size, chins lined up, so a move can swap the face;
  - the bolt (no dark outline): by colour;
  - the front view (top left) = the faint reference picture and the rig's own space (380 x 426, feet at 182, 418).
-> art/rigs/zeusgpt/*.png + art/rigs/zeusgpt.json (rig.html?char=zeusgpt, rig2d/bones.js).     pip install pillow numpy scipy ; python3 tools/art/zeus_sheet_cut.py"""
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
for k, im in IMG.items(): im.save(os.path.join(OUT, k + '.png'))
ref = Image.fromarray(A[6:432, 20:400].astype(np.uint8), 'RGB'); ref.save(os.path.join(OUT, 'ref.png'))
S = {k: im.size for k, im in IMG.items()}; print({k: v for k, v in S.items()})

# ---- the rig: every piece placed on the front view (its space), arms hanging like the first pose of the owner's attack row
def part(img, n, role, pv, at_, s=1, r=0, p='', **kw): return dict(img=img + '.png', n=n, role=role, pv=pv, at=at_, s=s, r=r, p=p, **kw)
w = lambda k: S[k][0]; h = lambda k: S[k][1]
PARTS = {   # the rest pose = the owner's front view: arms out to the sides, feet apart
  'thigh_r': part('thigh_r', 'ขาขวา (ซ้ายของรูป)', 'legF', [w('thigh_r') / 2, 9], [145, 318], .92, 0, 'torso'), 'thigh_l': part('thigh_l', 'ขาซ้าย', 'legB', [w('thigh_l') / 2, 9], [219, 318], .92, 0, 'torso'),
  'foot_r': part('foot_r', 'เท้าขวา', 'shinF', [w('foot_r') - 23, 10], [141, 364], .98, 0, 'thigh_r'), 'foot_l': part('foot_l', 'เท้าซ้าย', 'shinB', [23, 10], [222, 364], .98, 0, 'thigh_l'),
  'bolt': part('bolt', 'สายฟ้า', 'weapon', [w('bolt') / 2, h('bolt') * .55], [60, 272], .62, 6, 'fore_r'),
  'fore_r': part('fore_r', 'แขนล่าง + มือ ขวา (ถืออาวุธ)', 'foreF', [17, 15], [107, 231], .95, 85, 'uarm_r', g=.3), 'uarm_r': part('uarm_r', 'แขนบน ขวา', 'armF', [w('uarm_r') - 17, 15], [141, 207], .95, 16, 'torso', g=.9),
  'fore_l': part('fore_l', 'แขนล่าง + มือ ซ้าย', 'foreB', [w('fore_l') - 17, 15], [256, 231], .95, -85, 'uarm_l', g=.3), 'uarm_l': part('uarm_l', 'แขนบน ซ้าย', 'armB', [17, 15], [222, 207], .95, -16, 'torso', g=.9),
  'torso': part('torso', 'ลำตัว', 'body', [w('torso') / 2, h('torso') - 9], [181, 270], .93, 0, ''),
  'skirt': part('skirt', 'กระโปรง', 'cape', [w('skirt') / 2, 12], [181, 268], 1.03, 0, 'torso', g=.35),
  'head': part('face0', 'หัว', 'head', [w('face0') / 2, h('face0') - 12], [179, 176], 1.47, 0, 'torso'),
}
rig = dict(v=2, name='zeusgpt', title='ซุส (จากแผ่นของคุณ)', dir='art/rigs/zeusgpt/', ref='ref.png', size=[380, 426], feet=[182, 418], view='front', flip=True, parts=PARTS, order=list(PARTS),
           faces=dict(part='head', idle='face0', attack='face1', shoot='face1', cast='face2', hit='face4', die='face3', spawn='face0', cheer='face3'))   # which face picture the head shows during a move
json.dump(rig, open(os.path.join(R, 'art/rigs/zeusgpt.json'), 'w'), ensure_ascii=False, indent=1); print('art/rigs/zeusgpt.json', len(PARTS), 'pieces')
