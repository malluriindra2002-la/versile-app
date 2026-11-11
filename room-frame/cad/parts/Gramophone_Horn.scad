// Gramophone_Horn.stl  -  Store Versile room frame (Rev C)
// Quantity: 1   Filament: Gold silk (e.g. PLA Silk+ Gold)
// Print: layer 0.12 mm, infill 100%, 2 walls, brim 0 mm, NO supports
// Orientation: flip  (upside down)
// Notes: Bell mouth down on the bed, peg up.
// The library draws parts with their front toward +Y; mirror([0,1,0]) makes the real
// part face the viewer correctly (see build.py). Edit dimensions in versile_parts.scad.
use <../versile_parts.scad>

rotate([180, 0, 0]) mirror([0, 1, 0]) gramophone_horn();
