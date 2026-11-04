import React from 'react';
import {
  AbsoluteFill, Audio, Easing, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile,
  useCurrentFrame, useVideoConfig, continueRender, delayRender,
} from 'remotion';
import timeline from '../timeline.json';
import alignment from './alignment.json';
import bezel from './bezel.json';
import words from './words.json';

// Brand fonts (variable TTFs from aclsmed-social/fonts), loaded locally.
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
// Channel colours sampled from the app's own tiles (Console shell).
const CH: Record<string, string> = {
  ecg: '#61FFAA', art: '#E23A3A', pa: '#FFEB3B', cvp: '#A8DAFF', spo2: '#00DCF0', etco2: '#D0D0D0', cream: CREAM,
};

export const FPS = timeline.fps;
export const DURATION = Math.round(timeline.duration * FPS);

type Shot = { id: string; take: string | null; from: number; label?: string; eyebrow?: string; color?: string };
const SHOTS = timeline.shots as Shot[];
const SEGS = alignment.segments as { id: string; take: string; from: number; to: number; frames: number }[];
const WORDS = words as { id: string; at: number; dur: number; speechStart: number; speechEnd: number;
  words: { w: string; start: number; end: number; key: boolean }[] }[];

const sec = (f: number) => f / FPS;
const fr = (s: number) => Math.round(s * FPS);
const shotAt = (t: number) => {
  let cur = SHOTS[0];
  for (const s of SHOTS) if (s.from <= t + 1e-6) cur = s;
  return cur;
};
const shotStart = (id: string) => SHOTS.find((s) => s.id === id)!.from;
const END_AT = shotStart('end');
const OUTRO_AT = shotStart('outro');

// Safe areas for BOTH Instagram Reels and YouTube Shorts: 80 px clear on each
// side, no text above y=250 or below y=1500 (YouTube's bottom overlay is ~420 px).
const SAFE_TOP = 250;
const SAFE_BOTTOM = 1920 - 420;
const SIDE = 80;

// The iPad: Apple's iPad Pro 13" (M5) body drawn from the Simulator's display
// mask (ACLSMED iOS scripts/bezel_composite.swift --emit-bezel), 920 px wide.
const DEV_W = 1080 - 2 * SIDE;
const K = DEV_W / bezel.width;
const DEV_H = Math.round(bezel.height * K); // 704
const DEV_X = SIDE;
const DEV_Y = 560;
const SCR = {
  x: DEV_X + bezel.aperture.x * K - 1,
  y: DEV_Y + bezel.aperture.y * K - 1,
  w: bezel.aperture.w * K + 2,
  h: (bezel.aperture.w * K + 2) * (1032 / 1376), // clips are the whole 1376x1032 display
};
const CAPTION_Y = DEV_Y + DEV_H + 44; // 1308

// ── The monitor: real takes, cut on the same film-clock instant ─────────────
const Monitor: React.FC = () => (
  <div style={{ position: 'absolute', left: SCR.x, top: SCR.y, width: SCR.w, height: SCR.h, overflow: 'hidden', background: '#000' }}>
    {SEGS.map((g) => (
      <Sequence key={g.id} from={fr(g.from)} durationInFrames={g.frames} layout="none">
        <OffthreadVideo src={staticFile(`segments/${g.id}.mp4`)} muted
          style={{ width: SCR.w, height: SCR.h, display: 'block' }} />
      </Sequence>
    ))}
  </div>
);

const IPad: React.FC<{ opacity: number; y: number }> = ({ opacity, y }) => (
  <div style={{ position: 'absolute', left: 0, top: y, width: 1080, height: 1920, opacity }}>
    <Monitor />
    <Img src={staticFile('bezel.png')}
      style={{ position: 'absolute', left: DEV_X, top: DEV_Y, width: DEV_W, height: DEV_H,
        filter: 'drop-shadow(0 26px 46px rgba(0,0,0,0.6))' }} />
  </div>
);

