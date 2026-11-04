# ACLSMED Sim · monitoring lines, one at a time · narrated reel (IG Reels + YouTube Shorts)

- **File:** `aclsmed_monitor_lines.mp4` (1080×1920, 30 fps, H.264/AAC, 44.5 s). Cover: `cover.png`.
- **Status:** POSTED 2026-11-04 ~16:20 ET on the owner's go-ahead, from the mikko.figueroa Chrome.
  Instagram @aclsmed Reel: https://www.instagram.com/aclsmed/reel/DfVaCqaTtcE/ (9:16, cover.png as cover, caption below).
  YouTube ACLSMED Short (Public): https://youtube.com/shorts/wu4aE2gMS4Y (cover.png as thumbnail, not made for kids,
  paid promotion No, AI-use disclosure No and Instagram AI label off, both by the owner's choice).
- **What it shows:** the ACLSMED Sim iPad Monitor (Console shell) with one adult patient the whole time: sinus rhythm
  76/min, NIBP 120/80, PA 25/10 (MAP 15), CVP 6, SpO₂ 98 %, EtCO₂ 38, Resp 14, Temp 37.0 °C. It starts on ECG lead II
  alone, flips through the other eleven leads the app offers (I, III, aVR, aVL, aVF, V1–V6) and back to II, then turns on
  the arterial line (ART 120/80, MAP 93), PA line, CVP, EtCO₂ and SpO₂ one at a time. The cuff keeps reading 120/80.
- **Real app footage only:** every monitor frame is the app running in the Xcode iPad Pro 13" (M5) simulator. One take
  per step, all on the same film clock, cut on the change (see Rebuild), so the sweep and the beat carry straight across
  every cut and only the new line or lead changes. Nothing on the screen is drawn or mocked up. The labels above the
  iPad, the captions, the end card and the outro are reel graphics outside the screen.
- **Voice:** "Mikko (narration) v2", the local voice clone in `/Applications/Prayer Voice.app` (VoxCPM2 + LoRA, runs on
  this Mac, no API key). Every line read back word-for-word by Whisper. The owner's script plus one line added with
  the ART step the owner asked for: "Place an arterial line." "Integrated" on the end card was re-rendered from the
  spelling "Intigrated" (take 1) and spliced in, because the first take put an "r" in it ("intergrated"; third
  formant of the vowel before the g 2140 Hz -> 2686 Hz, now above the speaker's "ay"); the rest of line 9 is unchanged. The YouTube title has no disclaimer (it would not fit in 100
  characters); the description ends with it.
- **Sound:** narration, a quiet synthesized pad from `engine/sfx.py` ducked ~9 dB under the voice, the app's own
  `heart_beep.wav` low on every R wave while the monitor is on screen, small synthesized ticks on each cut. −14.7 LUFS.
- **Frame:** iPad Pro 13" (M5) bezel from `ACLSMED/iOS/scripts/bezel_composite.swift --emit-bezel` (same as the
  shell-loop reel), 920 px wide with 80 px clear each side. All text and the iPad sit inside y 250–1500, so neither the
  Instagram nor the taller YouTube Shorts bottom overlay covers anything.

## Instagram caption
Every code starts on lead II. Then add the lines you need, one at a time. 🫀

ACLSMED Sim turns an iPad into the patient monitor for your code room: all 12 ECG leads, an arterial line, PA, CVP, capnography and the pleth, synced with the instructor's remote.

Everything on the monitor in this video is the app running. Nothing is mocked up.

Comment SIM and we'll DM you the link.

#ACLS #HealthcareSimulation #NurseEducator #CriticalCareNursing #Paramedic

Educational only, not diagnostic and not a substitute for certified ACLS training.

## YouTube Shorts
**Title:** Every monitoring line, one at a time | ACLSMED Sim #Shorts

**Description:**
ACLSMED Sim on an iPad: start on ECG lead II, flip through all 12 leads, then add an arterial line, a PA line, CVP, capnography and the SpO₂ pleth. Every frame on the monitor is the real app.

