# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Python-based documentation scraper that converts ANY documentation website into a Claude skill. It's a single-file tool (`doc_scraper.py`) that scrapes documentation, extracts code patterns, detects programming languages, and generates structured skill files ready for use with Claude.

## Dependencies

```bash
pip3 install requests beautifulsoup4
```

## Core Commands

### Run with a preset configuration
```bash
python3 cli/doc_scraper.py --config configs/godot.json
python3 cli/doc_scraper.py --config configs/react.json
python3 cli/doc_scraper.py --config configs/vue.json
python3 cli/doc_scraper.py --config configs/django.json
python3 cli/doc_scraper.py --config configs/fastapi.json
```

### Interactive mode (for new frameworks)
```bash
python3 cli/doc_scraper.py --interactive
```

### Quick mode (minimal config)
```bash
python3 cli/doc_scraper.py --name react --url https://react.dev/ --description "React framework"
```

### Skip scraping (use cached data)
```bash
python3 cli/doc_scraper.py --config configs/godot.json --skip-scrape
```

### Resume interrupted scrapes
```bash
# If scrape was interrupted
python3 cli/doc_scraper.py --config configs/godot.json --resume

# Start fresh (clear checkpoint)
python3 cli/doc_scraper.py --config configs/godot.json --fresh
```

### Large documentation (10K-40K+ pages)
```bash
# 1. Estimate page count
python3 cli/estimate_pages.py configs/godot.json

# 2. Split into focused sub-skills
python3 cli/split_config.py configs/godot.json --strategy router

# 3. Generate router skill
python3 cli/generate_router.py configs/godot-*.json

# 4. Package multiple skills
python3 cli/package_multi.py output/godot*/
```

### AI-powered SKILL.md enhancement
```bash
# Option 1: During scraping (API-based, requires ANTHROPIC_API_KEY)
pip3 install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
python3 cli/doc_scraper.py --config configs/react.json --enhance

# Option 2: During scraping (LOCAL, no API key - uses Claude Code Max)
python3 cli/doc_scraper.py --config configs/react.json --enhance-local

# Option 3: Standalone after scraping (API-based)
python3 cli/enhance_skill.py output/react/

# Option 4: Standalone after scraping (LOCAL, no API key)
python3 cli/enhance_skill_local.py output/react/
```

The LOCAL enhancement option (`--enhance-local` or `enhance_skill_local.py`) opens a new terminal with Claude Code, which analyzes reference files and enhances SKILL.md automatically. This requires Claude Code Max plan but no API key.

### MCP Integration (Claude Code)
```bash
# One-time setup
./setup_mcp.sh

# Then in Claude Code, use natural language:
"List all available configs"
"Generate config for Tailwind at https://tailwindcss.com/docs"
"Split configs/godot.json using router strategy"
"Generate router for configs/godot-*.json"
"Package skill at output/react/"
```

9 MCP tools available: list_configs, generate_config, validate_config, estimate_pages, scrape_docs, package_skill, upload_skill, split_config, generate_router

### Test with limited pages (edit config first)
Set `"max_pages": 20` in the config file to test with fewer pages.

## Architecture

### Single-File Design
The entire tool is contained in `doc_scraper.py` (~737 lines). It follows a class-based architecture with a single `DocToSkillConverter` class that handles:
- **Web scraping**: BFS traversal with URL validation
- **Content extraction**: CSS selectors for title, content, code blocks
- **Language detection**: Heuristic-based detection from code samples (Python, JavaScript, GDScript, C++, etc.)
- **Pattern extraction**: Identifies common coding patterns from documentation
- **Categorization**: Smart categorization using URL structure, page titles, and content keywords with scoring
- **Skill generation**: Creates SKILL.md with real code examples and categorized reference files

### Data Flow
1. **Scrape Phase**:
   - Input: Config JSON (name, base_url, selectors, url_patterns, categories, rate_limit, max_pages)
   - Process: BFS traversal starting from base_url, respecting include/exclude patterns
   - Output: `output/{name}_data/pages/*.json` + `summary.json`

2. **Build Phase**:
   - Input: Scraped JSON data from `output/{name}_data/`
   - Process: Load pages → Smart categorize → Extract patterns → Generate references
   - Output: `output/{name}/SKILL.md` + `output/{name}/references/*.md`

