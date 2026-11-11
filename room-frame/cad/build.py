#!/usr/bin/env python3
"""
Store Versile room frame - assembly manifest + build driver.

  python3 build.py assembly        -> writes assembly.scad (open in OpenSCAD, F5)
  python3 build.py installed [-j4] -> exports every unique part (installed pose)
                                      to build/installed/*.stl + build/scene.json
                                      (used by the 3D preview renderer)

Positions come from ../layout/layout.json (the approved Stage-2 layout) so
the CAD and the drawings can never drift apart.

FRAMES
  layout frame : X right, Y = depth from back wall (0) toward glass (+25), Z up.
                 (used by layout.py / drawings; it is left-handed)
  CAD frame    : X right, Z up, viewer/glass on the -Y side (OpenSCAD "front"
                 view), back wall at y = 0, glass at y = -25. Right-handed.
  Library modules in versile_parts.scad are drawn with their front toward +Y;
  every exported / assembled part is wrapped in mirror([0,1,0]) so the real,
  printable part faces the viewer correctly (text reads the right way).
  layout -> CAD:  t = [x, -y, z],  rotate [rx, ry, rz] -> [-rx, ry, -rz]
"""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
LAYOUT = json.load(open(os.path.join(HERE, "..", "layout", "layout.json")))
E = {c["id"]: c for c in LAYOUT["components"]}
BUILD = os.path.join(HERE, "build")

# ------------------------------------------------------------------ unique parts
# name -> (OpenSCAD call in installed pose, material key)
PARTS = {
    "Floor_Tile_L": ("floor_tile(106, slot=[2,106], male_r=true)", "floor"),
    "Floor_Tile_C": ("floor_tile(112, fem_l=true, fem_r=true)", "floor"),
    "Floor_Tile_R": ("floor_tile(82, slot=[1,79], male_l=true)", "floor"),
    "Left_Wall_Panel_Lower": ("wall_panel_lower(104)", "slat"),
    "Left_Wall_Panel_Upper": (None, "slat"),          # filled below (shelf pin holes)
    "Right_Wall_Panel_Lower": ("wall_panel_lower(78)", "slat"),
    "Right_Wall_Panel_Upper": ("wall_panel_upper(78)", "slat"),
    "Floating_Shelf": ("floating_shelf()", "ivory"),
    "LOVE_Letters": ("love_letters()", "white"),
    "Photo_Frame_Small_P": ("photo_frame_small_p()", "gold"),
    "Photo_Frame_Small_L": ("photo_frame_small_l()", "gold"),
    "Photo_Frame_Large_P": ("photo_frame_large_p()", "gold"),
    "TV_Console_Body": ("tv_console_body()", "black"),
    "TV_Console_Drawer_Fronts": ("tv_console_drawers()", "white"),
    "TV_Console_Leg": ("tv_console_leg()", "white"),
    "Gramophone_Base": ("gramophone_base()", "brown"),
    "Gramophone_Horn": ("gramophone_horn()", "gold"),
    "Book_01": ("book_01()", "white"),
    "Book_02": ("book_02()", "black"),
    "Book_03": ("book_03()", "white"),
    "Plant_Pot_01": ("plant_pot_01()", "white"),
    "Plant_Leaves_01A": ("plant_leaves_01a()", "green"),
    "Plant_Leaves_01B": ("plant_leaves_01b()", "green"),
    "Plant_Pot_02": ("plant_pot_02()", "white"),
    "Plant_Leaves_02": ("plant_leaves_02()", "green"),
    "Plant_Pot_03": ("plant_pot_03()", "white"),
    "Plant_Leaves_03": ("plant_leaves_03()", "green2"),
    "Plant_Pot_04": ("plant_pot_04()", "white"),
    "Plant_Leaves_04": ("plant_leaves_04()", "green"),
    "Central_Arch": ("central_arch()", "white"),
    "Name_Plate": ("name_plate()", "white"),
    "Coffee_Table": ("coffee_table()", "white"),
    "Serving_Tray": ("serving_tray()", "wood"),
    "Mug": ("mug()", "white"),
    "Arch_Vase": ("arch_vase()", "beige"),
    "Silver_Heart_Plant": ("silver_hearts()", "silver"),
    "Right_Display_Shelf": (f"display_shelf(rows={json.dumps(E['SU']['rows'])})", "ivory"),
    "Gold_Ornament": ("gold_ornament()", "gold"),
    "Gold_Ornament_Leaves": ("gold_ornament_leaves()", "green"),
    "Takeaway_Cup": ("takeaway_cup()", "white"),
    "Donut_Vase": ("donut_vase()", "white"),
    "Pampas_Spray": ("pampas_spray()", "pampas"),
    "Bunny": ("bunny()", "white"),
    "Gold_Elephant": ("gold_elephant()", "gold"),
}
# two-colour-by-layer parts (filament change): local axis, split value, material above split
SPLITS = {
    "Coffee_Table": ("z", 26 - 2.6, "wood", "white"),     # below = wood legs/apron, above = white top
    "Name_Plate": ("y", -1.05, "black", "white"),   # CAD frame: raised text is at y < -1.0
}

