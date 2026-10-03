"""Procedural, loop-perfect ambience + SFX.

Beds are synthesised in the frequency domain over exactly one loop length, so
they are circular: sample N-1 flows straight into sample 0 with no seam. Events
(gull calls, roars, splashes) are placed at the exact frame they happen on
screen and wrap around the loop point, so reverb tails carry across the seam.
"""
import wave as wavmod
import numpy as np
from .px import DUR

SR = 48000
N = SR * DUR
T = np.arange(N) / SR


def colored(alpha, lo=20, hi=20000, seed=0, n=N, tilt_db=0.0):
    """Circular noise with 1/f^alpha spectrum, band-limited to [lo, hi] with soft skirts."""
    r = np.random.default_rng(seed)
    spec = r.normal(size=n // 2 + 1) + 1j * r.normal(size=n // 2 + 1)
    f = np.fft.rfftfreq(n, 1 / SR)
    f[0] = 1
    shape = f ** (-alpha / 2)
    shape *= 1 / (1 + (lo / f) ** 4) / (1 + (f / hi) ** 4)
    x = np.fft.irfft(spec * shape, n)
    return x / (np.sqrt(np.mean(x ** 2)) + 1e-12)


def band(x, lo, hi, order=4, circular=False):
    """Zero-phase FFT band-pass. Events are zero padded (nothing wraps); loop beds use circular=True."""
    n = len(x)
    m = n if circular else 1 << int(np.ceil(np.log2(n * 2)))
    X = np.fft.rfft(x, m)
    f = np.fft.rfftfreq(m, 1 / SR)
    f[0] = 1e-3
    X *= 1 / (1 + (lo / f) ** order) / (1 + (f / hi) ** order)
    return np.fft.irfft(X, m)[:n]


def reverb(x, secs=1.2, wet=0.3, seed=1, lp=5000):
    r = np.random.default_rng(seed)
    n = int(secs * SR)
    ir = r.normal(size=n) * np.exp(-np.arange(n) / (secs * SR / 6.0))
    ir = band(ir, 120, lp)
    ir /= np.sqrt(np.sum(ir ** 2)) + 1e-9
    m = 1 << int(np.ceil(np.log2(len(x) + n)))
    y = np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(ir, m), m)[:len(x) + n]
    out = np.zeros(len(x) + n)
    out[:len(x)] += x * (1 - wet)
    return out + y * wet


def periodic(period, fn):
    """Envelope evaluated on loop phase (period must divide the loop)."""
    return fn((T % period) / period)


def place(buf, sig, t0, gain=1.0, pan=0.0):
    """Add mono `sig` at time t0 (seconds) with constant-power pan, wrapping at the loop point."""
    i0 = int(round(t0 * SR)) % N
    idx = (i0 + np.arange(len(sig))) % N
    th = (np.clip(pan, -1, 1) + 1) * np.pi / 4
    np.add.at(buf[0], idx, sig * gain * np.cos(th))
    np.add.at(buf[1], idx, sig * gain * np.sin(th))


def bed(buf, sigL, sigR, gain):
    buf[0] += sigL * gain
    buf[1] += sigR * gain


def env_adsr(n, a, d_, s, r, sus_level=0.7):
    t = np.arange(n) / SR
    e = np.interp(t, [0, a, a + d_, a + d_ + s, a + d_ + s + r], [0, 1, sus_level, sus_level, 0])
    return e


def tone(freqs, harm=(1.0,), phase0=0.0):
    """Oscillator following an instantaneous frequency curve (Hz per sample)."""
    ph = 2 * np.pi * np.cumsum(freqs) / SR + phase0
    return sum(a * np.sin((k + 1) * ph) for k, a in enumerate(harm))


# ---------------------------------------------------------------- one-shots
def gull(seed=0):
    r = np.random.default_rng(seed)
    out = []
    for syl in range(r.integers(2, 4)):
        n = int(SR * r.uniform(0.26, 0.36))
        s = np.linspace(0, 1, n)
        f = 1350 + 900 * np.sin(np.pi * np.minimum(s * 1.6, 1)) * (1 - s) + 120 * np.sin(2 * np.pi * 22 * s * 0.3)
        f *= r.uniform(0.92, 1.08)
        x = tone(f, (1, 0.6, 0.45, 0.25, 0.12))
        x += 0.15 * band(r.normal(size=n), 1500, 5000)
        e = np.interp(s, [0, 0.06, 0.3, 0.8, 1], [0, 1, 0.8, 0.35, 0])
        out.append(band(x * e, 700, 7000))
        out.append(np.zeros(int(SR * r.uniform(0.05, 0.12))))
    return reverb(np.concatenate(out), 1.4, 0.25, seed)


def pok(seed=0):
    n = int(SR * 0.14)
    s = np.arange(n) / SR
    f = 260 * np.exp(-s * 12) + 150
    x = tone(f) * np.exp(-s * 38)
    x += 0.4 * band(np.random.default_rng(seed).normal(size=n), 800, 4000) * np.exp(-s * 160)
    return reverb(x, 0.4, 0.15, seed)


def thump(seed=0, f0=46):
    n = int(SR * 0.7)
    s = np.arange(n) / SR
    x = tone(f0 * (1 + 0.6 * np.exp(-s * 18))) * np.exp(-s * 7)
    x += 0.5 * band(np.random.default_rng(seed).normal(size=n), 30, 220) * np.exp(-s * 20)
    return x


