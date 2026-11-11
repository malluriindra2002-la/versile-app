// Gold_Ornament_Leaves.stl  -  Store Versile room frame (Rev C)
// Quantity: 1   Filament: Leaf green (e.g. PLA Matte Grass Green)
// Print: layer 0.12 mm, infill 100%, 2 walls, brim 0 mm, NO supports
// Orientation: back  (lying on its back, front face up)
// Notes: Glue the tab to the back of the gold pot.
// The library draws parts with their front toward +Y; mirror([0,1,0]) makes the real
// part face the viewer correctly (see build.py). Edit dimensions in versile_parts.scad.
use <../versile_parts.scad>

rotate([-90, 0, 0]) mirror([0, 1, 0]) gold_ornament_leaves();
