// =====================================================================
//  STORE VERSILE - Miniature Room Frame  (Rev B: 300 x 200 x 25 mm box)
//  Parametric part library - OpenSCAD 2021.01+
//
//  Conventions (every module):
//   * Built in its INSTALLED pose: X = width (left->right), Y = depth
//     (0 = back face, +Y = toward the glass/viewer), Z = up.
//   * Local origin = minimum corner of the part's bounding box unless the
//     module comment says otherwise (leaves / horn / legs use a mount point).
//   * Print orientation is applied in parts/*.scad, not here.
//   * Single-colour parts only (A1 Mini without AMS). Two-colour looks are
//     made from separate parts or a filament change at a layer height.
//  All dimensions in millimetres.
// =====================================================================

// ------------------------------------------------------------ globals
NOZZLE     = 0.4;
CLR        = 0.2;     // general sliding / press clearance
PIN_D      = 1.75;    // alignment pins = 1.75 mm filament off-cuts
PIN_HOLE   = 1.95;
FLUTE_P    = 5.2;     // fluted-panel pitch
WALL_T     = 2.4;     // fluted panel thickness (1.2 backer + 1.2 flutes)
BACKER     = 1.2;
FRAME_T    = 2.5;     // photo frame depth
NAME_TEXT  = "Your Name";
NAME_FONT  = "DejaVu Serif:style=Bold Italic";
LOVE_FONT  = "DejaVu Sans:style=Bold";
$fn = 40;

// ------------------------------------------------------------ helpers
// 2D (x,y) profile -> plate standing in the XZ plane, thickness t along +Y
module xz_plate(t) translate([0, t, 0]) rotate([90, 0, 0]) linear_extrude(t) children();
module rrect2d(w, h, r) translate([r, r]) offset(r = r) square([w - 2 * r, h - 2 * r]);
module dot(p, r, fn = 12) translate(p) circle(r, $fn = fn);
module arch2d(w, h) union() { square([w, h - w / 2]); translate([w / 2, h - w / 2]) intersection() { circle(w / 2, $fn = 96); translate([-w, 0]) square(2 * w); } }
// keep only y >= 0 (flat-backed relief parts print on their back, no supports)
module flatback(y = 0) intersection() { children(); translate([-500, y, -500]) cube(1000); }
module above(z = 0) intersection() { children(); translate([-500, -500, z]) cube(1000); }
// rounded box (all edges radius r)
module rbox(s, r) hull() for (x = [r, s[0] - r], y = [r, s[1] - r], z = [r, s[2] - r]) translate([x, y, z]) sphere(r, $fn = 16);
// point on a circular arc of length L that bends b degrees (starts along +Y)
function arcp(L, b, t) = (abs(b) < 0.01) ? [0, L * t]
    : let(R = L / (b * PI / 180)) [R * (1 - cos(b * t)), R * sin(b * t)];

// =====================================================================
//  STRUCTURE
// =====================================================================

// ---- fluted wall panel profile (2D, X width, Y depth)
module flutes2d(w) {
    n = round(w / FLUTE_P);
    bw = w / n - 0.6;                       // bead width, 0.6 groove
    square([w, BACKER]);
    for (i = [0:n - 1]) translate([w / n * (i + 0.5), BACKER]) scale([bw / 2, WALL_T - BACKER]) circle(1, $fn = 32);
}
// lower piece: z 0..29 (stands 1 mm deep in the floor-tile slot), 2 key tabs on top
module wall_panel_lower(w, h = 29) {
    linear_extrude(h) intersection() { flutes2d(w); square([w, WALL_T]); }
    for (x = [w * 0.25, w * 0.75]) translate([x - 1.5, 0.15, h - 0.01]) cube([3, 0.9, 3]);
}
// upper piece: z 0..168, key notches at the bottom, optional shelf-pin holes [[x,z],..]
module wall_panel_upper(w, h = 168, pins = []) difference() {
    linear_extrude(h) intersection() { flutes2d(w); square([w, WALL_T]); }
    for (x = [w * 0.25, w * 0.75]) translate([x - 1.5 - CLR, -0.01, -0.01]) cube([3 + 2 * CLR, 1.25, 3 + CLR]);
    for (p = pins) translate([p[0], -1, p[1]]) rotate([-90, 0, 0]) cylinder(d = PIN_HOLE, h = 5, $fn = 16);
}

