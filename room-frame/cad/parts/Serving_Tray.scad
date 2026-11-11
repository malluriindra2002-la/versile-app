// Serving_Tray.stl  -  Store Versile room frame (Rev C)
// Quantity: 1   Filament: Light wood (e.g. PLA Matte Latte Brown or PLA-Wood)
// Print: layer 0.12 mm, infill 100%, 2 walls, brim 0 mm, NO supports
// Orientation: flat  (as installed)
// Notes: Ripple grooves up.
// The library draws parts with their front toward +Y; mirror([0,1,0]) makes the real
// part face the viewer correctly (see build.py). Edit dimensions in versile_parts.scad.
use <../versile_parts.scad>

mirror([0, 1, 0]) serving_tray();
