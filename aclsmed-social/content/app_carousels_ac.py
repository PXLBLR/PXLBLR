"""ACLSMED Sim app carousels: AC00 (Oct 13, 5 PM extra) and AC02–AC06 (Oct 18–30).

Slides: app_carousels/src/<id>/s0N.dc.html, rendered by app_carousels/render.mjs. Same keys as CL01/AC01.
"""
from content.app_carousels import SIM_DM

DISCLAIMER = ("Educational only, not diagnostic and not a substitute for certified ACLS/PALS training. "
              "Follow AHA 2025 guidelines and your institution's protocols.")

AHA_BRADY = ("AHA 2025 Adult Bradycardia With a Pulse algorithm (epinephrine infusion 2–10 mcg/min, titrate to "
             "response; dopamine infusion 5–20 mcg/kg/min; atropine 1 mg, repeat every 3–5 min, max 3 mg) — "
             "https://cpr.heart.org/-/media/CPR-Files/CPR-Guidelines-Files/2025-Algorithms/Algorithm-ACLS-Bradycardia-250514.pdf "
             "(text of the AHA PDF confirmed via search index; direct download returns 403 from this environment) · "
             "Part 9: Adult Advanced Life Support, Circulation 2025;152(suppl 2), doi:10.1161/CIR.0000000000001376")


def _dm(first_line, pals=False):
    dm = f"{first_line}\n\n{SIM_DM}"
    if pals:  # PALS-topic posts name PALS in the disclaimer; the shared SIM_DM itself stays unchanged
        dm = dm.replace("certified ACLS training", "certified ACLS/PALS training")
    return dm