// ── Step label above the iPad ───────────────────────────────────────────────
const StepLabel: React.FC<{ t: number }> = ({ t }) => {
  const { fps } = useVideoConfig();
  const shot = shotAt(t);
  if (!shot.take || shot.id === 'hero') return null;
  // The lead flip-through keeps one label block; only the text changes.
  const isLead = shot.id.startsWith('lead');
  const groupStart = isLead ? 0 : shot.from;
  const local = (t - shot.from) * fps;
  const pop = isLead && shot.id !== 'lead2' ? 1 : spring({ frame: local, fps, config: { damping: 16, stiffness: 180 } });
  const groupIn = interpolate(t - groupStart, [0, 0.25], [0, 1], { extrapolateRight: 'clamp' });
  const color = CH[shot.color || 'cream'];
  const isAll = shot.id === 'all';
  return (
    <div style={{ position: 'absolute', left: SIDE, right: SIDE, top: SAFE_TOP + 50, height: 230, textAlign: 'center',
      opacity: Math.min(groupIn, interpolate(t, [END_AT - 0.35, END_AT], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })) }}>
      <div style={{ fontFamily: MONO, fontWeight: 600, fontSize: isAll ? 30 : 28, letterSpacing: '0.18em',
        color: isAll ? CREAM : 'rgba(242,238,227,0.62)' }}>
        {isAll ? (
          <>
            <span style={{ color: CH.ecg }}>ECG</span> · <span style={{ color: CH.art }}>ART</span> ·{' '}
            <span style={{ color: CH.pa }}>PA</span> ·{' '}
            <span style={{ color: CH.cvp }}>CVP</span> · <span style={{ color: CH.spo2 }}>SpO₂</span> ·{' '}
            <span style={{ color: CH.etco2 }}>EtCO₂</span>
          </>
        ) : shot.eyebrow}
      </div>
      <div style={{ marginTop: 14, fontFamily: isLead ? MONO : OUTFIT, fontWeight: 700,
        fontSize: isAll ? 84 : 112, lineHeight: 1, letterSpacing: isLead ? '0.02em' : '-0.01em',
        color: isAll ? CREAM : color, transform: `scale(${0.86 + 0.14 * pop})`,
        textShadow: isAll ? 'none' : `0 0 38px ${color}55` }}>
        {isAll ? 'One monitor' : shot.label}
      </div>
    </div>
  );
};

