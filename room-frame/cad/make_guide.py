#!/usr/bin/env python3
"""Writes docs/MANUFACTURING_GUIDE.md (+ .html for the PDF) from docs/print_table.json."""
import json
import os
from collections import defaultdict

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(ROOT, "docs", "print_table.json")))
CORE = {k: v for k, v in T.items() if k != "LED_Channel"}
ORIENT = {"flat": "As installed (bottom down)", "back": "On its back, front up", "flip": "Upside down"}


def hm(minutes):
    h, m = divmod(int(round(minutes)), 60)
    return f"{h} h {m:02d} min" if h else f"{m} min"


pieces = sum(v["qty"] for v in CORE.values())
grams = sum(v["slice"]["grams"] * v["qty"] for v in CORE.values())
mins = sum(v["slice"]["minutes"] * v["qty"] for v in CORE.values())

by_col = defaultdict(lambda: dict(parts=[], g=0.0, m=0.0, n=0))
for k, v in CORE.items():
    c = by_col[v["filament"]]
    c["parts"].append(f'{k} x{v["qty"]}')
    c["g"] += v["slice"]["grams"] * v["qty"]
    c["m"] += v["slice"]["minutes"] * v["qty"]
    c["n"] += v["qty"]

md = []
A = md.append
A("# Store Versile miniature room frame: manufacturing guide (Rev C)")
A("")
A("Box: 300 × 200 × 25 mm inside · Printer: Bambu Lab A1 Mini (single colour, 0.4 mm nozzle) · PLA · Scale about 1:12")
A("")
A("## 1. Status and what was checked")
A("")
A("| Check | Result |")
A("|---|---|")
A(f"| STL files | {len(T)} files ({len(CORE)} parts + optional LED channel), {pieces} printed pieces per frame |")
A("| Watertight, one closed body, no non-manifold edges (trimesh) | **All pass** |")
A("| Fits A1 Mini 180 × 180 × 180 in print orientation | **All pass** (largest: arch 78 × 176, wall panel 104 × 168, shelf unit 78 × 166) |")
A("| Parts overlapping in the assembly (`cad/check_interference.py`) | **None** |")
A("| Sliced with PrusaSlicer 2.7 (Bambu Studio is built on it) with an A1-Mini-like profile, **no supports** | **All slice** |")
A("| Overhangs steeper than 45° | Only small rounded edges (largest 35 mm² on the coffee-table chamfer). Flat ceilings are short bridges of 0.3–4 mm (frame photo slot, panel key notches, book covers) |")
A("| **Bambu Studio slicing and a physical test print** | **Still to do on your side.** Nothing here is called production-ready until the test prints in section 8 fit |")
A("")
A(f"**Per frame:** {pieces} pieces, about **{grams:.0f} g** of PLA, about **{hm(mins)}** of printing if every part is printed alone. "
  "Batching many parts on one plate per colour is faster. These estimates come from PrusaSlicer; Bambu Studio's numbers will be close but not identical (expect ±30 %).")
A("")
A("## 2. Bill of materials")
A("")
A("**Printed:** see the print list (section 3). **Bought per frame:**")
A("")
A("| Item | Qty | Note |")
A("|---|---|---|")
A("| Shadow-box frame, inside 300 × 200 × 25 mm, white back | 1 | Your existing frame |")
A("| Warm-white LED strip, 5 mm wide, about 300 mm, with battery box or USB | 1 | Under the top front edge (optional printed channel: `LED_Channel` × 2) |")
A("| PLA filament off-cuts, 1.75 mm | 6 × 6.4 mm | Shelf pins |")
A("| Gel CA glue (super glue) | — | Plastic to plastic |")
A("| Glue stick or photo-safe double-sided tape | — | Paper prints |")
A("| Photo paper, max 0.3 mm thick | 1 A4 | Arch print, 8 photo inserts, quote |")
A("| Sticker paper (or paper + glue) | 1 A4 | Wood floor, book spines |")
A("| Pink acrylic paint, fine brush | — | Bunny inner ears (optional) |")
A("")
A("## 3. Print list")
A("")
A("Settings that apply to every part: PLA, 0.4 mm nozzle, **supports OFF**, first layer 0.2 mm, nozzle 220 °C, bed 65 °C, gyroid infill (rectilinear at 100 %). "
  "Use Bambu Studio's *0.12mm Fine*, *0.16mm Optimal* or *0.20mm Standard* A1 Mini profile to match the layer column. Each STL already lies in its print orientation, so keep it as imported.")
