---
name: auto-skill
description: "Claude Skills meta-skill: extract domain material (docs/APIs/code/specs) into a reusable Skill (SKILL.md + references/scripts/assets), and refactor existing Skills for clarity, activation reliability, and quality gates."
---

# Auto Skill

Turn scattered domain material into a Skill that is reusable, maintainable, and reliably activatable:
- `SKILL.md` as the entrypoint (triggers, constraints, patterns, examples)
- `references/` for long-form evidence and navigation
- optional `scripts/` and `assets/` for scaffolding and templates

## When to Use This Skill

Trigger this meta-skill when you need to:
- Create a new Skill from scratch from docs/specs/repos
- Refactor an existing Skill (too long, unclear, inconsistent, misfires)
- Design reliable activation (frontmatter + triggers + boundaries)
- Extract a clean Quick Reference from large material
- Split long content into navigable `references/`
- Add a quality gate and a validator

## Not For / Boundaries

This meta-skill is NOT:
- A domain Skill by itself (it builds domain Skills)
- A license to invent external facts (if the material does not prove it, say so and add a verification path)
- A substitute for required inputs (if inputs are missing, ask 1-3 questions before proceeding)

## Quick Reference

### Deliverables (What You Must Produce)

Your output MUST include:
1. A concrete directory layout (typically `assets/skills/<skill-name>/`)
2. An actionable `SKILL.md` with decidable triggers, boundaries, and reproducible examples
3. Long-form docs moved to `references/` with a `references/index.md`
4. A pre-delivery checklist (Quality Gate)

### Built-in Tool (Mandatory): Skill Seekers (Linked)

This meta-skill exposes the `assets/repos/Skill_Seekers-development` submodule through a relative symlink so you can generate a first-draft Skill from:
- Documentation websites
- GitHub repositories
- PDFs

Bootstrap dependencies (once):

```bash
./assets/skills/auto-skill/scripts/skill-seekers-bootstrap.sh
```

Run Skill Seekers (from linked source):

```bash
./assets/skills/auto-skill/scripts/skill-seekers.sh -- --version
./assets/skills/auto-skill/scripts/skill-seekers.sh -- scrape --config ./assets/skills/auto-skill/scripts/Skill_Seekers-development/configs/react.json
./assets/skills/auto-skill/scripts/skill-seekers.sh -- github --repo facebook/react --name react
```

Import the generated skill into this repo's canonical `assets/skills/` tree:

```bash
./assets/skills/auto-skill/scripts/skill-seekers-import.sh react
./assets/skills/auto-skill/scripts/skill-seekers-import.sh react --force
```

Update the linked source by moving the `assets/repos/Skill_Seekers-development` submodule pointer directly. The legacy updater is guarded to avoid overwriting the linked repository.

```bash
./assets/skills/auto-skill/scripts/skill-seekers-update.sh --dry-run
```

### Recommended Layout (Minimal -> Full)

```
skill-name/
|-- SKILL.md              # Required: entrypoint with YAML frontmatter
|-- references/           # Optional: long-form docs/evidence/index
|   `-- index.md          # Recommended: navigation index
|-- scripts/              # Optional: helpers/automation
`-- assets/               # Optional: templates/configs/static assets
```

The truly minimal version is just `SKILL.md` (you can add `references/` later).

### YAML Frontmatter (Required)

```yaml
---
name: skill-name
description: "What it does + when to use (activation triggers)."
---
```

Frontmatter rules:
- `name` MUST match `^[a-z][a-z0-9-]*$` and SHOULD match the directory name
- `description` MUST be decidable (not "helps with X") and include concrete trigger keywords

### Minimal `SKILL.md` Skeleton (Copy/Paste)

```markdown
---
name: my-skill
description: "[Domain] capability: includes [capability 1], [capability 2]. Use when [decidable triggers]."
---

# my-skill Skill

One sentence that states the boundary and the deliverable.

## When to Use This Skill

Trigger when any of these applies:
- [Trigger 1: concrete task/keyword]
- [Trigger 2]
- [Trigger 3]

## Not For / Boundaries

- What this skill will not do (prevents misfires and over-promising)
- Required inputs; ask 1-3 questions if missing

## Quick Reference

### Common Patterns

**Pattern 1:** one-line explanation
```text
[command/snippet you can paste and run]
```

## Examples

### Example 1
- Input:
- Steps:
- Expected output / acceptance:

### Example 2

### Example 3

## References

- `references/index.md`: navigation
- `references/...`: long-form docs split by topic

## Maintenance

- Sources: docs/repos/specs (do not invent)
- Last updated: YYYY-MM-DD
- Known limits: what is explicitly out of scope
```

### Authoring Rules (Non-negotiable)

1. Quick Reference is for short, directly usable patterns
   - Keep it <= 20 patterns when possible.
   - Anything that needs paragraphs of explanation goes to `references/`.
