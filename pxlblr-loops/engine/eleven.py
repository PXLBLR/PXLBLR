"""ElevenLabs Sound Effects -> loop-perfect, frame-synced scene soundtracks.

The API key is read from the ELEVENLABS_API_KEY environment variable and is never written to disk.
Every generated clip is cached under audio_src/<scene>/<tag>.mp3 (with the prompt in
audio_src/<scene>/manifest.json), so rebuilding a mix never re-spends credits.

Beds: two different 30 s clips generated with loop=true are cross-faded A->B->A around the
60 s loop, so the soundtrack is seamless and does not audibly repeat every 30 s.
Events: one-shots are placed on the exact frame of the on-screen action and panned to it.
"""
import hashlib
import json
import os
import subprocess
import numpy as np
from .audio import SR, N, T, master
from .px import DUR

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "audio_src")
SRC_FAKE = os.path.join(ROOT, "out", "audio_src_fake")  # offline test clips, never mixed into real builds
API = "https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_192"


class NoKey(RuntimeError):
    pass


def _cache_path(scene, tag, fake=False):
    return os.path.join(SRC_FAKE if fake else SRC, scene, f"{tag}.mp3")


def generate(scene, tag, text, duration, influence=0.4, loop=False, fake=False):
    """Fetch (or reuse) one ElevenLabs clip. Returns the mp3 path."""
    path = _cache_path(scene, tag, fake)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    man_p = os.path.join(os.path.dirname(path), "manifest.json")
    man = json.load(open(man_p)) if os.path.exists(man_p) else {}
    spec = {"text": text, "duration_seconds": duration, "prompt_influence": influence, "loop": loop}
    key = hashlib.sha1(json.dumps(spec, sort_keys=True).encode()).hexdigest()[:12]
    if os.path.exists(path) and man.get(tag, {}).get("hash") == key:
        return path
    if fake:
        _fake_clip(path, duration, key)
    else:
        api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
        if not api_key.startswith("sk_"):
            raise NoKey("Set ELEVENLABS_API_KEY to an ElevenLabs secret key (starts with sk_).")
        body = json.dumps(dict(spec, model_id="eleven_text_to_sound_v2"))
        tmp = path + ".part"
        r = subprocess.run(["curl", "-sS", "-m", "180", "-X", "POST", API, "-H", "Content-Type: application/json",
                            "-H", f"xi-api-key: {api_key}", "--data-binary", body, "-o", tmp, "-w", "%{http_code}"],
                           capture_output=True, text=True)
        code = r.stdout.strip()
        if code != "200":
            msg = open(tmp, "rb").read()[:400].decode("utf-8", "replace") if os.path.exists(tmp) else r.stderr
            if os.path.exists(tmp):
                os.remove(tmp)
            raise RuntimeError(f"ElevenLabs {code} for {scene}/{tag}: {msg}")
        os.replace(tmp, path)
    man[tag] = dict(spec, hash=key)
    json.dump(man, open(man_p, "w"), indent=2, sort_keys=True)
    return path


def _fake_clip(path, duration, seed):
    """Offline stand-in (pink-ish noise burst) so the mixing pipeline can be tested without credits."""
    r = np.random.default_rng(int(seed, 16) % 2 ** 32)
    n = int(SR * duration)
    x = np.cumsum(r.normal(size=(n, 2)), axis=0)
    x -= np.linspace(x[0], x[-1], n)
    x = x / (np.abs(x).max() + 1e-9) * 0.5
    raw = (x * 32767).astype("<i2").tobytes()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", "-", path],
                   input=raw, check=True)


def load(path, circular=False, hp=35.0):
    """Decode to float stereo (2, n) at the engine sample rate, high-passed at `hp` Hz.

    Generated clips can carry inaudible sub-bass/DC that skews loudness matching and reads as rumble.
    Looping beds are filtered circularly so their own loop point stays seamless.
    """
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, "<f4").reshape(-1, 2).T.astype(np.float64)
    from .audio import band
    return np.stack([band(ch, hp, 20000, order=6, circular=circular) for ch in x])


def rms_norm(x, db=-20.0):
    r = np.sqrt(np.mean(x ** 2)) + 1e-12
    return x * (10 ** (db / 20) / r)


