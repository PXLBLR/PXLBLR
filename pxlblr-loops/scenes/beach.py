"""NINJA-BLOKS · Beach Day — 60 s seamless loop.

Every motion has a period that divides 60 s, so frame 1800 == frame 0.
Wave swell 6 s · volleyball rally 4 s · palms 4 s · surfer 30 s · crab 12 s ·
gulls 20/30 s · boat + near clouds 60 s · far clouds 60 s (2x tiled strip).
"""
import numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw
from engine.px import (W, H, S, INK, TAU, rgba, hx, vgrad, radial_dither, bayer, sprite, outline, rim,
                       shade, up, flip, wave, cyc, Frame, DUR)
from engine.bloks import draw_blok, blok
from scenes.common import sign, draw_bug, shadow_ellipse, _pad
from engine.flora import palm

HZ = 92  # horizon row
SUN = (296, 26)
SAND = ["#ecc98a", "#f3d6a0", "#f8e2b6"]
SAND_SHADOW = "#d9b077"
WET = "#cfa36a"

rng = np.random.default_rng(7)


def shore_y(x):
    return 139 + 2.0 * np.sin(x / 23.0) + 1.2 * np.sin(x / 9.0 + 1.0)


# ---------------------------------------------------------------- sprites
def cloud_sprite(w, h, seed, far=False):
    r = np.random.default_rng(seed)
    im = Image.new("RGBA", (w + 4, h + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    n = max(3, w // 10)
    for i in range(n):
        cx = 2 + w * (0.12 + 0.76 * i / (n - 1)) + r.integers(-2, 3)
        rr = h * (0.3 + 0.45 * np.sin(np.pi * (i + 0.5) / n)) + r.integers(-1, 3)
        d.ellipse([cx - rr * 1.15, h + 1 - 2 * rr, cx + rr * 1.15, h + 1], fill=rgba("#ffffff"))
    d.rectangle([2 + w * 0.12, h - 3, 2 + w * 0.88, h + 1], fill=rgba("#ffffff"))
    base = "#d2e6fa" if far else "#ffffff"
    a = np.array(im)
    m = a[..., 3] > 0
    a[m] = rgba(base)
    yy = np.arange(a.shape[0])[:, None] * np.ones((1, a.shape[1]))
    th = bayer(*m.shape)
    if far:
        a[m & ((yy - 0.55 * h) / (0.45 * h) > th)] = rgba("#b8d6f4")
    else:
        a[m & ((yy - 0.5 * h) / (0.5 * h) > th)] = rgba("#e2eefb")
        a[m & ((yy - 0.75 * h) / (0.25 * h) > th)] = rgba("#c4daf2")
    return Image.fromarray(a, "RGBA")


GULL = {
    0: ["W.......W", ".W.....W.", "..WWKWW..", "....W....", "........."],
    1: [".........", "WWW...WWW", "...WKW...", "....W....", "........."],
    2: [".........", "....K....", "..WWWWW..", ".W.....W.", "W.......W"],
}


@lru_cache(maxsize=None)
def gull(f):
    return up(outline(_pad(sprite(GULL[f], {"W": "#f6f9ff", "K": "#ffb340"})), "#2d3a58"))


BOAT = [
    "..........R.........",
    "..........KR........",
    "..........K.........",
    ".........KWK........",
    "........KWWWK.......",
    ".......KWWOWWK......",
    "......KWWOOOWWK.....",
    ".....KWWWWWWWWWK....",
    "..........K.........",
    "..KKKKKKKKKKKKKKKK..",
    "..KRRRRRRRRRRRRRRK..",
    "...KWWWWWWWWWWWWK...",
    "....KKKKKKKKKKKK....",
]


@lru_cache(maxsize=None)
def boat_up():
    return up(_pad(sprite(BOAT, {"K": INK, "W": "#ffffff", "O": "#ff9a3c", "R": "#ec4a35"})))


BALL = [
    "..KKK..",
    ".K112K.",
    "K11223K",
    "K33W22K",
    "K33W11K",
    ".K311K.",
    "..KKK..",
]


@lru_cache(maxsize=None)
def ball(f):
    cols = ["#ec4a35", "#ffd23f", "#3a92f0"]
    c = cols[f:] + cols[:f]
    return sprite(BALL, {"K": INK, "W": "#ffffff", "1": "#ffffff", "2": c[0], "3": c[1]})


CRAB = {
    0: ["K.....K", "KK...KK", ".KRRRK.", "KRRRRRK", "KRERERK", ".KRRRK.", "K.K.K.K"],
    1: ["KK...KK", ".K...K.", ".KRRRK.", "KRRRRRK", "KRERERK", ".KRRRK.", ".K.K.K."],
}


@lru_cache(maxsize=None)
def crab(f):
    return sprite(CRAB[f], {"K": INK, "R": "#ff6a3d", "E": "#ffffff"})


COCO = [
    "....Y.",
    "...YYY",
    "....K.",
    ".KKKKK",
    "KBBBBK",
    "KBbBBK",
    ".KKKK.",
]


@lru_cache(maxsize=None)
def coconut():
    return sprite(COCO, {"K": INK, "B": "#8a5a2b", "b": "#f4eedf", "Y": "#ff70b0"})


@lru_cache(maxsize=None)
def board():
    rows = [
        "...KKKKKKKKKKKKKKKKKKKKKKKKKKKKK...",
        ".KKYYYYYYYYYYYYRRYYYYYYYYYYYYYYYKK.",
        "KYYYYYYYYYYYYYYRRYYYYYYYYYYYYYYYYYK",
        ".KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK.",
    ]
    return sprite(rows, {"K": INK, "Y": "#ffd23f", "R": "#ec4a35"})


@lru_cache(maxsize=None)
def umbrella():
    w, h = 58, 20
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    a = np.zeros((h, w, 4), np.uint8)
    cx, cy, rx, ry = 29, 17, 27, 14
    cols = ["#ec4a35", "#ffffff", "#ffd23f", "#ffffff"]
    for y in range(h):
        for x in range(w):
            dx, dy = (x - cx) / rx, (y - cy) / ry
            if dy <= 0.05 and dx * dx + dy * dy <= 1:
                ang = np.arctan2(-(y - cy) - 0.01, x - cx)
                k = int(ang / np.pi * 8) % 4
                a[y, x] = rgba(cols[k])
    # scalloped hem
    for x in range(2, w - 2):
        if (x // 4) % 2 == 0:
            a[cy + 1, x] = a[cy, x]
    im = Image.fromarray(a, "RGBA")
    im = rim(im, "#ffffff", dy=1)
    return outline(im)


@lru_cache(maxsize=None)
def castle(f):
    im = Image.new("RGBA", (36, 34), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s, sd, sl = "#e8c07c", "#c99a55", "#f8dca4"
    d.rectangle([3, 20, 32, 31], fill=rgba(s))
    for x0, top, wdt in ((3, 15, 7), (25, 15, 7), (13, 11, 10)):
        d.rectangle([x0, top, x0 + wdt - 1, 31], fill=rgba(s))
        for cx in range(x0, x0 + wdt, 2):
            d.point((cx, top - 1), fill=rgba(s))
        d.line([x0 + wdt - 1, top, x0 + wdt - 1, 31], fill=rgba(sd))
        d.line([x0, top, x0, 31], fill=rgba(sl))
    d.rectangle([16, 24, 19, 31], fill=rgba("#7a5228"))
    d.point((16, 24), fill=(0, 0, 0, 0)); d.point((19, 24), fill=(0, 0, 0, 0))
    d.line([17, 2, 17, 10], fill=rgba(INK))
    flag = [[(18, 2), (23, 2), (23, 5), (18, 5)], [(18, 3), (23, 2), (23, 5), (18, 6)]][f]
    d.polygon(flag, fill=rgba("#ec4a35"))
    d.point((20, 3 + f), fill=rgba("#ffd23f"))
    for x in range(4, 32, 3):
        d.point((x, 26 + (x % 2)), fill=rgba(sd))
    return outline(im)


@lru_cache(maxsize=None)
def bucket():
    rows = [
        "..KKK.......",
        ".K...K......",
        "KKKKKKKK....",
        "KYYYYYYK..KK",
        ".KYRYYK..KWK",
        ".KYYYYK.KWK.",
        "..KKKK.KWK..",
        ".......KK...",
    ]
    return sprite(rows, {"K": INK, "Y": "#3a92f0", "R": "#ffd23f", "W": "#ffd23f"})


@lru_cache(maxsize=None)
def surfboard_v():
    """Upright branded board stuck in the sand (red stripe + Blok emblem)."""
    rows = [
        "..KKK..",
        ".KWWWK.",
        "KWWWWWK",
        "KWRRRWK",
        "KWRSRWK",
        "KWRRRWK",
        "KWWWWWK",
        "KWWWWWK",
        "KRRRRRK",
        "KWWWWWK",
        "KWWWWWK",
        "KWWWWWK",
        "KWWWWWK",
        "KRRRRRK",
        "KWWWWWK",
        "KWWWWWK",
        "KWWWWWK",
        ".KWWWK.",
        ".KKKKK.",
    ]
    return sprite(rows, {"K": INK, "W": "#fff7e6", "R": "#ec4a35", "S": "#ffd23f"})


@lru_cache(maxsize=None)
def towel():
    im = Image.new("RGBA", (42, 11), (0, 0, 0, 0))
    a = np.zeros((11, 42, 4), np.uint8)
    for y in range(1, 10):
        off = (9 - y) // 2
        for x in range(1 + off, 34 + off):
            c = "#1ec8b4" if ((x - off) // 4) % 2 == 0 else "#ffffff"
            a[y, x] = rgba(c)
    im = Image.fromarray(a, "RGBA")
    return outline(im)


# ---------------------------------------------------------------- scene
class Beach:
    name = "beach"

    def __init__(self):
        self.base = up(Image.fromarray(self._static(), "RGB"))
        self.near = [(cloud_sprite(70, 20, 1), 30, 14), (cloud_sprite(54, 16, 2), 190, 34), (cloud_sprite(44, 14, 3), 330, 8)]
        self.far = [(cloud_sprite(30, 7, 4, far=True), 20, 52), (cloud_sprite(22, 6, 5, far=True), 130, 64)]
        self.near_up = [(up(c), x, y) for c, x, y in self.near]
        self.far_up = [(up(c), x, y) for c, x, y in self.far]
        # sparkles: concentrated in the sun's reflection, sparser elsewhere
        k = 90
        ys = rng.uniform(HZ + 2, 132, k)
        spread = 6 + (ys - HZ) * 0.5
        xs = np.where(np.arange(k) < 60, SUN[0] + rng.normal(0, 1, k) * spread, rng.uniform(0, W, k))
        self.sparkles = list(zip(xs.astype(int), ys.astype(int), rng.choice([1, 1.5, 2, 3], k), rng.uniform(0, TAU, k)))
        self.dash_rows = [(95, 3, 26, "#4c95d6"), (98, 4, 30, "#5aa6e0"), (102, 5, 34, "#69b8e6"), (106, 6, 38, "#7cc8ea"),
                          (111, 7, 44, "#8fd7ee"), (117, 9, 50, "#a6e4f0"), (123, 11, 58, "#c2eef3"), (129, 13, 66, "#dcf7f6")]

    def _static(self):
        img = np.zeros((H, W, 3), np.uint8)
        img[:HZ] = vgrad(["#2457c9", "#2e6fdb", "#3d88e8", "#57a3f1", "#7cbff6", "#a6d8fa", "#cdeefc"], W, HZ, ease=0.85)
        radial_dither(img[:HZ], SUN[0], SUN[1], 40, "#6fb0f0", 10)
        radial_dither(img[:HZ], SUN[0], SUN[1], 29, "#a2d2f7", 8)
        radial_dither(img[:HZ], SUN[0], SUN[1], 19, "#e2f4fe", 5)
        im = Image.fromarray(img)
        d = ImageDraw.Draw(im)
        d.ellipse([SUN[0] - 9, SUN[1] - 9, SUN[0] + 9, SUN[1] + 9], fill=hx("#fff1a8"))
        d.ellipse([SUN[0] - 7, SUN[1] - 7, SUN[0] + 7, SUN[1] + 7], fill=hx("#fffbe6"))
        # distant island + lighthouse
        hill = [(14, HZ)] + [(x, HZ - 9 * np.exp(-((x - 62) / 26) ** 2) - 5 * np.exp(-((x - 100) / 12) ** 2) - 1) for x in range(14, 130, 2)] + [(130, HZ)]
        d.polygon(hill, fill=hx("#5d93bf"))
        img = np.array(im)
        for x in range(14, 130):
            for y in range(HZ - 12, HZ):
                if tuple(img[y, x]) == hx("#5d93bf") and tuple(img[y - 1, x]) != hx("#5d93bf"):
                    img[y, x] = hx("#7fb0d6")
        im = Image.fromarray(img)
        d = ImageDraw.Draw(im)
        lx = 100
        d.rectangle([lx - 1, HZ - 15, lx + 1, HZ - 5], fill=hx("#eef3f7"))
        for yy in range(HZ - 13, HZ - 5, 4):
            d.rectangle([lx - 1, yy, lx + 1, yy + 1], fill=hx("#d9675c"))
        d.rectangle([lx - 1, HZ - 17, lx + 1, HZ - 16], fill=hx("#3a4a68"))
        d.point((lx, HZ - 18), fill=hx("#d9675c"))
        img = np.array(im)
        # ocean
        img[HZ:150] = vgrad(["#1d4f9e", "#2262b6", "#2a7ccc", "#3197d8", "#3cb3dc", "#52cdd9"], W, 150 - HZ, ease=0.8)
        img[HZ] = hx("#9fd2f2")
        # sand
        yy = np.arange(H)[:, None]
        sand = vgrad(SAND, W, H - 130)
        sy = shore_y(np.arange(W))[None, :]
        mask = (yy >= sy) & (yy >= 130)
        full = np.zeros_like(img)
        full[130:] = sand
        img[mask] = full[mask]
        # texture: speckles, shells, footprints
        r = np.random.default_rng(11)
        for _ in range(900):
            x, y = r.integers(0, W), r.integers(150, H)
            img[y, x] = hx(r.choice(["#e0b676", "#fff1d2", "#dcae6c"]))
        for (x, y) in [(118, 202), (250, 207), (342, 186), (175, 210)]:
            img[y, x:x + 2] = hx("#ffffff"); img[y + 1, x:x + 3] = hx("#f6b3c8")
        for i in range(9):
            x, y = 236 + i * 9, 214 - i * 4 + (i % 2) * 2
            if y > 150:
                img[y:y + 2, x:x + 3] = hx("#dcb074")
        # star fish
        sx, sy0 = 262, 196
        for dx, dy in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1), (-2, -1), (2, -1), (-1, 2), (1, 2)):
            img[sy0 + dy, sx + dx] = hx("#ff8a5a")
        # palm shadows
        for (cx, cy, rx) in ((50, 205, 24), (330, 208, 22)):
            m2 = ((np.arange(W)[None, :] - cx) / rx) ** 2 + ((yy - cy) / 4.5) ** 2 < 1
            img[m2 & mask] = hx(SAND_SHADOW)
        return img

    # ------------------------------------------------------------ per frame
    def frame(self, t):
        t = t % DUR
        f = Frame(self.base)
        d = f.draw()
        # sun rays: 8 rays rotating 1 step per 1.5 s, pulsing on a 3 s cycle
        rot = int(cyc(t, 12) * 8) / 8 * (np.pi / 4)
        r0 = 12 + (1 if wave(t, 3) > 0 else 0)
        for k in range(8):
            a = rot + k * np.pi / 4
            for rr in range(r0, r0 + (3 if k % 2 == 0 else 2)):
                d.point((SUN[0] + round(np.cos(a) * rr), SUN[1] + round(np.sin(a) * rr)), fill=rgba("#fff6c4"))
        # lighthouse lamp (3 s blink)
        if cyc(t, 3) < 0.4:
            d.line([99, HZ - 17, 101, HZ - 17], fill=rgba("#fff36b"))
            for k in (1, 2, 3):
                d.point((98 - k, HZ - 17), fill=rgba("#fff9c8")); d.point((102 + k, HZ - 17), fill=rgba("#fff9c8"))
        f.flush()
        # far clouds: 224 px strip tiled twice, drifts one strip per minute
        for c, x0, y in self.far_up:
            for rep in range(3):
                x = ((x0 - 224 * t / DUR) % 224) + 224 * rep - 40
                f.smooth(c, x, y)
        for c, x0, y in self.near_up:
            x = ((x0 - 448 * t / DUR) % 448) - 64
            f.smooth(c, x, y + 0.6 * wave(t, 10, x0))
        # gulls
        for span_t, y0, direction, ph in ((20, 40, 1, 0.0), (30, 58, -1, 0.4)):
            x = (cyc(t, span_t, ph) * 448) - 40
            if direction < 0:
                x = W - x
            g = gull(int(cyc(t, 0.6) * 3))
            f.smooth(g if direction > 0 else flip(g), x, y0 + 3 * wave(t, 5, ph * 7))
        # ocean: drifting wave dashes
        d = f.draw()
        for i, (yr, ln, per, col) in enumerate(self.dash_rows):
            off = 7 * wave(t, (6, 5, 4, 6, 5, 4, 6, 3)[i], i * 1.3) + i * 11
            xs = np.arange(W)
            on = ((xs + off) % per) < ln
            for x in xs[on]:
                d.point((int(x), yr), fill=rgba(col))
                if i >= 4 and ((x + off) % per) < 2:
                    d.point((int(x), yr - 1), fill=rgba("#ffffff"))
        for (x, y, p, ph) in self.sparkles:
            v = wave(t, p, ph)
            if v > 0.55:
                d.point((x, y), fill=rgba("#ffffff"))
                if v > 0.92 and y > 100:
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        d.point((x + dx, y + dy), fill=rgba("#fff6b0"))
        f.flush()
        # sailboat crossing the horizon once per minute
        f.smooth(boat_up(), 430 - cyc(t, 60) * 500, HZ - 13 + 0.5 * wave(t, 3))
        # surfer: black Blok rides back and forth on a 30 s cycle
        sx = 236 + 58 * wave(t, 30)
        vel = np.cos(TAU * t / 30)
        sy = 93 + round(1.2 * wave(t, 3))
        fl = vel < 0
        d = f.draw()
        bx = sx - 4
        for i in range(10):
            wx = bx + (35 + i * 2 if not fl else -i * 2 - 2)
            if (i + int(t * 6)) % 3:
                d.point((int(wx), int(sy + 31 - (i % 3 == 0))), fill=rgba("#ffffff"))
        f.put(flip(board()) if fl else board(), bx, sy + 28)
        draw_blok(f, "black", sx, sy, t, eyes=1, flipx=fl, blink_phase=0.3, wind=1.5)
        # shoreline: swell every 6 s rolling along the beach
        self._shore(f, t)
        # back-row props
        f.put(sign(), 34, 140)
        cpx = 120 + 34 * wave(t, 12)
        f.put(crab(int(cyc(t, 0.4) * 2)), cpx, shore_y(cpx) + 14)
        f.put(castle(int(cyc(t, 1) * 2)), 84, 158)
        f.put(bucket(), 118, 183)
        f.put(surfboard_v(), 268, 160)
        # volleyball rally: red hits at t%4==0, blue at t%4==2
        self._rally(f, t)
        # lounge: umbrella, towel, pink Blok vibing in shades
        shadow_ellipse(f, 330, 200, 26, 4, SAND_SHADOW)
        f.put(towel(), 280, 190)
        bob = 1 if cyc(t, 1) < 0.5 else 0
        draw_blok(f, "pink", 288, 167 + bob, t, eyes="shades", blink_phase=0.6, wind=1.2)
        f.put(coconut(), 316, 191)
        d = f.draw()
        d.line([329, 150, 329, 199], fill=rgba("#e9e6ef"), width=1)
        d.line([330, 150, 330, 199], fill=rgba("#a9a6b8"), width=1)
        f.put(umbrella(), 301, 133)
        # foreground palms
        f.put(palm(t, (8, 222), (14, 140), (46, 62), [(185, 40, 0.55), (205, 38, 0.6), (235, 30, 0.7), (265, 24, 0.5),
                                                        (300, 30, 0.7), (330, 38, 0.6), (355, 42, 0.5)]), 0, 0)
        f.put(palm(t, (378, 222), (372, 150), (342, 70), [(180, 40, 0.5), (210, 36, 0.6), (240, 28, 0.6), (275, 24, 0.5),
                                                           (305, 30, 0.7), (335, 38, 0.6), (0, 40, 0.55)], phase=1.3, L=36), 0, 0)
        draw_bug(f)
        return f.out()

    def _shore(self, f, t):
        y0, y1 = 126, 156
        hh = y1 - y0
        a = np.zeros((hh, W, 4), np.uint8)
        xs = np.arange(W)
        s = shore_y(xs)
        swell = 3.2 + 3.4 * np.sin(TAU * t / 6 - xs / 70.0)
        edge = s + swell
        yy = np.arange(y0, y1)[:, None]
        th = bayer(hh, W)
        shallow = (yy >= s[None, :] - 9) & (yy < edge[None, :])
        depth = np.clip((edge[None, :] - yy) / 9.0, 0, 1)
        a[shallow] = rgba("#52cdd9")
        a[shallow & (depth < 0.66)] = rgba("#74dcd9")
        a[shallow & (depth < 0.33) & (th > 0.5)] = rgba("#9de6d6")
        wet = (yy >= edge[None, :]) & (yy < s[None, :] + 10) & (yy >= s[None, :] - 1)
        wetk = np.clip(1 - (yy - edge[None, :]) / np.maximum(s[None, :] + 10 - edge[None, :], 1), 0, 1)
        a[wet & (wetk > th * 0.9)] = rgba(WET)
        a[wet & (wetk <= th * 0.9)] = rgba("#e1b97f")
        foam = (yy >= edge[None, :] - 1.5) & (yy < edge[None, :] + 0.5)
        breakup = (np.sin(xs / 3.0 + TAU * t / 2) + np.sin(xs / 7.0 - TAU * t / 3)) > -1.2
        a[foam & breakup[None, :]] = rgba("#ffffff")
        foam2 = (yy >= edge[None, :] - 4.5) & (yy < edge[None, :] - 3.5) & ((np.sin(xs / 2.2 + TAU * t / 1.5) > 0.2)[None, :])
        a[foam2] = rgba("#e6fbfb")
        f.arr(a, 0, y0)

    def _rally(self, f, t):
        rx, bx, fy = 138, 228, 163
        ph = cyc(t, 4)
        # distance (s) to each Blok's hit time
        dr = min(ph, 1 - ph) * 4
        db = abs(ph - 0.5) * 4
        jr = 9 * max(0.0, 1 - (dr / 0.3) ** 2) if dr < 0.3 else 0
        jb = 9 * max(0.0, 1 - (db / 0.3) ** 2) if db < 0.3 else 0
        p = (ph * 2) % 1.0
        x0, x1 = (rx + 11, bx + 10) if ph < 0.5 else (bx + 10, rx + 11)
        bxp = x0 + (x1 - x0) * p
        byp = 152 - 4 * 52 * p * (1 - p)
        # shadows
        shadow_ellipse(f, rx + 14, 193, 11 - jr * 0.4, 2, SAND_SHADOW)
        shadow_ellipse(f, bx + 13, 193, 11 - jb * 0.4, 2, SAND_SHADOW)
        sh = max(1, 4 - (152 - byp) / 18)
        shadow_ellipse(f, bxp + 3, 196, sh, 1, SAND_SHADOW)
        # net (drawn between the players)
        d = f.draw()
        fx, bkx = 190, 204
        top_f, top_b, bot_f, bot_b = 152, 145, 168, 161
        for i in range(7):
            u = i / 6
            x = fx + (bkx - fx) * u
            d.line([x, top_f + (top_b - top_f) * u, x, bot_f + (bot_b - bot_f) * u], fill=rgba("#e9e4d8"))
        for v in range(0, 5):
            vv = v / 4
            d.line([fx, top_f + (bot_f - top_f) * vv, bkx, top_b + (bot_b - top_b) * vv], fill=rgba("#e9e4d8"))
        d.line([bkx, top_b - 2, bkx, 186], fill=rgba("#8a5a2b"), width=2)
        d.line([fx, top_f, bkx, top_b], fill=rgba("#ffffff"))
        d.line([fx, top_f - 2, fx, 195], fill=rgba("#b07a42"), width=2)
        d.line([fx, top_f - 3, fx + 1, top_f - 3], fill=rgba("#ec4a35")); d.line([bkx, top_b - 3, bkx + 1, top_b - 3], fill=rgba("#ec4a35"))
        look_r = 1
        draw_blok(f, "red", rx, fy - jr, t, eyes=look_r, mouth="open" if jr > 3 else "smile",
                  arms="up" if jr > 3 else "down", blink_phase=0.17)
        draw_blok(f, "blue", bx, fy - jb, t, eyes=1, flipx=True, mouth="open" if jb > 3 else "smile",
                  arms="up" if jb > 3 else "down", blink_phase=0.45)
        f.put(ball(int(cyc(t, 0.5) * 3)), bxp, byp)

    # ------------------------------------------------------------ audio
    def audio(self):
        """Surf synced to the on-screen swell (left/right channels follow the wave rolling along the
        beach), wind, palm rustle on the 4 s sway, gull calls as each gull crosses, volleyball poks."""
        from engine import audio as A
        T = A.T
        buf = np.zeros((2, A.N))
        for ch, x, sd in ((0, 70, 1), (1, 314, 2)):
            ph = TAU * T / 6 - x / 70.0
            e = (np.sin(ph) + 1) / 2
            retreat = np.clip(-np.cos(ph), 0, 1) ** 1.5
            low = A.colored(1.0, 60, 500, seed=sd) * (0.3 + 0.7 * e ** 1.5) * 0.35
            wash = A.colored(0.35, 150, 6000, seed=sd + 10) * (0.12 + 0.88 * e ** 2) * 0.55
            hiss = A.colored(0.0, 2500, 11000, seed=sd + 20) * retreat * 0.22
            far = A.colored(0.8, 80, 1200, seed=sd + 30) * 0.12
            wind = A.colored(1.0, 150, 1800, seed=sd + 40) * (0.6 + 0.4 * np.sin(TAU * T / 15 + ch)) * 0.06
            rustle = A.colored(0.0, 3500, 10000, seed=sd + 50) * np.clip(np.sin(TAU * T / 4 + ch * 1.3), 0, 1) * 0.03
            buf[ch] += low + wash + hiss + far + wind + rustle
        # gulls: call as they pass mid-screen (20 s and 30 s crossings)
        for i, t0 in enumerate((9.8, 29.9, 49.7)):
            A.place(buf, A.gull(i), t0, 0.9, pan=-0.1 + 0.3 * (i % 2))
        for i, t0 in enumerate((3.4, 33.6)):
            A.place(buf, A.gull(10 + i), t0, 0.6, pan=0.3)
        # volleyball: red hits on even 4 s marks, blue 2 s later
        for k in range(30):
            A.place(buf, A.pok(k), 2.0 * k, 0.6, pan=-0.3 if k % 2 == 0 else 0.3)
        return A.master(buf)
