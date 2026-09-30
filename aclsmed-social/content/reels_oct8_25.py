"""Oct 8–25, 2026: 36 faceless, voiceless reels / Shorts (2 per day). New topics only, none repeat Oct 1–7.

Clinical content aligned to AHA 2025 Guidelines (Parts 9, 10, 11) and standard ACLS teaching.
"""
from engine.brand import CYAN, RED, YELLOW

from .story import story

DISC = "Educational only. Follow AHA 2025 guidelines and your institution's protocols."
NP = "NO PULSE"


def cap(body, tags):
    return f"{body}\n\n{DISC}\n\n" + " ".join("#" + t for t in tags)


def r01():
    return story("S01_atrial_flutter_150", [
        {"d": 3.2, "hook": True, "top": "HR stuck at\nexactly *150?*", "rh": ("aflutter", {"conduction": 2}, "HR 150")},
        {"d": 6, "top": "Regular, narrow, and it *never changes.*",
         "bottom": "Classic *2:1 atrial flutter*: atria ~300, ventricles 150."},
        {"d": 6, "top": "Where are the flutter waves?",
         "bottom": "Hidden in the QRS and T. Look for a *sawtooth* in II, III, aVF."},
        {"d": 7, "top": "Slow the AV node and they *appear.*",
         "rh": ("sequence", {"parts": [("aflutter", 5.8, {"conduction": 2}), ("aflutter", 9, {"conduction": 4})]}, None),
         "bottom": "Vagal maneuvers or adenosine can *unmask* the sawtooth. Diagnostic, not a cure."},
        {"d": 5.5, "top": "Unstable? *Synchronized cardioversion.*",
         "bottom": "AHA 2025: an initial *200 J* may be reasonable for flutter.", "shock": True},
    ], caption=cap("HR stuck at exactly 150 and it never budges? Think atrial flutter with 2:1 block. 🪚\n\n"
                   "Atria fire around 300/min and the AV node lets every second one through. The flutter waves hide "
                   "in the QRS and T waves until you slow the AV node down.",
                   ["AtrialFlutter", "ECG", "ACLS", "Telemetry", "ICUNurse"]),
        shorts_title="Atrial Flutter: Why a Heart Rate of Exactly 150 Is a Clue #shorts")


def r02():
    return story("S02_vf_loop_40s", [
        {"d": 3, "hook": True, "top": "The VF loop\nin *40 seconds.*", "rh": ("vfib", {}, "HR ---")},
        {"d": 6, "pill": ("SHOCK 1", RED), "top": "Defibrillate, then *CPR 2 min*. No pulse check.",
         "big": "SHOCK", "sub": "Biphasic: manufacturer dose (often 120–200 J).", "shock": True},
        {"d": 5, "pill": ("CPR 2 MIN", CYAN), "top": "Get *IV access* (IO if IV fails).", "rh": ("cpr", {}, None),
         "bottom": "Charge the defibrillator *before* the rhythm check."},
        {"d": 6.5, "pill": ("SHOCK 2", RED), "top": "Still VF? Shock, *then epinephrine.*", "rh": ("vfib", {}, "HR ---"),
         "big": "EPI 1 mg", "big_color": CYAN, "sub": "Every 3–5 min. Consider an *advanced airway*.", "shock": True},
        {"d": 6.5, "pill": ("SHOCK 3", RED), "top": "Still VF? Shock, then *antiarrhythmic.*",
         "big": "AMIO 300 mg", "big_size": 100, "sub": "or *lidocaine 1–1.5 mg/kg*. Next amio dose: *150 mg*.",
         "shock": True},
        {"d": 4.5, "top": "Repeat the loop. Hunt the *H's & T's.*", "bottom": "*ROSC?* Move to post-arrest care."},
    ], caption=cap("The shockable arrest algorithm in 40 seconds. ⚡\n\nShock → CPR 2 min → shock → epinephrine → "
                   "shock → amiodarone (or lidocaine). Charge before every rhythm check and keep pauses short.",
                   ["ACLS", "VFib", "Megacode", "CodeBlue", "ParamedicLife"]),
        shorts_title="The VF Cardiac Arrest Algorithm in 40 Seconds #shorts")


def r03():
    return story("S03_wpw_preexcited_af", [
        {"d": 3.2, "hook": True, "top": "See that *slur*\nbefore the QRS?", "rh": ("beats", {"delta": True}, "HR 72")},
        {"d": 6, "top": "Short PR + *delta wave* + wide QRS",
         "bottom": "= *WPW*: an extra pathway that *skips the AV node.*"},
        {"d": 5.5, "top": "Now AFib travels down that pathway.", "rh": ("preexcited_af", {}, "HR 250 IRREG"),
         "bottom": "Irregular, very fast, *wide & bizarre* complexes.", "sfx": [(0, "alarm", 0.6)]},
        {"d": 6.5, "top": "Do *NOT* block the AV node.", "big": "AVOID",
         "sub": "Adenosine · beta-blockers · diltiazem/verapamil · digoxin",
         "bottom": "They push *more* impulses down the pathway → *VF*.", "bottom_size": 44},
        {"d": 6.5, "top": "So what works?",
         "bullets": ["Unstable → *synchronized cardioversion*", "Stable → *procainamide* (or ibutilide)",
                     "Get *expert consult*"]},
    ], caption=cap("Delta wave + short PR = WPW. Put AFib on top of it and you get irregular, very fast, wide "
                   "complexes.\n\nDon't block the AV node (adenosine, beta-blockers, CCBs, digoxin). It can push "
                   "the rhythm into VF. Unstable → cardiovert. Stable → procainamide + expert consult.",
                   ["WPW", "ECG", "ACLS", "EmergencyMedicine", "CardiacNurse"]),
        shorts_title="WPW + AFib: The One Time You Never Give Adenosine #shorts")


def r04():
    return story("S04_wide_complex_assume_vt", [
        {"d": 3.2, "hook": True, "top": "Wide & fast.\nSVT or *VT?*", "rh": ("vt", {"hr": 170}, "HR 170")},
        {"d": 6, "top": "Wide QRS, regular, fast.",
         "bottom": "Might be SVT with aberrancy, but *assume VT* until proven otherwise."},
        {"d": 6.5, "top": "Why assume VT?",
         "bullets": ["Most wide-complex tachycardias *are* VT", "Even more likely with *prior MI / heart disease*",
                     "Treating VT as SVT can cause *collapse*"]},
        {"d": 7, "top": "Stable, with a pulse?",
         "bullets": ["12-lead + *expert consult*", "Adenosine *only* if regular & monomorphic",
                     "Antiarrhythmic: *procainamide, amiodarone* or *sotalol*"]},
        {"d": 6, "top": "Unstable?", "big": "SYNC", "sub": "*Synchronized cardioversion.* Pulseless = defibrillate.",
         "shock": True},
    ], caption=cap("Wide, regular, fast: SVT with aberrancy or VT? At the bedside, assume VT. 🫀\n\nMost wide-complex "
                   "tachycardias are VT, especially with prior MI. Stable → 12-lead, expert consult, antiarrhythmic. "
                   "Unstable → synchronized cardioversion.",
                   ["VTach", "ECG", "ACLS", "ERNurse", "CriticalCare"]),
        shorts_title="Wide Complex Tachycardia: Why You Assume VT #shorts")


