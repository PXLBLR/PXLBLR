"""Reel timeline: captions (script words with Whisper times), rig events and the top-panel / outline plan.

    python3 make_timeline.py -> src/timeline.json
Reel clock = voice clock + LEAD_IN. public/monitor.mp4 starts at reel 0 (cut from the raw take at
offset - LEAD_IN, where offset = video - voice measured by events.py).
"""
import difflib, json, re
from pathlib import Path

import check_vo as C

HERE = Path(__file__).resolve().parent
LEAD_IN, FPS, TAIL = 0.4, 30, 1.3
S = json.loads((HERE / "script.json").read_text())
SENT = json.loads((HERE / "public/vo/sentences.json").read_text())
HEARD = json.loads((HERE / "public/vo/whisper.json").read_text())
CUES = {e["action"] + ("" if e["action"] != "picker_open" else str(i)): e["t"]
        for i, e in enumerate(json.loads((HERE / "out/film_cues.json").read_text())["events"])}
take = json.loads((HERE / "public/vo/take.json").read_text())
voice_len = 0.3 + sum(c["dur"] + c["gap"] for c in take["chunks"])

# caption words: display words of the script, timed by the heard words they align with
MERGES = [(["a", "c", "l", "s", "med"], "aclsmed"), (["acls", "med"], "aclsmed"), (["acls", "medsim"], None)]
htok, hidx = [], []
for i, (w, _, _) in enumerate(HEARD):
    for c in C.canon_text(w):
        htok.append(c); hidx.append(i)
mt, mi, k = [], [], 0
while k < len(htok):
    if htok[k:k + 2] == ["acls", "med"]:
        mt.append("aclsmed"); mi.append(hidx[k]); k += 2
    else:
        mt.append(htok[k]); mi.append(hidx[k]); k += 1
stok, sword = [], []          # script canon tokens -> (line, display word index)
disp = {}
for ln in S["lines"]:
    ws = ln["text"].split()
    disp[ln["id"]] = ws
    for j, w in enumerate(ws):
        for c in C.canon_text(w):
            stok.append(c); sword.append((ln["id"], j))
sm = difflib.SequenceMatcher(a=stok, b=mt, autojunk=False)
tok_time = {}
for op, a0, a1, b0, b1 in sm.get_opcodes():
    for d in range(min(a1 - a0, b1 - b0)):
        h = HEARD[mi[b0 + d]]
        tok_time[a0 + d] = (h[1], h[2])
lines = []
for ln in S["lines"]:
    words = []
    for j, w in enumerate(disp[ln["id"]]):
        ts = [tok_time[i] for i, sw in enumerate(sword) if sw == (ln["id"], j) and i in tok_time]
        words.append({"w": w, "start": round(min(a for a, _ in ts) + LEAD_IN, 3), "end": round(max(b for _, b in ts) + LEAD_IN, 3)})
    sp = SENT[ln["id"]]
    lines.append({"id": ln["id"], "cue": ln["cue"], "start": round(sp[0][0] + LEAD_IN, 3), "end": round(sp[-1][1] + LEAD_IN, 3),
                  "sentences": [[round(a + LEAD_IN, 3), round(b + LEAD_IN, 3)] for a, b in sp], "words": words})
L = {l["id"]: l for l in lines}
ev = {k.rstrip("0123456789") if k.startswith("picker_open") else k: v for k, v in CUES.items()}
E = {  # rig events on the reel clock (scheduled time; measured video times agree within ~0.15 s, see events.py)
    "picker_open": CUES["picker_open0"] + LEAD_IN, "lead_II": CUES["lead:II"] + LEAD_IN, "lead_V1": CUES["lead:V1"] + LEAD_IN,
    "lead_aVF": CUES["lead:aVF"] + LEAD_IN, "picker_close": CUES["picker_close"] + LEAD_IN,
    "picker_open2": CUES["picker_open5"] + LEAD_IN, "all_leads": CUES["all_leads"] + LEAD_IN,
    "rhythm": CUES["rhythm:stemi_ant"] + LEAD_IN, "pause": CUES["pause"] + LEAD_IN, "print": CUES["print"] + LEAD_IN,
    "print_close": CUES["print_close"] + LEAD_IN, "play": CUES["play"] + LEAD_IN,
}
E = {k: round(v, 3) for k, v in E.items()}
w_of = lambda lid, w: next(x["start"] for x in L[lid]["words"] if x["w"].strip(".,") == w)
# leads on the 12-lead grid: [column, row]
R = {"I": [0, 0], "II": [0, 1], "III": [0, 2], "aVR": [0, 3], "aVL": [0, 4], "aVF": [0, 5],
     "V1": [1, 0], "V2": [1, 1], "V3": [1, 2], "V4": [1, 3], "V5": [1, 4], "V6": [1, 5]}
