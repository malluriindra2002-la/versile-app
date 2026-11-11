# Store Versile miniature room frame: manufacturing guide (Rev C)

Box: 300 × 200 × 25 mm inside · Printer: Bambu Lab A1 Mini (single colour, 0.4 mm nozzle) · PLA · Scale about 1:12

## 1. Status and what was checked

| Check | Result |
|---|---|
| STL files | 45 files (44 parts + optional LED channel), 63 printed pieces per frame |
| Watertight, one closed body, no non-manifold edges (trimesh) | **All pass** |
| Fits A1 Mini 180 × 180 × 180 in print orientation | **All pass** (largest: arch 78 × 176, wall panel 104 × 168, shelf unit 78 × 166) |
| Parts overlapping in the assembly (`cad/check_interference.py`) | **None** |
| Sliced with PrusaSlicer 2.7 (Bambu Studio is built on it) with an A1-Mini-like profile, **no supports** | **All slice** |
| Overhangs steeper than 45° | Only small rounded edges (largest 35 mm² on the coffee-table chamfer). Flat ceilings are short bridges of 0.3–4 mm (frame photo slot, panel key notches, book covers) |
| **Bambu Studio slicing and a physical test print** | **Still to do on your side.** Nothing here is called production-ready until the test prints in section 8 fit |

**Per frame:** 63 pieces, about **212 g** of PLA, about **8 h 25 min** of printing if every part is printed alone. Batching many parts on one plate per colour is faster. These estimates come from PrusaSlicer; Bambu Studio's numbers will be close but not identical (expect ±30 %).

## 2. Bill of materials

**Printed:** see the print list (section 3). **Bought per frame:**

| Item | Qty | Note |
|---|---|---|
| Shadow-box frame, inside 300 × 200 × 25 mm, white back | 1 | Your existing frame |
| Warm-white LED strip, 5 mm wide, about 300 mm, with battery box or USB | 1 | Under the top front edge (optional printed channel: `LED_Channel` × 2) |
| PLA filament off-cuts, 1.75 mm | 6 × 6.4 mm | Shelf pins |
| Gel CA glue (super glue) | — | Plastic to plastic |
| Glue stick or photo-safe double-sided tape | — | Paper prints |
| Photo paper, max 0.3 mm thick | 1 A4 | Arch print, 8 photo inserts, quote |
| Sticker paper (or paper + glue) | 1 A4 | Wood floor, book spines |
| Pink acrylic paint, fine brush | — | Bunny inner ears (optional) |

## 3. Print list

Settings that apply to every part: PLA, 0.4 mm nozzle, **supports OFF**, first layer 0.2 mm, nozzle 220 °C, bed 65 °C, gyroid infill (rectilinear at 100 %). Use Bambu Studio's *0.12mm Fine*, *0.16mm Optimal* or *0.20mm Standard* A1 Mini profile to match the layer column. Each STL already lies in its print orientation, so keep it as imported.

