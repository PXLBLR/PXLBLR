"""Static 12-lead ECG panel (standard 3x4 layout + lead II rhythm strip) for teaching visuals.

Synthetic, teaching-grade morphology only. Never present a single monitor lead as a 12-lead diagnosis.
"""
import numpy as np
from PIL import Image, ImageDraw

from . import ecg
from .brand import CYAN, RED, font

PAPER = (252, 244, 240)
MINOR = (247, 205, 205)
MAJOR = (236, 150, 150)
INK = (20, 20, 24)
LAYOUT = [["I", "aVR", "V1", "V4"], ["II", "aVL", "V2", "V5"], ["III", "aVF", "V3", "V6"]]

# Anterior STEMI: ST elevation V2–V4 (+ I, aVL, V1, V5 mild), reciprocal ST depression III, aVF.
ANTERIOR_STEMI = {
    "I": {"r_amp": 0.7, "st": 0.15, "t_amp": 0.35}, "II": {"r_amp": 0.9, "t_amp": 0.25},
    "III": {"r_amp": 0.45, "st": -0.18, "t_amp": -0.12}, "aVR": {"r_amp": -0.75, "t_amp": -0.25, "p_amp": -0.12},
    "aVL": {"r_amp": 0.55, "st": 0.12, "t_amp": 0.3}, "aVF": {"r_amp": 0.6, "st": -0.15, "t_amp": -0.08},
    "V1": {"r_amp": -0.8, "st": 0.25, "t_amp": 0.35}, "V2": {"r_amp": -0.6, "st": 0.55, "t_amp": 0.7},
    "V3": {"r_amp": 0.5, "st": 0.6, "t_amp": 0.75}, "V4": {"r_amp": 0.9, "st": 0.5, "t_amp": 0.65},
    "V5": {"r_amp": 1.1, "st": 0.2, "t_amp": 0.4}, "V6": {"r_amp": 1.0, "t_amp": 0.3},
}


def render(pattern=ANTERIOR_STEMI, width=1000, height=470, hr=88, highlight=None, recip=None,
           title="12-LEAD  ·  TEACHING ILLUSTRATION"):
    """highlight / recip: lists of lead names outlined in red (ST elevation) / cyan (reciprocal depression)."""
    img = Image.new("RGBA", (width, height), PAPER + (255,))
    d = ImageDraw.Draw(img)
    rows = 3
    top = 34 if title else 8
    cell_w, cell_h = width / 4, (height - top - 8) / rows
    mm = cell_h / 30  # 1 mm in px (cell ≈ 30 mm tall)
    for x in np.arange(0, width, mm):
        d.line([(x, top), (x, height)], fill=MINOR, width=1)
    for y in np.arange(top, height, mm):
        d.line([(0, y), (width, y)], fill=MINOR, width=1)
    for x in np.arange(0, width, mm * 5):
        d.line([(x, top), (x, height)], fill=MAJOR, width=1)
    for y in np.arange(top, height, mm * 5):
        d.line([(0, y), (width, y)], fill=MAJOR, width=1)
    if title:
        d.rectangle((0, 0, width, top), fill=(30, 30, 36, 255))
        d.text((12, 6), title, font=font(22, "bold", "mono"), fill=(240, 240, 240))
    lab_f = font(22, "bold", "mono")
    for r, row in enumerate(LAYOUT):
        for c, lead in enumerate(row):
            x0, y0 = c * cell_w, top + r * cell_h
            kw = dict(hr=hr, seed=40 + r * 4 + c)
            kw.update(pattern.get(lead, {}))
            sig, _ = ecg.make("beats", 2.5, start=0.15, **kw)
            n = int(cell_w - 16)
            xs = np.linspace(0, sig.size - 1, n).astype(int)
            base = y0 + cell_h * 0.6
            gain = mm * 10  # 10 mm/mV
            pts = [(x0 + 8 + i, float(np.clip(base - sig[j] * gain, y0 + 4, y0 + cell_h - 4))) for i, j in enumerate(xs)]
            d.line(pts, fill=INK, width=2, joint="curve")
            d.text((x0 + 10, y0 + 6), lead, font=lab_f, fill=INK)
            if c:
                d.line([(x0, base - 8), (x0, base + 8)], fill=INK, width=2)
            for leads, col in ((highlight or [], RED), (recip or [], CYAN)):
                if lead in leads:
                    d.rounded_rectangle((x0 + 3, y0 + 3, x0 + cell_w - 3, y0 + cell_h - 3), radius=10,
                                        outline=col, width=5)
    d.rectangle((0, 0, width - 1, height - 1), outline=(40, 40, 48), width=3)
    return img
