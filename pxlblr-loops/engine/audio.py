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


# ---------------------------------------------------------------- season pack one-shots
def place_sweep(buf, sig, t0, gain, pan0, pan1):
    """Like place(), but the pan moves linearly from pan0 to pan1 over the sound (passing train, flyover)."""
    i0 = int(round(t0 * SR)) % N
    idx = (i0 + np.arange(len(sig))) % N
    pan = np.linspace(pan0, pan1, len(sig))
    th = (np.clip(pan, -1, 1) + 1) * np.pi / 4
    np.add.at(buf[0], idx, sig * gain * np.cos(th))
    np.add.at(buf[1], idx, sig * gain * np.sin(th))


def hoot(seed=0):
    out = []
    for f0, d in ((410, 0.32), (0, 0.16), (385, 0.62)):
        n = int(SR * d)
        if not f0:
            out.append(np.zeros(n)); continue
        s = np.linspace(0, 1, n)
        x = tone(f0 * (1 - 0.06 * s) * (1 + 0.01 * np.sin(2 * np.pi * 5 * s * d)), (1, 0.18))
        out.append(x * np.sin(np.pi * s) ** 1.5)
    return reverb(band(np.concatenate(out), 200, 1500), 1.8, 0.35, seed)


def creak(seed=0, dur=0.9):
    r = np.random.default_rng(seed)
    n = int(SR * dur)
    s = np.linspace(0, 1, n)
    rate = 35 + 170 * np.sin(np.pi * s) ** 1.3
    ph = np.cumsum(rate) / SR
    x = np.zeros(n)
    hit = np.flatnonzero(np.diff(np.floor(ph)) > 0)
    x[hit] = r.uniform(0.5, 1.0, len(hit))
    y = band(x, 600, 950, 6) + 0.7 * band(x, 1500, 1900, 6) + 0.4 * band(x, 2900, 3300, 6)
    return reverb(y * np.sin(np.pi * s) ** 0.5, 0.8, 0.25, seed)


def bell(seed=0, f=174.6, dur=7.0):
    n = int(SR * dur)
    s = np.arange(n) / SR
    x = np.zeros(n)
    for ratio, amp, dec in ((0.5, 0.5, 2.2), (1.0, 1.0, 1.6), (1.19, 0.6, 1.2), (1.5, 0.45, 1.0), (2.0, 0.5, 0.8),
                            (2.5, 0.3, 0.6), (2.67, 0.25, 0.5), (3.0, 0.2, 0.4), (4.07, 0.12, 0.3)):
        x += amp * np.sin(2 * np.pi * f * ratio * s) * np.exp(-s / dec)
    x *= 1 - np.exp(-s * 400)
    return reverb(x, 3.0, 0.4, seed, lp=4000)


def squeak(seed=0):
    r = np.random.default_rng(seed)
    out = []
    for _ in range(r.integers(2, 5)):
        n = int(SR * 0.018)
        s = np.linspace(0, 1, n)
        out.append(tone(r.uniform(6500, 9000) * (1 - 0.25 * s)) * np.sin(np.pi * s))
        out.append(np.zeros(int(SR * r.uniform(0.04, 0.09))))
    return reverb(np.concatenate(out), 0.5, 0.2, seed)


def ghost_woo(seed=0, dur=3.2):
    r = np.random.default_rng(seed)
    n = int(SR * dur)
    s = np.linspace(0, 1, n)
    f0 = np.interp(s, [0, 0.35, 0.7, 1], [250, 340, 300, 230]) * (1 + 0.03 * np.sin(2 * np.pi * 5 * s * dur))
    x = tone(f0, (1, 0.3, 0.08)) + 0.15 * band(r.normal(size=n), 300, 1400)
    return reverb(x * np.sin(np.pi * s) ** 1.2, 3.2, 0.5, seed, lp=3000)