def r05():
    return story("S05_iv_before_io_2025", [
        {"d": 3.2, "hook": True, "top": "IV or IO\nin cardiac arrest?", "rh": ("cpr", {}, None)},
        {"d": 6, "pill": ("AHA 2025 UPDATE", CYAN), "top": "Try *IV access first.*",
         "bottom": "IV-first is now suggested over IO-first for adults in arrest."},
        {"d": 6.5, "top": "Why the change?",
         "bottom": "3 large trials: starting with *IO* didn't improve outcomes and may *lower ROSC*."},
        {"d": 6, "top": "IV not happening?", "big": "GO IO", "big_color": CYAN,
         "sub": "After *2 failed IV attempts*. Don't let access delay drugs."},
        {"d": 6, "top": "Either way:",
         "bullets": ["Never pause *compressions* for access", "*Flush* after every push", "*Same doses* IV or IO"]},
    ], caption=cap("AHA 2025 update: for adults in cardiac arrest, try IV access first. 💉\n\nThree large trials "
                   "found IO-first didn't improve outcomes. If IV can't be placed within 2 attempts, go IO. Access "
                   "should never delay drugs or interrupt compressions.",
                   ["ACLS", "AHA2025", "IVAccess", "Paramedic", "ERNurse"]),
        shorts_title="IV vs IO in Cardiac Arrest: What Changed in AHA 2025 #shorts")


def r06():
    return story("S06_junctional_rhythm", [
        {"d": 3.2, "hook": True, "top": "Where did the\n*P waves* go?", "rh": ("junctional", {}, "HR 48")},
        {"d": 6, "top": "Narrow QRS, rate *40–60*, no P before the QRS.",
         "bottom": "= *Junctional rhythm*. The AV junction took over."},
        {"d": 6, "top": "Look *after* the QRS.",
         "bottom": "Inverted (retrograde) P waves can hide right after it, or inside it."},
        {"d": 6.5, "top": "Faster versions:",
         "bullets": ["*60–100*: accelerated junctional", "*Over 100*: junctional tachycardia",
                     "Think: *digoxin*, ischemia, post-cardiac surgery"]},
        {"d": 6, "top": "Symptomatic?",
         "bottom": "Treat like bradycardia: *atropine 1 mg*, then pacing or a drip. *Fix the cause.*"},
    ], caption=cap("No P waves, narrow QRS, rate 40–60: the AV junction is running the show. Look just after the QRS "
                   "for inverted, retrograde P waves.\n\nFaster junctional rhythms? Think digoxin toxicity, ischemia "
                   "or post-op. Symptomatic → bradycardia algorithm.",
                   ["ECG", "Junctional", "Telemetry", "NursingStudent", "ACLS"]),
        shorts_title="Junctional Rhythm: Where Did the P Waves Go? #shorts")


def r07():
    return story("S07_sinus_tach_vs_svt", [
        {"d": 3.2, "hook": True, "top": "Don't cardiovert\n*sinus tach.*", "rh": ("sinus", {"hr": 138}, "HR 138")},
        {"d": 6.5, "top": "Rate 100–150, *P waves visible*, changes with activity.",
         "bottom": "= *Sinus tachycardia*: a symptom, not the disease."},
        {"d": 6.5, "top": "Rate often 150+, *no visible P*, starts & stops *abruptly*.",
         "rh": ("svt", {"hr": 188}, "HR 188"), "bottom": "= *SVT* (reentry). Rate locked, doesn't vary."},
        {"d": 6.5, "top": "Sinus tach? Find the *why:*", "rh": ("sinus", {"hr": 138}, "HR 138"),
         "bullets": ["Pain, fever, anxiety", "*Hypovolemia*, bleeding, sepsis", "Hypoxia, PE, drugs, withdrawal"]},
        {"d": 5.5, "top": "Shocking sinus tach", "big": "WON'T FIX IT", "big_size": 96,
         "sub": "Treat the cause: fluids, analgesia, oxygen, antipyretics."},
    ], caption=cap("Sinus tach or SVT? Look for P waves, the rate (usually under 150 vs 150+), and whether it "
                   "starts and stops abruptly.\n\nSinus tach is the body compensating for something. Treat the fever, "
                   "pain, bleeding or hypoxia, not the monitor.",
                   ["SVT", "ECG", "ACLS", "NursingSchool", "Telemetry"]),
        shorts_title="Sinus Tachycardia vs SVT: How to Tell in Seconds #shorts")


def r08():
    return story("S08_pea_narrow_vs_wide", [
        {"d": 3.2, "hook": True, "top": "PEA? Check\nthe *QRS width.*", "rh": ("beats", {"hr": 118}, NP, RED)},
        {"d": 7, "top": "*Narrow* QRS PEA → think *mechanical*",
         "bullets": ["Tamponade", "Tension pneumothorax", "Massive PE · hypovolemia"]},
        {"d": 7, "top": "*Wide* QRS PEA → think *metabolic*",
         "rh": ("beats", {"hr": 58, "qrs_w": 0.16, "wide": True}, NP, RED),
         "bullets": ["*Hyperkalemia*", "Sodium-channel blocker toxins", "Severe acidosis · massive MI"]},
        {"d": 6, "top": "Ultrasound at the pulse check helps",
         "bottom": "Tamponade, RV strain, empty ventricle, but keep the pause *under 10 s*.", "bottom_size": 50},
        {"d": 4.5, "top": "The basics never change:", "rh": ("cpr", {}, None),
         "bottom": "*CPR + epinephrine ASAP*, then treat the cause."},
    ], caption=cap("A practical PEA shortcut: look at the QRS width. 🔍\n\nNarrow → mechanical problems (tamponade, "
                   "tension pneumo, PE, hypovolemia). Wide → metabolic or toxic (hyperkalemia, sodium-channel "
                   "blockers, acidosis). CPR and epi ASAP either way.",
                   ["PEA", "ACLS", "CodeBlue", "EmergencyMedicine", "CriticalCare"]),
        shorts_title="PEA Arrest: The Narrow vs Wide QRS Shortcut #shorts")


