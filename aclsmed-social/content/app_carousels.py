"""App carousels, Oct 14–31: teach one idea, use the real app screen as the example, end on a comment keyword.

Slides are designed on the Design canvas (https://claude.ai/artifact/892aFz9JQH7ADWyRPLKdC4), copied to
app_carousels/src/<id>/ and rendered by app_carousels/render.mjs. This file holds what goes with each one:
schedule slot, caption, alt text, the ManyChat DM and the sources the clinical gate checks.
"""

CARDIOLENS_IOS = "https://apps.apple.com/app/cardiolens/id6761556643"
CARDIOLENS_ANDROID = "https://play.google.com/store/apps/details?id=com.cardiolens.android"
ECGBUILDER_ANDROID = "https://play.google.com/store/apps/details?id=com.ecgbuilder.app"

UDMI = "Fourth Universal Definition of MI (2018) — https://www.ahajournals.org/doi/10.1161/CIR.0000000000000617"

CL01 = {
    "id": "CL01_read_any_strip", "app": "CardioLens AI", "date": "2026-10-14", "time": "12:00", "keyword": "LENS",
    "caption": """Read any rhythm strip in 5 questions. Save this for your next shift. 🫀

1. How fast? Regular: 300 ÷ big boxes between R waves. Irregular: count the QRS in a 6-second strip × 10.
2. Regular? March out the R waves.
3. A P before every QRS, and a QRS after every P?
4. PR 0.12–0.20 s (3–5 small boxes).
5. QRS narrow (under 0.12 s) or wide?

Want to practice on real strips? Comment LENS and we'll DM you the link to CardioLens AI.

Educational only, not a diagnostic tool. Never upload a strip with patient identifiers.

#ECG #EKG #NursingStudent #Telemetry #CardiacNurse""",
    "alt": ("Six-slide carousel from CardioLens AI. Slide 1: 'Read any rhythm strip in 5 questions' over a glowing ECG "
            "and a phone showing a CardioLens scan. Slide 2: rate and regularity, R to R of 4 big boxes = 75 per "
            "minute, and the 6-second method. Slide 3: a zoomed beat labelled P, QRS and T with the PR interval of "
            "0.16 s marked; normal PR 0.12 to 0.20 s. Slide 4: a narrow QRS of 0.07 s next to a wide QRS of 0.16 s "
            "and what a wide QRS can mean. Slide 5: the five answers checked against a CardioLens scan reading sinus "
            "tachycardia at 115. Slide 6: comment LENS to get the app link."),
    "dm": f"""Here's CardioLens AI 👉 {CARDIOLENS_IOS}
Android: {CARDIOLENS_ANDROID}

Start in Learn → Rhythm Mastery, then scan a textbook strip and run the 5 questions on it. 3 scans a month are free.

Educational only, not a diagnostic tool.""",
    "sources": [
        "AHA ECG interpretation basics: 25 mm/s paper, 1 small box 0.04 s, 1 big box 0.20 s; normal PR 0.12–0.20 s; "
        "QRS under 0.12 s — AHA/ACCF/HRS Recommendations for the Standardization and Interpretation of the ECG (2007) "
        "https://www.ahajournals.org/doi/10.1161/CIRCULATIONAHA.106.180200",
        "AHA 2025 ACLS: wide-complex tachycardia, treat as VT if unstable — "
        "https://www.ahajournals.org/doi/10.1161/CIR.0000000000001376",
        "CardioLens App Store listing (features, free tier: 3 scans/month, 288 quiz questions, 60 cases, 40+ rhythms) "
        f"— {CARDIOLENS_IOS}",
    ],
}

