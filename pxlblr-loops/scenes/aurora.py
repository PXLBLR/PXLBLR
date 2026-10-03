"""NINJA-BLOKS · Northern Lights Ice Camp — 60 s seamless loop.

Aurora curtains drift on 12/15/20 s cycles with 6 s ray shimmer and are mirrored in the frozen
lake. Other periods: campfire 0.5/0.75 s · steam 3 s · bobber 2 s · penguins 30 s · diamond
dust 10-30 s · telescope sweep 20 s. Events: shooting star at 36 s (Black cheers),
fish caught 48-50 s.
"""
import numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw
from engine.px import (W, H, S, INK, TAU, DUR, rgba, hx, vgrad, radial_dither, bayer, sprite, outline, rim,
                       up, flip, wave, cyc, Frame, _shift)
from engine.bloks import draw_blok, draw_scarf
from scenes.common import draw_bug, shadow_ellipse, _pad, snowy_sign

ICE = 120          # far edge of the frozen lake
SHORE = 160        # near snow bank
STAR_T = 36.0
FISH_T = 48.0
FIRE = (138, 196)

AUR = {"bright": "#d8fff0", "g1": "#5cffaa", "g2": "#22c98a", "t1": "#2ab8b0", "t2": "#1a7a8a", "p1": "#a070ff", "p2": "#5a3ab0"}
CURTAINS = [
    # base y, x-start, x-end, amp1, len, phase
    dict(base=62, xs=-20, xe=250, a1=10, L=40, ph=0.0),
    dict(base=48, xs=150, xe=410, a1=8, L=34, ph=2.1),
]

rng = np.random.default_rng(61)


# ---------------------------------------------------------------- sprites
@lru_cache(maxsize=None)
def penguin(f):
    rows = [
        "..KKK...",
        ".KKKKK..",
        ".KWKWKY.",
        "KKWWWKYY",
        "KKWWWWK.",
        "KKWWWWK.",
        "KKWWWWK.",
        ".KWWWK..",
        "..YY.YY.",
    ]
    if f:
        rows[8] = ".YY..YY."
    return outline(_pad(sprite(rows, {"K": "#1a1e30", "W": "#f4f8ff", "Y": "#ffb030"})), "#0a0c18")


