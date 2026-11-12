# Pixel stone blocks drawn in code (owner 2026-11-12 "ทำพื้นเป็นบล็อกหิน"): free, no jobs.
# blocks(h, w, bw, bh, pal, ...) -> an RGB float array of running-bond stone blocks seen a little from above:
# 1 px dark mortar, a light top / left edge, a darker front lip (lip rows) and right edge, a few specks, cracks and moss.
import numpy as np
def blocks(h, w, bw, bh, pal, seed=1, bond=True, lip=2, mortar=(46, 42, 48), moss=0.0, x0=0, y0=0):
    r = np.random.RandomState(seed)
    yy, xx = np.mgrid[0:h, 0:w]; yy = yy + y0; xx = xx + x0
    by = yy // bh; off = (by % 2) * (bw // 2) if bond else 0
    bx = (xx + off) // bw; lx = (xx + off) % bw; ly = yy % bh
    nbx, nby = int(bx.max()) + 2, int(by.max()) + 2
    pal = np.array(pal, float); pick = r.randint(0, len(pal), (nby, nbx)); jit = r.uniform(-9, 9, (nby, nbx))
    base = pal[pick[by, bx]] + jit[by, bx][..., None]
    out = base.copy()
    out[(ly == 0)] *= 1.16                                   # lit top edge
    out[(lx == 0) & (ly > 0)] *= 1.07                        # lit left edge
    out[(ly >= bh - 1 - lip) & (ly < bh - 1)] *= .76         # front lip (the camera looks a little from above)
    out[(lx == bw - 2) & (ly < bh - 1 - lip)] *= .88         # shaded right edge
    sp = r.rand(h, w)
    inner = (lx > 1) & (lx < bw - 2) & (ly > 1) & (ly < bh - 2 - lip)
    out[inner & (sp < .035)] *= .84; out[inner & (sp > .975)] *= 1.1
    # a crack on some blocks: a short diagonal of dark pixels
    ck = r.rand(nby, nbx) < .14; cx0 = r.randint(2, max(3, bw - 5), (nby, nbx)); cdir = r.choice([-1, 1], (nby, nbx))
    t = ly - 1; crack = ck[by, bx] & (t >= 0) & (t < bh - 3 - lip) & (lx == cx0[by, bx] + cdir[by, bx] * (t // 2))
    out[crack] = out[crack] * .62
    if moss:
        mm = (r.rand(nby, nbx) < moss)[by, bx] & ((ly >= bh - 2 - lip) | (lx <= 1)) & (sp < .55)
        out[mm] = out[mm] * .35 + np.array([70, 120, 50]) * .65
    out[(lx == bw - 1) | (ly == bh - 1)] = mortar
    return np.clip(out, 0, 255)
