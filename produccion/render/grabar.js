// Graba una página del motor v2 cuadro por cuadro y la codifica con ffmpeg.
// Uso: node grabar.js pagina.html salida.mp4 [--fps 30] [--workers 3] [--escala 1] [--desde s] [--hasta s] [--solo-datos]
// Escribe <salida>.sfx.json con los efectos de sonido que declaró la página.
const { chromium } = require('playwright-core');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const CHROME = [process.env.CHROME_PATH, '/opt/pw-browsers/chromium', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome']
  .find((p) => p && fs.existsSync(p));
const args = process.argv.slice(2);
const opt = (n, d) => (args.includes(n) ? args[args.indexOf(n) + 1] : d);
const [html, salida] = args;
const FPS = +opt('--fps', 30);
const WORKERS = +opt('--workers', 3);
const ESCALA = +opt('--escala', 1);

async function abrir(browser) {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: ESCALA });
  page.on('pageerror', (e) => { console.error('Error en la página:', e.message); process.exit(1); });
  await page.goto('file://' + path.resolve(html));
  await page.waitForFunction(() => window.__listo === true, null, { timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  return page;
}

function codificador(archivo) {
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', String(FPS), archivo], { stdio: ['pipe', 'inherit', 'inherit'] });
  return ff;
}

async function tramo(a, b, archivo, progreso) {
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
  const page = await abrir(browser);
  const ff = codificador(archivo);
  const cdp = await page.context().newCDPSession(page);
  for (let f = a; f < b; f++) {
    await page.evaluate((t) => window.__seek(t), f / FPS);
    const { data } = await cdp.send('Page.captureScreenshot', { format: 'jpeg', quality: 93, optimizeForSpeed: true });
    const buf = Buffer.from(data, 'base64');
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
    progreso();
  }
  ff.stdin.end();
  await new Promise((r, j) => ff.on('close', (c) => (c === 0 ? r() : j(new Error('ffmpeg terminó con ' + c)))));
  await browser.close();
}

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox', '--disable-gpu-vsync'] });
  const page = await abrir(browser);
  const dur = await page.evaluate(() => window.__duracion);
  const sfx = await page.evaluate(() => window.__sfx);
  await page.close();
  fs.writeFileSync(salida + '.sfx.json', JSON.stringify(sfx));
  if (args.includes('--solo-datos')) { console.log(JSON.stringify({ duracion: dur, sfx: sfx.length })); await browser.close(); return; }

  const desde = Math.round(+opt('--desde', 0) * FPS);
  const hasta = Math.min(Math.ceil(dur * FPS), Math.round(+opt('--hasta', dur) * FPS));
  const total = hasta - desde;
  const n = Math.max(1, Math.min(WORKERS, Math.ceil(total / (FPS * 4))));
  const tam = Math.ceil(total / n);
  let hechos = 0, ultimo = -1;
  const t0 = Date.now();
  const progreso = () => {
    hechos++;
    const pct = Math.floor((hechos / total) * 20) * 5;
    if (pct !== ultimo) {
      ultimo = pct;
      const seg = (Date.now() - t0) / 1000;
      process.stdout.write(`  · ${pct}% (${hechos}/${total} cuadros, ${(hechos / seg).toFixed(1)} cuadros/s)\n`);
    }
  };
  const partes = [];
  const trabajos = [];
  for (let i = 0; i < n; i++) {
    const a = desde + i * tam, b = Math.min(hasta, a + tam);
    if (a >= b) continue;
    const archivo = salida.replace(/\.mp4$/, '') + `.parte${i}.mp4`;
    partes.push(archivo);
    trabajos.push(tramo(a, b, archivo, progreso));
  }
  await browser.close();
  await Promise.all(trabajos);
  const lista = salida + '.partes.txt';
  fs.writeFileSync(lista, partes.map((p) => `file '${path.resolve(p)}'`).join('\n'));
  await new Promise((r, j) => spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lista, '-c', 'copy', salida], { stdio: 'inherit' })
    .on('close', (c) => (c === 0 ? r() : j(new Error('concat falló')))));
  partes.forEach((p) => fs.unlinkSync(p));
  fs.unlinkSync(lista);
  console.log(`✔ ${total} cuadros en ${((Date.now() - t0) / 1000).toFixed(0)} s`);
})().catch((e) => { console.error(e); process.exit(1); });