| STL file | Qty | Colour | Size W×D×H mm (as printed) | Orientation | Layer | Infill | Walls | Brim | g each | Time each | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `Floor_Tile_L.stl` | 1 | Any colour | 110 × 25 × 2 | As installed (bottom down) | 0.2 | 15% | 2 | – | 6.11 | 8m 55s | Wood sticker on top after printing. |
| `Floor_Tile_C.stl` | 1 | Any colour | 112 × 25 × 2 | As installed (bottom down) | 0.2 | 15% | 2 | – | 6.65 | 9m 40s | Wood sticker on top after printing. |
| `Floor_Tile_R.stl` | 1 | Any colour | 86 × 25 × 2 | As installed (bottom down) | 0.2 | 15% | 2 | – | 4.75 | 7m 5s | Wood sticker on top after printing. |
| `Left_Wall_Panel_Lower.stl` | 1 | Peach-beige | 104 × 31.99 × 2.4 | On its back, front up | 0.16 | 15% | 2 | – | 6.82 | 13m 19s | Flutes up. Seam is hidden behind the TV console. |
| `Left_Wall_Panel_Upper.stl` | 1 | Peach-beige | 104 × 168 × 2.4 | On its back, front up | 0.16 | 15% | 2 | – | 38.93 | 1h 0m 33s | Flutes up. 6 shelf-pin holes. |
| `Right_Wall_Panel_Lower.stl` | 1 | Peach-beige | 78 × 31.99 × 2.4 | On its back, front up | 0.16 | 15% | 2 | – | 5.12 | 10m 8s | Flutes up. Seam is hidden behind the shelving. |
| `Right_Wall_Panel_Upper.stl` | 1 | Peach-beige | 78 × 168 × 2.4 | On its back, front up | 0.16 | 15% | 2 | – | 29.20 | 43m 9s | Flutes up. |
| `Floating_Shelf.stl` | 3 | Ivory white | 55 × 8 × 3 | As installed (bottom down) | 0.16 | 100% | 3 | – | 1.60 | 3m 22s | Print 3. Two pin holes in the back edge. |
| `LOVE_Letters.stl` | 1 | White | 22.47 × 17.83 × 4 | On its back, front up | 0.12 | 100% | 2 | – | 1.21 | 5m 39s | Letters face up. |
| `Photo_Frame_Small_P.stl` | 4 | Gold silk | 24 × 27 × 2.5 | On its back, front up | 0.12 | 100% | 2 | – | 0.99 | 2m 45s | Gold face up (ironing on). Photo slot opens at the top. |
| `Photo_Frame_Small_L.stl` | 3 | Gold silk | 27 × 24 × 2.5 | On its back, front up | 0.12 | 100% | 2 | – | 0.99 | 2m 45s | Gold face up (ironing on). Photo slot opens at the top. |
| `Photo_Frame_Large_P.stl` | 2 | Gold silk | 30 × 39 × 2.5 | On its back, front up | 0.12 | 100% | 2 | – | 1.73 | 4m 1s | Gold face up (ironing on). Photo slot opens at the top. |
| `TV_Console_Body.stl` | 1 | Black | 102 × 24 × 10 | On its back, front up | 0.16 | 15% | 3 | – | 12.27 | 25m 14s | Lying on its back: bays and drawer recess face up. |
| `TV_Console_Drawer_Fronts.stl` | 1 | White | 96.7 × 9.2 × 0.8 | On its back, front up | 0.12 | 100% | 2 | – | 0.89 | 2m 37s | 0.8 mm plate, grooves up. Glue into the body recess. |
| `TV_Console_Leg.stl` | 4 | White | 3.76 × 2.2 × 11.6 | As installed (bottom down) | 0.12 | 100% | 2 | 3 | 0.05 | 51s | Print 4 together with a 3 mm brim, slow small-layer cooling on. |
| `Gramophone_Base.stl` | 1 | Dark brown | 14.98 × 8.1 × 13.48 | As installed (bottom down) | 0.12 | 20% | 2 | – | 1.19 | 8m 58s | Angled hole for the horn on top. |
| `Gramophone_Horn.stl` | 1 | Gold silk | 11 × 7.92 × 14 | Upside down | 0.12 | 100% | 2 | – | 0.09 | 2m 6s | Bell mouth down on the bed, peg up. |
| `Book_01.stl` | 2 | White | 24 × 8 × 5.5 | As installed (bottom down) | 0.12 | 20% | 2 | – | 0.74 | 3m 47s | Spine label = printed paper. |
| `Book_02.stl` | 2 | Black | 22.5 × 7.5 × 5.5 | As installed (bottom down) | 0.12 | 20% | 2 | – | 0.66 | 3m 40s | Spine label = printed paper. |
| `Book_03.stl` | 1 | White | 23.5 × 8 × 5.5 | As installed (bottom down) | 0.12 | 20% | 2 | – | 0.72 | 3m 46s | Spine label = printed paper. |
| `Plant_Pot_01.stl` | 2 | White | 14.9 × 9.93 × 29 | As installed (bottom down) | 0.12 | 15% | 3 | – | 3.46 | 22m 21s | Print 2. Two parallel leaf slots. |
| `Plant_Leaves_01A.stl` | 2 | Leaf green | 33.44 × 29.32 × 1 | On its back, front up | 0.12 | 100% | 2 | – | 0.42 | 5m 43s | Print 2. Flat, 1.0 mm. Front palm fan. |
| `Plant_Leaves_01B.stl` | 2 | Leaf green | 33.54 × 30.26 × 1 | On its back, front up | 0.12 | 100% | 2 | – | 0.34 | 4m 42s | Print 2. Flat, 1.0 mm. Rear palm fan. |
| `Plant_Pot_02.stl` | 1 | White | 24 × 7 × 12 | As installed (bottom down) | 0.12 | 15% | 3 | – | 1.92 | 9m 3s |  |
| `Plant_Leaves_02.stl` | 1 | Leaf green | 28.44 × 20.97 × 1 | On its back, front up | 0.12 | 100% | 2 | – | 0.31 | 1m 19s | Flat, 1.0 mm. |
| `Plant_Pot_03.stl` | 1 | White | 15 × 7 × 12 | As installed (bottom down) | 0.12 | 15% | 3 | – | 1.09 | 8m 59s | Diamond-knurl texture. |
| `Plant_Leaves_03.stl` | 1 | Light green | 17.89 × 18.85 × 1.2 | On its back, front up | 0.12 | 100% | 2 | – | 0.17 | 1m 2s | Flat, 1.2 mm. |
| `Plant_Pot_04.stl` | 2 | White | 14 × 7 × 10 | As installed (bottom down) | 0.12 | 15% | 3 | – | 0.86 | 7m 7s | Print 2 (shelf unit + TV console). |
| `Plant_Leaves_04.stl` | 2 | Leaf green | 13.06 × 13 × 1 | On its back, front up | 0.12 | 100% | 2 | – | 0.10 | 58s | Print 2. Flat, 1.0 mm. |
| `Central_Arch.stl` | 1 | White | 78 × 176 × 3 | On its back, front up | 0.16 | 15% | 2 | – | 17.93 | 26m 48s | Border up. 176 mm long: place diagonally if your plate edge is tight; no brim needed. |
| `Name_Plate.stl` | 1 | White | 20 × 8 × 1.6 | On its back, front up | 0.12 | 100% | 2 | – | 0.22 | 1m 12s | FILAMENT CHANGE at 1.0 mm: white base, then dark text. Edit the NAME line in this file per order. |
| `Coffee_Table.stl` | 1 | White | 60 × 14 × 26 | Upside down | 0.12 | 20% | 2 | – | 2.73 | 19m 16s | Upside down. FILAMENT CHANGE at 2.6 mm: white top first, then wood legs. |
| `Serving_Tray.stl` | 1 | Light wood | 38 × 10 × 1.5 | As installed (bottom down) | 0.12 | 100% | 2 | – | 0.69 | 2m 19s | Ripple grooves up. |
| `Mug.stl` | 2 | White | 9.8 × 7.5 × 8 | As installed (bottom down) | 0.12 | 100% | 2 | – | 0.20 | 2m 56s | Print 2 (one is turned so the handles face outward). |
| `Arch_Vase.stl` | 1 | Beige | 15 × 14 × 5 | On its back, front up | 0.12 | 20% | 2 | – | 0.71 | 3m 36s | Arch grooves up. |
| `Silver_Heart_Plant.stl` | 1 | Silver silk | 12.68 × 11.73 × 2.11 | On its back, front up | 0.12 | 100% | 2 | – | 0.17 | 1m 27s | Bumps up. Push the stem into the arch vase. |
| `Right_Display_Shelf.stl` | 1 | Cream | 78.2 × 165.7 × 12 | On its back, front up | 0.2 | 15% | 3 | – | 39.93 | 55m 26s | Lying on its back: every board is a vertical wall, no supports, no bridges. |
| `Gold_Ornament.stl` | 1 | Gold silk | 9.97 × 13.68 × 4.98 | On its back, front up | 0.12 | 20% | 2 | – | 0.41 | 3m 11s | Flat back down. |
| `Gold_Ornament_Leaves.stl` | 1 | Leaf green | 14.01 × 11.2 × 1 | On its back, front up | 0.12 | 100% | 2 | – | 0.07 | 39s | Glue the tab to the back of the gold pot. |
| `Takeaway_Cup.stl` | 1 | White | 9.3 × 9.3 × 22 | As installed (bottom down) | 0.12 | 20% | 2 | – | 1.43 | 13m 30s | Plain cup, no logo. Optional own-brand sticker on the sleeve. |
| `Donut_Vase.stl` | 1 | White | 12 × 13.6 × 3 | On its back, front up | 0.12 | 20% | 2 | – | 0.34 | 2m 17s | Flat back down. |
| `Pampas_Spray.stl` | 1 | Bone / ivory white | 11.03 × 13.74 × 1 | On its back, front up | 0.12 | 100% | 2 | – | 0.07 | 54s | Flat, 1.0 mm. Peg goes into the donut vase neck. |
| `Bunny.stl` | 1 | White | 13.15 × 24.68 × 6.18 | On its back, front up | 0.12 | 20% | 2 | – | 0.71 | 4m 39s | Flat back down. Paint inner ears pink. |
| `Gold_Elephant.stl` | 1 | Gold silk | 16.65 × 14.82 × 5.2 | On its back, front up | 0.12 | 20% | 2 | – | 0.70 | 4m 42s | Flat back down. |
| `LED_Channel.stl` | 2 | White | 148 × 5 × 6 | Upside down | 0.2 | 15% | 2 | – | 1.82 | 3m 40s | Optional, print 2. Hides the LED strip under the top front edge. |

