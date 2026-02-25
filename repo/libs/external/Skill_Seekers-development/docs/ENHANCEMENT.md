# AI-Powered SKILL.md Enhancement

Two scripts are available to dramatically improve your SKILL.md file:
1. **`enhance_skill_local.py`** - Uses Claude Code Max (no API key, **recommended**)
2. **`enhance_skill.py`** - Uses Anthropic API (~$0.15-$0.30 per skill)

Both analyze reference documentation and extract the best examples and guidance.

## Why Use Enhancement?

**Problem:** The auto-generated SKILL.md is often too generic:
- Empty Quick Reference section
- No practical code examples
- Generic "When to Use" triggers
- Doesn't highlight key features

**Solution:** Let Claude read your reference docs and create a much better SKILL.md with:
- ✅ Best code examples extracted from documentation
- ✅ Practical quick reference with real patterns
- ✅ Domain-specific guidance
- ✅ Clear navigation tips
- ✅ Key concepts explained

## Quick Start (LOCAL - No API Key)

**Recommended for Claude Code Max users:**

```bash
# Option 1: Standalone enhancement
python3 cli/enhance_skill_local.py output/steam-inventory/

# Option 2: Integrated with scraper
python3 cli/doc_scraper.py --config configs/steam-inventory.json --enhance-local
```

**What happens:**
1. Opens new terminal window
2. Runs Claude Code with enhancement prompt
3. Claude analyzes reference files (~15-20K chars)
4. Generates enhanced SKILL.md (30-60 seconds)
5. Terminal auto-closes when done

**Requirements:**
- Claude Code Max plan (you're already using it!)
- macOS (auto-launch works) or manual terminal run on other OS

## API-Based Enhancement (Alternative)

**If you prefer API-based approach:**

### Installation

```bash
pip3 install anthropic
```

### Setup API Key

```bash
# Option 1: Environment variable (recommended)
export ANTHROPIC_API_KEY=sk-ant-...

# Option 2: Pass directly with --api-key
python3 cli/enhance_skill.py output/react/ --api-key sk-ant-...
```

### Usage

```bash
# Standalone enhancement
python3 cli/enhance_skill.py output/steam-inventory/

# Integrated with scraper
python3 cli/doc_scraper.py --config configs/steam-inventory.json --enhance

# Dry run (see what would be done)
python3 cli/enhance_skill.py output/react/ --dry-run
```

## What It Does

1. **Reads reference files** (api_reference.md, webapi.md, etc.)
2. **Sends to Claude** with instructions to:
   - Extract 5-10 best code examples
   - Create practical quick reference
   - Write domain-specific "When to Use" triggers
   - Add helpful navigation guidance
3. **Backs up original** SKILL.md to SKILL.md.backup
4. **Saves enhanced version** as new SKILL.md

## Example Enhancement

### Before (Auto-Generated)
```markdown
## Quick Reference

### Common Patterns

*Quick reference patterns will be added as you use the skill.*
```

### After (AI-Enhanced)
```markdown
## Quick Reference

### Common API Patterns

**Granting promotional items:**
```cpp
void CInventory::GrantPromoItems()
{
    SteamItemDef_t newItems[2];
    newItems[0] = 110;
    newItems[1] = 111;
    SteamInventory()->AddPromoItems( &s_GenerateRequestResult, newItems, 2 );
}
```

**Getting all items in player inventory:**
```cpp
SteamInventoryResult_t resultHandle;
bool success = SteamInventory()->GetAllItems( &resultHandle );
```
[... 8 more practical examples ...]
```

## Cost Estimate

- **Input**: ~50,000-100,000 tokens (reference docs)
- **Output**: ~4,000 tokens (enhanced SKILL.md)
- **Model**: claude-sonnet-4-20250514
- **Estimated cost**: $0.15-$0.30 per skill

## Troubleshooting

### "No API key provided"
```bash
export ANTHROPIC_API_KEY=sk-ant-...
# or
python3 cli/enhance_skill.py output/react/ --api-key sk-ant-...
```

### "No reference files found"
Make sure you've run the scraper first:
```bash
python3 cli/doc_scraper.py --config configs/react.json
```

### "anthropic package not installed"
```bash
pip3 install anthropic
```

### Don't like the result?
```bash
# Restore original
mv output/steam-inventory/SKILL.md.backup output/steam-inventory/SKILL.md

# Try again (it may generate different content)
python3 cli/enhance_skill.py output/steam-inventory/
```

## Tips

1. **Run after scraping completes** - Enhancement works best with complete reference docs
2. **Review the output** - AI is good but not perfect, check the generated SKILL.md
3. **Keep the backup** - Original is saved as SKILL.md.backup
4. **Re-run if needed** - Each run may produce slightly different results
5. **Works offline after first run** - Reference files are local

## Real-World Results

**Test Case: steam-economy skill**
- **Before:** 75 lines, generic template, empty Quick Reference
- **After:** 570 lines, 10 practical API examples, key concepts explained
- **Time:** 60 seconds
- **Quality Rating:** 9/10

The LOCAL enhancement successfully:
- Extracted best HTTP/JSON examples from 24 pages of documentation
- Explained domain concepts (Asset Classes, Context IDs, Transaction Lifecycle)
- Created navigation guidance for beginners through advanced users
- Added best practices for security, economy design, and API integration

## Limitations

**LOCAL Enhancement (`enhance_skill_local.py`):**
- Requires Claude Code Max plan
- macOS auto-launch only (manual on other OS)
- Opens new terminal window
- Takes ~60 seconds

**API Enhancement (`enhance_skill.py`):**
- Requires Anthropic API key (paid)
- Cost: ~$0.15-$0.30 per skill
- Limited to ~100K tokens of reference input

**Both:**
- May occasionally miss the best examples
- Can't understand context beyond the reference docs
- Doesn't modify reference files (only SKILL.md)

## Enhancement Options Comparison

| Aspect | Manual Edit | LOCAL Enhancement | API Enhancement |
|--------|-------------|-------------------|-----------------|
| Time | 15-30 minutes | 30-60 seconds | 30-60 seconds |
| Code examples | You pick | AI picks best | AI picks best |
| Quick reference | Write yourself | Auto-generated | Auto-generated |
| Domain guidance | Your knowledge | From docs | From docs |
| Consistency | Varies | Consistent | Consistent |
| Cost | Free (your time) | Free (Max plan) | ~$0.20 per skill |
| Setup | None | None | API key needed |
| Quality | High (if expert) | 9/10 | 9/10 |
| **Recommended?** | For experts only | ✅ **Yes** | If no Max plan |

## When to Use

**Use enhancement when:**
- You want high-quality SKILL.md quickly
- Working with large documentation (50+ pages)
- Creating skills for unfamiliar frameworks
- Need practical code examples extracted
- Want consistent quality across multiple skills

**Skip enhancement when:**
- Budget constrained (use manual editing)
- Very small documentation (<10 pages)
- You know the framework intimately
- Documentation has no code examples

## Advanced: Customization

To customize how Claude enhances the SKILL.md, edit `enhance_skill.py` and modify the `_build_enhancement_prompt()` method around line 130.

Example customization:
```python
prompt += """
ADDITIONAL REQUIREMENTS:
- Focus on security best practices
- Include performance tips
- Add troubleshooting section
"""
```

## See Also

- [README.md](../README.md) - Main documentation
- [CLAUDE.md](CLAUDE.md) - Architecture guide
- [doc_scraper.py](../doc_scraper.py) - Main scraping tool
