"""Cut the Meta AI effect videos of the backpack game (black background, square, 10 s) into frame sheets for the 3D arena.

  python tools/art/bag_vfx.py [key ...]      (no key = every effect of FX whose video is in art/incoming/bag3d/vfx_meta/)
  python tools/art/bag_vfx.py --look <key>   = only a contact sheet with frame numbers (art/incoming/bag3d/vfx_meta/look_<key>.jpg) to pick frames
  python tools/art/bag_vfx.py --sheet        = art/bag3d/fx_preview.jpg: one middle frame of every cut effect on sand, to look at them together

The .mp4 are git-ignored (360 MB): they live only on the owner's PC, so the cutting must be done there; the sheets are in git.
Per effect: takes the video frames FX[key]['fr'] = (first, last) (or finds the part where something is on screen), picks n frames with more
of them early (the burst is fast, the fade is slow), lifts the video's black haze, turns brightness into transparency (the colour is kept, so
the sheet can be drawn with normal blending on the bright sand as well as added as light), fades everything toward the picture border with a
round window (Meta does not always keep an effect inside the frame: a bolt that touches the border dissolves instead of ending in a straight
line; owner 2026-11-28 "ระวังล้นกรอบ"), crops all frames to the box the effect really uses (square, nothing is squashed), and writes
art/bag3d/fx/<key>.webp + its entry in art/bag3d/fx/fx.json:
  { n, cols, rows, px (cell size), fps, flat (1 = drawn on the floor, the video was shot from above), loop, size (share of the video it used) }
Prompts: art/incoming/bag3d/vfx_meta/PROMPTS_META.txt. Played by bagFx() in bag3d/arena.js.
"""
import json, os, sys, glob
import numpy as np, cv2
from PIL import Image

