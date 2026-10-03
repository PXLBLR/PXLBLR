"""NINJA-BLOKS · Autumn Lake at Dawn — 60 s seamless loop.

Periods (all divide 60 s): canoe drift 60 s · paddle stroke 3 s · bobber 2 s · reflection
ripple 3 s · mist 20/30 s · loon dive 20 s · ducks 30 s · rake 2 s · steam 3 s · leaves
6-12 s. Events: loon calls 2 s + 31 s, deer at the shore 18-39 s, leaf-pile jump 44-49.5 s.
"""
import numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw
from engine.px import (W, H, S, INK, TAU, DUR, rgba, hx, vgrad, radial_dither, bayer, sprite, outline, rim,
                       up, flip, wave, cyc, Frame, _shift)
from engine.bloks import draw_blok
from scenes.common import sign, draw_bug, shadow_ellipse, _pad

WL = 118                       # waterline
SUN = (198, 101)
LOON_T = (2.0, 31.0)
DEER_T = (18.0, 39.0)
JUMP_T = 44.0
AUTUMN = ["#e0743a", "#c8443a", "#f2b84e", "#d8902e", "#b8562e"]

rng = np.random.default_rng(21)


def shore(x):
    return 177 + 3 * np.sin(x / 31.0) + 1.5 * np.sin(x / 9.0)


# ---------------------------------------------------------------- sprites
def reflect(img, col="#2e3658", k=0.0):
    """Mirror a sprite for the lake: flipped, tinted, checker-dithered so it reads as translucent."""
    a = np.array(img.transpose(Image.FLIP_TOP_BOTTOM))
    m = a[..., 3] > 0
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    a[m] = rgba(col)
    a[m & ((xx + yy) % 2 == 1)] = 0
    return Image.fromarray(a, "RGBA")


@lru_cache(maxsize=None)
def canoe():
    w, h = 78, 12
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(1, 2), (6, 4), (w - 7, 4), (w - 2, 2), (w - 6, 9), (6, 9)], fill=rgba("#c8443a"))
    d.line([(1, 2), (6, 4), (w - 7, 4), (w - 2, 2)], fill=rgba("#f0b070"))
    d.line([6, 9, w - 6, 9], fill=rgba("#8a2a2a"))
    d.line([8, 8, w - 8, 8], fill=rgba("#a8343a"))
    d.rectangle([34, 5, 38, 7], fill=rgba("#ffd23f"))  # brand stripe
    return outline(im)


@lru_cache(maxsize=None)
def loon(f):
    rows = [
        ".....KKK..",
        "....KKRKK.",
        "....KKKKKK",
        "....KWKWK.",
        ".KKKKKKKK.",
        "KWKWKWKWKK",
        ".KKKKKKKK.",
    ]
    if f == 1:
        rows = ["..........", "..........", ".....KKK..", "....KKRKKK", ".KKKKWKWK.", "KWKWKWKWKK", ".KKKKKKKK."]
    return sprite(rows, {"K": "#1e2030", "W": "#e8eef4", "R": "#ff4a3a"})


@lru_cache(maxsize=None)
def duck(f):
    rows = [["K.....", ".K...K", "..KKKG", ".KK..."], ["......", "..KKKG", ".KKK..", "K....."]][f]
    return up(sprite(rows, {"K": "#3a2e3a", "G": "#e8a040"}))


