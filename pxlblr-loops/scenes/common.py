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
