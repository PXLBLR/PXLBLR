"""NINJA-BLOKS · Rainy Neon Ramen Stand — 60 s seamless loop.

Rain layers fall exactly k screen-heights per minute, so they loop. Periods: lanterns
4 s · noren flutter 2 s · slurps 6 s (Red at +1 s, Blue at +4 s) · chef strainer 3 s ·
steam 3 s · drips 1.5/2 s · puddle rings 1.5-3 s · cat tail 4 s · window lights 5-20 s.
Events: neon "L" flickers at 11 s and 41 s, sign dips at 52 s, train overhead 28-33 s,
wet-tyre car pass 12 s + 47 s (audio only).
"""
import numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw
from engine.px import (W, H, S, INK, TAU, DUR, rgba, hx, vgrad, radial_dither, bayer, sprite, outline, rim,
                       up, flip, wave, cyc, Frame, _shift, text_mask, F57, F35)
from engine.bloks import draw_blok, blok_icon
from scenes.common import draw_bug, _pad

GROUND = 188
TRAIN_T = (28.0, 33.0)
FLICKER = ((11.0, 11.5), (41.0, 41.3), (41.6, 41.9))
DIP_T = (52.0, 52.15)
CAR_T = (12.0, 47.0)
PINK, CYAN, YELLOW, LANTERN = "#ff4fa8", "#3ff0ff", "#ffd23f", "#ff4a3a"

rng = np.random.default_rng(41)


