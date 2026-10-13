"""CardioLens AI app carousels CL02–CL06 (Oct 17–29, 12:00 PM ET). Keyword LENS.

Slides: app_carousels/src/<id>/s0N.dc.html, rendered by app_carousels/render.mjs. Same keys as CL01.
Every strip and diagram on the slides is synthetic (drawn as SVG). App claims were checked against the
CardioLens repo (/home/user/cardiolens: iOS + AndroidAPK) and cardiolens-website; paths are in each sources list.
"""
from content.app_carousels import CARDIOLENS_ANDROID, CARDIOLENS_IOS, UDMI

DISCLAIMER = "Educational only, not a diagnostic tool. Never upload a strip with patient identifiers."

# ---- shared clinical sources
AHA_CA = ("AHA 2025 Adult Cardiac Arrest Algorithm (CPR 2 min between rhythm checks; shock → CPR 2 min; IV/IO access; "
          "epinephrine IV/IO 1 mg every 3–5 min, ASAP for asystole/PEA; amiodarone IV/IO 300 mg bolus then 150 mg, or "
          "lidocaine 1–1.5 mg/kg then 0.5–0.75 mg/kg; consider advanced airway, capnography; treat reversible causes; "
          "change compressor every 2 min) — https://cpr.heart.org/-/media/CPR-Files/CPR-Guidelines-Files/2025-Algorithms/Algorithm-ACLS-CA-250527.pdf "
          "and Adult Cardiac Arrest Circular Algorithm (amiodarone or lidocaine for refractory VF/pVT) — "
          "https://cpr.heart.org/-/media/CPR-Files/CPR-Guidelines-Files/2025-Algorithms/Algorithm-ACLS-CA-Circular-250620.pdf "
          "(cpr.heart.org returns 403 to this environment; text verified word for word from the © 2025 AHA algorithm set "
          "reproduced at cprschoolhouse.com/resources/acls/acls_algorithms.pdf)")
AHA_PART9 = ("Part 9: Adult Advanced Life Support, 2025 AHA Guidelines for CPR and ECC, Circulation 2025 — "
             "https://doi.org/10.1161/CIR.0000000000001376")
AHA_TACHY = ("AHA 2025 Adult Tachyarrhythmia With a Pulse Algorithm (persistent tachyarrhythmia causing hypotension, acutely "
             "altered mental status, signs of shock, ischemic chest discomfort or acute heart failure; heart rate typically "
             "≥150/min if tachyarrhythmia) — https://cpr.heart.org/-/media/CPR-Files/CPR-Guidelines-Files/2025-Algorithms/Algorithm-ACLS-Tachycardia-250514.pdf")
AHA_BRADY = ("AHA 2025 Adult Bradycardia With a Pulse Algorithm (same five signs of cardiopulmonary compromise; heart rate "
             "typically <50/min if bradyarrhythmia) — https://cpr.heart.org/-/media/CPR-Files/CPR-Guidelines-Files/2025-Algorithms/Algorithm-ACLS-Bradycardia-250514.pdf "
             "(algorithm text verified from the same © 2025 AHA set as above)")
STD_I = ("AHA/ACCF/HRS Recommendations for the Standardization and Interpretation of the ECG, Part I (Kligfield 2007): "
         "25 mm/s paper, 0.04 s / 0.20 s boxes; P, PR, QRS definitions; normal PR 0.12–0.20 s — "
         "https://www.ahajournals.org/doi/10.1161/CIRCULATIONAHA.106.180200")
STD_III = ("AHA/ACCF/HRS ECG standardization Part III: Intraventricular Conduction Disturbances (Surawicz 2009): QRS ≥120 ms "
           "for bundle branch block; adult frontal-plane QRS axis normal −30° to +90°, left axis deviation −30° and beyond "
           "(−30° to −90°), right axis deviation +90° to +180° — https://www.ahajournals.org/doi/10.1161/CIRCULATIONAHA.108.191095 "
           "(axis figures confirmed through excerpts quoting the statement; the full text returns 403 here)")
APP_COUNTS = ("CardioLens repo: 288 quiz questions = 36 rhythms × 8 (iOS/CardioLens/Resources/quiz_bank_v1.json); 60 cases in "
              "10 series (Resources/cases.json); 36 ECG Library entries (Models/ECGRhythmLibrary.swift, Android "
              "core/data/ECGRhythmLibrary.kt); 3 free scans a month (Services/CreditManager.swift monthlyCreditsTotal "
              "isProUser ? 50 : 3); full library, quiz and cases need Pro")

