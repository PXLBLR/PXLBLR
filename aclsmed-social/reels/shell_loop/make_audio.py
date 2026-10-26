"""Sound for the shell-loop reel (30 s, loops seamlessly).

- A soft tick on every shell change (engine/sfx.py `tick`, synthesized).
- The monitor's QRS beep on every R wave drawn on screen: ACLSMED Sim's own
  `heart_beep.wav` (copied from the app's Resources/Sounds). The app fires
  that beep from its own HR timer, not from the drawn R wave, and simctl
  records no sound, so the beep is laid here on the beat grid measured from
  the footage by align.py (`rPhase`).

Everything is mixed into a circular 30 s buffer: a sound that runs past the
end continues at the start, so the loop has no seam. HR 76 puts exactly 38
beats in 30 s.

    python3 make_audio.py        -> public/audio.wav
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
A = json.loads((HERE / "src" / "alignment.json").read_text())
DUR, F0, HR = A["duration"], A["F0"], A["hr"]
N = int(round(DUR * SR))


def load_beep():
    with wave.open(str(HERE / "public" / "heart_beep.wav")) as w:
        assert w.getframerate() == SR
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, w.getnchannels())
    x = x[:, 0].astype(np.float64) / 32768
    onset = int(np.argmax(np.abs(x) > 0.05 * np.abs(x).max()))
    x = x[max(0, onset - int(0.002 * SR)):]           # onset lands on the R wave
    return x / np.abs(x).max()


def place(buf, t, s, gain):
    i = int(round(t * SR)) % N
    idx = (np.arange(s.size) + i) % N                  # wrap past the end -> loop start
    np.add.at(buf, idx, s * gain)


def main():
    out = np.zeros(N)
    beep = load_beep()
    period = 60.0 / HR
    # R waves on the film clock are rPhase + j*period; the reel shows F0 .. F0+DUR.
    j0 = int(np.ceil((F0 - A["rPhase"]) / period))
    beats = []
    while True:
        t = A["rPhase"] + j0 * period - F0
        if t >= DUR - 1e-6:
            break
        beats.append(t)
        place(out, t, beep, 0.55)
        j0 += 1
    for k in range(int(DUR)):
        place(out, float(k), sfx.tick(), 0.55)
    peak = np.abs(out).max()
    out = out / peak * 0.89                             # ~ -1 dBFS
    sfx.write_wav(HERE / "public" / "audio.wav", out)
    print(f"wrote public/audio.wav: {len(beats)} beeps, {int(DUR)} ticks, first beep at {beats[0]:.3f} s")


if __name__ == "__main__":
    main()
