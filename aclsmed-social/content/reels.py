"""Oct 1–7, 2026 ACLSMED faceless reels (voiceless, on-screen text + SFX).

Layout zones (1080x1920): logo y≈200 · top text 300–640 · monitor 700–1010 · bottom 1070–1460.
Clinical content aligned to AHA 2025 Guidelines (Part 9 Adult ALS, Part 11 Post-Arrest Care).
"""
from engine.brand import CYAN, DIM, NAVY, ORANGE, RED, WHITE, YELLOW

MON = (90, 720, 900, 290)  # x, y, w, h
MON_SMALL = (90, 700, 900, 200)
CAP_SMALL = (90, 990, 900, 170)


def T(txt, t, y, size=66, **kw):
    return {"type": "text", "txt": txt, "t": t, "y": y, "size": size, **kw}


def P(txt, t, y, bg=RED, fg=WHITE, size=34, **kw):
    return {"type": "pill", "txt": txt, "t": t, "y": y, "bg": bg, "fg": fg, "size": size, **kw}


def M(rhythm, t, rect=MON, readout=None, **kw):
    el = {"type": "ecg", "rhythm": rhythm, "t": t, "rect": rect, "readout": readout, "fade_in": 0,
          "fade_out": 0}
    el.update(kw)
    return el


def SHOCK(at, charge=True):
    """Charge whine -> shock thump + white flash + camera shake. Returns (elements, sfx)."""
    hit = at + (2.0 if charge else 0)
    sfx = ([(at, "charge", 0.8)] if charge else []) + [(hit, "shock", 1.0)]
    els = [{"type": "flash", "t": (hit, hit + 0.22)}, {"type": "shake", "t": (hit, hit + 0.4), "amp": 24}]
    return els, sfx, hit


def logo(dur):
    return {"type": "logo", "t": (0, dur), "y": 178, "h": 44, "anim": "none", "fade_in": 0}


def endcard(s, e, ask="Save this for your next *megacode*."):
    return [
        {"type": "box", "t": (s, e), "rect": (60, 330, 1020, 1470), "fill": (8, 12, 30, 245),
         "outline": RED, "width": 4, "anim": "up", "y": 330, "x": 60},
        T(ask, (s + 0.1, e), 440, 76, max_w=840, anim="pop"),
        P("FOLLOW  @ACLSMED", (s + 0.5, e), 760, size=44, anim="pop", sfx=[(0, "pop", 0.8)]),
        T("New megacode drill every day.", (s + 0.7, e), 880, 44, weight="medium", family="body", color=DIM),
        T("Practice real megacodes on the\n*ACLSMED simulator*  ·  link in bio", (s + 0.9, e), 1030, 48,
          weight="semibold", family="body", accent=CYAN),
        T("Educational only · Follow your institution's protocols · AHA 2025", (s + 1.1, e), 1360, 28,
          weight="regular", family="body", color=DIM, max_w=880),
    ]