CL02 = {
    "id": "CL02_afib_vs_mat", "app": "CardioLens AI", "date": "2026-10-17", "time": "12:00", "keyword": "LENS",
    "caption": f""""Irregular" isn't one rhythm. AFib, MAT and flutter with variable block can all look messy. The P waves tell them apart. 🫀

AFib: no distinct P waves, a wavy (fibrillatory) baseline, R-R intervals irregular with no pattern.
MAT: the P waves ARE there, in 3 or more different shapes in the same lead, rate over 100, flat baseline between them. MAT often comes with lung disease (most often COPD) or another acute illness. The fix starts with the cause.
Flutter with variable block: sawtooth flutter waves (best seen in II, III, aVF). The AV node lets through every 2nd, 3rd or 4th wave, so the R-R jumps around.

Comment LENS and we'll DM you the link to CardioLens AI.

{DISCLAIMER} Every strip shown is synthetic.

#ECG #EKG #AFib #Telemetry #CardiacNurse""",
    "alt": ("Six-slide carousel from CardioLens AI. "
            "Slide 1: the headline 'Irregular isn't one rhythm' above three synthetic lead II strips: AFib with no P waves "
            "and a wavy baseline, MAT with P waves of different shapes, and atrial flutter with a sawtooth baseline. "
            "Slide 2: an AFib strip with R-R intervals of 0.58, 0.47, 0.80, 0.54 and 0.68 seconds and the fibrillatory "
            "baseline circled, with the three ECG features of AF. "
            "Slide 3: a MAT strip with five different P-wave shapes boxed and lettered A to E, the criteria (3 or more P "
            "shapes, rate over 100, flat baseline) and the link to lung disease or another acute illness. "
            "Slide 4: a flutter strip with 2:1, 4:1 and 3:1 conduction marked, and a table comparing P waves, baseline "
            "and clues for AFib, MAT and flutter. "
            "Slide 5: the CardioLens Rhythm Mastery screen with Atrial Fibrillation and Atrial Flutter in the free "
            "survival rhythms, and three steps marked free or Pro. "
            "Slide 6: an ECG Library rhythm screen and 'Comment LENS' to get the download link."),
    "dm": f"""Here's CardioLens AI 👉 {CARDIOLENS_IOS}
Android: {CARDIOLENS_ANDROID}

First thing to try: Learn → Rhythm Mastery → Atrial Fibrillation, then Atrial Flutter (3 free questions on each). With Pro, open ECG Library → MAT and compare its P waves with AFib.

Educational only, not a diagnostic tool.""",
    "sources": [
        "2023 ACC/AHA/ACCP/HRS Guideline for the Diagnosis and Management of Atrial Fibrillation (Joglar et al., "
        "Circulation 2024;149:e1–e156): Table 4, AF ECG characteristics = irregular R-R intervals (when AV conduction is "
        "present), absence of distinct P waves, irregular atrial activity (fibrillatory waves); §2.2.2, in multifocal AT "
        "the P-wave morphology varies, typical flutter = sawtooth flutter waves in the inferior leads; SOS framework "
        "(stroke-risk assessment) — https://doi.org/10.1161/CIR.0000000000001193 (full text read via PMC11095842)",
        "2015 ACC/AHA/HRS Guideline for the Management of Adult Patients With SVT (Page et al., Circulation "
        "2016;133:e506–e574): MAT = irregular SVT with ≥3 distinct P-wave morphologies — "
        "https://doi.org/10.1161/CIR.0000000000000311 (publisher full text returns 403 here; definition cross-checked "
        "against StatPearls below)",
        "StatPearls: Multifocal Atrial Tachycardia (Custer, Yelamanchili, Lappin; 2023), PMID 29083603: rate >100, "
        "≥3 different non-sinus P-wave morphologies in the same lead, irregular P-P, isoelectric baseline between P "
        "waves, most commonly with COPD, typically in elderly/acutely ill patients, treatment is mainly of the underlying condition — "
        "https://www.ncbi.nlm.nih.gov/books/NBK459152/",
        "6-second method (count QRS in 6 s × 10) — as approved in CL01; AHA/ACCF/HRS standardization Part I — "
        "https://www.ahajournals.org/doi/10.1161/CIRCULATIONAHA.106.180200",
        "App: Rhythm Mastery 'survival' tier is free and includes atrial_fibrillation and atrial_flutter "
        "(iOS Resources/quiz_bank_v1.json tiers); free users get 3 non-Pro questions per survival rhythm, Pro all 8 "
        "(iOS Services/QuizManager.swift getQuestionsFor; Android core/data/QuizManager.kt). MAT is an ECG Library entry "
        "(ECGRhythmLibrary.swift id 'mat', with 3+ P morphologies, varying PR, COPD association); library free set is "
        "only nsr/sa/st/sb, so MAT is Pro (Tabs/ECGLibrary/ECGLibraryView.swift freeRhythmIDs; Android "
        "feature/library/EcgLibraryScreen.kt). s05 screenshot cardiolens-website/public/screens/ss4-quiz.png "
        "(Rhythm Mastery, SURVIVAL RHYTHMS · FREE, AFib and Atrial Flutter visible); s06 ss2-library.png (NSR detail, "
        "parent-sheet title sliver cropped)",
        APP_COUNTS,
    ],
}

