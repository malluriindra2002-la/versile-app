#!/usr/bin/env python3
"""
Stage 7 drawings: one dimensioned A4 sheet per part (third-angle projection: front,
top, right-side views taken from the real CAD meshes), an assembly positioning sheet
and a joint-detail sheet. Output: drawings/parts/*.svg and drawings/*.svg,
combined into drawings/Store_Versile_Drawings.pdf by make_docs.js.
"""
import json
import os
import sys

import numpy as np
import trimesh
from shapely.geometry import Polygon
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build  # noqa: E402

OUT = os.path.join(ROOT, "drawings", "parts")
TABLE = json.load(open(os.path.join(ROOT, "docs", "print_table.json")))
PAGE_W, PAGE_H = 297.0, 210.0          # A4 landscape, mm (SVG user units = mm)

KEY = {
    "Left_Wall_Panel_Upper": "Backer 1.2 + flutes 1.2 (pitch 5.2, 20 flutes). Key notches 3.4 x 3.2 at x=26/78. Shelf-pin holes dia 1.95 at x=13/44, z=133.5/98.5/64.5 from bottom.",
    "Left_Wall_Panel_Lower": "29 tall + 2 key tabs 3 x 0.9 x 3 on top at x=26/78. Stands 1 mm deep in the floor-tile slot.",
    "Right_Wall_Panel_Upper": "15 flutes at 5.2 pitch. Key notches 3.4 x 3.2 at x=19.5/58.5.",
    "Right_Wall_Panel_Lower": "29 tall + 2 key tabs on top at x=19.5/58.5.",
    "Floor_Tile_L": "2 thick. Panel slot 104.4 x 2.7 x 1 deep at back. Male dovetail 4 long (2->3 half-width) on the right edge.",
    "Floor_Tile_C": "2 thick. Female dovetails both ends, clearance 0.15 per side.",
    "Floor_Tile_R": "2 thick. Panel slot 78.4 x 2.7 x 1 deep. Male dovetail on the left edge.",
    "Floating_Shelf": "55 x 8 x 3. Front edges R0.6. Two blind pin holes dia 1.95 x 4 deep in the back edge at x=12/43, mid-thickness.",
    "Photo_Frame_Small_P": "Face border 1.2. Back 1.0 / photo slot 0.5 / lip 1.0. Slot 22.8 wide, open at top. Photo insert 22.6 x 26.4.",
    "Photo_Frame_Small_L": "Face border 1.2. Photo slot 25.8 wide, open at top. Photo insert 25.6 x 23.4.",
    "Photo_Frame_Large_P": "Face border 1.2. Photo slot 28.8 wide, open at top. Photo insert 28.6 x 38.4.",
    "TV_Console_Body": "102 x 24 x 10 deep, corner R5. 3 open bays 30.3 x 9.5, 8 deep. Drawer recess 97 x 9.5 x 0.8. 4 leg sockets 1.7 sq x 3 at x=9/93, y=2.5/7.5.",
    "TV_Console_Drawer_Fronts": "96.7 x 9.2 x 0.8 (recess minus 0.15). Two 0.6 separation grooves.",
    "TV_Console_Leg": "Tapered 2.2 -> 1.5 square, 9 long, splay 12 deg. Peg 1.4 sq x 2.6.",
    "Central_Arch": "78 wide x 176 tall, backer 1.0. Border 2.5 wide, stepped round 2.0 high, open at the floor. Print area inside border 73 x 173.5.",
    "Name_Plate": "20 x 8, R1.6 corners, base 1.0 + raised text 0.6. Edit the NAME line in cad/parts/Name_Plate.scad per order.",
    "Coffee_Table": "Top 60 x 14 x 2.6, corners R3. Apron 2.2 high x 1.2, inset 3.5/2.5. Legs 2.6 -> 1.9 sq, 23.4 long.",
    "Right_Display_Shelf": "Boards 3.2, depth 12, row pitch 32.5 (5 rows). Rows bottom->top [u_left, u_right, dividers]: " + json.dumps(build.E["SU"]["rows"]),
    "Plant_Pot_01": "Ribbed egg vase 15 x 10 x 29, 16 ribs. Two parallel leaf slots 4.4 x 1.4 x 5.2 deep at y = +/-1.8 from centre.",
    "Plant_Pot_02": "24 x 7 x 12, R1.4. Two 0.35 band grooves. Leaf slot 8.4 x 1.4.",
    "Plant_Pot_03": "Oval 15 x 7 x 12, diamond knurl, 1.2 smooth rim. Leaf slot 4.4 x 1.6.",
    "Plant_Pot_04": "Oval 14 x 7 x 10, swirl ribs. Leaf slot 3.8 x 1.4.",
    "Gramophone_Base": "Box 15 x 8 x 8.5 + top box 12 x 7 x 5.2. Horn hole dia 1.75 at 15/-35 deg.",
    "Gramophone_Horn": "Bell R5.5 (oval 0.72 in depth), length 11, wall 0.8. Peg dia 1.5 x 3.",
    "Mug": "Body dia 7.5 x 8, wall 0.9, floor 1.2. Handle ring R2.1, section dia 1.1.",
    "Arch_Vase": "15 x 14 x 5. Three 0.55 grooves. Stem hole dia 2.2 x 4 deep.",
    "Takeaway_Cup": "Dia 7.1 -> 8.7 x 18.5, sleeve band +0.3, lid rim dia 9.3.",
}


