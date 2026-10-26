"""Line up the shell takes on one film timeline and cut the reel's 30 one-second clips.

Takes come from `-uiDemo reel-shell-loop` (ACLSMED iOS, App/UIDemo+ShellReel.swift,
captured by iOS/scripts/record_shell_loop.sh). In that scenario the clock reads
10:30:00 + F, where F is seconds since launch, and the waveform engine is driven
by F itself: every trace starts at, and stays on, the beat phase and sweep
position it would have had since F = 0 (exactly 120 design px/s, HR 76). So the
sweep cursor in any frame says where that frame sits on the shared timeline:

    sweep_design_px = (F * 120) mod trace_width

For each take this script finds the cursor (the erase gap) in sampled frames and
solves F = video_time + k. The reel shows F0 .. F0+30 s; second s uses the shell
ORDER[s % 10]. The simulator stalls now and then, so each second is cut from
whichever take of that shell has the fewest frozen frames in that exact window.
Two takes of one shell at the same F are identical apart from those stalls.

    python3 align.py <takes_dir>            -> public/segments/s00..s29.mp4 + src/alignment.json
    python3 align.py <takes_dir> --recut    -> re-cut the same choices (e.g. after a crop change)
"""
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

FF = str(Path.home() / ".local/bin/ffmpeg")
HERE = Path(__file__).resolve().parent
W, H = 1376, 1032                  # takes are half the 2752x2064 framebuffer
S = W / 1430.0                     # MonitorLayout aspect-fit: screen px per design px
F0 = 13.0                          # reel t=0 on the film clock (every trace is full by ~11 s)
DUR = 30
SPEED = 120.0                      # design px per second (WaveformEngine.SPEED * 60)
GAP = 16                           # WaveformEngine.GAP
HR = 76
# Clips keep the WHOLE display (1376x1032): the reel frames them in an iPad
# bezel whose aperture is the real screen, so nothing is cropped. (Without a
# bezel, crop to 1004: below row 2007 of the 2752x2064 framebuffer every
# hardware shell leaves a 56 px band of app background.)
CROP_H = 1032

# Ten slots, three passes = 30 cuts. The reel ends on slot 10, the shell before
# slot 1, so the loop seam is just the next cut. Monitor (Classic) is the one
# shell that appears twice per pass (9 shells into 10 slots).
ORDER = ["console", "hospital", "consoleWhite", "transportRed", "whiteBlue",
         "classic", "hospitalWhiteBlue", "transportBeige", "brushedMetal", "classic"]

# (stripX, outerW, bandTop, bandBottom) from each shell's source; tileW = 172.
GEOM = {
    "console":           (20, 1220, 62, 782),
    "consoleWhite":      (20, 1220, 62, 782),
    "brushedMetal":      (24, 1382, 64, 716),
    "whiteBlue":         (24, 1382, 64, 716),
    "hospital":          (24, 1172, 64, 768),
    "hospitalWhiteBlue": (24, 1172, 64, 768),
    "transportRed":      (24, 1100, 64, 768),
    "transportBeige":    (24, 1100, 64, 768),
    "classic":           (14, 1196, 72, 776),
}


def frames(path, fps=None, start=None, count=None, scale=1, h_override=None):
    w, h = W // scale, (h_override or H) // scale
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


def geometry(shell):
    strip_x, outer_w, top, bottom = GEOM[shell]
    width = int(outer_w - 172)                      # trail length in design px
    x0, x1 = int(strip_x * S), int((strip_x + width) * S)
    y0, y1 = int(top * S) + 4, int(bottom * S) - 4
    return strip_x, width, x0, x1, y0, y1


def cursor(img, shell):
    """Sweep position (design px) from the erase gap, or None."""
    strip_x, width, x0, x1, y0, y1 = geometry(shell)
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
    # The stroke stops at sweepIdx and resumes at sweepIdx + GAP + 1.
    return center / S - strip_x - (GAP + 1) / 2.0


