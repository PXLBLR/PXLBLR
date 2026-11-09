import React from 'react';
import { AbsoluteFill, Audio, continueRender, delayRender, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { makeEcg } from './ecg';
import { DATA } from './data';
import REELS from '../rhythms/reels.json';

const OUTFIT = 'Outfit';
const MONO = 'JetBrains Mono';
const SANS = 'DM Sans';
const fontHandle = delayRender('fonts');
Promise.all(
  [[OUTFIT, 'Outfit.ttf'], [MONO, 'JetBrainsMono.ttf'], [SANS, 'DMSans.ttf']].map(([family, file]) =>
    new FontFace(family, `url(${staticFile(file)})`, { weight: '100 900' }).load().then((f) => document.fonts.add(f))),
).then(() => continueRender(fontHandle));

const NAVY = '#05081A';
const RED = '#EF4444';
const AMBER = '#F5A524';
const CYAN = '#00DCC8';
const CREAM = '#F2EEE3';
const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;

// Heart picture: 1206 x 1565, drawn 560 px wide.
const IMG_W = 1206;
const IMG_H = 1565;
const H_W = 560;
const H_H = (H_W * IMG_H) / IMG_W;
const H_X = 540 - H_W / 2;
const H_Y = 492;
const S = H_W / IMG_W; // image px -> screen px

// Conduction paths traced over the picture (image coordinates).
const SA = [248, 640];
const AV = [395, 775];
const BLOCK = [470, 830]; // just below the AV node, where a Mobitz II / CHB signal stops
const VENT_ORIGIN = [620, 1330]; // ventricular escape focus (CHB)
const P_ATRIA = [[248, 640], [212, 705], [232, 795], [320, 805], [395, 775]];
const P_LV = [[395, 775], [600, 880], [690, 1050], [790, 1290], [870, 1420], [990, 1380], [1050, 1120], [1030, 900]];
const P_RV = [[690, 1050], [700, 1240], [600, 1380], [400, 1250]];
const VENTRICLES = '300,980 560,880 700,760 900,640 1010,700 1080,900 1085,1200 980,1420 800,1480 560,1420 320,1260';
const ATRIA = ['150,600 260,560 400,610 440,760 410,900 300,960 170,900 140,750', '690,520 820,470 960,500 1010,600 900,660 760,700 680,640'];

const along = (pts: number[][], k: number) => {
  const seg = pts.slice(1).map((p, i) => Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1]));
  let d = Math.max(0, Math.min(1, k)) * seg.reduce((a, b) => a + b, 0);
  for (let i = 0; i < seg.length; i++) {
    if (d <= seg[i]) { const u = d / seg[i]; return [pts[i][0] + u * (pts[i + 1][0] - pts[i][0]), pts[i][1] + u * (pts[i + 1][1] - pts[i][1])]; }
    d -= seg[i];
  }
  return pts[pts.length - 1];
};

const rnd = (n: number) => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };

type Beat = { p: number | null; q: number | null; kind: string };

// Wavelets wandering inside a clip region (V-fib in the ventricles, A-fib in the atria).
const Wavelets: React.FC<{ t: number; n: number; x0: number; y0: number; w: number; h: number; life: number; spread: number; r0: number; rk: number; drift: number; clip: string }> =
  ({ t, n, x0, y0, w, h, life: L, spread, r0, rk, drift, clip }) => (
    <g clipPath={`url(#${clip})`} style={{ mixBlendMode: 'screen' }}>
      {Array.from({ length: n }, (_, i) => {
        const life = L + rnd(i) * spread;
        const ph = ((t + rnd(i + 50) * life) % life) / life;
        const cyc = Math.floor((t + rnd(i + 50) * life) / life);
        const x = x0 + rnd(i * 13 + cyc) * w + Math.cos(rnd(i * 7 + cyc) * Math.PI * 2) * ph * drift;
        const y = y0 + rnd(i * 29 + cyc + 3) * h + Math.sin(rnd(i * 7 + cyc) * Math.PI * 2) * ph * drift;
        return <circle key={i} cx={x} cy={y} r={r0 + rk * ph} fill={i % 3 ? '#FFE27A' : '#FF8A5B'} opacity={0.85 * Math.sin(Math.PI * ph)} filter="url(#glow)" />;
      })}
    </g>
  );

