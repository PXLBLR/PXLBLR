// Synthetic lead II: sinus rhythm at 75/min, then V-fib from VF_START seconds (set by the voice timeline). Values in mV.
import timeline from './timeline.json';

export const VF_START: number = timeline.vf_start;

const g = (t: number, mu: number, sd: number, a: number) => a * Math.exp(-((t - mu) ** 2) / (2 * sd * sd));

const sinus = (t: number) => {
  const p = ((t % 0.8) + 0.8) % 0.8; // 75/min (also before t = 0, so the strip starts full)
  return g(p, 0.1, 0.025, 0.15) + g(p, 0.205, 0.008, -0.12) + g(p, 0.225, 0.011, 1.25) + g(p, 0.248, 0.01, -0.3) + g(p, 0.45, 0.05, 0.3);
};

// Coarse V-fib: irregular undulations, no P, QRS or T; amplitude and rate wander.
const vfib = (t: number) => {
  const env = 0.42 + 0.22 * Math.sin(2 * Math.PI * 0.31 * t) + 0.12 * Math.sin(2 * Math.PI * 0.83 * t + 1.3);
  const ph = 2 * Math.PI * (5.1 * t + 0.35 * Math.sin(2 * Math.PI * 0.47 * t));
  return env * (Math.sin(ph) + 0.45 * Math.sin(1.63 * ph + 0.8) + 0.25 * Math.sin(2.71 * ph + 2.1)) * 0.75;
};

export const ecg = (t: number) => {
  if (t < VF_START) return sinus(t);
  const k = Math.min(1, (t - VF_START) / 0.25);
  return (1 - k) * sinus(t) + k * vfib(t);
};

// Seconds of each R peak before V-fib (for beeps and the squeeze).
export const R_TIMES = Array.from({ length: 80 }, (_, i) => i * 0.8 + 0.225).filter((r) => r < VF_START);
