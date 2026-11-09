import React from 'react';
import {
  AbsoluteFill, Audio, Easing, Img, OffthreadVideo, interpolate, spring, staticFile,
  useCurrentFrame, useVideoConfig, continueRender, delayRender,
} from 'remotion';
import TL from './timeline.json';
import bezel from './bezel.json';

// Brand fonts (variable TTFs), loaded locally.
const OUTFIT = 'Outfit';
const MONO = 'JetBrains Mono';
const SANS = 'DM Sans';
const fontHandle = delayRender('fonts');
Promise.all(
  [[OUTFIT, 'Outfit.ttf'], [MONO, 'JetBrainsMono.ttf'], [SANS, 'DMSans.ttf']].map(([family, file]) =>
    new FontFace(family, `url(${staticFile(file)})`, { weight: '100 900' }).load().then((f) => document.fonts.add(f))),
).then(() => continueRender(fontHandle));

// Light stage for the dark Hospital-shell iPad (owner, 2026-11-09).
const BG_TOP = '#F7F8FA';
const BG_BOT = '#E6E9F0';
const INK = '#0B1533';
const INK2 = 'rgba(11,21,51,0.58)';
const RED = '#E5322D';
const C = TL.colors;

export const FPS = TL.fps;
export const DURATION = Math.round(TL.duration * FPS);

// Safe areas for Instagram Reels and YouTube Shorts: 80 px each side, nothing above y=250 or below y=1500.
const SAFE_TOP = 250;
const SAFE_BOTTOM = 1500;
const SIDE = 80;

// The iPad, whole: iPad Pro 13" (M5) body from ACLSMED iOS scripts/bezel_composite.swift --emit-bezel, 920 px wide.
const DEV_W = 1080 - 2 * SIDE;
const K = DEV_W / bezel.width;
const DEV_H = Math.round(bezel.height * K); // 704
const DEV_X = SIDE;
const DEV_Y = 668;
const SCR = {
  x: DEV_X + bezel.aperture.x * K - 1,
  y: DEV_Y + bezel.aperture.y * K - 1,
  w: bezel.aperture.w * K + 2,
  h: (bezel.aperture.w * K + 2) * 0.75, // the clip is the whole 4:3 display
};
const CAPTION_Y = DEV_Y + DEV_H + 26;

// 12-lead grid rows, as fractions of the screen (measured on the Hospital shell's live 12-lead view).
type Rect = { x: number; y: number; w: number; h: number };
const ROWS = TL.rows as Record<string, [number, number]>;
const leadRect = (lead: string): Rect => {
  const [c, r] = ROWS[lead];
  const x0 = (c === 0 ? 35 : 745) / 2000;
  const x1 = (c === 0 ? 720 : 1432) / 2000;
  return { x: x0, y: (140 + 156.2 * r) / 1500, w: x1 - x0, h: 156 / 1500 };
};
// Neighbouring leads in one column draw as one outline.
const groupRects = (leads: string[]): Rect[] => {
  const out: { c: number; r0: number; r1: number }[] = [];
  for (const l of leads) {
    const [c, r] = ROWS[l];
    const g = out.find((o) => o.c === c && (o.r1 === r - 1 || o.r0 === r + 1));
    if (g) { g.r0 = Math.min(g.r0, r); g.r1 = Math.max(g.r1, r); } else out.push({ c, r0: r, r1: r });
  }
  return out.map((g) => {
    const a = leadRect(Object.keys(ROWS).find((k) => ROWS[k][0] === g.c && ROWS[k][1] === g.r0)!);
    return { ...a, h: (156.2 * (g.r1 - g.r0) + 156) / 1500 };
  });
};

