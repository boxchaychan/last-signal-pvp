#!/usr/bin/env python3
# Joins the frames of tools/qa/bag3d_cast.js into contact sheets: one row an item (3 moments), 12 rows a sheet.
# python3 tools/qa/bag3d_cast_sheet.py <folder of frames> [rows per sheet 12]
import json, sys, os
from PIL import Image, ImageDraw
d = sys.argv[1]; per = int(sys.argv[2]) if len(sys.argv) > 2 else 12
ids = json.load(open(os.path.join(d, 'ids.json')))
W, H = 422, 145
for s in range(0, len(ids), per):
    part = ids[s:s + per]; sh = Image.new('RGB', (W * 3, H * len(part)), '#000'); dr = ImageDraw.Draw(sh)
    for r, k in enumerate(part):
        for i in range(3):
            f = os.path.join(d, f'{k}_{i}.png')
            if os.path.exists(f): sh.paste(Image.open(f).convert('RGB').resize((W, H), Image.LANCZOS), (i * W, r * H))
        dr.rectangle((0, r * H, 150, r * H + 14), fill='#000'); dr.text((3, r * H + 1), k, fill='#ffe27a')
    sh.save(os.path.join(d, f'sheet_{s // per}.png')); print('sheet', s // per, part)
