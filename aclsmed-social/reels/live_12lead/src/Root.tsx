import React from 'react';
import { Composition } from 'remotion';
import { DURATION, FPS, Live12Lead } from './Live12Lead';

export const Root: React.FC = () => (
  <Composition id="Live12Lead" component={Live12Lead} durationInFrames={DURATION} fps={FPS} width={1080} height={1920} />
);
