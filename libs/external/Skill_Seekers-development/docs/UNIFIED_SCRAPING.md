# Unified Multi-Source Scraping

**Version:** 2.0 (Feature complete as of October 2025)

## Overview

Unified multi-source scraping allows you to combine knowledge from multiple sources into a single comprehensive Claude skill. Instead of choosing between documentation, GitHub repositories, or PDF manuals, you can now extract and intelligently merge information from all of them.

## Why Unified Scraping?

**The Problem**: Documentation and code often drift apart over time. Official docs might be outdated, missing features that exist in code, or documenting features that have been removed. Separately scraping docs and code creates two incomplete skills.

**The Solution**: Unified scraping:
- Extracts information from multiple sources (documentation, GitHub, PDFs)
- **Detects conflicts** between documentation and actual code implementation
- **Intelligently merges** conflicting information with transparency
- **Highlights discrepancies** with inline warnings (⚠️)
- Creates a single, comprehensive skill that shows the complete picture

## Quick Start

### 1. Create a Unified Config

Create a config file with multiple sources:

```json
{
  "name": "react",
  "description": "Complete React knowledge from docs + codebase",
  "merge_mode": "rule-based",
  "sources": [
    {
      "type": "documentation",
      "base_url": "https://react.dev/",
      "extract_api": true,
      "max_pages": 200
    },
    {
      "type": "github",
      "repo": "facebook/react",
      "include_code": true,
      "code_analysis_depth": "surface",
      "max_issues": 100
    }
  ]
}
```

### 2. Scrape and Build

```bash
python3 cli/unified_scraper.py --config configs/react_unified.json
```

The tool will:
1. ✅ **Phase 1**: Scrape all sources (docs + GitHub)
2. ✅ **Phase 2**: Detect conflicts between sources
3. ✅ **Phase 3**: Merge conflicts intelligently
4. ✅ **Phase 4**: Build unified skill with conflict transparency

### 3. Package and Upload

```bash
python3 cli/package_skill.py output/react/
```

## Config Format

### Unified Config Structure

```json
{
  "name": "skill-name",
  "description": "When to use this skill",
  "merge_mode": "rule-based|claude-enhanced",
  "sources": [
    {
      "type": "documentation|github|pdf",
      ...source-specific fields...
    }
  ]
}
```

### Documentation Source

```json
{
  "type": "documentation",
  "base_url": "https://docs.example.com/",
  "extract_api": true,
  "selectors": {
    "main_content": "article",
    "title": "h1",
    "code_blocks": "pre code"
  },
  "url_patterns": {
    "include": [],
    "exclude": ["/blog/"]
  },
  "categories": {
    "getting_started": ["intro", "tutorial"],
    "api": ["api", "reference"]
  },
  "rate_limit": 0.5,
  "max_pages": 200
}
```

### GitHub Source

```json
{
  "type": "github",
  "repo": "owner/repo",
  "github_token": "ghp_...",
  "include_issues": true,
  "max_issues": 100,
  "include_changelog": true,
  "include_releases": true,
  "include_code": true,
  "code_analysis_depth": "surface|deep|full",
  "file_patterns": [
    "src/**/*.js",
    "lib/**/*.ts"
  ]
}
```

**Code Analysis Depth**:
- `surface` (default): Basic structure, no code analysis
- `deep`: Extract class/function signatures, parameters, return types
- `full`: Complete AST analysis (expensive)

### PDF Source

```json
{
  "type": "pdf",
  "path": "/path/to/manual.pdf",
  "extract_tables": false,
  "ocr": false,
  "password": "optional-password"
}
```

## Conflict Detection

The unified scraper automatically detects 4 types of conflicts:

### 1. Missing in Documentation

**Severity**: Medium
**Description**: API exists in code but is not documented

**Example**:
```python
# Code has this method:
def move_local_x(self, delta: float, snap: bool = False) -> None:
    """Move node along local X axis"""

# But documentation doesn't mention it
```

**Suggestion**: Add documentation for this API

### 2. Missing in Code

**Severity**: High
**Description**: API is documented but not found in codebase

**Example**:
```python
# Docs say:
def rotate(angle: float) -> None

# But code doesn't have this function
```

**Suggestion**: Update documentation to remove this API, or add it to codebase

### 3. Signature Mismatch

**Severity**: Medium-High
**Description**: API exists in both but signatures differ

**Example**:
```python
# Docs say:
def move_local_x(delta: float)

# Code has:
def move_local_x(delta: float, snap: bool = False)
```

**Suggestion**: Update documentation to match actual signature

### 4. Description Mismatch

**Severity**: Low
**Description**: Different descriptions/docstrings

## Merge Modes

### Rule-Based Merge (Default)

Fast, deterministic merging using predefined rules:

1. **If API only in docs** → Include with `[DOCS_ONLY]` tag
2. **If API only in code** → Include with `[UNDOCUMENTED]` tag
3. **If both match perfectly** → Include normally
4. **If conflict exists** → Prefer code signature, keep docs description

**When to use**:
- Fast merging (< 1 second)
- Automated workflows
- You don't need human oversight

