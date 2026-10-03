# Prompt for Gemini: PXLBLR × NINJA-BLOKS winter and cosy pack (60-minute loops)

> Paste everything below the line into Gemini and attach the three reference videos:
> `PXLBLR_NinjaBloks_ChristmasCabin_1min_1080p.mp4`, `PXLBLR_NinjaBloks_NorthernLights_1min_1080p.mp4` and `PXLBLR_NinjaBloks_TreehouseLibrary_1min_1080p.mp4`.

---

You are producing three **60-minute** background loop videos for the **PXLBLR** YouTube channel, starring the **NINJA-BLOKS**. People leave these on while they study, work and sleep, so the mood is calm and cosy.

The three attached 1-minute videos are the **quality bar and the exact art direction**. Rebuild each scene to match them as closely as you can: same layout, same characters, same palette, same motion, same timing and same sound design. Then extend each one to 60 minutes using the plan in section 6. Don't redesign anything and don't simplify it. If something here conflicts with your defaults, this brief wins.

## 1. Technical spec (all three videos)

- **Output:** 1920×1080, 30 fps, H.264 High, CRF ≤ 16 (or ~12 Mbps), yuv420p, AAC 256 kbps 48 kHz stereo. Length 60:00.
- **Pixel grid:**
  - Draw every frame on a **384×216 art-pixel canvas** and scale it **exactly 5×** with nearest-neighbour.
  - Every on-screen pixel must be a crisp 5×5 block. No blur, no anti-aliasing, no smooth scaling, and no rotating or resizing sprites off the grid.
  - Slow movers (the sleigh, the penguins) may glide at screen-pixel offsets, but the sprites themselves must stay on the 5× grid.
- **Seamless loop:**
  - Every repeating motion must have a period that divides 60 s exactly: 0.5, 0.6, 0.75, 1, 1.5, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30 or 60 s.
  - **Snow and rain** must fall a whole number of screen heights per minute so they loop.
  - The last frame must flow into the first with no jump.
- **Safe areas:** keep the bottom 12% free of important action, because the YouTube scrubber covers it. Keep the brand bug in the top-left.
- **Lightning:** the lightning flash in the library is a brief palette shift toward cool white across the whole frame, lasting 3 short flickers. Don't use a strobe and don't go to pure white. These videos are for sleep.

## 2. Brand rules (identical in every scene)

### Outline and light

- One outline colour everywhere: `#1A1423`, 1 art-pixel thick, on every character, prop, creature and plant.
- Light comes from one direction per scene:
  - **Cabin:** cool moonlight from the upper right, plus warm window light pooling on the snow.
  - **Ice camp:** green aurora light rim-lighting the top edges of snow, peaks and the igloo `#9FFFD0`, plus warm campfire light.
  - **Library:** warm candle and fireplace glow, with cool light from the window.

### Dithering

Use ordered (Bayer) dithering only for:
- sky gradients;
- moon and light glow rings;
- the light pools on snow and floors;
- the body of the aurora curtains.

Use flat colour fills everywhere else. No noise.

### Corner bug (top-left, every frame)

- an 8×8 red Blok face icon;
- **PXLBLR** in a white 5×7 pixel font with a `#1A1423` outline and drop shadow;
- **NINJA-BLOKS** underneath, in a gold `#FFD23F` 3×5 font.

### In-world brand

- **Cabin and Ice camp:** the wooden two-plank signpost **with snow piled on top of both planks**.
  - Planks `#C08548`, light `#E0A468`, dark `#94592C`, post `#7A4A24`.
  - **PXLBLR** carved into the top plank in the 5×7 font.
  - **NINJA-BLOKS** carved into the arrow-shaped lower plank in the 3×5 font.
- **Library:** two in-world brand pieces instead of the signpost.
  - A red **PXLBLR pennant** with gold 5×7 letters, hanging on the wall.
  - A framed photo of the red Blok on the mantel.

### The NINJA-BLOKS (never redesign them)

Each Blok is **28×29 art pixels**, which is 140 px on screen.

- **Body:** a rounded square with a 1 px top-left highlight and a 2 px bottom-right shade. Nub arms (down or raised) and two dark feet.
- **Headband:** 4 px tall, with a **gold four-point shuriken emblem** and a dark centre pixel. A side knot with **two ribbon tails** that flutter on a 1 s cycle.
- **Katana:** a hilt diagonally over one shoulder, with dark and silver wrap and a gold guard.
- **Face:** 4×5 white eyes with 2×3 dark pupils and a 1 px catch-light, a blush mark under each eye, and a small smile.
- **Expressions:** blink every ~5 s, staggered so they never blink together; `^ ^` happy or sleeping eyes; open mouth when excited.

**Colourways**

| Blok | Body (light / main / shade) | Headband |
|---|---|---|
| Red | `#FF8F70` / `#EC4A35` / `#B42D27` | navy `#2B2740` |
| Blue | `#86D4FF` / `#3A92F0` / `#2161C0` | purple `#8A3FF0` |
| Black | `#5C5F82` / `#383A52` / `#22233A` | red `#EC4A35` |
| Pink | `#FFBCDC` / `#FF74B3` / `#D64489` | teal `#1EC8B4` |