# ---------------------------------------------------------------- R1 · Shock or No Shock quiz
def r1():
    rounds = [
        ("vfib", {}, "HR ---", True, "SHOCK", "Ventricular fibrillation",
         "Chaotic, no organized QRS = *VF*. Shock, then *resume CPR immediately*."),
        ("asystole", {}, "HR ---", False, "NO SHOCK", "Asystole",
         "Check leads & gain. Then *CPR + epinephrine ASAP*. Never shock a flat line."),
        ("vt", {"hr": 176}, "HR 176", True, "SHOCK", "Pulseless VT",
         "Wide, fast, regular, *no pulse*. Treat it like VF: *defibrillate*."),
        ("sinus", {"hr": 78}, "HR 78", False, "NO SHOCK", "PEA",
         "The monitor looks fine. *No pulse* = PEA. CPR, epi ASAP, hunt the *H's & T's*."),
    ]
    els, fx = [], [(0, "alarm", 0.7), (0.05, "heartbeat", 0.8)]
    els += [T("*SHOCK* or\nNO SHOCK?", (0, 3.2), 300, 128, anim="pop", fade_out=0.2),
            T("4 pulseless patients. 3 seconds each.", (0.7, 3.2), 610, 48, weight="semibold", family="body",
              color=CYAN),
            M("vfib", (0, 3.2), readout="HR ---", beeps=False)]
    S = 3.2
    for k, (rh, kw, ro, shockable, ans, name, teach) in enumerate(rounds):
        R = 8.4
        els += [P(f"RHYTHM {k + 1}/4", (S, S + R), 330, bg=CYAN, fg=NAVY, anim="pop", sfx=[(0, "whoosh", 0.8)]),
                T("Unresponsive. *No pulse.*", (S + 0.15, S + R), 425, 64, weight="extrabold", max_w=900),
                M(rh, (S, S + R), readout=ro, kw=kw),
                {"type": "countdown", "t": (S + 0.5, S + 3.5), "cy": 1250}]
        rv = S + 3.5
        col = RED if shockable else CYAN
        els += [T(ans, (rv, S + R), 1085, 118, color=col, anim="pop", weight="black"),
                T(name, (rv + 0.15, S + R), 1225, 46, weight="semibold", family="body", color=DIM),
                T(teach, (rv + 0.8, S + R), 1305, 46, weight="semibold", family="body", max_w=880,
                  accent=YELLOW if not shockable else RED)]
        if shockable:
            e2, f2, _ = SHOCK(rv + 0.1)
            els += e2
            fx += f2
        else:
            fx += [(rv, "buzzer", 0.9)]
        S += R
    els += endcard(S, S + 4.6, ask="How many did you get?\nComment your score */4*")
    return {"id": "R1_shock_or_no_shock", "duration": S + 4.6, "elements": [logo(S + 4.6)] + els, "sfx": fx,
            "cover_t": 1.6}


# ---------------------------------------------------------------- R2 · AFib cardioversion 200 J
def r2():
    D = 41.0
    els, fx = [], [(0, "alarm", 0.7)]
    els += [M("afib", (0, 33.5), readout="HR 150 IRREG", kw={"mean_hr": 150})]
    els += [T("Still cardioverting\nAFib at *120 J?*", (0, 3.6), 320, 104, anim="pop"),
            P("AHA 2025 UPDATE", (3.6, 13), 300, bg=CYAN, fg=NAVY, anim="pop", sfx=[(0, "whoosh", 0.8)]),
            T("The recommended *first shock* for AFib went *up*.", (3.8, 13), 400, 64, max_w=880),
            T("Irregularly irregular · no P waves · rate 150 · *pulse present, hypotensive*", (4.6, 13), 1080, 42,
              weight="semibold", family="body", color=DIM, max_w=860, accent=YELLOW),
            T("OLD HABIT", (7.2, 13), 1220, 38, weight="bold", family="mono", color=DIM),
            T("Start low: 120 J, then escalate", (7.4, 13), 1280, 60, weight="bold", max_w=940),
            {"type": "strike", "t": (8.8, 13), "x0": 120, "x1": 960, "y": 1312, "sfx": [(0, "buzzer", 0.8)]}]
    # new rule
    els += [T("Unstable AFib with a pulse →\n*SYNCHRONIZED* cardioversion", (13, 21), 330, 66, max_w=900),
            P("AHA 2025", (13.2, 21), 1080, bg=CYAN, fg=NAVY),
            T("AT LEAST", (13.3, 21), 1140, 40, weight="bold", family="mono", color=DIM),
            T("*200 J*", (13.4, 21), 1185, 190, anim="pop", weight="black"),
            T("first synchronized shock · biphasic", (13.8, 21), 1400, 44, weight="semibold", family="body",
              color=DIM)]
    e2, f2, _ = SHOCK(13.4)
    els += e2
    fx += f2
    els += [T("Atrial *flutter*?", (21, 27), 330, 76),
            T("An initial *200 J* may be reasonable too.", (21.3, 27), 450, 58, weight="bold", max_w=880),
            T("Shock fails? *Escalate* energy per your device.", (22.3, 27), 1150, 58, max_w=880,
              sfx=[(0, "pop", 0.7)])]
    els += [T("*Why the change?*", (27, 33.5), 320, 76, accent=CYAN),
            T("Across *3,000+* AF patients, 200 J shocks reached *>90%* cumulative success on all 3 biphasic "
              "platforms.", (27.3, 33.5), 430, 50, weight="semibold", family="body", max_w=880),
            T("Low-energy shocks mean *more failed shocks*, and more sedation time.", (28.8, 33.5), 1110, 50,
              weight="semibold", family="body", max_w=880)]
    els += [T("Before you press shock:", (33.5, 36.6), 400, 70),
            T("•  *Sync ON*: re-check after every shock\n•  Sedate if you can\n•  Everyone clear", (33.8, 36.6),
              620, 54, align="left", x=110, max_w=860, weight="semibold", family="body", accent=CYAN,
              line_gap=1.5, sfx=[(0, "pop", 0.7)])]
    els += endcard(36.6, D)
    return {"id": "R2_afib_cardioversion_200J", "duration": D, "elements": [logo(D)] + els, "sfx": fx,
            "cover_t": 2.0}