const sec = (f: number) => f / FPS;
type Panel = {
  from: number; to: number; kind: string; eyebrow?: string; text?: string; color?: string; mono?: boolean;
  rows?: string[]; win?: [number, number]; outline?: string[]; outlines?: string[][]; baseline?: boolean; steps?: [number, string][]; at2?: number;
};
const PANELS = TL.panels as Panel[];
const panelAt = (t: number) => PANELS.find((p) => t >= p.from && t < p.to);
const END_AT = TL.end_at;
const fadeIn = (t: number, a: number, d = 0.18) => interpolate(t, [a, a + d], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
const fadeOut = (t: number, b: number, d = 0.18) => interpolate(t, [b - d, b], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

// ── The monitor: one continuous take ────────────────────────────────────────
const Screen: React.FC = () => (
  <div style={{ position: 'absolute', left: SCR.x, top: SCR.y, width: SCR.w, height: SCR.h, overflow: 'hidden', background: '#000' }}>
    <OffthreadVideo src={staticFile('monitor.mp4')} muted style={{ width: SCR.w, height: SCR.h, display: 'block' }} />
  </div>
);

const Outline: React.FC<{ r: Rect; color: string; op: number }> = ({ r, color, op }) => (
  <div style={{ position: 'absolute', left: SCR.x + r.x * SCR.w - 4, top: SCR.y + r.y * SCR.h - 2,
    width: r.w * SCR.w + 8, height: r.h * SCR.h + 2, border: `3px solid ${color}`, borderRadius: 7, opacity: op,
    boxShadow: `0 0 14px ${color}88, inset 0 0 10px ${color}44` }} />
);

const Outlines: React.FC<{ t: number }> = ({ t }) => {
  const p = panelAt(t);
  if (!p || t >= END_AT) return null;
  const op = Math.min(fadeIn(t, p.from), fadeOut(t, p.to, 0.12));
  const sets: [string[], string][] = [];
  if (p.outline) sets.push([p.outline, p.color!]);
  if (p.outlines) { sets.push([p.outlines[0], C.red]); sets.push([p.outlines[1], C.blue]); }
  return <>{sets.flatMap(([leads, col], i) => groupRects(leads).map((r, j) => <Outline key={`${i}-${j}`} r={r} color={col} op={op} />))}</>;
};

const IPad: React.FC<{ t: number; opacity: number; y: number }> = ({ t, opacity, y }) => (
  <div style={{ position: 'absolute', left: 0, top: y, width: 1080, height: 1920, opacity }}>
    <Screen />
    <Img src={staticFile('bezel.png')}
      style={{ position: 'absolute', left: DEV_X, top: DEV_Y, width: DEV_W, height: DEV_H,
        filter: 'drop-shadow(0 34px 48px rgba(11,21,51,0.38)) drop-shadow(0 6px 12px rgba(11,21,51,0.22))' }} />
    <Outlines t={t} />
  </div>
);

// ── Top area: what the narration is pointing at ─────────────────────────────
const TOP_Y = SAFE_TOP + 6;
const Eyebrow: React.FC<{ text: string; color: string; op: number }> = ({ text, color, op }) => (
  <div style={{ position: 'absolute', left: SIDE, right: SIDE, top: TOP_Y, textAlign: 'center', opacity: op,
    fontFamily: MONO, fontWeight: 700, fontSize: 25, letterSpacing: '0.16em', color }}>
    {text}
  </div>
);

// Magnifier: the same live footage, two rows of the 12-lead enlarged (~2.2x of the iPad).
const MAG_W = 680;
const ROW_H = Math.round(MAG_W * (156 / 1500) * 0.75 / (685 / 2000)); // keeps the crop's aspect
const MAG_X = (1080 - MAG_W) / 2;
const MAG_Y = TOP_Y + 50;
const MagRow: React.FC<{ lead: string; top: number; color: string; baseline?: boolean; win: [number, number] }> = ({ lead, top, color, baseline, win }) => {
  const full = leadRect(lead);
  // Zoom into the middle of the row (the trace band), keeping the crop's aspect: a window of the row's height
  // [win] takes the same fraction of the column's width, centred.
  const f = win[1] - win[0];
  const r = { x: full.x + full.w * (1 - f) / 2, y: full.y + full.h * win[0], w: full.w * f, h: full.h * f };
  const VW = MAG_W / r.w;
  const VH = VW * 0.75;
  const b = ((TL.baseline as Record<string, number>).V2 - win[0]) / f; // the isoelectric line, same height in every row
  return (
    <div style={{ position: 'absolute', left: MAG_X, top, width: MAG_W, height: ROW_H, overflow: 'hidden', background: '#0E0F11' }}>
      <OffthreadVideo src={staticFile('monitor.mp4')} muted
        style={{ position: 'absolute', left: -r.x * VW, top: -r.y * VH, width: VW, height: VH }} />
      {baseline ? (
        <div style={{ position: 'absolute', left: 0, right: 0, top: b * ROW_H - 1, height: 0,
          borderTop: `2px dashed ${color}`, opacity: 0.8 }} />
      ) : null}
      <div style={{ position: 'absolute', left: 10, top: 8, padding: '2px 10px', borderRadius: 6, background: 'rgba(14,15,17,0.88)',
        fontFamily: MONO, fontWeight: 700, fontSize: 26, color: '#61FFAA' }}>{lead}</div>
    </div>
  );
};

const Magnifier: React.FC<{ p: Panel; op: number }> = ({ p, op }) => (
  <div style={{ position: 'absolute', left: 0, top: 0, width: 1080, height: 1920, opacity: op }}>
    <div style={{ position: 'absolute', left: MAG_X - 8, top: MAG_Y - 8, width: MAG_W + 16, height: 2 * ROW_H + 24,
      background: '#0E0F11', borderRadius: 18, border: `3px solid ${p.color}`,
      boxShadow: `0 18px 40px rgba(11,21,51,0.28), 0 0 0 6px ${p.color}22` }} />
    {p.rows!.map((l, i) => <MagRow key={l} lead={l} top={MAG_Y + i * (ROW_H + 8)} color={p.color!} baseline={p.baseline} win={p.win!} />)}
    {p.baseline ? (
      <div style={{ position: 'absolute', left: MAG_X + MAG_W - 210, top: MAG_Y + 2 * ROW_H + 26, width: 210, textAlign: 'right',
        fontFamily: MONO, fontSize: 18, letterSpacing: '0.08em', color: INK2 }}>
        - - - BASELINE
      </div>
    ) : null}
  </div>
);

const Big: React.FC<{ text: string; color: string; mono?: boolean; pop: number }> = ({ text, color, mono, pop }) => (
  <div style={{ position: 'absolute', left: SIDE, right: SIDE, top: TOP_Y + 92, textAlign: 'center',
    fontFamily: mono ? MONO : OUTFIT, fontWeight: 700, fontSize: mono ? 128 : 116, lineHeight: 1,
    letterSpacing: mono ? '0.04em' : '-0.015em', color, transform: `scale(${0.88 + 0.12 * pop})`, opacity: pop }}>
    {text}
  </div>
);

const Top: React.FC<{ t: number }> = ({ t }) => {
  const { fps } = useVideoConfig();
  const p = panelAt(t);
  if (!p) return null;
  const op = Math.min(fadeIn(t, p.from), fadeOut(t, p.to, 0.14));
  const pop = (at: number) => (t >= at ? spring({ frame: (t - at) * fps, fps, config: { damping: 16, stiffness: 190 } }) : 0);
  if (p.kind === 'title') {
    const s = pop(0.15);
    return (
      <div style={{ opacity: op }}>
        <Eyebrow text="ACLSMED SIM · NEW IN 2.8" color={RED} op={s} />
        <div style={{ position: 'absolute', left: SIDE, right: SIDE, top: TOP_Y + 74, textAlign: 'center', opacity: s,
          transform: `translateY(${(1 - s) * 24}px)`, fontFamily: OUTFIT, fontWeight: 700, fontSize: 120, lineHeight: 1,
          letterSpacing: '-0.02em', color: INK }}>
          Live <span style={{ color: RED }}>12-lead</span>
        </div>
        <div style={{ position: 'absolute', left: SIDE, right: SIDE, top: TOP_Y + 214, textAlign: 'center', opacity: pop(0.45),
          fontFamily: MONO, fontWeight: 600, fontSize: 26, letterSpacing: '0.2em', color: INK2 }}>
          ON THE PATIENT MONITOR
        </div>
      </div>
    );
  }
  if (p.kind === 'lead') {
    const steps = p.steps!;
    let k = 0;
    steps.forEach((s, i) => { if (t >= s[0]) k = i; });
    const at = k === 0 ? p.from : steps[k][0];
    return (
      <div style={{ opacity: op }}>
        <Eyebrow text={p.eyebrow!} color={INK2} op={1} />
        <Big text={steps[k][1]} color={p.color!} mono pop={pop(at)} />
      </div>
    );
  }
  if (p.kind === 'big') {
    return (
      <div style={{ opacity: op }}>
        <Eyebrow text={p.eyebrow!} color={p.color === C.red ? RED : p.color!} op={1} />
        <Big text={p.text!} color={p.text === 'The whole picture' ? INK : p.color!} mono={p.mono} pop={pop(p.from)} />
        {p.outlines ? (
          <div style={{ position: 'absolute', left: SIDE, right: SIDE, top: TOP_Y + 236, textAlign: 'center', opacity: pop(p.from + 0.25),
            fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: '0.1em' }}>
            <span style={{ color: C.red }}>ST UP · I aVL V1-V4</span>
            <span style={{ color: INK2 }}>{'   '}</span>
            <span style={{ color: C.blue }}>ST DOWN · III aVF</span>
          </div>
        ) : null}
      </div>
    );
  }
  if (p.kind === 'mag') {
    return (
      <>
        <Eyebrow text={p.eyebrow!} color={p.color!} op={op} />
        <Magnifier p={p} op={op} />
      </>
    );
  }
  if (p.kind === 'compare') {
    const a = pop(p.from + 0.1);
    const b = pop(p.at2!);
    const row = (label: string, value: string, vColor: string, s: number, top: number, dim: boolean) => (
      <div style={{ position: 'absolute', left: SIDE + 20, right: SIDE + 20, top, display: 'flex', alignItems: 'baseline',
        justifyContent: 'space-between', opacity: s, transform: `translateX(${(1 - s) * 30}px)` }}>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 40, color: dim ? INK2 : INK }}>{label}</div>
        <div style={{ fontFamily: OUTFIT, fontWeight: 700, fontSize: dim ? 74 : 86, color: vColor,
          textDecoration: dim ? 'line-through' : 'none', textDecorationThickness: 5 }}>{value}</div>
      </div>
    );
    return (
      <div style={{ opacity: op }}>
        {row('Most code simulators', '1 lead', 'rgba(11,21,51,0.45)', a, TOP_Y + 40, true)}
        <div style={{ position: 'absolute', left: SIDE + 20, right: SIDE + 20, top: TOP_Y + 168, height: 2,
          background: 'rgba(11,21,51,0.14)', opacity: b }} />
        {row('ACLSMED Sim', '12, live', RED, b, TOP_Y + 196, false)}
      </div>
    );
  }
  return null;
};

