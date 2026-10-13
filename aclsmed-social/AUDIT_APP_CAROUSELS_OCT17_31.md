# Clinical audit — app carousels Oct 17–31, 2026

Independent reviewers checked every slide, caption, alt text, DM and source against primary guidelines and the
apps' own code before RN sign-off. AHA PDFs and AHA Journals return 403 from the build environment, so some 2025
checks used search-index text of the AHA PDFs, mirrors or quoting summaries; those are flagged for the RN.

## ACLSMED Sim — AC02–AC06

Cross-cutting: (a) tablet Sim is paid; the only free tier is the web simulator with MegaCode #09. s05 is tagged
PRO, but s06, captions and DM first lines send people to #13–#16 / "33 MegaCodes" with no Pro mention → tag Pro
there. (b) The Remote MEDS tab and web med panel log fixed ADULT doses (epi 1 mg, adenosine 6/12, atropine 1.0,
amio 300/150): "tap the drug and it lands in the log" records an adult dose in PALS cases → tell learners to say the
weight-based dose aloud.

### AC02_pals_doses_weight
| # | Sev | Where | Finding | Fix |
|---|---|---|---|---|
| 1 | MED | s05 step 3, s06 | MEDS logs adult doses | s05 step 3: "Switch to **#14 Pediatric VF** (45 kg): first shock 90 J. Tap each drug on **MEDS** to time-stamp it. MEDS lists adult doses, so say the weight-based dose out loud." s06 log card likewise |
| 2 | MED | s06, caption, DM | Pro cases offered without Pro | s06: "4 PALS/neonatal MegaCodes (Pro) with weights on the chart"; caption "…pediatric MegaCodes (Pro plan)…"; DM "(Pro plan)" after "MegaCode #16 Pediatric SVT" |
| 3 | MED | s04 footer, sources | 2020 algorithm name; 2025 second adenosine dose (0.2 mg/kg max 12) not verified from a primary source | Footer "AHA 2025 PALS · Pediatric Tachyarrhythmia With a Pulse Algorithm"; **RN to confirm 0.2 mg/kg (max 12 mg) in the 2025 PDF** |
| 4 | LOW | s03, caption | Amiodarone cap missing | "Amiodarone 5 mg/kg IV/IO bolus (max 300 mg)" |
| 5 | LOW | s06 | #17 is neonatal | "PALS/neonatal" |
| 6 | LOW | s04 | "Never guess an adult dose" ambiguous | "Never guess, and never default to an adult dose." |
| 7 | LOW | s05 footer | Web capture, iPad steps | "Real ACLSMED Sim case chart (web simulator) · simulated patient" |
| 8 | LOW | DM | "certified ACLS training" on a PALS post | "certified ACLS/PALS training" (AC02, AC04, AC06 DMs) |

### AC03_mock_code_15min
| # | Sev | Where | Finding | Fix |
|---|---|---|---|---|
| 1 | MED | s03 footer | Educator moves credited to AHA Part 12; they're from the ACLSMED manual | Left "Educator moves: ACLSMED Instructor Manual"; right "RCDP: AHA 2025 Part 12 · Resuscitation Education Science" |
| 2 | MED | s06, caption, DM | No Pro mention; Remote is Pro & Clinical Suite | s06 "33 MegaCodes (Pro) with chart and learning objectives"; DM "On the Instructor Remote (Pro or Clinical Suite) open CODES…" |
| 3 | LOW | s04, caption | Script benefit overstated (weak rec.) | "AHA 2025: a debriefing script can help instructors guide the discussion and keep debriefs consistent." |
| 4 | LOW | s04 | "One for each learner" not PEARLS | "What will you take to practice?" |
| 5 | LOW | s01 | 5-min debrief short (optional) | Optional "BRIEF 0–3 · RUN 3–9 · DEBRIEF 9–15" (update everywhere if changed) |

### AC04_infant_brady_cpr
| # | Sev | Where | Finding | Fix |
|---|---|---|---|---|
| 1 | MED | s05, s06 | MEDS logs atropine 1.0 mg / epi 1 mg for 5.2 kg | s06 "Every drug time-stamped in the log (say the mg/kg dose aloud)"; same note on s05 |
| 2 | MED | s06, caption, DM | #15 is Pro | s06 "#15 Infant brady (Pro) with weight, vitals and chart"; DM "load MegaCode #15 (Pro) Infant Symptomatic Bradycardia…" |
| 3 | LOW | s01 | "poor perfusion" isn't the algorithm's criterion | "…when the rate stays under 60/min with cardiopulmonary compromise, even after you support the airway and breathing." |
| 4 | LOW | s02 | Algorithm covers children, not only infants | Label "IN CHILDREN"; "Hypoxia is a common, reversible cause. That's why airway and breathing come before the drugs." |
| 5 | LOW | hashtags | #NICU invites NRP confusion | Replace with #PediatricNursing |
| 6 | LOW | s03 footer | Box 6 (pacing) omitted | "Algorithm boxes 3–5, 7–8 (pacing omitted)" |