def active_norm(x, db=-20.0, floor_db=-30.0):
    """Match loudness over the audible part only (frames within 30 dB of the loudest), so short
    one-shots with silence around them aren't over-boosted."""
    n = int(0.05 * SR)
    k = max(1, x.shape[1] // n)
    fr = np.sqrt(np.mean(x[:, :k * n].reshape(2, k, n) ** 2, axis=(0, 2))) + 1e-12
    act = fr[fr > fr.max() * 10 ** (floor_db / 20)]
    r = np.sqrt(np.mean(act ** 2))
    return x * (10 ** (db / 20) / r)


def bed_loop(clips, xf=3.0):
    """Cross-fade two self-looping clips into one seamless loop of N samples (A for 0-30 s, B for 30-60 s)."""
    a, b = clips[0], clips[-1]
    la, lb = a.shape[1], b.shape[1]
    ia = np.arange(N) % la
    ib = np.arange(N) % lb
    half = DUR / 2
    # equal-power weights, periodic over the loop: A centred on 15 s, B on 45 s
    t = T
    d = np.minimum(np.abs(((t - half / 2) + DUR / 2) % DUR - DUR / 2), DUR / 2)  # distance from 15 s, circular
    w = np.clip((half / 2 + xf / 2 - d) / xf, 0, 1)
    wa, wb = np.sqrt(w), np.sqrt(1 - w)
    return a[:, ia] * wa + b[:, ib] * wb


def place(buf, sig, t0, gain=1.0, pan=0.0):
    """Add a stereo clip at t0 (wrapping at the loop point) with a balance pan that keeps its width."""
    i0 = int(round(t0 * SR)) % N
    idx = (i0 + np.arange(sig.shape[1])) % N
    gl = np.clip(1 - pan, 0, 1) if pan > 0 else 1.0
    gr = np.clip(1 + pan, 0, 1) if pan < 0 else 1.0
    mono = sig.mean(axis=0)
    # pan: blend toward the mono sum on the far side so hard pans stay natural
    left = sig[0] * gl + (mono * (1 - gl) * 0.35 if pan > 0 else 0)
    right = sig[1] * gr + (mono * (1 - gr) * 0.35 if pan < 0 else 0)
    np.add.at(buf[0], idx, left * gain)
    np.add.at(buf[1], idx, right * gain)


def sweep(buf, sig, t0, gain, pan0, pan1):
    i0 = int(round(t0 * SR)) % N
    idx = (i0 + np.arange(sig.shape[1])) % N
    pan = np.linspace(pan0, pan1, sig.shape[1])
    gl = np.where(pan > 0, 1 - pan, 1.0)
    gr = np.where(pan < 0, 1 + pan, 1.0)
    np.add.at(buf[0], idx, sig[0] * gl * gain)
    np.add.at(buf[1], idx, sig[1] * gr * gain)


def fade_edges(x, ms=8):
    m = int(SR * ms / 1000)
    if x.shape[1] > 2 * m:
        ramp = np.linspace(0, 1, m)
        x = x.copy()
        x[:, :m] *= ramp
        x[:, -m:] *= ramp[::-1]
    return x


def lean(spec):
    """Cheaper build: one take per bed and per event (beds then repeat every 30 s)."""
    out = {"beds": [dict(b, variants=1) for b in spec["beds"]], "events": [dict(e, variants=1) for e in spec["events"]]}
    return out


def render(scene, spec, fake=False, raw=False):
    """spec = {"beds": [...], "events": [...]} (see scenes/el_audio.py). Returns a mastered (2, N) mix."""
    buf = np.zeros((2, N))
    for bed in spec["beds"]:
        clips = []
        for v in range(bed.get("variants", 2)):
            p = generate(scene, f"{bed['tag']}_{v}", bed["text"], 30.0, bed.get("influence", 0.35), loop=True, fake=fake)
            clips.append(rms_norm(load(p, circular=True, hp=bed.get("hp", 35.0))))
        x = bed_loop(clips)
        if "env" in bed:
            x = x * bed["env"](T)[None, :]
        bal = bed.get("pan", 0.0)
        x[0] *= min(1.0, 1 - bal) if bal > 0 else 1.0
        x[1] *= min(1.0, 1 + bal) if bal < 0 else 1.0
        buf += x * 10 ** (bed["db"] / 20)
    for ev in spec["events"]:
        clips = []
        for v in range(ev.get("variants", 1)):
            p = generate(scene, f"{ev['tag']}_{v}", ev["text"], ev["dur"], ev.get("influence", 0.45), fake=fake)
            x = load(p)
            if np.abs(x).max() < 0.01:
                raise RuntimeError(f"{scene}/{ev['tag']}_{v} came back silent; change its prompt and regenerate")
            clips.append(fade_edges(active_norm(x, -20.0)))
        for i, hit in enumerate(ev["at"]):
            t0, gdb, pan = hit[0], hit[1] if len(hit) > 1 else 0.0, hit[2] if len(hit) > 2 else 0.0
            sig = clips[i % len(clips)]
            g = 10 ** ((ev["db"] + gdb) / 20)
            if len(hit) > 3:
                sweep(buf, sig, t0 - ev.get("lead", 0.0), g, pan, hit[3])
            else:
                place(buf, sig, t0 - ev.get("lead", 0.0), g, pan)
    return buf if raw else master(buf, rms_db=-19.0)


def plan(scene, spec):
    """Seconds of audio that would be requested (cached clips cost nothing)."""
    total = 0.0
    for bed in spec["beds"]:
        total += 30.0 * bed.get("variants", 2)
    for ev in spec["events"]:
        total += ev["dur"] * ev.get("variants", 1)
    return total