def r09():
    return story("S09_stemi_time_is_muscle", [
        {"d": 3.2, "hook": True, "top": "Chest pain +\n*this ST segment?*",
         "rh": ("beats", {"st": 0.5, "t_amp": 0.45, "hr": 88}, "ST ↑")},
        {"d": 5.5, "top": "ST elevation in *2 contiguous leads*", "bottom": "= *STEMI* until proven otherwise."},
        {"d": 7.5, "top": "The clock:",
         "bullets": ["12-lead within *10 min* of arrival", "Door-to-balloon *90 min* or less",
                     "No PCI? Fibrinolysis within *30 min*"]},
        {"d": 7, "top": "Meanwhile:",
         "bullets": ["*Aspirin* (no contraindication)", "Oxygen *only if SpO2 under 90%*",
                     "Nitro for pain, *not* if hypotensive or RV infarct"]},
        {"d": 4.5, "top": "Activate the cath lab *early.*", "big": "TIME = MUSCLE", "big_size": 92},
    ], caption=cap("ST elevation in 2 contiguous leads + chest pain = STEMI until proven otherwise. ⏱️\n\n12-lead in "
                   "10 min. Door-to-balloon in 90 min or less. No PCI center? Fibrinolysis within 30 min. Aspirin, "
                   "oxygen only if SpO2 under 90%, and careful with nitro.",
                   ["STEMI", "ECG", "ACLS", "CardiacNurse", "EmergencyMedicine"]),
        shorts_title="STEMI: The Time Targets Every Nurse Should Know #shorts")


def r10():
    return story("S10_inferior_mi_rv_infarct", [
        {"d": 3.2, "hook": True, "top": "Inferior STEMI?\nCheck the *right side.*",
         "rh": ("beats", {"st": 0.45, "t_amp": 0.4, "hr": 56}, "ST ↑", None, "III")},
        {"d": 5.5, "top": "ST elevation in *II, III, aVF*",
         "bottom": "Many also involve the *right ventricle.*"},
        {"d": 5.5, "top": "Get a *right-sided ECG*", "bottom": "ST elevation in *V4R* supports RV infarction."},
        {"d": 6.5, "top": "RV infarct = *preload dependent*", "big": "AVOID NITRATES", "big_size": 84,
         "big_color": YELLOW, "sub": "They can crash the BP. Hypotension → *IV fluids*."},
        {"d": 6, "top": "Also watch for:",
         "bullets": ["*Bradycardia* & AV block", "Hypotension with *clear lungs*", "Fast reperfusion is the fix"]},
    ], caption=cap("Inferior STEMI (II, III, aVF)? Get a right-sided ECG and look at V4R before you reach for the "
                   "nitro.\n\nRV infarcts are preload dependent. Nitrates can drop the BP fast. Treat hypotension "
                   "with fluids and get them to reperfusion.",
                   ["STEMI", "ECG", "CardiacNurse", "ACLS", "ICUNurse"]),
        shorts_title="Inferior STEMI: Why You Check V4R Before Nitro #shorts")


def r11():
    return story("S11_arrest_in_pregnancy", [
        {"d": 3.2, "hook": True, "top": "Cardiac arrest\nin *pregnancy.*", "rh": ("cpr", {}, None)},
        {"d": 6.5, "top": "Uterus at or above the navel?", "big": "LEFT UTERINE\nDISPLACEMENT", "big_size": 76,
         "big_color": CYAN, "sub": "*Manual* and continuous. Relieves aortocaval compression."},
        {"d": 6.5, "top": "Nothing else changes:",
         "bullets": ["*Same* compressions, drugs & doses", "*Same* defibrillation energy",
                     "Early airway, *100% oxygen*"]},
        {"d": 7, "top": "No ROSC by *4 minutes?*", "big": "DELIVER BY 5 MIN", "big_size": 84,
         "sub": "*Resuscitative cesarean* (20+ weeks) helps mom *and* baby."},
        {"d": 4.5, "top": "Call early:", "bottom": "*Obstetric + neonatal teams* the moment the code starts."},
    ], caption=cap("Cardiac arrest in pregnancy: continuous manual left uterine displacement, standard ACLS "
                   "drugs, doses and shocks, early airway.\n\nNo ROSC by 4 minutes at 20+ weeks → resuscitative "
                   "cesarean, aiming for delivery by 5 minutes. Call OB and neonatal early.",
                   ["ACLS", "Obstetrics", "LaborAndDelivery", "CodeBlue", "NurseEducator"]),
        shorts_title="Cardiac Arrest in Pregnancy: The 4-Minute Rule #shorts")


def r12():
    return story("S12_artifact_vs_vf", [
        {"d": 3.4, "hook": True, "top": "VF on the monitor…\nand she's *talking.*", "top_size": 88,
         "rh": ("artifact", {"start_noise": 5.0}, "HR 80")},
        {"d": 6, "top": "Look at the *patient*, not just the screen.",
         "bottom": "Brushing teeth, shivering, a loose lead: all can *mimic VF.*"},
        {"d": 7, "top": "Spot the artifact:",
         "bullets": ["*Normal QRS marching through* the chaos", "Awake, talking, *has a pulse*",
                     "Pleth / other leads look normal"]},
        {"d": 5, "top": "Unresponsive, *no pulse?*", "rh": ("vfib", {}, "HR ---"), "big": "SHOCK",
         "sub": "That's real VF.", "shock": True},
        {"d": 4.5, "top": "Never shock a *conscious* patient.", "rh": ("sinus", {"hr": 80}, "HR 80"),
         "bottom": "Assess first. It takes 5 seconds."},
    ], caption=cap("VF on the monitor, but the patient is talking to you? That's artifact. 📺\n\nMotion, "
                   "shivering and loose leads can mimic VF. Look for normal QRS complexes marching through, check "
                   "the patient and the pleth. Unresponsive + pulseless = real VF → shock.",
                   ["ECG", "Telemetry", "ACLS", "NursingStudent", "ICUNurse"]),
        shorts_title="VF or Artifact? Look at the Patient First #shorts")


def r13():
    return story("S13_aivr_reperfusion", [
        {"d": 3.2, "hook": True, "top": "Wide rhythm right\n*after the cath lab?*", "top_size": 90,
         "rh": ("aivr", {}, "HR 72")},
        {"d": 5.5, "top": "Wide QRS, regular, rate *50–110*",
         "bottom": "= *AIVR*: accelerated idioventricular rhythm."},
        {"d": 5.5, "top": "Often a *reperfusion* rhythm",
         "bottom": "Common right after the artery is opened (PCI or lytics)."},
        {"d": 7, "top": "Usually *benign* and self-limiting.", "big": "DON'T SUPPRESS", "big_size": 88,
         "big_color": YELLOW, "sub": "Antiarrhythmics can leave *no escape rhythm*. Monitor, check BP."},
        {"d": 6, "top": "Not VT:",
         "bullets": ["VT is usually *over 120*", "AIVR is slower, often *well tolerated*",
                     "Unstable? Treat per ACLS"]},
    ], caption=cap("Wide, regular rhythm at 50–110 right after reperfusion? That's likely AIVR, accelerated "
                   "idioventricular rhythm.\n\nUsually benign and self-limiting. Suppressing it with "
                   "antiarrhythmics can remove the only escape rhythm. Monitor, check the BP, treat if unstable.",
                   ["ECG", "CathLab", "CardiacNurse", "Telemetry", "ACLS"]),
        shorts_title="AIVR: The Wide Rhythm You Should NOT Treat #shorts")