def load_installed(part):
    m = trimesh.load(os.path.join(HERE, "build", "installed", part + ".stl"))
    # build/installed meshes are already in the CAD frame (front = -Y, mirrored by build.py)
    m.apply_translation(-m.bounds[0])
    return m


def silhouette(m, drop):
    keep = [i for i in range(3) if i != drop]
    tri = m.triangles[:, :, keep]
    polys = []
    for t in tri:
        p = Polygon(t)
        if p.area > 1e-6:
            polys.append(p.buffer(1e-4, join_style=2))
    return unary_union(polys).buffer(-1e-4, join_style=2)


def sharp_edges(m, drop, deg=28):
    keep = [i for i in range(3) if i != drop]
    ang = m.face_adjacency_angles
    e = m.face_adjacency_edges[ang > np.radians(deg)]
    if len(e) > 6000:
        e = e[:: int(len(e) / 6000) + 1]
    return m.vertices[e][:, :, keep]


def path_of(geom, tx):
    d = []
    geoms = getattr(geom, "geoms", [geom])
    for g in geoms:
        if g.is_empty:
            continue
        for ring in [g.exterior] + list(g.interiors):
            pts = [tx(x, y) for x, y in ring.coords]
            d.append("M" + " L".join(f"{a:.2f},{b:.2f}" for a, b in pts) + " Z")
    return " ".join(d)


SCALES = [10, 8, 5, 4, 3, 2, 1.5, 1, 0.75, 0.5, 0.4]


