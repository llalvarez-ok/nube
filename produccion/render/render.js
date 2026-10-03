// Renderiza trabajos HTML -> PNG/PDF con el Chromium preinstalado.
// Uso: node render.js trabajos.json   ([{html, out, w, h} | {html, pdf}])
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');
const CHROME = process.env.CHROME_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

(async () => {
  const trabajos = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
  for (const t of trabajos) {
    const page = await browser.newPage({ viewport: { width: t.w || 1920, height: t.h || 1080 } });
    await page.goto('file://' + path.resolve(t.html));
    await page.evaluate(() => document.fonts.ready);
    if (t.pdf) await page.pdf({ path: t.pdf, format: 'A4', printBackground: true });
    else await page.screenshot({ path: t.out });
    await page.close();
  }
  await browser.close();
})();
