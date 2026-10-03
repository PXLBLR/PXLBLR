# Prompt for Gemini: PXLBLR × NINJA-BLOKS season pack (60-minute loops)

> Paste everything below the line into Gemini and attach the three reference videos:
> `PXLBLR_NinjaBloks_PumpkinPatch_1min_1080p.mp4`, `PXLBLR_NinjaBloks_AutumnLake_1min_1080p.mp4` and `PXLBLR_NinjaBloks_RainyRamen_1min_1080p.mp4`.

---

You are producing three **60-minute** background loop videos for the **PXLBLR** YouTube channel, starring the **NINJA-BLOKS**. People leave these on while they study, work and sleep.

The three attached 1-minute videos are the **quality bar and the exact art direction**. Rebuild each scene to match them as closely as you can: same layout, same characters, same palette, same motion, same timing and same sound design. Then extend each one to 60 minutes using the plan in section 6. Don't redesign anything and don't simplify it. If something here conflicts with your defaults, this brief wins.

## 1. Technical spec (all three videos)

- **Output:** 1920×1080, 30 fps, H.264 High, CRF ≤ 16 (or ~12 Mbps), yuv420p, AAC 256 kbps 48 kHz stereo. Length 60:00.
- **Pixel grid:**
  - Draw every frame on a **384×216 art-pixel canvas** and scale it **exactly 5×** with nearest-neighbour.
  - Every on-screen pixel must be a crisp 5×5 block. No blur, no anti-aliasing, no smooth scaling, and no rotating or resizing sprites off the grid.
  - Slow movers (clouds, ducks, the ghost, the train) may glide at screen-pixel offsets, but the sprites themselves must stay on the 5× grid.
- **Seamless loop:**
  - Every repeating motion must have a period that divides 60 s exactly: 0.4, 0.5, 0.6, 0.75, 1, 1.5, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30 or 60 s.
  - Anything that crosses the screen must wrap by exactly one span per period.
  - **Rain** must fall a whole number of screen heights per minute so it loops.
  - The last frame must flow into the first with no jump.
- **Safe areas:** keep the bottom 12% free of important action, because the YouTube scrubber covers it. Keep the brand bug in the top-left.

## 2. Brand rules (identical in every scene)

### Outline and light

- One outline colour everywhere: `#1A1423`, 1 art-pixel thick, on every character, prop, creature and plant.
- Light comes from one direction per scene:
  - **Pumpkin Patch:** moonlight from the upper right, with lilac rim light `#7A5AA0`.
  - **Autumn Lake:** sunrise behind the hills, with warm rim light `#FFD09A` on top edges.
  - **Ramen:** the warm interior glow plus neon.
- Every sprite gets a 1 px highlight on the edges facing the light and a 1–2 px shade on the far side.

### Dithering

Use ordered (Bayer) dithering only for:
- sky gradients;
- the glow rings around the moon and sun;
- ground light pools;
- fog and mist edges;
- lamp light cones.

Use flat colour fills everywhere else. No noise.

### Corner bug (top-left, every frame)

- an 8×8 red Blok face icon;
- **PXLBLR** in a white 5×7 pixel font with a `#1A1423` outline and drop shadow;
- **NINJA-BLOKS** underneath, in a gold `#FFD23F` 3×5 font.

### In-world brand sign (every scene, matched to the world)

- **Pumpkin Patch and Autumn Lake:** the wooden two-plank signpost.
  - Planks `#C08548`, light `#E0A468`, dark `#94592C`, post `#7A4A24`.
  - **PXLBLR** carved into the top plank in the 5×7 font.
  - **NINJA-BLOKS** carved into the arrow-shaped lower plank in the 3×5 font.
- **Ramen:** neon instead.
  - **PXLBLR** in pink neon `#FF4FA8` on a dark board above the stand.
  - Vertical neon **NINJA** (cyan `#3FF0FF`) on the left building and **BLOKS** (pink) on the right building.
  - **RAMEN** across the five noren curtain panels.
  - **NINJA-BLOKS** in gold on the counter front, between two Blok icons.

### The NINJA-BLOKS (never redesign them)

