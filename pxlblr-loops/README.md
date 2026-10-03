# PXLBLR loops (NINJA-BLOKS)

Procedural pixel-art loop engine for the PXLBLR YouTube background videos. It renders 1080p30 seamless loops with ambience and SFX that are synced to what happens on screen.

- **Samples:**
  - Beach and Dino Valley: `out/PXLBLR_NinjaBloks_Beach_1min_1080p.mp4`, `out/PXLBLR_NinjaBloks_Dino_1min_1080p.mp4`
  - Season pack: `out/PXLBLR_NinjaBloks_PumpkinPatch_1min_1080p.mp4`, `out/PXLBLR_NinjaBloks_AutumnLake_1min_1080p.mp4`, `out/PXLBLR_NinjaBloks_RainyRamen_1min_1080p.mp4`
  - Winter and cosy pack: `out/PXLBLR_NinjaBloks_ChristmasCabin_1min_1080p.mp4`, `out/PXLBLR_NinjaBloks_NorthernLights_1min_1080p.mp4`, `out/PXLBLR_NinjaBloks_TreehouseLibrary_1min_1080p.mp4`
- **Briefs for Gemini:** [`PROMPT_GEMINI.md`](PROMPT_GEMINI.md) (Beach and Dino Valley) , [`PROMPT_GEMINI_SEASON_PACK.md`](PROMPT_GEMINI_SEASON_PACK.md) (Pumpkin Patch, Autumn Lake, Rainy Ramen) and [`PROMPT_GEMINI_WINTER_PACK.md`](PROMPT_GEMINI_WINTER_PACK.md) (Christmas Cabin, Northern Lights, Treehouse Library)
- **Stills:** `out/preview/*_sheet.png` (contact sheets) and `out/preview/compare_*.png` (old draft vs new)

## Rebuild

```bash
pip install pillow numpy
python3 build.py preview beach   # stills + contact sheet + loop-seam check, ~2 s
python3 build.py video beach     # 60 s 1080p mp4 with audio (or: dino, pumpkin, lake, ramen, cabin, aurora, library, all)
```

## How it works

- **The grid.** Every scene is drawn on a 384×216 art-pixel canvas and scaled 5× with nearest-neighbour, so every on-screen pixel is a 5×5 block. Slow movers such as clouds, boats and dinosaurs are pasted at screen-pixel offsets, so they glide while staying on the grid (`engine/px.py`, `Frame`).
- **The cast.** `engine/bloks.py` generates every Blok from one master sprite: the rounded block body, the headband with the gold shuriken emblem, the katana hilt, the eyes with catch-lights, blinks, sunglasses, open mouth and raised arms. Each Blok is a colourway of that sprite.
- **Brand props.** `scenes/common.py` holds the PXLBLR / NINJA-BLOKS signpost and the corner bug.
- **The loop.** Every animation uses `wave()` or `cyc()`, which assert that their period divides 60 s, so frame 1800 equals frame 0. `build.py preview` prints the seam diff, which should be 0.0.
- **Audio.** `engine/audio.py` builds the ambience beds in the frequency domain over exactly one loop length, so they loop with no click. Event SFX (gulls, poks, roar, splashes, footfalls) are placed on the frame where the action happens and panned to its position on screen.

## ElevenLabs soundtracks

`engine/eleven.py` and `scenes/el_audio.py` replace the synthesized audio with ElevenLabs Sound Effects:

- **Beds:** two 30 s takes generated with `loop=true` and cross-faded A → B → A, so the 60 s loop is seamless and doesn't repeat every 30 s.
- **Events:** one-shots placed on the exact frame of the on-screen action and panned to it, using the same timings as the visuals.
- **Cache:** every clip is saved to `audio_src/<scene>/` with its prompt in `manifest.json`, so rebuilding a mix never re-spends credits. Change a prompt and only that clip is regenerated.

```bash
python3 build.py eleven all --plan            # seconds requested (40 credits per second)
python3 build.py eleven all --plan --lean     # one take per sound, about half the cost
export ELEVENLABS_API_KEY=sk_...              # secret key, not the key ID; set it as an environment variable, never commit it
python3 build.py eleven all [--lean]          # generate, mix, and swap the new audio into the mp4s (video untouched)
python3 build.py eleven all --fake            # offline test with stand-in clips (written to out/audio_src_fake, never used in real builds)
```

Full build: about 1,137 s, roughly 45,500 credits. Lean build: about 598 s, roughly 23,900 credits.
