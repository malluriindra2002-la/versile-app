# Store Versile – Miniature Room Frame (CAD project)

Custom 3D-printed miniature room for a 300 × 200 × 50 mm shadow-box frame.
Printer: Bambu Lab A1 Mini · PLA · Bambu Studio.

| Folder | Contents |
|---|---|
| `docs/` | Stage reports. Start with `STAGE_1_2_Reference_Analysis_and_Layout.md` |
| `layout/` | `layout.py` holds every component envelope (single source of truth). It writes `layout.json`, the drawings and `docs/component_envelopes.md` |
| `drawings/` | Front elevation, side section, plan view (SVG + PNG) |
| `cad/` | `versile_parts.scad`: parametric OpenSCAD library of every part. `build.py`: places the parts from the layout, writes `assembly.scad` and exports meshes. `check_interference.py`: collision and box check |
| `preview/` | three.js renderer (`render.js`, `viewer.html`) and `renders/*.png` |

Regenerate:
```
python3 layout/layout.py              # layout + drawings
python3 cad/build.py installed        # assembly.scad + meshes (needs openscad)
python3 cad/check_interference.py     # needs trimesh, manifold3d, networkx
(cd preview && npm install && node render.js)   # renders (needs playwright + chromium)
```

Status: **Stage 3 done (3D assembly preview). Waiting for your approval of the look.** See `docs/STAGE_3_Assembly_Preview.md`.
