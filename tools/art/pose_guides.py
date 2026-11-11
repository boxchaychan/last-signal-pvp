# Owner 2026-11-11 "ไม่รู้ว่าจะทำท่าทางแบบไหน": pose guide sheets for the Codex queue, made from the moves we already have
# (the v4 Berserker's PixelLab side-view clips in art/action/bz4, same kind of character, same greatsword). Each guide is a
# numbered grid of grey silhouettes on white (the pose only, so the generator copies the MOTION and not the old design),
# with the hit frame marked in red. -> art/incoming/side/berserker/poses/<action>_POSES.png + a preview GIF per move.
import json, os, numpy as np
from PIL import Image, ImageDraw, ImageFont
B = 'art/action/bz4/'; M = json.load(open(B + 'bz4.json')); CW, CH = M['cw'], M['ch']
OUT = 'art/incoming/side/berserker/poses/'; os.makedirs(OUT, exist_ok=True)
def frames(clip):
    im = Image.open(B + clip + '.png').convert('RGBA'); return [im.crop((i * CW, 0, (i + 1) * CW, CH)) for i in range(M['n'][clip])]
def pick(fr, n):                                  # n evenly spaced frames
    return [fr[round(i * (len(fr) - 1) / max(1, n - 1))] for i in range(n)] if n < len(fr) else fr
# action -> (clip, frames wanted, grid cols, hit frame number (1-based) or 0)
JOBS = {'idle': ('idle', 8, 4, 0), 'run': ('run', 12, 6, 0), 'attack1': ('sweep', 12, 6, 3), 'attack3': ('vert', 12, 6, 6),
        'hurt': ('hurt', 8, 4, 0), 'death': ('death', 12, 6, 0), 'chain': ('chain', 12, 6, 3), 'spin': ('spin', 12, 6, 0),
        'slam': ('leap', 16, 4, 6), 'roll': ('roll', 12, 6, 0)}
try: font = ImageFont.load_default(size=28)
except TypeError: font = ImageFont.load_default()
S = 1.6
for act, (clip, n, cols, hit) in JOBS.items():
    fr = pick(frames(clip), n); rows = (len(fr) + cols - 1) // cols; cw, ch = int(CW * S), int(CH * S)
    sheet = Image.new('RGB', (cw * cols, ch * rows), (255, 255, 255)); d = ImageDraw.Draw(sheet); gif = []
    for i, f in enumerate(fr):
        a = np.asarray(f).copy(); m = a[..., 3] > 0
        sil = np.zeros_like(a); sil[m] = (150, 150, 158, 255)        # grey silhouette: the pose, not the old design
        g = Image.fromarray(sil).resize((cw, ch), Image.NEAREST); x, y = (i % cols) * cw, (i // cols) * ch
        sheet.paste(g, (x, y), g); col = (220, 30, 40) if hit and i + 1 == hit else (60, 60, 60)
        d.rectangle((x, y, x + cw - 1, y + ch - 1), outline=(200, 200, 200)); d.text((x + 10, y + 6), str(i + 1) + (' HIT' if hit and i + 1 == hit else ''), fill=col, font=font)
        c = Image.new('RGBA', f.size, (255, 255, 255, 255)); c.alpha_composite(f); gif.append(c.resize((cw, ch), Image.NEAREST).convert('RGB').quantize(255))
    sheet.save(OUT + act + '_POSES.png')
    gif[0].save(OUT + act + '_preview.gif', save_all=True, append_images=gif[1:], duration=90, loop=0)
    print(act, clip, len(fr), sheet.size)
