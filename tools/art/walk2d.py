# Painted 2D (no pixels) walk test with OUR cut-out rig (owner 2026-11-13 "ลองทำแบบไม่ใช้พิกเซลดูว่าทำท่าเดินได้ไหม"). Free, no jobs.
# Source: the side view of art/incoming/darkchibi/sword_v1/turn_cut.png (owner's 3-view chibi swordsman, white cut out).
# Layers: cape (sways), back leg + front leg (thigh / shin+boot each, the same drawn leg; the part the sword covered is filled with
# the trouser colour), upper body with the arm and the sword (one piece: bobs and leans a little). Smooth art, so parts are turned
# with bicubic sampling. The lowest boot is kept on the ground line.
#   python3 tools/art/walk2d.py -> art/incoming/darkchibi/sword_v1/walk2d_strip.png (12 frames, 250x280) + walk2d.gif + walk2d_parts.png
import math, numpy as np
from PIL import Image, ImageDraw, ImageFilter
D = 'art/incoming/darkchibi/sword_v1/'; X0, P = 500, 80
src = Image.open(D + 'turn_cut.png').convert('RGBA').crop((X0, 0, 960, 1000)); W, H = src.size
A = np.asarray(src).copy(); yy, xx = np.mgrid[0:H, 0:W]; xx = xx + X0; op = A[..., 3] > 30
r, g, b = (A[..., i].astype(int) for i in range(3)); mx = np.maximum(np.maximum(r, g), b)
def poly(pts):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([(x - X0, y) for x, y in pts], fill=255); return np.asarray(m) > 0
def grow(m, n): return np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(2 * n + 1))) > 0
# sword + fist below the tunic: the bright pixels inside a loose polygon, grown to take their outline
sw = grow(poly([(668, 640), (800, 660), (950, 935), (938, 972), (890, 955), (690, 770)]) & op & (mx > 95) & ~((r > 120) & (g < 90)), 5) & op & (yy >= 690)
red = op & (r > 85) & (g < 75) & (b < 95) & (r > g * 1.7)
cape = grow(red & (xx < 708) & (yy > 480), 5) & op & (xx < 712) & (yy > 474)
leg = op & (yy >= 700) & (xx >= 676) & ~sw & ~cape
upper = op & ~leg & ~cape
from scipy import ndimage
lab, n = ndimage.label(upper); sz = ndimage.sum(upper, lab, range(1, n + 1)); upper = np.isin(lab, [i + 1 for i in range(n) if sz[i] > 400])      # specks left where the cape was cut away
def layer(m): a = A.copy(); a[~m] = 0; return a
L = layer(leg); tro = np.median(A[leg & (yy < 790) & (mx < 80)][:, :3], axis=0).astype(np.uint8)        # trouser colour
thigh_poly = poly([(684, 696), (806, 696), (792, 800), (676, 800)]); hole = thigh_poly & ~leg
L[hole, :3] = tro; L[hole, 3] = 255
edge = hole & grow(~(thigh_poly | leg), 4); L[edge, :3] = (22, 16, 20)   # dark rim where the fill meets the outside
thigh = L.copy(); thigh[yy >= 800] = 0; thigh[yy < 696] = 0; shin = L.copy(); shin[yy < 786] = 0
def pad(a): c = Image.new('RGBA', (W + 2 * P, H + 2 * P)); c.alpha_composite(Image.fromarray(a), (P, P)); return c
IM = dict(cape=pad(layer(cape)), thigh=pad(thigh), shin=pad(shin), upper=pad(layer(upper)))
def loc(x, y): return (x - X0 + P, y + P)
HIP, KNEE, SOLE, CAPE_P, WAIST = loc(742, 706), loc(738, 800), [loc(690, 962), loc(800, 962)], loc(706, 470), loc(740, 690)
def rot(p, c, a): a = math.radians(a); dx, dy = p[0] - c[0], p[1] - c[1]; return (c[0] + dx * math.cos(a) + dy * math.sin(a), c[1] - dx * math.sin(a) + dy * math.cos(a))
def turn(im, c, a, t=(0, 0)): return im.rotate(a, resample=Image.BICUBIC, center=c, translate=(round(t[0]), round(t[1])))
def dark(im, k):
    a = np.asarray(im).astype(float); a[..., :3] *= k; return Image.fromarray(a.astype(np.uint8))
