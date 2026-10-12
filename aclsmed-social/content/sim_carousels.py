"""ACLSMED Sim (iPad) lead-magnet carousels: "comment a keyword → get the link by DM".

Feature claims are limited to what MASTER-MD marks shipped: Instructor Remote drives rhythm + vitals live,
Monitor shows them with defib / pacer / CPR, 4-digit pairing, Code Summary event log, AHA 2025.
"""
from engine.brand import CYAN, RED, YELLOW

SIM_GREEN = (97, 255, 170)  # iOS ECG green (#61FFAA)


def scen(n, title, patient, rhythm, kw, label, instructor, team, color=SIM_GREEN):
    return [("kicker", f"SCENARIO {n:02d} / 10", RED if n % 2 else CYAN), ("title", title, 64),
            ("body", patient, 36), ("ecg", rhythm, kw, label, color, 200, 4),
            ("scenario", instructor, team)]


SIM1 = {"id": "SIM1_10_megacodes_2_ipads", "slides": [
    [("kicker", "ACLSMED SIM  ·  iPAD"), ("title", "10 megacodes you can\nrun with *2 iPads*", 84),
     ("devices", "vfib", {}, "VF", "VF"),
     ("body", "The instructor drives the rhythm. The team runs the code. Save this for your next *skills day*.", 38),
     ("swipe",)],
    [("kicker", "HOW IT WORKS", CYAN), ("title", "One iPad drives.\nOne iPad *is the patient.*", 70),
     ("devices", "sinus", {"hr": 38}, "HR 38", "BRADY"),
     ("bullets", ["Pair the iPads with a *4-digit code*", "Instructor picks the *rhythm & vitals*, live",
                  "Team works the code on the Monitor: *defib, pacer, CPR*"], 38)],
    scen(1, "Brady that *won't respond*", "78M, dizzy, BP 78/40.", "chb", {}, "II  ·  HR 34",
         "Sinus brady 38 → no response to atropine → *complete heart block* 34.",
         "Atropine *1 mg* → pads on → *pace*, confirm mechanical capture. Epi/dopamine drip as a bridge."),
    scen(2, "Unstable *SVT*", "34F, palpitations, BP 82/50, confused.", "svt", {"hr": 192}, "II  ·  HR 192",
         "SVT 192, then drop the BP into the 70s. Run it again *stable* to test vagal → adenosine.",
         "Unstable → *synchronized cardioversion* (sedate if possible). Stable → vagal → *adenosine 6 → 12 mg*."),
    scen(3, "AFib RVR + *hypotension*", "71M, AFib at 150, BP 76/44.", "afib", {"mean_hr": 150},
         "II  ·  HR 150 IRREG",
         "AFib 150, BP drifting down after each delay.",
         "*SYNC* cardioversion, initial *at least 200 J* biphasic (AHA 2025). Re-check SYNC after every shock."),
    scen(4, "Witnessed *VF*", "62M collapses in the hallway.", "vfib", {}, "II  ·  VF", "VF from the first second. Keep VF through shock 3.",
         "Shock → *CPR 2 min* → shock → *epi 1 mg* → shock → *amiodarone 300 mg*. Pauses under 10 s."),
    scen(5, "Wide, fast, *no pulse*", "55F, post-MI day 2, unresponsive.", "vt", {"hr": 180}, "II  ·  VT 180",
         "Monomorphic VT 180, BP/SpO2 go to dashes.",
         "Pulseless VT = treat like VF: *unsynchronized* shock, CPR, epi, antiarrhythmic."),
    scen(6, "PEA in a *dialysis* patient", "58M, missed dialysis twice.", "beats",
         {"hr": 56, "qrs_w": 0.16, "wide": True}, "II  ·  NO PULSE",
         "Wide, slow organized rhythm. No pulse.",
         "CPR + *epi ASAP*. Wide-QRS PEA → think *hyperkalemia*: calcium per protocol. Hunt the H's & T's.", RED),
    scen(7, "The *flat line*", "80F found unresponsive in bed.", "asystole", {}, "II  ·  ASYSTOLE",
         "Flat line. Watch who checks leads and gain first.",
         "Check *leads & gain*, second lead → *CPR + epi ASAP* → every 3–5 min. Never shock asystole."),
    scen(8, "It *twists*", "49F on methadone, QTc 560.", "torsades", {}, "II  ·  TORSADES",
         "Torsades with a pulse → lose the pulse at 60 s.",
         "Pulse: *magnesium 1–2 g IV*. No pulse: *defibrillate*, CPR, then Mg. Stop QT-prolonging drugs."),
    scen(9, "Inferior STEMI + *brady*", "66M, chest pressure, HR 44, BP 84/50.", "beats",
         {"st": 0.45, "t_amp": 0.4, "hr": 44}, "III  ·  ST ↑",
         "Inferior ST elevation, slow and soft BP. Offer nitro and see who stops it.",
         "Aspirin, right-sided ECG, *avoid nitrates* (RV infarct), fluids, *cath lab*, pacer ready."),
    scen(10, "You got *ROSC*. Now what?", "Same patient as Scenario 4, 6 min later.", "sinus", {"hr": 96},
         "II  ·  HR 96  ·  ROSC",
         "Snap to sinus 96, BP 84/50, SpO2 88%.",
         "MAP *65+*, SpO2 *90–98%*, PaCO2 35–45, *12-lead*, temperature control if not following commands."),
    [("kicker", "DEBRIEF", YELLOW), ("title", "Then debrief with the\n*Code Summary*", 70),
     ("bullets", ["Every *rhythm change, shock and CPR* start/stop, timestamped",
                  "Walk the timeline: *when was epi due?* How long were the pauses?",
                  "Reset and run it again in seconds"], 40),
     ("callout", "Educational only, not diagnostic. Built by an ICU nurse. Aligned to *AHA 2025*.", CYAN)],
    [("leadcta", "SIM", "We'll DM you the *App Store link* for ACLSMED Sim.",
      "iPad app · Instructor + Monitor · Educational only, not diagnostic. Verify all care against AHA 2025 and "
      "your institution's protocols.")],
]}

