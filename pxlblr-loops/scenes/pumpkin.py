"""NINJA-BLOKS · Haunted Pumpkin Patch — 60 s seamless loop (Halloween).

Periods (all divide 60 s): bats 15/20/30 s · gate swing 20 s · lantern + jack-o'-lantern
flicker 0.5/0.75 s · carving 6 s burst · candy shake 5 s · ghost-Blok float 4 s ·
fog drift 20/30 s · window flicker 3-12 s. Events: owl hoots 7 s + 37 s, crow caw
15 s, big friendly ghost crosses 16-44 s (woo at 28 s), church bell 50 s.
"""
import numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw
from engine.px import (W, H, S, INK, TAU, DUR, rgba, hx, vgrad, radial_dither, bayer, sprite, outline, rim,
                       up, flip, wave, cyc, Frame, _shift, text_mask, F35)
from engine.bloks import draw_blok, BLOKS, GOLD
from scenes.common import sign, draw_bug, shadow_ellipse, _pad

MOON = (304, 42)
OWL_T = (7.0, 37.0)
CAW_T = 15.0
GHOST_T = (16.0, 44.0)
WOO_T = 28.0
BELL_T = 50.0
GATE_P = 20

rng = np.random.default_rng(31)


def ridge(x):
    return 108 - 8 * np.sin(x / 40.0 + 0.5) - 5 * np.sin(x / 17.0)


# ---------------------------------------------------------------- sprites
@lru_cache(maxsize=None)
def ghost(w, h, hem, arms="down", band=True, eyes="open"):
    im = Image.new("RGBA", (w + 6, h + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    white, sh = "#f6f2ff", "#c9c0e6"
    ox = 3
    d.ellipse([ox, 1, ox + w - 1, int(h * 0.7)], fill=rgba(white))
    d.rectangle([ox, int(h * 0.35), ox + w - 1, h - 4], fill=rgba(white))
    for x in range(w):
        yb = h - 3 + round(1.6 * np.sin(x / 2.6 + hem * np.pi))
        d.line([ox + x, h - 5, ox + x, yb], fill=rgba(white))
    ay = int(h * 0.48)
    if arms == "up":
        d.ellipse([0, ay - 7, 4, ay], fill=rgba(white)); d.ellipse([w + 1, ay - 7, w + 5, ay], fill=rgba(white))
    else:
        d.ellipse([0, ay, 4, ay + 5], fill=rgba(white)); d.ellipse([w + 1, ay, w + 5, ay + 5], fill=rgba(white))
    a = np.array(im)
    m = a[..., 3] > 0
    a[m & ~_shift(m, 0, -2)] = rgba(sh)
    im = Image.fromarray(a, "RGBA")
    d = ImageDraw.Draw(im)
    if band:
        by = int(h * 0.22)
        c = BLOKS["black"]
        d.rectangle([ox + 1, by, ox + w - 2, by + 2], fill=rgba(c["H"]))
        d.line([ox + 1, by + 3, ox + w - 2, by + 3], fill=rgba(c["h"]))
        cx = ox + w // 2
        for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1), (0, 0)):
            d.point((cx + dx, by + 1 + dy), fill=rgba(GOLD))
    ey = int(h * 0.42)
    for ex in (ox + int(w * 0.28), ox + int(w * 0.62)):
        if eyes == "happy":
            d.line([ex, ey + 1, ex + 2, ey + 1], fill=rgba(INK))
        else:
            d.rectangle([ex, ey, ex + 2, ey + 3], fill=rgba(INK))
            d.point((ex, ey), fill=rgba("#ffffff"))
    d.line([ox + int(w * 0.18), ey + 5, ox + int(w * 0.18) + 1, ey + 5], fill=rgba("#ff9fc4"))
    d.line([ox + int(w * 0.78), ey + 5, ox + int(w * 0.78) + 1, ey + 5], fill=rgba("#ff9fc4"))
    mx = ox + w // 2
    d.rectangle([mx - 1, ey + 6, mx + 1, ey + 8], fill=rgba(INK))
    return outline(im)


