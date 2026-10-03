# Prompt for Gemini: PXLBLR × NINJA-BLOKS 60-minute ambient loops

> Paste everything below the line into Gemini and attach the two reference videos:
> `PXLBLR_NinjaBloks_Beach_1min_1080p.mp4` and `PXLBLR_NinjaBloks_Dino_1min_1080p.mp4`.

---

You are producing 60-minute background loop videos for the **PXLBLR** YouTube channel, starring the **NINJA-BLOKS**. People use these videos to study, work, relax and sleep. The two attached 1-minute videos set the quality bar and the house style. Match them or beat them. Don't fall back to the look of earlier drafts.

## 1. What was wrong with the previous draft (don't repeat it)

1. **Mixed pixel sizes and blur.** It was rendered at 854×480 and upscaled with smoothing, so the pixel edges came out soft and pixels in different parts of the frame had different sizes.
2. **The Bloks were inconsistent.** Each character had different proportions, headbands, eyes and outline weight, so they didn't read as one cast.
3. **The branding was illegible.** The "PXL" sign was cut off and blurry, and there was no consistent wordmark.
4. **The scene was flat.** It had one or two depth layers, no lighting, no rim light and no shadows, and the sky and sea were busy with noisy dithering everywhere.
5. **Almost nothing moved, and the loop jumped.** Characters stood still, and positions didn't match at the loop point.
6. **The audio didn't match the picture.** None of the sound effects lined up with what was happening on screen.

## 2. Non-negotiable technical spec

- **Output:** 1920×1080, 30 fps, H.264 High, CRF ≤ 16 (or ~12 Mbps), yuv420p, AAC 256 kbps 48 kHz stereo.
- **Pixel grid:** draw every scene on a **384×216 art-pixel canvas** and scale it **exactly 5×** with nearest-neighbour. Every on-screen pixel must be a crisp 5×5 block, and there must be no blur, no anti-aliasing, no bilinear filtering and no sub-pixel rotation. Sprites must never be scaled or rotated off the grid.
- **Motion:** slow objects (clouds, boats, dinosaurs) may glide at screen-pixel offsets, but the sprites themselves stay on the 5× grid.
- **Seamless loop:**
  - Every animation must have a period that divides the loop length exactly. For a 60 s loop, use periods of 0.5, 0.6, 0.75, 1, 1.5, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30 or 60 s.
  - Anything that travels across the screen must wrap by exactly one span per period.
  - The last frame must flow directly into the first. Test this by playing the final 3 s followed by the first 3 s.
- **Safe areas:**
  - Keep the bottom 12% of the frame free of important detail, because the YouTube scrubber covers it.
  - Keep the brand bug in the top-left corner.

## 3. Brand bible (use it exactly)

### Outline and line work

- **One outline colour everywhere:** `#1A1423`, 1 art-pixel thick, on every character, prop and creature.
- **Key light** comes from the top-left in the beach scene and from the low sun in the dino scene.
  - Each sprite gets a 1 px highlight on the edges that face the light.
  - Each sprite gets a 1–2 px shade on the far side and the bottom.
  - The golden-hour scene adds a warm rim light (`#FFCF8A`) to the top edges of every creature and plant.

### Dithering

Use ordered (Bayer) dithering **only** in these places:
- sky gradients;
- the sun's glow rings;
- soft ground glows, such as campfire light.

Use flat colour fills everywhere else. Don't add noise.

### Corner bug (top-left, every frame)

- an 8×8 red Blok face icon;
- **PXLBLR** in a white 5×7 pixel font with a `#1A1423` outline and drop shadow;
- **NINJA-BLOKS** underneath, in a gold `#FFD23F` 3×5 pixel font.

### In-world signpost (in every scene, same design each time)

- Wooden planks: `#C08548`, light `#E0A468`, dark `#94592C`, post `#7A4A24`.
- The top plank has **PXLBLR** carved into it in the 5×7 font.
- The lower plank is arrow-shaped and has **NINJA-BLOKS** carved into it in the 3×5 font.
- All text must be fully legible at 1080p.

### Brand colours

| Role | Hex |
|---|---|
| Red | `#EC4A35` |
| Gold | `#FFD23F` |
| Teal | `#1EC8B4` |
| Blue | `#3A92F0` |
| Purple | `#8A3FF0` |
| Pink | `#FF74B3` |
| Ink (outline) | `#1A1423` |