# shelf-pin holes in the left upper panel (panel local x = world x - 2, z = world z - 30)
pins = []
for sid in ("S1", "S2", "S3"):
    s = E[sid]
    zc = (s["z0"] + s["z1"]) / 2 - 30
    for xw in (s["x0"] + 12, s["x1"] - 12):
        pins.append([round(xw - 2, 2), round(zc, 2)])
PARTS["Left_Wall_Panel_Upper"] = (f"wall_panel_upper(104, pins={json.dumps(pins)})", "slat")

# ------------------------------------------------------------------ instances
INST = []   # (label, part, translate, rotate)


def put(label, part, t, r=(0, 0, 0)):
    """t, r given in the LAYOUT frame; stored in the CAD frame."""
    INST.append((label, part, [round(t[0], 3), round(-t[1], 3) + 0.0, round(t[2], 3)], [-r[0], r[1], -r[2]]))


put("FL1", "Floor_Tile_L", (0, 0, 0))
put("FL2", "Floor_Tile_C", (106, 0, 0))
put("FL3", "Floor_Tile_R", (218, 0, 0))
put("LW_lower", "Left_Wall_Panel_Lower", (2, 0, 1))
put("LW_upper", "Left_Wall_Panel_Upper", (2, 0, 30))
put("RW_lower", "Right_Wall_Panel_Lower", (219, 0, 1))
put("RW_upper", "Right_Wall_Panel_Upper", (219, 0, 30))

for sid in ("S1", "S2", "S3"):
    put(sid, "Floating_Shelf", (E[sid]["x0"], E[sid]["y0"], E[sid]["z0"]))
put("LOVE", "LOVE_Letters", (E["LOVE"]["x0"], E["LOVE"]["y0"], E["LOVE"]["z0"]))
for fid in ("F1", "F2", "F3"):
    put(fid, "Photo_Frame_Small_P", (E[fid]["x0"], E[fid]["y0"], E[fid]["z0"]))
for fid in ("F4", "F5"):
    put(fid, "Photo_Frame_Large_P", (E[fid]["x0"], E[fid]["y0"], E[fid]["z0"]))


def plant(label, pot, leaves, x0, y0, z0, pw, pd, ph, lt=1.0):
    put(label + "_pot", pot, (x0, y0, z0))
    put(label + "_leaves", leaves, (x0 + pw / 2, y0 + pd / 2 - lt / 2, z0 + ph))


plant("PB", "Plant_Pot_02", "Plant_Leaves_02", 33, 3, 130, 24, 7, 12)
plant("PC", "Plant_Pot_03", "Plant_Leaves_03", 8, 3, 96, 15, 7, 12, 1.2)

# TV console
TVX, TVY, TVZ = 3, 2.4, 11
put("TV_body", "TV_Console_Body", (TVX, TVY, TVZ))
put("TV_drawers", "TV_Console_Drawer_Fronts", (TVX, TVY + 10 - 0.8, TVZ))
for (lx, ly) in ((9, 2.5), (9, 7.5)):
    put(f"TV_leg_{lx}_{ly}", "TV_Console_Leg", (TVX + lx, TVY + ly, TVZ))
for (lx, ly) in ((93, 2.5), (93, 7.5)):
    put(f"TV_leg_{lx}_{ly}", "TV_Console_Leg", (TVX + lx, TVY + ly, TVZ), (0, 0, 180))
CT = E["TV"]["z1"]   # console top 35
put("GR_base", "Gramophone_Base", (10, 3, CT))
put("GR_horn", "Gramophone_Horn", (10 + 8.5, 3 + 4, CT + 13.5), (-15, -35, 0))
plant("PD2", "Plant_Pot_04", "Plant_Leaves_04", 44, 4, CT, 14, 7, 10)
put("BK_1", "Book_01", (74, 3.5, CT))
put("BK_2", "Book_02", (74.8, 3.7, CT + 5.5))
put("BK_3", "Book_03", (74.3, 3.5, CT + 11))

# centre
put("AR", "Central_Arch", (E["AR"]["x0"], 0, E["AR"]["z0"]))
put("NP", "Name_Plate", (E["NP"]["x0"], 1.3, E["NP"]["z0"]))
put("CT", "Coffee_Table", (E["CT"]["x0"], E["CT"]["y0"], E["CT"]["z0"]))
TT = E["CT"]["z1"]
put("TR", "Serving_Tray", (135, 7, TT))
put("M1", "Mug", (146.25 + 3.75, 12.25 + 3.75, TT + 1.5), (0, 0, 180))   # handle left
put("M2", "Mug", (151, 8.5, TT + 1.5))                                    # handle right
put("AV", "Arch_Vase", (175, 9, TT))
put("SH", "Silver_Heart_Plant", (182.5, 11.5 - 0.95, TT + 14 - 4))
for pid in ("PA1", "PA2"):
    sx = (E[pid]["x0"] + E[pid]["x1"]) / 2
    put(pid + "_pot", "Plant_Pot_01", (sx - 7.5, 6, 2))
    put(pid + "_leavesA", "Plant_Leaves_01A", (sx, 11 + 1.8 - 0.5, 31))
    put(pid + "_leavesB", "Plant_Leaves_01B", (sx, 11 - 1.8 - 0.5, 31))

