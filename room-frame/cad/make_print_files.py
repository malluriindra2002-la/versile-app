#!/usr/bin/env python3
"""
Stage 4-6: print-ready files for the Store Versile room frame.

  python3 make_print_files.py            # all parts
  python3 make_print_files.py Mug Bunny  # only these

For every unique part this
  1. writes cad/parts/<Part>.scad  (editable source, already in print orientation)
  2. exports  stl/<Part>.stl       (binary STL, lying on the bed at z = 0, centred)
  3. checks the mesh: watertight, one body, fits 180 x 180 x 180, overhang area
  4. slices it with PrusaSlicer (same slicing core as Bambu Studio) using an
     A1-Mini-like profile -> filament grams + time estimate, and confirms it slices
  5. writes docs/print_table.json (used by the manufacturing guide)
"""
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import trimesh

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build  # noqa: E402  (parts + instances from the approved layout)

STL_DIR = os.path.join(ROOT, "stl")
PARTS_DIR = os.path.join(HERE, "parts")
TMP = os.path.join(HERE, "build", "print_tmp")
BED = 180.0

# orientation: flat = as installed (bottom on bed); back = lying on its back, front face up;
#              flip = upside down
ROT = {"flat": None, "back": [-90, 0, 0], "flip": [180, 0, 0]}

FIL = {
    "slat": "Peach-beige (e.g. Bambu PLA Matte Desert Tan / Latte Brown, or PLA Sparkle for shimmer)",
    "cream": "Cream (e.g. PLA Matte Ivory White; or the panel colour)",
    "ivory": "Ivory white (e.g. PLA Matte Ivory White)",
    "white": "White (e.g. PLA Basic Jade White / Matte Ivory White)",
    "gold": "Gold silk (e.g. PLA Silk+ Gold)",
    "black": "Black (PLA Basic / Matte Charcoal)",
    "brown": "Dark brown (e.g. PLA Matte Dark Brown)",
    "green": "Leaf green (e.g. PLA Matte Grass Green)",
    "green2": "Light green (e.g. PLA Matte Apple Green)",
    "wood": "Light wood (e.g. PLA Matte Latte Brown or PLA-Wood)",
    "beige": "Beige (e.g. PLA Matte Desert Tan)",
    "silver": "Silver silk (e.g. PLA Silk+ Silver)",
    "pampas": "Bone / ivory white",
    "floor": "Any colour (covered by the wood-grain sticker)",
}

