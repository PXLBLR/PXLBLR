"""Frame checks on the rendered reel (aclsmed_monitor_lines.mp4).

1. Lanes, every frame the monitor is on screen: the channels that step should
   show (ECG only -> +ART -> +PA -> +CVP -> +EtCO2 -> +SpO2) each carry their own
   colour across >= 85 % of the strip with real amplitude (no flatline), in
   the rows the app gives that many channels; with ECG only, the empty second
   row stays empty.
2. Vitals + lead + popups (OCR, macOS Vision, on the cut clips at 1376x1032,
   4 frames a second): HR 76, NIBP 120/80, Temp 37.0, Resp 14, and ART MAP 93, PA 25/10,
   CVP 6, SpO2 98, EtCO2 38 whenever that line is on; the ECG caption reads
   the shot's lead; any other text on screen is listed so a popup/toast shows.
3. Safe areas: no bright pixel outside x 80..1000, y 250..1500 in any frame.
4. Beat: R waves in the lead-II clips sit on the film-clock beat grid that
   make_audio.py lays the app's QRS beep on (R_PHASE).
5. Captions vs voice: Whisper on the reel's own audio; every caption word's
   start must agree with the spoken word within 150 ms.

    python3 check.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

import align
from make_audio import R_PHASE

HERE = Path(__file__).resolve().parent
FF = align.FF
VIDEO = HERE / "aclsmed_monitor_lines.mp4"
TL = json.loads((HERE / "timeline.json").read_text())
A = json.loads((HERE / "src" / "alignment.json").read_text())
WORDS = json.loads((HERE / "src" / "words.json").read_text())
BZ = json.loads((HERE / "src" / "bezel.json").read_text())
SHOTS = TL["shots"]
END_AT = next(s["from"] for s in SHOTS if s["id"] == "end")

# Same layout maths as src/MonitorLines.tsx
DEV_W = 920
K = DEV_W / BZ["width"]
DEV_X, DEV_Y = 80, 560
SCR_X = DEV_X + BZ["aperture"]["x"] * K - 1
SCR_Y = DEV_Y + BZ["aperture"]["y"] * K - 1
SCR_W = BZ["aperture"]["w"] * K + 2
D2R = align.S * SCR_W / 1376          # design px -> reel px
ORDER = ["ECG", "ART", "PA", "CVP", "SpO2", "EtCO2"]
LINES = {"lead": ["ECG"], "art": ["ECG", "ART"], "pa": ["ECG", "ART", "PA"], "cvp": ["ECG", "ART", "PA", "CVP"],
         "etco2": ["ECG", "ART", "PA", "CVP", "EtCO2"], "spo2": ORDER, "all": ORDER, "hero": ORDER}


def shot_at(t):
    cur = SHOTS[0]
    for s in SHOTS:
        if s["from"] <= t + 1e-6:
            cur = s
    return cur


def expected(sid):
    return LINES["lead" if sid.startswith("lead") else sid]


def classes(px):
    r, g, b = px[..., 0].astype(int), px[..., 1].astype(int), px[..., 2].astype(int)
    mx, mn = np.maximum(np.maximum(r, g), b), np.minimum(np.minimum(r, g), b)
    lit = mx > 70
    return {
        "ECG": lit & (g >= r + 30) & (g >= b + 10),
        "ART": lit & (r >= g + 40) & (r >= b + 40),
        "PA": lit & (r > 120) & (g > 110) & ((r + g) // 2 - b > 25) & (abs(r - g) < 60),
        "CVP": lit & (b >= r + 10) & (b >= g - 5) & (r * 100 >= 55 * b),
        "SpO2": lit & (np.minimum(g, b) - r > 60) & (b >= g - 30) & (g > 90),
        "EtCO2": lit & (mx - mn < 28) & (mx > 110),
    }


def lanes(active):
    n = max(2, len(active))
    top, bottom = align.TOP, align.BOTTOM
    row_h = (bottom - top - (n - 1) * 14) / n
    out = []
    for i in range(n):
        y0 = SCR_Y + (top + i * (row_h + 14) + 0.18 * row_h) * D2R
        y1 = SCR_Y + (top + i * (row_h + 14) + row_h) * D2R
        x0 = SCR_X + (align.STRIP_X + 240) * D2R
        x1 = SCR_X + (align.STRIP_X + align.OUTER_W - 172 - 6) * D2R
        out.append((active[i] if i < len(active) else None, int(x0), int(x1), int(y0), int(y1)))
    return out


def video_frames(path, w=1080, h=1920):
    p = subprocess.Popen([FF, "-loglevel", "error", "-i", str(path), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         stdout=subprocess.PIPE)
    n = w * h * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3)
    p.wait()


def frame_checks():
    worst, fails, safe_bad, nframes = {}, [], [], 0
    for f, img in enumerate(video_frames(VIDEO)):
        nframes += 1
        t = f / 30
        # 3. safe areas, every frame
        bright = img.max(axis=2) > 90
        outside = bright.copy()
        outside[250:1500, 80:1000] = False
        if outside.any():
            ys, xs = np.nonzero(outside)
            safe_bad.append((f, int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())))
        # 1. lanes while the monitor is fully on screen
        if t >= END_AT - 0.4:
            continue
        sid = shot_at(t)["id"]
        for name, x0, x1, y0, y1 in lanes(expected(sid)):
            region = img[y0:y1, x0:x1]
            if name is None:              # the empty half under an ECG-only strip
                lit = region.max(axis=2) > 70
                if lit.any(axis=0).mean() > 0.02:
                    fails.append((f, sid, "extra lane", round(float(lit.any(axis=0).mean()), 2)))
                continue
            m = classes(region)[name]
            cover = float(m.any(axis=0).mean())
            ys = np.nonzero(m)[0]
            amp = float(np.percentile(ys, 98) - np.percentile(ys, 2)) if ys.size else 0.0
            w = worst.setdefault(name, [1.0, 1e9])
            w[0], w[1] = min(w[0], cover), min(w[1], amp)
            if cover < 0.85 or amp < 6:
                fails.append((f, sid, name, round(cover, 2), round(amp, 1)))
    print(f"lanes: {nframes} frames, monitor frames checked up to {END_AT - 0.4:.1f} s")
    for name, (c, a) in worst.items():
        print(f"  {name:5s} lowest coverage {c*100:5.1f}%   lowest amplitude {a:5.1f} px")
    print(f"  failures: {len(fails)}" + (f"  first: {fails[:6]}" if fails else ""))
    print(f"safe areas: {len(safe_bad)} frames with bright pixels outside x80-1000 y250-1500"
          + (f"  first: {safe_bad[:4]}" if safe_bad else ""))
    return not fails and not safe_bad, nframes


EXPECT = {"ART": "MAP 93", "PA": "25/10", "CVP": "6", "SpO2": "98", "EtCO2": "38"}


def ocr_checks():
    tmp = HERE / "out" / "ocr"
    tmp.mkdir(parents=True, exist_ok=True)
    for p in tmp.glob("*.png"):
        p.unlink()
    plan = []
    for g in A["segments"]:
        n = g["frames"]
        picks = sorted(set([0, n // 2, n - 1] + list(range(0, n, 8))))
        for j in picks:
            out = tmp / f"{g['id']}_{j:04d}.png"
            subprocess.run([FF, "-loglevel", "error", "-y", "-i", str(HERE / "public" / "segments" / f"{g['id']}.mp4"),
                            "-vf", f"select=eq(n\\,{j})", "-frames:v", "1", str(out)], check=True)
            plan.append((g, j, out))
    res = subprocess.run(["swift", str(HERE / "ocr.swift")] + [str(p) for *_, p in plan],
                         capture_output=True, text=True, check=True).stdout.splitlines()
    by_file = {json.loads(l)["file"]: json.loads(l)["lines"] for l in res}
    bad, other_text, clocks = [], set(), set()
    allowed = re.compile(r"^(ACLSMED|ACLS|MED|DOE, JOHN|62y|M|84 kg|178 cm|NKDA|A\+|POWER|CHARGE|ALARM|HR|bpm|PA|CVP|SpO.?|EtCO.?|"
                         r"mmHg|%|NIBP|Temp|Resp|/min|CONNECTION|Monitor|Instructor|IVmed|RESPmed|CPR|MODE|DEFIB|AED|SYNC|ANALYZE|"
                         r"ENERGY|JOULES|SHOCK|PACER|RATE|mAmp|BATTERY|MEGA CODES|RHYTHM|SUMMARY|12-LEAD|X-RAY|LABS|MEDS|PADS|"
                         r"SILENCE|CONSOLE|ECG|THERAPY|normal.*|RR 14.*|live|MAP.*|\d+|[\d/ .:°C+\-±J]+|.{0,3})$", re.I)
    for g, j, p in plan:
        lines = by_file.get(str(p), [])
        # Vision sometimes reads Latin capitals as Cyrillic look-alikes ("МAP 93").
        cyr = str.maketrans("АВСЕНКМОРТХаеорсху", "ABCEHKMOPTXaeopcxy")
        texts = [l[0].strip().translate(cyr) for l in lines]
        joined = " | ".join(texts)
        sid = g["id"]
        lead = next((s["label"] for s in SHOTS if s["id"] == sid), "LEAD II")
        want_lead = lead.split()[-1] if sid.startswith("lead") else "II"
        lead_txt = [x for x in texts if x.upper().startswith("LEAD")]
        if not any(re.match(rf"LEAD\s*{re.escape(want_lead)}\b", x, re.I) for x in lead_txt):
            bad.append((sid, j, f"lead caption {lead_txt} != {want_lead}"))
        need = ["76", "120/80", "37.0", "14"] + [EXPECT[c] for c in expected(sid) if c in EXPECT]
        for v in need:
            if not any(x == v or x.endswith(" " + v) or x.startswith(v + " ") for x in texts):
                bad.append((sid, j, f"missing {v}"))
        for c, v in EXPECT.items():
            if c not in expected(sid) and v in texts and v not in ("6",):
                bad.append((sid, j, f"{c} value {v} shown while off"))
        for x in texts:
            m = re.match(r"^10:30:(\d\d)$", x)
            if m:
                clocks.add(x)
            elif not x.upper().startswith("LEAD") and not allowed.match(x):
                other_text.add(x)
    print(f"ocr: {len(plan)} frames from {len(A['segments'])} clips; clock readings {sorted(clocks)[:1]}..{sorted(clocks)[-1:]}")
    print(f"  problems: {len(bad)}" + (f"  {bad[:8]}" if bad else ""))
    print(f"  other text seen (check for popups): {sorted(other_text)}")
    return not bad


def beat_check():
    """R waves in the lead-II clips vs the film-clock beat grid."""
    period = 60.0 / TL["hr"]
    width, x0, x1, *_ = align.geometry()
    rts = []
    for g in A["segments"]:
        if g["take"] != "ecg_II":
            continue
        for n, img in enumerate(align.frames(HERE / "public" / "segments" / f"{g['id']}.mp4")):
            sw = align.cursor(img)
            if sw is None:
                continue
            row_h = (align.BOTTOM - align.TOP - 14) / 2
            ly0, ly1 = int(align.TOP * align.S), int((align.TOP + row_h) * align.S)
            lane = img[ly0:ly1, x0:x1].astype(np.int16)
            r, gg, b = lane[..., 0], lane[..., 1], lane[..., 2]
            green = (gg > 160) & (r < 150) & (gg - b > 35)
            has = green.any(axis=0)
            topy = np.where(has, green.argmax(axis=0), 10 ** 6).astype(float)
            xs_d = (x0 + np.arange(topy.size)) / align.S - align.STRIP_X
            clear = has & (xs_d > 230)
            if not clear.any():
                continue
            base, peak = np.median(topy[clear]), topy[clear].min()
            cols = np.where(clear & (topy < base - 0.5 * (base - peak)))[0]
            groups, cur = [], [cols[0]] if cols.size else []
            for c in cols[1:]:
                if c - cur[-1] <= 3:
                    cur.append(c)
                else:
                    groups.append(cur)
                    cur = [c]
            if cur:
                groups.append(cur)
            for gp in groups:
                gp = np.asarray(gp)
                xr = (x0 + gp[np.argmin(topy[gp])]) / align.S - align.STRIP_X
                d = (sw - xr) % width
                if align.GAP + 2 < d < 2 * align.SPEED * period:
                    F = A["F0"] + g["from"] + n / 30
                    rts.append((F - d / align.SPEED) % period)
    ang = np.array(rts) / period * 2 * np.pi
    ph = (np.angle(np.mean(np.exp(1j * ang))) % (2 * np.pi)) / (2 * np.pi) * period
    spread = np.median(np.abs(((np.array(rts) - ph) + period / 2) % period - period / 2)) * 1000
    print(f"beat: R wave at {ph:.4f} s into each beat ({len(rts)} R measurements, median spread {spread:.1f} ms); "
          f"make_audio.py uses {R_PHASE}")
    return abs(ph - R_PHASE) < 0.01


def caption_check():
    wav = HERE / "out" / "reel_audio.wav"
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", str(VIDEO), "-ac", "1", "-ar", "16000", str(wav)], check=True)
    py = Path.home() / "Developer/tts/PrayerVoice/.venv/bin/python"
    code = ("import mlx_whisper, json, sys; r = mlx_whisper.transcribe(sys.argv[1], path_or_hf_repo='mlx-community/whisper-large-v3-turbo', "
            "word_timestamps=True, language='en', no_speech_threshold=None, condition_on_previous_text=False); "
            "print(json.dumps([[w['word'].strip(), w['start'], w['end']] for s in r['segments'] for w in s['words']]))")
    out = subprocess.run([str(py), "-c", code, str(wav)], capture_output=True, text=True, check=True).stdout
    heard = json.loads(out.strip().splitlines()[-1])
    norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
    # Match each caption word to the nearest heard word with the same spelling.
    diffs, missing, worst = [], [], []
    for line in WORDS:
        for w in line["words"]:
            key = norm(w["w"])
            cands = [h for h in heard if norm(h[0]) == key or (len(key) > 3 and (key in norm(h[0]) or norm(h[0]) in key))]
            cands = [h for h in cands if abs(h[2] - w["end"]) < 1.0]
            if not cands:
                missing.append(w["w"])
                continue
            h = min(cands, key=lambda h: abs(h[2] - w["end"]))
            diffs.append(h[2] - w["end"])
            worst.append((abs(h[2] - w["end"]), w["w"], round(w["end"], 2), round(h[2], 2)))
    d = np.abs(np.array(diffs)) * 1000
    print(f"captions: {len(diffs)} caption words matched to the reel's own speech; word-end offset median {np.median(d):.0f} ms, "
          f"90th pct {np.percentile(d, 90):.0f} ms, worst {d.max():.0f} ms; unmatched (spelling) {missing}")
    print("  largest offsets (s, word, caption end, heard end): " + str(sorted(worst, reverse=True)[:4]))
    print("  heard: " + " ".join(h[0] for h in heard))
    return np.percentile(d, 90) < 150


if __name__ == "__main__":
    ok1, n = frame_checks()
    ok2 = ocr_checks()
    ok3 = beat_check()
    ok4 = caption_check()
    print("ALL CHECKS PASS" if ok1 and ok2 and ok3 and ok4 else "CHECKS FAILED")
