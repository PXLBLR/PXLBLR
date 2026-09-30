"""1080x1350 (4:5) carousel slide renderer. A carousel is {"id", "slides": [[block, ...], ...]}.

Blocks (tuples):  ("kicker", txt, color) · ("title", txt, size) · ("body", txt, size) · ("big", txt, size, color)
  ("ecg", rhythm, kw, label, color, height, seconds) · ("rows", [(name, clue, fix), ...])
  ("stats", [(label, value, note), ...]) · ("bullets", [txt, ...], size) · ("callout", txt, color)
  ("wrongright", wrong, right) · ("table", headers, rows) · ("spacer", px) · ("swipe",) · ("cta",)
Text supports *accent* runs.
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from . import ecg
from .brand import CYAN, DIM, NAVY, NAVY_2, NAVY_3, RED, WHITE, YELLOW, font, logo_mark, pill, text_block

W, H = 1080, 1350
X0, X1 = 72, 1008
CW = X1 - X0


def _mix(c, bg, a):
    return tuple(int(bg[i] + (c[i] - bg[i]) * a) for i in range(3))


def bg():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    g = _mix(NAVY_3, NAVY, 0.45)
    for x in range(0, W, 45):
        d.line([(x, 0), (x, H)], fill=g)
    for y in range(0, H, 45):
        d.line([(0, y), (W, y)], fill=g)
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse((-250, -450, W + 250, 650), fill=80)
    glow = glow.filter(ImageFilter.GaussianBlur(150))
    img = Image.composite(Image.new("RGB", (W, H), NAVY_2), img, glow)
    return img


def draw_strip(img, x, y, w, h, rhythm, kw, label, color, seconds):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((x, y, x + w, y + h), radius=22, fill=(8, 12, 30), outline=NAVY_3, width=3)
    # ECG paper minor grid inside the panel
    gx = _mix(color, (8, 12, 30), 0.08)
    for gxp in range(x + 20, x + w - 10, 24):
        d.line([(gxp, y + 50), (gxp, y + h - 14)], fill=gx)
    for gyp in range(y + 50, y + h - 10, 24):
        d.line([(x + 14, gyp), (x + w - 14, gyp)], fill=gx)
    d.text((x + 22, y + 14), label, font=font(28, "bold", "mono"), fill=color)
    sig, _ = ecg.make(rhythm, seconds, **(kw or {}))
    ix0, iw = x + 22, w - 44
    base = y + 50 + (h - 64) * 0.64
    gain = (h - 64) * 0.40
    xs = np.linspace(0, sig.size - 1, iw).astype(int)
    pts = [(ix0 + i, float(np.clip(base - sig[j] * gain, y + 52, y + h - 12))) for i, j in enumerate(xs)]
    for wdt, k in ((10, 0.15), (6, 0.35), (3, 1.0)):
        d.line(pts, fill=_mix(color, (8, 12, 30), k), width=wdt, joint="curve")
    return h


class Slide:
    TOP, BOTTOM = 140, H - 110

    def __init__(self, idx, total, y0=None):
        self.img = bg()
        self.d = ImageDraw.Draw(self.img)
        self.y = self.TOP if y0 is None else y0
        self.idx, self.total = idx, total

    def paste(self, im, x=None, y=None):
        x = X0 - 12 if x is None else x
        y = self.y if y is None else y
        self.img.paste(im, (int(x), int(y)), im)
        return im.height

    def text(self, txt, size, weight="bold", family="display", color=WHITE, accent=RED, gap=18, align="left",
             line_gap=1.14):
        im = text_block(txt, size, CW, color=color, accent=accent, weight=weight, family=family, align=align,
                        line_gap=line_gap, shadow=False)
        self.y += self.paste(im) + gap

    def chrome(self):
        lg = logo_mark(40)
        self.img.paste(lg, (X0, 62), lg)
        f = font(26, "bold", "mono")
        c = f"{self.idx + 1:02d}/{self.total:02d}"
        self.d.text((X1 - f.getlength(c), 70), c, font=f, fill=DIM)
        # progress dots
        n = self.total
        dw = 16
        tot = n * dw + (n - 1) * 10
        sx = (W - tot) // 2
        for i in range(n):
            col = RED if i == self.idx else NAVY_3
            wdt = 34 if i == self.idx else dw
            xx = sx + i * (dw + 10) + (0 if i <= self.idx else 18)
            self.d.rounded_rectangle((xx, H - 58, xx + wdt, H - 50), radius=4, fill=col)
        self.d.text((X0, H - 70), "@aclsmed", font=font(26, "semibold", "body"), fill=DIM)
        tag = "Educational only"
        tf = font(22, "regular", "body")
        self.d.text((X1 - tf.getlength(tag), H - 66), tag, font=tf, fill=_mix(DIM, NAVY, 0.7))

    # ---- blocks ----
    def block(self, b):
        k = b[0]
        if k == "kicker":
            col = b[2] if len(b) > 2 else RED
            fg = NAVY if col in (CYAN, YELLOW) else WHITE
            self.y += self.paste(pill(b[1], 28, fg=fg, bg=col, pad=(22, 10)), x=X0) + 26
        elif k == "title":
            self.text(b[1], b[2] if len(b) > 2 else 78, "extrabold", gap=24, line_gap=1.08)
        elif k == "body":
            self.text(b[1], b[2] if len(b) > 2 else 40, "medium", "body", color=(214, 222, 236), accent=CYAN,
                      gap=22, line_gap=1.3)
        elif k == "big":
            self.text(b[1], b[2], "black", color=b[3] if len(b) > 3 else RED, gap=10, line_gap=1.0)
        elif k == "spacer":
            self.y += b[1]
        elif k == "ecg":
            _, rh, kw, label, color, hh, secs = b
            self.y += draw_strip(self.img, X0, self.y, CW, hh, rh, kw, label, color, secs) + 26
        elif k == "rows":
            self.rows(b[1], b[2] if len(b) > 2 else None)
        elif k == "stats":
            self.stats(b[1])
        elif k == "bullets":
            size = b[2] if len(b) > 2 else 40
            for t in b[1]:
                self.d.ellipse((X0 + 2, self.y + size * 0.42, X0 + 16, self.y + size * 0.42 + 14), fill=RED)
                im = text_block(t, size, CW - 44, color=WHITE, accent=CYAN, weight="semibold", family="body",
                                align="left", line_gap=1.25, shadow=False)
                self.img.paste(im, (X0 + 24, int(self.y)), im)
                self.y += im.height + 18
            self.y += 8
        elif k == "callout":
            col = b[2] if len(b) > 2 else CYAN
            im = text_block(b[1], 38, CW - 80, color=WHITE, accent=col, weight="semibold", family="body",
                            align="left", line_gap=1.28, shadow=False)
            h = im.height + 44
            self.d.rounded_rectangle((X0, self.y, X1, self.y + h), radius=20, fill=_mix(col, NAVY, 0.12))
            self.d.rounded_rectangle((X0, self.y, X0 + 10, self.y + h), radius=5, fill=col)
            self.img.paste(im, (X0 + 34, int(self.y + 22)), im)
            self.y += h + 24
        elif k == "wrongright":
            self.wrongright(b[1], b[2])
        elif k == "table":
            self.table(b[1], b[2])
        elif k == "swipe":
            p = pill("SWIPE  →", 32, fg=NAVY, bg=CYAN, pad=(28, 14))
            self.img.paste(p, (X1 - p.width, H - 170), p)
        elif k == "cta":
            self.cta()
        elif k == "pairs":
            self.pairs(b[1], b[2])

    def rows(self, rows, heads=None):
        for name, clue, fix in rows:
            top = self.y
            nm = text_block(name, 38, CW - 60, color=WHITE, accent=RED, weight="extrabold", align="left",
                            shadow=False)
            cl = text_block(clue, 32, CW - 60, color=DIM, accent=YELLOW, weight="medium", family="body",
                            align="left", line_gap=1.2, shadow=False)
            fx = text_block("→ " + fix, 33, CW - 60, color=CYAN, accent=WHITE, weight="bold", family="body",
                            align="left", line_gap=1.2, shadow=False)
            h = nm.height + cl.height + fx.height + 44
            self.d.rounded_rectangle((X0, top, X1, top + h), radius=18, fill=(10, 15, 36), outline=NAVY_3, width=2)
            yy = top + 14
            for im, gap in ((nm, 4), (cl, 4), (fx, 0)):
                self.img.paste(im, (X0 + 12, int(yy)), im)
                yy += im.height + gap
            self.y = top + h + 14

    def stats(self, rows):
        for label, value, note in rows:
            top = self.y
            vim = text_block(value, 60, 540, color=RED, accent=CYAN, weight="black", align="left", shadow=False)
            lim = text_block(label, 38, 400, color=WHITE, accent=CYAN, weight="bold", align="left", shadow=False)
            nim = text_block(note, 31, CW - 40, color=DIM, accent=YELLOW, weight="medium", family="body",
                             align="left", line_gap=1.2, shadow=False) if note else None
            h = max(vim.height, lim.height) + (nim.height + 6 if nim else 0) + 36
            self.d.rounded_rectangle((X0, top, X1, top + h), radius=18, fill=(10, 15, 36), outline=NAVY_3, width=2)
            self.img.paste(lim, (X0 + 14, int(top + 22 + (vim.height - lim.height) / 2)), lim)
            vx = X1 - 24 - (max(0, vim.getbbox()[2]) if vim.getbbox() else vim.width)
            self.img.paste(vim, (int(vx), int(top + 16)), vim)
            if nim:
                self.img.paste(nim, (X0 + 14, int(top + 20 + max(vim.height, lim.height))), nim)
            self.y = top + h + 14

    def wrongright(self, wrong, right):
        for tag, txt, col in (("WRONG", wrong, RED), ("RIGHT", right, (34, 197, 94))):
            p = pill(tag, 26, fg=WHITE, bg=col, pad=(18, 8))
            im = text_block(txt, 40, CW - 60, color=WHITE, accent=col if tag == "RIGHT" else YELLOW,
                            weight="semibold", family="body", align="left", line_gap=1.25, shadow=False)
            h = p.height + im.height + 56
            top = self.y
            self.d.rounded_rectangle((X0, top, X1, top + h), radius=20, fill=_mix(col, NAVY, 0.10),
                                     outline=_mix(col, NAVY, 0.55), width=3)
            self.img.paste(p, (X0 + 24, int(top + 22)), p)
            self.img.paste(im, (X0 + 14, int(top + 34 + p.height)), im)
            self.y = top + h + 22

    def table(self, headers, rows):
        colw = [CW * 0.30, CW * 0.36, CW * 0.34]
        hf = font(26, "bold", "mono")
        x = X0
        for i, hd in enumerate(headers):
            self.d.text((x + 14, self.y), hd, font=hf, fill=CYAN)
            x += colw[i]
        self.y += 46
        for r in rows:
            ims = []
            for i, cell in enumerate(r):
                ims.append(text_block(cell, 30 if i else 32, int(colw[i]) - 30,
                                      color=WHITE if i == 0 else (214, 222, 236), accent=RED,
                                      weight="extrabold" if i == 0 else "medium",
                                      family="display" if i == 0 else "body", align="left", line_gap=1.18,
                                      shadow=False))
            h = max(im.height for im in ims) + 30
            self.d.rounded_rectangle((X0, self.y, X1, self.y + h), radius=14, fill=(10, 15, 36), outline=NAVY_3,
                                     width=2)
            x = X0
            for i, im in enumerate(ims):
                self.img.paste(im, (int(x + 4), int(self.y + 15)), im)
                x += colw[i]
            self.y += h + 10

    def pairs(self, heads, rows):
        half = (CW - 16) // 2
        for i, hd in enumerate(heads):
            self.d.text((X0 + i * (half + 16) + 8, self.y), hd, font=font(30, "bold", "mono"),
                        fill=CYAN if i == 0 else RED)
        self.y += 48
        for l, r in rows:
            for i, txt in enumerate((l, r)):
                x = X0 + i * (half + 16)
                self.d.rounded_rectangle((x, self.y, x + half, self.y + 92), radius=16, fill=(10, 15, 36),
                                         outline=NAVY_3, width=2)
                im = text_block(txt, 36, half - 40, color=WHITE, accent=RED, weight="extrabold", align="left",
                                shadow=False)
                self.img.paste(im, (int(x + 8), int(self.y + 46 - im.height / 2)), im)
            self.y += 104

    def cta(self):
        self.y = 250
        self.text("Save this.\nShare it with your *code team.*", 80, "extrabold", gap=40, line_gap=1.08)
        p = pill("FOLLOW  @ACLSMED", 44, pad=(34, 18))
        self.y += self.paste(p, x=X0) + 44
        self.text("A new ACLS drill every day, reels in the morning, cheat sheets at night.", 40, "medium",
                  "body", color=(214, 222, 236), gap=40, line_gap=1.3)
        self.text("Run full megacodes on a live monitor, defib & crash cart in the *ACLSMED simulator*. Link in bio.",
                  40, "semibold", "body", accent=CYAN, gap=40, line_gap=1.3)
        self.text("Educational only. Not medical advice. Follow AHA 2025 guidelines and your institution's "
                  "protocols.", 26, "regular", "body", color=DIM, line_gap=1.3)


def render_carousel(c, out_dir: Path):
    d = out_dir / c["id"]
    d.mkdir(parents=True, exist_ok=True)
    n = len(c["slides"])
    paths = []
    for i, blocks in enumerate(c["slides"]):
        # pass 1 measures content height; pass 2 centres it vertically in the safe area
        m = Slide(i, n)
        for b in blocks:
            m.block(b)
        y0 = Slide.TOP
        if not any(b[0] == "cta" for b in blocks):
            spare = Slide.BOTTOM - (80 if any(b[0] == "swipe" for b in blocks) else 0) - m.y
            y0 += int(max(0, spare * 0.45))
        s = Slide(i, n, y0)
        s.chrome()
        for b in blocks:
            s.block(b)
        if s.y > H - 110:
            print(f"  WARNING {c['id']} slide {i + 1} overflows ({int(s.y)}px)")
        p = d / f"{i + 1:02d}.png"
        s.img.save(p, optimize=True)
        paths.append(p)
    return d