CL03 = {
    "id": "CL03_work_an_ecg_case", "app": "CardioLens AI", "date": "2026-10-20", "time": "12:00", "keyword": "LENS",
    "caption": f"""How to work an ECG case, the same way every time. Save this. 🩺

1. Patient first. Is the rhythm causing hypotension, acutely altered mental status, signs of shock, ischemic chest discomfort or acute heart failure? Then it's unstable: get help and follow the AHA tachy- or brady- algorithm. No pulse? Start CPR.
2. Rhythm and rate: the 5 questions (rate, regular, P, PR, QRS).
3. The 12-lead: a change in 2 or more contiguous leads? Name the group: inferior II, III, aVF · lateral I, aVL, V5–V6 · anterior V1–V4.
4. The old ECG: it helps tell a new finding from a chronic one, but it should never delay treatment.
5. Act: escalate what's new, per your protocol. Still symptomatic with a non-diagnostic first ECG? Repeat it every 15–30 min over the first 1–2 hours.

Comment LENS and we'll DM you the link to CardioLens AI.

{DISCLAIMER}

#ECG #12Lead #NursingStudent #Paramedic #CardiacNurse""",
    "alt": ("Six-slide carousel from CardioLens AI. "
            "Slide 1: 'How to work an ECG case' with five numbered steps: patient first, rhythm and rate, the 12-lead, "
            "the old ECG, act. "
            "Slide 2: the five signs that make a rhythm unstable from the AHA 2025 algorithms, stable versus unstable, "
            "and 'no pulse, start CPR'. "
            "Slide 3: the five rhythm questions next to a 12-lead layout colour-coded into inferior, lateral and "
            "anterior lead groups (labelled common teaching groups), with the 2-contiguous-leads rule and the 10-minute target. "
            "Slide 4: synthetic lead III from a past visit beside today's lead III with new ST elevation, and steps to "
            "compare, escalate and repeat the ECG. "
            "Slide 5: the CardioLens Cases screen with 10 series and 60 cases, and how to work a case: strip and story "
            "first, tap Quiz before the Diagnosis box, then review; Cases marked Pro and Rhythm Mastery marked free. "
            "Slide 6: a CardioLens quiz question that opens with a patient, and 'Comment LENS' to get the download link."),
    "dm": f"""Here's CardioLens AI 👉 {CARDIOLENS_IOS}
Android: {CARDIOLENS_ANDROID}

First thing to try: Learn → Rhythm Mastery (free). Most of its free questions start from a patient, not just a strip. With Pro, open Learn → Clinical Cases, read the strip and the patient story, then tap Quiz before you scroll to the Diagnosis box.

Educational only, not a diagnostic tool.""",
    "sources": [
        AHA_TACHY,
        AHA_BRADY,
        AHA_CA + " — used here only for 'no pulse: start CPR'",
        "Fourth Universal Definition of MI (Thygesen et al., Eur Heart J 2019;40:237–269), §27: 12-lead ECG acquired and "
        "interpreted within 10 min of first medical contact; ST shift in ≥2 contiguous leads; 'A prior ECG is often "
        "helpful in distinguishing a new from a chronic finding, but should not delay the decision for treatment'; "
        "serial ECGs at 15–30 min intervals during the first 1–2 h for persistent or recurrent symptoms or an initial "
        "non-diagnostic ECG — https://doi.org/10.1093/eurheartj/ehy462 (verified in the full text) · " + UDMI,
        STD_I,
        "AHA/ACCF/HRS ECG standardization Part VI: Acute Ischemia/Infarction (Wagner 2009) — "
        "https://www.ahajournals.org/doi/10.1161/CIRCULATIONAHA.108.191098 (lead-group grouping on s03 follows the "
        "common convention also used in CardioLens' Coronary Vessels module: inferior II/III/aVF, lateral I/aVL/V5–V6, "
        "anterior V1–V4 — iOS Tabs/Learn/CoronaryVesselsView.swift L25, L100–102)",
        "App: Clinical Cases are Pro (iOS Tabs/Cases/CasesView.swift isLocked → paywall; Android feature/learn/"
        "LearnScreen.kt onCases if isPro). 60 cases in 10 series with Beg/Int/Adv levels (Resources/cases.json; "
        "screenshot). Each case opens on the Live Strip tab with age, sex and presentation; the Diagnosis box and teaching points "
        "are shown before the Quiz tab, so s05 tells users to tap Quiz first (Tabs/Cases/CaseDetailView.swift L136–166); "
        "per-question feedback (QuizView.swift feedbackBox) and teaching points (QuizResultView.swift). Per the audit, "
        "30 of 33 free Rhythm Mastery questions start from a patient ('most'). Free Rhythm "
        "Mastery question with a patient vignette: cardiolens-website/public/screens/ss5-question.png. s05 screenshot "
        "ss6-cases.png ('10 series · 60 cases')",
        APP_COUNTS + "; 8 study modules (Tabs/Learn/StudyModulesListView.swift)",
    ],
}

