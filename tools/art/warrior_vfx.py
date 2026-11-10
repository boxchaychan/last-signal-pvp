# Frostwindz "Pixel Art Animations - Warrior FREE" (owner's zip 2026-11-09, itch.io frostwindz; licence: use in games, modify,
# NO redistribution of the files, so the zip and its frames are NOT kept in this public repo, only the cut sheets the game
# loads). Five red pixel slash effects, 128 px frames facing right:
#   python3 tools/art/warrior_vfx.py <unzipped folder>  -> fx/wvfx1..5.png + fx/manifest.json
import sys, glob, re, json
from PIL import Image
src = sys.argv[1]; man = json.load(open('fx/manifest.json'))
for v in range(1, 6):
    fs = sorted(glob.glob(f'{src}/VFX {v}/Frames/*.png'), key=lambda f: int(re.findall(r'frame(\d+)', f)[0]))
    n = len(fs); out = Image.new('RGBA', (128 * n, 128))
    for i, f in enumerate(fs): out.alpha_composite(Image.open(f).convert('RGBA'), (i * 128, 0))
    out.save(f'fx/wvfx{v}.png', optimize=True)
    man[f'wvfx{v}'] = {'w': 128, 'h': 128, 'n': n, 'cols': n, 'fps': 20, 'ax': 64, 'ay': 64, 'src': f'Frostwindz Warrior FREE VFX {v} (itch.io, no redistribution)'}
json.dump(man, open('fx/manifest.json', 'w'), separators=(',', ':')); print('ok')
