// Coffee_Table.stl  -  Store Versile room frame (Rev C)
// Quantity: 1   Filament: White (e.g. PLA Basic Jade White / Matte Ivory White)
// Print: layer 0.12 mm, infill 20%, 2 walls, brim 0 mm, NO supports
// Orientation: flip  (upside down)
// Notes: Upside down. FILAMENT CHANGE at 2.6 mm: white top first, then wood legs.
// The library draws parts with their front toward +Y; mirror([0,1,0]) makes the real
// part face the viewer correctly (see build.py). Edit dimensions in versile_parts.scad.
use <../versile_parts.scad>

rotate([180, 0, 0]) mirror([0, 1, 0]) coffee_table();
