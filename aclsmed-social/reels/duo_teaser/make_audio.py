"""Trailer sound bed for the iPhone Duo teaser (22 s). Synthesized; no licensed audio."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from engine import sfx  # noqa: E402

SR, DUR = sfx.SR, 22.0


def boom(d=1.6, f0=72, f1=30):
    t = np.arange(int(d * SR)) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 3)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.4)
    click = np.random.default_rng(1).normal(0, 1, t.size) * np.exp(-t * 90) * 0.35
    return 1.1 * (x + click)


def drone(d):
    t = np.arange(int(d * SR)) / SR
    x = sum(a * np.sin(2 * np.pi * 41.2 * m * t + m) for m, a in [(1, .6), (2, .25), (3, .12), (4.02, .05)])
    swell = np.clip(t / 6, 0, 1) * np.clip((d - t) / 2, 0, 1)
    return 0.16 * x * (0.7 + 0.3 * np.sin(2 * np.pi * 0.25 * t)) * swell


sfx.SOUNDS.update({"boom": boom, "boom_s": lambda: boom(1.0, 90, 40) * 0.6})
events = [
    (0.30, "heartbeat", 1.0), (1.30, "heartbeat", 1.0), (2.10, "heartbeat", 1.1),
    (2.50, "boom", 1.0), (2.50, "whoosh", 0.5),
    (4.60, "pop", 0.8), (4.60, "whoosh", 0.4),
    (5.60, "riser", 0.9),
    (7.00, "whoosh", 0.9), (7.00, "boom", 1.0),
    (7.90, "swipe", 0.8), (8.80, "boom_s", 1.0), (8.80, "ding", 0.25),
    (9.40, "beep", 0.6), (10.40, "beep", 0.6), (11.40, "beep", 0.6),
    (12.00, "boom_s", 0.9), (12.00, "charge", 0.8),
    (13.50, "boom_s", 0.9), (13.50, "whoosh", 0.5),
    (15.00, "boom_s", 0.9), (15.00, "whoosh", 0.5),
    (16.50, "riser", 0.7),
    (18.00, "boom", 1.0), (18.00, "whoosh_down", 0.6), (18.40, "ding", 0.5),
    (19.60, "heartbeat", 0.8),
]
out = sfx.mix(DUR, events, bed_level=0.8)
d = drone(DUR)
out = out + d[: out.size]
out = np.tanh(out / (np.abs(out).max() or 1) * 1.4) * 0.89
sfx.write_wav(Path(__file__).parent / "public" / "audio.wav", out)
print("wrote public/audio.wav")
