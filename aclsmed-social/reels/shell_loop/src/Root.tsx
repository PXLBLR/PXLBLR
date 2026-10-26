import React from 'react';
import { Composition } from 'remotion';
import { FPS, SECONDS, ShellLoop } from './ShellLoop';

export const Root: React.FC = () => (
  <>
    <Composition id="ShellLoop" component={ShellLoop} durationInFrames={SECONDS * FPS} fps={FPS} width={1080} height={1920}
      defaultProps={{ showLabel: false }} />
    <Composition id="ShellLoopLabeled" component={ShellLoop} durationInFrames={SECONDS * FPS} fps={FPS} width={1080} height={1920}
      defaultProps={{ showLabel: true }} />
  </>
);