// ---- floor tiles (2 mm) : wood-grain sticker on top, panel slot, dovetails
module dovetail2d(c = 0) polygon([[-0.01, -2 - c], [4 + c, -3 - c], [4 + c, 3 + c], [-0.01, 2 + c]]);
module floor_tile(w, d = 25, slot = undef, male_r = false, male_l = false, fem_l = false, fem_r = false) difference() {
    linear_extrude(2) union() {
        square([w, d]);
        if (male_r) translate([w, d / 2]) dovetail2d();
        if (male_l) translate([0, d / 2]) mirror([1, 0]) dovetail2d();
    }
    if (fem_l) translate([0, d / 2, -1]) linear_extrude(4) dovetail2d(0.15);
    if (fem_r) translate([w, d / 2, -1]) linear_extrude(4) mirror([1, 0]) dovetail2d(0.15);
    if (!is_undef(slot)) translate([slot[0] - CLR, -0.01, 1]) cube([slot[1] - slot[0] + 2 * CLR, WALL_T + 0.3, 2]);
}

// ---- floating shelf 55 x 8 x 3 with 2 pin holes in the back face
module floating_shelf(w = 55, d = 8, t = 3) difference() {
    hull() {                                             // flat bottom, rounded front edges (r 0.6)
        cube([w, d - 0.6, t]);
        for (z = [0.6, t - 0.6]) translate([0, d - 0.6, z]) rotate([0, 90, 0]) cylinder(r = 0.6, h = w, $fn = 16);
        translate([0, 0, 0]) cube([w, d - 0.6, 0.01]);
    }
    for (x = [12, w - 12]) translate([x, -0.01, t / 2]) rotate([-90, 0, 0]) cylinder(d = PIN_HOLE, h = 4, $fn = 16);
}

// ---- central arch: 1.0 backer + stepped-round 2.5 x 2 border (open at the floor)
module central_arch(w = 78, h = 176, back = 1.0, b = 2.5, bh = 2.0) {
    xz_plate(back) arch2d(w, h);
    module ring(k) difference() {
        offset(delta = -k) arch2d(w, h);
        offset(delta = -(b - k)) arch2d(w, h);
        translate([b - k, -1]) square([w - 2 * (b - k), b + 1]);
        translate([-1, -10]) square([w + 2, 10]);
    }
    steps = [[0, 0.8], [0.35, 1.4], [0.8, 2.0]];          // [inset, height]
    for (i = [0:2]) translate([0, back - 0.01, 0]) xz_plate(steps[i][1] + 0.01) ring(steps[i][0]);
}

// ---- name plate 20 x 8 (1.0 base + 0.6 raised text: change filament at 1.0 mm)
module name_plate(txt = NAME_TEXT, w = 20, h = 8) {
    xz_plate(1.0) rrect2d(w, h, 1.6);
    translate([0, 0.99, 0]) xz_plate(0.61) translate([w / 2, h / 2])
        resize([w - 3, 0], auto = true) text(txt, size = 4, font = NAME_FONT, halign = "center", valign = "center");
}

// =====================================================================
//  LEFT ZONE
// =====================================================================

// ---- photo frames: slide-in photo from the top (photo W-1.4 x H-0.6 incl. printed white mat)
module photo_frame(W, H, T = FRAME_T, border = 1.2, back = 1.0, slot = 0.5) difference() {
    hull() { cube([W, T - 0.3, H]); translate([0.3, 0, 0.3]) cube([W - 0.6, T, H - 0.6]); }
    translate([border, back + slot - 0.01, border]) hull() {
        cube([W - 2 * border, 0.01, H - 2 * border]);
        translate([-0.3, T - back - slot + 0.01, -0.3]) cube([W - 2 * border + 0.6, 0.01, H - 2 * border + 0.6]);
    }
    translate([0.6, back, 0.6]) cube([W - 1.2, slot, H]);
}
module photo_frame_small_p() photo_frame(24, 27);
module photo_frame_small_l() photo_frame(27, 24);
module photo_frame_large_p() photo_frame(30, 39);

// ---- LOVE: stacked "LO" / "VE", 21 x 4 x 18
module love_letters(w = 21, h = 18, d = 4) {
    rh = h / 2 + 0.15;
    for (r = [[ "VE", 0], ["LO", h / 2 - 0.15]]) translate([0, 0, r[1]]) xz_plate(d)
        resize([w, rh]) text(r[0], size = 10, font = LOVE_FONT, spacing = 0.92);
    translate([w * 0.2, 0, 1]) cube([w * 0.6, 1.0, h - 2]);   // hidden back bar ties letters together
}

