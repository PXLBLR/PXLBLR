"""Paths for the live 12-lead reel (same interface as ../heart_rhythms/reel.py, one reel)."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
IDS = ["L12_live"]


def load(rid=None):
    return {"id": "L12_live", "cfg": {"out": "aclsmed_live_12lead.mp4"},
            "script": json.loads((HERE / "script.json").read_text()),
            "vo": HERE / "public" / "vo", "audio": HERE / "public" / "audio.wav",
            "timeline": HERE / "src" / "timeline.json"}
