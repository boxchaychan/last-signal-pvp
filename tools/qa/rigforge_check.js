// RigForge 2D check (rigforge.html = the owner's GPT-made 2D rig / animation tool, added 2026-11-28; manual tools/rigforge/MANUAL_TH.md).
// python3 -m http.server 8000 ; node tools/qa/rigforge_check.js [out prefix]   -> at 1280 x 720 and 844 x 390: the three rigs, play, the game test
// (wave + ultimate), export (sprite sheet .png + rig .json downloads), import of the sample green-screen sheet (parts cut); exit 1 on a failure or page error.
const { chromium } = require('playwright');
(async () => { const out = process.argv[2] || '/tmp/rigforge', b = await chromium.launch(), res = {};
  for (const [W, H] of [[1280, 720], [844, 390]]) {
    const pg = await (await b.newContext({ viewport: { width: W, height: H }, hasTouch: W < 900, acceptDownloads: true })).newPage(), errs = [];
    pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await pg.goto('http://localhost:8000/rigforge.html'); await pg.waitForTimeout(3500);
    const shot = async n => pg.screenshot({ path: `${out}_${W}_${n}.png` });
    await shot('zeus');
    const clk = async id => { const e = await pg.$('#' + id); if (!e) return 'missing'; const v = await e.isVisible(); if (!v) return 'hidden'; await e.click(); await pg.waitForTimeout(900); return 'ok'; };
    const r = {};
    r.play = await clk('btnPlayPause'); await pg.waitForTimeout(1200); await shot('zeus_play');
    r.parts = await clk('btnRigParts'); await pg.waitForTimeout(800); await shot('poseidon');
    r.single = await clk('btnRigSingle'); await pg.waitForTimeout(800); await shot('single');
    r.zeus = await clk('btnRigZeus');
    r.game = await clk('btnModePlaytest'); await pg.waitForTimeout(1500); await pg.keyboard.press('w'); await pg.waitForTimeout(1500); await pg.keyboard.press('f'); await pg.waitForTimeout(1200); await shot('game');
    r.editor = await clk('btnModeEditor');
    r.export = await clk('btnOpenExport'); await pg.waitForTimeout(1500); await shot('export');
    const dl = pg.waitForEvent('download', { timeout: 15000 }).catch(() => null); r.sheet = await clk('btnDownloadSheet'); const d = await dl; r.sheetFile = d ? d.suggestedFilename() : null; if (d) await d.saveAs(`${out}_${W}_sheet.png`);
    const dl2 = pg.waitForEvent('download', { timeout: 15000 }).catch(() => null); r.json = await clk('btnDownloadJson'); const d2 = await dl2; r.jsonFile = d2 ? d2.suggestedFilename() : null; if (d2) await d2.saveAs(`${out}_${W}_rig.json`);
    r.close = await clk('btnCloseExport');
    r.import = await clk('btnOpenImport'); await shot('import');
    try { const [fc] = await Promise.all([pg.waitForEvent('filechooser', { timeout: 5000 }), pg.click('#btnPickSheetFile')]); await fc.setFiles('tools/rigforge/samples/zeus_16parts_greenscreen.jpg'); await pg.waitForTimeout(4000); r.sliced = await pg.evaluate(() => document.querySelectorAll('#slicedPartsGrid > *').length); await shot('import_sliced'); } catch (e) { r.importErr = e.message.slice(0, 80); }
    r.errors = [...new Set(errs)].slice(0, 6); res[W] = r; await pg.close(); }
  let ok = true; for (const [W, r] of Object.entries(res)) { const good = ['play', 'parts', 'single', 'zeus', 'game', 'editor', 'export', 'sheet', 'json', 'close', 'import'].every(k => r[k] === 'ok') && r.sheetFile && r.jsonFile && r.sliced > 5 && !r.errors.length;
    console.log((good ? 'ok  ' : 'FAIL') + ` ${W}: buttons ok, downloads ${r.sheetFile} + ${r.jsonFile}, sample sheet cut into ${r.sliced} parts` + (r.errors.length ? ', ERRORS ' + r.errors.join(' | ') : '')); if (!good) ok = false; }
  console.log(ok ? 'RIGFORGE OK' : 'RIGFORGE FAIL'); await b.close(); process.exit(ok ? 0 : 1); })();
