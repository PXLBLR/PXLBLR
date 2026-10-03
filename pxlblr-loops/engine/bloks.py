"""NINJA-BLOKS: the PXLBLR cast.

One master sprite generator, recoloured per Blok, so every scene uses exactly
the same character design: rounded block body, top-left key light, ninja
headband with a gold shuriken emblem, twin katana hilts, big eyes with
catch-lights, blush, nub arms and feet. 28x28 art pixels (140x140 on screen).
"""
import numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw
from .px import sprite, rgba, hx, INK, flip, outline, _shift, wave

BLOKS = {
    #          light        body        shade       band        band shade  blush
    "red":   dict(L="#ff8f70", B="#ec4a35", b="#b42d27", H="#2b2740", h="#17142a", P="#ffb0a0"),
    "blue":  dict(L="#86d4ff", B="#3a92f0", b="#2161c0", H="#8a3ff0", h="#5822a6", P="#ff9fc4"),
    "black": dict(L="#5c5f82", B="#383a52", b="#22233a", H="#ec4a35", h="#a92a24", P="#ff8fa8"),
    "pink":  dict(L="#ffbcdc", B="#ff74b3", b="#d64489", H="#1ec8b4", h="#118a7c", P="#ff3f8a"),
}
GOLD, GOLD_D = "#ffd23f", "#d79a1c"
BW, BH = 28, 29
TOP = 2  # extra rows above the body for the katana hilt
KNOT = (24, 9 + TOP)  # headband knot (right side), tails attach here


