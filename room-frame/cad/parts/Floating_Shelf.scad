// Floating_Shelf.stl  -  Store Versile room frame (Rev C)
// Quantity: 3   Filament: Ivory white (e.g. PLA Matte Ivory White)
// Print: layer 0.16 mm, infill 100%, 3 walls, brim 0 mm, NO supports
// Orientation: flat  (as installed)
// Notes: Print 3. Two pin holes in the back edge.
// The library draws parts with their front toward +Y; mirror([0,1,0]) makes the real
// part face the viewer correctly (see build.py). Edit dimensions in versile_parts.scad.
use <../versile_parts.scad>

mirror([0, 1, 0]) floating_shelf();