CAPTION = """10 megacodes you can run tomorrow with 2 iPads. 🫀⚡

One iPad is the instructor remote: pick the rhythm, drop the BP, lose the pulse. The other iPad is the patient monitor your team works on, with defib, pacer and CPR. Debrief from the timestamped Code Summary.

Comment SIM and we'll DM you the App Store link for ACLSMED Sim.

Save this for your next skills day.

Educational only. Follow AHA 2025 guidelines and your institution's protocols.

#ACLS #Megacode #NurseEducator #Simulation #CodeBlue"""

DM_REPLY = """Here's ACLSMED Sim 👉 [App Store link]

Run it on 2 iPads: one as the Instructor Remote, one as the Monitor. Pair them with the 4-digit code and start with Scenario 01 (brady that won't respond).

Educational only, not diagnostic."""

ALT = ("Carousel promoting the ACLSMED Sim iPad app. Slide 1: '10 megacodes you can run with 2 iPads' with a "
       "schematic of an instructor iPad driving a patient monitor iPad showing VF. Slide 2: how it works, pairing "
       "with a 4-digit code. Slides 3 to 12: ten scenario cards (symptomatic bradycardia to complete heart block, "
       "unstable SVT, AFib with hypotension, witnessed VF, pulseless VT, PEA in a dialysis patient, asystole, "
       "torsades, inferior STEMI with bradycardia, post-ROSC care), each with an ECG strip, what the instructor "
       "does, and what the team must do. Slide 13: debrief with the Code Summary. Slide 14: comment SIM to get the "
       "App Store link by DM.")

SIM_CAROUSELS = [SIM1]


# ---- v2: fixes from the Oct 12 clinical audit (SIM1 was never posted) ----
import copy  # noqa: E402

from engine import twelvelead  # noqa: E402

AHA25_ACLS_CHANGES = ("AHA 2025 Interim Training Materials: ACLS Provider Manual Changes (cardioversion doses, "
                      "polymorphic VT) — https://cpr.heartandstroke.ca/resource/Guidelines2025InterimACLSProviderManualEN")
