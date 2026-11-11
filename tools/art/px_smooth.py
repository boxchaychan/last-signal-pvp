# Make PixelLab pixel art look painted when it has to be enlarged (owner 2026-11-11 "ทำให้สวยขึ้นได้ไหม PixelLab", MapleStory
# draws smooth, not blocky): Scale2x/EPX passes keep edges and diagonals clean (no blocks, no blur), then a soft Lanczos step
# to the exact size and a light unsharp.   python3 tools/art/px_smooth.py <in> <out> <factor>
import sys, numpy as np
from PIL import Image, ImageFilter
def scale2x(a):
    H, W = a.shape[:2]; p = np.pad(a, ((1, 1), (1, 1), (0, 0)), mode='edge')
    P = p[1:-1, 1:-1]; A = p[:-2, 1:-1]; B = p[1:-1, 2:]; C = p[1:-1, :-2]; D = p[2:, 1:-1]
    eq = lambda x, y: (x == y).all(-1)[..., None]
    e0 = np.where(eq(C, A) & ~eq(C, D) & ~eq(A, B), A, P); e1 = np.where(eq(A, B) & ~eq(A, C) & ~eq(B, D), B, P)
    e2 = np.where(eq(D, C) & ~eq(D, B) & ~eq(C, A), C, P); e3 = np.where(eq(B, D) & ~eq(B, A) & ~eq(D, C), D, P)
    o = np.zeros((H * 2, W * 2, a.shape[2]), a.dtype); o[0::2, 0::2] = e0; o[0::2, 1::2] = e1; o[1::2, 0::2] = e2; o[1::2, 1::2] = e3; return o
def smooth_up(im, k):
    a = np.asarray(im.convert('RGBA')); s = 1
    while s * 2 <= k: a = scale2x(a); s *= 2
    out = Image.fromarray(a)
    if s != k: out = out.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    return out.filter(ImageFilter.UnsharpMask(1.0, 30, 2))
if __name__ == '__main__':
    smooth_up(Image.open(sys.argv[1]), float(sys.argv[3])).save(sys.argv[2])
