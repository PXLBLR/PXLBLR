import React from 'react';
import { AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, staticFile, useCurrentFrame } from 'remotion';
import { continueRender, delayRender } from 'remotion';
import alignment from './alignment.json';
import bezel from './bezel.json';

// Brand fonts from the repo (variable TTFs), loaded locally so the render never depends on the network.
const OUTFIT = 'Outfit';
const MONO = 'JetBrains Mono';
const fontHandle = delayRender('fonts');
Promise.all(
  [[OUTFIT, 'Outfit.ttf'], [MONO, 'JetBrainsMono.ttf']].map(([family, file]) =>
    new FontFace(family, `url(${staticFile(file)})`, { weight: '100 900' }).load().then((f) => document.fonts.add(f))),
).then(() => continueRender(fontHandle));

const NAVY = '#05081A';
const RED = '#EF4444';
const CYAN = '#00DCC8';
const CREAM = '#F2EEE3';

export const FPS = 30;
export const SECONDS = 30;

// Which shell plays each second comes from align.py (src/alignment.json): ten
// slots x three passes = 30 cuts, ending on the shell before the opener so the
// loop seam is just the next cut. Each second is a 1 s clip cut from a real
// simulator take at the same film-clock instant (public/segments/sNN.mp4).
export const SEGMENTS = alignment.segments as { second: number; shell: string; take: string }[];

export const LABELS: Record<string, string> = {
  console: 'CONSOLE',
  consoleWhite: 'CONSOLE WHITE',
  brushedMetal: 'MEDIC · BRUSHED METAL',
  whiteBlue: 'MEDIC · CLINICAL WHITE',
  hospital: 'HOSPITAL · CHARCOAL',
  hospitalWhiteBlue: 'HOSPITAL · WHITE / BLUE',
  transportRed: 'TRANSPORT · RED',
  transportBeige: 'TRANSPORT · BEIGE',
  classic: 'MONITOR',
};

export const shellAt = (second: number) => SEGMENTS[second % SEGMENTS.length].shell;

// Instagram Reels safe zones: keep text below y=250 and above y=1580.
const SAFE_TOP = 250;
const SAFE_BOTTOM = 1920 - 340;

// The iPad: Apple's iPad Pro 13" (M5) body from the Simulator's own display mask
// and the device's published outside size (ACLSMED iOS scripts/bezel_composite.swift
// --emit-bezel), laid over the full-screen clips. 920 px wide leaves 80 px clear on
// each side, so Instagram's edge crop and rounded corners never reach the bezel.
const DEV_W = 920;
const K = DEV_W / bezel.width; // bezel.png is drawn at 2x
const DEV_H = Math.round(bezel.height * K); // 704
const DEV_X = (1080 - DEV_W) / 2;
const DEV_Y = Math.round((SAFE_TOP + SAFE_BOTTOM) / 2 - DEV_H / 2); // centred between the safe lines
// The screen: the measured aperture, grown 1 px under the opaque bezel edge so no gap shows.
const SCR = {
  x: DEV_X + bezel.aperture.x * K - 1,
  y: DEV_Y + bezel.aperture.y * K - 1,
  w: bezel.aperture.w * K + 2,
  h: (bezel.aperture.w * K + 2) * (1032 / 1376), // clips are the whole 1376x1032 display
};

const Headline: React.FC = () => (
  <div
    style={{
      position: 'absolute', left: 90, right: 90, top: Math.round((SAFE_TOP + DEV_Y) / 2 - 72), textAlign: 'center',
      fontFamily: OUTFIT, fontWeight: 600, fontSize: 64, lineHeight: 1.12, letterSpacing: '-0.01em', color: CREAM,
    }}
  >
    Simulation has just gotten
    <br />a new upgrade<span style={{ color: CYAN }}>...</span>
  </div>
);

const Footer: React.FC<{ label?: string }> = ({ label }) => (
  <>
    {label ? (
      <div style={{ position: 'absolute', left: 0, right: 0, top: DEV_Y + DEV_H + 22, textAlign: 'center',
        fontFamily: MONO, fontWeight: 500, fontSize: 22, letterSpacing: '0.2em', color: 'rgba(242,238,227,0.55)' }}>
        {label}
      </div>
    ) : null}
    <div style={{ position: 'absolute', left: 0, right: 0, top: DEV_Y + DEV_H + 78, textAlign: 'center',
      fontFamily: MONO, fontWeight: 700, fontSize: 28, letterSpacing: '0.16em', color: CREAM }}>
      INTEGRATED <span style={{ color: RED }}>·</span> IMMERSIVE <span style={{ color: RED }}>·</span> ESSENTIAL
    </div>
    <div style={{ position: 'absolute', left: 0, right: 0, top: DEV_Y + DEV_H + 122, textAlign: 'center',
      fontFamily: OUTFIT, fontWeight: 700, fontSize: 50, letterSpacing: '0.04em', color: CREAM }}>
      ACLS<span style={{ color: RED }}>MED</span>.COM
    </div>
    <div style={{ position: 'absolute', left: 0, right: 0, top: SAFE_BOTTOM - 36, textAlign: 'center',
      fontFamily: MONO, fontWeight: 400, fontSize: 19, letterSpacing: '0.08em', color: 'rgba(242,238,227,0.5)' }}>
      Educational only, not diagnostic
    </div>
  </>
);

export const ShellLoop: React.FC<{ showLabel?: boolean }> = ({ showLabel = false }) => {
  const frame = useCurrentFrame();
  const second = Math.floor(frame / FPS);
  const plates = Array.from({ length: SECONDS }, (_, k) => k);
  return (
    <AbsoluteFill style={{ background: NAVY }}>
      {/* soft glow behind the iPad */}
      <AbsoluteFill
        style={{ background: `radial-gradient(ellipse 700px 520px at 540px ${DEV_Y + DEV_H / 2}px, rgba(0,220,200,0.10), rgba(5,8,26,0) 70%)` }}
      />
      {/* A hard cut every second: each clip is its shell at the same film-clock instant. */}
      <div style={{ position: 'absolute', left: SCR.x, top: SCR.y, width: SCR.w, height: SCR.h, overflow: 'hidden', background: '#000' }}>
        {plates.map((k) => (
          <Sequence key={k} from={k * FPS} durationInFrames={FPS} layout="none">
            <OffthreadVideo
              src={staticFile(`segments/s${String(k).padStart(2, '0')}.mp4`)}
              muted
              style={{ width: SCR.w, height: SCR.h, display: 'block' }}
            />
          </Sequence>
        ))}
      </div>
      <Img
        src={staticFile('bezel.png')}
        style={{ position: 'absolute', left: DEV_X, top: DEV_Y, width: DEV_W, height: DEV_H,
          filter: 'drop-shadow(0 26px 46px rgba(0,0,0,0.6))' }}
      />
      <Headline />
      <Footer label={showLabel ? LABELS[shellAt(second)] : undefined} />
      <Audio src={staticFile('audio.wav')} />
    </AbsoluteFill>
  );
};