def sheet(part):
    m = load_installed(part)
    W, D, H = (m.bounds[1] - m.bounds[0])
    area_w, area_h = 250.0, 150.0
    s = next(sc for sc in SCALES if (W + D) * sc + 30 <= area_w and (H + D) * sc + 30 <= area_h)
    ox, oy = 20.0, 22.0 + D * s + 14 + H * s       # front view origin (bottom-left), page coords
    views = {
        "front": (1, lambda x, z: (ox + x * s, oy - z * s)),
        "top": (2, lambda x, y: (ox + x * s, oy - H * s - 14 - (y) * s)),
        "side": (0, lambda y, z: (ox + W * s + 14 + y * s, oy - z * s)),
    }
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{PAGE_W}mm" height="{PAGE_H}mm" viewBox="0 0 {PAGE_W} {PAGE_H}" '
           f'font-family="DejaVu Sans, Arial, sans-serif">',
           f'<rect x="0" y="0" width="{PAGE_W}" height="{PAGE_H}" fill="#fff"/>',
           f'<rect x="6" y="6" width="{PAGE_W - 12}" height="{PAGE_H - 12}" fill="none" stroke="#000" stroke-width="0.5"/>']
    for name, (drop, tx) in views.items():
        sil = silhouette(m, drop)
        for seg in sharp_edges(m, drop):
            (a, b), (c, d) = tx(*seg[0]), tx(*seg[1])
            out.append(f'<line x1="{a:.2f}" y1="{b:.2f}" x2="{c:.2f}" y2="{d:.2f}" stroke="#777" stroke-width="0.12"/>')
        out.append(f'<path d="{path_of(sil, tx)}" fill="none" stroke="#000" stroke-width="0.35" fill-rule="evenodd"/>')
        lx, ly = tx(0, 0)
        out.append(f'<text x="{lx:.1f}" y="{ly + (5 if name != "top" else 4):.1f}" font-size="2.6" fill="#555">'
                   f'{ {"front": "FRONT", "top": "TOP", "side": "RIGHT SIDE"}[name]}</text>')

    def dim(x1, y1, x2, y2, val, vertical=False):
        c = "#c0392b"
        out.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{c}" stroke-width="0.2" '
                   f'marker-start="url(#a)" marker-end="url(#a)"/>')
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        if vertical:
            out.append(f'<text x="{mx - 1.2:.2f}" y="{my:.2f}" font-size="3" fill="{c}" text-anchor="middle" '
                       f'transform="rotate(-90 {mx - 1.2:.2f} {my:.2f})">{val:.1f}</text>')
        else:
            out.append(f'<text x="{mx:.2f}" y="{my - 1:.2f}" font-size="3" fill="{c}" text-anchor="middle">{val:.1f}</text>')
    out.insert(2, '<defs><marker id="a" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">'
                  '<path d="M0,2 L10,5 L0,8 z" fill="#c0392b"/></marker></defs>')
    dim(ox, oy + 9, ox + W * s, oy + 9, W)                                   # width under front
    dim(ox - 6, oy, ox - 6, oy - H * s, H, vertical=True)                    # height left of front
    sx = ox + W * s + 14
    dim(sx, oy + 9, sx + D * s, oy + 9, D)                                   # depth under side
    # title block
    t = TABLE[part]
    tb_x, tb_y = PAGE_W - 6 - 120, PAGE_H - 6 - 40
    out.append(f'<rect x="{tb_x}" y="{tb_y}" width="120" height="40" fill="none" stroke="#000" stroke-width="0.4"/>')
    rows = [("PART", part), ("FILE", f"stl/{part}.stl   QTY {t['qty']}"), ("MATERIAL", t["filament"][:62]),
            ("PRINT", f"{t['orientation']} | layer {t['layer']} | infill {t['infill']}% | {t['walls']} walls | no supports"),
            ("SCALE", f"{s:g} : 1   units mm   third-angle projection   Rev C"),
            ("PROJECT", "Store Versile miniature room frame 300 x 200 x 25")]
    for i, (k, v) in enumerate(rows):
        y = tb_y + 6 + i * 6
        out.append(f'<text x="{tb_x + 2}" y="{y}" font-size="2.4" fill="#666">{k}</text>'
                   f'<text x="{tb_x + 20}" y="{y}" font-size="2.8" fill="#000">{v}</text>')
    if part in KEY:
        words, line, lines = KEY[part].split(), "", []
        for w in words:
            if len(line) + len(w) > 95:
                lines.append(line); line = ""
            line += w + " "
        lines.append(line)
        for i, l in enumerate(lines):
            out.append(f'<text x="10" y="{PAGE_H - 34 + i * 4.2:.1f}" font-size="2.8" fill="#000">{l.strip()}</text>')
        out.append(f'<text x="10" y="{PAGE_H - 39}" font-size="2.6" fill="#666">KEY DIMENSIONS</text>')
    out.append("</svg>")
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, part + ".svg"), "w").write("\n".join(out))
    return s


