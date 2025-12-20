# Handling Large Documentation Sites (10K+ Pages)

Complete guide for scraping and managing large documentation sites with Skill Seeker.

---

## Table of Contents

- [When to Split Documentation](#when-to-split-documentation)
- [Split Strategies](#split-strategies)
- [Quick Start](#quick-start)
- [Detailed Workflows](#detailed-workflows)
- [Best Practices](#best-practices)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

---

## When to Split Documentation

### Size Guidelines

| Documentation Size | Recommendation | Strategy |
|-------------------|----------------|----------|
| < 5,000 pages | **One skill** | No splitting needed |
| 5,000 - 10,000 pages | **Consider splitting** | Category-based |
| 10,000 - 30,000 pages | **Recommended** | Router + Categories |
| 30,000+ pages | **Strongly recommended** | Router + Categories |

### Why Split Large Documentation?

**Benefits:**
- ✅ Faster scraping (parallel execution)
- ✅ More focused skills (better Claude performance)
- ✅ Easier maintenance (update one topic at a time)
- ✅ Better user experience (precise answers)
- ✅ Avoids context window limits

**Trade-offs:**
- ⚠️ Multiple skills to manage
- ⚠️ Initial setup more complex
- ⚠️ Router adds one extra skill

---

## Split Strategies

### 1. **No Split** (One Big Skill)
**Best for:** Small to medium documentation (< 5K pages)

```bash
# Just use the config as-is
python3 cli/doc_scraper.py --config configs/react.json
```

**Pros:** Simple, one skill to maintain
**Cons:** Can be slow for large docs, may hit limits

---

### 2. **Category Split** (Multiple Focused Skills)
**Best for:** 5K-15K pages with clear topic divisions

```bash
# Auto-split by categories
python3 cli/split_config.py configs/godot.json --strategy category

# Creates:
# - godot-scripting.json
# - godot-2d.json
# - godot-3d.json
# - godot-physics.json
# - etc.
```

**Pros:** Focused skills, clear separation
**Cons:** User must know which skill to use

---

### 3. **Router + Categories** (Intelligent Hub) ⭐ RECOMMENDED
**Best for:** 10K+ pages, best user experience

```bash
# Create router + sub-skills
python3 cli/split_config.py configs/godot.json --strategy router

# Creates:
# - godot.json (router/hub)
# - godot-scripting.json
# - godot-2d.json
# - etc.
```

**Pros:** Best of both worlds, intelligent routing, natural UX
**Cons:** Slightly more complex setup

---

### 4. **Size-Based Split**
**Best for:** Docs without clear categories

```bash
# Split every 5000 pages
python3 cli/split_config.py configs/bigdocs.json --strategy size --target-pages 5000

# Creates:
# - bigdocs-part1.json
# - bigdocs-part2.json
# - bigdocs-part3.json
# - etc.
```

**Pros:** Simple, predictable
**Cons:** May split related topics

---

## Quick Start

### Option 1: Automatic (Recommended)

```bash
# 1. Create config
python3 cli/doc_scraper.py --interactive
# Name: godot
# URL: https://docs.godotengine.org
# ... fill in prompts ...

# 2. Estimate pages (discovers it's large)
python3 cli/estimate_pages.py configs/godot.json
# Output: ⚠️  40,000 pages detected - splitting recommended

# 3. Auto-split with router
python3 cli/split_config.py configs/godot.json --strategy router

# 4. Scrape all sub-skills
for config in configs/godot-*.json; do
  python3 cli/doc_scraper.py --config $config &
done
wait

# 5. Generate router
python3 cli/generate_router.py configs/godot-*.json

# 6. Package all
python3 cli/package_multi.py output/godot*/

# 7. Upload all .zip files to Claude
```

---

### Option 2: Manual Control

```bash
# 1. Define split in config
nano configs/godot.json

# Add:
{
  "split_strategy": "router",
  "split_config": {
    "target_pages_per_skill": 5000,
    "create_router": true,
    "split_by_categories": ["scripting", "2d", "3d", "physics"]
  }
}

# 2. Split
python3 cli/split_config.py configs/godot.json

# 3. Continue as above...
```

---

## Detailed Workflows

### Workflow 1: Router + Categories (40K Pages)

**Scenario:** Godot documentation (40,000 pages)

**Step 1: Estimate**
```bash
python3 cli/estimate_pages.py configs/godot.json

# Output:
# Estimated: 40,000 pages
# Recommended: Split into 8 skills (5K each)
```

**Step 2: Split Configuration**
```bash
python3 cli/split_config.py configs/godot.json --strategy router --target-pages 5000

# Creates:
# configs/godot.json (router)
# configs/godot-scripting.json (5K pages)
# configs/godot-2d.json (8K pages)
# configs/godot-3d.json (10K pages)
# configs/godot-physics.json (6K pages)
# configs/godot-shaders.json (11K pages)
```

**Step 3: Scrape Sub-Skills (Parallel)**
```bash
# Open multiple terminals or use background jobs
python3 cli/doc_scraper.py --config configs/godot-scripting.json &
python3 cli/doc_scraper.py --config configs/godot-2d.json &
python3 cli/doc_scraper.py --config configs/godot-3d.json &
python3 cli/doc_scraper.py --config configs/godot-physics.json &
python3 cli/doc_scraper.py --config configs/godot-shaders.json &

# Wait for all to complete
wait

# Time: 4-8 hours (parallel) vs 20-40 hours (sequential)
```

**Step 4: Generate Router**
```bash
python3 cli/generate_router.py configs/godot-*.json

# Creates:
# output/godot/SKILL.md (router skill)
```

**Step 5: Package All**
```bash
python3 cli/package_multi.py output/godot*/

# Creates:
# output/godot.zip (router)
# output/godot-scripting.zip
# output/godot-2d.zip
# output/godot-3d.zip
# output/godot-physics.zip
# output/godot-shaders.zip
```

**Step 6: Upload to Claude**
Upload all 6 .zip files to Claude. The router will intelligently direct queries to the right sub-skill!

---

### Workflow 2: Category Split Only (15K Pages)

**Scenario:** Vue.js documentation (15,000 pages)

**No router needed - just focused skills:**

```bash
# 1. Split
python3 cli/split_config.py configs/vue.json --strategy category

# 2. Scrape each
for config in configs/vue-*.json; do
  python3 cli/doc_scraper.py --config $config
done

# 3. Package
python3 cli/package_multi.py output/vue*/

# 4. Upload all to Claude
```

**Result:** 5 focused Vue skills (components, reactivity, routing, etc.)

---

## Best Practices

### 1. **Choose Target Size Wisely**

```bash
# Small focused skills (3K-5K pages) - more skills, very focused
python3 cli/split_config.py config.json --target-pages 3000

# Medium skills (5K-8K pages) - balanced (RECOMMENDED)
python3 cli/split_config.py config.json --target-pages 5000

# Larger skills (8K-10K pages) - fewer skills, broader
python3 cli/split_config.py config.json --target-pages 8000
```

### 2. **Use Parallel Scraping**

```bash
# Serial (slow - 40 hours)
for config in configs/godot-*.json; do
  python3 cli/doc_scraper.py --config $config
done

# Parallel (fast - 8 hours) ⭐
for config in configs/godot-*.json; do
  python3 cli/doc_scraper.py --config $config &
done
wait
```

### 3. **Test Before Full Scrape**

```bash
# Test with limited pages first
nano configs/godot-2d.json
# Set: "max_pages": 50

python3 cli/doc_scraper.py --config configs/godot-2d.json

# If output looks good, increase to full
```

### 4. **Use Checkpoints for Long Scrapes**

```bash
# Enable checkpoints in config
{
  "checkpoint": {
    "enabled": true,
    "interval": 1000
  }
}

# If scrape fails, resume
python3 cli/doc_scraper.py --config config.json --resume
```

---

## Examples

### Example 1: AWS Documentation (Hypothetical 50K Pages)

```bash
# 1. Split by AWS services
python3 cli/split_config.py configs/aws.json --strategy router --target-pages 5000

# Creates ~10 skills:
# - aws (router)
# - aws-compute (EC2, Lambda)
# - aws-storage (S3, EBS)
# - aws-database (RDS, DynamoDB)
# - etc.

# 2. Scrape in parallel (overnight)
# 3. Upload all skills to Claude
# 4. User asks "How do I create an S3 bucket?"
# 5. Router activates aws-storage skill
# 6. Focused, accurate answer!
```

### Example 2: Microsoft Docs (100K+ Pages)

```bash
# Too large even with splitting - use selective categories

# Only scrape key topics
python3 cli/split_config.py configs/microsoft.json --strategy category

# Edit configs to include only:
# - microsoft-azure (Azure docs only)
# - microsoft-dotnet (.NET docs only)
# - microsoft-typescript (TS docs only)

# Skip less relevant sections
```

---

## Troubleshooting

### Issue: "Splitting creates too many skills"

**Solution:** Increase target size or combine categories

```bash
# Instead of 5K per skill, use 8K
python3 cli/split_config.py config.json --target-pages 8000

# Or manually combine categories in config
```

### Issue: "Router not routing correctly"

**Solution:** Check routing keywords in router SKILL.md

```bash
# Review router
cat output/godot/SKILL.md

# Update keywords if needed
nano output/godot/SKILL.md
```

### Issue: "Parallel scraping fails"

**Solution:** Reduce parallelism or check rate limits

```bash
# Scrape 2-3 at a time instead of all
python3 cli/doc_scraper.py --config config1.json &
python3 cli/doc_scraper.py --config config2.json &
wait

python3 cli/doc_scraper.py --config config3.json &
python3 cli/doc_scraper.py --config config4.json &
wait
```

---

## Summary

**For 40K+ Page Documentation:**

1. ✅ **Estimate first**: `python3 cli/estimate_pages.py config.json`
2. ✅ **Split with router**: `python3 cli/split_config.py config.json --strategy router`
3. ✅ **Scrape in parallel**: Multiple terminals or background jobs
4. ✅ **Generate router**: `python3 cli/generate_router.py configs/*-*.json`
5. ✅ **Package all**: `python3 cli/package_multi.py output/*/`
6. ✅ **Upload to Claude**: All .zip files

**Result:** Intelligent, fast, focused skills that work seamlessly together!

---

**Questions? See:**
- [Main README](../README.md)
- [MCP Setup Guide](MCP_SETUP.md)
- [Enhancement Guide](ENHANCEMENT.md)
