"""Package the Oct 8–25 reels for upload: dated files, captions, schedule.json, calendar and upload prompt.

  python3 package_oct8_25.py <out_dir>
"""
import datetime as dt
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from content.reels_oct8_25 import REELS2  # noqa: E402

ROOT = Path(__file__).parent
SRC = ROOT / "out" / "reels_oct8_25"
START = dt.date(2026, 10, 8)
SLOTS = ["07:30", "19:30"]

PROMPT = """# Prompt for Claude on your computer

Unzip this folder into **Downloads** so the path is `~/Downloads/aclsmed-oct8-25/`. Open the **Claude desktop app** with Claude in Chrome turned on, make sure Chrome is logged in to business.facebook.com as @aclsmed, and paste everything below the line.

---

Schedule 36 Instagram Reels for @aclsmed in Meta Business Suite (business.facebook.com → Planner → Create → Reel). Everything is in `~/Downloads/aclsmed-oct8-25/`.

Read `schedule.json` in that folder. It lists every reel in order with its video file, cover image, exact caption, and `scheduled_at` time (America/Toronto, EDT).

For each reel, in order:
1. Create → Reel → upload the `video` file.
2. Set the cover by uploading the `cover` PNG.
3. Paste the `caption` exactly as written (keep the line breaks and the 5 hashtags).
4. Publish to Instagram only → **Schedule** at `scheduled_at`.
5. Check that it appears in the Planner at the right date and time before moving on.

Rules:
- Don't publish anything immediately. Every reel must be **scheduled**.
- Don't edit captions, add hashtags, or add music.
- If the time zone shown isn't Toronto/Eastern, convert the times, and tell me you did.
- If anything fails (upload error, login prompt, missing option), stop and tell me. Don't guess.
- Business Suite schedules up to 29 days ahead. All of these fall within that window.
- When you're done, list all 36 scheduled reels with the date and time Business Suite shows.

Optional (only if I ask): also schedule each video as a YouTube Short in YouTube Studio, using `shorts_title` as the title and the caption as the description, at the same `scheduled_at`.
"""


def main(out: Path):
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    posts, rows = [], []
    for i, fn in enumerate(REELS2):
        spec = fn()
        day = START + dt.timedelta(days=i // 2)
        hhmm = SLOTS[i % 2]
        stem = f"{day.isoformat()}_{hhmm.replace(':', '')}_{spec['id']}"
        shutil.copy(SRC / f"{spec['id']}.mp4", out / f"{stem}.mp4")
        shutil.copy(SRC / f"{spec['id']}_cover.png", out / f"{stem}_cover.png")
        (out / f"{stem}_caption.txt").write_text(spec["caption"] + "\n")
        posts.append({"date": day.isoformat(), "time_et": hhmm, "scheduled_at": f"{day.isoformat()}T{hhmm}:00-04:00",
                      "type": "reel", "id": spec["id"], "video": f"{stem}.mp4", "cover": f"{stem}_cover.png",
                      "duration_s": round(spec["duration"], 1), "caption": spec["caption"],
                      "shorts_title": spec["shorts_title"]})
        rows.append((day, hhmm, spec))
    (out / "schedule.json").write_text(json.dumps(
        {"account": "@aclsmed", "timezone": "America/Toronto (EDT, UTC-4)", "posts": posts}, indent=2,
        ensure_ascii=False))
    (out / "CLAUDE_UPLOAD_PROMPT.md").write_text(PROMPT)

    cal = ["# ACLSMED Reels / Shorts: Oct 8–25, 2026 (2 per day)", "",
           "Faceless and voiceless, with SFX (monitor beeps synced to each QRS, alarms, defib charge→shock, whooshes, "
           "ticks, dings). 1080×1920, H.264/AAC, −16 LUFS, 30–37 s each. Every topic is new; none repeat the Oct 1–7 "
           "reels or carousels. Posting slots: **7:30 AM ET** and **7:30 PM ET**. 5 hashtags per caption "
           "(Instagram's cap).", "",
           "| Date | 7:30 AM ET | 7:30 PM ET |", "|---|---|---|"]
    for k in range(0, len(rows), 2):
        (d, _, a), (_, _, b) = rows[k], rows[k + 1]
        cal.append(f"| {d.strftime('%a %b %-d')} | {a['shorts_title'].replace(' #shorts', '')} | "
                   f"{b['shorts_title'].replace(' #shorts', '')} |")
    cal.append("")
    for d, hhmm, spec in rows:
        cal += [f"## {d.strftime('%a %b %-d')} · {hhmm} ET · `{spec['id']}.mp4` ({spec['duration']:.0f} s)", "",
                f"**YouTube Shorts title:** {spec['shorts_title']}", "", "**Caption**", "", spec["caption"], ""]
    text = "\n".join(cal)
    (out / "CALENDAR.md").write_text(text)
    (ROOT / "CALENDAR_OCT8_25.md").write_text(text)
    print(f"packaged {len(posts)} reels → {out}")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
