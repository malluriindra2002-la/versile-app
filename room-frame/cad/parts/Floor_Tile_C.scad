// Floor_Tile_C.stl  -  Store Versile room frame (Rev C)
// Quantity: 1   Filament: Any colour (covered by the wood-grain sticker)
// Print: layer 0.2 mm, infill 15%, 2 walls, brim 0 mm, NO supports
// Orientation: flat  (as installed)
// Notes: Wood sticker on top after printing.
// The library draws parts with their front toward +Y; mirror([0,1,0]) makes the real
// part face the viewer correctly (see build.py). Edit dimensions in versile_parts.scad.
use <../versile_parts.scad>

mirror([0, 1, 0]) floor_tile(112, fem_l=true, fem_r=true);
