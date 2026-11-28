# joins the frames of tools/qa/bag3d_isk.js into contact sheets: <out>/sheet_arena.png, <out>/sheet_duel.png (one row per skill kind)
# python3 tools/qa/bag3d_isk_sheet.py <out> [scale .5]
import sys, json, os
from PIL import Image, ImageDraw
out = sys.argv[1]; sc = float(sys.argv[2]) if len(sys.argv) > 2 else .5
kinds = list(json.load(open(os.path.join(out, 'kinds.json'))).keys())
for part, n in (('arena', 2), ('duel', 3)):
    rows = []
    for k in kinds:
        fr = [os.path.join(out, f'{part}_{k}_{i}.png') for i in range(n)]
        if not all(os.path.exists(f) for f in fr): continue
        ims = [Image.open(f).convert('RGB') for f in fr]; ims = [im.resize((int(im.width * sc), int(im.height * sc))) for im in ims]
        row = Image.new('RGB', (sum(im.width for im in ims) + 90, ims[0].height), (20, 16, 24)); x = 90
        for im in ims: row.paste(im, (x, 0)); x += im.width
        ImageDraw.Draw(row).text((6, 6), k, fill=(255, 226, 122)); rows.append(row)
    if not rows: continue
    for c in range(0, len(rows), 8):
        part_rows = rows[c:c + 8]; sh = Image.new('RGB', (part_rows[0].width, sum(r.height for r in part_rows)), (0, 0, 0)); y = 0
        for r in part_rows: sh.paste(r, (0, y)); y += r.height
        sh.save(os.path.join(out, f'sheet_{part}_{c // 8}.png'))
print('sheets in', out)
