"""Paths and config for one reel of the series: `python3 <step>.py R02_pvt` (default R01_vfib).

rhythms/<id>/script.json   the narration (lines, cues, gaps)        rhythms/reels.json   visuals per reel
public/<id>/vo/            voice take + read-back (full.wav stays local: public repo)
public/<id>/audio.wav      the mix                                  src/data/<id>.*.json strips + timeline
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REELS = json.loads((HERE / "rhythms" / "reels.json").read_text())
IDS = [k for k in REELS if not k.startswith("_")]


def load(rid=None):
    rid = rid or (sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in REELS else "R01_vfib")
    script = json.loads((HERE / "rhythms" / rid / "script.json").read_text())
    return {"id": rid, "cfg": REELS[rid], "script": script,
            "vo": HERE / "public" / rid / "vo", "audio": HERE / "public" / rid / "audio.wav",
            "timeline": HERE / "src" / "data" / f"{rid}.timeline.json",
            "strips": HERE / "src" / "data" / f"{rid}.strips.json"}
