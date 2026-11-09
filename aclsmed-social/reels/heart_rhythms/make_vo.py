"""Render the narration as one take with the owner's "Mikko (narration) v2" voice (Prayer Voice.app, 127.0.0.1:8872).

    python3 make_vo.py [take]          -> public/vo/full.wav (+ public/vo/take.json: chunk texts, durations, gaps)
    python3 make_vo.py --say "text" [take] [out.wav]   -> one phrase, for a splice

The app renders every sentence as its own breath group and joins them; a [pause N] marker right after a sentence sets
that gap exactly. Gaps: the script's gap_after between lines, IN_LINE between sentences of one line.
Pronunciation is fixed in the text sent to the voice (SPOKEN); captions keep the script's spelling.
"""
import json
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
VO = HERE / "public" / "vo"
API = "http://127.0.0.1:8872"
IN_LINE = 0.35       # between two sentences of the same line
MIN_GAP = 0.3
SPOKEN = [           # written -> what the voice is given
    ("ACLSmed dot com", "A-C-L-S med dot com"),
    ("ACLSMED Sim", "A-C-L-S med Sim"),
    ("V-fib", "Vee-fib"),
    ("SA node", "S-A node"),
    ("AV node", "A-V node"),
]


def spoken(text):
    for a, b in SPOKEN:
        text = text.replace(a, b)
    return text


def call(path, body=None):
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read() if path.endswith(".wav") else json.loads(r.read())


def render(text, take, out):
    job = call("/render", {"text": text, "voice": "narration", "take": take, "reuse": True})
    while True:
        v = call(f"/job/{job['id']}")
        if v["status"] in ("done", "error", "cancelled"):
            break
        time.sleep(1)
    if v["status"] != "done":
        sys.exit(f"render failed: {v}")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(call(f"/job/{job['id']}/full.wav"))
    return v


if __name__ == "__main__":
    if sys.argv[1:2] == ["--say"]:
        text, take = sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 0
        out = Path(sys.argv[4]) if len(sys.argv) > 4 else VO / "patch.wav"
        v = render(spoken(text) + " [pause 0.3]", take, out)
        print(out, v["chunks"])
        sys.exit()
    take = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    script = json.loads((HERE / "script.json").read_text())
    parts = []
    for ln in script["lines"]:
        sents = [s.strip() + "." for s in ln["text"].rstrip(".").split(". ")]
        for k, s in enumerate(sents):
            last = k == len(sents) - 1
            gap = max(MIN_GAP, ln["gap_after"]) if last else IN_LINE
            parts.append(f"{spoken(s)} [pause {gap}]")
    text = " ".join(parts)
    print(text)
    v = render(text, take, VO / "full.wav")
    (VO / "take.json").write_text(json.dumps({"take": take, "sent": text, "chunks": v["chunks"]}, indent=1) + "\n")
    print("wrote public/vo/full.wav", v["seconds"], "s,", len(v["chunks"]), "chunks, render", v["render_seconds"], "s")