A("")
A("| STL file | Qty | Colour | Size W×D×H mm (as printed) | Orientation | Layer | Infill | Walls | Brim | g each | Time each | Notes |")
A("|---|---|---|---|---|---|---|---|---|---|---|---|")
for k, v in T.items():
    sz = " × ".join(f"{x:g}" for x in v["size_mm"])
    col = v["filament"].split(" (")[0]
    A(f'| `{k}.stl` | {v["qty"]} | {col} | {sz} | {ORIENT[v["orientation"]]} | {v["layer"]} | {v["infill"]}% | {v["walls"]} | '
      f'{v["brim"] or "–"} | {v["slice"]["grams"]:.2f} | {v["slice"]["time"]} | {v["notes"]} |')
A("")
A("## 4. Plates by colour (batch printing)")
A("")
A("Group parts by colour and fill each 180 × 180 plate. Small figurines print much better several at a time (each layer gets time to cool). Totals per frame:")
A("")
A("| Colour | Pieces | Filament | Time (parts printed alone) | Parts |")
A("|---|---|---|---|---|")
for col, c in sorted(by_col.items(), key=lambda kv: -kv[1]["g"]):
    A(f'| {col} | {c["n"]} | {c["g"]:.1f} g | {hm(c["m"])} | {", ".join(c["parts"])} |')
A("")
A("### Two-colour parts on a single-colour printer")
A("")
A("In Bambu Studio's preview, drag the layer slider to the height below, right-click the **+** and add a **Pause** (or *Change filament*). When the printer stops, swap the filament and resume.")
A("")
A("| Part | Height | First colour | Second colour |")
A("|---|---|---|---|")
A("| `Coffee_Table` (printed upside down) | first layer **above 2.6 mm** | White (table top) | Light wood (apron and legs) |")
A("| `Name_Plate` (printed on its back) | first layer **above 1.0 mm** | White (plate) | Dark brown/black (raised name) |")
A("")
A("## 5. Per-order customisation")
A("")
A("1. **Name plate:** open `cad/parts/Name_Plate.scad` in OpenSCAD, change the `NAME = \"...\";` line, press F6, then File > Export > STL. Command line: `openscad -D 'NAME=\"Ananya\"' -o Name_Plate.stl cad/parts/Name_Plate.scad`. The text auto-fits to 17 mm wide.")
A("2. **Arch print:** make the artwork 72.6 × 173.3 mm (marble + gold veins + customer cut-out), using page 1 of `templates/Store_Versile_Print_Templates.pdf` as the guide.")
A("3. **Photos:** 3 small portrait (22.6 × 26.4), 3 small landscape (25.6 × 23.4), 2 large portrait (28.6 × 38.4), plus the quote insert. Keep the image inside the blue window with a 1.4 mm white mat. Template page 2.")
A("4. Print the PDF at **100 % / Actual size**. Measure the 50 mm test bar before cutting.")
A("")
A("## 6. Assembly (three modules, then the box)")
A("")
A("Positions are in mm. X is measured from the inside left wall, Y from the back wall forward, Z from the inside floor. Exact positions for every piece are on the *Assembly positions* sheets in `drawings/Store_Versile_Drawings.pdf`.")
A("")
A("**Prepare**")
A("1. Remove any brims and lightly sand the edges. Slide the photos into the frames from the top, with a dot of glue.")
A("2. Stick the wood sticker on the three floor tiles. Cut the sticker open over the wall-panel slots at the back of tiles L and R.")
A("3. Glue the arch print inside the arch's raised border. Glue the name plate on the print, centred, 150–158 mm above the arch bottom.")
A("")
A("**Module L (tile L, x 0–106)**")
A("1. Glue `Left_Wall_Panel_Lower` into the slot, flutes facing forward. Push `Left_Wall_Panel_Upper` onto its two key tabs and glue the seam.")
A("2. Push 6 filament pins (1.75 mm × 6.4 mm) through the panel holes from the back, so 4 mm stick out. Slide the 3 `Floating_Shelf` parts onto the pins and glue.")
A("3. Glue the large frames on the flutes: F4 at x 68, z 135; F5 at x 68, z 76 (bottom-left corners).")
A("4. TV console: glue the white drawer plate into the front recess. Glue the 4 legs into the sockets, splaying outward (turn the right-hand pair 180°). Glue the console to the tile at x 3, touching the panel.")
A("5. On the console: gramophone at x 10 (horn into its angled hole), small fern pot (`Plant_Pot_04` + `Plant_Leaves_04`) at x 44, 3 books at x 74.")
A("6. Shelves, top to bottom: LOVE + frame; frame + leafy plant (`Plant_Pot_02`); succulent (`Plant_Pot_03`) + frame.")
A("")
A("**Module C (tile C, x 106–218)**")
A("1. Glue the arch standing on the tile at the back, centred at x 162.")
A("2. Floor palms: push `Plant_Leaves_01A` into the front slot and `01B` into the rear slot of each `Plant_Pot_01`. Glue the pots at x 118 and x 206, 6 mm in front of the back wall.")
A("3. Coffee table centred at x 162, 5 mm in front of the back wall. On it: tray, two mugs (handles outward), arch vase at the right end with the silver hearts pushed into its hole.")
A("")
A("**Module R (tile R, x 218–300)**")
A("1. Right wall panels: same as module L.")
A("2. Glue `Right_Display_Shelf` on the tile against the panel, left board datum at x 223.")
A("3. Fill the cells, top to bottom: frame | gold ornament (+ green leaves glued behind the eggs); cup | frame; donut vase + pampas | quote plaque | small fern; bunny | frame; 2 books | gold elephant.")
A("")
A("**Into the box**")
A("1. Join the three tiles with their dovetails. Dry-fit them in the box: the arch and panels touch the back board.")
A("2. Glue the tiles to the box floor and the panels and arch to the back board (thin CA or double-sided tape).")
A("3. Fit the LED strip under the top front edge (optional printed channel). Clean the glass, then close the frame.")
A("")
A("## 7. Quality checklist (every order)")
A("")
for item in ["Name spelled correctly and centred on the arch", "8 photos, the right ones in the right frames, nothing crooked; the quote is in the plaque",
             "No glue strings or haze on the glass side", "All plants upright, leaves not touching the glass (≥ 3 mm gap)",
             "LED lights evenly; battery or cable is reachable", "Nothing rattles when the frame is gently tilted"]:
    A(f"- [ ] {item}")