## 4. The NINJA-BLOKS: one master design, four colourways

Each Blok is **28×29 art pixels**, which is 140 px tall on screen.

### Body

- a rounded square (3 px corner radius);
- a 1 px top-left highlight and a 2 px bottom-right shade;
- two nub arms, which can be down or raised;
- two dark feet.

### Headband and katana

- The headband is 4 px tall across the forehead.
- It has a **gold four-point shuriken emblem** in the centre with a dark centre pixel.
- The knot sits on the side of the head.
- **Two ribbon tails** flutter on a 1 s cycle.
- A **katana hilt** pokes up diagonally over one shoulder. The grip has alternating dark and silver wrap, and the guard is gold.

### Face

- The eyes are 4×5 white ovals with 2×3 dark pupils, each with a 1 px white catch-light. The pupils look toward the action.
- There is a blush mark under each eye.
- The mouth is a small smile.
- Expressions: blink every ~5 s, staggered so the Bloks never blink together; open mouth when excited; `^ ^` closed eyes when calm; sunglasses when chilling.

### Colourways

| Blok | Body (light / main / shade) | Headband |
|---|---|---|
| Red | `#FF8F70` / `#EC4A35` / `#B42D27` | navy `#2B2740` |
| Blue | `#86D4FF` / `#3A92F0` / `#2161C0` | purple `#8A3FF0` |
| Black | `#5C5F82` / `#383A52` / `#22233A` | red `#EC4A35` |
| Pink | `#FFBCDC` / `#FF74B3` / `#D64489` | teal `#1EC8B4` |

Never redesign the Bloks per scene. Only their props and actions change.

## 5. Scene direction

### A. Beach Day

**Background layers**

- **Sky:** a dithered gradient from `#2457C9` at the top to `#CDEEFC` at the horizon.
- **Sun:** at the upper right, with three dithered glow rings. Eight rays step-rotate every 1.5 s and pulse on a 3 s cycle.
- **Clouds:**
  - The far clouds are small and pale and drift on a 224 px strip that wraps once every 60 s.
  - The near clouds are puffy, with shaded bottoms, and cross the screen once every 60 s.
- **Horizon:** a distant hazy island with a striped lighthouse whose lamp blinks every 3 s. A sailboat crosses the horizon once every 60 s, bobbing on a 3 s cycle.

**Ocean and shore**

- The ocean has six depth bands. Drifting wave dashes get longer and brighter toward the shore.
- Sparkles twinkle, concentrated in the sun's reflection.
- The shoreline has a turquoise shallow band, a wet-sand band and a broken white foam edge.
- The swell comes in on a 6 s cycle and **rolls along the beach**, reaching the left side before the right.

**Cast**

- **Red and Blue** play a volleyball rally over a net. A hit happens every 2 s, and each player jumps with arms up and mouth open on their hit. The ball spins, and its shadow shrinks as the ball rises.
- **Black** surfs back and forth on a yellow board on a 30 s cycle, leaving a foam wake.
- **Pink** lounges in sunglasses on a striped towel under a red, white and gold umbrella, bobbing to the music on a 1 s cycle, with a coconut drink beside her.

**Props and life**

- the PXLBLR sign;
- a sandcastle with a waving red flag;
- a bucket and spade;
- an upright branded surfboard;
- a crab scuttling along the wet sand on a 12 s cycle;
- two gulls crossing on 20 s and 30 s cycles;
- two framing palms whose fronds sway on a 4 s cycle;
- shells, a starfish and footprints.

### B. Dino Valley (golden hour)

**Sky and distance**

- **Sky:** a dithered gradient from `#2B1D5A` through `#CC5A86` and `#F89E66` to `#FFE08E`.
- **Sun:** a large low sun with three warm glow rings and thin cloud streaks across it. Faint stars twinkle at the top of the sky.
- **Volcano:** a purple volcano with a flickering crater glow, a lava trickle and **one smoke puff per second**. Each puff rises and drifts for 9 s.
- **Ridges:** two mountain ridges with warm rim light.
- **Canopy:** a dark teal jungle canopy whose tops catch the sunset.

**Dinosaurs**

- **Brachiosaurus:** crosses the whole frame once per loop on an 8-frame walk cycle (2 s stride). It passes in front of the canopy and behind the waterfall cliff.
- **T-Rex:**
  - It rises from behind the canopy at 23.5 s.
  - It **roars with its mouth open and a slight shake at 28 s**, and a flock of birds scatters from the trees.
  - It sinks back by 35.5 s.