const Heart: React.FC<{ t: number; tl: any; mode: string }> = ({ t, tl, mode }) => {
  const post = t >= tl.onset;
  const m = post ? mode : 'sinus';
  const beats: Beat[] = tl.beats;
  const spark = (p: number[], r: number, a: number, key: string, fill = '#FFF3B0') => (
    <circle key={key} cx={p[0]} cy={p[1]} r={r} fill={fill} opacity={a} filter="url(#glow)" />
  );
  const els: React.ReactNode[] = [];
  let squeeze = 0;
  let glow = 0;
  // Sinus-style conduction, driven by each beat's P (SA fire) and QRS onset. Timings match the original 75/min reel:
  // SA 0-0.05 s, atria 0-0.16 s, AV node 0.14 s -> QRS, ventricles QRS-0.03 -> +0.10, squeeze peak QRS+0.1.
  const squeezeGain = m === 'pea' ? 0.25 : m === 'pvt' ? 0.3 : m === 'svt' ? 0.75 : 1;
  const conduct = !['vf', 'torsades', 'asystole'].includes(m);
  if (conduct) {
    for (const [i, b] of beats.entries()) {
      const start = b.p ?? (b.q as number) - 0.1;
      if (start > t || t - start > 1.0) continue;
      if ((b.p ?? b.q ?? 0) >= tl.onset !== post) continue; // pre beats before the onset, post beats after
      if (b.p !== null) {
        const dp = t - b.p;
        if (dp >= 0 && dp < 0.05) els.push(spark(SA, 34, 1 - dp / 0.05, `sa${i}`));
        if (dp >= 0 && dp < 0.16) els.push(spark(along(P_ATRIA, dp / 0.16), 22, 0.95, `a${i}`));
        if (b.q !== null && dp > 0.14 && t < b.q) els.push(spark(AV, 30, 1, `av${i}`));
        if (b.q === null) {
          if (dp > 0.14 && dp < 0.2) els.push(spark(AV, 30, 1, `av${i}`));
          // blocked: the signal dies just below the AV node
          const k = interpolate(dp, [0.18, 0.24, 0.5], [0, 1, 0], clamp);
          if (k > 0) {
            els.push(<g key={`x${i}`} opacity={k}>
              <circle cx={BLOCK[0]} cy={BLOCK[1]} r={34} fill="none" stroke={RED} strokeWidth={9} />
              <path d={`M${BLOCK[0] - 20} ${BLOCK[1] - 20}L${BLOCK[0] + 20} ${BLOCK[1] + 20}M${BLOCK[0] + 20} ${BLOCK[1] - 20}L${BLOCK[0] - 20} ${BLOCK[1] + 20}`} stroke={RED} strokeWidth={9} strokeLinecap="round" />
            </g>);
          }
        }
      }
      if (b.q !== null) {
        const dq = t - b.q;
        const fromVent = b.kind === 'vent';
        if (b.p === null && !fromVent && dq > -0.06 && dq < 0) els.push(spark(AV, 30, 1, `avq${i}`));
        if (!fromVent && dq > -0.03 && dq < 0.10) {
          const v = (dq + 0.03) / 0.13;
          els.push(spark(along(P_LV, v), 22, 0.95, `lv${i}`), spark(along(P_RV, v * 1.6), 20, 0.9, `rv${i}`));
        }
        if (fromVent && dq > -0.03 && dq < 0.25 && m !== 'pvt') {
          const v = (dq + 0.03) / 0.28;
          els.push(<circle key={`ve${i}`} cx={VENT_ORIGIN[0]} cy={VENT_ORIGIN[1]} r={30 + 380 * v} fill="none" stroke="#FFE27A"
            strokeWidth={26 * (1 - v) + 4} opacity={0.75 * (1 - v)} filter="url(#glow)" clipPath="url(#vent)" />);
          if (dq < 0.06) els.push(spark(VENT_ORIGIN, 34, 1, `vo${i}`));
        }
        glow = Math.max(glow, interpolate(dq, [0, 0.06, 0.25], [0, 1, 0], clamp));
        squeeze = Math.max(squeeze, interpolate(dq, [0.02, 0.1, 0.35], [0, 1, 0], clamp) * squeezeGain);
      }
    }
  }
  const tp = t - tl.onset;
  const hrPost = Number(tl.hr_post) || 150;
  const jitter = m === 'vf' || m === 'torsades';
  const jx = jitter ? (rnd(Math.floor(t * 30)) - 0.5) * 3 : 0;
  const jy = jitter ? (rnd(Math.floor(t * 30) + 7) - 0.5) * 3 : 0;
  const dark = mode === 'asystole' ? interpolate(t, [tl.onset, tl.onset + 1.2], [0, 0.55], clamp) : 0;
  const loop = (cx: number, cy: number, rx: number, ry: number, period: number, color: string, key: string, r = 24) => {
    const a = (2 * Math.PI * tp) / period;
    return (
      <g key={key} style={{ mixBlendMode: 'screen' }}>
        <ellipse cx={cx} cy={cy} rx={rx} ry={ry} fill="none" stroke={color} strokeOpacity={0.6} strokeWidth={8} strokeDasharray="16 12" />
        {[0, 1, 2, 3, 4].map((k) => spark([cx + rx * Math.cos(a - k * 0.3), cy + ry * Math.sin(a - k * 0.3)], r - k * (r / 6), 1 - k * 0.18, `${key}${k}`))}
      </g>
    );
  };
  return (
    <div style={{ position: 'absolute', left: H_X, top: H_Y, width: H_W, height: H_H,
      transform: `translate(${jx}px, ${jy}px) scale(${1 - 0.018 * squeeze})`, transformOrigin: '58% 70%' }}>
      <Img src={staticFile('heart.png')} style={{ width: H_W, height: H_H, display: 'block', filter: dark ? `brightness(${1 - dark}) saturate(${1 - dark})` : undefined }} />
      <svg viewBox={`0 0 ${IMG_W} ${IMG_H}`} width={H_W} height={H_H} style={{ position: 'absolute', inset: 0 }}>
        <defs>
          <filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="9" /></filter>
          <filter id="soft"><feGaussianBlur stdDeviation="22" /></filter>
          <clipPath id="vent"><polygon points={VENTRICLES} /></clipPath>
          <clipPath id="atria">{ATRIA.map((p) => <polygon key={p} points={p} />)}</clipPath>
        </defs>
        {conduct && (
          <g style={{ mixBlendMode: 'screen' }}>
            {els}
            {/* ventricles light up together as they depolarise */}
            <polygon points={VENTRICLES} fill="#FFD36B" opacity={0.22 * glow} filter="url(#soft)" />
          </g>
        )}
        {m === 'vf' && <Wavelets t={t} n={26} x0={260} y0={620} w={820} h={820} life={0.35} spread={0.5} r0={18} rk={26} drift={90} clip="vent" />}
        {m === 'afib' && <Wavelets t={t} n={24} x0={150} y0={570} w={280} h={380} life={0.1} spread={0.14} r0={14} rk={22} drift={45} clip="atria" />}
        {m === 'afib' && <Wavelets t={t + 3.7} n={16} x0={690} y0={470} w={310} h={220} life={0.1} spread={0.14} r0={14} rk={22} drift={45} clip="atria" />}
        {m === 'aflutter' && loop(290, 770, 105, 140, 0.2, '#FFE27A', 'fl', 28)}
        {m === 'svt' && loop(AV[0] + 6, AV[1] + 12, 34, 30, 60 / hrPost, '#FFE27A', 'avnrt')}
        {m === 'pvt' && loop(840, 1180, 120, 80, 60 / hrPost, '#FFB36B', 'vt', 34)}
        {m === 'torsades' && (
          <g clipPath="url(#vent)" style={{ mixBlendMode: 'screen' }}>
            {Array.from({ length: 22 }, (_, i) => {
              // Twisting: a band of wavefronts rotating around the ventricles, its width waxing and waning (the spindles).
              const spin = 2 * Math.PI * (tp * 3.6) + (i / 22) * 2 * Math.PI;
              const breathe = 0.55 + 0.45 * Math.sin((2 * Math.PI * tp) / 2.4);
              const r = 120 + 230 * breathe * (0.5 + 0.5 * rnd(i));
              const x = 760 + Math.cos(spin) * r;
              const y = 1110 + Math.sin(spin) * r * 0.72;
              return <circle key={i} cx={x} cy={y} r={20 + 22 * breathe} fill={i % 3 ? '#FFE27A' : '#FF8A5B'} opacity={0.8} filter="url(#glow)" />;
            })}
          </g>
        )}
      </svg>
    </div>
  );
};

