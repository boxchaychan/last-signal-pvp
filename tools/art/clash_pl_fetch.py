"""Fetch a finished 64-slot create_1_direction_object review pack (clash.html batches) and make the numbered pick sheet. FREE (select + download).
  python3 tools/art/clash_pl_fetch.py <batch dir> <review object id> <tag>
-> <dir>/select.txt, object_ids.json (key -> object id), raw/<key>.png, sheet_numbered.png (8 x 8, numbers = key suffix, 4x pixels on grey).
Key names come from <dir>/keys.json (written by the batch script). Downloads go through api.pixellab.ai (the backblaze host is blocked here)."""
import json, os, re, sys, io, urllib.request
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')); os.environ.setdefault('PL_KEY', 'proxy-injected')
from pl_rpc import call
from PIL import Image, ImageDraw
d, oid, tag = sys.argv[1], sys.argv[2], sys.argv[3]; keys = json.load(open(os.path.join(d, 'keys.json')))
sel_f = os.path.join(d, 'select.txt')
if not os.path.exists(sel_f):
    r = call('select_object_frames', {'object_id': oid, 'indices': list(range(len(keys))), 'common_tag': tag}); open(sel_f, 'w').write(r)
txt = open(sel_f).read(); m = re.search(r'new_ids:\s*([0-9a-f, -]+)', txt); ids = [s.strip() for s in m.group(1).split(',') if s.strip()]
assert len(ids) == len(keys), (len(ids), len(keys), txt[:300])
json.dump(dict(zip(keys, ids)), open(os.path.join(d, 'object_ids.json'), 'w'), indent=1)
os.makedirs(os.path.join(d, 'raw'), exist_ok=True); KEY = os.environ['PL_KEY']
for k, i in zip(keys, ids):
    f = os.path.join(d, 'raw', k + '.png')
    if os.path.exists(f): continue
    for t in range(4):
        try:
            data = urllib.request.urlopen(urllib.request.Request(f'https://api.pixellab.ai/mcp/objects/{i}/download', headers={'Authorization': 'Bearer ' + KEY}), timeout=60).read(); break
        except Exception as e:
            if t == 3: raise
    if data[:2] == b'PK':   # a zip: take the first png inside
        import zipfile; z = zipfile.ZipFile(io.BytesIO(data)); n = next(x for x in z.namelist() if x.lower().endswith('.png')); data = z.read(n)
    open(f, 'wb').write(data)
ims = [Image.open(os.path.join(d, 'raw', k + '.png')).convert('RGBA') for k in keys]; S = max(max(im.size) for im in ims); Z = 4; C = S * Z + 18
sheet = Image.new('RGBA', (8 * C, ((len(keys) + 7) // 8) * C), (92, 98, 92, 255)); dr = ImageDraw.Draw(sheet)
for n, (k, im) in enumerate(zip(keys, ims)):
    x, y = (n % 8) * C, (n // 8) * C; dr.rectangle([x + 1, y + 1, x + C - 2, y + C - 2], outline=(60, 64, 60, 255))
    sheet.alpha_composite(im.resize((im.width * Z, im.height * Z), Image.NEAREST), (x + 9 + (S - im.width) * Z // 2, y + 16 + (S - im.height) * Z))
    lab = k.split('_')[-1]; dr.rectangle([x + 3, y + 3, x + 3 + 8 * len(lab), y + 15], fill=(20, 16, 12, 255)); dr.text((x + 5, y + 3), lab, fill=(255, 230, 120, 255))
sheet.save(os.path.join(d, 'sheet_numbered.png')); print('ok', len(keys), 'sprites, slot', S, 'px ->', os.path.join(d, 'sheet_numbered.png'))
