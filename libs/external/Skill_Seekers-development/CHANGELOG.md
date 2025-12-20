# Changelog

All notable changes to Skill Seeker will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

---

## [2.1.1] - 2025-11-30

### 🚀 GitHub Repository Analysis Enhancements

This release significantly improves GitHub repository scraping with unlimited local analysis, configurable directory exclusions, and numerous bug fixes.

### Added
- **Configurable directory exclusions** for local repository analysis ([#203](https://github.com/yusufkaraaslan/Skill_Seekers/issues/203))
  - `exclude_dirs_additional`: Extend default exclusions with custom directories
  - `exclude_dirs`: Replace default exclusions entirely (advanced users)
  - 19 comprehensive tests covering all scenarios
  - Logging: INFO for extend mode, WARNING for replace mode
- **Unlimited local repository analysis** via `local_repo_path` configuration parameter
- **Auto-exclusion** of virtual environments, build artifacts, and cache directories
- **Support for analyzing repositories without GitHub API rate limits** (50 → unlimited files)
- **Skip llms.txt option** - Force HTML scraping even when llms.txt is detected ([#198](https://github.com/yusufkaraaslan/Skill_Seekers/pull/198))

### Fixed
- Fixed logger initialization error causing `AttributeError: 'NoneType' object has no attribute 'setLevel'` ([#190](https://github.com/yusufkaraaslan/Skill_Seekers/issues/190))
- Fixed 3 NoneType subscriptable errors in release tag parsing
- Fixed relative import paths causing `ModuleNotFoundError`
- Fixed hardcoded 50-file analysis limit preventing comprehensive code analysis
- Fixed GitHub API file tree limitation (140 → 345 files discovered)
- Fixed AST parser "not iterable" errors eliminating 100% of parsing failures (95 → 0 errors)
- Fixed virtual environment file pollution reducing file tree noise by 95%
- Fixed `force_rescrape` flag not checked before interactive prompt causing EOFError in CI/CD environments

### Improved
- Increased code analysis coverage from 14% to 93.6% (+79.6 percentage points)
- Improved file discovery from 140 to 345 files (+146%)
- Improved class extraction from 55 to 585 classes (+964%)
- Improved function extraction from 512 to 2,784 functions (+444%)
- Test suite expanded to 427 tests (up from 391)

---

## [2.1.0] - 2025-11-12

### 🎉 Major Enhancement: Quality Assurance + Race Condition Fixes

This release focuses on quality and reliability improvements, adding comprehensive quality checks and fixing critical race conditions in the enhancement workflow.

### 🚀 Major Features

#### Comprehensive Quality Checker
- **Automatic quality checks before packaging** - Validates skill quality before upload
- **Quality scoring system** - 0-100 score with A-F grades
- **Enhancement verification** - Checks for template text, code examples, sections
- **Structure validation** - Validates SKILL.md, references/ directory
- **Content quality checks** - YAML frontmatter, language tags, "When to Use" section
- **Link validation** - Validates internal markdown links
- **Detailed reporting** - Errors, warnings, and info messages with file locations
- **CLI tool** - `skill-seekers-quality-checker` with verbose and strict modes

#### Headless Enhancement Mode (Default)
- **No terminal windows** - Runs enhancement in background by default
- **Proper waiting** - Main console waits for enhancement to complete
- **Timeout protection** - 10-minute default timeout (configurable)
- **Verification** - Checks that SKILL.md was actually updated
- **Progress messages** - Clear status updates during enhancement
- **Interactive mode available** - `--interactive-enhancement` flag for terminal mode

### Added

#### New CLI Tools
- **quality_checker.py** - Comprehensive skill quality validation
  - Structure checks (SKILL.md, references/)
  - Enhancement verification (code examples, sections)
  - Content validation (frontmatter, language tags)
  - Link validation (internal markdown links)
  - Quality scoring (0-100 + A-F grade)

#### New Features
- **Headless enhancement** - `skill-seekers-enhance` runs in background by default
- **Quality checks in packaging** - Automatic validation before creating .zip
- **MCP quality skip** - MCP server skips interactive checks
- **Enhanced error handling** - Better error messages and timeout handling

#### Tests
- **+12 quality checker tests** - Comprehensive validation testing
- **391 total tests passing** - Up from 379 in v2.0.0
- **0 test failures** - All tests green
- **CI improvements** - Fixed macOS terminal detection tests

### Changed

#### Enhancement Workflow
- **Default mode changed** - Headless mode is now default (was terminal mode)
- **Waiting behavior** - Main console waits for enhancement completion
- **No race conditions** - Fixed "Package your skill" message appearing too early
- **Better progress** - Clear status messages during enhancement

#### Package Workflow
- **Quality checks added** - Automatic validation before packaging
- **User confirmation** - Ask to continue if warnings/errors found
- **Skip option** - `--skip-quality-check` flag to bypass checks
- **MCP context** - Automatically skips checks in non-interactive contexts

#### CLI Arguments
- **doc_scraper.py:**
  - Updated `--enhance-local` help text (mentions headless mode)
  - Added `--interactive-enhancement` flag
- **enhance_skill_local.py:**
  - Changed default to `headless=True`
  - Added `--interactive-enhancement` flag
  - Added `--timeout` flag (default: 600 seconds)
- **package_skill.py:**
  - Added `--skip-quality-check` flag

### Fixed

#### Critical Bugs
- **Enhancement race condition** - Main console no longer exits before enhancement completes
- **MCP stdin errors** - MCP server now skips interactive prompts
- **Terminal detection tests** - Fixed for headless mode default

#### Enhancement Issues
- **Process detachment** - subprocess.run() now waits properly instead of Popen()
- **Timeout handling** - Added timeout protection to prevent infinite hangs
- **Verification** - Checks file modification time and size to verify success
- **Error messages** - Better error handling and user-friendly messages

#### Test Fixes
- **package_skill tests** - Added skip_quality_check=True to prevent stdin errors
- **Terminal detection tests** - Updated to use headless=False for interactive tests
- **MCP server tests** - Fixed to skip quality checks in non-interactive context

### Technical Details

#### New Modules
- `src/skill_seekers/cli/quality_checker.py` - Quality validation engine
- `tests/test_quality_checker.py` - 12 comprehensive tests

#### Modified Modules
- `src/skill_seekers/cli/enhance_skill_local.py` - Added headless mode
- `src/skill_seekers/cli/doc_scraper.py` - Updated enhancement integration
- `src/skill_seekers/cli/package_skill.py` - Added quality checks
- `src/skill_seekers/mcp/server.py` - Skip quality checks in MCP context
- `tests/test_package_skill.py` - Updated for quality checker
- `tests/test_terminal_detection.py` - Updated for headless default

#### Commits in This Release
- `e279ed6` - Phase 1: Enhancement race condition fix (headless mode)
- `3272f9c` - Phases 2 & 3: Quality checker implementation
- `2dd1027` - Phase 4: Tests (+12 quality checker tests)
- `befcb89` - CI Fix: Skip quality checks in MCP context
- `67ab627` - CI Fix: Update terminal tests for headless default

### Upgrade Notes

#### Breaking Changes
- **Headless mode default** - Enhancement now runs in background by default
  - Use `--interactive-enhancement` if you want the old terminal mode
  - Affects: `skill-seekers-enhance` and `skill-seekers scrape --enhance-local`

#### New Behavior
- **Quality checks** - Packaging now runs quality checks by default
  - May prompt for confirmation if warnings/errors found
  - Use `--skip-quality-check` to bypass (not recommended)

#### Recommendations
- **Try headless mode** - Faster and more reliable than terminal mode
- **Review quality reports** - Fix warnings before packaging
- **Update scripts** - Add `--skip-quality-check` to automated packaging scripts if needed

### Migration Guide

**If you want the old terminal mode behavior:**
```bash
# Old (v2.0.0): Default was terminal mode
skill-seekers-enhance output/react/

# New (v2.1.0): Use --interactive-enhancement
skill-seekers-enhance output/react/ --interactive-enhancement
```

**If you want to skip quality checks:**
```bash
# Add --skip-quality-check to package command
skill-seekers-package output/react/ --skip-quality-check
```

---

## [2.0.0] - 2025-11-11

### 🎉 Major Release: PyPI Publication + Modern Python Packaging

**Skill Seekers is now available on PyPI!** Install with: `pip install skill-seekers`

This is a major milestone release featuring complete restructuring for modern Python packaging, comprehensive testing improvements, and publication to the Python Package Index.

### 🚀 Major Changes

#### PyPI Publication
- **Published to PyPI** - https://pypi.org/project/skill-seekers/
- **Installation:** `pip install skill-seekers` or `uv tool install skill-seekers`
- **No cloning required** - Install globally or in virtual environments
- **Automatic dependency management** - All dependencies handled by pip/uv

#### Modern Python Packaging
- **pyproject.toml-based configuration** - Standard PEP 621 metadata
- **src/ layout structure** - Best practice package organization
- **Entry point scripts** - `skill-seekers` command available globally
- **Proper dependency groups** - Separate dev, test, and MCP dependencies
- **Build backend** - setuptools-based build with uv support

#### Unified CLI Interface
- **Single `skill-seekers` command** - Git-style subcommands
- **Subcommands:** `scrape`, `github`, `pdf`, `unified`, `enhance`, `package`, `upload`, `estimate`
- **Consistent interface** - All tools accessible through one entry point
- **Help system** - Comprehensive `--help` for all commands

### Added

#### Testing Infrastructure
- **379 passing tests** (up from 299) - Comprehensive test coverage
- **0 test failures** - All tests passing successfully
- **Test suite improvements:**
  - Fixed import paths for src/ layout
  - Updated CLI tests for unified entry points
  - Added package structure verification tests
  - Fixed MCP server import tests
  - Added pytest configuration in pyproject.toml

#### Documentation
- **Updated README.md** - PyPI badges, reordered installation options
- **FUTURE_RELEASES.md** - Roadmap for upcoming features
- **Installation guides** - Simplified with PyPI as primary method
- **Testing documentation** - How to run full test suite

### Changed

#### Package Structure
- **Moved to src/ layout:**
  - `src/skill_seekers/` - Main package
  - `src/skill_seekers/cli/` - CLI tools
  - `src/skill_seekers/mcp/` - MCP server
- **Import paths updated** - All imports use proper package structure
- **Entry points configured** - All CLI tools available as commands

#### Import Fixes
- **Fixed `merge_sources.py`** - Corrected conflict_detector import (`.conflict_detector`)
- **Fixed MCP server tests** - Updated to use `skill_seekers.mcp.server` imports
- **Fixed test paths** - All tests updated for src/ layout

### Fixed

#### Critical Bugs
- **Import path errors** - Fixed relative imports in CLI modules
- **MCP test isolation** - Added proper MCP availability checks
- **Package installation** - Resolved entry point conflicts
- **Dependency resolution** - All dependencies properly specified

#### Test Improvements
- **17 test fixes** - Updated for modern package structure
- **MCP test guards** - Proper skipif decorators for MCP tests
- **CLI test updates** - Accept both exit codes 0 and 2 for help
- **Path validation** - Tests verify correct package structure

### Technical Details

#### Build System
- **Build backend:** setuptools.build_meta
- **Build command:** `uv build`
- **Publish command:** `uv publish`
- **Distribution formats:** wheel + source tarball

#### Dependencies
- **Core:** requests, beautifulsoup4, PyGithub, mcp, httpx
- **PDF:** PyMuPDF, Pillow, pytesseract
- **Dev:** pytest, pytest-cov, pytest-anyio, mypy
- **MCP:** mcp package for Claude Code integration

### Migration Guide

#### For Users
**Old way:**
```bash
git clone https://github.com/yusufkaraaslan/Skill_Seekers.git
cd Skill_Seekers
pip install -r requirements.txt
python3 cli/doc_scraper.py --config configs/react.json
```

**New way:**
```bash
pip install skill-seekers
skill-seekers scrape --config configs/react.json
```

#### For Developers
- Update imports: `from cli.* → from skill_seekers.cli.*`
- Use `pip install -e ".[dev]"` for development
- Run tests: `python -m pytest`
- Entry points instead of direct script execution

### Breaking Changes
- **CLI interface changed** - Use `skill-seekers` command instead of `python3 cli/...`
- **Import paths changed** - Package now at `skill_seekers.*` instead of `cli.*`
- **Installation method changed** - PyPI recommended over git clone

### Deprecations
- **Direct script execution** - Still works but deprecated (use `skill-seekers` command)
- **Old import patterns** - Legacy imports still work but will be removed in v3.0

### Compatibility
- **Python 3.10+** required
- **Backward compatible** - Old scripts still work with legacy CLI
- **Config files** - No changes required
- **Output format** - No changes to generated skills

---

## [1.3.0] - 2025-10-26

### Added - Refactoring & Performance Improvements
- **Async/Await Support for Parallel Scraping** (2-3x performance boost)
  - `--async` flag to enable async mode
  - `async def scrape_page_async()` method using httpx.AsyncClient
  - `async def scrape_all_async()` method with asyncio.gather()
  - Connection pooling for better performance
  - asyncio.Semaphore for concurrency control
  - Comprehensive async testing (11 new tests)
  - Full documentation in ASYNC_SUPPORT.md
  - Performance: ~55 pages/sec vs ~18 pages/sec (sync)
  - Memory: 40 MB vs 120 MB (66% reduction)
- **Python Package Structure** (Phase 0 Complete)
  - `cli/__init__.py` - CLI tools package with clean imports
  - `skill_seeker_mcp/__init__.py` - MCP server package (renamed from mcp/)
  - `skill_seeker_mcp/tools/__init__.py` - MCP tools subpackage
  - Proper package imports: `from cli import constants`
- **Centralized Configuration Module**
  - `cli/constants.py` with 18 configuration constants
  - `DEFAULT_ASYNC_MODE`, `DEFAULT_RATE_LIMIT`, `DEFAULT_MAX_PAGES`
  - Enhancement limits, categorization scores, file limits
  - All magic numbers now centralized and configurable
- **Code Quality Improvements**
  - Converted 71 print() statements to proper logging calls
  - Added type hints to all DocToSkillConverter methods
  - Fixed all mypy type checking issues
  - Installed types-requests for better type safety
- Multi-variant llms.txt detection: downloads all 3 variants (full, standard, small)
- Automatic .txt → .md file extension conversion
- No content truncation: preserves complete documentation
- `detect_all()` method for finding all llms.txt variants
- `get_proper_filename()` for correct .md naming

### Changed
- `_try_llms_txt()` now downloads all available variants instead of just one
- Reference files now contain complete content (no 2500 char limit)
- Code samples now include full code (no 600 char limit)
- Test count increased from 207 to 299 (92 new tests)
- All print() statements replaced with logging (logger.info, logger.warning, logger.error)
- Better IDE support with proper package structure
- Code quality improved from 5.5/10 to 6.5/10

### Fixed
- File extension bug: llms.txt files now saved as .md
- Content loss: 0% truncation (was 36%)
- Test isolation issues in test_async_scraping.py (proper cleanup with try/finally)
- Import issues: no more sys.path.insert() hacks needed
- .gitignore: added test artifacts (.pytest_cache, .coverage, htmlcov, etc.)

---

## [1.2.0] - 2025-10-23

### 🚀 PDF Advanced Features Release

Major enhancement to PDF extraction capabilities with Priority 2 & 3 features.

### Added

#### Priority 2: Support More PDF Types
- **OCR Support for Scanned PDFs**
  - Automatic text extraction from scanned documents using Tesseract OCR
  - Fallback mechanism when page text < 50 characters
  - Integration with pytesseract and Pillow
  - Command: `--ocr` flag
  - New dependencies: `Pillow==11.0.0`, `pytesseract==0.3.13`

- **Password-Protected PDF Support**
  - Handle encrypted PDFs with password authentication
  - Clear error messages for missing/wrong passwords
  - Secure password handling
  - Command: `--password PASSWORD` flag

- **Complex Table Extraction**
  - Extract tables from PDFs using PyMuPDF's table detection
  - Capture table data as 2D arrays with metadata (bbox, row/col count)
  - Integration with skill references in markdown format
  - Command: `--extract-tables` flag

#### Priority 3: Performance Optimizations
- **Parallel Page Processing**
  - 3x faster PDF extraction using ThreadPoolExecutor
  - Auto-detect CPU count or custom worker specification
  - Only activates for PDFs with > 5 pages
  - Commands: `--parallel` and `--workers N` flags
  - Benchmarks: 500-page PDF reduced from 4m 10s to 1m 15s

- **Intelligent Caching**
  - In-memory cache for expensive operations (text extraction, code detection, quality scoring)
  - 50% faster on re-runs
  - Command: `--no-cache` to disable (enabled by default)

#### New Documentation
- **`docs/PDF_ADVANCED_FEATURES.md`** (580 lines)
  - Complete usage guide for all advanced features
  - Installation instructions
  - Performance benchmarks showing 3x speedup
  - Best practices and troubleshooting
  - API reference with all parameters

#### Testing
- **New test file:** `tests/test_pdf_advanced_features.py` (568 lines, 26 tests)
  - TestOCRSupport (5 tests)
  - TestPasswordProtection (4 tests)
  - TestTableExtraction (5 tests)
  - TestCaching (5 tests)
  - TestParallelProcessing (4 tests)
  - TestIntegration (3 tests)
- **Updated:** `tests/test_pdf_extractor.py` (23 tests fixed and passing)
- **Total PDF tests:** 49/49 PASSING ✅ (100% pass rate)

### Changed
- Enhanced `cli/pdf_extractor_poc.py` with all advanced features
- Updated `requirements.txt` with new dependencies
- Updated `README.md` with PDF advanced features usage
- Updated `docs/TESTING.md` with new test counts (142 total tests)

### Performance Improvements
- **3.3x faster** with parallel processing (8 workers)
- **1.7x faster** on re-runs with caching enabled
- Support for unlimited page PDFs (no more 500-page limit)

### Dependencies
- Added `Pillow==11.0.0` for image processing
- Added `pytesseract==0.3.13` for OCR support
- Tesseract OCR engine (system package, optional)

---

## [1.1.0] - 2025-10-22

### 🌐 Documentation Scraping Enhancements

Major improvements to documentation scraping with unlimited pages, parallel processing, and new configs.

### Added

#### Unlimited Scraping & Performance
- **Unlimited Page Scraping** - Removed 500-page limit, now supports unlimited pages
- **Parallel Scraping Mode** - Process multiple pages simultaneously for faster scraping
- **Dynamic Rate Limiting** - Smart rate limit control to avoid server blocks
- **CLI Utilities** - New helper scripts for common tasks

#### New Configurations
- **Ansible Core 2.19** - Complete Ansible documentation config
- **Claude Code** - Documentation for this very tool!
- **Laravel 9.x** - PHP framework documentation

#### Testing & Quality
- Comprehensive test coverage for CLI utilities
- Parallel scraping test suite
- Virtual environment setup documentation
- Thread-safety improvements

### Fixed
- Thread-safety issues in parallel scraping
- CLI path references across all documentation
- Flaky upload_skill tests
- MCP server streaming subprocess implementation

### Changed
- All CLI examples now use `cli/` directory prefix
- Updated documentation structure
- Enhanced error handling

---

## [1.0.0] - 2025-10-19

### 🎉 First Production Release

This is the first production-ready release of Skill Seekers with complete feature set, full test coverage, and comprehensive documentation.

### Added

#### Smart Auto-Upload Feature
- New `upload_skill.py` CLI tool for automatic API-based upload
- Enhanced `package_skill.py` with `--upload` flag
- Smart API key detection with graceful fallback
- Cross-platform folder opening in `utils.py`
- Helpful error messages instead of confusing errors

#### MCP Integration Enhancements
- **9 MCP tools** (added `upload_skill` tool)
- `mcp__skill-seeker__upload_skill` - Upload .zip files to Claude automatically
- Enhanced `package_skill` tool with smart auto-upload parameter
- Updated all MCP documentation to reflect 9 tools

#### Documentation Improvements
- Updated README with version badge (v1.0.0)
- Enhanced upload guide with 3 upload methods
- Updated MCP setup guide with all 9 tools
- Comprehensive test documentation (14/14 tests)
- All references to tool counts corrected

### Fixed
- Missing `import os` in `mcp/server.py`
- `package_skill.py` exit code behavior (now exits 0 when API key missing)
- Improved UX with helpful messages instead of errors

### Changed
- Test count badge updated (96 → 14 passing)
- All documentation references updated to 9 tools

### Testing
- **CLI Tests:** 8/8 PASSED ✅
- **MCP Tests:** 6/6 PASSED ✅
- **Total:** 14/14 PASSED (100%)

---

## [0.4.0] - 2025-10-18

### Added

#### Large Documentation Support (40K+ Pages)
- Config splitting functionality for massive documentation sites
- Router/hub skill generation for intelligent query routing
- Checkpoint/resume feature for long scrapes
- Parallel scraping support for faster processing
- 4 split strategies: auto, category, router, size

#### New CLI Tools
- `split_config.py` - Split large configs into focused sub-skills
- `generate_router.py` - Generate router/hub skills
- `package_multi.py` - Package multiple skills at once

#### New MCP Tools
- `split_config` - Split large documentation via MCP
- `generate_router` - Generate router skills via MCP

#### Documentation
- New `docs/LARGE_DOCUMENTATION.md` guide
- Example config: `godot-large-example.json` (40K pages)

### Changed
- MCP tool count: 6 → 8 tools
- Updated documentation for large docs workflow

---

## [0.3.0] - 2025-10-15

### Added

#### MCP Server Integration
- Complete MCP server implementation (`mcp/server.py`)
- 6 MCP tools for Claude Code integration:
  - `list_configs`
  - `generate_config`
  - `validate_config`
  - `estimate_pages`
  - `scrape_docs`
  - `package_skill`

#### Setup & Configuration
- Automated setup script (`setup_mcp.sh`)
- MCP configuration examples
- Comprehensive MCP setup guide (`docs/MCP_SETUP.md`)
- MCP testing guide (`docs/TEST_MCP_IN_CLAUDE_CODE.md`)

#### Testing
- 31 comprehensive unit tests for MCP server
- Integration tests via Claude Code MCP protocol
- 100% test pass rate

#### Documentation
- Complete MCP integration documentation
- Natural language usage examples
- Troubleshooting guides

### Changed
- Restructured project as monorepo with CLI and MCP server
- Moved CLI tools to `cli/` directory
- Added MCP server to `mcp/` directory

---

## [0.2.0] - 2025-10-10

### Added

#### Testing & Quality
- Comprehensive test suite with 71 tests
- 100% test pass rate
- Test coverage for all major features
- Config validation tests

#### Optimization
- Page count estimator (`estimate_pages.py`)
- Framework config optimizations with `start_urls`
- Better URL pattern coverage
- Improved scraping efficiency

#### New Configs
- Kubernetes documentation config
- Tailwind CSS config
- Astro framework config

### Changed
- Optimized all framework configs
- Improved categorization accuracy
- Enhanced error messages

---

## [0.1.0] - 2025-10-05

### Added

#### Initial Release
- Basic documentation scraper functionality
- Manual skill creation
- Framework configs (Godot, React, Vue, Django, FastAPI)
- Smart categorization system
- Code language detection
- Pattern extraction
- Local and API-based enhancement options
- Basic packaging functionality

#### Core Features
- BFS traversal for documentation scraping
- CSS selector-based content extraction
- Smart categorization with scoring
- Code block detection and formatting
- Caching system for scraped data
- Interactive mode for config creation

#### Documentation
- README with quick start guide
- Basic usage documentation
- Configuration file examples

---

## Release Links

- [v1.2.0](https://github.com/yusufkaraaslan/Skill_Seekers/releases/tag/v1.2.0) - PDF Advanced Features
- [v1.1.0](https://github.com/yusufkaraaslan/Skill_Seekers/releases/tag/v1.1.0) - Documentation Scraping Enhancements
- [v1.0.0](https://github.com/yusufkaraaslan/Skill_Seekers/releases/tag/v1.0.0) - Production Release
- [v0.4.0](https://github.com/yusufkaraaslan/Skill_Seekers/releases/tag/v0.4.0) - Large Documentation Support
- [v0.3.0](https://github.com/yusufkaraaslan/Skill_Seekers/releases/tag/v0.3.0) - MCP Integration

---

## Version History Summary

| Version | Date | Highlights |
|---------|------|------------|
| **1.2.0** | 2025-10-23 | 📄 PDF advanced features: OCR, passwords, tables, 3x faster |
| **1.1.0** | 2025-10-22 | 🌐 Unlimited scraping, parallel mode, new configs (Ansible, Laravel) |
| **1.0.0** | 2025-10-19 | 🚀 Production release, auto-upload, 9 MCP tools |
| **0.4.0** | 2025-10-18 | 📚 Large docs support (40K+ pages) |
| **0.3.0** | 2025-10-15 | 🔌 MCP integration with Claude Code |
| **0.2.0** | 2025-10-10 | 🧪 Testing & optimization |
| **0.1.0** | 2025-10-05 | 🎬 Initial release |

---

[Unreleased]: https://github.com/yusufkaraaslan/Skill_Seekers/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/yusufkaraaslan/Skill_Seekers/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/yusufkaraaslan/Skill_Seekers/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/yusufkaraaslan/Skill_Seekers/compare/v0.4.0...v1.0.0
[0.4.0]: https://github.com/yusufkaraaslan/Skill_Seekers/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/yusufkaraaslan/Skill_Seekers/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/yusufkaraaslan/Skill_Seekers/releases/tag/v0.2.0
[0.1.0]: https://github.com/yusufkaraaslan/Skill_Seekers/releases/tag/v0.1.0