### Directory Structure
```
Skill_Seekers/
├── cli/                        # CLI tools
│   ├── doc_scraper.py         # Main scraping & building tool
│   ├── enhance_skill.py       # AI enhancement (API-based)
│   ├── enhance_skill_local.py # AI enhancement (LOCAL, no API)
│   ├── estimate_pages.py      # Page count estimator
│   ├── split_config.py        # Large docs splitter (NEW)
│   ├── generate_router.py     # Router skill generator (NEW)
│   ├── package_skill.py       # Single skill packager
│   └── package_multi.py       # Multi-skill packager (NEW)
├── mcp/                        # MCP server
│   ├── server.py              # 9 MCP tools (includes upload)
│   └── README.md
├── configs/                    # Preset configurations
│   ├── godot.json
│   ├── godot-large-example.json  # Large docs example (NEW)
│   ├── react.json
│   └── ...
├── docs/                       # Documentation
│   ├── CLAUDE.md              # Technical architecture (this file)
│   ├── LARGE_DOCUMENTATION.md # Large docs guide (NEW)
│   ├── ENHANCEMENT.md
│   ├── MCP_SETUP.md
│   └── ...
└── output/                     # Generated output (git-ignored)
    ├── {name}_data/           # Raw scraped data (cached)
    │   ├── pages/             # Individual page JSONs
    │   ├── summary.json       # Scraping summary
    │   └── checkpoint.json    # Resume checkpoint (NEW)
    └── {name}/                # Generated skill
        ├── SKILL.md           # Main skill file with examples
        ├── SKILL.md.backup    # Backup (if enhanced)
        ├── references/        # Categorized documentation
        │   ├── index.md
        │   ├── getting_started.md
        │   ├── api.md
        │   └── ...
        ├── scripts/           # Empty (for user scripts)
        └── assets/            # Empty (for user assets)
```

### Configuration Format
Config files in `configs/*.json` contain:
- `name`: Skill identifier (e.g., "godot", "react")
- `description`: When to use this skill
- `base_url`: Starting URL for scraping
- `selectors`: CSS selectors for content extraction
  - `main_content`: Main documentation content (e.g., "article", "div[role='main']")
  - `title`: Page title selector
  - `code_blocks`: Code sample selector (e.g., "pre code", "pre")
- `url_patterns`: URL filtering
  - `include`: Only scrape URLs containing these patterns
  - `exclude`: Skip URLs containing these patterns
- `categories`: Keyword-based categorization mapping
- `rate_limit`: Delay between requests (seconds)
- `max_pages`: Maximum pages to scrape
- `split_strategy`: (Optional) How to split large docs: "auto", "category", "router", "size"
- `split_config`: (Optional) Split configuration
  - `target_pages_per_skill`: Pages per sub-skill (default: 5000)
  - `create_router`: Create router/hub skill (default: true)
  - `split_by_categories`: Category names to split by
- `checkpoint`: (Optional) Checkpoint/resume configuration
  - `enabled`: Enable checkpointing (default: false)
  - `interval`: Save every N pages (default: 1000)

### Key Features

**Auto-detect existing data**: Tool checks for `output/{name}_data/` and prompts to reuse, avoiding re-scraping.

**Language detection**: Detects code languages from:
1. CSS class attributes (`language-*`, `lang-*`)
2. Heuristics (keywords like `def`, `const`, `func`, etc.)

**Pattern extraction**: Looks for "Example:", "Pattern:", "Usage:" markers in content and extracts following code blocks (up to 5 per page).

**Smart categorization**:
- Scores pages against category keywords (3 points for URL match, 2 for title, 1 for content)
- Threshold of 2+ for categorization
- Auto-infers categories from URL segments if none provided
- Falls back to "other" category

**Enhanced SKILL.md**: Generated with:
- Real code examples from documentation (language-annotated)
- Quick reference patterns extracted from docs
- Common pattern section
- Category file listings

**AI-Powered Enhancement**: Two scripts to dramatically improve SKILL.md quality:
- `enhance_skill.py`: Uses Anthropic API (~$0.15-$0.30 per skill, requires API key)
- `enhance_skill_local.py`: Uses Claude Code Max (free, no API key needed)
- Transforms generic 75-line templates into comprehensive 500+ line guides
- Extracts best examples, explains key concepts, adds navigation guidance
- Success rate: 9/10 quality (based on steam-economy test)

**Large Documentation Support (NEW)**: Handle 10K-40K+ page documentation:
- `split_config.py`: Split large configs into multiple focused sub-skills
- `generate_router.py`: Create intelligent router/hub skills that direct queries
- `package_multi.py`: Package multiple skills at once
- 4 split strategies: auto, category, router, size
- Parallel scraping support for faster processing
- MCP integration for natural language usage

**Checkpoint/Resume (NEW)**: Never lose progress on long scrapes:
- Auto-saves every N pages (configurable, default: 1000)
- Resume with `--resume` flag
- Clear checkpoint with `--fresh` flag
- Saves on interruption (Ctrl+C)

## Key Code Locations

