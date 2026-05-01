---
name: snapdom
description: "snapDOM DOM-to-image skill: capture HTML elements as SVG/PNG/JPG/WebP/canvas/blob, preserve styles/fonts/pseudo-elements, use scaling/exclusion/CORS proxy options, and compare screenshot output."
---

# snapdom Skill

Use this skill to capture browser DOM elements into image outputs with snapDOM while preserving styling and controlling export options.

## When to Use This Skill

Trigger when any of these applies:
- Exporting a DOM element to SVG, PNG, JPG, WebP, Canvas, or Blob.
- Capturing styled UI with fonts, pseudo-elements, shadows, transforms, or Shadow DOM.
- Building screenshot/export/download features in web apps.
- Debugging missing assets, CORS-blocked images, scaling, tight bounds, or excluded controls.
- Comparing snapDOM with `html2canvas` or browser screenshot workflows.

## Not For / Boundaries

- Not for full-page browser automation screenshots; use Playwright/Puppeteer when viewport, navigation, or browser state is the core need.
- CORS-blocked resources may require a proxy or same-origin setup; do not assume cross-origin images will embed automatically.
- Do not capture sensitive DOM content unless the user explicitly intends to export it.
- Required inputs: target element selector, desired format, dimensions/scale, asset/CORS constraints, and where the image should be used.
- Verify package/API names against the installed version if build errors indicate version drift.

## Quick Reference

### Common Patterns

**Install**
```bash
npm install @zumer/snapdom
```

**Import from CDN as an ES module**
```html
<script type="module">
  import { snapdom } from "https://unpkg.com/@zumer/snapdom/dist/snapdom.mjs";
</script>
```

**Capture once and export multiple formats**
```javascript
const result = await snapdom(document.querySelector("#target"));
const png = await result.toPng();
const svg = await result.toSvg();
const canvas = await result.toCanvas();
```

**One-step PNG export**
```javascript
const png = await snapdom.toPng(document.querySelector("#target"));
```

**Download an element**
```javascript
await snapdom.download(document.querySelector("#target"), "screenshot.png");
```

**Set scale and dimensions**
```javascript
const png = await snapdom.toPng(element, {
  scale: 2,
  width: 1200,
  height: 630,
});
```

**Exclude UI controls**
```javascript
const png = await snapdom.toPng(element, {
  exclude: ".controls, [data-no-capture]",
});
```

**Use a CORS proxy fallback**
```javascript
const png = await snapdom.toPng(element, {
  useProxy: "https://cors.example.com/?",
});
```

## Examples

### Example 1: Social Card Export

- Input: element `#card`, target size `1200x630`, PNG output.
- Steps:
  1. Ensure fonts and images are loaded.
  2. Capture with explicit `width`, `height`, and `scale`.
  3. Download or upload the resulting PNG.
- Expected output / acceptance: exported image matches the card bounds and excludes editor controls.

### Example 2: SVG Snapshot for Documentation

- Input: styled component preview.
- Steps:
  1. Call `snapdom(element)`.
  2. Export `toSvg()` for scalable documentation output.
  3. Inspect missing fonts/assets if the snapshot differs from the page.
- Expected output / acceptance: SVG preserves visible styles and remains inspectable as a vector artifact.

### Example 3: CORS Asset Triage

- Input: export shows missing remote images.
- Steps:
  1. Confirm whether assets are same-origin and CORS-enabled.
  2. Retry with `useProxy` or replace remote assets with local/same-origin URLs.
  3. Validate final output in the target browser.
- Expected output / acceptance: missing images are attributed to CORS, loading, or selector/sizing issues.

## References

- `references/index.md`: local snapDOM reference navigation.
- `references/other.md`: generated upstream notes and API details.

## Maintenance

- Sources: local `references/` extracted from snapDOM documentation.
- Last updated: 2026-04-28
- Known limits: screenshot fidelity depends on browser support, loaded assets, CORS, fonts, and installed snapDOM version.