// ── Captions: the narration's own words, word by word ───────────────────────
type Word = { w: string; start: number; end: number };
type Line = { id: string; start: number; end: number; words: Word[] };
const LINES = TL.lines as Line[];
const textOf = (ws: Word[]) => ws.map((x) => x.w).join(' ');
const chunks = (ws: Word[]) => {
  if (textOf(ws).length <= 58) return [ws];
  const phrases: Word[][] = [];
  let cur: Word[] = [];
  for (const w of ws) { cur.push(w); if (/[,.?]$/.test(w.w)) { phrases.push(cur); cur = []; } }
  if (cur.length) phrases.push(cur);
  const out: Word[][] = [];
  for (const p of phrases) {
    const last = out[out.length - 1];
    if (last && textOf([...last, ...p]).length <= 56) out[out.length - 1] = [...last, ...p];
    else out.push(p);
  }
  return out;
};
const KEY = /^(II|V1|aVF|aVL|III|I|V4|12|12-lead|12-lead,|leads,|48|108,|STEMI\.|ST|elevation|reciprocal|Pause|Print|live\.|ACLSMED)$/;
const Caption: React.FC<{ t: number; line: Line; top: number; size?: number; keyColor?: string }> = ({ t, line, top, size = 44, keyColor }) => {
  const i = LINES.indexOf(line);
  const next = LINES[i + 1];
  const show0 = line.start - 0.12;
  const show1 = Math.min(line.end + 0.45, next ? next.start - 0.15 : 1e9);
  if (t < show0 || t > show1) return null;
  const parts = chunks(line.words);
  let k = 0;
  parts.forEach((p, j) => { if (t >= p[0].start - 0.12) k = j; });
  const part = parts[k];
  const partIn = k === 0 ? show0 : part[0].start - 0.12;
  const op = Math.min(fadeIn(t, partIn, 0.12), fadeOut(t, show1, 0.15));
  return (
    <div style={{ position: 'absolute', left: SIDE + 10, right: SIDE + 10, top, textAlign: 'center', opacity: op,
      fontFamily: SANS, fontWeight: 700, fontSize: size, lineHeight: 1.16, letterSpacing: '-0.005em' }}>
      {part.map((w, j) => {
        const said = t >= w.start - 0.03;
        const isKey = KEY.test(w.w.replace(/[.,]$/, '')) || KEY.test(w.w);
        return (
          <span key={j} style={{ color: isKey ? (keyColor || RED) : INK, opacity: said ? 1 : 0.32 }}>
            {w.w}{j < part.length - 1 ? ' ' : ''}
          </span>
        );
      })}
    </div>
  );
};

