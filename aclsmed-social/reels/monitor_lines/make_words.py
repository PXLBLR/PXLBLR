"""Word timings for the burned-in captions -> src/words.json.

Words come from the script (timeline.json `vo[].text`), timed from Whisper
(src/vo_whisper.json, large-v3-turbo on each narration clip). Whisper puts a
word's START too early after a pause (it absorbs the silence), so every start
that falls in silence is moved to the next voiced onset measured from the
clip itself (20 ms RMS frames, 35 dB under the clip's peak).

Line 9 is the end card ("Integrated. Immersive. Essential. ACLSmed.com"): its
four phrases are timed straight from the four voiced regions of the clip.

    python3 make_words.py
"""
import json
import re
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TL = json.loads((HERE / "timeline.json").read_text())
WH = json.loads((HERE / "src" / "vo_whisper.json").read_text())


def voiced(path):
    with wave.open(str(path)) as w:
        sr, ch = w.getframerate(), w.getnchannels()
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
    if ch > 1:
        x = x.reshape(-1, ch).mean(1)
    hop = int(sr * 0.02)
    r = np.array([20 * np.log10(np.sqrt(np.mean(x[i:i + hop] ** 2)) + 1e-9) for i in range(0, len(x) - hop, hop)])
    on = r > r.max() - 35
    segs, i = [], 0
    while i < len(on):
        if on[i]:
            j = i
            while j < len(on) and (on[j] or on[j:j + 6].any()):   # bridge gaps < 120 ms
                j += 1
            segs.append((i * 0.02, j * 0.02))
            i = j
        else:
            i += 1
    return segs, len(x) / sr


def snap(t, segs):
    for a, b in segs:
        if a <= t < b:
            return t
        if t < a:
            return a
    return t


def main():
    out = []
    for line in TL["vo"]:
        segs, dur = voiced(HERE / "public" / "vo" / f"{line['id']}.wav")
        script = line["text"].split()
        if line["id"] == "l9":
            phrases = ["Integrated.", "Immersive.", "Essential.", "ACLSmed.com"]
            assert len(segs) == 4, segs
            words = [{"w": p, "start": a, "end": b} for p, (a, b) in zip(phrases, segs)]
        else:
            wh = [list(x) for x in WH[line["id"]]["words"]]
            # Whisper wrote "coderoom." as one word; the script has two.
            k = 0
            while k < len(wh):
                if re.fullmatch(r"coderoom\.?", wh[k][0], re.I):
                    a, b = wh[k][1], wh[k][2]
                    wh[k:k + 1] = [["code", a, (a + b) / 2], ["room.", (a + b) / 2, b]]
                k += 1
            assert len(wh) == len(script), (line["id"], [x[0] for x in wh], script)
            words = []
            for s, (_, a, b) in zip(script, wh):
                a = snap(a, segs)
                words.append({"w": s, "start": a, "end": max(b, a + 0.08)})
        for w in words:
            w["start"] = round(line["at"] + w["start"], 3)
            w["end"] = round(line["at"] + w["end"], 3)
            w["key"] = w["w"] in line.get("key", [])
        out.append({"id": line["id"], "at": line["at"], "dur": round(dur, 3),
                    "speechStart": round(line["at"] + segs[0][0], 3),
                    "speechEnd": round(line["at"] + segs[-1][1], 3), "words": words})
        print(f"{line['id']:4s} {out[-1]['speechStart']:6.2f}-{out[-1]['speechEnd']:6.2f}  "
              + " ".join(f"{w['w']}@{w['start']:.2f}" for w in words))
    (HERE / "src" / "words.json").write_text(json.dumps(out, indent=1))
    print("wrote src/words.json")


if __name__ == "__main__":
    main()