# ---------------------------------------------------------------- sprites
@lru_cache(maxsize=None)
def neon_text(s, col, glow, font="F57", vertical=False, off_idx=None):
    fnt = F57 if font == "F57" else F35
    if vertical:
        ms = [text_mask(ch, fnt) for ch in s]
        w = max(m.shape[1] for m in ms)
        h = sum(m.shape[0] + 2 for m in ms)
        m = np.zeros((h, w), bool)
        y = 0
        for i, mm in enumerate(ms):
            if i != off_idx:
                m[y:y + mm.shape[0], (w - mm.shape[1]) // 2:(w - mm.shape[1]) // 2 + mm.shape[1]] = mm
            y += mm.shape[0] + 2
    else:
        m = text_mask(s, fnt)
        if off_idx is not None:
            gw = 6 if font == "F57" else 4
            m[:, off_idx * gw:off_idx * gw + gw - 1] = False
    h, w = m.shape
    a = np.zeros((h + 4, w + 4, 4), np.uint8)
    mm = np.zeros((h + 4, w + 4), bool)
    mm[2:h + 2, 2:w + 2] = m
    g = mm.copy()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
        g |= _shift(mm, dy, dx)
    a[g] = rgba(glow)
    a[mm] = rgba(col)
    core = mm & _shift(mm, 0, 1) & _shift(mm, 0, -1)
    a[core] = rgba("#ffffff")
    return Image.fromarray(a, "RGBA")


@lru_cache(maxsize=None)
def lantern(lit):
    rows = [
        "..KKKK..",
        ".KRRRRK.",
        "KRrRRrRK",
        "KRrRYrRK",
        "KRrRRrRK",
        "KRrRRrRK",
        ".KRRRRK.",
        "..KKKK..",
    ]
    return outline(_pad(sprite(rows, {"K": INK, "R": LANTERN if lit else "#d83a32", "r": "#b02a28", "Y": "#ffe08a"})))


@lru_cache(maxsize=None)
def bowl():
    rows = ["KWWWWWWK", ".KRRRRK.", "..KKKK.."]
    return sprite(rows, {"K": INK, "W": "#f4e6c8", "R": "#ec4a35"})


@lru_cache(maxsize=None)
def cat(tail):
    rows = [
        "..K.K.........",
        ".KGKGK........",
        ".KGGGKKKKKK...",
        "KGEGEGGGGGGK..",
        "KGGGGGGGGGGGKK",
        ".KKKKKKKKKKKK.",
    ]
    if tail:
        rows[3] = "KGEGEGGGGGGKKK"
    return sprite(rows, {"K": INK, "G": "#f2a04a", "E": "#2a2a40"})


@lru_cache(maxsize=None)
def umbrella():
    im = Image.new("RGBA", (40, 16), (0, 0, 0, 0))
    a = np.zeros((16, 40, 4), np.uint8)
    for y in range(16):
        for x in range(40):
            dx, dy = (x - 19.5) / 19, (y - 13) / 12
            if dy <= 0.05 and dx * dx + dy * dy <= 1:
                a[y, x] = rgba("#cfe8ff" if (x + y) % 2 == 0 else "#7ab0e0")
    im = Image.fromarray(a, "RGBA")
    im = rim(im, "#ffffff", dy=1)
    return outline(im, "#3a4a7a")


@lru_cache(maxsize=None)
def train_car(lit):
    w, h = 92, 16
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([1, 2, w - 2, h - 2], radius=3, fill=rgba("#c8ccd8"))
    d.rectangle([1, h - 6, w - 2, h - 5], fill=rgba("#3a92f0"))
    for x in range(6, w - 8, 10):
        d.rectangle([x, 5, x + 6, 8], fill=rgba("#ffe8a0" if lit else "#c8b070"))
    d.line([w // 2 - 6, 1, w // 2 + 6, 1], fill=rgba("#5a5e78"))
    return outline(im)


# ---------------------------------------------------------------- scene
class Ramen:
    name = "ramen"

    def __init__(self):
        self.base = up(Image.fromarray(self._static(), "RGB"))
        self.stand = up(self._stand())
        self.rain = []
        for (n, ln, col, ky, kx) in ((80, 3, "#33406c", 50, -4), (60, 5, "#6676aa", 70, -6), (24, 9, "#a6b4e0", 100, -8)):
            vy, vx = H * ky / DUR, W * kx / DUR
            self.rain.append([(rng.uniform(0, W), rng.uniform(0, H)) for _ in range(n)] + [(ln, col, vx, vy)])
        self.splashes = [(rng.uniform(4, W - 4), rng.uniform(GROUND + 2, H - 2), rng.choice([0.5, 0.75, 1, 1.5]), rng.uniform(0, 1)) for _ in range(40)]
        self.windows = [(x, y, rng.choice([5, 6, 10, 12, 15, 20]), rng.uniform(0, TAU), rng.choice(["#ffcf8a", "#bfe8ff", "#ffb070"]))
                        for (x, y) in [(10, 22), (26, 22), (42, 22), (10, 46), (42, 46), (26, 70), (10, 94), (42, 94),
                                       (316, 18), (334, 18), (352, 18), (370, 42), (316, 66), (352, 66), (334, 90), (370, 90)]]
        self.far = [(rng.integers(96, 300), rng.integers(70, 118), rng.choice([3, 4, 5, 6, 10]), rng.uniform(0, TAU)) for _ in range(40)]

    def _static(self):
        img = np.zeros((H, W, 3), np.uint8)
        img[:] = vgrad(["#070a1a", "#0d1228", "#151a38", "#221e46", "#33224e"], W, 140)[np.minimum(np.arange(H), 139)]
        im = Image.fromarray(img)
        d = ImageDraw.Draw(im)
        r = np.random.default_rng(6)
        # far skyline
        x = 80
        while x < 310:
            w = r.integers(14, 30)
            top = r.integers(64, 104)
            d.rectangle([x, top, x + w, 140], fill=hx(r.choice(["#161c3a", "#1a2244", "#141a34"])))
            d.point((x + w // 2, top - 1), fill=hx("#2a3050"))
            x += w + r.integers(-2, 3)
        # elevated track + pillars
        for px in (110, 280):
            d.rectangle([px, 60, px + 7, 150], fill=hx("#20243c"))
            d.line([px, 60, px, 150], fill=hx("#34385a"))
        d.rectangle([0, 52, W, 60], fill=hx("#262a46"))
        d.line([0, 52, W, 52], fill=hx("#4a4e74"))
        d.line([0, 60, W, 60], fill=hx("#14182c"))
        for x in range(4, W, 12):
            d.point((x, 56), fill=hx("#4a4e74"))
        d.line([0, 50, W, 50], fill=hx("#3a3e5a"))
        # buildings left and right
        for (x0, x1) in ((0, 92), (300, W)):
            d.rectangle([x0, 0, x1, GROUND], fill=hx("#1a1f36"))
            for yy in range(4, GROUND, 6):
                d.line([x0, yy, x1, yy], fill=hx("#1e2440"))
            for (wx, wy) in [(10, 22), (26, 22), (42, 22), (10, 46), (26, 46), (42, 46), (10, 70), (26, 70), (42, 70),
                             (10, 94), (26, 94), (42, 94)] if x0 == 0 else [(316, 18), (334, 18), (352, 18), (370, 18),
                                                                              (316, 42), (334, 42), (352, 42), (370, 42),
                                                                              (316, 66), (334, 66), (352, 66), (370, 66),
                                                                              (316, 90), (334, 90), (352, 90), (370, 90)]:
                d.rectangle([wx, wy, wx + 9, wy + 11], fill=hx("#0e1224"))
                d.line([wx, wy + 12, wx + 9, wy + 12], fill=hx("#2c3454"))
        d.line([92, 0, 92, GROUND], fill=hx("#2c3454"))
        d.line([300, 0, 300, GROUND], fill=hx("#2c3454"))
        # pipes + AC units
        d.line([88, 0, 88, GROUND], fill=hx("#2a3050"), width=2)
        for (ax, ay) in ((60, 120), (306, 116), (352, 118)):
            d.rectangle([ax, ay, ax + 14, ay + 9], fill=hx("#3a4060"))
            d.ellipse([ax + 3, ay + 2, ax + 9, ay + 7], outline=hx("#22283e"))
        # vending machine
        d.rectangle([34, 138, 62, GROUND - 1], fill=hx("#d8eefc"))
        d.rectangle([36, 141, 60, 166], fill=hx("#eaf7ff"))
        for row, y in enumerate((143, 151, 159)):
            for i, x in enumerate(range(38, 59, 4)):
                d.rectangle([x, y, x + 2, y + 5], fill=hx(["#ec4a35", "#3a92f0", "#ffd23f", "#1ec8b4", "#ff74b3", "#8a3ff0"][(i + row) % 6]))
        d.rectangle([38, 172, 58, 180], fill=hx("#2a3050"))
        d.rectangle([52, 168, 56, 170], fill=hx("#ffd23f"))
        # ground
        a = np.array(im)
        a[GROUND:] = vgrad(["#141a2e", "#111628", "#0e1222"], W, H - GROUND)
        a[GROUND] = hx("#2a3050")
        for (cx, cy, rx, ry) in ((70, 202, 26, 4), (190, 208, 34, 5), (330, 200, 22, 3)):
            yy, xx = np.mgrid[0:H, 0:W]
            pm = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 < 1
            a[pm] = hx("#1c2444")
        # glow pools on the wet street
        for (cx, cy, rr, col) in ((48, GROUND + 4, 30, "#2a3a5a"), (190, GROUND + 6, 70, "#3a2a34"), (334, GROUND + 4, 30, "#2e3048")):
            yy, xx = np.mgrid[0:H, 0:W]
            dd = np.sqrt((xx - cx) ** 2 + ((yy - cy) * 2.5) ** 2)
            a[(yy > GROUND) & (np.clip((rr - dd) / 12, 0, 1) > bayer(H, W))] = hx(col)
        # street lamp light cone
        yy, xx = np.mgrid[0:H, 0:W]
        cone = (yy > 72) & (yy < GROUND) & (np.abs(xx - 336) < (yy - 66) * 0.32)
        a[cone & (np.clip(0.35 - (yy - 72) / 400, 0, 1) > bayer(H, W))] = hx("#2e3454")
        im = Image.fromarray(a)
        d = ImageDraw.Draw(im)
        d.rectangle([343, 70, 345, GROUND], fill=hx("#2a2e48"))
        d.line([336, 68, 345, 68], fill=hx("#2a2e48"), width=2)
        d.rectangle([331, 68, 341, 71], fill=hx("#3a3e5a"))
        d.line([332, 72, 340, 72], fill=hx("#fff2c0"))
        # crate (cat bed)
        d.rectangle([302, 174, 326, GROUND - 1], fill=hx("#6a4a32"))
        d.line([302, 180, 326, 180], fill=hx("#4a3222"))
        d.line([302, 174, 326, 174], fill=hx("#8a6444"))
        return np.array(im)

    def _stand(self):
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        # interior back wall, warm
        d.rectangle([128, 104, 258, 152], fill=rgba("#5a2e22"))
        a = np.array(im)
        yy, xx = np.mgrid[0:H, 0:W]
        dd = np.sqrt((xx - 192) ** 2 + ((yy - 112) * 1.4) ** 2)
        a[(a[..., 3] > 0) & (np.clip((60 - dd) / 14, 0, 1) > bayer(H, W))] = rgba("#7a4430")
        a[(a[..., 3] > 0) & (np.clip((34 - dd) / 8, 0, 1) > bayer(H, W))] = rgba("#9a5a38")
        im = Image.fromarray(a, "RGBA")
        d = ImageDraw.Draw(im)
        # shelf with bowls + menu tags
        d.line([134, 126, 160, 126], fill=rgba("#3a1e16"))
        for x in (136, 144, 152):
            d.rectangle([x, 122, x + 5, 125], fill=rgba("#f4e6c8"))
            d.line([x, 125, x + 5, 125], fill=rgba("#ec4a35"))
        for i, x in enumerate(range(222, 254, 7)):
            d.rectangle([x, 118, x + 4, 128], fill=rgba("#fff6e0" if i % 2 else YELLOW))
            d.line([x + 1, 120, x + 3, 120], fill=rgba("#5a2e22")); d.line([x + 1, 123, x + 3, 123], fill=rgba("#5a2e22"))
        # pot
        d.rectangle([212, 136, 238, 151], fill=rgba("#9aa0b8"))
        d.line([212, 136, 238, 136], fill=rgba("#d8dcec"))
        d.line([238, 137, 238, 151], fill=rgba("#6a7088"))
        # posts
        for px in (126, 258):
            d.rectangle([px, 100, px + 3, GROUND - 1], fill=rgba("#5a3424"))
            d.line([px, 100, px, GROUND - 1], fill=rgba("#7a4a32"))
        # roof (wide eaves)
        d.polygon([(94, 104), (292, 104), (276, 90), (110, 90)], fill=rgba("#6a3a2a"))
        d.line([110, 90, 276, 90], fill=rgba("#9a5a3a"))
        d.line([94, 104, 292, 104], fill=rgba("#c8343a"))
        d.line([94, 105, 292, 105], fill=rgba("#2a1410"))
        for x in range(112, 276, 8):
            d.line([x, 91, x - 4, 103], fill=rgba("#5a3022"))
        # sign board on the roof
        d.rectangle([148, 70, 236, 89], fill=rgba("#16121f"))
        d.line([148, 70, 236, 70], fill=rgba("#2e2840"))
        d.line([160, 89, 160, 92], fill=rgba("#16121f")); d.line([224, 89, 224, 92], fill=rgba("#16121f"))
        # counter
        d.rectangle([122, 150, 264, 156], fill=rgba("#c8945a"))
        d.line([122, 150, 264, 150], fill=rgba("#e8b47a"))
        d.rectangle([126, 157, 260, GROUND - 1], fill=rgba("#8a5232"))
        for x in range(130, 260, 9):
            d.line([x, 158, x, GROUND - 2], fill=rgba("#6a3a22"))
        m = text_mask("NINJA-BLOKS", F35)
        a = np.array(im)
        x0 = 193 - m.shape[1] // 2
        a[169:174, x0 + 1:x0 + 1 + m.shape[1]][m] = rgba("#4a2412")
        a[168:173, x0:x0 + m.shape[1]][m] = rgba("#ffd23f")
        im = Image.fromarray(a, "RGBA")
        d = ImageDraw.Draw(im)
        ic = outline(_pad(blok_icon()))
        im.paste(ic, (x0 - 14, 165), ic)
        im.paste(ic, (x0 + m.shape[1] + 3, 165), ic)
        # stools (outer ends, under the eaves)
        for sx in (104, 268):
            d.rectangle([sx, 176, sx + 14, 179], fill=rgba("#e8402f"))
            d.line([sx + 2, 180, sx + 2, GROUND - 1], fill=rgba("#7a7e98")); d.line([sx + 12, 180, sx + 12, GROUND - 1], fill=rgba("#7a7e98"))
        return outline(im)

    # ------------------------------------------------------------ per frame
    def frame(self, t):
        t = t % DUR
        f = Frame(self.base)
        d = f.draw()
        # far skyline windows + aircraft lights
        for (x, y, p, ph) in self.far:
            if wave(t, p, ph) > -0.1:
                d.point((x, y), fill=rgba("#ffcf8a" if p < 6 else "#9fd8ff"))
        if cyc(t, 2) < 0.15:
            d.point((150, 72), fill=rgba("#ff3a3a")); d.point((246, 66), fill=rgba("#ff3a3a"))
        for (x, y, p, ph, col) in self.windows:
            if wave(t, p, ph) > -0.35:
                d.rectangle([x + 1, y + 1, x + 8, y + 10], fill=rgba(col))
                d.line([x + 1, y + 6, x + 8, y + 6], fill=rgba("#1a1f36"))
        # building neon (vertical) — NINJA left, BLOKS right
        f.put(neon_text("NINJA", CYAN, "#1a6a8a", vertical=True), 70, 66)
        f.put(neon_text("BLOKS", PINK, "#7a2050", vertical=True), 304, 64)
        # far rain (behind the stand)
        self._rain(f, t, 0)
        f.flush()
        # train overhead
        if TRAIN_T[0] - 0.5 <= t <= TRAIN_T[1] + 0.5:
            k = (t - TRAIN_T[0]) / (TRAIN_T[1] - TRAIN_T[0])
            x0 = 400 - 820 * k
            for i in range(4):
                f.smooth(up(train_car(int(t * 8) % 7 != 0)), x0 + i * 94, 35)
            d = f.draw()
            if int(t * 15) % 3 == 0:
                sx = int(x0 + 46)
                if 0 <= sx < W:
                    d.point((sx, 33), fill=rgba("#e8ffff")); d.point((sx + 1, 32), fill=rgba(CYAN))
        # the ramen stand
        f.smooth(self.stand, 0, 0)
        self._sign(f, t)
        self._interior(f, t)
        self._noren(f, t)
        # lanterns (swing 4 s)
        for i, lx in enumerate((102, 280)):
            sw = round(1.2 * wave(t, 4, i * 1.5))
            d = f.draw()
            d.line([lx + 4, 105, lx + 4 + sw, 108], fill=rgba(INK))
            f.put(lantern(wave(t, 0.75, i) > -0.5), lx + sw, 108)
        # customers on stools: Red (left) and Blue (right) slurping
        self._customer(f, t, "red", 100, 1.0, False)
        self._customer(f, t, "blue", 264, 4.0, True)
        # Pink under a clear umbrella by the vending machine
        px, py = 62, 160
        draw_blok(f, "pink", px, py, t, eyes="happy" if cyc(t, 12) < 0.25 else 1, blink_phase=0.75, wind=0.7)
        d = f.draw()
        d.line([px + 26, py + 18, px + 26, py - 12], fill=rgba("#e8e8f4"))
        d.point((px + 25, py + 19), fill=rgba("#e8e8f4"))
        f.put(umbrella(), px + 6, py - 26)
        for i in range(5):
            a = cyc(t, (0.5, 0.75, 1.0)[i % 3], i / 5)
            if a < 0.3:
                d = f.draw()
                ux = px + 10 + i * 7
                d.point((ux + (1 if i % 2 else -1), py - 26 + 4 - 10 * a + abs(ux - px - 26) * 0.4), fill=rgba("#cfe8ff"))
        # cat asleep on the crate
        tail = cyc(t, 4) < 0.2
        f.put(_pad_outline_cat(tail), 306, 167)
        # puddles, splashes, reflections
        self._street(f, t)
        # drips from the eaves
        d = f.draw()
        for i, (x, p) in enumerate(((96, 1.5), (150, 2.0), (236, 1.5), (290, 2.0))):
            a = cyc(t, p, i * 0.27)
            y = 106 + (GROUND - 106) * a ** 1.6
            d.line([x, y, x, y + 2], fill=rgba("#bcd4ff"))
            if a > 0.94:
                d.point((x - 1, GROUND - 1), fill=rgba("#bcd4ff")); d.point((x + 1, GROUND - 1), fill=rgba("#bcd4ff"))
        # near rain (in front of everything)
        self._rain(f, t, 1)
        self._rain(f, t, 2)
        draw_bug(f)
        return f.out()

    def _rain(self, f, t, layer):
        d = f.draw()
        pts = self.rain[layer]
        ln, col, vx, vy = pts[-1]
        dx, dy = vx / vy * ln, ln
        for (x0, y0) in pts[:-1]:
            x = (x0 + vx * t) % W
            y = (y0 + vy * t) % H
            c = col
            if layer > 0 and 320 < x < 352 and 72 < y < GROUND and abs(x - 336) < (y - 66) * 0.32:
                c = "#e8ecff"
            d.line([x, y, x + dx, y + dy], fill=rgba(c))

    def _sign(self, f, t):
        off = None
        for a, b in FLICKER:
            if a <= t <= b and int(t * 20) % 3 != 0:
                off = 2
        if DIP_T[0] <= t <= DIP_T[1]:
            f.put(neon_text("PXLBLR", "#7a2a5a", "#3a1430"), 173, 73)
            return
        f.put(neon_text("PXLBLR", PINK, "#a8306a", off_idx=off), 173, 73)

    def _interior(self, f, t):
        # chef Black lifts the noodle strainer from the pot every 3 s
        cx, cy = 180, 122
        draw_blok(f, "black", cx, cy, t, eyes=1, blink_phase=0.5, tail=False)
        p = cyc(t, 3)
        lift = max(0.0, np.sin(np.pi * min(1, p / 0.6))) * 10 if p < 0.6 else 0
        d = f.draw()
        sx, sy = 222, 136 - lift
        d.line([cx + 26, cy + 18, sx, sy], fill=rgba("#c8ccd8"))
        d.ellipse([sx - 3, sy - 2, sx + 5, sy + 4], fill=rgba("#f4e6a8"), outline=rgba(INK))
        if lift > 2:
            for i in range(3):
                d.point((sx - 1 + i * 2, sy + 6 + (int(t * 10) + i) % 4), fill=rgba("#bfe0ff"))
        # counter top covers the chef's lower half
        d.rectangle([122, 150, 264, 156], fill=rgba("#c8945a"))
        d.line([122, 150, 264, 150], fill=rgba("#e8b47a"))
        d.line([122, 149, 264, 149], fill=rgba(INK))
        # steam from the pot
        for i in range(5):
            a = cyc(t, 3, i / 5)
            x = 225 + 4 * np.sin(TAU * a + i) + (i - 2) * 2
            y = 134 - 26 * a
            if a < 0.85:
                d.point((x, y), fill=rgba("#f4eef4" if a < 0.5 else "#a89aa8"))

    def _noren(self, f, t):
        d = f.draw()
        letters = "RAMEN"
        for i in range(5):
            x0 = 130 + i * 25
            drop = 13 + round(wave(t, 2, i * 0.9))
            d.rectangle([x0, 105, x0 + 23, 105 + drop], fill=rgba("#2a2f6a"))
            d.line([x0, 105, x0 + 23, 105], fill=rgba("#4a50a0"))
            d.line([x0 + 23, 106, x0 + 23, 105 + drop], fill=rgba("#1a1e4a"))
            m = text_mask(letters[i], F35)
            for (yy, xx) in zip(*np.nonzero(m)):
                d.point((x0 + 10 + xx, 108 + yy), fill=rgba("#f4f0ff"))

    def _customer(self, f, t, name, x, t0, fl):
        k = (t - t0) % 6
        lifting = k < 1.4
        eyes = "happy" if lifting else (-1 if fl else 1)
        draw_blok(f, name, x, 150, t, eyes=eyes, mouth="o" if 0.6 < k < 1.2 else "smile", flipx=fl, blink_phase=0.3 if fl else 0.8)
        bx = x - 4 if fl else x + 22
        f.put(bowl(), bx, 168)
        d = f.draw()
        # chopsticks + noodles rising to the mouth
        u = np.sin(np.pi * min(1, k / 1.4)) if lifting else 0
        top = 166 - 10 * u
        cx_ = bx + 4
        d.line([cx_ - 1, top - 6, cx_ + 2, 168], fill=rgba("#c8945a"))
        d.line([cx_ + 1, top - 6, cx_ + 4, 168], fill=rgba("#c8945a"))
        if lifting:
            for yy in range(int(top), 168):
                d.point((cx_ + 1 + (yy % 2), yy), fill=rgba("#f4e6a8"))
        for i in range(3):
            a = cyc(t, 3, i / 3 + (0.5 if fl else 0))
            d.point((bx + 2 + i * 2 + round(np.sin(TAU * a + i)), 166 - 12 * a), fill=rgba("#d8d0e0" if a < 0.5 else "#8a8098"))

    def _street(self, f, t):
        d = f.draw()
        # neon + lantern reflections shimmering on the wet street
        th = bayer(H, W)
        for i, (x0, x1, col, dim) in enumerate(((168, 216, PINK, "#7a2a5a"), (101, 111, LANTERN, "#7a2a2a"), (279, 289, LANTERN, "#7a2a2a"),
                                               (36, 60, "#9fd8ff", "#3a5a7a"), (71, 77, CYAN, "#1a6a8a"), (305, 311, PINK, "#7a2a5a"),
                                               (331, 341, "#fff2c0", "#6a6450"))):
            for y in range(GROUND + 2, H):
                k = (y - GROUND) / (H - GROUND)
                wob = round(1.5 * np.sin(y * 1.3 + TAU * t / 1.5 + i))
                shrink = int((x1 - x0) * 0.25 * k)
                for x in range(x0 + shrink, x1 - shrink):
                    v = (1 - k) * 0.9 * (0.6 + 0.4 * np.sin(y * 0.9 - TAU * t / 1.0 + x * 0.3))
                    if v > th[y, x]:
                        d.point((x + wob, y), fill=rgba(col if v > 0.55 else dim))
        # puddle rings
        for i, (cx, cy, rx, p) in enumerate(((70, 202, 26, 1.5), (190, 208, 34, 2.0), (330, 200, 22, 3.0))):
            for k in (0, 0.5):
                a = cyc(t, p, k + i * 0.13)
                r = 2 + a * rx * 0.5
                if a < 0.9:
                    d.ellipse([cx - r + (i * 9 % 13), cy - r * 0.18, cx + r + (i * 9 % 13), cy + r * 0.18], outline=rgba("#5a6aa0"))
        # rain splashes
        for (x, y, p, ph) in self.splashes:
            a = cyc(t, p, ph)
            if a < 0.15:
                d.point((x - 1, y - 1), fill=rgba("#a6b4e0")); d.point((x + 1, y - 1), fill=rgba("#a6b4e0"))
                d.point((x, y - 2), fill=rgba("#e8ecff"))

    # ------------------------------------------------------------ audio
    def audio(self):
        from engine import audio as A
        T = A.T
        buf = np.zeros((2, A.N))
        rainL, rainR = A.rain_bed(401), A.rain_bed(402)
        awning = A.rain_bed(403, rate=40)
        awning = A.band(awning, 300, 3500, circular=True)
        awning /= np.std(awning) + 1e-9
        hum = A.colored(1.8, 30, 220, seed=404)
        sizzle = A.colored(0.0, 3500, 11000, seed=405) * A.slow_am(406, 0.5, 6.0, 0.5)
        buzz = A.buzz_bed(120.0)
        buzz = A.band(buzz, 100, 3000, circular=True)
        buzz /= np.std(buzz) + 1e-9
        buf[0] += rainL * 0.24 + awning * 0.10 + hum * 0.10 + sizzle * 0.025 + buzz * 0.012
        buf[1] += rainR * 0.24 + awning * 0.10 + hum * 0.10 + sizzle * 0.025 + buzz * 0.012
        for k in range(10):
            A.place(buf, A.pk(A.slurp(500 + k)), 6 * k + 1.5, 1.0, pan=-0.5)
            A.place(buf, A.pk(A.slurp(520 + k)), 6 * k + 4.5, 1.0, pan=0.55)
        for k in range(20):
            A.place(buf, A.pk(A.swish(540 + k, 0.4)), 3 * k + 0.6, 0.035, pan=0.15)
        for i, (x, p) in enumerate(((96, 1.5), (150, 2.0), (236, 1.5), (290, 2.0))):
            n = int(DUR / p)
            for k in range(n):
                t0 = (k + 1 - i * 0.27) * p
                A.place(buf, A.pk(A.plop(600 + i * 50 + k)), t0 % DUR, 0.5, pan=(x - 192) / 192)
        for a, b in FLICKER:
            A.place(buf, A.pk(A.zap(int(a * 10))), a, 1.2, pan=0.0)
        A.place(buf, A.pk(A.zap(77)), DIP_T[0], 1.4, pan=0.0)
        A.place_sweep(buf, A.pk(A.train(9, 7.0)), TRAIN_T[0] - 1.0, 0.7, 0.8, -0.8)
        for i, t0 in enumerate(CAR_T):
            hiss = A.pk(A.swish(700 + i, 2.6))
            car = hiss * 0.6 + A.pk(A.band(np.random.default_rng(i).normal(size=len(hiss)), 60, 400)) * 0.4
            A.place_sweep(buf, car * np.hanning(len(car)), t0, 0.4, -0.9 if i == 0 else 0.9, 0.9 if i == 0 else -0.9)
        return A.master(buf)


@lru_cache(maxsize=None)
def _pad_outline_cat(tail):
    return outline(_pad(cat(tail)))