def splash(seed=0, size=1.0):
    r = np.random.default_rng(seed)
    n = int(SR * 0.6 * size)
    s = np.arange(n) / SR
    x = band(r.normal(size=n), 500, 7000) * np.exp(-s * 9 / size) * (1 - np.exp(-s * 300))
    for _ in range(int(8 * size)):
        k = r.integers(0, n // 2)
        m = int(SR * 0.03)
        ss = np.arange(m) / SR
        b = np.sin(2 * np.pi * np.cumsum(r.uniform(500, 1400) * (1 + 3 * ss)) / SR) * np.exp(-ss * 90)
        x[k:k + m] += 0.4 * b[:len(x[k:k + m])]
    return reverb(x, 0.6, 0.2, seed)


def plop(seed=0):
    n = int(SR * 0.18)
    s = np.arange(n) / SR
    x = tone(380 + 900 * s * 4) * np.exp(-s * 30) * (1 - np.exp(-s * 800))
    return reverb(x, 0.4, 0.2, seed)


def roar(seed=0, dur=2.4):
    r = np.random.default_rng(seed)
    n = int(SR * dur)
    s = np.linspace(0, 1, n)
    f0 = np.interp(s, [0, 0.15, 0.55, 1], [62, 96, 84, 52]) * (1 + 0.035 * np.sin(2 * np.pi * 7.3 * s * dur))
    jit = band(r.normal(size=n), 2, 30)
    f0 *= 1 + 0.03 * jit / (np.std(jit) + 1e-9)
    x = tone(f0, [1.0 / (k ** 0.7) for k in range(1, 36)])
    x = band(x, 60, 3200)
    # formants for a throaty growl
    form = sum(band(x, fc * 0.8, fc * 1.25) * g for fc, g in ((380, 1.0), (850, 0.8), (1700, 0.45)))
    breath = band(r.normal(size=n), 250, 2600) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 31 * s * dur)))
    sub = tone(f0 / 2) * 0.6
    e = np.interp(s, [0, 0.08, 0.2, 0.75, 1], [0, 0.85, 1, 0.75, 0])
    y = (form * 1.4 + breath * 0.35 + sub * 0.5) * e
    y = np.tanh(y / (np.max(np.abs(y)) + 1e-9) * 2.2)
    return reverb(band(y, 40, 2800), 2.6, 0.45, seed, lp=2500)


def screech(seed=0):
    r = np.random.default_rng(seed)
    n = int(SR * 0.75)
    s = np.linspace(0, 1, n)
    f = np.interp(s, [0, 0.2, 1], [1900, 2700, 1500])
    x = tone(f, (1, 0.5, 0.3, 0.2)) * (0.6 + 0.4 * np.sin(2 * np.pi * 55 * s * 0.75))
    x += 0.2 * band(r.normal(size=n), 2000, 6000)
    e = np.interp(s, [0, 0.05, 0.6, 1], [0, 1, 0.6, 0])
    return reverb(band(x * e, 900, 6500), 2.0, 0.45, seed)


def chirp_seq(seed=0):
    r = np.random.default_rng(seed)
    out = []
    base = r.uniform(2600, 4200)
    for _ in range(r.integers(3, 7)):
        n = int(SR * r.uniform(0.05, 0.09))
        s = np.linspace(0, 1, n)
        f = base * (1 + r.choice([-1, 1]) * 0.35 * s)
        out.append(tone(f, (1, 0.2)) * np.sin(np.pi * s) ** 2)
        out.append(np.zeros(int(SR * r.uniform(0.03, 0.08))))
    return reverb(np.concatenate(out), 1.2, 0.3, seed)


def flutter(seed=0):
    r = np.random.default_rng(seed)
    n = int(SR * 1.2)
    s = np.arange(n) / SR
    x = band(r.normal(size=n), 400, 3000) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 14 * s))) * np.exp(-s * 2.5)
    return x


def crackle_bed(seed=0, rate=7.0):
    """Campfire crackle over the whole loop (circular)."""
    r = np.random.default_rng(seed)
    out = np.zeros(N)
    k = r.poisson(rate * DUR)
    for t0 in r.uniform(0, DUR, k):
        m = int(SR * r.uniform(0.002, 0.012))
        burst = r.normal(size=m) * np.exp(-np.arange(m) / (m / 3)) * r.uniform(0.2, 1.0) ** 2
        idx = (int(t0 * SR) + np.arange(m)) % N
        out[idx] += burst
    out = band(out, 900, 9000, circular=True)
    out /= np.sqrt(np.mean(out ** 2)) + 1e-9
    return np.tanh(out / 4) * 4  # tame the occasional full-scale pop


def cricket_bed(seed=0, rate=0.62, freq=4300):
    r = np.random.default_rng(seed)
    out = np.zeros(N)
    t0 = 0.0
    while t0 < DUR:
        for p in range(3):
            m = int(SR * 0.022)
            s = np.arange(m) / SR
            b = np.sin(2 * np.pi * freq * s) * np.sin(np.pi * s / s[-1])
            idx = (int((t0 + p * 0.045) * SR) + np.arange(m)) % N
            out[idx] += b
        t0 += rate * r.uniform(0.9, 1.1)
    return out / (np.sqrt(np.mean(out ** 2)) + 1e-9)


def master(buf, peak_db=-1.0, rms_db=-19.0):
    buf = buf - buf.mean(axis=1, keepdims=True)
    rms = np.sqrt(np.mean(buf ** 2))
    buf *= 10 ** (rms_db / 20) / (rms + 1e-12)
    buf = np.tanh(buf * 1.2) / 1.2
    pk = np.max(np.abs(buf))
    lim = 10 ** (peak_db / 20)
    if pk > lim:
        buf *= lim / pk
    return buf


def write_wav(path, buf):
    x = (np.clip(buf.T, -1, 1) * 32767).astype("<i2")
    with wavmod.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(x.tobytes())
