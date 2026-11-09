"""Checks on a rendered reel:  python3 check_reel.py R02_pvt [R03_torsades ...]

1. Read-back of the FINAL MIX (voice + bed + beeps): Whisper per sentence chunk, word for word against the script.
2. Captions: every heard word ends inside its caption's on-screen window (line at - 0.1 .. end + 0.3).
3. Cues: the rhythm starts before the first word of the onset line; the key tag starts within 0.2 s of its sentence;
   the end card is up before "Practice it on ...".
4. Loudness of the MP4 (ffmpeg ebur128): integrated LUFS and true peak.
5. Voice over bed + beeps per line, from the stems (make_audio.py run without writing).
Prints one block per reel; exit code 1 if any reel fails 1-4.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

import check_vo as C
import reel

HERE = Path(__file__).resolve().parent
FF = str(Path.home() / ".local/bin/ffmpeg")
SP = HERE / "out" / "check"
SP.mkdir(parents=True, exist_ok=True)


def stems(rid):
    src = (HERE / "make_audio.py").read_text()
    src = src[:src.index("# Loudness:")]
    ns = {"__file__": str(HERE / "make_audio.py")}
    argv, sys.argv = sys.argv, ["make_audio.py", rid]
    try:
        exec(compile(src, "make_audio.py", "exec"), ns)
    finally:
        sys.argv = argv
    return ns["SR"], ns["voice"], (ns["bed"] + ns["fx"] * 0.8) * ns["duck"]


def check(rid):
    R = reel.load(rid)
    TL = json.loads(R["timeline"].read_text())
    mp4 = HERE / "out" / R["cfg"]["out"]
    wav = SP / f"{rid}.wav"
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", str(mp4), "-ac", "1", "-ar", "16000", str(wav)], check=True)
    segs = [[a + 0.4, b + 0.4] for a, b in C.segments(R["vo"] / "full.wav")]
    out = subprocess.run([str(C.PY), "-c", C.CODE, str(wav), json.dumps(segs)], capture_output=True, text=True, check=True).stdout
    heard = []
    for w in json.loads(out.strip().splitlines()[-1]):
        if heard and w[0][:1] in "-." and len(w[0]) > 1:
            heard[-1] = [heard[-1][0] + w[0], heard[-1][1], w[2]]
        else:
            heard.append(w)
    # canonical tokens both sides (same rules as check_vo)
    ht, hi = [], []
    for i, (w, _, _) in enumerate(heard):
        for c in C.canon_text(w):
            ht.append(c); hi.append(i)
    stok, sline = [], []
    for ln in TL["lines"]:
        for c in C.canon_text(ln["text"]):
            stok.append(c); sline.append(ln)
    merges = [(["acls", "med"], "aclsmed"), (["v", "fib"], "vfib"), (["v", "tach"], "vtach"), (["a", "fib"], "afib"),
              (["tor", "sades"], "torsades"), (["tor", "saz"], "torsades"), (["cardio", "version"], "cardioversion"), (["s", "v", "t"], "svt"), (["p", "e", "a"], "pea")]
    mt, mi, k = [], [], 0
    while k < len(ht):
        for p, r in merges:
            if ht[k:k + len(p)] == p:
                mt.append(r); mi.append(hi[k]); k += len(p); break
        else:
            mt.append(ht[k]); mi.append(hi[k]); k += 1
    import difflib
    sm = difflib.SequenceMatcher(a=stok, b=mt, autojunk=False)
    errors, outside, first = [], [], {}
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        if op != "equal":
            errors.append(f"{op} {stok[a0:a1]} -> {mt[b0:b1]}"); continue
        for d in range(a1 - a0):
            ln, w = sline[a0 + d], heard[mi[b0 + d]]
            first.setdefault(ln["id"], w[1])
            # Whisper starts a chunk's first word at the clip edge, so judge each word by its end
            if not ln["at"] - 0.1 <= w[2] <= ln["end"] + 0.3:
                outside.append(f"{ln['id']} {w[0]} {w[1]:.2f}")
    script = R["script"]["lines"]
    onset_line = next(l["id"] for l in script if l["cue"] == "onset")
    end_line = next(l["id"] for l in script if l["cue"] == "end")
    sents = json.loads((R["vo"] / "sentences.json").read_text())
    key_line = next(l for l in script if l["cue"] == "key")
    key_said = 0.4 + sents[key_line["id"]][key_line.get("key_sentence", -1)][0]
    said = lambda lid: 0.4 + sents[lid][0][0]   # where the voice starts that line (waveform-snapped, check_vo.py)
    cues = {
        "onset before first onset word": (TL["onset"], said(onset_line), TL["onset"] < said(onset_line)),
        "key tag on its sentence": (TL["key"], key_said, abs(TL["key"] - key_said) < 0.2),
        "end card before 'Practice'": (TL["end_card"], said(end_line), TL["end_card"] < said(end_line)),
    }
    eb = subprocess.run([FF, "-hide_banner", "-nostats", "-i", str(mp4), "-af", "ebur128=peak=true", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", eb)[-1]); peak = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", eb)[-1])
    SR, v, bg = stems(rid)
    db = lambda x: 10 * np.log10(np.mean(np.asarray(x, np.float64) ** 2) + 1e-12)
    per_line = [db(v[int(l["at"] * SR):int(l["end"] * SR)]) - db(bg[int(l["at"] * SR):int(l["end"] * SR)]) for l in TL["lines"]]
    ok = not errors and all(c[2] for c in cues.values()) and -15.5 <= lufs <= -13.0 and peak <= -1.0
    print(f"== {rid} ({mp4.name}, {TL['duration']} s): {'PASS' if ok else 'FAIL'}")
    print(f"   read-back of final mix: {len(stok)} words, errors: {errors or 'none'}")
    print(f"   words outside caption window: {outside or 'none'}")
    for name, (a, b, good) in cues.items():
        print(f"   {name}: {a:.2f} vs {b:.2f} {'ok' if good else 'FAIL'}")
    print(f"   loudness {lufs} LUFS, peak {peak} dBFS; voice over bed+beeps per line: "
          f"{' '.join(f'{x:.0f}' for x in per_line)} dB (min {min(per_line):.1f})")
    return ok


if __name__ == "__main__":
    ids = sys.argv[1:] or reel.IDS
    results = [check(r) for r in ids]
    sys.exit(0 if all(results) else 1)
