"""ElevenLabs sound recipes for every scene.

beds:   30 s self-looping clips (2 variants cross-faded across the 60 s loop), level in dB.
events: one-shots placed on the on-screen frame. "at" rows are (time, extra dB, pan[, pan_end for a sweep]).
Timings mirror the visuals in each scene module, so every sound lands on its action.
"""
import numpy as np
from engine.px import TAU, DUR, cyc

QUIET = "No music, no voices, no speech."


def beach():
    from scenes.beach import SUN  # noqa: F401  (timings below follow beach.py)
    swell = lambda T: 0.78 + 0.22 * np.sin(TAU * T / 6 - 192 / 70.0)
    return {
        "beds": [
            dict(tag="surf", db=0, env=swell, text=f"Gentle tropical ocean waves rolling onto a sandy beach, soft foamy surf washing in and out, calm sunny day. {QUIET}"),
            dict(tag="breeze", db=-11, text=f"Light warm sea breeze rustling palm fronds, soft tropical leaves moving. {QUIET}"),
        ],
        "events": [
            dict(tag="gull", db=-9, dur=3.0, variants=3, text="Seagulls calling in the distance over the ocean, two or three short cries.",
                 at=[(9.8, 0, -0.2), (29.9, 0, 0.2), (49.7, 0, -0.1), (3.4, -3, 0.4), (33.6, -3, 0.35)]),
            dict(tag="volley", db=-15, dur=0.8, variants=3, text="Single soft hand bump on an inflatable beach volleyball, outdoors on sand.",
                 at=[(2.0 * k, 0, -0.35 if k % 2 == 0 else 0.35) for k in range(30)]),
        ],
    }


def dino():
    from scenes.dino import ROAR_T
    steps = []
    for k in range(60):
        t0 = k + 0.25
        x = cyc(t0, 60) * 520 - 116 + 56
        vis = float(np.clip((x + 30) / 60, 0, 1) * np.clip((440 - x) / 60, 0, 1))
        if vis > 0.05:
            steps.append((t0, 20 * np.log10(vis), float(np.clip((x - 192) / 192, -1, 1))))
    return {
        "beds": [
            dict(tag="jungle", db=0, text=f"Lush prehistoric jungle at sunset, warm evening insects and crickets, distant exotic birds, calm and peaceful. {QUIET}"),
            dict(tag="river", db=-5, pan=0.35, text=f"Gentle river flowing over stones with a small waterfall in the distance. {QUIET}"),
            dict(tag="campfire", db=-9, text=f"Small campfire crackling and popping softly outdoors. {QUIET}"),
        ],
        "events": [
            dict(tag="roar", db=-2, dur=4.0, lead=0.1, text="A huge T-Rex roar echoing across a wide valley, deep and powerful, distant with natural reverb.",
                 at=[(ROAR_T, 0, -0.35)]),
            dict(tag="birds_scatter", db=-8, dur=2.5, text="A flock of small birds suddenly taking off from trees, many wings flapping.",
                 at=[(ROAR_T + 0.3, 0, -0.25)]),
            dict(tag="footstep", db=-10, dur=1.5, variants=2, text="One very heavy dinosaur footstep thudding on soft earth, deep low rumble, distant.",
                 at=steps),
            dict(tag="ptero", db=-11, dur=2.0, variants=2, text="A pterodactyl screeching high in the sky, distant, echoing.",
                 at=[(12.1, 0, 0.0), (42.1, 0, 0.1), (39.1, -2, -0.1)]),
            dict(tag="fish_jump", db=-9, dur=1.2, variants=2, text="A small fish leaping out of a calm river with a light splash.",
                 at=[(b + 12.0, 0, -0.15) for b in (0, 20, 40)] + [(b + 13.4, -2, -0.05) for b in (0, 20, 40)]),
            dict(tag="bobber", db=-14, dur=0.6, text="A tiny fishing bobber dipping into water, small plop.",
                 at=[(13.6 + 15 * k, 0, -0.45) for k in range(4)]),
        ],
    }


