"""PXLBLR pixel-art core: one strict pixel grid, ordered dithering, auto outlines.

Every scene is drawn on a 384x216 "art pixel" canvas and scaled 5x (nearest
neighbour) to 1920x1080, so every pixel on screen is an exact 5x5 block. Slow
movers (clouds, boats, dinos) are pasted at screen-pixel offsets so they glide
smoothly while the sprites themselves stay on the grid.
"""
import numpy as np
from PIL import Image, ImageDraw

W, H, S = 384, 216, 5
FPS, DUR = 30, 60
N = FPS * DUR
TAU = 2 * np.pi
INK = "#1a1423"  # the one outline colour used across every PXLBLR scene


def hx(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def rgba(c, a=255):
    return hx(c) + (a,)


BAYER4 = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) + 0.5) / 16


def bayer(h, w):
    return np.tile(BAYER4, (h // 4 + 1, w // 4 + 1))[:h, :w]


def vgrad(stops, w, h, ease=1.0):
    """Vertical gradient that only ever uses the stop colours, ordered-dithered between neighbours."""
    cols = np.array([hx(c) for c in stops], np.uint8)
    n = len(cols)
    t = (np.linspace(0, 1, h) ** ease * (n - 1))[:, None] * np.ones((1, w))
    i0 = np.floor(t).astype(int)
    idx = np.clip(i0 + ((t - i0) > bayer(h, w)), 0, n - 1)
    return cols[idx]


def radial_dither(arr, cx, cy, r, col, band=6.0):
    """Solid disc of `col` with a `band`-px ordered-dither edge (a glow ring, not noise)."""
    h, w = arr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    m = np.clip((r - d) / band, 0, 1) > bayer(h, w)
    arr[m] = hx(col)
    return arr


def sprite(rows, pal):
    h, w = len(rows), max(len(r) for r in rows)
    a = np.zeros((h, w, 4), np.uint8)
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            c = pal.get(ch)
            if c:
                a[y, x] = rgba(c)
    return Image.fromarray(a, "RGBA")


def _mask(a):
    return a[..., 3] > 0


def _shift(m, dy, dx):
    out = np.zeros_like(m)
    h, w = m.shape
    ys, yd = (slice(0, h - dy), slice(dy, h)) if dy >= 0 else (slice(-dy, h), slice(0, h + dy))
    xs, xd = (slice(0, w - dx), slice(dx, w)) if dx >= 0 else (slice(-dx, w), slice(0, w + dx))
    out[yd, xd] = m[ys, xs]
    return out


def outline(img, col=INK):
    """1px outline around the opaque area (canvas needs a 1px transparent margin)."""
    a = np.array(img)
    m = _mask(a)
    d = _shift(m, 1, 0) | _shift(m, -1, 0) | _shift(m, 0, 1) | _shift(m, 0, -1)
    a[d & ~m] = rgba(col)
    return Image.fromarray(a, "RGBA")


def rim(img, col, dy=1, dx=0, skip=(INK,)):
    """Light the edge facing the light source (pixels whose neighbour toward the light is empty)."""
    a = np.array(img)
    m = _mask(a)
    skipm = np.zeros_like(m)
    for s in skip:
        skipm |= np.all(a[..., :3] == hx(s), axis=-1)
    edge = m & ~_shift(m, dy, dx) & ~skipm
    a[edge] = rgba(col)
    return Image.fromarray(a, "RGBA")


def shade(img, col, dy=-2, dx=0, only=None):
    """Darken the side away from the light: pixels within |d| of the far edge."""
    a = np.array(img)
    m = _mask(a)
    if only is not None:
        m &= np.all(a[..., :3] == hx(only), axis=-1)
    e = m & ~_shift(_mask(a), dy, dx)
    a[e] = rgba(col)
    return Image.fromarray(a, "RGBA")


def up(img):
    return img.resize((img.width * S, img.height * S), Image.NEAREST)


def flip(img):
    return img.transpose(Image.FLIP_LEFT_RIGHT)


def wave(t, period, phase=0.0):
    """sin() whose period divides the loop length -> loops seamlessly."""
    assert abs((DUR / period) - round(DUR / period)) < 1e-6, period
    return np.sin(TAU * t / period + phase)


def cyc(t, period, phase=0.0):
    assert abs((DUR / period) - round(DUR / period)) < 1e-6, period
    return ((t / period) + phase) % 1.0


class Frame:
    """Composites native-grid layers and smooth (screen-offset) sprites in z-order."""

    def __init__(self, base):
        self.scr = base.copy()
        self.nat = None

    def layer(self):
        if self.nat is None:
            self.nat = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            self.d = ImageDraw.Draw(self.nat)
        return self.nat

    def draw(self):
        self.layer()
        return self.d

    def put(self, spr, x, y):
        self.layer().paste(spr, (int(round(x)), int(round(y))), spr)

    def arr(self, a, x, y):
        im = Image.fromarray(a, "RGBA")
        self.put(im, x, y)

    def flush(self):
        if self.nat is None:
            return
        bb = self.nat.getbbox()
        if bb:
            c = up(self.nat.crop(bb))
            self.scr.paste(c, (bb[0] * S, bb[1] * S), c)
        self.nat = None

    def smooth(self, spr_up, x, y):
        self.flush()
        self.scr.paste(spr_up, (int(round(x * S)), int(round(y * S))), spr_up)

    def out(self):
        self.flush()
        return self.scr


# ---------------------------------------------------------------- pixel fonts
F57 = {
    "A": ".###.|#...#|#...#|#####|#...#|#...#|#...#", "B": "####.|#...#|#...#|####.|#...#|#...#|####.",
    "C": ".###.|#...#|#....|#....|#....|#...#|.###.", "D": "####.|#...#|#...#|#...#|#...#|#...#|####.",
    "E": "#####|#....|#....|####.|#....|#....|#####", "F": "#####|#....|#....|####.|#....|#....|#....",
    "G": ".###.|#...#|#....|#.###|#...#|#...#|.####",
    "H": "#...#|#...#|#...#|#####|#...#|#...#|#...#", "I": "#####|..#..|..#..|..#..|..#..|..#..|#####",
    "J": "..###|...#.|...#.|...#.|#..#.|#..#.|.##..", "K": "#...#|#..#.|#.#..|##...|#.#..|#..#.|#...#",
    "L": "#....|#....|#....|#....|#....|#....|#####", "M": "#...#|##.##|#.#.#|#.#.#|#...#|#...#|#...#",
    "N": "#...#|##..#|#.#.#|#..##|#...#|#...#|#...#", "O": ".###.|#...#|#...#|#...#|#...#|#...#|.###.",
    "P": "####.|#...#|#...#|####.|#....|#....|#....", "R": "####.|#...#|#...#|####.|#.#..|#..#.|#...#",
    "S": ".####|#....|#....|.###.|....#|....#|####.", "T": "#####|..#..|..#..|..#..|..#..|..#..|..#..",
    "U": "#...#|#...#|#...#|#...#|#...#|#...#|.###.", "V": "#...#|#...#|#...#|#...#|#...#|.#.#.|..#..",
    "W": "#...#|#...#|#...#|#.#.#|#.#.#|##.##|#...#", "X": "#...#|#...#|.#.#.|..#..|.#.#.|#...#|#...#",
    "Y": "#...#|#...#|.#.#.|..#..|..#..|..#..|..#..", "Z": "#####|....#|...#.|..#..|.#...|#....|#####",
    "-": ".....|.....|.....|.###.|.....|.....|.....",
    " ": "...|...|...|...|...|...|...",
}
F35 = {
    "A": "###|#.#|###|#.#|#.#", "B": "##.|#.#|##.|#.#|##.", "C": "###|#..|#..|#..|###", "D": "##.|#.#|#.#|#.#|##.",
    "E": "###|#..|##.|#..|###", "F": "###|#..|##.|#..|#..", "G": "###|#..|#.#|#.#|###", "H": "#.#|#.#|###|#.#|#.#",
    "I": "###|.#.|.#.|.#.|###", "J": "..#|..#|..#|#.#|###", "K": "#.#|#.#|##.|#.#|#.#", "L": "#..|#..|#..|#..|###",
    "M": "#.#|###|###|#.#|#.#", "N": "###|#.#|#.#|#.#|#.#", "O": "###|#.#|#.#|#.#|###", "P": "###|#.#|###|#..|#..",
    "R": "##.|#.#|##.|#.#|#.#", "S": "###|#..|###|..#|###", "T": "###|.#.|.#.|.#.|.#.", "U": "#.#|#.#|#.#|#.#|###",
    "V": "#.#|#.#|#.#|#.#|.#.", "W": "#.#|#.#|###|###|#.#", "X": "#.#|#.#|.#.|#.#|#.#", "Y": "#.#|#.#|.#.|.#.|.#.",
    "Z": "###|..#|.#.|#..|###", "-": "...|...|###|...|...", " ": "..|..|..|..|..",
}


def text_mask(s, font=F57, gap=1):
    glyphs = [font[ch].split("|") for ch in s.upper()]
    h = len(glyphs[0])
    w = sum(len(g[0]) for g in glyphs) + gap * (len(glyphs) - 1)
    m = np.zeros((h, w), bool)
    x = 0
    for g in glyphs:
        for y, row in enumerate(g):
            for i, ch in enumerate(row):
                if ch == "#":
                    m[y, x + i] = True
        x += len(g[0]) + gap
    return m


def text_sprite(s, col, font=F57, shadow=None, out=None, gap=1):
    m = text_mask(s, font, gap)
    h, w = m.shape
    a = np.zeros((h + 3, w + 3, 4), np.uint8)
    if shadow:
        a[2:h + 2, 2:w + 2][m] = rgba(shadow)
    a[1:h + 1, 1:w + 1][m] = rgba(col)
    im = Image.fromarray(a, "RGBA")
    if out:
        im = outline(im, out)
    return im
