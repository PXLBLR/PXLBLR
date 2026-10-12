"""Corrections and replacements after the Oct 12 STEMI call-out.

Every reel here carries `sources` (primary references for each on-screen claim) and must pass the
CLINICAL_REVIEW.md gate before it is packaged.
"""
from engine import twelvelead
from engine.brand import CYAN, RED, YELLOW

from .reels_oct8_25 import NP, cap
from .story import story

ECG_12 = twelvelead.render()
ECG_12_MARKED = twelvelead.render(highlight=["V2", "V3", "V4"], recip=["III", "aVF"])
INF_12 = twelvelead.render(twelvelead.INFERIOR_STEMI, hr=56)
INF_12_MARKED = twelvelead.render(twelvelead.INFERIOR_STEMI, hr=56, highlight=["II", "III", "aVF"], recip=["I", "aVL"])

UDMI = ("Fourth Universal Definition of Myocardial Infarction (2018) — "
        "https://www.ahajournals.org/doi/10.1161/CIR.0000000000000617")
AHA25_ACLS_CHANGES = ("AHA 2025 Interim Training Materials: ACLS Provider Manual Changes — "
                      "https://cpr.heartandstroke.ca/resource/Guidelines2025InterimACLSProviderManualEN")
STEMI_2013 = ("2013 ACCF/AHA STEMI guideline (RV infarction, V4R, nitrate avoidance) — "
              "https://www.ahajournals.org/doi/10.1161/CIR.0b013e3182742cf6")

CORRECTION = ("Updated version of our earlier STEMI reel. Thank you to everyone who flagged it: STEMI is diagnosed "
              "on a 12-lead with mm criteria, and nitrates have real contraindications.")


def s09_v2():
    return story("S09_stemi_v2_12lead", [
        {"d": 3.2, "hook": True, "top": "Chest pain +\n*ST elevation?*", "img": ECG_12},
        {"d": 5.5, "pill": ("NOT FOR ST DIAGNOSIS", RED), "top": "Diagnose STEMI on a *12-lead*, not the monitor.",
         "rh": ("sinus", {"hr": 88}, "HR 88", None, "MONITOR  ·  II"),
         "bottom": "Monitor filters can *distort the ST segment*."},
        {"d": 7, "top": "New ST elevation at the J point\nin *2 contiguous leads*", "rh": "off", "img": ECG_12_MARKED,
         "bullets": ["*1 mm or more* in most leads",
                     "V2–V3: *2 mm* men 40+, *2.5 mm* men under 40, *1.5 mm* women"]},
        {"d": 4.5, "top": "Look for *reciprocal* depression", "img": ECG_12_MARKED,
         "bottom": "ST elevation V2–V4, *reciprocal depression III & aVF*.", "bottom_accent": CYAN},
        {"d": 5.5, "top": "Rule out *mimics*",
         "bullets": ["LBBB · paced rhythm · LVH", "Early repolarization · pericarditis",
                     "Compare with an *old ECG*"]},
        {"d": 7.5, "pill": ("2025 ACC/AHA", CYAN), "top": "Reperfusion targets",
         "bullets": ["12-lead within *10 min* of arrival",
                     "Primary PCI: first contact to device *90 min* or less (*120 min* with transfer)",
                     "PCI delay over 120 min + symptoms under 12 h → *fibrinolysis* if no contraindications"]},
        {"d": 7.5, "top": "Before *nitroglycerin*, check:",
         "bullets": ["SBP under 90 (or 30+ below baseline)", "*RV infarct*: get right-sided leads",
                     "*PDE-5 inhibitor*: 24 h (sildenafil, vardenafil), 48 h (tadalafil)",
                     "Marked bradycardia or tachycardia"]},
        {"d": 3.6, "top": "Activate the cath lab *early.*", "img": ECG_12_MARKED, "big": "TIME = MUSCLE",
         "big_size": 92},
    ], caption=cap(CORRECTION + "\n\nSTEMI = new ST elevation at the J point in 2 contiguous leads on a 12-lead: "
                   "1 mm or more in most leads; in V2–V3, 2 mm (men 40+), 2.5 mm (men under 40), 1.5 mm (women). "
                   "Look for reciprocal depression and rule out mimics.\n\nPrimary PCI: first medical contact to "
                   "device in 90 min or less (120 with transfer). Expected PCI delay over 120 min and symptoms under "
                   "12 h → fibrinolysis if no contraindications. Aspirin if no contraindication; oxygen only if "
                   "SpO2 under 90%. No nitrates with SBP under 90, RV infarct, recent PDE-5 inhibitors, or marked "
                   "brady/tachycardia.",
                   ["STEMI", "ECG", "ACLS", "CardiacNurse", "EmergencyMedicine"]),
        shorts_title="STEMI on the 12-Lead: Criteria, Targets & Nitro Safety #shorts",
        sources=[
            "2025 ACC/AHA/ACEP/NAEMSP/SCAI Guideline for Acute Coronary Syndromes — "
            "https://www.ahajournals.org/doi/10.1161/CIR.0000000000001309",
            "Fourth Universal Definition of Myocardial Infarction (2018), STEMI ST criteria — "
            "https://www.ahajournals.org/doi/10.1161/CIR.0000000000000617",
            "PDE-5 inhibitor / nitrate interaction (AHA) — "
            "https://www.ahajournals.org/doi/10.1161/circulationaha.110.944603",
            "Nitrate contraindications in ACS (2013 STEMI / 2014 NSTE-ACS guidance summary) — "
            "https://www.ebmconsult.com/articles/contraindications-nitroglycerin-in-acute-coronary-syndrome",
            "AHA Practice Standards for Electrocardiographic Monitoring (monitor vs diagnostic filtering) — "
            "https://www.ahajournals.org/doi/10.1161/CIR.0000000000000527",
        ])