A("")
A("## 8. First test prints (do these before production)")
A("")
A("| Test | Print | Pass when | If not, change in `versile_parts.scad` |")
A("|---|---|---|---|")
A("| Photo slot | `Photo_Frame_Small_P` + a cut photo-paper insert | Insert slides in fully, no gap at the window | slot (0.5) in `photo_frame()` |")
A("| Panel key + shelf pin | Both wall panels (L) + 1 shelf | Panels align flute-to-flute; shelf slides onto 2 pins | `CLR` (0.2), `PIN_HOLE` (1.95) |")
A("| Leaf fit | `Plant_Pot_04` + `Plant_Leaves_04` | Tab pushes in by hand and holds | `CLR` |")
A("| Console legs | `TV_Console_Body` + 4 legs | Pegs press in, console stands level | leg socket (1.7) |")
A("| Fine detail | `Plant_Leaves_01A`, `Pampas_Spray`, `Bunny` at 0.12 mm | Leaflets complete, no stringing | slow down, more cooling, or use a 0.2 mm nozzle |")
A("")
A("## 9. Files")
A("")
A("| Folder / file | Contents |")
A("|---|---|")
A("| `stl/` | One print-oriented STL per part |")
A("| `cad/versile_parts.scad` | Parametric OpenSCAD library (all dimensions) |")
A("| `cad/parts/*.scad` | One editable file per STL, already in print orientation |")
A("| `cad/assembly.scad`, `assembly/Store_Versile_Assembly.3mf` | Complete assembled room |")
A("| `drawings/Store_Versile_Drawings.pdf` | Layout, assembly positions, joint details and a dimensioned sheet for every part |")
A("| `templates/Store_Versile_Print_Templates.pdf` | 1:1 paper templates |")
A("| `preview/renders/` | Rendered views |")
A("| `layout/layout.py` | The approved layout (single source of truth) |")
A("")
A("STEP export isn't produced: the OpenSCAD (mesh) workflow cannot write true STEP solids. The 3MF and the parametric `.scad` source cover the assembly and editing needs.")

text = "\n".join(md) + "\n"
open(os.path.join(ROOT, "docs", "MANUFACTURING_GUIDE.md"), "w").write(text)
body = markdown.markdown(text, extensions=["tables"])
html = f"""<!doctype html><html><head><meta charset="utf-8"><title>Store Versile manufacturing guide</title><style>
body {{ font-family: "DejaVu Sans", Arial, sans-serif; font-size: 9.5pt; color: #222; line-height: 1.4 }}
h1 {{ font-size: 17pt }} h2 {{ font-size: 13pt; margin-top: 18pt; border-bottom: 1px solid #ccc }} h3 {{ font-size: 11pt }}
table {{ border-collapse: collapse; width: 100%; margin: 6pt 0; font-size: 7.6pt }}
th, td {{ border: 1px solid #bbb; padding: 2pt 4pt; vertical-align: top; text-align: left }}
th {{ background: #efe7dc }} tr:nth-child(even) td {{ background: #faf7f3 }}
code {{ font-size: 7.4pt }}
</style></head><body>{body}</body></html>"""
open(os.path.join(ROOT, "docs", "MANUFACTURING_GUIDE.html"), "w").write(html)
print(f"guide written: {pieces} pieces, {grams:.0f} g, {hm(mins)}")