# part: (orientation, layer mm, infill %, perimeters, brim mm, notes)
P = {
    "Floor_Tile_L": ("flat", 0.20, 15, 2, 0, "Wood sticker on top after printing."),
    "Floor_Tile_C": ("flat", 0.20, 15, 2, 0, "Wood sticker on top after printing."),
    "Floor_Tile_R": ("flat", 0.20, 15, 2, 0, "Wood sticker on top after printing."),
    "Left_Wall_Panel_Lower": ("back", 0.16, 15, 2, 0, "Flutes up. Seam is hidden behind the TV console."),
    "Left_Wall_Panel_Upper": ("back", 0.16, 15, 2, 0, "Flutes up. 6 shelf-pin holes."),
    "Right_Wall_Panel_Lower": ("back", 0.16, 15, 2, 0, "Flutes up. Seam is hidden behind the shelving."),
    "Right_Wall_Panel_Upper": ("back", 0.16, 15, 2, 0, "Flutes up."),
    "Floating_Shelf": ("flat", 0.16, 100, 3, 0, "Print 3. Two pin holes in the back edge."),
    "LOVE_Letters": ("back", 0.12, 100, 2, 0, "Letters face up."),
    "Photo_Frame_Small_P": ("back", 0.12, 100, 2, 0, "Gold face up (ironing on). Photo slot opens at the top."),
    "Photo_Frame_Small_L": ("back", 0.12, 100, 2, 0, "Gold face up (ironing on). Photo slot opens at the top."),
    "Photo_Frame_Large_P": ("back", 0.12, 100, 2, 0, "Gold face up (ironing on). Photo slot opens at the top."),
    "TV_Console_Body": ("back", 0.16, 15, 3, 0, "Lying on its back: bays and drawer recess face up."),
    "TV_Console_Drawer_Fronts": ("back", 0.12, 100, 2, 0, "0.8 mm plate, grooves up. Glue into the body recess."),
    "TV_Console_Leg": ("flat", 0.12, 100, 2, 3, "Print 4 together with a 3 mm brim, slow small-layer cooling on."),
    "Gramophone_Base": ("flat", 0.12, 20, 2, 0, "Angled hole for the horn on top."),
    "Gramophone_Horn": ("flip", 0.12, 100, 2, 0, "Bell mouth down on the bed, peg up."),
    "Book_01": ("flat", 0.12, 20, 2, 0, "Spine label = printed paper."),
    "Book_02": ("flat", 0.12, 20, 2, 0, "Spine label = printed paper."),
    "Book_03": ("flat", 0.12, 20, 2, 0, "Spine label = printed paper."),
    "Plant_Pot_01": ("flat", 0.12, 15, 3, 0, "Print 2. Two parallel leaf slots."),
    "Plant_Leaves_01A": ("back", 0.12, 100, 2, 0, "Print 2. Flat, 1.0 mm. Front palm fan."),
    "Plant_Leaves_01B": ("back", 0.12, 100, 2, 0, "Print 2. Flat, 1.0 mm. Rear palm fan."),
    "Plant_Pot_02": ("flat", 0.12, 15, 3, 0, ""),
    "Plant_Leaves_02": ("back", 0.12, 100, 2, 0, "Flat, 1.0 mm."),
    "Plant_Pot_03": ("flat", 0.12, 15, 3, 0, "Diamond-knurl texture."),
    "Plant_Leaves_03": ("back", 0.12, 100, 2, 0, "Flat, 1.2 mm."),
    "Plant_Pot_04": ("flat", 0.12, 15, 3, 0, "Print 2 (shelf unit + TV console)."),
    "Plant_Leaves_04": ("back", 0.12, 100, 2, 0, "Print 2. Flat, 1.0 mm."),
    "Central_Arch": ("back", 0.16, 15, 2, 0, "Border up. 176 mm long: place diagonally if your plate edge is tight; no brim needed."),
    "Name_Plate": ("back", 0.12, 100, 2, 0, "FILAMENT CHANGE at 1.0 mm: white base, then dark text. Edit the NAME line in this file per order."),
    "Coffee_Table": ("flip", 0.12, 20, 2, 0, "Upside down. FILAMENT CHANGE at 2.6 mm: white top first, then wood legs."),
    "Serving_Tray": ("flat", 0.12, 100, 2, 0, "Ripple grooves up."),
    "Mug": ("flat", 0.12, 100, 2, 0, "Print 2 (one is turned so the handles face outward)."),
    "Arch_Vase": ("back", 0.12, 20, 2, 0, "Arch grooves up."),
    "Silver_Heart_Plant": ("back", 0.12, 100, 2, 0, "Bumps up. Push the stem into the arch vase."),
    "Right_Display_Shelf": ("back", 0.20, 15, 3, 0, "Lying on its back: every board is a vertical wall, no supports, no bridges."),
    "Gold_Ornament": ("back", 0.12, 20, 2, 0, "Flat back down."),
    "Gold_Ornament_Leaves": ("back", 0.12, 100, 2, 0, "Glue the tab to the back of the gold pot."),
    "Takeaway_Cup": ("flat", 0.12, 20, 2, 0, "Plain cup, no logo. Optional own-brand sticker on the sleeve."),
    "Donut_Vase": ("back", 0.12, 20, 2, 0, "Flat back down."),
    "Pampas_Spray": ("back", 0.12, 100, 2, 0, "Flat, 1.0 mm. Peg goes into the donut vase neck."),
    "Bunny": ("back", 0.12, 20, 2, 0, "Flat back down. Paint inner ears pink."),
    "Gold_Elephant": ("back", 0.12, 20, 2, 0, "Flat back down."),
}
EXTRA = {"LED_Channel": ("led_channel()", "white", "flip", 0.20, 15, 2, 0, "Optional, print 2. Hides the LED strip under the top front edge.", 2)}


