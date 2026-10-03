"""Props shared by every PXLBLR loop: the branded wooden sign and the corner bug."""
import numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw
from engine.px import (W, H, INK, rgba, hx, outline, rim, text_mask, text_sprite, F57, F35, sprite)
from engine.bloks import blok_icon

WOOD = dict(main="#c08548", dark="#94592c", light="#e0a468", carve="#4a2a14", post="#7a4a24")


@lru_cache(maxsize=None)
def sign(line1="PXLBLR", line2="NINJA-BLOKS"):
    """Two-plank signpost. Plank 1: brand wordmark (5x7). Plank 2: arrow plank with series name (3x5)."""
    m1 = text_mask(line1, F57)
    m2 = text_mask(line2, F35)
    w1, w2 = m1.shape[1] + 8, m2.shape[1] + 10
    cw = max(w1, w2) + 6
    ch = 40
    im = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    px = cw // 2 - 1
    d.rectangle([px, 8, px + 2, ch - 2], fill=rgba(WOOD["post"]))
    d.line([px + 2, 8, px + 2, ch - 2], fill=rgba("#5c361a"))

    def plank(x0, y0, w, h, arrow=False):
        d.rectangle([x0, y0, x0 + w - 1, y0 + h - 1], fill=rgba(WOOD["main"]))
        if arrow:
            for i in range(h):
                k = min(i, h - 1 - i)
                d.line([x0 + w, y0 + i, x0 + w + k, y0 + i], fill=rgba(WOOD["main"]))
        d.line([x0, y0, x0 + w - 1, y0], fill=rgba(WOOD["light"]))
        d.line([x0, y0 + h - 1, x0 + w - 1, y0 + h - 1], fill=rgba(WOOD["dark"]))
        for gx in range(x0 + 3, x0 + w - 2, 7):
            d.point((gx, y0 + h // 2 + (gx // 7) % 2), fill=rgba(WOOD["dark"]))
        d.point((x0 + 1, y0 + 1), fill=rgba("#e8e4dc"))
        d.point((x0 + w - 2, y0 + 1), fill=rgba("#e8e4dc"))

    plank((cw - w1) // 2, 1, w1, 11)
    plank((cw - w2) // 2 - 2, 15, w2, 9, arrow=True)
    a = np.array(im)
    x1, x2 = (cw - m1.shape[1]) // 2, (cw - w2) // 2 + 3
    hl = np.zeros(a.shape[:2], bool)
    hl[3 + 1:3 + 1 + 7, x1:x1 + m1.shape[1]] |= m1
    hl[17 + 1:17 + 1 + 5, x2:x2 + m2.shape[1]] |= m2
    a[hl] = rgba(WOOD["light"])
    cm = np.zeros(a.shape[:2], bool)
    cm[3:10, x1:x1 + m1.shape[1]] |= m1
    cm[17:22, x2:x2 + m2.shape[1]] |= m2
    a[cm] = rgba(WOOD["carve"])
    # brand red emblem on the post
    im = Image.fromarray(a, "RGBA")
    return outline(_pad(im))


def _pad(im, p=1):
    out = Image.new("RGBA", (im.width + 2 * p, im.height + 2 * p), (0, 0, 0, 0))
    out.paste(im, (p, p))
    return out


@lru_cache(maxsize=None)
def bug():
    """Corner brand bug: Blok icon + PXLBLR wordmark + NINJA-BLOKS, all on the scene's pixel grid."""
    icon = outline(_pad(blok_icon()))
    t1 = text_sprite("PXLBLR", "#ffffff", F57, shadow=INK, out=INK)
    t2 = text_sprite("NINJA-BLOKS", "#ffd23f", F35, shadow=INK, out=INK)
    w = icon.width + 2 + max(t1.width, t2.width)
    im = Image.new("RGBA", (w, 18), (0, 0, 0, 0))
    im.paste(icon, (0, 1), icon)
    im.paste(t1, (icon.width + 1, 0), t1)
    im.paste(t2, (icon.width + 1, 10), t2)
    return im


def draw_bug(frame, x=5, y=5):
    frame.put(bug(), x, y)


def shadow_ellipse(frame, cx, cy, rx, ry, col):
    frame.draw().ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=rgba(col))


class Snow:
    """Looping snowfall: each layer falls a whole number of screen heights per minute and sways."""

    def __init__(self, seed=0, layers=((90, 1, "#c8d4f0", 12, 3), (60, 1, "#e8eeff", 18, 4), (26, 2, "#ffffff", 26, 5))):
        from engine.px import DUR
        r = np.random.default_rng(seed)
        self.layers = []
        for (n, size, col, k, sway) in layers:
            pts = [(r.uniform(0, W), r.uniform(0, H), r.choice([2, 3, 4, 5]), r.uniform(0, 6.28)) for _ in range(n)]
            self.layers.append((pts, size, col, H * k / DUR, sway))

    def draw(self, frame, t, layer, x0=0, x1=W):
        from engine.px import wave
        d = frame.draw()
        pts, size, col, vy, sway = self.layers[layer]
        for (x, y, p, ph) in pts:
            yy = (y + vy * t) % H
            xx = (x + sway * wave(t, p, ph) + yy * 0.08) % W
            if x0 <= xx < x1:
                if size == 1:
                    d.point((xx, yy), fill=rgba(col))
                else:
                    d.rectangle([xx, yy, xx + 1, yy + 1], fill=rgba(col))


@lru_cache(maxsize=None)
def snowy_sign():
    """The brand signpost with snow piled on both planks."""
    s = sign().copy()
    a = np.array(s)
    m = a[..., 3] > 0
    from engine.px import _shift
    top = m & ~_shift(m, 1, 0)
    ys, xs = np.nonzero(top)
    for y, x in zip(ys, xs):
        if y < 26 and abs(x - s.width // 2) > 2:
            a[max(0, y - 1), x] = rgba("#ffffff")
            a[y, x] = rgba("#e2ecff")
    return outline(_pad(Image.fromarray(a, "RGBA")))