def r14():
    return story("S14_hypothermia_osborn", [
        {"d": 3.2, "hook": True, "top": "That hump right\n*after the QRS?*",
         "rh": ("beats", {"j_amp": 0.35, "hr": 46, "qt": 0.5}, "HR 46 · 29°C")},
        {"d": 5.5, "top": "*Osborn (J) wave*",
         "bottom": "A classic sign of *hypothermia*. Grows as the temperature drops."},
        {"d": 6.5, "top": "Also on the strip:",
         "bullets": ["*Bradycardia*, long intervals", "Shivering artifact", "AFib, then *VF* as it gets colder"]},
        {"d": 7, "top": "Hypothermic arrest?", "rh": ("vfib", {}, "HR ---"),
         "bullets": ["*Standard ACLS* + high-quality CPR", "*Active rewarming* (ECMO if available)",
                     "Handle gently: rough movement can trigger VF"]},
        {"d": 4.5, "top": "Remember:", "big": "NOT DEAD\nUNTIL WARM", "big_size": 92},
    ], caption=cap("That hump right after the QRS is an Osborn (J) wave, a classic sign of hypothermia. 🧊\n\n"
                   "Expect bradycardia, long intervals and shivering artifact, then AFib and VF as it gets colder. "
                   "In arrest: standard ACLS, active rewarming, ECMO where available.",
                   ["Hypothermia", "ECG", "ACLS", "EmergencyMedicine", "Paramedic"]),
        shorts_title="Osborn Waves & Hypothermic Arrest: Not Dead Until Warm #shorts")


def r15():
    return story("S15_opioid_overdose", [
        {"d": 3.2, "hook": True, "top": "Opioid overdose:\n*breathing or not?*",
         "rh": ("sinus", {"hr": 52}, "HR 52 · RR 4")},
        {"d": 6.5, "top": "Pulse, but not breathing?", "big": "NALOXONE", "big_color": CYAN,
         "sub": "Plus *rescue breaths / bag-mask* right away."},
        {"d": 6.5, "top": "No pulse?", "rh": ("cpr", {}, None), "big": "CPR FIRST",
         "sub": "Naloxone may be reasonable, but *never* at the cost of CPR."},
        {"d": 6, "top": "Naloxone doesn't restart a heart.",
         "bottom": "It reverses *respiratory depression*. Oxygen & ventilation do the rest."},
        {"d": 6, "top": "After reversal:", "rh": ("sinus", {"hr": 96}, "HR 96 · RR 14"),
         "bullets": ["Watch for *re-sedation*", "Withdrawal, agitation, vomiting", "*Monitor*, don't rush discharge"]},
    ], caption=cap("Opioid overdose, AHA 2025 style: pulse but not breathing → naloxone + ventilation. No pulse → "
                   "CPR first; naloxone may be reasonable if it doesn't interrupt CPR.\n\nNaloxone treats breathing, "
                   "not cardiac arrest. Watch for re-sedation after reversal.",
                   ["Naloxone", "ACLS", "AHA2025", "EMS", "ERNurse"]),
        shorts_title="Opioid Overdose: Naloxone vs CPR First (AHA 2025) #shorts")


def r16():
    return story("S16_defib_pad_placement", [
        {"d": 3.2, "hook": True, "top": "Where do the\n*pads* go?", "rh": ("vfib", {}, "HR ---")},
        {"d": 7, "top": "*Anterolateral*: fastest default",
         "bullets": ["Right pad *below the right clavicle*", "Left pad on the *left mid-axillary line*, below the armpit"]},
        {"d": 6.5, "top": "*Anteroposterior* works too",
         "bottom": "Front: left chest. Back: left of the spine, *below the scapula.*"},
        {"d": 7.5, "top": "Pad checklist:",
         "bullets": ["Adult pads *8 cm+*", "*Not over breast tissue*", "Dry skin, remove med patches",
                     "Not *directly over* a pacemaker/ICD"]},
        {"d": 4.5, "top": "Then:", "big": "CLEAR · SHOCK", "big_size": 96, "shock": True},
    ], caption=cap("Defib pad placement, AHA 2025: anterolateral (right below the clavicle + left mid-axillary) or "
                   "anteroposterior (left chest + left of the spine below the scapula). ⚡\n\nKeep pads off breast "
                   "tissue and implanted devices, dry the skin, and remove med patches.",
                   ["Defibrillation", "ACLS", "BLS", "AHA2025", "CodeBlue"]),
        shorts_title="Defibrillator Pad Placement: AL vs AP (AHA 2025) #shorts")


def r17():
    return story("S17_long_qt_eyeball", [
        {"d": 3.2, "hook": True, "top": "Is this QT\n*too long?*",
         "rh": ("beats", {"qt": 0.62, "hr": 62, "t_w": 0.07}, "HR 62")},
        {"d": 6.5, "top": "The *half-RR* eyeball rule",
         "bottom": "T wave ends *past halfway* to the next QRS? QT is probably long (HR 60–100)."},
        {"d": 6.5, "top": "Then calculate the QTc:",
         "bullets": ["Over *450 ms* (men) / *460 ms* (women): prolonged", "Over *500 ms*: high *torsades* risk"]},
        {"d": 6.5, "top": "Common culprits:",
         "bullets": ["*Low K+, Mg, Ca*", "Antiarrhythmics, antipsychotics", "Some antibiotics, *ondansetron*, methadone"]},
        {"d": 4.5, "top": "Why it matters:", "rh": ("torsades", {}, "HR 250"),
         "bottom": "Long QT is the setup for *torsades.*"},
    ], caption=cap("Quick QT check: if the T wave ends more than halfway to the next QRS, the QT is probably long "
                   "(at HR 60–100). Then calculate the QTc.\n\nOver 500 ms = high torsades risk. Check K+, Mg, Ca "
                   "and the MAR.",
                   ["LongQT", "ECG", "Telemetry", "Pharmacology", "NursingStudent"]),
        shorts_title="How to Eyeball a Long QT in 3 Seconds #shorts")


