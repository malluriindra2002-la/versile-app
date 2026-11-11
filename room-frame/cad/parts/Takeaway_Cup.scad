// Takeaway_Cup.stl  -  Store Versile room frame (Rev C)
// Quantity: 1   Filament: White (e.g. PLA Basic Jade White / Matte Ivory White)
// Print: layer 0.12 mm, infill 20%, 2 walls, brim 0 mm, NO supports
// Orientation: flat  (as installed)
// Notes: Plain cup, no logo. Optional own-brand sticker on the sleeve.
// The library draws parts with their front toward +Y; mirror([0,1,0]) makes the real
// part face the viewer correctly (see build.py). Edit dimensions in versile_parts.scad.
use <../versile_parts.scad>

mirror([0, 1, 0]) takeaway_cup();