RAW = 'art/incoming/bag3d/vfx_meta/'; OUT = 'art/bag3d/fx'; os.makedirs(OUT, exist_ok=True)
CELL = 200; COLS = 6; WORK = 480   # frames are worked on at 480 px (the cells are 200)
# key: n = frames in the sheet, fr = (first, last) video frames, flat = on the floor, loop = plays round, src = another video file name,
# ease = how much the picked frames crowd toward the start (1 = even), fps = playback speed in the game, gain = brightness -> alpha
D = lambda n, a, b, **k: dict(n=n, fr=(a, b), **k)
FX = {
    # element reactions (the first clips of shock / overload / shatter / gas / crit ran off the frame: the game uses the second ones)
    'react_shock': D(20, 4, 140, src='react_shock2'), 'react_overload': D(20, 50, 180, src='react_overload2'), 'react_shatter': D(20, 20, 150, src='react_shatter2'),
    'react_gas': D(20, 30, 170, src='react_gas2'), 'react_wet': D(18, 6, 170), 'react_venom': D(20, 8, 175, flat=1),
    # five stacks of one element
    'blaze': D(18, 6, 140), 'bolt': D(16, 30, 180), 'frost': D(20, 8, 200, ease=1.1),
    # crit, melee
    'crit': D(16, 8, 110, src='crit2', ease=1.3), 'slash': D(16, 8, 170, ease=1.2), 'spin': D(16, 8, 180, flat=1), 'parry': D(14, 4, 130), 'dash': D(12, 8, 140), 'slam': D(16, 4, 180, flat=1),
    # spell items
    'storm': D(20, 8, 180, flat=1), 'timestop': D(22, 10, 190, flat=1, ease=1.2), 'summon': D(22, 8, 190, flat=1, ease=1.1), 'blink': D(16, 8, 160), 'curse': D(20, 8, 180, ease=1.2),
    'vines': D(22, 4, 175, ease=1.1), 'revive': D(22, 8, 190, ease=1.2), 'ball': D(16, 20, 60, loop=1, ease=1), 'guard': D(18, 8, 185, ease=1.2), 'hex': D(16, 4, 170), 'silence': D(18, 8, 185, flat=1),
    # item signature skills and class skills
    'meteor': D(20, 4, 165), 'nova': D(18, 4, 170, flat=1), 'pillar': D(20, 4, 200), 'spikes': D(18, 4, 180), 'tornado': D(20, 8, 190), 'rain': D(20, 8, 190), 'void': D(20, 8, 170, flat=1),
    'blood': D(18, 4, 175), 'blizzard': D(20, 8, 150, flat=1), 'poisoncloud': D(18, 8, 180), 'heal': D(18, 8, 170), 'shieldbash': D(16, 8, 150), 'arrowfan': D(12, 8, 100), 'venomslash': D(18, 4, 170),
    # fight and screen moments
    'ko': D(12, 4, 70), 'bossin': D(18, 8, 170, flat=1), 'clash': D(20, 8, 180), 'victory': D(20, 4, 175), 'coins': D(18, 4, 175), 'craft': D(18, 8, 170),
    # projectiles (they stay in the middle of the video and loop; they fly to the right)
    # loops that sit on a fighter: the power-up aura and the four element statuses (rad = keep only this share of the picture round the middle: the burn clip came with a frame)
    'aura': D(14, 60, 110, loop=1, ease=1), 'st_burn': D(10, 60, 90, loop=1, ease=1, rad=.6), 'st_shock': D(10, 60, 90, loop=1, ease=1), 'st_poison': D(12, 60, 110, loop=1, ease=1), 'st_chill': D(10, 60, 100, loop=1, ease=1),
    'p_fire': D(10, 40, 70, loop=1, ease=1), 'p_ice': D(10, 40, 70, loop=1, ease=1), 'p_arcane': D(10, 40, 70, loop=1, ease=1), 'p_poison': D(10, 40, 70, loop=1, ease=1), 'p_light': D(10, 60, 90, loop=1, ease=1),
}
def frames_of(path, only=None):
    cap = cv2.VideoCapture(path); out = []; i = 0; want = set(only) if only is not None else None; last = max(want) if want else 10 ** 9
    while i <= last:
        ok, im = cap.read()
        if not ok: break
        if want is None or i in want: out.append(cv2.cvtColor(cv2.resize(im, (WORK, WORK), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2RGB))
        i += 1
    return out, cap.get(cv2.CAP_PROP_FPS) or 24, int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
def look(key):
    cap = cv2.VideoCapture(RAW + key + '.mp4'); N = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); n = 30; idx = [int(round(i * (N - 1) / (n - 1))) for i in range(n)]; fr, fps, _ = frames_of(RAW + key + '.mp4', idx); cells = []
    for f, im in zip(sorted(set(idx)), fr):
        im = cv2.cvtColor(cv2.resize(im, (200, 200)), cv2.COLOR_RGB2BGR); cv2.putText(im, str(f), (4, 16), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 255), 1); cells.append(im)
    while len(cells) % 6: cells.append(np.zeros_like(cells[0]))
    cv2.imwrite(RAW + 'look_' + key + '.jpg', np.vstack([np.hstack(cells[i:i + 6]) for i in range(0, len(cells), 6)])); print('look', key, N, 'frames', fps, 'fps')
