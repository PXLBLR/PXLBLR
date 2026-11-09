"""Build timeline.json (caption + cue times) from the narration, so the visuals follow the voice.

Voice sources, in order of preference (all in public/vo/):
  1. full.wav + lines.json  -- one continuous take (most natural); lines.json = {"l1": [start, end], ...} in seconds,
                               from Whisper word timestamps on the Mac.
  2. l1.wav ... l7.wav      -- one file per line; placed back to back with each line's gap_after.
  3. none                   -- mockup timing at ~150 wpm (no voice).
The V-fib onset lands 0.25 s before line 'l3' starts ("Now watch what happens in V-fib").
"""
import json
import wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
VO = HERE / "public" / "vo"
LEAD_IN = 0.4
script = json.loads((HERE / "script.json").read_text())


def dur(p):
    with wave.open(str(p)) as w:
        return w.getnframes() / w.getframerate()


lines, mode = [], "mockup"
if (VO / "full.wav").exists() and (VO / "lines.json").exists():
    mode, spans = "full", json.loads((VO / "lines.json").read_text())
    for ln in script["lines"]:
        s, e = spans[ln["id"]]
        lines.append({**ln, "at": round(LEAD_IN + s, 3), "end": round(LEAD_IN + e, 3)})
else:
    t = LEAD_IN
    per_line = all((VO / f"{ln['id']}.wav").exists() for ln in script["lines"])
    mode = "lines" if per_line else "mockup"
    for ln in script["lines"]:
        d = dur(VO / f"{ln['id']}.wav") if per_line else len(ln["text"].split()) / 2.5 + 0.3
        lines.append({**ln, "at": round(t, 3), "end": round(t + d, 3)})
        t += d + ln["gap_after"]

first = {c: next(l["at"] for l in lines if l["cue"] == c) for c in ("vf", "nopulse", "action", "end")}
total = lines[-1]["end"] + lines[-1]["gap_after"] + 1.0
timeline = {"mode": mode, "duration": round(max(total, 24.0), 2), "vf_start": round(first["vf"] - 0.25, 3),
            "nopulse": first["nopulse"], "action": first["action"], "end_card": round(first["end"] - 0.3, 3),
            "lines": [{k: l[k] for k in ("id", "text", "at", "end")} for l in lines]}
(HERE / "src" / "timeline.json").write_text(json.dumps(timeline, indent=2) + "\n")
print(mode, "duration", timeline["duration"], "vf", timeline["vf_start"])