DEER = {
    "stand": ["..............a..a..", "..............aaaa..", "...............BBB..", "..............BBEBBB",
              "..............BBBBBN", ".............BBB....", "..W.........BBB.....", ".WBBBBBBBBBBBBB.....",
              ".BBBBBBBBBBBBBB.....", ".BBBBBBBBBBBBB......", "..CCCCCCCCCCC.......", "..B.B.....B.B.......",
              "..B.B.....B.B.......", "..B.B.....B.B.......", "..K.K.....K.K......."],
    "walk": ["..............a..a..", "..............aaaa..", "...............BBB..", "..............BBEBBB",
             "..............BBBBBN", ".............BBB....", "..W.........BBB.....", ".WBBBBBBBBBBBBB.....",
             ".BBBBBBBBBBBBBB.....", ".BBBBBBBBBBBBB......", "..CCCCCCCCCCC.......", "..B..B....B..B......",
             ".B...B...B...B......", ".B....B..B....B.....", ".K....K..K....K....."],
    "drink": ["....................", "....................", "....................", "....................",
              "....................", "....................", "..W.................", ".WBBBBBBBBBBBBB.....",
              ".BBBBBBBBBBBBBBB....", ".BBBBBBBBBBBBBBBB...", "..CCCCCCCCCCC.aBBB..", "..B.B.....B.B.aBBBB.",
              "..B.B.....B.B..BEBBN", "..B.B.....B.B...BB..", "..K.K.....K.K......."],
}


@lru_cache(maxsize=None)
def deer(pose, step=0):
    rows = DEER["walk" if (pose == "walk" and step) else ("stand" if pose == "walk" else pose)]
    im = _pad(sprite(rows, {"B": "#a8703a", "C": "#e8c89a", "a": "#6a4026", "E": INK, "N": INK, "W": "#ffffff", "K": "#4a2e1e"}))
    im = rim(im, "#ffd09a", dy=1, skip=(INK, "#ffffff", "#6a4026"))
    return outline(im)


@lru_cache(maxsize=None)
def mug():
    rows = ["KKKKK.", "KRRRKK", "KRWRK.K", "KRRRKK", ".KKK.."]
    rows = [r.ljust(7, ".") for r in rows]
    return sprite(rows, {"K": INK, "R": "#ec4a35", "W": "#ffd23f"})


@lru_cache(maxsize=None)
def leafpile():
    w, h = 54, 20
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([1, 3, w - 2, h + 12], fill=rgba("#c8602e"))
    a = np.array(im)
    m = a[..., 3] > 0
    r = np.random.default_rng(5)
    ys, xs = np.nonzero(m)
    for y, x in zip(ys, xs):
        if r.random() < 0.55:
            a[y, x] = rgba(r.choice(AUTUMN + ["#8a4a26"]))
    im = Image.fromarray(a, "RGBA")
    im = rim(im, "#ffd09a", dy=1)
    return outline(im)


@lru_cache(maxsize=None)
def cloud(w, h, seed):
    r = np.random.default_rng(seed)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i in range(5):
        cx = w * (0.15 + 0.7 * i / 4) + r.integers(-3, 4)
        d.ellipse([cx - w * 0.2, h * 0.25 + r.integers(-1, 2), cx + w * 0.2, h - 1], fill=rgba("#f2b6b4"))
    a = np.array(im)
    m = a[..., 3] > 0
    a[m & ~_shift(m, -2, 0)] = rgba("#ffd8a8")
    a[m & ~_shift(m, 1, 0)] = rgba("#f8cccc")
    return up(Image.fromarray(a, "RGBA"))


