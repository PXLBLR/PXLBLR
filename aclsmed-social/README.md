# ACLSMED social content engine

Generates the faceless, voiceless Instagram reels (1080×1920, 30–45 s, SFX-driven) and carousels (1080×1350) for @aclsmed. Everything is procedural: the ECG and capnography traces, the SFX (monitor beeps synced to each QRS, alarms, defib charge and shock, whooshes, ticks, dings) and the ACLSMED brand styling. There are no stock assets, so there's no licensing to worry about.

- **This week's posts:** see [`CALENDAR.md`](CALENDAR.md) (Oct 1–7, 2026: times, captions, hashtags, alt text).
- **Finished files:** `out/reels/*.mp4` (+ `*_cover.png`), `out/carousels/<id>/NN.png`.

## Rebuild

```bash
pip install pillow numpy imageio-ffmpeg
python3 build.py preview R3   # contact sheet of frames → out/preview/ (fast QA, no encode)
python3 build.py reels        # all reels (or: python3 build.py reels R3)
python3 build.py carousels    # all carousel slides
```

## Make a new post

- **Reel:** add a function to `content/reels.py` that returns `{"id", "duration", "elements", "sfx"}` and append it to `REELS`. Helpers: `T()` text, `P()` pill, `M()` monitor strip, `SHOCK()` charge→shock with flash and shake, `endcard()`. Text marked `*like this*` renders in the accent colour.
- **Carousel:** add a dict to `content/carousels.py`. The block types are listed at the top of `engine/carousel.py`.
- **Rhythms** (`engine/ecg.py`): sinus, first_degree, svt, afib, aflutter, vt, torsades, vfib, asystole, mobitz1, mobitz2, chb, paced (capture on/off), hyperk (stages 1–3), cpr, and `sequence` to chain them (e.g. SVT → adenosine pause → sinus).
- **Logo:** drop a transparent `assets/logo.png` and it replaces the built-in wordmark everywhere.

Brand: Red `#EF4444`, Navy `#05081A`, Cyan `#00DCC8`, monitor green `#00E640`. Fonts: Outfit, DM Sans, JetBrains Mono (OFL, in `fonts/`).

All clinical content is educational only and aligned to the AHA 2025 Guidelines. Verify it against your institution's protocols before posting.
