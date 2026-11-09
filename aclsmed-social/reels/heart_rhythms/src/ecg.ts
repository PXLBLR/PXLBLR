// Lead II for a reel, in mV. Before the onset: the 'pre' strip; after: the 'post' strip, cross-faded over 0.25 s.
// Strips come from ECGSim (src/data/<id>.strips.json, export_strips.mjs); R01 keeps its builtin sinus 75 + coarse V-fib.

const g = (t: number, mu: number, sd: number, a: number) => a * Math.exp(-((t - mu) ** 2) / (2 * sd * sd));

export const sinus75 = (t: number) => {
  const p = ((t % 0.8) + 0.8) % 0.8; // 75/min (also before t = 0, so the strip starts full)
  return g(p, 0.1, 0.025, 0.15) + g(p, 0.205, 0.008, -0.12) + g(p, 0.225, 0.011, 1.25) + g(p, 0.248, 0.01, -0.3) + g(p, 0.45, 0.05, 0.3);
};

// Coarse V-fib: irregular undulations, no P, QRS or T; amplitude and rate wander.
export const vfib = (t: number) => {
  const env = 0.42 + 0.22 * Math.sin(2 * Math.PI * 0.31 * t) + 0.12 * Math.sin(2 * Math.PI * 0.83 * t + 1.3);
  const ph = 2 * Math.PI * (5.1 * t + 0.35 * Math.sin(2 * Math.PI * 0.47 * t));
  return env * (Math.sin(ph) + 0.45 * Math.sin(1.63 * ph + 0.8) + 0.25 * Math.sin(2.71 * ph + 2.1)) * 0.75;
};

type Part = { t0: number; fs: number; y: number[] };
const sample = (p: Part, t: number) => {
  const x = (t - p.t0) * p.fs;
  const i = Math.max(0, Math.min(p.y.length - 2, Math.floor(x)));
  const u = Math.max(0, Math.min(1, x - i));
  return p.y[i] * (1 - u) + p.y[i + 1] * u;
};

export const makeEcg = (tl: any, strips: any, cfg: any) => {
  const pre = (t: number) => (cfg.pre.builtin ? sinus75(t) : sample(strips.pre, t));
  const post = (t: number) => (cfg.post.builtin ? vfib(t) : sample(strips.post, t - tl.post_shift));
  return (t: number) => {
    if (t < tl.onset) return pre(t);
    const k = Math.min(1, (t - tl.onset) / 0.25);
    return (1 - k) * pre(t) + k * post(t);
  };
};
