# Store Versile – Miniature Room Frame (CAD project)

Custom 3D-printed miniature room for a 300 × 200 × 50 mm shadow-box frame.
Printer: Bambu Lab A1 Mini · PLA · Bambu Studio.

| Folder | Contents |
|---|---|
| `docs/` | Stage reports. Start with `STAGE_1_2_Reference_Analysis_and_Layout.md` |
| `layout/` | `layout.py` holds every component envelope (single source of truth). It writes `layout.json`, the drawings and `docs/component_envelopes.md` |
| `drawings/` | Front elevation, side section, plan view (SVG + PNG) |

Regenerate: `python3 layout/layout.py`

Status: **Stage 1–2 done, waiting for layout approval.** No STLs until it is approved.
