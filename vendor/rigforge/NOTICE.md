# RigForge 2D support files

`rigforge.html` (the owner's GPT-made 2D rig / animation tool, added 2026-11-28) used two CDN scripts that the cloud session cannot reach and that a phone may load slowly:

- `tailwind.css` = Tailwind CSS 3.4.17 (MIT, `LICENSE_tailwindcss.txt`) compiled once for the classes `rigforge.html` uses (default config). Rebuild after editing the page's classes: `npm i tailwindcss@3.4.17` in a scratch folder, `@tailwind base; @tailwind components; @tailwind utilities;` as input, `content: ['rigforge.html']`, `tailwindcss -i in.css -o vendor/rigforge/tailwind.css --minify`.
- `lucide.min.js` = Lucide icons 0.460.0 UMD build (ISC, `LICENSE_lucide.txt`), from the npm package.
