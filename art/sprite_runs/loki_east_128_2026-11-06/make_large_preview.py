from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FINAL = ROOT / "128" / "final"
OUT = ROOT / "loki-east-all-actions-large-preview.png"

rows = [
    ("IDLE - EAST - 4 FRAMES", Image.open(FINAL / "idle-sheet-clean.png").convert("RGBA")),
    ("ATTACK - FANG CROSS SLASH - EAST - 6 FRAMES", Image.open(FINAL / "attack-sheet-clean.png").convert("RGBA")),
    ("SKILL - KING OF TRICKS - EAST - 6 FRAMES", Image.open(FINAL / "skill-sheet-clean.png").convert("RGBA")),
]

cell = 128
cols = 6
label_h = 34
pad = 20
base_w = cols * cell
base_h = len(rows) * (cell + label_h) + pad * 2
preview = Image.new("RGBA", (base_w + pad * 2, base_h), (25, 21, 35, 255))
draw = ImageDraw.Draw(preview)
font = ImageFont.load_default(size=18)

for row_i, (label, sheet) in enumerate(rows):
    y = pad + row_i * (cell + label_h)
    draw.text((pad, y), label, fill=(245, 225, 155, 255), font=font)
    y += label_h
    for gy in range(0, cell, 16):
        for gx in range(0, base_w, 16):
            c = (62, 61, 73, 255) if (gx // 16 + gy // 16) % 2 == 0 else (46, 45, 56, 255)
            draw.rectangle((pad + gx, y + gy, pad + gx + 15, y + gy + 15), fill=c)
    preview.alpha_composite(sheet, (pad, y))
    for c in range(cols + 1):
        x = pad + c * cell
        draw.line((x, y, x, y + cell), fill=(130, 119, 147, 150), width=1)
    draw.rectangle((pad, y, pad + base_w, y + cell), outline=(195, 174, 215, 220), width=1)

preview = preview.resize((preview.width * 2, preview.height * 2), Image.Resampling.NEAREST)
preview.save(OUT)
print(f"wrote {OUT}")
