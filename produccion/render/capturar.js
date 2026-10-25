// Captura PNG de una página del motor v2 en segundos concretos (revisión visual de los agentes).
// Uso: node capturar.js pagina.html carpeta 3,12.5,40 [--escala 1]
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const CHROME = [process.env.CHROME_PATH, '/opt/pw-browsers/chromium', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome']
  .find((p) => p && fs.existsSync(p));
const [html, carpeta, lista] = process.argv.slice(2);
const escala = process.argv.includes('--escala') ? +process.argv[process.argv.indexOf('--escala') + 1] : 1;

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: escala });
  page.on('pageerror', (e) => { console.error('Error en la página:', e.message); process.exit(1); });
  await page.goto('file://' + path.resolve(html));
  await page.waitForFunction(() => window.__listo === true, null, { timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  for (const s of lista.split(',').map(Number)) {
    await page.evaluate((t) => window.__seek(t), s);
    const out = path.join(carpeta, `t${String(s.toFixed(1)).padStart(6, '0')}.png`);
    await page.screenshot({ path: out });
    console.log(out);
  }
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
