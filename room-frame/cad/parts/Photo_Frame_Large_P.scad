// Photo_Frame_Large_P.stl  -  Store Versile room frame (Rev C)
// Quantity: 2   Filament: Gold silk (e.g. PLA Silk+ Gold)
// Print: layer 0.12 mm, infill 100%, 2 walls, brim 0 mm, NO supports
// Orientation: back  (lying on its back, front face up)
// Notes: Gold face up (ironing on). Photo slot opens at the top.
// The library draws parts with their front toward +Y; mirror([0,1,0]) makes the real
// part face the viewer correctly (see build.py). Edit dimensions in versile_parts.scad.
use <../versile_parts.scad>

rotate([-90, 0, 0]) mirror([0, 1, 0]) photo_frame_large_p();
