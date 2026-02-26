# Complete Usage Guide for Skill Seeker

Comprehensive reference for all commands, options, and workflows.

## Table of Contents

- [Quick Reference](#quick-reference)
- [Main Tool: doc_scraper.py](#main-tool-doc_scraperpy)
- [Estimator: estimate_pages.py](#estimator-estimate_pagespy)
- [Enhancement Tools](#enhancement-tools)
- [Packaging Tool](#packaging-tool)
- [Testing Tools](#testing-tools)
- [Available Configs](#available-configs)
- [Common Workflows](#common-workflows)
- [Troubleshooting](#troubleshooting)

---

## Quick Reference

```bash
# 1. Estimate pages (fast, 1-2 min)
python3 cli/estimate_pages.py configs/react.json

# 2. Scrape documentation (20-40 min)
python3 cli/doc_scraper.py --config configs/react.json

# 3. Enhance with Claude Code (60 sec)
python3 cli/enhance_skill_local.py output/react/

# 4. Package to .zip (instant)
python3 cli/package_skill.py output/react/

# 5. Test everything (1 sec)
python3 cli/run_tests.py
```

---

## Main Tool: doc_scraper.py

### Full Help

```
usage: doc_scraper.py [-h] [--interactive] [--config CONFIG] [--name NAME]
                      [--url URL] [--description DESCRIPTION] [--skip-scrape]
                      [--dry-run] [--enhance] [--enhance-local]
                      [--api-key API_KEY]

Convert documentation websites to Claude skills

options:
  -h, --help            Show this help message and exit
  --interactive, -i     Interactive configuration mode
  --config, -c CONFIG   Load configuration from file (e.g., configs/godot.json)
  --name NAME           Skill name
  --url URL             Base documentation URL
  --description, -d DESCRIPTION
                        Skill description
  --skip-scrape         Skip scraping, use existing data
  --dry-run             Preview what will be scraped without actually scraping
  --enhance             Enhance SKILL.md using Claude API after building
                        (requires API key)
  --enhance-local       Enhance SKILL.md using Claude Code in new terminal
                        (no API key needed)
  --api-key API_KEY     Anthropic API key for --enhance (or set ANTHROPIC_API_KEY)
```

### Usage Examples

**1. Use Preset Config (Recommended)**
```bash
python3 cli/doc_scraper.py --config configs/godot.json
python3 cli/doc_scraper.py --config configs/react.json
python3 cli/doc_scraper.py --config configs/vue.json
python3 cli/doc_scraper.py --config configs/django.json
python3 cli/doc_scraper.py --config configs/fastapi.json
```

**2. Interactive Mode**
```bash
python3 cli/doc_scraper.py --interactive
# Wizard walks you through:
# - Skill name
# - Base URL
# - Description
# - Selectors (optional)
# - URL patterns (optional)
# - Rate limit
# - Max pages
```

**3. Quick Mode (Minimal)**
```bash
python3 cli/doc_scraper.py \
  --name react \
  --url https://react.dev/ \
  --description "React framework for building UIs"
```

**4. Dry-Run (Preview)**
```bash
python3 cli/doc_scraper.py --config configs/react.json --dry-run
# Shows what will be scraped without downloading data
# No directories created
# Fast validation
```

**5. Skip Scraping (Use Cached Data)**
```bash
python3 cli/doc_scraper.py --config configs/godot.json --skip-scrape
# Uses existing output/godot_data/
# Fast rebuild (1-3 minutes)
# Useful for testing changes
```

**6. With Local Enhancement**
```bash
python3 cli/doc_scraper.py --config configs/react.json --enhance-local
# Scrapes + enhances in one command
# Opens new terminal for Claude Code
# No API key needed
```

**7. With API Enhancement**
```bash
export ANTHROPIC_API_KEY=sk-ant-...
python3 cli/doc_scraper.py --config configs/react.json --enhance

# Or with inline API key:
python3 cli/doc_scraper.py --config configs/react.json --enhance --api-key sk-ant-...
```

### Output Structure

```
output/
├── {name}_data/              # Scraped raw data (cached)
│   ├── pages/
│   │   ├── page_0.json
│   │   ├── page_1.json
│   │   └── ...
│   └── summary.json          # Scraping stats
│
└── {name}/                   # Built skill directory
    ├── SKILL.md              # Main skill file
    ├── SKILL.md.backup       # Backup (if enhanced)
    ├── references/           # Categorized docs
    │   ├── index.md
    │   ├── getting_started.md
    │   ├── api.md
    │   └── ...
    ├── scripts/              # Empty (user scripts)
    └── assets/               # Empty (user assets)
```

---

## Estimator: estimate_pages.py

### Full Help

```
usage: estimate_pages.py [-h] [--max-discovery MAX_DISCOVERY]
                         [--timeout TIMEOUT]
                         config

Estimate page count for Skill Seeker configs

positional arguments:
  config                Path to config JSON file

options:
  -h, --help            Show this help message and exit
  --max-discovery, -m MAX_DISCOVERY
                        Maximum pages to discover (default: 1000)
  --timeout, -t TIMEOUT
                        HTTP request timeout in seconds (default: 30)
```

### Usage Examples

**1. Quick Estimate (100 pages)**
```bash
python3 cli/estimate_pages.py configs/react.json --max-discovery 100
# Time: ~30-60 seconds
# Good for: Quick validation
```

**2. Standard Estimate (1000 pages - default)**
```bash
python3 cli/estimate_pages.py configs/godot.json
# Time: ~1-2 minutes
# Good for: Most use cases
```

**3. Deep Estimate (2000 pages)**
```bash
python3 cli/estimate_pages.py configs/vue.json --max-discovery 2000
# Time: ~3-5 minutes
# Good for: Large documentation sites
```

**4. Custom Timeout**
```bash
python3 cli/estimate_pages.py configs/django.json --timeout 60
# Useful for slow servers
```

### Output Example

```
🔍 Estimating pages for: react
📍 Base URL: https://react.dev/
🎯 Start URLs: 6
⏱️  Rate limit: 0.5s
🔢 Max discovery: 1000

⏳ Discovered: 180 pages (1.3 pages/sec)

======================================================================
📊 ESTIMATION RESULTS
======================================================================

Config: react
Base URL: https://react.dev/

✅ Pages Discovered: 180
⏳ Pages Pending: 50
📈 Estimated Total: 230

⏱️  Time Elapsed: 140.5s
⚡ Discovery Rate: 1.28 pages/sec

======================================================================
💡 RECOMMENDATIONS
======================================================================

✅ Current max_pages (300) is sufficient

⏱️  Estimated full scrape time: 1.9 minutes
   (Based on rate_limit: 0.5s)
```

**What It Shows:**
- Estimated total pages to scrape
- Whether current `max_pages` is sufficient
- Recommended `max_pages` value
- Estimated scraping time
- Discovery rate (pages/sec)

---

## Enhancement Tools

### enhance_skill_local.py (Recommended)

**No API key needed - uses Claude Code Max plan**

```bash
# Usage
python3 cli/enhance_skill_local.py output/react/
python3 cli/enhance_skill_local.py output/godot/

# What it does:
# 1. Reads SKILL.md and references/
# 2. Opens new terminal with Claude Code
# 3. Claude enhances SKILL.md
# 4. Backs up original to SKILL.md.backup
# 5. Saves enhanced version

# Time: ~60 seconds
# Cost: Free (uses your Claude Code Max plan)
```

### enhance_skill.py (Alternative)

**Requires Anthropic API key**

```bash
# Install dependency first
pip3 install anthropic

# Usage with environment variable
export ANTHROPIC_API_KEY=sk-ant-...
python3 cli/enhance_skill.py output/react/

# Usage with inline API key
python3 cli/enhance_skill.py output/godot/ --api-key sk-ant-...

# What it does:
# 1. Reads SKILL.md and references/
# 2. Calls Claude API (Sonnet 4)
# 3. Enhances SKILL.md
# 4. Backs up original to SKILL.md.backup
# 5. Saves enhanced version

# Time: ~30-60 seconds
# Cost: ~$0.01-0.10 per skill (depending on size)
```

---

## Packaging Tool

### package_skill.py

```bash
# Usage
python3 cli/package_skill.py output/react/
python3 cli/package_skill.py output/godot/

# What it does:
# 1. Validates SKILL.md exists
# 2. Creates .zip with all skill files
# 3. Saves to output/{name}.zip

# Output:
# output/react.zip
# output/godot.zip

# Time: Instant
```

---

## Testing Tools

### run_tests.py

```bash
# Run all tests (default)
python3 cli/run_tests.py
# 71 tests, ~1 second

# Verbose output
python3 cli/run_tests.py -v
python3 cli/run_tests.py --verbose

# Quiet output
python3 cli/run_tests.py -q
python3 cli/run_tests.py --quiet

# Stop on first failure
python3 cli/run_tests.py -f
python3 cli/run_tests.py --failfast

# Run specific test suite
python3 cli/run_tests.py --suite config
python3 cli/run_tests.py --suite features
python3 cli/run_tests.py --suite integration

# List all tests
python3 cli/run_tests.py --list
```

### Individual Tests

```bash
# Run single test file
python3 -m unittest tests.test_config_validation
python3 -m unittest tests.test_scraper_features
python3 -m unittest tests.test_integration

# Run single test class
python3 -m unittest tests.test_config_validation.TestConfigValidation

# Run single test method
python3 -m unittest tests.test_config_validation.TestConfigValidation.test_valid_complete_config
```

---

## Available Configs

### Preset Configs (Ready to Use)

| Config | Framework | Pages | Description |
|--------|-----------|-------|-------------|
| `godot.json` | Godot Engine | ~500 | Game engine documentation |
| `react.json` | React | ~300 | React framework docs |
| `vue.json` | Vue.js | ~250 | Vue.js framework docs |
| `django.json` | Django | ~400 | Django web framework |
| `fastapi.json` | FastAPI | ~200 | FastAPI Python framework |
| `steam-economy-complete.json` | Steam | ~100 | Steam Economy API docs |

### View Config Details

```bash
# List all configs
ls configs/

# View config content
cat configs/react.json
python3 -m json.tool configs/godot.json
```

### Config Structure

```json
{
  "name": "react",
  "base_url": "https://react.dev/",
  "description": "React - JavaScript library for building UIs",
  "start_urls": [
    "https://react.dev/learn",
    "https://react.dev/reference/react",
    "https://react.dev/reference/react-dom"
  ],
  "selectors": {
    "main_content": "article",
    "title": "h1",
    "code_blocks": "pre code"
  },
  "url_patterns": {
    "include": ["/learn/", "/reference/"],
    "exclude": ["/blog/", "/community/"]
  },
  "categories": {
    "getting_started": ["learn", "tutorial", "intro"],
    "api": ["reference", "api", "hooks"],
    "guides": ["guide"]
  },
  "rate_limit": 0.5,
  "max_pages": 300
}
```

---

## Common Workflows

### Workflow 1: Use Preset (Fastest)

```bash
# 1. Estimate (optional, 1-2 min)
python3 cli/estimate_pages.py configs/react.json

# 2. Scrape with local enhancement (25 min)
python3 cli/doc_scraper.py --config configs/react.json --enhance-local

# 3. Package (instant)
python3 cli/package_skill.py output/react/

# Result: output/react.zip
# Upload to Claude!
```

### Workflow 2: Custom Documentation

```bash
# 1. Create config
cat > configs/my-docs.json << 'EOF'
{
  "name": "my-docs",
  "base_url": "https://docs.example.com/",
  "description": "My documentation site",
  "rate_limit": 0.5,
  "max_pages": 200
}
EOF

# 2. Estimate
python3 cli/estimate_pages.py configs/my-docs.json

# 3. Dry-run test
python3 cli/doc_scraper.py --config configs/my-docs.json --dry-run

# 4. Full scrape
python3 cli/doc_scraper.py --config configs/my-docs.json

# 5. Enhance
python3 cli/enhance_skill_local.py output/my-docs/

# 6. Package
python3 cli/package_skill.py output/my-docs/
```

### Workflow 3: Interactive Mode

```bash
# 1. Start interactive wizard
python3 cli/doc_scraper.py --interactive

# 2. Answer prompts:
#    - Name: my-framework
#    - URL: https://framework.dev/
#    - Description: My favorite framework
#    - Selectors: (uses defaults)
#    - Rate limit: 0.5
#    - Max pages: 100

# 3. Enhance
python3 cli/enhance_skill_local.py output/my-framework/

# 4. Package
python3 cli/package_skill.py output/my-framework/
```

### Workflow 4: Quick Mode

```bash
python3 cli/doc_scraper.py \
  --name vue \
  --url https://vuejs.org/ \
  --description "Vue.js framework" \
  --enhance-local
```

### Workflow 5: Rebuild from Cache

```bash
# Already scraped once?
# Skip re-scraping, just rebuild
python3 cli/doc_scraper.py --config configs/godot.json --skip-scrape

# Try new enhancement
python3 cli/enhance_skill_local.py output/godot/

# Re-package
python3 cli/package_skill.py output/godot/
```

### Workflow 6: Testing New Config

```bash
# 1. Create test config with low max_pages
cat > configs/test.json << 'EOF'
{
  "name": "test-site",
  "base_url": "https://docs.test.com/",
  "max_pages": 20,
  "rate_limit": 0.1
}
EOF

# 2. Estimate
python3 cli/estimate_pages.py configs/test.json --max-discovery 50

# 3. Dry-run
python3 cli/doc_scraper.py --config configs/test.json --dry-run

# 4. Small scrape
python3 cli/doc_scraper.py --config configs/test.json

# 5. Validate output
ls output/test-site/
ls output/test-site/references/

# 6. If good, increase max_pages and re-run
```

---

## Troubleshooting

### Issue: "Rate limit exceeded"

```bash
# Increase rate_limit in config
# Default: 0.5 seconds
# Conservative: 1.0 seconds
# Very conservative: 2.0 seconds

# Edit config:
{
  "rate_limit": 1.0
}
```

### Issue: "Too many pages"

```bash
# Estimate first
python3 cli/estimate_pages.py configs/my-config.json

# Set max_pages based on estimate
# Add buffer: estimated + 50

# Edit config:
{
  "max_pages": 350  # for 300 estimated
}
```

### Issue: "No content extracted"

```bash
# Wrong selectors
# Test selectors manually:
curl -s https://docs.example.com/ | grep -i 'article\|main\|content'

# Common selectors:
"main_content": "article"
"main_content": "main"
"main_content": ".content"
"main_content": "#main-content"
"main_content": "div[role=\"main\"]"

# Update config with correct selector
```

### Issue: "Tests failing"

```bash
# Run specific failing test
python3 -m unittest tests.test_config_validation.TestConfigValidation.test_name -v

# Check error message
# Verify expectations match implementation
```

### Issue: "Enhancement fails"

```bash
# Local enhancement:
# Make sure Claude Code is running
# Check terminal output

# API enhancement:
# Verify API key is set:
echo $ANTHROPIC_API_KEY

# Or use inline:
python3 cli/enhance_skill.py output/react/ --api-key sk-ant-...
```

### Issue: "Package fails"

```bash
# Verify SKILL.md exists
ls output/my-skill/SKILL.md

# If missing, build first:
python3 cli/doc_scraper.py --config configs/my-skill.json --skip-scrape
```

### Issue: "Can't find output"

```bash
# Check output directory
ls output/

# Skill data (cached):
ls output/{name}_data/

# Built skill:
ls output/{name}/

# Packaged skill:
ls output/{name}.zip
```

---

## Advanced Usage

### Custom Selectors

```json
{
  "selectors": {
    "main_content": "div.documentation",
    "title": "h1.page-title",
    "code_blocks": "pre.highlight code",
    "navigation": "nav.sidebar"
  }
}
```

### URL Pattern Filtering

```json
{
  "url_patterns": {
    "include": [
      "/docs/",
      "/guide/",
      "/api/",
      "/tutorial/"
    ],
    "exclude": [
      "/blog/",
      "/news/",
      "/community/",
      "/showcase/"
    ]
  }
}
```

### Custom Categories

```json
{
  "categories": {
    "getting_started": ["intro", "tutorial", "quickstart", "installation"],
    "core_concepts": ["concept", "fundamental", "architecture"],
    "api": ["reference", "api", "method", "function"],
    "guides": ["guide", "how-to", "example"],
    "advanced": ["advanced", "expert", "performance"]
  }
}
```

### Multiple Start URLs

```json
{
  "start_urls": [
    "https://docs.example.com/getting-started/",
    "https://docs.example.com/api/",
    "https://docs.example.com/guides/",
    "https://docs.example.com/examples/"
  ]
}
```

---

## Performance Tips

1. **Estimate first**: Save 20-40 minutes by validating config
2. **Use dry-run**: Test selectors before full scrape
3. **Cache data**: Use `--skip-scrape` for fast rebuilds
4. **Adjust rate_limit**: Balance speed vs politeness
5. **Set appropriate max_pages**: Don't scrape more than needed
6. **Use start_urls**: Target specific documentation sections
7. **Filter URLs**: Use include/exclude patterns
8. **Run tests**: Catch issues early

---

## Environment Variables

```bash
# Anthropic API key (for API enhancement)
export ANTHROPIC_API_KEY=sk-ant-...

# Optional: Set custom output directory
export SKILL_SEEKER_OUTPUT_DIR=/path/to/output
```

---

## Exit Codes

- `0`: Success
- `1`: Error (general)
- `2`: Warning (estimation hit limit)

---

## File Locations

```
Skill_Seekers/
├── doc_scraper.py           # Main tool
├── estimate_pages.py        # Estimator
├── enhance_skill.py         # API enhancement
├── enhance_skill_local.py   # Local enhancement
├── package_skill.py         # Packager
├── run_tests.py             # Test runner
├── configs/                 # Preset configs
├── tests/                   # Test suite
├── docs/                    # Documentation
└── output/                  # Generated output
```

---

## Getting Help

```bash
# Tool-specific help
python3 cli/doc_scraper.py --help
python3 cli/estimate_pages.py --help
python3 cli/run_tests.py --help

# Documentation
cat CLAUDE.md              # Quick reference for Claude Code
cat docs/CLAUDE.md         # Detailed technical docs
cat docs/TESTING.md        # Testing guide
cat docs/USAGE.md          # This file
cat docs/ENHANCEMENT.md    # Enhancement guide
cat docs/UPLOAD_GUIDE.md   # Upload instructions
cat README.md              # Project overview
```

---

## Summary

**Essential Commands:**
```bash
python3 cli/estimate_pages.py configs/react.json              # Estimate
python3 cli/doc_scraper.py --config configs/react.json        # Scrape
python3 cli/enhance_skill_local.py output/react/              # Enhance
python3 cli/package_skill.py output/react/                    # Package
python3 cli/run_tests.py                                      # Test
```

**Quick Start:**
```bash
pip3 install requests beautifulsoup4
python3 cli/doc_scraper.py --config configs/react.json --enhance-local
python3 cli/package_skill.py output/react/
# Upload output/react.zip to Claude!
```

Happy skill creating! 🚀
