# Store Versile – Miniature Room Frame
## Stage 1: Reference analysis & component inventory · Stage 2: Dimensioned layout proposal

**Status: Rev B. Your answers are applied (see §0). Waiting for final layout approval; no STLs yet.**

## 0. Rev B: decisions from the customer (supersede anything below)
| # | Decision | What changed |
|---|---|---|
| 1 | **8 photo frames** (not 10) | The frame on the TV console (F6) was replaced by a small fern in a swirl pot (same parts as PD). The bottom-left frame in the shelving unit (F10) was replaced by a 2-book stack (same parts as the console books). **No new parts were needed.** Frames left: 3 on shelves, 2 on the wall, 3 in the shelving unit, plus the quote plaque |
| 2 | **Internal depth is 25 mm** (was 50) | The front view (all widths and heights) is **unchanged**. Every part is made shallower, like a relief. Round pots, the cup and the vases become **oval in plan**, so they still look round from the front. New depth plan below |
| 3 | Printed floor tiles + wood sticker | Approved: 3 tiles, 2 mm thick, each 106 / 112 / 82 × 25 mm |
| 4 | Plain A1 Mini (no AMS, 0.4 mm nozzle) | Every part is **single colour**. Multi-colour items are split into separate parts that are glued together: console body (black) + drawer fronts (white) + legs (white); every pot (white) + leaves (green). Tiny accents (bunny's pink ears, book spine titles) are paint or printed paper labels. The name plate can use Bambu Studio's "pause/change filament at layer" for 2-colour text. All details are sized for a 0.4 mm nozzle: ≥ 0.8 mm walls and leaves, ≥ 1 mm pins |
| 5 | 3D-printed leaves | Leaves are printed **flat** (0.8–1.0 mm thick, leaflets ≥ 1 mm wide) as fan-shaped sprays that slot into the pot. The fans are mostly flat (side to side), which suits the 25 mm depth |
| 6 | Plain cup, no logo | Plain takeaway cup with lid and a raised sleeve band |

### Rev B depth plan (Y, back wall 0 → glass 25)
| Layer | Y range | Depth |
|---|---|---|
| Fluted panels (1.2 backer + 1.2 flutes) | 0 – 2.4 | 2.4 |
| Arch backer 1.0 + border 2.5 wide × 2 high | 0 – 3.0 | 3.0 |
| Photo frames (all) | 2.4 – 5.5 | 2.5 thick |
| Floating shelves | 2.4 – 10.4 | 8 |
| TV console | 2.4 – 12.4 | 10 |
| Shelving unit | 2.4 – 14.4 | 12 (boards 2.5) |
| Coffee table | 5 – 19 | 14 |
| Floor plants (oval vase 15 × 10, flat fan foliage) | 4 – 20 | 16 |
| **Keep-out to glass** | 22 – 25 | ≥ 3 mm everywhere (closest part: plant leaves at 20 → 5 mm clear) |
| LED strip channel (optional) | 17 – 22, z 192 – 198 | |

**Effect of 25 mm:** the room looks almost the same from the front, but there's less 3D depth when you view it from the side. The furniture reads more like a high relief than a full dollhouse. All parts still fit and print.

> The original Rev A text below is kept for reference. Where a depth or frame count below differs from §0, **§0 applies**. Exact current numbers for every part are in `component_envelopes.md`.

---

Box: 300 W × 200 H × 50 D mm inside · Printer: Bambu Lab A1 Mini (180³ mm) · PLA · Bambu Studio
Coordinates: X = width (0 = inner left wall) · Y = depth (0 = back wall, 50 = inner face of glass) · Z = height (0 = inner floor)

Drawings (in `room-frame/drawings/`):
- `front_layout.svg/.png`: dimensioned front elevation
- `side_section.svg/.png`: how the 50 mm depth is shared out
- `plan_view.svg/.png`: footprints on the floor tiles
- `../docs/component_envelopes.md`: exact X/Y/Z box for every part, generated from `layout/layout.py`

---

## 1. How the dimensions were derived

1. I put a pixel grid over the straight-on finished photo (frame on the table) and measured every object.
2. The reference box's back wall is 681 × 418 px. That is a 1.63 : 1 ratio, but your box is 1.5 : 1, so the reference room is a little wider than yours. Two scales were used:
   - **Object sizes** use one uniform scale (0.44 mm/px from the width), so every piece of furniture keeps its true proportions.
   - **Vertical positions** (shelf heights, rows, arch top) are spread over the full 198 mm of usable height. Without that, about 16 mm of empty space would sit at the top.
3. The perspective difference between front and back objects in that photo is about 2 %, which is small enough to ignore. The close-up photos (table, cabinet, shelves) were used for shape and detail only, not size, because their wide-angle perspective distorts proportions.
4. **Check:** the proposed layout was overlaid on the reference photo. Shelves, frames, console, arch, plants, table and every shelving cell line up within about 1–3 mm (overlay image sent in chat; it isn't committed because it contains the customer's photo).
5. The result is close to **1:12 scale**: console 102 mm ≈ 1.2 m, mug Ø7.5 mm ≈ 9 cm, frame 24×27 mm ≈ 29×32 cm, bunny 24 mm ≈ 29 cm.

---

## 2. Stage 1: Component inventory (everything visible in the 13 photos)

### A. Structure / walls
| # | Item | What the photos show | Build approach |
|---|---|---|---|
| A1 | Left fluted wall panel | Peach/beige, about 20 rounded vertical flutes with a slight shimmer. Runs floor to ceiling, x ≈ 0–106 | Real modelled flutes (pitch 5.2 mm, bead height 1.4 mm) on a 1.6 mm backer. **2 pieces**, seam at z = 30 hidden behind the TV console |
| A2 | Right fluted wall panel | Same finish, behind the shelving unit, x ≈ 218–298 | Same design, 2 pieces, seam hidden behind the shelving |
| A3 | Centre back wall | Plain white | The box's own white back (no print needed) |
| A4 | Floor | Warm wood planks running left–right | **Proposal:** 3 printed 2 mm floor tiles (one per zone) with locating pockets, covered with wood-grain sticker/paper (see §5) |
| A5 | LED strip | Warm-white strip under the top front edge (photos 9, 11, 12) | Bought part. Optional printed channel (2 pcs) |
| A6 | White box, top-right corner | Small white block at x ≈ 265–298, z ≈ 190–200 | Probably the LED battery/switch box → **question Q7** |

### B. Left zone
| # | Item | Qty | Measured (W × H mm) | Notes |
|---|---|---|---|---|
| B1 | Floating shelves | 3 | 55 long × 12 deep × 3 thick | Tops at z 165 / 130 / 96, pitch about 34 mm, ivory |
| B2 | "LOVE" lettering | 1 | 21 × 18 × 5 | Stacked LO / VE block letters, white, on shelf 1 |
| B3 | Small portrait frames on shelves | 3 | 24 × 27 | Gold edge, white mat; grey-dress (S1), red-dress (S2), black-outfit (S3) photos |
| B4 | Large portrait frames on wall | 2 | 30 × 39 | Hung on the flutes, right-hand column |
| B5 | Leafy plant, rectangular white pot | 1 | pot 24 × 12, total height 27 | Shelf 2 |
| B6 | Succulent/aloe, textured round pot | 1 | pot Ø15 × 12, total height 26 | Shelf 3 |
| B7 | TV console | 1 | 102 × 16 D × 33 H | Black body with rounded ends; upper half has **3 open recessed bays**, lower half **3 white drawer fronts**; 4 splayed tapered white legs (9 mm) |
| B8 | Gramophone on box | 1 | 18 × 27 | Dark brown stepped box base + gold horn |
| B9 | Small landscape frame on console | 1 | 27 × 24 | |
| B10 | Book stack | 3 books | 24 × 16.5 (3 × 5.5) | White / black / white, spine titles as printed labels |

### C. Centre zone
| # | Item | Qty | Measured | Notes |
|---|---|---|---|---|
| C1 | Arch | 1 | 78 W × 176 H | Round top. 3 mm raised rounded white border. Backer for a **printed photo (customer + marble with gold veins)**, which is not 3D printed |
| C2 | Name plate ("Shruthi") | 1 | 20 × 8 × 1.5 | Near the top of the arch. **Different on every order**, so it will be a parametric text plate |
| C3 | Coffee table | 1 | 60 W × 27 D × 26 H | White top with rounded corners (3 mm thick), light-wood apron and 4 slightly tapered legs |
| C4 | Serving tray | 1 | 38 × 15 × 1.5 | Light wood, ripple/arch groove pattern |
| C5 | Coffee mugs | 2 | Ø7.5 × 8 + handle | White |
| C6 | Rainbow-arch vase | 1 | 15 × 14 × 6 | Beige, 3 engraved concentric arches, hole on top |
| C7 | Silver heart foliage | 1 | 11 × 12 | Two textured silver heart lobes on a stem, sits in C6 |
| C8 | Floor plant: fern in tall ribbed vase | 2 (identical) | vase Ø15 × 29, total 54 tall, spread 30 | Either side of the table, in front of the arch edges |

### D. Right zone: staggered open-cube shelving (most important part)
- Envelope: 75 W × 163 H × 20 D, boards 2.5 mm, **no back**, ivory.
- 5 rows, each 32.5 mm pitch (inside clear height 30 mm). Dividers and outer side boards **shift from row to row**, which creates the zig-zag outline in the photos.

| Row (top→bottom) | Outer edges (from unit's left datum) | Dividers | Cell contents (left → right) |
|---|---|---|---|
| 1 | 3 → 73 | 48 | landscape photo frame · **gold ornament** (gold sphere pot + gold eggs + green leaves) |
| 2 | 0 → 73 | 25 | **takeaway coffee cup** · landscape photo frame |
| 3 | 7 → 75 | 23, 48 | **donut vase + pampas** · **message plaque** "A SMILE IS ALWAYS THE BEST MAKE UP" · **small fern in swirl pot** |
| 4 | 3 → 69 | 27 | **bunny figurine** (white, pink inner ears) · landscape photo frame |
| 5 | 7 → 75 | 51 | landscape photo frame · **geometric gold elephant** |

### E. Totals
| Category | Count |
|---|---|
| Photo frames | **10** (left zone: 3 on shelves + 2 on wall + 1 on console; right unit: 4), plus 1 message plaque. **Your brief says 7, but the photos show 10 (see Q1)** |
| Plants | 4 designs (floor fern ×2, leafy rectangular, succulent, small fern), plus pampas and silver hearts |
| Decor | LOVE, gramophone, 3 books, bunny, gold ornament, gold elephant, takeaway cup, donut vase, arch vase, tray, 2 mugs, name plate |
| Furniture | TV console, coffee table, 3 floating shelves, staggered shelving unit, arch |

---

## 3. Stage 2: Front layout (see `drawings/front_layout.png`)

```
 x:0        106                 218            300
 z ┌──────────┬───────────────────┬─────────────┐ 200
   │ LEFT     │  CENTRE           │ RIGHT       │
   │ fluted   │  white wall       │ fluted      │
   │ panel    │   ╭─────────╮     │ panel       │ 178 arch top
   │ S1 z165  │   │  arch   │     │┌──────────┐ │ 164.5 unit top
   │ S2 z130  │   │ 78 wide │     ││ 5 rows × │ │
   │ S3 z96   │   │         │     ││ 32.5     │ │
   │ console  │ PA1 table  PA2    ││ staggered│ │
   │ top z35  │   │ 60×26   │     │└──────────┘ │
   └──────────┴───────────────────┴─────────────┘ 0
      106 mm        112 mm           82 mm
```

### 3.1 Zone allocation (X)
| Zone | X range | Width | Contents |
|---|---|---|---|
| L – Left | 0 – 106 | 106 | Fluted panel 104 wide (x 2–106), shelves, wall frames, console |
| C – Centre | 106 – 218 | 112 | Arch (centre line x = 162), table, 2 floor plants |
| R – Right | 218 – 300 | 82 | Fluted panel 78 wide (x 219–297), shelving unit (x 223–298) |

### 3.2 Key heights (Z, from inside floor; 2 mm floor tile included)
| Element | Z |
|---|---|
| Floor tile top | 2 |
| Console legs / body / top | 2–11 / 11–35 / top **35** |
| Items on console (gramophone, frame, books) | 35 → 62 max |
| Shelf 3 / 2 / 1 top surface | **96 / 130 / 165** |
| Wall frames F5 / F4 | 76–115 / 135–174 |
| Highest left item (frame F1) | 192 (6 mm below ceiling) |
| Coffee table top | **28** |
| Mug top / silver hearts top | 37.5 / 52 |
| Floor plant tips | 56 |
| Arch | 2 → **178** (22 mm clear to the ceiling for the LED zone) |
| Name plate | 152–160 |
| Shelving unit rows (board centres) | 2 / 34.5 / 67 / 99.5 / 132 / **164.5** |

### 3.3 Depth allocation (Y), see `drawings/side_section.png`
| Layer | Y range | Comment |
|---|---|---|
| Back wall | 0 | |
| Fluted panels / arch backer + border | 0 – 3 / 0 – 4.2 | Thin layer on the back wall |
| Wall frames | 3 – 6.5 | Glued to the flute tops |
| Floating shelves | 3 – 15 | 12 mm deep: frames lean, pots fit |
| TV console | 3 – 19 | 16 mm deep (shallowed for the shadow box; front view unaffected) |
| Shelving unit | 3 – 23 | 20 mm deep cells |
| Floor plants | 20 – 42 | Vases at y ≈ 31, in front of the arch edges |
| Coffee table | 13 – 40 | In front of the arch, overlapping the portrait like the reference |
| **Keep-out** | 42 – 50 | ≥ 8 mm to the glass for every part. Also clear of the LED strip |

The automatic check in `layout.py` passes: every part is inside the box, every part keeps at least 8 mm from the glass, and every single printed piece is 180 mm or less.

---

## 4. Printability / split plan (for approval, before CAD)

| Part | Largest piece | Split | Joint | Print orientation |
|---|---|---|---|---|
| Fluted panel, left | 104 × 168 (upper) + 104 × 28 (lower) | Horizontal seam at **z = 30**, **fully hidden behind the TV console** | Tongue and groove + 2 × Ø1.75 mm filament-offcut pins (holes Ø1.95) | Flat, flutes up, no supports |
| Fluted panel, right | 78 × 168 + 78 × 28 | Same seam height, hidden behind the shelving | Same joint (shared geometry) | Flat |
| Arch | 78 × 176 × 4.2 | **One piece** (fits the 180 bed with 2 mm to spare, no brim) | – | Flat, border up |
| Shelving unit | 75 × 163.75 × 20 | **One piece** | – | Lying on its back: all boards print as vertical walls, **zero supports, zero bridges** |
| TV console | 102 × 16 × 24 | Body (black) + drawer-front plate (white) + 4 legs (white, press-fit pegs) | 0.6 mm recess for the drawer plate; Ø1.5 peg holes for legs | Body on its back face |
| Floor tiles | 112 × 50 × 2 max | 3 tiles = 3 zone modules | Dovetail keys between tiles | Flat |
| Small parts | < 60 mm | Not split | – | Per part, chosen in Stage 4 |

**Modular production idea:** each zone (L / C / R) is built and glued on its own floor tile, with the fluted panel standing in a 1.2 mm slot at the tile's back edge. You assemble three modules on the bench and drop them into the box. Parts can be made in batches, any module can be replaced, and every unit comes out identical because the pockets fix where things go.

**Standard frame sizes:** I suggest making all 10 photo frames + the plaque from **2 STLs** instead of 7–11 different ones:
- `Photo_Frame_Small` 24 × 27 × 3.5 mm, used 9× (portrait or rotated to landscape), plus the plaque
- `Photo_Frame_Large` 30 × 39 × 3.5 mm, used 2× (wall)

The frames would be printed in Silk Gold with a 1.2 mm face border. The **white mat is printed as part of the photo** (I'll supply a print template with the exact sizes). That copies the look in the reference with a single filament colour. The photo goes in through a slot in the top edge, which makes fulfilling each order quick.

---

## 5. Questions before Stage 3 (please answer, especially ★)

1. ★ **Photo frame count.** The photos show **10 photo frames + 1 quote plaque**, and your brief says 7. Should I keep all 10? Are the 2 standard frame sizes acceptable?
2. ★ **Is 50 mm the depth up to the inside face of the glass?** How wide is the frame lip that covers the edges of the opening? This decides whether F1 at z = 192 and the wall panel tops are visible.
3. ★ **Floor:** OK to use 3 printed 2 mm floor tiles (zone modules) with a wood-grain sticker on top? The other option is no printed floor: parts are glued straight onto a sticker on the box floor, which gives 2 mm more height but less repeatable positioning.
4. ★ **Printer setup:** do you have the **AMS Lite** (multi-colour) and/or a **0.2 mm nozzle**? This decides whether the console, the plant pots and leaves, and the fine foliage are printed as one multi-colour piece or as separate single-colour parts.
5. ★ **Foliage:** fully 3D-printed leaves (stiff, about 0.8–1.0 mm thick fronds, slot-crossed for a 3D look), or printed pots with bought artificial miniature greenery and real dried pampas, as the reference appears to use? Bought greenery looks more realistic. Printed leaves are more repeatable and cheaper.
6. ★ **Takeaway cup:** the reference shows a **Starbucks logo**. Selling products with a third-party trademark is legally risky, so I'll model a plain cup with a sleeve band. You can add a Store Versile or generic sticker. Is that OK?
7. **Top-right white box** (x ≈ 265–298, z ≈ 190–200): is it the LED battery/switch box? Should I design a printed housing for it, and an LED channel?
8. **Centring:** in the reference, the table and plants sit about 6 mm right of the arch's centre line. I've centred them on the arch (x = 162) for a symmetric product. Is that OK?
9. **Colours/finish:** the fluted panels have a peach-beige shimmer. Do you have a filament in mind (for example Bambu PLA Matte "Desert Tan"/"Latte Brown" or a sparkle PLA), or will you paint or spray glitter?
10. **Name plate:** printed raised text (parametric font/name per order, one small print each), or a printed sticker or acrylic piece?

---

## 6. Next stages (after your approval)
- **Stage 3:** realistic 3D assembly preview (OpenSCAD → rendered images), checked against the photos again.
- **Stage 4:** parametric OpenSCAD source for every part, sculpted from primitives and hulls (no plain boxes for bunny, elephant, gramophone, plants and so on). All dimensions will be driven from `layout/layout.py` / `layout.json`.
- **Stage 5–6:** STL export, mesh validity checks (watertight/manifold, dimensions), A1 Mini build-volume and overhang checks. Final slicing in Bambu Studio has to be confirmed on your side; nothing is called production-ready before that.
- **Stage 7:** ZIP containing STLs, CAD source, 3MF assembly, drawings, print guide and photo/plaque print templates.
