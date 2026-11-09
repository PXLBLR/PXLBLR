# Heart rhythms 01-10 · render notes (2026-11-09)

All ten reels built 2026-11-09. Status: **awaiting the owner's review and RN sign-off. Nothing posted or scheduled.**

## Layout (one pipeline, a reel id per step)
| Path | What |
|---|---|
| `rhythms/<id>/script.json` | narration: lines, cues (pre/onset/mech/key/action/end), gaps, `key_sentence` |
| `rhythms/reels.json` | visuals per reel: ECGSim presets, heart mode, tags, key tag, cue sounds, beeps after onset |
| `src/data/<id>.strips.json` | lead II + beat/P times from ECGSim (`node export_strips.mjs`), committed so renders need no ECGSim |
| `src/data/<id>.timeline.json` | captions, cue times, every beat on the reel clock (`make_timeline.py`) |
| `public/<id>/vo/` | take.json, lines/sentences/whisper.json committed; **full.wav local only** (owner's decision: public repo) |

```
python3 make_vo.py R02_pvt && python3 check_vo.py R02_pvt      # voice (Mac, Prayer Voice.app) + read-back
python3 make_vo.py R02_pvt --splice "Then pace" 1               # re-render one sentence and splice it at its breaths
python3 make_timeline.py R02_pvt && python3 make_audio.py R02_pvt
CHROMIUM=<Chrome for Testing 149> node render.mjs R02_pvt [R03_torsades ...]
python3 check_reel.py [ids]                                     # checks on the rendered MP4s
```
R01 moved into this layout unchanged: its new mix is identical sample for sample to the delivered one, and its frames
match the delivered MP4 within compression noise.

## Scripts 02-10
Drafted on the R01 pattern, then fact-checked by a fresh-context agent against the AHA 2025 Guidelines Part 9 (Adult
ALS). Applied: torsades = shock sustained runs right away, pulse or not, magnesium for recurrences; Mobitz II / CHB =
atropine first (may fail below the AV node), then pacing or an epinephrine drip; QT definition; asystole = check leads
and gain (fine V-fib); PEA = not enough output (the heart may still contract; the reel shows a weak squeeze); flutter
"often" 2:1; SVT = the most common type (AVNRT); CHB block level and "often" 20-40; unstable branch first for AF and
flutter, both with stroke risk. The RN should confirm against the live AHA page.

## Voice fixes 02-10
Read-back is per sentence chunk (take.json gives each chunk's place in full.wav): the whole-file decode dropped the
last phrase and once doubled a word. Spliced sentences (alternate takes): R04 "Asystole is not shockable." (take 1),
R04 "Check the leads ... isn't missed." (take 2), R09 "Then pace, or start an epinephrine drip." (take 1). Reworded
because Whisper cannot hear the difference: R06 "The atria stop squeezing and just quiver" -> "The atria no longer
squeeze. They just quiver" (stop/stops squeezing), R04 "so you don't miss fine V-fib" -> "so fine V-fib isn't missed".
"A-fib" is sent as written (the "Ay-fib" respelling read as "eye-fib"). **Listen to "torsades de pointes" (R03):**
Whisper writes it "Torsad's de point" / "tor saz", i.e. French-style with silent s's.

## Checks on the ten MP4s (`check_reel.py`, all PASS)
Final mix read back word for word; every word ends inside its caption window; the rhythm starts before "Now watch...";
the key tag starts on its sentence; the end card is up before "Practice it on..."; -14.1 to -14.3 LUFS, peak -1.3/-1.4
dBFS; voice 8-17 dB over bed + beeps per line (lowest: A-fib's onset line, alarm + fast beeps start together).

---

# R01 V-fib · narrated render notes (2026-11-09)
(Paths below are from before the series layout: script.json, public/vo/ and src/timeline.json now live under
rhythms/R01_vfib/, public/R01_vfib/vo/ and src/data/R01_vfib.timeline.json.)

Output: `out/heart_vfib_mockup.mp4` (gitignored): 1080×1920, 30 fps, H.264 + AAC 48 kHz, 35.2 s.
Status: **awaiting the owner's review and RN sign-off. Not posted or scheduled.**

## Voice
- "Mikko (narration) v2" in Prayer Voice.app (VoxCPM2 + LoRA, local, `127.0.0.1:8872`, voice id `narration`, take 0),
  the same setup as `../monitor_lines`.
- `python3 make_vo.py` sends all seven lines of `script.json` as ONE job → `public/vo/full.wav` (33.8 s, 48 kHz).
  **full.wav is local only for now** (this repo is public and `*.wav` is gitignored; a clean voice stem is cloning
  material). The JSON next to it is committed; the owner decides whether full.wav goes in.
  The app renders each sentence as its own breath group and joins them; a `[pause N]` after each sentence sets the gap:
  the script's `gap_after` between lines (floor 0.3 s), 0.35 s between sentences of one line. Speech ≈ 154 wpm.
  `public/vo/take.json` keeps the exact text sent and every chunk's length and gap.
- Pronunciation is fixed in the text sent to the voice (captions keep the script spelling):
  V-fib → "Vee-fib" (capital V: a sentence starts with it), SA node → "S-A node", AV node → "A-V node",
  ACLSMED Sim → "A-C-L-S med Sim" (assumed to match "ACLSmed dot com"), ACLSmed dot com → "A-C-L-S med dot com".
- No word came out wrong, so nothing was spliced. `python3 make_vo.py --say "phrase" <take>` renders one phrase for
  a splice if a later take needs one.

## Read-back (`python3 check_vo.py`)
- Whisper large-v3-turbo (mlx, Prayer Voice venv), word timestamps → `public/vo/whisper.json`.
  All 73 script words read, none dropped, added or changed. Whisper heard "SA node", "AV node", "V-fib", "ACLS Med".
- "A-C-L-S" spelled out, not "ackles": checked on the waveform. Right after "A" there is a 0.12 s high-band hiss
  (the s of "see"), and another before "med" (the s of "ess"). "Ackles" would have a silent k closure there.
- `public/vo/lines.json`: each line's [start, end] in full.wav from the word timestamps, edges snapped to where the
  voice starts/stops (Whisper put line 1 at 0.0 s although speech starts at 0.35 s). `public/vo/sentences.json`: the
  same per sentence; make_timeline.py uses it to put the NO PULSE cue on the sentence "No pulse." instead of the start
  of its line (which was ~3 s early).

## Build
```
python3 make_vo.py && python3 check_vo.py          # voice (Mac only, Prayer Voice.app running)
python3 make_timeline.py && python3 make_audio.py
CHROMIUM=<chrome-headless-shell 149> node render.mjs
```
- `public/heart_beep.wav` = the app's QRS beep, copied from `ACLSMED/iOS/ACLSMED/Resources/Sounds/heart_beep.wav`
  (same file as the website's). It was missing from the repo (`*.wav` is gitignored); now force-added.
- make_audio.py now sets loudness like monitor_lines: measure with ffmpeg loudnorm, gain to -14 LUFS, look-ahead
  limiter at -1.5 dBFS, a second pass to make up what the limiter takes. Was -18.6 LUFS before.
- render.mjs: own port 3418, and software WebGL (`swangle`) only on Linux. On this Mac the Chromium 157 that
  `npm ci` downloads hangs on "Waiting for root component to load"; Chrome for Testing 149
  (`_TOOLING/RosaryRender/node_modules/.remotion/chrome-headless-shell/...`) renders in 18 s.

## Checks on the rendered MP4
| Check | Result |
|---|---|
| Captions with the words | Whisper on the reel audio: every spoken word falls in its caption's on-screen window (two "misses" are Whisper starting a word inside the silence before it) |
| V-fib onset | 8.92 s on strip and heart (flash, V-FIB badge, wavelets); "Now" sounds at 9.17 s |
| NO PULSE | tag fades in 20.85–21.25 s; "No pulse." spoken 20.65–21.63 s |
| End card | 28.11 s (icon, PRACTICE IT ON, ACLSMED SIM, ACLSMED.COM); "Practice" starts 28.41 s |
| Loudness | -14.2 LUFS integrated, -1.4 dBFS peak, LRA 2.3 LU |
| Voice over bed + beeps | each line 11–12 dB above everything else, median 14 dB over voiced moments; the charge, buzzer and end-card whoosh start in the breath before a line and are under the voice within ~50 ms of the first sound |
| Read-back of the final mix | all words heard; a full-file decode once wrote "as as soon as", but four segment decodes (clean and mixed) and the waveform (one vowel, then the hiss of "as soon") show one "as" |

Stills for review: 5.07 s normal beat, 9.5 s V-fib start, 21.5 s NO PULSE, 30.0 s end card
(`~/Downloads/ACLSMED R01 V-fib review/`).