const Tag: React.FC<{ x: number; y: number; text: string; color?: string; o: number }> = ({ x, y, text, color = CREAM, o }) => (
  <div style={{ position: 'absolute', left: H_X + x * S, top: H_Y + y * S, transform: 'translate(-50%, -50%)', opacity: o,
    padding: '6px 14px', borderRadius: 10, background: 'rgba(5,8,26,0.82)', border: `2px solid ${color}`, color, fontFamily: MONO,
    fontWeight: 700, fontSize: 22, letterSpacing: '0.08em', whiteSpace: 'nowrap' }}>{text}</div>
);

const Strip: React.FC<{ t: number; ecg: (t: number) => number; tl: any; cfg: any; accent: string }> = ({ t, ecg, tl, cfg, accent }) => {
  const X = 80, Y = 1228, W = 920, HGT = 236, SWEEP = 4; // 4 s across
  const mid = 132, mv = 70 * (cfg.gain ?? (cfg.pre.builtin ? 1 : 0.8)); // baseline y, px per mV (ECGSim strips run taller)
  const pos = ((t % SWEEP) / SWEEP) * W;
  const gap = 26;
  let d = '';
  let pen = false;
  for (let x = 0; x <= W; x += 2) {
    const behind = (pos - x + W) % W;
    if (behind < gap && behind >= 0 && x > pos - 0.5 && x < pos + gap) { pen = false; continue; }
    const tx = t - behind / W * SWEEP;
    const y = Math.max(-40, Math.min(HGT + 40, mid - ecg(tx) * mv));
    d += `${pen ? 'L' : 'M'}${x.toFixed(1)} ${y.toFixed(1)} `;
    pen = true;
  }
  const post = t >= tl.onset;
  const alarm = post && cfg.arrest && Math.floor(t * 2) % 2 === 0;
  return (
    <div style={{ position: 'absolute', left: X, top: Y, width: W, height: HGT, borderRadius: 22, overflow: 'hidden', background: '#020403',
      boxShadow: `0 0 0 2px ${post ? (cfg.arrest ? 'rgba(239,68,68,0.6)' : 'rgba(245,165,36,0.6)') : 'rgba(0,230,64,0.35)'}` }}>
      <svg width={W} height={HGT} style={{ position: 'absolute' }}>
        {Array.from({ length: 47 }, (_, i) => <line key={'v' + i} x1={i * 20} y1={0} x2={i * 20} y2={HGT} stroke="#0d2a14" strokeWidth={i % 5 ? 1 : 2} />)}
        {Array.from({ length: 13 }, (_, i) => <line key={'h' + i} x1={0} y1={i * 20} x2={W} y2={i * 20} stroke="#0d2a14" strokeWidth={i % 5 ? 1 : 2} />)}
        <path d={d} fill="none" stroke="#00E640" strokeWidth={4} strokeLinejoin="round" />
      </svg>
      <div style={{ position: 'absolute', left: 18, top: 12, fontFamily: MONO, fontWeight: 700, fontSize: 24, color: '#00E640' }}>II</div>
      <div style={{ position: 'absolute', right: 18, top: 10, textAlign: 'right', fontFamily: MONO, fontWeight: 700, color: post ? accent : '#00E640' }}>
        <div style={{ fontSize: 18, opacity: 0.8 }}>HR</div>
        <div style={{ fontSize: 46, lineHeight: 1 }}>{post ? tl.hr_post : tl.hr_pre}</div>
      </div>
      {post && <div style={{ position: 'absolute', right: 18, bottom: 12, padding: '4px 12px', borderRadius: 8,
        background: cfg.arrest ? (alarm ? RED : 'transparent') : 'transparent',
        border: `2px solid ${accent}`, color: alarm ? '#fff' : accent, fontFamily: MONO, fontWeight: 700, fontSize: 20 }}>{cfg.badge}</div>}
      <div style={{ position: 'absolute', left: 18, bottom: 10, fontFamily: SANS, fontSize: 16, color: 'rgba(242,238,227,0.55)' }}>Synthetic tracing · 25 mm/s</div>
    </div>
  );
};

