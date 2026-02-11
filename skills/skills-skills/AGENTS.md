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
|   |-- Skill_Seekers-development/
|   |-- create-skill.sh
|   |-- skill-seekers-bootstrap.sh
|   |-- skill-seekers-configs -> Skill_Seekers-development/configs
|   |-- skill-seekers-import.sh
|   |-- skill-seekers.sh
|   |-- skill-seekers-src -> Skill_Seekers-development/src
|   |-- skill-seekers-update.sh
|   `-- validate-skill.sh
`-- references/
    |-- index.md
    |-- README.md
    |-- anti-patterns.md
    |-- skill-seekers.md
    |-- quality-checklist.md
    `-- skill-spec.md
```

## File Responsibilities

- `skills/skills-skills/SKILL.md`: entrypoint (triggers, deliverables, workflow, quality gate, tooling).
- `skills/skills-skills/assets/template-minimal.md`: minimal template (small domains / quick bootstrap).
- `skills/skills-skills/assets/template-complete.md`: full template (production-grade / complex domains).
- `skills/skills-skills/scripts/create-skill.sh`: scaffold generator (minimal/full, output dir, overwrite).
- `skills/skills-skills/scripts/Skill_Seekers-development/`: vendored Skill Seekers source snapshot (code + configs; excludes upstream Markdown docs).
- `skills/skills-skills/scripts/skill-seekers-bootstrap.sh`: create a local venv and install deps for the vendored Skill Seekers tool.
- `skills/skills-skills/scripts/skill-seekers.sh`: run Skill Seekers from vendored source (docs/github/pdf -> output/<name>/).
- `skills/skills-skills/scripts/skill-seekers-import.sh`: import output/<name>/ into the canonical skills/<name>/ tree.
- `skills/skills-skills/scripts/skill-seekers-update.sh`: update the vendored source snapshot from upstream (network required).
- `skills/skills-skills/scripts/validate-skill.sh`: spec validator (supports `--strict`).
- `skills/skills-skills/references/index.md`: navigation for this meta-skill's reference docs.
- `skills/skills-skills/references/README.md`: upstream official reference (lightly adjusted to keep links working in this repo).
- `skills/skills-skills/references/skill-spec.md`: the local Skill spec (MUST/SHOULD/NEVER).
- `skills/skills-skills/references/quality-checklist.md`: quality gate checklist + scoring.
- `skills/skills-skills/references/anti-patterns.md`: common failure modes and how to fix them.
- `skills/skills-skills/references/skill-seekers.md`: how to use the vendored tool as a mandatory first-draft generator.

## Dependencies & Boundaries

- `scripts/*.sh`: depend on `bash` + common POSIX tooling; some scripts require extra tooling:
  - `skill-seekers-bootstrap.sh`: requires `python3` + `pip` (network required for PyPI).
  - `skill-seekers-update.sh`: requires `curl` + `tar` + `rsync` (network required).
- This directory is about "how to build Skills", not about any specific domain; domain knowledge belongs in `skills/<domain>/`.
