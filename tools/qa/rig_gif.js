// A move of a rig as a GIF / strip, drawn exactly like a game draws it (rig2d/bones.js player + rig2d/fx.js effects), 30 frames a second.
// python3 -m http.server 8000 ; node tools/qa/rig_gif.js <char> <move> <out.gif> [stand seconds before .25] [size 360]
//   also writes <out>.strip.png (every 3rd frame) and prints the move events.
const { chromium } = require('playwright'), fs = require('fs'), { execFileSync } = require('child_process'), path = require('path');
(async () => {
  const [ch, mv, out, pre, size] = process.argv.slice(2), dir = out + '.frames'; fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  const b = await chromium.launch(), pg = await (await b.newContext({ viewport: { width: 400, height: 300 } })).newPage(), errs = []; pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto('http://localhost:8000/rig.html?char=' + ch + '&play=0&t=' + Date.now()); await pg.waitForFunction(() => typeof Bones2D !== 'undefined' && typeof Bones2DFX !== 'undefined', null, { timeout: 20000 });
  const r = await pg.evaluate(async ([ch, mv, pre, size]) => {
    const B = Bones2D, rig = await B.load(`art/rigs/${ch}.json?` + Date.now()), S = +size || 360, W = Math.round(S * 1.9), H = S, c = document.createElement('canvas'); c.width = W; c.height = H; const g = c.getContext('2d');
    const P = B.player(rig, { base: 'idle' }), FX = Bones2DFX.create(), sc = (H * .78) / (rig.figH || rig.size[1]), fx0 = W * ((rig.clips && rig.clips[mv] ? (rig.clips[mv].dirx || 1) < 0 : rig.flip) ? .66 : .3), fy = H * .9, frames = [], ev = [];
    P.play('idle'); const steps = Math.round((+pre || .25) * 30); for (let i = 0; i < steps; i++) P.update(1 / 30);
    P.play(mv, { restart: true }); if (rig.bake) B.bake(rig); const dur = (B.MOVES[mv] && B.MOVES[mv].dur) || (rig.clips && rig.clips[mv] && rig.clips[mv].dur) || 1, n = Math.round((dur + .55) * 30);
    for (let i = 0; i < n; i++) { P.update(1 / 30); g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; const gr = g.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, '#36407a'); gr.addColorStop(1, '#1d2244'); g.fillStyle = gr; g.fillRect(0, 0, W, H); g.fillStyle = '#2c3566'; g.fillRect(0, fy, W, H - fy); g.fillStyle = '#00000044'; g.beginPath(); g.ellipse(fx0, fy + 3, 70 * sc * 2.2, 9, 0, 0, 7); g.fill();
      P.draw(g, fx0, fy, sc, false); FX.step(P, 1 / 30, { scale: sc * 2.4, width: W, height: H, range: W * .55 }); FX.draw(g); if (P.fired.length) ev.push([i, P.fired.join(',')]); frames.push(c.toDataURL('image/png')); }
    return { frames, ev, n }; }, [ch, mv, pre, size]);
  r.frames.forEach((u, i) => fs.writeFileSync(path.join(dir, String(i).padStart(3, '0') + '.png'), Buffer.from(u.split(',')[1], 'base64')));
  execFileSync('python3', ['-c', `import glob,sys
from PIL import Image
fs=sorted(glob.glob(sys.argv[1]+'/*.png')); ims=[Image.open(f).convert('RGB') for f in fs]
ims[0].save(sys.argv[2],save_all=True,append_images=ims[1:],duration=33,loop=0)
pick=ims[::3]; w,h=ims[0].size; k=.5; sh=Image.new('RGB',(int(w*k)*min(8,len(pick)), int(h*k)*(-(-len(pick)//8))))
for i,im in enumerate(pick): sh.paste(im.resize((int(w*k),int(h*k))),(i%8*int(w*k),i//8*int(h*k)))
sh.save(sys.argv[2]+'.strip.png')`, dir, out]);
  console.log(r.n, 'frames', 'events', JSON.stringify(r.ev), errs.length ? 'ERRORS ' + errs.slice(0, 4).join(' | ') : 'no errors'); await b.close();
})();
