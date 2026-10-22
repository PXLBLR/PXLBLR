// A generic book-style foldable drawn in CSS 3D: two panels on a hinge, a titanium-style rim and black
// bezels around every screen. Not a render of Apple's hardware and no Apple marks.
import React from 'react';

export const W = 420; // one panel
export const H = 640;
const RIM = 6; // metal frame
const BEZEL = 14; // black glass border around the display
const IN = RIM + BEZEL; // 20: inner display is (2W - 2*IN) x (H - 2*IN) = 800 x 600, exactly 4:3
export const SCREEN_W = 2 * W - 2 * IN;
export const SCREEN_H = H - 2 * IN;

const metal = 'linear-gradient(135deg, #5b6170 0%, #23262e 22%, #3d424e 48%, #15171c 70%, #4a505d 100%)';

const radii = (l: boolean, r: boolean, v: number) => `${l ? v : 6}px ${r ? v : 6}px ${r ? v : 6}px ${l ? v : 6}px`;

const Rim: React.FC<{ l: boolean; r: boolean; children: React.ReactNode; style?: React.CSSProperties }> = ({ l, r, children, style }) => (
  <div style={{ position: 'absolute', inset: 0, borderRadius: radii(l, r, 46), background: metal,
    boxShadow: 'inset 0 0 0 1px rgba(255,255,255,0.18), inset 0 1px 2px rgba(255,255,255,0.35)', ...style }}>
    {/* black bezel */}
    <div style={{ position: 'absolute', inset: RIM, borderRadius: radii(l, r, 40), background: '#030405',
      boxShadow: 'inset 0 0 0 1px rgba(255,255,255,0.06)' }} />
    {children}
  </div>
);

type Props = {
  open: number; // 0 folded, 1 flat open
  yaw: number; pitch: number; scale: number; x?: number; y?: number;
  cover: React.ReactNode; // outer 5.4"-style display
  inner: React.ReactNode; // laid out at SCREEN_W x SCREEN_H, split across the hinge
  glow?: number;
};

export const Device: React.FC<Props> = ({ open, yaw, pitch, scale, x = 0, y = 0, cover, inner, glow = 0.5 }) => {
  const fold = -180 * (1 - open);
  const lift = 5 * (1 - open);
  const shift = (W / 2) * (1 - open); // keep the folded stack centred
  const screen = (offset: number, l: boolean, r: boolean): React.ReactNode => (
    <div style={{ position: 'absolute', top: IN, bottom: IN, left: l ? IN : 0, right: r ? IN : 0, overflow: 'hidden',
      borderRadius: radii(l, r, 30), background: '#000' }}>
      <div style={{ position: 'absolute', top: 0, left: offset, width: SCREEN_W, height: SCREEN_H }}>{inner}</div>
    </div>
  );
  return (
    <div style={{ position: 'absolute', left: 540 - W + x, top: 960 - H / 2 + y, width: 2 * W, height: H, perspective: 2600 }}>
      <div style={{ position: 'absolute', inset: 0, transformStyle: 'preserve-3d',
        transform: `translateX(${shift}px) scale(${scale}) rotateX(${pitch}deg) rotateY(${yaw}deg)` }}>
        {/* floor glow */}
        <div style={{ position: 'absolute', left: -120 + shift * 0, top: H - 40, width: 2 * W + 240, height: 160, borderRadius: '50%',
          background: `radial-gradient(ellipse, rgba(0,220,200,${0.35 * glow}) 0%, rgba(0,220,200,0) 70%)`, transform: 'translateZ(-60px)' }} />
        {/* left panel: inner display, bezel on three sides */}
        <div style={{ position: 'absolute', left: 0, top: 0, width: W, height: H, transformStyle: 'preserve-3d', borderRadius: radii(true, false, 46),
          boxShadow: `0 60px 120px -30px rgba(0,0,0,0.9), 0 0 140px rgba(0,220,200,${0.18 * glow})` }}>
          <Rim l r={false}>
            {screen(0, true, false)}
          </Rim>
        </div>
        {/* right panel: inner display (front) + cover display (back), hinged on its left edge */}
        <div style={{ position: 'absolute', left: W, top: 0, width: W, height: H, transformStyle: 'preserve-3d', transformOrigin: '0 50%',
          transform: `translateZ(${lift}px) rotateY(${fold}deg)` }}>
          <div style={{ position: 'absolute', inset: 0, backfaceVisibility: 'hidden' }}>
            <Rim l={false} r>{screen(-(W - IN), false, true)}</Rim>
            {/* crease */}
            <div style={{ position: 'absolute', left: 0, top: IN, bottom: IN, width: 10,
              background: 'linear-gradient(90deg, rgba(255,255,255,0.10), rgba(0,0,0,0.25), rgba(255,255,255,0))', opacity: open }} />
          </div>
          <div style={{ position: 'absolute', inset: 0, backfaceVisibility: 'hidden', transform: 'rotateY(180deg)' }}>
            <Rim l r>
              <div style={{ position: 'absolute', inset: IN, borderRadius: 30, overflow: 'hidden', background: '#000' }}>{cover}</div>
              {/* front camera */}
              <div style={{ position: 'absolute', top: IN + 14, left: '50%', width: 22, height: 22, marginLeft: -11, borderRadius: '50%',
                background: 'radial-gradient(circle at 35% 35%, #2b3448 0%, #000 60%)', boxShadow: '0 0 0 2px #0a0a0a' }} />
            </Rim>
          </div>
        </div>
        {/* hinge spine, visible when folded */}
        <div style={{ position: 'absolute', left: W - 10, top: 26, width: 16, height: H - 52, borderRadius: 8, opacity: 1 - open,
          background: 'linear-gradient(90deg, #15171c, #6a7080 45%, #1d2027)', transform: 'translateZ(2px)' }} />
      </div>
    </div>
  );
};