// "l4+0.4" -> that line's start + 0.4 s; "key-0.3" -> a cue time - 0.3 s.
const when = (tl: any, spec: string) => {
  const m = /^([a-z_]+\d*)([+-][\d.]+)?$/.exec(spec)!;
  const base = /^l\d+$/.test(m[1]) ? tl.lines.find((l: any) => l.id === m[1]).at : tl[m[1] === 'end' ? 'end_card' : m[1]];
  return base + Number(m[2] || 0);
};

export const HeartRhythm: React.FC<{ id: string }> = ({ id }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  const { timeline: tl, strips } = DATA[id];
  const cfg = (REELS as any)[id];
  const ecg = React.useMemo(() => makeEcg(tl, strips, cfg), [id]);
  const post = t >= tl.onset;
  const accent = cfg.arrest ? RED : AMBER;
  const line = tl.lines.find((l: any) => t >= l.at - 0.1 && t <= l.end + 0.2);
  const lineIn = line ? interpolate(t, [line.at - 0.1, line.at + 0.15], [0, 1], clamp) : 0;
  const end = interpolate(t, [tl.end_card, tl.end_card + 0.6], [0, 1], clamp);
  const flash = interpolate(t, [tl.onset, tl.onset + 0.05, tl.onset + 0.5], [0, cfg.arrest ? 0.55 : 0.3, 0], clamp);
  const keyTag = interpolate(t, [tl.key + 0.2, tl.key + 0.6], [0, 1], clamp) * (1 - end);
  const l2 = tl.lines[1];
  const preTags = cfg.pre_tags !== 'none';
  return (
    <AbsoluteFill style={{ background: `radial-gradient(90% 50% at 50% 45%, ${post ? (cfg.arrest ? '#2a0a12' : '#2a1a08') : '#0f1838'} 0%, ${NAVY} 60%, #000 100%)` }}>
      <Audio src={staticFile(`${id}/audio.wav`)} />
      {/* top block: series kicker + caption (the voice-over) */}
      <div style={{ position: 'absolute', top: 252, left: 60, right: 60, textAlign: 'center' }}>
        <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 26, letterSpacing: '0.2em', color: post ? accent : CYAN }}>
          RHYTHM {String(tl.n).padStart(2, '0')} · {post ? cfg.title : (cfg.pre_title ?? 'NORMAL SINUS RHYTHM')}
        </div>
        <div style={{ marginTop: 16, minHeight: 130, fontFamily: OUTFIT, fontWeight: 800, fontSize: 42, lineHeight: 1.16, color: CREAM,
          opacity: lineIn * (1 - end), transform: `translateY(${(1 - lineIn) * 16}px)` }}>{line?.text}</div>
      </div>
      <Heart t={t} tl={tl} mode={cfg.heart} />
      {preTags && <Tag x={248} y={560} text="SA NODE" o={post ? 0 : interpolate(t, [l2.at + 0.2, l2.at + 0.6, tl.onset - 0.4, tl.onset], [0, 1, 1, 0], clamp)} />}
      {preTags && <Tag x={395} y={860} text="AV NODE" o={post ? 0 : interpolate(t, [l2.at + 1.6, l2.at + 2.0, tl.onset - 0.4, tl.onset], [0, 1, 1, 0], clamp)} />}
      {cfg.tags.map((g: any) => {
        const a = when(tl, g.from), b = when(tl, g.to);
        return <Tag key={g.text} x={g.x} y={g.y} text={g.text} color={g.red ? RED : AMBER} o={interpolate(t, [a, a + 0.4, b, b + 0.3], [0, 1, 1, 0], clamp)} />;
      })}
      <Tag x={660} y={250} text={cfg.key_tag.text} color={cfg.key_tag.red ? RED : AMBER} o={keyTag} />
      <Strip t={t} ecg={ecg} tl={tl} cfg={cfg} accent={accent} />
      <AbsoluteFill style={{ background: '#fff', opacity: flash, pointerEvents: 'none' }} />
      {/* end card */}
      <AbsoluteFill style={{ opacity: end, background: `radial-gradient(80% 50% at 50% 45%, #142355 0%, ${NAVY} 62%, #000 100%)`,
        alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 26 }}>
        <Img src={staticFile('app-icon.png')} style={{ width: 240, height: 240, borderRadius: 54, marginBottom: 18,
          transform: `scale(${0.85 + 0.15 * end})`, boxShadow: '0 0 0 2px rgba(255,255,255,0.12), 0 30px 90px rgba(239,68,68,0.45)' }} />
        <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 28, letterSpacing: '0.2em', color: CYAN }}>PRACTICE IT ON</div>
        <div style={{ fontFamily: OUTFIT, fontWeight: 900, fontSize: 96, color: '#fff', letterSpacing: '-0.03em' }}>
          ACLS<span style={{ color: RED }}>MED</span> <span style={{ color: CYAN }}>SIM</span>
        </div>
        <div style={{ fontFamily: OUTFIT, fontWeight: 700, fontSize: 60, color: CREAM }}>ACLSMED.COM</div>
        <div style={{ position: 'absolute', top: 1400, left: 100, right: 100, textAlign: 'center', fontFamily: SANS, fontSize: 24, lineHeight: 1.4,
          color: 'rgba(242,238,227,0.7)' }}>
          Educational only, not diagnostic and not a substitute for certified ACLS training. Synthetic tracing.
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
