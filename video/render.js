const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const tl = JSON.parse(fs.readFileSync(path.join(__dirname, 'timeline.json')));
  const fps = +(process.env.FPS || 30), out = process.argv[2] || path.join(__dirname, 'frames');
  const only = process.argv[3] ? process.argv[3].split(',').map(Number) : null;
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 720, height: 1280 } });
  await pg.goto('file://' + path.join(__dirname, 'render.html'));
  await pg.evaluate(t => window.setup(t), tl);
  const times = only || Array.from({ length: Math.ceil(tl.total * fps) }, (_, i) => i / fps);
  for (let i = 0; i < times.length; i++) {
    const d = await pg.evaluate(t => window.renderFrame(t), times[i]);
    fs.writeFileSync(path.join(out, (only ? 'p_' + times[i] : String(i).padStart(5, '0')) + '.jpg'), Buffer.from(d.split(',')[1], 'base64'));
  }
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
