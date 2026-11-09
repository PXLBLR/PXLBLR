"""Find when the rig's events show up in a raw take (video clock), and the offset to the voice clock.

    python3 events.py raw/take1.mov  -> prints per-event video times + offset; writes out/events.json
Signals (landscape frame scaled to 688x516): lead-menu popover (bright panel mid-screen), 12-lead header text,
HR digits change 48 -> 108, FROZEN label, printout paper (cream).
"""
import json, subprocess, sys
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
FF = str(Path.home() / ".local/bin/ffmpeg")
src = sys.argv[1]
W, H, FPS = 688, 516, 30
p = subprocess.run([FF, "-loglevel", "error", "-i", src, "-vf", f"fps={FPS},scale={W}:{H}", "-f", "rawvideo",
                    "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
fr = np.frombuffer(p, np.uint8).reshape(-1, H, W, 3).astype(np.int16)
t = np.arange(len(fr)) / FPS
def region(x0, y0, x1, y1):  # fractions of the frame
    return fr[:, int(y0*H):int(y1*H), int(x0*W):int(x1*W)]
# lead menu: the popover's "ECG LEAD" header band (panel grey over the black monitor)
menu = region(0.27, 0.23, 0.46, 0.26).mean(axis=(1, 2, 3))
# paper: cream printout covers the screen
paper = region(0.30, 0.40, 0.70, 0.60).mean(axis=(1, 2, 3))
# 12-lead view: its PRINT/PAUSE/BACK keys sit where lead II's label strip is in single-lead view
keys = region(0.55, 0.055, 0.70, 0.085).mean(axis=(1, 2, 3))
# FROZEN label: amber pixels in the 12-lead header
hdr = region(0.25, 0.055, 0.45, 0.085)
amber = ((hdr[..., 0] > 180) & (hdr[..., 1] > 110) & (hdr[..., 2] < 90)).mean(axis=(1, 2))
# HR digits: the tile's number area
hr = region(0.76, 0.09, 0.84, 0.18).mean(axis=(1, 2, 3))
np.save(HERE / "out/menu.npy", np.stack([menu, paper, keys, amber * 1000, hr]))
def first(sig, cond, after=0):
    idx = np.nonzero(cond(sig) & (t > after))[0]
    return float(t[idx[0]]) if len(idx) else None
base = np.median(menu[FPS * 5: FPS * 8])
print("menu baseline", base, "max", menu.max())
ev = {}
ev["picker_open_1"] = first(menu, lambda s: s > base + 12, 4)
ev["picker_close_1"] = first(menu, lambda s: s < base + 5, ev["picker_open_1"] + 0.5)
ev["picker_open_2"] = first(menu, lambda s: s > base + 12, ev["picker_close_1"] + 0.3)
ev["all_leads"] = first(keys, lambda s: s > np.median(keys[FPS * 5: FPS * 8]) + 8, ev["picker_open_2"])
hr0 = np.median(hr[FPS * 5: FPS * 8])
ev["rhythm"] = first(hr, lambda s: abs(s - hr0) > 6, ev["all_leads"] + 1)
ev["pause"] = first(amber, lambda s: s > 0.01, ev["rhythm"])
ev["print"] = first(paper, lambda s: s > 150, 5)
ev["print_close"] = first(paper, lambda s: s < 100, ev["print"] + 0.5)
cues = {e["action"]: e["t"] for e in json.loads((HERE / "out/film_cues.json").read_text())["events"]}
pairs = [("picker_open_1", cues["picker_open"]), ("picker_close_1", cues["picker_close"]), ("all_leads", cues["all_leads"]),
         ("rhythm", cues["rhythm:stemi_ant"]), ("pause", cues["pause"]), ("print", cues["print"]), ("print_close", cues["print_close"])]
offs = [ev[k] - v for k, v in pairs if ev[k] is not None]
for k, v in ev.items():
    print(f"{k:16s} {v}")
print("offsets video - voice:", [(k, round(ev[k] - v, 3)) for k, v in pairs if ev[k] is not None])
json.dump({"events": ev, "offset": round(float(np.median(offs)), 3), "frames": len(fr), "fps": FPS},
          open(HERE / "out/events.json", "w"), indent=1)