def r18():
    roles = [("1 · *Team leader*", "Stands back, sees everything, *assigns & decides.*"),
             ("2 · *Compressor*", "Hard & fast. *Swaps every 2 min.*"),
             ("3 · *Airway*", "BVM or advanced airway + *capnography.*"),
             ("4 · *Monitor / defib*", "Pads, rhythm checks, *pre-charging.*"),
             ("5 · *IV / IO / meds*", "Access, drugs, flush, *calls back doses.*"),
             ("6 · *Recorder*", "Times everything: *epi due, next rhythm check.*")]
    beats = [{"d": 3, "hook": True, "top": "6 jobs in\nevery *code.*", "rh": ("cpr", {}, None)}]
    beats += [{"d": 4.2, "top": a, "top_size": 76, "bottom": b} for a, b in roles]
    beats += [{"d": 4.2, "top": "+ a *CPR coach* if you can", "bottom": "Watches rate & depth, keeps pauses short."}]
    return story("S18_code_team_roles", beats,
                 caption=cap("The 6 roles in every resuscitation team: team leader, compressor, airway, "
                             "monitor/defibrillator, IV/IO/meds and recorder, plus a CPR coach if you have the "
                             "people.\n\nWhich role do you usually take? 👇",
                             ["CodeBlue", "ACLS", "Teamwork", "NurseLife", "Megacode"]),
                 shorts_title="The 6 Roles on Every Code Team #shorts",
                 ask="Which role do *you* take?\nComment below.")


def r19():
    return story("S19_bb_ccb_overdose", [
        {"d": 3.2, "hook": True, "top": "Slow & low\n*after an overdose?*",
         "rh": ("sinus", {"hr": 38}, "HR 38 · BP 70/40")},
        {"d": 5.5, "top": "Bradycardia + hypotension →",
         "bottom": "Think *beta-blocker* or *calcium-channel blocker* toxicity."},
        {"d": 5.5, "top": "Standard brady treatment often *fails.*",
         "bottom": "Atropine and pacing may not bring the BP up."},
        {"d": 7.5, "top": "Toxin-specific options:",
         "bullets": ["*IV calcium*", "*High-dose insulin* + dextrose", "*Glucagon* (beta-blockers)",
                     "Vasopressors · ECMO if refractory"]},
        {"d": 5, "top": "Call *poison control* early.", "bottom": "Doses are protocol-specific. Get help fast."},
    ], caption=cap("Bradycardia + hypotension after an overdose? Think beta-blocker or calcium-channel blocker "
                   "toxicity.\n\nAtropine and pacing often aren't enough. Options include IV calcium, high-dose "
                   "insulin with dextrose, glucagon, vasopressors and ECMO. Loop in toxicology early.",
                   ["Toxicology", "ACLS", "ICUNurse", "EmergencyMedicine", "Pharmacology"]),
        shorts_title="Beta-Blocker & CCB Overdose: Why Atropine Isn't Enough #shorts")


def r20():
    return story("S20_fine_vf_or_asystole", [
        {"d": 3.2, "hook": True, "top": "Flat line.\nOr *is it?*",
         "rh": ("fine_vs_asystole", {"gain_up_at": 8.4}, "HR ---")},
        {"d": 5, "top": "Before calling asystole, *turn up the gain.*", "sfx": [(1.2, "riser", 0.5)]},
        {"d": 6, "top": "*Fine VF* can look flat at low gain.",
         "bottom": "Fine VF = *shockable*. Asystole is *not.*"},
        {"d": 6.5, "top": "Confirm a flat line:",
         "bullets": ["Check the *leads* are connected", "Turn up the *gain*", "Look in a *second lead*"]},
        {"d": 6, "top": "True asystole?", "rh": ("asystole", {}, "HR ---"), "big": "CPR + EPI", "big_color": CYAN,
         "sub": "Epi *ASAP*, then every 3–5 min. Hunt the H's & T's."},
    ], caption=cap("Flat line on the monitor? Before you call asystole: check the leads, turn up the gain and "
                   "look in a second lead. 📈\n\nFine VF can hide at low gain, and it's shockable. True asystole "
                   "gets CPR + epinephrine ASAP.",
                   ["Asystole", "ACLS", "ECG", "CodeBlue", "Megacode"]),
        shorts_title="Asystole or Fine VF? Turn Up the Gain #shorts")


def r21():
    return story("S21_stroke_last_known_well", [
        {"d": 3.2, "hook": True, "top": "Sudden\n*facial droop.*", "rh": ("sinus", {"hr": 84}, "BP 182/96")},
        {"d": 6.5, "top": "Screen with *BE-FAST*",
         "bullets": ["*B*alance · *E*yes", "*F*ace · *A*rms", "*S*peech · *T*ime to call"]},
        {"d": 6.5, "top": "The question that matters most:", "big": "LAST KNOWN WELL?", "big_size": 84,
         "sub": "Not when symptoms were found. When they were *last normal.*"},
        {"d": 5, "top": "Check *glucose* first.", "bottom": "*Hypoglycemia* can mimic a stroke perfectly."},
        {"d": 7.5, "top": "Eligible patients:",
         "bullets": ["IV thrombolysis within *4.5 h*", "Large-vessel occlusion → *thrombectomy* (selected up to 24 h)",
                     "Stroke alert + *CT fast*"]},
    ], caption=cap("Suspected stroke: BE-FAST, then the most important question: when were they last known well? 🧠"
                   "\n\nCheck glucose (hypoglycemia mimics stroke). Eligible patients may get IV thrombolysis within "
                   "4.5 h, and thrombectomy for large-vessel occlusion in selected patients up to 24 h.",
                   ["Stroke", "BEFAST", "ACLS", "NeuroNurse", "EmergencyMedicine"]),
        shorts_title="Stroke Alert: Why 'Last Known Well' Is Everything #shorts")


def r22():
    return story("S22_pvcs_r_on_t", [
        {"d": 3.2, "hook": True, "top": "Early, wide\n*and ugly.*", "rh": ("pvcs", {}, "HR 78")},
        {"d": 6.5, "top": "*PVC*: premature ventricular complex",
         "bullets": ["Comes *early*", "*Wide & bizarre*, no P wave", "Usually a *pause* after it"]},
        {"d": 6.5, "top": "Often harmless, *but* check:",
         "bullets": ["*K+ and Mg*", "Ischemia", "Stimulants, hypoxia, drugs"]},
        {"d": 6, "top": "The dangerous one: *R-on-T*", "rh": ("pvcs", {"ron_t": True}, "HR 190"),
         "bottom": "A PVC landing on the T wave can trigger *VT / VF.*"},
        {"d": 5, "top": "Pulseless?", "rh": ("vfib", {}, "HR ---"), "big": "DEFIBRILLATE", "big_size": 96,
         "shock": True},
    ], caption=cap("PVCs: early, wide, bizarre, with a pause after. Often benign, but check K+, Mg, ischemia and "
                   "stimulants.\n\nThe dangerous one is R-on-T, a PVC landing on the T wave that can trigger VT/VF. "
                   "Pulseless → defibrillate.",
                   ["PVC", "ECG", "Telemetry", "CardiacNurse", "ACLS"]),
        shorts_title="PVCs and R-on-T: When an Extra Beat Turns Deadly #shorts")