CL04 = {
    "id": "CL04_conduction_system", "app": "CardioLens AI", "date": "2026-10-23", "time": "12:00", "keyword": "LENS",
    "caption": f"""The conduction system in 1 slide, and what each part draws on the ECG. ⚡

SA node fires → the atria depolarize = the P wave. Upright P in lead II before every QRS: points to a sinus beat.
AV node slows the impulse → His bundle → bundle branches = the flat PR segment. Whole PR (start of P to start of QRS): 0.12–0.20 s.
Purkinje fibers fire both ventricles at once = a quick, narrow QRS (under 0.12 s). A detour, like a blocked bundle branch or a beat that starts in the ventricle, makes it 0.12 s or wider.

Pacemaker rates: SA node 60–100/min; backups: AV junction 40–60/min (narrow QRS), ventricles 20–40/min (wide QRS). The fastest one sets the pace; a lower one takes over as an escape rhythm when the faster one fails or is blocked.

Comment LENS and we'll DM you the link to CardioLens AI.

{DISCLAIMER}

#ECG #EKG #NursingStudent #CardiacNurse #NursingSchool""",
    "alt": ("Six-slide carousel from CardioLens AI. "
            "Slide 1: a schematic heart showing the SA node, atrial pathways, AV node, His bundle, bundle branches and "
            "Purkinje fibers, colour-matched to a single synthetic beat: P wave, PR segment and QRS. "
            "Slide 2: a zoomed beat with the P wave and PR segment highlighted and a PR of 0.16 seconds bracketed, "
            "explaining that P is the atria and the PR is the trip through the AV node, His and bundle branches. "
            "Slide 3: the same beat with a 0.09-second QRS highlighted, explaining that Purkinje fibers fire the "
            "ventricles, and narrow versus wide QRS. "
            "Slide 4: 'If the top fails or is blocked, the next one down takes over', with three synthetic strips: SA node 60 to 100, AV junction 40 to 60 with "
            "narrow QRS, ventricles 20 to 40 with wide QRS. "
            "Slide 5: the CardioLens Conduction System module with its heart diagram and Play Animation button, marked "
            "free, with three steps. "
            "Slide 6: the PQRST Wave Origins module and 'Comment LENS' to get the download link."),
    "dm": f"""Here's CardioLens AI 👉 {CARDIOLENS_IOS}
Android: {CARDIOLENS_ANDROID}

First thing to try (free): Learn → Study Modules → Conduction System and press Play Animation (iPhone), then open PQRST Waves and match each stage to its wave.

Educational only, not a diagnostic tool.""",
    "sources": [
        STD_I,
        STD_III,
        "StatPearls: Junctional Rhythm (Hafeez, Wollard, Grossman; updated 2026), PMID 29939537: impulse SA node → AV "
        "node (conduction slows briefly) → His → right and left bundle branches → Purkinje; faster SA node suppresses "
        "lower pacemakers (overdrive suppression); junctional escape rhythm 40–60 bpm — "
        "https://pubmed.ncbi.nlm.nih.gov/29939537/",
        "Merck Manual Professional, Atrioventricular Block: escapes above the His bifurcation give narrow QRS; below it, "
        "wider QRS at 20–40 beats/min (Merck lists junctional escape at 35–50 bpm, so the s04 footer cites Merck for the ventricular 20–40/min only; the junctional 40–60 is StatPearls) — "
        "https://www.merckmanuals.com/professional/cardiovascular-disorders/specific-cardiac-arrhythmias/atrioventricular-block",
        "MedGen/HPO 'Ventricular escape rhythm' (C0232216): escape rate usually 20–40 bpm, often broad QRS (≥120 ms) — "
        "https://www.ncbi.nlm.nih.gov/medgen/65423",
        "Sinus 60–100/min: 2018 ACC/AHA/HRS Bradycardia Guideline §2.2 (bradycardia = HR <60 bpm per NIH) — "
        "https://doi.org/10.1161/CIR.0000000000000628 · sinus tachycardia >100 bpm, 2015 ACC/AHA/HRS SVT Guideline — "
        "https://doi.org/10.1161/CIR.0000000000000311 (same 60–100 range as CL01)",
        "App: Conduction System and PQRST Waves are free modules (iOS Tabs/Learn/StudyModulesListView.swift "
        "freeModuleIDs = pqrst, conduction, coronary, bbb; Android feature/learn/LearnScreen.kt freeModuleIds). "
        "Stage pills SA node / Atrial spread / AV node / Bundle of His / Bundle branches / Purkinje fibers and Play "
        "Animation: Tabs/Learn/ConductionView.swift L111–147. Android renders modules as a text summary with an example "
        "strip (LearnScreen.kt header PORT NOTE + ModuleDetailPane), so the animation is described as iPhone. "
        "s05 screenshot ss9-conduction.png; s06 ss10-pqrst.png",
        APP_COUNTS,
    ],
}

