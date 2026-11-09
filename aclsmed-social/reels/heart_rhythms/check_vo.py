"""Read the narration back with Whisper and check it word for word against script.json; write public/vo/lines.json.

    python3 check_vo.py R02_pvt [wav]      (default public/R02_pvt/vo/full.wav)

Whisper large-v3-turbo (mlx, the Prayer Voice venv) with word timestamps. Both sides are put in one canonical form
(lower case, no punctuation, "V-fib"/"vee-fib"/"VFib" -> vfib, "S-A"/"S.A." -> sa, "ACLS med"/"ACLSmed" -> aclsmed,
".com" -> dot com) and aligned word by word. Any dropped, added or changed word is printed and the exit code is 1.
lines.json = {line id: [start of its first word, end of its last word]} in seconds within the wav; each edge is then
snapped to where the voice actually starts/stops in the waveform (Whisper clamps the first word to 0.0 and often starts
a word inside the pause before it).
sentences.json = the same per sentence ({line id: [[start, end], ...]}), for cues inside a line ("No pulse.").
Whisper words are also saved to public/vo/whisper.json.
"""
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

import reel

R = None
VO = None
PY = Path.home() / "Developer/tts/PrayerVoice/.venv/bin/python"
# Whisper per sentence chunk (take.json gives each chunk's exact place in full.wav): short clips read far more reliably
# than one long file, which dropped the last phrase and once doubled a word. Without take.json: the whole file.
CODE = """
import json, sys, mlx_whisper
from mlx_whisper.audio import load_audio
wav, segs = sys.argv[1], json.loads(sys.argv[2])
audio = load_audio(wav)
out = []
for a, b in segs:
    clip = audio[int(max(0, a) * 16000):int(b * 16000)]
    r = mlx_whisper.transcribe(clip, path_or_hf_repo='mlx-community/whisper-large-v3-turbo', word_timestamps=True,
                               language='en', no_speech_threshold=None, condition_on_previous_text=False)
    out += [[w['word'].strip(), round(w['start'] + max(0, a), 3), round(w['end'] + max(0, a), 3)] for s in r['segments'] for w in s['words']]
print(json.dumps(out))
"""


def segments(wav):
    take = wav.parent / "take.json"
    if wav.name != "full.wav" or not take.exists():
        return [[0, 1e6]]
    t, segs = 0.3, []
    for c in json.loads(take.read_text())["chunks"]:
        segs.append([round(t - 0.08, 3), round(t + c["dur"] + 0.08, 3)])
        t += c["dur"] + c["gap"]
    return segs


def canon_text(s):
    s = s.lower()
    s = re.sub(r"\.com\b", " dot com", s)
    s = re.sub(r"\b(?:vee|v)[\s-]*fib\b", "vfib", s)
    s = re.sub(r"\b(?:vee|v)[\s-]*(?:tach|tack|tac|tak)\b", "vtach", s)
    s = re.sub(r"\b(?:ay|a)[\s-]*fib\b", "afib", s)
    s = re.sub(r"\bs[\s.-]*v[\s.-]*t\b\.?", "svt", s)
    s = re.sub(r"\bp[\s.-]*e[\s.-]*a\b\.?", "pea", s)
    s = re.sub(r"\bi[\s.-]*v\b\.?(?=\s+magnesium)", "iv", s)
    s = re.sub(r"\bq[\s.-]*t\b\.?", "qt", s)
    s = re.sub(r"\btorsade\b", "torsades", s)
    s = re.sub(r"\bpointe?s?\b", "pointes", s)          # same sound in French
    s = re.sub(r"\btor\s*-?\s*[sz]a(?:h)?(?:d(?:e?[sz]|'s)?|[sz])\b", "torsades", s)
    s = re.sub(r"\bthird\b", "3rd", s)
    for k, w in enumerate(["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]):
        s = re.sub(rf"\b{w}\b", str(k), s)
    s = re.sub(r"\bmanoeuvres\b", "maneuvers", s)
    s = re.sub(r"\b(\d+)\s*(?:-|to)\s*(\d+)\b", r"\1 to \2", s)
    s = re.sub(r"\bs[\s.-]*a\.?(?=\s+node)", "sa", s)
    s = re.sub(r"\ba[\s.-]*v\.?(?=\s+node)", "av", s)
    s = re.sub(r"\ba[\s.-]*c[\s.-]*l[\s.-]*s[\s.-]*med\b", "aclsmed", s)
    s = re.sub(r"\bmedsim\b", "med sim", s)          # Whisper runs "med Sim" together
    s = re.sub(r"\bacls\s+med\b", "aclsmed", s)
    s = s.replace("'", "")
    return re.findall(r"[a-z0-9]+", s)


def snap(wav, spans):
    import wave
    import numpy as np
    with wave.open(str(wav)) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
        if w.getnchannels() == 2:
            x = x.reshape(-1, 2).mean(1)
    hop = sr // 100
    rms = np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, mode="same"))[::hop]
    on = rms > rms.max() * 10 ** (-55 / 20)           # voice = within 55 dB of the loudest moment (gaps are digital silence)
    out = {}
    for k, (s, e) in spans.items():
        a = int(max(0, s - 0.1) * 100); b = int((s + 0.6) * 100)
        hit = np.nonzero(on[a:b])[0]
        s2 = (a + hit[0]) / 100 if len(hit) else s
        a = int((e - 0.5) * 100); b = int((e + 0.4) * 100)
        hit = np.nonzero(on[a:b])[0]
        e2 = (a + hit[-1] + 1) / 100 if len(hit) else e
        out[k] = [round(float(s2), 3), round(float(e2), 3)]
    return out