def r23():
    return story("S23_anaphylaxis_im_epi", [
        {"d": 3.2, "hook": True, "top": "Hives, wheeze,\n*BP crashing.*", "rh": ("sinus", {"hr": 132}, "BP 70/40")},
        {"d": 6.5, "top": "Anaphylaxis, first line:", "big": "IM EPINEPHRINE", "big_size": 84, "big_color": CYAN,
         "sub": "Adults *0.3–0.5 mg* (1 mg/mL) into the *anterolateral thigh.*"},
        {"d": 6, "top": "Repeat every *5–15 min* as needed.",
         "bottom": "Not improving? *Epi infusion* + large-volume IV fluids."},
        {"d": 6.5, "top": "Second line only:",
         "bullets": ["Antihistamines · steroids", "Bronchodilators", "Glucagon if on *beta-blockers*"]},
        {"d": 5.5, "top": "Arrest?", "rh": ("cpr", {}, None),
         "bottom": "*Standard ACLS*, big fluids, *early airway*. It swells fast."},
    ], caption=cap("Anaphylaxis: IM epinephrine into the anterolateral thigh first (adults 0.3–0.5 mg of "
                   "1 mg/mL), repeated every 5–15 min as needed. 💉\n\nAntihistamines and steroids are second line. "
                   "Refractory → epi infusion + fluids. Arrest → standard ACLS and an early airway.",
                   ["Anaphylaxis", "Epinephrine", "ACLS", "ERNurse", "Paramedic"]),
        shorts_title="Anaphylaxis: IM Epinephrine First, Everything Else Second #shorts")


def r24():
    return story("S24_how_many_joules", [
        {"d": 3.2, "hook": True, "top": "How many\n*joules?*", "rh": ("vfib", {}, "HR ---")},
        {"d": 6, "top": "*Biphasic* defibrillator", "big": "120–200 J",
         "sub": "Use the *manufacturer's* recommended dose."},
        {"d": 6, "top": "Don't know the dose?", "big": "USE MAX", "sub": "Later shocks: *same or higher.*",
         "shock": True},
        {"d": 5, "top": "*Monophasic* (older devices)", "big": "360 J"},
        {"d": 6.5, "top": "Energy matters less than:",
         "bullets": ["Shocking *fast*", "*Short* pre- & post-shock pauses", "*CPR immediately* after"]},
    ], caption=cap("Defibrillation energy for VF/pVT: biphasic → manufacturer dose (usually 120–200 J; unknown? "
                   "use max). Monophasic → 360 J. ⚡\n\nWhat matters more: shock fast, keep pauses short and resume "
                   "CPR right after.",
                   ["Defibrillation", "ACLS", "VFib", "Megacode", "CodeBlue"]),
        shorts_title="Defibrillation Energy: Biphasic vs Monophasic Joules #shorts")


def r25():
    return story("S25_hypokalemia_u_waves", [
        {"d": 3.2, "hook": True, "top": "Flat T waves\nand a *U wave?*",
         "rh": ("beats", {"t_amp": 0.07, "u_amp": 0.22, "st": -0.05}, "HR 80")},
        {"d": 6.5, "top": "Classic *hypokalemia*",
         "bullets": ["*Flattened* T waves", "Prominent *U waves*", "ST depression"]},
        {"d": 6, "top": "Why it's dangerous:",
         "bullets": ["Long QT(U)", "*PVCs, VT, torsades*", "Worse with *digoxin*"]},
        {"d": 6.5, "top": "Fix it:",
         "bullets": ["Replace *K+* per protocol", "Replace *Mg* too", "Keep them on telemetry"]},
        {"d": 4.5, "top": "Low K + low Mg?", "big": "FIX BOTH", "big_color": CYAN,
         "sub": "K+ won't stay up while Mg is low."},
    ], caption=cap("Flat T waves, prominent U waves and ST depression: classic hypokalemia.\n\nIt sets up PVCs, "
                   "VT and torsades, especially with digoxin. Replace K+ and Mg together, because potassium won't "
                   "hold while magnesium is low.",
                   ["Hypokalemia", "ECG", "Electrolytes", "ICUNurse", "NursingStudent"]),
        shorts_title="Hypokalemia on the ECG: Flat T Waves and U Waves #shorts")


def r26():
    return story("S26_team_leader_script", [
        {"d": 3.2, "hook": True, "top": "What the instructor\nwants to *hear.*", "top_size": 88,
         "rh": ("vfib", {}, "HR ---")},
        {"d": 6.5, "top": "Take charge, out loud:",
         "bottom": "\"I'm the *team leader*. Maria, start compressions. Jay, *pads on.*\""},
        {"d": 6, "top": "*Closed-loop* every order",
         "bottom": "\"Give *epinephrine 1 mg IV.*\" → \"Epi 1 mg *given.*\""},
        {"d": 6.5, "top": "Rhythm check script:", "shock": True,
         "bottom": "\"Stop compressions. Rhythm? VF. *Charging.* Everyone *clear.*\""},
        {"d": 6, "top": "*Summarize* every 2 min", "rh": ("cpr", {}, None),
         "bottom": "\"VF, 3 shocks, epi at 4 min, amio given. *H's & T's?*\""},
    ], caption=cap("Passing the megacode is as much about communication as algorithms. 🗣️\n\nName the roles, "
                   "close the loop on every order, call the rhythm check out loud, and summarize every 2 minutes. "
                   "Save this before your ACLS class.",
                   ["Megacode", "ACLS", "Leadership", "NursingStudent", "CodeBlue"]),
        shorts_title="ACLS Megacode: What the Team Leader Should Say #shorts")


def r27():
    return story("S27_tca_overdose_bicarb", [
        {"d": 3.2, "hook": True, "top": "Overdose +\na *widening QRS.*",
         "rh": ("beats", {"qrs_w": 0.15, "wide": True, "hr": 118}, "HR 118")},
        {"d": 5.5, "top": "Think *sodium-channel blockade*",
         "bottom": "Classic: *tricyclic antidepressant (TCA)* overdose."},
        {"d": 6.5, "top": "ECG clues:", "bullets": ["Sinus tachycardia", "*QRS over 100 ms*", "*Tall R wave in aVR*"]},
        {"d": 6.5, "top": "The antidote:", "big": "SODIUM BICARB", "big_size": 88, "big_color": CYAN,
         "sub": "Narrows the QRS. Dosing per *toxicology / protocol.*"},
        {"d": 6.5, "top": "Also:",
         "bullets": ["Seizures → *benzodiazepines*", "Avoid other sodium-channel blockers", "Call *poison control*"]},
    ], caption=cap("Overdose + sinus tach + QRS over 100 ms + a tall R in aVR? Think TCA (sodium-channel blocker) "
                   "toxicity.\n\nSodium bicarbonate is the antidote. It narrows the QRS. Treat seizures with "
                   "benzodiazepines, avoid other sodium-channel blockers, and call poison control.",
                   ["Toxicology", "ECG", "EmergencyMedicine", "ACLS", "ERNurse"]),
        shorts_title="TCA Overdose: The Wide QRS That Needs Bicarb #shorts")