RED, BLUE, GREEN, AMBER = "#D92D20", "#1D4ED8", "#0B8A4E", "#B45309"
end_at = L["l10"]["start"] - 0.25
panels = [
    {"from": 0, "to": L["l2"]["start"] - 0.1, "kind": "title"},
    {"from": L["l2"]["start"] - 0.1, "to": E["picker_open2"], "kind": "lead", "eyebrow": "TAP THE ECG. PICK A LEAD.",
     "steps": [[0, "LEAD II"], [E["lead_V1"], "V1"], [E["lead_aVF"], "aVF"]], "color": GREEN},
    {"from": E["picker_open2"], "to": L["l4"]["start"] - 0.1, "kind": "big", "eyebrow": "ONE TAP", "text": "All 12 leads", "color": GREEN},
    {"from": L["l4"]["start"] - 0.1, "to": E["rhythm"] + 0.6, "kind": "mag", "eyebrow": "SINUS BRADYCARDIA · 48/MIN",
     "rows": ["II", "V1"], "color": GREEN, "outline": ["II", "V1"], "win": [0.12, 0.86]},
    {"from": E["rhythm"] + 0.6, "to": L["l6"]["start"] - 0.1, "kind": "mag", "eyebrow": "SINUS TACH 108 · ANTERIOR STEMI",
     "rows": ["V2", "V3"], "color": RED, "outline": ["V2", "V3"], "baseline": True, "win": [0.16, 0.90]},
    {"from": L["l6"]["start"] - 0.1, "to": w_of("l6", "I") - 0.1, "kind": "mag", "eyebrow": "ST ELEVATION · V1 TO V4",
     "rows": ["V2", "V3"], "color": RED, "outline": ["V1", "V2", "V3", "V4"], "baseline": True, "win": [0.16, 0.90]},
    {"from": w_of("l6", "I") - 0.1, "to": L["l7"]["start"] - 0.1, "kind": "mag", "eyebrow": "ST ELEVATION · I, aVL",
     "rows": ["I", "aVL"], "color": RED, "outline": ["I", "aVL"], "baseline": True, "win": [0.26, 0.70]},
    {"from": L["l7"]["start"] - 0.1, "to": L["l7"]["sentences"][2][0] - 0.1, "kind": "mag", "eyebrow": "RECIPROCAL ST DEPRESSION · III, aVF",
     "rows": ["III", "aVF"], "color": BLUE, "outline": ["III", "aVF"], "baseline": True, "win": [0.30, 0.68]},
    {"from": L["l7"]["sentences"][2][0] - 0.1, "to": L["l8"]["start"] - 0.1, "kind": "big", "eyebrow": "ONE SCREEN", "text": "The whole picture",
     "color": RED, "outlines": [["I", "aVL", "V1", "V2", "V3", "V4"], ["III", "aVF"]]},
    {"from": L["l8"]["start"] - 0.1, "to": E["print"] - 0.05, "kind": "big", "eyebrow": "FREEZE THE TRACE", "text": "PAUSE", "color": AMBER, "mono": True},
    {"from": E["print"] - 0.05, "to": L["l9"]["start"] - 0.1, "kind": "big", "eyebrow": "THE FULL 12-LEAD ON PAPER", "text": "PRINT", "color": GREEN, "mono": True},
    {"from": L["l9"]["start"] - 0.1, "to": end_at, "kind": "compare", "at2": L["l9"]["sentences"][1][0]},
]
dur = round(voice_len + LEAD_IN + TAIL, 3)
out = {"fps": FPS, "duration": dur, "lead_in": LEAD_IN, "end_at": round(end_at, 3), "events": E, "lines": lines,
       "panels": panels, "rows": R, "baseline": {"V2": 0.4783},  # isoelectric height in a row (same in every row)
       "colors": {"red": RED, "blue": BLUE, "green": GREEN, "amber": AMBER}}
(HERE / "src").mkdir(exist_ok=True)
(HERE / "src/timeline.json").write_text(json.dumps(out, indent=1) + "\n")
print("duration", dur, "end card", end_at)
for p in panels:
    print(f'{p["from"]:6.2f} {p["to"]:6.2f} {p["kind"]:7s} {p.get("eyebrow", "")}')
