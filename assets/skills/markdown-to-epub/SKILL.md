---
name: markdown-to-epub
description: "Markdown to EPUB build skill: normalize local image references, copy assets, call Calibre ebook-convert, inspect EPUB package structure, and report missing images. Use when turning Markdown manuscripts into reproducible EPUB files."
---

# markdown-to-epub Skill

Use this skill to build a reproducible EPUB from Markdown manuscripts with local image assets, without mutating the source manuscript.

## When to Use This Skill

Trigger when any of these applies:
- Converting one or more Markdown files into an EPUB deliverable.
- Normalizing broken or inconsistent image references before conversion.
- Recovering local assets with unreliable extensions such as `.bin` or `.idunno`.
- Running Calibre `ebook-convert` non-interactively from a repeatable build directory.
- Checking the resulting EPUB archive for OPF, NCX/NAV, and image inclusion.

## Not For / Boundaries

- Not for authoring, rewriting, proofreading, or typesetting the manuscript body.
- Not for downloading remote `http(s)` or `data:` images; remote references are preserved unless the user supplies local replacements.
- Not a substitute for full EPUB QA in dedicated readers; it performs structural and asset checks only.
- Required inputs: source Markdown path, desired EPUB path/title/authors/language, source root, and any fallback asset map.
- If Calibre is unavailable, fail clearly and provide the install/`--ebook-convert-bin` verification path instead of producing a fake EPUB.

## Quick Reference

### Common Patterns

**Build a basic EPUB**
```bash
python3 assets/skills/markdown-to-epub/scripts/build_epub.py \
  --input-md "./book.md" \
  --output-epub "./book.epub" \
  --title "Book Title" \
  --authors "Author Name" \
  --language "zh-CN"
```

**Use a custom source root and build directory**
```bash
python3 assets/skills/markdown-to-epub/scripts/build_epub.py \
  --input-md "./manuscript/book.md" \
  --source-root "./manuscript" \
  --build-dir "./build/book-epub" \
  --output-epub "./dist/book.epub"
```

**Recover missing assets with a fallback map**
```bash
python3 assets/skills/markdown-to-epub/scripts/build_epub.py \
  --input-md "./book.md" \
  --output-epub "./book.epub" \
  --fallback-map "./fallback-map.json"
```

**Allow unresolved local images but report them**
```bash
python3 assets/skills/markdown-to-epub/scripts/build_epub.py \
  --input-md "./book.md" \
  --output-epub "./book.epub" \
  --no-strict-missing
```

**Point to a non-standard Calibre binary**
```bash
python3 assets/skills/markdown-to-epub/scripts/build_epub.py \
  --input-md "./book.md" \
  --ebook-convert-bin "/opt/calibre/ebook-convert"
```

**Inspect the generated package**
```bash
unzip -l ./book.epub | rg 'content.opf|toc.ncx|nav.xhtml|\\.(png|jpg|jpeg|webp|gif)$'
```

## Examples

### Example 1: Clean Manuscript Build

- Input: `book.md` with valid local images and metadata title/author/language.
- Steps:
  1. Run the basic build command.
  2. Inspect `build_epub/report.json`.
  3. Check the EPUB zip listing for OPF and navigation files.
- Expected output / acceptance: `book.epub` exists, `missing_images` is empty, and package structure contains OPF plus NCX or NAV.

### Example 2: Extension Recovery

- Input: Markdown references `images/cover.idunno`, but the file signature is a PNG.
- Steps:
  1. Run the build script in strict mode.
  2. Confirm copied assets in `build_epub/assets/` use normalized extensions.
  3. Rebuild after fixing any missing file mapping.
- Expected output / acceptance: EPUB includes the normalized image and the report records no unresolved local image.

### Example 3: Missing Asset Triage

- Input: manuscript references old file names that no longer exist.
- Steps:
  1. Create a JSON fallback map from missing basenames to replacement basenames.
  2. Re-run with `--fallback-map`.
  3. Keep strict mode enabled so unmapped missing assets fail the build.
- Expected output / acceptance: every missing local image is either resolved by the map or listed in `report.json` for explicit follow-up.

## References

- `references/index.md`: navigation, script contract, and validation notes.
- `scripts/build_epub.py`: executable builder used by this skill.
- `agents/openai.yaml`: agent metadata for this skill package.

## Maintenance

- Sources: local script implementation and EPUB/Calibre behavior observed by the build report.
- Last updated: 2026-04-28
- Known limits: structural checks do not guarantee visual fidelity in every EPUB reader; run reader-specific QA for final publication.