# ---------------------------------------------------------------- R3 · Torsades → magnesium
def r3():
    D = 38.5
    els, fx = [], [(0, "alarm", 0.8)]
    els += [M("torsades", (0, 14.5), readout="HR 250", beep_gain=0.35),
            T("This rhythm\n*twists.*", (0, 3.2), 320, 120, anim="pop"),
            T("Polymorphic VT + a *long QT*\n= *Torsades de Pointes*", (3.2, 14.5), 330, 64, max_w=900,
              sfx=[(0, "whoosh", 0.7)]),
            T("QRS spirals around the baseline: tall, tiny, tall.", (3.8, 7.2), 1100, 46, weight="semibold",
              family="body", color=DIM, max_w=860),
            T("Pulse present. What's the *first drug*?", (7.2, 14.5), 1080, 54, max_w=880),
            {"type": "countdown", "t": (7.5, 10.2), "n": 3, "cy": 1270},
            T("MAGNESIUM", (10.2, 14.5), 1170, 124, color=RED, anim="pop", weight="black", sfx=[(0, "ding", 0.9)]),
            T("*1–2 g IV*", (10.5, 14.5), 1320, 70, accent=CYAN)]
    els += [M("torsades", (14.5, 21.5), readout="NO PULSE", beeps=False, color=RED),
            T("Lost the pulse?", (14.5, 21.5), 330, 80, sfx=[(0, "alarm", 0.6)]),
            T("SHOCK FIRST", (15.3, 21.5), 1100, 116, color=RED, anim="pop", weight="black"),
            T("*Defibrillate* (unsynchronized) + CPR.\nThen give magnesium.", (16.0, 21.5), 1260, 50,
              weight="bold", max_w=900)]
    e2, f2, _ = SHOCK(15.6)
    els += e2
    fx += f2
    els += [M("sinus", (21.5, 33), readout="HR 72", kw={"hr": 72, "t_amp": 0.22}),
            T("Then fix *why* the QT is long", (21.5, 33), 330, 72, max_w=900, sfx=[(0, "whoosh", 0.7)]),
            T("• Stop QT-prolonging drugs\n• Correct *low K+ and low Mg*\n• Review the MAR: antiarrhythmics, "
              "antipsychotics, some antibiotics & antiemetics", (22.1, 33), 1080, 46, align="left", x=110,
              max_w=860, weight="semibold", family="body", accent=CYAN, line_gap=1.35, sfx=[(0, "pop", 0.7)])]
    els += [T("Torsades = think *Mg*.", (30, 33), 500, 64, anim="pop", accent=RED, sfx=[(0, "pop", 0.7)])]
    els += endcard(33, D)
    return {"id": "R3_torsades_magnesium", "duration": D, "elements": [logo(D)] + els, "sfx": fx, "cover_t": 1.8}


