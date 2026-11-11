// Builds the PDFs with headless Chromium (Playwright):
//   templates/Store_Versile_Print_Templates.pdf   (A4 portrait, 1:1)
//   drawings/Store_Versile_Drawings.pdf           (A4 landscape: layout, assembly, joints, every part)
//   docs/Store_Versile_Manufacturing_Guide.pdf    (from docs/MANUFACTURING_GUIDE.html)
// run: node make_docs.js   (from room-frame/cad)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();

  await p.goto('file://' + path.join(ROOT, 'templates/print_templates.html'));
  await p.pdf({ path: path.join(ROOT, 'templates/Store_Versile_Print_Templates.pdf'), preferCSSPageSize: true, printBackground: true });

  const parts = fs.readdirSync(path.join(ROOT, 'drawings/parts')).filter(f => f.endsWith('.svg'));
  const order = JSON.parse(fs.readFileSync(path.join(ROOT, 'docs/print_table.json')));
  parts.sort((a, b) => Object.keys(order).indexOf(a.slice(0, -4)) - Object.keys(order).indexOf(b.slice(0, -4)));
  const sheets = ['front_layout.svg', 'side_section.svg', 'plan_view.svg', 'assembly_positions_1.svg', 'assembly_positions_2.svg',
    'assembly_positions_3.svg', 'joint_details.svg'].map(f => 'drawings/' + f).concat(parts.map(f => 'drawings/parts/' + f));
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>
    @page { size: A4 landscape; margin: 0 } body { margin: 0 }
    .pg { width: 297mm; height: 210mm; page-break-after: always; display: flex; align-items: center; justify-content: center; box-sizing: border-box; padding: 4mm }
    .pg img { max-width: 100%; max-height: 100%; }
  </style></head><body>${sheets.map(s => `<div class="pg"><img src="file://${path.join(ROOT, s)}"></div>`).join('')}</body></html>`;
  const tmp = path.join(ROOT, 'cad/build/drawings_book.html');
  fs.writeFileSync(tmp, html);
  await p.goto('file://' + tmp); await p.waitForTimeout(1500);
  await p.pdf({ path: path.join(ROOT, 'drawings/Store_Versile_Drawings.pdf'), preferCSSPageSize: true, printBackground: true });

  const guide = path.join(ROOT, 'docs/MANUFACTURING_GUIDE.html');
  if (fs.existsSync(guide)) {
    await p.goto('file://' + guide); await p.waitForTimeout(800);
    await p.pdf({ path: path.join(ROOT, 'docs/Store_Versile_Manufacturing_Guide.pdf'), format: 'A4', printBackground: true,
      margin: { top: '14mm', bottom: '14mm', left: '12mm', right: '12mm' } });
  }
  await b.close();
  console.log('PDFs written:', sheets.length, 'drawing sheets');
})();
