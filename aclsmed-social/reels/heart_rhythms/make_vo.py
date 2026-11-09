"""Render a reel's narration as one take with the owner's "Mikko (narration) v2" voice (Prayer Voice.app, 127.0.0.1:8872).

    python3 make_vo.py R02_pvt [take]                  -> public/R02_pvt/vo/full.wav (+ take.json: text sent, chunks)
    python3 make_vo.py R02_pvt --say "text" [take] [out.wav]   -> one phrase
    python3 make_vo.py R09_mobitz2 --splice "Then pace" 3      -> re-render the sentence containing that text with take 3
                                                                   and splice it into full.wav at its breaths (take.json notes it)

The app renders every sentence as its own breath group and joins them; a [pause N] marker right after a sentence sets
that gap exactly. Gaps: the script's gap_after between lines, IN_LINE between sentences of one line.
Pronunciation is fixed in the text sent to the voice (SPOKEN + the script's optional "spoken" map); captions keep the
script's spelling. full.wav is gitignored on purpose (public repo; a dry voice stem is cloning material).
"""
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

import reel

API = "http://127.0.0.1:8872"
IN_LINE = 0.35       # between two sentences of the same line
MIN_GAP = 0.3
SPOKEN = [           # written -> what the voice is given (whole words only)
    ("ACLSmed dot com", "A-C-L-S med dot com"),
    ("ACLSMED Sim", "A-C-L-S med Sim"),
    ("V-fib", "Vee-fib"),
    ("V-tach", "Vee-tack"),
    ("SA node", "S-A node"),
    ("AV node", "A-V node"),
    ("SVT", "S-V-T"),
    ("PEA", "P-E-A"),
    ("QT", "Q-T"),
    ("IV", "I-V"),
]


def spoken(text, extra=()):
    for a, b in list(extra) + SPOKEN:
        text = re.sub(rf"(?<![\w-]){re.escape(a)}(?![\w-])", b, text)
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


def script_text(script):
    extra = [tuple(p) for p in script.get("spoken", [])]
    parts = []
    for ln in script["lines"]:
        sents = re.split(r"(?<=\.)\s+", ln["text"].strip())
        for k, s in enumerate(sents):
            gap = max(MIN_GAP, ln["gap_after"]) if k == len(sents) - 1 else IN_LINE
            parts.append(f"{spoken(s, extra)} [pause {gap}]")
    return " ".join(parts)


if __name__ == "__main__":
    R = reel.load()
    args = [a for a in sys.argv[1:] if a != R["id"]]
    if args[:1] == ["--say"]:
        text, take = args[1], int(args[2]) if len(args) > 2 else 0
        out = Path(args[3]) if len(args) > 3 else R["vo"] / "patch.wav"
        v = render(spoken(text, [tuple(p) for p in R["script"].get("spoken", [])]) + " [pause 0.3]", take, out)
        print(out, v["chunks"])
        sys.exit()
    if args[:1] == ["--splice"]:
        import wave
        import numpy as np
        needle, take = args[1], int(args[2])
        tj = json.loads((R["vo"] / "take.json").read_text())
        t, hit = 0.3, None
        for i, c in enumerate(tj["chunks"]):
            if needle.lower() in c["text"].lower():
                hit = (i, t, c); break
            t += c["dur"] + c["gap"]
        if hit is None:
            sys.exit(f"no sentence contains {needle!r}")
        i, start, c = hit
        tmp = R["vo"] / "patch.wav"
        v = render(c["text"] + " [pause 0.3]", take, tmp)   # chunk text is already in spoken form
        with wave.open(str(tmp)) as w:
            sr = w.getframerate(); pa = np.frombuffer(w.readframes(w.getnframes()), np.int16)
        new = pa[int(0.3 * sr):int(0.3 * sr) + int(round(v["chunks"][0]["dur"] * sr))]
        with wave.open(str(R["vo"] / "full.wav")) as w:
            params = w.getparams(); fa = np.frombuffer(w.readframes(w.getnframes()), np.int16)
        a, b = int(round(start * sr)), int(round((start + c["dur"]) * sr))
        out = np.concatenate([fa[:a], new, fa[b:]])
        with wave.open(str(R["vo"] / "full.wav"), "wb") as w:
            w.setparams(params); w.writeframes(out.tobytes())
        c["dur"] = round(len(new) / sr, 3); c["spliced_take"] = take
        (R["vo"] / "take.json").write_text(json.dumps(tj, indent=1) + "\n")
        tmp.unlink()
        print(f"{R['id']}: spliced chunk {i} ({c['text']!r}) take {take}, {c['dur']} s")
        sys.exit()
    take = int(args[0]) if args else 0
    text = script_text(R["script"])
    print(text)
    v = render(text, take, R["vo"] / "full.wav")
    (R["vo"] / "take.json").write_text(json.dumps({"take": take, "sent": text, "chunks": v["chunks"]}, indent=1) + "\n")
    print(f"{R['id']}: wrote vo/full.wav", v["seconds"], "s,", len(v["chunks"]), "chunks, render", v["render_seconds"], "s")
