// TV_Console_Body.stl  -  Store Versile room frame (Rev C)
// Quantity: 1   Filament: Black (PLA Basic / Matte Charcoal)
// Print: layer 0.16 mm, infill 15%, 3 walls, brim 0 mm, NO supports
// Orientation: back  (lying on its back, front face up)
// Notes: Lying on its back: bays and drawer recess face up.
// The library draws parts with their front toward +Y; mirror([0,1,0]) makes the real
// part face the viewer correctly (see build.py). Edit dimensions in versile_parts.scad.
use <../versile_parts.scad>

rotate([-90, 0, 0]) mirror([0, 1, 0]) tv_console_body();
