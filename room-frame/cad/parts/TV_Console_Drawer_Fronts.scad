// TV_Console_Drawer_Fronts.stl  -  Store Versile room frame (Rev C)
// Quantity: 1   Filament: White (e.g. PLA Basic Jade White / Matte Ivory White)
// Print: layer 0.12 mm, infill 100%, 2 walls, brim 0 mm, NO supports
// Orientation: back  (lying on its back, front face up)
// Notes: 0.8 mm plate, grooves up. Glue into the body recess.
// The library draws parts with their front toward +Y; mirror([0,1,0]) makes the real
// part face the viewer correctly (see build.py). Edit dimensions in versile_parts.scad.
use <../versile_parts.scad>

rotate([-90, 0, 0]) mirror([0, 1, 0]) tv_console_drawers();
