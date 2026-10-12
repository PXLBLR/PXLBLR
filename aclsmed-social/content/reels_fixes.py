"""Corrections and replacements after the Oct 12 STEMI call-out.

Every reel here carries `sources` (primary references for each on-screen claim) and must pass the
CLINICAL_REVIEW.md gate before it is packaged.
"""
from engine import twelvelead
from engine.brand import CYAN, RED, YELLOW

from .reels_oct8_25 import cap
from .story import story

ECG_12 = twelvelead.render()
ECG_12_MARKED = twelvelead.render(highlight=["V2", "V3", "V4"], recip=["III", "aVF"])

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


FIXES = [s09_v2, s37_choking]