def pumpkin():
    from scenes.pumpkin import OWL_T, CAW_T, WOO_T, BELL_T, GATE_P
    return {
        "beds": [
            dict(tag="night", db=0, text=f"Cozy autumn Halloween night in a pumpkin field, crickets chirping, soft wind through dry leaves, calm. {QUIET}"),
        ],
        "events": [
            dict(tag="owl", db=-8, dur=3.0, text="A barn owl hooting twice at night, soft and close, gentle reverb.",
                 at=[(t, 0, -0.75) for t in OWL_T]),
            dict(tag="crow", db=-9, dur=2.0, text="A single crow cawing twice in an open field.", at=[(CAW_T, 0, 0.25)]),
            dict(tag="gate", db=-13, dur=2.0, variants=2, text="An old wooden garden gate slowly creaking on rusty hinges.",
                 at=[(k + 0.3, 0, -0.2) for k in range(0, 60, GATE_P // 2)]),
            dict(tag="bats", db=-16, dur=1.0, text="Tiny bats squeaking as they fly past.", at=[(10.0, 0, 0.0), (45.0, 0, 0.0), (33.0, 0, 0.1)]),
            dict(tag="ghost", db=-8, dur=4.0, text="A friendly cartoon ghost going 'wooooo', soft, playful and airy, not scary.",
                 at=[(WOO_T - 1.0, 0, -0.5, 0.5)]),
            dict(tag="bell", db=-7, dur=7.0, text="One distant church bell toll at night with a long ringing decay.", at=[(BELL_T, 0, -0.55)]),
            dict(tag="carve", db=-18, dur=0.8, variants=3, text="A knife carving into a pumpkin, short wet scrape.",
                 at=[(k + s + 0.2, 0, -0.05) for k in range(0, 60, 6) for s in range(3)]),
            dict(tag="candy", db=-15, dur=0.8, variants=2, text="A small plastic bucket of wrapped candy shaken briefly.",
                 at=[(k, 0, 0.15) for k in range(0, 60, 5)]),
        ],
    }


def lake():
    from scenes.lake import LOON_T, DEER_T, JUMP_T
    rake = [(k + 0.25, 0, -0.25) for k in range(60) if not (JUMP_T - 0.5 <= k <= JUMP_T + 6)]
    return {
        "beds": [
            dict(tag="lake", db=0, text=f"Calm lake at dawn, gentle water lapping at the shore and a wooden dock, soft morning birdsong. {QUIET}"),
            dict(tag="leaves", db=-11, text=f"Light autumn breeze rustling dry leaves in the trees. {QUIET}"),
        ],
        "events": [
            dict(tag="loon", db=-6, dur=4.0, variants=2, text="A common loon's haunting wail echoing across a misty lake.",
                 at=[(LOON_T[0], 0, -0.45), (LOON_T[1], 0, 0.35)]),
            dict(tag="paddle", db=-13, dur=1.5, variants=3, text="One gentle canoe paddle stroke in calm water, soft swish and drip.",
                 at=[(3.0 * k, 0, float((150 + 40 * np.sin(TAU * 3 * k / 60) + 70 - 192) / 192)) for k in range(20)]),
            dict(tag="ducks", db=-10, dur=2.5, text="A few ducks quacking as they fly overhead.", at=[(16.0, 0, -0.2, 0.3), (46.0, 0, -0.2, 0.3)]),
            dict(tag="rake", db=-17, dur=0.8, variants=3, text="A garden rake scraping dry leaves on grass, one stroke.", at=rake),
            dict(tag="leafjump", db=-7, dur=2.0, text="Someone jumping into a big pile of crunchy dry autumn leaves.", at=[(JUMP_T + 1.0, 0, -0.15)]),
            dict(tag="leafhop", db=-11, dur=1.0, text="A short rustle of dry leaves as someone climbs out of a leaf pile.", at=[(JUMP_T + 4.5, 0, -0.2)]),
            dict(tag="twig", db=-14, dur=0.6, text="A single small twig snapping in a quiet forest.", at=[(DEER_T[0] + 0.2, 0, -0.85)]),
            dict(tag="dive", db=-14, dur=0.8, text="A water bird diving under the surface of a calm lake, small splash.",
                 at=[(8.4 + 20 * k, 0, -0.6) for k in range(3)] + [(11.0 + 20 * k, -4, -0.55) for k in range(3)]),
        ],
    }


def ramen():
    from scenes.ramen import FLICKER, DIP_T, TRAIN_T, CAR_T
    drips = []
    for i, (x, p) in enumerate(((96, 1.5), (150, 2.0), (236, 1.5), (290, 2.0))):
        for k in range(int(DUR / p)):
            drips.append((((k + 1 - i * 0.27) * p) % DUR, -2 if i % 2 else 0, (x - 192) / 192))
    return {
        "beds": [
            dict(tag="rain", db=0, text=f"Steady gentle rain on a city street at night, rain pattering on a fabric awning and puddles, cozy. {QUIET}"),
            dict(tag="city", db=-12, text=f"Quiet city at night in the distance, soft low traffic hum. {QUIET}"),
            dict(tag="broth", db=-13, text=f"A big pot of broth simmering and gently bubbling on a stove, soft sizzle. {QUIET}"),
        ],
        "events": [
            dict(tag="slurp", db=-10, dur=1.2, variants=3, text="One person happily slurping ramen noodles.",
                 at=[(6 * k + 1.5, 0, -0.5) for k in range(10)] + [(6 * k + 4.5, 0, 0.55) for k in range(10)]),
            dict(tag="zap", db=-12, dur=0.6, variants=2, text="A neon sign flickering with a short electric buzz and zap.",
                 at=[(a, 0, 0.0) for a, _ in FLICKER] + [(DIP_T[0], 2, 0.0)]),
            dict(tag="train", db=-4, dur=8.0, text="An elevated commuter train passing overhead on steel rails, rhythmic clacking and rumble, night city.",
                 at=[(TRAIN_T[0] - 1.0, 0, 0.8, -0.8)]),
            dict(tag="car", db=-10, dur=3.0, text="A car driving past slowly on a wet road at night, tyres hissing on water.",
                 at=[(CAR_T[0], 0, -0.9, 0.9), (CAR_T[1], 0, 0.9, -0.9)]),
            dict(tag="drip", db=-20, dur=0.5, variants=3, text="A single water drip falling into a shallow puddle.", at=drips),
            dict(tag="strainer", db=-21, dur=0.8, variants=2, text="A noodle strainer lifted out of hot water, short water pour.",
                 at=[(3 * k + 0.6, 0, 0.15) for k in range(20)]),
        ],
    }


def cabin():
    from scenes.cabin import SLEIGH_T, SLED_P
    return {
        "beds": [
            dict(tag="snow", db=0, text=f"Quiet snowy winter night outdoors, very soft wind, gentle snowfall hush, peaceful. {QUIET}"),
            dict(tag="hearth", db=-12, pan=0.1, text=f"A fireplace crackling inside a log cabin, heard muffled from outside. {QUIET}"),
        ],
        "events": [
            dict(tag="sleigh", db=-6, dur=14.0, text="Sleigh bells jingling rhythmically as a horse-drawn sleigh passes by in the distance.",
                 at=[(SLEIGH_T[0], 0, 0.8, -0.8)]),
            dict(tag="sled", db=-9, dur=2.6, variants=2, text="A wooden sled sliding fast down a snowy hill, swoosh through powder.",
                 at=[(c * SLED_P, 0, 0.7) for c in range(4)]),
            dict(tag="snowsteps", db=-15, dur=11.0, variants=2, text="Slow footsteps crunching uphill through fresh snow, dragging a sled.",
                 at=[(c * SLED_P + 4.0, 0, 0.6) for c in range(4)]),
            dict(tag="pat", db=-17, dur=0.6, variants=3, text="Hands patting packed snow on a snowman, soft muffled thump.",
                 at=[(2 * k + 0.05, 0, -0.45) for k in range(30)]),
            dict(tag="hop", db=-16, dur=0.6, variants=2, text="A small hop landing in fresh snow, soft crunch.",
                 at=[(4 * k + 2.0, 0, -0.25) for k in range(15)]),
        ],
    }


def aurora():
    from scenes.aurora import STAR_T, FISH_T
    return {
        "beds": [
            dict(tag="arctic", db=0, text=f"Arctic night on a frozen lake, very soft cold wind over snow and ice, vast and peaceful. {QUIET}"),
            dict(tag="fire", db=-10, pan=-0.3, text=f"A small campfire crackling outdoors in freezing cold air. {QUIET}"),
        ],
        "events": [
            dict(tag="ice", db=-10, dur=3.0, variants=3, text="A frozen lake making eerie singing 'pew' sounds as the ice shifts, echoing laser-like tones.",
                 at=[(t, 0, p) for t, p in ((4.1, -0.6), (11.7, 0.5), (19.3, -0.2), (26.8, 0.7), (33.2, -0.7), (41.5, 0.3), (50.4, -0.4), (56.9, 0.6))]),
            dict(tag="penguins", db=-9, dur=2.5, text="A few penguins squawking and honking as they waddle past.",
                 at=[(14.2, 0, 0.3, -0.3), (44.2, 0, 0.3, -0.3)]),
            dict(tag="star", db=-8, dur=2.5, text="A magical twinkling shimmer, like a shooting star sparkling across the sky.", at=[(STAR_T, 0, 0.3)]),
            dict(tag="fish_out", db=-9, dur=1.2, text="A fish being pulled up out of an ice-fishing hole, splash of icy water.", at=[(FISH_T, 0, 0.45)]),
            dict(tag="fish_in", db=-10, dur=1.0, text="A small fish dropping back into an ice hole with a splash.", at=[(FISH_T + 1.5, 0, 0.4)]),
        ],
    }


def library():
    from scenes.library import THUNDER_T, CAT_T
    return {
        "beds": [
            dict(tag="fireplace", db=0, pan=0.2, text=f"A warm cozy fireplace crackling and popping in a quiet wooden room, close and intimate, logs burning steadily. No wind, no rain. {QUIET}"),
        ],
        "events": [
            dict(tag="tick", db=-17, dur=0.5, variants=2, text="A single tick of an old pendulum clock in a quiet room.",
                 at=[(k + 0.5, 0, 0.35) for k in range(60)]),
            dict(tag="quill", db=-17, dur=4.0, variants=2, text="A quill pen writing on parchment paper, gentle scratching.",
                 at=[(6 * k, 0, -0.3) for k in range(10)]),
            dict(tag="page", db=-11, dur=1.0, variants=3, text="Turning one page of an old book, soft paper rustle.",
                 at=[(10 * k, 0, 0.1) for k in range(6)] + [(12 * k + 2, -1, 0.4) for k in range(5)]),
            dict(tag="snore", db=-21, dur=2.0, variants=2, text="A tiny cute soft snore, gentle and sleepy.",
                 at=[(3 * k + 0.3, 0, 0.7) for k in range(20)]),
            dict(tag="thunder", db=-9, dur=6.0, text="Distant soft rolling thunder heard from indoors, muffled and gentle.", at=[(THUNDER_T, 0, 0.0)]),
            dict(tag="meow", db=-10, dur=1.5, text="A cat waking up with a big yawn and a soft sleepy meow.", at=[(CAT_T[0] + 0.4, 0, 0.15)]),
        ],
    }


SPECS = dict(beach=beach, dino=dino, pumpkin=pumpkin, lake=lake, ramen=ramen, cabin=cabin, aurora=aurora, library=library)
