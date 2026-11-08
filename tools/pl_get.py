# Download files a PixelLab tool reply points at ("download https://api.pixellab.ai/mcp/pixel-tools/<id>/: a.gif, a.json, a.png").
#   python tools/pl_get.py <base url ending in /> <out dir> <file> [<file> ...]      (key from PL_KEY, see pl_rpc.py)
import sys, os, urllib.request
KEY = os.environ.get('PL_KEY') or sys.exit('PL_KEY not set')
base, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
for f in sys.argv[3:]:
    req = urllib.request.Request(base + f, headers={'Authorization': 'Bearer ' + KEY})
    data = urllib.request.urlopen(req, timeout=120).read()
    open(os.path.join(out, f), 'wb').write(data); print(f, len(data))
