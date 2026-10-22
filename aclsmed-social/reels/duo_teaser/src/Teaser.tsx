import React from 'react';
import { AbsoluteFill, Audio, Easing, Img, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { continueRender, delayRender } from 'remotion';
import { Device, SCREEN_H, SCREEN_W } from './Device';

// Brand fonts from the repo (variable TTFs), loaded locally so the render never depends on the network.
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

// Scene boundaries (30 fps)
const S_FOLD = 75; // folded device
const S_FLASH = 210; // flash into the hinge
const S_OPEN = 240; // unfold
const S_CUTS = 360; // feature cuts every 45 frames
const S_END = 540; // end card

const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;
const ease = Easing.bezier(0.22, 1, 0.36, 1);

const Kicker: React.FC<{ children: React.ReactNode; color?: string }> = ({ children, color = CYAN }) => (
  <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 30, letterSpacing: '0.22em', color }}>{children}</div>
);

// Words that rise in with a slight blur, trailer style.
const Rise: React.FC<{ at: number; children: React.ReactNode; style?: React.CSSProperties }> = ({ at, children, style }) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [at, at + 14], [0, 1], { ...clamp, easing: ease });
  return (
    <div style={{ opacity: p, transform: `translateY(${(1 - p) * 40}px)`, filter: `blur(${(1 - p) * 10}px)`, ...style }}>{children}</div>
  );
};

// ECG line that draws itself (synthetic sinus beats).
const ecgPath = (() => {
  let d = 'M -20 0';
  for (let i = 0; i < 4; i++) {
    const x = 60 + i * 300;
    d += ` L ${x} 0 Q ${x + 25} -22 ${x + 50} 0 L ${x + 80} 0 L ${x + 92} 14 L ${x + 108} -170 L ${x + 124} 44 L ${x + 136} 0 L ${x + 175} 0 Q ${x + 215} -48 ${x + 255} 0`;
  }
  return d + ' L 1120 0';
})();

const ColdOpen: React.FC = () => {
  const f = useCurrentFrame();
  const draw = interpolate(f, [0, 66], [0, 1], clamp);
  const out = interpolate(f, [64, 75], [1, 0], clamp);
  return (
    <AbsoluteFill style={{ background: '#000', opacity: out }}>
      <svg width={1080} height={1920} style={{ position: 'absolute' }}>
        <defs>
          <filter id="g"><feGaussianBlur stdDeviation="6" /></filter>
        </defs>
        <g transform="translate(0 1180)">
          {[{ w: 14, o: 0.5, fl: 'url(#g)' }, { w: 5, o: 1, fl: undefined }].map((s, i) => (
            <path key={i} d={ecgPath} fill="none" stroke={RED} strokeWidth={s.w} strokeLinejoin="round" strokeLinecap="round" opacity={s.o}
              filter={s.fl} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - draw} />
          ))}
        </g>
      </svg>
      <div style={{ position: 'absolute', top: 640, width: '100%', textAlign: 'center', color: CREAM, fontFamily: OUTFIT, fontWeight: 900,
        fontSize: 104, lineHeight: 1, letterSpacing: '-0.03em' }}>
        <Rise at={18}>Something's</Rise>
        <Rise at={34} style={{ color: CYAN }}>unfolding.</Rise>
      </div>
    </AbsoluteFill>
  );
};

