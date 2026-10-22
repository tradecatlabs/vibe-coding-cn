# Quality Checklist (Production Gate)

Use this checklist to decide whether a Skill is shippable. It is intentionally biased toward reliability and maintainability over "more content".

## Scoring

Score each item:
- 2 = fully satisfied
- 1 = partially satisfied / needs work
- 0 = missing

Suggested ship threshold:
- Total score >= 24 (out of 32)
- No "critical" item below 2

## A. Activation Reliability (Critical)

1. Frontmatter `name` matches `^[a-z][a-z0-9-]*$` and matches directory name (2)
2. Frontmatter `description` is decidable ("what + when") with concrete keywords (2)
3. `## When to Use This Skill` lists concrete tasks/inputs/goals (2)
4. `## Not For / Boundaries` exists and meaningfully prevents misfires (2)

## B. Usability (Critical)

5. `## Quick Reference` is short and directly usable (no doc dumps) (2)
6. Quick Reference patterns are formatted for copy/paste (2)
7. `## Examples` contains >= 3 reproducible examples (2)
8. Examples include acceptance criteria / expected output (2)

## C. Evidence & Correctness

9. `## Maintenance` lists sources (docs/repos/specs) and last-updated date (2)
10. Uncertain external details include a verification path (2)
11. Terminology is consistent (one concept, one name) (2)
12. No contradictions between Quick Reference and Examples (2)

## D. Structure & Maintainability

13. Long-form content lives in `references/` with `references/index.md` navigation (2)
14. Reference files are split by topic (not one giant file) (2)
15. The skill reads like an operator manual (task -> steps -> acceptance) (2)
16. Optional: scripts/assets are minimal and clearly scoped (2)

## Common Reasons to Fail the Gate

- Vague activation ("helps with X") with no boundaries
- Quick Reference contains pasted documentation instead of patterns
- Examples are not reproducible (no inputs, no steps, no expected output)
- No sources and no update date (cannot be trusted or maintained)