def s37_choking():
    return story("S37_choking_2025", [
        {"d": 3.2, "hook": True, "top": "Choking adult?\n*Back blows* come first now.", "top_size": 90, "rh": "off",
         "open_sfx": "alarm"},
        {"d": 5, "pill": ("AHA 2025", CYAN), "top": "Can they *cough or speak?*", "big": "LET THEM COUGH",
         "big_size": 96, "big_color": CYAN, "sub": "Mild obstruction. Stay with them, watch for it getting worse."},
        {"d": 4.5, "top": "Can't speak, cough or breathe?", "big": "CALL 911", "sub": "Severe obstruction. Then act fast."},
        {"d": 5, "pill": ("STEP 1", RED), "top": "Lean them forward", "big": "5 BACK BLOWS",
         "sub": "Firm blows *between the shoulder blades*.", "sfx": [(0.6 + i * 0.32, "pop", 0.8) for i in range(5)]},
        {"d": 5.5, "pill": ("STEP 2", RED), "top": "Then", "big": "5 ABDOMINAL\nTHRUSTS", "big_size": 96,
         "sub": "Repeat *5 + 5* until it's out or they become unresponsive.",
         "sfx": [(0.6 + i * 0.32, "pop", 0.8) for i in range(5)]},
        {"d": 5, "top": "Late pregnancy, or can't reach around them?", "big": "5 CHEST THRUSTS", "big_size": 96,
         "big_color": YELLOW, "sub": "Use chest thrusts *instead of* abdominal thrusts."},
        {"d": 6.5, "top": "Becomes unresponsive?",
         "bullets": ["Lower them to the floor", "*Start CPR*, compressions first",
                     "See the object? Remove it. *No blind finger sweeps.*"]},
        {"d": 4.5, "top": "Infants (under 1 year):",
         "bottom": "5 back blows + 5 *chest* thrusts. *No abdominal thrusts.*"},
    ], ask="Share this with someone\nwho *eats with you.*",
        caption=cap("AHA 2025 changed choking care: for a conscious adult with severe choking, give 5 back blows, "
                    "then 5 abdominal thrusts, and repeat until the object comes out or they become unresponsive. "
                    "🫁\n\nCan they cough or speak? Let them cough and watch closely. Late pregnancy or can't reach "
                    "around them? Chest thrusts instead. Unresponsive? Start CPR. Infants: 5 back blows + 5 chest "
                    "thrusts, never abdominal thrusts.",
                    ["Choking", "BLS", "CPR", "AHA2025", "FirstAid"]),
        shorts_title="Choking: The 2025 AHA Change (Back Blows First) #shorts",
        sources=[
            "AHA newsroom, 2025 Guidelines: choking update (5 back blows + 5 abdominal thrusts; infants 5 + 5 chest "
            "thrusts, no abdominal thrusts) — https://newsroom.heart.org/news/updated-cpr-guidelines-tackle-choking-"
            "response-opioid-related-emergencies-and-a-revised-chain-of-survival",
            "Part 7: Adult Basic Life Support, 2025 AHA Guidelines (mild FBAO: allow coughing; severe: activate EMS, "
            "5 + 5; late pregnancy / can't encircle: chest thrusts; unresponsive: start CPR) — "
            "https://www.ahajournals.org/doi/10.1161/CIR.0000000000001369",
            "Evolution of FBAO guidelines 2005–2025 (ILCOR: against blind finger sweeps; remove visible objects) — "
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC13395594/",
        ])