AC00 = {
    "id": "AC00_drip_math", "app": "ACLSMED Sim", "date": "2026-10-13", "time": "17:00", "keyword": "SIM",
    "caption": f"""Drip math in 3 steps: mcg/min → mL/h. Save this and practise it. 💧

The formula: mL/h = dose (mcg/min) × 60 ÷ concentration (mcg/mL)

1. Bag → mcg/mL. Example bag: epinephrine 4 mg in 250 mL = 4,000 mcg ÷ 250 mL = 16 mcg/mL.
2. Dose per hour. 2 mcg/min × 60 = 120 mcg/h.
3. ÷ concentration. 120 ÷ 16 = 7.5 mL/h.
Check it backwards: 7.5 mL/h × 16 mcg/mL ÷ 60 = 2 mcg/min ✓

Context: in the AHA 2025 adult bradycardia algorithm, if atropine is ineffective, an epinephrine infusion of 2–10 mcg/min (titrated to patient response) is an alternative to transcutaneous pacing.
Read the order's unit first: adult brady epinephrine is mcg/min, so never multiply it by kg.

Weight-based (mcg/kg/min)? Multiply by kg first: mL/h = mcg/kg/min × kg × 60 ÷ mcg/mL. Example: dopamine 5 mcg/kg/min, 80 kg, 1,600 mcg/mL bag = 15 mL/h.

Same dose, different bag: 2 mcg/min from a 4 mcg/mL bag is 30 mL/h. Read the concentration every time.

The concentrations here are examples. Use your institution's standard concentration and smart-pump library, and the independent double-check your policy calls for.

Comment SIM and we'll DM you the link to ACLSMED Sim.

{DISCLAIMER}

#NursingStudent #DripMath #ICUNurse #NurseEducator #ACLS""",
    "alt": ("Six-slide carousel from ACLSMED. Slide 1: 'Drip math in 3 steps' with the formula mL/h = mcg/min × 60 ÷ "
            "mcg/mL and three step cards. Slide 2: step 1, an example bag of epinephrine 4 mg in 250 mL converted to "
            "4,000 mcg and then 16 mcg/mL, labelled as an example concentration. Slide 3: steps 2 and 3, 2 mcg/min "
            "times 60 is 120 mcg/h, divided by 16 is 7.5 mL/h, checked backwards, with the AHA 2025 bradycardia range "
            "of 2 to 10 mcg/min if atropine is ineffective. Slide 4: the weight-based formula with a dopamine example, 5 mcg/kg/min for 80 kg "
            "from a 1,600 mcg/mL bag is 15 mL/h, with a warning never to multiply a mcg/min order by weight. Slide 5: the IVmed pump confirming epinephrine 1 mg/250 mL at "
            "2.00 mcg/min and 30.0 mL/hr, with three steps to try it. Slide 6: comment SIM to get the ACLSMED Sim link."),
    "dm": _dm("Drip math practice: work it by hand first (epinephrine 1 mg in 250 mL: 1,000 ÷ 250 = 4 mcg/mL → "
              "2 × 60 ÷ 4 = 30 mL/h). Then in IVmed (Clinical Suite), Critical Care profile, choose Epinephrine "
              "1 mg/250 mL NS, check Dose 2 mcg/min, Confirm and see if the pump agrees."),
    "sources": [
        AHA_BRADY,
        "Infusion rate arithmetic: mL/h = dose (mcg/min) × 60 ÷ concentration (mcg/mL); weight-based mL/h = "
        "mcg/kg/min × kg × 60 ÷ mcg/mL; 1 mg = 1,000 mcg — standard dimensional analysis, identical to IVmed's own "
        "dose-to-rate code (aclsmed/iv.html commitField() and _polarDoseToRate(): 'mcg/min' → (dose × 60) / conc; "
        "'mcg/kg/min' → (dose × w × 60) / conc). Worked numbers checked: 4,000/250 = 16; 2×60/16 = 7.5; "
        "7.5×16/60 = 2; 1,000/250 = 4; 120/4 = 30; 400,000/250 = 1,600; 5×80×60/1,600 = 15.",
        "Example concentrations are labelled as examples on every slide (4 mg/250 mL epinephrine; 400 mg/250 mL "
        "dopamine); institution's standard concentration + smart-pump library + independent double-check per policy.",
        "App: IVmed drug library entry 'Epinephrine 1mg/250mL NS' (conc 4 mcg/mL, default dose 2 mcg/min, rate "
        "30 mL/hr, soft max 10 / hard max 20 mcg/min) and 'Dopamine 400mg/250mL D5W' (1,600 mcg/mL) — "
        "aclsmed/iv.html lines ~1956–1968; pump computes rate from dose + concentration (commitField); dose "
        "guardrails SOFT/HARD LIMIT and Program Line → Confirm → read-back — aclsmed/manual.html § 05.05–05.06; "
        "IVmed is a Clinical Suite role — manual § 01.06 / § 02.03.",
        "Screenshot: app_carousels/assets/ac_ivmed_epi.jpg and ac_ivmed_epi_lcd.jpg are captures of the real IVmed "
        "pump (aclsmed/iv.html, 'pro' face, which matches the tablet figures in images/manual/fig-ivmed-*.jpg) "
        "driven to Confirm Line A: Epinephrine 1mg/250mL NS · Rate 30.0 mL/hr · Dose 2.00 mcg/min · VTBI 250 mL.",
    ],
}

PALS_CA = ("AHA 2025 PALS Pediatric Cardiac Arrest Algorithm (epinephrine 0.01 mg/kg IV/IO every 3–5 min, max 1 mg; "
           "shocks 2 J/kg, then 4 J/kg, then ≥4 J/kg up to 10 J/kg or adult dose; amiodarone 5 mg/kg bolus or lidocaine "
           "1 mg/kg) — https://cpr.heart.org/-/media/CPR-Files/CPR-Guidelines-Files/2025-Algorithms/Algorithm-PALS-CA-250123.pdf "
           "(PDF text confirmed via search index; direct download 403 here) · Part 8: Pediatric Advanced Life Support, "
           "Circulation 2025;152(suppl 2):S479–S537, doi:10.1161/CIR.0000000000001368 · epinephrine 0.01 mg/kg = 0.1 mL/kg "
           "of 0.1 mg/mL, max 1 mg, every 3–5 min also in Lee JE et al., Anesth Pain Med 2026 review of the 2025 guidelines, "
           "doi:10.17085/apm.26581")