Each Blok is **28×29 art pixels**, which is 140 px on screen.

- **Body:** a rounded square with a 1 px top-left highlight and a 2 px bottom-right shade. Nub arms (down or raised) and two dark feet.
- **Headband:** 4 px tall, with a **gold four-point shuriken emblem** and a dark centre pixel. A side knot with **two ribbon tails** that flutter on a 1 s cycle.
- **Katana:** a hilt diagonally over one shoulder, with dark and silver wrap and a gold guard.
- **Face:** 4×5 white eyes with 2×3 dark pupils and a 1 px catch-light, a blush mark under each eye, and a small smile.
- **Expressions:** blink every ~5 s, staggered so they never blink together; `^ ^` happy eyes; open mouth or `o` mouth when eating or excited.

**Colourways**

| Blok | Body (light / main / shade) | Headband |
|---|---|---|
| Red | `#FF8F70` / `#EC4A35` / `#B42D27` | navy `#2B2740` |
| Blue | `#86D4FF` / `#3A92F0` / `#2161C0` | purple `#8A3FF0` |
| Black | `#5C5F82` / `#383A52` / `#22233A` | red `#EC4A35` |
| Pink | `#FFBCDC` / `#FF74B3` / `#D64489` | teal `#1EC8B4` |

## 3. Scene A: Haunted Pumpkin Patch (Halloween night)

### Background

- **Sky:** a dithered gradient from `#0C0820` through `#341A5E` and `#6A2C70` to a `#C8585A` horizon glow. About 46 stars twinkle on 2–6 s cycles.
- **Moon:** a big full moon at the upper right (cream `#FFF1C4`, craters `#ECD9A0`) with three dithered violet glow rings.
- **Far hills:** dark `#24163A` with a lilac moonlit ridge line, and small bare-tree silhouettes.
- **Haunted house:** a gabled house with a pointed tower on the left hill. Its windows flicker warm yellow and amber, each on its own 3–12 s cycle.
- **Field:**
  - rows of pumpkins receding into the distance, connected by vines; a few far ones have tiny glowing faces that twinkle;
  - a picket fence across the middle, with a **gate that swings open and closed on a 20 s cycle** and a flickering lantern on the gate post;
  - a scarecrow wearing a **red ninja headband**, with a crow on its arm that turns its head every 4 s;
  - gravestones reading **RIP** and **BOO**, plus a small cross.

### Foreground