def s10_v2():
    return story("S10_inferior_mi_rv_v2", [
        {"d": 3.2, "hook": True, "top": "Inferior STEMI?\nCheck the *right side.*", "img": INF_12},
        {"d": 7, "top": "ST elevation in *II, III, aVF*", "img": INF_12_MARKED,
         "bullets": ["*1 mm or more*, 2 contiguous leads, on a *12-lead*",
                     "Reciprocal depression in *I and aVL*"]},
        {"d": 6, "top": "Get a *right-sided ECG*", "rh": ("beats", {"st": 0.2, "t_amp": 0.3, "hr": 56}, None,
                                                          None, "V4R  ·  RIGHT-SIDED 12-LEAD"),
         "bottom": "ST elevation *1 mm or more in V4R* supports RV infarction."},
        {"d": 7, "top": "RV infarct = *preload dependent*", "rh": "off", "img": INF_12_MARKED,
         "big": "AVOID NITRATES", "big_size": 84, "big_color": YELLOW,
         "sub": "They can crash the BP. Hypotension → *IV fluids*."},
        {"d": 6, "top": "Also watch for:", "img": INF_12_MARKED,
         "bullets": ["*Bradycardia* & AV block", "Hypotension with *clear lungs*",
                     "*Activate the cath lab* early"]},
    ], caption=cap("Inferior STEMI = new ST elevation of 1 mm or more in 2 contiguous inferior leads (II, III, aVF) on "
                   "a 12-lead, often with reciprocal depression in I and aVL.\n\nGet a right-sided ECG: ST elevation "
                   "of 1 mm or more in V4R supports RV infarction. RV infarcts are preload dependent, so avoid "
                   "nitrates and treat hypotension with fluids. Watch for bradycardia and AV block, and get them to "
                   "reperfusion fast.",
                   ["STEMI", "ECG", "CardiacNurse", "ACLS", "ICUNurse"]),
        shorts_title="Inferior STEMI on the 12-Lead: Check V4R Before Nitro #shorts",
        sources=[UDMI, STEMI_2013,
                 "2025 ACC/AHA ACS guideline — https://www.ahajournals.org/doi/10.1161/CIR.0000000000001309"])


