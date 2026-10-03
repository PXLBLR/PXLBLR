"""Render PXLBLR loops.

  python3 build.py preview beach      # contact sheet + full-res stills -> out/preview/
  python3 build.py video beach        # 1920x1080 30 fps 60 s mp4 with ambience -> out/
  python3 build.py video all
  python3 build.py audio library      # re-mix only the soundtrack into the existing mp4
"""
import os
import subprocess
import sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine.px import W, H, S, FPS, DUR, N  # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "out")


def scene(name):
    if name == "beach":
        from scenes.beach import Beach
        return Beach()
    if name == "dino":
        from scenes.dino import Dino
        return Dino()
    if name == "pumpkin":
        from scenes.pumpkin import Pumpkin
        return Pumpkin()
    if name == "lake":
        from scenes.lake import Lake
        return Lake()
    if name == "ramen":
        from scenes.ramen import Ramen
        return Ramen()
    if name == "cabin":
        from scenes.cabin import Cabin
        return Cabin()
    if name == "aurora":
        from scenes.aurora import Aurora
        return Aurora()
    if name == "library":
        from scenes.library import Library
        return Library()
    raise SystemExit(f"unknown scene {name}")


def preview(name, times=(0, 2.9, 7.4, 15, 22.2, 30, 37.5, 44, 52.1)):
    sc = scene(name)
    os.makedirs(os.path.join(OUT, "preview"), exist_ok=True)
    frames = [sc.frame(t) for t in times]
    frames[0].save(os.path.join(OUT, "preview", f"{name}_still.png"))
    frames[2].save(os.path.join(OUT, "preview", f"{name}_still2.png"))
    tw, th = 640, 360
    sheet = Image.new("RGB", (tw * 3, th * 3))
    for i, fr in enumerate(frames):
        sheet.paste(fr.resize((tw, th), Image.LANCZOS), ((i % 3) * tw, (i // 3) * th))
    sheet.save(os.path.join(OUT, "preview", f"{name}_sheet.png"))
    # loop check: frame N must equal frame 0
    a = np.asarray(sc.frame(0)).astype(int)
    b = np.asarray(sc.frame(DUR)).astype(int)
    print("loop seam diff:", np.abs(a - b).mean())


def video(name):
    sc = scene(name)
    os.makedirs(OUT, exist_ok=True)
    wav = os.path.join(OUT, f"{name}.wav")
    from engine import audio
    audio.write_wav(wav, sc.audio())
    title = {"pumpkin": "PumpkinPatch", "lake": "AutumnLake", "ramen": "RainyRamen", "cabin": "ChristmasCabin",
             "aurora": "NorthernLights", "library": "TreehouseLibrary"}.get(name, name.capitalize())
    mp4 = os.path.join(OUT, f"PXLBLR_NinjaBloks_{title}_1min_1080p.mp4")
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W*S}x{H*S}", "-r", str(FPS),
           "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-tune", "animation",
           "-pix_fmt", "yuv420p", "-profile:v", "high", "-x264-params", "keyint=60",
           "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", mp4]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(N):
        p.stdin.write(sc.frame(i / FPS).tobytes())
        if i % 300 == 0:
            print(name, i, "/", N, flush=True)
    p.stdin.close()
    p.wait()
    print("wrote", mp4)


def audio_only(name):
    """Re-mix just the soundtrack and swap it into the existing mp4 (video stream copied untouched)."""
    sc = scene(name)
    from engine import audio
    wav = os.path.join(OUT, f"{name}.wav")
    audio.write_wav(wav, sc.audio())
    title = {"pumpkin": "PumpkinPatch", "lake": "AutumnLake", "ramen": "RainyRamen", "cabin": "ChristmasCabin",
             "aurora": "NorthernLights", "library": "TreehouseLibrary"}.get(name, name.capitalize())
    mp4 = os.path.join(OUT, f"PXLBLR_NinjaBloks_{title}_1min_1080p.mp4")
    tmp = mp4 + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, mp4)
    print("re-muxed", mp4)


if __name__ == "__main__":
    mode, name = sys.argv[1], sys.argv[2]
    names = ["beach", "dino", "pumpkin", "lake", "ramen", "cabin", "aurora", "library"] if name == "all" else [name]
    for n in names:
        {"preview": preview, "video": video, "audio": audio_only}[mode](n)