## 4. Plates by colour (batch printing)

Group parts by colour and fill each 180 × 180 plate. Small figurines print much better several at a time (each layer gets time to cool). Totals per frame:

| Colour | Pieces | Filament | Time (parts printed alone) | Parts |
|---|---|---|---|---|
| Peach-beige (e.g. Bambu PLA Matte Desert Tan / Latte Brown, or PLA Sparkle for shimmer) | 4 | 80.1 g | 2 h 07 min | Left_Wall_Panel_Lower x1, Left_Wall_Panel_Upper x1, Right_Wall_Panel_Lower x1, Right_Wall_Panel_Upper x1 |
| Cream (e.g. PLA Matte Ivory White; or the panel colour) | 1 | 39.9 g | 55 min | Right_Display_Shelf x1 |
| White (e.g. PLA Basic Jade White / Matte Ivory White) | 23 | 39.9 g | 2 h 54 min | LOVE_Letters x1, TV_Console_Drawer_Fronts x1, TV_Console_Leg x4, Book_01 x2, Book_03 x1, Plant_Pot_01 x2, Plant_Pot_02 x1, Plant_Pot_03 x1, Plant_Pot_04 x2, Central_Arch x1, Name_Plate x1, Coffee_Table x1, Mug x2, Takeaway_Cup x1, Donut_Vase x1, Bunny x1 |
| Any colour (covered by the wood-grain sticker) | 3 | 17.5 g | 26 min | Floor_Tile_L x1, Floor_Tile_C x1, Floor_Tile_R x1 |
| Black (PLA Basic / Matte Charcoal) | 3 | 13.6 g | 33 min | TV_Console_Body x1, Book_02 x2 |
| Gold silk (e.g. PLA Silk+ Gold) | 12 | 11.6 g | 38 min | Photo_Frame_Small_P x4, Photo_Frame_Small_L x3, Photo_Frame_Large_P x2, Gramophone_Horn x1, Gold_Ornament x1, Gold_Elephant x1 |
| Ivory white (e.g. PLA Matte Ivory White) | 3 | 4.8 g | 10 min | Floating_Shelf x3 |
| Leaf green (e.g. PLA Matte Grass Green) | 8 | 2.1 g | 25 min | Plant_Leaves_01A x2, Plant_Leaves_01B x2, Plant_Leaves_02 x1, Plant_Leaves_04 x2, Gold_Ornament_Leaves x1 |
| Dark brown (e.g. PLA Matte Dark Brown) | 1 | 1.2 g | 9 min | Gramophone_Base x1 |
| Beige (e.g. PLA Matte Desert Tan) | 1 | 0.7 g | 4 min | Arch_Vase x1 |
| Light wood (e.g. PLA Matte Latte Brown or PLA-Wood) | 1 | 0.7 g | 2 min | Serving_Tray x1 |
| Light green (e.g. PLA Matte Apple Green) | 1 | 0.2 g | 1 min | Plant_Leaves_03 x1 |
| Silver silk (e.g. PLA Silk+ Silver) | 1 | 0.2 g | 1 min | Silver_Heart_Plant x1 |
| Bone / ivory white | 1 | 0.1 g | 1 min | Pampas_Spray x1 |