def s11_v2():
    return story("S11_arrest_pregnancy_v2", [
        {"d": 3.2, "hook": True, "top": "Cardiac arrest\nin *pregnancy.*", "rh": ("cpr", {}, None)},
        {"d": 6.5, "top": "Uterus at or above the navel?", "big": "LEFT UTERINE\nDISPLACEMENT", "big_size": 76,
         "big_color": CYAN, "sub": "*Manual* and continuous. Relieves aortocaval compression."},
        {"d": 6.5, "top": "Nothing else changes:",
         "bullets": ["*Same* compressions, drugs & doses", "*Same* defibrillation energy",
                     "Early airway, *100% oxygen*"]},
        {"d": 7, "pill": ("AHA 2025", CYAN), "top": "Arrest recognized?", "big": "PREP DELIVERY NOW",
         "big_size": 84, "sub": "Start preparing at once. Goal: *delivery by 5 min* if no ROSC."},
        {"d": 5, "top": "Call early:", "bottom": "*Obstetric + neonatal teams* the moment the code starts. "
                                                 "ECPR may be reasonable where available."},
    ], caption=cap("Cardiac arrest in pregnancy (AHA 2025): continuous manual left uterine displacement when the "
                   "uterus is at or above the umbilicus, and standard ACLS drugs, doses and shocks.\n\nPreparation "
                   "for resuscitative delivery starts at the recognition of arrest, with the goal of completing "
                   "delivery by 5 minutes. Call OB and neonatal early; ECPR may be reasonable where available.",
                   ["ACLS", "Obstetrics", "LaborAndDelivery", "CodeBlue", "NurseEducator"]),
        shorts_title="Cardiac Arrest in Pregnancy: Prep Delivery From Minute Zero #shorts",
        sources=[AHA25_ACLS_CHANGES,
                 "AHA 2025 algorithm: Cardiac Arrest in Pregnancy — https://cpr.heart.org/-/media/CPR-Files/"
                 "CPR-Guidelines-Files/2025-Algorithms/Algorithm-SC-ACLS-CA-in-Pregnancy-250620.pdf"])


def s13_v2():
    return story("S13_aivr_v2", [
        {"d": 3.2, "hook": True, "top": "Wide rhythm right\n*after the cath lab?*", "top_size": 90,
         "rh": ("aivr", {}, "HR 72")},
        {"d": 5.5, "top": "Wide QRS, regular, rate *50–110*",
         "bottom": "= *AIVR*: accelerated idioventricular rhythm."},
        {"d": 5.5, "top": "Often a *reperfusion* rhythm",
         "bottom": "Common right after the artery is opened (PCI or lytics)."},
        {"d": 7, "top": "Usually *benign* and self-limiting.", "big": "DON'T SUPPRESS", "big_size": 88,
         "big_color": YELLOW, "sub": "Antiarrhythmics can leave *no escape rhythm*. Monitor, check BP."},
        {"d": 6.5, "top": "Not VT:",
         "bullets": ["VT is usually *over 120*", "AIVR is slower, often *well tolerated*",
                     "Symptomatic? *Speed up the sinus rate* (atropine / pacing), don't suppress"]},
    ], caption=cap("Wide, regular rhythm at 50–110 right after reperfusion? That's likely AIVR, accelerated "
                   "idioventricular rhythm.\n\nUsually benign and self-limiting. Suppressing it with "
                   "antiarrhythmics can remove the only escape rhythm. If it causes symptoms (lost atrial kick), "
                   "the fix is to speed up the sinus rate, not to suppress the ventricle.",
                   ["ECG", "CathLab", "CardiacNurse", "Telemetry", "ACLS"]),
        shorts_title="AIVR: The Wide Rhythm You Should NOT Suppress #shorts",
        sources=["AIVR overview (StatPearls) — https://www.ncbi.nlm.nih.gov/books/NBK534815/",
                 "AIVR (LITFL ECG library) — https://litfl.com/accelerated-idioventricular-rhythm-aivr-ecg-library/"])


