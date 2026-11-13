# Chibi swordsman: slash combo frames — queue for Codex

Owner 2026-11-13: the new chibi pixel swordsman needs his sword combo, following the motion of a sketch sheet. Reply to the
owner in Thai, short and plain. "ทำท่าฟัน" / "ทำท่าฟันต่อ" = the first `todo` row below.

## Rules
- ONE picture per row: attach the two pictures named in the row (the numbered pose sheet first, the character second) and
  use the row's prompt as it is. Make the picture with the built-in image tool.
- The pose sheet is ONLY a motion reference (a rough sketch of another figure): copy the poses, never its look.
  The character must stay exactly the one in `CHAR_swordsman16_side.png` in every cell, the same size in every cell.
- Save full size PNG (not shrunk, not re-pixelised) as the row's file; add one Thai line per file to
  `art/incoming/chibi_sword/REPORT_TH.txt` (a pose that does not match its cell, a frame crossing a cell, a changed face or
  costume, a missing cell).
- Do row 1 first and stop: the owner and Claude look at it before the other rows are made.
- Mark the row `done` here. Branch `codex/chibi-slash`, open a pull request, never merge, never push to `main`. When you
  stop, switch the folder back with `git checkout main`.

## Queue
| # | key | move | status | file |
|---|-----|------|--------|------|
| 1 | slash_A | two fast horizontal slashes | todo | `art/incoming/chibi_sword/slash_A.png` |
| 2 | slash_B | overhead chop, then winding into a spin | todo | `art/incoming/chibi_sword/slash_B.png` |
| 3 | slash_C | spin, dash, wide slash | todo | `art/incoming/chibi_sword/slash_C.png` |
| 4 | slash_D | follow-through back to the ready stance | todo | `art/incoming/chibi_sword/slash_D.png` |

## Prompts

### Row 1: slash_A
Attach, in this order: `art/poses/ref_sketch/slash_A.png` (pose sheet), `art/poses/ref_sketch/CHAR_swordsman16_side.png` (the character).

```
The FIRST picture is a motion reference: 8 numbered cells in a grid, a rough sketch of a small swordsman doing two fast horizontal slashes, left to right and back. Cell 1 is the start. Use it ONLY for the poses and the timing (body lean, legs, where the sword is, how big the slash arc is). Do not copy that sketch character's look.

The SECOND picture is the character to draw: a chibi pixel-art swordsman (dark violet messy hair with an ahoge, violet eyes, torn red scarf-cape, white shirt, brown belt and gauntlets, dark trousers, brown boots, a straight silver sword with a gold guard in his right hand). Draw THIS character once in every cell, in the same pose as the sketch figure of that cell.

Rules:
- The same character in all 8 cells: same face, hair, colours, outfit and proportions as the second picture, the SAME SIZE in every cell, in the same chunky 16-bit pixel-art style (square pixels on one grid, dark outline, 3 shade steps), seen from the side, facing RIGHT unless the sketch figure of that cell is turned.
- Keep the grid and the order 1 to 8 (left to right, top row first). One figure per cell with empty space around it, feet on the same ground line, nothing crossing into another cell.
- Where the sketch shows a slash arc, draw a clean white-blue slash arc of the same shape and size, kept inside its own cell. No other effects, no dust, no shadow.
- Do NOT draw the numbers or the cell borders.
- Plain flat pure white background. Landscape picture, 1536 x 1024.
```

### Row 2: slash_B
Attach, in this order: `art/poses/ref_sketch/slash_B.png` (pose sheet), `art/poses/ref_sketch/CHAR_swordsman16_side.png` (the character).

