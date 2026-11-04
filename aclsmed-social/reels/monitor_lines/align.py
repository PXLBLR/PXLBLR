"""Line up the monitor-line takes on one film timeline and cut the reel's clips.

Takes come from `-uiDemo reel-monitor-lines` (ACLSMED iOS,
App/UIDemo+MonitorLines.swift, captured by iOS/scripts/record_monitor_lines.sh):
one take per step (ECG lead II only, each other lead, + PA, + CVP, + EtCO2,
+ SpO2). Every take runs the same film clock as the shell-loop reel: the
engine is driven by F = seconds since launch, so the sweep cursor in any
frame says where that frame sits on the shared timeline:

    sweep_design_px = (F * 120) mod trace_width

For each take this finds the cursor (the erase gap) in sampled frames and
solves F = video_time + k. Reel time r shows film time F0 + r, and each shot
in timeline.json is cut from its take at that same F, so the sweep and the
beat carry straight across every cut and only the new line (or lead) changes.

    python3 align.py <takes_dir>          -> public/segments/<id>.mp4 + src/alignment.json
    python3 align.py <takes_dir> --recut  -> re-cut the same starts
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

FF = str(Path.home() / ".local/bin/ffmpeg")
HERE = Path(__file__).resolve().parent
TL = json.loads((HERE / "timeline.json").read_text())
W, H = 1376, 1032                  # takes are half the 2752x2064 framebuffer
S = W / 1430.0                     # MonitorLayout aspect-fit: screen px per design px
F0 = TL["F0"]
FPS = TL["fps"]
SPEED = 120.0                      # design px per second (WaveformEngine.SPEED * 60)
GAP = 16                           # WaveformEngine.GAP
HR = TL["hr"]
# Console shell (stripX, outerW, bandTop, bandBottom); tileW = 172.
STRIP_X, OUTER_W, TOP, BOTTOM = 20, 1220, 62, 782


def frames(path, fps=None, start=None, count=None, scale=1):
    w, h = W // scale, H // scale
    vf = []
    if fps:
        vf.append(f"fps={fps}")
    if scale != 1:
        vf.append(f"scale={w}:{h}")
    args = [FF, "-loglevel", "error"]
    if start is not None:
        args += ["-ss", f"{start:.4f}"]
    args += ["-i", str(path)]
    if vf:
        args += ["-vf", ",".join(vf)]
    if count:
        args += ["-frames:v", str(count)]
    args += ["-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    n = w * h * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3)
    p.stdout.close()
    p.wait()


def geometry():
    width = int(OUTER_W - 172)                      # trail length in design px
    x0, x1 = int(STRIP_X * S), int((STRIP_X + width) * S)
    y0, y1 = int(TOP * S) + 4, int(BOTTOM * S) - 4
    return width, x0, x1, y0, y1


def cursor(img):
    """Sweep position (design px) from the erase gap, or None."""
    width, x0, x1, y0, y1 = geometry()
    band = img[y0:y1, x0:x1].astype(np.int16)
    lit = band.max(axis=2) > 95
    empty = lit.sum(axis=0) == 0
    best = None
    i = 0
    while i < empty.size:
        if empty[i]:
            j = i
            while j < empty.size and empty[j]:
                j += 1
            if 9 <= j - i <= 24 and 0 < i and j < empty.size:
                if best is None or (j - i) > (best[1] - best[0]):
                    best = (i, j)
            i = j
        else:
            i += 1
    if best is None:
        return None
    center = x0 + (best[0] + best[1] - 1) / 2.0
    return center / S - STRIP_X - (GAP + 1) / 2.0


def fr(sec):
    """Reel frame of a time, rounded like JS Math.round (Remotion), not banker's round()."""
    return int(np.floor(sec * FPS + 0.5))


def wrap(d, width):
    return (d + width / 2) % width - width / 2


def solve(take, meta):
    """F = v + k for this take."""
    width, *_ = geometry()
    period = width / SPEED
    vs, qs = [], []
    for i, img in enumerate(frames(take, fps=10)):
        sw = cursor(img)
        if sw is None:
            continue
        v = i / 10.0
        vs.append(v)
        qs.append((sw / SPEED - v) % period)
    qs = np.array(qs)
    ang = qs / period * 2 * np.pi
    k0 = (np.angle(np.mean(np.exp(1j * ang))) % (2 * np.pi)) / (2 * np.pi) * period
    resid = (qs - k0 + period / 2) % period - period / 2
    k0 = (k0 + np.median(resid)) % period
    resid = (qs - k0 + period / 2) % period - period / 2
    # Coarse F at v=0 from the script's timestamps: the film epoch is set when
    # the scenario view is built (a few s after the launch command) and
    # recordVideo starts a moment after its command; on the shell takes that
    # netted out to k = launch->record gap - 1.8 s (+-1.3 s). It only has to
    # land within half a sweep period (4.4 s) to pick the right wrap.
    coarse = meta["t_record_cmd"] - meta["t_launch"] - 1.8
    n = round((coarse - k0) / period)
    k = k0 + n * period
    good = np.abs(resid) < 0.03
    dur = float(subprocess.run([FF, "-i", str(take)], capture_output=True, text=True).stderr
                .split("Duration: ")[1].split(",")[0].split(":")[-1])
    return k, float(np.median(np.abs(resid))), float(good.mean()), coarse, dur