def qty(part):
    return sum(1 for i in build.INST if i[1] == part)


def spec(part):
    if part in EXTRA:
        call, mat, o, lh, inf, per, brim, note, q = EXTRA[part]
        return call, mat, o, lh, inf, per, brim, note, q
    call, mat = build.PARTS[part]
    o, lh, inf, per, brim, note = P[part]
    return call, mat, o, lh, inf, per, brim, note, qty(part)


def write_scad(part):
    call, mat, o, lh, inf, per, brim, note, q = spec(part)
    rot = ROT[o]
    lines = [
        f"// {part}.stl  -  Store Versile room frame (Rev C)",
        f"// Quantity: {q}   Filament: {FIL[mat]}",
        f"// Print: layer {lh} mm, infill {inf}%, {per} walls, brim {brim} mm, NO supports",
        f"// Orientation: {o}  ({'as installed' if o == 'flat' else 'lying on its back, front face up' if o == 'back' else 'upside down'})",
        f"// Notes: {note}" if note else "//",
        "// The library draws parts with their front toward +Y; mirror([0,1,0]) makes the real",
        "// part face the viewer correctly (see build.py). Edit dimensions in versile_parts.scad.",
        "use <../versile_parts.scad>",
        "",
    ]
    if part == "Name_Plate":
        lines += ['NAME = "Your Name";   // <-- type the customer name here for each order', ""]
        call = "name_plate(NAME)"
    lines += [
        (f"rotate({rot}) " if rot else "") + f"mirror([0, 1, 0]) {call};",
        "",
    ]
    path = os.path.join(PARTS_DIR, part + ".scad")
    open(path, "w").write("\n".join(lines))
    return path


def overhang_area(m, angle=45.0):
    """down-facing area steeper than `angle` from vertical, not resting on the bed."""
    n = m.face_normals
    c = m.triangles_center
    a = m.area_faces
    down = n[:, 2] < -np.cos(np.radians(angle))
    off_bed = c[:, 2] > 0.15
    bridge = down & off_bed & (n[:, 2] < -0.98)          # ~flat ceilings (bridges)
    steep = down & off_bed & ~(n[:, 2] < -0.98)
    return float(a[steep].sum()), float(a[bridge].sum())


PRUSA_INI = """
bed_shape = 0x0,180x0,180x180,0x180
max_print_height = 180
nozzle_diameter = 0.4
filament_diameter = 1.75
filament_density = 1.24
filament_cost = 20
temperature = 220
first_layer_temperature = 220
bed_temperature = 65
first_layer_bed_temperature = 65
first_layer_height = 0.2
top_solid_layers = 5
bottom_solid_layers = 4
fill_pattern = gyroid
support_material = 0
skirts = 0
gcode_flavor = marlin2
machine_limits_usage = time_estimate_only
machine_max_acceleration_extruding = 10000
machine_max_acceleration_travel = 10000
machine_max_acceleration_x = 20000
machine_max_acceleration_y = 20000
machine_max_feedrate_x = 500
machine_max_feedrate_y = 500
machine_max_jerk_x = 9
machine_max_jerk_y = 9
perimeter_speed = 300
external_perimeter_speed = 200
small_perimeter_speed = 50
infill_speed = 270
solid_infill_speed = 250
top_solid_infill_speed = 200
gap_fill_speed = 150
bridge_speed = 50
travel_speed = 500
first_layer_speed = 50
cooling = 1
slowdown_below_layer_time = 4
min_print_speed = 20
thin_walls = 1
"""


