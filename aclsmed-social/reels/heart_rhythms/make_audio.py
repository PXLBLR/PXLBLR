"""Sound for a heart-rhythm reel, timed from src/timeline.json.

- Voice: the owner's narration ("Mikko (narration) v2", Prayer Voice.app on the Mac) from public/vo/ -- either one
  continuous take (full.wav) or one file per line (l1.wav ...). Each clip gets 15 ms fades, DC removal and a common
  loudness so lines match; the bed ducks under it smoothly so the read sounds like one natural voice-over.
- The app's own QRS beep on every sinus R wave, the V-fib alarm, a few soft transitions, and a quiet pad.
Run make_timeline.py first.
"""
import json
import sys
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from engine import sfx  # noqa: E402

SR = sfx.SR
TL = json.loads((HERE / "src" / "timeline.json").read_text())
VO = HERE / "public" / "vo"
DUR = TL["duration"]
N = int(DUR * SR)


def read_wav(p):
    with wave.open(str(p)) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
        if w.getnchannels() == 2:
            x = x.reshape(-1, 2).mean(1)
        if w.getframerate() != SR:
            n = int(len(x) * SR / w.getframerate())
            x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x)
    return x


def polish(x):
    x = x - x.mean()
    f = int(0.015 * SR)
    if len(x) > 2 * f:
        x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    rms = np.sqrt(np.mean(x[np.abs(x) > 0.01] ** 2)) if np.any(np.abs(x) > 0.01) else 1
    return x * (0.12 / rms)  # same speaking level for every clip


def place(buf, t, x):
    i = int(t * SR); x = x[: max(0, len(buf) - i)]; buf[i:i + len(x)] += x


voice = np.zeros(N)
if TL["mode"] == "full":
    place(voice, 0.4, polish(read_wav(VO / "full.wav")))
elif TL["mode"] == "lines":
    for ln in TL["lines"]:
        place(voice, ln["at"], polish(read_wav(VO / f"{ln['id']}.wav")))

beep = read_wav(HERE / "public" / "heart_beep.wav")
fx = np.zeros(N)
for k in range(200):
    r = k * 0.8 + 0.225
    if r >= TL["vf_start"]:
        break
    place(fx, r, beep * 0.35)
vf = TL["vf_start"]
for t0, name, g in [(vf, "whoosh", 0.5), (vf + 0.1, "alarm", 0.4), (vf + 2.0, "alarm", 0.25), (vf + 4.0, "alarm", 0.2),
                    (TL["nopulse"], "buzzer", 0.25), (TL["action"], "charge", 0.3), (TL["end_card"], "whoosh_down", 0.4),
                    (TL["end_card"] + 0.4, "ding", 0.3)]:
    place(fx, t0, sfx.get(name) * g)

bed = sfx.bed(DUR)[:N] * 2.2
# Smooth duck: bed and effects drop ~8 dB while the voice is up, with slow attack/release so nothing pumps.
env = np.abs(voice)
win = int(0.25 * SR)
env = np.convolve(env, np.ones(win) / win, mode="same")
duck = 1 - 0.6 * np.clip(env / 0.03, 0, 1)
mix = voice + (bed + fx * 0.8) * duck
mix = np.tanh(mix / (np.abs(mix).max() or 1) * 1.15) * 0.89
sfx.write_wav(HERE / "public" / "audio.wav", mix)
print("wrote public/audio.wav", TL["mode"], f"{DUR:.1f}s")