PALS_BRADY = ("AHA 2025 PALS Pediatric Bradycardia With a Pulse Algorithm, accessible text (Box 2 compromise = acutely "
              "altered mental status, signs of shock, hypotension; Box 3 airway/oxygen/PPV as necessary/monitor; Box 4 "
              "persists with compromise?; Box 5 'Start CPR if heart rate is less than 60 per minute', IV/IO, epinephrine, "
              "atropine for increased vagal tone or primary AV block; Box 7 pulse check every 2 min; Box 8 to arrest "
              "algorithm; epinephrine 0.01 mg/kg (0.1 mg/mL, max 1 mg); atropine 0.02 mg/kg, may repeat once, min 0.1 mg, "
              "max single 0.5 mg; causes incl. hypoxia) — https://cpr.heart.org/-/media/CPR-Files/CPR-Guidelines-Files/"
              "2025-Accessible/Algorithm-PALS-Bradycardia-LngDscrp-250729-Ed.pdf (read in full)")
PART12 = ("AHA 2025 Part 12: Resuscitation Education Science (scripted debriefing helps instructors guide discussion and "
          "consistency; rapid-cycle deliberate practice; spaced learning and booster training defined) — Donoghue AJ et al., "
          "Circulation 2025;152(suppl 2):S719–S750, doi:10.1161/CIR.0000000000001374 (top-10 messages via LearningRQI summary "
          "and PAAD review quoting the text; full text 403 here)")
PEARLS = ("PEARLS Healthcare Debriefing Tool, Bajaj K, Meguerdichian M, Thoma B, Huang S, Eppich W, Cheng A. Acad Med "
          "2018;93(2):336 (phases setting the scene, reactions, description, analysis, application/summary; sample phrases "
          "quoted verbatim) — https://debrief2learn.org/wp-content/uploads/2017/12/PEARLS-Pocket-Card-5.8x7.2-PDF-EN.pdf · "
          "Eppich W, Cheng A. PEARLS: development and rationale for a blended approach to debriefing. Simul Healthc "
          "2015;10(2):106–115, doi:10.1097/SIH.0000000000000072")
DROWN = ("AHA 2025 Part 10: Adult and Pediatric Special Circumstances of Resuscitation (drowning section incorporates the "
         "2024 AHA/AAP focused update) — Circulation 2025, doi:10.1161/CIR.0000000000001380; 2024 AHA/AAP Focused Update on "
         "Special Circumstances: Resuscitation Following Drowning, Circulation 2024;150:e501–e516, "
         "doi:10.1161/CIR.0000000000001274 (CPR with rescue breaths and compressions; trained rescuers may start with breaths "
         "then compressions; compressions alone reasonable if unwilling/untrained/unable; breaths by first means available; "
         "oxygen when available — arrest generally the result of severe hypoxemia; CPR with breaths before AED application, "
         "don't delay CPR for an AED, AED use reasonable; in-water breathing by trained rescuers if safe; lower mortality when "
         "breaths interrupt drowning before arrest). Recommendation list checked against Contemporary Pediatrics summary "
         "https://www.contemporarypediatrics.com/view/aap-aha-updates-guidance-for-resuscitation-following-drowning; full text 403 here")

