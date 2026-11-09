"""R waves as the monitor draws them, on the reel clock (public/monitor.mp4 starts at reel 0).

    python3 rwaves.py -> src/rwaves.json  {"r": [t, ...]}
Lead II: the single-lead strip until ALL 12 LEADS opens, then lead II's row of the 12-lead view. A beat is drawn
when newly drawn trace pixels reach high above the row's baseline. While the screen is frozen (PAUSE) or covered
(the printout) nothing is drawn, so beats there are carried on at the measured R-R interval.
"""
import json, subprocess
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
FF = str(Path.home() / ".local/bin/ffmpeg")
T = json.loads((HERE / "src/timeline.json").read_text())
W, H, FPS = 1032, 774, 60
raw = subprocess.run([FF, "-loglevel", "error", "-i", str(HERE / "public/monitor.mp4"), "-vf", f"fps={FPS},scale={W}:{H}",
                      "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
green = (fr[..., 1] > 150) & (fr[..., 0] < 170)          # the ECG trace colour
def tops(x0, x1, y0, y1):
    g = green[:, int(y0*H):int(y1*H), int(x0*W):int(x1*W)]
    new = g[1:] & ~g[:-1]
    out = np.full(len(fr), 1e9)
    for i, m in enumerate(new):
        ys = np.nonzero(m.any(1))[0]
        if len(ys): out[i + 1] = ys.min() / (y1 - y0) / H   # 0 = top of the row
    return out
single = tops(0.015, 0.71, 0.075, 0.215)
row2 = tops(0.0175, 0.36, 0.197, 0.301)
t = np.arange(len(fr)) / FPS
open_at = T["events"]["all_leads"] + 0.25
top = np.where(t < open_at, single, row2)
r, last = [], -1
for i, v in enumerate(top):
    if v < 0.30 and t[i] - last > 0.3:                # R peak drawn near the top of the row
        r.append(round(float(t[i]), 3)); last = t[i]
r = np.array(r)
# The rate is constant within each rhythm, so the beats are a regular grid fitted to the clean stretches (lead switching
# redraws the whole strip and the pause/printout draw nothing); residuals are printed.
def grid(lo, hi, start, stop, hr):
    b = r[(r > lo) & (r < hi)]
    k = np.round((b - b[0]) / (60 / hr))             # beat number from the preset rate (48 / 108)
    P, a = np.polyfit(k, b, 1)
    res = b - (a + P * k)
    print(f"grid {lo}-{hi}: period {P:.4f} s ({60 / P:.1f}/min), {len(b)} beats, residual max {np.abs(res).max() * 1000:.0f} ms")
    n0 = int(np.ceil((start - a) / P)); n1 = int(np.floor((stop - a) / P))
    return [round(float(a + P * n), 3) for n in range(n0, n1 + 1)]
E = T["events"]
full = (grid(E["all_leads"] + 0.3, E["rhythm"] - 0.2, 0.0, E["rhythm"], 48)
        + grid(E["rhythm"] + 0.7, E["pause"] - 0.1, E["rhythm"] + 0.15, T["duration"], 108))
print(len(full), "beats; first", full[:3], "around the change", [x for x in full if 23 < x < 27])
(HERE / "src/rwaves.json").write_text(json.dumps({"r": full}) + "\n")
