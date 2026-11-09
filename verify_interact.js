/** 线上交互回归：所有按钮点击必须生效（验证 DOM 重建不再吞掉点击） */
const { chromium } = require('playwright-core');
(async () => {
  const b = await chromium.launch({ channel: 'msedge', headless: true });
  const p = await b.newPage({ viewport: { width: 1500, height: 860 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('https://workbuddy.link/p/6fpJOhy9hjgnF16Qq3MOsZ', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await p.waitForTimeout(12000);
  const fr = p.frames().find(f => f !== p.mainFrame());
  const click = async (sel) => { await fr.click(sel); await fr.waitForTimeout(600); };
  const val = async (sel) => fr.evaluate(s => (document.querySelector(s)||{}).textContent, sel);

  // 总览：价格调整
  await fr.click('#tabs button[data-t="op"]'); await fr.waitForTimeout(600);
  const hintBefore = await val('#op-hint');
  await click('#p-op [data-act="price-up"]');
  const hintAfter = await val('#op-hint');
  console.log('价格调整:', hintBefore!==hintAfter ? '生效' : '未生效');

  // 人力：加派后厨
  await fr.click('#tabs button[data-t="staff"]'); await fr.waitForTimeout(600);
  const cookBefore = await fr.evaluate(() => document.querySelector('[data-step="cook"]').parentElement.querySelector('b').textContent);
  await click('#p-staff [data-step="cook"][data-d="1"]');
  const cookAfter = await fr.evaluate(() => document.querySelector('[data-step="cook"]').parentElement.querySelector('b').textContent);
  console.log('加派后厨:', cookBefore+' -> '+cookAfter, cookBefore!==cookAfter?'生效':'未生效');

  // 供应链：采购
  await fr.click('#tabs button[data-t="supply"]'); await fr.waitForTimeout(600);
  const stockBefore = await val('#stock-patty');
  const cashBefore = await val('#sp-cash');
  await click('#p-supply [data-buy="patty"]');
  const stockAfter = await val('#stock-patty');
  const cashAfter = await val('#sp-cash');
  console.log('采购肉饼:', stockBefore+' -> '+stockAfter, '| 资金:', cashBefore.trim(), '->', cashAfter.trim());

  // 报表：保存
  await fr.click('#tabs button[data-t="report"]'); await fr.waitForTimeout(600);
  await click('#p-report [data-act="save"]');
  console.log('保存状态:', (await val('#rp-save')).trim());

  // 订单页渲染
  await fr.click('#tabs button[data-t="order"]'); await fr.waitForTimeout(600);
  console.log('订单页:', (await fr.textContent('#p-order')).slice(0,120).replace(/\n+/g,' | '));

  console.log('ERRORS:', errs.length ? errs : 'none');
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });
