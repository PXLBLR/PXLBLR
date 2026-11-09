# ACLSMED Sim · live 12-lead on the monitor · narrated reel (IG Reels + YouTube Shorts)

- **File:** `aclsmed_live_12lead.mp4` (1080×1920, 30 fps, H.264/AAC, 64.3 s, 7.8 MB). Cover: `cover.png` (ST elevation V1-V4).
- **Status:** RN sign-off by the owner 2026-11-09. **POSTED 2026-11-09 ~15:00 ET** from the mikko.figueroa Chrome (already on @aclsmed):
  Instagram @aclsmed Reel https://www.instagram.com/aclsmed/reel/DfiI4RtP3xA/ (9:16, cover.png, caption below, AI label off) ·
  YouTube ACLSMED Short (Public) https://youtube.com/shorts/Krz7VYg9sOU (cover.png thumbnail, not made for kids, paid promotion No,
  altered content No; published after YouTube's checks finished: "No issues found").
- **What it shows:** ACLSMED Sim 2.8.0 Monitor, **Hospital shell**, on a light stage (the last monitor reel used Console
  on navy). Sinus bradycardia 48 on lead II with ART, pleth and capnogram; the lead menu, V1, aVF; ALL 12 LEADS;
  the instructor changes the rhythm live to anterior STEMI (LAD) at 108 (app presets: BP 102/65, SpO₂ 92, EtCO₂ 33);
  ST elevation V1-V4 and I, aVL, reciprocal depression III and aVF; PAUSE (FROZEN); PRINT (the built-in 12-lead
  sheet); back to live; end card.
- **Real app footage only:** one continuous take of the app in an iPad Pro 13" (M5) simulator (iPadOS 26.5), driven by
  a DEBUG film rig timed to the narration. Above the iPad, a magnifier shows the same footage enlarged, zoomed into
  the trace band of two rows, with a dashed isoelectric guide (reel graphic). The outlines on the iPad, labels,
  captions and end card are reel graphics outside the app.
- **Frame:** the whole iPad, 920 px wide (x 80-1000, y 668-1372), never cropped or zoomed; all text inside
  y 250-1500.
- **Voice:** "Mikko (narration) v2" (Prayer Voice.app, local), one take, two sentences spliced from alternate takes
  ("in I and aVL" take 1, "Now look at III and aVF" take 2) because Whisper heard "and" as "NA"/"in". The read-back
  is clean, 133 of 133 words. full.wav stays local (gitignored).
- **Sound:** narration, ducked pad (`engine/sfx.py`), the app's `heart_beep.wav` on every R wave the monitor draws
  (beat grid fitted to the drawn lead II: 47.9/min, then 108.6/min, residual ≤ 80 ms), ticks on the taps.
  -14.8 LUFS, -1.4 dBTP.

## Instagram caption (as posted)
A live 12-lead, on a code simulator. 🫀

Tap the ECG on the ACLSMED Sim monitor, pick any lead, or open all 12 at once. Here the instructor switches the
patient from sinus bradycardia to sinus tachycardia with an anterior STEMI, live: ST elevation in V1 to V4, I and
aVL, and the reciprocal ST depression in III and aVF. Pause it, print it, teach from it.

New in ACLSMED Sim 2.8. Everything on the monitor in this video is the app running.

Comment SIM and we'll DM you the link.

#ACLS #12LeadECG #HealthcareSimulation #NurseEducator #STEMI

Educational only, not diagnostic and not a substitute for certified ACLS training.

## YouTube Shorts (as posted)
**Title:** A live 12-lead on a code simulator: STEMI, lead by lead | ACLSMED Sim #Shorts

**Description:**
ACLSMED Sim 2.8 on an iPad: tap the ECG to change leads, or open all 12 leads live on the monitor. Sinus
bradycardia, then the instructor switches to sinus tachycardia with an anterior STEMI: ST elevation V1 to V4, I and
aVL, reciprocal depression in III and aVF. Pause the trace or print the full 12-lead. Every frame on the monitor is
the real app.

ACLSMED Sim is on the App Store and Google Play. More at aclsmed.com

#ACLS #12LeadECG #Shorts

Educational only, not diagnostic and not a substitute for certified ACLS training.

## Checks (`python3 check.py`, 2026-11-09: PASS)
1. Read-back of the final mix: 133 words, no errors.
2. Every heard word ends inside its caption's window.
3. Screen events at their lines: lead menu on "Tap the ECG", single lead before "all 12 leads", the grid on "Sinus
   bradycardia" and "ST elevation", the printout on "Print", the grid back on "ACLSMED Sim gives you all 12"; HR tile
   48 → 108 at the change. FROZEN + PLAY seen on the PAUSE frame.
4. -14.8 LUFS, -1.4 dBFS true peak.
5. The iPad body is whole inside the frame; nothing outside the safe box.
- **Known:** the III/aVF reciprocal depression is small in the app's monitor engine (about the thickness of the trace
  at the iPad's size); the magnifier and dashed baseline make it readable. The printout is the anterior STEMI
  recording from the 12-lead library (PTB-XL).

## Rebuild
1. Voice: `python3 make_vo.py && python3 check_vo.py` (Prayer Voice.app running); `--splice "<text>" <take>` re-renders one sentence.
2. `python3 make_cues.py` → `out/film_cues.json` (rig timing from the sentence times).
3. Capture (DEBUG rig, side copy `ACLSMED/_reel-12lead-2026-11-09/iOS`, `App/UIDemo+Live12Lead.swift`, scenario
   `-uiDemo reel-live-12lead -shell hospital`; DEBUG hooks in WaveformPanel + AllLeadsPanel): build Debug, turn the
   iPad sim landscape, `UDID=… APP=… OUT=raw/take1.mov ./capture.sh`.
4. `python3 events.py raw/take1.mov` → offset video − voice (7.09 s on take 1); cut `public/monitor.mp4` from
   `offset − 0.4` s (30 fps, 2064×1548).
5. `python3 make_timeline.py && python3 rwaves.py && python3 make_audio.py`
6. `CHROMIUM=<chrome-headless-shell 149> node render.mjs` (port 3419), then `python3 check.py`.
