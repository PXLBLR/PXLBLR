// Render the teaser with the Chromium already on the machine.
//   node render.mjs            -> out/aclsmed_iphone_duo_teaser.mp4
//   node render.mjs stills 0 150 300 ...  -> out/stills/f<frame>.png
import { bundle } from '@remotion/bundler';
import { renderMedia, renderStill, selectComposition } from '@remotion/renderer';
import { mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const browserExecutable = process.env.CHROMIUM || null;
const serveUrl = await bundle({ entryPoint: join(here, 'src/index.ts'), publicDir: join(here, 'public') });
const composition = await selectComposition({ serveUrl, id: 'DuoTeaser', browserExecutable });
mkdirSync(join(here, 'out/stills'), { recursive: true });
const chromiumOptions = { gl: 'swangle' };
if (process.argv[2] === 'stills') {
  for (const frame of process.argv.slice(3).map(Number)) {
    await renderStill({ serveUrl, composition, frame, output: join(here, `out/stills/f${frame}.png`), browserExecutable, chromiumOptions });
    console.log('still', frame);
  }
} else {
  await renderMedia({ serveUrl, composition, codec: 'h264', crf: 18, audioCodec: 'aac', audioBitrate: '192k', pixelFormat: 'yuv420p',
    outputLocation: join(here, 'out/aclsmed_iphone_duo_teaser.mp4'), browserExecutable, chromiumOptions,
    onProgress: ({ progress }) => { if (Math.round(progress * 100) % 10 === 0) process.stdout.write(`${Math.round(progress * 100)}% `); } });
  console.log('\nwrote out/aclsmed_iphone_duo_teaser.mp4');
}
