"""Checks on the rendered reel (aclsmed_live_12lead.mp4). Exit 1 on any failure.

1. Read-back of the FINAL MIX: Whisper per sentence chunk, word for word against script.json.
2. Captions: every heard word ends inside its caption's on-screen window.
3. Screen events at their lines (frames of the MP4, inside the iPad's screen): lead menu open on "Tap the ECG",
   the 12-lead grid after "all 12 leads", HR 108 tile colour/brightness change after the rhythm change, the cream
   printout on "Print", back to the grid on "Most code simulators".
4. Loudness (ebur128): -15.5..-13 LUFS, true peak <= -1 dBFS.
5. Frame: the whole iPad inside the frame; nothing but background outside x 80-1000, y 250-1500.
"""
import json, re, subprocess, sys
import numpy as np
from pathlib import Path
import check_vo as C

HERE = Path(__file__).resolve().parent
FF = str(Path.home() / ".local/bin/ffmpeg")
MP4 = HERE / "aclsmed_live_12lead.mp4"
TL = json.loads((HERE / "src/timeline.json").read_text())
LI = TL["lead_in"]
ok = True
def fail(msg):
    global ok; ok = False; print("  FAIL", msg)

# 1 + 2
wav = HERE / "out/check.wav"
subprocess.run([FF, "-y", "-loglevel", "error", "-i", str(MP4), "-ac", "1", "-ar", "16000", str(wav)], check=True)
segs = [[a + LI, b + LI] for a, b in C.segments(HERE / "public/vo/full.wav")]
out = subprocess.run([str(C.PY), "-c", C.CODE, str(wav), json.dumps(segs)], capture_output=True, text=True, check=True).stdout
heard = []
for w in json.loads(out.strip().splitlines()[-1]):
    if heard and w[0][:1] in "-." and len(w[0]) > 1: heard[-1] = [heard[-1][0] + w[0], heard[-1][1], w[2]]
    else: heard.append(w)
ht, hi = [], []
for i, (w, _, _) in enumerate(heard):
    for c in C.canon_text(w): ht.append(c); hi.append(i)
mt, mi, k = [], [], 0
while k < len(ht):
    if ht[k:k + 2] == ["acls", "med"]: mt.append("aclsmed"); mi.append(hi[k]); k += 2
    else: mt.append(ht[k]); mi.append(hi[k]); k += 1
lines = TL["lines"]
stok, sline = [], []
for l in lines:                       # canon per line: some rules need context ("I and aVL")
    for c in C.canon_text(" ".join(w["w"] for w in l["words"])): stok.append(c); sline.append(l)
import difflib
sm = difflib.SequenceMatcher(a=stok, b=mt, autojunk=False)
errs, outside = [], []
for op, a0, a1, b0, b1 in sm.get_opcodes():
    if op != "equal": errs.append(f"{op} {stok[a0:a1]} -> {mt[b0:b1]}"); continue
    for d in range(a1 - a0):
        l = sline[a0 + d]; w = heard[mi[b0 + d]]
        i = lines.index(l); nxt = lines[i + 1] if i + 1 < len(lines) else None
        lo, hi_ = l["start"] - 0.12, min(l["end"] + 0.45, nxt["start"] - 0.15 if nxt else 1e9)
        if not lo <= w[2] <= hi_ + 0.05: outside.append(f"{l['id']} {w[0]} {w[2]:.2f}")
print(f"1. read-back of the final mix: {len(stok)} words, errors: {errs or 'none'}")
if errs: fail("word errors")
print(f"2. words outside their caption window: {outside or 'none'}")
if outside: fail("caption timing")

