# Copy a move from an example animation onto our own character (owner 2026-11-10 "ทำทูลขึ้นมาสำหรับการลอกท่า"):
# the example's poses, not its pixels. 1) PixelLab estimate_skeleton on every example frame and on our still (0.1 each),
# 2) retarget: every bone of ours takes the example bone's ANGLE but keeps OUR length, built out from our hips, so our
# proportions stay, 3) animate_with_skeleton_v3 draws our character in those poses (3 frames = 2 gen, 4-14 = 3, 15 = 4).
#   python tools/art/pose_copy.py <example frames dir or sheet.png[:cols]> <our still.png> <out dir> "<what we look like>" [action] [direction] [--dry]
# --dry stops before the paid step and writes preview.png (example skeletons | ours retargeted) to check first.
import sys, os, json, glob, base64, time, io
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from PIL import Image, ImageDraw
from pl_rpc import call

J = ['NOSE', 'NECK', 'RIGHT SHOULDER', 'RIGHT ELBOW', 'RIGHT ARM', 'LEFT SHOULDER', 'LEFT ELBOW', 'LEFT ARM', 'RIGHT HIP', 'RIGHT KNEE',
     'RIGHT LEG', 'LEFT HIP', 'LEFT KNEE', 'LEFT LEG', 'RIGHT EYE', 'LEFT EYE', 'RIGHT EAR', 'LEFT EAR']
# bones from the root (hip centre) outward: (parent, child); the hips and neck hang off the root
BONES = [('ROOT', 'RIGHT HIP'), ('ROOT', 'LEFT HIP'), ('ROOT', 'NECK'), ('RIGHT HIP', 'RIGHT KNEE'), ('RIGHT KNEE', 'RIGHT LEG'),
         ('LEFT HIP', 'LEFT KNEE'), ('LEFT KNEE', 'LEFT LEG'), ('NECK', 'RIGHT SHOULDER'), ('RIGHT SHOULDER', 'RIGHT ELBOW'),
         ('RIGHT ELBOW', 'RIGHT ARM'), ('NECK', 'LEFT SHOULDER'), ('LEFT SHOULDER', 'LEFT ELBOW'), ('LEFT ELBOW', 'LEFT ARM'),
         ('NECK', 'NOSE'), ('NOSE', 'RIGHT EYE'), ('NOSE', 'LEFT EYE'), ('NOSE', 'RIGHT EAR'), ('NOSE', 'LEFT EAR')]

def b64(im):
    bio = io.BytesIO(); im.save(bio, 'PNG'); return 'data:image/png;base64,' + base64.b64encode(bio.getvalue()).decode()

