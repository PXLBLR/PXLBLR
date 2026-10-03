"""NINJA-BLOKS · Dino Valley (golden hour) — 60 s seamless loop.

Periods (all divide 60 s): brachiosaurus crossing 60 s (2 s stride) · T-Rex
peek + roar once per loop (t=24..35, roar at 28 s) · pterosaurs 20/30 s ·
waterfall + river flow continuous scroll · campfire 0.5/0.75 s flicker ·
volcano smoke 1 puff/s · fishing bobber 2 s bob, bite at 15 s · fish jump
every 20 s · egg wobble 5 s · fireflies 10-30 s paths.
"""
import numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw
from engine.px import (W, H, S, INK, TAU, DUR, rgba, hx, vgrad, radial_dither, bayer, sprite, outline, rim,
                       up, flip, wave, cyc, Frame, _shift)
from engine.bloks import draw_blok
from engine.flora import palm, fern
from scenes.common import sign, draw_bug, shadow_ellipse, _pad

SUN = (226, 94)
VOLC = (64, 34)
RIVER = (146, 170)
FIRE = (196, 197)
RIM = "#ffcf8a"
ROAR_T = 28.0

TREEFERN = dict(trunk=("#5a3a32", "#4a2e2a"), trunk_shade="#36211f", spine="#24502e",
                leaf=("#3f8a3e", "#2f6e34"), light="#ffc07a", nuts=("#000000", "#000000"))
GFERN = dict(TREEFERN, leaf=("#4f9a3a", "#3a7a30"), spine="#2a5a2a")

rng = np.random.default_rng(3)


def near_bank(x):
    return 169 + 1.5 * np.sin(x / 17.0) + 1.0 * np.sin(x / 6.0 + 2)


# ---------------------------------------------------------------- creatures
@lru_cache(maxsize=None)
def brachio(k):
    """8-frame walk cycle (k=0..7), 112x86 art px, facing right."""
    w, h = 114, 88
    ph = k / 8 * TAU
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    body, belly, dark, spot = "#5a9a7e", "#a9cf8c", "#3c6e5c", "#4a8570"

    def leg(x, phase, col):
        dx = 2.5 * np.sin(ph + phase)
        lift = max(0.0, -np.sin(ph + phase)) * 2.5
        d.ellipse([x - 2, 46, x + 10, 64], fill=rgba(col))
        d.polygon([(x, 56), (x + 8, 56), (x + dx + 7, 82 - lift), (x + dx, 82 - lift)], fill=rgba(col))
        d.rectangle([x + dx - 1, 79 - lift, x + dx + 8, 82 - lift], fill=rgba(col))
        for tx in (0, 3, 6):
            d.point((x + dx + tx, 82 - lift), fill=rgba("#e8e0c8"))
    # far-side legs (darker), then near-side
    leg(38, np.pi, dark); leg(70, 0, dark)
    # tail
    for i in range(30):
        s = i / 29
        x = 32 - 30 * s
        y = 50 + 16 * s * s + 1.2 * np.sin(ph + s * 3)
        r = 6 - 5 * s
        d.ellipse([x - r, y - r, x + r, y + r], fill=rgba(body))
    # neck (sways with stride)
    sway = 1.0 * np.sin(ph)
    for i in range(34):
        s = i / 33
        x = 74 + 20 * s + 4 * s * s
        y = 44 - 36 * s + sway * s
        r = 5.5 - 1.5 * s
        d.ellipse([x - r, y - r, x + r, y + r], fill=rgba(body))
    hx_, hy = 98, 7 + sway
    d.ellipse([hx_ - 5, hy - 5, hx_ + 8, hy + 3], fill=rgba(body))
    d.ellipse([hx_ + 3, hy - 3, hx_ + 11, hy + 3], fill=rgba(body))
    d.ellipse([28, 34, 82, 62], fill=rgba(body))
    leg(30, 0, body); leg(62, np.pi, body)
    a = np.array(im)
    m = a[..., 3] > 0
    bodym = m & np.all(a[..., :3] == hx(body), axis=-1)
    yy = np.arange(h)[:, None] * np.ones((1, w))
    xx = np.ones((h, 1)) * np.arange(w)[None, :]
    a[bodym & (yy > 56) & (yy < 64) & (xx > 34) & (xx < 80)] = rgba(belly)
    a[bodym & ~_shift(m, -2, 0) & (yy > 70)] = rgba(dark)
    for (sx, sy) in ((44, 40), (52, 38), (60, 41), (48, 46), (68, 42), (76, 30), (84, 20)):
        a[sy:sy + 2, sx:sx + 3][bodym[sy:sy + 2, sx:sx + 3]] = rgba(spot)
    im = Image.fromarray(a, "RGBA")
    im = rim(im, RIM, dy=1, skip=(INK, dark))
    im = rim(im, RIM, dy=0, dx=-1, skip=(INK, dark, belly))
    d = ImageDraw.Draw(im)
    d.point((hx_ + 4, int(hy - 2)), fill=rgba(INK))
    d.point((hx_ + 10, int(hy - 1)), fill=rgba("#2d4a40"))
    d.line([hx_ + 6, int(hy + 1), hx_ + 10, int(hy + 1)], fill=rgba("#2d4a40"))
    return up(outline(im))


