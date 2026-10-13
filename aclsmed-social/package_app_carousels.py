"""Package the app carousels for Business Suite scheduling.

  python3 package_app_carousels.py review <out_dir>   # preview bundle for the clinician (no gate)
  python3 package_app_carousels.py post <out_dir>     # gated: only items that pass review.check()
  Add carousel ids after <out_dir> to package only those.

Each carousel goes in its own dated folder with the slides in order plus CAPTION.txt, ALT.txt, DM.txt and
SOURCES.txt; `post` also writes schedule.json.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import review  # noqa: E402
from content.app_carousels_all import APP_CAROUSELS  # noqa: E402

RENDERS = Path(__file__).parent / "out" / "app_carousels"


def write_item(c, dest):
    folder = dest / f"{c['date']}_{c['time'].replace(':', '')}_{c['id']}"
    folder.mkdir(parents=True, exist_ok=True)
    slides = sorted((RENDERS / c["id"]).glob("s*.png"))
    if not slides:
        sys.exit(f"{c['id']}: no renders — run app_carousels/render.mjs first")
    for i, png in enumerate(slides, 1):
        shutil.copy(png, folder / f"{i:02d}.png")
    (folder / "CAPTION.txt").write_text(c["caption"] + "\n")
    (folder / "ALT.txt").write_text(c["alt"] + "\n")
    (folder / "DM.txt").write_text(f"Keyword: {c['keyword']}\n\n{c['dm']}\n")
    (folder / "SOURCES.txt").write_text("\n".join(f"- {s}" for s in c["sources"]) + "\n")
    return folder, len(slides)


if __name__ == "__main__":
    mode, dest, only = sys.argv[1], Path(sys.argv[2]), set(sys.argv[3:])
    schedule = []
    for c in APP_CAROUSELS:
        if only and c["id"] not in only:
            continue
        if mode == "post":
            problems = review.check(c["id"])
            if problems:
                print(f"SKIP {c['id']}: {'; '.join(problems)}")
                continue
        folder, n = write_item(c, dest)
        schedule.append({"id": c["id"], "app": c["app"], "type": "carousel", "slides": n,
                         "publish_at": f"{c['date']}T{c['time']}:00-04:00", "folder": folder.name,
                         "keyword": c["keyword"]})
        print(f"{'OK  ' if mode == 'post' else 'PREV'} {folder.name} ({n} slides)")
    if mode == "post":
        if not schedule:
            sys.exit("nothing passed the review gate")
        (dest / "schedule.json").write_text(json.dumps(schedule, indent=2) + "\n")