def assembly_table_svg():
    """positioning table: every piece, its file and where it goes (layout frame, mm)."""
    rows = []
    for label, part, t, r in build.INST:
        rows.append((label, part, t[0], -t[1], t[2], r))
    per = 31
    pages = []
    for p0 in range(0, len(rows), per):
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{PAGE_W}mm" height="{PAGE_H}mm" viewBox="0 0 {PAGE_W} {PAGE_H}" font-family="DejaVu Sans, Arial, sans-serif">',
               f'<rect width="{PAGE_W}" height="{PAGE_H}" fill="#fff"/>',
               f'<rect x="6" y="6" width="{PAGE_W - 12}" height="{PAGE_H - 12}" fill="none" stroke="#000" stroke-width="0.5"/>',
               f'<text x="12" y="16" font-size="5" font-weight="bold">ASSEMBLY POSITIONS ({p0 // per + 1}/{(len(rows) - 1) // per + 1})</text>',
               '<text x="12" y="22" font-size="2.8" fill="#444">Position of each piece\'s reference corner, mm. X from the inner left wall, '
               'Y from the back wall toward the glass, Z from the inner floor. Rotation in degrees (CAD frame).</text>']
        hdr = ["Piece", "File (stl/)", "X", "Y", "Z", "Rotation"]
        xs = [12, 52, 150, 172, 194, 218]
        for x, h in zip(xs, hdr):
            out.append(f'<text x="{x}" y="31" font-size="3" font-weight="bold">{h}</text>')
        for i, (label, part, x, y, z, r) in enumerate(rows[p0:p0 + per]):
            yy = 36.5 + i * 5
            if i % 2 == 0:
                out.append(f'<rect x="10" y="{yy - 3.6}" width="{PAGE_W - 20}" height="5" fill="#f3efe9"/>')
            for xx, v in zip(xs, [label, part + ".stl", f"{x:.2f}", f"{y:.2f}", f"{z:.2f}", str(r)]):
                out.append(f'<text x="{xx}" y="{yy}" font-size="2.9">{v}</text>')
        out.append("</svg>")
        pages.append("\n".join(out))
    for i, pg in enumerate(pages):
        open(os.path.join(ROOT, "drawings", f"assembly_positions_{i + 1}.svg"), "w").write(pg)
    return len(pages)


