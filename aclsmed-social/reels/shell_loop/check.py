"""Frame checks on the rendered reel (aclsmed_shell_loop.mp4).

1. Traces: in every one of the 900 frames, each of the five lanes (ECG II, ART,
   PA, CVP, SpO2) of the shell on screen carries ITS channel's colour across the
   strip with real amplitude: no missing trace, no flatline, no sixth lane
   shifting the rows.
2. Audio loop: 38 QRS beeps on a 60/76 s grid, the gap across the loop seam
   equal to every other gap, and a tick on every second.

    python3 check.py
"""
import json
import subprocess
from pathlib import Path

import numpy as np

import align

HERE = Path(__file__).resolve().parent
FF = align.FF
VIDEO = HERE / "aclsmed_shell_loop.mp4"
A = json.loads((HERE / "src" / "alignment.json").read_text())
BZ = json.loads((HERE / "src" / "bezel.json").read_text())

# Same layout maths as src/ShellLoop.tsx
DEV_W = 920
K = DEV_W / BZ["width"]
DEV_H = round(BZ["height"] * K)
DEV_X = (1080 - DEV_W) / 2
DEV_Y = round((250 + 1580) / 2 - DEV_H / 2)
SCR_X = DEV_X + BZ["aperture"]["x"] * K - 1
SCR_Y = DEV_Y + BZ["aperture"]["y"] * K - 1
SCR_W = BZ["aperture"]["w"] * K + 2
D2R = align.S * SCR_W / 1376          # design px -> reel px


def classes(px):
    """Channel colours by hue, not brightness: at reel scale a 2.2 pt trace is
    ~1.3 px wide and anti-aliasing darkens most of its pixels."""
    r, g, b = px[..., 0].astype(int), px[..., 1].astype(int), px[..., 2].astype(int)
    lit = np.maximum(np.maximum(r, g), b) > 70
    return {
        "ECG": lit & (g >= r + 30) & (g >= b + 10),
        "ART": lit & (r >= g + 40) & (r >= b + 40),
        # H.264 4:2:0 chroma washes thin coloured lines out (PA reads as
        # 229,228,183 and SpO2 as 89,212,196 on single-pixel strokes).
        "PA": lit & (r > 120) & (g > 110) & ((r + g) // 2 - b > 25) & (abs(r - g) < 60),
        "CVP": lit & (b >= r + 10) & (b >= g - 5) & (r * 100 >= 55 * b),
        "SpO2": lit & (np.minimum(g, b) - r > 60) & (b >= g - 30) & (g > 90),
    }


def lanes(shell):
    strip_x, outer_w, top, bottom = align.GEOM[shell]
    row_h = (bottom - top - 4 * 14) / 5
    out = []
    for i, name in enumerate(["ECG", "ART", "PA", "CVP", "SpO2"]):
        y0 = SCR_Y + (top + i * (row_h + 14) + 0.18 * row_h) * D2R
        y1 = SCR_Y + (top + i * (row_h + 14) + row_h) * D2R
        x0 = SCR_X + (strip_x + 240) * D2R          # clear of the lane caption
        x1 = SCR_X + (strip_x + outer_w - 172 - 6) * D2R
        out.append((name, int(x0), int(x1), int(y0), int(y1)))
    return out


def trace_check():
    worst = {}
    fails = []
    p = subprocess.Popen([FF, "-loglevel", "error", "-i", str(VIDEO), "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    n = 1080 * 1920 * 3
    f = 0
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        img = np.frombuffer(b, np.uint8).reshape(1920, 1080, 3)
        shell = A["segments"][f // 30]["shell"]
        for name, x0, x1, y0, y1 in lanes(shell):
            m = classes(img[y0:y1, x0:x1])[name]
            cover = m.any(axis=0).mean()
            ys = np.nonzero(m)[0]
            amp = float(np.percentile(ys, 98) - np.percentile(ys, 2)) if ys.size else 0.0
            w = worst.setdefault(name, [1.0, 1e9])
            w[0], w[1] = min(w[0], cover), min(w[1], amp)
            if cover < 0.85 or amp < 6:
                fails.append((f, shell, name, round(cover, 2), round(amp, 1)))
        f += 1
    p.wait()
    print(f"traces: {f} frames checked")
    for name, (c, a) in worst.items():
        print(f"  {name:5s} lowest coverage {c*100:5.1f}%   lowest amplitude {a:5.1f} px")
    print(f"  failures: {len(fails)}" + (f"  first: {fails[:5]}" if fails else ""))
    return f == 900 and not fails


def audio_check():
    raw = subprocess.run([FF, "-loglevel", "error", "-i", str(VIDEO), "-ac", "1", "-ar", "48000",
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32)
    sr = 48000
    dur = x.size / sr
    env = np.abs(x)
    hop = int(0.002 * sr)
    e = np.array([env[i:i + hop].max() for i in range(0, env.size - hop, hop)])
    t = np.arange(e.size) * hop / sr
    peak = e.max()

    def onsets(lo, hi):
        on, last = [], -1.0
        for ti, v in zip(t, e):
            if lo * peak <= v < hi * peak or (hi >= 1 and v >= lo * peak):
                if ti - last > 0.25:
                    on.append(ti)
                last = ti
        return on

    beeps = onsets(0.55, 1.01)
    period = 60.0 / A["hr"]
    gaps = np.diff(beeps + [beeps[0] + dur])
    print(f"audio: {dur:.3f} s, {len(beeps)} beeps, first at {beeps[0]:.3f} s, gaps {gaps[:-1].min()*1000:.1f}-{gaps[:-1].max()*1000:.1f} ms "
          f"(grid {period*1000:.1f} ms), gap across the seam {gaps[-1]*1000:.1f} ms")
    # ticks: energy right after each whole second
    tick_ok = sum(1 for s in range(int(round(dur))) if e[(t >= s) & (t < s + 0.04)].max() > 0.1 * peak)
    print(f"  ticks present at {tick_ok}/{int(round(dur))} whole seconds")
    inner_ok = np.all(np.abs(gaps[:-1] - period) < 0.006)
    seam_ok = abs(gaps[-1] - period) < 0.022   # AAC pads the end by < one 1024-sample frame
    return len(beeps) == 38 and inner_ok and seam_ok and tick_ok == int(round(dur))


if __name__ == "__main__":
    ok_t = trace_check()
    ok_a = audio_check()
    print("ALL CHECKS PASS" if ok_t and ok_a else "CHECKS FAILED")