// Cover display: app icon, a tap, then the app launching.
const Cover: React.FC<{ f: number }> = ({ f }) => {
  const tap = 63; // local frame of the tap
  const press = interpolate(f, [tap - 4, tap, tap + 4], [1, 0.86, 1], clamp);
  const launch = interpolate(f, [tap + 2, tap + 16], [0, 1], { ...clamp, easing: ease });
  return (
    <AbsoluteFill style={{ background: 'radial-gradient(120% 80% at 50% 30%, #13204a 0%, #05081A 60%, #000 100%)' }}>
      <div style={{ position: 'absolute', top: 70, width: '100%', textAlign: 'center', color: CREAM, fontFamily: SANS, fontWeight: 700, fontSize: 64,
        opacity: 1 - launch }}>7:30</div>
      <div style={{ position: 'absolute', top: 236, left: '50%', width: 120, height: 120, marginLeft: -60, borderRadius: 28, overflow: 'hidden',
        transform: `scale(${press})`, opacity: 1 - launch, boxShadow: `0 0 ${40 + 30 * Math.sin(f / 6)}px rgba(239,68,68,0.55)` }}>
        <Img src={staticFile('icon.png')} style={{ width: '100%', height: '100%' }} />
      </div>
      <div style={{ position: 'absolute', top: 372, width: '100%', textAlign: 'center', color: CREAM, fontFamily: SANS, fontWeight: 500, fontSize: 22,
        opacity: 1 - launch }}>ACLSMED SIM</div>
      {/* tap ripple */}
      <div style={{ position: 'absolute', top: 296, left: '50%', width: 10, height: 10, marginLeft: -5, marginTop: -5, borderRadius: '50%',
        border: `3px solid ${CREAM}`, opacity: interpolate(f, [tap - 2, tap + 12], [0.9, 0], clamp),
        transform: `scale(${interpolate(f, [tap - 2, tap + 12], [1, 22], clamp)})`, display: f < tap - 2 ? 'none' : 'block' }} />
      {/* launch: splash grows out of the icon */}
      <AbsoluteFill style={{ background: NAVY, opacity: launch, transform: `scale(${0.4 + 0.6 * launch})`, display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center', gap: 22 }}>
        <Img src={staticFile('icon.png')} style={{ width: 132, height: 132, borderRadius: 30 }} />
        <div style={{ fontFamily: OUTFIT, fontWeight: 900, fontSize: 44, color: '#fff', letterSpacing: '-0.02em' }}>
          ACLS<span style={{ color: RED }}>MED</span>
        </div>
        <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 16, letterSpacing: '0.3em', color: CYAN }}>SIM</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const Shot: React.FC<{ src: string; zoom?: number }> = ({ src, zoom = 1 }) => (
  <Img src={staticFile(src)} style={{ width: SCREEN_W, height: SCREEN_H, objectFit: 'cover', transform: `scale(${zoom})` }} />
);

const CUTS = [
  { src: 'fig-monitor-charged.jpg', word: 'Defib.', kicker: 'CHARGE · SHOCK' },
  { src: 'fig-12lead.jpg', word: '12-lead.', kicker: 'READ IT BIG' },
  { src: 'fig-respmed-main.jpg', word: 'Ventilator.', kicker: 'RESPMED' },
  { src: 'fig-monitor-megacodes.jpg', word: 'MegaCodes.', kicker: 'RUN THE CODE' },
];

const DeviceStage: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const g = f + S_FOLD; // global frame
  const appear = spring({ frame: f, fps, config: { damping: 18, mass: 0.9 } });
  const open = spring({ frame: g - (S_OPEN + 6), fps, config: { damping: 15, stiffness: 70, mass: 1.1 } });
  const cutIdx = Math.max(-1, Math.min(3, Math.floor((g - S_CUTS) / 45)));
  const cutLocal = g - S_CUTS - cutIdx * 45;
  const punch = cutIdx >= 0 ? interpolate(cutLocal, [0, 12], [1.07, 1], { ...clamp, easing: ease }) : 1;

  // Camera: slow orbit while folded, snap face-on at the flash, gentle drift while open.
  const yaw = g < S_FLASH
    ? interpolate(g, [S_FOLD, S_FLASH], [-32, 14], { ...clamp, easing: Easing.inOut(Easing.sin) })
    : g < S_CUTS
      ? interpolate(g, [S_FLASH, S_FLASH + 10, S_CUTS], [14, 0, -5], { ...clamp, easing: ease })
      : (cutIdx % 2 === 0 ? -1 : 1) * interpolate(cutLocal, [0, 45], [7, 3], clamp);
  const pitch = g < S_FLASH ? interpolate(g, [S_FOLD, S_FLASH], [14, 6], clamp) : interpolate(g, [S_FLASH, S_OPEN + 30], [6, 2], clamp);
  const baseScale = g < S_FLASH
    ? interpolate(g, [S_FOLD, S_FLASH], [1.12, 1.32], clamp) * (0.6 + 0.4 * appear)
    : interpolate(open, [0, 1], [1.3, 1.12]);
  const exit = interpolate(g, [S_END - 12, S_END + 6], [0, 1], { ...clamp, easing: Easing.in(Easing.cubic) });

  const inner = cutIdx < 0 ? <Shot src="fig-monitor.jpg" zoom={interpolate(g, [S_OPEN, S_CUTS], [1.08, 1], clamp)} />
    : <Shot src={CUTS[cutIdx].src} zoom={interpolate(cutLocal, [0, 45], [1.0, 1.06], clamp)} />;

  return (
    <AbsoluteFill style={{ background: `radial-gradient(90% 55% at 50% 50%, #101a3c 0%, ${NAVY} 55%, #000 100%)` }}>
      {/* light sweep */}
      <div style={{ position: 'absolute', inset: -400, opacity: 0.22,
        background: `linear-gradient(105deg, transparent 40%, rgba(255,255,255,0.5) 50%, transparent 60%)`,
        transform: `translateX(${interpolate(g % 150, [0, 150], [-900, 900])}px)` }} />
      <div style={{ position: 'absolute', inset: 0, opacity: 1 - exit, transform: `translateY(${exit * -120}px) scale(${1 - exit * 0.2})`,
        filter: `blur(${exit * 14}px)` }}>
        <Device open={open} yaw={yaw} pitch={pitch} scale={baseScale * punch} y={g < S_CUTS ? 40 : 60}
          cover={<Cover f={g - S_FOLD} />} inner={inner} glow={0.6 + 0.4 * open} />
      </div>

      {/* Folded titles */}
      <Sequence from={10} durationInFrames={S_FLASH - S_FOLD - 10} layout="none">
        <div style={{ position: 'absolute', top: 290, width: '100%', textAlign: 'center' }}>
          <Rise at={0}><Kicker>IPHONE DUO · LAUNCH DAY</Kicker></Rise>
          <Rise at={10} style={{ fontFamily: OUTFIT, fontWeight: 900, fontSize: 96, color: CREAM, letterSpacing: '-0.03em', marginTop: 14 }}>Folded.</Rise>
        </div>
      </Sequence>
      {/* Open titles */}
      <Sequence from={S_OPEN + 20 - S_FOLD} durationInFrames={S_CUTS - S_OPEN - 20} layout="none">
        <div style={{ position: 'absolute', top: 290, width: '100%', textAlign: 'center' }}>
          <Rise at={0} style={{ fontFamily: OUTFIT, fontWeight: 900, fontSize: 96, color: CREAM, letterSpacing: '-0.03em' }}>Unfolded.</Rise>
        </div>
        <div style={{ position: 'absolute', top: 1390, width: '100%', textAlign: 'center', fontFamily: OUTFIT, fontWeight: 700, fontSize: 56,
          color: CREAM, lineHeight: 1.15 }}>
          <Rise at={30}>The full monitor.</Rise>
          <Rise at={44} style={{ color: CYAN }}>In your pocket.</Rise>
        </div>
      </Sequence>
      {/* Feature cut titles */}
      {CUTS.map((c, i) => (
        <Sequence key={c.word} from={S_CUTS + i * 45 - S_FOLD} durationInFrames={45} layout="none">
          <div style={{ position: 'absolute', top: 290, width: '100%', textAlign: 'center' }}>
            <Rise at={0}><Kicker color={i % 2 ? CYAN : RED}>{c.kicker}</Kicker></Rise>
            <Rise at={3} style={{ fontFamily: OUTFIT, fontWeight: 900, fontSize: 110, color: CREAM, letterSpacing: '-0.03em', marginTop: 10 }}>{c.word}</Rise>
          </div>
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

const Flash: React.FC<{ at: number; len?: number; peak?: number }> = ({ at, len = 14, peak = 1 }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [at, at + 2, at + len], [0, peak, 0], clamp);
  return <AbsoluteFill style={{ background: `radial-gradient(circle at 50% 50%, #fff 0%, #bff8f2 40%, rgba(0,220,200,0.6) 100%)`, opacity: o, pointerEvents: 'none' }} />;
};

const EndCard: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame: f - 4, fps, config: { damping: 12 } });
  const fade = interpolate(f, [0, 10], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ background: `radial-gradient(80% 50% at 50% 42%, #142355 0%, ${NAVY} 60%, #000 100%)`, opacity: fade,
      alignItems: 'center' }}>
      <div style={{ position: 'absolute', top: 420, width: 230, height: 230, borderRadius: 52, overflow: 'hidden', transform: `scale(${pop})`,
        boxShadow: '0 0 120px rgba(239,68,68,0.55)' }}>
        <Img src={staticFile('icon.png')} style={{ width: '100%', height: '100%' }} />
      </div>
      <div style={{ position: 'absolute', top: 700, width: '100%', textAlign: 'center' }}>
        <Rise at={10} style={{ fontFamily: OUTFIT, fontWeight: 900, fontSize: 92, color: '#fff', letterSpacing: '-0.03em' }}>
          ACLS<span style={{ color: RED }}>MED</span> <span style={{ color: CYAN }}>SIM</span>
        </Rise>
        <Rise at={20} style={{ fontFamily: OUTFIT, fontWeight: 700, fontSize: 62, color: CREAM, marginTop: 26, lineHeight: 1.1 }}>
          Ready for iPhone Duo.
        </Rise>
        <Rise at={30} style={{ fontFamily: OUTFIT, fontWeight: 700, fontSize: 62, color: CYAN, lineHeight: 1.1 }}>Day one.</Rise>
        <Rise at={44} style={{ display: 'inline-flex', alignItems: 'center', gap: 16, marginTop: 56, padding: '20px 40px', borderRadius: 999,
          background: CREAM, color: NAVY, fontFamily: SANS, fontWeight: 700, fontSize: 40 }}>
          Comment <span style={{ fontFamily: MONO, fontSize: 44 }}>SIM</span>
        </Rise>
      </div>
      <Rise at={56} style={{ position: 'absolute', top: 1468, left: 90, right: 90, textAlign: 'center', fontFamily: SANS, fontWeight: 500,
        fontSize: 25, lineHeight: 1.4, color: 'rgba(242,238,227,0.7)' }}>
        Educational only, not diagnostic. Not affiliated with or endorsed by Apple. iPhone is a trademark of Apple Inc.
      </Rise>
    </AbsoluteFill>
  );
};

const Grain: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ pointerEvents: 'none', mixBlendMode: 'overlay', opacity: 0.18,
      backgroundImage: `repeating-radial-gradient(circle at ${(f * 37) % 100}% ${(f * 53) % 100}%, rgba(255,255,255,0.5) 0 1px, transparent 1px 3px)` }} />
  );
};

export const Teaser: React.FC = () => (
  <AbsoluteFill style={{ background: '#000' }}>
    <Audio src={staticFile('audio.wav')} />
    <Sequence durationInFrames={S_FOLD}><ColdOpen /></Sequence>
    <Sequence from={S_FOLD} durationInFrames={S_END - S_FOLD + 8}><DeviceStage /></Sequence>
    <Sequence from={S_END}><EndCard /></Sequence>
    <Flash at={S_FOLD - 2} len={10} peak={0.5} />
    <Flash at={S_FLASH} len={18} />
    {[0, 1, 2, 3].map((i) => <Flash key={i} at={S_CUTS + i * 45} len={6} peak={0.35} />)}
    <Flash at={S_END - 2} len={10} peak={0.6} />
    <AbsoluteFill style={{ pointerEvents: 'none', background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.55) 100%)' }} />
    <Grain />
  </AbsoluteFill>
);
