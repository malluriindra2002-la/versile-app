// LED_Channel.stl  -  Store Versile room frame (Rev C)
// Quantity: 2   Filament: White (e.g. PLA Basic Jade White / Matte Ivory White)
// Print: layer 0.2 mm, infill 15%, 2 walls, brim 0 mm, NO supports
// Orientation: flip  (upside down)
// Notes: Optional, print 2. Hides the LED strip under the top front edge.
// The library draws parts with their front toward +Y; mirror([0,1,0]) makes the real
// part face the viewer correctly (see build.py). Edit dimensions in versile_parts.scad.
use <../versile_parts.scad>

rotate([180, 0, 0]) mirror([0, 1, 0]) led_channel();
