// Plant_Pot_04.stl  -  Store Versile room frame (Rev C)
// Quantity: 2   Filament: White (e.g. PLA Basic Jade White / Matte Ivory White)
// Print: layer 0.12 mm, infill 15%, 3 walls, brim 0 mm, NO supports
// Orientation: flat  (as installed)
// Notes: Print 2 (shelf unit + TV console).
// The library draws parts with their front toward +Y; mirror([0,1,0]) makes the real
// part face the viewer correctly (see build.py). Edit dimensions in versile_parts.scad.
use <../versile_parts.scad>

mirror([0, 1, 0]) plant_pot_04();
