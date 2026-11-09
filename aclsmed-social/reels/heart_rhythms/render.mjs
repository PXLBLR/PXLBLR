// Render heart-rhythm reels.
//   node render.mjs                         -> R01 (out/heart_vfib_mockup.mp4)
//   node render.mjs R02_pvt R03_torsades    -> out/<reels.json "out"> for each
//   node render.mjs stills R02_pvt 0 150 …  -> out/stills/R02_pvt-f<frame>.png
// On this Mac use CHROMIUM=<Chrome for Testing 149> (the Chromium 157 that npm downloads hangs; RENDER-NOTES.md).
import { bundle } from '@remotion/bundler';
import { renderMedia, renderStill, selectComposition } from '@remotion/renderer';
import { mkdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const browserExecutable = process.env.CHROMIUM || null;
// Own port: another Remotion job on this Mac may serve on 3000 and selectComposition would talk to it.
const port = Number(process.env.PORT || 3418);
// Software WebGL only where there is no GPU (the Linux cloud box); the Mac uses its own GL.
const chromiumOptions = process.platform === 'linux' ? { gl: 'swangle' } : {};
const reels = JSON.parse(readFileSync(join(here, 'rhythms/reels.json'), 'utf8'));
const serveUrl = await bundle({ entryPoint: join(here, 'src/index.ts'), publicDir: join(here, 'public') });
const comp = (id) => selectComposition({ serveUrl, id: id.replace(/_/g, '-'), inputProps: { id }, browserExecutable, port });
mkdirSync(join(here, 'out/stills'), { recursive: true });

if (process.argv[2] === 'stills') {
  const id = process.argv[3];
  const composition = await comp(id);
  for (const frame of process.argv.slice(4).map(Number)) {
    await renderStill({ serveUrl, composition, frame, inputProps: { id }, output: join(here, `out/stills/${id}-f${frame}.png`),
      browserExecutable, chromiumOptions, port });
    console.log('still', id, frame);
  }
} else {
  const ids = process.argv.slice(2).length ? process.argv.slice(2) : ['R01_vfib'];
  for (const id of ids) {
    const composition = await comp(id);
    const out = join(here, 'out', reels[id].out);
    await renderMedia({ serveUrl, composition, inputProps: { id }, codec: 'h264', crf: 18, audioCodec: 'aac', audioBitrate: '192k',
      pixelFormat: 'yuv420p', outputLocation: out, browserExecutable, chromiumOptions, port,
      onProgress: ({ progress }) => { if (Math.round(progress * 100) % 25 === 0) process.stdout.write(`${Math.round(progress * 100)}% `); } });
    console.log(`\n${id}: wrote out/${reels[id].out}`);
  }
}
