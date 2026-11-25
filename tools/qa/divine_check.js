const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ executablePath: '/usr/bin/chromium' });
  const page = await (await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 1,
    hasTouch: true,
  })).newPage();
  const errors = [];
  page.on('pageerror', error => errors.push(String(error)));
  page.on('console', message => {
    if (message.type() === 'error') errors.push(message.text());
  });

  const base = process.env.QA_BASE || 'http://127.0.0.1:4173';
  await page.goto(base + '/divine.html', { waitUntil: 'networkidle' });
  await page.waitForFunction(() => window.DIVINE && window.DIVINE.state());
  await page.click('#summon');
  await page.click('#boss');
  const result = await page.evaluate(() => {
    const state = DIVINE.state();
    state.gold = 10000;
    for (let i = 0; i < 19; i++) DIVINE.summon();
    state.grid[0].tier = 'MYTHIC';
    state.grid[0].awakened = false;
    state.selected = 0;
    state.core = 1;
    DIVINE.awakenSelected();
    for (let i = 0; i < 900; i++) DIVINE.step();
    return {
      wave: state.wave,
      slots: state.grid.length,
      units: state.grid.filter(Boolean).length,
      awakened: state.grid[0].awakened,
      mobs: state.mobs.length,
      kills: state.kills,
      gold: state.gold,
    };
  });
  await page.screenshot({ path: '/tmp/divine-game.png', fullPage: true });
  console.log(JSON.stringify({ errors, result }));
  await browser.close();
  if (errors.length || result.slots !== 18 || result.units !== 18 || !result.awakened) process.exit(1);
})();
