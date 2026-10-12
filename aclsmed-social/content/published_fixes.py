"""Corrected versions of already-published items flagged by the Oct 12 clinical audit.

Instagram can't swap the media on a live post, so each of these replaces a post that is deleted (or
archived) and re-posted. HIGH: C2, S03. MED: R3, C6.
"""
import copy

from engine.brand import CYAN

from .carousels import C2, C6
from .reels_fixes import AHA25_ACLS_CHANGES
from .reels_oct8_25 import cap
from .story import story

AF_2023 = ("2023 ACC/AHA/ACCP/HRS Atrial Fibrillation guideline (pre-excited AF: IV beta-blockers, diltiazem, "
           "verapamil, digoxin, adenosine and amiodarone potentially harmful) — "
           "https://www.ahajournals.org/doi/10.1161/CIR.0000000000001193")


def s03_v2():
    return story("S03_wpw_preexcited_af_v2", [
        {"d": 3.2, "hook": True, "top": "See that *slur*\nbefore the QRS?", "rh": ("beats", {"delta": True}, "HR 72")},
        {"d": 6, "top": "Short PR + *delta wave* + wide QRS",
         "bottom": "= *WPW pattern*: an extra pathway that *skips the AV node.*"},
        {"d": 5.5, "top": "Now AFib travels down that pathway.", "rh": ("preexcited_af", {}, "HR 250 IRREG"),
         "bottom": "Irregular, very fast, *wide & bizarre* complexes.", "sfx": [(0, "alarm", 0.6)]},
        {"d": 7, "top": "Do *NOT* give these:", "big": "AVOID",
         "sub": "Adenosine · beta-blockers · diltiazem/verapamil · digoxin · *IV amiodarone*",
         "bottom": "They can push *more* impulses down the pathway → *VF*.", "bottom_size": 44},
        {"d": 6.5, "top": "So what works?",
         "bullets": ["Unstable → *synchronized cardioversion*", "Stable → *procainamide* or *ibutilide*",
                     "Get *expert consult*"]},
    ], caption=cap("Updated version: we've added IV amiodarone to the avoid list.\n\nShort PR + delta wave = WPW "
                   "pattern. Put AFib on top of it and you get irregular, very fast, wide complexes.\n\nAvoid "
                   "adenosine, beta-blockers, diltiazem/verapamil, digoxin and IV amiodarone; they can push the "
                   "rhythm into VF. Unstable → synchronized cardioversion. Stable → procainamide or ibutilide + "
                   "expert consult.",
                   ["WPW", "ECG", "ACLS", "EmergencyMedicine", "CardiacNurse"]),
        shorts_title="WPW + AFib: What Never to Give (Incl. Amiodarone) #shorts",
        sources=[AF_2023])


def r03_v2():
    return story("R3_torsades_v2", [
        {"d": 3.2, "hook": True, "top": "This rhythm\n*twists.*", "top_size": 110,
         "rh": ("torsades", {}, "HR 250"), "open_sfx": "alarm"},
        {"d": 5.5, "top": "Polymorphic VT + a *long QT*\n= *Torsades de Pointes*",
         "bottom": "QRS spirals around the baseline: tall, tiny, tall."},
        {"d": 6, "top": "*Unstable* (even with a pulse) or pulseless?", "big": "DEFIBRILLATE",
         "big_size": 100, "sub": "Defibrillation dose, *not synchronized*. CPR if no pulse.", "shock": True},
        {"d": 6, "top": "*Stable*, with a pulse?", "big": "MAGNESIUM", "big_color": CYAN,
         "sub": "*1–2 g IV*, per protocol. Get expert help."},
        {"d": 7, "top": "Then fix *why* the QT is long", "rh": ("sinus", {"hr": 72, "t_amp": 0.22}, "HR 72"),
         "bullets": ["Stop QT-prolonging drugs", "Correct *low K+ and low Mg*",
                     "Review the MAR: antiarrhythmics, antipsychotics, some antibiotics"]},
    ], caption=cap("Updated version: unstable torsades gets defibrillated even with a pulse.\n\nTorsades de "
                   "pointes is polymorphic VT with a long QT. Unstable or pulseless → defibrillation dose, not "
                   "synchronized (AHA 2025). Stable with a pulse → magnesium 1–2 g IV. Then stop QT-prolonging drugs "
                   "and correct K+ and Mg.",
                   ["ACLS", "TorsadesDePointes", "ECG", "ICUNurse", "Paramedic"]),
        shorts_title="Torsades: Shock if Unstable, Magnesium if Stable #shorts",
        sources=[AHA25_ACLS_CHANGES,
                 "Part 9: Adult ALS, 2025 AHA Guidelines (magnesium for torsades with long QT) — "
                 "https://www.ahajournals.org/doi/10.1161/CIR.0000000000001376"])


C2_V2 = copy.deepcopy(C2)
C2_V2["id"] = "C2_stable_vs_unstable_tachy_v2"
C2_V2["slides"][3] = [
    ("kicker", "UNSTABLE  →  SHOCK IT"), ("title", "*Synchronized*\ncardioversion", 84),
    ("bullets", ["Sedate if possible, but *don't delay* for a crashing patient",
                 "Press *SYNC*, look for markers on each R wave, re-check after *every* shock"], 36),
    ("stats", [("Narrow-complex", "100 J", "AHA 2025 initial synchronized dose"),
               ("Monomorphic VT", "100 J", None),
               ("AFib / flutter", "200 J", None),
               ("Polymorphic VT", "DEFIB", "Defibrillation dose, *NOT synchronized*")])]
C2_V2["slides"][4][1][2][3] = ["Wide, irregular", "Expert consult", "*No* AV-nodal blockers or IV amiodarone if "
                               "pre-excited"]
C2_V2["sources"] = [AHA25_ACLS_CHANGES, AF_2023]
C2_V2["caption_note"] = ("Updated version: AHA 2025 set fixed starting doses for synchronized cardioversion "
                         "(narrow 100 J, monomorphic VT 100 J, AFib/flutter 200 J) and polymorphic VT gets a "
                         "defibrillation dose, not synchronized.")

C6_V2 = copy.deepcopy(C6)
C6_V2["id"] = "C6_megacode_mistakes_v2"
C6_V2["slides"][3] = [
    ("kicker", "MISTAKE 3"), ("title", "Wrong defib mode", 72),
    ("wrongright", "SYNC on for VF (it may never fire) · or no SYNC for unstable AFib with a pulse",
     "Pulseless VF/pVT: *unsynchronized*. Unstable tachy *with a pulse*: *SYNC*, re-checked each shock, "
     "*except polymorphic VT: defibrillate*")]
C6_V2["sources"] = [AHA25_ACLS_CHANGES]
C6_V2["caption_note"] = "Updated version: unstable polymorphic VT gets defibrillated, not synchronized."

REELS_PUB = [s03_v2, r03_v2]
CAROUSELS_PUB = [C2_V2, C6_V2]
REPLACES_PUB = {"S03_wpw_preexcited_af_v2": "S03 (posted Oct 9)", "R3_torsades_v2": "R3 (posted Oct 3)",
                "C2_stable_vs_unstable_tachy_v2": "C2 (posted Oct 2)", "C6_megacode_mistakes_v2": "C6 (posted Oct 6)"}

