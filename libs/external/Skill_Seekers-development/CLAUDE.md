# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🎯 Current Status (November 30, 2025)

**Version:** v2.1.1 (Production Ready - GitHub Analysis Enhanced!)
**Active Development:** Flexible, incremental task-based approach

### Recent Updates (November 2025):

**🎉 MAJOR MILESTONE: Published on PyPI! (v2.0.0)**
- **📦 PyPI Publication**: Install with `pip install skill-seekers` - https://pypi.org/project/skill-seekers/
- **🔧 Modern Python Packaging**: pyproject.toml, src/ layout, entry points
- **✅ CI/CD Fixed**: All 5 test matrix jobs passing (Ubuntu + macOS, Python 3.10-3.12)
- **📚 Documentation Complete**: README, CHANGELOG, FUTURE_RELEASES.md all updated
- **🚀 Unified CLI**: Single `skill-seekers` command with Git-style subcommands
- **🧪 Test Coverage**: 427 tests passing (up from 391), 39% coverage
- **🌐 Community**: GitHub Discussion, Release notes, announcements published

**🚀 Unified Multi-Source Scraping (v2.0.0)**
- **NEW**: Combine documentation + GitHub + PDF in one skill
- **NEW**: Automatic conflict detection between docs and code
- **NEW**: Rule-based and AI-powered merging
- **NEW**: 5 example unified configs (React, Django, FastAPI, Godot, FastAPI-test)
- **Status**: ✅ All 22 unified tests passing (18 core + 4 MCP integration)

**✅ Community Response (H1 Group):**
- **Issue #8 Fixed** - Added BULLETPROOF_QUICKSTART.md and TROUBLESHOOTING.md for beginners
- **Issue #7 Fixed** - Fixed all 11 configs (Django, Laravel, Astro, Tailwind) - 100% working
- **Issue #4 Linked** - Connected to roadmap Tasks A2/A3 (knowledge sharing + website)
- **PR #5 Reviewed** - Approved anchor stripping feature (security verified, 32/32 tests pass)
- **MCP Setup Fixed** - Path expansion bug resolved in setup_mcp.sh

**📦 Configs Status:**
- ✅ **24 total configs available** (including unified configs)
- ✅ 5 unified configs added (React, Django, FastAPI, Godot, FastAPI-test)
- ✅ Core selectors tested and validated
- 📝 Single-source configs: ansible-core, astro, claude-code, django, fastapi, godot, godot-large-example, hono, kubernetes, laravel, react, steam-economy-complete, tailwind, vue
- 📝 Multi-source configs: django_unified, fastapi_unified, fastapi_unified_test, godot_unified, react_unified
- 📝 Test/Example configs: godot_github, react_github, python-tutorial-test, example_pdf, test-manual