CL05 = {
    "id": "CL05_axis_two_leads", "app": "CardioLens AI", "date": "2026-10-26", "time": "12:00", "keyword": "LENS",
    "caption": f"""Axis in 2 leads: I and aVF. 🧭

Step 1: Is the QRS mostly up or mostly down in each lead? Compare the R with the Q + S.
Step 2: Both up = normal. I down, aVF up = right axis. Both down = extreme axis.
Step 3: I up, aVF down? Check lead II before you call it left axis. II up = between 0° and −30° = still normal. II down = past −30° = left axis deviation.

Adult normal axis: −30° to +90° (AHA/ACCF/HRS standardization statement). Some books use +100° as the upper limit.

Comment LENS and we'll DM you the link to CardioLens AI.

{DISCLAIMER}

#ECG #12Lead #EKG #NursingStudent #Paramedic""",
    "alt": ("Six-slide carousel from CardioLens AI. "
            "Slide 1: 'Axis in 2 leads: I and aVF' with a 2-by-2 grid of synthetic QRS complexes: both up is normal, I up "
            "and aVF down is possible left axis, I down and aVF up is right axis, both down is extreme. "
            "Slide 2: a positive QRS (R taller than Q + S are deep) and a negative one (Q + S deeper than the R is tall), explaining how to judge the net deflection and what an equiphasic "
            "QRS means. "
            "Slide 3: a hexaxial wheel shaded into normal from −30° to +90°, left axis deviation from −30° to −90°, right "
            "axis deviation from +90° to +180° and extreme axis. "
            "Slide 4: the wheel with lead II at +60° and the −30° boundary, showing that lead II up means still normal "
            "and lead II down means left axis deviation. "
            "Slide 5: the CardioLens Study Modules list with the locked Axis Interpretation module highlighted as Pro, "
            "and a warning that its Axis Finder calls I up plus aVF down left axis, so check lead II yourself. "
            "Slide 6: a CardioLens scan screen, the note that scans don't report axis, and 'Comment LENS' to get the download link."),
    "dm": f"""Here's CardioLens AI 👉 {CARDIOLENS_IOS}
Android: {CARDIOLENS_ANDROID}

First thing to try: with Pro, open Learn → Study Modules → Axis Interpretation and use the Axis Finder (iPhone): set lead I and aVF up or down; it names the quadrant. I up, aVF down? It will say left axis, so check lead II yourself (slide 4). Free modules to start with: PQRST Waves and Conduction System.

Educational only, not a diagnostic tool.""",
    "sources": [
        STD_III,
        "StatPearls: Electrical Right and Left Axis Deviation (normal −30° to +90°, sometimes extended to +100°) — "
        "https://www.ncbi.nlm.nih.gov/books/NBK470532/",
        "Hexaxial geometry (lead I 0°, II +60°, III +120°, aVF +90°, aVL −30°, aVR −150°; a lead reads positive when the "
        "axis is within 90° of its positive pole, so lead II is positive from −30° to +150°) — standard limb-lead "
        "reference frame, AHA/ACCF/HRS standardization Part I — "
        "https://www.ahajournals.org/doi/10.1161/CIRCULATIONAHA.106.180200",
        "App: Axis Interpretation module ('Lead I & aVF method') exists on both platforms and is Pro: not in the free "
        "set (iOS Tabs/Learn/StudyModulesListView.swift freeModuleIDs; Android feature/learn/LearnScreen.kt "
        "freeModuleIds). The iOS module has the hexaxial wheel, the Axis Finder (lead I and aVF positive/negative → "
        "Normal / Left / Right / Extreme) and labels normal −30° to +90° (Tabs/Learn/AxisInterpretationView.swift). "
        "Android shows the module as a text summary only (LearnScreen.kt ModuleDetailPane). The Axis Finder maps I+ / aVF− straight to 'Left Axis Deviation' (AxisInterpretationView.swift axisResult), hence the s05/DM warning. Scans do not report axis "
        "(no axis field in Models/AnalysisResult.swift), so no scan-based axis claim is made. s05 screenshot "
        "ss3-modules.png (Axis Interpretation row with lock); s06 cl_scan.png (CL01's scan screen)",
        APP_COUNTS + "; 8 study modules, 4 free",
    ],
}