def last_r_behind(img, shell, sweep):
    """Design px from the newest R wave back to the cursor (beat-phase check)."""
    strip_x, width, x0, x1, y0, y1 = geometry(shell)
    _, _, top, bottom = GEOM[shell]
    row_h = (bottom - top - 4 * 14) / 5
    ly0, ly1 = int(top * S), int((top + row_h) * S)
    lane = img[ly0:ly1, x0:x1].astype(np.int16)
    r, g, b = lane[..., 0], lane[..., 1], lane[..., 2]
    green = (g > 160) & (r < 150) & (g - b > 35)
    has = green.any(axis=0)
    topy = np.where(has, green.argmax(axis=0), 10**6).astype(float)
    xs_design = (x0 + np.arange(topy.size)) / S - strip_x
    clear = has & (xs_design > 230)              # clear of the "LEAD II" caption
    if not clear.any():
        return None
    base = np.median(topy[clear])
    peak = topy[clear].min()
    # R waves rise well above everything else in lead II; respiration changes
    # their height by about 7.5 %, so take the top half of the excursion.
    cols = np.where(clear & (topy < base - 0.5 * (base - peak)))[0]
    if cols.size == 0:
        return None
    groups, cur = [], [cols[0]]
    for c in cols[1:]:
        if c - cur[-1] <= 3:
            cur.append(c)
        else:
            groups.append(cur)
            cur = [c]
    groups.append(cur)
    xs = [(x0 + topy_argmin(topy, gp)) / S - strip_x for gp in groups]
    behind = [(sweep - x) % width for x in xs]
    behind = [d for d in behind if d > GAP + 2]
    return min(behind) if behind else None


def topy_argmin(topy, cols):
    """Column of the R apex within a group of R columns."""
    cols = np.asarray(cols)
    return float(cols[np.argmin(topy[cols])])


def solve(take, meta, shell):
    """F = v + k for this take."""
    _, width, *_ = geometry(shell)
    period = width / SPEED
    vs, qs = [], []
    for i, img in enumerate(frames(take, fps=10)):
        sw = cursor(img, shell)
        if sw is None:
            continue
        v = i / 10.0
        vs.append(v)
        qs.append((sw / SPEED - v) % period)
    qs = np.array(qs)
    ang = qs / period * 2 * np.pi
    k0 = (np.angle(np.mean(np.exp(1j * ang))) % (2 * np.pi)) / (2 * np.pi) * period
    resid = (qs - k0 + period / 2) % period - period / 2
    k0 = (k0 + np.median(resid)) % period     # stalled frames lag; the median ignores them
    resid = (qs - k0 + period / 2) % period - period / 2
    # Coarse F at v=0 from the script's timestamps (measured on the first
    # takes: k = launch->record gap - 1.8 s, +-1.3 s). It only has to land
    # within half a sweep period (>= 3.8 s) to pick the right wrap.
    coarse = meta["t_record_cmd"] - meta["t_launch"] - 1.8
    n = round((coarse - k0) / period)
    k = k0 + n * period
    good = np.abs(resid) < 0.03
    return k, period, float(np.median(np.abs(resid))), float(good.mean()), coarse


def wrap(d, width):
    return (d + width / 2) % width - width / 2


def refine(take, shell, k, second):
    """Best start time (s) for reel second `second` from this take, and its quality.

    The global fit k is good to ~10 ms on average, but the simulator's render
    latency wanders (stalls show older frames), so measure the cursor in this
    exact window, correct for the local latency, then try +-2 source frames and
    keep the start whose 30 fps samples repeat the fewest frames.
    """
    _, width, x0, x1, y0, y1 = geometry(shell)
    F = F0 + second
    v0 = F - k
    lead = 0.25
    imgs = list(frames(take, start=max(0.0, v0 - lead), count=int((1 + 2 * lead) * 60)))
    t0 = max(0.0, v0 - lead)
    curs, thumbs = [], []
    for img in imgs:
        curs.append(cursor(img, shell))
        thumbs.append(img[y0:y1:4, x0:x1:4].max(axis=2).astype(np.int16))
    # residual (px) of what is on screen vs where the film clock says the cursor is
    res = [wrap(c - (t0 + j / 60 + k) * SPEED, width) for j, c in enumerate(curs) if c is not None]
    lag = -np.percentile(res, 70) / SPEED if len(res) >= 10 else 0.0   # fresh frames, not stalled ones
    best = None
    for shift in range(-2, 3):
        start = v0 + lag + shift / 60
        idx = [int(round((start - t0) * 60 + n * 2)) for n in range(FPS)]
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
    (maxrun, dups, err), start = best
    return {"start": round(start, 4), "repeats": dups, "longestRepeat": maxrun, "cursorErrPx": round(err, 1)}


FPS = 30