AC02 = {
    "id": "AC02_pals_doses_weight", "app": "ACLSMED Sim", "date": "2026-10-18", "time": "12:00", "keyword": "SIM",
    "caption": f"""Kids aren't small adults. Every PALS dose starts with one number: the weight. 👶

Worked for a 20 kg child (example):
• Epinephrine (arrest): 0.01 mg/kg IV/IO, max 1 mg → 0.2 mg (2 mL of 0.1 mg/mL), every 3–5 min
• Shocks for VF/pVT: 2 J/kg → 40 J, then 4 J/kg → 80 J, then ≥4 J/kg up to 10 J/kg or the adult dose
• Amiodarone (refractory VF/pVT): 5 mg/kg IV/IO bolus (max 300 mg) → 100 mg (or lidocaine 1 mg/kg → 20 mg)
• Adenosine (SVT): 0.1 mg/kg (max 6 mg) → 2 mg, then 0.2 mg/kg (max 12 mg) → 4 mg

No scale in the room? Use a length-based tape or your unit's weight-based dosing reference. Never guess, and never default to an adult dose.

Practice it: ACLSMED Sim's pediatric MegaCodes (Pro plan) put the weight on the chart. The MEDS list shows adult doses, so say the weight-based dose out loud. Comment SIM and we'll DM you the link to ACLSMED Sim.

{DISCLAIMER}

#PALS #PediatricNursing #PedsNurse #NurseEducator #NursingStudent""",
    "alt": ("Six-slide carousel from ACLSMED. Slide 1: 'Kids aren't small adults' with a 20 kg badge and four doses for a "
            "20 kg child: epinephrine 0.2 mg, first shock 40 J, amiodarone 100 mg, adenosine 2 mg. Slide 2: epinephrine "
            "0.01 mg/kg, never more than 1 mg, worked as 0.2 mg or 2 mL of 0.1 mg/mL. Slide 3: shock energy climbing as bars "
            "from 2 J/kg to 4 J/kg to at least 4 J/kg, plus amiodarone 5 mg/kg (max 300 mg) = 100 mg. Slide 4: adenosine "
            "first dose 0.1 mg/kg max 6 mg and second dose 0.2 mg/kg max 12 mg, with a length-based tape reminder and a "
            "warning never to default to an adult dose. Slide 5: the ACLSMED Sim chart (web simulator) for the pediatric SVT "
            "MegaCode, a 6-year-old weighing 21 kg, with three practice steps and a note that MEDS lists adult doses. Slide "
            "6: four PALS/neonatal MegaCodes on the Pro plan, and comment SIM to get the ACLSMED Sim link."),
    "dm": _dm("PALS dose practice: load MegaCode #16 Pediatric SVT (Pro plan; 21 kg on the chart) and work the adenosine "
              "before the team calls it: 2.1 mg, then 4.2 mg. Then try #14 Pediatric VF (45 kg): first shock 90 J. MEDS "
              "lists adult doses, so say the weight-based dose out loud.", pals=True),
    "sources": [
        PALS_CA + " · amiodarone 5 mg/kg bolus, max 300 mg (PALS algorithm text)",
        "AHA 2025 PALS Pediatric Tachyarrhythmia With a Pulse Algorithm (adenosine 0.1 mg/kg rapid bolus, max 6 mg; "
        "second dose 0.2 mg/kg rapid bolus, max 12 mg). Checked against the 2020 AHA text "
        "https://cpr.heart.org/-/media/CPR-Files/CPR-Guidelines-Files/Algorithms/Text-Descriptions/"
        "AlgorithmPALS_Tachycardia_LngDscrp_200702_Ed.pdf and 2025 secondary summaries only. RN TO CONFIRM the second "
        "dose, 0.2 mg/kg (max 12 mg), in the 2025 PDF (audit AC02 #3). Adult 6 mg / 12 mg per AHA 2025 Adult "
        "Tachyarrhythmia algorithm.",
        "Length-based tape / weight-based reference: practice tip, not attributed to AHA on the slide.",
        "Arithmetic checked: 20×0.01=0.2 mg (=2 mL of 0.1 mg/mL); 100×0.01=1 mg cap; 20×2=40 J; 20×4=80 J; 20×5=100 mg; "
        "20×1=20 mg; 20×0.1=2 mg; 20×0.2=4 mg; 60×0.1=6 mg and 60×0.2=12 mg (caps reached at 60 kg); 21×0.1=2.1; "
        "21×0.2=4.2; 45×2=90 J.",
        "App: PALS/Neonatal MegaCodes #14 Pediatric VF (12 y, 45 kg), #15 Infant bradycardia (5.2 kg), #16 Pediatric SVT "
        "(6 y, 21 kg), #17 NRP (3.2 kg) — aclsmed/simulator.html SCENARIOS.pals_vf/pals_brady/pals_svt/nrp_resus and "
        "manual.html § 04.15 + Appendix A; MEDS tap time-stamps the drug but lists fixed adult doses — manual § 04.09 "
        "and audit cross-cutting (b); rhythm never converts by itself — manual § 04.16; non-free scenarios need Pro "
        "(simulator.html showCase(): free tier = MegaCode #09 only).",
        "Screenshot: app_carousels/assets/ac_case_peds_svt.jpg — real ACLSMED Sim (web simulator, simulator.html) "
        "MegaCode chart for Pediatric SVT: Sophia Alvarez, 6y F, 21 kg; HR 248, BP 82/50, SpO2 97%. Footer says "
        "'(web simulator)'.",
    ],
}