def main():
    global R, VO
    R = reel.load(); VO = R["vo"]
    rest = [a for a in sys.argv[1:] if a != R["id"]]
    wav = Path(rest[0]) if rest else VO / "full.wav"
    out = subprocess.run([str(PY), "-c", CODE, str(wav), json.dumps(segments(wav))], capture_output=True, text=True, check=True).stdout
    heard = []
    for w in json.loads(out.strip().splitlines()[-1]):   # glue "V" "-fib", "20" "-40", "aclsmed" ".com" back together
        if heard and w[0][:1] in "-." and len(w[0]) > 1:
            heard[-1] = [heard[-1][0] + w[0], heard[-1][1], w[2]]
        else:
            heard.append(w)
    (VO / "whisper.json").write_text(json.dumps(heard) + "\n")
    # canonical tokens of what Whisper heard, each pointing back to its Whisper word (first, last)
    htok, hidx = [], []
    for i, (w, _, _) in enumerate(heard):
        for c in canon_text(w):
            htok.append(c); hidx.append((i, i))
    # join forms Whisper splits across words: "ACLS" "med", "A" "C" "L" "S" "med", "V" "fib", "S" "A" (node)
    MERGES = [(["a", "c", "l", "s", "med"], "aclsmed"), (["acls", "med"], "aclsmed"),
              (["v", "fib"], "vfib"), (["vee", "fib"], "vfib"),
              (["v", "tach"], "vtach"), (["v", "tack"], "vtach"), (["vee", "tach"], "vtach"), (["vee", "tack"], "vtach"),
              (["a", "fib"], "afib"), (["ay", "fib"], "afib"), (["s", "v", "t"], "svt"), (["p", "e", "a"], "pea"),
              (["tor", "sades"], "torsades"), (["cardio", "version"], "cardioversion"),
              (["q", "t"], "qt"), (["i", "v"], "iv"), (["s", "a", "node"], "sa"), (["a", "v", "node"], "av")]
    merged_t, merged_i, k = [], [], 0
    while k < len(htok):
        for pat, rep in MERGES:
            if rep and htok[k:k + len(pat)] == pat:
                n = len(pat) - (1 if pat[-1] == "node" else 0)
                merged_t.append(rep); merged_i.append((hidx[k][0], hidx[k + n - 1][1])); k += n
                break
        else:
            merged_t.append(htok[k]); merged_i.append(hidx[k]); k += 1

    script = R["script"]
    stok, sline, ssent = [], [], []          # script tokens, their line id, their sentence number within the line
    for ln in script["lines"]:
        for k, sent in enumerate(re.split(r"(?<=\.)\s+", ln["text"])):
            for c in canon_text(sent):
                stok.append(c); sline.append(ln["id"]); ssent.append(k)

    sm = difflib.SequenceMatcher(a=stok, b=merged_t, autojunk=False)
    errors = []
    s2h = {}
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        if op == "equal":
            for d in range(a1 - a0):
                s2h[a0 + d] = merged_i[b0 + d]
        else:
            errors.append(f"{op}: script {stok[a0:a1]} vs heard {merged_t[b0:b1]} "
                          f"(at {heard[merged_i[b0][0]][1] if b0 < len(merged_i) else '?'} s)")
            for d in range(min(a1 - a0, b1 - b0)):     # timing for replaced words still comes from where they sit
                s2h[a0 + d] = merged_i[b0 + d]
    if errors:
        print("heard:", " ".join(w for w, _, _ in heard))
        print("\nWORD ERRORS:"); [print(" ", e) for e in errors]
        sys.exit(1)

    def span(idx):
        idx = [i for i in idx if i in s2h]
        return [round(heard[s2h[idx[0]][0]][1], 3), round(heard[s2h[idx[-1]][1]][2], 3)]
    spans = snap(wav, {ln["id"]: span([i for i, l in enumerate(sline) if l == ln["id"]]) for ln in script["lines"]})
    sents = {}
    for ln in script["lines"]:
        ks = sorted({ssent[i] for i, l in enumerate(sline) if l == ln["id"]})
        sp = snap(wav, {k: span([i for i, l in enumerate(sline) if l == ln["id"] and ssent[i] == k]) for k in ks})
        sents[ln["id"]] = [sp[k] for k in ks]
    print("heard:", " ".join(w for w, _, _ in heard))
    for k, v in spans.items():
        print(k, v)
    if errors:
        print("\nWORD ERRORS:"); [print(" ", e) for e in errors]
        sys.exit(1)
    (VO / "lines.json").write_text(json.dumps(spans, indent=1) + "\n")
    (VO / "sentences.json").write_text(json.dumps(sents, indent=1) + "\n")
    print("sentences:", sents)
    print(f"\nclean: {len(stok)} script words all read; wrote public/vo/lines.json + sentences.json")


if __name__ == "__main__":
    main()
