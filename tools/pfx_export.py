# pixelfx without Node (owner's PC has none): serve the pixelfx checkout (.tools/pixelfx, MIT) and a page that renders
# effects in the browser and posts transparent sprite sheets + the same JSON as `node tools/render.mjs --sheet` back here.
#   python tools/pfx_export.py [port=8765] [out dir=.tools/pfx_out]
#   then open http://localhost:8765/export.html in the built-in browser and run in the page:
#     await exportAll([["fire/meteor", 15], ["ice/frost-nova", 15, {"palette": ["#102", "#215", "#43a", "#8cf", "#fff"]}]])
#   -> <out>/<category>/<name>/<name>.png + .json (also works for new files under src/fx/<category>/, no index needed;
#      opts.as = another output name, e.g. a recoloured copy). Then tools/art/pixelfx_import.py brings sheets into fx/.
#   contact(id, fps, opts) posts <out>/<id>/contact.png (every frame on a dark backdrop, x3) to look at while drafting.
import http.server, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.tools', 'pixelfx')
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
OUT = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.tools', 'pfx_out'))
PAGE = r'''<!doctype html><meta charset="utf-8"><title>pixelfx export</title><body>pixelfx export
<script type="module">
import { effects } from "./src/fx/index.js";
import { createFrame, clearFrame, createFx, composite } from "./src/core/index.js";
function edgeFade(f, E = 8) {
  const { w, h, light: L } = f;
  for (let y = 0; y < h; y++) { const ey = Math.min(y, h - 1 - y);
    for (let x = 0; x < w; x++) { const e = Math.min(ey, x, w - 1 - x); if (e >= E) { x = w - 1 - E; continue; }
      const i = y * w + x, l = L[i]; if (!(l & 0xffffff)) continue; const u = (e + 0.5) / E, k = u * u * (3 - 2 * u);
      L[i] = (l & 0xff000000) | Math.round((l & 255) * k) | (Math.round(((l >>> 8) & 255) * k) << 8) | (Math.round(((l >>> 16) & 255) * k) << 16); } }
}
async function modOf(id) { return effects[id] || await import("./src/fx/" + id + ".js?v=" + Date.now()); }
async function frames(id, fps, opts = {}) {
  const mod0 = await modOf(id), meta = { fps: 30, bg: "dark", loop: false, duration: 1, tags: [], options: {}, ...mod0.meta }, mod = { ...mod0, meta };
  const [W, H] = meta.size, [OX, OY] = meta.origin; fps = fps || meta.fps;
  const n = Math.max(1, Math.round(meta.duration * fps) + (meta.loop ? 0 : 1));
  const { as, ...o } = opts, bare = createFrame(W, H, 0, 0), inst = createFx(mod, { x: OX, y: OY, seed: 1, ...o });
  const screen = W >= 320 && Math.abs(W / H - 16 / 9) < .05, out = [];
  for (let i = 0; i < n; i++) { if (i > 0) inst.update(1 / fps); clearFrame(bare); inst.draw(bare); if (!screen) edgeFade(bare);
    out.push(composite(bare, new Uint8ClampedArray(W * H * 4), null)); }
  return { meta, W, H, n, fps, out, name: as || id.split("/")[1], cat: id.split("/")[0] };
}
async function post(path, body) { await fetch("/save/" + path, { method: "POST", body }); }
window.exportOne = async (id, fps, opts) => {
  const r = await frames(id, fps, opts), { W, H, n } = r;
  const cols = Math.min(n, Math.max(1, Math.ceil(Math.sqrt((n * H) / W)))), rows = Math.ceil(n / cols);
  const cv = document.createElement("canvas"); cv.width = cols * W; cv.height = rows * H; const g = cv.getContext("2d");
  r.out.forEach((f, i) => g.putImageData(new ImageData(f, W, H), (i % cols) * W, Math.floor(i / cols) * H));
  const json = { meta: { pixelfx: { id, name: r.meta.name, fps: r.fps, loop: r.meta.loop, frames: n, frameSize: [W, H], pivot: r.meta.origin, columns: cols } } };
  await post(`${r.cat}/${r.name}/${r.name}.png`, await new Promise(k => cv.toBlob(k, "image/png")));
  await post(`${r.cat}/${r.name}/${r.name}.json`, JSON.stringify(json));
  return [id, r.name, n, W, H, r.meta.loop];
};
window.exportAll = async (list) => { const res = []; for (const [id, fps, opts] of list) res.push(await window.exportOne(id, fps, opts)); return res; };
window.contact = async (id, fps, opts) => {
  const r = await frames(id, fps, opts), { W, H, n } = r, k = 3, cols = Math.min(n, 8), rows = Math.ceil(n / cols);
  const cv = document.createElement("canvas"); cv.width = cols * (W * k + 4); cv.height = rows * (H * k + 4); const g = cv.getContext("2d");
  g.fillStyle = "#1a1724"; g.fillRect(0, 0, cv.width, cv.height); g.imageSmoothingEnabled = false;
  const t = document.createElement("canvas"); t.width = W; t.height = H; const tg = t.getContext("2d");
  r.out.forEach((f, i) => { tg.clearRect(0, 0, W, H); tg.putImageData(new ImageData(f, W, H), 0, 0); g.drawImage(t, (i % cols) * (W * k + 4) + 2, Math.floor(i / cols) * (H * k + 4) + 2, W * k, H * k); });
  await post(`${r.cat}/${r.name}/contact.png`, await new Promise(k2 => cv.toBlob(k2, "image/png")));
  return [id, n, W, H];
};
window.ready = true;
</script>'''
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def do_GET(self):
        if self.path.split('?')[0] == '/export.html':
            b = PAGE.encode(); self.send_response(200); self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b); return
        super().do_GET()
    def end_headers(self): self.send_header('Cache-Control', 'no-store'); super().end_headers()
    def do_POST(self):
        if not self.path.startswith('/save/') or '..' in self.path: self.send_error(400); return
        p = os.path.join(OUT, *self.path[6:].split('/')); os.makedirs(os.path.dirname(p), exist_ok=True)
        n = int(self.headers.get('Content-Length', 0)); open(p, 'wb').write(self.rfile.read(n))
        self.send_response(200); self.end_headers(); self.wfile.write(b'ok')
    def log_message(self, *a): pass
print('serving', ROOT, 'on', PORT, '->', OUT, flush=True)
http.server.ThreadingHTTPServer(('127.0.0.1', PORT), H).serve_forever()
