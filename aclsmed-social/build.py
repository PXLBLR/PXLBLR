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
from engine.video import Reel  # noqa: E402

OUT = Path(__file__).parent / "out"


def _pick(fns, key):
    return [f for f in fns if not key or key in f()["id"]]


def render_reel(fn_name):
    fn = next(f for f in REELS if f.__name__ == fn_name)
    spec = fn()
    p = Reel(spec).render(OUT / "reels" / f"{spec['id']}.mp4")
    return str(p)


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
    if cmd == "preview":
        for f in _pick(REELS, key):
            print(preview(f))
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