- A gnarled bare tree on the left, with an **owl** on a branch that blinks every 6 s.
- Hay bales.
- Three big carved jack-o'-lanterns whose faces flicker on combined 0.5 s and 0.75 s cycles, each with a warm dithered glow pool on the ground.
- Rising purple wisps, falling leaves, and two drifting fog layers (one far, one at ground level over the characters' feet). Draw the fog as solid wisps that are dithered only at the edges.

### Cast

- **Red:** wears a purple witch hat and sits on the hay bales, swinging gently on a 2 s cycle.
- **Blue:** carves a pumpkin. The knife makes three strokes, then rests, on a 6 s cycle.
- **Pink:** shakes a jack-o'-lantern candy bucket every 5 s, with happy eyes, arms up and candy bouncing.
- **Black:** wears a **white ghost-sheet costume that still has its red ninja headband and gold emblem**. Black floats on a 4 s bob, the hem waves, and the shadow below shrinks as Black rises.

### Animated life

- Three bats flap across the sky on 15, 20 and 30 s crossings.

### Headline event

**A big friendly ghost** drifts across the sky in front of the moon, waving.

### Sound

**Ambience**

- wind with gusts on a 20 s cycle;
- a faint howl band around 500–700 Hz;
- crickets swelling on a 12 s cycle;
- leaves rustling;
- soft lantern crackle.

**SFX** (each on its frame and panned to its object)

- owl "hoo-hoo" (left);
- crow caws as its beak opens;
- a wooden gate creak on each swing;
- tiny bat squeaks as bats pass mid-screen;
- a soft "woooo" panned across with the big ghost;
- a distant church bell toll with a long tail;
- quiet knife scrapes;
- candy rattles.

## 4. Scene B: Autumn Lake at Dawn

### Background

- **Sky:** a dithered gradient from `#3C5A96` through `#C4A4BC` and `#F8C89A` to `#FFE2B0`.
- **Sun:** rising behind the hills, with three warm glow rings.
- **Clouds:** pink wispy clouds with peach undersides, drifting one span per 60 s.
- **Mountains:** a misty lavender range `#8A8CBC` with snow caps.
- **Forest:** two rows of autumn trees on the far shore (orange `#E0743A`, red `#C8443A`, gold `#F2B84E`, plus a few dark pines). The back row is hazier, and the front row's tops are rim-lit.

### The lake (signature effect)

- The lake is a **mirror reflection** of the sky, mountains and forest: flipped, tinted toward `#33416E`, and with each row shifted sideways by a sine ripple on a 3 s cycle. The ripple gets stronger toward the viewer.
- Glint dashes drift across the water, and they turn peach in the sun's reflection.
- Morning mist hangs along the far shore as solid wisps with dithered edges, on a 30 s drift.

### Foreground

- A big maple on the left with a dense orange, red and gold canopy, lit from the right, dropping leaves continuously on 6–12 s paths.
- A grassy bank covered in fallen leaves.
- Swaying cattails.
- A wooden dock on the right.
- The PXLBLR signpost.

### Cast

- **Blue and Black** are in a red canoe that has a gold stripe. The canoe drifts on a 60 s cycle and has a translucent dithered reflection.
  - **Blue** fishes. The bobber bobs on a 2 s cycle with ripple rings.
  - **Black** paddles on a 3 s stroke, splashing as the blade enters the water.
- **Pink** sits on the end of the dock with a steaming mug. Steam curls rise on a 3 s cycle, and Pink sometimes closes their eyes happily.
- **Red** rakes leaves on a 2 s stroke, then **runs and jumps into the leaf pile**. Leaves burst out, Red peeks out with `^ ^` eyes, then hops back and goes back to raking.

### Animated life

- A loon swims and **dives every 20 s**: it disappears with ripple rings and resurfaces further along.
- A V of five ducks crosses the sky every 30 s.

### Headline event

**A deer** steps out from the trees on the far left shore, drinks from the lake (with its own reflection), then walks back.

### Sound

**Ambience**

- gentle water lapping on a 5 s swell;
- small random water plips;
- wind through the leaves in 15 s gusts;
- dawn birdsong.

**SFX**

- the long, echoing loon wail;
- loon dive and resurface plops;
- paddle swishes on every stroke, panned with the canoe;
- duck quacks as the V passes;
- quiet rake scrapes on every stroke;
- a big leaf-pile crunch on the jump and a smaller one on the hop out;
- a twig snap when the deer appears.

## 5. Scene C: Rainy Neon Ramen Stand

### Background

- A night city alley with tall dark buildings left and right (`#1A1F36`).
- The windows switch on and off at random on 5–20 s cycles, in warm `#FFCF8A` and cool `#BFE8FF`.
- A far skyline in the middle with tiny lit windows and blinking red aircraft lights.
- An elevated train track crossing the upper frame.
- Vertical neon **NINJA** (cyan) and **BLOKS** (pink) signs on the buildings.
- A glowing vending machine on the left with rows of coloured bottles.
- A street lamp on the right with a dithered light cone. Raindrops turn bright inside the cone.

### The ramen stand (centre)

- A wide wooden roof with a red trim line.
- The **PXLBLR pink neon sign** on top.
- Two red paper lanterns swinging on a 4 s cycle.
- Five indigo noren curtains spelling **R A M E N** that flutter on a 2 s cycle.
- A warm, dithered interior glow with a bowl shelf, menu tags and a steaming stock pot.
- A wooden counter with **NINJA-BLOKS** in gold on its front.
- Red stools under the eaves.

### Cast

- **Black** is the chef. Black lifts a noodle strainer from the pot every 3 s, with water dripping.
- **Red** (left stool) and **Blue** (right stool) eat ramen. Every 6 s, offset by 3 s from each other, they lift noodles with chopsticks to an `o` mouth with happy eyes. Steam rises from their bowls.
- **Pink** stands under a clear dithered umbrella by the vending machine, with rain bouncing off the canopy.
- An orange cat sleeps on a crate under the lamp, flicking its tail every 4 s.

### Rain and water

- **Rain:** three parallax layers, all slanted the same way:
  - far: dim and short, behind the stand;
  - mid;
  - near: bright and long, in front of everything.
- **Drips:** water drips off the roof edge on 1.5 s and 2 s cycles.
- **Street:**
  - splash crowns pop on the wet street;
  - puddles show expanding ripple rings;
  - **reflections shimmer on the wet asphalt:** wobbly vertical streaks of every light source (pink neon, red lanterns, vending machine, lamp), fading and narrowing downward.

### Recurring events

- The neon "L" in PXLBLR flickers out briefly a few times a minute.
- The whole sign occasionally dips dark for an instant.

### Headline event

**A commuter train** with four lit cars crosses the elevated track, with sparks at the pantograph.

### Sound

**Ambience**

- a steady rain bed (broadband hiss plus dense droplet ticks), slightly different in each channel;
- rain pattering on the awning;
- a low city hum;
- a soft 120 Hz neon buzz;
- broth simmering and sizzling at the centre.

**SFX**

- slurps synced to each noodle lift (Red on the left, Blue on the right);
- a quiet strainer swish;
- plips for the drips, panned to each drip's x position;
- an electric zap on every neon flicker;
- the train: low rumble, rail clacks and a faint motor whine, panned right to left with the train;
- wet-tyre car passes, panned across, from an unseen street.

## 6. How to build each 60-minute video

1. **Rebuild the 1-minute master loop** to match the reference video. Frame 1800 must equal frame 0.
2. **Make variant loops that share identical first and last frames,** so any order of them splices seamlessly.
   - **A:** the calm base, with no headline event.
   - **B:** the headline event (big ghost, deer, or train).
   - **C:** a secondary event:
     - **Pumpkin:** a black cat walks along the fence.
     - **Lake:** a fish jumps by the canoe.
     - **Ramen:** a delivery scooter's headlights sweep past.
   - **D:** the same as A, but the Bloks swap or vary their activities.
3. **Sequence the variants so the big moments are rare and unpredictable:**

   | Scene | Event spacing |
   |---|---|
   | Pumpkin | Ghost every 6–9 min. Owl hoots every 1–3 min. Bell only at 15, 30, 45 and 60 min. |
   | Lake | Deer every 7–10 min. Leaf-pile jump every 4–6 min. Loon calls every 2–4 min. Ducks every ~3 min. |
   | Ramen | Train every 4–6 min. Neon flicker every 1–3 min. Car passes every 1–2 min. |

   Never put a headline event on a fixed 60 s beat.
4. **Make the audio a separate, non-repeating 60-minute track.**
   - Use long, slowly evolving beds with no audible 60 s repetition.
   - Re-time the event SFX to whichever variant is on screen.
   - Fade in over 5 s and out over 10 s.
   - Mix to about −19 dBFS RMS with peaks at −1 dBFS or below.
   - These videos are for sleep and study, so nothing may be harsh or startling. Keep the roar-level moments soft and distant.
5. **Concatenate the variants and mux the audio without re-encoding:**

   ```
   ffmpeg -f concat -safe 0 -i playlist.txt -i ambience_60min.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest PXLBLR_<scene>_60min.mp4
   ```

## 7. QA checklist (check every video before delivery)

- [ ] At 200% zoom, every pixel is a sharp 5×5 block, with no blur and no mixed pixel sizes.
- [ ] All four Bloks match the master design and colourways, and they blink at different times.
- [ ] The corner bug and the in-world brand signs are crisp and readable.
- [ ] Playing the last 3 s and then the first 3 s of the master loop shows no jump and no audio click.
- [ ] Every SFX lines up with its on-screen action to within one frame and is panned to the right place.
- [ ] The light direction and rim light are consistent within each scene, and every scene has at least four depth layers.
- [ ] Nothing important sits in the bottom 12% of the frame.
- [ ] Headline events are spaced several minutes apart in the 60-minute cut, never every minute.