// ── Hero headline ───────────────────────────────────────────────────────────
const HeroTitle: React.FC<{ t: number }> = ({ t }) => {
  const { fps } = useVideoConfig();
  const h0 = shotStart('hero');
  if (t < h0 || t >= END_AT) return null;
  const s = spring({ frame: (t - h0) * fps, fps, config: { damping: 18, stiffness: 120 } });
  const out = interpolate(t, [END_AT - 0.35, END_AT], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  return (
    <div style={{ position: 'absolute', left: SIDE, right: SIDE, top: SAFE_TOP + 60, textAlign: 'center', opacity: s * out,
      transform: `translateY(${(1 - s) * 30}px)` }}>
      <div style={{ fontFamily: OUTFIT, fontWeight: 700, fontSize: 124, lineHeight: 1, letterSpacing: '-0.01em', color: CREAM }}>
        ACLS<span style={{ color: RED }}>MED</span> <span style={{ fontWeight: 500 }}>Sim</span>
      </div>
      <div style={{ marginTop: 22, fontFamily: MONO, fontWeight: 500, fontSize: 26, letterSpacing: '0.22em', color: CYAN }}>
        PATIENT MONITOR SIMULATOR
      </div>
    </div>
  );
};

// ── Burned-in captions (the narration's own words, word by word) ────────────
// A long line is shown one phrase at a time so a caption never runs past two
// lines (it must stay above y=1500). Lines up to FIT chars show whole; longer
// ones break only at punctuation, merging phrases while they still fit.
const FIT = 64;
type Word = { w: string; start: number; end: number; key: boolean };
const textOf = (ws: Word[]) => ws.map((x) => x.w).join(' ');
const chunks = (ws: Word[]) => {
  if (textOf(ws).length <= FIT) return [ws];
  const phrases: Word[][] = [];
  let cur: Word[] = [];
  for (const w of ws) {
    cur.push(w);
    if (/[,.?]$/.test(w.w)) { phrases.push(cur); cur = []; }
  }
  if (cur.length) phrases.push(cur);
  const out: Word[][] = [];
  for (const p of phrases) {
    const last = out[out.length - 1];
    if (last && textOf([...last, ...p]).length <= 60) out[out.length - 1] = [...last, ...p];
    else out.push(p);
  }
  return out;
};

const Caption: React.FC<{ t: number; lineId: string; top: number; size?: number; color?: string }> = ({ t, lineId, top, size = 52, color }) => {
  const line = WORDS.find((l) => l.id === lineId)!;
  const show0 = line.speechStart - 0.12;
  const next = WORDS[WORDS.indexOf(line) + 1];
  const show1 = Math.min(line.speechEnd + 0.5, next ? next.speechStart - 0.15 : 1e9);
  if (t < show0 || t > show1) return null;
  const parts = chunks(line.words);
  // The phrase on screen: the last one whose first word has (nearly) been said.
  let k = 0;
  parts.forEach((p, i) => { if (t >= p[0].start - 0.12) k = i; });
  const part = parts[k];
  const partIn = k === 0 ? show0 : part[0].start - 0.12;
  const op = Math.min(interpolate(t, [partIn, partIn + 0.12], [0, 1], { extrapolateRight: 'clamp' }),
    interpolate(t, [show1 - 0.15, show1], [1, 0], { extrapolateLeft: 'clamp' }));
  return (
    <div style={{ position: 'absolute', left: SIDE + 40, right: SIDE + 40, top, textAlign: 'center', opacity: op,
      fontFamily: SANS, fontWeight: 700, fontSize: size, lineHeight: 1.18, letterSpacing: '-0.005em' }}>
      {part.map((w, i) => {
        const said = t >= w.start - 0.03;
        // A key word takes the colour of the step it names (the shot on screen as it is said).
        const c = w.key ? (color || CH[shotAt(w.start + 0.1).color || 'cream']) : CREAM;
        return (
          <span key={i} style={{ color: c, opacity: said ? 1 : 0.38 }}>
            {w.w}{i < part.length - 1 ? ' ' : ''}
          </span>
        );
      })}
    </div>
  );
};

// ── End card: one word per spoken word ──────────────────────────────────────
const EndCard: React.FC<{ t: number }> = ({ t }) => {
  const { fps } = useVideoConfig();
  if (t < END_AT || t >= OUTRO_AT) return null;
  const l9 = WORDS.find((l) => l.id === 'l9')!.words;
  const fadeOut = interpolate(t, [OUTRO_AT - 0.3, OUTRO_AT], [1, 0], { extrapolateLeft: 'clamp' });
  const pop = (i: number) => spring({ frame: (t - l9[i].start + 0.04) * fps, fps, config: { damping: 15, stiffness: 190 } });
  const big = (txt: string, i: number) => {
    const p = t >= l9[i].start - 0.04 ? pop(i) : 0;
    return (
      <div style={{ fontFamily: OUTFIT, fontWeight: 700, fontSize: 132, lineHeight: 1.04, letterSpacing: '-0.015em',
        color: CREAM, opacity: p, transform: `translateY(${(1 - p) * 26}px) scale(${0.94 + 0.06 * p})` }}>
        {txt}<span style={{ color: RED }}>.</span>
      </div>
    );
  };
  const pUrl = t >= l9[3].start - 0.04 ? pop(3) : 0;
  return (
    <AbsoluteFill style={{ opacity: fadeOut }}>
      <div style={{ position: 'absolute', left: SIDE, right: SIDE, top: 560, textAlign: 'center' }}>
        {big('Integrated', 0)}
        {big('Immersive', 1)}
        {big('Essential', 2)}
        <div style={{ marginTop: 70, fontFamily: OUTFIT, fontWeight: 700, fontSize: 76, letterSpacing: '0.03em', color: CREAM,
          opacity: pUrl, transform: `translateY(${(1 - pUrl) * 20}px)` }}>
          ACLS<span style={{ color: RED }}>MED</span>.COM
        </div>
      </div>
      <Disclaimer />
    </AbsoluteFill>
  );
};

const Disclaimer: React.FC = () => (
  <div style={{ position: 'absolute', left: 0, right: 0, top: SAFE_BOTTOM - 44, textAlign: 'center',
    fontFamily: MONO, fontWeight: 400, fontSize: 22, letterSpacing: '0.08em', color: 'rgba(242,238,227,0.55)' }}>
    Educational only, not diagnostic
  </div>
);

// ── Outro: icon, name, both store badges ────────────────────────────────────
const Outro: React.FC<{ t: number }> = ({ t }) => {
  const { fps } = useVideoConfig();
  if (t < OUTRO_AT) return null;
  const a = (d: number) => spring({ frame: (t - OUTRO_AT - d) * fps, fps, config: { damping: 16, stiffness: 150 } });
  const l10 = WORDS.find((l) => l.id === 'l10')!.words;
  const storeAt = l10.find((w) => w.w === 'App')!.start;
  const playAt = l10.find((w) => w.w === 'Google')!.start;
  const b = (at: number) => (t >= at - 0.05 ? spring({ frame: (t - at + 0.05) * fps, fps, config: { damping: 14, stiffness: 200 } }) : 0);
  const end = interpolate(t, [timeline.duration - 0.4, timeline.duration], [1, 0], { extrapolateLeft: 'clamp' });
  return (
    <AbsoluteFill style={{ opacity: end }}>
      <div style={{ position: 'absolute', left: 0, right: 0, top: 380, textAlign: 'center' }}>
        <Img src={staticFile('app-icon.png')} style={{ width: 236, height: 236, borderRadius: 54,
          boxShadow: '0 18px 50px rgba(0,0,0,0.55), 0 0 0 1px rgba(242,238,227,0.12)',
          opacity: a(0), transform: `scale(${0.8 + 0.2 * a(0)})` }} />
        <div style={{ marginTop: 44, fontFamily: OUTFIT, fontWeight: 700, fontSize: 104, lineHeight: 1, color: CREAM, opacity: a(0.12) }}>
          ACLS<span style={{ color: RED }}>MED</span> <span style={{ fontWeight: 500 }}>Sim</span>
        </div>
        <div style={{ marginTop: 22, fontFamily: MONO, fontWeight: 600, fontSize: 28, letterSpacing: '0.2em', color: CYAN, opacity: a(0.24) }}>
          AVAILABLE TODAY
        </div>
        <div style={{ marginTop: 56, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 28 }}>
          <Img src={staticFile('badge-app-store.png')} style={{ height: 104, opacity: b(storeAt), transform: `scale(${0.85 + 0.15 * b(storeAt)})` }} />
          <Img src={staticFile('badge-google-play.png')} style={{ height: 104, opacity: b(playAt), transform: `scale(${0.85 + 0.15 * b(playAt)})` }} />
        </div>
      </div>
      <Caption t={t} lineId="l10" top={1268} size={42} color={CYAN} />
      <Disclaimer />
    </AbsoluteFill>
  );
};

export const MonitorLines: React.FC = () => {
  const frame = useCurrentFrame();
  const t = sec(frame);
  // The iPad leaves as the end card arrives.
  const ipadOut = interpolate(t, [END_AT - 0.35, END_AT], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
    easing: Easing.in(Easing.cubic) });
  const heroGlow = interpolate(t, [shotStart('hero'), shotStart('hero') + 1.2], [0.10, 0.2], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  return (
    <AbsoluteFill style={{ background: NAVY }}>
      <AbsoluteFill style={{ opacity: ipadOut,
        background: `radial-gradient(ellipse 700px 520px at 540px ${DEV_Y + DEV_H / 2}px, rgba(0,220,200,${heroGlow}), rgba(5,8,26,0) 70%)` }} />
      {t < END_AT ? <IPad opacity={ipadOut} y={(1 - ipadOut) * 40} /> : null}
      <StepLabel t={t} />
      <HeroTitle t={t} />
      {['l1', 'l2', 'lart', 'l3', 'l4', 'l5', 'l6', 'l7', 'l8'].map((id) => (
        <Caption key={id} t={t} lineId={id} top={CAPTION_Y} />
      ))}
      <EndCard t={t} />
      <Outro t={t} />
      <Audio src={staticFile('audio.wav')} />
    </AbsoluteFill>
  );
};
