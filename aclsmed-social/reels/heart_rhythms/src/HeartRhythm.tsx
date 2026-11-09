import React from 'react';
import { AbsoluteFill, Audio, continueRender, delayRender, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { ecg, R_TIMES, VF_START } from './ecg';

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
const CYAN = '#00DCC8';
const CREAM = '#F2EEE3';
const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;

// Voice-over script (rendered later in the owner's voice); captions follow it.
export const SCRIPT = [
  { at: 0.3, end: 1.7, text: 'This is a normal beat.' },
  { at: 1.8, end: 6.2, text: 'The SA node fires, the signal travels down to the ventricles, and they squeeze together.' },
  { at: 6.6, end: 7.9, text: 'Now, V-fib.' },
  { at: 8.0, end: 13.6, text: 'Chaotic electrical activity across the ventricles. They quiver instead of squeezing.' },
  { at: 14.0, end: 19.0, text: 'No squeeze means no cardiac output. No pulse.' },
  { at: 19.5, end: 25.2, text: 'V-fib is shockable. Start CPR and defibrillate as soon as possible.' },
  { at: 25.6, end: 29.6, text: 'Practice it on ACLSMED Sim. ACLSMED.COM' },
];

// Heart picture: 1206 x 1565, drawn 600 px wide.
const IMG_W = 1206;
const IMG_H = 1565;
const H_W = 560;
const H_H = (H_W * IMG_H) / IMG_W; // 778.6
const H_X = 540 - H_W / 2;
const H_Y = 492;
const S = H_W / IMG_W; // image px -> screen px

// Conduction paths traced over the picture (image coordinates).
const P_ATRIA = [[248, 640], [212, 705], [232, 795], [320, 805], [395, 775]];
const P_LV = [[395, 775], [600, 880], [690, 1050], [790, 1290], [870, 1420], [990, 1380], [1050, 1120], [1030, 900]];
const P_RV = [[690, 1050], [700, 1240], [600, 1380], [400, 1250]];
const VENTRICLES = '300,980 560,880 700,760 900,640 1010,700 1080,900 1085,1200 980,1420 800,1480 560,1420 320,1260';

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

const Heart: React.FC<{ t: number }> = ({ t }) => {
  const vf = t >= VF_START;
  // Sinus: phase within the beat drives the spark and the squeeze.
  const beat = t % 0.8;
  const atria = interpolate(beat, [0.0, 0.16], [0, 1], clamp);
  const vent = interpolate(beat, [0.17, 0.3], [0, 1], clamp);
  const squeeze = vf ? 0 : interpolate(beat, [0.22, 0.3, 0.55], [0, 1, 0], clamp);
  const jx = vf ? (rnd(Math.floor(t * 30)) - 0.5) * 3 : 0;
  const jy = vf ? (rnd(Math.floor(t * 30) + 7) - 0.5) * 3 : 0;
  const spark = (p: number[], r: number, a: number, key: string) => (
    <circle key={key} cx={p[0]} cy={p[1]} r={r} fill="#FFF3B0" opacity={a} filter="url(#glow)" />
  );
  return (
    <div style={{ position: 'absolute', left: H_X, top: H_Y, width: H_W, height: H_H,
      transform: `translate(${jx}px, ${jy}px) scale(${1 - 0.018 * squeeze})`, transformOrigin: '58% 70%' }}>
      <Img src={staticFile('heart.png')} style={{ width: H_W, height: H_H, display: 'block' }} />
      <svg viewBox={`0 0 ${IMG_W} ${IMG_H}`} width={H_W} height={H_H} style={{ position: 'absolute', inset: 0 }}>
        <defs>
          <filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="9" /></filter>
          <filter id="soft"><feGaussianBlur stdDeviation="22" /></filter>
          <clipPath id="vent"><polygon points={VENTRICLES} /></clipPath>
        </defs>
        {!vf && (
          <g style={{ mixBlendMode: 'screen' }}>
            {beat < 0.05 && spark([248, 640], 34, 1 - beat / 0.05, 'sa')}
            {atria < 1 && spark(along(P_ATRIA, atria), 22, 0.95, 'a')}
            {beat > 0.14 && beat < 0.2 && spark([395, 775], 30, 1, 'av')}
            {vent > 0 && vent < 1 && [spark(along(P_LV, vent), 22, 0.95, 'lv'), spark(along(P_RV, vent * 1.6), 20, 0.9, 'rv')]}
            {/* ventricles light up together as they depolarise */}
            <polygon points={VENTRICLES} fill="#FFD36B" opacity={0.22 * interpolate(beat, [0.2, 0.26, 0.45], [0, 1, 0], clamp)} filter="url(#soft)" />
          </g>
        )}
        {vf && (
          <g clipPath="url(#vent)" style={{ mixBlendMode: 'screen' }}>
            {Array.from({ length: 26 }, (_, i) => {
              // Wavelets: each wanders, fades in and out on its own clock.
              const life = 0.35 + rnd(i) * 0.5;
              const ph = ((t + rnd(i + 50) * life) % life) / life;
              const cyc = Math.floor((t + rnd(i + 50) * life) / life);
              const x0 = 260 + rnd(i * 13 + cyc) * 820;
              const y0 = 620 + rnd(i * 29 + cyc + 3) * 820;
              const ang = rnd(i * 7 + cyc) * Math.PI * 2;
              const x = x0 + Math.cos(ang) * ph * 90;
              const y = y0 + Math.sin(ang) * ph * 90;
              const a = Math.sin(Math.PI * ph);
              return <circle key={i} cx={x} cy={y} r={18 + 26 * ph} fill={i % 3 ? '#FFE27A' : '#FF8A5B'} opacity={0.85 * a} filter="url(#glow)" />;
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

const Strip: React.FC<{ t: number }> = ({ t }) => {
  const X = 80, Y = 1228, W = 920, HGT = 236, SWEEP = 4; // 4 s across
  const mid = 132, mv = 70; // baseline y, px per mV
  const pos = ((t % SWEEP) / SWEEP) * W;
  const gap = 26;
  let d = '';
  let pen = false;
  for (let x = 0; x <= W; x += 2) {
    const behind = (pos - x + W) % W;
    if (behind < gap && behind >= 0 && x > pos - 0.5 && x < pos + gap) { pen = false; continue; }
    const tx = t - behind / W * SWEEP;
    const y = mid - ecg(tx) * mv;
    d += `${pen ? 'L' : 'M'}${x.toFixed(1)} ${y.toFixed(1)} `;
    pen = true;
  }
  const vf = t >= VF_START;
  const alarm = vf && Math.floor(t * 2) % 2 === 0;
  return (
    <div style={{ position: 'absolute', left: X, top: Y, width: W, height: HGT, borderRadius: 22, overflow: 'hidden', background: '#020403',
      boxShadow: `0 0 0 2px ${vf ? 'rgba(239,68,68,0.6)' : 'rgba(0,230,64,0.35)'}` }}>
      <svg width={W} height={HGT} style={{ position: 'absolute' }}>
        {Array.from({ length: 47 }, (_, i) => <line key={'v' + i} x1={i * 20} y1={0} x2={i * 20} y2={HGT} stroke="#0d2a14" strokeWidth={i % 5 ? 1 : 2} />)}
        {Array.from({ length: 13 }, (_, i) => <line key={'h' + i} x1={0} y1={i * 20} x2={W} y2={i * 20} stroke="#0d2a14" strokeWidth={i % 5 ? 1 : 2} />)}
        <path d={d} fill="none" stroke="#00E640" strokeWidth={4} strokeLinejoin="round" />
      </svg>
      <div style={{ position: 'absolute', left: 18, top: 12, fontFamily: MONO, fontWeight: 700, fontSize: 24, color: '#00E640' }}>II</div>
      <div style={{ position: 'absolute', right: 18, top: 10, textAlign: 'right', fontFamily: MONO, fontWeight: 700, color: vf ? RED : '#00E640' }}>
        <div style={{ fontSize: 18, opacity: 0.8 }}>HR</div>
        <div style={{ fontSize: 46, lineHeight: 1 }}>{vf ? '---' : '75'}</div>
      </div>
      {vf && <div style={{ position: 'absolute', right: 18, bottom: 12, padding: '4px 12px', borderRadius: 8, background: alarm ? RED : 'transparent',
        border: `2px solid ${RED}`, color: alarm ? '#fff' : RED, fontFamily: MONO, fontWeight: 700, fontSize: 20 }}>V-FIB</div>}
      <div style={{ position: 'absolute', left: 18, bottom: 10, fontFamily: SANS, fontSize: 16, color: 'rgba(242,238,227,0.55)' }}>Synthetic tracing · 25 mm/s</div>
    </div>
  );
};

export const HeartRhythm: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  const vf = t >= VF_START;
  const line = SCRIPT.find((l) => t >= l.at - 0.1 && t <= l.end + 0.2);
  const lineIn = line ? interpolate(t, [line.at - 0.1, line.at + 0.15], [0, 1], clamp) : 0;
  const end = interpolate(t, [25.4, 26.0], [0, 1], clamp);
  const flash = interpolate(t, [VF_START, VF_START + 0.05, VF_START + 0.5], [0, 0.55, 0], clamp);
  const noPulse = interpolate(t, [14.2, 14.6], [0, 1], clamp) * (1 - end);
  return (
    <AbsoluteFill style={{ background: `radial-gradient(90% 50% at 50% 45%, ${vf ? '#2a0a12' : '#0f1838'} 0%, ${NAVY} 60%, #000 100%)` }}>
      <Audio src={staticFile('audio.wav')} />
      {/* top block: series kicker + caption (the voice-over) */}
      <div style={{ position: 'absolute', top: 252, left: 60, right: 60, textAlign: 'center' }}>
        <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 26, letterSpacing: '0.2em', color: vf ? RED : CYAN }}>
          RHYTHM 01 · {vf ? 'VENTRICULAR FIBRILLATION' : 'NORMAL SINUS RHYTHM'}
        </div>
        <div style={{ marginTop: 16, minHeight: 130, fontFamily: OUTFIT, fontWeight: 800, fontSize: 42, lineHeight: 1.16, color: CREAM,
          opacity: lineIn * (1 - end), transform: `translateY(${(1 - lineIn) * 16}px)` }}>{line?.text}</div>
      </div>
      <Heart t={t} />
      <Tag x={248} y={560} text="SA NODE" o={vf ? 0 : interpolate(t, [2.0, 2.4, 6.2, 6.5], [0, 1, 1, 0], clamp)} />
      <Tag x={395} y={860} text="AV NODE" o={vf ? 0 : interpolate(t, [2.8, 3.2, 6.2, 6.5], [0, 1, 1, 0], clamp)} />
      <Tag x={780} y={1300} text="VENTRICLES" color={RED} o={interpolate(t, [8.4, 8.8, 13.8, 14.1], [0, 1, 1, 0], clamp)} />
      <Tag x={660} y={250} text="NO PULSE" color={RED} o={noPulse} />
      <Strip t={t} />
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
