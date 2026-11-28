// RigForge 2D check (rigforge.html = the owner's GPT-made 2D rig / animation tool, added 2026-11-28; manual tools/rigforge/MANUAL_TH.md).
// python3 -m http.server 8000 ; node tools/qa/rigforge_check.js [out prefix]   -> at 1280 x 720 and 844 x 390: the three rigs, play, the game test
// (wave + ultimate), export (sprite sheet .png + rig .json downloads), import of the sample green-screen sheet (parts cut); exit 1 on a failure or page error.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');

async function checkJointEditing(pg, touch) {
  await pg.click('#btnNewClip');
  await pg.click('#btnSubSetup');
  await pg.locator('#stageCanvas').scrollIntoViewIfNeeded();
  await pg.waitForFunction(() => !!state.worldJoints.head);
  const jointPoint = id => pg.evaluate(id => {
    const rect = stageCanvas.getBoundingClientRect(), joint = state.worldJoints[id];
    return { x: rect.left + joint.x, y: rect.top + joint.y };
  }, id);
  const session = touch ? await pg.context().newCDPSession(pg) : null;
  async function drag(start, dx, dy) {
    if (session) {
      await session.send('Input.dispatchTouchEvent', {type:'touchStart', touchPoints:[start]});
      await session.send('Input.dispatchTouchEvent', {type:'touchMove', touchPoints:[{x:start.x+dx, y:start.y+dy}]});
      await session.send('Input.dispatchTouchEvent', {type:'touchEnd', touchPoints:[]});
    } else {
      await pg.mouse.move(start.x, start.y);
      await pg.mouse.down();
      await pg.mouse.move(start.x+dx, start.y+dy, {steps:4});
      await pg.mouse.up();
    }
    await pg.evaluate(() => new Promise(requestAnimationFrame));
  }
  const initial = await jointPoint('head');
  await drag(initial, 12, -8);
  const after = await jointPoint('head');
  assert.ok(Math.abs(after.x-initial.x-12) < 2 && Math.abs(after.y-initial.y+8) < 2, 'Setup drag follows pointer');
  const boneState = () => pg.evaluate(() => JSON.stringify(state.bones));
  const moved = await boneState();
  await pg.click('#btnJointGuides');
  await pg.locator('#stageCanvas').scrollIntoViewIfNeeded();
  await drag(await jointPoint('head'), -15, 10);
  assert.equal(await boneState(), moved, 'hidden guides cannot move a joint');
  await pg.click('#btnJointGuides');
  await pg.click('#btnSubAnimate');
  await pg.click('#btnToggleSlotVis');
  assert.equal(await pg.evaluate(() => sampleClipPose(state.currentClip, 0).head.vis), 0, 'slot hidden in saved key');
  await pg.click('#btnToggleSlotVis');
  assert.equal(await pg.evaluate(() => sampleClipPose(state.currentClip, 0).head.vis), 1, 'slot restored');
  await pg.locator('#stageCanvas').scrollIntoViewIfNeeded();
  const hand = await jointPoint('handR');
  const elbow = await jointPoint('armLowerR');
  const dx = (elbow.x - hand.x) / 3, dy = (elbow.y - hand.y) / 3;
  await drag(hand, dx, dy);
  const posed = await jointPoint('handR');
  assert.ok(Math.hypot(posed.x - hand.x - dx, posed.y - hand.y - dy) < 2, 'IK hand reaches target');
  const clipState = () => pg.evaluate(() => JSON.stringify(state.clips[state.currentClip]));
  const posedClip = await clipState();
  const canvas = await pg.locator('#stageCanvas').boundingBox();
  await drag({x:canvas.x+12, y:canvas.y+canvas.height/2}, 8, 8);
  assert.equal(await clipState(), posedClip, 'empty stage drag leaves keys alone');
  if (session) await session.detach();
}

async function checkSeam(pg) {
  const colors = await pg.evaluate(async () => {
    const canvas = document.createElement('canvas');
    canvas.width = canvas.height = 48;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#101010';
    ctx.fillRect(8, 8, 32, 32);
    ctx.fillStyle = '#40b0ff';
    ctx.fillRect(10, 10, 28, 28);
    ctx.fillStyle = '#101010';
    ctx.fillRect(20, 14, 4, 1);
    const image = new Image();
    image.src = erasePartSeamInCanvas(canvas, 'top');
    await image.decode();
    ctx.clearRect(0, 0, 48, 48);
    ctx.drawImage(image, 0, 0);
    return [[20, 8], [20, 14], [8, 8], [20, 7]].map(([x, y]) => [...ctx.getImageData(x, y, 1, 1).data]);
  });
  assert.deepEqual(colors, [[64,176,255,255], [16,16,16,255], [16,16,16,255], [0,0,0,0]]);
}
(async () => { const out = process.argv[2] || '/tmp/rigforge', b = await chromium.launch(), res = {};
  for (const [W, H] of [[1280, 720], [844, 390]]) {
    const pg = await (await b.newContext({ viewport: { width: W, height: H }, hasTouch: W < 900, acceptDownloads: true })).newPage(), errs = [];
    pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await pg.goto(new URL('rigforge.html', process.env.RIGFORGE_URL || 'http://localhost:8000/').href); await pg.waitForTimeout(3500);
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
    await pg.click('#btnCloseImport');
    await checkJointEditing(pg, W < 900);
    await checkSeam(pg);
    r.errors = [...new Set(errs)].slice(0, 6); res[W] = r; await pg.close(); }
  let ok = true; for (const [W, r] of Object.entries(res)) { const good = ['play', 'parts', 'single', 'zeus', 'game', 'editor', 'export', 'sheet', 'json', 'close', 'import'].every(k => r[k] === 'ok') && r.sheetFile && r.jsonFile && r.sliced > 5 && !r.errors.length;
    console.log((good ? 'ok  ' : 'FAIL') + ` ${W}: buttons ok, downloads ${r.sheetFile} + ${r.jsonFile}, sample sheet cut into ${r.sliced} parts` + (r.errors.length ? ', ERRORS ' + r.errors.join(' | ') : '')); if (!good) ok = false; }
  console.log(ok ? 'RIGFORGE OK' : 'RIGFORGE FAIL'); await b.close(); process.exit(ok ? 0 : 1); })();
