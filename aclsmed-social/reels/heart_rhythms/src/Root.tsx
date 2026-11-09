import React from 'react';
import { Composition } from 'remotion';
import { HeartRhythm } from './HeartRhythm';
import timeline from './timeline.json';

export const Root: React.FC = () => (
  <Composition id="HeartRhythm" component={HeartRhythm} durationInFrames={Math.round(timeline.duration * 30)} fps={30} width={1080} height={1920} />
);