**📋 Completed (November 29, 2025):**
- **✅ DONE**: PyPI publication complete (v2.0.0)
- **✅ DONE**: CI/CD fixed - all checks passing
- **✅ DONE**: Documentation updated (README, CHANGELOG, FUTURE_RELEASES.md)
- **✅ DONE**: Quality Assurance + Race Condition Fixes (v2.1.0)
- **✅ DONE**: All critical bugs fixed (Issues #190, #192, #193)
- **✅ DONE**: Test suite stabilized (427 tests passing)
- **✅ DONE**: Unified tests fixed (all 22 passing)
- **✅ DONE**: PR #195 merged - Unlimited local repository analysis
- **✅ DONE**: PR #198 merged - Skip llms.txt config option
- **✅ DONE**: Issue #203 - Configurable EXCLUDED_DIRS (19 tests, 2 commits)

**📋 Next Up (Post-v2.1.0):**
- **Priority 1**: Review open PRs (#187, #186)
- **Priority 2**: Issue #202 - Add warning for missing local_repo_path
- **Priority 3**: Task H1.3 - Create example project folder
- **Priority 4**: Task A3.1 - GitHub Pages site (skillseekersweb.com)

**📊 Roadmap Progress:**
- 134 tasks organized into 22 feature groups
- Project board: https://github.com/users/yusufkaraaslan/projects/2
- See [FLEXIBLE_ROADMAP.md](FLEXIBLE_ROADMAP.md) for complete task list

---

## 🔌 MCP Integration Available

**This repository includes a fully tested MCP server with 9 tools:**
- `mcp__skill-seeker__list_configs` - List all available preset configurations
- `mcp__skill-seeker__generate_config` - Generate a new config file for any docs site
- `mcp__skill-seeker__validate_config` - Validate a config file structure
- `mcp__skill-seeker__estimate_pages` - Estimate page count before scraping
- `mcp__skill-seeker__scrape_docs` - Scrape and build a skill
- `mcp__skill-seeker__package_skill` - Package skill into .zip file (with auto-upload)
- `mcp__skill-seeker__upload_skill` - Upload .zip to Claude (NEW)
- `mcp__skill-seeker__split_config` - Split large documentation configs
- `mcp__skill-seeker__generate_router` - Generate router/hub skills

**Setup:** See [docs/MCP_SETUP.md](docs/MCP_SETUP.md) or run `./setup_mcp.sh`

**Status:** ✅ Tested and working in production with Claude Code

## Overview

Skill Seeker automatically converts any documentation website into a Claude AI skill. It scrapes documentation, organizes content, extracts code patterns, and packages everything into an uploadable `.zip` file for Claude.

## Prerequisites

**Python Version:** Python 3.10 or higher (required for MCP integration)

**Installation:**

### Option 1: Install from PyPI (Recommended - Easiest!)
```bash
# Install globally or in virtual environment
pip install skill-seekers

# Use the unified CLI immediately
skill-seekers scrape --config configs/react.json
skill-seekers --help
```

### Option 2: Install from Source (For Development)
```bash
# Clone the repository
git clone https://github.com/yusufkaraaslan/Skill_Seekers.git
cd Skill_Seekers

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux (Windows: venv\Scripts\activate)

# Install in editable mode
pip install -e .

# Or install dependencies manually
pip install -r requirements.txt
```

**Why use a virtual environment?**
- Keeps dependencies isolated from system Python
- Prevents package version conflicts
- Standard Python development practice
- Required for running tests with pytest

**Optional (for API-based enhancement):**
```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
```

## Core Commands

### Quick Start - Use a Preset

```bash
# Single-source scraping (documentation only)
skill-seekers scrape --config configs/godot.json
skill-seekers scrape --config configs/react.json
skill-seekers scrape --config configs/vue.json
skill-seekers scrape --config configs/django.json
skill-seekers scrape --config configs/laravel.json
skill-seekers scrape --config configs/fastapi.json
```

### Unified Multi-Source Scraping (**NEW - v2.0.0**)

```bash
# Combine documentation + GitHub + PDF in one skill
skill-seekers unified --config configs/react_unified.json
skill-seekers unified --config configs/django_unified.json
skill-seekers unified --config configs/fastapi_unified.json
skill-seekers unified --config configs/godot_unified.json

# Override merge mode
skill-seekers unified --config configs/react_unified.json --merge-mode claude-enhanced

# Result: One comprehensive skill with conflict detection
```

**What makes it special:**
- ✅ Detects discrepancies between documentation and code
- ✅ Shows both versions side-by-side with ⚠️ warnings
- ✅ Identifies outdated docs and undocumented features
- ✅ Single source of truth showing intent (docs) AND reality (code)

**See full guide:** [docs/UNIFIED_SCRAPING.md](docs/UNIFIED_SCRAPING.md)

### First-Time User Workflow (Recommended)

```bash
# 1. Install from PyPI (one-time, easiest!)
pip install skill-seekers

# 2. Estimate page count BEFORE scraping (fast, no data download)
skill-seekers estimate configs/godot.json
# Time: ~1-2 minutes, shows estimated total pages and recommended max_pages

# 3. Scrape with local enhancement (uses Claude Code Max, no API key)
skill-seekers scrape --config configs/godot.json --enhance-local
# Time: 20-40 minutes scraping + 60 seconds enhancement

# 4. Package the skill
skill-seekers package output/godot/

# Result: godot.zip ready to upload to Claude
```

### Interactive Mode

```bash
# Step-by-step configuration wizard
skill-seekers scrape --interactive
```

### Quick Mode (Minimal Config)

```bash
# Create skill from any documentation URL
skill-seekers scrape --name react --url https://react.dev/ --description "React framework for UIs"
```

### Skip Scraping (Use Cached Data)

```bash
# Fast rebuild using previously scraped data
skill-seekers scrape --config configs/godot.json --skip-scrape
# Time: 1-3 minutes (instant rebuild)
```

### Async Mode (2-3x Faster Scraping)

```bash
# Enable async mode with 8 workers for best performance
skill-seekers scrape --config configs/react.json --async --workers 8

# Quick mode with async
skill-seekers scrape --name react --url https://react.dev/ --async --workers 8

# Dry run with async to test
skill-seekers scrape --config configs/godot.json --async --workers 4 --dry-run
```

**Recommended Settings:**
- Small docs (~100-500 pages): `--async --workers 4`
- Medium docs (~500-2000 pages): `--async --workers 8`
- Large docs (2000+ pages): `--async --workers 8 --no-rate-limit`

**Performance:**
- Sync: ~18 pages/sec, 120 MB memory
- Async: ~55 pages/sec, 40 MB memory (3x faster!)

**See full guide:** [ASYNC_SUPPORT.md](ASYNC_SUPPORT.md)

### Enhancement Options

**LOCAL Enhancement (Recommended - No API Key Required):**
```bash
# During scraping
skill-seekers scrape --config configs/react.json --enhance-local

# Standalone after scraping
skill-seekers enhance output/react/
```

**API Enhancement (Alternative - Requires API Key):**
```bash
# During scraping
skill-seekers scrape --config configs/react.json --enhance

# Standalone after scraping
skill-seekers-enhance output/react/
skill-seekers-enhance output/react/ --api-key sk-ant-...
```

### Package and Upload the Skill

```bash
# Package skill (opens folder, shows upload instructions)
skill-seekers package output/godot/
# Result: output/godot.zip

# Package and auto-upload (requires ANTHROPIC_API_KEY)
export ANTHROPIC_API_KEY=sk-ant-...
skill-seekers package output/godot/ --upload

# Upload existing .zip
skill-seekers upload output/godot.zip

# Package without opening folder
skill-seekers package output/godot/ --no-open
```

### Force Re-scrape

```bash
# Delete cached data and re-scrape from scratch
rm -rf output/godot_data/
skill-seekers scrape --config configs/godot.json
```

### Estimate Page Count (Before Scraping)

```bash
# Quick estimation - discover up to 100 pages
skill-seekers estimate configs/react.json --max-discovery 100
# Time: ~30-60 seconds

# Full estimation - discover up to 1000 pages (default)
skill-seekers estimate configs/godot.json
# Time: ~1-2 minutes

# Deep estimation - discover up to 2000 pages
skill-seekers estimate configs/vue.json --max-discovery 2000
# Time: ~3-5 minutes

# What it shows:
# - Estimated total pages
# - Recommended max_pages value
# - Estimated scraping time
# - Discovery rate (pages/sec)
```

**Why use estimation:**
- Validates config URL patterns before full scrape
- Helps set optimal `max_pages` value
- Estimates total scraping time
- Fast (only HEAD requests + minimal parsing)
- No data downloaded or stored

## Repository Architecture

### File Structure (v2.0.0 - Modern Python Packaging)

```
Skill_Seekers/
├── pyproject.toml              # Modern Python package configuration (PEP 621)
├── src/                        # Source code (src/ layout best practice)
│   └── skill_seekers/
│       ├── __init__.py
│       ├── cli/                # CLI tools (entry points)
│       │   ├── doc_scraper.py      # Main scraper (~790 lines)
│       │   ├── estimate_pages.py   # Page count estimator
│       │   ├── enhance_skill.py    # AI enhancement (API-based)
│       │   ├── package_skill.py    # Skill packager
│       │   ├── github_scraper.py   # GitHub scraper
│       │   ├── pdf_scraper.py      # PDF scraper
│       │   ├── unified_scraper.py  # Unified multi-source scraper
│       │   ├── merge_sources.py    # Source merger
│       │   └── conflict_detector.py # Conflict detection
│       └── mcp/                # MCP server integration
│           └── server.py
├── tests/                      # Test suite (391 tests passing)
│   ├── test_scraper_features.py
│   ├── test_config_validation.py
│   ├── test_integration.py
│   ├── test_mcp_server.py
│   ├── test_unified.py         # Unified scraping tests (18 tests)
│   ├── test_unified_mcp_integration.py  # (4 tests)
│   └── ...
├── configs/                    # Preset configurations (24 configs)
│   ├── godot.json
│   ├── react.json
│   ├── django_unified.json     # Multi-source configs
│   └── ...
├── docs/                       # Documentation
│   ├── CLAUDE.md               # This file
│   ├── ENHANCEMENT.md          # Enhancement guide
│   ├── UPLOAD_GUIDE.md         # Upload instructions
│   └── UNIFIED_SCRAPING.md     # Unified scraping guide
├── README.md                   # User documentation
├── CHANGELOG.md                # Release history
├── FUTURE_RELEASES.md          # Roadmap
└── output/                     # Generated output (git-ignored)
    ├── {name}_data/            # Scraped raw data (cached)
    │   ├── pages/*.json        # Individual page data
    │   └── summary.json        # Scraping summary
    └── {name}/                 # Built skill directory
        ├── SKILL.md            # Main skill file
        ├── SKILL.md.backup     # Backup (if enhanced)
        ├── references/         # Categorized documentation
        │   ├── index.md
        │   ├── getting_started.md
        │   ├── api.md
        │   └── ...
        ├── scripts/            # Empty (user scripts)
        └── assets/             # Empty (user assets)
```

**Key Changes in v2.0.0:**
- **src/ layout**: Modern Python packaging structure
- **pyproject.toml**: PEP 621 compliant configuration
- **Entry points**: `skill-seekers` CLI with subcommands
- **Published to PyPI**: `pip install skill-seekers`

### Data Flow

1. **Scrape Phase** (`scrape_all()` in src/skill_seekers/cli/doc_scraper.py):
   - Input: Config JSON (name, base_url, selectors, url_patterns, categories)
   - Process: BFS traversal from base_url, respecting include/exclude patterns
   - Output: `output/{name}_data/pages/*.json` + `summary.json`

2. **Build Phase** (`build_skill()` in src/skill_seekers/cli/doc_scraper.py):
   - Input: Scraped JSON data from `output/{name}_data/`
   - Process: Load pages → Smart categorize → Extract patterns → Generate references
   - Output: `output/{name}/SKILL.md` + `output/{name}/references/*.md`

3. **Enhancement Phase** (optional via enhance_skill.py or enhance_skill_local.py):
   - Input: Built skill directory with references
   - Process: Claude analyzes references and rewrites SKILL.md
   - Output: Enhanced SKILL.md with real examples and guidance

4. **Package Phase** (via package_skill.py):
   - Input: Skill directory
   - Process: Zip all files (excluding .backup)
   - Output: `{name}.zip`

5. **Upload Phase** (optional via upload_skill.py):
   - Input: Skill .zip file
   - Process: Upload to Claude AI via API
   - Output: Skill available in Claude

### Configuration File Structure

Config files (`configs/*.json`) define scraping behavior:

```json
{
  "name": "godot",
  "description": "When to use this skill",
  "base_url": "https://docs.godotengine.org/en/stable/",
  "selectors": {
    "main_content": "div[role='main']",
    "title": "title",
    "code_blocks": "pre"
  },
  "url_patterns": {
    "include": [],
    "exclude": ["/search.html", "/_static/"]
  },
  "categories": {
    "getting_started": ["introduction", "getting_started"],
    "scripting": ["scripting", "gdscript"],
    "api": ["api", "reference", "class"]
  },
  "rate_limit": 0.5,
  "max_pages": 500
}
```

**Config Parameters:**
- `name`: Skill identifier (output directory name)
- `description`: When Claude should use this skill
- `base_url`: Starting URL for scraping
- `selectors.main_content`: CSS selector for main content (common: `article`, `main`, `div[role="main"]`)
- `selectors.title`: CSS selector for page title
- `selectors.code_blocks`: CSS selector for code samples
- `url_patterns.include`: Only scrape URLs containing these patterns
- `url_patterns.exclude`: Skip URLs containing these patterns
- `categories`: Keyword mapping for categorization
- `rate_limit`: Delay between requests (seconds)
- `max_pages`: Maximum pages to scrape
- `skip_llms_txt`: Skip llms.txt detection, force HTML scraping (default: false)
- `exclude_dirs_additional`: Add custom directories to default exclusions (for local repo analysis)
- `exclude_dirs`: Replace default directory exclusions entirely (advanced, for local repo analysis)

## Key Features & Implementation

### Auto-Detect Existing Data
Tool checks for `output/{name}_data/` and prompts to reuse, avoiding re-scraping (check_existing_data() in doc_scraper.py:653-660).

### Configurable Directory Exclusions (Local Repository Analysis)

When using `local_repo_path` for unlimited local repository analysis, you can customize which directories to exclude from analysis.

**Smart Defaults:**
Automatically excludes common directories: `venv`, `node_modules`, `__pycache__`, `.git`, `build`, `dist`, `.pytest_cache`, `htmlcov`, `.tox`, `.mypy_cache`, etc.

**Extend Mode** (`exclude_dirs_additional`): Add custom exclusions to defaults
```json
{
  "sources": [{
    "type": "github",
    "local_repo_path": "/path/to/repo",
    "exclude_dirs_additional": ["proprietary", "legacy", "third_party"]
  }]
}
```

**Replace Mode** (`exclude_dirs`): Override defaults entirely (advanced)
```json
{
  "sources": [{
    "type": "github",
    "local_repo_path": "/path/to/repo",
    "exclude_dirs": ["node_modules", ".git", "custom_vendor"]
  }]
}
```

**Use Cases:**
- Monorepos with custom directory structures
- Enterprise projects with non-standard naming
- Including unusual directories (e.g., analyzing venv code)
- Minimal exclusions for small/simple projects

See: `should_exclude_dir()` in github_scraper.py:304-306

### Language Detection
Detects code languages from:
1. CSS class attributes (`language-*`, `lang-*`)
2. Heuristics (keywords like `def`, `const`, `func`, etc.)

See: `detect_language()` in doc_scraper.py:135-165

### Pattern Extraction
Looks for "Example:", "Pattern:", "Usage:" markers in content and extracts following code blocks (up to 5 per page).

See: `extract_patterns()` in doc_scraper.py:167-183

### Smart Categorization
- Scores pages against category keywords (3 points for URL match, 2 for title, 1 for content)
- Threshold of 2+ for categorization
- Auto-infers categories from URL segments if none provided
- Falls back to "other" category

See: `smart_categorize()` and `infer_categories()` in doc_scraper.py:282-351

### Enhanced SKILL.md Generation
Generated with:
- Real code examples from documentation (language-annotated)
- Quick reference patterns extracted from docs
- Common pattern section
- Category file listings

See: `create_enhanced_skill_md()` in doc_scraper.py:426-542

## Common Workflows

### First Time (With Scraping + Enhancement)

```bash
# 1. Scrape + Build + AI Enhancement (LOCAL, no API key)
skill-seekers scrape --config configs/godot.json --enhance-local

# 2. Wait for enhancement terminal to close (~60 seconds)

# 3. Verify quality
cat output/godot/SKILL.md

# 4. Package
skill-seekers package output/godot/

# Result: godot.zip ready for Claude
# Time: 20-40 minutes (scraping) + 60 seconds (enhancement)
```

### Using Cached Data (Fast Iteration)

```bash
# 1. Use existing data + Local Enhancement
skill-seekers scrape --config configs/godot.json --skip-scrape
skill-seekers enhance output/godot/

# 2. Package
skill-seekers package output/godot/

# Time: 1-3 minutes (build) + 60 seconds (enhancement)
```

### Without Enhancement (Basic)

```bash
# 1. Scrape + Build (no enhancement)
skill-seekers scrape --config configs/godot.json

# 2. Package
skill-seekers package output/godot/

# Note: SKILL.md will be basic template - enhancement recommended
# Time: 20-40 minutes
```

### Creating a New Framework Config

**Option 1: Interactive**
```bash
skill-seekers scrape --interactive
# Follow prompts, it creates the config for you
```

**Option 2: Copy and Modify**
```bash
# Copy a preset
cp configs/react.json configs/myframework.json

# Edit it
nano configs/myframework.json

# Test with limited pages first
# Set "max_pages": 20 in config

# Use it
skill-seekers scrape --config configs/myframework.json
```

## Testing & Verification

### Finding the Right CSS Selectors

Before creating a config, test selectors with BeautifulSoup:

```python
from bs4 import BeautifulSoup
import requests

url = "https://docs.example.com/page"
soup = BeautifulSoup(requests.get(url).content, 'html.parser')

# Try different selectors
print(soup.select_one('article'))
print(soup.select_one('main'))
print(soup.select_one('div[role="main"]'))
print(soup.select_one('div.content'))

# Test code block selector
print(soup.select('pre code'))
print(soup.select('pre'))
```

### Verify Output Quality

After building, verify the skill quality:

```bash
# Check SKILL.md has real examples
cat output/godot/SKILL.md

# Check category structure
cat output/godot/references/index.md

# List all reference files
ls output/godot/references/

# Check specific category content
cat output/godot/references/getting_started.md

# Verify code samples have language detection
grep -A 3 "```" output/godot/references/*.md | head -20
```

### Test with Limited Pages

For faster testing, edit config to limit pages:

```json
{
  "max_pages": 20  // Test with just 20 pages
}
```

## Troubleshooting

### No Content Extracted
**Problem:** Pages scraped but content is empty

**Solution:** Check `main_content` selector in config. Try:
- `article`
- `main`
- `div[role="main"]`
- `div.content`

Use the BeautifulSoup testing approach above to find the right selector.

### Poor Categorization
**Problem:** Pages not categorized well

**Solution:** Edit `categories` section in config with better keywords specific to the documentation structure. Check URL patterns in scraped data:

```bash
# See what URLs were scraped
cat output/godot_data/summary.json | grep url | head -20
```

### Data Exists But Won't Use It
**Problem:** Tool won't reuse existing data

**Solution:** Force re-scrape:
```bash
rm -rf output/myframework_data/
skill-seekers scrape --config configs/myframework.json
```

### Rate Limiting Issues
**Problem:** Getting rate limited or blocked by documentation server

**Solution:** Increase `rate_limit` value in config:
```json
{
  "rate_limit": 1.0  // Change from 0.5 to 1.0 seconds
}
```

### Package Path Error
**Problem:** doc_scraper.py shows wrong cli/package_skill.py path

**Expected output:**
```bash
skill-seekers package output/godot/
```

**Not:**
```bash
python3 /mnt/skills/examples/skill-creator/scripts/cli/package_skill.py output/godot/
```

The correct command uses the local `cli/package_skill.py` in the repository root.

## Key Code Locations (v2.0.0)

**Documentation Scraper** (`src/skill_seekers/cli/doc_scraper.py`):
- **URL validation**: `is_valid_url()`
- **Content extraction**: `extract_content()`
- **Language detection**: `detect_language()`
- **Pattern extraction**: `extract_patterns()`
- **Smart categorization**: `smart_categorize()`
- **Category inference**: `infer_categories()`
- **Quick reference generation**: `generate_quick_reference()`
- **SKILL.md generation**: `create_enhanced_skill_md()`
- **Scraping loop**: `scrape_all()`
- **Main workflow**: `main()`

**Other Key Files**:
- **GitHub scraper**: `src/skill_seekers/cli/github_scraper.py`
- **PDF scraper**: `src/skill_seekers/cli/pdf_scraper.py`
- **Unified scraper**: `src/skill_seekers/cli/unified_scraper.py`
- **Conflict detection**: `src/skill_seekers/cli/conflict_detector.py`
- **Source merger**: `src/skill_seekers/cli/merge_sources.py`
- **Package tool**: `src/skill_seekers/cli/package_skill.py`
- **Upload tool**: `src/skill_seekers/cli/upload_skill.py`
- **MCP server**: `src/skill_seekers/mcp/server.py`
- **Entry points**: `pyproject.toml` (project.scripts section)

## Enhancement Details

### LOCAL Enhancement (Recommended)
- Uses your Claude Code Max plan (no API costs)
- Opens new terminal with Claude Code
- Analyzes reference files automatically
- Takes 30-60 seconds
- Quality: 9/10 (comparable to API version)
- Backs up original SKILL.md to SKILL.md.backup

### API Enhancement (Alternative)
- Uses Anthropic API (~$0.15-$0.30 per skill)
- Requires ANTHROPIC_API_KEY
- Same quality as LOCAL
- Faster (no terminal launch)
- Better for automation/CI

**What Enhancement Does:**
1. Reads reference documentation files
2. Analyzes content with Claude
3. Extracts 5-10 best code examples
4. Creates comprehensive quick reference
5. Adds domain-specific key concepts
6. Provides navigation guidance for different skill levels
7. Transforms 75-line templates into 500+ line comprehensive guides

## Performance

| Task | Time | Notes |
|------|------|-------|
| Scraping | 15-45 min | First time only |
| Building | 1-3 min | Fast! |
| Re-building | <1 min | With --skip-scrape |
| Enhancement (LOCAL) | 30-60 sec | Uses Claude Code Max |
| Enhancement (API) | 20-40 sec | Requires API key |
| Packaging | 5-10 sec | Final zip |

## Available Configs (24 Total)

### Single-Source Documentation Configs (14 configs)

**Web Frameworks:**
- ✅ `react.json` - React (article selector, 7,102 chars)
- ✅ `vue.json` - Vue.js (main selector, 1,029 chars)
- ✅ `astro.json` - Astro (article selector, 145 chars)
- ✅ `django.json` - Django (article selector, 6,468 chars)
- ✅ `laravel.json` - Laravel 9.x (#main-content selector, 16,131 chars)
- ✅ `fastapi.json` - FastAPI (article selector, 11,906 chars)
- ✅ `hono.json` - Hono web framework **NEW!**

**DevOps & Automation:**
- ✅ `ansible-core.json` - Ansible Core 2.19 (div[role='main'] selector, ~32K chars)
- ✅ `kubernetes.json` - Kubernetes (main selector, 2,100 chars)

**Game Engines:**
- ✅ `godot.json` - Godot (div[role='main'] selector, 1,688 chars)
- ✅ `godot-large-example.json` - Godot large docs example

**CSS & Utilities:**
- ✅ `tailwind.json` - Tailwind CSS (div.prose selector, 195 chars)

**Gaming:**
- ✅ `steam-economy-complete.json` - Steam Economy (div.documentation_bbcode, 588 chars)

**Development Tools:**
- ✅ `claude-code.json` - Claude Code documentation **NEW!**

### Unified Multi-Source Configs (5 configs - **NEW v2.0!**)
- ✅ `react_unified.json` - React (docs + GitHub + code analysis)
- ✅ `django_unified.json` - Django (docs + GitHub + code analysis)
- ✅ `fastapi_unified.json` - FastAPI (docs + GitHub + code analysis)
- ✅ `fastapi_unified_test.json` - FastAPI test config
- ✅ `godot_unified.json` - Godot (docs + GitHub + code analysis)

### Test/Example Configs (5 configs)
- 📝 `godot_github.json` - GitHub-only scraping example
- 📝 `react_github.json` - GitHub-only scraping example
- 📝 `python-tutorial-test.json` - Python tutorial test
- 📝 `example_pdf.json` - PDF extraction example
- 📝 `test-manual.json` - Manual testing config

**Note:** All configs verified and working! Unified configs fully tested with 22 passing tests.
**Last verified:** November 29, 2025 (Post-v2.1.0 bug fixes)

## Additional Documentation

**User Guides:**
- **[README.md](README.md)** - Complete user documentation
- **[BULLETPROOF_QUICKSTART.md](BULLETPROOF_QUICKSTART.md)** - Complete beginner guide
- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 3 steps
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Comprehensive troubleshooting

**Technical Documentation:**
- **[docs/CLAUDE.md](docs/CLAUDE.md)** - Detailed technical architecture
- **[docs/ENHANCEMENT.md](docs/ENHANCEMENT.md)** - AI enhancement guide
- **[docs/UPLOAD_GUIDE.md](docs/UPLOAD_GUIDE.md)** - How to upload skills to Claude
- **[docs/UNIFIED_SCRAPING.md](docs/UNIFIED_SCRAPING.md)** - Multi-source scraping guide
- **[docs/MCP_SETUP.md](docs/MCP_SETUP.md)** - MCP server setup

**Project Planning:**
- **[CHANGELOG.md](CHANGELOG.md)** - Release history and v2.0.0 details **UPDATED!**
- **[FUTURE_RELEASES.md](FUTURE_RELEASES.md)** - Roadmap for v2.1.0+  **NEW!**
- **[FLEXIBLE_ROADMAP.md](FLEXIBLE_ROADMAP.md)** - Complete task catalog (134 tasks)
- **[NEXT_TASKS.md](NEXT_TASKS.md)** - What to work on next
- **[TODO.md](TODO.md)** - Current focus
- **[STRUCTURE.md](STRUCTURE.md)** - Repository structure

## Notes for Claude Code

**Project Status (v2.0.0):**
- ✅ **Published on PyPI**: Install with `pip install skill-seekers`
- ✅ **Modern Python Packaging**: pyproject.toml, src/ layout, entry points
- ✅ **Unified CLI**: Single `skill-seekers` command with Git-style subcommands
- ✅ **CI/CD Working**: All 5 test matrix jobs passing (Ubuntu + macOS, Python 3.10-3.12)
- ✅ **Test Coverage**: 391 tests passing, 39% coverage
- ✅ **Documentation**: Complete user and technical documentation

**Architecture:**
- **Python-based documentation scraper** with multi-source support
- **Main scraper**: `src/skill_seekers/cli/doc_scraper.py` (~790 lines)
- **Unified scraping**: Combines docs + GitHub + PDF with conflict detection
- **Modern packaging**: PEP 621 compliant with proper dependency management
- **MCP Integration**: 9 tools for Claude Code Max integration

**Development Workflow:**
1. **Install**: `pip install -e .` (editable mode for development)
2. **Run tests**: `pytest tests/` (391 tests)
3. **Build package**: `uv build` or `python -m build`
4. **Publish**: `uv publish` (PyPI)

**Key Points:**
- Output is cached and reusable in `output/` (git-ignored)
- Enhancement is optional but highly recommended
- All 24 configs are working and tested
- CI workflow requires `pip install -e .` to install package before running tests
