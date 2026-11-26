"""Cut each god's idle picture into parts (body, head, weapon arm, free arm) for divine.html, so the arm really swings. Free, original pixels.
  python3 tools/art/divine_rig.py
Owner 2026-11-26 "ตัวละครง่ายๆ เองนะ ตัวเล็กๆ": the reference genre moves the pieces of a character with keyframes, so we do the same.
Shapes are hand-set per god in the 512 frame (feet at 256,500). The body is under-painted with its own nearest colours where the head and arms
covered it, so no hole shows when they turn. Parts are scaled like the god sets (Zeus idle body 322 px -> 200 px).
-> art/divine/rig_<set>_<part>.png + art/divine/rig.json {set: {part: {x, y, w, h, px, py}}} (x, y, px, py relative to the feet = x 256, y bottom of the idle picture; scaled px)"""
import json, os
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'); D = os.path.join(R, 'art/divine'); F = 200 / 322; AX, AY = 256, 500
RIG = {
  'zeus': {'arm': ([(116, 183), (180, 183), (180, 288), (224, 292), (227, 338), (208, 350), (212, 372), (210, 418), (148, 418), (116, 340)], (218, 312)),
           'arm2': ([(327, 296), (390, 296), (390, 386), (327, 386)], (331, 306)), 'head': (lambda x, y: (y <= 286) & (x >= 182), (252, 284))},
  'thor': {'arm': ([(138, 290), (224, 290), (226, 352), (242, 362), (244, 396), (224, 402), (214, 474), (156, 474), (138, 400)], (236, 375)),
           'arm2': ([(311, 381), (352, 381), (354, 442), (311, 442)], (316, 388)), 'head': (lambda x, y: (y <= 343) & (x >= 214), (268, 340))},
  'anubis': {'arm': ([(132, 168), (192, 168), (192, 300), (206, 316), (224, 328), (224, 366), (197, 373), (186, 506), (132, 506)], (216, 346)),
             'arm2': ([(306, 341), (352, 341), (352, 422), (306, 422)], (310, 352)), 'head': (lambda x, y: (y <= 302) & (x >= 190), (262, 300))},
}
out = {}
for name, spec in RIG.items():
    a = np.array(Image.open(os.path.join(D, name, 'idle_key.png')).convert('RGBA')); H, W = a.shape[:2]; AY = int(np.where(a[..., 3] > 0)[0].max()) + 1; fig = a[..., 3] > 16; yy, xx = np.mgrid[0:H, 0:W]
    def poly(pts):
        m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon(pts, fill=1); return np.array(m).astype(bool)
    arm = fig & poly(spec['arm'][0]); arm2 = fig & poly(spec['arm2'][0]) & ~arm; head = fig & spec['head'][0](xx, yy) & ~arm & ~arm2; body = fig & ~arm & ~arm2 & ~head
    parts = {'body': body, 'arm2': arm2, 'head': head, 'arm': arm}; rgb = a[..., :3]
    # under-paint the body: inside its own row span (and up to 18 px under the chin) fill covered pixels with the nearest body colour
    span = np.zeros_like(body)
    for r in np.where(body.any(1))[0]: xs_ = np.where(body[r])[0]; span[r, xs_.min():xs_.max() + 1] = True
    neck = head & (yy > spec['head'][1][1] - 18) & nd.binary_dilation(body, iterations=18)
    fill = ((span & fig) | neck) & ~body
    idx = nd.distance_transform_edt(~body, return_distances=False, return_indices=True)
    bpx = a.copy(); bpx[fill, :3] = rgb[idx[0], idx[1]][fill]; bpx[..., 3] = np.where(body | fill, a[..., 3], 0); bpx[fill, 3] = 255
    o = {}
    for pn, m in parts.items():
        src = bpx if pn == 'body' else np.where(m[..., None], a, 0).astype(np.uint8)
        al = src[..., 3] > 0; ys, xs = np.where(al); x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
        im = Image.fromarray(src[y0:y1, x0:x1]); w, h = max(1, round(im.width * F)), max(1, round(im.height * F)); im.resize((w, h), Image.LANCZOS).save(os.path.join(D, f'rig_{name}_{pn}.png'))
        piv = spec[pn][1] if pn != 'body' else (AX, AY)
        o[pn] = {'x': round((x0 - AX) * F, 2), 'y': round((y0 - AY) * F, 2), 'w': w, 'h': h, 'px': round((piv[0] - AX) * F, 2), 'py': round((piv[1] - AY) * F, 2)}
    out[name] = o
    chk = Image.new('RGBA', (W, H)); chk.alpha_composite(Image.fromarray(a)); cols = {'body': (90, 160, 255), 'arm2': (255, 200, 60), 'head': (120, 230, 120), 'arm': (255, 90, 90)}
    for pn, m in parts.items():
        c = np.zeros((H, W, 4), np.uint8); c[m] = (*cols[pn], 110); chk.alpha_composite(Image.fromarray(c))
    chk.crop(Image.fromarray(a).getbbox()).save(os.path.join(R, 'art/incoming/divine_game', f'rig_check_{name}.png'))
json.dump(out, open(os.path.join(D, 'rig.json'), 'w'), indent=1); print(json.dumps(out)[:300])
