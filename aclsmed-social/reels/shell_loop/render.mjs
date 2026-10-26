// Render the shell-loop reel with a local Chromium.
//   CHROMIUM=<headless shell> node render.mjs                 -> aclsmed_shell_loop.mp4
//   CHROMIUM=<headless shell> node render.mjs stills 0 29 ...  -> out/stills/f<frame>.png
//   COMP=ShellLoopLabeled node render.mjs ...                  -> same, with the small shell label
import { bundle } from '@remotion/bundler';
import { renderMedia, renderStill, selectComposition } from '@remotion/renderer';
import { mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const browserExecutable = process.env.CHROMIUM || null;
const id = process.env.COMP || 'ShellLoop';
// Own port: another Remotion job on this Mac serves on 3000 and selectComposition would talk to it.
const port = Number(process.env.PORT || 3417);
const serveUrl = await bundle({ entryPoint: join(here, 'src/index.ts'), publicDir: join(here, 'public') });
const composition = await selectComposition({ serveUrl, id, browserExecutable, port });
mkdirSync(join(here, 'out/stills'), { recursive: true });
if (process.argv[2] === 'stills') {
  for (const frame of process.argv.slice(3).map(Number)) {
    await renderStill({ serveUrl, composition, frame, output: join(here, `out/stills/f${frame}.png`), browserExecutable, port });
    console.log('still', frame);
  }
} else {
  const out = join(here, id === 'ShellLoop' ? 'aclsmed_shell_loop.mp4' : 'aclsmed_shell_loop_labeled.mp4');
  await renderMedia({ serveUrl, composition, codec: 'h264', crf: 16, audioCodec: 'aac', audioBitrate: '192k', pixelFormat: 'yuv420p',
    outputLocation: out, browserExecutable, port,
    onProgress: ({ progress }) => { if (Math.round(progress * 100) % 10 === 0) process.stdout.write(`${Math.round(progress * 100)}% `); } });
  console.log(`\nwrote ${out}`);
}
