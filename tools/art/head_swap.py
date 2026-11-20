"""Put OUR character's head on a move sheet whose face came out wrong (owner 2026-11-21: "เอาอันนี้ไปเปลี่ยนเป็นตัวละครเรา หน้ามันเพี้ยน เอาแค่ท่าเดิน").

  python tools/art/head_swap.py <sheet.png> <head_picture.png> <out_prefix> [cols rows] [scale]

The sheet: a grid of frames on transparent background, side view facing right (the owner's video walk of the dragon, 4 x 4).
The head picture: our character cut out (art/pixmap/dragon_2d.png, 369 x 512, facing right).
Per frame: the old head is tracked from frame 0 (template match on face + front hair), the hair / face above the neck is erased (the spear is kept:
its shaft line is found below the hands and a band round it is protected), our head (scaled, bottom edge feathered into the collar) is pasted with
its chin on the old chin, then the spear pixels are drawn back on top. Output = a strip + json + preview gif like blue_sheet_cut.py
(all frames one size, feet on one line).
Numbers below are for the dragon picture and the owner's walk; another pair needs new anchor points.
"""
import sys, json
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd
from scipy.spatial import ConvexHull

src, headp, out = sys.argv[1], sys.argv[2], sys.argv[3]
C = int(sys.argv[4]) if len(sys.argv) > 4 else 4
Rn = int(sys.argv[5]) if len(sys.argv) > 5 else 4
K = float(sys.argv[6]) if len(sys.argv) > 6 else .56
S = np.array(Image.open(src).convert('RGBA')).astype(float); H, W = S.shape[:2]; cw, ch = W // C, H // Rn
cell = lambda i: S[(i // C) * ch:(i // C + 1) * ch, (i % C) * cw:(i % C + 1) * cw].copy()

# ---- our head: crop + mask (dragon_2d coordinates), spear left out, bottom feathered
HD = np.array(Image.open(headp).convert('RGBA')).astype(float)
hy, hx = np.mgrid[0:HD.shape[0], 0:HD.shape[1]]
m = (hy < 240).astype(float)
m[(hx > 298) & (hy < 178)] = 0; m[hx > 321] = 0                     # the spear tip / shaft of the head picture
m *= np.clip((240 - hy) / 16, 0, 1)                                     # feather into the collar
HD[..., 3] *= m
CHIN = (290, 218)                                                       # jaw bottom of the head picture
hd_img = Image.fromarray(HD.astype(np.uint8), 'RGBA'); hd_s = hd_img.resize((round(HD.shape[1] * K), round(HD.shape[0] * K)), Image.LANCZOS)
chin_s = (CHIN[0] * K, CHIN[1] * K)

# ---- track the old head from frame 0
f0 = cell(0); TY, TX, TH, TW = 105, 195, 67, 63; T = f0[TY:TY + TH, TX:TX + TW, :3]; Ta = f0[TY:TY + TH, TX:TX + TW, 3] > 40
CHIN0, NECK_R, NECK_L, HAIR_L = (242, 172), 176, 180, 128
frames = []
for i in range(C * Rn):
    c = cell(i); best = None
    for dy in range(-30, 31):
        for dx in range(-40, 41):
            y0, x0 = TY + dy, TX + dx
            if y0 < 0 or x0 < 0 or x0 + TW > cw or y0 + TH > ch: continue
            e = ((c[y0:y0 + TH, x0:x0 + TW, :3] - T) ** 2).sum(2)[Ta].mean()
            if best is None or e < best[0]: best = (e, dx, dy)
    _, dx, dy = best
    # the spear above the neck = its gold tip (no gold in hair or face) + the dark outline / red inlays round it + the bit of shaft from the socket down
    yy, xx = np.mgrid[0:ch, 0:cw]; rgb = c[..., :3]; al = c[..., 3] > 30; neck = np.where(xx < 200 + dx, NECK_L, NECK_R) + dy
    gold = al & (rgb[..., 0] > 150) & (rgb[..., 1] > 95) & (rgb[..., 2] < 120) & (rgb[..., 0] - rgb[..., 2] > 70) & (yy < neck) & (xx > CHIN0[0] + dx - 30)
    lab, n = nd.label(nd.binary_dilation(gold, iterations=3), structure=np.ones((3, 3))); lab[~gold] = 0   # the blade's gold is in fragments: join them first
    sz = nd.sum(gold, lab, range(1, n + 1)) if n else []; cx_ = nd.center_of_mass(gold, lab, range(1, n + 1)) if n else []
    tip = np.isin(lab, [k + 1 for k, v in enumerate(sz) if v > 80 and cx_[k][1] > CHIN0[0] + dx - 5]) if n else gold
    hairish = (rgb.min(2) > 165) & (rgb.max(2) - rgb.min(2) < 60)
    hull = np.zeros_like(tip)   # each gold piece filled as its convex shape (the red inlays and the outline inside the blade come with it)
    for k in range(1, n + 1):
        if not tip[lab == k].any(): continue
        ys_, xs_ = np.where(lab == k)
        try: H_ = ConvexHull(np.c_[xs_, ys_]); poly = [tuple(v) for v in np.c_[xs_, ys_][H_.vertices]]
        except Exception: continue
        pim = Image.new('L', (cw, ch), 0); ImageDraw.Draw(pim).polygon(poly, fill=1); hull |= np.array(pim) > 0
    spear = nd.binary_dilation(hull, iterations=3) & al & ~hairish
    if tip.any():   # shaft from the lowest tip pixel down to the rightmost dark run below the neck
        ty, tx = np.where(tip); sy = ty.max(); sx = tx[ty >= sy - 2].mean(); yb = min(ch - 1, int(neck.max()) + 30); row = c[yb]
        dk = np.where((row[:, 3] > 120) & (row[:, :3].max(1) < 80))[0]; bx = dk[dk > CHIN0[0] + dx - 20][-1] if (dk > CHIN0[0] + dx - 20).any() else sx
        t = np.clip((yy - sy) / max(1, yb - sy), 0, 1); lx = sx + (bx - sx) * t
        spear |= (yy >= sy - 2) & (yy <= yb) & (np.abs(xx - lx) < 6) & al & ~hairish
    erase = (yy < neck) & (xx >= HAIR_L + dx) & ~spear
    keep = c.copy(); a, b = 0, 0
    c[erase, 3] = 0
    im = Image.fromarray(np.clip(c, 0, 255).astype(np.uint8), 'RGBA')
    px, py = round(CHIN0[0] + dx - chin_s[0]), round(CHIN0[1] + dy - chin_s[1])
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); lay.paste(hd_s, (px, py)); im = Image.alpha_composite(im, lay)
    sp = keep.copy(); sp[~spear, 3] = 0; im = Image.alpha_composite(im, Image.fromarray(np.clip(sp, 0, 255).astype(np.uint8), 'RGBA'))
    frames.append(im); print(i, 'head', dx, dy, 'tip px', int(tip.sum()))

# ---- one size, feet on one line (lowest figure pixel of each frame)
arrs = [np.array(f) for f in frames]; foots = []
for a_ in arrs: ys = np.where((a_[..., 3] > 60).any(1))[0]; foots.append(ys.max())
FOOT = max(foots); shifted = []
for f, ft in zip(frames, foots): g = Image.new('RGBA', f.size, (0, 0, 0, 0)); g.paste(f, (0, FOOT - ft)); shifted.append(g)
box = None
for g in shifted:
    bb = g.getbbox(); box = bb if box is None else (min(box[0], bb[0]), min(box[1], bb[1]), max(box[2], bb[2]), max(box[3], bb[3]))
frames = [g.crop(box) for g in shifted]; fw, fh = frames[0].size; footy = FOOT - box[1]
FH = 256; k = FH / fh; fw2 = round(fw * k); frames = [f.resize((fw2, FH), Image.LANCZOS) for f in frames]
strip = Image.new('RGBA', (fw2 * len(frames), FH))
for i, f in enumerate(frames): strip.alpha_composite(f, (i * fw2, 0))
strip.save(out + '.png'); json.dump({'n': len(frames), 'w': fw2, 'h': FH, 'foot': round(footy * k), 'src': src}, open(out + '.json', 'w'))
pv = [Image.alpha_composite(Image.new('RGBA', f.size, (232, 214, 180, 255)), f).resize((fw2 // 2, FH // 2), Image.LANCZOS).convert('P', palette=Image.ADAPTIVE) for f in frames]
pv[0].save(out + '_preview.gif', save_all=True, append_images=pv[1:], duration=90, loop=0)
print('frames', len(frames), fw2, 'x', FH, '->', out)