def r28():
    return story("S28_airway_during_cpr", [
        {"d": 3.2, "hook": True, "top": "Intubating\n*during CPR?*", "rh": ("cpr", {}, None)},
        {"d": 6, "top": "Rule 1:", "big": "DON'T STOP CPR", "big_size": 92,
         "sub": "If a pause is unavoidable, keep it *under 10 s.*"},
        {"d": 6, "top": "Confirm placement with", "big": "WAVEFORM\nCAPNOGRAPHY", "big_size": 78, "big_color": YELLOW,
         "sub": "Plus exam, then continuous monitoring."},
        {"d": 6.5, "top": "Once it's in:",
         "bullets": ["*1 breath every 6 s* (10/min)", "*Continuous* compressions, no more 30:2", "Don't hyperventilate"]},
        {"d": 5.5, "top": "BVM is fine too.",
         "bottom": "It's not a race. *Good BVM + good CPR* come first."},
    ], caption=cap("Advanced airway during CPR: don't stop compressions to place it, confirm with waveform "
                   "capnography, then 1 breath every 6 s with continuous compressions.\n\nA good BVM with good CPR "
                   "beats a rushed tube.",
                   ["Airway", "ACLS", "RespiratoryTherapist", "Capnography", "Paramedic"]),
        shorts_title="Intubating During CPR: The Rules That Matter #shorts")


def r29():
    return story("S29_brugada_pattern", [
        {"d": 3.2, "hook": True, "top": "Young, fainted,\n*and this V1.*", "rh": ("brugada", {}, "HR 70", None, "V1")},
        {"d": 6, "top": "*Coved* ST elevation + inverted T in V1–V2",
         "bottom": "= *Type 1 Brugada pattern.*"},
        {"d": 6.5, "top": "Why it matters:",
         "bullets": ["Inherited *sodium-channel* disorder", "Risk of *VF / sudden death*",
                     "Often young, at night, or *with fever*"]},
        {"d": 7, "top": "What to do:",
         "bullets": ["*Cardiology referral* (ICD if high risk)", "*Treat fever* fast",
                     "Avoid triggering drugs (brugadadrugs.org)"]},
        {"d": 4.5, "top": "Syncope + this ECG:", "big": "NEVER IGNORE", "big_size": 96},
    ], caption=cap("Coved ST elevation with an inverted T in V1–V2 = type 1 Brugada pattern.\n\nIt's an "
                   "inherited sodium-channel disorder with risk of VF and sudden death, often in young people, at "
                   "night or with fever. Syncope + this ECG = cardiology now.",
                   ["Brugada", "ECG", "Cardiology", "EmergencyMedicine", "Telemetry"]),
        shorts_title="Brugada Pattern: The V1 You Can't Ignore #shorts")


def r30():
    return story("S30_modified_valsalva", [
        {"d": 3.2, "hook": True, "top": "The *vagal trick*\nthat works better.", "rh": ("svt", {"hr": 188}, "HR 188")},
        {"d": 6.5, "top": "Standard Valsalva vs *modified*",
         "bottom": "About *17%* conversion vs about *43%* (REVERT trial)."},
        {"d": 6.5, "pill": ("STEP 1", CYAN), "top": "Semi-sitting, *strain for 15 s*",
         "bottom": "Blow into a *10 mL syringe* hard enough to move the plunger."},
        {"d": 6, "pill": ("STEP 2", CYAN), "top": "*Immediately lie flat*",
         "bottom": "Lift the legs to *45°* for 15 s, then sit back up."},
        {"d": 6, "top": "Check the rhythm.",
         "rh": ("sequence", {"parts": [("svt", 5.4, {"hr": 188}), ("asystole", 0.9, {}), ("sinus", 9, {"hr": 86})]}, None),
         "big": "CONVERTED", "big_color": CYAN, "sub": "Still SVT? Next step: *adenosine.*",
         "sfx": [(2.4, "ding", 0.8)]},
    ], caption=cap("The modified Valsalva for stable SVT: strain for 15 s (blowing into a 10 mL syringe), then "
                   "immediately lie flat with the legs raised 45° for 15 s. 🦵\n\nIn the REVERT trial it converted "
                   "about 43% vs 17% with standard Valsalva. Still in SVT? Move to adenosine.",
                   ["SVT", "Valsalva", "ACLS", "ERNurse", "EmergencyMedicine"]),
        shorts_title="Modified Valsalva: The SVT Trick That Works Better #shorts")


def r31():
    return story("S31_electrical_alternans", [
        {"d": 3.2, "hook": True, "top": "QRS keeps\n*changing size?*",
         "rh": ("beats", {"alternans": 0.45, "r_amp": 0.55, "hr": 112}, "HR 112")},
        {"d": 6.5, "top": "*Electrical alternans* + low voltage + tachycardia",
         "bottom": "Think *pericardial effusion / tamponade*: the heart swings in the fluid.", "bottom_size": 50},
        {"d": 6, "top": "Beck's triad:", "bullets": ["*Hypotension*", "*JVD*", "*Muffled* heart sounds"]},
        {"d": 5, "top": "Confirm fast:", "bottom": "*Bedside ultrasound*: effusion + RV collapse."},
        {"d": 6, "top": "Treatment:", "big": "DRAIN IT", "big_color": CYAN,
         "sub": "*Pericardiocentesis* or surgical drainage. Fluids buy time."},
    ], caption=cap("QRS amplitude alternating beat to beat? That's electrical alternans. With low voltage and "
                   "tachycardia, think pericardial effusion and tamponade.\n\nBeck's triad: hypotension, JVD, "
                   "muffled heart sounds. Confirm with ultrasound and drain it.",
                   ["Tamponade", "ECG", "CardiacSurgery", "ICUNurse", "EmergencyMedicine"]),
        shorts_title="Electrical Alternans: The ECG Sign of Tamponade #shorts")


def r32():
    return story("S32_precharge_defib", [
        {"d": 3.2, "hook": True, "top": "Every second\n*off the chest* counts.", "top_size": 92, "rh": ("cpr", {}, None)},
        {"d": 6.8, "top": "Charge the defibrillator *during compressions.*",
         "bottom": "About *15 s* before the rhythm check."},
        {"d": 5.5, "top": "Then: *pause · look · shock*", "rh": ("vfib", {}, "HR ---"), "big": "SHOCK",
         "sub": "Pre-shock pause *under 10 s*. Shorter is better.", "shock": True},
        {"d": 5.5, "top": "Not shockable?", "rh": ("beats", {"hr": 76}, NP, RED),
         "bottom": "*Disarm the charge* and resume CPR right away."},
        {"d": 5, "top": "Short pauses = *better survival.*", "rh": ("cpr", {}, None),
         "bottom": "Resume compressions *immediately* after every shock."},
    ], caption=cap("Pre-charge the defibrillator during compressions, about 15 s before the rhythm check. ⚡\n\n"
                   "Then pause, look and shock in under 10 s. Not shockable? Disarm and resume CPR. Shorter pauses, "
                   "better outcomes.",
                   ["Defibrillation", "CPR", "ACLS", "CodeBlue", "Megacode"]),
        shorts_title="Pre-Charging the Defibrillator: Cut the Pre-Shock Pause #shorts")