def s14_v2():
    return story("S14_hypothermia_v2", [
        {"d": 3.2, "hook": True, "top": "That hump right\n*after the QRS?*",
         "rh": ("beats", {"j_amp": 0.35, "hr": 46, "qt": 0.5}, "HR 46 · 29°C")},
        {"d": 5.5, "top": "*Osborn (J) wave*",
         "bottom": "A classic sign of *hypothermia*. Grows as the temperature drops."},
        {"d": 6.5, "top": "Also on the strip:",
         "bullets": ["*Bradycardia*, long intervals", "Shivering artifact", "AFib, then *VF* as it gets colder"]},
        {"d": 7.5, "top": "Hypothermic arrest?", "rh": ("vfib", {}, "HR ---"),
         "bullets": ["*Standard ACLS* + high-quality CPR (AHA)", "*Active rewarming*, ECMO if available",
                     "Some protocols limit shocks/epi *below 30 °C*", "Handle gently: movement can trigger VF"]},
        {"d": 4.5, "top": "Remember:", "big": "NOT DEAD\nUNTIL WARM", "big_size": 92,
         "sub": "A rule of thumb, with exceptions. Follow your protocol."},
    ], caption=cap("That hump right after the QRS is an Osborn (J) wave, a classic sign of hypothermia. 🧊\n\n"
                   "Expect bradycardia, long intervals and shivering artifact, then AFib and VF as it gets colder. "
                   "In arrest: AHA recommends standard ACLS with active rewarming and ECMO where available; some "
                   "protocols (e.g. ERC) limit shocks and epinephrine below 30 °C.",
                   ["Hypothermia", "ECG", "ACLS", "EmergencyMedicine", "Paramedic"]),
        shorts_title="Osborn Waves & Hypothermic Arrest #shorts",
        sources=["AHA Part 10: Special Circumstances of Resuscitation — https://professional.heart.org/en/"
                 "guidelines-statements/part-10-special-circumstances-of-resuscitations501",
                 "ERC Guidelines 2025 Special Circumstances (hypothermia: delay shocks after 3 and withhold "
                 "adrenaline below 30 °C) — https://www.resuscitationjournal.com/article/S0300-9572(25)00265-5/fulltext"])


def s15_v2():
    return story("S15_opioid_v2", [
        {"d": 3.2, "hook": True, "top": "Opioid overdose:\n*breathing or not?*",
         "rh": ("sinus", {"hr": 52}, "HR 52 · RR 4")},
        {"d": 6.5, "top": "Pulse, but not breathing?", "big": "VENTILATE", "big_color": CYAN,
         "sub": "*Bag-mask* right away, *plus naloxone*."},
        {"d": 6.5, "top": "No pulse?", "rh": ("cpr", {}, None), "big": "CPR FIRST",
         "sub": "Naloxone may be reasonable, but *never* at the cost of CPR."},
        {"d": 6, "top": "Naloxone doesn't restart a heart.",
         "bottom": "It reverses *respiratory depression*. Oxygen & ventilation do the rest."},
        {"d": 6, "top": "After reversal:", "rh": ("sinus", {"hr": 96}, "HR 96 · RR 14"),
         "bullets": ["Watch for *re-sedation*", "Withdrawal, agitation, vomiting", "*Monitor*, don't rush discharge"]},
    ], caption=cap("Opioid overdose: pulse but not breathing → ventilate with a bag-mask and give naloxone. No "
                   "pulse → CPR first; naloxone may be reasonable if it doesn't interrupt CPR.\n\nNaloxone treats "
                   "breathing, not cardiac arrest. Watch for re-sedation after reversal.",
                   ["Naloxone", "ACLS", "AHA2025", "EMS", "ERNurse"]),
        shorts_title="Opioid Overdose: Ventilate, Naloxone, CPR First (AHA) #shorts",
        sources=[AHA25_ACLS_CHANGES,
                 "Part 10: Special Circumstances, 2025 AHA Guidelines — "
                 "https://www.ahajournals.org/doi/10.1161/CIR.0000000000001380"])


