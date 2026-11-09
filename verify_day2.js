const { chromium } = require('playwright-core');
(async () => {
  const b = await chromium.launch({ channel: 'msedge', headless: true });
  const p = await b.newPage({ viewport: { width: 1500, height: 860 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8090/mcd-city.html', { waitUntil: 'load' });
  await p.waitForTimeout(600);
  await p.evaluate(() => {
    const S = { day:3, minute:22*60+58, cash:12400, price:1.05, reputation:0.78, weather:'rain',
      staff:{counter:2,cook:3,packer:1,rider:2},
      stock:{patty:60,bun:80,fry:40,chicken:35,drink:120,coffee:50},
      deliveryCap:0, orders:[], nextOrderId:100, counters:{dine:2,deliver:1}, inStore:[], riders:[],
      stats:{revenue:8640,cost:3629,dine:132,deliver:96,served:228,lost:11,waste:3,
        items:{big:48,chick:41,fry:30,drink:36,coffee:22,chickn:29,mug:22},
        hourly:{revenue:[],orders:[],dine:[],deliver:[]}},
      history:[], events:[], adCampaign:0, stockoutAlert:false };
    localStorage.setItem('mcd-city-save', JSON.stringify({state:S, speed:1}));
  });
  await p.reload({ waitUntil: 'load' });
  await p.waitForTimeout(1500);
  await p.waitForTimeout(2500);
  const shown = await p.evaluate(() => document.getElementById('modalWrap').classList.contains('on'));
  console.log('日结算弹窗:', shown);
  if (shown) {
    console.log('结算:', (await p.textContent('#modal')).replace(/\n+/g,' | '));
    await p.click('#modal .btn');
    await p.waitForTimeout(1500);
    console.log('跨天:', await p.evaluate(() => document.getElementById('dayLabel').textContent + ' ' + document.getElementById('clock').textContent));
    await p.click('#tabs button[data-t="report"]');
    await p.waitForTimeout(700);
    console.log('报表:', (await p.textContent('#p-report')).slice(0,240).replace(/\n+/g,' | '));
    await p.screenshot({ path:'shot_day_ok.png' });
  }
  console.log('ERRORS:', errs.length ? errs : 'none');
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });
