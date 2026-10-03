# PXLBLR loops (NINJA-BLOKS)

Procedural pixel-art loop engine for the PXLBLR YouTube background videos. It renders 1080p30 seamless loops with ambience and SFX that are synced to what happens on screen.

- **Samples:** `out/PXLBLR_NinjaBloks_Beach_1min_1080p.mp4` and `out/PXLBLR_NinjaBloks_Dino_1min_1080p.mp4`
- **Brief for Gemini:** [`PROMPT_GEMINI.md`](PROMPT_GEMINI.md)
- **Stills:** `out/preview/*_sheet.png` (contact sheets) and `out/preview/compare_*.png` (old draft vs new)

## Rebuild

```bash
pip install pillow numpy
python3 build.py preview beach   # stills + contact sheet + loop-seam check, ~2 s
python3 build.py video beach     # 60 s 1080p mp4 with audio (or: dino, all)
```

## How it works

- **The grid.** Every scene is drawn on a 384×216 art-pixel canvas and scaled 5× with nearest-neighbour, so every on-screen pixel is a 5×5 block. Slow movers such as clouds, boats and dinosaurs are pasted at screen-pixel offsets, so they glide while staying on the grid (`engine/px.py`, `Frame`).
- **The cast.** `engine/bloks.py` generates every Blok from one master sprite: the rounded block body, the headband with the gold shuriken emblem, the katana hilt, the eyes with catch-lights, blinks, sunglasses, open mouth and raised arms. Each Blok is a colourway of that sprite.
- **Brand props.** `scenes/common.py` holds the PXLBLR / NINJA-BLOKS signpost and the corner bug.
- **The loop.** Every animation uses `wave()` or `cyc()`, which assert that their period divides 60 s, so frame 1800 equals frame 0. `build.py preview` prints the seam diff, which should be 0.0.
- **Audio.** `engine/audio.py` builds the ambience beds in the frequency domain over exactly one loop length, so they loop with no click. Event SFX (gulls, poks, roar, splashes, footfalls) are placed on the frame where the action happens and panned to its position on screen.
