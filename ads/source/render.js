// usage: node render.js test 0.9,1.5,...   |   node render.js full [workers]
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const DIR = __dirname, URL = 'file://' + path.join(DIR, 'ad.html');
const FPS = 30, DUR = 20, N = FPS * DUR;
(async () => {
  const mode = process.argv[2] || 'test';
  const b = await chromium.launch({ args: ['--no-sandbox', '--force-color-profile=srgb', '--font-render-hinting=none'] });
  async function open() {
    const c = await b.newContext({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
    const p = await c.newPage();
    p.on('pageerror', e => console.error('PAGEERR', e.message));
    p.on('console', m => { if (m.type() === 'error') console.error('CONSOLE', m.text()); });
    await p.goto(URL);
    const info = await p.evaluate(() => window.ready);
    return { p, info };
  }
  if (mode === 'test') {
    const times = (process.argv[3] || '1').split(',').map(Number);
    const out = path.join(DIR, 'test'); fs.mkdirSync(out, { recursive: true });
    const { p, info } = await open(); console.log('anims', JSON.stringify(info));
    for (const t of times) {
      await p.evaluate(t => window.seek(t), t);
      await p.screenshot({ path: path.join(out, 't' + t.toFixed(2).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 88 });
    }
  } else {
    const W = Number(process.argv[3] || 4);
    const out = path.join(DIR, 'out'); fs.mkdirSync(out, { recursive: true });
    await Promise.all([...Array(W)].map(async (_, w) => {
      const { p } = await open();
      for (let i = w; i < N; i += W) {
        await p.evaluate(t => window.seek(t), i / FPS);
        await p.screenshot({ path: path.join(out, 'f' + String(i).padStart(4, '0') + '.jpg'), type: 'jpeg', quality: 97 });
        if (i % 60 === w) console.log('frame', i);
      }
    }));
  }
  await b.close(); console.log('DONE');
})().catch(e => { console.error(e); process.exit(1); });
