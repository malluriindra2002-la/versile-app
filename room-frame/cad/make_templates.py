#!/usr/bin/env python3
"""
Paper print templates at exact 1:1 scale (A4). Writes templates/print_templates.html;
make_docs.js turns it into templates/Store_Versile_Print_Templates.pdf.
Print the PDF at 100 % / "actual size" (never "fit to page").
"""
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "templates")
random.seed(7)

# frame inserts: (W, H) of the frame -> insert W-1.4 x H-0.6, visible window W-2.4 x H-2.4
FRAMES = [("Small portrait 24 x 27", 24, 27, 3, "F1, F2, F3 (shelves)"),
          ("Small landscape 27 x 24", 27, 24, 3, "F7, F8, F9 (shelf unit)"),
          ("Large portrait 30 x 39", 30, 39, 2, "F4, F5 (wall)")]


def insert_svg(W, H, x, y, label, quote=False):
    iw, ih = W - 1.4, H - 0.6
    vx, vy, vw, vh = 0.5, 1.2, W - 2.4, H - 2.4      # visible window inside the insert (from insert top-left)
    m = 1.4                                           # suggested white mat inside the window
    s = [f'<g transform="translate({x},{y})">',
         f'<rect x="0" y="0" width="{iw}" height="{ih}" fill="#fff" stroke="#000" stroke-width="0.15"/>',
         f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" fill="none" stroke="#2a7fd4" stroke-width="0.12" stroke-dasharray="0.8 0.5"/>']
    if quote:
        lines = ["A SMILE", "IS", "ALWAYS", "THE", "BEST", "MAKE UP"]
        for i, t in enumerate(lines):
            s.append(f'<text x="{iw / 2}" y="{vy + 4.2 + i * 3.3}" font-size="2.5" font-weight="700" text-anchor="middle" '
                     f'font-family="DejaVu Sans, Arial, sans-serif">{t}</text>')
    else:
        s.append(f'<rect x="{vx + m}" y="{vy + m}" width="{vw - 2 * m}" height="{vh - 2 * m}" fill="#eadbd2"/>')
        s.append(f'<text x="{iw / 2}" y="{vy + vh / 2}" font-size="1.8" text-anchor="middle" fill="#7a6458" '
                 f'font-family="DejaVu Sans, Arial, sans-serif">photo</text>')
    s.append(f'<text x="0" y="{ih + 3}" font-size="1.9" fill="#444" font-family="DejaVu Sans, Arial, sans-serif">{label}</text>')
    s.append("</g>")
    return "\n".join(s)


def page(svg_body, title, note):
    return f'''<section class="page">
<div class="hd"><b>{title}</b><span>{note}</span></div>
<svg xmlns="http://www.w3.org/2000/svg" width="190mm" height="262mm" viewBox="0 0 190 262">{svg_body}</svg>
<div class="ft">Store Versile room frame Rev C. Print at 100 % (actual size). Check: the 50 mm test bar must measure 50 mm.</div>
</section>'''


def test_bar(x, y):
    return (f'<rect x="{x}" y="{y}" width="50" height="3" fill="none" stroke="#000" stroke-width="0.2"/>'
            f'<text x="{x + 52}" y="{y + 2.6}" font-size="2.6" font-family="DejaVu Sans, Arial, sans-serif">50 mm test bar</text>')


def arch_page():
    w, h = 72.6, 173.3        # inside the raised border (73 x 173.5) minus 0.2 / 0.1 fitting allowance
    r = w / 2
    x0, y0 = (190 - w) / 2, 70
    d = f"M{x0},{y0 + h} L{x0 + w},{y0 + h} L{x0 + w},{y0 + r} A{r},{r} 0 0 0 {x0},{y0 + r} Z"
    np_z0 = 152 - 2 - 0.5       # name plate bottom above the arch print bottom (print starts 0.5 above floor tile)
    body = [test_bar(10, 6),
            '<text x="10" y="18" font-size="3.2" font-weight="700" font-family="DejaVu Sans, Arial, sans-serif">How to use</text>',
            '<text x="10" y="23" font-size="2.7" font-family="DejaVu Sans, Arial, sans-serif">1. Make the artwork 72.6 x 173.3 mm: marble background, gold veins, customer photo (cut-out).</text>',
            '<text x="10" y="27" font-size="2.7" font-family="DejaVu Sans, Arial, sans-serif">2. Print on photo paper, cut on the solid line, glue onto the arch backer inside the raised border.</text>',
            '<text x="10" y="31" font-size="2.7" font-family="DejaVu Sans, Arial, sans-serif">3. The dashed box marks the 3D-printed name plate: keep faces and text out of it.</text>',
            '<text x="10" y="35" font-size="2.7" font-family="DejaVu Sans, Arial, sans-serif">4. Bottom 28 mm are hidden behind the coffee table: keep the customer\'s face above that line.</text>',
            f'<path d="{d}" fill="#f2efed" stroke="#000" stroke-width="0.2"/>',
            f'<rect x="{x0 + w / 2 - 10}" y="{y0 + h - np_z0 - 8}" width="20" height="8" fill="none" stroke="#c0392b" stroke-width="0.2" stroke-dasharray="1 0.6"/>',
            f'<line x1="{x0}" y1="{y0 + h - 28}" x2="{x0 + w}" y2="{y0 + h - 28}" stroke="#2a7fd4" stroke-width="0.15" stroke-dasharray="1 0.6"/>',
            f'<text x="{x0 + w + 2}" y="{y0 + h - 27}" font-size="2.4" fill="#2a7fd4" font-family="DejaVu Sans, Arial, sans-serif">table top line</text>',
            f'<text x="{x0 + w / 2}" y="{y0 + h / 2}" font-size="3" text-anchor="middle" fill="#888" font-family="DejaVu Sans, Arial, sans-serif">ARCH PRINT 72.6 x 173.3</text>']
    return page("\n".join(body), "Arch portrait print (1 per order)", "Cut on the solid line.")


def inserts_page():
    body = [test_bar(10, 6),
            '<text x="10" y="17" font-size="2.7" font-family="DejaVu Sans, Arial, sans-serif">Solid line = cut line (slides into the frame from the top). Blue dashed = visible window. '
            'Put the photo inside the window,</text>',
            '<text x="10" y="21" font-size="2.7" font-family="DejaVu Sans, Arial, sans-serif">leaving a 1.4 mm white mat like the reference. Photo paper max 0.3 mm thick.</text>']
    y = 30
    for name, W, H, n, where in FRAMES:
        body.append(f'<text x="10" y="{y}" font-size="3" font-weight="700" font-family="DejaVu Sans, Arial, sans-serif">{name}: insert {W - 1.4:.1f} x {H - 0.6:.1f} mm, {n} per order ({where})</text>')
        x = 10
        for i in range(n):
            body.append(insert_svg(W, H, x, y + 4, f"insert {i + 1}"))
            x += W + 8
        y += H + 16
    body.append(f'<text x="10" y="{y}" font-size="3" font-weight="700" font-family="DejaVu Sans, Arial, sans-serif">Quote plaque (small portrait frame)</text>')
    body.append(insert_svg(24, 27, 10, y + 4, "quote insert", quote=True))
    return page("\n".join(body), "Photo-frame inserts (8 photos + 1 quote per order)", "")


def floor_page():
    body = [test_bar(10, 6),
            '<text x="10" y="17" font-size="2.7" font-family="DejaVu Sans, Arial, sans-serif">Floor sticker: 300 x 25 mm in two strips (150.5 x 25, 1 mm overlap). Print on sticker paper or glue printed paper.</text>',
            '<text x="10" y="21" font-size="2.7" font-family="DejaVu Sans, Arial, sans-serif">Planks run left-right. Lay strip A from the left wall, B from the right wall, overlap in the middle.</text>']
    for k, y0 in (("A", 30), ("B", 70)):
        body.append(f'<text x="10" y="{y0 - 2}" font-size="2.8" font-weight="700" font-family="DejaVu Sans, Arial, sans-serif">Strip {k}</text>')
        for row in range(5):
            x = -random.uniform(0, 30)
            while x < 150.5:
                L = random.uniform(28, 55)
                b = random.randint(160, 192)
                xx, ww = max(0, x), min(150.5, x + L) - max(0, x)
                if ww > 0:
                    body.append(f'<rect x="{10 + xx:.2f}" y="{y0 + row * 5:.2f}" width="{ww:.2f}" height="4.85" fill="rgb({b + 25},{b - 28},{b - 88})"/>')
                    for g in range(3):
                        gy = y0 + row * 5 + random.uniform(0.6, 4.2)
                        body.append(f'<line x1="{10 + xx:.2f}" y1="{gy:.2f}" x2="{10 + xx + ww:.2f}" y2="{gy + random.uniform(-0.3, 0.3):.2f}" stroke="rgba(90,50,20,0.18)" stroke-width="0.12"/>')
                x += L
        body.append(f'<rect x="10" y="{y0}" width="150.5" height="25" fill="none" stroke="#000" stroke-width="0.15"/>')
    body.append('<text x="10" y="112" font-size="3" font-weight="700" font-family="DejaVu Sans, Arial, sans-serif">Book spine labels (cut, glue to the book front)</text>')
    spines = [("HISTORY PROJECT", 20, "#fff", "#222"), ("DREAM COUNT", 19, "#232428", "#eee"), ("JOURNAL", 20, "#fff", "#222"),
              ("POETRY", 20, "#fff", "#222"), ("MEMORIES", 19, "#232428", "#eee")]
    y = 118
    for t, w, bg, fg in spines:
        body.append(f'<rect x="10" y="{y}" width="{w}" height="4.2" fill="{bg}" stroke="#000" stroke-width="0.1"/>'
                    f'<text x="{10 + w / 2}" y="{y + 2.9}" font-size="2" text-anchor="middle" fill="{fg}" font-family="DejaVu Serif, Georgia, serif" font-weight="700">{t}</text>')
        y += 7
    return page("\n".join(body), "Wood floor sticker + book spine labels", "")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    html = f'''<!doctype html><html><head><meta charset="utf-8"><title>Store Versile print templates</title>
<style>
@page {{ size: A4 portrait; margin: 0 }}
body {{ margin: 0; font-family: "DejaVu Sans", Arial, sans-serif }}
.page {{ width: 210mm; height: 297mm; padding: 10mm; box-sizing: border-box; page-break-after: always; display: flex; flex-direction: column; gap: 2mm }}
.hd {{ display: flex; justify-content: space-between; font-size: 4mm }} .hd span {{ font-size: 3mm; color: #555 }}
.ft {{ font-size: 2.6mm; color: #555 }}
svg {{ display: block }}
</style></head><body>
{arch_page()}
{inserts_page()}
{floor_page()}
</body></html>'''
    open(os.path.join(OUT, "print_templates.html"), "w").write(html)
    print("templates/print_templates.html written")