def cut(key):
    C = FX.get(key, {}); path = RAW + C.get('src', key) + '.mp4'
    if not os.path.exists(path): print('no video for', key); return None
    cap = cv2.VideoCapture(path); N = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); vfps = cap.get(cv2.CAP_PROP_FPS) or 24; cap.release()
    if C.get('fr'): a, b = C['fr']; b = min(b, N - 1)
    else:
        fr, vfps, N = frames_of(path); lum = np.array([f.max(axis=2).astype(np.float32).mean() for f in fr]); act = lum - np.percentile(lum, 5); pk = act.max()
        on = np.where(act > pk * .05)[0]; a = int(on[0]); b = min(int(on[-1]), int(np.where(act > pk * .1)[0][-1]) + 6)
    n = C.get('n', 20); ease = C.get('ease', 1.5); idx = sorted(set(int(round(a + (b - a) * (i / (n - 1)) ** ease)) for i in range(n))); n = len(idx)
    fr, _, _ = frames_of(path, idx); H = W = WORK
    # the border fade: 1 in the middle, 0 at the picture edge (a smooth round window, the corners go first)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); r = np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)); win = np.clip((C.get('rad', 1.0) - r) / .2, 0, 1); win = win * win * (3 - 2 * win)
    cells = []
    for im in fr:
        im = im.astype(np.float32) / 255; v = im.max(axis=2); v = np.clip((v - .06) / .94, 0, 1)   # lift the black haze
        al = np.clip(v * C.get('gain', 1.9), 0, 1) * win; col = im / np.maximum(im.max(axis=2, keepdims=True), 1e-3)   # full-bright colour, brightness lives in alpha
        col = col * (.55 + .45 * np.clip(v * 1.4, 0, 1))[..., None]   # keep some shading inside the shape
        cells.append(np.dstack([col, al]))
    if C.get('loop'): cells = cells[:-1]; n = len(cells)   # the last frame of a loop = the first again, near enough
    # one crop box for the whole effect: square, centred on the video's middle when the effect sits on the floor or loops, else on what is drawn
    m = np.max([c[..., 3] for c in cells], axis=0) > .05; ys, xs = np.where(m)
    if len(xs) == 0: print('!!', key, 'is empty'); return None
    if C.get('flat') or C.get('loop'): cx, cy = W / 2, H / 2; half = max(abs(xs.min() - cx), abs(xs.max() - cx), abs(ys.min() - cy), abs(ys.max() - cy)) + 3
    else: cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2; half = max(xs.max() - xs.min(), ys.max() - ys.min()) / 2 * 1.03 + 3
    half = int(min(half, W / 2)); x0 = int(np.clip(cx - half, 0, W - 2 * half)); y0 = int(np.clip(cy - half, 0, H - 2 * half))
    cols = min(COLS, n); rows = (n + cols - 1) // cols; sheet = Image.new('RGBA', (cols * CELL, rows * CELL), (0, 0, 0, 0))
    for i, c in enumerate(cells):
        c = c[y0:y0 + 2 * half, x0:x0 + 2 * half]; im = Image.fromarray((np.clip(c, 0, 1) * 255).astype(np.uint8), 'RGBA').resize((CELL, CELL), Image.LANCZOS)
        sheet.paste(im, (i % cols * CELL, i // cols * CELL))
    sheet.save(f'{OUT}/{key}.webp', quality=82, method=4)
    span = (idx[-1] - idx[0]) / vfps; fps = C.get('fps') or (round(n / max(.3, span), 1) if C.get('loop') else round(max(12, min(24, n / max(.4, span * .55))), 1))
    # ox, oy = where the middle of the cut box sits in the video (-1 .. 1): a pillar that hits the lower centre keeps its foot point
    return dict(n=n, cols=cols, rows=rows, px=CELL, fps=fps, flat=1 if C.get('flat') else 0, loop=1 if C.get('loop') else 0, size=round(2 * half / W, 3), ox=round((x0 + half - W / 2) / (W / 2), 3), oy=round((y0 + half - H / 2) / (H / 2), 3)), (a, b)
def preview():
    J = json.load(open(OUT + '/fx.json')); ks = sorted(J); cols = 9; rows = (len(ks) + cols - 1) // cols; z = 150; out = Image.new('RGB', (cols * z, rows * (z + 16)), (196, 150, 96))
    from PIL import ImageDraw
    d = ImageDraw.Draw(out)
    for i, k in enumerate(ks):
        E = J[k]; sh = Image.open(f'{OUT}/{k}.webp').convert('RGBA'); f = int(E['n'] * (.5 if E['loop'] else .38)); c = sh.crop((f % E['cols'] * E['px'], f // E['cols'] * E['px'], (f % E['cols'] + 1) * E['px'], (f // E['cols'] + 1) * E['px'])).resize((z, z), Image.LANCZOS)
        x, y = i % cols * z, i // cols * (z + 16); out.paste(c, (x, y), c); d.text((x + 4, y + z + 2), k + (' (floor)' if E['flat'] else ''), fill=(40, 20, 10))
    out.save('art/bag3d/fx_preview.jpg', quality=86); print('wrote art/bag3d/fx_preview.jpg', len(ks), 'effects')

if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == '--look':
        for k in sys.argv[2:]: look(k)
        sys.exit()
    if len(sys.argv) > 1 and sys.argv[1] == '--sheet': preview(); sys.exit()
    keys = sys.argv[1:] or list(FX); jf = OUT + '/fx.json'; J = json.load(open(jf)) if os.path.exists(jf) else {}
    for k in keys:
        r = cut(k)
        if r: J[k] = r[0]; print(k, r[0], 'video frames', r[1], os.path.getsize(f'{OUT}/{k}.webp') // 1024, 'KB', flush=True)
    for k in list(J):
        if k not in FX: del J[k]
    json.dump(J, open(jf, 'w'), indent=1, sort_keys=True); print('wrote', jf, len(J), 'effects')