```
The FIRST picture is a motion reference: 8 numbered cells in a grid, a rough sketch of a small swordsman doing an overhead chop down to the ground, then winding into a spin. Cell 1 is the start. Use it ONLY for the poses and the timing (body lean, legs, where the sword is, how big the slash arc is). Do not copy that sketch character's look.

The SECOND picture is the character to draw: a chibi pixel-art swordsman (dark violet messy hair with an ahoge, violet eyes, torn red scarf-cape, white shirt, brown belt and gauntlets, dark trousers, brown boots, a straight silver sword with a gold guard in his right hand). Draw THIS character once in every cell, in the same pose as the sketch figure of that cell.

Rules:
- The same character in all 8 cells: same face, hair, colours, outfit and proportions as the second picture, the SAME SIZE in every cell, in the same chunky 16-bit pixel-art style (square pixels on one grid, dark outline, 3 shade steps), seen from the side, facing RIGHT unless the sketch figure of that cell is turned.
- Keep the grid and the order 1 to 8 (left to right, top row first). One figure per cell with empty space around it, feet on the same ground line, nothing crossing into another cell.
- Where the sketch shows a slash arc, draw a clean white-blue slash arc of the same shape and size, kept inside its own cell. No other effects, no dust, no shadow.
- Do NOT draw the numbers or the cell borders.
- Plain flat pure white background. Landscape picture, 1536 x 1024.
```

### Row 3: slash_C
Attach, in this order: `art/poses/ref_sketch/slash_C.png` (pose sheet), `art/poses/ref_sketch/CHAR_swordsman16_side.png` (the character).

```
The FIRST picture is a motion reference: 8 numbered cells in a grid, a rough sketch of a small swordsman doing a spinning slash (frames 1-3), then a running dash into a wide slash (frames 4-8). Cell 1 is the start. Use it ONLY for the poses and the timing (body lean, legs, where the sword is, how big the slash arc is). Do not copy that sketch character's look.

The SECOND picture is the character to draw: a chibi pixel-art swordsman (dark violet messy hair with an ahoge, violet eyes, torn red scarf-cape, white shirt, brown belt and gauntlets, dark trousers, brown boots, a straight silver sword with a gold guard in his right hand). Draw THIS character once in every cell, in the same pose as the sketch figure of that cell.

Rules:
- The same character in all 8 cells: same face, hair, colours, outfit and proportions as the second picture, the SAME SIZE in every cell, in the same chunky 16-bit pixel-art style (square pixels on one grid, dark outline, 3 shade steps), seen from the side, facing RIGHT unless the sketch figure of that cell is turned.
- Keep the grid and the order 1 to 8 (left to right, top row first). One figure per cell with empty space around it, feet on the same ground line, nothing crossing into another cell.
- Where the sketch shows a slash arc, draw a clean white-blue slash arc of the same shape and size, kept inside its own cell. No other effects, no dust, no shadow.
- Do NOT draw the numbers or the cell borders.
- Plain flat pure white background. Landscape picture, 1536 x 1024.
```

### Row 4: slash_D
Attach, in this order: `art/poses/ref_sketch/slash_D.png` (pose sheet), `art/poses/ref_sketch/CHAR_swordsman16_side.png` (the character).

```
The FIRST picture is a motion reference: 4 numbered cells in a grid, a rough sketch of a small swordsman doing the end of the dash slash: follow-through and back to the ready stance. Cell 1 is the start. Use it ONLY for the poses and the timing (body lean, legs, where the sword is, how big the slash arc is). Do not copy that sketch character's look.

The SECOND picture is the character to draw: a chibi pixel-art swordsman (dark violet messy hair with an ahoge, violet eyes, torn red scarf-cape, white shirt, brown belt and gauntlets, dark trousers, brown boots, a straight silver sword with a gold guard in his right hand). Draw THIS character once in every cell, in the same pose as the sketch figure of that cell.

Rules:
- The same character in all 4 cells: same face, hair, colours, outfit and proportions as the second picture, the SAME SIZE in every cell, in the same chunky 16-bit pixel-art style (square pixels on one grid, dark outline, 3 shade steps), seen from the side, facing RIGHT unless the sketch figure of that cell is turned.
- Keep the grid and the order 1 to 4 (left to right, top row first). One figure per cell with empty space around it, feet on the same ground line, nothing crossing into another cell.
- Where the sketch shows a slash arc, draw a clean white-blue slash arc of the same shape and size, kept inside its own cell. No other effects, no dust, no shadow.
- Do NOT draw the numbers or the cell borders.
- Plain flat pure white background. Landscape picture, 1536 x 512.
```
