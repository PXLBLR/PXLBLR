"""NINJA-BLOKS · Cozy Treehouse Library (rainy night, indoors) — 60 s seamless loop.

Periods (all divide 60 s): pendulum 2 s (tick every 1 s) · candle 0.5/0.75 s · fire 0.5/0.75 s ·
fairy lights 2-6 s · rain on the window (looping streaks + sliding drops) · hammock sway 4 s ·
Zzz 3 s · Red writes 6 s (4 s writing, 2 s pause) · Pink turns a page every 10 s, Blue every 12 s.
Event: lightning at 30 s, thunder 31 s, the cat wakes, stretches and meows 31-34 s.
"""
import numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw
from engine.px import (W, H, S, INK, TAU, DUR, rgba, hx, vgrad, radial_dither, bayer, sprite, outline, rim,
                       up, flip, wave, cyc, Frame, _shift, text_mask, text_sprite, F57, F35)
from engine.bloks import draw_blok, GOLD
from scenes.common import draw_bug, shadow_ellipse, _pad

WIN = (204, 78, 37)       # round window centre + radius
FLASH = ((30.0, 30.1), (30.22, 30.34), (30.5, 30.56))
THUNDER_T = 30.9
CAT_T = (31.0, 34.5)
FLOOR = 186
BOOKS = ["#a8343a", "#3a5a9a", "#4a7a3a", "#c8902a", "#6a3a8a", "#2a6a6a", "#b8643a", "#8a2a4a", "#d8c8a0"]

rng = np.random.default_rng(71)


# ---------------------------------------------------------------- sprites
@lru_cache(maxsize=None)
def cat(pose):
    if pose == "stretch":
        rows = [
            "...........K.K",
            "..........KGKG",
            "K.........KGEG",
            "KK.KKKKKKKGGGGK",
            ".KGGGGGGGGGGGK.",
            "..KGGGGGGGGGK..",
            "..KG.K....KGK..",
            "..KK.K....KK...",
        ]
    else:
        rows = [
            "..K.K.........",
            ".KGKGK........",
            ".KGGGKKKKKK...",
            "KGKGKGGGGGGK..",
            "KGGGGGGGGGGGKK",
            ".KKKKKKKKKKKK.",
        ]
    rows = [r.ljust(15, ".") for r in rows]
    return outline(_pad(sprite(rows, {"K": INK, "G": "#f2a04a", "E": "#2a2a40"})))