**Winter scarves (Cabin and Ice camp only)**

Each Blok wears a striped scarf across its lower body, under the mouth. One end hangs down and sways on a 2 s cycle. Each Blok keeps its own scarf colours:

| Blok | Cabin | Ice camp |
|---|---|---|
| Red | green / white | green / white |
| Blue | gold / red | pink / white |
| Black | teal | gold / red |
| Pink | purple / gold | purple / gold |

## 3. Scene A: Snowy Christmas Cabin (night)

### Background

- **Sky:** a dithered gradient from `#0A1030` to `#5A6EA8`, with about 36 twinkling stars.
- **Moon:** a big pale moon at the upper right (`#EEF4FF`) with three blue glow rings.
- **Mountains:** snowy mountains with bright moonlit ridges.
- **Forest:** two rows of snow-capped pines.
- **Snow field:** gently undulating, with ground sparkles that twinkle.

### The log cabin (centre)

- Log walls with round log ends at the corners.
- A thick snow roof with icicles.
- A stone chimney with smoke puffs rising and drifting every 10 s.
- **String lights** along the roofline that chase in red, green, gold and blue on a 2 s cycle.
- **Left window:** a little Christmas tree with blinking bulbs.
- **Right window:** a fireplace flickering on combined 0.5 s and 0.75 s cycles.
- A door with a green wreath and red bow, and a door lantern.
- Warm light pools on the snow in front, and footprints leading to the door.

### Snowfall

Snow falls in three parallax layers: a far one behind the cabin, and a mid and a near one in front of everything.

### Cast

- **Black** stands on a ladder at the left gable, hanging lights. Arms go up with happy eyes on a 2 s cycle.
- **Red** pats a snowman on a 2 s cycle, with snow puffs. **The snowman wears a red ninja headband with a gold emblem.**
- **Blue** hops happily every 4 s.
- **Pink** sleds down the hill on the right on a 15 s cycle:
  - slides down for 2.5 s with a snow spray, mouth open and arms up;
  - rests for 1.5 s;
  - walks back up the slope, dragging the sled, for 11 s.
- A white bunny hops across the far field every 30 s.

### Headline event

**Santa's sleigh and four reindeer** cross in front of the moon in silhouette, with the lead reindeer's red nose glowing and moonlit rim light on the sleigh.

### Sound

**Ambience**

- soft wind in 20 s gusts, with a faint whistle;
- the hush of falling snow;
- fireplace crackle and a low rumble, muffled as if heard from inside the cabin.

**SFX**

- sleigh bells panned right to left with the sleigh;
- a sled whoosh on each run;
- snow-crunch footsteps as Pink walks back up;
- soft pats on the snowman;
- crunches when Blue lands.

## 4. Scene B: Northern Lights Ice Camp (night)

### Sky and aurora

- **Sky:** a dithered gradient from `#03061A` to `#1A3E5E`, with about 80 stars.
- **Aurora (signature effect):** two overlapping curtains, built like this:
  - **Bottom edge:** the curtain's bottom edge undulates on 20 s and 15 s cycles.
  - **Height:** the curtain's height breathes on a 12 s cycle.
  - **Rays:** vertical ray striations shimmer on a 6 s cycle.
  - **Colour, from the bottom edge up:** a bright mint edge `#D8FFF0`, then green `#5CFFAA` / `#22C98A`, then teal `#2AB8B0`, then purple tips `#A070FF` / `#5A3AB0`.
  - **Body:** ordered-dithered, with a dark teal haze filling the gaps.
- **Mountains:** dark glacier peaks with dithered snow caps and aurora-green rim light.

### The lake and camp

- **Frozen lake:** ice with cracks and snow patches, showing a **dimmed, checker-dithered reflection of the aurora**.
- **Snow bank:** in the foreground, with a green-tinted lip.
- **Igloo (left):** ice-block lines and a warm glowing doorway.
- **Campfire:** a stone ring and log seats, with flames and sparks.
- **Diamond dust:** tiny ice sparkles drifting and twinkling.

### Cast

- **Red and Pink** sit by the fire sipping cocoa. The mugs lift every 6 s, offset from each other, with happy eyes. Steam curls rise.
- **Blue** ice-fishes from a stool on the frozen lake. The ice hole has ripple rings.
  - **Fish event (48–50 s):** the rod tugs, a fish arcs out of the hole with splashes, then drops back in.
- **Black** stands at a telescope on a tripod, slowly sweeping the sky on a 20 s cycle.
- Three **penguins** waddle across the far ice every 30 s.

### Headline event

**A shooting star** streaks across the sky with a long fading tail. Black cheers, jumping with arms up, mouth open and happy eyes.

### Sound

**Ambience**

- low arctic wind in 30 s gusts, with a faint high whistle;
- a very quiet airy shimmer under the aurora;
- campfire crackle on the left.

**SFX**

