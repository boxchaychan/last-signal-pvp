# ParticleFX "chain lightning between orbs" sheet (6x6 frames, 4 orbs joined by bolts) -> two parts the game moves itself
# (owner 2026-11-09 "สกิล 2 เมจ"): fx/pfx_orb.png = one orb (put on every monster the chain hits) and fx/pfx_bolt.png = one
# bolt laid flat left to right (stretched and turned between any two monsters). Orb centres in a 684x488 cell were measured
# on frame 0: A (135,285) B (264,178) C (385,316) D (515,208); the orb is B, the bolt is B -> C with both orbs masked out.
#   python tools/art/pfx_chain_parts.py <sheet.png> [scale=.6]
import json, math, sys
import numpy as np
from PIL import Image, ImageDraw

src = sys.argv[1]; sc = float(sys.argv[2]) if len(sys.argv) > 2 else .6
im = Image.open(src).convert('RGBA'); W, H = im.size; cw, ch = W // 6, H // 6
frames = [im.crop((c * cw, r * ch, (c + 1) * cw, (r + 1) * ch)) for r in range(6) for c in range(6)]
def dehaze(f, lo):   # the whole frame carries a faint haze; drop it so the parts have no grey box round them
    a = np.array(f).astype(float); a[..., 3] = np.clip((a[..., 3] - lo) / (255 - lo), 0, 1) ** .9 * 255; return Image.fromarray(a.astype(np.uint8))
B, C = (264, 178), (385, 316); R_ORB = 52
man = json.load(open('fx/manifest.json'))

def sheet(fr, key, ax, ay, fps=30):
    w, h = fr[0].size; n = len(fr); cols = min(12, n); rows = (n + cols - 1) // cols
    s = Image.new('RGBA', (w * cols, h * rows), (0, 0, 0, 0))
    for i, f in enumerate(fr): s.paste(f, ((i % cols) * w, (i // cols) * h))
    s.save(f'fx/{key}.png', optimize=True)
    man[key] = {'w': w, 'h': h, 'n': n, 'cols': cols, 'fps': fps, 'ax': int(round(ax)), 'ay': int(round(ay)), 'src': 'ParticleFX chain lightning, ' + key}
    print(key, n, 'frames', w, 'x', h)

# the orb: a soft round mask round B
mask = Image.new('L', (R_ORB * 2, R_ORB * 2), 0); ImageDraw.Draw(mask).ellipse((0, 0, R_ORB * 2 - 1, R_ORB * 2 - 1), fill=255)
mask = np.array(mask).astype(float) / 255
orbs = []
for f in frames:
    o = np.array(f.crop((B[0] - R_ORB, B[1] - R_ORB, B[0] + R_ORB, B[1] + R_ORB))).astype(float); o[..., 3] *= mask
    o = dehaze(Image.fromarray(o.astype(np.uint8)), 40); orbs.append(o.resize((round(o.width * sc), round(o.height * sc)), Image.LANCZOS))
sheet(orbs, 'pfx_orb', orbs[0].width / 2, orbs[0].height / 2)

# the bolt: turn each frame so B -> C is flat, cut a band between the two orbs
ang = math.degrees(math.atan2(C[1] - B[1], C[0] - B[0])); L = math.hypot(C[0] - B[0], C[1] - B[1]); band = 46
bolts = []
for f in frames:
    big = Image.new('RGBA', (cw * 2, ch * 2), (0, 0, 0, 0)); big.paste(f, (cw // 2, ch // 2))
    cx, cy = B[0] + cw // 2, B[1] + ch // 2
    r = big.rotate(ang, resample=Image.BICUBIC, center=(cx, cy))      # PIL turns counter-clockwise: this lays B -> C flat
    seg = np.array(r.crop((cx, cy - band, round(cx + L), cy + band))).astype(float)
    hh, ww = seg.shape[:2]; yy, xx = np.mgrid[0:hh, 0:ww]
    for ox in (0, L):                                                  # fade the orbs out at both ends
        d = np.hypot(xx - ox, yy - band); seg[..., 3] *= np.clip((d - 34) / 12, 0, 1)
    s2 = dehaze(Image.fromarray(seg.astype(np.uint8)), 70); bolts.append(s2.resize((round(s2.width * sc), round(s2.height * sc)), Image.LANCZOS))
sheet(bolts, 'pfx_bolt', 0, bolts[0].height / 2)
man['pfx_bolt']['len'] = bolts[0].width
json.dump(man, open('fx/manifest.json', 'w'), separators=(',', ':'))