**Example**:
```bash
python3 cli/unified_scraper.py --config config.json --merge-mode rule-based
```

### Claude-Enhanced Merge

AI-powered reconciliation using local Claude Code:

1. Opens new terminal with Claude Code
2. Provides conflict context and instructions
3. Claude analyzes and creates reconciled API reference
4. Human can review and adjust before finalizing

**When to use**:
- Complex conflicts requiring judgment
- You want highest quality merge
- You have time for human oversight

**Example**:
```bash
python3 cli/unified_scraper.py --config config.json --merge-mode claude-enhanced
```

## Skill Output Structure

The unified scraper creates this structure:

```
output/skill-name/
├── SKILL.md                     # Main skill file with merged APIs
├── references/
│   ├── documentation/           # Documentation references
│   │   └── index.md
│   ├── github/                  # GitHub references
│   │   ├── README.md
│   │   ├── issues.md
│   │   └── releases.md
│   ├── pdf/                     # PDF references (if applicable)
│   │   └── index.md
│   ├── api/                     # Merged API reference
│   │   └── merged_api.md
│   └── conflicts.md             # Detailed conflict report
├── scripts/                     # Empty (for user scripts)
└── assets/                      # Empty (for user assets)
```

### SKILL.md Format

```markdown
# React

Complete React knowledge base combining official documentation and React codebase insights.

## 📚 Sources

This skill combines knowledge from multiple sources:

- ✅ **Documentation**: https://react.dev/
  - Pages: 200
- ✅ **GitHub Repository**: facebook/react
  - Code Analysis: surface
  - Issues: 100

## ⚠️ Data Quality

**5 conflicts detected** between sources.

**Conflict Breakdown:**
- missing_in_docs: 3
- missing_in_code: 2

See `references/conflicts.md` for detailed conflict information.

## 🔧 API Reference

*Merged from documentation and code analysis*

### ✅ Verified APIs

*Documentation and code agree*

#### `useState(initialValue)`

...

### ⚠️ APIs with Conflicts

*Documentation and code differ*

#### `useEffect(callback, deps?)`

⚠️ **Conflict**: Documentation signature differs from code implementation

**Documentation says:**
```
useEffect(callback: () => void, deps: any[])
```

**Code implementation:**
```
useEffect(callback: () => void | (() => void), deps?: readonly any[])
```

*Source: both*

---
```

## Examples

### Example 1: React (Docs + GitHub)

```json
{
  "name": "react",
  "description": "Complete React framework knowledge",
  "merge_mode": "rule-based",
  "sources": [
    {
      "type": "documentation",
      "base_url": "https://react.dev/",
      "extract_api": true,
      "max_pages": 200
    },
    {
      "type": "github",
      "repo": "facebook/react",
      "include_code": true,
      "code_analysis_depth": "surface"
    }
  ]
}
```

### Example 2: Django (Docs + GitHub)

```json
{
  "name": "django",
  "description": "Complete Django framework knowledge",
  "merge_mode": "rule-based",
  "sources": [
    {
      "type": "documentation",
      "base_url": "https://docs.djangoproject.com/en/stable/",
      "extract_api": true,
      "max_pages": 300
    },
    {
      "type": "github",
      "repo": "django/django",
      "include_code": true,
      "code_analysis_depth": "deep",
      "file_patterns": [
        "django/db/**/*.py",
        "django/views/**/*.py"
      ]
    }
  ]
}
```

### Example 3: Mixed Sources (Docs + GitHub + PDF)

```json
{
  "name": "godot",
  "description": "Complete Godot Engine knowledge",
  "merge_mode": "claude-enhanced",
  "sources": [
    {
      "type": "documentation",
      "base_url": "https://docs.godotengine.org/en/stable/",
      "extract_api": true,
      "max_pages": 500
    },
    {
      "type": "github",
      "repo": "godotengine/godot",
      "include_code": true,
      "code_analysis_depth": "deep"
    },
    {
      "type": "pdf",
      "path": "/path/to/godot_manual.pdf",
      "extract_tables": true
    }
  ]
}
```

## Command Reference

### Unified Scraper

```bash
# Basic usage
python3 cli/unified_scraper.py --config configs/react_unified.json

# Override merge mode
python3 cli/unified_scraper.py --config configs/react_unified.json --merge-mode claude-enhanced

# Use cached data (skip re-scraping)
python3 cli/unified_scraper.py --config configs/react_unified.json --skip-scrape
```

### Validate Config

```bash
python3 -c "
import sys
sys.path.insert(0, 'cli')
from config_validator import validate_config

validator = validate_config('configs/react_unified.json')
print(f'Format: {\"Unified\" if validator.is_unified else \"Legacy\"}')
print(f'Sources: {len(validator.config.get(\"sources\", []))}')
print(f'Needs API merge: {validator.needs_api_merge()}')
"
```

## MCP Integration

The unified scraper is fully integrated with MCP. The `scrape_docs` tool automatically detects unified vs legacy configs and routes to the appropriate scraper.

