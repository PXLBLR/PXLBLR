# App issues found while auditing the Oct 13–31 carousels (not fixed; queue for the app repos)

## ACLSMED (aclsmed/simulator.html SCENARIOS) — priority: Oct 24 carousel sends learners to #15
1. `pals_brady` debrief: "Begin CPR immediately" contradicts AHA 2025 Pediatric Bradycardia (support airway/breathing
   first, CPR if HR stays <60/min with compromise); teaches 2-finger infant compressions (removed in AHA/AAP 2025: two-thumb
   encircling or heel of one hand); "at least 100/min" (2025: 100–120/min); cites 2020.
2. `pals_vf`, `bls_drown` cite 2020 (drowning: cite the 2024 AHA/AAP focused update + 2025).
3. `bls_drown` 12-lead text "Sinus Tachycardia 108, J-waves" vs case HR 40.
4. Infant chart age "0.25y" → "3 mo".
5. Remote MEDS tab and web med panel only have fixed adult doses; PALS cases log adult doses.
6. RESPmed New Patient PBW (77.0 kg vs 73.2 kg for 178 cm male) and VC waveforms — already queued Oct 13.

## CardioLens (cardiolens/iOS, cardiolens/AndroidAPK)
1. Rhythm Mastery questions say "this strip" but show no strip (quiz_bank_v1.json, MasteryQuizView.swift, LearnScreen.kt).
2. Axis Finder labels I up + aVF down "Left Axis Deviation, −30° to −90°" — needs the lead II check (AxisInterpretationView.swift).
3. Clinical Cases show Diagnosis + teaching points before the Quiz tab (CaseDetailView.swift, CasesScreen.kt).
4. algorithms.json / MegaCodeScenario.swift: ERC-style wording (adrenaline, 4 H's & 4 T's, amiodarone only, TTM), lidocaine
   graded wrong in Classic VFib Arrest, unsourced survival percentages — not AHA 2025.
5. PQRST module: "ST isoelectric ±0.5 mm — elevation or depression is pathological" overstates.
6. Library has 36 rhythms; website/listing say "40+".
