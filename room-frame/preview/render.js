// node render.js [view ...]  -> renders/<view>.png  (serves room-frame/ on :8765)
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
(async () => {
  const root = path.resolve(__dirname, '..');
  const srv = spawn('python3', ['-m', 'http.server', '8765', '--bind', '127.0.0.1'], { cwd: root, stdio: 'ignore' });
  await new Promise(r => setTimeout(r, 800));
  const views = process.argv.slice(2).length ? process.argv.slice(2) : ['front', 'angle', 'left', 'centre', 'right', 'table'];
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  try {
    for (const v of views) {
      const p = await b.newPage({ viewport: { width: 1800, height: 1200 } });
      p.on('pageerror', e => console.log('PAGEERROR', v, e.message));
      p.on('console', m => { if (m.type() === 'error') console.log('CONSOLE', v, m.text()); });
      await p.goto(`http://127.0.0.1:8765/preview/viewer.html?view=${v}`);
      await p.waitForFunction(() => window.__done === true, null, { timeout: 240000 });
      await p.screenshot({ path: path.join(__dirname, 'renders', `${v}.png`) });
      console.log('rendered', v);
      await p.close();
    }
  } finally { await b.close(); srv.kill(); }
})();
