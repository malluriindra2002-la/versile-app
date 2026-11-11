// Right_Display_Shelf.stl  -  Store Versile room frame (Rev C)
// Quantity: 1   Filament: Cream (e.g. PLA Matte Ivory White; or the panel colour)
// Print: layer 0.2 mm, infill 15%, 3 walls, brim 0 mm, NO supports
// Orientation: back  (lying on its back, front face up)
// Notes: Lying on its back: every board is a vertical wall, no supports, no bridges.
// The library draws parts with their front toward +Y; mirror([0,1,0]) makes the real
// part face the viewer correctly (see build.py). Edit dimensions in versile_parts.scad.
use <../versile_parts.scad>

rotate([-90, 0, 0]) mirror([0, 1, 0]) display_shelf(rows=[[7, 75, [51]], [3, 69, [27]], [7, 75, [23.5, 52]], [0, 73, [25]], [3, 73, [48]]], b=3.2);
