# Call a PixelLab MCP tool straight over HTTP with the key in the PL_KEY environment variable (never printed).
# For when the Claude app still holds an older key (owner switched PixelLab accounts 2026-11-08).
#   PowerShell: $env:PL_KEY=[Environment]::GetEnvironmentVariable('PIXELLAB_API_KEY','User'); python tools/pl_rpc.py <tool> '<json args>'
#   python tools/pl_rpc.py --upload <file.png> ...      -> prints upload:<id> refs (get_upload_url + multipart POST)
import sys, os, json, urllib.request, uuid

KEY = os.environ.get('PL_KEY') or sys.exit('PL_KEY not set')
URL = 'https://api.pixellab.ai/mcp'

def call(tool, args):
    body = json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call', 'params': {'name': tool, 'arguments': args}}).encode()
    req = urllib.request.Request(URL, body, {'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json',
                                             'Accept': 'application/json, text/event-stream'})
    txt = urllib.request.urlopen(req, timeout=120).read().decode()
    out = []
    for line in txt.splitlines():
        if line.startswith('data:'):
            d = json.loads(line[5:])
            for c in d.get('result', {}).get('content', []):
                if c.get('type') == 'text': out.append(c['text'])
                elif c.get('type') == 'image' and os.environ.get('PL_IMG'):   # replies with pictures (vfx_workbench frames)
                    import base64, time
                    os.makedirs(os.environ['PL_IMG'], exist_ok=True)
                    f = os.path.join(os.environ['PL_IMG'], f'{int(time.time() * 1000)}_{len(out)}.' + c.get('mimeType', 'image/png').split('/')[-1])
                    open(f, 'wb').write(base64.b64decode(c['data'])); out.append(f'[saved image: {f}]')
            if 'error' in d: out.append('ERROR ' + json.dumps(d['error']))
    return '\n'.join(out)

def upload(path):
    up = call('get_upload_url', {})
    url = next(l.strip() for l in up.splitlines() if l.strip().startswith('https://api.pixellab.ai/v2/uploads/'))
    bnd = uuid.uuid4().hex; data = open(path, 'rb').read()
    body = (f'--{bnd}\r\nContent-Disposition: form-data; name="file"; filename="{os.path.basename(path)}"\r\n'
            f'Content-Type: image/png\r\n\r\n').encode() + data + f'\r\n--{bnd}--\r\n'.encode()
    req = urllib.request.Request(url, body, {'Content-Type': 'multipart/form-data; boundary=' + bnd})
    return json.loads(urllib.request.urlopen(req, timeout=120).read().decode())['ref']

if __name__ == '__main__':
    if sys.argv[1] == '--upload':
        for p in sys.argv[2:]: print(os.path.basename(p), upload(p))
    else:
        # args: '<json>' | @file.json | name=value ... (PowerShell 5.1 strips the double quotes of a JSON argument)
        args = {}
        for a in sys.argv[2:]:
            if a.startswith('@'): args.update(json.load(open(a[1:], encoding='utf-8-sig')))
            elif a.startswith('{'): args.update(json.loads(a))
            else:
                k, v = a.split('=', 1)
                try: args[k] = json.loads(v)
                except ValueError: args[k] = v
        print(call(sys.argv[1], args))
