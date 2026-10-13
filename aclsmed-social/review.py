"""Clinical review gate (see CLINICAL_REVIEW.md).

  python3 review.py check <id>                     # exit 1 unless sourced + human-approved
  python3 review.py approve <id> "<Name, RN>"      # record a human clinician's sign-off
  python3 review.py status                         # list every gated item and its state
"""
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from content.app_carousels import APP_CAROUSELS  # noqa: E402
from content.published_fixes import CAROUSELS_PUB, REELS_PUB  # noqa: E402
from content.reels_fixes import FIXES  # noqa: E402
from content.sim_carousels import SIM1_V2  # noqa: E402

LOG = Path(__file__).parent / "review_log.json"


def load():
    return json.loads(LOG.read_text()) if LOG.exists() else {}


def specs():
    items = {s["id"]: s for s in (f() for f in FIXES + REELS_PUB)}
    items.update({c["id"]: c for c in CAROUSELS_PUB + [SIM1_V2] + APP_CAROUSELS})
    return items


def check(rid):
    s = specs().get(rid)
    problems = []
    if s is None:
        problems.append("unknown id")
    elif not s.get("sources"):
        problems.append("no sources listed")
    entry = load().get(rid)
    if not entry or entry.get("status") != "approved":
        problems.append("no human clinician sign-off in review_log.json")
    return problems


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "check":
        pr = check(sys.argv[2])
        print("PASS" if not pr else "BLOCKED: " + "; ".join(pr))
        sys.exit(1 if pr else 0)
    elif cmd == "approve":
        log = load()
        log[sys.argv[2]] = {"reviewer": sys.argv[3], "date": dt.date.today().isoformat(), "status": "approved"}
        LOG.write_text(json.dumps(log, indent=2) + "\n")
        print("approved", sys.argv[2])
    else:
        log = load()
        for rid, s in specs().items():
            e = log.get(rid, {})
            print(f"{rid:28} sources={len(s.get('sources', []))}  {e.get('status', 'PENDING human sign-off')}")
