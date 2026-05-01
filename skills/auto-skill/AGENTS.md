# skills/auto-skill

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
|   |-- Skill_Seekers-development -> ../../../tools/external/Skill_Seekers-development
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

- `skills/auto-skill/SKILL.md`: entrypoint (triggers, deliverables, workflow, quality gate, tooling).
- `skills/auto-skill/assets/template-minimal.md`: minimal template (small domains / quick bootstrap).
- `skills/auto-skill/assets/template-complete.md`: full template (production-grade / complex domains).
- `skills/auto-skill/scripts/create-skill.sh`: scaffold generator (minimal/full, output dir, overwrite).
- `skills/auto-skill/scripts/Skill_Seekers-development`: relative symlink to the `tools/external/Skill_Seekers-development` submodule.
- `skills/auto-skill/scripts/skill-seekers-bootstrap.sh`: create a local venv and install deps for the linked Skill Seekers tool.
- `skills/auto-skill/scripts/skill-seekers.sh`: run Skill Seekers from the linked source (docs/github/pdf -> output/<name>/).
- `skills/auto-skill/scripts/skill-seekers-import.sh`: import output/<name>/ into the canonical skills/<name>/ tree.
- `skills/auto-skill/scripts/skill-seekers-update.sh`: legacy updater; guarded because the tool source now lives in `tools/external/`.
- `skills/auto-skill/scripts/validate-skill.sh`: spec validator (supports `--strict`).
- `skills/auto-skill/references/index.md`: navigation for this meta-skill's reference docs.
- `skills/auto-skill/references/README.md`: upstream official reference (lightly adjusted to keep links working in this repo).
- `skills/auto-skill/references/skill-spec.md`: the local Skill spec (MUST/SHOULD/NEVER).
- `skills/auto-skill/references/quality-checklist.md`: quality gate checklist + scoring.
- `skills/auto-skill/references/anti-patterns.md`: common failure modes and how to fix them.
- `skills/auto-skill/references/skill-seekers.md`: how to use the linked tool as a mandatory first-draft generator.

## Dependencies & Boundaries

- `scripts/*.sh`: depend on `bash` + common POSIX tooling; some scripts require extra tooling:
  - `skill-seekers-bootstrap.sh`: requires `python3` + `pip` (network required for PyPI).
  - `skill-seekers-update.sh`: legacy helper; do not use it to overwrite the linked `tools/external/` source.
- This directory is about "how to build Skills", not about any specific domain; domain knowledge belongs in `skills/<domain>/`.