2. Activation must be decidable
   - Frontmatter `description` should say "what + when" with concrete keywords.
   - "When to Use" must list specific tasks/inputs/goals, not vague help text.
   - "Not For / Boundaries" is mandatory for reliability.
3. No bluffing on external details
   - If the material does not prove it, say so and include a verification path.

### Workflow (Material -> Skill)

Do not skip steps:
0. If your source material is a docs site / GitHub repo / PDF: generate a first draft with the linked Skill Seekers tool, then import into `assets/skills/<skill-name>/`
1. Scope: write MUST/SHOULD/NEVER (three sentences total is fine)
2. Extract patterns: pick 10-20 high-frequency patterns (commands/snippets/flows)
3. Add examples: >= 3 end-to-end examples (input -> steps -> acceptance)
4. Define boundaries: what is out-of-scope + required inputs
5. Split references: move long text into `references/` + write `references/index.md`
6. Apply the gate: run the checklist and the validator

### Quality Gate (Pre-delivery Checklist)

Minimum checks (see `references/quality-checklist.md` for the full version):
1. `name` matches `^[a-z][a-z0-9-]*$` and matches the directory name
2. `description` states "what + when" with concrete trigger keywords
3. Has "When to Use This Skill" with decidable triggers
4. Has "Not For / Boundaries" to reduce misfires
5. Quick Reference is <= 20 patterns and each is directly usable
6. Has >= 3 reproducible examples
7. Long content is in `references/` and `references/index.md` is navigable
8. Uncertain claims include a verification path (no bluffing)
9. Reads like an operator's manual, not a documentation dump

Validate locally:

```bash
# From repo root (basic validation)
./assets/skills/auto-skill/scripts/validate-skill.sh assets/skills/<skill-name>

# From repo root (strict validation)
./assets/skills/auto-skill/scripts/validate-skill.sh assets/skills/<skill-name> --strict

# From assets/skills/auto-skill/ (basic validation)
./scripts/validate-skill.sh ../<skill-name>

# From assets/skills/auto-skill/ (strict validation)
./scripts/validate-skill.sh ../<skill-name> --strict
```

### Tools & Templates

Generate a new Skill skeleton:

```bash
# From repo root (generate into ./assets/skills/)
./assets/skills/auto-skill/scripts/create-skill.sh my-skill --full --output assets/skills

# From auto-skill/ (generate into ../ i.e. ./assets/skills/)
./scripts/create-skill.sh my-skill --full --output ..

# Minimal skeleton
./assets/skills/auto-skill/scripts/create-skill.sh my-skill --minimal --output assets/skills
```

Templates:
- `assets/template-minimal.md`
- `assets/template-complete.md`

## Examples

### Example 1: Create a Skill from Docs

- Input: an official doc/spec + 2-3 real code samples + common failure modes
- Steps:
  1. Run `create-skill.sh` to scaffold `assets/skills/<skill-name>/`
  2. Write frontmatter `description` as "what + when"
  3. Extract 10-20 high-frequency patterns into Quick Reference
  4. Add >= 3 end-to-end examples with acceptance criteria
  5. Put long content into `references/` and wire `references/index.md`
  6. Run `validate-skill.sh --strict` and iterate

### Example 2: Refactor a "Doc Dump" Skill

- Input: an existing `SKILL.md` with long pasted documentation
- Steps:
  1. Identify which parts are patterns vs. long-form explanation
  2. Move long-form text into `references/` (split by topic)
  3. Rewrite Quick Reference as short copy/paste patterns
  4. Add or fix Examples until they are reproducible
  5. Add "Not For / Boundaries" to reduce misfires

### Example 3: Validate and Gate a Skill

- Input: `assets/skills/<skill-name>/`
- Steps:
  1. Run `validate-skill.sh` (non-strict) to get warnings
  2. Fix frontmatter/name mismatches and missing sections
  3. Run `validate-skill.sh --strict` to enforce the spec
  4. Run the scoring rubric in `references/quality-checklist.md` before shipping

## References

Local docs:
- `references/index.md`
- `references/skill-spec.md`
- `references/quality-checklist.md`
- `references/anti-patterns.md`
- `references/README.md` (upstream official reference)
- `references/skill-seekers.md` (linked tool integration + workflow)

External (official):
- https://support.claude.com/en/articles/12512176-what-are-skills
- https://support.claude.com/en/articles/12512180-using-skills-in-claude
- https://support.claude.com/en/articles/12512198-creating-custom-skills
- https://docs.claude.com/en/api/skills-guide

## Maintenance

- Sources: local spec files in `assets/skills/auto-skill/references/` + upstream official docs in `references/README.md`
- Last updated: 2025-12-14
- Known limits: `validate-skill.sh` is heuristic; strict mode assumes the recommended section headings