### AC05_debrief_5_questions
| # | Sev | Where | Finding | Fix |
|---|---|---|---|---|
| 1 | MED | s04, caption | Basic assumption is © Center for Medical Simulation, uncredited | Add "Basic assumption © Center for Medical Simulation, as printed in PEARLS (Bajaj 2018)" |
| 2 | LOW | s01 | Paraphrases inside quote marks; "?" on an instruction | “Can you share a short summary of the case?” / “What was managed well, and why?” / “What are some take-aways?” (or drop quote marks) |
| 3 | LOW | s03, caption | Not verbatim | "What aspects were managed well and why? What aspects do you want to change and why?" |
| 4 | LOW | s05 | Example lacks advocacy; screenshot shows epi logged same second as VF | “I saw epinephrine logged at 07:22:21, the same second as the VF and before a shock. I was worried the shock was delayed. What were you weighing at that point?” |
| 5 | LOW | s06 (and AC06 s06) | "Free ACLSMED CPR scores each compressor" overstates | "Free ACLSMED CPR measures each compressor's rate, depth and hands-on time." |
| 6 | LOW | s06 | CODE SUMMARY crop unreadable at feed size | Crop tighter/enlarge or drop |
| 7 | MED | s06, DM | No Pro mention | "33 MegaCodes (Pro) with learning objectives"; DM "open LOG on the Instructor Remote (Pro/Clinical Suite)…" |
| 8 | LOW | s04, caption | Script overstatement | as AC03 #3 |

### AC06_drowning_breaths_first
| # | Sev | Where | Finding | Fix |
|---|---|---|---|---|
| 1 | MED | s01, caption | "Breaths come first" overstates AHA (2024 update: trained rescuers may start with breaths or compressions; only ERC says breaths first) | Title "Drowning arrest: why breaths can't be skipped." (id stays); s03 add "(starting with compressions is also acceptable)" |
| 2 | MED | s05 | Mortality claim not in 2025 Part 10; it's 2024 AHA/AAP update supporting data | "He still has a pulse. The 2024 AHA/AAP drowning update cites lower mortality (44% vs 93%) when breathing support interrupts drowning before CPR is needed." |
| 3 | MED | s06, caption, DM | #13 is Pro | s06 "#13 Drowning MegaCode (Pro) with chart and chest film"; caption "(no. 13, Pro plan)"; DM "load MegaCode #13 (Pro)…" |
| 4 | LOW | s05 step 3 | Compressions not indicated with a pulse | "If he arrests, watch the order: breaths and compressions first, then pads. Check the CPR start in the LOG." |
| 5 | LOW | s06 | Case card clipped at right edge | Fit within 1008 px safe width or crop to title/patient/HR/BP |

Verified correct (ACLSMED): PALS epi 0.01 mg/kg max 1 mg; shocks 2→4→≥4 J/kg max 10 J/kg or adult dose; amio 5 mg/kg or
lido 1 mg/kg; atropine 0.02 mg/kg, min 0.1 mg, max single 0.5 mg, may repeat once; "Start CPR if heart rate is less than
60 per minute"; all arithmetic; brady strip geometry (50/min, PR 0.12, QRS 0.06); every case chart vs simulator.html;
INACSL 2025 Prebriefing; Part 12 RCDP and booster definitions; PEARLS card phrases; 2024 AHA/AAP drowning recommendations;
ERC 2025 five rescue breaths; LOG behaviour (manual §04.12).

App issues found (not in the carousels): `simulator.html` SCENARIOS.pals_brady debrief says "Begin CPR immediately",
teaches 2-finger infant compressions (removed in 2025) and "at least 100/min", cites 2020; MEDS has no weight-based
pediatric entries; pals_vf and bls_drown cite 2020; bls_drown 12-lead text "Sinus Tachycardia 108, J-waves" vs HR 40;
infant age shown as "0.25y".

## CardioLens AI — CL02–CL06

Clinical content held up; three HIGH findings are app claims.

### CL02_afib_vs_mat
| # | Sev | Where | Finding | Fix |
|---|---|---|---|---|
| 1 | HIGH | s05 step 01 | "Strip-based questions" is false: Rhythm Mastery shows text, options and rationale, no strip | "Case-style questions with the reasoning behind each answer." |
| 2 | LOW | s03 footer | 2015 SVT text unreadable here | Add "2023 ACC/AHA/ACCP/HRS AF Guideline" (verified) to the s03 footer |
| 3 | LOW | s03, caption | Other MAT causes omitted | "MAT often comes with lung disease (most often COPD) or another acute illness. The fix starts with the cause." |

### CL03_work_an_ecg_case
| # | Sev | Where | Finding | Fix |
|---|---|---|---|---|
| 1 | HIGH | s05 steps 02–03 | Cases open on the Live Strip tab, with Diagnosis and teaching points shown before the Quiz tab | 02 "Strip + story — Each case opens on a live strip with age, sex and the story. Skip the Diagnosis box; tap Quiz first." 03 "Answer, then review — Feedback on every question, then the diagnosis and teaching points." |
| 2 | MED | DM | Wrong order; reading top-down gives away the diagnosis | "With Pro, open Learn → Clinical Cases, read the strip and the patient story, then tap Quiz before you scroll to the Diagnosis box." |
| 3 | LOW | s05 step 04 | 30 of 33 free questions start from a patient | "Most of Rhythm Mastery's free questions also start from a patient." |
| 4 | LOW | s03 legend | Lateral/anterior groups are teaching conventions | Add "(common teaching groups)" |

