"""Read the narration back with Whisper and check it word for word against script.json; write public/vo/lines.json.

    python3 check_vo.py [wav]      (default public/vo/full.wav)

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

HERE = Path(__file__).resolve().parent
VO = HERE / "public" / "vo"
PY = Path.home() / "Developer/tts/PrayerVoice/.venv/bin/python"
CODE = ("import mlx_whisper, json, sys; r = mlx_whisper.transcribe(sys.argv[1], "
        "path_or_hf_repo='mlx-community/whisper-large-v3-turbo', word_timestamps=True, language='en', "
        "no_speech_threshold=None, condition_on_previous_text=False); "
        "print(json.dumps([[w['word'].strip(), w['start'], w['end']] for s in r['segments'] for w in s['words']]))")


def canon_text(s):
    s = s.lower()
    s = re.sub(r"\.com\b", " dot com", s)
    s = re.sub(r"\b(?:vee|v)[\s-]*fib\b", "vfib", s)
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
    wav = Path(sys.argv[1]) if len(sys.argv) > 1 else VO / "full.wav"
    out = subprocess.run([str(PY), "-c", CODE, str(wav)], capture_output=True, text=True, check=True).stdout
    heard = json.loads(out.strip().splitlines()[-1])
    (VO / "whisper.json").write_text(json.dumps(heard) + "\n")
    # canonical tokens of what Whisper heard, each pointing back to its Whisper word (first, last)
    htok, hidx = [], []
    for i, (w, _, _) in enumerate(heard):
        for c in canon_text(w):
            htok.append(c); hidx.append((i, i))
    # join forms Whisper splits across words: "ACLS" "med", "A" "C" "L" "S" "med", "V" "fib", "S" "A" (node)
    MERGES = [(["a", "c", "l", "s", "med"], "aclsmed"), (["acls", "med"], "aclsmed"),
              (["v", "fib"], "vfib"), (["vee", "fib"], "vfib"), (["s", "a", "node"], "sa"), (["a", "v", "node"], "av")]
    merged_t, merged_i, k = [], [], 0
    while k < len(htok):
        for pat, rep in MERGES:
            if rep and htok[k:k + len(pat)] == pat:
                n = len(pat) - (1 if pat[-1] == "node" else 0)
                merged_t.append(rep); merged_i.append((hidx[k][0], hidx[k + n - 1][1])); k += n
                break
        else:
            merged_t.append(htok[k]); merged_i.append(hidx[k]); k += 1

    script = json.loads((HERE / "script.json").read_text())
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
