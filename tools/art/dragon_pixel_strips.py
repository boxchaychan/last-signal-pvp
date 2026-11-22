"""Turn the dragon's fitted painted moves (art/dune/hero, same body size, feet on the ground) into true pixel strips for pixmap.html.

  python tools/art/dragon_pixel_strips.py [body_px=48]

-> art/pixmap/dragon<body_px>/<move>.png + .json {n, w, h, foot, fps}: one row of frames, feet on one row, body centred.
Effects drawn in the frames stay. Free (no generator). Colours: tools/art/pixel_punch.py on the whole strip, so a move keeps one palette.
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image

BODY = int(sys.argv[1]) if len(sys.argv) > 1 else 48
PAINTED_BODY = 233 * .82                   # the idle body in art/dune/hero (feet to top of the head)
K = BODY / PAINTED_BODY; OUT = f'art/pixmap/dragon{BODY}'; os.makedirs(OUT, exist_ok=True)
MOVES = {'idle': ('hero_idle', 10), 'run': ('hero_run', 22), 'attack1': ('hero_attack1', 34), 'attack2': ('hero_attack2', 34), 'attack3': ('hero_attack3', 30), 'skill_dash': ('hero_skill_dash', 24), 'hurt': ('hero_hurt', 24), 'death': ('hero_death', 14)}
sp = json.load(open('art/dune/sprites.json'))
for name, (key, fps) in MOVES.items():
    m = sp[key]; im = Image.open(m['src']).convert('RGBA'); dy = m.get('dy') or [0] * m['n']; dx = m.get('dx') or [0] * m['n']
    L = max(m['cx'] - d for d in dx) + 2; R = max(m['w'] - m['cx'] + d for d in dx) + 2; U = max(m['foot'] - d for d in dy) + 2; D = max(m['h'] - m['foot'] + d for d in dy) + 2
    W, H = int(L + R), int(U + D); w, h = max(1, round(W * K)), max(1, round(H * K)); foot = round(U * K); frames = []
    for i in range(m['n']):
        x, y = (i % m['cols']) * m['w'], (i // m['cols']) * m['h']; c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); f = im.crop((x, y, x + m['w'], y + m['h'])); c.paste(f, (int(L - m['cx'] + dx[i]), int(U - m['foot'] + dy[i])))
        p = np.array(c).astype(float); p[..., :3] *= p[..., 3:] / 255; s = np.array(Image.fromarray(p.astype(np.uint8), 'RGBA').resize((w, h), Image.BOX)).astype(float); a = s[..., 3:] / 255
        s[..., :3] = np.where(a > 0, s[..., :3] / np.maximum(a, 1e-3), 0); s[..., 3] = (s[..., 3] > 112) * 255; frames.append(s.astype(np.uint8))
    raw = f'{OUT}/_{name}.png'; Image.fromarray(np.hstack(frames), 'RGBA').save(raw)
    subprocess.run([sys.executable, 'tools/art/pixel_punch.py', raw, f'{OUT}/{name}.png', '1.0', '32'], check=True); os.remove(raw)
    json.dump({'n': m['n'], 'w': w, 'h': h, 'foot': foot, 'fps': fps, 'cx': round(L * K / w - .5, 4)}, open(f'{OUT}/{name}.json', 'w')); print(f'{name:11} {w}x{h} foot {foot}')
