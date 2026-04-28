# markdown-to-epub Reference Index

This directory keeps long-form notes for the Markdown to EPUB skill. The entrypoint stays in `../SKILL.md`; operational behavior is implemented by `../scripts/build_epub.py`.

## Navigation

- `../SKILL.md`: triggers, boundaries, quick commands, and examples.
- `../scripts/build_epub.py`: source of truth for CLI arguments, asset normalization, Calibre invocation, and EPUB inspection.
- `../agents/openai.yaml`: optional agent metadata.

## Script Contract

- Source Markdown is read-only.
- Build artifacts are written to `--build-dir`.
- Local images are copied into the build workspace and normalized when the file signature proves a better extension.
- Remote `http(s)` and `data:` image references are not downloaded.
- Strict mode fails when local image references cannot be resolved.

## Verification

Run the builder, then inspect:

```bash
unzip -l ./book.epub | rg 'content.opf|toc.ncx|nav.xhtml|\\.(png|jpg|jpeg|webp|gif)$'
```

Also inspect `report.json` in the build directory for `missing_images`, copied assets, and conversion status.