// ---- TV console body 102 x 10 x 24 (black). Upper: 3 open bays. Lower: recess for drawer plate.
CON = [102, 10, 24];
CON_LEGS = [[9, 2.5], [9, 7.5], [93, 2.5], [93, 7.5]];
module tv_console_body() difference() {
    xz_plate(CON[1]) rrect2d(CON[0], CON[2], 5);
    bw = (CON[0] - 5 - 3) / 3;
    for (i = [0:2]) translate([2.5 + i * (bw + 1.5), 2, 0]) xz_plate(CON[1]) translate([0, 12.5]) rrect2d(bw, 9.5, 1.2);
    translate([0, CON[1] - 0.8, 0]) xz_plate(1) translate([2.5, 1.5]) rrect2d(CON[0] - 5, 9.5, 1.5);
    for (p = CON_LEGS) translate([p[0] - 0.85, p[1] - 0.85, -0.01]) cube([1.7, 1.7, 3]);
}
// white drawer-front plate (0.8) with two separation grooves
module tv_console_drawers() difference() {
    xz_plate(0.8) offset(delta = -0.15) translate([2.5, 1.5]) rrect2d(CON[0] - 5, 9.5, 1.5);
    for (i = [1, 2]) translate([2.5 + (CON[0] - 5) * i / 3 - 0.3, 0.45, 0]) cube([0.6, 1, 20]);
    for (i = [0:2]) translate([2.5 + (CON[0] - 5) * (i + 0.5) / 3 - 4, 0.5, 9.0]) cube([8, 1, 0.6]);   // finger-pull line
}
// tapered splayed leg; mount point = top centre (0,0,0), foot at z=-9, splays toward -X
module tv_console_leg(l = 9, a = 12) {
    hull() {
        translate([-1.1, -1.1, -0.01]) cube([2.2, 2.2, 0.01]);
        translate([-l * tan(a) - 0.75, -0.75, -l]) cube([1.5, 1.5, 0.01]);
    }
    translate([-0.7, -0.7, 0]) cube([1.4, 1.4, 2.6]);   // peg
}

// ---- gramophone: dark box base 15 x 8 x 13.5 + gold horn (separate)
GR_HOLE = [8.5, 4, 13.5];  GR_ROT = [-15, -35, 0];
module gramophone_base() difference() {
    union() {
        rbox([15, 8, 8.5], 0.6);
        translate([1.5, 0.5, 8.3]) rbox([12, 7, 5.2], 0.6);
        translate([0.8, -0.0, 3.6]) cube([13.4, 8.1, 0.5]);       // trim line
    }
    translate(GR_HOLE) rotate(GR_ROT) translate([0, 0, -3.5]) cylinder(d = 1.75, h = 5, $fn = 16);
    translate([2, 7.6, 1.5]) cube([11, 1, 1.2]);                   // drawer slot detail
}
// horn: mount point at the neck (0,0,0), bell along +Z; peg below
module gramophone_horn(L = 11, R = 5.5, wall = 0.8) {
    function r(z) = 0.85 + (R - 0.85) * pow(z / L, 2.4);
    N = 24;
    outer = [for (i = [0:N]) [r(L * i / N), L * i / N]];
    zi = L * 0.35;
    inner = [for (i = [N:-1:0]) let(z = zi + (L - zi) * i / N) [max(0.3, r(z) - wall), z]];
    scale([1, 0.72, 1]) rotate_extrude($fn = 48) polygon(concat([[0, 0]], outer, inner, [[0, zi]]));
    translate([0, 0, -3]) cylinder(d = 1.5, h = 3.2, $fn = 16);
}

// ---- books: spine faces the viewer (+Y), pages at back/sides
module book(w = 24, d = 8, h = 5.5) {
    c = 0.55;
    for (z = [0, h - c]) translate([0, 0, z]) rbox([w, d, c], 0.2);
    translate([0.45, 0.45, c - 0.01]) cube([w - 0.9, d - 0.9, h - 2 * c + 0.02]);       // page block
    translate([0, d - 0.9, 0]) hull() {                                                 // rounded spine
        cube([w, 0.4, h]);
        translate([0, 0.5, 0.6]) cube([w, 0.4, h - 1.2]);
    }
}
module book_01() book(24, 8, 5.5);
module book_02() book(22.5, 7.5, 5.5);
module book_03() book(23.5, 8, 5.5);