- **Pterosaurs:** two of them fly across on 20 s and 30 s cycles with 3-frame wing flaps.
- **Baby triceratops:** it wags its tail and blinks.

**Water**

- The river reflects the sunset and flows to the right. A glitter column sits under the sun.
- Two rocks in the river have ripple rings.
- On the right, a waterfall pours over a cliff, with streaks scrolling down and mist puffs at the base.

**Cast**

- **Blue** fishes from a rock. The bobber bobs on a 2 s cycle, there's a bite every 15 s, and a fish jumps every 20 s.
- **Red and Pink** sit on logs at a campfire, which flickers on combined 0.5 s and 0.75 s cycles with rising sparks. Pink toasts a marshmallow.
- **Black** meditates, floating above a rock pillar on a 4 s cycle, with gold sparkles orbiting every 6 s.

**Props and life**

- a nest of three speckled eggs, one of which wobbles every 5 s;
- swaying tree ferns and ground ferns;
- fireflies blinking along slow looping paths;
- the PXLBLR sign.

## 6. Audio: ambience plus SFX that match the frame

Every sound effect must land on the frame where it happens on screen and be panned to that object's position on screen.

### Beach

**Ambience**

- **Surf:** the wash swells and crashes exactly with the visible 6 s swell, with fizz as the water retreats. Because the wave rolls left to right, the left channel crashes before the right.
- low wind;
- palm rustle on the 4 s sway.

**SFX**

- gull calls when a gull crosses mid-screen;
- a soft volleyball "pok" on every hit, panned left for Red and right for Blue.

### Dino Valley

**Ambience**

- river flow;
- a waterfall on the right;
- campfire crackle in the centre;
- crickets and insects swelling on a 12–20 s cycle;
- distant volcano rumble on the left;
- occasional birdsong.

**SFX**

- brachiosaurus footfalls (deep thumps) panned and faded with its position;
- a T-Rex roar with a long reverb tail at 28 s;
- wing flutter as the birds scatter;
- pterosaur screeches;
- a fish splash in and out;
- a bobber plop on each bite.

### Mix

- Aim for about −19 dBFS RMS with peaks at −1 dBFS or below.
- The beds must stay calm, with no harsh transients and nothing startling. These videos are for sleep and study.
- Every bed must loop with no click at the seam.

## 7. How to build the 60-minute version

1. **Make the 60 s master loop** to the spec above. Frame 1800 must equal frame 0.
2. **Make variant loops** that share the identical first and last frame, so any order of them splices seamlessly. For example:
   - **A** is the calm base.
   - **B** adds the headline event: the T-Rex roar, or a dolphin jump at the beach.
   - **C** adds a pterosaur flock, or a passing cruise ship at the beach.
   - **D** is the same as A but the Bloks swap activities.
3. **Sequence the variants** so that big events happen only every 4–8 minutes, never on a predictable 60 s beat. For example: A A A B A A C A A A D A …, sixty minutes in total.
4. **Make the audio a separate, non-repeating 60-minute track.**
   - Build it from long, slowly evolving ambience beds, with no audible 60 s repetition.
   - Re-time the event SFX to whichever variant is playing.
   - Fade in over the first 5 s and out over the last 10 s.
5. **Concatenate and mux without re-encoding:**

   ```
   ffmpeg -f concat -safe 0 -i playlist.txt -i ambience_60min.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest PXLBLR_<scene>_60min.mp4
   ```

## 8. QA checklist before delivery

- [ ] At 200% zoom, every pixel is a sharp 5×5 block, with no blur and no mixed pixel sizes.
- [ ] All four Bloks match the master design, use the exact colourways and blink at different times.
- [ ] The PXLBLR and NINJA-BLOKS text on the bug and the sign is crisp and readable.
- [ ] Playing the last 3 s and then the first 3 s shows no jump and no audio click.
- [ ] Every sound effect lines up with its on-screen action to within one frame and is panned to the right place.
- [ ] Every scene has at least four depth layers, with consistent light direction, rim light and shadows.
- [ ] Nothing important sits in the bottom 12% of the frame.
- [ ] Big events are spaced 4–8 minutes apart in the 60-minute cut.