def caw(seed=0):
    r = np.random.default_rng(seed)
    out = []
    for _ in range(r.integers(2, 4)):
        n = int(SR * 0.26)
        s = np.linspace(0, 1, n)
        f = 560 * (1 - 0.18 * s) * r.uniform(0.95, 1.05)
        x = tone(f, [1 / k for k in range(1, 14)]) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 70 * s * 0.26)))
        x += 0.4 * band(r.normal(size=n), 800, 3500)
        out.append(band(x, 400, 4000) * np.interp(s, [0, 0.08, 0.6, 1], [0, 1, 0.7, 0]))
        out.append(np.zeros(int(SR * 0.12)))
    return reverb(np.concatenate(out), 1.5, 0.3, seed)


def scrape(seed=0, dur=0.35, lo=1500, hi=6000):
    r = np.random.default_rng(seed)
    n = int(SR * dur)
    s = np.linspace(0, 1, n)
    grain = (r.random(n) < 0.02) * r.uniform(0.5, 1, n)
    x = band(r.normal(size=n) * 0.4 + grain * 3, lo, hi)
    return x * np.sin(np.pi * s) ** 0.8


def loon(seed=0, dur=2.8):
    n = int(SR * dur)
    s = np.linspace(0, 1, n)
    f = np.interp(s, [0, 0.12, 0.35, 0.5, 0.62, 1], [620, 980, 930, 940, 1230, 1180])
    f *= 1 + 0.018 * np.sin(2 * np.pi * 6 * s * dur)
    x = tone(f, (1, 0.35, 0.12)) * np.interp(s, [0, 0.06, 0.45, 0.52, 0.6, 0.9, 1], [0, 1, 0.8, 0.4, 0.9, 0.7, 0])
    return reverb(x, 3.5, 0.55, seed, lp=4000)


def quack(seed=0):
    r = np.random.default_rng(seed)
    n = int(SR * 0.17)
    s = np.linspace(0, 1, n)
    x = tone(r.uniform(230, 270) * (1 - 0.15 * s), [1 / k for k in range(1, 20)])
    x = band(x, 700, 1600) * 2 + band(x, 1800, 3000) * 0.6
    return reverb(x * np.interp(s, [0, 0.05, 0.7, 1], [0, 1, 0.8, 0]), 1.0, 0.3, seed)


