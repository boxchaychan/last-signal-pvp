"""pixel_hires.py - make a pixel-art picture finer with GPT, piece by piece.
(From the owner's doc "ทำภาพ Pixel Art ละเอียดสูงด้วย GPT", 2026-11-05; steps for people and for AI are in
docs/babies-and-beasts.md, section "ภาพพิกเซลละเอียดขึ้นด้วย GPT".)

  pip install pillow numpy
  python pixel_hires.py cut   picture.png work/ --scale 3 --tile 1254
  (GPT redraws every work/in/*.png -> save each result as work/out/<same name>.png)
  python pixel_hires.py merge picture.png work/ result.png

cut   : cuts the picture into overlapping pieces, enlarges each with NEAREST to --tile px.
merge : for every piece GPT returned: checks it (size, shift, mask), keeps the ORIGINAL
        colour + light and takes only GPT's fine detail, then joins the pieces with soft
        seams into one picture --scale times bigger than the original.
"""
import argparse, json, os
import numpy as np
from PIL import Image, ImageFilter

MASK = (255, 0, 255)          # background / hole colour that must never change


def mask_of(a):
    return (a[..., 0] > 200) & (a[..., 1] < 80) & (a[..., 2] > 200)


def blur(a, r):
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return np.asarray(img.filter(ImageFilter.GaussianBlur(r))).astype(np.float32)


def cut(a):
    src = Image.open(a.picture).convert("RGB")
    W, H = src.size
    piece = a.tile // a.scale                  # piece side in original px
    step = max(1, piece - piece // 4)          # 1/4 overlap
    xs = list(range(0, max(1, W - piece) + 1, step)); ys = list(range(0, max(1, H - piece) + 1, step))
    if xs[-1] + piece < W: xs.append(W - piece)
    if ys[-1] + piece < H: ys.append(H - piece)
    os.makedirs(f"{a.work}/in", exist_ok=True); os.makedirs(f"{a.work}/out", exist_ok=True)
    pieces = []
    for r, y in enumerate(ys):
        for c, x in enumerate(xs):
            crop = src.crop((x, y, x + piece, y + piece))
            arr = np.asarray(crop)
            if mask_of(arr.astype(np.float32)).mean() > 0.98:
                continue                        # only background: nothing to redraw
            name = f"r{r:02d}_c{c:02d}"
            crop.resize((a.tile, a.tile), Image.NEAREST).save(f"{a.work}/in/{name}.png")
            pieces.append({"name": name, "x": x, "y": y})
    json.dump({"scale": a.scale, "tile": a.tile, "piece": piece, "size": [W, H], "pieces": pieces},
              open(f"{a.work}/pieces.json", "w"), indent=1)
    print(f"{len(pieces)} pieces of {piece} px -> {a.work}/in (send each to GPT, save as {a.work}/out/<name>.png)")


def shift_check(o, g):
    """best match offset (in tile px) of a few blocks; big numbers = GPT moved things."""
    small = lambda x: np.asarray(Image.fromarray(x.astype(np.uint8)).convert("L").resize((256, 256), Image.BOX)).astype(np.float32)
    ol, gl = small(o), small(g); k = o.shape[0] / 256; worst = 0
    for by in (32, 112, 176):
        for bx in (32, 112, 176):
            B = ol[by:by + 48, bx:bx + 48] - ol[by:by + 48, bx:bx + 48].mean()
            if B.std() < 3: continue
            best = (-2, 0)
            for dy in range(-8, 9):
                for dx in range(-8, 9):
                    A = gl[by + dy:by + dy + 48, bx + dx:bx + dx + 48]; A = A - A.mean()
                    cc = (A * B).sum() / np.sqrt((A * A).sum() * (B * B).sum() + 1e-9)
                    if cc > best[0]: best = (cc, abs(dx) + abs(dy))
            worst = max(worst, best[1] * k)
    return worst


def merge(a):
    meta = json.load(open(f"{a.work}/pieces.json")); S, T = meta["scale"], meta["tile"]
    W, H = meta["size"]
    big = np.asarray(Image.open(a.picture).convert("RGB").resize((W * S, H * S), Image.NEAREST)).astype(np.float32)
    acc = np.zeros_like(big); wsum = np.zeros(big.shape[:2], np.float32)
    rng = np.random.default_rng(1)
    r = a.blur or S * 2                         # blur radius ~ 2 original pixels
    ramp = np.minimum(np.arange(T) + 1, np.arange(T)[::-1] + 1) / (T / 8)
    wt = np.clip(np.minimum.outer(ramp, ramp), 0, 1)
    for p in meta["pieces"]:
        f = f"{a.work}/out/{p['name']}.png"
        if not os.path.exists(f):
            print(f"MISSING {p['name']} - keeping the enlarged original there"); continue
        G = Image.open(f).convert("RGB")
        if G.size != (T, T):
            print(f"  {p['name']}: size {G.size} -> resized to {T}"); G = G.resize((T, T), Image.LANCZOS)
        g = np.asarray(G).astype(np.float32)
        y0, x0 = p["y"] * S, p["x"] * S
        o = big[y0:y0 + T, x0:x0 + T]
        mo, mg = mask_of(o), mask_of(g)
        iou = (mo & mg).sum() / max(1, (mo | mg).sum()) if mo.any() or mg.any() else 1.0
        sh = shift_check(o, g)
        flag = "REDRAW" if sh > T / 40 or iou < 0.9 else "ok"
        print(f"  {p['name']}: shift {sh:.0f} px, mask IoU {iou:.2f} -> {flag}")
        if flag == "REDRAW" and not a.force:
            continue
        out = blur(o, r) + (g - blur(g, r))      # original colour + GPT detail
        out = np.clip(out, 0, 255)
        out[mo] = MASK; out[mg & ~mo] = o[mg & ~mo]
        w = wt * (0.75 + 0.5 * rng.random((T, T)))  # wiggly seam
        acc[y0:y0 + T, x0:x0 + T] += out * w[..., None]; wsum[y0:y0 + T, x0:x0 + T] += w
    have = wsum > 0
    res = big.copy(); res[have] = acc[have] / wsum[have][:, None]
    res[mask_of(big)] = MASK
    Image.fromarray(res.astype(np.uint8)).save(a.result)
    small = lambda x: np.asarray(Image.fromarray(x.astype(np.uint8)).resize((W // 2 or 1, H // 2 or 1), Image.BOX)).astype(np.float32)
    keep = ~mask_of(small(big))
    print(f"saved {a.result} ({W * S}x{H * S}); zoomed-out colour difference {np.abs(small(res) - small(big))[keep].mean():.1f} (aim < 5)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    c = sp.add_parser("cut"); c.add_argument("picture"); c.add_argument("work")
    c.add_argument("--scale", type=int, default=3); c.add_argument("--tile", type=int, default=1254)
    m = sp.add_parser("merge"); m.add_argument("picture"); m.add_argument("work"); m.add_argument("result")
    m.add_argument("--blur", type=float, default=0); m.add_argument("--force", action="store_true")
    a = ap.parse_args(); {"cut": cut, "merge": merge}[a.cmd](a)