def slice_part(stl, lh, inf, per, brim):
    os.makedirs(TMP, exist_ok=True)
    ini = os.path.join(TMP, "a1mini.ini")
    if not os.path.exists(ini):
        open(ini, "w").write(PRUSA_INI)
    out = os.path.join(TMP, os.path.basename(stl)[:-4] + ".gcode")
    cmd = ["prusa-slicer", "--export-gcode", "--load", ini, "--layer-height", str(lh),
           "--fill-density", f"{inf}%", "--perimeters", str(per), "--brim-width", str(brim),
           "--center", "90,90", "--output", out, stl]
    if inf >= 100:
        cmd[cmd.index("--fill-density"):cmd.index("--fill-density")] = ["--fill-pattern", "rectilinear"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(out):
        return dict(ok=False, err=(r.stderr or r.stdout).strip().splitlines()[-2:])
    g, t, layers = None, None, 0
    with open(out, errors="ignore") as f:
        for line in f:
            if line.startswith(";LAYER_CHANGE"):
                layers += 1
            elif "filament used [g]" in line:
                g = float(line.split("=")[1])
            elif "estimated printing time (normal mode)" in line:
                t = line.split("=")[1].strip()
    os.remove(out)
    return dict(ok=True, grams=g, time=t, minutes=to_min(t), layers=layers)


def to_min(t):
    if not t:
        return None
    d = {u: int(n) for n, u in re.findall(r"(\d+)([dhms])", t)}
    return round(d.get("d", 0) * 1440 + d.get("h", 0) * 60 + d.get("m", 0) + d.get("s", 0) / 60, 1)


def process(part):
    call, mat, o, lh, inf, per, brim, note, q = spec(part)
    src = write_scad(part)
    raw = os.path.join(TMP, part + "_raw.stl")
    os.makedirs(TMP, exist_ok=True)
    r = subprocess.run(["openscad", "-o", raw, src], capture_output=True, text=True)
    if r.returncode != 0:
        return part, dict(error=r.stderr[-300:])
    m = trimesh.load(raw)
    m.apply_translation([-(m.bounds[0][0] + m.bounds[1][0]) / 2, -(m.bounds[0][1] + m.bounds[1][1]) / 2, -m.bounds[0][2]])
    stl = os.path.join(STL_DIR, part + ".stl")
    m.export(stl)
    os.remove(raw)
    ext = (m.bounds[1] - m.bounds[0]).round(2).tolist()
    steep, bridge = overhang_area(m)
    res = dict(part=part, qty=q, material=mat, filament=FIL[mat], orientation=o, layer=lh, infill=inf, walls=per,
               brim=brim, supports="none", notes=note, size_mm=ext,
               watertight=bool(m.is_watertight), bodies=len(m.split(only_watertight=False)),
               fits_bed=bool(ext[0] <= BED and ext[1] <= BED and ext[2] <= BED),
               volume_mm3=round(float(m.volume), 1), overhang_45_mm2=round(steep, 1), bridge_mm2=round(bridge, 1),
               min_z=round(float(m.bounds[0][2]), 3))
    res["slice"] = slice_part(stl, lh, inf, per, brim)
    return part, res


if __name__ == "__main__":
    os.makedirs(STL_DIR, exist_ok=True)
    os.makedirs(PARTS_DIR, exist_ok=True)
    names = sys.argv[1:] or (list(build.PARTS) + list(EXTRA))
    table_path = os.path.join(ROOT, "docs", "print_table.json")
    table = json.load(open(table_path)) if (sys.argv[1:] and os.path.exists(table_path)) else {}
    with ThreadPoolExecutor(4) as ex:
        for part, res in ex.map(process, names):
            table[part] = res
            if "error" in res:
                print("ERROR", part, res["error"])
                continue
            s = res["slice"]
            flag = "OK " if (res["watertight"] and res["bodies"] == 1 and res["fits_bed"] and s["ok"]) else "!! "
            print(f"{flag}{part:26s} x{res['qty']} {str(res['size_mm']):24s} ovh45={res['overhang_45_mm2']:6.1f} "
                  f"bridge={res['bridge_mm2']:6.1f}  {s.get('grams')} g  {s.get('time')}")
    order = list(build.PARTS) + list(EXTRA)
    json.dump({k: table[k] for k in order if k in table}, open(table_path, "w"), indent=1)