AC01 = {
    "id": "AC01_four_stations", "app": "ACLSMED Sim", "date": "2026-10-15", "time": "12:00", "keyword": "SIM",
    "caption": """One patient. Four stations. How to run a full mock code from tablets and phones. 🏥

01 Monitor + Instructor Remote: you drive the rhythm, they run the code. Change it mid-scenario without saying a word.
02 IVmed pump: learners program the drip. IV epinephrine and amiodarone are high-alert medications, so practice the independent double-check.
03 RESPmed ventilator: tidal volume comes from predicted body weight (height + sex), not the scale.
04 ACLSMED CPR: live rate, depth and recoil. AHA 2025 recommends feedback devices in CPR training.

Comment SIM and we'll DM you the link to ACLSMED Sim.

Educational only, not a substitute for certified ACLS training. Follow AHA 2025 guidelines and your institution's protocols.

#Simulation #NurseEducator #ACLS #MockCode #SimLab""",
    "alt": ("Six-slide carousel from ACLSMED. Slide 1: 'One patient. Four stations.' over the ACLSMED Sim suite on four "
            "devices. Slide 2: the instructor remote driving the patient monitor. Slide 3: the IVmed infusion pump, "
            "with the teaching point that IV epinephrine and amiodarone are high-alert medications. Slide 4: the "
            "RESPmed ventilator and a worked example: a 178 cm male has a predicted body weight of 73 kg, so 6 mL/kg "
            "is 440 mL whatever he weighs. Slide 5: ACLSMED CPR showing live compression feedback for six learners. "
            "Slide 6: comment SIM to get the ACLSMED Sim link."),
    "dm": "Uses the existing SIM keyword reply (content/sim_carousels.py DM_REPLY).",
    "sources": [
        "ISMP List of High-Alert Medications in Acute Care Settings (IV adrenergic agonists e.g. epinephrine; IV "
        "antiarrhythmics e.g. amiodarone) — https://www.ismp.org/recommendations/high-alert-medications-acute-list",
        "ATS/ESICM/SCCM 2017 ARDS guideline: 4–8 mL/kg predicted body weight; PBW male 50 + 0.91 × (cm − 152.4), "
        "female 45.5 + 0.91 × (cm − 152.4) (ARDSNet) — https://doi.org/10.1164/rccm.201703-0548ST",
        "AHA 2025 Part 12: Resuscitation Education Science (CPR feedback devices in training) — "
        "https://cpr.heart.org/en/resuscitation-science/cpr-and-ecc-guidelines/resuscitation-education-science",
        "ACLSMED download + institutions pages (Clinical Suite: Monitor, Instructor Remote, IVmed, RESPmed sharing one "
        "patient; ACLSMED CPR free, pairs up to 6 learners; web simulator) — aclsmed.com/download, "
        "aclsmed.com/institutions",
    ],
}

EB01 = {
    "id": "EB01_inferior_stemi_avl", "app": "ECG Builder", "date": "2026-10-16", "time": "12:00", "keyword": "BUILD",
    "caption": """Inferior STEMI leaves a clue in aVL. 🔎

Step 1: ST elevation in II, III and aVF (new, at the J point, 1 mm or more in 2 contiguous leads).
Step 2: Look at aVL. ST depression there is the mirror image: reciprocal change.
Step 3: Rule out look-alikes. Pericarditis: widespread ST elevation, often PR depression, no reciprocal change except aVR (sometimes V1). Early repolarization: J-point notch or slur, no reciprocal change, doesn't evolve.

Every tracing here was built in ECG Builder. Comment BUILD and we'll DM you the download link.

Synthetic tracings. Educational only, not diagnostic.

#ECG #STEMI #12Lead #CardiacNurse #Paramedic""",
    "alt": ("Six-slide carousel from ECG Builder. Slide 1: a synthetic 12-lead ECG with inferior ST elevation, titled "
            "'Inferior STEMI leaves a clue in aVL'. Slide 2: leads II, III and aVF boxed, showing ST elevation, with "
            "the criteria. Slide 3: aVL boxed, showing reciprocal ST depression, and why it happens. Slide 4: STEMI "
            "compared with pericarditis and early repolarization. Slide 5: the ECG Builder rhythm picker and "
            "ischaemia tool on iPhone. Slide 6: comment BUILD to get the download link."),
    "dm": f"""Here's ECG Builder 👉 [App Store link — confirm it is live]
Android: {ECGBUILDER_ANDROID}

Try it: pick sinus rhythm, open Ischaemia, choose Inferior and drag the ST shift. Watch aVL mirror it.

Every tracing is synthetic. Educational only, not a medical device.""",
    "sources": [
        UDMI,
        "2015 ESC Guidelines on pericardial diseases (widespread ST elevation, PR depression) — "
        "https://doi.org/10.1093/eurheartj/ehv318",
        "AHA/ACCF/HRS ECG standardization Part VI: acute ischemia/infarction (reciprocal ST depression) — "
        "https://www.ahajournals.org/doi/10.1161/CIRCULATIONAHA.108.191098",
        "ECG Builder App Store metadata (synthetic tracings, reciprocal change modelled as a vector, export) — "
        "PXLBLR/ECGBuilder Marketing/AppStore/METADATA.md",
    ],
}

APP_CAROUSELS = [CL01, AC01, EB01]