ACLSMED Sim is available on the App Store and Google Play. More at aclsmed.com

#ACLS #HealthcareSimulation #Shorts

Educational only, not diagnostic and not a substitute for certified ACLS training.

## Alt text
A 44-second narrated video of the ACLSMED Sim patient monitor running on an iPad, on a dark navy background. It starts with a single green ECG trace labelled lead II at 76 beats per minute and a cuff pressure of 120/80. The ECG then flips quickly through leads I, III, aVR, aVL, aVF and V1 to V6, with the lead name shown in large green letters above the iPad, and returns to lead II. New traces then appear one at a time: a red arterial line at 120/80, a yellow pulmonary artery line at 25/10, a light blue central venous line at 6, a white capnography trace at 38 and a cyan SpO₂ pleth at 98 percent, each named above the iPad as it appears. Captions under the iPad follow the narration. The end card reads "Integrated. Immersive. Essential." word by word, then "ACLSMED.COM" and "Educational only, not diagnostic". The last card shows the ACLSMED Sim app icon, "Available today", and the App Store and Google Play badges.

## Checks
All from `python3 check.py` on the final MP4 (2026-11-04): ALL CHECKS PASS.
- **Lanes, all 924 monitor frames (0–30.4 s):** each step shows exactly its channels (ECG only → +ART → +PA → +CVP →
  +EtCO₂ → +SpO₂), each in its own colour across ≥ 91 % of the strip with real amplitude (no flatline); with ECG only,
  the empty half under the strip stays empty.
- **Vitals, lead, popups (macOS Vision OCR, 157 frames from all 18 clips):** HR 76, NIBP 120/80, Temp 37.0, Resp 14
  everywhere; ART MAP 93, PA 25/10, CVP 6, SpO₂ 98, EtCO₂ 38 whenever that line is on; the ECG caption reads the
  shot's lead in every lead shot; film clock 10:30:12–10:30:42. No sheet, toast or popup text anywhere.
- **Safe areas:** no bright pixel outside x 80–1000, y 250–1500 in any of the 1335 frames.
- **Beat:** R waves on the lead-II clips sit 0.1717 s into each 0.789 s beat (267 R waves, median spread 6 ms); the
  QRS beep is laid on that grid.
- **Captions vs voice:** Whisper on the reel's own audio; caption word ends within 20 ms (median), 40 ms (90th pct).
  The largest "offset" (0.46 s, "Integrated.") is Whisper stretching the word into the pause after it; that card pops
  on the measured voice onset.
- **Known:** the simulator stalled for 1–2 frames (≤ 100 ms) a few times inside some shots (align.py lists them);
  they are not hidden or patched.
- Contact sheet of 16 moments checked by eye: right lines and labels at every step, end card and outro clean.

## Rebuild
1. Capture (ACLSMED iOS, Debug build, iPad Pro 13" (M5) iPadOS 26.5 simulator 7BC4…, turned landscape):
   `OUT_DIR=<dir> ./scripts/record_monitor_lines.sh` (scenario `-uiDemo reel-monitor-lines -lines <art,pa,cvp,etco2,spo2>
   -lead <lead>`, `App/UIDemo+MonitorLines.swift`, DEBUG only). `ONLY="<take names>"` re-shoots single takes. The raw
   takes are not in this repo (about 30 MB); the cut clips are (`public/segments`).
2. `python3 align.py <dir>` → `public/segments/<shot>.mp4` + `src/alignment.json`.
3. Narration: render each `timeline.json` line with the Prayer Voice app (voice `narration`, take 0) into
   `public/vo/l1..l10.wav` (`*.wav` is gitignored here, so the clips stay local), Whisper word times into
   `src/vo_whisper.json`, then `python3 make_words.py` → `src/words.json`.
4. Copy `heart_beep.wav` from `ACLSMED/iOS/ACLSMED/Resources/Sounds/` into `public/`, then `python3 make_audio.py`.
5. `npm ci && CHROMIUM=<chrome-headless-shell> node render.mjs` (`node render.mjs stills <frames…>` for stills; port 3417).
6. `python3 check.py`.
