"""Synthetic Lead II rhythm generator (teaching-grade morphology, not diagnostic).

Every generator returns (y, r_times): y sampled at FS Hz in mV-ish units (baseline 0,
R ≈ 1.0), and the times of ventricular complexes (for monitor beeps).
"""
import numpy as np

FS = 250


def _t(dur):
    return np.arange(int(dur * FS)) / FS


def _g(t, c, s, a):
    return a * np.exp(-0.5 * ((t - c) / s) ** 2)


def _p(t, c, amp=0.17):
    return _g(t, c, 0.022, amp)


def _qrs(t, c, width=0.08, amp=1.0, wide=False):
    if wide:
        return (_g(t, c, width / 3.2, amp) + _g(t, c + width * 0.75, width / 2.8, -0.35 * amp))
    return (_g(t, c - width * 0.32, width / 9, -0.10 * amp) + _g(t, c, width / 6.5, amp)
            + _g(t, c + width * 0.36, width / 8, -0.24 * amp))


def _twave(t, c, amp=0.28, s=0.055):
    return _g(t, c, s, amp)


def _wander(t, seed=1, amp=0.02):
    rng = np.random.default_rng(seed)
    return amp * np.sin(2 * np.pi * 0.23 * t + rng.uniform(0, 6)) + rng.normal(0, 0.006, t.size)


def sinus(dur, hr=78, pr=0.16, qrs_w=0.08, t_amp=0.28, p_amp=0.14, seed=1, start=0.25):
    t = _t(dur)
    y = _wander(t, seed)
    rr = 60 / hr
    qt = min(0.42, 0.40 * np.sqrt(rr))
    rs, b = [], start
    while b < dur + 1:
        q = b + pr
        y += _p(t, b + 0.05, p_amp) + _qrs(t, q, qrs_w) + _twave(t, q + qt - 0.12, t_amp)
        rs.append(q)
        b += rr
    return y, [r for r in rs if r < dur]


def first_degree(dur, hr=68, pr=0.32):
    return sinus(dur, hr=hr, pr=pr)


def svt(dur, hr=186):
    t = _t(dur)
    y = _wander(t, 3, 0.012)
    rr = 60 / hr
    rs, q = [], 0.2
    while q < dur + 1:
        y += _qrs(t, q, 0.07, 0.95) + _twave(t, q + 0.19, 0.22, 0.04)
        rs.append(q)
        q += rr
    return y, [r for r in rs if r < dur]


def afib(dur, mean_hr=128, seed=7):
    t = _t(dur)
    rng = np.random.default_rng(seed)
    y = _wander(t, seed, 0.01)
    for f in rng.uniform(5.0, 8.0, 5):  # fibrillatory baseline
        y += 0.028 * np.sin(2 * np.pi * f * t + rng.uniform(0, 6))
    rs, q = [], 0.2
    while q < dur + 1:
        y += _qrs(t, q, 0.08, 1.0) + _twave(t, q + 0.24, 0.20, 0.05)
        rs.append(q)
        q += rng.uniform(0.34, 0.80) * (128 / mean_hr)
    return y, [r for r in rs if r < dur]


def aflutter(dur, conduction=2, atrial=300):
    t = _t(dur)
    fa = atrial / 60
    phase = (t * fa) % 1.0
    y = -0.34 * (phase - 0.5) + 0.05 * np.sin(2 * np.pi * fa * t)  # sawtooth
    rs, q = [], 0.25
    while q < dur + 1:
        y += _qrs(t, q, 0.08, 1.0)
        rs.append(q)
        q += conduction / fa
    return y + _wander(t, 5, 0.006), [r for r in rs if r < dur]


def vt(dur, hr=176, amp=1.1):
    t = _t(dur)
    y = _wander(t, 9, 0.01)
    rr = 60 / hr
    rs, q = [], 0.15
    while q < dur + 1:
        y += _g(t, q, 0.045, amp) + _g(t, q + 0.13, 0.06, -0.55 * amp)
        rs.append(q)
        q += rr
    return y, [r for r in rs if r < dur]


def torsades(dur, hr=250, spindle=2.6):
    t = _t(dur)
    f = hr / 60
    base = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t + 0.8)
    env = np.cos(np.pi * t / spindle)  # passes through zero -> "twisting" polarity
    env = np.sign(env) * (0.18 + 0.82 * np.abs(env))
    y = 0.9 * env * base + _wander(t, 11, 0.01)
    rs = list(np.arange(0.1, dur, 1 / f))
    return y, rs


