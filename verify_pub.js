/** 线上双页验证：工作台（含 3D 小屋 + 游戏入口）+ 城市麦当劳 3D 游戏 */
const { chromium } = require('playwright-core');

(async () => {
  const browser = await chromium.launch({ channel: 'msedge', headless: true });
  const ctx = await browser.newContext({ viewport: { width: 1500, height: 900 } });
  const p = await ctx.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));

  // 1) 工作台
  await p.goto('https://workbuddy.link/p/kn5a1cVtzPsecrCno2Z8O2', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await p.waitForTimeout(15000);
  const wsFrame = p.frames().find(f => f !== p.mainFrame());
  const ws = wsFrame ? await wsFrame.evaluate(() => {
    const entry = document.getElementById('mcd-entry');
    return {
      title: document.title,
      hasCanvas: document.querySelectorAll('canvas').length > 0,
      entry: !!entry,
      entryText: entry ? entry.innerText.replace(/\n/g, ' ') : '',
      entryHref: entry ? entry.getAttribute('href') : ''
    };
  }) : { err: 'no frame' };
  console.log('工作台:', JSON.stringify(ws));
  await p.screenshot({ path: 'shot_pub_ws.png' });

  // 2) 游戏（3D）
  const p2 = await ctx.newPage();
  p2.on('pageerror', e => errs.push('GAME PAGEERROR: ' + e.message));
  await p2.goto('https://workbuddy.link/p/6fpJOhy9hjgnF16Qq3MOsZ', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await p2.waitForTimeout(15000);
  const gf = p2.frames().find(f => f !== p2.mainFrame());
  const gm = gf ? await gf.evaluate(() => {
    const St = window.__STAGE__;
    return {
      title: document.title,
      clock: (document.getElementById('clock') || {}).textContent,
      stage: St ? { ready: St.ready, models: Object.keys(St.models).length,
                    actors: (St.actors || []).length, vehicles: (St.vehicles || []).length } : null,
      kpis: [...document.querySelectorAll('#p-op .kpi')].map(k =>
        k.querySelector('.lb').textContent + '=' + k.querySelector('.vl').textContent)
    };
  }) : { err: 'no frame' };
  console.log('游戏:', JSON.stringify(gm));
  await p2.screenshot({ path: 'shot_pub_game.png' });

  console.log('ERRORS:', errs.length ? errs.slice(0, 5) : 'none');
  await browser.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });
