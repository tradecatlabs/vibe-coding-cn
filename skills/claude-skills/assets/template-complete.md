---
name: {{skill_name}}
description: "[Domain] end-to-end capability: includes [capability 1], [capability 2], [capability 3]. Use when [decidable triggers]."
---

# {{skill_name}} Skill

Production-grade skill for [domain]: extract rules, patterns, and reproducible examples from source material (avoid documentation dumps).

## When to Use This Skill

Trigger when any of these applies:
- You are designing/implementing/debugging [domain/tech]
- You need to turn requirements into concrete commands/code/configs
- You need common pitfalls, boundaries, and acceptance criteria

## Not For / Boundaries

- What this skill will not do (prevents misfires and over-promising)
- Required inputs; ask 1-3 questions if missing

## Quick Reference

### Common Patterns

**Pattern 1:** one-line explanation
```text
[command/snippet you can paste and run]
```

**Pattern 2:**
```text
[command/snippet you can paste and run]
```

## Rules & Constraints

- MUST: non-negotiable rules (security boundaries, defaults, acceptance)
- SHOULD: strong recommendations (best practices, performance habits)
- NEVER: explicit prohibitions (dangerous ops, inventing facts)

## Examples

### Example 1
- Input:
- Steps:
- Expected output / acceptance:

### Example 2

### Example 3

## FAQ

- Q: ...
  - A: ...

## Troubleshooting

- Symptom -> Likely causes -> Diagnosis -> Fix

## References

- `references/index.md`: navigation
- `references/getting_started.md`: onboarding and vocabulary
- `references/api.md`: API/CLI/config reference (if applicable)
- `references/examples.md`: long examples and extra use cases
- `references/troubleshooting.md`: edge cases and failure modes

## Maintenance

- Sources: docs/repos/specs (do not invent)
- Last updated: YYYY-MM-DD
- Known limits: what is explicitly out of scope

## Quality Gate

Minimum checks before shipping (see meta-skill `claude-skills` for the full version):

1. `description` is decidable ("what + when") and includes trigger keywords
2. Has "When to Use This Skill" with decidable triggers
3. Has "Not For / Boundaries" to reduce misfires
4. Quick Reference is <= 20 patterns and each is directly usable
5. Has >= 3 reproducible examples (input -> steps -> acceptance)
6. Long content is in `references/` with a navigable `references/index.md`
7. Uncertain claims include a verification path (no bluffing)
8. No documentation dumps in Quick Reference
9. Reads like an operator's manual, not a knowledge dump