- **URL validation**: `is_valid_url()` doc_scraper.py:47-62
- **Content extraction**: `extract_content()` doc_scraper.py:64-131
- **Language detection**: `detect_language()` doc_scraper.py:133-163
- **Pattern extraction**: `extract_patterns()` doc_scraper.py:165-181
- **Smart categorization**: `smart_categorize()` doc_scraper.py:280-321
- **Category inference**: `infer_categories()` doc_scraper.py:323-349
- **Quick reference generation**: `generate_quick_reference()` doc_scraper.py:351-370
- **SKILL.md generation**: `create_enhanced_skill_md()` doc_scraper.py:424-540
- **Scraping loop**: `scrape_all()` doc_scraper.py:226-249
- **Main workflow**: `main()` doc_scraper.py:661-733

## Workflow Examples

### First time scraping (with scraping)
```bash
# 1. Scrape + Build
python3 cli/doc_scraper.py --config configs/godot.json
# Time: 20-40 minutes

# 2. Package
python3 cli/package_skill.py output/godot/

# Result: godot.zip
```

### Using cached data (fast iteration)
```bash
# 1. Use existing data
python3 cli/doc_scraper.py --config configs/godot.json --skip-scrape
# Time: 1-3 minutes

# 2. Package
python3 cli/package_skill.py output/godot/
```

### Creating a new framework config
```bash
# Option 1: Interactive
python3 cli/doc_scraper.py --interactive

# Option 2: Copy and modify
cp configs/react.json configs/myframework.json
# Edit configs/myframework.json
python3 cli/doc_scraper.py --config configs/myframework.json
```

### Large documentation workflow (40K pages)
```bash
# 1. Estimate page count (fast, 1-2 minutes)
python3 cli/estimate_pages.py configs/godot.json

# 2. Split into focused sub-skills
python3 cli/split_config.py configs/godot.json --strategy router --target-pages 5000

# Creates: godot-scripting.json, godot-2d.json, godot-3d.json, etc.

# 3. Scrape all in parallel (4-8 hours instead of 20-40!)
for config in configs/godot-*.json; do
  python3 cli/doc_scraper.py --config $config &
done
wait

# 4. Generate intelligent router skill
python3 cli/generate_router.py configs/godot-*.json

# 5. Package all skills
python3 cli/package_multi.py output/godot*/

# 6. Upload all .zip files to Claude
# Result: Router automatically directs queries to the right sub-skill!
```

**Time savings:** Parallel scraping reduces 20-40 hours to 4-8 hours

**See full guide:** [Large Documentation Guide](LARGE_DOCUMENTATION.md)

## Testing Selectors

To find the right CSS selectors for a documentation site:

```python
from bs4 import BeautifulSoup
import requests

url = "https://docs.example.com/page"
soup = BeautifulSoup(requests.get(url).content, 'html.parser')

# Try different selectors
print(soup.select_one('article'))
print(soup.select_one('main'))
print(soup.select_one('div[role="main"]'))
```

## Running Tests

**IMPORTANT: You must install the package before running tests**

```bash
# 1. Install package in editable mode (one-time setup)
pip install -e .

# 2. Run all tests
pytest

# 3. Run specific test files
pytest tests/test_config_validation.py
pytest tests/test_github_scraper.py

# 4. Run with verbose output
pytest -v

# 5. Run with coverage report
pytest --cov=src/skill_seekers --cov-report=html
```

**Why install first?**
- Tests import from `skill_seekers.cli` which requires the package to be installed
- Modern Python packaging best practice (PEP 517/518)
- CI/CD automatically installs with `pip install -e .`
- conftest.py will show helpful error if package not installed

**Test Coverage:**
- 391+ tests passing
- 39% code coverage
- All core features tested
- CI/CD tests on Ubuntu + macOS with Python 3.10-3.12

## Troubleshooting

**No content extracted**: Check `main_content` selector. Common values: `article`, `main`, `div[role="main"]`, `div.content`

**Poor categorization**: Edit `categories` section in config with better keywords specific to the documentation structure

**Force re-scrape**: Delete cached data with `rm -rf output/{name}_data/`

**Rate limiting issues**: Increase `rate_limit` value in config (e.g., from 0.5 to 1.0 seconds)

## Output Quality Checks

After building, verify quality:
```bash
cat output/godot/SKILL.md              # Should have real code examples
cat output/godot/references/index.md   # Should show categories
ls output/godot/references/            # Should have category .md files
```

## llms.txt Support

Skill_Seekers automatically detects llms.txt files before HTML scraping:

### Detection Order
1. `{base_url}/llms-full.txt` (complete documentation)
2. `{base_url}/llms.txt` (standard version)
3. `{base_url}/llms-small.txt` (quick reference)

### Benefits
- ⚡ 10x faster (< 5 seconds vs 20-60 seconds)
- ✅ More reliable (maintained by docs authors)
- 🎯 Better quality (pre-formatted for LLMs)
- 🚫 No rate limiting needed

### Example Sites
- Hono: https://hono.dev/llms-full.txt

If no llms.txt is found, automatically falls back to HTML scraping.