@lru_cache(maxsize=None)
def igloo():
    w, h = 76, 34
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.pieslice([2, 2, 62, 58], 180, 360, fill=rgba("#dfeaf8"))
    d.rectangle([52, 18, 72, 31], fill=rgba("#dfeaf8"))
    d.pieslice([52, 10, 72, 40], 180, 360, fill=rgba("#dfeaf8"))
    for y in range(8, 31, 6):
        d.line([4, y, 62, y], fill=rgba("#a8bedc"))
        for x in range(6 + (y // 6 % 2) * 5, 62, 10):
            d.line([x, y, x, y + 5], fill=rgba("#a8bedc"))
    d.rectangle([60, 21, 70, 31], fill=rgba("#e08a3a"))
    d.pieslice([60, 15, 70, 27], 180, 360, fill=rgba("#e08a3a"))
    d.rectangle([62, 23, 68, 31], fill=rgba("#ffcf6a"))
    im = rim(im, "#ffffff", dy=1, skip=("#a8bedc", "#e08a3a", "#ffcf6a"))
    im = rim(im, "#9fe8cc", dy=0, dx=1, skip=("#a8bedc", "#e08a3a", "#ffcf6a"))
    return outline(im, "#1a2440")


@lru_cache(maxsize=None)
def mug(col="#ec4a35"):
    return sprite(["KKKK.", "KCCKK", "KCCK.K", "KCCKK", ".KK.."], {"K": INK, "C": col})


@lru_cache(maxsize=None)
def fish():
    rows = ["K..KKK..", "KK.KSSK.", "KSKSSSSK", "KK.KSWK.", "K..KKK.."]
    return sprite(rows, {"K": INK, "S": "#8ac8e8", "W": "#ffffff"})


# ---------------------------------------------------------------- scene
class Aurora:
    name = "aurora"

    def __init__(self):
        self.base = up(Image.fromarray(self._static(), "RGB"))
        self.front = up(self._front())
        self.stars = [(int(rng.uniform(0, W)), int(rng.uniform(1, 100)), rng.choice([2, 3, 4, 5, 6]), rng.uniform(0, TAU),
                       rng.choice(["#ffffff", "#cfe0ff", "#ffe8c8"])) for _ in range(80)]
        self.dust = [(rng.uniform(0, W), rng.uniform(0, H), rng.choice([10, 12, 15, 20, 30]), rng.uniform(0, 1), rng.choice([1, 1.5, 2])) for _ in range(30)]
        self.pings = sorted(rng.uniform(0, DUR, 8))
        self.th = bayer(110, W)

    def _static(self):
        img = np.zeros((H, W, 3), np.uint8)
        img[:] = vgrad(["#03061a", "#060c24", "#0a1632", "#0e2040", "#143050", "#1a3e5e"], W, ICE, ease=1.0)[np.minimum(np.arange(H), ICE - 1)]
        a = img
        xs = np.arange(W)
        yy = np.arange(H)[:, None]
        rg = 104 - 26 * np.abs(np.sin(xs / 52.0 + 0.4)) ** 1.5 - 8 * np.abs(np.sin(xs / 14.0))
        mm = (yy >= rg[None, :]) & (yy < ICE)
        a[mm] = hx("#1a2e4a")
        cap = np.clip((rg[None, :] + 7 - yy) / 7.0, 0, 1) * (rg[None, :] < 96)
        a[mm & (cap > bayer(H, W))] = hx("#7a96bc")
        a[mm & (cap > 0.7)] = hx("#a8c0dc")
        a[mm & (yy < rg[None, :] + 1)] = hx("#9fffd0")
        # frozen lake base + cracks
        a[ICE:SHORE + 6] = vgrad(["#18324e", "#1e3c5c", "#25486a", "#2c5476"], W, SHORE + 6 - ICE)
        a[ICE] = hx("#4a7aa0")
        im = Image.fromarray(a)
        d = ImageDraw.Draw(im)
        r = np.random.default_rng(8)
        for _ in range(14):
            x, y = r.uniform(0, W), r.uniform(ICE + 3, SHORE)
            pts = [(x, y)]
            for _ in range(4):
                x += r.uniform(-12, 12); y += r.uniform(-2, 3)
                pts.append((x, min(max(y, ICE + 2), SHORE)))
            d.line(pts, fill=hx("#4e7898"))
        for _ in range(10):
            x, y = r.uniform(0, W), r.uniform(ICE + 4, SHORE - 2)
            d.ellipse([x - r.uniform(4, 12), y - 1, x + r.uniform(4, 12), y + 1], fill=hx("#9ab4d4"))
        return np.array(im)

    def _front(self):
        a = np.zeros((H, W, 4), np.uint8)
        xs = np.arange(W)
        yy = np.arange(H)[:, None]
        bank = SHORE + 2 * np.sin(xs / 23.0) + 1.5 * np.sin(xs / 8.0)
        m = yy >= bank[None, :]
        g = vgrad(["#a8c8d8", "#c8dcee", "#dde8f6", "#ecf2fc"], W, H - SHORE + 4)
        full = np.zeros((H, W, 3), np.uint8)
        full[SHORE - 4:] = g
        a[m, :3] = full[m]
        a[m, 3] = 255
        a[m & (yy < bank[None, :] + 1)] = rgba("#c8ffe8")
        # warm glow from the igloo door + campfire
        for (cx, cy, rr) in ((96, 168, 26), (FIRE[0], FIRE[1], 40)):
            dd = np.sqrt((xs[None, :] - cx) ** 2 + ((yy - cy) * 2.4) ** 2)
            a[m & (np.clip((rr - dd) / 10, 0, 1) > bayer(H, W))] = rgba("#f2dcc0")
            a[m & (np.clip((rr * 0.55 - dd) / 6, 0, 1) > bayer(H, W))] = rgba("#f8c890")
        im = Image.fromarray(a, "RGBA")
        ig = igloo()
        im.paste(ig, (24, 134), ig)
        d = ImageDraw.Draw(im)
        # logs + fire ring
        for (lx, ly) in ((98, 198), (160, 198)):
            d.rounded_rectangle([lx, ly, lx + 26, ly + 6], radius=3, fill=rgba("#8a5a2b"), outline=rgba(INK))
            d.line([lx + 3, ly + 2, lx + 20, ly + 2], fill=rgba("#a8743c"))
            d.line([lx + 2, ly - 1, lx + 24, ly - 1], fill=rgba("#ffffff"))
        for i in range(8):
            ang = np.pi * (0.05 + 0.9 * i / 7)
            sx, sy = FIRE[0] + 11 * np.cos(ang + np.pi), FIRE[1] + 3
            d.ellipse([sx - 3, sy - 2, sx + 3, sy + 2], fill=rgba("#8a8aa0"), outline=rgba(INK))
        # telescope tripod
        d.line([318, 200, 326, 172], fill=rgba("#5a5e78")); d.line([334, 200, 326, 172], fill=rgba("#5a5e78"))
        d.line([326, 200, 326, 172], fill=rgba("#3a3e58"))
        return im

    # ------------------------------------------------------------ aurora
    def _aurora(self, t):
        hh = 110
        out = np.zeros((hh, W, 4), np.uint8)
        xs = np.arange(W)[None, :]
        ys = np.arange(hh)[:, None]
        for c in CURTAINS:
            yb = (c["base"] + c["a1"] * np.sin(xs / 46.0 + TAU * t / 20 + c["ph"]) + 4 * np.sin(xs / 17.0 - TAU * t / 15 + c["ph"] * 2))
            L = c["L"] + 10 * np.sin(xs / 23.0 + TAU * t / 12 + c["ph"])
            ray = 0.62 + 0.38 * np.sin(xs * 0.85 + TAU * t / 6 + 3 * np.sin(xs * 0.07 + c["ph"]))
            env = np.clip(np.sin(np.pi * (xs - c["xs"]) / (c["xe"] - c["xs"])), 0, 1) ** 0.7
            u = (yb - ys) / L
            inside = (u >= 0) & (u <= 1)
            I = np.where(inside, ray * env * (1 - np.clip(u, 0, 1)) ** 1.2 * (0.55 + 0.45 * np.clip(u * 12, 0, 1)), 0)
            I = np.where(inside & (u < 0.06), ray * env, I)
            I = np.clip(I * 1.45, 0, 1)
            on = I > self.th[:hh] * 0.9
            haze = inside & (I > 0.06) & ~on & (out[..., 3] == 0)
            out[haze, :3] = hx("#0f3240") if c["ph"] == 0 else hx("#1a2448")
            out[haze, 3] = 255
            col = np.zeros((hh, W, 3), np.uint8)
            for (lo, hi, k1, k2) in ((0, 0.06, "bright", "g1"), (0.06, 0.45, "g1", "g2"), (0.45, 0.72, "t1", "t2"), (0.72, 1.01, "p1", "p2")):
                band_ = (u >= lo) & (u < hi)
                col[band_ & (I > 0.55)] = hx(AUR[k1])
                col[band_ & (I <= 0.55)] = hx(AUR[k2])
            sel = on & ((out[..., 3] == 0) | np.all(out[..., :3] == hx("#0f3240"), axis=-1) | np.all(out[..., :3] == hx("#1a2448"), axis=-1))
            out[sel, :3] = col[sel]
            out[sel, 3] = 255
        return out

    # ------------------------------------------------------------ per frame
    def frame(self, t):
        t = t % DUR
        f = Frame(self.base)
        d = f.draw()
        for (x, y, p, ph, c) in self.stars:
            if wave(t, p, ph) > -0.3:
                d.point((x, y), fill=rgba(c if wave(t, p, ph) > 0.6 else "#6a7aa8"))
        f.flush()
        aur = self._aurora(t)
        # the sky part (masked by mountains drawn in base? aurora sits behind the peaks)
        sky = aur.copy()
        base_np = np.asarray(Image.fromarray(self._static_cache()).crop((0, 0, W, 110)))
        mtn = np.any(base_np != self._skyonly()[:110], axis=-1)
        sky[mtn] = 0
        f.arr(sky, 0, 0)
        # shooting star
        if STAR_T <= t <= STAR_T + 1.2:
            k = (t - STAR_T) / 1.2
            hx_, hy = 310 - 130 * k, 10 + 34 * k
            d = f.draw()
            fade = 1 - max(0.0, (k - 0.8) / 0.2)
            tail = 60 * fade
            ex, ey = hx_ + tail * 0.95, hy - tail * 0.32
            mx, my = hx_ + tail * 0.35, hy - tail * 0.12
            d.line([ex, ey, mx, my], fill=rgba("#5a7ac8"))
            d.line([mx, my, hx_, hy], fill=rgba("#cfe8ff"))
            d.line([mx * 0.5 + hx_ * 0.5, my * 0.5 + hy * 0.5 + 1, hx_, hy + 1], fill=rgba("#8ab0f0"))
            d.rectangle([hx_ - 1, hy - 1, hx_ + 1, hy + 1], fill=rgba("#ffffff"))
            d.point((hx_ - 2, hy), fill=rgba("#cfe8ff")); d.point((hx_, hy + 2), fill=rgba("#cfe8ff"))
        # aurora reflected in the ice: mirrored, dimmed, every other pixel
        refl = np.zeros((SHORE - ICE, W, 4), np.uint8)
        rows = np.clip((96 - np.arange(SHORE - ICE) * 2.2).astype(int), 0, aur.shape[0] - 1)
        src = aur[rows]  # compressed mirror: the lake shows the curtains' lower glow
        if src is not None:
            yy, xx = np.mgrid[0:src.shape[0], 0:W]
            keep = (src[..., 3] > 0) & ((xx + yy + int(cyc(t, 0.5) * 2)) % 2 == 0)
            refl[keep, :3] = (src[keep, :3].astype(int) * 0.55 + np.array(hx("#1e3c5c")) * 0.45).astype(np.uint8)
            refl[keep, 3] = 255
            f.arr(refl, 0, ICE + 1)
        # penguins waddling across the ice (30 s)
        for i in range(3):
            px_ = W - (cyc(t, 30) * 470 - 40) + i * 14
            wob = int(cyc(t, 0.5, i * 0.3) * 2)
            f.put(penguin(wob), px_, 134 + (i % 2) - wob)
        # Blue ice fishing
        self._fishing(f, t)
        # snow bank, igloo, fire ring
        f.smooth(self.front, 0, 0)
        self._camp(f, t)
        # Black + telescope
        cheer = STAR_T + 0.3 <= t <= STAR_T + 3.5
        d = f.draw()
        ang = np.radians(-35 + 6 * wave(t, 20))
        x0, y0 = 326, 172
        x1, y1 = x0 - 18 * np.cos(ang), y0 + 18 * np.sin(ang)
        d.line([x0, y0, x1, y1], fill=rgba("#c9ccd8"), width=3)
        d.line([x0, y0 - 1, x1, y1 - 1], fill=rgba("#ffffff"))
        d.rectangle([x1 - 2, y1 - 2, x1 + 1, y1 + 2], fill=rgba("#5a5e78"))
        draw_blok(f, "black", 336, 170 - (4 if cheer and int(t * 4) % 2 else 0), t, eyes="happy" if cheer else -1,
                  mouth="open" if cheer else "smile", arms="up" if cheer else "down", flipx=True, blink_phase=0.55)
        draw_scarf(f, 336, 170 - (4 if cheer and int(t * 4) % 2 else 0), t, flipx=True, col="#ffd23f", stripe="#ec4a35")
        f.put(snowy_sign(), 200, 168)
        # diamond dust
        d = f.draw()
        for (x0_, y0_, p, ph, tw) in self.dust:
            a = cyc(t, p, ph)
            y = (y0_ + a * H * 0.5) % H
            x = x0_ + 4 * np.sin(TAU * a * 2)
            if wave(t, tw, ph * 9) > 0.5:
                d.point((x, y), fill=rgba("#e8fff4" if wave(t, tw, ph * 9) > 0.85 else "#8ad8c0"))
        draw_bug(f)
        return f.out()

    @lru_cache(maxsize=None)
    def _static_cache(self):
        return self._static()

    @lru_cache(maxsize=None)
    def _skyonly(self):
        img = np.zeros((H, W, 3), np.uint8)
        img[:] = vgrad(["#03061a", "#060c24", "#0a1632", "#0e2040", "#143050", "#1a3e5e"], W, ICE, ease=1.0)[np.minimum(np.arange(H), ICE - 1)]
        return img

    def _fishing(self, f, t):
        bx, by = 236, 124
        hx_, hy = 282, 152
        d = f.draw()
        d.ellipse([hx_ - 8, hy - 2, hx_ + 8, hy + 2], fill=rgba("#0a1a2e"), outline=rgba("#cfe0f4"))
        rr = cyc(t, 2) * 5
        d.ellipse([hx_ - 2 - rr, hy - 0.5, hx_ + 2 + rr, hy + 0.5 + rr * 0.15], outline=rgba("#3a6a9a"))
        d.rectangle([bx + 6, by + 26, bx + 22, by + 29], fill=rgba("#8a5a2b"))
        draw_blok(f, "blue", bx, by, t, eyes=1, blink_phase=0.35)
        draw_scarf(f, bx, by, t, col="#ff74b3", stripe="#ffffff")
        d = f.draw()
        k = t - FISH_T
        tug = 0 <= k <= 2.0
        tip = (bx + 44, by + 4 + (-4 if tug else round(wave(t, 4))))
        d.line([bx + 26, by + 20, tip[0], tip[1]], fill=rgba("#8a5a2b"))
        if 0 <= k <= 1.6:
            u = k / 1.6
            fx, fy = hx_ - 4 - 10 * u, hy - 4 - 30 * 4 * u * (1 - u)
            d.line([tip[0], tip[1], fx + 4, fy + 2], fill=rgba("#f4f0e6"))
            f.put(fish() if u < 0.5 else flip(fish()), fx, fy)
            if u < 0.15 or u > 0.85:
                for i in range(4):
                    d.point((hx_ - 3 + i * 2, hy - 3 - (i % 2)), fill=rgba("#ffffff"))
        else:
            d.line([tip[0], tip[1], hx_, hy], fill=rgba("#f4f0e6"))

    def _camp(self, f, t):
        cx, cy = FIRE
        d = f.draw()
        d.line([cx - 6, cy + 1, cx + 6, cy - 1], fill=rgba("#6b4220"), width=2)
        d.line([cx - 6, cy - 1, cx + 6, cy + 1], fill=rgba("#7a4a22"), width=2)
        for dx in range(-5, 6):
            hgt = (11 - 0.3 * dx * dx) * (0.78 + 0.12 * wave(t, 0.5, dx * 1.7) + 0.1 * wave(t, 0.75, dx * 0.9))
            for kk in range(int(max(0, hgt))):
                fr = kk / max(hgt, 1)
                col = "#fff6c4" if fr < 0.25 and abs(dx) < 2 else "#ffd23f" if fr < 0.5 else "#ff8a2a" if fr < 0.8 else "#e8402f"
                d.point((cx + dx, cy - 1 - kk), fill=rgba(col))
        for i in range(5):
            a = cyc(t, (1.5, 2, 2.5, 3)[i % 4], i / 5)
            if a < 0.8:
                d.point((cx - 3 + i * 1.5 + 3 * np.sin(a * 5 + i), cy - 12 - 24 * a), fill=rgba("#ffd23f" if a < 0.4 else "#ff8a2a"))
        for name, x, fl, col, st, mc in (("red", 98, False, "#2a8a4a", "#ffffff", "#ffffff"), ("pink", 158, True, "#8a3ff0", "#ffd23f", "#3a92f0")):
            sip = cyc(t, 6, 0.5 if fl else 0) < 0.25
            draw_blok(f, name, x, 170, t, eyes="happy" if sip else (-1 if fl else 1), flipx=fl, blink_phase=0.2 if fl else 0.7)
            draw_scarf(f, x, 170, t, flipx=fl, col=col, stripe=st)
            mx = x - 3 if fl else x + 24
            my = 184 - (4 if sip else 0)
            f.put(mug(mc), mx, my)
            d = f.draw()
            for i in range(3):
                a = cyc(t, 3, i / 3 + (0.5 if fl else 0))
                d.point((mx + 2 + round(1.5 * np.sin(TAU * a + i)), my - 2 - 10 * a), fill=rgba("#eef4ff" if a < 0.5 else "#8a9ac0"))

    # ------------------------------------------------------------ audio
    def audio(self):
        from engine import audio as A
        T = A.T
        buf = np.zeros((2, A.N))
        for ch in (0, 1):
            wind = A.colored(1.4, 60, 900, seed=900 + ch) * (0.4 + 0.6 * np.clip(np.sin(TAU * T / 30 + ch * 1.7), 0, 1) ** 1.5) * 0.22
            whistle = A.colored(0.0, 1500, 2200, seed=902 + ch) * np.clip(np.sin(TAU * T / 20 + ch * 2), 0, 1) ** 4 * 0.03
            sheen = A.colored(0.0, 6000, 12000, seed=904 + ch) * (0.5 + 0.5 * np.sin(TAU * T / 12 + ch)) * 0.012
            buf[ch] += wind + whistle + sheen
        fire = A.crackle_bed(906, 4.0)
        fire_low = A.colored(1.4, 50, 300, seed=907) * (0.8 + 0.2 * np.sin(TAU * T / 0.75))
        A.bed(buf, fire * 0.06 + fire_low * 0.05, fire * 0.04 + fire_low * 0.03, 1.0)
        r = np.random.default_rng(910)
        for i, t0 in enumerate(self.pings):
            A.place(buf, A.pk(A.ice_ping(920 + i)), t0, 0.5, pan=r.uniform(-0.8, 0.8))
        for base_t in (15.0, 45.0):
            for i, dt in enumerate((-0.8, 0.1, 0.9)):
                A.place(buf, A.pk(A.squawk(int(base_t) * 3 + i)), base_t + dt, 0.45, pan=0.3 - 0.3 * i)
        A.place(buf, A.pk(A.shimmer(7)), STAR_T, 0.30, pan=0.3)
        A.place(buf, A.pk(A.splash(11, 0.6)), FISH_T, 0.40, pan=0.45)
        A.place(buf, A.pk(A.splash(12, 0.6)), FISH_T + 1.5, 0.35, pan=0.4)
        for k in range(3):
            A.place(buf, A.pk(A.thud(30 + k)), FISH_T + 0.5 + k * 0.25, 0.08, pan=0.42)
        return A.master(buf)