def vfib(dur, coarse=True, seed=4):
    t = _t(dur)
    rng = np.random.default_rng(seed)
    y = np.zeros_like(t)
    amp = 0.55 if coarse else 0.18
    for _ in range(6):
        fr = rng.uniform(3.5, 7.5)
        y += np.sin(2 * np.pi * fr * t + rng.uniform(0, 6)) * (0.5 + 0.5 * np.sin(2 * np.pi * rng.uniform(0.2, 0.6) * t + rng.uniform(0, 6)))
    y = amp * y / np.abs(y).max() * 1.2
    return y + _wander(t, seed, 0.01), []


def asystole(dur):
    t = _t(dur)
    return 0.6 * _wander(t, 2, 0.02), []


def mobitz1(dur, atrial=80, cycle=4, pr0=0.16, dpr=0.09):
    t = _t(dur)
    y = _wander(t, 12)
    pp = 60 / atrial
    rs, b, k = [], 0.2, 0
    while b < dur + 1:
        y += _p(t, b + 0.05)
        idx = k % cycle
        if idx < cycle - 1:
            q = b + pr0 + dpr * idx
            y += _qrs(t, q) + _twave(t, q + 0.26)
            rs.append(q)
        b += pp
        k += 1
    return y, [r for r in rs if r < dur]


def mobitz2(dur, atrial=80, cycle=3, pr=0.18, wide=True):
    t = _t(dur)
    y = _wander(t, 13)
    pp = 60 / atrial
    rs, b, k = [], 0.2, 0
    while b < dur + 1:
        y += _p(t, b + 0.05)
        if k % cycle != cycle - 1:
            q = b + pr
            y += _qrs(t, q, 0.13 if wide else 0.08, 1.0, wide=wide) + _twave(t, q + 0.30, 0.25)
            rs.append(q)
        b += pp
        k += 1
    return y, [r for r in rs if r < dur]


def chb(dur, atrial=84, vent=36):
    t = _t(dur)
    y = _wander(t, 14)
    b = 0.12
    while b < dur + 1:
        y += _p(t, b)
        b += 60 / atrial
    rs, q = [], 0.55
    while q < dur + 1:
        y += _qrs(t, q, 0.16, 1.05, wide=True) + _twave(t, q + 0.38, -0.3, 0.08)
        rs.append(q)
        q += 60 / vent
    return y, [r for r in rs if r < dur]


def paced(dur, rate=70, capture=True, underlying_hr=34):
    """Transcutaneous pacing. capture=False shows spikes marching with no QRS after them."""
    t = _t(dur)
    y = _wander(t, 15, 0.012)
    rs, s = [], 0.3
    spikes = []
    while s < dur + 1:
        spikes.append(s)
        s += 60 / rate
    for s in spikes:
        y += _g(t, s, 0.0035, 1.6)  # pacer spike
        if capture:
            q = s + 0.07
            y += _g(t, q, 0.05, 1.05) + _g(t, q + 0.30, 0.07, -0.38)  # wide QRS + discordant T
            rs.append(q)
    if not capture:  # slow underlying escape rhythm
        q = 0.9
        while q < dur + 1:
            y += _qrs(t, q, 0.14, 0.9, wide=True) + _twave(t, q + 0.36, -0.25, 0.08)
            rs.append(q)
            q += 60 / underlying_hr
    return y, [r for r in rs if r < dur]


def hyperk(dur, stage=1, hr=72):
    """1 peaked T · 2 flat P + long PR + wider QRS · 3 sine wave."""
    t = _t(dur)
    if stage == 3:
        f = 1.9
        y = 0.75 * np.sin(2 * np.pi * f * t) + 0.18 * np.sin(4 * np.pi * f * t + 1.2)
        return y + _wander(t, 16, 0.01), list(np.arange(0.13, dur, 1 / f))
    y = _wander(t, 16)
    rr = 60 / hr
    rs, b = [], 0.2
    while b < dur + 1:
        if stage == 1:
            q = b + 0.16
            y += _p(t, b + 0.05) + _qrs(t, q, 0.09) + _g(t, q + 0.24, 0.032, 0.95)
        else:
            q = b + 0.26
            y += _p(t, b + 0.05, 0.05) + _qrs(t, q, 0.17, 0.9, wide=True) + _g(t, q + 0.30, 0.04, 0.85)
        rs.append(q)
        b += rr
    return y, [r for r in rs if r < dur]