AC03 = {
    "id": "AC03_mock_code_15min", "app": "ACLSMED Sim", "date": "2026-10-21", "time": "12:00", "keyword": "SIM",
    "caption": f"""Plan a 15-minute mock code. Brief, run, debrief. ⏱️

0–3 min BRIEF: 2–3 observable objectives (e.g. leader assigns every role out loud; closed-loop communication on every drug order). Assign real roles: leader, compressors, airway, meds/IV, recorder. Ground rules: expectations, psychological safety, confidentiality, the fiction contract, a quick tour of the monitor.
3–9 min RUN: run it straight. You change the patient: slide pressure and SpO₂ down without a word, give data only when asked, change the rhythm at a planned moment. New team or new skill? Try rapid-cycle deliberate practice: pause at set points, feedback, rerun.
9–15 min DEBRIEF: use a script (reactions, description, analysis, take-aways). AHA 2025: a debriefing script can help instructors guide the discussion and keep debriefs consistent.
Then make it a series: spaced learning and booster training.

The suggested split is a starting point, not a standard. In ACLSMED Sim, the 33 MegaCodes and the Instructor Remote are on the Pro plan. Comment SIM and we'll DM you the link to ACLSMED Sim.

{DISCLAIMER}

#Simulation #NurseEducator #MockCode #SimLab #ACLS""",
    "alt": ("Six-slide carousel from ACLSMED. Slide 1: 'Plan a 15-minute mock code' with a timeline split into brief 0 to "
            "3 minutes, run 3 to 9 and debrief 9 to 15. Slide 2: the brief, with three example objectives, five role "
            "chips and the ground rules. Slide 3: the run, with three educator moves from the ACLSMED Instructor Manual "
            "and rapid-cycle deliberate practice as an option. Slide 4: the debrief, with four PEARLS phases ending on "
            "'What will you take to practice?', why a script can help, and spaced learning. Slide 5: the ACLSMED "
            "Instructor Remote with a V-Fib rhythm armed to fire on the next shock, and three steps for brief, run and "
            "debrief. Slide 6: 33 MegaCodes on the Pro plan, and comment SIM to get the ACLSMED Sim link."),
    "dm": _dm("15-minute mock code: on the Instructor Remote (Pro or Clinical Suite) open CODES, load a case and play the "
              "handoff (brief), select a rhythm and tap TRIGGER so it fires on the team's next shock (run), then open "
              "LOG for the debrief."),
    "sources": [
        "INACSL Healthcare Simulation Standard of Best Practice: Prebriefing — Preparation and Briefing (2025 revision), "
        "Clin Simul Nurs 2025;105:101777, doi:10.1016/j.ecns.2025.101777 (briefing: expectations, role clarification, "
        "ground rules, psychological and physical safety, confidentiality, fiction contract; structured orientation to "
        "environment and modality; review learning objectives)",
        PART12 + " — s03 footer credits RCDP only to Part 12; s04 says a script 'can help'",
        "PEARLS phases on s04 — " + PEARLS,
        "Roles (leader, compressor, airway, drugs, recorder) and 'run straight through, then debrief' — ACLSMED Instructor "
        "Manual § 08.03 Full mock code & the debrief; educator moves (slide pressure/saturation, data only when asked, "
        "planned rhythm change) — manual § 04.14 and § 04.17 five-beat code, credited on the s03 footer as 'Educator "
        "moves: ACLSMED Instructor Manual'. The 3/6/6-minute split (0–3 / 3–9 / 9–15) is our suggestion and is "
        "labelled 'suggested split' on the slide.",
        "App: CODES → load case, ▶ EMS handoff, START SCENARIO (manual § 04.08); vitals sliders (§ 04.04); QUEUE/TRIGGER/"
        "PLAY, nothing auto-plays (§ 04.06–04.07); LOG time-stamped, cleared by Reset/power-off (§ 04.12); Instructor role "
        "on Pro and Clinical Suite (§ 01.06); 33 MegaCodes with learning objectives (§ 04.15), Pro (simulator.html "
        "showCase()).",
        "Screenshot: app_carousels/assets/ac_remote_armed.jpg — crop of aclsmed/images/manual/fig-remote-queued.jpg "
        "(iPad Instructor Remote, RHYTHMS tab, bar reading 'ARMED · awaiting shock — V-Fib — Coarse' with CLEAR / DISARM / "
        "PLAY NOW). s06 reuses ac_remote.jpg (Remote driving Monitor).",
    ],
}

