"""'8-bit' look for a pixel sprite (owner 2026-11-24 "ลองทำเป็น 8 บิต"), FREE: every colour snapped to the classic 8-bit console
palette (54 colours), then only the K most used of them kept per sprite (flat colours, no soft shading), outer edge pure black.
  python3 tools/art/eightbit.py in.png out.png [K=6]"""
import sys, numpy as np
from PIL import Image
NES = ['7C7C7C','0000FC','0000BC','4428BC','940084','A80020','A81000','881400','503000','007800','006800','005800','004058','000000',
 'BCBCBC','0078F8','0058F8','6844FC','D800CC','E40058','F83800','E45C10','AC7C00','00B800','00A800','00A844','008888',
 'F8F8F8','3CBCFC','6888FC','9878F8','F878F8','F85898','F87858','FCA044','F8B800','B8F818','58D854','58F898','00E8D8','787878',
 'FCFCFC','A4E4FC','B8B8F8','D8B8F8','F8B8F8','F8A4C0','F0D0B0','FCE0A8','F8D878','D8F878','B8F8B8','B8F8D8','00FCFC','F8D8F8']
P = np.array([[int(h[i:i + 2], 16) for i in (0, 2, 4)] for h in NES], float)
src, dst = sys.argv[1], sys.argv[2]; K = int(sys.argv[3]) if len(sys.argv) > 3 else 6
a = np.asarray(Image.open(src).convert('RGBA')).astype(float); op = a[..., 3] > 0; rgb = a[..., :3]
w = np.array([.3, .59, .11]) * 3   # brightness counts more than hue when snapping
def near(c, pal): return np.argmin((((c[:, None, :] - pal[None]) * w) ** 2).sum(2), 1)
px = rgb[op]; idx = near(px, P); cnt = np.bincount(idx, minlength=len(P)); keep = np.argsort(-cnt)[:K]; keep = keep[cnt[keep] > 0]
idx2 = keep[near(P[idx], P[keep])]; out = a.copy(); out[op, :3] = P[idx2]
edge = op & ~(np.roll(op, 1, 0) & np.roll(op, -1, 0) & np.roll(op, 1, 1) & np.roll(op, -1, 1)); out[edge, :3] = 0
Image.fromarray(out.astype(np.uint8)).save(dst)