# right shelving unit + cell contents
UX0 = 223.0
ROWS = E["SU"]["rows"]
B = 2.5
put("SU", "Right_Display_Shelf", (UX0, 2.4, 2))


def cell(row, idx):
    ul, ur, divs = ROWS[row]
    edges = [ul] + divs + [ur]
    a, b = UX0 + edges[idx] + B / 2, UX0 + edges[idx + 1] - B / 2
    return (a + b) / 2, 2 + B + row * 32.5


cx, zf = cell(4, 0); put("F7", "Photo_Frame_Small_L", (cx - 13.5, 2.6, zf))
cx, zf = cell(4, 1); put("GO", "Gold_Ornament", (cx - 8.5, 5.2, zf)); put("GO_leaves", "Gold_Ornament_Leaves", (cx, 4.2, zf + 8.4))
cx, zf = cell(3, 0); put("CUP", "Takeaway_Cup", (cx - 4.5, 4, zf))
cx, zf = cell(3, 1); put("F8", "Photo_Frame_Small_L", (cx - 13.5, 2.6, zf))
cx, zf = cell(2, 0); put("DV", "Donut_Vase", (cx - 6, 5, zf)); put("DV_pampas", "Pampas_Spray", (cx, 5.5, zf + 13.6))
cx, zf = cell(2, 1); put("PQ", "Photo_Frame_Small_P", (cx - 12, 2.6, zf))
cx, zf = cell(2, 2); plant("PD", "Plant_Pot_04", "Plant_Leaves_04", cx - 7, 4, zf, 14, 7, 10)
cx, zf = cell(1, 0); put("BN", "Bunny", (cx - 6.5, 4, zf))
cx, zf = cell(1, 1); put("F9", "Photo_Frame_Small_L", (cx - 13.5, 2.6, zf))
cx, zf = cell(0, 0); put("BK2_1", "Book_01", (cx - 12, 3.5, zf)); put("BK2_2", "Book_02", (cx - 11.25, 3.7, zf + 5.5))
cx, zf = cell(0, 1); put("EL", "Gold_Elephant", (cx - 8, 4, zf))

MAT_RGB = {
    "floor": "#b9824c", "slat": "#ecc9a6", "ivory": "#f4e8d8", "white": "#f7f6f2", "gold": "#cfa53a",
    "black": "#232428", "brown": "#4e3426", "green": "#4f8f35", "green2": "#6c9b4a", "wood": "#d2a774",
    "beige": "#e6cf9f", "silver": "#c3c6cc", "pampas": "#eadfc8",
}


def write_assembly():
    lines = ['// AUTO-GENERATED by build.py from layout/layout.json - preview with F5',
             'use <versile_parts.scad>', '']
    for label, part, t, r in INST:
        call, mat = PARTS[part]
        lines.append(f'// {label}: {part}')
        lines.append(f'color("{MAT_RGB[mat]}") translate({t}) rotate({r}) mirror([0,1,0]) {call};')
    # frame box outline (not printed)
    lines.append('%translate([-12,-28,-12]) difference(){cube([324,31,224]); translate([12,-1,12]) cube([300,29,200]);}')
    open(os.path.join(HERE, "assembly.scad"), "w").write("\n".join(lines) + "\n")
    print(f"assembly.scad: {len(INST)} instances of {len(PARTS)} unique parts")


def export_one(name, outdir):
    call = PARTS[name][0]
    src = os.path.join(BUILD, "tmp", name + ".scad")
    out = os.path.join(outdir, name + ".stl")
    with open(src, "w") as f:
        f.write(f'use <{os.path.join(HERE, "versile_parts.scad")}>\nmirror([0,1,0]) {call};\n')
    r = subprocess.run(["openscad", "-o", out, src], capture_output=True, text=True)
    ok = r.returncode == 0 and os.path.exists(out)
    return name, ok, (r.stderr.strip().splitlines()[-3:] if not ok else "")


def export_installed(jobs=4, only=None):
    outdir = os.path.join(BUILD, "installed")
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(os.path.join(BUILD, "tmp"), exist_ok=True)
    names = [n for n in PARTS if (not only or n in only)]
    with ThreadPoolExecutor(jobs) as ex:
        for name, ok, err in ex.map(lambda n: export_one(n, outdir), names):
            print(("OK   " if ok else "FAIL ") + name, err if err else "")
    scene = dict(materials=MAT_RGB, parts={k: v[1] for k, v in PARTS.items()},
                 splits={k: list(v) for k, v in SPLITS.items()},
                 instances=[dict(label=l, part=p, t=t, r=r) for l, p, t, r in INST])
    json.dump(scene, open(os.path.join(BUILD, "scene.json"), "w"), indent=1)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "assembly"
    if cmd == "assembly":
        write_assembly()
    elif cmd == "installed":
        write_assembly()
        export_installed(only=sys.argv[2:] or None)
