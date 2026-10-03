"""NINJA-BLOKS · Snowy Christmas Cabin — 60 s seamless loop.

Periods (all divide 60 s): snowfall 3 layers (12/18/26 screens per minute) · light chase 2 s ·
window fire flicker 0.5/0.75 s · chimney smoke 1 puff/1.5 s · Pink's sled run 15 s ·
Red pats the snowman 2 s · Blue hops 4 s · Black hangs lights 2 s · bunny 30 s.
Event: Santa's sleigh crosses the moon 20-34 s (sleigh bells).
"""
import numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw
from engine.px import (W, H, S, INK, TAU, DUR, rgba, hx, vgrad, radial_dither, bayer, sprite, outline, rim,
                       up, flip, wave, cyc, Frame, _shift)
from engine.bloks import draw_blok, draw_scarf, BLOKS, GOLD
from scenes.common import draw_bug, shadow_ellipse, _pad, Snow, snowy_sign

MOON = (304, 38)
SLEIGH_T = (20.0, 34.0)
SLED_P = 15
BULBS = ["#ff4a3a", "#3aff7a", "#ffd23f", "#3ab0ff"]

rng = np.random.default_rng(51)


def roof_line(x):
    """Lower edge of the snowy roof (for the string lights)."""
    return 122 - (62 - abs(x - 214)) * (36 / 62) if abs(x - 214) <= 62 else 122


# ---------------------------------------------------------------- sprites
def pine(d, x, base, h, w, dark="#1c3646", snow="#d8e4f8"):
    tiers = 4
    for i in range(tiers):
        ty = base - h + i * h / tiers
        tw = w * (0.35 + 0.65 * (i + 1) / tiers)
        d.polygon([(x, ty), (x - tw / 2, ty + h / tiers + 3), (x + tw / 2, ty + h / tiers + 3)], fill=hx(dark))
        d.line([(x - tw / 2 + 1, ty + h / tiers + 2), (x, ty), (x + tw / 4, ty + h / tiers * 0.5)], fill=hx(snow))
    d.rectangle([x - 1, base, x + 1, base + 2], fill=hx("#3a2a2a"))