// =====================================================================
//  PLANTS  (pots: white, upright prints;  leaves: green, flat prints)
// =====================================================================
TAB_W = 4;  LEAF_T = 1.0;  TAB_D = 5;
module pot_slot(cx, cy, top, tw = TAB_W, t = LEAF_T) translate([cx - tw / 2 - CLR, cy - t / 2 - CLR, top - TAB_D - 0.2]) cube([tw + 2 * CLR, t + 2 * CLR, TAB_D + 1]);

// ---- textured vessel: one closed polyhedron (watertight by construction)
//  shape = 1: egg/barrel (pot 01), 2: straight with slight taper, tex = 1 vertical ribs,
//  2 diamond knurl, 3 swirl.  Smooth band of `band` mm at the top.
function _prof(shape, t) = shape == 1 ? (t < 0.655 ? 0.8 + 0.2 * t / 0.655 : 1 - 0.16 * (t - 0.655) / 0.345)
                                      : 0.93 + 0.07 * t;
function _tex(tex, a, z, h, n) =
    tex == 1 ? pow(max(0, cos(n * a)), 6) :
    tex == 2 ? max(pow(max(0, cos(n * (a + 70 * z / h))), 6), pow(max(0, cos(n * (a - 70 * z / h))), 6)) :
               pow(max(0, cos(n * (a + 55 * z / h))), 4);
module textured_vessel(w, d, h, shape, tex, n, g, band = 1.0, N = 144, M = 48) {
    pts = concat(
        [for (j = [0:M], i = [0:N - 1]) let(z = h * j / M, a = 360 * i / N,
            k = _prof(shape, z / h) * (1 - (z > h - band ? 0 : 2 * g / w * _tex(tex, a, z, h, n))))
            [w / 2 * k * cos(a), d / 2 * k * sin(a), z]],
        [[0, 0, 0], [0, 0, h]]);
    B = (M + 1) * N;
    faces = concat(
        [for (j = [0:M - 1], i = [0:N - 1]) let(i2 = (i + 1) % N) [j * N + i, (j + 1) * N + i, (j + 1) * N + i2, j * N + i2]],
        [for (i = [0:N - 1]) [B, i, (i + 1) % N]],
        [for (i = [0:N - 1]) [B + 1, M * N + (i + 1) % N, M * N + i]]);
    polyhedron(pts, faces, convexity = 6);
}
// Pot 01: tall ribbed egg vase 15 x 10 x 29 (floor ferns), two slots (main fan + side fan)
module plant_pot_01(w = 15, d = 10, h = 29) difference() {
    translate([w / 2, d / 2, 0]) textured_vessel(w, d, h, 1, 1, 16, 0.45, 0);
    pot_slot(w / 2, d / 2 + 1.8, h);     // front fan (01A)
    pot_slot(w / 2, d / 2 - 1.8, h);     // rear fan  (01B)
}
// Pot 02: rectangular planter 24 x 7 x 12 with two band grooves
module plant_pot_02(w = 24, d = 7, h = 12) difference() {
    translate([w / 2, d / 2, 0]) linear_extrude(h, scale = 1) offset(r = 1.4) square([w - 2.8, d - 2.8], center = true);
    for (z = [3.5, 8.5]) translate([-1, -1, z]) difference() { cube([w + 2, d + 2, 0.5]); translate([1.35, 1.35, -1]) cube([w - 0.7, d - 0.7, 3]); }
    pot_slot(w / 2, d / 2, h, 8);
}
// Pot 03: diamond-knurled oval pot 15 x 7 x 12
module plant_pot_03(w = 15, d = 7, h = 12) difference() {
    translate([w / 2, d / 2, 0]) textured_vessel(w, d, h, 2, 2, 14, 0.5, 1.2);
    pot_slot(w / 2, d / 2, h, 4, 1.2);
}
// Pot 04: swirl pot 14 x 7 x 10
module plant_pot_04(w = 14, d = 7, h = 10) difference() {
    translate([w / 2, d / 2, 0]) textured_vessel(w, d, h, 2, 3, 12, 0.6, 1.0);
    pot_slot(w / 2, d / 2, h, 3.4);
}