# ---------------------------------------------------------------- scene
class Lake:
    name = "lake"

    def __init__(self):
        upper = self._upper()
        self.upper = upper
        src = upper[WL - 72:WL][::-1].astype(float)
        tint = np.array(hx("#33416e"), float)
        self.refl = (src * 0.62 + tint * 0.38).astype(np.uint8)
        self.base = up(Image.fromarray(upper, "RGB"))
        self.front = up(self._front())
        self.clouds = [(cloud(56, 9, 1), 20, 26), (cloud(40, 7, 2), 150, 14), (cloud(64, 10, 3), 260, 36)]
        self.leaves = [(rng.uniform(0, 150), rng.uniform(30, 80), rng.choice([6, 7.5, 10, 12]), rng.uniform(0, 1),
                        rng.choice(AUTUMN)) for _ in range(22)]
        self.birds = [(rng.uniform(0, DUR), rng.uniform(-0.8, 0.8)) for _ in range(12)]

    def _upper(self):
        img = np.zeros((H, W, 3), np.uint8)
        img[:] = vgrad(["#3c5a96", "#5a78b0", "#8a94c4", "#c4a4bc", "#eeb4a4", "#f8c89a", "#ffe2b0"], W, WL, ease=1.0)[np.minimum(np.arange(H), WL - 1)]
        radial_dither(img, SUN[0], SUN[1], 64, "#f8c09a", 12)
        radial_dither(img, SUN[0], SUN[1], 40, "#ffd8a8", 8)
        radial_dither(img, SUN[0], SUN[1], 24, "#fff0c8", 5)
        im = Image.fromarray(img)
        d = ImageDraw.Draw(im)
        d.ellipse([SUN[0] - 13, SUN[1] - 13, SUN[0] + 13, SUN[1] + 13], fill=hx("#fff6d8"))
        a = np.array(im)
        xs = np.arange(W)
        yy = np.arange(H)[:, None]
        rg = 94 - 18 * np.abs(np.sin(xs / 45.0 + 0.3)) - 6 * np.sin(xs / 15.0) ** 2
        a[(yy >= rg[None, :]) & (yy < WL)] = hx("#8a8cbc")
        a[(yy >= rg[None, :]) & (yy < rg[None, :] + 1)] = hx("#f6c8c4")
        snow = (yy >= rg[None, :]) & (yy < rg[None, :] + 3) & (rg[None, :] < 80)
        a[snow] = hx("#e8e4f4")
        mist = (yy > 96) & (yy < WL) & (np.clip((yy - 96) / 14.0, 0, 1) * 0.8 > bayer(H, W))
        a[mist] = hx("#b6aed0")
        im = Image.fromarray(a)
        d = ImageDraw.Draw(im)
        r = np.random.default_rng(8)
        # two rows of autumn forest on the far shore (back row hazier)
        for row, (y0, cols, pine) in enumerate(((106, ["#d8a08a", "#e0b48a", "#c89088"], "#7a8a9a"),
                                                (111, AUTUMN, "#3e5a4a"))):
            x = -6
            while x < W + 6:
                if r.random() < 0.22:
                    hgt = r.integers(9, 15) - row * 2
                    d.polygon([(x, WL), (x + 3, WL - hgt), (x + 6, WL)], fill=hx(pine))
                    x += 5
                else:
                    rr = r.integers(4, 7)
                    cy = y0 + r.integers(-2, 3)
                    d.ellipse([x - rr, cy - rr, x + rr, cy + rr], fill=hx(r.choice(cols)))
                    d.rectangle([x - rr, cy, x + rr, WL], fill=hx(r.choice(cols)))
                    x += rr + r.integers(1, 4)
        a = np.array(im)
        fm = (yy > 96) & (yy < WL)
        tops = fm & np.any([np.all(a == hx(c), axis=-1) for c in AUTUMN], axis=0)
        above = np.zeros_like(tops)
        above[1:] = ~np.any([np.all(a[:-1] == hx(c), axis=-1) for c in AUTUMN + ["#3e5a4a"]], axis=0)
        a[tops & above] = hx("#ffd8a0")
        a[WL - 1] = hx("#3a3e5a")
        return a

    def _ground_static(self):
        a = np.zeros((H, W, 3), np.uint8)
        xs = np.arange(W)
        yy = np.arange(H)[:, None]
        g = vgrad(["#7a7a3e", "#6a7036", "#5a6430", "#4e582c"], W, H - 168)
        sh = shore(xs)
        gm = yy >= sh[None, :]
        full = np.zeros((H, W, 3), np.uint8)
        full[168:] = g
        a[gm] = full[gm]
        a[gm & (yy < sh[None, :] + 1.5)] = hx("#9a8a5a")
        r = np.random.default_rng(13)
        for _ in range(1600):
            x, y = r.integers(0, W), r.integers(178, H)
            if gm[y, x]:
                a[y, x] = hx(r.choice(AUTUMN + ["#8a5a2a", "#a8a04a"]))
        return a

    def _front(self):
        """Shore, dock, foreground maple — static overlay drawn over the lake."""
        g = self._ground_static()
        ga = np.zeros((H, W, 4), np.uint8)
        gm = np.arange(H)[:, None] >= shore(np.arange(W))[None, :]
        ga[gm, :3] = g[gm]
        ga[gm, 3] = 255
        im = Image.fromarray(ga, "RGBA")
        d = ImageDraw.Draw(im)
        # dock out into the lake on the right
        for px in (290, 312, 334, 356, 378):
            d.rectangle([px, 156, px + 2, 172], fill=rgba("#5a3e2a"))
        d.rectangle([284, 151, W, 157], fill=rgba("#a8784a"))
        for px in range(284, W, 6):
            d.line([px, 151, px, 157], fill=rgba("#7a5232"))
        d.line([284, 151, W, 151], fill=rgba("#e0b07a"))
        # maple trunk + branches (canopy drawn from blobs)
        d.polygon([(0, 216), (4, 150), (10, 100), (14, 70), (22, 70), (22, 104), (18, 160), (24, 216)], fill=rgba("#5a3a2e"))
        d.line([16, 84, 50, 60], fill=rgba("#5a3a2e"), width=3)
        d.line([14, 96, -4, 70], fill=rgba("#5a3a2e"), width=3)
        r = np.random.default_rng(17)
        for _ in range(70):
            cx, cy = r.uniform(-20, 120), r.uniform(-14, 66)
            if (cx - 40) ** 2 / 90 ** 2 + (cy - 22) ** 2 / 46 ** 2 > 1:
                continue
            rr = r.uniform(6, 13)
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=rgba(r.choice(AUTUMN)))
        a = np.array(im)
        m = a[..., 3] > 0
        canopy = m & (np.arange(H)[:, None] < 80)
        a[canopy & ~_shift(m, 0, -1)] = rgba("#ffd09a")   # sun from the right
        a[canopy & ~_shift(m, -2, 0)] = rgba("#8a3a2e")
        im = Image.fromarray(a, "RGBA")
        return outline(im)

    # ------------------------------------------------------------ per frame
    def frame(self, t):
        t = t % DUR
        f = Frame(self.base)
        for c, x0, y in self.clouds:
            f.smooth(c, ((x0 + 448 * t / DUR) % 448) - 64, y)
        # ducks: a V of five, crossing every 30 s
        dx = cyc(t, 30) * 520 - 90
        for i, (ox, oy) in enumerate(((0, 0), (-7, -4), (-7, 4), (-14, -8), (-14, 8))):
            f.smooth(duck(int(cyc(t, 0.4, i * 0.2) * 2)), dx + ox, 50 + oy + 2 * wave(t, 5))
        # lake: rippled mirror of the shore, then morning mist on the far shore
        self._water(f, t)
        self._mist(f, t, 110, 126, "#e6dae8", 0.8, 30)
        # deer at the far shore (+ its reflection)
        dpose = self._deer(t)
        if dpose:
            x, pose, step, fl = dpose
            sp = deer(pose, step)
            sp = flip(sp) if fl else sp
            f.put(sp, x, WL - 16)
            f.put(reflect(sp, "#5a4a68"), x, WL - 1)
        # loon (dives every 20 s)
        self._loon(f, t)
        # canoe: Black paddles, Blue fishes
        self._canoe(f, t)
        # shore, dock, maple
        f.smooth(self.front, 0, 0)
        self._reeds(f, t)
        # Pink on the dock with a hot drink
        px, py = 288, 123
        draw_blok(f, "pink", px, py, t, eyes="happy" if cyc(t, 10) > 0.6 else 1, flipx=True, blink_phase=0.3, wind=0.6)
        f.put(mug(), px - 4, py + 17)
        d = f.draw()
        for i in range(3):
            a = cyc(t, 3, i / 3)
            d.point((px - 2 + round(2 * np.sin(TAU * a + i)), py + 15 - 12 * a), fill=rgba("#f4eef4" if a < 0.6 else "#c8c0d8"))
        # Red rakes, then jumps into the leaf pile
        self._rake(f, t)
        f.put(sign(), 222, 166)
        # falling leaves
        d = f.draw()
        for (x0, y0, p, ph, col) in self.leaves:
            a = cyc(t, p, ph)
            x = x0 + 60 * a + 6 * np.sin(TAU * a * 3 + ph * 6)
            y = y0 + (H - y0) * a
            d.point((x, y), fill=rgba(col))
            d.point((x + (1 if cyc(t, 0.5, ph) < 0.5 else -1), y + (1 if cyc(t, 0.75, ph) < 0.5 else 0)), fill=rgba(col))
        draw_bug(f)
        return f.out()

    def _deer(self, t):
        a, b = DEER_T
        if not (a <= t <= b):
            return None
        step = int(t * 4) % 2
        if t < a + 4:
            return 6 + 26 * (t - a) / 4, "walk", step, False
        if t < a + 6:
            return 32, "stand", 0, False
        if t < a + 15:
            return 32, "drink", 0, False
        if t < a + 17:
            return 32, "stand", 0, False
        return 32 - 26 * (t - a - 17) / 4, "walk", step, True

    def _water(self, f, t):
        hh = self.refl.shape[0]
        out = np.zeros((hh, W, 4), np.uint8)
        for r in range(hh):
            amp = 0.4 + r * 0.05
            off = int(round(amp * np.sin(r * 0.7 + TAU * t / 3)))
            out[r, :, :3] = np.roll(self.refl[r], off, axis=0)
        out[..., 3] = 255
        # ripple glints
        for i, (y, per, ln) in enumerate(((121, 26, 4), (125, 30, 5), (130, 34, 6), (136, 38, 8), (143, 44, 10), (151, 52, 12), (160, 60, 14))):
            off = int(6 * wave(t, (6, 5, 4, 6, 5, 3, 4)[i], i)) + i * 9
            for x in range(-per, W, per):
                xx = x + off
                out[y - WL, max(0, xx):max(0, min(W, xx + ln)), :3] = hx("#f4d0b8" if abs(xx - SUN[0]) < 40 else "#9aa4cc")
        f.arr(out, 0, WL)

    def _mist(self, f, t, y0, y1, col, strength, period):
        """A drifting mist band: solid core, dithered edges, thickness varying along x."""
        hh = y1 - y0
        xs = np.arange(W)[None, :]
        ys = np.arange(hh)[:, None]
        yc = (hh - 1) / 2
        wisp = np.clip(0.15 + 0.55 * np.sin(xs / 37.0 + TAU * t / period) + 0.3 * np.sin(xs / 13.0 - TAU * t / 20), 0, 1)
        th = hh * strength * wisp
        dens = np.clip((th - np.abs(ys - yc) * 2) / 4.0, 0, 1)
        a = np.zeros((hh, W, 4), np.uint8)
        a[dens > bayer(hh, W)] = rgba(col)
        f.arr(a, 0, y0)

    def _loon(self, f, t):
        x0 = 78
        k = t % 20
        d = f.draw()
        if 11.5 <= k or k < 8:
            u = ((k - 11.5) % 20) / 16.5
            x = x0 + 14 - 14 * u
            f.put(loon(0), x, 147 + round(0.5 * wave(t, 2)))
            d.line([x - 2, 155, x + 12, 155], fill=rgba("#c8c8e0"))
        elif k < 8.5:
            f.put(loon(1), x0, 148)
        else:
            rr = int((k - 8.5) * 3) % 6 + 2
            d.ellipse([x0 + 5 - rr, 153, x0 + 5 + rr, 156], outline=rgba("#c8c8e0"))
            if k > 11.0:
                d.ellipse([x0 + 12, 153, x0 + 20, 156], outline=rgba("#e8e8f4"))

    def _canoe(self, f, t):
        cx = 150 + 40 * wave(t, 60)
        cy = 142 + round(0.6 * wave(t, 3))
        d = f.draw()
        # ripple rings around the canoe
        rr = cyc(t, 3) * 10
        d.ellipse([cx + 4 - rr, cy + 10, cx + 74 + rr, cy + 14], outline=rgba("#b4b8d8"))
        # Blue fishing at the bow (left), Black paddling at the stern (right)
        draw_blok(f, "blue", cx + 8, cy - 18, t, eyes=-1, flipx=False, blink_phase=0.6, wind=0.6)
        draw_blok(f, "black", cx + 40, cy - 18, t, eyes=-1, flipx=True, blink_phase=0.1, wind=0.6)
        d = f.draw()
        tip = (cx - 22, cy - 22 + wave(t, 4))
        d.line([cx + 10, cy - 2, tip[0], tip[1]], fill=rgba("#8a5a2b"))
        bob = (cx - 34, 150 + round(wave(t, 2)))
        d.line([tip[0], tip[1], bob[0], bob[1]], fill=rgba("#f4f0e6"))
        d.rectangle([bob[0] - 1, bob[1] - 2, bob[0] + 1, bob[1]], fill=rgba("#ec4a35"))
        r2 = cyc(t, 2) * 6
        d.ellipse([bob[0] - 2 - r2, bob[1] + 1, bob[0] + 2 + r2, bob[1] + 2 + r2 * 0.3], outline=rgba("#c8c8e0"))
        # paddle stroke (3 s): blade in the water for the first half
        p = cyc(t, 3)
        hx_, hy = cx + 50, cy - 4
        if p < 0.5:
            bx, by = cx + 62 + 18 * (p / 0.5), cy + 9
        else:
            q = (p - 0.5) / 0.5
            bx, by = cx + 80 - 18 * q, cy + 2 - 5 * np.sin(np.pi * q)
        d.line([hx_, hy, bx, by], fill=rgba("#b07a42"))
        d.rectangle([bx - 1, by - 1, bx + 2, by + 2], fill=rgba("#b07a42"))
        if p < 0.08 or 0.5 < p < 0.58:
            for i in range(4):
                d.point((bx - 2 + i * 2, by - 2 - (i % 2)), fill=rgba("#ffffff"))
        c = canoe()
        f.put(reflect(c, "#7a4a68"), cx, cy + 11)
        f.put(c, cx, cy)

    def _reeds(self, f, t):
        d = f.draw()
        for i, (x, hgt) in enumerate(((262, 14), (266, 18), (270, 12), (276, 16), (352, 13), (358, 17), (40, 12), (46, 15))):
            sw = round(1.2 * wave(t, 4, i * 0.6))
            base = shore(x) + 1
            d.line([x, base, x + sw, base - hgt], fill=rgba("#6a7a3a"))
            d.rectangle([x + sw - 1, base - hgt - 1, x + sw, base - hgt + 3], fill=rgba("#7a4a2a"))

    def _rake(self, f, t):
        rx, ry = 104, 176
        pile_x, pile_y = 142, 186
        k = t - JUMP_T
        d = f.draw()
        if 0 <= k <= 5.5:
            d.line([118, 206, 146, 204], fill=rgba("#a8784a"))
            for i in range(5):
                d.point((147, 202 + i), fill=rgba("#7a7a8a"))
        if 0 <= k < 1.0:
            u = k / 1.0
            x = rx + (156 - rx) * u
            y = ry - 22 * np.sin(np.pi * u) - 4 * u
            draw_blok(f, "red", x, y, t, eyes="happy", mouth="open", arms="up", wind=1.4)
            f.put(leafpile(), pile_x, pile_y)
        elif 1.0 <= k < 4.5:
            draw_blok(f, "red", 156, 164, t, eyes="happy" if k > 1.6 else "blink", mouth="open", arms="up", tail=True, wind=1.0)
            f.put(leafpile(), pile_x, pile_y)
            if k < 2.6:
                d = f.draw()
                for i in range(14):
                    ang = TAU * i / 14
                    sp = (k - 1.0) * 26
                    lx = 168 + np.cos(ang) * sp * 0.9
                    ly = 186 - abs(np.sin(ang)) * sp * 1.3 + 10 * (k - 1.0) ** 2
                    d.rectangle([lx, ly, lx + 1, ly + (i % 2)], fill=rgba(AUTUMN[i % len(AUTUMN)]))
        elif 4.5 <= k < 5.5:
            u = (k - 4.5) / 1.0
            x = 156 + (rx - 156) * u
            y = 164 - 20 * np.sin(np.pi * u) + 12 * u
            f.put(leafpile(), pile_x, pile_y)
            draw_blok(f, "red", x, y, t, eyes="happy", mouth="open", arms="up", flipx=True, wind=1.4)
        else:
            f.put(leafpile(), pile_x, pile_y)
            p = cyc(t, 2)
            hx_ = rx + 30 + 10 * np.sin(TAU * p)
            draw_blok(f, "red", rx, ry, t, eyes=1, blink_phase=0.4)
            d = f.draw()
            d.line([rx + 25, ry + 18, hx_, 204], fill=rgba("#a8784a"))
            d.line([hx_ - 3, 205, hx_ + 3, 205], fill=rgba("#7a7a8a"))
            for i in range(-3, 4, 2):
                d.point((hx_ + i, 206), fill=rgba("#7a7a8a"))
            if abs(np.sin(TAU * p)) > 0.9:
                d.point((hx_ + 5 * np.sign(np.cos(TAU * p) + 1e-6), 203), fill=rgba(AUTUMN[int(t) % 5]))

    # ------------------------------------------------------------ audio
    def audio(self):
        from engine import audio as A
        T = A.T
        buf = np.zeros((2, A.N))
        for ch in (0, 1):
            lap = A.colored(0.6, 150, 2500, seed=80 + ch) * (0.6 + 0.4 * np.clip(np.sin(TAU * T / 5 + ch), 0, 1) ** 2) * 0.18
            wind = A.colored(0.2, 2500, 9000, seed=82 + ch) * (0.3 + 0.7 * np.clip(np.sin(TAU * T / 15 + ch * 2), 0, 1)) * 0.05
            air = A.colored(1.2, 80, 900, seed=84 + ch) * 0.06
            buf[ch] += lap + wind + air
        r = np.random.default_rng(90)
        for i in range(40):
            A.place(buf, A.pk(A.plop(100 + i)) * 0.5, r.uniform(0, DUR), 0.03, pan=r.uniform(-0.6, 0.6))
        for i, (t0, pan) in enumerate(self.birds):
            A.place(buf, A.pk(A.chirp_seq(110 + i)), t0, 0.10, pan=pan)
        for i, t0 in enumerate(LOON_T):
            A.place(buf, A.pk(A.loon(i)), t0, 0.55, pan=-0.45 if i == 0 else 0.35)
        for k in range(3):
            A.place(buf, A.pk(A.plop(200 + k)), 8.4 + 20 * k, 0.12, pan=-0.6)
            A.place(buf, A.pk(A.plop(210 + k)), 11.0 + 20 * k, 0.08, pan=-0.55)
        for k in range(20):
            t0 = 3.0 * k
            cx = 150 + 40 * np.sin(TAU * t0 / 60) + 70
            A.place(buf, A.pk(A.swish(k)), t0, 0.7, pan=(cx - 192) / 192)
        for base_t in (16.0, 46.0):
            for i, dt in enumerate((0.0, 0.3, 0.75, 1.1)):
                A.place(buf, A.pk(A.quack(int(base_t) + i)), base_t + dt, 0.9, pan=-0.2 + 0.4 * i / 3)
        for k in range(60):
            t0 = float(k)
            if JUMP_T - 0.5 <= t0 <= JUMP_T + 6:
                continue
            A.place(buf, A.pk(A.scrape(300 + k, 0.4, 900, 5000)), t0 + 0.25, 0.5, pan=-0.25)
        A.place(buf, A.pk(A.rustle(1, 1.2)), JUMP_T + 1.0, 0.6, pan=-0.15)
        A.place(buf, A.pk(A.rustle(2, 0.8)), JUMP_T + 4.5, 0.22, pan=-0.2)
        A.place(buf, A.pk(A.snap(3)), DEER_T[0] + 0.2, 0.10, pan=-0.85)
        return A.master(buf)