@lru_cache(maxsize=None)
def book(col="#3a5a9a", flip_k=-1):
    """Open book held in front; flip_k 0..2 = page mid-turn."""
    im = Image.new("RGBA", (18, 12), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([1, 2, 16, 10], fill=rgba(col))
    d.rectangle([2, 2, 8, 9], fill=rgba("#f6eedc")); d.rectangle([9, 2, 15, 9], fill=rgba("#f6eedc"))
    for y in (4, 6, 8):
        d.line([3, y, 7, y], fill=rgba("#b8a888")); d.line([10, y, 14, y], fill=rgba("#b8a888"))
    d.line([8, 2, 8, 9], fill=rgba("#c8b898"))
    if flip_k >= 0:
        x = (13, 9, 5)[flip_k]
        h_ = (5, 8, 5)[flip_k]
        d.rectangle([min(x, 8), 9 - h_, max(x, 8), 9], fill=rgba("#ffffff"))
    return outline(im)


@lru_cache(maxsize=None)
def desk():
    im = Image.new("RGBA", (86, 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([1, 12, 84, 16], fill=rgba("#9a643a"))
    d.line([1, 12, 84, 12], fill=rgba("#c08450"))
    d.rectangle([4, 17, 81, 38], fill=rgba("#7a4a2a"))
    for x in (6, 44):
        d.rectangle([x, 20, x + 34, 28], outline=rgba("#5a3420"))
        d.point((x + 17, 24), fill=rgba(GOLD))
    d.rectangle([6, 31, 78, 34], fill=rgba("#6a3e22"))
    # papers, inkwell, stacked books, candle holder
    d.polygon([(20, 11), (40, 10), (42, 12), (22, 12)], fill=rgba("#f6eedc"))
    d.rectangle([46, 7, 51, 11], fill=rgba("#2a2a40")); d.line([46, 7, 51, 7], fill=rgba("#5a5a7a"))
    for i, c in enumerate(("#a8343a", "#3a5a9a", "#c8902a")):
        d.rectangle([6, 8 - i * 3, 17 - i, 10 - i * 3], fill=rgba(c))
    d.rectangle([62, 1, 65, 11], fill=rgba("#f6eedc"))
    d.rectangle([59, 10, 68, 11], fill=rgba("#c8902a"))
    return outline(im)


@lru_cache(maxsize=None)
def armchair_front():
    im = Image.new("RGBA", (58, 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([1, 4, 11, 26], radius=3, fill=rgba("#a8343a"))
    d.rounded_rectangle([46, 4, 56, 26], radius=3, fill=rgba("#a8343a"))
    d.rectangle([8, 18, 50, 27], fill=rgba("#8a2a32"))
    d.line([2, 5, 10, 5], fill=rgba("#d0545a")); d.line([47, 5, 55, 5], fill=rgba("#d0545a"))
    d.rectangle([4, 27, 6, 29], fill=rgba("#5a3420")); d.rectangle([51, 27, 53, 29], fill=rgba("#5a3420"))
    return outline(im)


@lru_cache(maxsize=None)
def pennant():
    t = text_mask("PXLBLR", F57)
    w = t.shape[1] + 14
    im = Image.new("RGBA", (w + 8, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(1, 2), (w, 2), (w + 6, 8), (w, 14), (1, 14)], fill=rgba("#c8343a"))
    d.line([1, 2, w, 2], fill=rgba("#e8545a"))
    d.rectangle([1, 2, 4, 14], fill=rgba("#f6eedc"))
    a = np.array(im)
    a[5:12, 7:7 + t.shape[1]][t] = rgba(GOLD)
    return outline(Image.fromarray(a, "RGBA"))


# ---------------------------------------------------------------- scene
class Library:
    name = "library"

    def __init__(self):
        self.base = up(Image.fromarray(self._static(), "RGB"))
        cx, cy, r = WIN
        yy, xx = np.mgrid[0:2 * r + 1, 0:2 * r + 1]
        self.wmask = (xx - r) ** 2 + (yy - r) ** 2 <= (r - 3) ** 2
        self.wbg = self._window_bg()
        self.drops = [(rng.uniform(0, 2 * r), rng.uniform(0, 2 * r)) for _ in range(40)]
        self.slides = [(rng.uniform(6, 2 * r - 6), rng.choice([4, 5, 6, 10]), rng.uniform(0, 1)) for _ in range(9)]
        self.fairy = [(x, 15 + 5 * np.sin(np.pi * ((x - 4) % 64) / 64), rng.choice([2, 3, 4, 6]), rng.uniform(0, TAU))
                      for x in range(6, W, 8)]
        self.motes = [(rng.uniform(150, 260), rng.uniform(60, 170), rng.choice([10, 12, 15, 20]), rng.uniform(0, 1)) for _ in range(12)]

    def _static(self):
        img = np.zeros((H, W, 3), np.uint8)
        im = Image.fromarray(img)
        d = ImageDraw.Draw(im)
        # plank wall
        for i, x in enumerate(range(0, W, 12)):
            d.rectangle([x, 0, x + 11, FLOOR], fill=hx("#5a3a28" if i % 2 else "#64402c"))
            d.line([x, 0, x, FLOOR], fill=hx("#3e2618"))
            for y in range(20 + (i * 37) % 40, FLOOR, 60):
                d.point((x + 5, y), fill=hx("#3e2618"))
        a = np.array(im)
        yy, xx = np.mgrid[0:H, 0:W]
        for (cx, cy, rr, col) in ((164, 136, 70, "#6e4a32"), (338, 160, 80, "#704a2e"), (164, 136, 36, "#7e5636"), (338, 160, 44, "#80542e")):
            dd = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
            m = (yy < FLOOR) & (np.clip((rr - dd) / 14, 0, 1) > bayer(H, W))
            a[m] = (a[m].astype(int) * 0.5 + np.array(hx(col)) * 0.5).astype(np.uint8)
        im = Image.fromarray(a)
        d = ImageDraw.Draw(im)
        # ceiling beam
        d.rectangle([0, 0, W, 9], fill=hx("#3e2618"))
        d.line([0, 9, W, 9], fill=hx("#2a180e"))
        # floor + rug
        for y in range(FLOOR, H, 5):
            d.rectangle([0, y, W, y + 4], fill=hx("#7a4e30"))
            d.line([0, y, W, y], fill=hx("#5a3820"))
            for x in range((y * 13) % 40, W, 40):
                d.line([x, y, x, y + 4], fill=hx("#5a3820"))
        d.line([0, FLOOR, W, FLOOR], fill=hx("#2a180e"))
        d.ellipse([120, 190, 300, 214], fill=hx("#8a2a32"))
        d.ellipse([132, 193, 288, 211], fill=hx("#c8902a"))
        d.ellipse([144, 196, 276, 208], fill=hx("#8a2a32"))
        # window frame ring (interior drawn per frame)
        cx, cy, r = WIN
        d.ellipse([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2], fill=hx("#8a5a36"))
        d.ellipse([cx - r + 1, cy - r + 1, cx + r - 1, cy + r - 1], fill=hx("#5a3a24"))
        d.ellipse([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2], outline=hx("#2a180e"))
        d.rectangle([cx - r + 2, cy + r - 2, cx + r - 2, cy + r + 3], fill=hx("#9a643a"))
        # bookshelf
        d.rectangle([2, 14, 90, FLOOR], fill=hx("#4a2c1a"))
        d.rectangle([2, 14, 90, FLOOR], outline=hx("#2a180e"))
        r_ = np.random.default_rng(5)
        for sy in (16, 48, 80, 112, 144):
            x = 6
            while x < 86:
                bw = int(r_.integers(3, 7))
                bh = int(r_.integers(18, 28))
                if x + bw > 86:
                    break
                c = r_.choice(BOOKS)
                if r_.random() < 0.08 and x < 76:
                    d.polygon([(x, sy + 30), (x + 4, sy + 30), (x + bw + 7, sy + 30 - bh + 2), (x + bw + 3, sy + 30 - bh)], fill=hx(c))
                    x += bw + 8
                    continue
                d.rectangle([x, sy + 30 - bh, x + bw - 1, sy + 29], fill=hx(c))
                d.line([x, sy + 30 - bh + 3, x + bw - 1, sy + 30 - bh + 3], fill=hx("#e8d8a8"))
                d.line([x + bw - 1, sy + 30 - bh, x + bw - 1, sy + 29], fill=hx("#2a180e"))
                x += bw
            d.rectangle([2, sy + 30, 90, sy + 32], fill=hx("#7a4a2a"))
            d.line([2, sy + 30, 90, sy + 30], fill=hx("#9a643a"))
        # globe on the bottom shelf front + plant
        d.ellipse([60, 160, 76, 176], fill=hx("#3a7ab0"))
        d.polygon([(64, 164), (70, 162), (72, 168), (66, 172)], fill=hx("#4a9a4a"))
        d.line([58, 168, 78, 168], fill=hx(GOLD)); d.rectangle([66, 176, 70, 180], fill=hx("#8a5a2a"))
        # ladder
        d.line([74, 186, 84, 20], fill=hx("#a8743c"), width=2); d.line([88, 186, 96, 20], fill=hx("#a8743c"), width=2)
        for y in range(30, 186, 14):
            x0 = 74 + (186 - y) * 10 / 166
            d.line([x0, y, x0 + 13, y], fill=hx("#c08450"))
        # fireplace (stone) + mantel
        d.rectangle([300, 116, 376, FLOOR], fill=hx("#7a6a6e"))
        for y in range(118, FLOOR, 7):
            off = 0 if (y // 7) % 2 else 6
            for x in range(300 + off, 376, 12):
                d.rectangle([x, y, x + 10, y + 5], outline=hx("#5a4a50"))
        d.rectangle([318, 140, 358, FLOOR], fill=hx("#1e1416"))
        d.pieslice([318, 128, 358, 152], 180, 360, fill=hx("#1e1416"))
        d.rectangle([294, 110, 382, 116], fill=hx("#8a5a36"))
        d.line([294, 110, 382, 110], fill=hx("#b07a48"))
        # mantel: candles + framed photo
        for x in (300, 372):
            d.rectangle([x, 100, x + 3, 109], fill=hx("#f6eedc"))
        d.rectangle([330, 96, 346, 109], fill=hx("#c8902a"))
        d.rectangle([332, 98, 344, 107], fill=hx("#3a5a9a"))
        im.paste(outline(_pad(_tiny_blok())), (333, 98), outline(_pad(_tiny_blok())))
        # armchair back (Pink sits in it)
        d.rounded_rectangle([196, 132, 252, 182], radius=6, fill=hx("#a8343a"))
        d.line([200, 133, 248, 133], fill=hx("#d0545a"))
        for x in range(206, 248, 10):
            d.point((x, 146), fill=hx("#6a1e24"))
        # Blue's floor cushion
        d.ellipse([256, 182, 298, 194], fill=hx("#2a6a6a"))
        d.line([262, 183, 292, 183], fill=hx("#3a8a8a"))
        # potted plant
        d.rectangle([178, 170, 190, FLOOR], fill=hx("#b8643a"))
        for (lx, ly) in ((176, 160), (184, 154), (192, 162), (180, 166), (190, 168)):
            d.ellipse([lx - 4, ly - 3, lx + 4, ly + 3], fill=hx("#3a7a3a"))
        # pennant + clock
        p = pennant()
        im.paste(p, (104, 24), p)
        d.line([104, 26, 96, 14], fill=hx("#2a180e")); d.line([104 + p.width - 8, 26, 112 + p.width - 8, 14], fill=hx("#2a180e"))
        d.rectangle([256, 50, 276, 100], fill=hx("#6a3e22"))
        d.ellipse([257, 51, 275, 69], fill=hx("#f6eedc"))
        d.ellipse([257, 51, 275, 69], outline=hx("#2a180e"))
        for k in range(12):
            ang = TAU * k / 12
            d.point((266 + 7 * np.cos(ang), 60 + 7 * np.sin(ang)), fill=hx("#3a2a1a"))
        d.rectangle([259, 72, 273, 98], fill=hx("#3e2414"))
        return np.array(im)

    def _window_bg(self):
        cx, cy, r = WIN
        n = 2 * r + 1
        a = np.zeros((n, n, 4), np.uint8)
        a[..., :3] = vgrad(["#0a1226", "#101c36", "#16264a", "#1e3058"], n, n)
        a[..., 3] = 255
        im = Image.fromarray(a, "RGBA")
        d = ImageDraw.Draw(im)
        # branches + leaves outside the treehouse
        d.line([0, 50, 30, 38, 60, 44, n, 30], fill=rgba("#06091a"), width=3)
        d.line([30, 38, 40, 22], fill=rgba("#06091a"), width=2)
        for (lx, ly) in ((38, 20), (44, 26), (62, 40), (70, 34), (10, 46), (22, 36), (54, 48)):
            d.ellipse([lx - 5, ly - 3, lx + 5, ly + 3], fill=rgba("#0a1424"))
        d.ellipse([46, 10, 50, 14], fill=rgba("#c8d4f0"))
        return np.array(im)

    # ------------------------------------------------------------ per frame
    def frame(self, t):
        t = t % DUR
        flash = any(a <= t <= b for a, b in FLASH)
        f = Frame(self.base)
        self._window(f, t, flash)
        d = f.draw()
        # fairy lights along the beam
        for i, (x, y, p, ph) in enumerate(self.fairy):
            d.line([x - 8, 15 + 5 * np.sin(np.pi * ((x - 12) % 64) / 64), x, y], fill=rgba("#2a180e"))
            on = wave(t, p, ph) > -0.3
            d.rectangle([x, y + 1, x + 1, y + 2], fill=rgba("#ffd88a" if on else "#a8743c"))
        # clock pendulum (2 s) + hands
        ang = np.radians(16) * np.sin(TAU * t / 2)
        px_, py = 266 + 18 * np.sin(ang), 74 + 18 * np.cos(ang)
        d.line([266, 74, px_, py], fill=rgba("#c8902a"))
        d.ellipse([px_ - 2, py - 2, px_ + 2, py + 2], fill=rgba(GOLD), outline=rgba(INK))
        d.line([266, 60, 266, 55], fill=rgba(INK))
        ma = TAU * cyc(t, 60)
        d.line([266, 60, 266 + 6 * np.sin(ma), 60 - 6 * np.cos(ma)], fill=rgba(INK))
        # fire + candles
        self._fire(f, t)
        for x in (301, 373, 160):
            y0 = 99 if x != 160 else 139
            k = wave(t, 0.5, x) + 0.5 * wave(t, 0.75, x * 0.3)
            d.point((x, y0), fill=rgba("#fff6c4"))
            d.point((x, y0 - 1), fill=rgba("#ffd23f"))
            d.point((x, y0 - 2 - (1 if k > 0 else 0)), fill=rgba("#ff8a2a"))
        # Black asleep in a hammock over the fireplace
        self._hammock(f, t)
        # Red writing at the desk (desk drawn in front)
        writing = cyc(t, 6) < 0.66
        draw_blok(f, "red", 112, 120, t, eyes=1 if writing else 0 if cyc(t, 6) < 0.83 else "happy", blink_phase=0.45, tail=True, wind=0.4)
        f.put(desk(), 96, 140)
        d = f.draw()
        qx = 140 + (round(2 * np.sin(t * 9)) if writing else 0) + (round((t % 6) * 3) % 12 if writing else 0)
        qy = 149 + (1 if writing and int(t * 8) % 2 else 0)
        d.line([qx, qy, qx + 5, qy - 8], fill=rgba("#f6eedc"))
        d.line([qx + 3, qy - 5, qx + 6, qy - 9], fill=rgba("#e8545a"))
        # Pink in the armchair with a book and the cat
        page = (t % 10)
        flip_k = int(page / 0.15) if page < 0.45 else -1
        draw_blok(f, "pink", 210, 140, t, eyes=-1 if page > 0.6 else "happy", blink_phase=0.15, wind=0.3)
        f.put(book("#6a3a8a", flip_k), 207, 160)
        cat_up = CAT_T[0] <= t <= CAT_T[1]
        if cat_up:
            f.put(armchair_front(), 195, 158)
            f.put(cat("stretch"), 228, 123 - (1 if int(t * 2) % 2 else 0))
        else:
            f.put(cat("curl"), 222, 164)
        if not cat_up:
            f.put(armchair_front(), 195, 158)
        # Blue on the floor cushion reading
        bp = (t - 2) % 12
        flip_b = int(bp / 0.15) if bp < 0.45 else -1
        draw_blok(f, "blue", 263, 158, t, eyes=1 if bp > 0.6 else "happy", blink_phase=0.7, wind=0.3)
        f.put(book("#2a6a6a", flip_b), 259, 176)
        # dust motes in the warm light
        d = f.draw()
        for (x0, y0, p, ph) in self.motes:
            a = cyc(t, p, ph)
            d.point((x0 + 6 * np.sin(TAU * a), y0 - 20 * a), fill=rgba("#e8c890" if a < 0.6 else "#a8845a"))
        draw_bug(f)
        out = f.out()
        if flash:
            # lightning: the whole room's palette shifts toward cold white for a few frames
            arr = np.asarray(out).astype(np.float32)
            out = Image.fromarray((arr * 0.62 + np.array([196, 210, 246], np.float32) * 0.38).astype(np.uint8))
        return out

    def _window(self, f, t, flash):
        cx, cy, r = WIN
        a = self.wbg.copy()
        n = a.shape[0]
        if flash:
            a[..., :3] = hx("#dfe8ff")
            leaves = np.all(self.wbg[..., :3] == hx("#06091a"), axis=-1) | np.all(self.wbg[..., :3] == hx("#0a1424"), axis=-1)
            a[leaves, :3] = hx("#1a2040")
        im = Image.fromarray(a, "RGBA")
        d = ImageDraw.Draw(im)
        vy, vx = n * 30 / DUR, -n * 6 / DUR
        for (x0, y0) in self.drops:
            x = (x0 + vx * t) % n
            y = (y0 + vy * t) % n
            d.line([x, y, x - 1, y + 4], fill=rgba("#5a7ab0" if not flash else "#8aa0d0"))
        # drops sliding down the glass
        for (x, p, ph) in self.slides:
            k = cyc(t, p, ph)
            y = 6 + (n - 12) * (k ** 2)
            d.point((x, y), fill=rgba("#a8c8f0")); d.point((x, y - 1), fill=rgba("#6a8ac0"))
            d.line([x, max(6, y - 8 * k), x, y - 2], fill=rgba("#2a3e64"))
        a = np.array(im)
        a[~self.wmask] = 0
        f.arr(a, cx - r, cy - r)
        d = f.draw()
        d.line([cx - r + 3, cy, cx + r - 3, cy], fill=rgba("#8a5a36"), width=3)
        d.line([cx, cy - r + 3, cx, cy + r - 3], fill=rgba("#8a5a36"), width=3)
        d.line([cx - r + 3, cy - 1, cx + r - 3, cy - 1], fill=rgba("#b07a48"))

    def _flash(self, f):
        """Cold lightning light washing the room (ordered-dither overlay, a few frames)."""
        a = np.zeros((H, W, 4), np.uint8)
        yy, xx = np.mgrid[0:H, 0:W]
        dd = np.sqrt((xx - WIN[0]) ** 2 + ((yy - WIN[1]) * 0.8) ** 2)
        m = np.clip(0.45 - dd / 500, 0, 1) > bayer(H, W)
        a[m] = rgba("#b8c8f0")
        f.arr(a, 0, 0)

    def _fire(self, f, t):
        d = f.draw()
        cx, base = 338, 184
        d.line([cx - 12, base, cx + 12, base - 2], fill=rgba("#6b4220"), width=3)
        d.line([cx - 12, base - 2, cx + 12, base], fill=rgba("#7a4a22"), width=3)
        for dx in range(-11, 12):
            hgt = (20 - 0.14 * dx * dx) * (0.75 + 0.15 * wave(t, 0.5, dx * 1.3) + 0.1 * wave(t, 0.75, dx * 0.7))
            for k in range(int(max(0, hgt))):
                fr = k / max(hgt, 1)
                col = "#fff6c4" if fr < 0.2 and abs(dx) < 4 else "#ffd23f" if fr < 0.45 else "#ff8a2a" if fr < 0.75 else "#e8402f"
                d.point((cx + dx, base - 3 - k), fill=rgba(col))
        for i in range(6):
            a = cyc(t, (1.5, 2, 3)[i % 3], i / 6)
            if a < 0.7:
                d.point((cx - 6 + i * 2.5 + 3 * np.sin(a * 6 + i), base - 18 - 30 * a), fill=rgba("#ffd23f" if a < 0.35 else "#ff8a2a"))
        # steaming mug on the mantel
        d.rectangle([352, 104, 357, 109], fill=rgba("#3a92f0"), outline=rgba(INK))
        for i in range(3):
            a = cyc(t, 3, i / 3)
            d.point((354 + round(1.5 * np.sin(TAU * a + i)), 101 - 10 * a), fill=rgba("#f4eef4" if a < 0.5 else "#a89aa8"))

    def _hammock(self, f, t):
        sw = 2 * wave(t, 4)
        d = f.draw()
        x0, x1, ytop = 292, 376, 30
        d.line([x0, 10, x0 + 8 + sw, ytop + 10], fill=rgba("#c8b088")); d.line([x1, 10, x1 - 8 + sw, ytop + 10], fill=rgba("#c8b088"))
        draw_blok(f, "black", 320 + sw, 26, t, eyes="happy", blink_phase=0.0, tail=False)
        d = f.draw()
        pts = [(x0 + 8 + sw + i * (x1 - x0 - 16) / 20, ytop + 10 + 18 * np.sin(np.pi * i / 20)) for i in range(21)]
        poly = pts + [(p[0], p[1] - 10 + 4 * np.sin(np.pi * i / 20)) for i, p in reversed(list(enumerate(pts)))]
        d.polygon(poly, fill=rgba("#2a8a8a"))
        d.line(pts, fill=rgba(INK))
        for i in range(0, 21, 3):
            d.line([pts[i][0], pts[i][1], pts[i][0], pts[i][1] - 6], fill=rgba("#ffd23f"))
        # Zzz rising every 3 s
        z = text_mask("Z", F35)
        for k in range(3):
            a = cyc(t, 3, k / 3)
            if a < 0.85:
                zx, zy = int(348 + sw + 10 * a + k * 2), int(26 - 22 * a)
                col = "#ffffff" if a < 0.5 else "#a8b8e0"
                for (yy, xx) in zip(*np.nonzero(z)):
                    d.point((zx + xx, zy + yy), fill=rgba(col))

    # ------------------------------------------------------------ audio
    def audio(self):
        from engine import audio as A
        T = A.T
        buf = np.zeros((2, A.N))
        # the room's only ambience bed: a warm fireplace on the right (no rain hiss, no wind)
        fl, fr = A.fire_bed(1004, pan=0.25)
        buf[0] += fl
        buf[1] += fr
        for k in range(60):
            A.place(buf, A.pk(A.tick(k, hi=k % 2 == 0)), k + 0.5, 0.35, pan=0.35)
        for k in range(10):
            A.place(buf, A.pk(A.scrape(1100 + k, 4.0, 3000, 9000)), 6 * k, 0.05, pan=-0.3)
        for k in range(6):
            A.place(buf, A.pk(A.page_turn(1200 + k)), 10 * k, 0.5, pan=0.1)
        for k in range(5):
            A.place(buf, A.pk(A.page_turn(1300 + k)), 12 * k + 2, 0.45, pan=0.4)
        for k in range(20):
            A.place(buf, A.pk(A.snore(1400 + k)), 3 * k + 0.3, 0.035, pan=0.7)
        A.place(buf, A.pk(A.thunder(1500)), THUNDER_T, 0.65, pan=0.0)
        A.place(buf, A.pk(A.meow(1501)), CAT_T[0] + 0.4, 0.30, pan=0.15)
        return A.master(buf)


@lru_cache(maxsize=None)
def _tiny_blok():
    from engine.bloks import blok_icon
    return blok_icon()
