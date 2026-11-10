# The owner's Berserker Q sheet (2026-11-10, "Q โซ่รวบวิญญาณ", 6x4 cells of 320 px on flat green): black chains with a neon
# red rim fan out from the caster, snap back, then a black ring cleave round him breaks into smoke.
# Two game sheets come out of it:
#   fx/pfx_bzchain.png  chains, anchor = the caster's ring on the left of each cell, pointing right (the game turns it)
#   fx/pfx_bzring.png   the ring cleave, anchor = the ring centre, squashed to a ground ellipse (x 1, y .55)
#   python3 tools/art/bz_chain_import.py [art/incoming/pfx/bz_chain_sheet.png]
import json, sys
import numpy as np
from PIL import Image

src = sys.argv[1] if len(sys.argv) > 1 else 'art/incoming/pfx/bz_chain_sheet.png'
im = np.asarray(Image.open(src).convert('RGB')).astype(np.int16)
C = 320

def key(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]; mx = np.maximum(r, b); d = g - mx
    al = np.clip((95 - d) / 55.0, 0, 1)                       # flat green (0,166,53) has d ~ 113
    sp = d > 0                                                 # despill: the effect is only black and red, so green-tinted
    g2 = np.where(sp, np.minimum(g, r // 2), g)                # (half see-through smoke) pixels lose their green and teal
    b2 = np.where(sp, np.minimum(b, r * 6 // 10 + 8), b)
    return np.dstack([r, g2, b2, (al * 255).astype(np.int16)]).clip(0, 255).astype(np.uint8)

cells = [key(im[(i // 6) * C:(i // 6 + 1) * C, (i % 6) * C:(i % 6 + 1) * C]) for i in range(24)]

def sheet(frames, name, ax, ay, sy=1.0, fps=24):
    fr = [Image.fromarray(f) for f in frames]
    if sy != 1: fr = [f.resize((f.width, round(f.height * sy)), Image.LANCZOS) for f in fr]
    # crop every frame to the union box round the content, keep the anchor
    box = None
    for f in fr:
        b = f.getbbox()
        if b: box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
    x0, y0, x1, y1 = box; x0 = max(0, x0 - 2); y0 = max(0, y0 - 2); w, h = x1 - x0 + 2, y1 - y0 + 2
    cols = min(8, len(fr)); rows = -(-len(fr) // cols); out = Image.new('RGBA', (w * cols, h * rows))
    for i, f in enumerate(fr): out.paste(f.crop((x0, y0, x0 + w, y0 + h)), ((i % cols) * w, (i // cols) * h))
    out.save(f'fx/{name}.png', optimize=True)
    m = dict(w=w, h=h, n=len(fr), cols=cols, fps=fps, ax=round(ax - x0), ay=round(ay * sy - y0), src=f"owner's Berserker Q sheet ({src}), tools/art/bz_chain_import.py")
    print(name, m); return m

man = json.load(open('fx/manifest.json'))
# chains: frames 0-5 fan out, 12-14 snap back (rows 1 and 2 repeat the fan, so only row 1 is used); caster ring ~ (32, 200) in a cell
man['pfx_bzchain'] = sheet([cells[i] for i in (0, 1, 2, 3, 4, 5, 12, 13, 14)], 'pfx_bzchain', 34, 200, fps=18)
# ring: frames 18-20 (ring + smoke) then 21-23 (it breaks into smoke), the ring centre ~ (160, 180) in those cells
man['pfx_bzring'] = sheet([cells[i] for i in (15, 18, 19, 20, 16, 21, 22, 23)], 'pfx_bzring', 160, 172, sy=.55, fps=16)
json.dump(man, open('fx/manifest.json', 'w'), separators=(',', ':'))
