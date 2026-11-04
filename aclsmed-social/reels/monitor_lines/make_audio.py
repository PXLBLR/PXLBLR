"""Sound for the monitor-lines reel -> public/audio.wav (48 kHz stereo).

- Narration: the ten lines in public/vo/ (local "Mikko (narration) v2" voice,
  Prayer Voice.app), each placed at its `at` time from timeline.json.
- Bed: engine/sfx.py `bed` (a quiet synthesized pad), ducked about 9 dB under
  the voice with a smooth envelope so it never pumps.
- The monitor's QRS beep, low: ACLSMED Sim's own `heart_beep.wav` (from the
  app's Resources/Sounds) on every R wave the footage draws. simctl records no
  sound and the app fires the beep from its own HR timer, so it is laid here on
  the film clock's beat grid (R at `R_PHASE` s into each 60/76 s beat, measured
  from the takes by check.py). Beeps run while the monitor is on screen.
- Small synthesized ticks on each lead change and each new line, pops on the
  end-card words and the store badges.

Loudness: integrated -14 LUFS, true peak under -1 dBFS (ffmpeg ebur128 /
loudnorm measure, then a plain gain).

    python3 make_audio.py
"""
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from engine import sfx  # noqa: E402

FF = str(Path.home() / ".local/bin/ffmpeg")
SR = 48000
TL = json.loads((HERE / "timeline.json").read_text())
WORDS = json.loads((HERE / "src" / "words.json").read_text())
DUR = TL["duration"]
N = int(round(DUR * SR))
F0, HR = TL["F0"], TL["hr"]
R_PHASE = 0.1717           # s into each beat on the film clock, measured on this reel's lead-II clips by check.py (shell reel: 0.1671)
SHOT = {s["id"]: s["from"] for s in TL["shots"]}


def read(path):
    with wave.open(str(path)) as w:
        sr, ch = w.getframerate(), w.getnchannels()
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64) / 32768
    if ch > 1:
        x = x.reshape(-1, ch).mean(1)
    return resample(x, sr)


def resample(x, sr):
    if sr == SR:
        return x
    t = np.arange(int(len(x) * SR / sr)) / SR
    return np.interp(t, np.arange(len(x)) / sr, x)


def place(buf, t, s, gain=1.0):
    i = int(round(t * SR))
    if i >= buf.size:
        return
    seg = s[: buf.size - i] * gain
    buf[i:i + seg.size] += seg


def smooth_env(x, attack, release):
    """One-pole follower on |x| with separate attack/release (s)."""
    a = np.exp(-1 / (attack * SR))
    r = np.exp(-1 / (release * SR))
    out = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(np.abs(x)):
        c = a if v > acc else r
        acc = c * acc + (1 - c) * v
        out[i] = acc
    return out


def main():
    voice = np.zeros(N)
    for line in TL["vo"]:
        place(voice, line["at"], read(HERE / "public" / "vo" / f"{line['id']}.wav"))

    # Bed, ducked under speech: gain 1 -> 0.35 while the voice is up.
    bed = resample(sfx.bed(DUR + 1.0, root=55.0), sfx.SR)[:N]
    dec = voice[::48]                                   # follower at 1 kHz keeps this fast
    env = smooth_env(dec, 0.004, 0.12)
    talking = np.clip(env / 0.02, 0, 1)
    talking = smooth_env(talking, 0.08, 0.45)
    duck = np.interp(np.arange(N) / SR, np.arange(dec.size) * 48 / SR, 1 - 0.65 * np.clip(talking, 0, 1))
    bed_gain = 2.2 * duck
    # Bed swells a little into the end card and closes with the outro.
    t = np.arange(N) / SR
    bed_gain *= np.interp(t, [0, 1.0, SHOT["end"], SHOT["end"] + 1.0, DUR - 1.2, DUR], [0.6, 1, 1, 1.25, 1.25, 0])

    fx = np.zeros(N)
    beep = read(HERE / "public" / "heart_beep.wav")
    onset = int(np.argmax(np.abs(beep) > 0.05 * np.abs(beep).max()))
    beep = beep[max(0, onset - int(0.002 * SR)):]
    beep /= np.abs(beep).max()
    period = 60.0 / HR
    beeps = []
    j = int(np.ceil((F0 - R_PHASE) / period))
    while True:
        tb = R_PHASE + j * period - F0
        if tb >= SHOT["end"] - 0.25:
            break
        if tb >= 0.15:
            beeps.append(tb)
            place(fx, tb, beep, 0.085)
        j += 1

    tick = resample(sfx.tick(), sfx.SR)
    pop = resample(sfx.pop(), sfx.SR)
    for s in TL["shots"]:
        if s["id"].startswith("lead") and s["id"] != "lead2":
            place(fx, s["from"], tick, 0.10)
        elif s["id"] in ("art", "pa", "cvp", "etco2", "spo2"):
            place(fx, s["from"], tick, 0.28)
            place(fx, s["from"], pop, 0.10)
    for w in next(l for l in WORDS if l["id"] == "l9")["words"]:
        place(fx, w["start"] - 0.02, pop, 0.22)
    l10 = next(l for l in WORDS if l["id"] == "l10")["words"]
    for word in ("App", "Google"):
        place(fx, next(w["start"] for w in l10 if w["w"] == word) - 0.04, pop, 0.22)

    mix = voice + bed * bed_gain + fx
    tmp = HERE / "out" / "audio_pre.wav"
    tmp.parent.mkdir(exist_ok=True)
    write(tmp, mix / np.abs(mix).max() * 0.5)
    meas = subprocess.run([FF, "-hide_banner", "-i", str(tmp), "-af", "loudnorm=print_format=json", "-f", "null", "-"],
                          capture_output=True, text=True).stderr
    js = json.loads(meas[meas.rindex("{"):meas.rindex("}") + 1])
    lufs, tp = float(js["input_i"]), float(js["input_tp"])
    # Gain to -14 LUFS, then a gentle look-ahead limiter (ffmpeg alimiter,
    # ceiling -1.5 dBFS) catches the voice peaks that gain pushes over.
    gain_db = -14.0 - lufs
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", str(tmp), "-af",
                    f"volume={gain_db:.2f}dB,alimiter=limit=0.84:attack=4:release=60:level=false",
                    "-ar", str(SR), "-c:a", "pcm_s16le", str(HERE / "public" / "audio.wav")], check=True)
    meas = subprocess.run([FF, "-hide_banner", "-i", str(HERE / "public" / "audio.wav"), "-af",
                           "loudnorm=print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    js2 = json.loads(meas[meas.rindex("{"):meas.rindex("}") + 1])
    out_lufs, out_tp = float(js2["input_i"]), float(js2["input_tp"])
    tmp.unlink()
    print(f"wrote public/audio.wav: {DUR:.2f} s, {len(beeps)} beeps (first {beeps[0]:.3f} s), "
          f"pre {lufs:.1f} LUFS / {tp:.1f} dBTP, gain {gain_db:+.1f} dB -> {out_lufs:.1f} LUFS, {out_tp:.1f} dBTP")


def write(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    st = np.repeat(pcm[:, None], 2, axis=1)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(st.tobytes())


if __name__ == "__main__":
    main()