- the eerie "pew" pings of the frozen lake, a few per minute at random pans;
- penguin squawks as they cross;
- a sparkling chime with the shooting star;
- the fish splash out, flop and splash back.

## 5. Scene C: Cozy Treehouse Library (indoors, rainy night)

### The room

- **Walls and ceiling:** vertical plank walls with warm dithered glow pools from the candle and the fireplace, and a dark ceiling beam.
- **Fairy lights:** a string of warm lights hanging in swags along the beam, twinkling on 2–6 s cycles.
- **Bookshelf (left):** a tall shelf packed with colourful book spines (a few leaning), a globe and a rolling ladder.
- **Round window (centre):**
  - outside: a rainy night with tree branches, a small moon, and rain streaks that loop;
  - on the glass: drops sliding down, leaving trails.
- **PXLBLR pennant** hanging on the wall.
- **Pendulum clock:**
  - the pendulum swings on a 2 s cycle;
  - the minute hand sweeps once per minute.
- **Stone fireplace (right):** big flickering flames and sparks, with a mantel holding candles, a steaming blue mug and the framed red-Blok photo.
- **Floor:** wooden planks with a round red and gold rug.
- **Furniture and plants:** a red armchair, a teal floor cushion and a potted plant.

### Cast

- **Red** writes at a desk with a quill on a 6 s cycle: 4 s writing, 2 s looking up. The desk has a candle, an inkwell, papers and stacked books.
- **Pink** reads in the armchair. **An orange cat naps curled on Pink's lap.** Pink turns a page every 10 s.
- **Blue** reads on the floor cushion and turns a page every 12 s.
- **Black** is asleep in a teal hammock strung above the fireplace. The hammock sways on a 4 s cycle, and **Zzz** letters float up every 3 s.
- Dust motes drift in the warm light.

### Headline event

**Lightning** (30 s): the window flashes and the room shifts to cold white for 3 flickers. Thunder rolls about a second later. **The cat wakes**, climbs onto the chair back, **stretches and meows**, then curls back up on Pink's lap.

### Sound

**Ambience**

- rain on the window and roof, softened as if heard from indoors;
- fireplace crackle and a low rumble on the right;
- a soft cat purr while the cat sleeps.

**SFX**

- a clock tick-tock every second, synced to the pendulum;
- quill scratches while Red writes;
- page turns for Pink and Blue;
- a gentle snore from the hammock;
- rolling thunder;
- the cat's meow.

## 6. How to build each 60-minute video

1. **Rebuild the 1-minute master loop** to match the reference video. Frame 1800 must equal frame 0.
2. **Make variant loops that share identical first and last frames,** so any order of them splices seamlessly.
   - **A:** the calm base, with no headline event.
   - **B:** the headline event (sleigh, shooting star, or lightning with the cat stretch).
   - **C:** a secondary event:
     - **Cabin:** an owl lands on the chimney.
     - **Ice camp:** an arctic fox trots past.
     - **Library:** a book slides off the shelf and Blue catches it.
   - **D:** the same as A, but the Bloks vary their activities. Examples:
     - **Cabin:** a snowball toss.
     - **Ice camp:** Pink builds a mini snow-Blok.
     - **Library:** Red stretches and sips tea.
3. **Sequence the variants so the big moments are rare and unpredictable:**

   | Scene | Event spacing |
   |---|---|
   | Cabin | Sleigh every 7–10 min. Pink sleds continuously. |
   | Ice camp | Shooting star every 5–8 min. Penguins every 2–4 min. Fish caught every 6–9 min. Lake pings at random, a few per minute. |
   | Library | Lightning every 8–12 min, at most. Page turns continuously. |

   Never put a headline event on a fixed 60 s beat.
4. **Make the audio a separate, non-repeating 60-minute track.**
   - Use long, slowly evolving beds with no audible 60 s repetition.
   - Re-time the event SFX to whichever variant is on screen.
   - Fade in over 5 s and out over 10 s.
   - Mix to about −19 dBFS RMS with peaks at −1 dBFS or below.
   - The thunder must stay distant and soft, with nothing startling.
5. **Concatenate the variants and mux the audio without re-encoding:**

   ```
   ffmpeg -f concat -safe 0 -i playlist.txt -i ambience_60min.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest PXLBLR_<scene>_60min.mp4
   ```

## 7. QA checklist (check every video before delivery)

- [ ] At 200% zoom, every pixel is a sharp 5×5 block, with no blur and no mixed pixel sizes.
- [ ] All four Bloks match the master design and colourways, with the right winter scarves, and they blink at different times.
- [ ] The corner bug and the in-world brand pieces are crisp and readable.
- [ ] Playing the last 3 s and then the first 3 s of the master loop shows no jump and no audio click.
- [ ] Every SFX lines up with its on-screen action to within one frame and is panned to the right place.
- [ ] The light direction and rim light are consistent within each scene, and every scene has at least four depth layers.
- [ ] Nothing important sits in the bottom 12% of the frame.
- [ ] Headline events are spaced several minutes apart in the 60-minute cut, never every minute.
- [ ] The lightning flash is gentle: no strobing and no full-white frames.