@lru_cache(maxsize=None)
def witch_hat():
    im = Image.new("RGBA", (24, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(7, 12), (17, 12), (13, 5), (18, 1), (11, 4)], fill=rgba("#3e2a5e"))
    d.ellipse([1, 11, 22, 14], fill=rgba("#3e2a5e"))
    d.rectangle([7, 10, 16, 11], fill=rgba("#8a3ff0"))
    d.rectangle([11, 10, 12, 11], fill=rgba(GOLD))
    im = rim(im, "#7a5aa8", dy=1, skip=("#8a3ff0", GOLD))
    return outline(im)


@lru_cache(maxsize=None)
def pumpkin(w, h, face=None, glow=0):
    """face: None (plain) | 'grin' | 'scary'. glow: 0 off, 1/2 flicker states."""
    im = Image.new("RGBA", (w + 2, h + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    body, rib, hi = "#e8742a", "#b4501e", "#ffa452"
    d.ellipse([1, 3, w, h + 2], fill=rgba(body))
    for k in (0.28, 0.5, 0.72):
        x = 1 + int(w * k)
        d.line([x, 5, x, h], fill=rgba(rib))
    d.rectangle([w // 2, 0, w // 2 + 1, 3], fill=rgba("#4a7a2a"))
    d.point((w // 2 + 2, 1), fill=rgba("#4a7a2a"))
    a = np.array(im)
    m = a[..., 3] > 0
    a[m & ~_shift(m, 1, 0) & (np.arange(a.shape[0])[:, None] > 3)] = rgba(hi)
    a[m & ~_shift(m, -2, 0)] = rgba(rib)
    im = Image.fromarray(a, "RGBA")
    if face:
        d = ImageDraw.Draw(im)
        c1 = {0: "#3a1a10", 1: "#ffd23f", 2: "#ffb030"}[glow]
        c2 = {0: "#3a1a10", 1: "#fff6b0", 2: "#ffd23f"}[glow]
        cx, ey, my = w // 2 + 1, 3 + h // 3, 3 + int(h * 0.62)
        es = max(2, w // 7)
        for ex in (cx - es - 2, cx + 2):
            d.polygon([(ex, ey + es), (ex + es, ey + es), (ex + es // 2, ey)], fill=rgba(c1))
        mw = int(w * 0.32)
        pts = [(cx - mw, my)]
        for i in range(0, 2 * mw + 1, 2):
            pts.append((cx - mw + i, my + (2 if (i // 2) % 2 else 0) + (1 if face == "scary" else 0)))
        pts += [(cx + mw, my), (cx + mw - 1, my + 3), (cx - mw + 1, my + 3)]
        d.polygon(pts, fill=rgba(c1))
        d.point((cx, my + 1), fill=rgba(c2))
    return outline(im)


@lru_cache(maxsize=None)
def bat(f):
    rows = {
        0: ["K.........K", "KK.......KK", ".KKK.K.KKK.", "..KKKRKKK..", "....KKK....", "..........."],
        1: ["...........", "...........", "KKKK.K.KKKK", ".KKKKRKKKK.", "....KKK....", "..........."],
        2: ["...........", "...........", "....K.K....", "..KKKRKKK..", ".KKK.K.KKK.", "KK.......KK"],
    }[f]
    return up(sprite(rows, {"K": "#120a1c", "R": "#ff5a4a"}))


@lru_cache(maxsize=None)
def owl(blink, hoot, look):
    rows = [
        ".K........K.",
        ".KK......KK.",
        ".KBBBBBBBBK.",
        "KBEEEBBEEEBK",
        "KBEPEBBEPEBK",
        "KBEEEYYEEEBK",
        "KBBBBYYBBBBK",
        "KBLLLLLLLLBK",
        "KBLlLLlLLlBK",
        "KBLLLLLLLLBK",
        ".KBLlLLlLBK.",
        ".KBBLLLLBBK.",
        "..KKYKKYKK..",
    ]
    if look:
        rows[4] = "KBEEPBBEEPBK"
    if blink:
        rows[3] = "KBBBBBBBBBBK"; rows[4] = "KBKKKBBKKKBK"; rows[5] = "KBBBBYYBBBBK"
    if hoot:
        rows[7] = "KBLLLLLLLLLBK"[:12]
        rows[6] = "KBBBBKKBBBBK"
    pal = {"K": INK, "B": "#8a6a4a", "E": "#ffd23f", "P": INK, "Y": "#e8a030", "L": "#d8b888", "l": "#a8885a"}
    return sprite(rows, pal)


@lru_cache(maxsize=None)
def crow(f):
    rows = [["..KK...", ".KKKY..", "KKKKK..", ".KKKKK.", "..K.K.."],
            ["..KK.Y.", ".KKKYY.", "KKKKK..", ".KKKKK.", "..K.K.."]][f]
    return sprite(rows, {"K": "#1a1424", "Y": "#ffd23f"})


@lru_cache(maxsize=None)
def scarecrow():
    w, h = 34, 58
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([16, 12, 18, h - 2], fill=rgba("#6a4a3a"))
    d.rectangle([2, 24, 32, 26], fill=rgba("#6a4a3a"))
    d.rectangle([9, 22, 25, 40], fill=rgba("#5a6aa8"))
    for y in range(24, 40, 4):
        d.line([9, y, 25, y], fill=rgba("#3a4a88"))
    for x in range(12, 25, 5):
        d.line([x, 22, x, 40], fill=rgba("#3a4a88"))
    d.rectangle([3, 22, 9, 27], fill=rgba("#5a6aa8")); d.rectangle([25, 22, 31, 27], fill=rgba("#5a6aa8"))
    for (x, y) in ((1, 24), (2, 28), (31, 24), (32, 28), (12, 41), (16, 42), (20, 41), (23, 40)):
        d.line([x, y, x + (1 if x < 17 else -1), y + 2], fill=rgba("#e8c860"))
    d.ellipse([10, 9, 24, 23], fill=rgba("#d8b878"))
    c = BLOKS["red"]
    d.rectangle([10, 13, 24, 14], fill=rgba(c["B"]))
    d.point((17, 13), fill=rgba(GOLD))
    d.line([25, 14, 28, 17], fill=rgba(c["B"])); d.line([25, 13, 29, 14], fill=rgba(c["b"]))
    for ex in (13, 19):
        d.point((ex, 16), fill=rgba(INK)); d.point((ex + 1, 17), fill=rgba(INK))
        d.point((ex + 1, 16), fill=rgba(INK)); d.point((ex, 17), fill=rgba(INK))
    d.line([14, 20, 20, 20], fill=rgba("#7a5a3a"))
    for x in range(14, 21, 2):
        d.point((x, 19), fill=rgba("#7a5a3a"))
    d.rectangle([6, 8, 28, 9], fill=rgba("#4a3a2a"))
    d.polygon([(11, 8), (13, 1), (21, 1), (23, 8)], fill=rgba("#4a3a2a"))
    im = rim(im, "#a898c8", dy=0, dx=-1, skip=(INK,))
    return outline(im)


@lru_cache(maxsize=None)
def gravestone(text="RIP", w=14, h=17, cross=False):
    im = Image.new("RGBA", (w + 2, h + 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if cross:
        d.rectangle([w // 2 - 1, 1, w // 2 + 1, h], fill=rgba("#6a6a82"))
        d.rectangle([w // 2 - 5, 5, w // 2 + 5, 7], fill=rgba("#6a6a82"))
    else:
        d.rounded_rectangle([1, 1, w, h], radius=5, fill=rgba("#6a6a82"))
        m = text_mask(text, F35)
        a = np.array(im)
        x0 = (w + 2 - m.shape[1]) // 2
        a[6:11, x0:x0 + m.shape[1]][m] = rgba("#3a3a50")
        im = Image.fromarray(a, "RGBA")
    im = rim(im, "#a6a6c4", dy=0, dx=-1, skip=("#3a3a50",))
    im = rim(im, "#a6a6c4", dy=1, skip=("#3a3a50",))
    d = ImageDraw.Draw(im)
    d.line([1, h, 4, h - 2], fill=rgba("#3e6a3a"))
    return outline(im)


@lru_cache(maxsize=None)
def bucket():
    rows = [
        ".KKKKKK.",
        "K......K",
        "KOOOOOOK",
        "KOYOOYOK",
        "KOOOOOOK",
        "KOYYYYOK",
        "KOOOOOOK",
        ".KKKKKK.",
    ]
    return sprite(rows, {"K": INK, "O": "#e8742a", "Y": INK})


@lru_cache(maxsize=None)
def bales():
    im = Image.new("RGBA", (56, 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for (x0, y0, x1, y1) in ((2, 18, 52, 37), (9, 3, 45, 18)):
        d.rectangle([x0, y0, x1, y1], fill=rgba("#c4a048"))
        for x in range(x0 + 2, x1, 4):
            d.line([x, y0 + 1, x + 1, y1 - 1], fill=rgba("#a8802e"))
        d.line([x0, y0 + 4, x1, y0 + 4], fill=rgba("#7a5a2a")); d.line([x0, y1 - 4, x1, y1 - 4], fill=rgba("#7a5a2a"))
        d.line([x0, y0, x1, y0], fill=rgba("#e8c868"))
    return outline(im)


def bare_tree(d, x, y, ln, ang, depth, col, r, width=3):
    if depth == 0 or ln < 2:
        return
    x2 = x + ln * np.cos(ang)
    y2 = y + ln * np.sin(ang)
    d.line([x, y, x2, y2], fill=rgba(col), width=max(1, int(width)))
    for da in (-0.5 + r.uniform(-0.15, 0.15), 0.45 + r.uniform(-0.15, 0.15)):
        bare_tree(d, x2, y2, ln * r.uniform(0.6, 0.78), ang + da, depth - 1, col, r, width * 0.7)


# ---------------------------------------------------------------- scene
class Pumpkin:
    name = "pumpkin"

    def __init__(self):
        self.base = up(Image.fromarray(self._static(), "RGB"))
        self.tree = up(self._tree())
        self.stars = [(int(rng.uniform(0, W)), int(rng.uniform(2, 80)), rng.choice([2, 3, 4, 5, 6]), rng.uniform(0, TAU)) for _ in range(46)]
        self.windows = [((57, 89), 3, 0.2), ((64, 89), 4, 1.1), ((73, 89), 6, 2.0), ((57, 96), 12, 0.7),
                        ((73, 96), 5, 1.9), ((82, 73), 3, 0.4), ((82, 82), 10, 2.6)]
        self.wisps = [(rng.uniform(100, 360), rng.uniform(120, 190), rng.choice([10, 12, 15, 20]), rng.uniform(0, 1),
                       rng.choice([2, 3, 4]), rng.uniform(0, TAU)) for _ in range(16)]
        self.leaves = [(rng.uniform(10, 120), rng.choice([6, 7.5, 10, 12]), rng.uniform(0, 1), rng.choice(["#e8742a", "#c8443a", "#f2b84e", "#8a5a2a"]))
                       for _ in range(10)]
        self.far_lit = [(x, y, rng.choice([0.5, 0.75]), rng.uniform(0, TAU)) for (x, y) in ((118, 125), (206, 127), (292, 124), (176, 134), (330, 133))]
        self.big = [(108, 180, 22, 18, "grin", 0.0), (284, 186, 18, 15, "scary", 1.3), (356, 190, 16, 13, "grin", 2.1)]

    def _static(self):
        img = np.zeros((H, W, 3), np.uint8)
        img[:] = vgrad(["#0c0820", "#170e33", "#24144a", "#341a5e", "#4a2268", "#6a2c70", "#9a3e6c", "#c8585a"], W, 124, ease=1.15)[np.minimum(np.arange(H), 123)]
        radial_dither(img, MOON[0], MOON[1], 66, "#3a2266", 14)
        radial_dither(img, MOON[0], MOON[1], 46, "#563a86", 10)
        radial_dither(img, MOON[0], MOON[1], 32, "#7e62a8", 6)
        im = Image.fromarray(img)
        d = ImageDraw.Draw(im)
        mx, my = MOON
        d.ellipse([mx - 22, my - 22, mx + 22, my + 22], fill=hx("#fff1c4"))
        for (cx, cy, r) in ((-8, -6, 5), (7, 4, 6), (-3, 10, 3), (10, -10, 3), (-12, 6, 2)):
            d.ellipse([mx + cx - r, my + cy - r, mx + cx + r, my + cy + r], fill=hx("#ecd9a0"))
        a = np.array(im)
        yy, xx = np.mgrid[0:H, 0:W]
        dm = np.sqrt((xx - mx) ** 2 + (yy - my) ** 2)
        a[(dm <= 22) & (np.sqrt((xx - mx + 6) ** 2 + (yy - my + 4) ** 2) > 22)] = hx("#e2c88e")
        # far hills + haunted house
        xs = np.arange(W)
        rg = ridge(xs)
        hm = (yy >= rg[None, :]) & (yy < 124)
        a[hm] = hx("#24163a")
        a[(yy >= rg[None, :]) & (yy < rg[None, :] + 1)] = hx("#7a5aa0")
        im = Image.fromarray(a)
        d = ImageDraw.Draw(im)
        hc = "#170d26"
        d.rectangle([52, 84, 86, 106], fill=hx(hc))
        d.polygon([(49, 85), (69, 71), (89, 85)], fill=hx(hc))
        d.rectangle([78, 66, 88, 106], fill=hx(hc))
        d.polygon([(76, 67), (83, 52), (90, 67)], fill=hx(hc))
        d.rectangle([56, 74, 58, 80], fill=hx(hc))
        d.line([83, 52, 83, 48], fill=hx(hc)); d.line([81, 49, 85, 49], fill=hx(hc))
        for (wx, wy) in ((57, 89), (64, 89), (73, 89), (57, 96), (73, 96)):
            d.rectangle([wx, wy, wx + 2, wy + 3], fill=hx("#2e1f42"))
        d.rectangle([82, 73, 83, 75], fill=hx("#2e1f42")); d.rectangle([82, 82, 83, 84], fill=hx("#2e1f42"))
        d.line([(90, 67), (83, 52)], fill=hx("#5a4280"))
        r = np.random.default_rng(4)
        for (tx, ln) in ((150, 9), (214, 8), (24, 7), (366, 8)):
            bare_tree(d, tx, ridge(tx) + 2, ln, -np.pi / 2, 5, "#170d26", r, 2)
        a = np.array(im)
        # field
        field = vgrad(["#1c1830", "#222236", "#262c36", "#283432", "#2c3c30"], W, H - 116)
        a[118:] = field[2:]
        a[118] = hx("#352a4e")
        im = Image.fromarray(a)
        d = ImageDraw.Draw(im)
        # pumpkin rows with vines, receding
        for (ry, step, pw, ph) in ((123, 22, 5, 4), (131, 26, 7, 5), (141, 30, 9, 6)):
            d.line([0, ry + ph - 1, W, ry + ph - 1], fill=hx("#2a4a2e"))
            for x in range(-4 + (ry % 7), W, step):
                xx_ = x + int(r.integers(-3, 4))
                d.ellipse([xx_, ry, xx_ + pw, ry + ph], fill=hx("#b4561f"))
                d.line([xx_ + 1, ry, xx_ + pw - 1, ry], fill=hx("#e8904a"))
                d.point((xx_ + pw // 2, ry - 1), fill=hx("#4a7a2a"))
                for k in range(3):
                    d.point((xx_ + pw + 2 + k * 3, ry + ph - 2 - (k % 2)), fill=hx("#3a6a32"))
        # glow pools around the big jack-o'-lanterns
        a = np.array(im)
        for (x, y, w, h, _, _) in [(108, 180, 22, 18, 0, 0), (284, 186, 18, 15, 0, 0), (356, 190, 16, 13, 0, 0)]:
            cx, cy = x + w // 2, y + h
            dist = np.sqrt(((xx - cx) / 1.0) ** 2 + ((yy - cy) / 0.45) ** 2)
            ground = yy > 150
            a[ground & (np.clip((34 - dist) / 10, 0, 1) > bayer(H, W))] = hx("#3e3a34")
            a[ground & (np.clip((20 - dist) / 6, 0, 1) > bayer(H, W))] = hx("#5a4632")
        # grass speckle
        for _ in range(500):
            x, y = r.integers(0, W), r.integers(150, H - 1)
            a[y, x] = hx(r.choice(["#3a4c34", "#22301e", "#46583a"]))
        im = Image.fromarray(a)
        d = ImageDraw.Draw(im)
        # fence with gate gap (148..176)
        for x in list(range(4, 148, 18)) + [148, 176] + list(range(194, W, 18)):
            d.rectangle([x, 128, x + 2, 152], fill=hx("#5a4a5e"))
            d.line([x, 128, x + 2, 128], fill=hx("#9a8aa8"))
            d.point((x + 1, 127), fill=hx("#5a4a5e"))
        for y in (134, 144):
            d.line([0, y, 148, y], fill=hx("#4e4054"), width=2)
            d.line([178, y, W, y], fill=hx("#4e4054"), width=2)
            d.line([0, y, 148, y], fill=hx("#7a6a86"))
            d.line([178, y, W, y], fill=hx("#7a6a86"))
        im.paste(bales(), (50, 162), bales())
        for (gx, gy, txt, cr) in ((322, 136, "RIP", False), (344, 140, "BOO", False), (364, 134, "", True)):
            g = gravestone(txt or "RIP", cross=cr)
            im.paste(g, (gx, gy), g)
        return np.array(im)

    def _tree(self):
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        r = np.random.default_rng(12)
        col = "#1c1428"
        d.polygon([(0, 216), (2, 150), (8, 110), (14, 86), (22, 80), (24, 92), (20, 120), (22, 160), (30, 216)], fill=rgba(col))
        for (ang, ln) in ((-0.35, 26), (-1.2, 22), (-0.9, 30)):
            bare_tree(d, 18, 88, ln, ang, 5, col, r, 4)
        bare_tree(d, 12, 120, 20, -2.6, 3, col, r, 3)
        d.line([18, 96, 52, 92], fill=rgba(col), width=3)  # owl branch
        im = rim(im, "#5a4680", dy=0, dx=-1)
        return outline(im, "#0c0818")

    # ------------------------------------------------------------ per frame
    def frame(self, t):
        t = t % DUR
        f = Frame(self.base)
        d = f.draw()
        for (x, y, p, ph) in self.stars:
            v = wave(t, p, ph)
            if v > -0.3 and not ((x - MOON[0]) ** 2 + (y - MOON[1]) ** 2 < 40 ** 2):
                d.point((x, y), fill=rgba("#fff6d8" if v > 0.7 else "#9a84c8"))
        for (wx, wy), p, ph in self.windows:
            v = wave(t, p, ph)
            if v > -0.2:
                w_ = 2 if wx > 80 else 3
                d.rectangle([wx, wy, wx + w_ - 1, wy + 3 - (1 if wx > 80 else 0)], fill=rgba("#ffd23f" if v > 0.4 else "#c87a2a"))
        f.flush()
        # bats
        for span_t, y0, direction, ph in ((20, 30, 1, 0.0), (30, 58, -1, 0.0), (15, 74, 1, 0.3)):
            x = cyc(t, span_t, ph) * 460 - 40
            if direction < 0:
                x = W - x
            b = bat(int(cyc(t, 0.6, ph) * 3))
            f.smooth(b if direction > 0 else flip(b), x, y0 + 4 * wave(t, 2, ph * 9))
        # the big friendly ghost crossing the moonlit sky
        if GHOST_T[0] <= t <= GHOST_T[1]:
            k = (t - GHOST_T[0]) / (GHOST_T[1] - GHOST_T[0])
            gx = -44 + 470 * k
            gy = 38 + 6 * wave(t, 4)
            arms = "up" if cyc(t, 1) < 0.5 else "down"
            f.smooth(up(ghost(32, 34, int(cyc(t, 0.5) * 2), arms, band=False)), gx, gy)
        # far fog drifting over the field
        self._fog(f, t, 114, 134, "#3e3258", 0.75, 30)
        # far jack-o'-lanterns twinkling in the rows
        d = f.draw()
        for (x, y, p, ph) in self.far_lit:
            on = wave(t, p, ph) > -0.4
            d.point((x, y), fill=rgba("#ffd23f" if on else "#ff8a2a")); d.point((x + 2, y), fill=rgba("#ffd23f" if on else "#ff8a2a"))
            d.line([x, y + 2, x + 2, y + 2], fill=rgba("#ff8a2a"))
        # scarecrow + crow
        f.put(scarecrow(), 236, 94)
        caw = CAW_T <= t <= CAW_T + 0.8 and int(t * 6) % 2 == 0
        cr = crow(1 if caw else 0)
        f.put(cr if cyc(t, 4) < 0.5 else flip(cr), 262, 113)
        # swinging gate (20 s cycle) + lantern
        self._gate(f, t)
        # cast
        self._cast(f, t)
        # big jack-o'-lanterns
        for i, (x, y, w, h, face, ph) in enumerate(self.big):
            g = 1 if wave(t, 0.5, ph) + 0.6 * wave(t, 0.75, ph * 2) > -0.2 else 2
            f.put(pumpkin(w, h, face, g), x, y)
        # wisps rising
        d = f.draw()
        for (x0, y0, p, ph, tb, ph2) in self.wisps:
            a = cyc(t, p, ph)
            x = x0 + 5 * np.sin(TAU * a * 2 + ph2)
            y = y0 - 26 * a
            if wave(t, tb, ph2) > 0 and a < 0.9:
                d.point((x, y), fill=rgba("#c8a8ff" if a < 0.5 else "#8a6ad8"))
        # near ground fog over the Bloks' feet
        self._fog(f, t, 192, 216, "#4e4468", 0.7, 20, rising=True)
        # foreground tree + owl
        f.smooth(self.tree, 0, 0)
        hoot = any(t0 <= t <= t0 + 1.3 for t0 in OWL_T)
        f.put(outline(_pad(owl(((t / 6 + 0.4) % 1) < 0.04, hoot, cyc(t, 12) > 0.5))), 34, 77)
        # falling leaves
        d = f.draw()
        for (x0, p, ph, col) in self.leaves:
            a = cyc(t, p, ph)
            x = x0 + 40 * a + 5 * np.sin(TAU * a * 3)
            y = 80 + 136 * a
            d.point((x, y), fill=rgba(col))
            d.point((x + (1 if cyc(t, 0.5, ph) < 0.5 else -1), y), fill=rgba(col))
        f.put(sign(), 300, 150)
        draw_bug(f)
        return f.out()

    def _fog(self, f, t, y0, y1, col, strength, period, rising=False):
        hh = y1 - y0
        xs = np.arange(W)[None, :]
        ys = np.arange(hh)[:, None]
        prof = np.sin(np.pi * ys / hh) if not rising else (ys / hh) ** 1.2
        dens = strength * prof * (0.55 + 0.25 * np.sin(xs / 31.0 + TAU * t / period + ys / 5.0)
                                  + 0.2 * np.sin(xs / 13.0 - TAU * t / 20 + ys / 3.0))
        m = np.clip((dens - 0.3) * 4, 0, 1) > bayer(hh, W)  # mostly solid wisps, dithered only at the edges
        a = np.zeros((hh, W, 4), np.uint8)
        a[m] = rgba(col)
        f.arr(a, 0, y0)

    def _gate(self, f, t):
        d = f.draw()
        th = np.radians(32 + 30 * wave(t, GATE_P))
        wdt = 26 * np.cos(th)
        for y in (132, 140, 148):
            d.line([150, y, 150 + wdt, y - 3 * np.sin(th)], fill=rgba("#6a5a70"), width=2)
        for k in (0.5, 1.0):
            x = 150 + wdt * k
            d.line([x, 130 - 3 * np.sin(th) * k, x, 150 - 3 * np.sin(th) * k], fill=rgba("#6a5a70"), width=2)
        # lantern on the gate post
        d.line([147, 126, 147, 122], fill=rgba(INK))
        lit = "#ffd23f" if wave(t, 0.5, 0.7) + wave(t, 0.75) > -0.4 else "#ffb030"
        d.rectangle([145, 122, 149, 127], fill=rgba(INK))
        d.rectangle([146, 123, 148, 126], fill=rgba(lit))

    def _cast(self, f, t):
        # Red: witch hat, sitting on the hay bales, swinging happily
        rx, ry = 64, 137
        draw_blok(f, "red", rx, ry + (1 if cyc(t, 2) < 0.5 else 0), t, eyes=1, blink_phase=0.15, wind=0.8)
        f.put(witch_hat(), rx + 3, ry - 3 + (1 if cyc(t, 2) < 0.5 else 0))
        # Blue: carving a big pumpkin (3 strokes every 6 s)
        bx, by = 150, 161
        shadow_ellipse(f, bx + 14, 190, 11, 2, "#1e2a24")
        draw_blok(f, "blue", bx, by, t, eyes=1, blink_phase=0.55)
        carving = (t % 6) < 3
        k = cyc(t, 1) if carving else 0.0
        kx, ky = bx + 28, by + 14 + round(5 * np.sin(np.pi * k))
        d = f.draw()
        d.line([kx, ky, kx + 3, ky - 3], fill=rgba("#e6e8f0"))
        d.point((kx - 1, ky + 1), fill=rgba("#7a4a22"))
        f.put(pumpkin(24, 19, "grin", 0), bx + 30, by + 8)
        # Pink: shaking a candy bucket every 5 s
        px, py = 214, 161
        shadow_ellipse(f, px + 14, 190, 11, 2, "#1e2a24")
        shake = (t % 5) < 0.6
        draw_blok(f, "pink", px, py, t, eyes="happy" if shake else -1, mouth="open" if shake else "smile",
                  arms="up" if shake else "down", flipx=True, blink_phase=0.85)
        jit = (1 if int(t * 12) % 2 else -1) if shake else 0
        f.put(bucket(), px - 6 + jit, py + 16)
        if shake:
            d = f.draw()
            for i, c in enumerate(("#ff4fa8", "#3ff0ff", "#ffd23f")):
                d.point((px - 4 + i * 2, py + 14 - (int(t * 12) + i) % 3), fill=rgba(c))
        # Black: a ghost-sheet costume (with the ninja headband), floating
        gy = 150 + round(3 * wave(t, 4))
        shadow_ellipse(f, 270, 191, 9 - round(wave(t, 4)), 2, "#1e2a24")
        f.put(ghost(28, 30, int(cyc(t, 0.5) * 2), "down"), 256, gy)

    # ------------------------------------------------------------ audio
    def audio(self):
        from engine import audio as A
        T = A.T
        buf = np.zeros((2, A.N))
        for ch in (0, 1):
            wind = A.colored(1.0, 120, 1400, seed=60 + ch) * (0.5 + 0.5 * np.clip(np.sin(TAU * T / 20 + ch), -0.3, 1)) * 0.18
            howl = A.colored(0.0, 480, 680, seed=62 + ch) * np.clip(np.sin(TAU * T / 30 + ch * 1.5), 0, 1) ** 2 * 0.08
            leaves = A.colored(0.0, 3000, 9000, seed=64 + ch) * np.clip(np.sin(TAU * T / 20 + ch), 0, 1) * 0.03
            buf[ch] += wind + howl + leaves
        swell = 0.5 + 0.5 * (np.sin(TAU * T / 12) + 1) / 2
        A.bed(buf, A.cricket_bed(71, 0.58, 4200) * swell * 0.07, A.cricket_bed(72, 0.67, 4550) * swell * 0.06, 1.0)
        A.bed(buf, A.crackle_bed(73, 3.0) * 0.025, A.crackle_bed(74, 3.0) * 0.03, 1.0)
        for i, t0 in enumerate(OWL_T):
            A.place(buf, A.pk(A.hoot(i)), t0, 0.32, pan=-0.75)
        A.place(buf, A.pk(A.caw(3)), CAW_T, 0.8, pan=0.25)
        for k in range(0, 60, GATE_P // 2):
            A.place(buf, A.pk(A.creak(k)), k + 0.3, 1.2, pan=-0.2)
        for t0, pan in ((10.0, 0.0), (45.0, 0.0), (33.0, 0.1)):
            A.place(buf, A.pk(A.squeak(int(t0))), t0, 0.06, pan=pan)
        A.place_sweep(buf, A.pk(A.ghost_woo(5)), WOO_T - 1.0, 0.6, -0.5, 0.5)
        A.place(buf, A.pk(A.bell(9)), BELL_T, 1.2, pan=-0.55)
        for k in range(0, 60, 6):
            for s_ in range(3):
                A.place(buf, A.pk(A.scrape(k + s_, 0.3, 2500, 7000)), k + s_ + 0.2, 0.025, pan=-0.05)
        for k in range(0, 60, 5):
            A.place(buf, A.pk(A.rustle(k, 0.5)), k, 0.04, pan=0.15)
        return A.master(buf)
