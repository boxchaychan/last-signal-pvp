# Cut a skill effect out of a video on flat green (owner 2026-11-10 "ทำทูลตัดเอฟเฟกต์จากวิดีโอไว้ใช้เลย ฉันจะเจนเอฟเฟกต์จากวิดีโอ";
# Meta AI clips, 24 fps, often portrait 720x1280): green keyed out (key colour read from the border), despill, anything that
# reaches the frame edge fades out (the generator lets rings and sparks run off the picture), a time range squeezed into a
# short game effect, scaled, cropped to the union box, written as fx/<key>.png + a manifest entry the game's pfx() reads,
# plus a preview GIF on the grass next to the Berserker at game scale.
#   python3 tools/video/vfx_cut.py <video.mp4> <key> [--from=0.7] [--to=7] [--dur=2] [--fps=24] [--size=260]
#        [--anchor=x,y] [--edge=60] [--cols=8]
#   --size: how wide the effect is in the game, in world px (the hero is ~76 tall; skill areas in
#           art/incoming/action/berserker/fx_size/size_guide.png: leap 260, whirl 270, Q ring 300)
#   --radial: an effect that repeats round its centre (a star of chains) is completed where it ran off the frame (copies turned by
#             whole repeat steps fill the cut parts)
#   --sym=N: a round effect that is fuller on some sides is completed with N turned copies of itself
#   --mirror (=full for a whole symmetric blast): a slam whose crack ran off one side is completed with its mirror image about the impact point
#   --anchor: the ground point in VIDEO px (default: middle, near the bottom of everything drawn; --center or a key ending in
#             _ring / _all / _shackle / burst: the frame centre = the start spark, and --size = the whole width)
import sys, os, json, subprocess
import numpy as np
from PIL import Image

def opt(name, d):
    for a in sys.argv:
        if a.startswith('--' + name + '='): return a.split('=', 1)[1]
    return d

def frames_of(path):
    pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=width,height,r_frame_rate',
                         '-of', 'csv=p=0', path], capture_output=True, text=True, check=True).stdout.strip().split(',')
    W, H = int(pr[0]), int(pr[1]); a, b = pr[2].split('/'); fps = float(a) / float(b)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3), fps

def keyer(fr, kc, edge):
    f = fr.astype(np.int16); r, g, b = f[..., 0], f[..., 1], f[..., 2]
    if kc[1] >= max(kc[0], kc[2]):                              # green screen
        mx = np.maximum(r, b); d = g - mx; dk = kc[1] - max(kc[0], kc[2])
        a = np.clip((1.15 - d / dk * 1.15 - .16) / .84, 0, 1)   # below ~16% = background noise (it left a faint box round some effects)            # owner: smoke came out green; a = how much of the key is NOT there
        aa = np.maximum(a, .05)[..., None]; un = (np.dstack([r, g, b]) - (1 - aa) * np.array(kc)) / aa   # take the key colour out of half see-through pixels
        r, g, b = [np.clip(un[..., c], 0, 255).astype(np.int16) for c in range(3)]; g = np.minimum(g, np.maximum(r, b) + 12)
    else:                                                        # magenta screen
        mn = np.minimum(r, b); d = mn - g; dk = min(kc[0], kc[2]) - kc[1]
        a = np.clip((dk * .8 - d) / (dk * .5), 0, 1); sp = d > 0
        r = np.where(sp, np.minimum(r, g + 10), r); b = np.where(sp, np.minimum(b, g + 10), b)
    H, W = a.shape; yy, xx = np.mgrid[0:H, 0:W]; e = np.minimum.reduce([xx, yy, W - 1 - xx, H - 1 - yy]).astype(float)
    a = a * np.clip(e / max(edge, 1), 0, 1)
    a[e < 8] = 0                                                  # Meta AI clips carry a faint dark line round the frame edge
    return np.dstack([r, g, b, (a * 255).astype(np.int16)]).clip(0, 255).astype(np.uint8)

