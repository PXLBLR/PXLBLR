"""Declarative timeline renderer for 1080x1920 voiceless reels.

A reel spec is {"id", "duration", "elements": [...], "sfx": [(t, name, gain)]}.
Element types: text, pill, ecg, capno, countdown, box, strike, flash, shake, logo, endcard.
Every element has "t": (start, end). Elements may carry "sfx": [(offset, name, gain)].
"""
import math
import subprocess
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from . import ecg, sfx
from .brand import CYAN, ECG_GREEN, NAVY, NAVY_2, NAVY_3, RED, WHITE, YELLOW, font, logo_mark, pill, text_block

W, H, FPS = 1080, 1920, 30
SAFE_TOP, SAFE_BOTTOM = 250, 1480  # keep key content clear of IG UI chrome


def _mix(c, bg, a):
    return tuple(int(bg[i] + (c[i] - bg[i]) * a) for i in range(3))


def background():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    grid = _mix(NAVY_3, NAVY, 0.55)
    for x in range(0, W, 54):
        d.line([(x, 0), (x, H)], fill=grid, width=1)
    for y in range(0, H, 54):
        d.line([(0, y), (W, y)], fill=grid, width=1)
    # vignette + top/bottom glow
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-300, -500, W + 300, 900), fill=70)
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    tint = Image.new("RGB", (W, H), NAVY_2)
    img = Image.composite(tint, img, glow)
    vig = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vig)
    vd.rectangle((0, 0, W, H), fill=150)
    vd.ellipse((-200, 150, W + 200, H - 150), fill=0)
    vig = vig.filter(ImageFilter.GaussianBlur(180))
    img = Image.composite(Image.new("RGB", (W, H), (2, 3, 10)), img, vig)
    return img


def ease_out_back(x, s=1.9):
    x -= 1
    return x * x * ((s + 1) * x + s) + 1


def ease_out(x):
    return 1 - (1 - x) ** 3


