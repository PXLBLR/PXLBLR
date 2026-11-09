// Render the teaser with the Chromium already on the machine.
//   node render.mjs            -> out/heart_vfib_mockup.mp4
//   node render.mjs stills 0 150 300 ...  -> out/stills/f<frame>.png
import { bundle } from '@remotion/bundler';
import { renderMedia, renderStill, selectComposition } from '@remotion/renderer';
import { mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const browserExecutable = process.env.CHROMIUM || null;
// Own port: another Remotion job on this Mac may serve on 3000 and selectComposition would talk to it.
const port = Number(process.env.PORT || 3418);
const serveUrl = await bundle({ entryPoint: join(here, 'src/index.ts'), publicDir: join(here, 'public') });
const composition = await selectComposition({ serveUrl, id: 'HeartRhythm', browserExecutable, port });
mkdirSync(join(here, 'out/stills'), { recursive: true });
// Software WebGL only where there is no GPU (the Linux cloud box); the Mac uses its own GL.
const chromiumOptions = process.platform === 'linux' ? { gl: 'swangle' } : {};
if (process.argv[2] === 'stills') {
  for (const frame of process.argv.slice(3).map(Number)) {
    await renderStill({ serveUrl, composition, frame, output: join(here, `out/stills/f${frame}.png`), browserExecutable, chromiumOptions, port });
    console.log('still', frame);
  }
} else {
  await renderMedia({ serveUrl, composition, codec: 'h264', crf: 18, audioCodec: 'aac', audioBitrate: '192k', pixelFormat: 'yuv420p',
    outputLocation: join(here, 'out/heart_vfib_mockup.mp4'), browserExecutable, chromiumOptions, port,
    onProgress: ({ progress }) => { if (Math.round(progress * 100) % 10 === 0) process.stdout.write(`${Math.round(progress * 100)}% `); } });
  console.log('\nwrote out/heart_vfib_mockup.mp4');
}
