# Build one effect with PixelLab's free vfx_workbench and bring it into the game in one go.
#   python tools/pl_vfx.py <export name> <fx key> '<part json>' [fps]          (key from PL_KEY, see pl_rpc.py)
# = start, add_part (the json: name + its sliders), export, download the sheet, tools/art/vfx_import.py -> fx/<key>.png.
import sys, os, json, re, subprocess, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
from pl_rpc import call, KEY

def step(argv):
    r = call('vfx_workbench', {'argv': argv})
    m = re.search(r'effect step: (\S+)', r)
    return r, (m.group(1) if m else None)

def make(name, key, part, fps=20):
    _, sid = step(['start', '--fps', str(fps)])
    r, sid = step([sid, 'add_part', json.dumps(part)])
    ok = re.search(r'render ok[^\n]*', r); print(key, ok.group(0) if ok else r[:300])
    r, _ = step([sid, 'export', '--name', name])
    url = re.search(r'download (https://\S+/):', r).group(1); nm = name.replace('_', '-')
    out = os.path.join('art', 'incoming', 'fx_raw', name); os.makedirs(out, exist_ok=True)
    for f in (nm + '.json', nm + '.png'):
        req = urllib.request.Request(url + f, headers={'Authorization': 'Bearer ' + KEY})
        open(os.path.join(out, f), 'wb').write(urllib.request.urlopen(req, timeout=120).read())
    subprocess.run([sys.executable, 'tools/art/vfx_import.py', out, nm, key], check=True)

if __name__ == '__main__':
    make(sys.argv[1], sys.argv[2], json.loads(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else 20)