def mirror_fill(K, full=False):
    # owner 2026-11-10 "มีขาดไปบ้าง ต่อให้หน่อย": the ground crack of a slam ran off one side of the frame; pad the frame left and right
    # and fill what lies outside the old frame with the effect mirrored about its impact point (the column where the lower band
    # of the late frames is heaviest), so the crack reaches the same length on both sides
    H, W = K[0].shape[:2]; P = W // 3
    band = sum(k[int(H * .7):, :, 3].astype(float).sum(0) for k in K[len(K) // 2:])

    ci = int(np.average(np.arange(W), weights=band + 1e-6)) if full else int(np.argmax(np.convolve(band, np.ones(41) / 41, 'same')))   # a blast: its middle
    print('mirror fill about x =', ci)
    out = []
    for k in K:
        pad = np.zeros((H, W + 2 * P, 4), np.uint8); pad[:, P:P + W] = k
        xs = np.arange(W + 2 * P); src = 2 * (ci + P) - xs                       # mirrored column in padded coordinates
        ok = (src >= P) & (src < P + W); outside = (xs < P) | (xs >= P + W)
        y0 = 0 if full else int(H * .72)                                         # --mirror=full: a symmetric blast, every row; else only the ground band
        for x in np.nonzero(outside & ok)[0]: pad[y0:, x] = pad[y0:, src[x]]
        # a soft join: just inside the old edge, blend the mirrored copy where the original is thinner
        for x in list(range(P, P + (90 if full else 24))) + list(range(P + W - (90 if full else 24), P + W)):
            if 0 <= src[x] < W + 2 * P: col, scol = pad[y0:, x], pad[y0:, src[x]]; m = scol[:, 3] > col[:, 3]; col[m] = scol[m]
        out.append(pad)
    return out

def sym_fill(K, n):
    # owner 2026-11-10 "สวยแต่ไม่เต็ม เอาอันที่เต็มมาเติมอันที่ไม่เต็ม": a round effect (a ring with smoke on some sides only) is
    # completed with copies of itself turned by 360/n degrees round the frame centre; wherever a copy is more solid it wins
    from scipy import ndimage
    out = []
    for k in K:
        res = k.copy()
        for m in range(1, n):
            rot = ndimage.rotate(k, 360 / n * m, axes=(1, 0), reshape=False, order=1)
            take = rot[..., 3] > res[..., 3]; res[take] = rot[take]
        out.append(res)
    print('sym fill:', n, 'copies'); return out

def radial_fill(K):
    # owner 2026-11-10 "ควันบางข้างไม่เต็ม แก้ให้เต็มทุกข้าง": an effect that repeats round its centre (chains in a star) gets cut where
    # it runs off the frame edges, while along the diagonals it is still whole. Find how many times it repeats (angular
    # autocorrelation of the alpha in a ring), pad the frame and fill everything outside the old frame from copies turned by
    # whole steps of that repeat, so every side is complete.
    from scipy import ndimage
    H, W = K[0].shape[:2]; cy, cx = H / 2, W / 2; R0 = min(H, W) / 2
    acc = np.zeros(360)
    yy, xx = np.mgrid[0:H, 0:W]; rr = np.hypot(yy - cy, xx - cx); ang = (np.degrees(np.arctan2(yy - cy, xx - cx)) % 360).astype(int)
    ring = (rr > R0 * .35) & (rr < R0 * .9)
    for k in K: acc += np.bincount(ang[ring], weights=(k[..., 3][ring] > 60).astype(float), minlength=360)[:360]
    acc -= acc.mean(); best, nsym = -1e9, 0
    for n in range(5, 17):
        sh = round(360 / n); c = (acc * np.roll(acc, sh)).sum()
        if c > best: best, nsym = c, n
    step = 360 / nsym; P = int(max(H, W) * 1.5) // 2 * 2; oy, ox = (P - H) // 2, (P - W) // 2
    inside = np.zeros((P, P), bool); inside[oy + 60:oy + H - 60, ox + 60:ox + W - 60] = True   # the 60 px band inside the old edge is blended too (no square seam)
    out = []
    for k in K:
        pad = np.zeros((P, P, 4), np.uint8); pad[oy:oy + H, ox:ox + W] = k; res = pad.copy()
        for m in (1, -1, 2, -2, 3, -3):
            rot = ndimage.rotate(pad, step * m, axes=(1, 0), reshape=False, order=1)
            hole = (~inside) & (res[..., 3] < rot[..., 3])
            res[hole] = rot[hole]
        out.append(res)
    print('radial fill:', nsym, 'repeats, step %.1f deg' % step)
    return out

if __name__ == '__main__':
    vid, key = sys.argv[1], sys.argv[2]
    t0, t1 = float(opt('from', 0)), opt('to', None); dur, ofps = float(opt('dur', 2)), int(opt('fps', 24))
    # game width per effect (world px; the hero is 76 tall), so no --size is needed for the planned ones
    SIZE = {'bz_hit': 60, 'bz_swing': 200, 'bz_chain_all': 300, 'bz_chain_ring': 300, 'bz_triple': 260, 'bz_slam': 190,
            'bz_slam_ring': 260, 'bz_crack_line': 300, 'bz_shackle': 200, 'bz_rage': 105, 'bz_wave': 120, 'bz_hook': 300}
    size, edge, cols = float(opt('size', SIZE.get(key, 260))), int(opt('edge', 60)), int(opt('cols', 8))
    V, vfps = frames_of(vid); n_in = len(V); t1 = float(t1) if t1 else n_in / vfps
    border = np.concatenate([V[0, 0], V[0, -1], V[0, :, 0], V[0, :, -1]]); kc = np.median(border, 0)
    n = max(2, round(dur * ofps)); idx = np.linspace(t0 * vfps, min(n_in - 1, t1 * vfps - 1), n).round().astype(int)
    RADIAL = '--radial' in sys.argv
    K = [keyer(V[i], kc, 0 if RADIAL else edge) for i in idx]
    if RADIAL: K = radial_fill(K)
    SYM = int(opt('sym', 0))
    if SYM: K = sym_fill(K, SYM)
    if '--mirror' in sys.argv or opt('mirror', None): K = mirror_fill(K, opt('mirror', 'ground') == 'full')
    # owner's clips often stop with the effect still showing: fade the last part out (--fade=0 keeps it, loops should use 0)
    fade = float(opt('fade', .2)); nf = int(round(n * fade))
    for j in range(nf): K[n - nf + j][..., 3] = (K[n - nf + j][..., 3] * (1 - (j + 1) / nf)).astype(np.uint8)
    al = np.stack([k[..., 3] > 40 for k in K]).any(0); ys, xs = np.nonzero(al)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    # the effect's ground width = the widest row band in the lower third of the union box
    lower = al[y0 + (y1 - y0) * 2 // 3:y1]; cx = np.nonzero(lower.any(0))[0]; gw = (cx.max() - cx.min() + 1) if len(cx) else (x1 - x0)
    CENTER = '--center' in sys.argv or key.endswith(('_ring', '_all', '_shackle', '_burst', 'burst'))   # effects that grow from the spark in the middle
    if CENTER:   # the main body: columns that are covered in a fair share of the frames (stray sparks do not count)
        cov = np.stack([k[..., 3] > 40 for k in K]).sum(0).sum(0).astype(float); live = np.nonzero(cov > cov.max() * .08)[0]
        gw = (live.max() - live.min() + 1) if len(live) else (x1 - x0)
    sc = size / gw
    an = opt('anchor', None)
    ax, ay = (float(v) for v in an.split(',')) if an else (K[0].shape[1] / 2, K[0].shape[0] / 2) if CENTER else ((cx.min() + cx.max()) / 2 if len(cx) else (x0 + x1) / 2, y1 - (y1 - y0) * .1)
    w, h = max(1, round((x1 - x0) * sc)), max(1, round((y1 - y0) * sc))
    rows = -(-n // cols); sheet = Image.new('RGBA', (w * cols, h * rows)); fr = []
    for i, k in enumerate(K):
        im = Image.fromarray(k[y0:y1, x0:x1]).resize((w, h), Image.LANCZOS); fr.append(im)
        sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    os.makedirs('fx', exist_ok=True)
    sheet.quantize(256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE).save(f'fx/{key}.png', optimize=True)   # 256 colours: ~5x smaller for phones
    man = json.load(open('fx/manifest.json')) if os.path.exists('fx/manifest.json') else {}
    man[key] = dict(w=w, h=h, n=n, cols=cols, fps=ofps, ax=round((ax - x0) * sc), ay=round((ay - y0) * sc),
                    src=f'video {os.path.basename(vid)} {t0}-{t1:.2f}s, tools/video/vfx_cut.py')
    json.dump(man, open('fx/manifest.json', 'w'), separators=(',', ':'))
    # preview: grass, the Berserker (76 px tall like in the world), the effect at its game size in front of him
    od = f'art/incoming/fx_video/{key}'; os.makedirs(od, exist_ok=True)
    try:
        hero = Image.open('art/incoming/action/berserker/pl_dl_paid/Idle/rotations/south-east.png').convert('RGBA'); hero = hero.crop(hero.getbbox())
        hero = hero.resize((round(hero.width / 1.5), round(hero.height / 1.5)), Image.LANCZOS)
    except Exception: hero = None
    PW, PH = max(360, w + 160), max(240, h + 60); g = []
    gx, gy = PW - 20 - (w - man[key]['ax']), PH - 30 - (h - man[key]['ay'])
    for im in fr:
        c = Image.new('RGBA', (PW, PH), (92, 150, 62, 255))
        if hero: c.alpha_composite(hero, (20, PH - 30 - hero.height))
        c.alpha_composite(im, (gx - man[key]['ax'], gy - man[key]['ay'])); g.append(c.convert('RGB').quantize(128, dither=Image.Dither.NONE))
    g[0].save(f'{od}/preview.gif', save_all=True, append_images=g[1:], duration=round(1000 / ofps), loop=0)
    print(key, man[key], '->', f'fx/{key}.png', f'{od}/preview.gif')