### Two-colour parts on a single-colour printer

In Bambu Studio's preview, drag the layer slider to the height below, right-click the **+** and add a **Pause** (or *Change filament*). When the printer stops, swap the filament and resume.

| Part | Height | First colour | Second colour |
|---|---|---|---|
| `Coffee_Table` (printed upside down) | first layer **above 2.6 mm** | White (table top) | Light wood (apron and legs) |
| `Name_Plate` (printed on its back) | first layer **above 1.0 mm** | White (plate) | Dark brown/black (raised name) |

## 5. Per-order customisation

1. **Name plate:** open `cad/parts/Name_Plate.scad` in OpenSCAD, change the `NAME = "...";` line, press F6, then File > Export > STL. Command line: `openscad -D 'NAME="Ananya"' -o Name_Plate.stl cad/parts/Name_Plate.scad`. The text auto-fits to 17 mm wide.
2. **Arch print:** make the artwork 72.6 × 173.3 mm (marble + gold veins + customer cut-out), using page 1 of `templates/Store_Versile_Print_Templates.pdf` as the guide.
3. **Photos:** 3 small portrait (22.6 × 26.4), 3 small landscape (25.6 × 23.4), 2 large portrait (28.6 × 38.4), plus the quote insert. Keep the image inside the blue window with a 1.4 mm white mat. Template page 2.
4. Print the PDF at **100 % / Actual size**. Measure the 50 mm test bar before cutting.