# ---------------------------------------------------------------- R4 · EtCO2 during CPR
def r4():
    D = 36.5
    win = 4.0
    cwin = 12.0  # capnography sweep shows ~2 breaths at 10/min
    els, fx = [], [(0, "heartbeat", 0.8)]
    ecg_cpr = M("cpr", (0, 22), rect=MON_SMALL, label="II  ·  CPR IN PROGRESS", beeps=False)

    def cap(t, kw, readout):
        return {"type": "capno", "t": t, "rect": CAP_SMALL, "kw": kw, "readout": readout, "window": cwin,
                "label": "EtCO2  mmHg", "fade_in": 0.2, "gain": 170 * 0.85 / 45}

    els += [ecg_cpr, cap((0, 11), {"etco2": 8, "rr": 10}, "8")]
    els += [T("Your CPR has\na *live score.*", (0, 3.2), 320, 108, anim="pop"),
            T("It's the *EtCO2* number on capnography.", (3.2, 11), 380, 62, max_w=880, sfx=[(0, "whoosh", .7)]),
            T("*< 10 mmHg*", (4.5, 11), 1210, 130, anim="pop", color=WHITE, accent=RED, sfx=[(0, "buzzer", .7)]),
            T("= compressions aren't moving enough blood", (4.9, 11), 1370, 44, weight="semibold",
              family="body", color=DIM, max_w=940)]
    els += [cap((11, 22), {"etco2": 18, "rr": 10}, "18"),
            T("Fix it *now*:", (11, 22), 330, 80, sfx=[(0, "whoosh", .7)]),
            T("• Depth *2–2.4 in* (5–6 cm)\n• Rate *100–120/min*, full recoil\n• *Switch compressors* every 2 min"
              "\n• Pauses under *10 s*", (11.4, 22), 1220, 46, align="left", x=120, max_w=860, weight="semibold",
              family="body", accent=CYAN, line_gap=1.35, sfx=[(0, "pop", .7)]),
            T("Better CPR → *higher number*", (16, 22), 470, 54, accent=CYAN)]
    rise_at = 25.0  # absolute reel time of the ROSC jump
    s3 = 22.0
    els += [M("sequence", (s3, 32), rect=MON_SMALL, label="II",
              kw={"parts": [("cpr", win + (rise_at - s3), {}), ("sinus", 8, {"hr": 92})]}, readout=None),
            cap((s3, 32), {"etco2": 18, "rr": 10, "rise": (cwin + rise_at - s3, 40)},
                lambda tt: str(int(18 + 22 * min(1, max(0, (tt - (rise_at - s3)) / 1.2))))),
            T("Watch for a *sudden, sustained jump*", (s3, 29), 330, 66, max_w=900),
            T("to *35–40+ mmHg*", (rise_at + 0.3, 32), 1220, 86, anim="pop", sfx=[(0, "ding", .9)]),
            T("= think *ROSC*. Check rhythm & pulse at the next pause.", (rise_at + 1.0, 32), 1350, 44,
              weight="semibold", family="body", max_w=880, accent=CYAN)]
    fx += [(rise_at - 1.4, "riser", 0.6)]
    els += [T("Bonus: waveform capnography also confirms *ET tube placement*.", (29, 32), 340, 56,
              max_w=900, accent=YELLOW, sfx=[(0, "pop", .7)])]
    els += endcard(32, D)
    return {"id": "R4_etco2_during_cpr", "duration": D, "elements": [logo(D)] + els, "sfx": fx, "cover_t": 1.8}


