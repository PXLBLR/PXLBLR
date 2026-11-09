// Lead II strips + beat times for each reel, from the local ECGSim engine (_TOOLING/ECGSim, not in this repo).
//   node export_strips.mjs [R02_pvt ...]     -> src/data/<id>.strips.json (committed, so a render needs no ECGSim)
// pre  = the rhythm before the onset (t0 = -5 s so the strip starts full), 70 s.
// post = the rhythm after the onset, 45 s; make_timeline.py places it at the onset.
// Beats: QRS onset times; p: P-wave times; reels with a builtin strip (R01) are skipped.
import { createRequire } from 'node:module';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { homedir } from 'node:os';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const ECGSIM = process.env.ECGSIM || join(homedir(), 'Documents/Claude Projects/_TOOLING/ECGSim');
const require = createRequire(import.meta.url);
const Core = require(join(ECGSIM, 'engine/ecg-core.js'));
const Presets = require(join(ECGSIM, 'engine/presets.js'));
const FS = 250;
const reels = JSON.parse(readFileSync(join(here, 'rhythms/reels.json'), 'utf8'));
const ids = process.argv.slice(2).length ? process.argv.slice(2) : Object.keys(reels).filter((k) => !k.startsWith('_'));

const part = (spec, duration, t0) => {
  const pr = Presets.get(spec.preset);
  if (!pr) throw new Error(`unknown ECGSim preset ${spec.preset}`);
  const params = Core.deepMerge(Core.deepMerge(pr.params, spec.set || {}), { duration, seed: spec.seed ?? 1 });
  const g = Core.generate(params);
  const II = g.leads.II;
  const step = g.fs / FS;
  const y = Array.from({ length: Math.floor(II.length / step) }, (_, i) => Math.round(II[Math.round(i * step)] * 1000) / 1000);
  const seg = g.schedule.segments;
  const r3 = (v) => Math.round((v + t0) * 1000) / 1000;
  return {
    preset: spec.preset, set: spec.set || {}, seed: spec.seed ?? 1, t0, fs: FS, y,
    qrs: g.meta.beats.map((b) => ({ t: r3(b.t), type: b.type, qrs: Math.round(b.qrs * 1000) / 1000 })),
    p: seg.flatMap((s) => (s.ptimes || []).map((p) => r3(p.t))),
    atrial: seg[0].atrial || null,
  };
};

mkdirSync(join(here, 'src/data'), { recursive: true });
for (const id of ids) {
  const r = reels[id];
  if (r.pre.builtin) { console.log(id, 'builtin strip, skipped'); continue; }
  const out = { id, pre: part(r.pre, 70, -5), post: part(r.post, 45, 0) };
  writeFileSync(join(here, `src/data/${id}.strips.json`), JSON.stringify(out));
  const rr = out.post.qrs.slice(1).map((b, i) => b.t - out.post.qrs[i].t);
  const hr = rr.length ? Math.round(60 / (rr.reduce((a, b) => a + b, 0) / rr.length)) : 0;
  console.log(id, `pre ${r.pre.preset} ${out.pre.qrs.length} beats; post ${r.post.preset} ${out.post.qrs.length} beats, ` +
    `${out.post.p.length} P, mean HR ${hr}`);
}