## 6. Assembly (three modules, then the box)

Positions are in mm. X is measured from the inside left wall, Y from the back wall forward, Z from the inside floor. Exact positions for every piece are on the *Assembly positions* sheets in `drawings/Store_Versile_Drawings.pdf`.

**Prepare**
1. Remove any brims and lightly sand the edges. Slide the photos into the frames from the top, with a dot of glue.
2. Stick the wood sticker on the three floor tiles. Cut the sticker open over the wall-panel slots at the back of tiles L and R.
3. Glue the arch print inside the arch's raised border. Glue the name plate on the print, centred, 150–158 mm above the arch bottom.

**Module L (tile L, x 0–106)**
1. Glue `Left_Wall_Panel_Lower` into the slot, flutes facing forward. Push `Left_Wall_Panel_Upper` onto its two key tabs and glue the seam.
2. Push 6 filament pins (1.75 mm × 6.4 mm) through the panel holes from the back, so 4 mm stick out. Slide the 3 `Floating_Shelf` parts onto the pins and glue.
3. Glue the large frames on the flutes: F4 at x 68, z 135; F5 at x 68, z 76 (bottom-left corners).
4. TV console: glue the white drawer plate into the front recess. Glue the 4 legs into the sockets, splaying outward (turn the right-hand pair 180°). Glue the console to the tile at x 3, touching the panel.
5. On the console: gramophone at x 10 (horn into its angled hole), small fern pot (`Plant_Pot_04` + `Plant_Leaves_04`) at x 44, 3 books at x 74.
6. Shelves, top to bottom: LOVE + frame; frame + leafy plant (`Plant_Pot_02`); succulent (`Plant_Pot_03`) + frame.

