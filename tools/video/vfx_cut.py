# Cut a skill effect out of a video on flat green (owner 2026-11-10 "ทำทูลตัดเอฟเฟกต์จากวิดีโอไว้ใช้เลย ฉันจะเจนเอฟเฟกต์จากวิดีโอ";
# Meta AI clips, 24 fps, often portrait 720x1280): green keyed out (key colour read from the border), despill, anything that
# reaches the frame edge fades out (the generator lets rings and sparks run off the picture), a time range squeezed into a
# short game effect, scaled, cropped to the union box, written as fx/<key>.png + a manifest entry the game's pfx() reads,
# plus a preview GIF on the grass next to the Berserker at game scale.
#   python3 tools/video/vfx_cut.py <video.mp4> <key> [--from=0.7] [--to=7] [--dur=2] [--fps=24] [--size=260]
#        [--anchor=x,y] [--edge=60] [--cols=8]
#   --size: how wide the effect is in the game, in world px (the hero is ~76 tall; skill areas in
#           art/incoming/action/berserker/fx_size/size_guide.png: leap 260, whirl 270, Q ring 300)
#   --anchor: the ground point in VIDEO px (default: middle, near the bottom of everything drawn)
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
        a = np.clip((dk * .8 - d) / (dk * .5), 0, 1); sp = d > 0
        g = np.where(sp, np.minimum(g, (r + b) // 2 + 10), g)
    else:                                                        # magenta screen
        mn = np.minimum(r, b); d = mn - g; dk = min(kc[0], kc[2]) - kc[1]
        a = np.clip((dk * .8 - d) / (dk * .5), 0, 1); sp = d > 0
        r = np.where(sp, np.minimum(r, g + 10), r); b = np.where(sp, np.minimum(b, g + 10), b)
    H, W = a.shape; yy, xx = np.mgrid[0:H, 0:W]; e = np.minimum.reduce([xx, yy, W - 1 - xx, H - 1 - yy]).astype(float)
    a = a * np.clip(e / max(edge, 1), 0, 1)
    return np.dstack([r, g, b, (a * 255).astype(np.int16)]).clip(0, 255).astype(np.uint8)

if __name__ == '__main__':
    vid, key = sys.argv[1], sys.argv[2]
    t0, t1 = float(opt('from', 0)), opt('to', None); dur, ofps = float(opt('dur', 2)), int(opt('fps', 24))
    size, edge, cols = float(opt('size', 260)), int(opt('edge', 60)), int(opt('cols', 8))
    V, vfps = frames_of(vid); n_in = len(V); t1 = float(t1) if t1 else n_in / vfps
    border = np.concatenate([V[0, 0], V[0, -1], V[0, :, 0], V[0, :, -1]]); kc = np.median(border, 0)
    n = max(2, round(dur * ofps)); idx = np.linspace(t0 * vfps, min(n_in - 1, t1 * vfps - 1), n).round().astype(int)
    K = [keyer(V[i], kc, edge) for i in idx]
    al = np.stack([k[..., 3] > 40 for k in K]).any(0); ys, xs = np.nonzero(al)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    # the effect's ground width = the widest row band in the lower third of the union box
    lower = al[y0 + (y1 - y0) * 2 // 3:y1]; cx = np.nonzero(lower.any(0))[0]; gw = (cx.max() - cx.min() + 1) if len(cx) else (x1 - x0)
    sc = size / gw
    an = opt('anchor', None)
    ax, ay = (float(v) for v in an.split(',')) if an else ((cx.min() + cx.max()) / 2 if len(cx) else (x0 + x1) / 2, y1 - (y1 - y0) * .1)
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