AC04 = {
    "id": "AC04_infant_brady_cpr", "app": "ACLSMED Sim", "date": "2026-10-24", "time": "12:00", "keyword": "SIM",
    "caption": f"""Infant brady under 60: when to start CPR. 👶🫀

Not when the heart stops. Per the AHA 2025 Pediatric Bradycardia With a Pulse algorithm:
1. Cardiopulmonary compromise? Acutely altered mental status, signs of shock, hypotension.
2. Support first: patent airway and oxygen, positive-pressure ventilation as needed, cardiorespiratory monitor, monitor the pulse.
3. Bradycardia still there with compromise? Start CPR if the heart rate is under 60/min. Then IV/IO access, epinephrine, and atropine for increased vagal tone or primary AV block.
4. Pulse check every 2 minutes. No pulse → Pediatric Cardiac Arrest Algorithm.

Doses: epinephrine 0.01 mg/kg IV/IO (0.1 mg/mL, max 1 mg). Atropine 0.02 mg/kg, may repeat once, minimum 0.1 mg, max single dose 0.5 mg.
Worked for 5.2 kg (example): epinephrine 0.052 mg = 0.52 mL; atropine 0.104 mg.

Practice it with the Infant Symptomatic Bradycardia MegaCode (no. 15, Pro plan); say the mg/kg dose aloud, because the MEDS list shows adult doses. Comment SIM and we'll DM you the link to ACLSMED Sim.

{DISCLAIMER}

#PALS #PedsNurse #PediatricNursing #PICU #NurseEducator""",
    "alt": ("Six-slide carousel from ACLSMED. Slide 1: 'Infant brady under 60: when to start CPR' over a synthetic sinus "
            "bradycardia strip at 50 per minute, R to R of 6 big boxes: start CPR when the rate stays under 60 with "
            "cardiopulmonary compromise after airway and breathing support. Slide 2: the three signs of cardiopulmonary "
            "compromise, what to do for yes and no, and why hypoxia in children puts airway and breathing first. Slide 3: "
            "a flow from airway, oxygen and ventilation support, to asking again, to starting CPR if the heart rate stays "
            "under 60 per minute; pacing omitted. Slide 4: epinephrine 0.01 mg/kg and atropine 0.02 mg/kg with their "
            "limits, worked for a 5.2 kg infant. Slide 5: the ACLSMED Sim chart for the infant symptomatic bradycardia "
            "MegaCode, 5.2 kg, HR 48, with three practice steps and a note to say the mg/kg dose aloud because MEDS lists "
            "adult doses. Slide 6: the infant brady MegaCode on the Pro plan, and comment SIM to get the ACLSMED Sim link."),
    "dm": _dm("Infant brady practice: load MegaCode #15 (Pro) Infant Symptomatic Bradycardia (5.2 kg, HR 48) and hold "
              "the HR slider at 48 while the team supports the airway. Who calls for compressions? MEDS lists adult "
              "doses, so have them say the mg/kg dose aloud.", pals=True),
    "sources": [
        PALS_BRADY,
        "ECG strip on s01/s06 is synthetic, drawn at 25 mm/s (small box 0.04 s, big box 0.20 s): sinus rhythm at 50/min, "
        "R–R 6 big boxes = 1.2 s (300 ÷ 6 = 50), P before every QRS, PR 0.12 s, QRS 0.06 s.",
        "Arithmetic: 5.2×0.01 = 0.052 mg; 0.052 mg ÷ 0.1 mg/mL = 0.52 mL; 5.2×0.02 = 0.104 mg (above the 0.1 mg minimum).",
        "Deliberately left out: pacing (Box 6; s03 footer says 'Algorithm boxes 3–5, 7–8 (pacing omitted)') — already "
        "posted; repeat interval for epinephrine in this algorithm (not stated in the bradycardia text).",
        "App: MegaCode #15 Infant Symptomatic Bradycardia (Baby Lily Chen, 3 months, 5.2 kg, HR 48, BP 50/28, SpO2 68%, "
        "RR 8) — aclsmed/simulator.html SCENARIOS.pals_brady; manual Appendix A #15; HR slider on the Remote — manual "
        "§ 04.04; MEDS logs fixed adult doses (audit cross-cutting (b)); Pro needed for non-free cases (simulator.html "
        "showCase()).",
        "Screenshot: app_carousels/assets/ac_case_infant_brady.jpg — real ACLSMED Sim (web simulator) MegaCode chart: "
        "title, patient line and initial vital signs.",
    ],
}