CL06 = {
    "id": "CL06_megacodes_on_phone", "app": "CardioLens AI", "date": "2026-10-29", "time": "12:00", "keyword": "LENS",
    "caption": f"""A code runs on a 2-minute clock. Here's the loop from the AHA 2025 adult cardiac arrest algorithm. ⏱️

Every 2 minutes: a brief rhythm check. Shockable (VF/pulseless VT)? Shock, then straight back into 2 minutes of CPR. Not shockable? Straight into CPR.
Shockable side: CPR + oxygen until the pads are on, then the check. Shock 1 → CPR + IV/IO access. Shock 2 → CPR + epinephrine 1 mg IV/IO, then every 3–5 min. Shock 3 → CPR + amiodarone 300 mg (or lidocaine 1–1.5 mg/kg). Second dose: amiodarone 150 mg (or lidocaine 0.5–0.75 mg/kg).
Asystole/PEA: no shock, epinephrine 1 mg as soon as possible, then every 3–5 min. Treat reversible causes. If a check shows VF/pVT, shock and switch sides.

Learn to spot VF, VT and asystole free in CardioLens AI, and rehearse with MEGA CODES (Pro). The app's flowcharts and MEGA CODES use general ACLS wording and are not the AHA 2025 algorithm, so check every step against AHA 2025.

Comment LENS and we'll DM you the link to CardioLens AI.

{DISCLAIMER} Not a substitute for certified ACLS training; follow AHA 2025 and your institution's protocols.

#ACLS #CodeBlue #Megacode #NursingStudent #Paramedic""",
    "alt": ("Six-slide carousel from CardioLens AI. "
            "Slide 1: 'A code runs on a 2-minute clock' with a dial split into rhythm check, shock if shockable, and CPR "
            "plus medications (2:00 of CPR, then a pause under 10 s to check), next to the CardioLens MEGA CODES list. "
            "Slide 2: a flow diagram: rhythm check, shock for VF or pulseless VT or no shock for asystole or PEA, then 2 "
            "minutes of CPR with IV/IO access, drugs, airway, reversible causes and compressor swaps. "
            "Slide 3: a timeline for the shockable side: CPR and oxygen until pads are on, shock 1 then IV/IO access, shock 2 then epinephrine 1 mg every "
            "3 to 5 minutes, shock 3 then amiodarone 300 mg or lidocaine, then a second and last amiodarone dose of 150 mg or lidocaine. "
            "Slide 4: a timeline for asystole or PEA: epinephrine 1 mg as soon as possible, CPR, reversible causes, and "
            "switching to the shockable side if VF appears. "
            "Slide 5: 'Know the rhythm. Rehearse the code.' with the CardioLens Algorithms tab and MEGA CODES list: Rhythm "
            "Mastery VF, VT and asystole marked free, MEGA CODES and the ACLS flowchart marked Pro, and a note that the "
            "app's flowcharts and MEGA CODES use general ACLS wording and are not the AHA 2025 algorithm. "
            "Slide 6: the Rhythm Mastery screen, 7 scored MEGA CODE scenarios on iPhone, and 'Comment LENS' to get the download link."),
    "dm": f"""Here's CardioLens AI 👉 {CARDIOLENS_IOS}
Android: {CARDIOLENS_ANDROID}

First thing to try: warm up free in Learn → Rhythm Mastery (VF, VT and asystole). With Pro, open Algorithms → MEGA CODES → Classic VFib Arrest for scenario practice.

Heads-up: the app lists amiodarone only; AHA 2025 accepts amiodarone or lidocaine. The app's flowcharts and MEGA CODES use general ACLS wording and are not the AHA 2025 algorithm, so check every step against AHA 2025.

Educational only, not a diagnostic tool, and not a substitute for certified ACLS training.""",
    "sources": [
        AHA_CA,
        AHA_PART9,
        "AHA 2025 Adult Cardiac Arrest Algorithm box 1: start CPR, give oxygen, attach monitor/defibrillator (s03 0:00); "
        "brief rhythm checks — Part 9 (pause under 10 s, as in approved C6)",
        "Angle check: previous posts covered megacode mistakes (C6) and drug doses as a cheat sheet (C5); this one is the "
        "cycle structure on a timeline. '~2:00 / ~4:00' marks are the algorithm's 2-minute CPR blocks; 'every 3–5 min ≈ "
        "every other 2-minute cycle' is arithmetic (4 min falls inside 3–5 min)",
        "App: Algorithms and MEGA CODES are Pro on both platforms (iOS Tabs/Algorithms/AlgorithmsView.swift L45–50, "
        "L133–137; Android feature/algorithms/AlgorithmsScreen.kt L85–87 'Algorithms are subscriber-only'). Classic VFib "
        "Arrest scenario with rhythm + HR/BP/SpO2/ETCO2 at each decision and a scored debrief (iOS "
        "Models/MegaCodeScenario.swift scenario1, Tabs/Algorithms/MegaCodesView.swift L145–152, MegaCodesViewModel.swift; "
        "Android feature/algorithms/MegaCodesScreen.kt). 7 scored scenarios on iOS (MegaCodeLibrary.allScenarios), 5 on Android, so s06 says "
        "'(iPhone)'. App flowcharts/MEGA CODES use non-AHA wording (adrenaline, 4 H's & 4 T's, amiodarone only, TTM; "
        "lidocaine graded wrong in scenario1) — Resources/algorithms.json, Models/MegaCodeScenario.swift — hence the "
        "s05/caption/DM caveat and the app is positioned for rhythm recognition + scenario practice only. Algorithm filters ACLS · PALS · BCLS · "
        "Stroke (AlgorithmsView.swift header). VF, VT and asystole are free 'survival' quiz rhythms (quiz_bank_v1.json). "
        "s01/s05 screenshots ss8-megacodes.png and ss7-algorithms.png (shown unlocked, i.e. the Pro view); s06 "
        "ss4-quiz.png",
        APP_COUNTS,
    ],
}

CL_CAROUSELS = [CL02, CL03, CL04, CL05, CL06]