// ---- foliage (2D fans, extruded LEAF_T, standing in XZ). Mount = tab top centre at (0,0,0).
module fern_frond2d(L, ang, bend, rw = 0.55, n = 9, leaf = 2.4) rotate(-ang) {
    for (i = [0:n - 1]) hull() { dot(arcp(L, bend, i / n), rw * (1 - 0.4 * i / n)); dot(arcp(L, bend, (i + 1) / n), rw * (1 - 0.4 * (i + 1) / n)); }
    for (i = [1:n - 1], s = [-1, 1]) let(t = i / n, p = arcp(L, bend, t), ph = bend * t, a = -s * 58,
        T = [sin(ph), cos(ph)], D = [T[0] * cos(a) - T[1] * sin(a), T[0] * sin(a) + T[1] * cos(a)], ll = leaf * (1 - 0.72 * t))
        hull() { dot(p, 0.42); dot(p + D * ll, 0.33); }
}
module spike2d(L, w, ang, bend) rotate(-ang) for (i = [0:3]) hull() {
    dot(arcp(L, bend, i / 4), w * (1 - i / 4) + 0.35);
    dot(arcp(L, bend, (i + 1) / 4), w * (1 - (i + 1) / 4) + 0.35);
}
module tab2d(tw = TAB_W) union() { translate([-tw / 2, -TAB_D]) square([tw, TAB_D + 0.6]); intersection() { circle(tw / 2 + 0.4, $fn = 20); translate([-10, 0]) square(20); } }
module leaf_plate(t = LEAF_T) xz_plate(t) children();
module above0() intersection() { children(); translate([-100, 0]) square(200); }

// palm frond: long narrow leaflets swept toward the tip (areca / parlour-palm look, like the reference)
module palm_frond2d(L, ang, bend, n = 12, leaf = 4.2, rw = 0.5) rotate(-ang) {
    for (i = [0:n - 1]) hull() { dot(arcp(L, bend, i / n), rw * (1 - 0.35 * i / n)); dot(arcp(L, bend, (i + 1) / n), rw * (1 - 0.35 * (i + 1) / n)); }
    for (i = [2:n - 1], s = [-1, 1]) let(t = i / n, p = arcp(L, bend, t), ph = bend * t, a = -s * 34,
        T = [sin(ph), cos(ph)], D = [T[0] * cos(a) - T[1] * sin(a), T[0] * sin(a) + T[1] * cos(a)], ll = leaf * (1 - 0.5 * t))
        hull() { dot(p, 0.38); dot(p + D * ll, 0.3); }
}
// Leaves 01A: front palm fan, about 30 wide x 25 above the vase
module plant_leaves_01a() leaf_plate() union() {
    tab2d();
    n = 7;
    above0() for (i = [0:n - 1]) let(f = (i - (n - 1) / 2) / ((n - 1) / 2))
        palm_frond2d(24 * (1 - 0.25 * pow(abs(f), 1.5)), 50 * f, 24 * f, 12, 4.0);
}
// Leaves 01B: rear palm fan, parallel to 01A in its own slot (fills the gaps, adds depth)
module plant_leaves_01b() leaf_plate() union() {
    tab2d();
    above0() for (f = [-1, -0.55, -0.15, 0.25, 0.7]) palm_frond2d(26 * (1 - 0.2 * abs(f)), 46 * f, 22 * f, 12, 4.0);
}
// Leaves 02: bushy grass/leaf spray for the rectangular pot, 26 x 15
module plant_leaves_02() leaf_plate() union() {
    tab2d(8);
    n = 15;
    above0() for (i = [0:n - 1]) let(f = (i - (n - 1) / 2) / ((n - 1) / 2))
        translate([f * 4, 0]) spike2d(15 * (1 - 0.35 * f * f) + 1.5 * sin(i * 97), 0.55, 62 * f + 4 * sin(i * 53), 26 * f);
}
// Leaves 03: aloe / air-plant succulent, 15 x 14
module plant_leaves_03() leaf_plate(1.2) union() {
    tab2d(4);
    above0() for (f = [-1, -0.66, -0.33, 0, 0.33, 0.66, 1]) spike2d(13.5 * (1 - 0.3 * abs(f)), 1.05, 52 * f, 30 * f);
}
// Leaves 04: small fern 14 x 7.5 (right shelf + console)
module plant_leaves_04() leaf_plate() union() {
    tab2d(3.4);
    above0() for (f = [-1, -0.6, -0.2, 0.2, 0.6, 1]) fern_frond2d(8.5 * (1 - 0.25 * abs(f)), 66 * f, 40 * f, 0.5, 6, 1.7);
}