INF_SIM = twelvelead.render(twelvelead.INFERIOR_STEMI, width=936, height=360, hr=44,
                            highlight=["II", "III", "aVF"], recip=["I", "aVL"])

SIM1_V2 = copy.deepcopy(SIM1)
SIM1_V2["id"] = "SIM1_10_megacodes_2_ipads_v2"
S = SIM1_V2["slides"]
S[2] = scen(1, "Brady that *won't respond*", "78M, dizzy, BP 78/40.", "chb", {"vent": 34}, "II  ·  HR 34",
            "Sinus brady 38 → no response to atropine → *complete heart block* 34.",
            "Atropine *1 mg* → pads on → *pace* (analgesia/sedation), confirm mechanical capture. "
            "Epi/dopamine drip as a bridge.")
S[3] = scen(2, "Unstable *SVT*", "34F, palpitations, BP 82/50, confused.", "svt", {"hr": 192}, "II  ·  HR 192",
            "SVT 192, then drop the BP into the 70s. Run it again *stable* to test vagal → adenosine.",
            "Unstable → *synchronized cardioversion, 100 J* (AHA 2025; sedate if possible). "
            "Stable → vagal → *adenosine 6 → 12 mg*.")
S[8] = scen(7, "The *flat line*", "80F found unresponsive in bed.", "asystole", {}, "II  ·  ASYSTOLE",
            "Flat line. Watch whether CPR starts *before* anyone fiddles with the monitor.",
            "*CPR now.* Confirm the flat line (leads, gain, 2nd lead) without pausing. *Epi ASAP* → every 3–5 min. "
            "Never shock asystole.")
S[9] = scen(8, "It *twists*", "49F on methadone, QTc 560.", "torsades", {}, "II  ·  TORSADES",
            "Torsades with a pulse and soft BP → lose the pulse at 60 s.",
            "Unstable or pulseless: *defibrillate* (not synced), CPR if no pulse, then *Mg 1–2 g IV*. "
            "Stable: *Mg 1–2 g IV*. Stop QT-prolonging drugs.")
S[10] = [("kicker", "SCENARIO 09 / 10", RED), ("title", "Inferior STEMI + *brady*", 64),
         ("body", "66M, chest pressure, HR 44, BP 84/50.", 34), ("image", INF_SIM),
         ("scenario", "Show the *12-lead*: inferior ST elevation, reciprocal I/aVL. Soft BP. Offer nitro and see "
                      "who stops it.",
          "*V4R*. Aspirin, *no nitrates* (SBP under 90, HR 44, RV infarct), fluid bolus if lungs clear, "
          "*atropine 1 mg* → pace if no response, *cath lab*.")]
S[4] = scen(3, "AFib RVR + *hypotension*", "71M, AFib at 150, BP 76/44.", "afib", {"mean_hr": 150},
            "II  ·  HR 150 IRREG", "AFib 150, BP drifting down after each delay.",
            "*SYNC* cardioversion (sedate if possible), *200 J* initial (AHA 2025). Re-check SYNC after every shock.")
SIM1_V2["sources"] = [
    AHA25_ACLS_CHANGES,
    "Fourth Universal Definition of MI (STEMI on a 12-lead) — https://www.ahajournals.org/doi/10.1161/CIR.0000000000000617",
    "2013 ACCF/AHA STEMI guideline (RV infarction, V4R, nitrates) — "
    "https://www.ahajournals.org/doi/10.1161/CIR.0b013e3182742cf6",
    "AHA 2025 Bradycardia algorithm (atropine 1 mg, pacing, drips) — https://cpr.heart.org/-/media/CPR-Files/"
    "CPR-Guidelines-Files/2025-Algorithms/Algorithm-ACLS-Bradycardia-250514.pdf",
]
ALT_V2 = ALT.replace("each with an ECG strip", "each with an ECG strip (Scenario 9: a 12-lead)")
SIM_CAROUSELS = [SIM1_V2]
