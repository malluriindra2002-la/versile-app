#!/usr/bin/env python3
"""
STORE VERSILE - Miniature Room Frame
Stage 2 layout: single source of truth for every component envelope.

Coordinate system (mm), origin = inside bottom-left-back corner of the frame:
  X = width  (0 = left inner wall,  300 = right inner wall)
  Y = depth  (0 = back wall,         25 = inside face of the glass)
  Z = height (0 = inside floor,     200 = inside top)

Run:  python3 layout.py            -> writes layout.json + drawings/*.svg
These envelopes will drive the OpenSCAD part files in Stage 4, so a change
made here (once approved) propagates to the CAD.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DRAW = os.path.join(HERE, "..", "drawings")

# ---------------------------------------------------------------- box
# Rev B: internal depth reduced to 25 mm (customer request). Front view is
# unchanged; every part is made shallower ("relief" depth), round pots become
# oval in plan so they still look round from the front.
BOX = dict(W=300.0, H=200.0, D=25.0)
FLOOR_T = 2.0          # printed modular floor tiles
GLASS_CLEAR = 3.0      # keep >= 3 mm between any part and the glass
WALL_T = 2.4           # fluted panel: 1.2 backer + 1.2 flutes
FT = 2.5               # photo frame thickness (depth)

# ---------------------------------------------------------------- zones
ZONES = [
    dict(id="L", name="Left wall zone",   x0=0.0,   x1=106.0),
    dict(id="C", name="Centre portrait zone", x0=106.0, x1=218.0),
    dict(id="R", name="Right shelving zone",  x0=218.0, x1=300.0),
]

# ---------------------------------------------------------------- palette (render only)
COL = dict(
    slat="#e9c9a8", white="#fbfaf7", black="#26272b", gold="#c9a227",
    green="#5f9a3c", wood="#c89a62", brown="#5a3d2b", silver="#b9bcc2",
    marble="#f1eeec", photo="#e7d6cf", floor="#b9824c", ivory="#f3e6d3",
)

C = []   # component envelopes


def add(id, name, x0, x1, z0, z1, y0, y1, shape="rect", color="white",
        zone="", stl="", qty=1, note="", **extra):
    d = dict(id=id, name=name, x0=x0, x1=x1, z0=z0, z1=z1, y0=y0, y1=y1,
             w=round(x1 - x0, 2), h=round(z1 - z0, 2), d=round(y1 - y0, 2),
             shape=shape, color=color, zone=zone, stl=stl, qty=qty, note=note)
    d.update(extra)
    C.append(d)
    return d


D = BOX["D"]

# ================================================================ FLOOR
add("FL1", "Floor tile - left",   0, 106, 0, FLOOR_T, 0, D, color="floor", zone="L", stl="Floor_Tile_L")
add("FL2", "Floor tile - centre", 106, 218, 0, FLOOR_T, 0, D, color="floor", zone="C", stl="Floor_Tile_C")
add("FL3", "Floor tile - right",  218, 300, 0, FLOOR_T, 0, D, color="floor", zone="R", stl="Floor_Tile_R")

# ================================================================ LEFT ZONE
FLUTE_PITCH = 5.2
add("LW", "Left fluted wall panel (2 pcs, seam z=30 hidden behind console)",
    2, 106, FLOOR_T, 198, 0, WALL_T, shape="fluted", color="slat", zone="L",
    stl="Left_Wall_Panel_Lower + Left_Wall_Panel_Upper", pitch=FLUTE_PITCH, seam_z=30.0)

SHELF_TOPS = [165.0, 130.0, 96.0]
SHELF_D = 8.0
for i, zt in enumerate(SHELF_TOPS, 1):
    add(f"S{i}", f"Floating shelf {i}", 3, 58, zt - 3.0, zt, WALL_T, WALL_T + SHELF_D,
        color="ivory", zone="L", stl="Floating_Shelf")

SF = (24.0, 27.0)   # small frame W x H (portrait); landscape = 27 x 24
LF = (30.0, 39.0)   # large frame W x H (portrait)
FY = (WALL_T + 0.6, WALL_T + 0.6 + FT)   # frames stand/lean against the wall

add("LOVE", "LOVE lettering (LO/VE stacked)", 7, 28, 165, 183, 3, 7, color="white", zone="L", stl="LOVE_Letters")
add("F1", "Photo frame - small portrait", 32, 32 + SF[0], 165, 165 + SF[1], *FY, shape="frame", color="gold", zone="L", stl="Photo_Frame_Small")
add("F2", "Photo frame - small portrait", 7, 7 + SF[0], 130, 130 + SF[1], *FY, shape="frame", color="gold", zone="L", stl="Photo_Frame_Small")
add("PB", "Shelf plant B - leafy spray in rectangular pot", 33, 57, 130, 157, 3, 10, shape="plant", color="green", zone="L",
    stl="Plant_Pot_02 + Plant_Leaves_02", pot_h=12.0, pot_w=24.0)
add("PC", "Shelf plant C - succulent in textured oval pot", 8, 23, 96, 122, 3, 10, shape="plant", color="green", zone="L",
    stl="Plant_Pot_03 + Plant_Leaves_03", pot_h=12.0, pot_w=15.0)
add("F3", "Photo frame - small portrait", 32, 32 + SF[0], 96, 96 + SF[1], *FY, shape="frame", color="gold", zone="L", stl="Photo_Frame_Small")
add("F4", "Photo frame - large portrait (wall)", 68, 68 + LF[0], 135, 135 + LF[1], WALL_T, WALL_T + FT, shape="frame", color="gold", zone="L", stl="Photo_Frame_Large")
add("F5", "Photo frame - large portrait (wall)", 68, 68 + LF[0], 76, 76 + LF[1], WALL_T, WALL_T + FT, shape="frame", color="gold", zone="L", stl="Photo_Frame_Large")

CON_TOP = FLOOR_T + 9.0 + 24.0    # legs 9, body 24 -> top at z=35
add("TV", "TV console (black body, 3 open bays, 3 white drawer fronts, 4 splayed legs)",
    3, 105, FLOOR_T, CON_TOP, WALL_T, WALL_T + 10, shape="console", color="black", zone="L",
    stl="TV_Console_Body + TV_Console_Drawer_Fronts + TV_Console_Leg x4", leg_h=9.0)
add("GR", "Gramophone on stacked box base", 10, 28, CON_TOP, CON_TOP + 27, 3, 11, shape="gramophone", color="gold", zone="L",
    stl="Gramophone_Base + Gramophone_Horn")
add("PD2", "Small fern in swirl pot (same parts as PD)", 44, 58, CON_TOP, CON_TOP + 17, 4, 11, shape="plant", color="green", zone="L",
    stl="Plant_Pot_04 + Plant_Leaves_04", pot_h=10.0, pot_w=14.0)
add("BK", "Book stack (3 books)", 74, 98, CON_TOP, CON_TOP + 16.5, 3.5, 11, shape="books", color="white", zone="L",
    stl="Book_01 + Book_02 + Book_03")

# ================================================================ CENTRE ZONE
CX = 162.0   # centre line of arch / table / plants
ARCH_W, ARCH_TOP = 78.0, 178.0
add("AR", "Central arch: 1.0 mm backer + 2.5 wide x 2 mm raised rounded border; photo insert in front",
    CX - ARCH_W / 2, CX + ARCH_W / 2, FLOOR_T, ARCH_TOP, 0, 3.0, shape="arch", color="marble", zone="C",
    stl="Central_Arch", border=2.5)
add("NP", "Name plate (parametric raised text)", CX - 10, CX + 10, 152, 160, 1.3, 2.8, color="white", zone="C",
    stl="Name_Plate (generated per order)")

TBL_W, TBL_D, TBL_H = 60.0, 14.0, 26.0
TBL_Y0 = 5.0
TBL_TOP = FLOOR_T + TBL_H
add("CT", "Coffee table (rounded top, apron, 4 tapered legs)", CX - TBL_W / 2, CX + TBL_W / 2, FLOOR_T, TBL_TOP,
    TBL_Y0, TBL_Y0 + TBL_D, shape="table", color="ivory", zone="C", stl="Coffee_Table")
add("TR", "Serving tray (arch-ripple pattern)", 135, 173, TBL_TOP, TBL_TOP + 1.5, 7, 17, color="wood", zone="C", stl="Serving_Tray")
add("M1", "Coffee mug 1", 140, 150, TBL_TOP + 1.5, TBL_TOP + 9.5, 8.5, 16, shape="mug", color="white", zone="C", stl="Mug_01")
add("M2", "Coffee mug 2", 151, 161, TBL_TOP + 1.5, TBL_TOP + 9.5, 8.5, 16, shape="mug", color="white", zone="C", stl="Mug_02")
add("AV", "Rainbow-arch vase", 175, 190, TBL_TOP, TBL_TOP + 14, 9, 14, shape="archvase", color="wood", zone="C", stl="Arch_Vase")
add("SH", "Silver heart foliage", 177, 188, TBL_TOP + 12, TBL_TOP + 24, 9.5, 13.5, shape="blob", color="silver", zone="C", stl="Silver_Heart_Plant")

PLANT_DX = 44.0
for sid, sx in (("PA1", CX - PLANT_DX), ("PA2", CX + PLANT_DX)):
    add(sid, "Floor plant A - fern in ribbed oval vase", sx - 15, sx + 15, FLOOR_T, FLOOR_T + 54, 4, 20,
        shape="plant", color="green", zone="C", stl="Plant_Pot_01 + Plant_Leaves_01", pot_h=29.0, pot_w=15.0,
        pot_y=(6.0, 16.0))

# ================================================================ RIGHT ZONE
add("RW", "Right fluted wall panel (2 pcs, seam z=30 hidden behind shelving)",
    219, 297, FLOOR_T, 198, 0, WALL_T, shape="fluted", color="slat", zone="R",
    stl="Right_Wall_Panel_Lower + Right_Wall_Panel_Upper", pitch=FLUTE_PITCH, seam_z=30.0)

UX0 = 223.0          # shelving unit datum
BOARD = 2.5
UNIT_D = 12.0
ROW_Z = [2.0, 34.5, 67.0, 99.5, 132.0, 164.5]      # board centre heights bottom->top
# rows listed bottom -> top : (u_left, u_right, [divider u positions])
ROWS = [
    (7, 75, [51]),        # row 5 (bottom): books | elephant
    (3, 69, [27]),        # row 4: bunny | photo
    (7, 75, [23, 48]),    # row 3: donut vase | plaque | plant D
    (0, 73, [25]),        # row 2: cup | photo
    (3, 73, [48]),        # row 1 (top): photo | gold ornament
]
add("SU", "Asymmetric staggered open-cube display shelf (no back)", UX0, UX0 + 75, FLOOR_T, ROW_Z[-1] + BOARD / 2,
    WALL_T, WALL_T + UNIT_D, shape="unit", color="ivory", zone="R", stl="Right_Display_Shelf", rows=ROWS, row_z=ROW_Z, board=BOARD, ux0=UX0)


def cell(row, idx):
    """inner x-range and floor z of a shelf cell (row 0 = bottom)."""
    ul, ur, divs = ROWS[row]
    edges = [ul] + divs + [ur]
    a, b = edges[idx], edges[idx + 1]
    return UX0 + a + BOARD / 2, UX0 + b - BOARD / 2, ROW_Z[row] + BOARD / 2


def place(id, name, row, idx, w, h, y0, y1, **kw):
    a, b, zf = cell(row, idx)
    cx = (a + b) / 2
    return add(id, name, cx - w / 2, cx + w / 2, zf, zf + h, y0, y1, zone="R", **kw)


place("F7", "Photo frame - small landscape", 4, 0, SF[1], SF[0], *FY, shape="frame", color="gold", stl="Photo_Frame_Small")
place("GO", "Gold ornament (gold sphere pot + egg/leaf cluster)", 4, 1, 17, 21, 4, 12, shape="blob", color="gold", stl="Gold_Ornament")
place("CUP", "Takeaway coffee cup with lid & sleeve (plain, unbranded)", 3, 0, 9, 22, 4, 13, shape="cup", color="white", stl="Takeaway_Cup")
place("F8", "Photo frame - small landscape", 3, 1, SF[1], SF[0], *FY, shape="frame", color="gold", stl="Photo_Frame_Small")
place("DV", "Donut vase + pampas spray", 2, 0, 12, 26, 5, 10, shape="donut", color="white", stl="Donut_Vase + Pampas_Spray")
place("PQ", "Message plaque (small frame, portrait)", 2, 1, SF[0], SF[1], *FY, shape="frame", color="gold", stl="Photo_Frame_Small (+ quote print)")
place("PD", "Shelf plant D - small fern in swirl pot", 2, 2, 14, 17, 4, 11, shape="plant", color="green",
      stl="Plant_Pot_04 + Plant_Leaves_04", pot_h=10.0, pot_w=14.0)
place("BN", "Bunny figurine (sitting)", 1, 0, 13, 24, 4, 12, shape="bunny", color="white", stl="Bunny")
place("F9", "Photo frame - small landscape", 1, 1, SF[1], SF[0], *FY, shape="frame", color="gold", stl="Photo_Frame_Small")
place("BK2", "Book stack (2 books, same parts as BK)", 0, 0, 24, 11, 3.5, 11, shape="books", color="white", stl="Book_01 + Book_02")
place("EL", "Geometric gold elephant", 0, 1, 16, 17, 4, 12, shape="blob", color="gold", stl="Gold_Elephant")

# optional
add("LED", "LED strip channel (optional, 2 pcs)", 2, 298, 192, 198, 17, 22, color="white", zone="-", stl="LED_Channel_L + LED_Channel_R",
    note="optional")


# ================================================================ checks
def checks():
    out = []
    for c in C:
        if c["x0"] < 0 or c["x1"] > BOX["W"] or c["z0"] < 0 or c["z1"] > BOX["H"] or c["y0"] < 0 or c["y1"] > BOX["D"]:
            out.append(f"OUTSIDE BOX: {c['id']}")
        if c["id"] != "LED" and not c["id"].startswith("FL") and c["y1"] > BOX["D"] - GLASS_CLEAR:
            out.append(f"GLASS CLEARANCE < {GLASS_CLEAR}: {c['id']} (front y={c['y1']})")
    # single-print fit on A1 mini (envelope of the largest single printed piece)
    big = {"LW": (104, 168, 2.4), "RW": (78, 168, 2.4), "AR": (78, 176, 3), "SU": (75, 163.75, 12), "TV": (102, 10, 24)}
    for k, (a, b, t) in big.items():
        if max(a, b, t) > 180:
            out.append(f"BUILD VOLUME: {k}")
    return out


# ================================================================ SVG helpers
def svg_open(w, h, title, sc=3.0, m=60):
    W, H = w * sc + 2 * m, h * sc + 2 * m + 40
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}" '
         f'font-family="Helvetica,Arial,sans-serif">',
         f'<rect width="100%" height="100%" fill="#ffffff"/>',
         f'<text x="{m}" y="28" font-size="18" font-weight="bold" fill="#222">{title}</text>']
    return s, sc, m


def dim_h(s, X, x0, x1, y, txt=None, off=0):
    a, b = X(x0), X(x1)
    t = txt or f"{x1 - x0:g}"
    s.append(f'<g stroke="#c0392b" stroke-width="1" fill="#c0392b" font-size="11">'
             f'<line x1="{a}" y1="{y}" x2="{b}" y2="{y}"/>'
             f'<line x1="{a}" y1="{y-5}" x2="{a}" y2="{y+5}"/><line x1="{b}" y1="{y-5}" x2="{b}" y2="{y+5}"/>'
             f'<text x="{(a+b)/2}" y="{y-4+off}" text-anchor="middle" stroke="none">{t}</text></g>')


def dim_v(s, Z, z0, z1, x, txt=None, left=True):
    a, b = Z(z0), Z(z1)
    t = txt or f"{z1 - z0:g}"
    tx = x - 4 if left else x + 4
    anc = "end" if left else "start"
    s.append(f'<g stroke="#c0392b" stroke-width="1" fill="#c0392b" font-size="11">'
             f'<line x1="{x}" y1="{a}" x2="{x}" y2="{b}"/>'
             f'<line x1="{x-5}" y1="{a}" x2="{x+5}" y2="{a}"/><line x1="{x-5}" y1="{b}" x2="{x+5}" y2="{b}"/>'
             f'<text x="{tx}" y="{(a+b)/2+4}" text-anchor="{anc}" stroke="none">{t}</text></g>')


# ================================================================ FRONT VIEW
def front_svg():
    s, sc, m = svg_open(BOX["W"], BOX["H"], "FRONT ELEVATION (X-Z)  -  Store Versile room frame  -  all dims mm", sc=3.2, m=110)
    X = lambda x: m + x * sc
    Z = lambda z: m + 40 + (BOX["H"] - z) * sc
    # box + back wall
    s.append(f'<rect x="{X(0)}" y="{Z(200)}" width="{300*sc}" height="{200*sc}" fill="#f6f5f2" stroke="#111" stroke-width="3"/>')
    order = sorted(C, key=lambda c: c["y0"])
    for c in order:
        if c["id"] == "LED":
            s.append(f'<rect x="{X(c["x0"])}" y="{Z(c["z1"])}" width="{(c["x1"]-c["x0"])*sc}" height="{(c["z1"]-c["z0"])*sc}" '
                     f'fill="none" stroke="#999" stroke-dasharray="6 4"/>')
            continue
        draw(s, c, X, Z, sc)
    # zone lines
    for zn in ZONES[1:]:
        s.append(f'<line x1="{X(zn["x0"])}" y1="{Z(200)-6}" x2="{X(zn["x0"])}" y2="{Z(0)+30}" stroke="#2c6fbb" stroke-dasharray="4 4"/>')
    # ---- dimensions
    yb = Z(0) + 28
    dim_h(s, X, 0, 300, Z(0) + 70, "300 internal width")
    for zn in ZONES:
        dim_h(s, X, zn["x0"], zn["x1"], yb, f'{zn["id"]}: {zn["x1"]-zn["x0"]:g}')
    dim_v(s, Z, 0, 200, X(0) - 70, "200")
    # left: shelves + console
    dim_v(s, Z, 0, FLOOR_T + 9, X(0) - 8, "floor+legs 11")
    dim_v(s, Z, FLOOR_T + 9, CON_TOP, X(0) - 8, "24")
    for zt in SHELF_TOPS:
        s.append(f'<text x="{X(58)+3}" y="{Z(zt)+4}" font-size="10" fill="#c0392b">shelf top z={zt:g}</text>')
    dim_h(s, X, 3, 58, Z(SHELF_TOPS[0]) - 34, "shelf 55")
    dim_h(s, X, 3, 105, Z(CON_TOP) + 12, "console 102", off=24)
    dim_h(s, X, 68, 98, Z(174) - 6, "30")
    dim_v(s, Z, 135, 174, X(98) + 6, "39", left=False)
    # centre
    dim_h(s, X, CX - ARCH_W / 2, CX + ARCH_W / 2, Z(ARCH_TOP) - 10, f"arch {ARCH_W:g}")
    dim_v(s, Z, FLOOR_T, ARCH_TOP, X(CX + ARCH_W / 2) - 8, f"{ARCH_TOP-FLOOR_T:g}")
    dim_h(s, X, CX - TBL_W / 2, CX + TBL_W / 2, Z(TBL_TOP) + 60, f"table {TBL_W:g}", off=26)
    dim_h(s, X, CX - PLANT_DX, CX + PLANT_DX, Z(FLOOR_T + 54) - 8, f"plant c/c {2*PLANT_DX:g}")
    s.append(f'<line x1="{X(CX)}" y1="{Z(200)}" x2="{X(CX)}" y2="{Z(0)}" stroke="#2c6fbb" stroke-width="0.8" stroke-dasharray="10 3 2 3"/>')
    s.append(f'<text x="{X(CX)+3}" y="{Z(196)}" font-size="10" fill="#2c6fbb">CL x={CX:g}</text>')
    # right unit rows
    for i in range(5):
        dim_v(s, Z, ROW_Z[i], ROW_Z[i + 1], X(300) + 10, f"{ROW_Z[i+1]-ROW_Z[i]:g}", left=False)
    dim_h(s, X, UX0, UX0 + 75, Z(ROW_Z[-1]) - 14, "unit 75")
    s.append(f'<text x="{X(0)}" y="{Z(0)+100}" font-size="11" fill="#555">Dashed box at top = LED strip zone (optional channel).  '
             f'Blue dashed = zone boundaries / module seams.  Red = dimensions.  Scale approx. 1:12.</text>')
    s.append("</svg>")
    return "\n".join(s)


def draw(s, c, X, Z, sc):
    col = COL[c["color"]]
    x0, x1, z0, z1 = c["x0"], c["x1"], c["z0"], c["z1"]
    w, h = (x1 - x0) * sc, (z1 - z0) * sc
    sh = c["shape"]
    st = 'stroke="#333" stroke-width="0.8"'
    if sh == "fluted":
        s.append(f'<rect x="{X(x0)}" y="{Z(z1)}" width="{w}" height="{h}" fill="{col}" {st}/>')
        n = int(round((x1 - x0) / c["pitch"]))
        for i in range(1, n):
            xx = X(x0 + i * (x1 - x0) / n)
            s.append(f'<line x1="{xx}" y1="{Z(z1)}" x2="{xx}" y2="{Z(z0)}" stroke="#c9a283" stroke-width="1"/>')
        s.append(f'<line x1="{X(x0)}" y1="{Z(c["seam_z"])}" x2="{X(x1)}" y2="{Z(c["seam_z"])}" stroke="#8e44ad" stroke-width="1.2" stroke-dasharray="3 3"/>')
    elif sh == "arch":
        r = (x1 - x0) / 2
        def path(inset):
            a, b, top, bot = x0 + inset, x1 - inset, z1 - inset, z0
            rr = r - inset
            return (f'M{X(a)},{Z(bot)} L{X(a)},{Z(top-rr)} A{rr*sc},{rr*sc} 0 0 1 {X(b)},{Z(top-rr)} L{X(b)},{Z(bot)} Z')
        s.append(f'<path d="{path(0)}" fill="#ffffff" {st}/>')
        s.append(f'<path d="{path(c["border"])}" fill="{col}" stroke="#bbb"/>')
        s.append(f'<path d="M{X(x0+22)},{Z(z1-14)} q20,60 -5,120 q30,40 10,90" fill="none" stroke="#d4b25a" stroke-width="1.5"/>')
        s.append(f'<text x="{X((x0+x1)/2)}" y="{Z(95)}" font-size="12" text-anchor="middle" fill="#999">customer photo</text>')
        s.append(f'<text x="{X((x0+x1)/2)}" y="{Z(89)}" font-size="12" text-anchor="middle" fill="#999">on marble print</text>')
    elif sh == "frame":
        b = 1.2 * sc
        s.append(f'<rect x="{X(x0)}" y="{Z(z1)}" width="{w}" height="{h}" fill="{col}" {st}/>')
        s.append(f'<rect x="{X(x0)+b}" y="{Z(z1)+b}" width="{w-2*b}" height="{h-2*b}" fill="#ffffff"/>')
        s.append(f'<rect x="{X(x0)+b+4}" y="{Z(z1)+b+4}" width="{w-2*b-8}" height="{h-2*b-8}" fill="{COL["photo"]}"/>')
    elif sh == "plant":
        ph, pw = c["pot_h"], c["pot_w"]
        cx = (x0 + x1) / 2
        s.append(f'<path d="M{X(cx)},{Z(z0+ph)} ' + " ".join(
            f'Q{X(cx + dx*0.5)},{Z(z0 + ph + (z1-z0-ph)*0.9)} {X(cx + dx)},{Z(z0 + ph + (z1-z0-ph)*k)} M{X(cx)},{Z(z0+ph)}'
            for dx, k in [(-(x1-x0)/2, .55), (-(x1-x0)/3, .9), (-(x1-x0)/6, 1), (0, 1), ((x1-x0)/6, 1), ((x1-x0)/3, .9), ((x1-x0)/2, .55)])
            + f'" fill="none" stroke="{col}" stroke-width="{2.2*sc/3}" stroke-linecap="round"/>')
        s.append(f'<rect x="{X(cx-pw/2)}" y="{Z(z0+ph)}" width="{pw*sc}" height="{ph*sc}" rx="{1.5*sc}" fill="#ffffff" {st}/>')
        for i in range(1, 5):
            xx = X(cx - pw / 2 + i * pw / 5)
            s.append(f'<line x1="{xx}" y1="{Z(z0+ph)+2}" x2="{xx}" y2="{Z(z0)-2}" stroke="#ddd"/>')
    elif sh == "console":
        lh = c["leg_h"]
        for lx, dx in ((x0 + 9, -4), (x0 + 13, 2), (x1 - 13, -2), (x1 - 9, 4)):
            s.append(f'<line x1="{X(lx)}" y1="{Z(z0+lh)}" x2="{X(lx+dx)}" y2="{Z(z0)}" stroke="#ddd" stroke-width="{2.4*sc/3}" stroke-linecap="round"/>')
        bz0 = z0 + lh
        s.append(f'<rect x="{X(x0)}" y="{Z(z1)}" width="{w}" height="{(z1-bz0)*sc}" rx="{6*sc}" fill="{col}" {st}/>')
        bw = (x1 - x0 - 4) / 3
        for i in range(3):
            bx = x0 + 2 + i * bw
            s.append(f'<rect x="{X(bx+0.6)}" y="{Z(z1-2)}" width="{(bw-1.2)*sc}" height="{9*sc}" fill="#111"/>')
            s.append(f'<rect x="{X(bx+0.4)}" y="{Z(bz0+11.5)}" width="{(bw-0.8)*sc}" height="{10*sc}" fill="#fff" stroke="#999"/>')
    elif sh == "table":
        tt = 3.0
        for lx, dx in ((x0 + 4, -1), (x1 - 4, 1)):
            s.append(f'<line x1="{X(lx)}" y1="{Z(z1-tt)}" x2="{X(lx+dx)}" y2="{Z(z0)}" stroke="{COL["wood"]}" stroke-width="{3*sc}" stroke-linecap="butt"/>')
        s.append(f'<rect x="{X(x0+4)}" y="{Z(z1-tt)}" width="{(x1-x0-8)*sc}" height="{2.5*sc}" fill="{COL["wood"]}"/>')
        s.append(f'<rect x="{X(x0)}" y="{Z(z1)}" width="{w}" height="{tt*sc}" rx="{1.5*sc}" fill="#fff" {st}/>')
    elif sh == "unit":
        bd = c["board"]
        rows, rz = c["rows"], c["row_z"]
        ux = c["ux0"]
        # shadow interior
        for i, (ul, ur, divs) in enumerate(rows):
            s.append(f'<rect x="{X(ux+ul)}" y="{Z(rz[i+1])}" width="{(ur-ul)*sc}" height="{(rz[i+1]-rz[i])*sc}" fill="#ead2b4"/>')
        for i, (ul, ur, divs) in enumerate(rows):
            zb, zt = rz[i], rz[i + 1]
            for u in [ul] + divs + [ur]:
                s.append(f'<rect x="{X(ux+u-bd/2)}" y="{Z(zt)}" width="{bd*sc}" height="{(zt-zb)*sc}" fill="{col}" {st}/>')
        for i in range(len(rz)):
            lo = rows[max(0, i - 1)] if i > 0 else rows[0]
            hi = rows[min(i, len(rows) - 1)]
            a = min(lo[0], hi[0]) if 0 < i < len(rows) else (rows[0][0] if i == 0 else rows[-1][0])
            b = max(lo[1], hi[1]) if 0 < i < len(rows) else (rows[0][1] if i == 0 else rows[-1][1])
            s.append(f'<rect x="{X(ux+a-bd/2)}" y="{Z(rz[i]+bd/2)}" width="{(b-a+bd)*sc}" height="{bd*sc}" fill="{col}" {st}/>')
    elif sh == "mug":
        s.append(f'<rect x="{X(x0)}" y="{Z(z1)}" width="{(w-2.5*sc)}" height="{h}" rx="{1*sc}" fill="#fff" {st}/>')
        s.append(f'<path d="M{X(x1-2.5)},{Z(z1-1.5)} a{2.2*sc},{2.6*sc} 0 0 1 0,{5*sc}" fill="none" stroke="#333" stroke-width="{1*sc}"/>')
    elif sh == "archvase":
        r = (x1 - x0) / 2
        s.append(f'<path d="M{X(x0)},{Z(z0)} L{X(x0)},{Z(z1-r)} A{r*sc},{r*sc} 0 0 1 {X(x1)},{Z(z1-r)} L{X(x1)},{Z(z0)} Z" fill="#e8d3a6" {st}/>')
        for k in (0.75, 0.55, 0.35):
            rr = r * k
            s.append(f'<path d="M{X(x0+r-rr)},{Z(z0)} L{X(x0+r-rr)},{Z(z1-r)} A{rr*sc},{rr*sc} 0 0 1 {X(x0+r+rr)},{Z(z1-r)} L{X(x0+r+rr)},{Z(z0)}" fill="none" stroke="#b89b62"/>')
    elif sh == "donut":
        cx = (x0 + x1) / 2
        s.append(f'<path d="M{X(cx)},{Z(z0+14)} l-3,{-12*sc/3} M{X(cx)},{Z(z0+14)} l0,{-12*sc} M{X(cx)},{Z(z0+14)} l3,{-12*sc/3}" stroke="#e9e1d0" stroke-width="{1.2*sc}"/>')
        s.append(f'<circle cx="{X(cx)}" cy="{Z(z0+6)}" r="{6*sc}" fill="#fff" {st}/><circle cx="{X(cx)}" cy="{Z(z0+6)}" r="{2*sc}" fill="#ead2b4" {st}/>')
    elif sh == "bunny":
        cx = (x0 + x1) / 2
        s.append(f'<ellipse cx="{X(cx)}" cy="{Z(z0+6)}" rx="{6.5*sc}" ry="{6*sc}" fill="#fff" {st}/>')
        s.append(f'<ellipse cx="{X(cx)}" cy="{Z(z0+14)}" rx="{4.5*sc}" ry="{4.5*sc}" fill="#fff" {st}/>')
        for dx in (-2, 2):
            s.append(f'<ellipse cx="{X(cx+dx)}" cy="{Z(z0+20.5)}" rx="{1.4*sc}" ry="{3.5*sc}" fill="#fff" {st}/>')
    elif sh == "cup":
        s.append(f'<path d="M{X(x0+1)},{Z(z0)} L{X(x0)},{Z(z1-3)} L{X(x1)},{Z(z1-3)} L{X(x1-1)},{Z(z0)} Z" fill="#fff" {st}/>')
        s.append(f'<rect x="{X(x0-0.4)}" y="{Z(z1)}" width="{(w+0.8*sc)}" height="{3*sc}" rx="{1*sc}" fill="#fff" {st}/>')
        s.append(f'<rect x="{X(x0+0.3)}" y="{Z(z0+13)}" width="{w-0.6*sc}" height="{6*sc}" fill="#cfe0c3" {st}/>')
    elif sh == "gramophone":
        s.append(f'<rect x="{X(x0+1.5)}" y="{Z(z0+17)}" width="{15*sc}" height="{17*sc}" fill="{COL["brown"]}" {st}/>')
        s.append(f'<line x1="{X(x0+9)}" y1="{Z(z0+17)}" x2="{X(x0+9)}" y2="{Z(z0+20)}" stroke="#333" stroke-width="3"/>')
        s.append(f'<ellipse cx="{X(x0+8)}" cy="{Z(z1-4)}" rx="{6.5*sc}" ry="{4.5*sc}" fill="{col}" {st} transform="rotate(-25 {X(x0+8)} {Z(z1-4)})"/>')
    elif sh == "books":
        for i, cc in enumerate(("#fff", "#26272b", "#fff")):
            s.append(f'<rect x="{X(x0+ (i%2))}" y="{Z(z0+5.5*(i+1))}" width="{(w-1*sc)}" height="{5.5*sc}" fill="{cc}" {st}/>')
    elif sh == "blob":
        s.append(f'<ellipse cx="{X((x0+x1)/2)}" cy="{Z((z0+z1)/2)}" rx="{w/2}" ry="{h/2}" fill="{col}" {st}/>')
    else:
        s.append(f'<rect x="{X(x0)}" y="{Z(z1)}" width="{w}" height="{h}" fill="{col}" {st}/>')
    if c["shape"] not in ("fluted", "unit") and not c["id"].startswith("FL"):
        s.append(f'<text x="{X(x0)+1}" y="{Z(z1)+9}" font-size="8" fill="#1d5fa8" font-weight="bold">{c["id"]}</text>')
    if c["shape"] in ("fluted",):
        s.append(f'<text x="{X(x0)+3}" y="{Z(z0)-3}" font-size="9" fill="#1d5fa8" font-weight="bold">{c["id"]}</text>')


# ================================================================ SIDE SECTION (Y-Z) and PLAN (X-Y)
def side_svg():
    s, sc, m = svg_open(BOX["D"] + 110, BOX["H"], "SIDE SECTION (Y-Z) - 25 mm depth, all zones overlaid", sc=3.2, m=70)
    Y = lambda y: m + 40 + y * sc
    Z = lambda z: m + 40 + (BOX["H"] - z) * sc
    s.append(f'<rect x="{Y(0)}" y="{Z(200)}" width="{D*sc}" height="{200*sc}" fill="#f6f5f2" stroke="#111" stroke-width="3"/>')
    s.append(f'<line x1="{Y(D)}" y1="{Z(200)}" x2="{Y(D)}" y2="{Z(0)}" stroke="#4aa3df" stroke-width="5"/>')
    s.append(f'<text x="{Y(D)+6}" y="{Z(100)}" font-size="11" fill="#4aa3df">GLASS (y=25)</text>')
    s.append(f'<rect x="{Y(D-GLASS_CLEAR)}" y="{Z(200)}" width="{GLASS_CLEAR*sc}" height="{200*sc}" fill="#4aa3df" opacity="0.08"/>')
    s.append(f'<text x="{Y(D-GLASS_CLEAR)+2}" y="{Z(60)}" font-size="9" fill="#4aa3df" transform="rotate(-90 {Y(D-GLASS_CLEAR)+10} {Z(60)})">3 mm keep-out</text>')
    for c in sorted(C, key=lambda c: -(c["z1"] - c["z0"]) * (c["y1"] - c["y0"])):
        col = COL[c["color"]]
        dash = ' stroke-dasharray="4 3"' if c["id"] == "LED" else ""
        s.append(f'<rect x="{Y(c["y0"])}" y="{Z(c["z1"])}" width="{(c["y1"]-c["y0"])*sc}" height="{(c["z1"]-c["z0"])*sc}" '
                 f'fill="{col}" fill-opacity="0.55" stroke="#333" stroke-width="0.7"{dash}/>')
    labels = [("wall panels / arch 0-3", 0, 3, 185), ("shelves 2.4-10.4", 2.4, 10.4, 168), ("console 2.4-12.4", 2.4, 12.4, 30),
              ("shelf unit 2.4-14.4", 2.4, 14.4, 120), ("coffee table 5-19", 5, 19, 22), ("floor plants 4-20", 4, 20, 62)]
    for t, a, b, z in labels:
        s.append(f'<text x="{Y(D)+8}" y="{Z(z)}" font-size="10" fill="#c0392b">{t}</text>')
        s.append(f'<line x1="{Y((a+b)/2)}" y1="{Z(z)}" x2="{Y(D)+6}" y2="{Z(z)-3}" stroke="#c0392b" stroke-width="0.5"/>')
    dim_h(s, Y, 0, D, Z(0) + 28, "25 internal depth")
    s.append("</svg>")
    return "\n".join(s)


def plan_svg():
    s, sc, m = svg_open(BOX["W"], BOX["D"] + 20, "PLAN VIEW (X-Y) - footprints on floor tiles (back wall at top)", sc=3.2, m=70)
    X = lambda x: m + x * sc
    Y = lambda y: m + 40 + y * sc
    s.append(f'<rect x="{X(0)}" y="{Y(0)}" width="{300*sc}" height="{D*sc}" fill="{COL["floor"]}" fill-opacity="0.35" stroke="#111" stroke-width="3"/>')
    for zn in ZONES[1:]:
        s.append(f'<line x1="{X(zn["x0"])}" y1="{Y(0)}" x2="{X(zn["x0"])}" y2="{Y(D)}" stroke="#2c6fbb" stroke-width="2" stroke-dasharray="5 4"/>')
    floor_items = [c for c in C if c["z0"] <= FLOOR_T + 0.01 and not c["id"].startswith("FL")]
    for c in floor_items:
        col = COL[c["color"]]
        if c["shape"] == "plant":
            cx = (c["x0"] + c["x1"]) / 2
            py = c.get("pot_y", (c["y0"], c["y1"]))
            cy = (py[0] + py[1]) / 2
            s.append(f'<ellipse cx="{X(cx)}" cy="{Y(cy)}" rx="{(c["x1"]-c["x0"])/2*sc}" ry="{(c["y1"]-c["y0"])/2*sc}" fill="{col}" fill-opacity="0.25" stroke="{col}" stroke-dasharray="3 2"/>')
            s.append(f'<circle cx="{X(cx)}" cy="{Y(cy)}" r="{c["pot_w"]/2*sc}" fill="#fff" stroke="#333"/>')
        else:
            s.append(f'<rect x="{X(c["x0"])}" y="{Y(c["y0"])}" width="{(c["x1"]-c["x0"])*sc}" height="{(c["y1"]-c["y0"])*sc}" '
                     f'fill="{col}" fill-opacity="0.6" stroke="#333"/>')
        s.append(f'<text x="{X(c["x0"])+2}" y="{Y(c["y1"])-3}" font-size="10" fill="#1d5fa8" font-weight="bold">{c["id"]}</text>')
    s.append(f'<line x1="{X(0)}" y1="{Y(D-GLASS_CLEAR)}" x2="{X(300)}" y2="{Y(D-GLASS_CLEAR)}" stroke="#4aa3df" stroke-dasharray="6 4"/>')
    s.append(f'<text x="{X(300)+4}" y="{Y(D)}" font-size="10" fill="#4aa3df">glass</text>')
    dim_h(s, X, 0, 300, Y(D) + 26, "300")
    for zn in ZONES:
        dim_h(s, X, zn["x0"], zn["x1"], Y(D) + 50, f'tile {zn["id"]}: {zn["x1"]-zn["x0"]:g} x {D:g} x {FLOOR_T:g}')
    s.append("</svg>")
    return "\n".join(s)


if __name__ == "__main__":
    os.makedirs(OUT_DRAW, exist_ok=True)
    with open(os.path.join(OUT_DRAW, "front_layout.svg"), "w") as f:
        f.write(front_svg())
    with open(os.path.join(OUT_DRAW, "side_section.svg"), "w") as f:
        f.write(side_svg())
    with open(os.path.join(OUT_DRAW, "plan_view.svg"), "w") as f:
        f.write(plan_svg())
    with open(os.path.join(HERE, "layout.json"), "w") as f:
        json.dump(dict(box=BOX, floor_t=FLOOR_T, zones=ZONES, components=C), f, indent=1)
    issues = checks()
    print(f"{len(C)} components written.")
    print("CHECKS:", "OK - all inside box, >= 3 mm glass clearance, all parts <= 180 mm" if not issues else issues)


def envelopes_md():
    rows = ["| ID | Component | Zone | X range | Z range | Y range | W x D x H | Planned STL(s) |",
            "|---|---|---|---|---|---|---|---|"]
    for c in C:
        rows.append(f'| {c["id"]} | {c["name"]} | {c["zone"]} | {c["x0"]:g}-{c["x1"]:g} | {c["z0"]:g}-{c["z1"]:g} | '
                    f'{c["y0"]:g}-{c["y1"]:g} | {c["w"]:g} x {c["d"]:g} x {c["h"]:g} | {c["stl"]} |')
    return "\n".join(rows)


if __name__ == "__main__":
    with open(os.path.join(HERE, "..", "docs", "component_envelopes.md"), "w") as f:
        f.write("# Component envelopes (auto-generated by layout/layout.py - do not edit by hand)\n\n"
                "Origin: inside bottom-left-back corner. X = width (left->right), Y = depth (back wall 0 -> glass 25), "
                "Z = height (floor 0 -> top 200). All mm. Envelopes are bounding boxes incl. leaves/handles.\n\n")
        f.write(envelopes_md() + "\n")