def cpr_artifact(dur, rate=110, amp=0.55, seed=21):
    """Compression artifact over VF-ish baseline, as seen during CPR."""
    t = _t(dur)
    f = rate / 60
    y = amp * (np.maximum(0, np.sin(2 * np.pi * f * t)) ** 1.5) - amp * 0.3
    return y + 0.25 * vfib(dur, coarse=False, seed=seed)[0], []


def sequence(dur, parts=()):
    """Concatenate rhythms: parts=[(name, seconds, kw), ...]; last part fills remaining time."""
    ys, rs, t0 = [], [], 0.0
    for i, (name, d, kw) in enumerate(parts):
        if i == len(parts) - 1:
            d = max(d, dur - t0)
        y, r = RHYTHMS[name](d, **kw)
        ys.append(np.asarray(y)[: int(d * FS)])
        rs += [t0 + x for x in r]
        t0 += d
    return np.concatenate(ys)[: int(dur * FS) + 1], rs


def beats(dur, hr=72, pr=0.16, qrs_w=0.08, wide=False, r_amp=1.0, p_amp=0.17, t_amp=0.28, t_w=0.055, qt=None,
          st=0.0, u_amp=0.0, delta=False, j_amp=0.0, alternans=0.0, p_after=False, seed=31, start=0.25):
    """General-purpose conducted rhythm with morphology knobs (ST shift, U waves, delta wave, Osborn J wave,
    electrical alternans, retrograde P)."""
    t = _t(dur)
    y = _wander(t, seed)
    rr = 60 / hr
    qt = qt or min(0.42, 0.40 * np.sqrt(rr))
    rs, b, k = [], start, 0
    while b < dur + 1:
        q = b + (0.11 if delta else pr)
        amp = r_amp * (1 - alternans if k % 2 else 1)
        if p_amp and not p_after:
            y += _p(t, b + 0.05, p_amp)
        if delta:
            y += _g(t, q - 0.045, 0.024, 0.32 * amp)
        y += _qrs(t, q, qrs_w, amp, wide=wide)
        if p_after:
            y += _p(t, q + 0.12, -0.12)
        if j_amp:
            y += _g(t, q + qrs_w * 0.55 + 0.02, 0.022, j_amp)
        if st:  # plateau from the J point into the T wave
            j0, j1 = q + qrs_w * 0.55, q + qt - 0.14
            y += st / (1 + np.exp(np.clip(-(t - j0) / 0.006, -60, 60))) / (1 + np.exp(np.clip((t - j1) / 0.03, -60, 60)))
        y += _twave(t, q + qt - 0.12, t_amp * (amp / r_amp if alternans else 1), t_w)
        if u_amp:
            y += _g(t, q + qt + 0.06, 0.045, u_amp)
        rs.append(q)
        b += rr
        k += 1
    return y, [r for r in rs if r < dur]


def junctional(dur, hr=48):
    return beats(dur, hr=hr, p_amp=0.0, p_after=True, seed=32)


def aivr(dur, hr=72):
    t = _t(dur)
    y = _wander(t, 33)
    rs, q = [], 0.3
    while q < dur + 1:
        y += _qrs(t, q, 0.15, 1.0, wide=True) + _twave(t, q + 0.34, -0.3, 0.075)
        rs.append(q)
        q += 60 / hr
    return y, [r for r in rs if r < dur]


def pvcs(dur, hr=78, every=3, ron_t=False):
    """Sinus with a PVC replacing every Nth beat; ron_t lands it on the preceding T wave then runs VT."""
    t = _t(dur)
    y = _wander(t, 34)
    rr = 60 / hr
    rs, b, k = [], 0.25, 0
    while b < dur + 1:
        q = b + 0.16
        if k % every == every - 1:
            early = q - (0.36 if ron_t else 0.24)
            y += _qrs(t, early, 0.16, 1.25, wide=True) + _twave(t, early + 0.32, -0.45, 0.08)
            rs.append(early)
            if ron_t:
                vt_y, vt_r = vt(max(0.1, dur - early - 0.4), hr=190)
                i0 = int((early + 0.4) * FS)
                n = min(vt_y.size, y.size - i0)
                y[i0:i0 + n] += vt_y[:n]
                rs += [early + 0.4 + r for r in vt_r]
                break
            b += rr * 1.6
        else:
            y += _p(t, b + 0.05) + _qrs(t, q, 0.08) + _twave(t, q + 0.26)
            rs.append(q)
            b += rr
        k += 1
    return y, [r for r in rs if r < dur]