const Disclaimer: React.FC = () => (
  <div style={{ position: 'absolute', left: 0, right: 0, top: SAFE_BOTTOM - 40, textAlign: 'center',
    fontFamily: MONO, fontWeight: 400, fontSize: 21, letterSpacing: '0.08em', color: INK2 }}>
    Educational only, not diagnostic
  </div>
);

// ── Outro: icon, name, both stores, the site ────────────────────────────────
const Outro: React.FC<{ t: number }> = ({ t }) => {
  const { fps } = useVideoConfig();
  if (t < END_AT) return null;
  const a = (d: number) => spring({ frame: Math.max(0, (t - END_AT - d) * fps), fps, config: { damping: 16, stiffness: 150 } });
  const l10 = LINES.find((l) => l.id === 'l10')!;
  const siteAt = l10.words.find((w) => w.w === 'ACLSmed')!.start;
  const b = (at: number) => (t >= at - 0.05 ? spring({ frame: (t - at + 0.05) * fps, fps, config: { damping: 14, stiffness: 200 } }) : 0);
  const end = interpolate(t, [TL.duration - 0.4, TL.duration], [1, 0], { extrapolateLeft: 'clamp' });
  return (
    <AbsoluteFill style={{ opacity: end }}>
      <div style={{ position: 'absolute', left: 0, right: 0, top: 360, textAlign: 'center' }}>
        <Img src={staticFile('app-icon.png')} style={{ width: 236, height: 236, borderRadius: 54,
          boxShadow: '0 22px 50px rgba(11,21,51,0.30), 0 0 0 1px rgba(11,21,51,0.08)',
          opacity: a(0), transform: `scale(${0.8 + 0.2 * a(0)})` }} />
        <div style={{ marginTop: 44, fontFamily: OUTFIT, fontWeight: 700, fontSize: 104, lineHeight: 1, color: INK, opacity: a(0.12) }}>
          ACLS<span style={{ color: RED }}>MED</span> <span style={{ fontWeight: 500 }}>Sim</span>
        </div>
        <div style={{ marginTop: 22, fontFamily: MONO, fontWeight: 600, fontSize: 26, letterSpacing: '0.18em', color: INK2, opacity: a(0.24) }}>
          LIVE 12-LEAD · NEW IN 2.8
        </div>
        <div style={{ marginTop: 56, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 28, opacity: a(0.36) }}>
          <Img src={staticFile('badge-app-store.png')} style={{ height: 100 }} />
          <Img src={staticFile('badge-google-play.png')} style={{ height: 100 }} />
        </div>
        <div style={{ marginTop: 64, fontFamily: OUTFIT, fontWeight: 700, fontSize: 72, letterSpacing: '0.03em', color: INK,
          opacity: b(siteAt), transform: `translateY(${(1 - b(siteAt)) * 18}px)` }}>
          ACLS<span style={{ color: RED }}>MED</span>.COM
        </div>
      </div>
      <Caption t={t} line={l10} top={1330} size={40} />
      <Disclaimer />
    </AbsoluteFill>
  );
};

export const Live12Lead: React.FC = () => {
  const frame = useCurrentFrame();
  const t = sec(frame);
  const ipadOut = interpolate(t, [END_AT - 0.35, END_AT], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
    easing: Easing.in(Easing.cubic) });
  return (
    <AbsoluteFill style={{ background: `linear-gradient(180deg, ${BG_TOP} 0%, ${BG_BOT} 100%)` }}>
      <AbsoluteFill style={{ background: `radial-gradient(ellipse 760px 560px at 540px ${DEV_Y + DEV_H / 2}px, rgba(255,255,255,0.95), rgba(255,255,255,0) 70%)` }} />
      {t < END_AT ? <IPad t={t} opacity={ipadOut} y={(1 - ipadOut) * 40} /> : null}
      {t < END_AT ? <Top t={t} /> : null}
      {LINES.filter((l) => l.id !== 'l10').map((l) => <Caption key={l.id} t={t} line={l} top={CAPTION_Y} />)}
      <Outro t={t} />
      <Audio src={staticFile('audio.wav')} />
    </AbsoluteFill>
  );
};