def main():
    takes = Path(sys.argv[1])
    seg_dir = HERE / "public" / "segments"
    seg_dir.mkdir(parents=True, exist_ok=True)

    fits = {}
    by_shell = defaultdict(list)
    for meta_path in sorted(takes.glob("*_t*.json")):
        meta = json.loads(meta_path.read_text())
        shell, name = meta["shell"], meta_path.stem
        take = takes / f"{name}.mp4"
        k, period, med_ms, good, coarse = solve(take, meta, shell)
        fits[name] = {"shell": shell, "k": round(k, 4), "medianResidMs": round(med_ms * 1000, 1),
                      "onTimeFrames": round(good, 3)}
        by_shell[shell].append(name)
        print(f"{name:22s} k={k:7.3f} (coarse {coarse:5.2f}, period {period:5.2f}s)  "
              f"cursor median resid {med_ms*1000:4.1f} ms, {good*100:3.0f}% on time")

    # Pick the smoothest take for each reel second.
    segments = []
    print("\nsecond  shell               take                   repeated frames (of 29)  longest run  cursor err px")
    for s in range(DUR):
        shell = ORDER[s % len(ORDER)]
        opts = []
        for n in by_shell[shell]:
            r = refine(takes / f"{n}.mp4", shell, fits[n]["k"], s)
            opts.append(((r["longestRepeat"], r["repeats"], r["cursorErrPx"]), n, r))
        opts.sort(key=lambda o: o[0])
        _, best, r = opts[0]
        segments.append({"second": s, "shell": shell, "take": best, **r})
        flag = "" if r["longestRepeat"] <= 1 else "  <- hitch"
        print(f"  {s:2d}    {shell:18s}  {best:22s}  {r['repeats']:2d}                       "
              f"{r['longestRepeat']}            {r['cursorErrPx']}{flag}")

    finish(takes, seg_dir, segments, fits)


def finish(takes, seg_dir, segments, fits):
    """Cut the 30 clips from the chosen takes, check the beat, write alignment.json."""
    # Cut the 30 one-second clips (frames at start + n/30 of the chosen take).
    for g in segments:
        subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{g['start']:.4f}",
                        "-i", str(takes / f"{g['take']}.mp4"), "-frames:v", "30",
                        "-vf", f"fps=30,crop={W}:{CROP_H}:0:0", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                        "-pix_fmt", "yuv420p", "-an", str(seg_dir / f"s{g['second']:02d}.mp4")], check=True)

    # Beat check on the clips themselves: in every frame, the newest R wave sits
    # d px behind the cursor, so it was drawn at film time F - d/120. Every
    # second must agree on where R falls in the beat, or the cuts would jump
    # and the beeps would miss the R waves.
    period = 60.0 / HR
    per_seg, allr = [], []
    for g in segments:
        rts = []
        for n, img in enumerate(frames(seg_dir / f"s{g['second']:02d}.mp4", h_override=CROP_H)):
            sw = cursor(img, g["shell"])
            d = None if sw is None else last_r_behind(img, g["shell"], sw)
            if d is not None and d < 2 * SPEED * period:
                rts.append((F0 + g["second"] + n / FPS - d / SPEED) % period)
        per_seg.append(rts)
        allr += rts
    ang = np.array(allr) / period * 2 * np.pi
    r_phase = (np.angle(np.mean(np.exp(1j * ang))) % (2 * np.pi)) / (2 * np.pi) * period
    print("\nbeat check on the cut clips (R wave vs the shared beat grid, ms):")
    worst = 0.0
    for g, rts in zip(segments, per_seg):
        if not rts:
            print(f"  {g['second']:2d} {g['shell']:18s}  no R measured (cursor under the caption)")
            continue
        dev = np.median([wrap(r - r_phase, period) for r in rts]) * 1000
        worst = max(worst, abs(dev))
        g["beatOffsetMs"] = round(float(dev), 1)
        print(f"  {g['second']:2d} {g['shell']:18s}  {dev:+6.1f} ms  ({len(rts)} frames)")
    print(f"R wave at {r_phase:.3f} s into each {period:.4f} s beat; worst second {worst:.1f} ms off")

    result = {"F0": F0, "duration": DUR, "hr": HR, "order": ORDER, "rPhase": round(float(r_phase), 4),
              "segments": segments,
              "takes": fits}
    (HERE / "src" / "alignment.json").write_text(json.dumps(result, indent=2))
    print("\nwrote src/alignment.json and public/segments/s00..s29.mp4")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "--recut":
        # Re-cut from the takes and starts already chosen (src/alignment.json).
        prev = json.loads((HERE / "src" / "alignment.json").read_text())
        finish(Path(sys.argv[1]), HERE / "public" / "segments", prev["segments"], prev["takes"])
    else:
        main()