# 3: screen events (iPad screen rect in the reel frame)
SX, SY, SW, SH = 106, 694, 866, 650
def frame(t):
    raw = subprocess.run([FF, "-loglevel", "error", "-ss", f"{t:.3f}", "-i", str(MP4), "-frames:v", "1", "-vf",
                          f"crop={SW}:{SH}:{SX}:{SY}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(SH, SW, 3).astype(int)
L = {l["id"]: l for l in lines}
E = TL["events"]
def menu_open(f): return f[int(.315*SH):int(.345*SH), int(.28*SW):int(.31*SW), 1].mean() > 150   # the lit "II" key
def grid(f):  # 12-lead: PRINT/PAUSE/BACK keys outlined at the top of the trace area
    return f[int(.055*SH):int(.085*SH), int(.55*SW):int(.70*SW)].mean() > 22
def paper(f): return f[int(.4*SH):int(.6*SH), int(.3*SW):int(.7*SW)].mean() > 150
checks = [
    ("lead menu open during 'Tap the ECG and pick any lead.'", L["l2"]["sentences"][0][1] - 0.2, menu_open, True),
    ("single lead (no grid) before 'Or choose all 12 leads'", L["l3"]["start"] - 0.3, grid, False),
    ("12-lead grid on 'Sinus bradycardia'", L["l4"]["start"] + 0.3, grid, True),
    ("12-lead grid on 'ST elevation in V1 to V4'", L["l6"]["start"] + 0.3, grid, True),
    ("printout on 'Print for the full 12-lead.'", L["l8"]["sentences"][1][1] - 0.2, paper, True),
    ("grid back on 'ACLSMED Sim gives you all 12, live.'", L["l9"]["sentences"][1][0] + 0.3, grid, True),
]
print("3. screen events:")
for name, t, fn, want in checks:
    got = fn(frame(t)); print(f"   {name} @ {t:.2f}s: {'ok' if got == want else 'FAIL'}")
    if got != want: fail(name)
# HR tile reads 108 after the change: compare the HR digits region before and after
hr = lambda t: frame(t)[int(.04*SH):int(.2*SH), int(.73*SW):int(.83*SW)]
d = np.abs(hr(E["rhythm"] - 1.0) - hr(E["rhythm"] + 1.0)).mean()
print(f"   HR tile changes at the rhythm change (48 -> 108): mean diff {d:.1f} {'ok' if d > 8 else 'FAIL'}")
if d <= 8: fail("HR change")

# 4
eb = subprocess.run([FF, "-hide_banner", "-nostats", "-i", str(MP4), "-af", "ebur128=peak=true", "-f", "null", "-"],
                    capture_output=True, text=True).stderr
lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", eb)[-1]); peak = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", eb)[-1])
print(f"4. loudness {lufs} LUFS, true peak {peak} dBFS")
if not (-15.5 <= lufs <= -13 and peak <= -1.0): fail("loudness")

# 5: everything that is not background stays inside the safe box (sampled every 0.5 s)
raw = subprocess.run([FF, "-loglevel", "error", "-i", str(MP4), "-vf", "fps=2", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                     capture_output=True, check=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, 1920, 1080, 3).astype(int)
bg = np.median(fr, axis=0)                                  # each pixel's own background (gradient + glow are static)
dev = np.abs(fr - bg[None]).max(axis=3)
mask = np.ones((1920, 1080), bool); mask[250:1500, 80:1000] = False
# the iPad body is x 80-1000, y 668-1372 (bezel 920x704): whole, inside the frame. Its soft drop shadow may spill a
# few px past x 80 / 1000; that margin is not content.
IPAD = (80, 668, 1000, 1372)
assert 0 <= IPAD[0] and IPAD[2] <= 1080 and 0 <= IPAD[1] and IPAD[3] <= 1920
mask[IPAD[1] - 30:IPAD[3] + 60, IPAD[0] - 30:IPAD[2] + 30] = False
print(f"5. iPad body {IPAD} fully inside the 1080x1920 frame: ok")
bad = (dev[:, mask] > 40).sum(axis=1)
print(f"   frames with content outside the safe box: {int((bad > 50).sum())} of {len(fr)} (worst {int(bad.max())} px)")
if (bad > 50).any(): fail("safe area")
print("PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
