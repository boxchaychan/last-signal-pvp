"""ONE front-view picture of a character (on a flat background) cut into rig pieces by hand-set regions, nothing redrawn
(owner 2026-11-28 on Apollo: "ให้ใช้ทูลทำนะ ไม่ใช่เอาเฟรมมาต่อ" = make the move with the tool's bones, not by joining drawn frames).
  - background out by its colour from the border (soft edge);
  - every figure pixel goes to the region (polygon) it lies in, the rest to the nearest region; outlines stay with the pixels they belong to;
  - each piece is UNDER-PAINTED a little way past its cut with its own nearest colours, so a joint that opens in a move shows the piece, not a hole;
  - the weapon (and its arrow) come from elsewhere on the sheet, scaled to the figure.
  python3 tools/art/rig_from_front.py apollo"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
CHARS = {
  'apollo': dict(sheet='art/incoming/apollo/owner_sheet_raw.png', title='อพอลโล (จากแผ่นของคุณ)', box=(560, 14, 730, 300), K=2, flip=False,
    # regions in SHEET pixels: name: (role, parent, turning point, polygon[, capsule]). His left hand (right of the picture) holds the bow, the right one draws.
    # capsule = (shoulder, fist, radius): the WHOLE limb along that line is the limb's (2026-11-28: the polygons gave the upper-arm muscle to the torso,
    # so a lifted arm left its own shoulder behind = a torn armpit). Two points + a thickness, easier to set than a polygon and it follows the limb.
    parts=dict(
      leg_r=('legB', 'torso', (627, 240), [(606, 236), (646, 236), (646, 300), (606, 300)]),
      leg_l=('legF', 'torso', (676, 240), [(656, 236), (705, 236), (705, 300), (656, 300)]),
      skirt=('none', 'torso', (646, 212), [(596, 210), (712, 210), (712, 262), (596, 262), (596, 236), (606, 236), (646, 236), (656, 236), (705, 236), (712, 236)]),
      torso=('body', '', (646, 230), [(612, 136), (682, 136), (684, 212), (608, 212)]),
      arm_r=('armB', 'torso', (619, 150), [(592, 140), (613, 140), (613, 212), (592, 212)], ((618, 151), (604, 202), 9.5)),
      arm_l=('armF', 'torso', (680, 150), [(682, 140), (706, 140), (706, 212), (682, 212)], ((680, 151), (695, 202), 9.5)),
      head=('head', 'torso', (646, 138), [(560, 14), (730, 14), (730, 140), (682, 140), (612, 140), (560, 140)])),
    order=['leg_r', 'leg_l', 'arm_r', 'skirt', 'torso', 'bow', 'arm_l', 'head'],
    weapon=dict(name='bow', box=(1462, 126, 1504, 296), role='weapon', parent='arm_l', hold=(698, 198), height=.62, r=0),
    arrow=dict(box=(1434, 192, 1454, 294)),
    hold_frac=.5),
}
name = sys.argv[1] if len(sys.argv) > 1 else 'apollo'; C = CHARS[name]; OUT = os.path.join(R, 'art/rigs', name); os.makedirs(OUT, exist_ok=True); K = C['K']
SH = Image.open(os.path.join(R, C['sheet'])).convert('RGB'); x0, y0, x1, y1 = C['box']
def cutbg(box, k):
    """a box of the sheet, enlarged k times, its flat background taken out (colour distance from the border colours, reached from the border)"""
    im = SH.crop(box).resize(((box[2] - box[0]) * k, (box[3] - box[1]) * k), Image.LANCZOS); a = np.asarray(im).astype(np.float32); bd = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]]); bg = np.median(bd, 0)
    d = np.abs(a - bg).sum(2); near = d < 60; lab, _ = nd.label(near); edge = (set(lab[0]) | set(lab[-1]) | set(lab[:, 0]) | set(lab[:, -1])) - {0}; out = np.isin(lab, list(edge)); fig = ~out
    fig = nd.binary_opening(fig, iterations=1); lab2, n2 = nd.label(fig); fig = lab2 == (np.bincount(lab2.ravel())[1:].argmax() + 1) if n2 else fig; fig = nd.binary_fill_holes(fig)
    al = fig.astype(np.float32); rim = fig & ~nd.binary_erosion(fig, iterations=1); al[rim] = np.clip((d[rim] - 20) / 70, .2, 1); return a, fig, al
A, FIG, AL = cutbg(C['box'], K); H, W = FIG.shape
Image.fromarray(np.dstack([A, AL * 255]).astype(np.uint8), 'RGBA').save(os.path.join(OUT, 'ref.png')); Image.fromarray((FIG * 255).astype(np.uint8)).save(os.path.join(OUT, 'ref_mask.png'))
S2 = lambda p: ((p[0] - x0) * K, (p[1] - y0) * K)
keys = [k for k in C['parts']]; owner = np.full((H, W), -1)
for j, k in enumerate(keys):   # later regions win (head over arms over torso ...)
    pm = Image.new('L', (W, H), 0); ImageDraw.Draw(pm).polygon([S2(p) for p in C['parts'][k][3]], fill=1); owner[(np.asarray(pm) > 0) & FIG] = j
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
for j, k in enumerate(keys):   # limbs given as a capsule take every figure pixel along their line (after the polygons, before nothing else)
    cap = C['parts'][k][4] if len(C['parts'][k]) > 4 else None
    if not cap: continue
    (ax, ay), (bx, by) = S2(cap[0]), S2(cap[1]); r = cap[2] * K; vx, vy = bx - ax, by - ay; t = np.clip(((XX - ax) * vx + (YY - ay) * vy) / (vx * vx + vy * vy), 0, 1)
    d = np.hypot(XX - ax - vx * t, YY - ay - vy * t); owner[(d <= r) & FIG & (owner != keys.index('head'))] = j
miss = FIG & (owner < 0); _, (iy, ix) = nd.distance_transform_edt(owner < 0, return_indices=True); owner[miss] = owner[iy[miss], ix[miss]]
PARTS = {}; UNDER = 14 * K // 2
for j, k in enumerate(keys):
    role, par, tp = C['parts'][k][:3]; own = owner == j
    # under-paint ONLY into the area of pieces drawn ABOVE this one (hidden there at rest; under a piece drawn below it would cover that piece and leave
    # a ghost of it when it moves). (A full-depth fill under the arms was tried 2026-11-28: brown streaks where the background should show; shallow is better.)
    above = np.isin(owner, [j2 for j2, k2 in enumerate(keys) if k2 in C['order'] and C['order'].index(k2) > C['order'].index(k)]) if k in C['order'] else np.zeros_like(own)
    deep = role in ('body', 'none'); zone = nd.binary_dilation(own, iterations=UNDER * (2 if role == 'body' else 1)) & FIG & ~own & above if k not in ('head',) else np.zeros_like(own)
    edge = np.zeros_like(own)
    if deep:   # OUTLINE CONTINUED (2026-11-28 "รักแร้ก็ขาด"): where an arm hides the body's side, the side is not in the picture. Rows where the body's edge
        # meets the background are known; rows where it meets a piece drawn above are not: the edge there is joined straight from the known rows above
        # and below, the under-paint stops at it, and its last pixels get the outline colour, so a lifted arm shows the body's own side, not a strip.
        ys_, = np.nonzero(own.any(1)); y0_, y1_ = ys_.min(), ys_.max(); allow = np.zeros_like(own); outl = A[own & ~nd.binary_erosion(own, iterations=2)]
        oc = np.median(outl[outl.sum(1) < np.percentile(outl.sum(1), 25)], 0) if len(outl) else np.array([40, 30, 30])
        for side in (0, 1):
            ext = np.full(H, np.nan); known = np.zeros(H, bool)
            for y in range(y0_, y1_ + 1):
                xs_ = np.nonzero(own[y])[0]
                if not len(xs_): continue
                x = xs_.max() if side else xs_.min(); nx = x + (1 if side else -1); ext[y] = x
                known[y] = not (0 <= nx < W) or not FIG[y, nx] or not above[y, nx]   # the edge meets the background (or something below) = real
            ky = np.nonzero(known)[0]
            if len(ky) < 2: continue
            est = np.interp(np.arange(H), ky, ext[ky])
            for y in range(y0_, y1_ + 1):
                if known[y] or np.isnan(ext[y]): continue
                a, b = sorted((ext[y], est[y])); allow[y, int(a):int(b) + 1] = True
                xe = int(round(est[y])); edge[y, max(0, xe - 1):min(W, xe + 2)] = True
        lateral = np.zeros_like(own)   # beside the body in its own rows: only there is the under-paint held to the continued outline
        for y in range(y0_, y1_ + 1):
            xs_ = np.nonzero(own[y])[0]
            if len(xs_): lateral[y, :xs_.min()] = True; lateral[y, xs_.max() + 1:] = True
        zone &= ~(lateral & ~allow); edge &= zone
    src = own & (np.asarray(SH.crop(C['box']).resize((W, H)).convert('L')) > 70); _, (jy, jx) = nd.distance_transform_edt(~src, return_indices=True)
    rgb = A.copy(); rgb[zone] = A[jy[zone], jx[zone]]; rgb[edge] = oc if deep else rgb[edge]; m = own | zone; ys, xs = np.nonzero(m); bx0, by0, bx1, by1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    alpha = np.where(own, AL, np.where(zone, 1, 0)); Image.fromarray(np.dstack([rgb[by0:by1, bx0:bx1], alpha[by0:by1, bx0:bx1] * 255]).astype(np.uint8), 'RGBA').save(os.path.join(OUT, k + '.png'))
    t = S2(tp); PARTS[k] = dict(img=k + '.png', n=k, role=role, p=par, pv=[round(t[0] - bx0, 1), round(t[1] - by0, 1)], at=[round(t[0], 1), round(t[1], 1)], r=0, s=1)
NAMES = dict(head='หัว', torso='ลำตัว', skirt='ผ้านุ่ง', arm_r='แขนขวา (ดึงสาย)', arm_l='แขนซ้าย (ถือธนู)', leg_r='ขาขวา', leg_l='ขาซ้าย')
for k in PARTS: PARTS[k]['n'] = NAMES.get(k, k)
for k in ('arm_r', 'arm_l'): PARTS[k]['g'] = 1
# the weapon from its own place on the sheet, scaled to a share of the figure height, held at the hand
wp = C['weapon']; wa, wf, wal = cutbg(wp['box'], 1); ys, xs = np.nonzero(FIG); figH = ys.max() - ys.min(); k_ = figH * wp['height'] / wf.shape[0]
wim = Image.fromarray(np.dstack([wa, wal * 255]).astype(np.uint8), 'RGBA').resize((max(1, int(wf.shape[1] * k_)), int(wf.shape[0] * k_)), Image.LANCZOS); wim.save(os.path.join(OUT, 'bow.png'))
hp = S2(wp['hold']); PARTS['bow'] = dict(img='bow.png', n='ธนู', role='weapon', p=wp['parent'], pv=[wim.width * .45, wim.height * C['hold_frac']], at=[round(hp[0], 1), round(hp[1], 1)], r=wp['r'], s=1)
ar = C['arrow']; aa, af, aal = cutbg(ar['box'], 1); aim = Image.fromarray(np.dstack([aa, aal * 255]).astype(np.uint8), 'RGBA').resize((max(1, int(af.shape[1] * k_)), int(af.shape[0] * k_)), Image.LANCZOS); aim.save(os.path.join(OUT, 'arrow.png'))
feet = [round(float(xs[ys > ys.max() - 6].mean()), 1), float(ys.max())]
rig = dict(v=2, name=name, title=C['title'], dir=f'art/rigs/{name}/', ref='ref.png', refMask='ref_mask.png', size=[W, H], feet=feet, view='front', flip=C['flip'], figH=float(figH), bake=True,
           shot='arrow.png', checks=dict(throw=False), parts=PARTS, order=C['order'])
json.dump(rig, open(os.path.join(R, f'art/rigs/{name}.json'), 'w'), ensure_ascii=False, indent=1, default=float); print(f'art/rigs/{name}.json', len(PARTS), 'pieces', W, 'x', H)