def joints_svg():
    """joint details (schematic)."""
    s = 5
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{PAGE_W}mm" height="{PAGE_H}mm" viewBox="0 0 {PAGE_W} {PAGE_H}" font-family="DejaVu Sans, Arial, sans-serif">',
         f'<rect width="{PAGE_W}" height="{PAGE_H}" fill="#fff"/>',
         f'<rect x="6" y="6" width="{PAGE_W - 12}" height="{PAGE_H - 12}" fill="none" stroke="#000" stroke-width="0.5"/>',
         '<text x="12" y="16" font-size="5" font-weight="bold">JOINT DETAILS  (schematic sketches, dimensions in mm)</text>']
    R = "#c0392b"

    def txt(x, y, t, sz=2.8, c="#000", bold=False):
        o.append(f'<text x="{x}" y="{y}" font-size="{sz}" fill="{c}"{" font-weight=\"bold\"" if bold else ""}>{t}</text>')

    def rect(x, y, w, h, fill="#e8e1d8", stroke="#000"):
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="0.3"/>')

    # 1 dovetail (plan)
    x0, y0 = 20, 30
    txt(x0, y0, "1  Floor-tile dovetail (plan view)", 3.2, bold=True)
    rect(x0, y0 + 6, 30, 25 * 1.2)
    pts = [(0, -2), (4, -3), (4, 3), (0, 2)]
    cy = y0 + 6 + 12.5 * 1.2
    o.append('<polygon points="' + " ".join(f"{x0 + 30 + px * s:.1f},{cy + py * s:.1f}" for px, py in pts) + '" fill="#e8e1d8" stroke="#000" stroke-width="0.3"/>')
    txt(x0, y0 + 44, "Male on tile L (right edge) and tile R (left edge),")
    txt(x0, y0 + 48, "4 long, half-width 2 at root, 3 at tip. Female in tile C:")
    txt(x0, y0 + 52, "same shape + 0.15 clearance per side.")
    # 2 panel key
    x0 = 110
    txt(x0, y0, "2  Wall-panel key (seam at z = 30)", 3.2, bold=True)
    rect(x0, y0 + 30, 50, 10)
    rect(x0 + 10, y0 + 30 - 3 * s / 2, 3 * s / 2, 3 * s / 2, fill="#cfe3c9")
    txt(x0, y0 + 46, "Lower panel: 2 tabs 3 x 0.9 x 3 on top.")
    txt(x0, y0 + 50, "Upper panel: notches 3.4 x 1.25 x 3.2.")
    txt(x0, y0 + 54, "Seam hidden behind the TV console / shelving unit.")
    # 3 shelf pins
    x0 = 200
    txt(x0, y0, "3  Floating-shelf pins", 3.2, bold=True)
    rect(x0, y0 + 10, 2.4 * s, 30)
    rect(x0 + 2.4 * s, y0 + 20, 8 * s, 3 * s)
    o.append(f'<rect x="{x0 - 2}" y="{y0 + 20 + 1.5 * s - 0.875 * s}" width="{2 + 2.4 * s + 4 * s}" height="{1.75 * s}" fill="#9ec3e6" stroke="#000" stroke-width="0.3"/>')
    txt(x0, y0 + 46, "Pin = 1.75 mm filament, cut 6.4 long.")
    txt(x0, y0 + 50, "Holes 1.95: through the panel,")
    txt(x0, y0 + 54, "4 deep in the shelf. 2 per shelf.")
    # 4 photo slot
    x0, y0 = 20, 100
    txt(x0, y0, "4  Photo-frame section", 3.2, bold=True)
    yb = y0 + 8
    rect(x0, yb, 1.0 * s, 40)                      # back
    rect(x0 + 1.0 * s, yb + 30, 0.5 * s, 10, fill="#fff")
    o.append(f'<rect x="{x0 + 1.0 * s}" y="{yb}" width="{0.5 * s}" height="30" fill="#f6d5a8" stroke="#000" stroke-width="0.3"/>')
    rect(x0 + 1.5 * s, yb + 30, 1.0 * s, 10)        # lip
    txt(x0 + 16, yb + 6, "back 1.0")
    txt(x0 + 16, yb + 12, "photo slot 0.5 (photo paper 0.2-0.3)", c=R)
    txt(x0 + 16, yb + 18, "front lip 1.0, face border 1.2")
    txt(x0 + 16, yb + 24, "insert = frame W - 1.4  x  H - 0.6")
    # 5 leaf slot
    x0 = 110
    txt(x0, y0, "5  Leaf fan into pot (section)", 3.2, bold=True)
    rect(x0, y0 + 20, 40, 25)
    rect(x0 + 20 - 0.7 * s, y0 + 20, 1.4 * s, 5.2 * s / 2, fill="#fff")
    o.append(f'<rect x="{x0 + 20 - 0.5 * s}" y="{y0 + 5}" width="{1.0 * s}" height="{15 + 5 * s / 2}" fill="#9fcf8a" stroke="#000" stroke-width="0.3"/>')
    txt(x0, y0 + 52, "Tab 1.0 thick x 5 deep. Slot = tab + 0.2 each side,")
    txt(x0, y0 + 56, "5.2 deep. Drop of CA glue. Floor vase: 2 parallel slots.")
    # 6 console leg
    x0 = 200
    txt(x0, y0, "6  TV-console leg socket", 3.2, bold=True)
    rect(x0, y0 + 10, 40, 12)
    rect(x0 + 15, y0 + 22 - 3 * s / 2.5, 1.7 * s, 3 * s / 2.5, fill="#fff")
    o.append(f'<polygon points="{x0 + 15.5},{y0 + 22} {x0 + 15.5 + 1.4 * s},{y0 + 22} {x0 + 16 + 1.4 * s},{y0 + 50} {x0 + 9},{y0 + 50}" fill="#ddd" stroke="#000" stroke-width="0.3"/>')
    txt(x0, y0 + 56, "Socket 1.7 sq x 3. Peg 1.4 sq x 2.6. Leg splays")
    txt(x0, y0 + 60, "12 deg outward; turn the right-hand legs 180 deg.")
    txt(12, PAGE_H - 12, "Sketches are not to scale. Exact geometry is in cad/versile_parts.scad and the part sheets.", 2.6, "#666")
    o.append("</svg>")
    open(os.path.join(ROOT, "drawings", "joint_details.svg"), "w").write("\n".join(o))


if __name__ == "__main__":
    for part in build.PARTS:
        sc = sheet(part)
        print(f"{part:26s} scale {sc}:1")
    print("assembly position pages:", assembly_table_svg())
    joints_svg()
