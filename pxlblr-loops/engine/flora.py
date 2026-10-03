"""Procedural swaying plants (palms, tree ferns, ground ferns) on the art-pixel grid."""
import numpy as np
from PIL import Image, ImageDraw
from .px import W, H, INK, rgba, rim, outline, wave, _shift

PALM = dict(trunk=("#a8743c", "#8a5a2b"), trunk_shade="#6b4220", spine="#1f7a3a",
            leaf=("#3fbf5a", "#2a9548"), light="#8fe885", nuts=("#7a4a22", "#b07a42"))


def _frond(d, t, cx, cy, ang, ln, droop, k, phase, col, sway=5, period=4, leaflet=7, up_side=0.55):
    a0 = np.radians(ang + sway * wave(t, period, phase + k * 0.8))
    dr = droop + 0.08 * wave(t, period, phase + k * 0.8 + 1)
    dvec = np.array([np.cos(a0), np.sin(a0)])
    pts = [np.array([cx, cy]) + ln * (j / 23) * dvec + np.array([0, dr * ln * (j / 23) ** 2]) for j in range(24)]
    for j in range(1, 24):
        s = j / 23
        p, q = pts[j - 1], pts[j]
        tang = (q - p) / (np.linalg.norm(q - p) + 1e-6)
        nrm = np.array([-tang[1], tang[0]])
        if nrm[1] < 0:
            nrm = -nrm
        if 0.12 < s < 0.98 and j % 2 == 0:
            ll = 3 + leaflet * np.sin(np.pi * s) * 0.9
            for side, k2 in ((1, 1.0), (-1, up_side)):
                e = q + side * nrm * ll * k2 + tang * ll * 0.55 + np.array([0, ll * 0.35])
                d.line([tuple(q), tuple(e)], fill=rgba(col["leaf"][(j // 2) % 2]), width=1)
        d.line([tuple(p), tuple(q)], fill=rgba(col["spine"]), width=2)


def palm(t, base, ctrl, crown, fronds, phase=0.0, L=40, col=PALM, nuts=True, period=4):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    p0, p1, p2 = map(np.array, (base, ctrl, crown))
    n = 46
    for i in range(n):
        s = i / (n - 1)
        p = (1 - s) ** 2 * p0 + 2 * (1 - s) * s * p1 + s * s * p2
        r = 3.6 - 1.6 * s
        c = col["trunk"][int(s * 15) % 2]
        d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=rgba(c))
    a = np.array(im)
    m = a[..., 3] > 0
    a[m & ~_shift(m, 0, -2)] = rgba(col["trunk_shade"])
    im = Image.fromarray(a, "RGBA")
    d = ImageDraw.Draw(im)
    cx, cy = crown
    for k, (ang, ln, droop) in enumerate(fronds):
        _frond(d, t, cx, cy, ang, ln * L / 40, droop, k, phase, col, period=period)
    if nuts:
        for ox, oy in ((-3, 3), (2, 4), (-1, 6)):
            d.ellipse([cx + ox - 2, cy + oy - 2, cx + ox + 2, cy + oy + 2], fill=rgba(col["nuts"][0]))
            d.point((cx + ox - 1, cy + oy - 1), fill=rgba(col["nuts"][1]))
    skip = (INK, col["trunk_shade"]) + tuple(col["trunk"]) + tuple(col["nuts"])
    im = rim(im, col["light"], dy=1, skip=skip)
    return outline(im)


def fern(t, base, fronds, phase=0.0, col=PALM, light=None, period=4, leaflet=5):
    """Ground fern: fronds fanning up and out from one point."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for k, (ang, ln, droop) in enumerate(fronds):
        _frond(d, t, base[0], base[1], ang, ln, droop, k, phase, col, sway=4, period=period, leaflet=leaflet, up_side=0.8)
    im = rim(im, light or col["light"], dy=1, skip=(INK,))
    return outline(im)
