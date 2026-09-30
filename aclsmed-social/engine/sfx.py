"""Procedural SFX for faceless reels: monitor beeps, alarms, defib charge/shock, whooshes, pops,
ticks, dings, buzzers, risers and a quiet ambient bed. All synthesized — no licensing issues."""
import wave

import numpy as np

SR = 44100
_rng = np.random.default_rng(42)


def _t(d):
    return np.arange(int(d * SR)) / SR


def _env(n, a=0.005, r=0.05):
    e = np.ones(n)
    na, nr = max(1, int(a * SR)), max(1, int(r * SR))
    e[:na] = np.linspace(0, 1, na)
    e[-nr:] *= np.linspace(1, 0, nr)
    return e


def _lowpass(x, cutoff):
    """One-pole lowpass; cutoff may be scalar or per-sample array (Hz)."""
    c = np.broadcast_to(np.asarray(cutoff, dtype=float), x.shape)
    a = 1 - np.exp(-2 * np.pi * c / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(x.size):
        acc += a[i] * (x[i] - acc)
        y[i] = acc
    return y


def monitor_beep(freq=880, d=0.09):
    t = _t(d)
    x = np.sin(2 * np.pi * freq * t) + 0.2 * np.sin(2 * np.pi * 2 * freq * t)
    return 0.35 * x * _env(t.size, 0.003, 0.03)


def alarm(d=1.6):
    """High-priority style: 3 + 2 pulse burst."""
    out = np.zeros(int(d * SR))
    notes = [(0.0, 988), (0.16, 784), (0.32, 988), (0.62, 988), (0.78, 784)]
    for st, f in notes:
        t = _t(0.12)
        x = np.sign(np.sin(2 * np.pi * f * t)) * 0.25 + np.sin(2 * np.pi * f * t) * 0.5
        x = _lowpass(x, 5000) * _env(t.size, 0.004, 0.02)
        i = int(st * SR)
        out[i:i + x.size] += 0.55 * x
    return out


def charge(d=1.8):
    t = _t(d)
    f = 380 + (2600 - 380) * (t / d) ** 1.6
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = 0.28 * np.sin(ph) + 0.08 * np.sign(np.sin(ph))
    x *= _env(t.size, 0.05, 0.03) * (0.4 + 0.6 * t / d)
    # "ready" double-chirp at the end
    tail = np.concatenate([monitor_beep(1760, 0.07), np.zeros(int(0.05 * SR)), monitor_beep(1760, 0.07)])
    return np.concatenate([x, tail * 0.8])


def shock(d=0.7):
    t = _t(d)
    thump = np.sin(2 * np.pi * (70 - 30 * t / d) * t) * np.exp(-t * 9)
    crack = _rng.normal(0, 1, t.size) * np.exp(-t * 38)
    crack = crack - _lowpass(crack, 900)
    return 0.95 * thump + 0.45 * crack


def whoosh(d=0.42, up=True):
    t = _t(d)
    n = _rng.normal(0, 1, t.size)
    sweep = (400 + 5200 * (t / d)) if up else (5600 - 5200 * (t / d))
    x = _lowpass(n, sweep) - _lowpass(n, 180)
    e = np.sin(np.pi * t / d) ** 2
    return 0.55 * x * e


def pop(d=0.09):
    t = _t(d)
    f = 820 - 520 * t / d
    x = np.sin(2 * np.pi * np.cumsum(f) / SR)
    return 0.5 * x * np.exp(-t * 38)


def tick(d=0.035):
    t = _t(d)
    x = np.sin(2 * np.pi * 2100 * t) * np.exp(-t * 180) + 0.3 * _rng.normal(0, 1, t.size) * np.exp(-t * 400)
    return 0.45 * x


def ding(d=0.9):
    t = _t(d)
    x = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * k)
            for f, a, k in [(1318.5, 0.5, 4.5), (1975.5, 0.3, 6), (2637, 0.12, 9)])
    return 0.55 * x * _env(t.size, 0.002, 0.05)


def buzzer(d=0.45):
    t = _t(d)
    x = np.sign(np.sin(2 * np.pi * 140 * t)) + 0.6 * np.sign(np.sin(2 * np.pi * 147 * t))
    return 0.16 * _lowpass(x, 2200) * _env(t.size, 0.005, 0.06)


def riser(d=1.4):
    t = _t(d)
    n = _rng.normal(0, 1, t.size)
    x = _lowpass(n, 300 + 6000 * (t / d) ** 2) * (t / d) ** 2
    tone = np.sin(2 * np.pi * np.cumsum(200 + 700 * (t / d) ** 2) / SR) * (t / d) ** 2
    return 0.35 * x + 0.12 * tone


def heartbeat(d=0.6):
    t = _t(d)
    lub = np.sin(2 * np.pi * 55 * t) * np.exp(-t * 22)
    t2 = np.clip(t - 0.2, 0, None)
    dub = np.sin(2 * np.pi * 65 * t2) * np.exp(-t2 * 26) * (t > 0.2)
    return 0.9 * (lub + 0.7 * dub)


def type_click(d=0.02):
    t = _t(d)
    return 0.18 * _rng.normal(0, 1, t.size) * np.exp(-t * 350)


def swipe(d=0.25):
    return whoosh(d, up=False) * 0.7


def bed(d, root=55.0):
    """Very quiet dark pad so the reel never drops to digital silence."""
    t = _t(d)
    x = np.zeros_like(t)
    for mult, a in [(1, 0.5), (1.5, 0.3), (2, 0.25), (3, 0.08)]:
        x += a * np.sin(2 * np.pi * root * mult * t + mult)
    lfo = 0.65 + 0.35 * np.sin(2 * np.pi * 0.11 * t)
    fade = np.minimum(1, np.minimum(t / 1.5, (d - t) / 1.5))
    return 0.055 * x * lfo * np.clip(fade, 0, 1)


SOUNDS = {
    "beep": monitor_beep, "beep_hi": lambda: monitor_beep(1040), "alarm": alarm, "charge": charge,
    "shock": shock, "whoosh": whoosh, "whoosh_down": lambda: whoosh(up=False), "pop": pop,
    "tick": tick, "ding": ding, "buzzer": buzzer, "riser": riser, "heartbeat": heartbeat,
    "type": type_click, "swipe": swipe,
}
_cache = {}


def get(name):
    if name not in _cache:
        _cache[name] = np.asarray(SOUNDS[name](), dtype=np.float64)
    return _cache[name]


def mix(duration, events, bed_level=1.0):
    """events: [(time_s, name, gain)] -> float stereo-ready mono mix."""
    n = int(duration * SR) + SR
    out = np.zeros(n)
    if bed_level:
        b = bed(duration) * bed_level
        out[:b.size] += b
    for t0, name, gain in events:
        s = get(name) * gain
        i = int(t0 * SR)
        if i >= n:
            continue
        seg = s[: n - i]
        out[i:i + seg.size] += seg
    out = out[: int(duration * SR)]
    peak = np.abs(out).max() or 1
    out = np.tanh(out / peak * 1.3) * 0.89  # gentle limiter, ~ -1 dBFS
    return out


def write_wav(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    st = np.repeat(pcm[:, None], 2, axis=1)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(st.tobytes())
