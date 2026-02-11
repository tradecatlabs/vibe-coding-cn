# skills/skills-skills

This directory is a **meta-skill**: it turns arbitrary domain material (docs/APIs/code/specs) into a reusable Skill (`SKILL.md` + `references/` + `scripts/` + `assets/`), and ships an executable quality gate + scaffolding.

## Layout

```
skills-skills/
|-- AGENTS.md
|-- SKILL.md
|-- assets/
|   |-- template-minimal.md
|   `-- template-complete.md
|-- scripts/
|   |-- create-skill.sh
|   `-- validate-skill.sh
`-- references/
    |-- index.md
    |-- README.md
    |-- anti-patterns.md
    |-- quality-checklist.md
    `-- skill-spec.md
```

## File Responsibilities

- `skills/skills-skills/SKILL.md`: entrypoint (triggers, deliverables, workflow, quality gate, tooling).
- `skills/skills-skills/assets/template-minimal.md`: minimal template (small domains / quick bootstrap).
- `skills/skills-skills/assets/template-complete.md`: full template (production-grade / complex domains).
- `skills/skills-skills/scripts/create-skill.sh`: scaffold generator (minimal/full, output dir, overwrite).
- `skills/skills-skills/scripts/validate-skill.sh`: spec validator (supports `--strict`).
- `skills/skills-skills/references/index.md`: navigation for this meta-skill's reference docs.
- `skills/skills-skills/references/README.md`: upstream official reference (lightly adjusted to keep links working in this repo).
- `skills/skills-skills/references/skill-spec.md`: the local Skill spec (MUST/SHOULD/NEVER).
- `skills/skills-skills/references/quality-checklist.md`: quality gate checklist + scoring.
- `skills/skills-skills/references/anti-patterns.md`: common failure modes and how to fix them.

## Dependencies & Boundaries

- `scripts/*.sh`: depend only on `bash` + common POSIX tooling (`sed/awk/grep/find`), no network required.
- This directory is about "how to build Skills", not about any specific domain; domain knowledge belongs in `skills/<domain>/`.
