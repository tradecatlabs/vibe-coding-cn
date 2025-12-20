# llms.txt Support

## Overview

Skill_Seekers now automatically detects and uses llms.txt files when available, providing 10x faster documentation ingestion.

## What is llms.txt?

The llms.txt convention is a growing standard where documentation sites provide pre-formatted, LLM-ready markdown files:

- `llms-full.txt` - Complete documentation
- `llms.txt` - Standard balanced version
- `llms-small.txt` - Quick reference

## How It Works

1. Before HTML scraping, Skill_Seekers checks for llms.txt files
2. If found, downloads and parses the markdown
3. If not found, falls back to HTML scraping
4. Zero config changes needed

## Configuration

### Automatic Detection (Recommended)

No config changes needed. Just run normally:

```bash
python3 cli/doc_scraper.py --config configs/hono.json
```

### Explicit URL

Optionally specify llms.txt URL:

```json
{
  "name": "hono",
  "llms_txt_url": "https://hono.dev/llms-full.txt",
  "base_url": "https://hono.dev/docs"
}
```

## Performance Comparison

| Method | Time | Requests |
|--------|------|----------|
| HTML Scraping (20 pages) | 20-60s | 20+ |
| llms.txt | < 5s | 1 |

## Supported Sites

Sites known to provide llms.txt:

- Hono: https://hono.dev/llms-full.txt
- (More to be discovered)

## Fallback Behavior

If llms.txt download or parsing fails, automatically falls back to HTML scraping with no user intervention required.
