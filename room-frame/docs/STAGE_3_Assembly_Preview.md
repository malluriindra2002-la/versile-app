# Store Versile – Miniature Room Frame
## Stage 3: 3D assembly preview (Rev B: 300 × 200 × 25 mm, 8 photo frames)

**Status: waiting for your approval of the look. Print-ready STLs (Stage 5) have not been exported yet.**

### What the preview is
The renders in `preview/renders/` are **not** an artist's impression. They show the **real CAD geometry**:
- All 44 unique parts are modelled in OpenSCAD (`cad/versile_parts.scad`). They are placed by `cad/build.py` from the approved layout numbers (`layout/layout.json`), 63 placed pieces in total.
- Each part was exported as a mesh and rendered with materials and LED-style lighting (`preview/viewer.html`, `preview/render.js`).
- Photos, the arch portrait, the quote print and the book labels are **placeholders**. Your customer's real photos are printed on paper and are not part of the 3D model.

| View | File |
|---|---|
| Straight front (like your product photo) | `renders/front.png` |
| 3/4 angle (shows the 25 mm depth) | `renders/angle.png` |
| Left wall close-up | `renders/left.png` |
| Centre close-up | `renders/centre.png` |
| Right shelving close-up | `renders/right.png` |
| Coffee-table close-up | `renders/table.png` |

### Checks already run on the CAD (automated, repeatable)
| Check | Result |
|---|---|
| Every part a single closed, watertight (manifold) body | **44 / 44 pass** (`trimesh`) |
| Every part inside the 300 × 200 × 25 box | **pass** |
| Parts in the assembly overlapping each other (`cad/check_interference.py`) | **pass**, after the fixes below |
| Largest single print (arch 78 × 176 mm; wall panel 104 × 168 mm) | Fits the 180 × 180 A1 Mini bed |

### Problems the checks found and fixed during this stage
1. **Mirror-image parts (important).** The layout used X right, Y toward the glass, Z up. That is a left-handed set of axes, so seen from the front every part would have printed as a mirror image (the name plate and LOVE would read backwards). All exported parts are now mirrored front-to-back, and the CAD uses OpenSCAD's normal front (−Y). The text now reads correctly.
2. **Quote plaque didn't fit its cell** (cell 22.5 mm, frame 24 mm). Row 3 of the shelving unit was re-divided: donut vase 14 mm | plaque 26 mm | plant 20.5 mm. Updated in the layout, the drawings and the CAD.
3. **Crossed fern fans collided** and poked through the back wall. They're now two **parallel** fans (front and rear) in two slots in the vase. That's easier to assemble and gives the same 3D fullness.
4. Leaf tips dipped into the pot rims, so leaves are now clipped at the rim. The heart-foliage stem was square in a round hole and is now round. The gold-ornament leaves passed through the eggs, so they now stand behind the eggs, glued to the flat back of the pot. The pampas peg was 0.4 mm too long. The arch-outline helper poked 1 mm below arches that are wider than they are tall; that's fixed.

### How the parts are made (single-colour A1 Mini)
| Look in the render | How it's printed |
|---|---|
| Black TV console with white drawers and white legs | 3 parts: black body, white drawer plate (0.8 mm, sits flush in a recess), 4 white legs with square pegs |
| Coffee table: white top, wood legs | **One print**, upside down, with a filament change from white to wood at 2.6 mm (Bambu Studio "change filament at layer") |
| Name plate: white with dark text | One print with a filament change at 1.0 mm |
| Plants | White pot + green leaf fan(s) pushed into a slot |
| Gramophone | Brown base + gold horn on an angled peg |
| Bunny, elephant, gold ornament, donut vase | Flat-backed reliefs, printed lying on their back, **no supports** |
| Photo frames (3 sizes) | Silk-gold PLA; the photo slides in from the top; the white mat is printed on the photo |

### Your decision needed
1. **Overall look.** Does this match what you want to sell? (Compare with your photo: the comparison image is in chat.)
2. **Shelving unit:** the reference has **thicker, cream boards** (about 3–3.5 mm) and looks chunkier. Mine are 2.5 mm. Should I make them 3.2 mm and match the cream/peach colour of the wall panels?
3. **Floor plants:** the reference uses sparser, longer, palm-like leaves. Mine are a fuller fern. Keep the fern, or change to a palm style?
4. Anything to add, remove or move?

### Next (after approval)
- **Stage 4–5:** print-oriented STL for every part (one file each, laid flat for printing), each part's file in OpenSCAD, mesh checks.
- **Stage 6:** build-volume, overhang and thin-wall check per part. You confirm in Bambu Studio.
- **Stage 7:** ZIP package with STLs, CAD, assembly, drawings, manufacturing guide, and paper templates for the photos, arch print and quote.