AC05 = {
    "id": "AC05_debrief_5_questions", "app": "ACLSMED Sim", "date": "2026-10-27", "time": "12:00", "keyword": "SIM",
    "caption": f"""Debrief like a pro: 5 questions. 🗣️ (PEARLS framework)

Set the scene: "Let's spend X minutes debriefing. Our goal is to improve how we work together and care for our patients."
1. Reactions: "How are you feeling?"
2. Description: "Can you please share a short summary of the case?"
3. Analysis, self-assessment: "What aspects were managed well and why? What aspects do you want to change and why?"
4. Analysis, advocacy + inquiry: "I saw [observation], I think [your view]. How do you see it?"
5. Application/summary: "What are some take-aways from this discussion for our clinical practice?"

AHA 2025 education science: a debriefing script can help instructors guide the discussion and keep debriefs consistent. And say the basic assumption out loud: "Everyone here is intelligent and wants to improve." (Basic assumption © Center for Medical Simulation, as printed in PEARLS (Bajaj 2018).)

ACLSMED Sim's LOG (Instructor Remote, Pro/Clinical Suite) time-stamps every rhythm, shock and drug, so the description phase starts from facts. Comment SIM and we'll DM you the link to ACLSMED Sim.

{DISCLAIMER}

#Debriefing #Simulation #NurseEducator #SimLab #HealthcareSimulation""",
    "alt": ("Six-slide carousel from ACLSMED. Slide 1: 'Debrief like a pro: 5 questions' listing reactions, description, "
            "two analysis questions and take-aways. Slide 2: setting the scene, then speech bubbles for 'How are you "
            "feeling?' and 'Can you please share a short summary of the case?'. Slide 3: two analysis bubbles, the "
            "verbatim self-assessment question and advocacy plus inquiry, with an example. Slide 4: the take-aways "
            "question, why a script can help, the basic assumption credited to the Center for Medical Simulation, and the "
            "PEARLS order. Slide 5: the ACLSMED Instructor Remote LOG tab with time-stamped events, three steps to debrief "
            "from data, and an advocacy-inquiry example about epinephrine logged before a shock. Slide 6: the five PEARLS "
            "steps, 33 MegaCodes on the Pro plan, and comment SIM to get the ACLSMED Sim link."),
    "dm": _dm("Debrief from data: open LOG on the Instructor Remote (Pro/Clinical Suite) the moment you call the code, "
              "let the team rebuild the timeline, then check it against the log. Screenshot it before you reset."),
    "sources": [
        PEARLS,
        PART12 + " — worded 'can help' (weak recommendation)",
        "'Basic assumption' wording is © Center for Medical Simulation, as printed on the PEARLS card (used with "
        "permission there); credited on s04 and in the caption.",
        "App: LOG tab = the Monitor's CODE SUMMARY — every rhythm change, shock with energy and mode, drug, CPR start/stop "
        "with duration and AED cycle, stamped HH:mm:ss; cleared by Reset Scenario and Monitor power-off — manual § 04.12 "
        "and § 03.16; debrief from Code Summary, CPR board and recorder — manual § 08.03; Remote is Pro & Clinical "
        "Suite (§ 01.06). ACLSMED CPR measures rate, depth and hands-on time (manual § 07.01).",
        "Screenshot: app_carousels/assets/ac_remote_log.jpg — crop of aclsmed/images/manual/fig-remote-log.jpg (iPad "
        "Remote LOG: Epinephrine 1 mg IV/IO, CPR Started, V-Fib — Coarse, each 07:22:21). The unreadable CODE SUMMARY "
        "crop was dropped from s06 (audit #6) and replaced by the five PEARLS steps.",
    ],
}

