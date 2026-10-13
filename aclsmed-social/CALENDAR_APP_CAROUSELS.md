# App carousels — Oct 13–31, 2026 (12:00 PM ET, between the 7:30 AM / PM reels)

One carousel a day, rotating CardioLens AI → ACLSMED Sim → ECG Builder. Each one teaches a single idea,
uses the real app screen as the example, and ends on a comment keyword that ManyChat answers with the
store link. Design canvas: https://claude.ai/artifact/892aFz9JQH7ADWyRPLKdC4

| Date | App | Topic | Keyword | Status |
|---|---|---|---|---|
| Tue Oct 13 (5:00 PM) | ACLSMED Sim | Drip math in 3 steps: mcg/min → mL/h (IVmed) | SIM | building |
| Wed Oct 14 | CardioLens AI | Read any strip in 5 questions | LENS | approved (Mikko Figueroa, RN) · bundle ready |
| Thu Oct 15 | ACLSMED Sim | One patient, four stations | SIM | approved (Mikko Figueroa, RN) · bundle ready |
| Fri Oct 16 | ECG Builder | Inferior STEMI: the clue in aVL | BUILD | approved (Mikko Figueroa, RN) · bundle ready |
| Sat Oct 17 | CardioLens AI | "Irregular" isn't one rhythm: AFib vs MAT | LENS | planned |
| Sun Oct 18 | ACLSMED Sim | Kids aren't small adults: PALS doses by weight | SIM | planned |
| Mon Oct 19 | ECG Builder | LBBB vs RBBB: build both | BUILD | planned |
| Tue Oct 20 | CardioLens AI | How to work an ECG case | LENS | planned |
| Wed Oct 21 | ACLSMED Sim | Plan a 15-minute mock code | SIM | planned |
| Thu Oct 22 | ECG Builder | Posterior MI: the STEMI hiding in V1–V3 | BUILD | planned |
| Fri Oct 23 | CardioLens AI | The conduction system in 1 slide | LENS | planned |
| Sat Oct 24 | ACLSMED Sim | Infant brady under 60: when to start CPR | SIM | planned |
| Sun Oct 25 | ECG Builder | LVH: big voltage, strain, not a STEMI | BUILD | planned |
| Mon Oct 26 | CardioLens AI | Axis in 2 leads: I and aVF | LENS | planned |
| Tue Oct 27 | ACLSMED Sim | Debrief like a pro: 5 questions | SIM | planned |
| Wed Oct 28 | ECG Builder | Educators: an exam strip in 60 s | BUILD | planned |
| Thu Oct 29 | CardioLens AI | Mega codes on your phone | LENS | planned |
| Fri Oct 30 | ACLSMED Sim | Drowning arrest: why breaths come first | SIM | planned |
| Sat Oct 31 | ECG Builder | Halloween: the ghost STEMI (de Winter T waves) | BUILD | planned |

Topics were checked against everything already posted (R1–R7, C1–C7, S01–S37, SIM1). Dropped for repeating
earlier posts: AV blocks (C7), CPR numbers (C4), capnography (R4), hyperkalemia (R7), pacing (R6),
H's & T's (C1), tombstone STEMI (S09 v2 reposts Oct 26), and "Defib, sync or pace?" (S24, R6, C2).

## Pipeline
1. Design on the canvas, copy each artboard to `app_carousels/src/<id>/s0N.dc.html`.
2. `NODE_PATH=$(npm root -g) node app_carousels/render.mjs` → `out/app_carousels/<id>/s0N.png` (1080×1350).
   The renderer fails on missing images or on any fixed-height element squeezed by overflow.
3. Captions, alt text, DM reply and sources live in `content/app_carousels.py`.
4. Clinical gate: `python3 review.py approve <id> "<Name, RN>"`, then
   `python3 package_app_carousels.py post <dir>` (skips anything not signed off).

## Before these post
- ManyChat replies for **LENS** and **BUILD** (SIM already exists).
- ECG Builder's iOS App Store link: the website still lists it as "coming soon" on iOS. Fill it in the
  BUILD DM, or change the last slide to Android only.
