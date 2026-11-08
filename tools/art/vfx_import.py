# A vfx_workbench export (the plain sheet: <name>.png + <name>.json, TexturePacker style) -> fx/<key>.png + an
# fx/manifest.json entry (w h n cols fps ax ay) for action.html's pfx(). Blank frames at the end are dropped.
#   python tools/art/vfx_import.py <dir with the export> <export name> <key> [loop]
import sys, json, os, subprocess
from PIL import Image

src, name, key = sys.argv[1], sys.argv[2], sys.argv[3]
loop = 'loop' in sys.argv[4:]
j = json.load(open(os.path.join(src, name + '.json'), encoding='utf-8'))
fr = j['frames'] if isinstance(j['frames'], list) else list(j['frames'].values())
im = Image.open(os.path.join(src, name + '.png')).convert('RGBA')
w, h = fr[0]['frame']['w'], fr[0]['frame']['h']
cells = [im.crop((f['frame']['x'], f['frame']['y'], f['frame']['x'] + w, f['frame']['y'] + h)) for f in fr]
while len(cells) > 1 and cells[-1].getbbox() is None: cells.pop()          # blank tail
out = Image.new('RGBA', (w * len(cells), h))
for i, c in enumerate(cells): out.paste(c, (i * w, 0))
os.makedirs('fx', exist_ok=True); out.save(f'fx/{key}.png', optimize=True)
piv = fr[0].get('pivot', {'x': .5, 'y': .5}); dur = fr[0].get('duration', 83)
orig = subprocess.run(['git', 'show', 'HEAD:fx/manifest.json'], capture_output=True, text=True, encoding='utf-8').stdout
m = json.load(open('fx/manifest.json', encoding='utf-8'))
m[key] = {'w': w, 'h': h, 'n': len(cells), 'cols': len(cells), 'fps': round(1000 / dur), 'ax': round(piv['x'] * w), 'ay': round(piv['y'] * h),
          **({'loop': 1} if loop else {}), 'src': f'PixelLab vfx_workbench "{name}"'}
compact = orig and '\n' not in orig.strip()
open('fx/manifest.json', 'w', encoding='utf-8').write(json.dumps(m, separators=(',', ':')) if compact else json.dumps(m, indent=1))
print(key, m[key])