def r33():
    return story("S33_tension_pneumothorax", [
        {"d": 3.2, "hook": True, "top": "Crashing on the vent?\n*Think tension.*", "top_size": 84,
         "rh": ("sinus", {"hr": 138}, "HR 138 · SpO2 78")},
        {"d": 7, "top": "Signs:",
         "bullets": ["*Hypotension* + hypoxia", "Absent breath sounds on one side", "*High airway pressures*",
                     "JVD · tracheal shift is *late*"]},
        {"d": 4.5, "top": "Don't wait for the X-ray.", "big": "DECOMPRESS", "big_color": CYAN, "big_size": 104},
        {"d": 7.5, "top": "Where? (adults)",
         "bullets": ["*4th/5th intercostal space*, just in front of the *mid-axillary line*",
                     "Alternative: *2nd ICS, mid-clavicular*", "Follow your protocol"]},
        {"d": 4.5, "top": "Then:", "bottom": "*Chest tube* / finger thoracostomy. Reassess."},
    ], caption=cap("Tension pneumothorax is a clinical diagnosis: hypotension, hypoxia, absent breath sounds, high "
                   "airway pressures. Don't wait for the X-ray.\n\nIn adults, decompress at the 4th/5th ICS just "
                   "anterior to the mid-axillary line (2nd ICS mid-clavicular as an alternative), then place a "
                   "chest tube.",
                   ["Trauma", "ICUNurse", "RespiratoryTherapist", "EmergencyMedicine", "Paramedic"]),
        shorts_title="Tension Pneumothorax: Where to Decompress in Adults #shorts")


def r34():
    return story("S34_icd_pacemaker_arrest", [
        {"d": 3.2, "hook": True, "top": "Cardiac arrest\nwith an *ICD?*", "rh": ("vfib", {}, "HR ---")},
        {"d": 5.5, "top": "Treat it like *any other* arrest.",
         "bottom": "CPR, defibrillate, ACLS drugs. *Same algorithm.*"},
        {"d": 5.5, "top": "Pads:", "bottom": "Keep them *off the device*. AP position is an easy workaround."},
        {"d": 6, "top": "ICD firing during CPR?",
         "bottom": "You may feel a jolt, but the risk to rescuers is *minimal*. Keep going."},
        {"d": 6, "top": "After ROSC:", "rh": ("sinus", {"hr": 88}, "HR 88"),
         "bullets": ["*Interrogate* the device", "Why did it fire / fail?", "Treat the *cause*"]},
    ], caption=cap("Arrest in a patient with an ICD or pacemaker? Same algorithm: CPR, defibrillation, ACLS drugs. "
                   "Keep pads off the device (AP placement works well).\n\nIf the ICD fires during CPR, the risk to "
                   "rescuers is minimal. After ROSC, get the device interrogated.",
                   ["ICD", "Pacemaker", "ACLS", "CardiacNurse", "CodeBlue"]),
        shorts_title="Cardiac Arrest With an ICD or Pacemaker: What Changes? #shorts")


def r35():
    return story("S35_treat_the_patient", [
        {"d": 3.2, "hook": True, "top": "HR 42.\n*Do you treat it?*", "rh": ("sinus", {"hr": 42}, "HR 42")},
        {"d": 6, "top": "Depends on the *patient.*",
         "bottom": "Athlete, asleep, on a beta-blocker, feeling fine? *Monitor.*"},
        {"d": 7, "top": "Treat if it's *causing*:",
         "bullets": ["Hypotension", "Altered mental status", "Signs of shock", "Chest pain · acute heart failure"]},
        {"d": 6.5, "top": "Symptomatic?",
         "bullets": ["*Atropine 1 mg*, q3–5 min (max 3 mg)", "Then *pacing* or *epi / dopamine* drip"]},
        {"d": 4.5, "top": "The rule:", "big": "PATIENT FIRST", "big_size": 100},
    ], caption=cap("HR 42 on the monitor: do you treat it? Only if it's causing problems (hypotension, altered "
                   "mental status, shock, chest pain, acute heart failure). 🩺\n\nAsymptomatic athlete or sleeping "
                   "patient? Monitor. Symptomatic? Atropine 1 mg, then pacing or a drip.",
                   ["Bradycardia", "ACLS", "NursingStudent", "Telemetry", "ICUNurse"]),
        shorts_title="Bradycardia: Treat the Patient, Not the Monitor #shorts")


def r36():
    return story("S36_pea_asystole_loop", [
        {"d": 3.2, "hook": True, "top": "The PEA / asystole\nloop in *40 s.*", "top_size": 88,
         "rh": ("asystole", {}, "HR ---")},
        {"d": 5, "pill": ("START", RED), "top": "*CPR* + oxygen + monitor", "rh": ("cpr", {}, None),
         "bottom": "Non-shockable? *Don't shock.*"},
        {"d": 5.5, "top": "*Epinephrine 1 mg ASAP*", "bottom": "Then every *3–5 min.*"},
        {"d": 5.5, "top": "Every 2 min: *rhythm check*", "rh": ("beats", {"hr": 70}, NP, RED),
         "bottom": "Organized rhythm? *Pulse check* in under 10 s."},
        {"d": 6.5, "top": "The whole time:", "rh": ("cpr", {}, None),
         "bullets": ["Hunt the *H's & T's*", "Advanced airway + capnography", "IV first, *IO* if IV fails"]},
        {"d": 6, "top": "Became shockable?", "rh": ("vfib", {}, "HR ---"), "big": "SHOCK",
         "sub": "Switch to the *VF loop.*", "shock": True},
    ], caption=cap("The non-shockable arrest algorithm in 40 seconds: CPR, epinephrine 1 mg ASAP then every "
                   "3–5 min, rhythm check every 2 min, and hunt the H's & T's the whole time.\n\nIf it becomes "
                   "shockable, switch to the VF loop.",
                   ["ACLS", "Asystole", "PEA", "Megacode", "CodeBlue"]),
        shorts_title="PEA & Asystole Algorithm in 40 Seconds #shorts")


REELS2 = [r01, r02, r03, r04, r05, r06, r07, r08, r09, r10, r11, r12, r13, r14, r15, r16, r17, r18,
          r19, r20, r21, r22, r23, r24, r25, r26, r27, r28, r29, r30, r31, r32, r33, r34, r35, r36]