class Reel:
    def __init__(self, spec):
        self.spec = spec
        self.dur = spec["duration"]
        self.bg = background()
        self.layers = {}
        self.sig = {}
        self.events = list(spec.get("sfx", []))
        for i, el in enumerate(spec["elements"]):
            el["_i"] = i
            s, e = el["t"]
            for off, name, gain in el.get("sfx", []):
                self.events.append((s + off, name, gain))
            if el["type"] in ("ecg", "capno"):
                self._prep_signal(el)
            if el["type"] == "countdown":
                n = el.get("n", 3)
                step = (e - s) / n
                for k in range(n):
                    self.events.append((s + k * step, "tick", 0.9))
            if el["type"] == "text" and el.get("anim") == "type":
                n = len(el["txt"].replace("*", ""))
                td = el.get("type_dur", min(1.2, n * 0.035))
                for k in range(0, n, 2):
                    self.events.append((s + td * k / n, "type", 0.6))

    # ---------- signals ----------
    def _prep_signal(self, el):
        s, e = el["t"]
        win = el.get("window", 4.0)
        total = (e - s) + win + 1
        if el["type"] == "ecg":
            y, rs = ecg.make(el["rhythm"], total, **el.get("kw", {}))
            self.sig[el["_i"]] = y
            if el.get("beeps", True):
                for r in rs:
                    tr = r - win
                    if 0 <= tr < (e - s) - 0.05:
                        self.events.append((s + tr, "beep", el.get("beep_gain", 0.55)))
        else:
            self.sig[el["_i"]] = ecg.capno(total, **el.get("kw", {}))

    # ---------- layers ----------
    def layer(self, el):
        k = el["_i"]
        if k in self.layers:
            return self.layers[k]
        t = el["type"]
        if t == "text":
            img = text_block(el["txt"], el.get("size", 72), el.get("max_w", 900), color=el.get("color", WHITE),
                             accent=el.get("accent", RED), weight=el.get("weight", "extrabold"),
                             family=el.get("family", "display"), align=el.get("align", "center"),
                             line_gap=el.get("line_gap", 1.1))
        elif t == "pill":
            img = pill(el["txt"], el.get("size", 34), fg=el.get("fg", WHITE), bg=el.get("bg", RED),
                       weight=el.get("weight", "extrabold"))
        elif t == "logo":
            img = logo_mark(el.get("h", 46))
        elif t == "box":
            x0, y0, x1, y1 = el["rect"]
            img = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            fill = el.get("fill", (*NAVY_2, 235))
            d.rounded_rectangle((0, 0, x1 - x0 - 1, y1 - y0 - 1), radius=el.get("radius", 28), fill=fill,
                                outline=el.get("outline"), width=el.get("width", 3))
        else:
            img = None
        self.layers[k] = img
        return img

    def _pos(self, el, img):
        x = el.get("x")
        if x is None:
            x = (W - img.width) // 2
        y = el.get("y", 800)
        if el.get("anchor") == "center":
            y -= img.height // 2
        return int(x), int(y)

    # ---------- per-frame ----------
    def alpha_for(self, el, t):
        s, e = el["t"]
        fi, fo = el.get("fade_in", 0.18), el.get("fade_out", 0.15)
        a = 1.0
        if el.get("anim", "up") != "none" and fi:
            a = min(a, (t - s) / fi)
        if fo and e < self.dur - 0.01:
            a = min(a, (e - t) / fo)
        return max(0.0, min(1.0, a))

    def paste(self, frame, img, xy, alpha=1.0):
        if alpha <= 0:
            return
        if alpha < 0.999:
            a = img.getchannel("A").point(lambda v: int(v * alpha))
            frame.paste(img, xy, a)
        else:
            frame.paste(img, xy, img)

    def draw_layer_el(self, frame, el, t):
        img = self.layer(el)
        s, e = el["t"]
        x, y = self._pos(el, img)
        a = self.alpha_for(el, t)
        anim = el.get("anim", "up")
        p = min(1.0, (t - s) / 0.32)
        if anim == "pop" and p < 1:
            sc = max(0.05, ease_out_back(p))
            nw, nh = max(1, int(img.width * sc)), max(1, int(img.height * sc))
            im2 = img.resize((nw, nh), Image.BILINEAR)
            self.paste(frame, im2, (x + (img.width - nw) // 2, y + (img.height - nh) // 2), a)
            return
        if anim == "up":
            y += int((1 - ease_out(p)) * 60)
        if anim == "left":
            x += int((1 - ease_out(p)) * 140)
        if anim == "type":
            td = el.get("type_dur", min(1.2, len(el["txt"]) * 0.035))
            frac = min(1.0, (t - s) / td)
            if frac < 1:
                img = img.crop((0, 0, max(1, int(img.width * frac)), img.height))
                a = 1.0
        if el.get("pulse"):
            k = 1 + 0.035 * math.sin((t - s) * 2 * math.pi * el["pulse"])
            nw, nh = int(img.width * k), int(img.height * k)
            im2 = img.resize((nw, nh), Image.BILINEAR)
            self.paste(frame, im2, (x - (nw - img.width) // 2, y - (nh - img.height) // 2), a)
            return
        self.paste(frame, img, (x, y), a)

    def draw_trace(self, d, el, t, values, color, gain, baseline):
        s, e = el["t"]
        win = el.get("window", 4.0)
        x0, y0, w, h = el["rect"]
        tt = (t - s) + win
        cur = (tt % win) / win * w
        gap = 26
        xs = np.arange(0, w, 3, dtype=np.float64)
        back = ((cur - xs) % w) / w * win
        st = tt - back
        idx = np.clip((st * ecg.FS).astype(int), 0, values.size - 1)
        ys = baseline - values[idx] * gain
        ys = np.clip(ys, y0 + 4, y0 + h - 4)
        hidden = ((xs - cur) % w) < gap
        segs, curseg = [], []
        for xi, yi, hd in zip(xs, ys, hidden):
            if hd:
                if len(curseg) > 1:
                    segs.append(curseg)
                curseg = []
            else:
                curseg.append((x0 + xi, yi))
        if len(curseg) > 1:
            segs.append(curseg)
        # split at wrap (cursor) so we don't draw a line across the screen
        final = []
        for sg in segs:
            part = [sg[0]]
            for a, b in zip(sg, sg[1:]):
                if b[0] < a[0]:
                    final.append(part)
                    part = [b]
                else:
                    part.append(b)
            final.append(part)
        a = self.alpha_for(el, t)
        for width, k in ((12, 0.16), (7, 0.38), (3, 1.0)):
            col = _mix(color, NAVY, k * a)
            for sg in final:
                if len(sg) > 1:
                    d.line(sg, fill=col, width=width, joint="curve")
        # leading dot
        ci = int(np.argmin(np.abs(xs - (cur - 3) % w)))
        cx, cy = x0 + xs[ci], ys[ci]
        d.ellipse((cx - 6, cy - 6, cx + 6, cy + 6), fill=_mix(WHITE, NAVY, a))

    def draw_monitor(self, frame, d, el, t):
        x0, y0, w, h = el["rect"]
        a = self.alpha_for(el, t)
        if el.get("panel", True):
            d.rounded_rectangle((x0 - 20, y0 - 58, x0 + w + 20, y0 + h + 16), radius=26,
                                fill=_mix((8, 12, 30), NAVY, a), outline=_mix(NAVY_3, NAVY, a), width=3)
        color = el.get("color", ECG_GREEN if el["type"] == "ecg" else YELLOW)
        lab_f = font(30, "bold", "mono")
        lab = el.get("label", "II" if el["type"] == "ecg" else "EtCO2")
        d.text((x0, y0 - 46), lab, font=lab_f, fill=_mix(color, NAVY, a))
        if el.get("readout"):
            rf = font(40, "extrabold", "mono")
            txt = el["readout"] if isinstance(el["readout"], str) else el["readout"](t - el["t"][0])
            tw = rf.getlength(txt)
            d.text((x0 + w - tw, y0 - 52), txt, font=rf, fill=_mix(color, NAVY, a))
        vals = self.sig[el["_i"]]
        if el["type"] == "ecg":
            self.draw_trace(d, el, t, vals, color, el.get("gain", h * 0.42), y0 + h * 0.62)
        else:
            self.draw_trace(d, el, t, vals, color, el.get("gain", h * 0.9 / 50), y0 + h - 8)

    def draw_countdown(self, d, el, t):
        s, e = el["t"]
        n = el.get("n", 3)
        cx, cy, r = el.get("cx", W // 2), el.get("cy", 1300), el.get("r", 78)
        frac = (t - s) / (e - s)
        num = n - int(frac * n)
        a = self.alpha_for(el, t)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=_mix(NAVY_3, NAVY, a), width=12)
        d.arc((cx - r, cy - r, cx + r, cy + r), start=-90, end=-90 + 360 * (1 - frac),
              fill=_mix(CYAN, NAVY, a), width=12)
        f = font(84, "black")
        txt = str(max(1, num))
        l, tp, rr, b = f.getbbox(txt)
        d.text((cx - (rr - l) / 2 - l, cy - (b - tp) / 2 - tp), txt, font=f, fill=_mix(WHITE, NAVY, a))

    def draw_strike(self, d, el, t):
        s, e = el["t"]
        x0, y0, x1 = el["x0"], el["y"], el["x1"]
        p = ease_out(min(1, (t - s) / 0.35))
        d.line([(x0, y0), (x0 + (x1 - x0) * p, y0 - 6 * p)], fill=RED, width=12)

    def frame(self, t):
        fr = self.bg.copy()
        d = ImageDraw.Draw(fr)
        post = []
        for el in self.spec["elements"]:
            s, e = el["t"]
            if not (s <= t < e):
                continue
            ty = el["type"]
            if ty in ("ecg", "capno"):
                self.draw_monitor(fr, d, el, t)
            elif ty in ("text", "pill", "logo", "box"):
                self.draw_layer_el(fr, el, t)
            elif ty == "countdown":
                self.draw_countdown(d, el, t)
            elif ty == "strike":
                self.draw_strike(d, el, t)
            elif ty in ("flash", "shake"):
                post.append(el)
        # progress bar (retention cue)
        d.rectangle((0, 0, int(W * t / self.dur), 9), fill=RED)
        for el in post:
            s, e = el["t"]
            k = 1 - (t - s) / (e - s)
            if el["type"] == "flash":
                fr = Image.blend(fr, Image.new("RGB", (W, H), el.get("color", WHITE)), 0.75 * k)
            else:
                amp = el.get("amp", 22) * k
                dx, dy = int(math.sin(t * 91) * amp), int(math.cos(t * 77) * amp)
                sh = Image.new("RGB", (W, H), NAVY)
                sh.paste(fr, (dx, dy))
                fr = sh
        return fr

    def render(self, out_path: Path, preview_times=()):
        out_path.parent.mkdir(parents=True, exist_ok=True)
        wav = out_path.with_suffix(".wav")
        sfx.write_wav(wav, sfx.mix(self.dur, self.events, self.spec.get("bed", 1.0)))
        ff = imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [ff, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
               "-r", str(FPS), "-i", "-", "-i", str(wav), "-c:v", "libx264", "-profile:v", "high",
               "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
               "-c:a", "aac", "-b:a", "192k",
               "-ar", "44100", "-shortest", "-movflags", "+faststart", str(out_path)]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        n = int(self.dur * FPS)
        cover = self.spec.get("cover_t", 1.2)
        for i in range(n):
            t = i / FPS
            fr = self.frame(t)
            p.stdin.write(fr.tobytes())
            if abs(t - cover) < 0.5 / FPS:
                fr.save(out_path.with_name(out_path.stem + "_cover.png"))
            for pt in preview_times:
                if abs(t - pt) < 0.5 / FPS:
                    fr.save(out_path.with_name(f"{out_path.stem}_t{pt:05.1f}.png"))
        p.stdin.close()
        p.wait()
        wav.unlink(missing_ok=True)
        if p.returncode:
            raise RuntimeError(f"ffmpeg failed for {out_path}")
        return out_path
