# assets/skills/auto-skill

This directory is a **meta-skill**: it turns arbitrary domain material (docs/APIs/code/specs) into a reusable Skill (`SKILL.md` + `references/` + `scripts/` + `assets/`), and ships an executable quality gate + scaffolding.

## Layout

```text
auto-skill/
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

- `assets/skills/auto-skill/SKILL.md`: entrypoint (triggers, deliverables, workflow, quality gate, tooling).
- `assets/skills/auto-skill/assets/template-minimal.md`: minimal template (small domains / quick bootstrap).
- `assets/skills/auto-skill/assets/template-complete.md`: full template (production-grade / complex domains).
- `assets/skills/auto-skill/scripts/create-skill.sh`: scaffold generator (minimal/full, output dir, overwrite).
- `assets/skills/auto-skill/scripts/Skill_Seekers-development/`: vendored Skill Seekers source snapshot (code + configs; excludes upstream Markdown docs).
- `assets/skills/auto-skill/scripts/skill-seekers-bootstrap.sh`: create a local venv and install deps for the vendored Skill Seekers tool.
- `assets/skills/auto-skill/scripts/skill-seekers.sh`: run Skill Seekers from vendored source (docs/github/pdf -> output/<name>/).
- `assets/skills/auto-skill/scripts/skill-seekers-import.sh`: import output/<name>/ into the canonical assets/skills/<name>/ tree.
- `assets/skills/auto-skill/scripts/skill-seekers-update.sh`: update the vendored source snapshot from upstream (network required).
- `assets/skills/auto-skill/scripts/validate-skill.sh`: spec validator (supports `--strict`).
- `assets/skills/auto-skill/references/index.md`: navigation for this meta-skill's reference docs.
- `assets/skills/auto-skill/references/README.md`: upstream official reference (lightly adjusted to keep links working in this repo).
- `assets/skills/auto-skill/references/skill-spec.md`: the local Skill spec (MUST/SHOULD/NEVER).
- `assets/skills/auto-skill/references/quality-checklist.md`: quality gate checklist + scoring.
- `assets/skills/auto-skill/references/anti-patterns.md`: common failure modes and how to fix them.
- `assets/skills/auto-skill/references/skill-seekers.md`: how to use the vendored tool as a mandatory first-draft generator.

## Dependencies & Boundaries

- `scripts/*.sh`: depend on `bash` + common POSIX tooling; some scripts require extra tooling:
  - `skill-seekers-bootstrap.sh`: requires `python3` + `pip` (network required for PyPI).
  - `skill-seekers-update.sh`: requires `curl` + `tar` + `rsync` (network required).
- This directory is about "how to build Skills", not about any specific domain; domain knowledge belongs in `assets/skills/<domain>/`.
