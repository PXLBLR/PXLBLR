"""ACLSMED brand tokens + font/text helpers shared by reels and carousels."""
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "fonts"
ASSETS = ROOT / "assets"

# Brand (aclsmed-web.md): Red #EF4444, Navy #05081A, Cyan #00DCC8.
NAVY = (5, 8, 26)
NAVY_2 = (12, 18, 44)
NAVY_3 = (22, 30, 64)
RED = (239, 68, 68)
CYAN = (0, 220, 200)
WHITE = (255, 255, 255)
DIM = (148, 163, 184)
# Monitor trace colours from simulator.html
ECG_GREEN = (0, 230, 64)
YELLOW = (232, 208, 32)
ORANGE = (255, 140, 32)
MAGENTA = (232, 64, 232)

WEIGHTS = {"regular": 400, "medium": 500, "semibold": 600, "bold": 700, "extrabold": 800, "black": 900}
FAMILIES = {"display": "Outfit.ttf", "body": "DMSans.ttf", "mono": "JetBrainsMono.ttf"}


@lru_cache(maxsize=256)
def font(size: int, weight: str = "bold", family: str = "display") -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(str(FONTS / FAMILIES[family]), size)
    axes = f.get_variation_axes()
    w = WEIGHTS[weight]
    if family == "mono":
        w = min(w, 800)
    vals = []
    for ax in axes:
        name = ax["name"].decode() if isinstance(ax["name"], bytes) else ax["name"]
        if name == "Weight":
            vals.append(max(ax["minimum"], min(ax["maximum"], w)))
        elif name == "Optical size":
            vals.append(max(ax["minimum"], min(ax["maximum"], min(size, 40))))
        else:
            vals.append(ax["default"])
    f.set_variation_by_axes(vals)
    return f


def text_w(txt: str, f) -> int:
    l, _, r, _ = f.getbbox(txt)
    return r - l


def wrap(txt: str, f, max_w: int) -> list[str]:  # plain wrap (no accents)
    """Greedy word wrap; honours explicit newlines."""
    out = []
    for para in txt.split("\n"):
        line = ""
        for word in para.split(" "):
            trial = (line + " " + word).strip()
            if text_w(trial, f) <= max_w or not line:
                line = trial
            else:
                out.append(line)
                line = word
        out.append(line)
    return out


def layout(txt, f, max_w):
    """Greedy wrap over tokens. Returns lines of [(word, accent, glue_left)]."""
    # Track glue (no space before) for tokens produced by a '*' toggle mid-word.
    toks, acc, word, glue, nl = [], False, "", False, False
    for ch in txt:
        if ch == "*":
            if word:
                toks.append((word, acc, glue, nl)); word, nl = "", False
                glue = True
            acc = not acc
        elif ch in " \n":
            if word:
                toks.append((word, acc, glue, nl)); word, nl = "", False
            glue = False
            if ch == "\n":
                nl = True
        else:
            word += ch
    if word:
        toks.append((word, acc, glue, nl))
    sp = f.getlength(" ")
    lines, cur, cur_w = [], [], 0.0
    for w, a, g, n in toks:
        ww = f.getlength(w)
        add = ww + (0 if (g or not cur) else sp)
        if cur and (n or cur_w + add > max_w) and not g:
            lines.append(cur); cur, cur_w = [], 0.0
            add = ww
        cur.append((w, a, g and bool(cur)))
        cur_w += add
    if cur:
        lines.append(cur)
    return lines


def line_width(line, f):
    sp = f.getlength(" ")
    return sum(f.getlength(w) + (0 if (g or i == 0) else sp) for i, (w, a, g) in enumerate(line))


def draw_line(d, x, y, line, f, color, accent, shadow=False, stroke=0):
    sp = f.getlength(" ")
    for i, (w, a, g) in enumerate(line):
        if i and not g:
            x += sp
        if shadow:
            d.text((x + 3, y + 4), w, font=f, fill=(0, 0, 0, 150))
        d.text((x, y), w, font=f, fill=accent if a else color, stroke_width=stroke, stroke_fill=NAVY)
        x += f.getlength(w)


def text_block(txt, size, max_w, color=WHITE, accent=RED, weight="bold", family="display",
               align="center", line_gap=1.12, stroke=0, shadow=True) -> Image.Image:
    """Render wrapped text (with *accent* runs) to an RGBA image max_w+24 wide, cropped vertically."""
    f = font(size, weight, family)
    lines = layout(txt, f, max_w)
    asc, desc = f.getmetrics()
    lh = int(size * line_gap)
    h = lh * len(lines) + desc + 16
    w = max_w + 24
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, ln in enumerate(lines):
        lw = line_width(ln, f)
        x = 12 if align == "left" else 12 + (max_w - lw) / 2
        draw_line(d, x, 6 + i * lh, ln, f, color, accent, shadow=shadow, stroke=stroke)
    bbox = img.getbbox()
    if bbox:
        img = img.crop((0, max(0, bbox[1] - 4), w, min(h, bbox[3] + 6)))
    return img


def pill(txt, size=34, fg=WHITE, bg=RED, pad=(26, 12), weight="bold", family="display", radius=None):
    f = font(size, weight, family)
    l, t, r, b = f.getbbox(txt)
    w, h = r - l + pad[0] * 2, (b - t) + pad[1] * 2
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=radius if radius is not None else h // 2, fill=bg)
    d.text((pad[0] - l, pad[1] - t), txt, font=f, fill=fg)
    return img


def icon(size=64, radius=0.22):
    """ACLSMED app icon (assets/icon.png) with app-style rounded corners."""
    im = Image.open(ASSETS / "icon.png").convert("RGBA").resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size * 4 - 1, size * 4 - 1), radius=int(size * 4 * radius), fill=255)
    im.putalpha(mask.resize((size, size), Image.LANCZOS))
    return im


def logo_mark(height=54):
    """ACLSMED icon + wordmark."""
    f = font(int(height * 0.74), "black")
    tw = text_w("ACLSMED", f)
    gap = int(height * 0.28)
    img = Image.new("RGBA", (height + gap + tw + 10, height), (0, 0, 0, 0))
    ic = icon(height)
    img.paste(ic, (0, 0), ic)
    d = ImageDraw.Draw(img)
    l, t, r, b = f.getbbox("ACLSMED")
    y = (height - (b - t)) // 2 - t
    d.text((height + gap - l, y), "ACLS", font=f, fill=WHITE)
    d.text((height + gap - l + f.getlength("ACLS"), y), "MED", font=f, fill=RED)
    return img
