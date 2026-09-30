"""Build ACLSMED Oct 1–7 content.

  python3 build.py reels            # render all reels to out/reels/*.mp4 (+ _cover.png)
  python3 build.py reels R3         # render reels whose id contains "R3"
  python3 build.py carousels        # render carousel slides to out/carousels/<id>/NN.png
  python3 build.py preview R3       # contact sheet of frames for quick QA (no encode)
"""
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from content.reels import REELS  # noqa: E402
from content.reels_oct8_25 import REELS2  # noqa: E402
from engine.video import Reel  # noqa: E402

OUT = Path(__file__).parent / "out"


def _pick(fns, key):
    return [f for f in fns if not key or key in f()["id"]]


def render_reel(fn_name, batch="reels"):
    fns, sub = (REELS2, "reels_oct8_25") if batch == "reels2" else (REELS, "reels")
    fn = next(f for f in fns if f.__name__ == fn_name)
    spec = fn()
    p = Reel(spec).render(OUT / sub / f"{spec['id']}.mp4")
    return str(p)


def lint(spec):
    """Flag text/pill layers that overlap each other, the monitor panel, or IG UI zones while on screen."""
    r = Reel(spec)
    boxes = []
    for el in spec["elements"]:
        if el["type"] in ("text", "pill", "icon"):
            img = r.layer(el)
            x, y = r._pos(el, img)
            bb = img.getbbox() or (0, 0, 1, 1)
            boxes.append((el["t"], (x + bb[0], y + bb[1], x + bb[2], y + bb[3]), el.get("txt", el["type"])[:40]))
    mons = [(el["t"], (el["rect"][0] - 20, el["rect"][1] - 58, el["rect"][0] + el["rect"][2] + 20,
                       el["rect"][1] + el["rect"][3] + 16)) for el in spec["elements"] if el["type"] in ("ecg", "capno")]
    probs = []

    def ov(a, b):
        return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]

    def tov(a, b):
        return a[0] < b[1] - 0.2 and b[0] < a[1] - 0.2

    endcard_start = max(e["t"][0] for e in spec["elements"] if e["type"] == "box")
    for i, (t1, b1, n1) in enumerate(boxes):
        if b1[3] > 1500 or b1[1] < 150:
            probs.append(f"out of safe zone: {n1!r} {b1}")
        if t1[0] >= endcard_start:
            continue
        for t2, b2, n2 in boxes[i + 1:]:
            if tov(t1, t2) and ov(b1, b2) and t2[0] < endcard_start:
                probs.append(f"overlap: {n1!r} x {n2!r}")
        for tm, bm in mons:
            if tov(t1, tm) and ov(b1, bm):
                probs.append(f"on monitor: {n1!r} t={t1}")
    return probs


def preview(fn, step=1.6, cols=6):
    spec = fn()
    r = Reel(spec)
    ts = [x * step + 0.8 for x in range(int(spec["duration"] / step))]
    thumbs = [r.frame(t).resize((270, 480)) for t in ts]
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 270, rows * 480), (0, 0, 0))
    for i, im in enumerate(thumbs):
        sheet.paste(im, ((i % cols) * 270, (i // cols) * 480))
    dst = OUT / "preview" / f"{spec['id']}.png"
    dst.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(dst)
    return dst


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "reels"
    key = sys.argv[2] if len(sys.argv) > 2 else ""
    if cmd in ("preview", "preview2"):
        for f in _pick(REELS2 if cmd == "preview2" else REELS, key):
            print(preview(f))
    elif cmd == "lint":
        for f in REELS + REELS2:
            spec = f()
            for pr in lint(spec):
                print(spec["id"], "|", pr)
            print(f"{spec['id']}: {spec['duration']:.1f}s")
    elif cmd == "reels2":
        from functools import partial
        names = [f.__name__ for f in _pick(REELS2, key)]
        with ProcessPoolExecutor(max_workers=4) as ex:
            for p in ex.map(partial(render_reel, batch="reels2"), names):
                print("rendered", p)
    elif cmd == "reels":
        names = [f.__name__ for f in _pick(REELS, key)]
        with ProcessPoolExecutor(max_workers=4) as ex:
            for p in ex.map(render_reel, names):
                print("rendered", p)
    elif cmd == "carousels":
        from content.carousels import CAROUSELS
        from engine.carousel import render_carousel
        for c in CAROUSELS:
            if not key or key in c["id"]:
                print(render_carousel(c, OUT / "carousels"))