// =====================================================================
//  CENTRE ZONE
// =====================================================================

// ---- coffee table 60 x 14 x 26 (print upside down; filament change white->wood at 2.6 mm)
module coffee_table(w = 60, d = 14, h = 26, tt = 2.6) {
    translate([0, 0, h - tt]) hull() for (x = [3, w - 3], y = [3, d - 3]) translate([x, y, 0]) {
        translate([0, 0, 0.4]) cylinder(r = 3, h = tt - 0.8);
        cylinder(r = 2.6, h = tt);
    }
    ins = 3.5;
    translate([ins, 2.5, h - tt - 2.2]) difference() {             // apron
        cube([w - 2 * ins, d - 5, 2.21]);
        translate([1.2, 1.2, -1]) cube([w - 2 * ins - 2.4, d - 7.4, 5]);
    }
    for (x = [ins, w - ins - 2.6], y = [2.5, d - 2.5 - 2.6]) hull() {   // tapered legs
        translate([x, y, h - tt - 0.01]) cube([2.6, 2.6, 0.01]);
        translate([x + 0.35, y + 0.35, 0]) cube([1.9, 1.9, 0.01]);
    }
}
// ---- serving tray 38 x 10 x 1.5, rounded left end with engraved ripple arcs
module serving_tray(w = 38, d = 10, t = 1.5) difference() {
    linear_extrude(t) hull() { translate([d / 2, d / 2]) circle(d / 2, $fn = 64); translate([w - 1, 1]) circle(1); translate([w - 1, d - 1]) circle(1); }
    for (r = [1.6, 2.9, 4.2]) translate([d / 2, d / 2, t - 0.4]) linear_extrude(1) difference() {
        circle(r + 0.25, $fn = 64); circle(r - 0.25, $fn = 64); translate([-10, -10]) square([10, 20]);
    }
    for (x = [12, 16]) translate([x, d / 2, t - 0.4]) linear_extrude(1) difference() {
        scale([1, 1.1]) circle(4.2 + 0.25, $fn = 64); scale([1, 1.1]) circle(4.2 - 0.25, $fn = 64); translate([0, -10]) square([10, 20]);
    }
}
// ---- coffee mug: body dia 7.5 x 8, handle to +X. Mount: body centre at (3.75, 3.75)
module mug(r = 3.75, h = 8, wall = 0.9) {
    translate([r, r, 0]) {
        difference() {
            union() { cylinder(r1 = r - 0.25, r2 = r, h = h, $fn = 48); }
            translate([0, 0, 1.2]) cylinder(r = r - wall, h = h, $fn = 48);
        }
        translate([r - 0.35, 0, 4.3]) rotate([90, 0, 0]) rotate([0, 0, -90]) rotate_extrude(angle = 180, $fn = 32) translate([2.1, 0]) circle(0.55, $fn = 16);
    }
}
// ---- rainbow-arch vase 15 x 5 x 14 with stem hole on top
module arch_vase(w = 15, d = 5, h = 14) difference() {
    hull() { xz_plate(d - 0.5) arch2d(w, h); translate([0.4, 0, 0]) xz_plate(d) offset(delta = -0.4) arch2d(w - 0.8, h - 0.4); }
    for (k = [1.6, 3.3, 5.0]) translate([0, d - 0.4, 0]) xz_plate(1) difference() {
        translate([k, -1]) arch2d(w - 2 * k, h - k + 1);
        translate([k + 0.55, -1]) arch2d(w - 2 * k - 1.1, h - k + 1 - 0.55);
    }
    translate([w / 2, d / 2, h - 4]) cylinder(d = 2.2, h = 5, $fn = 16);
}
// ---- silver heart foliage: two textured hearts on a stem. Mount: stem bottom centre (0,1,0)
module heart2d(s) { hull() { dot([-s * 0.27, 0], s * 0.3, 32); dot([0, -s * 0.62], 0.3); } hull() { dot([s * 0.27, 0], s * 0.3, 32); dot([0, -s * 0.62], 0.3); } }
module silver_hearts() {
    translate([0, 0.95, 0]) cylinder(d = 1.9, h = 5, $fn = 16);   // stem / plug (fits 2.2 hole)
    for (s = [-1, 1]) translate([s * 2.6, 0, 9]) rotate([0, s * 22, 0]) {
        xz_plate(1.8) heart2d(6.8);
        intersection() {
            translate([-5, 1.6, -6]) for (x = [-4:1.2:4], z = [-5:1.2:3]) translate([x + 5 + 0.3 * (z % 2), 0, z + 6]) sphere(0.55, $fn = 8);
            xz_plate(3) heart2d(6.8);
        }
    }
    translate([-1.2, 0, 3.8]) cube([2.4, 1.9, 4]);
}
// ---- floor plant mount helpers are in the manifest

