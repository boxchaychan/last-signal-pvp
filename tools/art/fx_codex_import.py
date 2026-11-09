# Codex effect pictures (art/incoming/fx_codex/<name>.png: 6 frames in a 3x2 grid of 512 px cells on pure black) -> game
# effect sheets fx/<key>.png + fx/manifest.json (w, h, n, cols, fps, ax, ay), like the other effect importers.
#   python tools/art/fx_codex_import.py            (every effect in the list L below)
# mode add   = pure light: brightness becomes see-through (dark parts vanish), for glows, flames, sparks
# mode solid = has dark solid parts (rocks, roots, smoke, water): black joined to the picture edge goes, with a soft
#              edge from brightness; everything inside stays
# size = the widest frame in game pixels (1 art px = 1 world px, like the heroes); rot = also write <key><deg> copies
# turned to every rot-th degree (projectiles, the ground crack; the turn is done on the full picture, then pixelized,
# ground things flattened to the camera); anchor c = centre of the ink, g = centre x on the lowest ink row, l = left end.
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

SRC, DST = 'art/incoming/fx_codex', 'fx'
L = {   # key: (picture, mode, size, fps, rot, anchor, flat)
 'cfire': ('fireball', 'add', 46, 14, 15, 'c', 0), 'cghost': ('ghost_fire', 'add', 46, 14, 15, 'c', 0),
 'cmeteor': ('meteor', 'solid', 120, 14, 0, 'c', 0), 'cmeteorhit': ('meteor_hit', 'solid', 300, 14, 0, 'g', 0),
 'cfirehit': ('meteor_hit', 'solid', 130, 16, 0, 'g', 0), 'cnova': ('frost_nova', 'add', 320, 16, 0, 'c', 0),
 'cshield': ('mana_shield', 'add', 92, 10, 0, 'c', 0), 'cblink': ('blink', 'add', 80, 16, 0, 'c', 0),
 'ccrack': ('ground_crack', 'solid', 320, 14, 15, 'l', .6), 'cwhirl': ('whirlwind', 'add', 300, 18, 0, 'c', 0),
 'crage': ('berserk', 'add', 84, 12, 0, 'g', 0), 'cslam': ('leap_slam', 'solid', 290, 16, 0, 'g', 0),
 'cspore': ('spore_cloud', 'solid', 90, 12, 0, 'c', 0), 'croots': ('root_spikes', 'solid', 120, 12, 0, 'g', 0),
 'cwave': ('water_wave', 'solid', 170, 12, 0, 'g', 0), 'csteam': ('steam', 'solid', 150, 14, 0, 'c', 0),
 'cshatter': ('shatter', 'add', 100, 16, 0, 'c', 0), 'coverload': ('overload', 'solid', 220, 15, 0, 'c', 0),
}

def cells(path):
    a = np.array(Image.open(path).convert('RGB')).astype(float); H, W = a.shape[:2]; cw, ch = W // 3, H // 2
    return [a[r * ch:(r + 1) * ch, c * cw:(c + 1) * cw] for r in range(2) for c in range(3)]

def to_rgba(c, mode):
    v = c.max(2)
    if mode == 'add':
        al = np.clip((v - 6) / 200, 0, 1) ** .8
    else:
        dark = v < 34; lab, n = ndimage.label(dark); edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
        bg = np.isin(lab, list(edge)); al = np.where(bg, np.clip((v - 6) / 28, 0, 1), 1.0)
    rgb = np.where(al[..., None] > 0, c / np.maximum(al[..., None], 1e-3) if mode == 'add' else c, 0)
    rgb = np.clip(rgb, 0, 255)
    return np.dstack([rgb, al * 255]).astype(np.uint8)

def shrink(im, s):
    p = im.astype(float) / 255; p[..., :3] *= p[..., 3:4]; h, w = p.shape[:2]
    q = np.array(Image.fromarray((p * 255).astype(np.uint8)).resize((max(1, round(w * s)), max(1, round(h * s))), Image.BOX)).astype(float) / 255
    a = q[..., 3:4]; rgb = np.where(a > 0, q[..., :3] / np.maximum(a, 1e-6), 0)
    out = np.dstack([rgb, a]) * 255; out[..., 3] = np.where(out[..., 3] < 20, 0, out[..., 3])
    return out.clip(0, 255).astype(np.uint8)

def build(key, pic, mode, size, fps, rot, anchor, flat, man):
    fr = [to_rgba(c, mode) for c in cells(f'{SRC}/{pic}.png')]
    A0 = np.stack([f[..., 3] for f in fr]).max(0) > 20; xs0 = np.nonzero(A0.any(0))[0]; s0 = size / max(1, xs0.max() + 1 - xs0.min())   # one scale for every turned copy
    variants = [(key, 0)] + ([(f'{key}{d}', d) for d in range(0, 360, rot)] if rot else [])
    if rot: variants = variants[1:]
    for name, deg in variants:
        fs = fr
        if deg:   # turn on the full picture, flatten ground things toward the camera
            fs = []
            for f in fr:
                fs.append(np.array(Image.fromarray(f).rotate(-deg, resample=Image.BICUBIC, expand=True)))
        A = np.stack([f[..., 3] for f in fs]); m = A.max(0) > 20; ys, xs = np.nonzero(m)
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        s = s0
        crop = [f[y0:y1, x0:x1] for f in fs]
        small = [shrink(f, s) for f in crop]
        if flat and deg:   # squash the vertical to the ground plane
            small = [np.array(Image.fromarray(f).resize((f.shape[1], max(1, round(f.shape[0] * flat))), Image.NEAREST)) for f in small]
        h, w = small[0].shape[:2]
        allpx = np.concatenate([f[f[..., 3] > 0][:, :3] for f in small if (f[..., 3] > 0).any()])[None]
        pal = Image.fromarray(allpx.astype(np.uint8)).quantize(48, method=Image.Quantize.MEDIANCUT)
        sheet = Image.new('RGBA', (w * len(small), h), (0, 0, 0, 0))
        for i, f in enumerate(small):
            q = np.array(Image.fromarray(f[..., :3]).quantize(palette=pal, dither=Image.Dither.NONE).convert('RGB'))
            sheet.paste(Image.fromarray(np.dstack([q, f[..., 3]])), (i * w, 0))
        S = np.stack([f[..., 3] for f in small]).astype(float).sum(0); yy, xx = np.mgrid[0:h, 0:w]; tw = S.sum()
        if anchor == 'c': ax, ay = (S * xx).sum() / tw, (S * yy).sum() / tw
        elif anchor == 'l':   # the start of the line: centre of the ink, moved back along the heading to its end
            cx, cy = (S * xx).sum() / tw, (S * yy).sum() / tw; r = np.radians(deg)
            half = size / 2 * .95; ax, ay = cx - np.cos(r) * half, cy - np.sin(r) * half * (flat or 1)
        else: rows = S.sum(1); ax = (S * xx).sum() / tw; ay = int(np.nonzero(rows > rows.max() * .05)[0].max())
        sheet.save(f'{DST}/{name}.png', optimize=True)
        man[name] = {'w': w, 'h': h, 'n': len(small), 'cols': len(small), 'fps': fps, 'ax': int(round(ax)), 'ay': int(round(ay)), 'src': f'Codex {pic}.png ({mode})'}
    print(key, len(variants), 'sheet(s)', w, 'x', h)

if __name__ == '__main__':
    man = json.load(open(f'{DST}/manifest.json'))
    for k in (sys.argv[1:] or L): build(k, *L[k], man)
    json.dump(man, open(f'{DST}/manifest.json', 'w'), separators=(',', ':'))
