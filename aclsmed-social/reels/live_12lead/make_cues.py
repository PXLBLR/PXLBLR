"""Film cues for the ACLSMED DEBUG rig (reel-live-12lead) from the narration's sentence times.

    python3 make_cues.py  -> out/film_cues.json  (pushed into the app's Documents by capture.sh)
Times are on the voice clock (0 = start of full.wav); the rig adds `go` after the Monitor appears.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
S = json.loads((HERE / "public/vo/sentences.json").read_text())
W = json.loads((HERE / "public/vo/whisper.json").read_text())
GO = 4.0
word = lambda w, after: next(x[1] for x in W if x[0].lower().strip(".,") == w and x[1] > after)
ev = [
    (S["l2"][0][0] + 0.25, "picker_open"),          # "Tap the ECG ..."
    (S["l2"][1][0] - 0.08, "lead:II"),               # "Lead II."
    (S["l2"][2][0] - 0.08, "lead:V1"),               # "V1."
    (S["l2"][3][0] - 0.08, "lead:aVF"),              # "aVF."
    (S["l2"][3][1] - 0.15, "picker_close"),
    (S["l3"][0][0] + 0.05, "picker_open"),           # "Or choose ..."
    (word("all", S["l3"][0][0]) + 0.1, "all_leads"),  # "... all 12 leads"
    (S["l5"][0][1] + 0.05, "rhythm:stemi_ant"),      # after "Now the instructor changes the rhythm."
    (S["l8"][0][0] + 0.15, "pause"),                 # "Pause ..."
    (S["l8"][1][0] + 0.15, "print"),                 # "Print ..."
    (S["l9"][0][0] - 0.05, "print_close"),           # "Most code simulators ..."
    (S["l9"][0][0] + 0.35, "play"),
]
out = {"go": GO, "events": [{"t": round(t, 3), "action": a} for t, a in ev]}
(HERE / "out").mkdir(exist_ok=True)
(HERE / "out/film_cues.json").write_text(json.dumps(out, indent=1) + "\n")
for e in out["events"]:
    print(e)