@lru_cache(maxsize=None)
def trex(open_):
    w, h = 50, 40
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c, belly, stripe = "#9a5c42", "#e2aa72", "#74402e"
    d.polygon([(8, 20), (22, 18), (24, 39), (6, 39)], fill=rgba(c))  # neck
    d.polygon([(4, 14), (10, 6), (26, 3), (40, 5), (45, 9), (46, 15), (30, 18), (12, 22)], fill=rgba(c))
    jaw = [(12, 20), (44, 17), (44, 21), (28, 25), (12, 27)] if not open_ else [(12, 20), (40, 27), (38, 31), (24, 32), (12, 27)]
    d.polygon(jaw, fill=rgba(belly))
    if open_:
        d.polygon([(14, 20), (44, 16), (40, 26), (14, 22)], fill=rgba("#5a1f2a"))
        for x in range(18, 42, 3):
            d.point((x, 17 + (44 - x) // 9), fill=rgba("#fff6e0"))
            d.point((x - 1, 25 + (x - 14) // 8), fill=rgba("#fff6e0"))
    else:
        for x in range(18, 44, 3):
            d.point((x, 19 + (44 - x) // 12), fill=rgba("#fff6e0"))
    for (x0, y0) in ((14, 8), (19, 6), (24, 26), (12, 30)):
        d.line([x0, y0, x0 + 2, y0 + 3], fill=rgba(stripe))
    d.line([26, 6, 32, 5], fill=rgba(stripe))  # brow ridge
    d.rectangle([28, 7, 30, 9], fill=rgba("#ffd23f"))
    d.point((29, 8), fill=rgba(INK))
    d.point((42, 8), fill=rgba(INK))
    im = rim(im, RIM, dy=1, skip=(INK, "#5a1f2a", "#fff6e0"))
    return up(outline(im))


@lru_cache(maxsize=None)
def ptero(f):
    w, h = 30, 16
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = "#7a4466"
    tip = (2, 9, 14)[f]
    d.polygon([(13, 8), (2, tip), (8, 9), (14, 11)], fill=rgba(c))
    d.polygon([(17, 8), (28, tip), (22, 9), (16, 11)], fill=rgba(c))
    d.ellipse([12, 7, 18, 11], fill=rgba(c))
    d.polygon([(17, 7), (19, 5), (26, 8), (19, 9)], fill=rgba(c))       # head + beak
    d.polygon([(18, 6), (14, 3), (17, 6)], fill=rgba(c))                # crest
    d.point((20, 7), fill=rgba("#ffd23f"))
    im = rim(im, "#ff9f7a", dy=1, skip=(INK, "#ffd23f"))
    return up(outline(im, "#2a1630"))


@lru_cache(maxsize=None)
def trike(blink, wag):
    w, h = 30, 20
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c, belly, frill = "#6fc0ae", "#c6ead8", "#f2b84e"
    d.polygon([(2, 11 + wag), (8, 9), (8, 13)], fill=rgba(c))
    for lx in (8, 11, 15, 18):
        d.rectangle([lx, 14, lx + 2, 17], fill=rgba("#4f9a8a" if lx in (11, 18) else c))
    d.ellipse([6, 7, 21, 16], fill=rgba(c))
    d.ellipse([14, 1, 24, 13], fill=rgba(frill))
    for (fx, fy) in ((16, 3), (19, 2), (22, 4)):
        d.point((fx, fy), fill=rgba("#e0703a"))
    d.ellipse([18, 6, 27, 13], fill=rgba(c))
    d.line([21, 5, 23, 2], fill=rgba("#fff6e0")); d.line([24, 5, 26, 3], fill=rgba("#fff6e0"))
    d.point((27, 8), fill=rgba("#fff6e0")); d.point((28, 7), fill=rgba("#fff6e0"))
    a = np.array(im)
    m = np.all(a[..., :3] == hx(c), axis=-1) & (a[..., 3] > 0)
    a[m & (np.arange(h)[:, None] > 12)] = rgba(belly)
    im = Image.fromarray(a, "RGBA")
    d = ImageDraw.Draw(im)
    if blink:
        d.line([22, 8, 23, 8], fill=rgba(INK))
    else:
        d.rectangle([22, 7, 23, 9], fill=rgba("#ffffff")); d.point((23, 8), fill=rgba(INK))
    d.point((19, 11), fill=rgba("#ff8fa3"))
    im = rim(im, RIM, dy=1, skip=(INK, "#fff6e0", "#ffffff"))
    return outline(im)


@lru_cache(maxsize=None)
def nest():
    im = Image.new("RGBA", (30, 18), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([1, 9, 28, 16], fill=rgba("#7a5230"))
    for x in range(2, 28, 2):
        d.line([x, 10 + (x % 3), x + 3, 13 + (x % 2)], fill=rgba("#a87444" if x % 4 else "#5a3a22"))
    return outline(im)


@lru_cache(maxsize=None)
def egg(spots="#7fbf8a"):
    rows = [".WWW.", "WWWWW", "WSWWW", "WWWSW", "WWWWW", ".WWW."]
    return outline(_pad(sprite(rows, {"W": "#f6ecd2", "S": spots})))


@lru_cache(maxsize=None)
def fish():
    rows = ["K..KKK..", "KK.KOOK.", "KOKOOOOK", "KK.KOWK.", "K..KKK.."]
    return sprite(rows, {"K": INK, "O": "#ff8a3d", "W": "#ffffff"})


# ---------------------------------------------------------------- scene
class Dino:
    name = "dino"

    def __init__(self):
        self.base = up(Image.fromarray(self._sky(), "RGB"))
        self.canopy = up(self._canopy())
        self.front = up(self._front())
        self.stars = [(int(rng.uniform(0, W)), int(rng.uniform(2, 34)), rng.choice([2, 3, 4, 5]), rng.uniform(0, TAU)) for _ in range(26)]
        self.flies = [(rng.uniform(20, 360), rng.uniform(150, 205), rng.uniform(6, 16), rng.uniform(3, 8),
                       rng.choice([10, 12, 15, 20]), rng.choice([12, 15, 20, 30]), rng.uniform(0, TAU), rng.choice([2, 3, 4]))
                      for _ in range(18)]

    # ------------------------------------------------------------ static layers
    def _sky(self):
        img = np.zeros((H, W, 3), np.uint8)
        img[:] = vgrad(["#2b1d5a", "#40276e", "#663685", "#9a4590", "#cc5a86", "#ec7a74", "#f89e66", "#fcc06e", "#ffe08e"], W, 140, ease=1.0).repeat(1, 0)[np.minimum(np.arange(H), 139)]
        radial_dither(img, SUN[0], SUN[1], 70, "#f7a46a", 12)
        radial_dither(img, SUN[0], SUN[1], 48, "#fcc27a", 10)
        radial_dither(img, SUN[0], SUN[1], 30, "#ffe0a0", 6)
        im = Image.fromarray(img)
        d = ImageDraw.Draw(im)
        d.ellipse([SUN[0] - 16, SUN[1] - 16, SUN[0] + 16, SUN[1] + 16], fill=hx("#fff0b8"))
        d.ellipse([SUN[0] - 13, SUN[1] - 13, SUN[0] + 13, SUN[1] + 13], fill=hx("#fffbe6"))
        # thin cloud streaks across the sun
        for (x0, y0, ln, col) in ((150, 70, 90, "#f8b27a"), (196, 84, 70, "#ffd49a"), (240, 102, 110, "#f6a070"),
                                  (40, 52, 70, "#d97a8a"), (300, 44, 60, "#c46a8e"), (110, 30, 50, "#9a4f8e")):
            d.ellipse([x0, y0 - 1, x0 + ln, y0 + 2], fill=hx(col))
            d.ellipse([x0 + ln * 0.2, y0 - 3, x0 + ln * 0.7, y0], fill=hx(col))
        # far range
        xs = np.arange(W)
        ridge = 104 - 14 * np.abs(np.sin(xs / 37.0 + 1)) - 8 * np.abs(np.sin(xs / 13.0)) - 4 * np.sin(xs / 5.0) * 0.5
        a = np.array(im)
        yy = np.arange(H)[:, None]
        a[(yy >= ridge[None, :])] = hx("#9a5a8e")
        rimm = (yy >= ridge[None, :]) & (yy < ridge[None, :] + 1.5)
        a[rimm] = hx("#e48a86")
        # volcano
        vx, vy = VOLC
        half = np.where(np.abs(xs - vx) < 6, vy, vy + np.maximum(np.abs(xs - vx) - 6, 0) ** 1.25 * 0.95)
        vm = yy >= half[None, :]
        a[vm] = hx("#5e3c6e")
        a[vm & (yy < half[None, :] + 1.5) & (xs[None, :] > vx)] = hx("#d9787e")
        for i in range(40):
            y = vy + i
            x = vx - 3 + int(2.5 * np.sin(i / 4.0)) - i // 3
            if 0 <= x < W:
                a[y, x] = hx("#7a2f4a")
        # mid hills
        hills = 128 - 9 * np.abs(np.sin(xs / 29.0 + 2)) - 5 * np.sin(xs / 11.0) ** 2
        hm = yy >= hills[None, :]
        a[hm] = hx("#5a3a6e")
        a[hm & (yy < hills[None, :] + 1)] = hx("#c8707e")
        return a

    def _canopy(self):
        a = np.zeros((H, W, 4), np.uint8)
        xs = np.arange(W)
        yy = np.arange(H)[:, None]
        r = np.random.default_rng(5)
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        for x in range(-10, W + 10, 9):
            rr = r.integers(8, 15)
            cy = 134 - r.integers(0, 10)
            d.ellipse([x - rr, cy - rr, x + rr, cy + rr], fill=rgba("#2f4a4c"))
        d.rectangle([0, 132, W, 150], fill=rgba("#2f4a4c"))
        im = rim(im, "#d98a62", dy=1)
        a = np.array(im)
        m = a[..., 3] > 0
        a[m & ~_shift(m, 2, 0) & _shift(m, 1, 0)] = rgba("#4f5f50")
        # cycad silhouettes poking above the canopy
        im = Image.fromarray(a, "RGBA")
        for (x, y, ln) in ((40, 126, 16), (170, 122, 18), (300, 124, 14)):
            p = palm(0, (x, y + 14), (x, y + 6), (x, y - 6), [(200, ln, 0.7), (235, ln, 0.6), (270, ln * 0.7, 0.4),
                                                              (305, ln, 0.6), (340, ln, 0.7)], col=dict(TREEFERN, leaf=("#2f4a4c", "#2f4a4c"), spine="#2f4a4c", trunk=("#2f4a4c", "#2f4a4c"), trunk_shade="#2f4a4c", light="#d98a62"), nuts=False)
            pa = np.array(p)
            pa[np.all(pa[..., :3] == hx(INK), axis=-1)] = 0
            p = Image.fromarray(pa, "RGBA")
            im.paste(p, (0, 0), p)
        return im

    def _front(self):
        a = np.zeros((H, W, 4), np.uint8)
        xs = np.arange(W)
        yy = np.arange(H)[:, None]
        # far bank lip
        fb = 145 + 0.8 * np.sin(xs / 9.0)
        a[(yy >= fb[None, :] - 3) & (yy < RIVER[0] + 1)] = rgba("#3e5f36")
        a[(yy >= fb[None, :] - 3) & (yy < fb[None, :] - 2)] = rgba("#e0a060")
        # river base
        riv = vgrad(["#3a4a80", "#4a5a90", "#7a6a9a", "#c27a8a", "#e8967a"], W, RIVER[1] - RIVER[0] + 5, ease=1.0)
        a[RIVER[0] + 1:RIVER[1] + 5, :, :3] = riv[1:]
        a[RIVER[0] + 1:RIVER[1] + 5, :, 3] = 255
        # foreground ground
        nb = near_bank(xs)
        g = vgrad(["#6a9a3e", "#5a8a36", "#4a782e", "#3e6a2a"], W, H - 160)
        gm = yy >= nb[None, :]
        full = np.zeros((H, W, 3), np.uint8)
        full[160:] = g
        a[gm, :3] = full[gm]
        a[gm, 3] = 255
        a[gm & (yy < nb[None, :] + 1.2)] = rgba("#a8c860")
        a[(yy >= nb[None, :] + 1.2) & (yy < nb[None, :] + 3)] = rgba("#3a5a2a")
        # dirt clearing round the fire, with warm glow rings
        cx, cy = FIRE
        dist = np.sqrt(((xs[None, :] - cx) / 1.0) ** 2 + ((yy - cy) / 0.42) ** 2)
        clear = gm & (np.clip((52 - dist) / 8, 0, 1) > bayer(H, W))
        a[clear] = rgba("#9a7a50")
        a[gm & (np.clip((34 - dist) / 6, 0, 1) > bayer(H, W))] = rgba("#b48e58")
        a[gm & ~clear & (np.clip((78 - dist) / 14, 0, 1) > bayer(H, W))] = rgba("#8a9a40")
        # grass tufts + flowers
        r = np.random.default_rng(9)
        for _ in range(260):
            x, y = r.integers(0, W), r.integers(174, H - 1)
            if a[y, x, 3] and not clear[y, x]:
                a[y, x] = rgba(r.choice(["#7aaa48", "#3e6a2a", "#8aba50"]))
                a[y - 1, x] = a[y, x]
        for _ in range(24):
            x, y = r.integers(4, W - 4), r.integers(180, H - 4)
            if not clear[y, x]:
                c = r.choice(["#ff70b0", "#ffd23f", "#ffffff"])
                a[y, x] = rgba(c); a[y - 1, x] = rgba(c); a[y, x - 1] = rgba(c); a[y, x + 1] = rgba(c)
                a[y + 1, x] = rgba("#2f5a2a")
        im = Image.fromarray(a, "RGBA")
        d = ImageDraw.Draw(im)
        # cliff + waterfall lip on the right
        cl = [(318, 150), (320, 112), (328, 100), (340, 96), (360, 92), (384, 88), (384, 152)]
        d.polygon(cl, fill=rgba("#6e4a5e"))
        for i, y in enumerate(range(104, 150, 7)):
            d.line([322 + (i % 2) * 3, y, 384, y - 3], fill=rgba("#5a3a4e"))
        d.line([(320, 112), (328, 100), (340, 96)], fill=rgba("#c87a7a"), width=1)
        d.line([319, 114, 319, 148], fill=rgba("#b06a72"))
        d.polygon([(326, 99), (340, 94), (360, 90), (384, 86), (384, 90), (360, 94), (340, 98), (328, 102)], fill=rgba("#3e6a36"))
        d.line([(326, 99), (340, 94), (360, 90), (384, 86)], fill=rgba("#e0a060"))
        # rocks: fishing rock (left), meditation pillar (right)
        d.polygon([(40, 186), (44, 168), (56, 160), (80, 158), (94, 166), (98, 186)], fill=rgba("#7a6a7e"))
        d.polygon([(44, 168), (56, 160), (80, 158), (84, 162), (60, 164)], fill=rgba("#a08aa0"))
        d.polygon([(276, 202), (280, 156), (286, 150), (300, 150), (306, 158), (308, 202)], fill=rgba("#6e5e74"))
        d.polygon([(280, 156), (286, 150), (300, 150), (296, 154), (284, 158)], fill=rgba("#a08aa0"))
        d.line([300, 152, 306, 160], fill=rgba(RIM))
        im = outline(im)
        return im

    # ------------------------------------------------------------ per frame
    def frame(self, t):
        t = t % DUR
        f = Frame(self.base)
        d = f.draw()
        for (x, y, p, ph) in self.stars:
            v = wave(t, p, ph)
            if v > -0.2:
                d.point((x, y), fill=rgba("#fff6d8" if v > 0.6 else "#c9a8d8"))
        # volcano: crater glow + lava flicker + smoke (1 puff/s, 9 s life)
        vx, vy = VOLC
        glow = "#ffb14a" if wave(t, 0.5) > 0 else "#ff7a3d"
        d.line([vx - 5, vy, vx + 5, vy], fill=rgba(glow))
        d.line([vx - 3, vy - 1, vx + 3, vy - 1], fill=rgba("#ff7a3d"))
        for i in range(0, 40, 2):
            if (i + int(t * 8)) % 6 < 4:
                y = vy + i
                x = vx - 3 + int(2.5 * np.sin(i / 4.0)) - i // 3
                d.point((x, y), fill=rgba("#ff8a3d" if i < 20 else "#e0503a"))
        for k in range(9):
            age = cyc(t, 1, k / 9) * 0 + ((t + k) % 9) / 9
            r = 2 + 6 * age
            px_ = vx + 2 + 30 * age ** 1.3 + 2 * np.sin(age * 6 + k)
            py = vy - 3 - 30 * age
            col = ["#c8a0b4", "#b48ea8", "#a07e9e", "#8e6e92"][min(3, int(age * 4))]
            d.ellipse([px_ - r, py - r * 0.8, px_ + r, py + r * 0.8], fill=rgba(col))
        f.flush()
        # pterosaurs
        for span_t, y0, direction, ph in ((30, 46, 1, 0.1), (20, 64, -1, 0.55)):
            x = cyc(t, span_t, ph) * 460 - 40
            if direction < 0:
                x = W - x
            p = ptero(int(cyc(t, 0.8, ph) * 3))
            f.smooth(p if direction > 0 else flip(p), x, y0 + 4 * wave(t, 5, ph * 9))
        # T-Rex peeks over the canopy and roars
        tr = self._trex_y(t)
        if tr is not None:
            yoff, open_ = tr
            shake = (int(t * 30) % 2) * 0.4 if open_ else 0
            f.smooth(trex(open_), 100 + shake, 86 + yoff)
        f.smooth(self.canopy, 0, 0)
        # birds scatter at the roar
        if ROAR_T - 0.2 < t < ROAR_T + 6:
            d = f.draw()
            a = t - (ROAR_T - 0.2)
            for i in range(6):
                bx = 120 + i * 7 + a * (14 + i * 3)
                by = 124 - a * (16 + i * 2) + (i % 3) * 3
                wing = int((t * 8 + i) % 2)
                d.point((bx, by), fill=rgba("#2a1a30"))
                d.point((bx - 1, by - wing), fill=rgba("#2a1a30")); d.point((bx + 1, by - wing), fill=rgba("#2a1a30"))
            f.flush()
        # brachiosaurus crossing (2 s stride, 60 s crossing)
        bx = cyc(t, 60) * 520 - 116
        f.smooth(brachio(int(cyc(t, 2) * 8) % 8), bx, 62)
        f.smooth(self.front, 0, 0)
        self._water(f, t)
        self._foreground(f, t)
        draw_bug(f)
        return f.out()

    @staticmethod
    def _trex_y(t):
        if not (23.5 <= t <= 35.5):
            return None
        if t < 25.5:
            k = (t - 23.5) / 2
            return 40 * (1 - k * k * (3 - 2 * k)), False
        if t > 33.5:
            k = (t - 33.5) / 2
            return 40 * (k * k * (3 - 2 * k)), False
        return 0, (ROAR_T - 0.1 <= t <= ROAR_T + 2.4)

    def _water(self, f, t):
        d = f.draw()
        # river ripples flowing right: 24 px pattern at 12 px/s (720 px per loop = 30 patterns)
        rows = [(149, 2, 20, "#6a7ab0"), (152, 3, 24, "#8a8ab8"), (156, 4, 28, "#b88aa8"), (160, 5, 30, "#e8a090"), (164, 6, 34, "#ffc09a")]
        for i, (y, ln, per, col) in enumerate(rows):
            off = (12 * t * (0.5 + 0.25 * i)) % per + i * 7
            for x in range(-per, W, per):
                xx = int(x + off)
                d.line([xx, y, xx + ln, y], fill=rgba(col))
        # sun glitter on the river
        for i in range(26):
            x = SUN[0] - 14 + (i * 37) % 30
            y = 148 + (i * 13) % 20
            if wave(t, (1, 1.5, 2)[i % 3], i) > 0.4:
                d.line([x, y, x + 1 + (i % 2), y], fill=rgba("#fff0b0"))
        # waterfall: vertical streaks scrolling down at 24 px/s
        for x in range(336, 352):
            for y in range(96, 149):
                k = (y - 24 * t + (x * 7) % 12) % 12
                if k < 3:
                    col = "#ffffff"
                elif k < 7:
                    col = "#bfe2ee"
                else:
                    col = "#8fb8d8" if (x in (336, 351)) else "#a8d0e4"
                d.point((x, y), fill=rgba(col))
        d.line([336, 95, 351, 95], fill=rgba("#ffffff"))
        # splash + mist
        for k in range(6):
            a = cyc(t, 1.5, k / 6)
            r = 2 + 4 * a
            cx = 332 + k * 4 + 3 * np.sin(k)
            cy = 148 - 6 * a
            d.ellipse([cx - r, cy - r * 0.7, cx + r, cy + r * 0.7], fill=rgba("#e8f6fa" if a < 0.5 else "#c8dde8"))
        # rocks in the river with ripple rings
        for (rx, ry) in ((140, 160), (258, 156)):
            rr = 3 + int(cyc(t, 2) * 3)
            d.ellipse([rx - 4 - rr, ry + 1, rx + 6 + rr, ry + 4], outline=rgba("#d8c8e0"))
            d.ellipse([rx - 4, ry - 3, rx + 6, ry + 3], fill=rgba("#6e5e74"))
            d.line([rx - 2, ry - 3, rx + 3, ry - 3], fill=rgba("#a08aa0"))
        f.flush()

    def _foreground(self, f, t):
        d = f.draw()
        # fish jump every 20 s (t%20 in 12..13.4)
        ft = t % 20 - 12
        if 0 <= ft <= 1.4:
            k = ft / 1.4
            fxp, fyp = 156 + 26 * k, 160 - 26 * 4 * k * (1 - k)
            sp = fish() if k < 0.5 else fish().rotate(0)
            f.put(sp, fxp, fyp)
            for sx in (156, 182):
                if abs(fxp - sx) < 6:
                    for i in range(5):
                        d.point((sx - 4 + i * 2, 158 - (i % 2) * 2), fill=rgba("#ffffff"))
        # blue Blok fishing from the rock
        bx, by = 56, 131
        draw_blok(f, "blue", bx, by, t, eyes=1, blink_phase=0.2)
        d = f.draw()
        tip = (bx + 46, by - 2 + wave(t, 4))
        d.line([bx + 26, by + 22, tip[0], tip[1]], fill=rgba("#8a5a2b"), width=1)
        d.line([bx + 25, by + 22, bx + 30, by + 18], fill=rgba("#5a3a1a"), width=2)
        bite = (t % 15) > 13.6
        bob_y = 156 + (2 if bite else round(wave(t, 2)))
        bob_x = bx + 58
        d.line([tip[0], tip[1], bob_x, bob_y], fill=rgba("#f4f0e6"))
        d.rectangle([bob_x - 1, bob_y - 2, bob_x + 1, bob_y], fill=rgba("#ec4a35"))
        d.rectangle([bob_x - 1, bob_y + 1, bob_x + 1, bob_y + 1], fill=rgba("#ffffff"))
        if bite:
            d.ellipse([bob_x - 5, bob_y + 1, bob_x + 5, bob_y + 3], outline=rgba("#d8c8e0"))
        # baby trike + nest
        f.put(trike(((t / 4 + 0.3) % 1) < 0.05, int(cyc(t, 1) * 2)), 72, 184)
        f.put(nest(), 104, 188)
        wob = 0
        if (t % 5) < 0.6:
            wob = 1 if int(t * 10) % 2 else -1
        f.put(egg(), 108, 189)
        f.put(egg("#ff9fc4"), 120 + wob, 188 - (1 if wob else 0))
        f.put(egg("#8fc8ff"), 114, 186)
        # campfire with seated Bloks
        self._fire(f, t)
        # black Blok meditating, floating above the pillar
        mby = 121 + round(2 * wave(t, 4))
        d = f.draw()
        shadow_ellipse(f, 292, 150, 7 - round(wave(t, 4)), 1, "#4e4058")
        draw_blok(f, "black", 278, mby, t, eyes="happy", wind=0.8)
        d = f.draw()
        for k in range(3):
            ang = TAU * (cyc(t, 6) + k / 3)
            d.point((292 + round(18 * np.cos(ang)), mby + 16 + round(6 * np.sin(ang))), fill=rgba("#ffe08a"))
        # sign + foreground flora
        f.put(sign(), 312, 164)
        f.put(palm(t, (8, 220), (12, 170), (22, 112), [(190, 34, 0.7), (215, 32, 0.6), (245, 26, 0.5), (275, 22, 0.4),
                                                         (305, 26, 0.5), (335, 32, 0.6), (355, 34, 0.7)], col=TREEFERN, nuts=False, L=40), 0, 0)
        f.put(fern(t, (370, 216), [(200, 30, 0.5), (225, 34, 0.4), (250, 32, 0.3), (275, 28, 0.25), (300, 30, 0.35), (330, 30, 0.5)],
                   phase=1.1, col=GFERN, light="#b8d870"), 0, 0)
        f.put(fern(t, (250, 218), [(215, 20, 0.5), (245, 22, 0.3), (285, 22, 0.3), (320, 20, 0.5)], phase=2.4, col=GFERN, light="#b8d870"), 0, 0)
        f.put(fern(t, (38, 218), [(220, 22, 0.4), (255, 24, 0.3), (290, 24, 0.3), (325, 22, 0.5)], phase=0.4, col=GFERN, light="#b8d870"), 0, 0)
        # fireflies
        d = f.draw()
        for (x0, y0, ax, ay, tx, ty, ph, tb) in self.flies:
            x = x0 + ax * wave(t, tx, ph)
            y = y0 + ay * wave(t, ty, ph * 2)
            v = wave(t, tb, ph * 3)
            if v > 0.1:
                d.point((x, y), fill=rgba("#fff6a0"))
                if v > 0.7:
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        d.point((x + dx, y + dy), fill=rgba("#e0c040"))

    def _fire(self, f, t):
        cx, cy = FIRE
        d = f.draw()
        # log seats
        for (lx, ly) in ((146, 200), (222, 200)):
            d.rounded_rectangle([lx, ly, lx + 30, ly + 7], radius=3, fill=rgba("#8a5a2b"), outline=rgba(INK))
            d.ellipse([lx + 25, ly, lx + 31, ly + 7], fill=rgba("#d0a060"), outline=rgba(INK))
            d.point((lx + 28, ly + 3), fill=rgba("#8a5a2b"))
            d.line([lx + 3, ly + 2, lx + 20, ly + 2], fill=rgba("#a8743c"))
        draw_blok(f, "red", 150, 174, t, eyes=1, blink_phase=0.7)
        draw_blok(f, "pink", 220, 174, t, eyes=1, flipx=True, blink_phase=0.1)
        d = f.draw()
        # marshmallow stick
        d.line([226, 192, cx + 7, cy - 9], fill=rgba("#8a5a2b"))
        d.rectangle([cx + 4, cy - 12, cx + 7, cy - 9], fill=rgba("#fff6ec"), outline=rgba(INK))
        d.line([cx + 5, cy - 9, cx + 6, cy - 9], fill=rgba("#e0a050"))
        # stones + logs
        for i in range(9):
            ang = np.pi * (0.05 + 0.9 * i / 8)
            sx, sy = cx + 13 * np.cos(ang + np.pi), cy + 3 + 3 * np.sin(ang) * 0 + 2
            d.ellipse([sx - 3, sy - 2, sx + 3, sy + 2], fill=rgba("#8a7a8a"), outline=rgba(INK))
        d.line([cx - 8, cy + 2, cx + 8, cy - 1], fill=rgba("#6b4220"), width=3)
        d.line([cx - 8, cy - 1, cx + 8, cy + 2], fill=rgba("#7a4a22"), width=3)
        # flames: per-column height with 0.5/0.75/1.5 s flicker
        for dx in range(-7, 8):
            hgt = (16 - 0.28 * dx * dx) * (0.78 + 0.12 * wave(t, 0.5, dx * 1.7) + 0.1 * wave(t, 0.75, dx * 0.9))
            for k in range(int(max(0, hgt))):
                frac = k / max(hgt, 1)
                col = "#fff6c4" if frac < 0.25 and abs(dx) < 3 else "#ffd23f" if frac < 0.5 else "#ff8a2a" if frac < 0.8 else "#e8402f"
                d.point((cx + dx, cy - 1 - k), fill=rgba(col))
        # sparks rising
        for i in range(7):
            a = cyc(t, (1.5, 2, 2.5, 3)[i % 4], i / 7)
            sx = cx - 4 + i * 1.3 + 4 * np.sin(a * 5 + i)
            sy = cy - 14 - 30 * a
            if a < 0.85:
                d.point((sx, sy), fill=rgba("#ffd23f" if a < 0.5 else "#ff8a2a"))

    # ------------------------------------------------------------ audio
    def audio(self):
        """River + waterfall (right), campfire crackle (centre), crickets/insects, distant volcano
        rumble, birdsong, brachiosaurus footfalls panned with its walk, T-Rex roar at 28 s with birds
        scattering, pterosaur calls, fish splashes and the bobber plop — all on their on-screen frames."""
        from engine import audio as A
        T = A.T
        buf = np.zeros((2, A.N))
        for ch in (0, 1):
            river = A.colored(0.5, 200, 5000, seed=3 + ch) * (0.9 + 0.1 * np.sin(TAU * T / 5 + ch)) * 0.22
            fall = A.colored(0.2, 300, 8000, seed=7 + ch) * (0.10 if ch == 0 else 0.30)
            rumble = A.colored(1.5, 25, 120, seed=11 + ch) * (0.10 if ch == 0 else 0.04)
            fire_low = A.colored(1.2, 60, 400, seed=13 + ch) * (0.8 + 0.2 * np.sin(TAU * T / 0.75)) * 0.05
            insects = (A.colored(0.0, 5200, 7200, seed=17 + ch) * (0.5 + 0.5 * np.sin(TAU * 35 * T))
                       * (0.25 + 0.75 * np.clip(np.sin(TAU * T / 20 + ch * 2), 0, 1)) * 0.03)
            buf[ch] += river + fall + rumble + fire_low + insects
        A.bed(buf, A.crackle_bed(21) * 0.09, A.crackle_bed(22) * 0.07, 1.0)
        swell = 0.4 + 0.6 * (np.sin(TAU * T / 12) + 1) / 2
        A.bed(buf, A.cricket_bed(31, 0.62, 4300) * swell * 0.05, A.cricket_bed(32, 0.71, 4650) * swell[::-1] * 0.04, 1.0)
        r = np.random.default_rng(40)
        for i, t0 in enumerate(np.sort(r.uniform(0, DUR, 9))):
            if not (ROAR_T - 1 < t0 < ROAR_T + 6):
                A.place(buf, A.chirp_seq(50 + i), t0, 0.12, pan=r.uniform(-0.8, 0.8))
        # brachiosaurus footfalls every 1 s, panned + faded with its position
        for k in range(60):
            t0 = k + 0.25
            x = cyc(t0, 60) * 520 - 116 + 56
            vis = np.clip((x + 30) / 60, 0, 1) * np.clip((440 - x) / 60, 0, 1)
            if vis > 0:
                A.place(buf, A.thump(k, 44 if k % 2 else 50), t0, 0.5 * vis, pan=(x - 192) / 192)
        A.place(buf, A.roar(5), ROAR_T - 0.1, 1.0, pan=-0.35)
        A.place(buf, A.flutter(6), ROAR_T + 0.2, 0.25, pan=-0.25)
        for t0, pan in ((12.1, 0.0), (42.1, 0.1), (39.1, -0.1)):
            A.place(buf, A.screech(int(t0)), t0, 0.6, pan=pan)
        for base_t in (0, 20, 40):
            A.place(buf, A.splash(base_t, 0.8), base_t + 12.0, 1.0, pan=-0.15)
            A.place(buf, A.splash(base_t + 1, 0.7), base_t + 13.4, 0.75, pan=-0.05)
        for k in range(4):
            A.place(buf, A.plop(k), 13.6 + 15 * k, 0.9, pan=-0.45)
        return A.master(buf)
