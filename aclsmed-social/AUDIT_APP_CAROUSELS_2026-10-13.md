# Clinical audit — app carousels CL01, AC01, EB01 (Oct 13, 2026)

An independent reviewer checked every slide, caption, DM and listed source against primary guidelines and the
apps' own repos and listings before RN sign-off. All findings below were fixed and re-rendered.

| # | Sev | Item | Finding | Fix |
|---|---|---|---|---|
| 1 | HIGH | EB01 s05 | iPhone screenshot read "Sinus bradycardia… 150/min" with atrial flutter selected | Replaced with the iPad screen of the same inferior STEMI at 52/min, sinus bradycardia selected |
| 2 | HIGH | EB01 s05 | Second screenshot showed an **Anterior** build at 74/min under "Ischaemia → Inferior" | Removed (same replacement) |
| 3 | HIGH | EB01 s05, DM | Ischaemia tool and export are Pro-only; "try it" steps implied free | Steps tagged FREE (describe → watermarked preview) / PRO (ischaemia, export); DM reworded |
| 4 | HIGH | EB01 s06, DM | "iPhone, iPad & Android" — iOS not live (site lists it as coming soon) | "On Google Play now · iPhone & iPad coming soon"; DM uses the real Play link |
| 5 | HIGH | AC01 DM | Reused SIM1's reply with a literal "[App Store link]" placeholder | New SIM reply with real iPad, Android, web and ACLSMED CPR links (also serves SIM1 v2) |
| 6 | HIGH | AC01 caption | Claimed the CPR app measures recoil; listing says rate, depth, hands-on time | Caption now "rate, depth and hands-on time" |
| 7 | MED | CL01 s04 | "Wide, fast and unstable? Treat as VT" attributed to AHA; skipped the pulse check | "Wide and fast? Check for a pulse, and assume VT until proven otherwise"; cites AHA 2025 tachycardia algorithm |
| 8 | MED | CL01 s03 | Non-conducted P omitted blocked PACs | "A P with no QRS: a blocked PAC, or a 2nd- or 3rd-degree block" |
| 9 | MED | CL01 s06 | Library/quiz/cases next to "Free download" (they're Pro) | "full library, quiz & cases with Pro" |
| 10 | MED | AC01 s01/s06 | "Every station shares one patient" — the CPR app only pairs to the tablet | "Monitor, pump and ventilator share one virtual patient" |
| 11 | MED | EB01 s05 | "Real specimens" contradicted "every tracing is synthetic" | Removed with the s05 rewrite |
| 12 | MED | EB01 s04 | Cited ESC 2015 pericardial guideline (superseded) | ESC 2025 Myocarditis & Pericarditis |
| 13 | LOW | AC01 s04 | RESPmed VC waveforms not physiologic (square Paw; expiratory flow not reaching zero while volume does) | Waveforms cropped out; readouts only. App fix queued separately |
| 14 | LOW | AC01 s04 | Headline said "height" only | "height and sex" |
| 15 | LOW | AC01 s03 | Double-check stated as universal | "the independent double-check your policy calls for" |
| 16 | LOW | CL01 s03 | PR label far from bracket; QRS bracket unlabelled | Labels "PR 0.16 s" and "QRS 0.08 s" beside their brackets |
| 17 | LOW | CL01 sources | QRS cut-off cited to the wrong standardization part | Added Surawicz 2009 (Part III) and the AHA 2025 tachycardia algorithm |
| 18 | LOW | CL01 s02, AC01 s04/s05 | "6-/second" line break; PBW formula wrap; clipped 6th learner name | Fixed (no-wrap, one formula per line, recropped) |
| 19 | LOW | EB01 s02/s06 | Sliver of the next row in the crop; s06 iPad showed an anterior build | Crop tightened; s06 now shows the exported inferior STEMI sheet |

Verified correct (with sources in `content/app_carousels.py`): timing (0.04/0.20 s boxes), PR 0.12–0.20 s,
QRS 0.12 s, 300 rule and 6-second method, drawn brackets measured from the SVGs (4 big boxes, PR 0.16 s,
QRS 0.07/0.16 s), boxed leads II/III/aVF/aVL, UDMI ST criteria, reciprocal change, pericarditis and early
repolarization features, PBW worked example (73.3 kg → 440 mL), ISMP high-alert listing, AHA 2025 Part 12
feedback devices, and every remaining app claim against the listings and repos.

Found in the apps (not in the carousels): RESPmed's New Patient screen opens at 77.0 kg / 462 mL for a
178 cm male (correct: 73.2 kg / 439 mL); RESPmed VC waveforms (item 13). Both queued as separate tasks.

Status: all three **pending human clinician sign-off** (`python3 review.py approve <id> "<Name, RN>"`).