AC06 = {
    "id": "AC06_drowning_breaths_first", "app": "ACLSMED Sim", "date": "2026-10-30", "time": "12:00", "keyword": "SIM",
    "caption": f"""Drowning arrest: why breaths can't be skipped. 🌊

It's a hypoxic arrest. AHA 2025: cardiac arrest after drowning is generally the result of severe hypoxemia, so oxygen is recommended when available.

What AHA 2025 says for drowning:
• CPR with rescue breaths AND chest compressions.
• Trained rescuers may start with rescue breaths, then compressions (starting with compressions is also acceptable).
• Give breaths by the first means available: mouth-to-mouth, pocket mask or bag-mask.
• Unwilling, untrained or unable to give breaths? Compressions alone are reasonable until help arrives.
• Start CPR with rescue breaths before applying the AED. Don't delay CPR to get one. Using an AED is reasonable.
• Trained rescuers may give in-water rescue breaths to an unresponsive victim if it's safe for them.

ERC 2025 (European guideline): unresponsive and not breathing after rescue from drowning → 5 rescue breaths, then standard CPR.

Practice it with the Submersion / Drowning MegaCode (no. 13, Pro plan). Comment SIM and we'll DM you the link to ACLSMED Sim.

{DISCLAIMER}

#BLS #Drowning #CPR #NurseEducator #Lifeguard""",
    "alt": ("Six-slide carousel from ACLSMED. Slide 1: 'Drowning arrest: why breaths can't be skipped' with a chain from "
            "under water to severe hypoxemia to a slowing heart to arrest. Slide 2: compressions move blood, breaths "
            "bring the oxygen, comparing sudden cardiac arrest with drowning arrest. Slide 3: five AHA points on rescue "
            "breaths, starting with breaths as an option (starting with compressions also acceptable), the first means "
            "available, oxygen, and compressions alone if breaths can't be given. Slide 4: breaths and compressions "
            "before the AED pads, with the ERC 2025 five rescue breaths and in-water breathing. Slide 5: the ACLSMED Sim "
            "drowning MegaCode chart, a 17-year-old at 68 kg with HR 40 and RR 0, three practice steps, and the 2024 "
            "AHA/AAP update's 44% versus 93% mortality figure. Slide 6: the drowning MegaCode header on the Pro plan, and "
            "comment SIM to get the ACLSMED Sim link."),
    "dm": _dm("Drowning practice: load MegaCode #13 (Pro) Submersion / Drowning. He opens not breathing with a weak pulse "
              "at 40. If the team ventilates well, lift SpO2 and HR on the Remote; if not, change to an arrest rhythm "
              "and watch whether breaths and compressions come before the pads.", pals=True),
    "sources": [
        DROWN + " · 44% vs 93% mortality figure is from the 2024 AHA/AAP drowning update's supporting text (quoted as "
        "'The 2024 AHA/AAP drowning update cites…' on s05).",
        "ERC Guidelines 2025 (European Resuscitation Council), plain-language guideline book, Drowning section: 'If "
        "following rescue from drowning the person is unresponsive and not breathing, promptly deliver 5 rescue breaths "
        "and then start standard CPR with chest compressions'; 'With the lack of oxygen, the heart slows down and finally "
        "stops' — https://www.erc.edu/media/p5ymaeej/gl2025_layperson_book_ipdf-v11-e.pdf · full chapter: ERC Guidelines "
        "2025 Special Circumstances in Resuscitation, Resuscitation 2025;215, doi:10.1016/j.resuscitation.2025.110753 "
        "(not retrievable here).",
        "Slide 2 SCA vs drowning comparison is labelled 'physiology simplified' (oxygen content still adequate early in "
        "sudden VF arrest vs already depleted in asphyxial arrest).",
        "Deliberately left out: hypothermia and cervical-spine guidance (not verifiable in the 2025 text from here).",
        "App: MegaCode #13 Submersion / Drowning — Rescue Breathing (17 y M, 68 kg, HR 40, BP 60/30, SpO2 48%, EtCO2 15, "
        "temp 35 °C, RR 0; opens as respiratory arrest with a pulse; chest X-ray) — aclsmed/simulator.html SCENARIOS."
        "bls_drown, manual Appendix A #13; sliders and rhythm change — manual § 04.04/§ 04.14; CPR start logged — § 03.14/"
        "§ 04.12; Pro needed (simulator.html showCase()). ACLSMED CPR measures rate, depth and hands-on time (§ 07.01).",
        "Screenshots: app_carousels/assets/ac_case_drowning.jpg (s05) — real ACLSMED Sim (web simulator) MegaCode chart: "
        "title, patient line and initial vital signs; ac_case_drowning_title.jpg (s06) — crop of the same chart, title "
        "and patient line only, fitted inside the 1008 px safe width.",
    ],
}

AC_CAROUSELS = [AC00, AC02, AC03, AC04, AC05, AC06]
