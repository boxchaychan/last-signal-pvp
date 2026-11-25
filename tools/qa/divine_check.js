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

  await page.goto('http://127.0.0.1:4173/divine.html', { waitUntil: 'networkidle' });
  await page.screenshot({ path: '/tmp/divine-title.png', fullPage: true });
  await page.goto('http://127.0.0.1:4173/divine.html?skip=1', { waitUntil: 'networkidle' });
  await page.waitForFunction(() => window.DC && window.DC.G());
  const result = await page.evaluate(() => {
    DC.place('shiba', 0);
    for (let i = 0; i < 900; i++) DC.step(1 / 60);
    const state = DC.G();
    return {
      wave: state.wave,
      units: state.units.length,
      mobs: state.mobs.length,
      kills: state.kills,
      hp: state.hp,
      gold: state.gold,
    };
  });
  await page.screenshot({ path: '/tmp/divine-game.png', fullPage: true });
  console.log(JSON.stringify({ errors, result }));
  await browser.close();
  if (errors.length || result.units !== 1) process.exit(1);
})();