N = 12; frames = []
for i in range(N):
    t = 2 * math.pi * i / N; out = Image.new('RGBA', IM['upper'].size); legs = []; low = 0
    for ph, k in ((math.pi, .72), (0, 1)):                       # back leg first (darker), then the front one
        s = 25 * math.sin(t + ph); fold = 38 * max(0, math.cos(t + ph + .7)); k2 = rot(KNEE, HIP, s)
        th = turn(IM['thigh'], HIP, s); sh = turn(IM['shin'], KNEE, s - fold, (k2[0] - KNEE[0], k2[1] - KNEE[1]))
        for q in SOLE:
            p = rot(q, KNEE, s - fold); low = max(low, p[1] + k2[1] - KNEE[1])
        legs.append((dark(sh, k) if k < 1 else sh, dark(th, k) if k < 1 else th))
    lift = round(SOLE[0][1] - low)                               # push everything down so the lower boot stands on the ground
    bob = lift + round(2 * math.sin(2 * t))
    out.alpha_composite(turn(IM['cape'], CAPE_P, 5 * math.sin(2 * t - 1.0) - 3, (0, bob)))
    for sh, th in legs:
        for im in (sh, th): out.alpha_composite(im.transform(im.size, Image.AFFINE, (1, 0, 0, 0, 1, -lift)))
    out.alpha_composite(turn(IM['upper'], WAIST, -2 + 1.2 * math.sin(2 * t + .5), (0, bob)))
    frames.append(out)
bb = [min(f.getbbox()[0] for f in frames), min(f.getbbox()[1] for f in frames), max(f.getbbox()[2] for f in frames), SOLE[0][1] + 6]
K = 270 / (bb[3] - bb[1]); cw, ch = 250, 280; strip = Image.new('RGBA', (cw * N, ch)); small = []
for i, f in enumerate(frames):
    c = f.crop(bb); c = c.resize((round(c.width * K), round(c.height * K)), Image.LANCZOS); cell = Image.new('RGBA', (cw, ch)); cell.alpha_composite(c, ((cw - c.width) // 2, ch - c.height - 4)); small.append(cell); strip.alpha_composite(cell, (i * cw, 0))
strip.save(D + 'walk2d_strip.png')
g = []
for j in range(N * 2):
    c = Image.new('RGBA', (cw * 2, ch * 2), (214, 226, 190, 255)); d = ImageDraw.Draw(c); d.rectangle((0, ch * 2 - 14, cw * 2, ch * 2), fill=(150, 170, 130))
    f = small[j % N].resize((cw * 2, ch * 2), Image.LANCZOS); c.alpha_composite(f, (0, 0)); g.append(c.convert('RGB'))
g[0].save(D + 'walk2d.gif', save_all=True, append_images=g[1:], duration=75, loop=0)
pp = Image.new('RGBA', (IM['upper'].width * 4 // 2, IM['upper'].height // 2), (214, 226, 190, 255))
for j, k in enumerate(('upper', 'cape', 'thigh', 'shin')): pp.alpha_composite(IM[k].resize((IM[k].width // 2, IM[k].height // 2)), (j * IM[k].width // 2, 0))
pp.save(D + 'walk2d_parts.png'); sheet = Image.new('RGBA', (cw * 6, ch * 2), (214, 226, 190, 255))
for i, f in enumerate(small): sheet.alpha_composite(f, (i % 6 * cw, i // 6 * ch))
sheet.save(D + 'walk2d_frames.png'); print('ok', bb, K)