@lru_cache(maxsize=None)
def blok(name, eyes=1, mouth="smile", arms="down"):
    c = BLOKS[name]
    im = Image.new("RGBA", (BW, BH), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # arms
    ay = (8, 11) if arms == "up" else (16, 19)
    for ax in (1, 24):
        d.rectangle([ax, ay[0], ax + 1, ay[1]], fill=rgba(c["B"]))
        d.point((ax + (0 if ax == 1 else 1), ay[0]), fill=rgba(c["L"]))
    # feet
    for fx in (6, 17):
        d.rectangle([fx, 24, fx + 3, 26], fill=rgba(c["b"]))
    # body with rounded corners + key light from top-left
    body = Image.new("RGBA", (BW, BH), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)
    bd.rounded_rectangle([3, 4, 23, 24], radius=3, fill=rgba(c["B"]))
    a = np.array(body)
    m = a[..., 3] > 0
    a[m & ~_shift(m, 0, -2)] = rgba(c["b"])                       # right side shade
    a[m & ~_shift(m, -3, 0)] = rgba(c["b"])                       # bottom shade
    a[m & ~_shift(m, 1, 0)] = rgba(c["L"])                        # top light
    a[m & ~_shift(m, 0, 1) & _shift(m, -3, 0)] = rgba(c["L"])  # left light
    body = Image.fromarray(a, "RGBA")
    im.paste(body, (0, 0), body)
    d = ImageDraw.Draw(im)
    # headband + shuriken emblem
    d.rectangle([3, 7, 24, 10], fill=rgba(c["H"]))
    d.line([3, 11, 24, 11], fill=rgba(c["h"]))
    d.line([4, 7, 22, 7], fill=rgba(_mix(c["H"], "#ffffff", 0.25)))
    for (dx, dy) in ((0, -2), (-1, -1), (0, -1), (1, -1), (-2, 0), (-1, 0), (1, 0), (2, 0), (-1, 1), (0, 1), (1, 1), (0, 2)):
        d.point((13 + dx, 9 + dy), fill=rgba(GOLD))
    d.point((13, 9), fill=rgba(c["h"]))
    d.point((12, 8), fill=rgba("#fff6c4"))
    d.rectangle([24, 8, 25, 10], fill=rgba(c["H"]))  # knot
    # eyes
    for ex in (6, 17):
        _eye(d, ex, 13, eyes, c)
    if eyes == "shades":
        d.line([5, 13, 22, 13], fill=rgba(INK))
        for ex in (5, 16):
            d.rectangle([ex, 13, ex + 5, 16], fill=rgba("#26243c"))
            d.point((ex + 1, 14), fill=rgba("#9ff0ff")); d.point((ex + 2, 14), fill=rgba("#9ff0ff"))
            d.point((ex + 1, 15), fill=rgba("#5fb6d6"))
        d.line([11, 14, 15, 14], fill=rgba(INK))
    # blush
    for bx in (5, 20):
        d.line([bx, 18, bx + 1, 18], fill=rgba(c["P"]))
    # mouth
    if mouth == "open":
        d.rectangle([11, 19, 15, 21], fill=rgba(INK))
        d.line([12, 21, 14, 21], fill=rgba("#ff6b81"))
    elif mouth == "o":
        d.rectangle([12, 19, 14, 21], fill=rgba(INK))
    else:
        d.point((11, 19), fill=rgba(INK)); d.point((15, 19), fill=rgba(INK))
        d.line([12, 20, 14, 20], fill=rgba(INK))
    im = outline(im)
    # katana over the right shoulder, drawn behind the body
    full = Image.new("RGBA", (BW, BH + TOP), (0, 0, 0, 0))
    hd = ImageDraw.Draw(full)
    for i in range(6):
        y = 6 - i
        col = "#d9dbe6" if i % 2 else "#3b3355"
        hd.point((18 + i, y), fill=rgba(col)); hd.point((19 + i, y), fill=rgba("#3b3355" if i % 2 else "#d9dbe6"))
    hd.point((24, 1), fill=rgba(GOLD)); hd.point((25, 1), fill=rgba(GOLD_D))
    for (gx, gy) in ((16, 5), (17, 6), (18, 7), (19, 8)):
        hd.point((gx + 1, gy - 1), fill=rgba(GOLD))
    full = outline(full)
    full.paste(im, (0, TOP), im)
    return full


def _eye(d, x, y, look, c):
    if look == "shades":
        return
    if look == "blink":
        d.line([x, y + 3, x + 3, y + 3], fill=rgba(INK))
        return
    if look == "happy":
        d.point((x, y + 3), fill=rgba(INK)); d.point((x + 3, y + 3), fill=rgba(INK))
        d.line([x + 1, y + 2, x + 2, y + 2], fill=rgba(INK))
        return
    d.rectangle([x, y + 1, x + 3, y + 3], fill=rgba("#ffffff"))
    d.line([x + 1, y, x + 2, y], fill=rgba("#ffffff"))
    d.line([x + 1, y + 4, x + 2, y + 4], fill=rgba("#ffffff"))
    px = {1: x + 2, 0: x + 1, -1: x}[look]
    d.rectangle([px, y + 1, px + 1, y + 3], fill=rgba(INK))
    d.point((px, y + 1), fill=rgba("#ffffff"))


def _mix(a, b, k):
    A, B = np.array(hx(a)), np.array(hx(b))
    return "#%02x%02x%02x" % tuple((A * (1 - k) + B * k).astype(int))


def tails(frame, name, x, y, t, flip_dir=False, wind=1.0):
    """Two headband tails fluttering from the knot (1 s flutter cycle)."""
    c = BLOKS[name]
    d = frame.draw()
    sgn = -1 if flip_dir else 1
    kx = x + (BW - 1 - KNOT[0] - 1 if flip_dir else KNOT[0] + 1)
    ky = y + KNOT[1]
    for k, (ln, ph, col) in enumerate(((7, 0.0, c["H"]), (5, 1.9, c["h"]))):
        pts = []
        for i in range(ln + 1):
            f = i / ln
            yy = ky + k * 2 + i * (0.15 + 0.25 * k) + wind * 1.3 * f * np.sin(2 * np.pi * t / 1.0 + ph - i * 0.9)
            pts.append((kx + sgn * (i + 1), int(round(yy))))
        for p in pts:
            d.point((p[0], p[1] - 1), fill=rgba(INK))
            d.point((p[0], p[1] + 1), fill=rgba(INK))
        d.point((pts[-1][0] + sgn, pts[-1][1]), fill=rgba(INK))
        for p in pts:
            d.point(p, fill=rgba(col))


def draw_blok(frame, name, x, y, t, eyes=1, flipx=False, mouth="smile", arms="down", tail=True, wind=1.0, blink_phase=0.0):
    """Blinks once every 5 s (staggered per Blok via blink_phase)."""
    if eyes not in ("shades", "happy") and ((t / 5.0 + blink_phase) % 1.0) < 0.035:
        eyes = "blink"
    spr = blok(name, eyes, mouth, arms)
    if flipx:
        spr = flip(spr)
    if tail:
        tails(frame, name, x, y, t, flip_dir=flipx, wind=wind)
    frame.put(spr, x, y)


@lru_cache(maxsize=None)
def blok_icon():
    """9x9 brand mark: a tiny Blok face with headband + emblem (corner bug)."""
    rows = [
        ".BBBBBBB.",
        "HHHHSHHHH",
        "hhhhhhhhh",
        "BWEBBBWEB",
        "BWEBBBWEB",
        "BBBBBBBBB",
        "BBBKKKBBB",
        "bbbbbbbbb",
        ".bbbbbbb.",
    ]
    c = BLOKS["red"]
    return sprite(rows, dict(c, K=INK, S=GOLD, W="#ffffff", E=INK))


def draw_scarf(frame, x, y, t, flipx=False, col="#ec4a35", stripe="#ffffff"):
    """Winter scarf wrapped under the mouth, one end hanging and swaying (2 s)."""
    d = frame.draw()
    x, y = int(round(x)), int(round(y))
    y0 = y + TOP + 21
    d.rectangle([x + 3, y0, x + 23, y0 + 2], fill=rgba(col))
    for sx in range(x + 5, x + 23, 4):
        d.line([sx, y0, sx, y0 + 2], fill=rgba(stripe))
    d.line([x + 3, y0 - 1, x + 23, y0 - 1], fill=rgba(INK))
    d.line([x + 3, y0 + 3, x + 23, y0 + 3], fill=rgba(INK))
    ex = x + 6 if not flipx else x + 18
    sw = round(wave(t, 2, x * 0.1))
    for i in range(7):
        d.line([ex + sw * (i > 3), y0 + 3 + i, ex + 2 + sw * (i > 3), y0 + 3 + i], fill=rgba(stripe if i % 3 == 2 else col))
        d.point((ex - 1 + sw * (i > 3), y0 + 3 + i), fill=rgba(INK))
        d.point((ex + 3 + sw * (i > 3), y0 + 3 + i), fill=rgba(INK))
    d.line([ex + sw, y0 + 10, ex + 2 + sw, y0 + 10], fill=rgba(INK))