def preexcited_af(dur, seed=35):
    """Irregular, very fast, wide and bizarre complexes of varying width (AF over an accessory pathway)."""
    t = _t(dur)
    rng = np.random.default_rng(seed)
    y = _wander(t, seed, 0.01)
    rs, q = [], 0.2
    while q < dur + 1:
        w = rng.uniform(0.09, 0.16)
        a = rng.uniform(0.75, 1.45)
        y += _g(t, q - 0.03, 0.03, 0.3 * a) + _qrs(t, q, w, a, wide=True) + _twave(t, q + 0.2, -0.25 * a, 0.05)
        rs.append(q)
        q += rng.uniform(0.22, 0.42)
    return y, [r for r in rs if r < dur]


def artifact(dur, hr=80, start_noise=1.0, seed=36):
    """Motion artifact that mimics VF, with the patient's normal QRS marching through it."""
    y, rs = sinus(dur, hr=hr, seed=seed)
    t = _t(dur)
    rng = np.random.default_rng(seed)
    noise = sum(np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) for f in rng.uniform(4, 9, 5))
    noise = 0.55 * noise / np.abs(noise).max() + rng.normal(0, 0.05, t.size)
    y = y + noise * (t > start_noise)
    return y, rs


def brugada(dur, hr=70):
    """V1-style type 1 Brugada: rSR' with coved ST elevation into an inverted T."""
    t = _t(dur)
    y = _wander(t, 37)
    rr = 60 / hr
    rs, b = [], 0.25
    while b < dur + 1:
        q = b + 0.16
        y += (_p(t, b + 0.05, 0.1) + _g(t, q - 0.02, 0.012, 0.25) + _g(t, q + 0.02, 0.014, -0.35)
              + _g(t, q + 0.065, 0.022, 0.75) + _g(t, q + 0.14, 0.055, 0.42) + _g(t, q + 0.29, 0.05, -0.32))
        rs.append(q)
        b += rr
    return y, [r for r in rs if r < dur]


def fine_vs_asystole(dur, gain_up_at=3.0):
    """Fine VF that looks flat until the gain is turned up."""
    y, _ = vfib(dur, coarse=False, seed=38)
    t = _t(dur)
    scale = np.where(t < gain_up_at, 0.12, 1.0)
    return y * scale, []


RHYTHMS = {
    "sinus": sinus, "first_degree": first_degree, "svt": svt, "afib": afib, "aflutter": aflutter,
    "vt": vt, "torsades": torsades, "vfib": vfib, "asystole": asystole, "mobitz1": mobitz1,
    "mobitz2": mobitz2, "chb": chb, "paced": paced, "hyperk": hyperk, "cpr": cpr_artifact,
    "sequence": sequence, "beats": beats, "junctional": junctional, "aivr": aivr, "pvcs": pvcs,
    "preexcited_af": preexcited_af, "artifact": artifact, "brugada": brugada, "fine_vs_asystole": fine_vs_asystole,
}


def make(name, dur, **kw):
    y, rs = RHYTHMS[name](dur, **kw)
    return np.asarray(y, dtype=np.float32), [float(r) for r in rs]


def capno(dur, etco2=12.0, rr=10, rise=None):
    """Capnography waveform (mmHg). rise=(t0, new_value) for an abrupt ROSC jump."""
    t = _t(dur)
    period = 60 / rr
    ph = (t % period) / period
    plateau = np.clip((ph - 0.08) / 0.06, 0, 1) * np.clip((0.72 - ph) / 0.05, 0, 1)
    level = np.full_like(t, etco2)
    if rise:
        t0, val = rise
        level = np.where(t < t0, etco2, etco2 + (val - etco2) * np.clip((t - t0) / 1.2, 0, 1))
    return (plateau * level * (1 + 0.04 * ph)).astype(np.float32)