```python
# MCP tool usage
{
  "name": "scrape_docs",
  "arguments": {
    "config_path": "configs/react_unified.json",
    "merge_mode": "rule-based"  # Optional override
  }
}
```

The tool will:
1. Auto-detect unified format
2. Route to `unified_scraper.py`
3. Apply specified merge mode
4. Return comprehensive output

## Backward Compatibility

**Legacy configs still work!** The system automatically detects legacy single-source configs and routes to the original `doc_scraper.py`.

```json
// Legacy config (still works)
{
  "name": "react",
  "base_url": "https://react.dev/",
  ...
}

// Automatically detected as legacy format
// Routes to doc_scraper.py
```

## Testing

Run integration tests:

```bash
python3 cli/test_unified_simple.py
```

Tests validate:
- ✅ Unified config validation
- ✅ Backward compatibility with legacy configs
- ✅ Mixed source type support
- ✅ Error handling for invalid configs

## Architecture

### Components

1. **config_validator.py**: Validates unified and legacy configs
2. **code_analyzer.py**: Extracts code signatures at configurable depth
3. **conflict_detector.py**: Detects API conflicts between sources
4. **merge_sources.py**: Implements rule-based and Claude-enhanced merging
5. **unified_scraper.py**: Main orchestrator
6. **unified_skill_builder.py**: Generates final skill structure
7. **skill_seeker_mcp/server.py**: MCP integration with auto-detection

### Data Flow

```
Unified Config
     ↓
ConfigValidator (validates format)
     ↓
UnifiedScraper.run()
     ↓
┌────────────────────────────────────┐
│ Phase 1: Scrape All Sources        │
│  - Documentation → doc_scraper     │
│  - GitHub → github_scraper         │
│  - PDF → pdf_scraper               │
└────────────────────────────────────┘
     ↓
┌────────────────────────────────────┐
│ Phase 2: Detect Conflicts          │
│  - ConflictDetector                │
│  - Compare docs APIs vs code APIs  │
│  - Classify by type and severity   │
└────────────────────────────────────┘
     ↓
┌────────────────────────────────────┐
│ Phase 3: Merge Sources              │
│  - RuleBasedMerger (fast)          │
│  - OR ClaudeEnhancedMerger (AI)    │
│  - Create unified API reference    │
└────────────────────────────────────┘
     ↓
┌────────────────────────────────────┐
│ Phase 4: Build Skill                │
│  - UnifiedSkillBuilder             │
│  - Generate SKILL.md with conflicts│
│  - Create reference structure      │
│  - Generate conflicts report       │
└────────────────────────────────────┘
     ↓
Unified Skill (.zip ready)
```

## Best Practices

### 1. Start with Rule-Based Merge

Rule-based is fast and works well for most cases. Only use Claude-enhanced if you need human oversight.

### 2. Use Surface-Level Code Analysis

`code_analysis_depth: "surface"` is usually sufficient. Deep analysis is expensive and rarely needed.

### 3. Limit GitHub Issues

`max_issues: 100` is a good default. More than 200 issues rarely adds value.

### 4. Be Specific with File Patterns

```json
"file_patterns": [
  "src/**/*.js",     // Good: specific paths
  "lib/**/*.ts"
]

// Not recommended:
"file_patterns": ["**/*.js"]  // Too broad, slow
```

### 5. Monitor Conflict Reports

Always review `references/conflicts.md` to understand discrepancies between sources.

## Troubleshooting

### No Conflicts Detected

**Possible causes**:
- `extract_api: false` in documentation source
- `include_code: false` in GitHub source
- Code analysis found no APIs (check `code_analysis_depth`)

**Solution**: Ensure both sources have API extraction enabled

### Too Many Conflicts

**Possible causes**:
- Fuzzy matching threshold too strict
- Documentation uses different naming conventions
- Old documentation version

**Solution**: Review conflicts manually and adjust merge strategy

### Merge Takes Too Long

**Possible causes**:
- Using `code_analysis_depth: "full"` (very slow)
- Too many file patterns
- Large repository

**Solution**:
- Use `"surface"` or `"deep"` analysis
- Narrow file patterns
- Increase `rate_limit`

## Future Enhancements

Planned features:
- [ ] Automated conflict resolution strategies
- [ ] Conflict trend analysis across versions
- [ ] Multi-version comparison (docs v1 vs v2)
- [ ] Custom merge rules DSL
- [ ] Conflict confidence scores

## Support

For issues, questions, or suggestions:
- GitHub Issues: https://github.com/yusufkaraaslan/Skill_Seekers/issues
- Documentation: https://github.com/yusufkaraaslan/Skill_Seekers/docs

## Changelog

**v2.0 (October 2025)**: Unified multi-source scraping feature complete
- ✅ Config validation for unified format
- ✅ Deep code analysis with AST parsing
- ✅ Conflict detection (4 types, 3 severity levels)
- ✅ Rule-based merging
- ✅ Claude-enhanced merging
- ✅ Unified skill builder with inline conflict warnings
- ✅ MCP integration with auto-detection
- ✅ Backward compatibility with legacy configs
- ✅ Comprehensive tests and documentation
