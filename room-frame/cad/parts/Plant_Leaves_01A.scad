// Plant_Leaves_01A.stl  -  Store Versile room frame (Rev C)
// Quantity: 2   Filament: Leaf green (e.g. PLA Matte Grass Green)
// Print: layer 0.12 mm, infill 100%, 2 walls, brim 0 mm, NO supports
// Orientation: back  (lying on its back, front face up)
// Notes: Print 2. Flat, 1.0 mm. Front palm fan.
// The library draws parts with their front toward +Y; mirror([0,1,0]) makes the real
// part face the viewer correctly (see build.py). Edit dimensions in versile_parts.scad.
use <../versile_parts.scad>

rotate([-90, 0, 0]) mirror([0, 1, 0]) plant_leaves_01a();
