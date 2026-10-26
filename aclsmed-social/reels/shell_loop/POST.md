# ACLSMED Sim · every device shell · 30 s looping reel

- **File:** `aclsmed_shell_loop.mp4` (1080×1920, 30 fps, 30 s, H.264/AAC). Loops seamlessly: the last second is the shell
  before the opener, and the sound is mixed on a circular 30 s buffer.
- **Status:** SCHEDULED on Instagram @aclsmed for **Sun Oct 25, 2026, 10:00 PM ET** (owner's go-ahead, 2026-10-25),
  through instagram.com → Scheduled content in the mikko.figueroa Chrome. Caption verified on the calendar after
  scheduling. Not published by hand; never "Publish now"/"Share".
- **Cover frame:** frame 0 (Console), Instagram's default.
- **What it shows:** one ACLSMED Sim iPad Monitor running the same patient (sinus rhythm 76/min, ART 120/80 MAP 93,
  PA 25/10 mean 15, CVP 6, SpO₂ 98 %, NIBP 120/80, Temp 37.0 °C, Resp 14) while the device shell changes every second,
  three passes through all nine shells the app ships (⚙ → DEVICE SHELL): Console, Console White, MEDIC Brushed Metal,
  MEDIC Clinical White (white/blue), Hospital Charcoal, Hospital White/Blue, Transport Red, Transport Beige and the
  classic Monitor. Monitor (Classic) fills the tenth slot of each pass.
- **Frame:** the footage sits in an iPad Pro 13" (M5) bezel, 920 px wide with 80 px clear on each side so Instagram's
  edge crop never reaches it. The body is drawn by `ACLSMED/iOS/scripts/bezel_composite.swift --emit-bezel` from the
  display mask in Apple's Simulator bundle and the device's published outside size (no Apple logo or artwork). No shell
  name on screen (owner's choice).
- **Real app footage:** every frame is the app running in the Xcode iPad Pro 13" simulator (iPadOS 27), one take per
  shell, cut together on the same clock instant. Nothing is drawn or mocked up. The QRS beep is the app's own
  `heart_beep.wav`, placed on each R wave drawn on screen; the tick on each shell change is synthesized (`engine/sfx.py`).

## Caption
One patient. Nine device shells. 🔁

ACLSMED Sim lets you put the same monitor in the housing that fits your room: Console, Hospital, MEDIC, Transport or the classic Monitor. Same rhythm, same numbers. Only the shell changes.

Find it in ⚙ → DEVICE SHELL.

Comment SIM and we'll DM you the link.

Educational only, not diagnostic and not a substitute for certified ACLS training.

#ACLS #HealthcareSimulation #NurseEducator #NursingStudent #Paramedic

## Alt text
A 30-second looping video of the ACLSMED Sim patient monitor running on an iPad. The screen shows the same patient the whole time: a green ECG in sinus rhythm at 76 beats per minute, red arterial line at 120/80, yellow pulmonary artery line at 25/10, light blue central venous line at 6 and a cyan SpO₂ pleth at 98 percent, with temperature 37.0 and respiratory rate 14. Every second the device housing around the screen changes: silver and white consoles, brushed metal and white field defibrillators, charcoal and white bedside units, red and beige transport units, and a plain flat monitor. Text above reads "Simulation has just gotten a new upgrade..." and text below reads "Integrated · Immersive · Essential", "ACLSMED.COM" and "Educational only, not diagnostic".

## DM (keyword SIM)
Use the existing SIM reply (`content/app_carousels.py` SIM_DM).

## Checks (2026-10-25, `python3 check.py` + OCR)
- All 900 frames: five lanes (ECG II, ART, PA, CVP, SpO₂), each with its own colour across ≥ 92 % of the strip and real
  amplitude (no flatline, no sixth lane).
- Vitals read by macOS Vision on all 30 seconds: 76, 120/80 MAP 93, 25/10 MAP 15, 6, 98, NIBP 120/80, 37.0, 14,
  film clock 10:30:xx. No sheets or popups (contact sheet of every second).
- Beat: R waves agree with the shared beat grid within ±20 ms on most seconds (worst reliable second −39 ms).
- Audio: 38 beeps 788-790 ms apart, a tick on all 30 seconds; the seam gap reads 806 ms only because AAC pads the end
  by 16 ms.
- Known: the simulator stalled now and then during capture (another render was loading the Mac), so a few seconds hold
  the sweep for 1-2 frames.

## Rebuild
1. Capture (ACLSMED iOS repo, Debug build on the iPad Pro 13" iPadOS 27 simulator):
   `OUT_DIR=<dir> TAKES="1 2" ./scripts/record_shell_loop.sh`, scenario `-uiDemo reel-shell-loop -shell <rawValue>`.
   The raw takes are not in this repo (about 50 MB); the 30 cut clips are (`public/segments`).
2. `python3 align.py <dir>` → `public/segments/s00..s29.mp4` + `src/alignment.json` (fits every take to the film clock,
   picks the smoothest take for each second, checks the R waves agree across shells). `--recut` re-cuts the same choices.
3. Bezel: `swift ACLSMED/iOS/scripts/bezel_composite.swift --emit-bezel public/bezel.png --role monitor --margin 0
   --shadow 0 --maxlong 1840 --bg none`, then measure the aperture into `src/bezel.json` (1730×1298 at 55,55).
4. Copy `heart_beep.wav` from `ACLSMED/iOS/ACLSMED/Resources/Sounds/` into `public/` (`*.wav` is gitignored here), then
   `python3 make_audio.py` → `public/audio.wav`.
5. `npm ci && CHROMIUM=<chrome-headless-shell> node render.mjs` → `aclsmed_shell_loop.mp4`
   (`node render.mjs stills 0 105 899` for stills; `COMP=ShellLoopLabeled` adds a small shell name under the iPad).
   `render.mjs` serves on port 3417 because another Remotion job on this Mac uses 3000.
6. `python3 check.py`.
