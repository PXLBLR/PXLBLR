import React from 'react';
import { Composition } from 'remotion';
import { HeartRhythm } from './HeartRhythm';
import { DATA } from './data';

// One composition per reel with a timeline (src/data/index.ts, written by make_timeline.py). Id: R02_pvt -> R02-pvt.
export const Root: React.FC = () => (
  <>
    {Object.entries(DATA).map(([id, d]) => (
      <Composition key={id} id={id.replace(/_/g, '-')} component={HeartRhythm} defaultProps={{ id }}
        durationInFrames={Math.round(d.timeline.duration * 30)} fps={30} width={1080} height={1920} />
    ))}
  </>
);