def skeleton(im):
    bb = im.getbbox(); k = 1
    if bb:
        h = max(bb[3] - bb[1], bb[2] - bb[0]) + 16; k = max(1, min(6, 250 // max(h, 1)))   # stays inside the 256 px limit
    if k > 1:   # a small figure: crop round it, enlarge (nearest) so the estimator sees it, then map the joints back
        pad = 8; x0, y0 = max(0, bb[0] - pad), max(0, bb[1] - pad); x1, y1 = min(im.width, bb[2] + pad), min(im.height, bb[3] + pad)
        big = im.crop((x0, y0, x1, y1)).resize(((x1 - x0) * k, (y1 - y0) * k), Image.NEAREST)
        s = skeleton_raw(big); return {j: (x0 + x / k, y0 + y / k) for j, (x, y) in s.items()}
    return skeleton_raw(im)

def skeleton_raw(im):
    r = call('estimate_skeleton', {'image': b64(im)}); jid = [w for w in r.replace('"', ' ').split() if len(w) == 36 and w.count('-') == 4][0]
    for _ in range(60):
        r = call('estimate_skeleton', {'job_id': jid})
        if 'NOSE' in r: break
        time.sleep(5)
    pts = {}
    k = r.find('keypoints:')
    if k >= 0:
        arr = json.JSONDecoder().raw_decode(r[r.index('[', k):])[0]
        pts = {q['label']: (q['x'], q['y']) for q in arr}
    if len(pts) < 18: raise SystemExit('skeleton reply not understood:\n' + r[:800])
    return {k: (x * im.width, y * im.height) for k, (x, y) in pts.items()}

def root(s): return ((s['RIGHT HIP'][0] + s['LEFT HIP'][0]) / 2, (s['RIGHT HIP'][1] + s['LEFT HIP'][1]) / 2)

def retarget(ref, ours, ref0):
    import math
    out = {'ROOT': root(ours)}; R = dict(ref, ROOT=root(ref)); O = dict(ours, ROOT=root(ours))
    hr = abs(root(ref0)[1] - ref0['NECK'][1]) or 1; ho = abs(root(ours)[1] - ours['NECK'][1]) or 1
    out['ROOT'] = (O['ROOT'][0] + (R['ROOT'][0] - root(ref0)[0]) * ho / hr, O['ROOT'][1] + (R['ROOT'][1] - root(ref0)[1]) * ho / hr)   # the body's travel, scaled
    HEAD = {'NOSE', 'RIGHT EYE', 'LEFT EYE', 'RIGHT EAR', 'LEFT EAR'}
    for p, c in BONES:
        if c in HEAD: continue
        ang = math.atan2(R[c][1] - R[p][1], R[c][0] - R[p][0]); L = math.hypot(O[c][0] - O[p][0], O[c][1] - O[p][1])
        out[c] = (out[p][0] + math.cos(ang) * L, out[p][1] + math.sin(ang) * L)
    # the head: our own face, carried by the neck and tipped by the example's neck->nose tilt (small sprites misread faces)
    t = math.atan2(R['NOSE'][1] - R['NECK'][1], R['NOSE'][0] - R['NECK'][0]) - math.atan2(ref0['NOSE'][1] - ref0['NECK'][1], ref0['NOSE'][0] - ref0['NECK'][0])
    t = max(-.5, min(.5, t)); ct, st = math.cos(t), math.sin(t)
    for h in HEAD:
        dx, dy = O[h][0] - O['NECK'][0], O[h][1] - O['NECK'][1]; out[h] = (out['NECK'][0] + dx * ct - dy * st, out['NECK'][1] + dx * st + dy * ct)
    return out

def frames_from(src):
    if os.path.isdir(src): return [Image.open(f).convert('RGBA') for f in sorted(glob.glob(os.path.join(src, '*.png')))]
    path, cols = (src.rsplit(':', 1) + [None])[:2] if ':' in os.path.basename(src) else (src, None)
    im = Image.open(path).convert('RGBA'); n = int(cols) if cols else max(1, im.width // im.height); w = im.width // n
    return [im.crop((i * w, 0, (i + 1) * w, im.height)) for i in range(n)]

def draw(im, s, col):
    g = ImageDraw.Draw(im)
    for p, c in BONES:
        if p == 'ROOT': continue
        g.line([s[p], s[c]], fill=col, width=2)
    for k, (x, y) in s.items(): g.ellipse([x - 2, y - 2, x + 2, y + 2], fill=col)

if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]; dry = '--dry' in sys.argv
    src, still, out, desc = a[:4]; action = a[4] if len(a) > 4 else 'attack'; dirn = a[5] if len(a) > 5 else 'east'
    os.makedirs(out, exist_ok=True)
    ex = [f for f in frames_from(src) if f.getbbox()][:15]; me = Image.open(still).convert('RGBA')
    sk = [skeleton(f) for f in ex]; ours = skeleton(me)
    tg = [retarget(s, ours, sk[0]) for s in sk]
    json.dump({'example': sk, 'ours': ours, 'target': [{k: v for k, v in t.items() if k != 'ROOT'} for t in tg]}, open(os.path.join(out, 'skeletons.json'), 'w'))
    W = max(f.width for f in ex); pv = Image.new('RGBA', (len(ex) * max(W, me.width), max(ex[0].height, me.height) * 2), (60, 90, 50, 255))
    for i, (f, s, t) in enumerate(zip(ex, sk, tg)):
        x0 = i * max(W, me.width); pv.alpha_composite(f, (x0, 0)); q = Image.new('RGBA', me.size, (0, 0, 0, 0)); q.alpha_composite(me)
        g = Image.new('RGBA', f.size, (0, 0, 0, 0)); draw(g, s, (255, 80, 80, 255)); pv.alpha_composite(g, (x0, 0))
        h = Image.new('RGBA', me.size, (0, 0, 0, 0)); h.alpha_composite(me); h.putalpha(h.getchannel('A').point(lambda v: v // 3)); draw(h, {k: v for k, v in t.items() if k != 'ROOT'}, (80, 220, 255, 255)); pv.alpha_composite(h, (x0, ex[0].height))
    pv.save(os.path.join(out, 'preview.png')); print('preview', os.path.join(out, 'preview.png'), len(ex), 'frames')
    if dry: sys.exit(0)
    kp = [[{'label': k, 'x': round(t[k][0] / me.width, 4), 'y': round(t[k][1] / me.height, 4)} for k in J] for t in tg]
    fk = [{'label': k, 'x': round(ours[k][0] / me.width, 4), 'y': round(ours[k][1] / me.height, 4)} for k in J]
    r = call('animate_with_skeleton_v3', {'description': desc, 'action': action, 'direction': dirn, 'keypoints': kp, 'first_frame_url': b64(me), 'first_frame_keypoints': fk, 'view': 'low top-down'})
    print(r[:600]); open(os.path.join(out, 'job.txt'), 'w').write(r)
