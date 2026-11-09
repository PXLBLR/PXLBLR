"""Mockup sound: the app's QRS beep on each sinus R wave, the V-fib alarm, a quiet pad. Voice-over is added later
(owner's Prayer Voice app on the Mac); this mix leaves room for it."""
import sys
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from engine import sfx  # noqa: E402

DUR, SR = 30.0, sfx.SR
VF_START = 6.5
R_TIMES = [i * 0.8 + 0.225 for i in range(9) if i * 0.8 + 0.225 < VF_START]


def read_wav(p):
    with wave.open(str(p)) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
        if w.getnchannels() == 2:
            x = x.reshape(-1, 2).mean(1)
        if w.getframerate() != SR:
            n = int(len(x) * SR / w.getframerate())
            x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x)
    return x


beep = read_wav(HERE / "public" / "heart_beep.wav")
sfx.SOUNDS["qrs"] = lambda: beep * 0.8
events = [(r, "qrs", 0.5) for r in R_TIMES]
events += [(VF_START, "whoosh", 0.6), (VF_START + 0.1, "alarm", 0.5), (8.0, "alarm", 0.35), (10.0, "alarm", 0.35), (12.0, "alarm", 0.3),
           (14.0, "buzzer", 0.4), (19.5, "charge", 0.5), (25.4, "whoosh_down", 0.5), (25.8, "ding", 0.4)]
out = sfx.mix(DUR, events, bed_level=0.8)
sfx.write_wav(HERE / "public" / "audio.wav", out)
print("wrote public/audio.wav")