def swish(seed=0, dur=0.6):
    r = np.random.default_rng(seed)
    n = int(SR * dur)
    s = np.linspace(0, 1, n)
    x = band(r.normal(size=n), 250, 2500) * np.sin(np.pi * s) ** 2
    for _ in range(5):
        k = r.integers(n // 4, n - SR // 30)
        m = SR // 30
        ss = np.arange(m) / SR
        x[k:k + m] += 0.3 * np.sin(2 * np.pi * np.cumsum(r.uniform(500, 1100) * (1 + 4 * ss)) / SR) * np.exp(-ss * 80)
    return reverb(x, 1.2, 0.3, seed)


def rustle(seed=0, dur=0.7):
    r = np.random.default_rng(seed)
    n = int(SR * dur)
    s = np.linspace(0, 1, n)
    grains = (r.random(n) < 0.03) * r.uniform(0.2, 1, n)
    x = band(grains * 2 + r.normal(size=n) * 0.3, 1800, 9000)
    return x * np.interp(s, [0, 0.1, 0.5, 1], [0, 1, 0.7, 0])


def snap(seed=0):
    r = np.random.default_rng(seed)
    n = int(SR * 0.08)
    s = np.arange(n) / SR
    return reverb(band(r.normal(size=n), 900, 6000) * np.exp(-s * 70), 0.8, 0.3, seed)


def zap(seed=0):
    r = np.random.default_rng(seed)
    n = int(SR * 0.14)
    s = np.arange(n) / SR
    x = band(r.normal(size=n), 2000, 8000) * np.exp(-s * 40)
    x += tone(np.full(n, 120.0), [1 / k for k in range(1, 16)]) * 0.4 * np.exp(-s * 20)
    return x


def slurp(seed=0, dur=0.6):
    r = np.random.default_rng(seed)
    n = int(SR * dur)
    out = np.zeros(n + SR // 10)
    seg = SR // 25
    for i, c in enumerate(np.linspace(700, 2600, int(n / (seg / 2)))):
        k = int(i * seg / 2)
        w = np.hanning(seg)
        out[k:k + seg] += band(r.normal(size=seg), c * 0.8, c * 1.25) * w
    s = np.arange(len(out)) / SR
    out *= 0.6 + 0.4 * np.sin(2 * np.pi * 23 * s)
    return out * np.interp(s, [0, 0.1, dur * 0.8, dur + 0.1], [0, 1, 0.8, 0])


def train(seed=0, dur=7.0):
    r = np.random.default_rng(seed)
    n = int(SR * dur)
    s = np.linspace(0, 1, n)
    env = np.interp(s, [0, 0.25, 0.4, 0.7, 1], [0, 0.6, 1, 0.8, 0])
    x = band(r.normal(size=n), 30, 260) * 1.4
    x += band(r.normal(size=n), 300, 2500) * 0.25
    x += tone(np.interp(s, [0, 1], [780, 690]), (1, 0.3)) * 0.05
    for t0 in np.arange(0.3, dur - 0.3, 0.55):
        for dt in (0.0, 0.11):
            k = int((t0 + dt) * SR)
            m = int(SR * 0.12)
            ss = np.arange(m) / SR
            clack = np.sin(2 * np.pi * 95 * ss) * np.exp(-ss * 45) + 0.5 * band(r.normal(size=m), 800, 4000) * np.exp(-ss * 120)
            x[k:k + m] += clack[:len(x[k:k + m])] * 1.2
    return reverb(x * env, 1.6, 0.3, seed)


def rain_bed(seed=0, rate=70.0):
    """Circular rain: broadband hiss + dense droplet ticks."""
    r = np.random.default_rng(seed)
    hiss = colored(0.15, 500, 14000, seed=seed)
    drops = np.zeros(N)
    k = r.poisson(rate * DUR)
    m = int(SR * 0.004)
    shape = np.exp(-np.arange(m) / (m / 4))
    for t0, a in zip(r.uniform(0, DUR, k), r.uniform(0.1, 1, k) ** 2):
        idx = (int(t0 * SR) + np.arange(m)) % N
        drops[idx] += shape * a * r.choice([-1, 1])
    drops = band(drops, 1500, 9000, circular=True)
    drops /= np.sqrt(np.mean(drops ** 2)) + 1e-9
    return hiss * 0.7 + np.tanh(drops / 3) * 3 * 0.45


def buzz_bed(f=120.0):
    return sum(np.sin(2 * np.pi * f * k * T + k * 1.3) / k for k in range(1, 14))


def slow_am(seed, lo=0.3, hi=4.0, depth=0.4):
    a = colored(0.0, lo, hi, seed=seed)
    return np.clip(1 - depth + depth * a, 0.1, 2)


def pk(x, peak=1.0):
    """Peak-normalise a one-shot so scene gains read as real levels."""
    return x * peak / (np.max(np.abs(x)) + 1e-12)


# ---------------------------------------------------------------- winter / cosy pack one-shots
def jingle(seed=0, dur=6.0, rate=9.0):
    """Sleigh bells: clusters of tiny metallic bells shaken at `rate` per second."""
    r = np.random.default_rng(seed)
    n = int(SR * dur)
    out = np.zeros(n + SR)
    m = int(SR * 0.35)
    s = np.arange(m) / SR
    for t0 in np.arange(0, dur, 1 / rate):
        for _ in range(r.integers(3, 7)):
            f = r.uniform(2600, 5200)
            b = sum(np.sin(2 * np.pi * f * k * s + r.uniform(0, 6)) / k ** 1.5 for k in (1, 2.76, 5.4))
            k0 = int((t0 + r.uniform(0, 0.03)) * SR)
            out[k0:k0 + m] += b * np.exp(-s * r.uniform(14, 24)) * r.uniform(0.3, 1)
    env = np.interp(np.arange(len(out)) / SR, [0, dur * 0.25, dur * 0.75, dur + 1], [0, 1, 1, 0])
    return reverb(band(out * env, 1800, 12000), 1.5, 0.35, seed)


def crunch(seed=0):
    r = np.random.default_rng(seed)
    n = int(SR * 0.16)
    s = np.linspace(0, 1, n)
    grains = (r.random(n) < 0.08) * r.uniform(0.3, 1, n)
    x = band(grains + r.normal(size=n) * 0.2, 700, 6000)
    return x * np.interp(s, [0, 0.1, 0.6, 1], [0, 1, 0.6, 0])


def ice_ping(seed=0):
    """The eerie 'pew' of a frozen lake: a fast descending chirp with a long tail."""
    r = np.random.default_rng(seed)
    n = int(SR * 0.9)
    s = np.arange(n) / SR
    f = 300 + r.uniform(1800, 2600) * np.exp(-s * r.uniform(5, 8))
    x = tone(f, (1, 0.25)) * np.exp(-s * 3.5) * (1 - np.exp(-s * 600))
    return reverb(x, 3.0, 0.5, seed, lp=6000)


def squawk(seed=0):
    r = np.random.default_rng(seed)
    n = int(SR * 0.28)
    s = np.linspace(0, 1, n)
    f0 = r.uniform(380, 460) * (1 + 0.25 * np.sin(np.pi * s))
    x = tone(f0, [1 / k ** 0.8 for k in range(1, 18)]) * (0.7 + 0.3 * np.sin(2 * np.pi * 40 * s * 0.28))
    x = band(x, 500, 2400) * 1.5 + band(x, 2600, 4000) * 0.3
    return reverb(x * np.interp(s, [0, 0.06, 0.7, 1], [0, 1, 0.8, 0]), 1.2, 0.3, seed)


def shimmer(seed=0, dur=1.6):
    r = np.random.default_rng(seed)
    n = int(SR * dur)
    out = np.zeros(n)
    for i in range(14):
        m = int(SR * 0.6)
        s = np.arange(m) / SR
        f = 5200 - i * 230 + r.uniform(-60, 60)
        k0 = int(i * (dur - 0.6) / 14 * SR)
        out[k0:k0 + m] += np.sin(2 * np.pi * f * s) * np.exp(-s * 7) * (1 - np.exp(-s * 900))
    return reverb(out, 2.4, 0.5, seed)


def thunder(seed=0, dur=7.0):
    r = np.random.default_rng(seed)
    n = int(SR * dur)
    s = np.linspace(0, 1, n)
    x = band(r.normal(size=n), 25, 220) * 1.6 + band(r.normal(size=n), 200, 1200) * 0.35
    am = np.clip(band(r.normal(size=n), 0.5, 7), -3, 3)
    am = 0.6 + 0.4 * am / (np.max(np.abs(am)) + 1e-9)
    env = np.interp(s, [0, 0.03, 0.12, 0.35, 1], [0, 0.7, 1, 0.55, 0])
    return reverb(x * am * env, 3.0, 0.4, seed, lp=1500)


def tick(seed=0, hi=True):
    n = int(SR * 0.06)
    s = np.arange(n) / SR
    f = 3200 if hi else 2500
    x = (np.sin(2 * np.pi * f * s) + 0.5 * np.sin(2 * np.pi * f * 1.6 * s)) * np.exp(-s * 140)
    x += band(np.random.default_rng(seed).normal(size=n), 2000, 7000) * np.exp(-s * 300) * 0.5
    return reverb(x, 0.6, 0.25, seed)


def page_turn(seed=0):
    r = np.random.default_rng(seed)
    n = int(SR * 0.45)
    s = np.linspace(0, 1, n)
    x = band(r.normal(size=n), 1200, 9000) * np.interp(s, [0, 0.2, 0.5, 0.8, 1], [0, 0.6, 1, 0.3, 0])
    x += band((r.random(n) < 0.01) * 1.0, 1500, 7000) * 2
    return x


def meow(seed=0):
    n = int(SR * 0.9)
    s = np.linspace(0, 1, n)
    f0 = np.interp(s, [0, 0.3, 1], [420, 640, 380])
    x = tone(f0, [1 / k for k in range(1, 16)])
    form = band(x, 600, 1100) * np.interp(s, [0, 0.5, 1], [0.4, 1, 0.5]) + band(x, 1500, 2800) * np.interp(s, [0, 0.5, 1], [1, 0.6, 0.3])
    return reverb(form * np.interp(s, [0, 0.1, 0.7, 1], [0, 1, 0.8, 0]), 0.8, 0.25, seed)


def purr_bed(seed=0, rate=26.0):
    """Circular purr: low noise pulsed at ~26 Hz, breathing in and out every 3 s."""
    x = colored(1.0, 40, 400, seed=seed)
    pulse = 0.5 + 0.5 * np.sin(2 * np.pi * rate * T) ** 8
    breath = 0.6 + 0.4 * np.sin(2 * np.pi * T / 3.0)
    return x * pulse * breath


def snore(seed=0, dur=1.6):
    r = np.random.default_rng(seed)
    n = int(SR * dur)
    s = np.linspace(0, 1, n)
    x = band(r.normal(size=n), 80, 700) * (0.6 + 0.4 * np.sin(2 * np.pi * 32 * s * dur))
    return x * np.sin(np.pi * s) ** 2


def thud(seed=0):
    n = int(SR * 0.2)
    s = np.arange(n) / SR
    return tone(np.full(n, 110.0)) * np.exp(-s * 30) + band(np.random.default_rng(seed).normal(size=n), 200, 2500) * np.exp(-s * 40) * 0.5


def fire_bed(seed=0, pan=0.4):
    """Warm indoor fireplace, circular over the loop. Returns (left, right).

    Layers: low breathing roar, soft flame flutter, fine crackles, bigger wood pops
    (some doubled), occasional sap hiss and an ember settling now and then.
    """
    r = np.random.default_rng(seed)
    flick = colored(0.0, 0.15, 1.6, seed=seed + 1)
    flick = 0.75 + 0.25 * np.tanh(flick)
    roar = colored(0.9, 90, 450, seed=seed + 2) * flick
    flutter = colored(0.7, 180, 1500, seed=seed + 3) * flick ** 2

    def pops(sd, rate, lo, hi, dmin, dmax, doubles=0.0):
        rr = np.random.default_rng(sd)
        out = np.zeros(N)
        k = rr.poisson(rate * DUR)
        for t0 in rr.uniform(0, DUR, k):
            for rep in range(2 if rr.random() < doubles else 1):
                m = int(SR * rr.uniform(dmin, dmax))
                burst = rr.normal(size=m) * np.exp(-np.arange(m) / (m / 4)) * rr.uniform(0.25, 1.0) ** 1.5
                idx = (int((t0 + rep * rr.uniform(0.03, 0.09)) * SR) + np.arange(m)) % N
                out[idx] += burst
        out = band(out, lo, hi, circular=True)
        out /= np.sqrt(np.mean(out ** 2)) + 1e-9
        return np.tanh(out / 4) * 4

    side = []
    for ch in (0, 1):
        crackle = pops(seed + 10 + ch, 14.0, 1200, 9000, 0.0015, 0.006)
        wood = pops(seed + 20 + ch, 0.9, 350, 3800, 0.012, 0.05, doubles=0.3)
        side.append(crackle * 0.55 + wood * 0.45)
    hiss = np.zeros(N)
    for t0 in r.uniform(0, DUR, 3):
        m = int(SR * r.uniform(0.5, 1.3))
        s = np.linspace(0, 1, m)
        seg = band(r.normal(size=m), 3000, 8000) * np.sin(np.pi * s) ** 2
        idx = (int(t0 * SR) + np.arange(m)) % N
        hiss[idx] += seg
    hiss /= np.sqrt(np.mean(hiss ** 2)) + 1e-9
    settle = np.zeros(N)
    for t0 in r.uniform(0, DUR, 2):
        x = thud(int(t0 * 10)) * 0.6 + band(r.normal(size=int(SR * 0.2)), 300, 2500) * np.exp(-np.arange(int(SR * 0.2)) / SR * 25) * 0.4
        idx = (int(t0 * SR) + np.arange(len(x))) % N
        settle[idx] += x
    settle /= np.max(np.abs(settle)) + 1e-9
    body = roar * 0.10 + flutter * 0.07 + hiss * 0.03 + settle * 0.12
    gl, gr = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    left = body * gl + side[0] * 0.42 * gl
    right = body * gr + side[1] * 0.42 * gr
    return left, right
