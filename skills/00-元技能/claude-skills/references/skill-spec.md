# Skill Spec (This Repo)

This document defines what a "production-grade Skill" means in this repository. Use it as the source of truth when creating or refactoring anything under `skills/`.

Keywords: MUST / SHOULD / MAY / MUST NOT / SHOULD NOT are normative.

## 1. Directory & Naming

- A Skill MUST be a directory under `skills/` named after its `name` field.
- The directory name MUST match `^[a-z][a-z0-9-]*$`.
- The Skill entrypoint MUST be `SKILL.md` at the root of the skill directory.

## 2. Frontmatter (Required)

`SKILL.md` MUST start with YAML frontmatter:

```yaml
---
name: skill-name
description: "What it does + when to use (activation triggers)."
---
```

Rules:
- `name` MUST match `^[a-z][a-z0-9-]*$`.
- `name` SHOULD equal the directory name.
- `description` MUST be decidable and operational:
  - Good: "X development and debugging. Use when doing A/B/C."
  - Bad: "Helps with X."

## 3. SKILL.md Structure

### 3.1 Required Sections

`SKILL.md` SHOULD follow this section order, and in strict mode it MUST:

1. `## When to Use This Skill`
2. `## Not For / Boundaries`
3. `## Quick Reference`
4. `## Examples`
5. `## References`
6. `## Maintenance`

Rationale:
- Activation reliability depends on explicit triggers and boundaries.
- Usability depends on short patterns and reproducible examples.
- Maintainability depends on sources and navigable references.

### 3.2 Quick Reference Rules

- Quick Reference MUST contain short, directly usable patterns.
- Quick Reference MUST NOT become a documentation dump.
- Long explanations SHOULD go to `references/`.
- A good target is <= 20 patterns, but large domains may justify more.

### 3.3 Example Rules

- The Examples section MUST contain reproducible examples.
- Each example SHOULD specify:
  - input(s)
  - steps
  - expected output / acceptance criteria
- Pseudo-code MAY be used only if the platform is unavailable, and MUST be clearly labeled.

### 3.4 Boundaries Rules

- "Not For / Boundaries" MUST list:
  - explicit out-of-scope items (to prevent misfires)
  - required inputs and what to ask when missing (1-3 questions)

## 4. references/ (Long-form Docs)

- `references/` SHOULD exist when the domain has:
  - long docs
  - many edge cases
  - extensive APIs/CLIs/config surfaces
- If `references/` exists, it SHOULD include:
  - `references/index.md` as a navigation entrypoint

Guideline:
- `references/` is for evidence, depth, and navigation.
- `SKILL.md` is for execution: short patterns + examples + constraints.

## 5. scripts/ and assets/

- `scripts/` MAY contain helper automation (generators, validators, setup).
  - Scripts MUST be non-interactive by default.
  - Scripts MUST NOT require network access unless explicitly stated.
- `assets/` MAY contain templates, configs, or static resources.

## 6. Safety & Integrity

- Skills MUST NOT include secrets (API keys, tokens, credentials).
- Skills MUST NOT invent external facts.
  - If uncertain, they MUST include a verification path (where/how to check).
- Potentially destructive commands MUST be explicitly labeled and gated.

## 7. Maintenance Metadata

Each Skill SHOULD include a `## Maintenance` section with:
- sources (docs/repos/specs)
- last-updated date
- known limits / non-goals

## 8. Quality Gate

Before shipping, run the checklist in `quality-checklist.md` and (if available) the validator:

```bash
./skills/claude-skills/scripts/validate-skill.sh skills/<skill-name> --strict
```