def s16_v2():
    return story("S16_pad_placement_v2", [
        {"d": 3.2, "hook": True, "top": "Where do the\n*pads* go?", "rh": ("vfib", {}, "HR ---")},
        {"d": 7, "top": "*Anterolateral*: fastest default",
         "bullets": ["Right pad *below the right clavicle*",
                     "Left pad: *mid-axillary line*, level with the apex (V6)"]},
        {"d": 6.5, "top": "*Anteroposterior* works too",
         "bottom": "Front: left chest. Back: left of the spine, *below the scapula.*"},
        {"d": 7.5, "top": "Pad checklist:",
         "bullets": ["Adult pads *over 8 cm*", "*Not over breast tissue*", "Dry skin, remove med patches",
                     "Not *directly over* a pacemaker/ICD"]},
        {"d": 4.5, "top": "Then:", "big": "CLEAR · SHOCK", "big_size": 96, "shock": True},
    ], caption=cap("Defib pad placement (AHA 2025): anterolateral (right pad below the clavicle, left pad on the "
                   "mid-axillary line at the apex) or anteroposterior (left chest + left of the spine below the "
                   "scapula). ⚡\n\nKeep pads off breast tissue and implanted devices, dry the skin, and remove "
                   "med patches.",
                   ["Defibrillation", "ACLS", "BLS", "AHA2025", "CodeBlue"]),
        shorts_title="Defibrillator Pad Placement: AL vs AP (AHA 2025) #shorts",
        sources=["Part 7: Adult BLS, 2025 AHA Guidelines (pad position, >8 cm, no breast tissue) — "
                 "https://www.ahajournals.org/doi/10.1161/CIR.0000000000001369",
                 "Red Cross defibrillation guideline (pad placement) — "
                 "https://guidelines.redcross.org/guidelines-database/defibrillation/"])


def s26_v2():
    return story("S26_team_leader_v2", [
        {"d": 3.2, "hook": True, "top": "What the instructor\nwants to *hear.*", "top_size": 88,
         "rh": ("vfib", {}, "HR ---")},
        {"d": 6.5, "top": "Take charge, out loud:",
         "bottom": "\"I'm the *team leader*. Maria, start compressions. Jay, *pads on.*\""},
        {"d": 6, "top": "*Closed-loop* every order",
         "bottom": "\"Give *epinephrine 1 mg IV.*\" → \"Epi 1 mg *given.*\""},
        {"d": 7, "top": "Rhythm check script:", "shock": True,
         "bottom": "\"Pause. Rhythm? VF. *Resume compressions while I charge.* Charged. Everyone *clear.*\"",
         "bottom_size": 50},
        {"d": 6, "top": "*Summarize* every 2 min", "rh": ("cpr", {}, None),
         "bottom": "\"VF, 3 shocks, epi at 4 min, amio given. *H's & T's?*\""},
    ], caption=cap("Passing the megacode is as much about communication as algorithms. 🗣️\n\nName the roles, "
                   "close the loop on every order, keep compressions going while the defibrillator charges, and "
                   "summarize every 2 minutes. Save this before your ACLS class.",
                   ["Megacode", "ACLS", "Leadership", "NursingStudent", "CodeBlue"]),
        shorts_title="ACLS Megacode: What the Team Leader Should Say #shorts",
        sources=["Part 9: Adult ALS, 2025 AHA Guidelines (minimize pre-shock pause) — "
                 "https://www.ahajournals.org/doi/10.1161/CIR.0000000000001376", AHA25_ACLS_CHANGES])