// =====================================================================
//  RIGHT ZONE
// =====================================================================

// ---- asymmetric staggered open-cube shelf. rows = [[u_left,u_right,[dividers]],..] bottom->top
//      Local: x = u (unit datum), z = 0 at the bottom of the bottom board. Depth 12, boards 2.5.
SU_ROWS  = [[7, 75, [51]], [3, 69, [27]], [7, 75, [23.5, 52]], [0, 73, [25]], [3, 73, [48]]];   // keep in sync with layout.py (build.py passes the layout values)
SU_PITCH = 32.5;  SU_B = 3.2;  SU_D = 12;
function su_zc(i, b = SU_B) = b / 2 + i * SU_PITCH;          // board centre heights
module display_shelf(rows = SU_ROWS, b = SU_B) xz_plate(SU_D) union() {
    n = len(rows);
    for (i = [0:n - 1]) let(r = rows[i]) for (u = concat([r[0]], r[2], [r[1]]))
        translate([u - b / 2, su_zc(i, b)]) square([b, SU_PITCH]);
    for (k = [0:n]) let(lo = rows[max(0, k - 1)], hi = rows[min(n - 1, k)],
                         a = (k == 0) ? rows[0][0] : (k == n) ? rows[n - 1][0] : min(lo[0], hi[0]),
                         bb = (k == 0) ? rows[0][1] : (k == n) ? rows[n - 1][1] : max(lo[1], hi[1]))
        translate([a - b / 2, su_zc(k, b) - b / 2]) square([bb - a + b, b]);
}