# ---------------------------------------------------------------- R5 · Adenosine push
def r5():
    D = 40.0
    els, fx = [], [(0, "alarm", 0.6)]
    els += [M("svt", (0, 23), readout="HR 186", beep_gain=0.4),
            T("Adenosine *failed?*\nCheck your *push.*", (0, 3.4), 320, 100, anim="pop", max_w=960),
            T("Stable *narrow-complex* SVT.\nVagal maneuvers failed.", (3.4, 8), 350, 62, max_w=920,
              sfx=[(0, "whoosh", .7)]),
            T("Half-life: *under 10 seconds*. A slow push never reaches the heart.", (4.2, 8), 1120, 48,
              weight="semibold", family="body", max_w=880, accent=YELLOW)]
    steps = [
        ("STEP 1", "Big, *proximal* IV (antecubital). Arm up."),
        ("STEP 2", "*6 mg* rapid IV push, as fast as you can."),
        ("STEP 3", "*Immediately* flush *20 mL NS* (2-syringe / stopcock)."),
        ("STEP 4", "Warn them: brief *chest pressure, flushing, doom*. Record the strip."),
    ]
    S = 8.0
    for k, (lab, txt) in enumerate(steps):
        els += [P(lab, (S, S + 3.75), 1090, bg=CYAN, fg=NAVY, anim="pop", sfx=[(0, "pop", .8)]),
                T(txt, (S + 0.1, S + 3.75), 1190, 60, max_w=880),
                T("Rapid push technique", (S, S + 3.75), 360, 70)]
        S += 3.75
    # conversion
    els += [M("sequence", (23, 32), readout=None,
              kw={"parts": [("svt", 4.0 + 1.2, {}), ("asystole", 2.2, {}), ("sinus", 8, {"hr": 82})]}),
            T("Expect a *pause*. Don't panic.", (23, 32), 360, 70, max_w=900),
            T("No conversion in 1–2 min? → *12 mg* rapid push + flush", (26.8, 32), 1120, 56, max_w=880,
              sfx=[(0, "pop", .7)])]
    fx += [(26.45, "ding", 0.8)]
    els += [P("CAUTION", (32, 35.5), 360, bg=YELLOW, fg=NAVY, anim="pop", sfx=[(0, "whoosh", .7)]),
            T("Don't give it for *irregular, wide-complex* tachycardia (pre-excited AF).", (32.2, 35.5), 460,
              58, max_w=880, accent=YELLOW)]
    els += [M("sinus", (32, 35.5), readout="HR 82", kw={"hr": 82})]
    els += endcard(35.5, D)
    return {"id": "R5_adenosine_push", "duration": D, "elements": [logo(D)] + els, "sfx": fx, "cover_t": 1.8}


# ---------------------------------------------------------------- R6 · Pacing capture
def r6():
    D = 38.5
    els, fx = [], [(0, "alarm", 0.6)]
    els += [M("paced", (0, 10), readout="PACING 70", kw={"capture": False}),
            T("Pacer spikes don't\nmean *capture.*", (0, 3.3), 320, 104, anim="pop", max_w=960),
            T("Symptomatic brady. Transcutaneous pacer at *60–80/min*.", (3.3, 10), 360, 56, max_w=900,
              sfx=[(0, "whoosh", .7)]),
            T("A spike with *no QRS* after it", (4.5, 10), 1100, 60, max_w=880),
            T("= *FAILURE TO CAPTURE*", (5.4, 10), 1200, 72, anim="pop", accent=RED, sfx=[(0, "buzzer", .8)])]
    els += [M("paced", (10, 30), readout="PACING 70"),
            T("Raise the *mA* until *every spike*\ngets a *wide QRS + T wave*", (10, 17), 340, 62,
              max_w=960),
            P("ELECTRICAL CAPTURE", (11.2, 17), 1110, bg=(0, 150, 60), size=40, anim="pop",
              sfx=[(0, "ding", .8)])]
    els += [T("Now prove *mechanical* capture", (17, 24), 340, 70, max_w=900, sfx=[(0, "whoosh", .7)]),
            T("Feel a *femoral pulse* that matches the paced rate.", (17.4, 24), 1090, 58, max_w=880),
            T("Skip the carotid: pacing makes the muscles jump and can fool you.", (18.8, 24), 1270, 44,
              weight="semibold", family="body", color=DIM, max_w=860),
            T("BP & SpO2 pleth should *track the paced rate* too.", (20.5, 24), 1380, 40, weight="semibold",
              family="body", max_w=860, accent=CYAN)]
    fx += [(17.6 + i * 0.857, "heartbeat", 0.9) for i in range(7)]
    els += [T("Then:", (24, 30), 340, 76),
            T("• Set output *just above* the capture threshold\n• *Analgesia / sedation*: pacing hurts\n"
              "• Keep treating the *cause*", (24.3, 30), 1080, 50, align="left", x=110, max_w=860,
              weight="semibold", family="body", accent=CYAN, line_gap=1.4, sfx=[(0, "pop", .7)])]
    els += endcard(30, D, ask="Tag the nurse who always\nchecks the *femoral*.")
    return {"id": "R6_pacing_capture", "duration": D, "elements": [logo(D)] + els, "sfx": fx, "cover_t": 1.8}


