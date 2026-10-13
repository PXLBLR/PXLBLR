// Render the canvas slides (.dc.html) to 1080×1350 PNGs.
//
//   NODE_PATH=$(npm root -g) node app_carousels/render.mjs [CAROUSEL_ID ...]
//
// The slides are authored on the Design canvas, where images are canvas uploads
// (/_blob/<id>). Here the canvas wrappers are stripped and each upload is swapped
// for its local copy in assets/ (blobs.json maps one to the other).
import { readFileSync, readdirSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';

// ESM ignores NODE_PATH, so resolve the globally installed playwright through require.
const { chromium } = createRequire(import.meta.url)('playwright');

const ROOT = dirname(fileURLToPath(import.meta.url));
const OUT = join(ROOT, '..', 'out', 'app_carousels');
const BLOBS = JSON.parse(readFileSync(join(ROOT, 'assets', 'blobs.json'), 'utf8'));

function toPlainHtml(src) {
  return src
    .replace('<script src="./support.js"></script>', '')
    .replace(/<\/?x-dc>|<\/?helmet>/g, '')
    .replace(/<script type="text\/x-dc"[\s\S]*?<\/script>/g, '')
    .replace(/\/_blob\/([0-9a-f]{32})/g, (m, id) => {
      if (!BLOBS[id]) throw new Error(`unknown upload ${id}`);
      return pathToFileURL(join(ROOT, 'assets', BLOBS[id])).href;
    });
}

const wanted = process.argv.slice(2);
const carousels = readdirSync(join(ROOT, 'src')).filter((c) => !wanted.length || wanted.includes(c)).sort();
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined });
const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
for (const c of carousels) {
  mkdirSync(join(OUT, c), { recursive: true });
  for (const f of readdirSync(join(ROOT, 'src', c)).filter((f) => f.endsWith('.dc.html')).sort()) {
    // Loaded from a file:// page so the local images are allowed; fonts come from Google Fonts.
    const tmp = join(OUT, c, `.${f}.html`);
    writeFileSync(tmp, toPlainHtml(readFileSync(join(ROOT, 'src', c, f), 'utf8')));
    await page.goto(pathToFileURL(tmp).href, { waitUntil: 'networkidle' });
    rmSync(tmp);
    await page.evaluate(() => document.fonts.ready);
    const broken = await page.evaluate(() => [...document.images].filter((i) => !i.naturalWidth).map((i) => i.alt));
    if (broken.length) throw new Error(`${c}/${f}: images failed to load: ${broken.join(', ')}`);
    // A flex column that overflows quietly shrinks its fixed-height children (it clipped
    // the PR label once), so any element drawn shorter than its declared height fails.
    const squeezed = await page.evaluate(() => [...document.querySelectorAll('[style*="height:"]')]
      .filter((el) => /(^|;)\s*height:\s*\d+px/.test(el.getAttribute('style')))
      .filter((el) => el.getBoundingClientRect().height + 1 < parseFloat(el.style.height))
      .map((el) => `${el.tagName.toLowerCase()} ${el.style.height} drawn ${Math.round(el.getBoundingClientRect().height)}px`));
    if (squeezed.length) throw new Error(`${c}/${f}: squeezed by overflow: ${squeezed.join('; ')}`);
    const png = join(OUT, c, f.replace('.dc.html', '.png'));
    await page.screenshot({ path: png, clip: { x: 0, y: 0, width: 1080, height: 1350 } });
    console.log('wrote', png);
  }
}
await browser.close();
