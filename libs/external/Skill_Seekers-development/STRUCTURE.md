# Repository Structure

```
Skill_Seekers/
│
├── 📄 Root Documentation
│   ├── README.md                  # Main documentation (start here!)
│   ├── CLAUDE.md                  # Quick reference for Claude Code
│   ├── QUICKSTART.md              # 3-step quick start guide
│   ├── ROADMAP.md                 # Development roadmap
│   ├── TODO.md                    # Current sprint tasks
│   ├── STRUCTURE.md               # This file
│   ├── LICENSE                    # MIT License
│   └── .gitignore                 # Git ignore rules
│
├── 🔧 CLI Tools (cli/)
│   ├── doc_scraper.py             # Main scraping tool
│   ├── estimate_pages.py          # Page count estimator
│   ├── enhance_skill.py           # AI enhancement (API-based)
│   ├── enhance_skill_local.py     # AI enhancement (LOCAL, no API)
│   ├── package_skill.py           # Skill packaging tool
│   └── run_tests.py               # Test runner
│
├── 🌐 MCP Server (mcp/)
│   ├── server.py                  # Main MCP server
│   ├── requirements.txt           # MCP dependencies
│   └── README.md                  # MCP setup guide
│
├── 📁 configs/                    # Preset configurations
│   ├── godot.json
│   ├── react.json
│   ├── vue.json
│   ├── django.json
│   ├── fastapi.json
│   ├── kubernetes.json
│   └── steam-economy-complete.json
│
├── 🧪 tests/                      # Test suite (71 tests, 100% pass rate)
│   ├── test_config_validation.py
│   ├── test_integration.py
│   └── test_scraper_features.py
│
├── 📚 docs/                       # Detailed documentation
│   ├── CLAUDE.md                  # Technical architecture
│   ├── ENHANCEMENT.md             # AI enhancement guide
│   ├── USAGE.md                   # Complete usage guide
│   ├── TESTING.md                 # Testing guide
│   └── UPLOAD_GUIDE.md            # How to upload skills
│
├── 🔀 .github/                    # GitHub configuration
│   ├── SETUP_GUIDE.md             # GitHub project setup
│   ├── ISSUES_TO_CREATE.md        # Issue templates
│   └── ISSUE_TEMPLATE/            # Issue templates
│
└── 📦 output/                     # Generated skills (git-ignored)
    ├── {name}_data/               # Scraped raw data (cached)
    └── {name}/                    # Built skills
        ├── SKILL.md               # Main skill file
        └── references/            # Reference documentation
```

## Key Files

### For Users:
- **README.md** - Start here for overview and installation
- **QUICKSTART.md** - Get started in 3 steps
- **configs/** - 7 ready-to-use presets
- **mcp/README.md** - MCP server setup for Claude Code

### For CLI Usage:
- **cli/doc_scraper.py** - Main scraping tool
- **cli/estimate_pages.py** - Page count estimator
- **cli/enhance_skill_local.py** - Local enhancement (no API key)
- **cli/package_skill.py** - Package skills to .zip

### For MCP Usage (Claude Code):
- **mcp/server.py** - MCP server (6 tools)
- **mcp/README.md** - Setup instructions
- **configs/** - Shared configurations

### For Developers:
- **docs/CLAUDE.md** - Architecture and internals
- **docs/USAGE.md** - Complete usage guide
- **docs/TESTING.md** - Testing guide
- **tests/** - 71 tests (100% pass rate)

### For Contributors:
- **ROADMAP.md** - Development roadmap
- **TODO.md** - Current sprint tasks
- **.github/SETUP_GUIDE.md** - GitHub setup
- **LICENSE** - MIT License

## Architecture

### Monorepo Structure

The repository is organized as a monorepo with two main components:

1. **CLI Tools** (`cli/`): Standalone Python scripts for direct command-line usage
2. **MCP Server** (`mcp/`): Model Context Protocol server for Claude Code integration

Both components share the same configuration files and output directory.

### Data Flow

```
Config (configs/*.json)
  ↓
CLI Tools OR MCP Server
  ↓
Scraper (cli/doc_scraper.py)
  ↓
Output (output/{name}_data/)
  ↓
Builder (cli/doc_scraper.py)
  ↓
Skill (output/{name}/)
  ↓
Enhancer (optional)
  ↓
Packager (cli/package_skill.py)
  ↓
Skill .zip (output/{name}.zip)
```
