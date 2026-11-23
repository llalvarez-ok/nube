// Uso: node render.js pdf <html> <salida.pdf> <ancho> <alto>
//      node render.js png <html> <salida.png> <anchoPx> <altoPx>
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [modo, html, salida, ancho, alto] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage(
    modo === 'png' ? { viewport: { width: +ancho, height: +alto } } : {}
  );
  await page.goto('file://' + path.resolve(html), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  if (modo === 'pdf') {
    await page.pdf({ path: salida, width: ancho, height: alto, printBackground: true });
  } else {
    await page.screenshot({ path: salida });
  }
  await browser.close();
})();