def s29_v2():
    return story("S29_brugada_v2", [
        {"d": 3.2, "hook": True, "top": "Young, fainted,\n*and this V1.*",
         "rh": ("brugada", {}, "HR 70", None, "V1  ·  FROM 12-LEAD")},
        {"d": 6.5, "top": "*Coved* ST elevation *2 mm or more* + inverted T in V1–V2",
         "bottom": "= *Type 1 Brugada pattern* (on a 12-lead)."},
        {"d": 6, "top": "Rule out *mimics*:",
         "bullets": ["RBBB · anteroseptal STEMI", "*Hyperkalemia*", "Sodium-channel blocker drugs"]},
        {"d": 6.5, "top": "Why it matters:",
         "bullets": ["Inherited *sodium-channel* disorder", "Risk of *VF / sudden death*",
                     "Often young, at night, or *with fever*"]},
        {"d": 7, "top": "What to do:",
         "bullets": ["*Cardiology referral* (ICD if high risk)", "*Treat fever* fast",
                     "Avoid triggering drugs (brugadadrugs.org)"]},
        {"d": 4, "top": "Syncope + this ECG:", "big": "NEVER IGNORE", "big_size": 96},
    ], caption=cap("Type 1 Brugada pattern: coved ST elevation of 2 mm or more with an inverted T wave in V1–V2 "
                   "on a 12-lead. Rule out mimics like RBBB, anteroseptal STEMI, hyperkalemia and sodium-channel "
                   "blocker drugs.\n\nIt's an inherited sodium-channel disorder with risk of VF and sudden death, "
                   "often in young people, at night or with fever. Syncope + this ECG = cardiology now.",
                   ["Brugada", "ECG", "Cardiology", "EmergencyMedicine", "Telemetry"]),
        shorts_title="Brugada Pattern: The V1 You Can't Ignore #shorts",
        sources=["2017 AHA/ACC/HRS Ventricular Arrhythmias & SCD guideline (Brugada) — "
                 "https://www.ahajournals.org/doi/10.1161/CIR.0000000000000549"])


def s32_v2():
    return story("S32_precharge_v2", [
        {"d": 3.2, "hook": True, "top": "Every second\n*off the chest* counts.", "top_size": 92,
         "rh": ("cpr", {}, None)},
        {"d": 6.8, "top": "Charge the defibrillator *during compressions.*",
         "bottom": "Just *before* the rhythm check, so the pause is only look + shock."},
        {"d": 5.5, "top": "Then: *pause · look · shock*", "rh": ("vfib", {}, "HR ---"), "big": "SHOCK",
         "sub": "Pre-shock pause *under 10 s*. Shorter is better.", "shock": True},
        {"d": 5.5, "top": "Not shockable?", "rh": ("beats", {"hr": 76}, NP, RED),
         "bottom": "*Disarm the charge* and resume CPR right away."},
        {"d": 5, "top": "Short pauses = *better survival.*", "rh": ("cpr", {}, None),
         "bottom": "Resume compressions *immediately* after every shock."},
    ], caption=cap("Pre-charge the defibrillator during compressions, just before the rhythm check. ⚡\n\n"
                   "Then pause, look and shock in under 10 s. Not shockable? Disarm and resume CPR. Shorter pauses, "
                   "better outcomes.",
                   ["Defibrillation", "CPR", "ACLS", "CodeBlue", "Megacode"]),
        shorts_title="Pre-Charging the Defibrillator: Cut the Pre-Shock Pause #shorts",
        sources=["Part 9: Adult ALS, 2025 AHA Guidelines (minimize pre/post-shock pauses) — "
                 "https://www.ahajournals.org/doi/10.1161/CIR.0000000000001376"])


FIXES = [s09_v2, s37_choking, s10_v2, s11_v2, s13_v2, s14_v2, s15_v2, s16_v2, s26_v2, s29_v2, s32_v2]

# Upcoming scheduled reels each v2 replaces (swap these in Business Suite).
REPLACES = {"S10_inferior_mi_rv_v2": "S10_inferior_mi_rv_infarct", "S11_arrest_pregnancy_v2": "S11_arrest_in_pregnancy",
            "S13_aivr_v2": "S13_aivr_reperfusion", "S14_hypothermia_v2": "S14_hypothermia_osborn",
            "S15_opioid_v2": "S15_opioid_overdose", "S16_pad_placement_v2": "S16_defib_pad_placement",
            "S26_team_leader_v2": "S26_team_leader_script", "S29_brugada_v2": "S29_brugada_pattern",
            "S32_precharge_v2": "S32_precharge_defib"}
