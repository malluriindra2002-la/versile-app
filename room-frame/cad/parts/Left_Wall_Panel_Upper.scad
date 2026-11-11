// Left_Wall_Panel_Upper.stl  -  Store Versile room frame (Rev C)
// Quantity: 1   Filament: Peach-beige (e.g. Bambu PLA Matte Desert Tan / Latte Brown, or PLA Sparkle for shimmer)
// Print: layer 0.16 mm, infill 15%, 2 walls, brim 0 mm, NO supports
// Orientation: back  (lying on its back, front face up)
// Notes: Flutes up. 6 shelf-pin holes.
// The library draws parts with their front toward +Y; mirror([0,1,0]) makes the real
// part face the viewer correctly (see build.py). Edit dimensions in versile_parts.scad.
use <../versile_parts.scad>

rotate([-90, 0, 0]) mirror([0, 1, 0]) wall_panel_upper(104, pins=[[13, 133.5], [44, 133.5], [13, 98.5], [44, 98.5], [13, 64.5], [44, 64.5]]);