@lru_cache(maxsize=None)
def snowman():
    im = Image.new("RGBA", (40, 48), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for (cx, cy, r) in ((20, 37, 10), (20, 22, 8), (20, 10, 6)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=rgba("#f4f8ff"))
    a = np.array(im)
    m = a[..., 3] > 0
    a[m & ~_shift(m, 0, -2)] = rgba("#c4d4f0")
    a[m & ~_shift(m, -2, 0)] = rgba("#c4d4f0")
    im = Image.fromarray(a, "RGBA")
    d = ImageDraw.Draw(im)
    c = BLOKS["red"]
    d.rectangle([14, 6, 26, 7], fill=rgba(c["B"]))
    d.point((20, 6), fill=rgba(GOLD))
    d.line([27, 7, 30, 10], fill=rgba(c["B"])); d.line([27, 6, 31, 7], fill=rgba(c["b"]))
    d.point((18, 10), fill=rgba(INK)); d.point((22, 10), fill=rgba(INK))
    d.polygon([(20, 12), (26, 13), (20, 14)], fill=rgba("#ff8a2a"))
    for x in (17, 19, 21, 23):
        d.point((x, 15 + (x in (19, 21))), fill=rgba(INK))
    for y in (20, 24, 28):
        d.point((20, y), fill=rgba(INK))
    d.line([12, 22, 3, 15], fill=rgba("#6a4a2e")); d.line([5, 17, 3, 19], fill=rgba("#6a4a2e"))
    d.line([28, 22, 37, 16], fill=rgba("#6a4a2e")); d.line([35, 17, 37, 19], fill=rgba("#6a4a2e"))
    return outline(im)


@lru_cache(maxsize=None)
def sled():
    rows = [
        "..KKKKKKKKKKKKKKKK..",
        ".KRRRRRRRRRRRRRRRRK.",
        "..KKKKKKKKKKKKKKKK..",
        "...G...........G....",
        "KGGGGGGGGGGGGGGGGG..",
        ".KK.................",
    ]
    return sprite(rows, {"K": INK, "R": "#c8343a", "G": "#c9ccd8"})


@lru_cache(maxsize=None)
def bunny(f):
    rows = [["..W.W..", "..W.W..", ".WWWW..", "WWEWW..", ".WWWWW.", "..W..WW"],
            ["...W.W.", "..W.W..", ".WWWW..", "WWEWW..", ".WWWWWW", ".W....W"]][f]
    return outline(_pad(sprite(rows, {"W": "#f4f8ff", "E": INK})), "#5a6a9a")


@lru_cache(maxsize=None)
def sleigh(f):
    """Santa's sleigh and four reindeer in silhouette (crossing the moon)."""
    im = Image.new("RGBA", (82, 22), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = "#1a2246"
    for i in range(4):
        x = 4 + i * 11
        leg = 1 if (f + i) % 2 else -1
        d.ellipse([x, 10, x + 8, 14], fill=rgba(c))
        d.line([x + 1, 14, x + 1 + leg, 18], fill=rgba(c)); d.line([x + 6, 14, x + 6 - leg, 18], fill=rgba(c))
        d.line([x, 11, x - 2, 7], fill=rgba(c))
        d.rectangle([x - 4, 5, x - 1, 7], fill=rgba(c))
        d.line([x - 2, 5, x - 1, 2], fill=rgba(c)); d.line([x - 3, 5, x - 5, 2], fill=rgba(c))
    d.point((0, 6), fill=rgba("#ff3a3a"))
    d.line([40, 12, 50, 13], fill=rgba(c))
    d.polygon([(50, 8), (72, 8), (76, 4), (78, 6), (74, 15), (52, 15)], fill=rgba(c))
    d.line([48, 17, 78, 17], fill=rgba(c)); d.line([48, 17, 46, 15], fill=rgba(c))
    d.ellipse([58, 1, 66, 9], fill=rgba(c))
    d.ellipse([66, 2, 74, 9], fill=rgba(c))
    im = rim(im, "#6a80c0", dy=1, skip=("#ff3a3a",))
    return up(im)


# ---------------------------------------------------------------- scene
class Cabin:
    name = "cabin"

    def __init__(self):
        self.base = up(Image.fromarray(self._static(), "RGB"))
        self.snow = Snow(52)
        self.stars = [(int(rng.uniform(0, W)), int(rng.uniform(2, 60)), rng.choice([2, 3, 4, 5]), rng.uniform(0, TAU)) for _ in range(36)]
        self.glints = [(int(rng.uniform(0, W)), int(rng.uniform(150, H - 2)), rng.choice([1, 1.5, 2, 3]), rng.uniform(0, TAU)) for _ in range(40)]
        self.bulbs = [(x, roof_line(x)) for x in range(154, 276, 6)]

    def _static(self):
        img = np.zeros((H, W, 3), np.uint8)
        img[:] = vgrad(["#0a1030", "#121a44", "#1c2a5a", "#2a3c74", "#3e5290", "#5a6ea8"], W, 132, ease=1.1)[np.minimum(np.arange(H), 131)]
        radial_dither(img, MOON[0], MOON[1], 56, "#26386e", 12)
        radial_dither(img, MOON[0], MOON[1], 38, "#3a4e88", 8)
        radial_dither(img, MOON[0], MOON[1], 26, "#5a72aa", 5)
        im = Image.fromarray(img)
        d = ImageDraw.Draw(im)
        mx, my = MOON
        d.ellipse([mx - 18, my - 18, mx + 18, my + 18], fill=hx("#eef4ff"))
        for (cx, cy, r) in ((-6, -4, 4), (6, 5, 5), (8, -9, 2)):
            d.ellipse([mx + cx - r, my + cy - r, mx + cx + r, my + cy + r], fill=hx("#d6e2f8"))
        a = np.array(im)
        xs = np.arange(W)
        yy = np.arange(H)[:, None]
        rg = 96 - 20 * np.abs(np.sin(xs / 48.0 + 0.8)) - 7 * np.sin(xs / 17.0) ** 2
        mm = (yy >= rg[None, :]) & (yy < 132)
        a[mm] = hx("#5a6ea8")
        a[mm & (yy < rg[None, :] + 5)] = hx("#c8d8f4")
        a[mm & (yy < rg[None, :] + 1)] = hx("#f0f6ff")
        im = Image.fromarray(a)
        d = ImageDraw.Draw(im)
        r = np.random.default_rng(3)
        for x in range(-6, W + 6, 7):
            pine(d, x + r.integers(-2, 3), 128 + r.integers(-2, 3), r.integers(16, 26), r.integers(9, 13), "#22405a", "#b8cae8")
        for x in range(-4, W + 6, 11):
            if 150 < x < 280:
                continue
            pine(d, x + r.integers(-3, 4), 140 + r.integers(-2, 3), r.integers(22, 32), r.integers(12, 16))
        a = np.array(im)
        a[136:] = vgrad(["#b8c8ea", "#cfdcf4", "#e2eafa", "#eef3fd", "#f6f9ff"], W, H - 136)
        bumps = 136 + 2 * np.sin(xs / 19.0) + 1.5 * np.sin(xs / 7.0)
        # sled hill on the right
        hill = np.where(xs > 276, np.clip(176 - (xs - 276) * 0.42, 140, 176), 300)
        hm = (yy >= hill[None, :]) & (yy < H)
        a[hm] = hx("#eaf0fc")
        a[hm & (yy < hill[None, :] + 1)] = hx("#ffffff")
        a[hm & (yy >= hill[None, :] + 1) & (yy < hill[None, :] + 3) & (xs[None, :] < 360)] = hx("#c8d6f0")
        shadow = hm & (np.clip((xs[None, :] - 300) / 120.0 * 0.5, 0, 0.5) > bayer(H, W)) & (yy > hill[None, :] + 3)
        a[shadow] = hx("#d6e2f6")
        # warm window + door light pools on the snow
        for (cx, cy, rr) in ((181, 176, 26), (247, 176, 26), (214, 176, 18)):
            dd = np.sqrt((xs[None, :] - cx) ** 2 + ((yy - cy) * 2.6) ** 2)
            a[(yy > 168) & (np.clip((rr - dd) / 8, 0, 1) > bayer(H, W))] = hx("#f6e6c6")
            a[(yy > 168) & (np.clip((rr * 0.55 - dd) / 6, 0, 1) > bayer(H, W))] = hx("#fbd99a")
        # footprints toward the door
        for i in range(10):
            x, y = 214 - 6 + (i % 2) * 6 - i * 3, 176 + i * 4
            if y < H - 2:
                a[y, x:x + 2] = hx("#aebde0")
        im = Image.fromarray(a)
        im.paste(self._cabin(), (0, 0), self._cabin())
        return np.array(im)

    @lru_cache(maxsize=None)
    def _cabin(self):
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        # walls (logs)
        d.polygon([(160, 122), (214, 90), (268, 122), (268, 170), (160, 170)], fill=rgba("#7a4a2e"))
        for y in range(124, 170, 5):
            d.line([160, y, 268, y], fill=rgba("#5a3420"))
            d.line([160, y + 1, 268, y + 1], fill=rgba("#9a6238"))
        for y in range(124, 170, 5):
            d.ellipse([157, y, 162, y + 4], fill=rgba("#b07a48"), outline=rgba("#5a3420"))
            d.ellipse([266, y, 271, y + 4], fill=rgba("#b07a48"), outline=rgba("#5a3420"))
        # chimney (behind the roof snow)
        d.rectangle([246, 92, 256, 112], fill=rgba("#6a5a6a"))
        for y in range(94, 112, 4):
            d.line([246, y, 256, y], fill=rgba("#4a3e4a"))
        d.rectangle([244, 88, 258, 92], fill=rgba("#f4f8ff"))
        # snowy roof with overhang
        d.polygon([(148, 124), (214, 84), (280, 124), (276, 127), (214, 90), (152, 127)], fill=rgba("#f4f8ff"))
        d.line([(148, 124), (214, 84), (280, 124)], fill=rgba("#ffffff"))
        d.line([(152, 127), (214, 90), (276, 127)], fill=rgba("#b8c8e8"))
        for x in range(154, 276, 4):
            ln = 1 + (x * 7 % 5)
            y0 = roof_line(x) + 4
            d.line([x, y0, x, y0 + ln], fill=rgba("#cfeaff"))
        # windows + door
        for (x0, x1) in ((170, 192), (236, 258)):
            d.rectangle([x0, 130, x1, 148], fill=rgba("#ffcf6a"))
            d.rectangle([x0 - 1, 129, x1 + 1, 149], outline=rgba("#4a2a18"))
            d.rectangle([x0 - 2, 149, x1 + 2, 151], fill=rgba("#f4f8ff"))
        d.rectangle([206, 142, 222, 170], fill=rgba("#5a3020"))
        d.line([206, 142, 222, 142], fill=rgba("#3a1e14"))
        d.point((219, 157), fill=rgba(GOLD))
        d.ellipse([209, 129, 219, 139], outline=rgba("#2a8a4a"), width=2)
        d.point((214, 138), fill=rgba("#ec4a35")); d.point((213, 139), fill=rgba("#ec4a35")); d.point((215, 139), fill=rgba("#ec4a35"))
        # snow drift along the base
        d.ellipse([150, 164, 280, 176], fill=rgba("#eef3fd"))
        return outline(im)

    # ------------------------------------------------------------ per frame
    def frame(self, t):
        t = t % DUR
        f = Frame(self.base)
        d = f.draw()
        for (x, y, p, ph) in self.stars:
            if wave(t, p, ph) > -0.2 and (x - MOON[0]) ** 2 + (y - MOON[1]) ** 2 > 30 ** 2:
                d.point((x, y), fill=rgba("#ffffff" if wave(t, p, ph) > 0.7 else "#9aaee0"))
        f.flush()
        if SLEIGH_T[0] <= t <= SLEIGH_T[1]:
            k = (t - SLEIGH_T[0]) / (SLEIGH_T[1] - SLEIGH_T[0])
            f.smooth(sleigh(int(t * 6) % 2), 430 - 560 * k, 30 - 10 * np.sin(np.pi * k) + 2 * wave(t, 2))
        self.snow.draw(f, t, 0)
        # bunny hopping across the far field
        bx = cyc(t, 30) * 440 - 30
        hop = abs(np.sin(TAU * t / 0.6)) * 3
        f.put(bunny(int(cyc(t, 0.6) * 2)), bx, 136 - hop)
        # windows: fire flicker + tree lights
        d = f.draw()
        fl = wave(t, 0.5) + 0.6 * wave(t, 0.75, 1)
        d.rectangle([237, 140, 257, 148], fill=rgba("#ffb040" if fl > 0 else "#ff9030"))
        d.rectangle([241, 142, 253, 148], fill=rgba("#ff7a2a"))
        for i, fx in enumerate(range(242, 253, 2)):
            h_ = 3 + int(2 * (1 + wave(t, 0.5, i)))
            d.line([fx, 147, fx, 147 - h_], fill=rgba("#ffd23f"))
        d.polygon([(181, 132), (175, 147), (187, 147)], fill=rgba("#2a6a3a"))
        for i, (px, py) in enumerate(((181, 135), (179, 139), (183, 141), (178, 144), (184, 145))):
            d.point((px, py), fill=rgba(BULBS[(i + int(t * 2)) % 4]))
        d.line([170, 139, 192, 139], fill=rgba("#4a2a18")); d.line([181, 130, 181, 148], fill=rgba("#4a2a18"))
        d.line([236, 139, 258, 139], fill=rgba("#4a2a18")); d.line([247, 130, 247, 148], fill=rgba("#4a2a18"))
        # door lantern
        lit = "#ffd23f" if fl > -0.5 else "#ffb030"
        d.rectangle([224, 146, 227, 150], fill=rgba(INK)); d.rectangle([225, 147, 226, 149], fill=rgba(lit))
        # chimney smoke
        for k in range(6):
            a = cyc(t, 10, k / 6)
            r = 2 + 4 * a
            px_, py = 251 + 18 * a ** 1.2 + 2 * np.sin(a * 6 + k), 86 - 30 * a
            d.ellipse([px_ - r, py - r * 0.8, px_ + r, py + r * 0.8], fill=rgba(["#8a96b8", "#7a86aa", "#6a769c"][min(2, int(a * 3))]))
        # string lights chasing along the roof (2 s)
        for i, (x, y) in enumerate(self.bulbs):
            on = (i + int(cyc(t, 2) * 4)) % 4
            c = BULBS[i % 4] if on != 0 else "#3a3a50"
            d.point((x, y + 3), fill=rgba(INK))
            d.rectangle([x, y + 4, x + 1, y + 5], fill=rgba(c))
        f.flush()
        # Black on the ladder, hanging lights
        d = f.draw()
        d.line([148, 172, 156, 118], fill=rgba("#8a5a2b"), width=2)
        d.line([158, 172, 164, 118], fill=rgba("#8a5a2b"), width=2)
        for y in range(124, 172, 8):
            x0 = 148 + (172 - y) * 8 / 54
            d.line([x0, y, x0 + 9, y], fill=rgba("#a8743c"))
        up_ = cyc(t, 2) < 0.5
        draw_blok(f, "black", 140, 98, t, eyes="happy" if up_ else 1, arms="up" if up_ else "down", blink_phase=0.4, wind=1.2)
        draw_scarf(f, 140, 98, t, col="#1ec8b4")
        # snowman, Red patting it, Blue hopping
        shadow_ellipse(f, 100, 193, 14, 2, "#aebde0")
        f.put(snowman(), 80, 146)
        pat = cyc(t, 2) < 0.5
        draw_blok(f, "red", 50, 164, t, eyes="happy" if pat else 1, arms="up" if pat else "down", blink_phase=0.1)
        draw_scarf(f, 50, 164, t, col="#2a8a4a", stripe="#ffffff")
        if pat:
            d = f.draw()
            for i in range(4):
                d.point((84 + i * 2, 168 - (int(t * 10) + i) % 4), fill=rgba("#ffffff"))
        hop = max(0.0, np.sin(TAU * t / 4)) * 9 if cyc(t, 4) < 0.5 else 0
        shadow_ellipse(f, 140, 193, 10 - hop * 0.4, 2, "#aebde0")
        draw_blok(f, "blue", 126, 164 - hop, t, eyes="happy" if hop > 2 else 1, flipx=True, arms="up" if hop > 2 else "down", blink_phase=0.6)
        draw_scarf(f, 126, 164 - hop, t, flipx=True, col="#ffd23f", stripe="#ec4a35")
        # Pink sledding (15 s: slide 0-2.5, rest 2.5-4, walk back up 4-15)
        self._sled(f, t)
        f.put(snowy_sign(), 324, 171)
        # sparkles + near snowfall
        d = f.draw()
        for (x, y, p, ph) in self.glints:
            if wave(t, p, ph) > 0.85:
                d.point((x, y), fill=rgba("#ffffff"))
                d.point((x - 1, y), fill=rgba("#cfe0ff")); d.point((x + 1, y), fill=rgba("#cfe0ff"))
        self.snow.draw(f, t, 1)
        self.snow.draw(f, t, 2)
        draw_bug(f)
        return f.out()

    @staticmethod
    def sled_pos(t):
        k = t % SLED_P
        top, bot = (356, 118), (290, 152)
        if k < 2.5:
            u = (k / 2.5) ** 1.6
            return top[0] + (bot[0] - top[0]) * u, top[1] + (bot[1] - top[1]) * u, "slide", u
        if k < 4:
            return bot[0], bot[1], "rest", 1.0
        u = (k - 4) / (SLED_P - 4)
        return bot[0] + (top[0] - bot[0]) * u, bot[1] + (top[1] - bot[1]) * u, "walk", u

    def _sled(self, f, t):
        x, y, mode, u = self.sled_pos(t)
        d = f.draw()
        if mode == "slide":
            for i in range(8):
                sx = x + 22 + i * 2
                d.point((sx, y + 32 - (i % 3) + i * 0.5), fill=rgba("#ffffff"))
            f.put(sled(), x - 2, y + 26)
            draw_blok(f, "pink", x, y - 2, t, eyes="happy", mouth="open", arms="up", blink_phase=0.2, wind=1.8)
            draw_scarf(f, x, y - 2, t, col="#8a3ff0", stripe="#ffd23f")
        elif mode == "rest":
            f.put(sled(), x - 2, y + 26)
            draw_blok(f, "pink", x, y - 2, t, eyes="happy", blink_phase=0.2)
            draw_scarf(f, x, y - 2, t, col="#8a3ff0", stripe="#ffd23f")
        else:
            step = int(t * 4) % 2
            f.put(sled(), x + 24, y + 28 - 2)
            d.line([x + 22, y + 20, x + 26, y + 29], fill=rgba("#e8e0d0"))
            draw_blok(f, "pink", x, y - step, t, eyes=1, flipx=True, blink_phase=0.2)
            draw_scarf(f, x, y - step, t, flipx=True, col="#8a3ff0", stripe="#ffd23f")

    # ------------------------------------------------------------ audio
    def audio(self):
        from engine import audio as A
        T = A.T
        buf = np.zeros((2, A.N))
        for ch in (0, 1):
            wind = A.colored(1.2, 100, 1200, seed=600 + ch) * (0.45 + 0.55 * np.clip(np.sin(TAU * T / 20 + ch * 1.4), 0, 1) ** 1.5) * 0.22
            whistle = A.colored(0.0, 900, 1300, seed=602 + ch) * np.clip(np.sin(TAU * T / 30 + ch), 0, 1) ** 3 * 0.03
            hush = A.colored(0.0, 4000, 11000, seed=604 + ch) * 0.02
            buf[ch] += wind + whistle + hush
        fire = A.band(A.crackle_bed(606, 5.0), 200, 3500, circular=True)
        fire_low = A.colored(1.4, 50, 300, seed=607) * (0.8 + 0.2 * np.sin(TAU * T / 0.75))
        A.bed(buf, fire * 0.05 + fire_low * 0.05, fire * 0.07 + fire_low * 0.06, 1.0)
        A.place_sweep(buf, A.pk(A.jingle(5, SLEIGH_T[1] - SLEIGH_T[0])), SLEIGH_T[0], 0.25, 0.8, -0.8)
        for c in range(4):
            t0 = c * SLED_P
            A.place(buf, A.pk(A.swish(610 + c, 2.6)), t0, 0.35, pan=0.7)
            for k in range(22):
                st = t0 + 4 + k * 0.5
                A.place(buf, A.pk(A.crunch(620 + c * 30 + k)), st, 0.2, pan=0.55 + 0.2 * k / 22)
        for k in range(30):
            A.place(buf, A.pk(A.thud(700 + k)), 2 * k + 0.05, 0.18, pan=-0.45)
            A.place(buf, A.pk(A.crunch(740 + k)), 2 * k + 0.05, 0.15, pan=-0.45)
        for k in range(15):
            A.place(buf, A.pk(A.crunch(800 + k)), 4 * k + 2.0, 0.3, pan=-0.25)
        return A.master(buf)