# ---------------------------------------------------------------- R7 · Hyperkalemia progression
def r7():
    D = 39.5
    els, fx = [], [(0, "heartbeat", 0.8)]
    els += [T("This ECG is telling\nyou the *potassium.*", (0, 3.2), 320, 92, anim="pop", max_w=960),
            M("hyperk", (0, 9), readout="K+ ↑", kw={"stage": 1}),
            P("STAGE 1", (3.2, 9), 330, bg=YELLOW, fg=NAVY, anim="pop", sfx=[(0, "whoosh", .7)]),
            T("Tall, narrow, *peaked T waves*", (3.4, 9), 430, 64, max_w=900, accent=YELLOW),
            M("hyperk", (9, 15), readout="K+ ↑↑", kw={"stage": 2}, color=ORANGE),
            P("STAGE 2", (9, 15), 330, bg=ORANGE, fg=NAVY, anim="pop", sfx=[(0, "whoosh", .7)]),
            T("P waves flatten · PR lengthens · *QRS widens*", (9.2, 15), 430, 60, max_w=900,
              accent=ORANGE),
            M("hyperk", (15, 21), readout="K+ ↑↑↑", kw={"stage": 3}, color=RED, beep_gain=0.3),
            P("STAGE 3", (15, 21), 330, bg=RED, anim="pop", sfx=[(0, "alarm", .7)]),
            T("*Sine wave.* Arrest is next: VF, PEA, or asystole.", (15.2, 21), 430, 60, max_w=900)]
    els += [T("Tall T waves → wide QRS → sine wave", (3.4, 21), 1110, 44, weight="semibold", family="body",
              color=DIM, max_w=880)]
    els += [M("hyperk", (21, 34), readout="K+ ↑↑↑", kw={"stage": 2}, color=ORANGE),
            T("Your *first* move?", (21, 29), 340, 80),
            {"type": "countdown", "t": (21.4, 24.4), "cy": 1260},
            T("IV CALCIUM", (24.4, 29), 1110, 116, color=RED, anim="pop", weight="black", sfx=[(0, "ding", .9)]),
            T("Stabilizes the heart. It does *not* lower K+.", (24.9, 29), 1260, 46,
              weight="semibold", family="body", max_w=880, accent=YELLOW)]
    els += [T("Then *shift* it.\nThen *remove* it.", (29, 34), 330, 76, max_w=900, sfx=[(0, "whoosh", .7)]),
            T("*Shift:* insulin + dextrose · albuterol · bicarb if acidotic\n*Remove:* dialysis, diuretics, "
              "binders", (29.3, 34), 1090, 48, align="left", x=110, max_w=860, weight="semibold", family="body",
              accent=CYAN, line_gap=1.45, sfx=[(0, "pop", .7)])]
    els += endcard(34, D)
    return {"id": "R7_hyperkalemia_ecg", "duration": D, "elements": [logo(D)] + els, "sfx": fx, "cover_t": 1.6}


REELS = [r1, r2, r3, r4, r5, r6, r7]
