/** 验证原生 <a> 入口：真实点击应打开新标签页到游戏 */
const { chromium } = require('playwright-core');
(async () => {
  const b = await chromium.launch({ channel: 'msedge', headless: true });
  const ctx = await b.newContext({ viewport: { width: 1500, height: 860 } });
  const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('https://workbuddy.link/p/kn5a1cVtzPsecrCno2Z8O2', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await p.waitForTimeout(14000);
  const ws = p.frames().find(f => f !== p.mainFrame());
  const info = await ws.evaluate(() => {
    const el = document.getElementById('mcd-entry');
    return { tag: el ? el.tagName : null, href: el ? el.getAttribute('href') : null, target: el ? el.getAttribute('target') : null,
             txt: el ? el.innerText.replace(/\n/g,' ') : null };
  });
  console.log('入口:', JSON.stringify(info));
  const popupPromise = ctx.waitForEvent('page', { timeout: 20000 }).catch(()=>null);
  // 用 Playwright 对 iframe 内元素做真实点击
  await ws.click('#mcd-entry', { timeout: 10000 }).catch(e => console.log('click err:', e.message));
  const popup = await popupPromise;
  console.log('新标签页:', popup ? popup.url() : '未捕获');
  if (popup) {
    await popup.waitForLoadState('domcontentloaded', { timeout: 30000 });
    await popup.waitForTimeout(13000);
    const gf = popup.frames().find(f => f !== popup.mainFrame());
    const gi = gf ? await gf.evaluate(() => ({ title: document.title, clock:(document.getElementById('clock')||{}).textContent, stage:!!document.getElementById('stage') })).catch(e=>({e:e.message})) : { title: popup.title() };
    console.log('游戏内容:', JSON.stringify(gi));
    await popup.screenshot({ path:'shot_link_game.png' });
  }
  console.log('ERRORS:', errs.length ? errs : 'none');
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });
