# Store Versile – Miniature Room Frame (CAD project)

Custom 3D-printed miniature room for a 300 × 200 × 50 mm shadow-box frame.
Printer: Bambu Lab A1 Mini · PLA · Bambu Studio.

| Folder | Contents |
|---|---|
| `docs/` | Stage reports. Start with `STAGE_1_2_Reference_Analysis_and_Layout.md` |
| `layout/` | `layout.py` holds every component envelope (single source of truth). It writes `layout.json`, the drawings and `docs/component_envelopes.md` |
| `drawings/` | Front elevation, side section, plan view (SVG + PNG) |
| `cad/` | `versile_parts.scad`: parametric OpenSCAD library of every part. `build.py`: places the parts from the layout, writes `assembly.scad` and exports meshes. `check_interference.py`: collision and box check |
| `stl/` | **Print-ready STL per part** (45 files, already lying in print orientation) |
| `cad/parts/` | One editable `.scad` per STL (print orientation, settings in the header) |
| `assembly/` | `Store_Versile_Assembly.3mf` (whole room, 63 coloured pieces) + `assembly.scad` |
| `templates/` | 1:1 paper templates PDF (arch print, photo inserts, quote, wood floor, book spines) |
| `release/` | ZIP of the whole package |
| `preview/` | three.js renderer (`render.js`, `viewer.html`) and `renders/*.png` |

Regenerate:
```
python3 layout/layout.py              # layout + drawings
python3 cad/build.py installed        # assembly.scad + meshes (needs openscad)
python3 cad/check_interference.py     # needs trimesh, manifold3d, networkx
python3 cad/make_print_files.py       # stl/ + cad/parts/ + slicing check (needs prusa-slicer)
python3 cad/make_drawings.py && python3 cad/make_templates.py && python3 cad/make_guide.py
python3 cad/make_assembly_3mf.py && (cd cad && node make_docs.js)   # PDFs
(cd preview && npm install && node render.js)   # renders (needs playwright + chromium)
```

Status: **Rev C manufacturing package complete (Stages 4-7).** Start with `docs/MANUFACTURING_GUIDE.md` (also as PDF). Download everything as `release/Store_Versile_Room_Frame_RevC.zip`. Still to do on your side: open the STLs in Bambu Studio and run the test prints in guide section 8.