**Module C (tile C, x 106–218)**
1. Glue the arch standing on the tile at the back, centred at x 162.
2. Floor palms: push `Plant_Leaves_01A` into the front slot and `01B` into the rear slot of each `Plant_Pot_01`. Glue the pots at x 118 and x 206, 6 mm in front of the back wall.
3. Coffee table centred at x 162, 5 mm in front of the back wall. On it: tray, two mugs (handles outward), arch vase at the right end with the silver hearts pushed into its hole.

**Module R (tile R, x 218–300)**
1. Right wall panels: same as module L.
2. Glue `Right_Display_Shelf` on the tile against the panel, left board datum at x 223.
3. Fill the cells, top to bottom: frame | gold ornament (+ green leaves glued behind the eggs); cup | frame; donut vase + pampas | quote plaque | small fern; bunny | frame; 2 books | gold elephant.

**Into the box**
1. Join the three tiles with their dovetails. Dry-fit them in the box: the arch and panels touch the back board.
2. Glue the tiles to the box floor and the panels and arch to the back board (thin CA or double-sided tape).
3. Fit the LED strip under the top front edge (optional printed channel). Clean the glass, then close the frame.

## 7. Quality checklist (every order)

- [ ] Name spelled correctly and centred on the arch
- [ ] 8 photos, the right ones in the right frames, nothing crooked; the quote is in the plaque
- [ ] No glue strings or haze on the glass side
- [ ] All plants upright, leaves not touching the glass (≥ 3 mm gap)
- [ ] LED lights evenly; battery or cable is reachable
- [ ] Nothing rattles when the frame is gently tilted

## 8. First test prints (do these before production)

| Test | Print | Pass when | If not, change in `versile_parts.scad` |
|---|---|---|---|
| Photo slot | `Photo_Frame_Small_P` + a cut photo-paper insert | Insert slides in fully, no gap at the window | slot (0.5) in `photo_frame()` |
| Panel key + shelf pin | Both wall panels (L) + 1 shelf | Panels align flute-to-flute; shelf slides onto 2 pins | `CLR` (0.2), `PIN_HOLE` (1.95) |
| Leaf fit | `Plant_Pot_04` + `Plant_Leaves_04` | Tab pushes in by hand and holds | `CLR` |
| Console legs | `TV_Console_Body` + 4 legs | Pegs press in, console stands level | leg socket (1.7) |
| Fine detail | `Plant_Leaves_01A`, `Pampas_Spray`, `Bunny` at 0.12 mm | Leaflets complete, no stringing | slow down, more cooling, or use a 0.2 mm nozzle |

## 9. Files

| Folder / file | Contents |
|---|---|
| `stl/` | One print-oriented STL per part |
| `cad/versile_parts.scad` | Parametric OpenSCAD library (all dimensions) |
| `cad/parts/*.scad` | One editable file per STL, already in print orientation |
| `cad/assembly.scad`, `assembly/Store_Versile_Assembly.3mf` | Complete assembled room |
| `drawings/Store_Versile_Drawings.pdf` | Layout, assembly positions, joint details and a dimensioned sheet for every part |
| `templates/Store_Versile_Print_Templates.pdf` | 1:1 paper templates |
| `preview/renders/` | Rendered views |
| `layout/layout.py` | The approved layout (single source of truth) |

STEP export isn't produced: the OpenSCAD (mesh) workflow cannot write true STEP solids. The 3MF and the parametric `.scad` source cover the assembly and editing needs.
