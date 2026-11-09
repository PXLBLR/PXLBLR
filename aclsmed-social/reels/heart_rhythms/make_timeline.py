"""Build src/data/<id>.timeline.json (captions, cue times, beat events) from the narration, so the visuals follow the voice.

    python3 make_timeline.py R02_pvt

Voice sources, in order of preference (public/<id>/vo/):
  1. full.wav + lines.json  -- one continuous take; lines.json = {"l1": [start, end], ...} in seconds (check_vo.py).
  2. none                   -- mockup timing at ~150 wpm (no voice).
Cues: the rhythm starts ('onset') 0.25 s before the first 'onset' line ("Now watch what happens in ..."); the key tag
sits on the last sentence of the 'key' line (or its key_sentence) (sentences.json); 'action' and 'end' on their lines.
Events: every beat on the reel clock. pre-onset beats from the 'pre' strip, post-onset from the 'post' strip shifted to
the onset (POST_SKIP s into it, so the new rhythm starts settled). Each beat: p (P wave / SA fire, or null), q (QRS onset,
or null if the P was blocked), kind. Reels with a builtin strip (R01) use sinus at 75/min: p = k*0.8, q = p + 0.2.
"""
import json
import wave
from pathlib import Path

import reel

R = reel.load()
VO = R["vo"]
LEAD_IN = 0.4
POST_SKIP = 0.5
script = R["script"]

lines, mode = [], "mockup"
if (VO / "full.wav").exists() and (VO / "lines.json").exists():
    mode, spans = "full", json.loads((VO / "lines.json").read_text())
    for ln in script["lines"]:
        s, e = spans[ln["id"]]
        lines.append({**ln, "at": round(LEAD_IN + s, 3), "end": round(LEAD_IN + e, 3)})
else:
    t = LEAD_IN
    for ln in script["lines"]:
        d = len(ln["text"].split()) / 2.5 + 0.3
        lines.append({**ln, "at": round(t, 3), "end": round(t + d, 3)})
        t += d + ln["gap_after"]

first = {c: next(l["at"] for l in lines if l["cue"] == c) for c in ("onset", "key", "action", "end")}
key_line = next(l["id"] for l in lines if l["cue"] == "key")
if mode == "full" and (VO / "sentences.json").exists():
    ks = next(l for l in script["lines"] if l["id"] == key_line).get("key_sentence", -1)
    first["key"] = round(LEAD_IN + json.loads((VO / "sentences.json").read_text())[key_line][ks][0], 3)
total = lines[-1]["end"] + lines[-1]["gap_after"] + 1.0
duration = round(max(total, 24.0), 2)
onset = round(first["onset"] - 0.25, 3)


def pair(qrs, ptimes, lo, hi, shift=0.0):
    """Beats in [lo, hi) on the reel clock: each QRS with the P wave 0.08-0.4 s before it; P waves with no QRS after
    them within 0.4 s are 'blocked'."""
    out, used = [], set()
    for b in qrs:
        q = b["t"] + shift
        if not lo <= q < hi:
            continue
        p = next((x + shift for x in reversed(ptimes) if 0.08 <= b["t"] - x <= 0.4), None)
        if p is not None:
            used.add(round(p - shift, 3))
        out.append({"p": None if p is None else round(p, 3), "q": round(q, 3), "kind": b["type"]})
    for x in ptimes:
        if round(x, 3) in used or not lo <= x + shift < hi:
            continue
        if not any(0 <= b["t"] - x <= 0.4 for b in qrs):
            out.append({"p": round(x + shift, 3), "q": None, "kind": "blocked"})
        elif not any(0.08 <= b["t"] - x <= 0.4 for b in qrs):
            out.append({"p": round(x + shift, 3), "q": None, "kind": "p_only"})
    return sorted(out, key=lambda e: e["q"] if e["p"] is None else e["p"])


cfg = R["cfg"]
if cfg["pre"].get("builtin"):
    beats = [{"p": round(k * 0.8, 3), "q": round(k * 0.8 + 0.2, 3), "kind": "normal"}
             for k in range(-6, 200) if k * 0.8 + 0.2 < onset]
    hr = cfg["hr"]
else:
    S = json.loads(R["strips"].read_text())
    pre, post = S["pre"], S["post"]
    shift = onset - POST_SKIP
    beats = pair(pre["qrs"], pre["p"], -5, onset) + pair(post["qrs"], post["p"], onset, duration + 1, shift)
    # In CHB the P waves never conduct: keep them as atrial-only events even when one lands just before a QRS.
    if cfg["heart"] == "chb":
        post_q = [{"p": None, "q": round(b["t"] + shift, 3), "kind": b["type"]} for b in post["qrs"] if onset <= b["t"] + shift < duration + 1]
        post_p = [{"p": round(x + shift, 3), "q": None, "kind": "blocked"} for x in post["p"] if onset <= x + shift < duration + 1]
        beats = [b for b in beats if (b["q"] or b["p"]) < onset] + sorted(post_q + post_p, key=lambda e: e["q"] or e["p"])
    rr = [b["t"] for b in post["qrs"]]
    rr = [b - a for a, b in zip(rr, rr[1:])]
    hr = cfg["hr"] if cfg["hr"] != "auto" else (str(round(60 / (sum(rr) / len(rr)))) if rr else "0")
    pre_hr = [b["t"] for b in pre["qrs"]]
    pre_rr = [b - a for a, b in zip(pre_hr, pre_hr[1:])]

timeline = {
    "id": R["id"], "n": script["n"], "mode": mode, "duration": duration, "onset": onset,
    "key": first["key"], "action": first["action"], "end_card": round(first["end"] - 0.3, 3),
    "post_shift": None if cfg["pre"].get("builtin") else round(onset - POST_SKIP, 3),
    "hr_pre": "75" if cfg["pre"].get("builtin") else str(round(60 / (sum(pre_rr) / len(pre_rr)))),
    "hr_post": hr,
    "lines": [{k: l[k] for k in ("id", "text", "at", "end")} for l in lines],
    "beats": beats,
}
R["timeline"].parent.mkdir(parents=True, exist_ok=True)
R["timeline"].write_text(json.dumps(timeline, indent=1) + "\n")

# Index of every reel with a timeline, for the Remotion bundle.
data = R["timeline"].parent
ids = [i for i in reel.IDS if (data / f"{i}.timeline.json").exists()]
imp = "\n".join(f"import t{k} from './{i}.timeline.json';" +
                (f"\nimport s{k} from './{i}.strips.json';" if (data / f"{i}.strips.json").exists() else "")
                for k, i in enumerate(ids))
rows = ",\n".join(f"  {i}: {{ timeline: t{k}, strips: {'s%d' % k if (data / f'{i}.strips.json').exists() else 'null'} }}"
                  for k, i in enumerate(ids))
(data / "index.ts").write_text("// Generated by make_timeline.py: every reel with a timeline.\n" + imp +
                               "\n\nexport const DATA: Record<string, { timeline: any; strips: any }> = {\n" + rows + ",\n};\n")
print(R["id"], mode, "duration", duration, "onset", onset, "key", first["key"], "beats", len(beats), "hr", timeline["hr_pre"], "->", hr)
