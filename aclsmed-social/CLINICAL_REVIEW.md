# Clinical review gate — required before any reel or carousel is posted

Added Oct 12, 2026 after the S09 STEMI reel was publicly called out. Nothing gets packaged for upload unless it
passes all four steps below. `review.py` enforces steps 1, 3 and 4.

## 1. Sources on every claim
Each spec carries `sources=[...]`: the primary reference (guideline / consensus statement / monograph) for every
number, dose, threshold, time target, contraindication and algorithm step shown on screen or in the caption.
Secondary blogs are not enough on their own. If a claim can't be sourced, it comes out.

## 2. Writer self-check (the failure modes that hit S09)
- **Right test for the claim.** Diagnoses that need a 12-lead (STEMI, Brugada, QT measurement, WPW, axis) are never
  taught from a single monitor lead. Use `engine/twelvelead.py`, or say clearly that it's a monitor strip.
- **Thresholds, not vibes.** "ST elevation = STEMI" is wrong without mm criteria; "give X" is wrong without its
  "only if" conditions.
- **Contraindications that cause harm.** If the reel says to give a drug, it says when *not* to (e.g. nitrates:
  SBP < 90, RV infarct, PDE-5 inhibitors, marked brady/tachy).
- **Current terminology.** e.g. first-medical-contact-to-device, not just door-to-balloon; AHA 2025 wording.
- **Visual matches text.** Strip morphology, lead label, readout and HR agree with what the text claims.
- **Mark simplifications.** Teaching illustrations are labelled as such; "per protocol" where institutions differ.

## 3. Independent review
A second reviewer (independent AI audit against the sources, then a human clinician) reads the final frames and
caption, not the script. Findings are logged as HIGH (wrong/unsafe → must fix), MED (misleading → should fix),
LOW (wording). Any HIGH or MED blocks posting.

## 4. Human sign-off
A licensed clinician (RN/MD/RRT/paramedic) signs off in `review_log.json`:
`{"S37_choking_2025": {"reviewer": "M. Figueroa, RN", "date": "2026-10-12", "status": "approved"}}`.
`python3 review.py check <id>` must pass before packaging. Educational-only disclaimer stays on every post.

## If something slips through
1. Delete or archive the post the same day and pin a correction comment.
2. Log the issue below, fix it with sources, run it through this gate again, and post the corrected version.
3. Re-audit similar content for the same failure mode.

## Incident log
| Date | Item | Problem | Action |
|---|---|---|---|
| 2026-10-12 | S09 STEMI (posted Oct 12 AM) | STEMI taught from a single monitor lead; no mm criteria or mimics; outdated "door-to-balloon"; fibrinolysis without the >120 min / <12 h / contraindication conditions; nitrate contraindications missing PDE-5 inhibitors | Post deleted; replaced today by S37 (choking, AHA 2025); corrected S09 v2 (12-lead, full criteria, sourced) ready to post after Oct 25; full audit of all 57 items run |