// ---- gold ornament: sphere pot (flat back) + egg cluster; green leaves are a separate fan
module gold_ornament(w = 17) flatback() translate([w / 2, 0, 0]) {
    difference() {
        above(0) translate([0, 0, 4.4]) sphere(5, $fn = 40);
        translate([-6, -6, 8.6]) cube(12);
    }
    for (e = [[-2.3, 1.2, 10.2, -25], [0.8, 1.6, 11.6, 10], [3.0, 1.2, 9.9, 30], [-0.6, 2.3, 9.4, -5]])
        translate([e[0], e[1], e[2]]) rotate([0, e[3], 0]) scale([1.5, 1.5, 2.1]) sphere(1, $fn = 20);
}
// stands behind the eggs; its tab is glued to the flat back of the pot
module gold_ornament_leaves() leaf_plate() union() {
    tab2d(4);
    for (f = [-1, -0.5, 0.5, 1]) spike2d(8.5 * (1 - 0.2 * abs(f)), 0.9, 70 * f, 20 * f);
}
// ---- takeaway cup dia 9 x 22 (plain, raised sleeve band, domed lid)
module takeaway_cup(h = 18.5) translate([4.5, 4.5, 0]) {
    cylinder(r1 = 3.55, r2 = 4.35, h = h, $fn = 48);
    translate([0, 0, 7]) cylinder(r1 = 3.55 + 0.8 * 7 / h + 0.3, r2 = 3.55 + 0.8 * 13 / h + 0.3, h = 6, $fn = 48);
    translate([0, 0, h - 0.01]) cylinder(r = 4.65, h = 1.2, $fn = 48);
    translate([0, 0, h + 1.19]) cylinder(r1 = 4.35, r2 = 3.3, h = 1.8, $fn = 48);
    translate([0, 2.2, h + 2.9]) cylinder(r = 0.8, h = 0.6, $fn = 16);
}
// ---- donut vase OD 12, flat back (prints on its back) + neck with pampas hole
module donut_vase() flatback() translate([6, 1.0, 0]) difference() {
    union() {
        above(0) translate([0, 0, 6 - 0.6]) rotate([90, 0, 0]) rotate_extrude($fn = 48) translate([4, 0]) circle(2, $fn = 24);
        translate([0, 0, 10.6]) cylinder(r = 1.7, h = 3, $fn = 24);
    }
    translate([0, 0, 11]) cylinder(d = 1.7, h = 5, $fn = 12);
}
module pampas_spray() leaf_plate() union() {
    translate([-0.5, -2.4]) square([1.0, 3.0]);   // peg: 2.4 deep into the 2.6 mm neck hole
    for (k = [0:4]) let(a = (k - 2) * 13, L = 10 + 2 * cos(k * 70)) rotate(-a) {
        translate([-0.35, 0]) square([0.7, L * 0.45]);
        for (j = [0:7]) let(t = 0.4 + 0.6 * j / 7) dot([0.35 * sin(j * 131), L * t], 0.95 - 0.35 * j / 7);
    }
}
// ---- sitting bunny 13 x 8 x 24 (flat back)
module bunny() flatback() above(0) {
    translate([6.5, 0, 6.3]) scale([5.9, 6.2, 6.4]) sphere(1, $fn = 40);
    translate([3.6, 0, 4.0]) sphere(4, $fn = 32);
    for (x = [8.2, 10.2]) translate([x, 4.6, 1.2]) scale([1.4, 1.6, 1.2]) sphere(1, $fn = 16);
    difference() {
        union() {
            translate([7.6, 0, 15.2]) scale([4.3, 4.6, 4.2]) sphere(1, $fn = 36);
            translate([9.6, 3.0, 14.4]) sphere(1.9, $fn = 20);
            for (e = [[6.1, -14], [8.9, 12]]) translate([e[0], 0.6, 19.0]) rotate([0, e[1], 0]) translate([0, 0, 2.4]) scale([1.35, 1.25, 3.4]) sphere(1, $fn = 20);
        }
        for (x = [6.6, 9.4]) translate([x, 4.1, 16.2]) sphere(0.45, $fn = 10);                       // eyes
        for (e = [[6.1, -14], [8.9, 12]]) translate([e[0], 1.95, 19.0]) rotate([0, e[1], 0]) translate([0, 0, 2.6]) scale([0.55, 0.4, 2.4]) sphere(1, $fn = 12); // inner ear (paint pink)
    }
    translate([0.9, 1.0, 3.2]) sphere(1.7, $fn = 16);
}
// ---- geometric (low-poly) elephant 16 x 8 x 17, trunk to +X, flat back
module gold_elephant() flatback() above(0) {
    hull() { translate([6, 0, 8.5]) sphere(5, $fn = 8); translate([9, 0, 9]) sphere(4.5, $fn = 8); }
    for (x = [2.3, 5.4, 8.5, 11.0]) hull() { translate([x, 0, 5]) cube([2.6, 5.2, 0.1]); translate([x + 0.2, 0, 0]) cube([2.2, 4.8, 0.1]); }   // legs reach the flat back (print bed)
    translate([12.3, 1, 11.4]) sphere(3.7, $fn = 8);
    hull() { translate([10.6, 3.1, 11.5]) scale([1, 0.35, 1]) sphere(3.2, $fn = 6); translate([9.6, 3.0, 9.4]) scale([1, 0.35, 1]) sphere(2.2, $fn = 6); }
    for (s = [[14.3, 1.6, 10, 1.25], [15.2, 1.7, 6.5, 1.05], [15.0, 1.8, 3.4, 0.95], [15.6, 1.9, 1.4, 0.9]]) translate([s[0], s[1], s[2]]) sphere(s[3], $fn = 6);
    for (i = [0:2]) let(a = [[14.3, 1.6, 10, 1.25], [15.2, 1.7, 6.5, 1.05], [15.0, 1.8, 3.4, 0.95], [15.6, 1.9, 1.4, 0.9]])
        hull() { translate([a[i][0], a[i][1], a[i][2]]) sphere(a[i][3], $fn = 6); translate([a[i + 1][0], a[i + 1][1], a[i + 1][2]]) sphere(a[i + 1][3], $fn = 6); }
    hull() { translate([1.2, 1, 9]) sphere(0.6, $fn = 6); translate([0.3, 1, 6.5]) sphere(0.45, $fn = 6); }
}

// =====================================================================
//  OPTIONAL
// =====================================================================
// LED channel: L-profile 148 long, hides a 5 mm strip behind a 5 mm lip
module led_channel(l = 148) difference() { cube([l, 5, 6]); translate([-1, 1.0, -0.01]) cube([l + 2, 5, 5]); }
