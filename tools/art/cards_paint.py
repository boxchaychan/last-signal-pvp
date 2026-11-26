"""Painted card pictures for cards.html (owner's ChatGPT / Gemini card art, 2026-11-26).
Each raw picture is a whole card drawn by GPT (frame, name ribbon, stars, stat bars with gacha numbers).
Makes two game files per card, the raw stays untouched in art/incoming/monstercards/gpt/:
  art/cards/p_<key>_full.jpg  the whole card, the baked numbers painted out (cards.html writes ours in the bars) -> zoom / summon splash
  art/cards/p_<key>_art.jpg   the picture inside the frame, cut to the board card shape (54 x 74) -> board + hand cards
usage: python3 tools/art/cards_paint.py lubu"""
import sys
from PIL import Image

CARDS = {
    # raw file, erase boxes (x0, y0, x1, y1, sample column) in raw pixels, art crop box
    'lubu': ('art/incoming/monstercards/gpt/lubu_card_raw.png',
             [(320, 1300, 486, 1357, 312), (806, 1300, 990, 1357, 799)],
             (264, 44, 926, 951)),
}

def erase(im, box):
    x0, y0, x1, y1, sx = box; px = im.load()
    for y in range(y0, y1):
        c = px[sx, y]
        for x in range(x0, x1):
            k = 1 - .2 * (x - x0) / (x1 - x0)   # the bars darken a little to the right
            px[x, y] = tuple(int(v * k) for v in c)

def build(key):
    raw, boxes, crop = CARDS[key]
    im = Image.open(raw).convert('RGB')
    full = im.copy()
    for b in boxes: erase(full, b)
    full.resize((540, 720), Image.LANCZOS).save(f'art/cards/p_{key}_full.jpg', quality=90)
    im.crop(crop).resize((330, 452), Image.LANCZOS).save(f'art/cards/p_{key}_art.jpg', quality=90)
    print('ok', key, im.size)

if __name__ == '__main__':
    for k in sys.argv[1:] or CARDS: build(k)