### CL04_conduction_system
| # | Sev | Where | Finding | Fix |
|---|---|---|---|---|
| 1 | MED | s04 headline/subhead | "Lower ones only show up as slower escape rhythms" is false (accelerated junctional, AIVR; escape also in AV block) | Headline "If the top fails or is blocked, the next one down takes over." Subhead "Each level has its own built-in rate. The fastest one sets the pace; a lower one takes over as an escape rhythm when the faster one fails or is blocked." |
| 2 | LOW | s04 footer | Merck says junctional 35–50 | "StatPearls: Junctional Rhythm (2026) · Merck Manual Professional: AV block (ventricular escape 20–40/min)" |
| 3 | LOW | s02, caption | Upright P in II is necessary, not sufficient | "Upright P in lead II before every QRS: points to a sinus beat." |
| 4 | LOW | s03 bracket, alt | Bracket measures 0.086 s, labelled 0.08 s | Shorten the bracket to 83 px (0.08 s) or relabel 0.09 s and alt to match |
| 5 | LOW | caption | SA node called a "backup pacemaker" | "Pacemaker rates: SA node 60–100/min; backups: AV junction 40–60/min (narrow QRS), ventricles 20–40/min (wide QRS)." |
| 6 | LOW | s05 | "fibres" vs "fibers" | "Purkinje fibers" |
| 7 | LOW | s01 | "His" tag collides with "LV" | Move the His tag onto the septum or drop LV ~40 px |

### CL05_axis_two_leads
| # | Sev | Where | Finding | Fix |
|---|---|---|---|---|
| 1 | MED | s05 step 02, DM | The app's Axis Finder calls I up + aVF down "Left Axis Deviation" — the shortcut the post warns against | "Set lead I and aVF up or down; it names the quadrant. I up, aVF down? It will say left axis, so check lead II yourself (slide 4)." Same in DM |
| 2 | LOW | s02 | "R taller than the Q or S is deep" contradicts "Compare R with Q + S" | "R taller than Q + S are deep" / "Q + S deeper than the R is tall" |
| 3 | LOW | s06 | Scan screen implies scans report axis | Add "Practise it in Learn. Scans don't report axis." |

### CL06_megacodes_on_phone
| # | Sev | Where | Finding | Fix |
|---|---|---|---|---|
| 1 | HIGH | s05, DM, caption | Post teaches the AHA 2025 loop then says "run the cycle on your phone", but the app's flowcharts/MEGA CODES use non-AHA wording (adrenaline, 4 H's & 4 T's, amiodarone only, TTM) and grade lidocaine as wrong | Reframe s05 so the app is for rhythm recognition + practice, with small print: "The app's flowcharts and MEGA CODES use general ACLS wording (eg, adrenaline, 4 Hs & 4 Ts, amiodarone only) and are not the AHA 2025 algorithm. Check every step against AHA 2025." DM: "Heads-up: the app lists amiodarone only; AHA 2025 accepts amiodarone or lidocaine." |
| 2 | MED | s03, caption | "Next amiodarone 150 mg" can read as every loop | "2nd (last) amiodarone dose 150 mg" / "or lidocaine 0.5–0.75 mg/kg"; caption "Second dose: amiodarone 150 mg (or lidocaine 0.5–0.75 mg/kg)." |
| 3 | MED | s06 | MEGA CODES and flowcharts are Pro, not in the Pro line | "Free download · 3 free scans a month · Rhythm Mastery free · algorithms, MEGA CODES, library & cases with Pro" |
| 4 | LOW | s06 | "Branching" overstated (2 of 7) | "7 scored MEGA CODE scenarios" |
| 5 | LOW | s03 0:00 | Box 1 omitted | "CPR + O2 until pads on → Check: VF/pVT → Shock 1 → CPR 2 min" |
| 6 | LOW | s01 | Check/shock slices inside a ring labelled "2:00 of CPR" | "of CPR, then a pause under 10 s to check" or move the slices out |

Across the series (MED): CL01 s06 says "40+ rhythms"; the apps have 36. CL01 is approved and scheduled, so this needs a
CL01_v2 decision from the RN.

Verified correct (CardioLens): AHA 2025 adult arrest sequence and doses, "typically ≥150/min" / "<50/min" and the five
signs; adult axis −30° to +90° (Part III); junctional 40–60 (StatPearls); MAT/COPD; AF and flutter criteria (2023 AF
guideline); all strip geometry except CL04 s03 QRS; free/Pro gating; 36 library rhythms; 60 cases in 10 series.

App issues found: Rhythm Mastery questions say "this strip" with no strip; Axis Finder's LAD shortcut; Cases show the
Diagnosis before the Quiz; algorithms.json / MEGA CODES ERC-style wording and lidocaine graded wrong; PQRST module
"ST ±0.5 mm — elevation or depression is pathological" overstates.
