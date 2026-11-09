/**
 * 游戏验证脚本：用真实浏览器跑一段时间，检查渲染与经营逻辑。
 */
const { chromium } = require('playwright-core');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ channel: 'msedge', headless: true });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));

  await page.goto('http://127.0.0.1:8090/mcd-city.html', { waitUntil: 'load' });
  await page.waitForTimeout(1000);

  // 加速到 8x
  await page.click('#speedBtns button[data-s="8"]');
  await page.waitForTimeout(12000);

  const state1 = await page.evaluate(() => ({
    clock: document.getElementById('clock').textContent,
    day: document.getElementById('dayLabel').textContent,
    cash: document.getElementById('cashLb').textContent,
    kpis: [...document.querySelectorAll('#p-op .kpi')].map(k => k.querySelector('.lb').textContent + '=' + k.querySelector('.vl').textContent),
    store: document.querySelector('#p-op .card:nth-of-type(3)') ? null : null
  }));
  console.log('--- 12s @8x ---');
  console.log(JSON.stringify(state1, null, 1));

  // canvas 是否真的画了东西（非纯色）
  const canvasInfo = await page.evaluate(() => {
    const c = document.getElementById('stage');
    const g = c.getContext('2d');
    const d = g.getImageData(0, 0, c.width, c.height).data;
    const colors = new Set();
    for (let i = 0; i < d.length; i += 4 * 997) {
      colors.add(d[i] + ',' + d[i+1] + ',' + d[i+2]);
    }
    return { w: c.width, h: c.height, distinctColors: colors.size };
  });
  console.log('canvas:', JSON.stringify(canvasInfo));

  // 切到各标签页验证不报错
  for (const t of ['order', 'staff', 'supply', 'report']) {
    await page.click(`#tabs button[data-t="${t}"]`);
    await page.waitForTimeout(500);
    const visible = await page.evaluate(tt => {
      const el = document.getElementById('p-' + tt);
      return { on: el.classList.contains('on'), len: el.innerHTML.length, text: el.innerText.slice(0, 80).replace(/\n/g, ' | ') };
    }, t);
    console.log('tab', t, JSON.stringify(visible));
  }

  // 交互：加派人员
  await page.click('#tabs button[data-t="staff"]');
  await page.waitForTimeout(300);
  const before = await page.textContent('#p-staff');
  await page.click('#p-staff [data-step="cook"][data-d="1"]');
  await page.waitForTimeout(400);
  const after = await page.textContent('#p-staff');
  console.log('加派后厨人数变化:', before !== after ? 'YES' : 'NO');

  // 交互：采购原料
  await page.click('#tabs button[data-t="supply"]');
  await page.waitForTimeout(300);
  const cashBefore = await page.textContent('#cashLb');
  await page.click('#p-supply [data-buy="patty"]');
  await page.waitForTimeout(500);
  const cashAfter = await page.textContent('#cashLb');
  console.log('采购后资金:', cashBefore, '->', cashAfter);

  // 交互：广告投放
  await page.click('#tabs button[data-t="op"]');
  await page.waitForTimeout(300);
  await page.click('#p-op [data-act="ad"]');
  await page.waitForTimeout(400);
  console.log('广告后事件流:', (await page.textContent('#p-op .events')).slice(0, 120).replace(/\n/g, ' | '));

  // 订单页检查
  await page.click('#tabs button[data-t="order"]');
  await page.waitForTimeout(400);
  console.log('订单页文本:', (await page.textContent('#p-order')).slice(0, 260).replace(/\n/g, ' | '));

  await page.screenshot({ path: 'shot_game.png' });
  console.log('CONSOLE ERRORS:', errors.length ? errors.slice(0, 8) : 'none');
  await browser.close();
})().catch(e => { console.error('FATAL', e); process.exit(1); });