def refine(take, k, r0, r1):
    """Best start (s, video time) for reel window [r0, r1) from this take."""
    width, x0, x1, y0, y1 = geometry()
    F = F0 + r0
    n_out = fr(r1) - fr(r0)
    v0 = F - k
    lead = 0.25
    t0 = max(0.0, v0 - lead)
    imgs = list(frames(take, start=t0, count=int((n_out / FPS + 2 * lead) * 60) + 4))
    curs, thumbs = [], []
    for img in imgs:
        curs.append(cursor(img))
        thumbs.append(img[y0:y1:4, x0:x1:4].max(axis=2).astype(np.int16))
    res = [wrap(c - (t0 + j / 60 + k) * SPEED, width) for j, c in enumerate(curs) if c is not None]
    lag = -np.percentile(res, 70) / SPEED if len(res) >= 10 else 0.0
    best = None
    for shift in range(-2, 3):
        start = v0 + lag + shift / 60
        idx = [int(round((start - t0) * 60 + n * 2)) for n in range(n_out)]
        if idx[0] < 0 or idx[-1] >= len(imgs):
            continue
        dups, run, maxrun = 0, 0, 0
        for a, bb in zip(idx, idx[1:]):
            if np.abs(thumbs[bb] - thumbs[a]).max() < 24:
                dups += 1
                run += 1
                maxrun = max(maxrun, run)
            else:
                run = 0
        rs = [wrap(curs[i] - (F + n / FPS) * SPEED, width) for n, i in enumerate(idx) if curs[i] is not None]
        err = float(np.median(np.abs(rs))) if rs else 99.0
        score = (maxrun, dups, err)
        if best is None or score < best[0]:
            best = (score, start)
    if best is None:
        raise SystemExit(f"{take.name}: window r {r0:.2f}-{r1:.2f} (F {F0 + r0:.2f}) is outside the take")
    (maxrun, dups, err), start = best
    return {"start": round(start, 4), "frames": n_out, "repeats": dups, "longestRepeat": maxrun,
            "cursorErrPx": round(err, 1)}


def windows():
    """Monitor shots as (id, take, r0, r1): consecutive shots of one take merge."""
    shots = TL["shots"]
    out = []
    for i, s in enumerate(shots):
        if not s["take"]:
            continue
        r1 = shots[i + 1]["from"] if i + 1 < len(shots) else TL["duration"]
        if out and out[-1][1] == s["take"] and abs(out[-1][3] - s["from"]) < 1e-6:
            out[-1] = (out[-1][0], s["take"], out[-1][2], r1)
        else:
            out.append((s["id"], s["take"], s["from"], r1))
    return out


def main():
    takes = Path(sys.argv[1])
    seg_dir = HERE / "public" / "segments"
    seg_dir.mkdir(parents=True, exist_ok=True)
    fits = {}
    for meta_path in sorted(takes.glob("*.json")):
        meta = json.loads(meta_path.read_text())
        take = takes / f"{meta['name']}.mp4"
        k, med, good, coarse, dur = solve(take, meta)
        fits[meta["name"]] = {"k": round(k, 4), "F": [round(k, 2), round(k + dur, 2)],
                              "medianResidMs": round(med * 1000, 1), "onTimeFrames": round(good, 3)}
        print(f"{meta['name']:9s} k={k:7.3f} (coarse {coarse:6.2f})  covers F {k:6.2f}..{k + dur:6.2f}  "
              f"resid {med * 1000:4.1f} ms, {good * 100:3.0f}% on time")
    segments = []
    print("\nshot      take      reel s          F            repeats  longest  cursor err px")
    for sid, take, r0, r1 in windows():
        r = refine(takes / f"{take}.mp4", fits[take]["k"], r0, r1)
        segments.append({"id": sid, "take": take, "from": r0, "to": r1, **r})
        flag = "" if r["longestRepeat"] <= 1 else "  <- hitch"
        print(f"  {sid:8s} {take:8s} {r0:6.2f}-{r1:6.2f}  {F0 + r0:6.2f}-{F0 + r1:6.2f}  "
              f"{r['repeats']:3d}/{r['frames'] - 1:<4d} {r['longestRepeat']:3d}      {r['cursorErrPx']}{flag}")
    finish(takes, seg_dir, segments, fits)


def finish(takes, seg_dir, segments, fits):
    for g in segments:
        subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{g['start']:.4f}",
                        "-i", str(takes / f"{g['take']}.mp4"), "-frames:v", str(g["frames"]),
                        "-vf", "fps=30", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                        "-pix_fmt", "yuv420p", "-an", str(seg_dir / f"{g['id']}.mp4")], check=True)
    result = {"F0": F0, "segments": segments, "takes": fits}
    (HERE / "src" / "alignment.json").write_text(json.dumps(result, indent=2))
    print(f"\nwrote src/alignment.json and {len(segments)} clips in public/segments/")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "--recut":
        prev = json.loads((HERE / "src" / "alignment.json").read_text())
        finish(Path(sys.argv[1]), HERE / "public" / "segments", prev["segments"], prev["takes"])
    else:
        main()
