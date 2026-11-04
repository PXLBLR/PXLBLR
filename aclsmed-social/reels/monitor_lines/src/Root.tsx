import React from 'react';
import { Composition } from 'remotion';
import { DURATION, FPS, MonitorLines } from './MonitorLines';

export const Root: React.FC = () => (
  <Composition id="MonitorLines" component={MonitorLines} durationInFrames={DURATION} fps={FPS} width={1080} height={1920} />
);
