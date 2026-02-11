#!/usr/bin/env bash

set -euo pipefail

# ==================== Help ====================

usage() {
  cat <<'EOF'
Usage:
  create-skill.sh <skill-name> [--minimal|--full] [--output <dir>] [--force]

Notes:
  - <skill-name> MUST be lowercase, start with a letter, and only contain letters, digits, and hyphens
  - Default mode: --full
  - Default output: current directory (creates ./<skill-name>/)

Examples:
  ./skills/claude-skills/scripts/create-skill.sh postgresql --full --output skills
  ./skills/claude-skills/scripts/create-skill.sh my-api --minimal
EOF
}

die() {
  echo "Error: $*" >&2
  exit 1
}

# ==================== Arg Parsing ====================

skill_name=""
mode="full"
output_dir="."
force=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --minimal)
      mode="minimal"
      shift
      ;;
    --full)
      mode="full"
      shift
      ;;
    -o|--output)
      [[ $# -ge 2 ]] || die "--output requires a directory argument"
      output_dir="$2"
      shift 2
      ;;
    -f|--force)
      force=1
      shift
      ;;
    --)
      shift
      break
      ;;
    -*)
      die "Unknown argument: $1 (use --help)"
      ;;
    *)
      if [[ -z "$skill_name" ]]; then
        skill_name="$1"
        shift
      else
        die "Extra argument: $1 (only one <skill-name> is allowed)"
      fi
      ;;
  esac
done

[[ -n "$skill_name" ]] || { usage; exit 1; }

if [[ ! "$skill_name" =~ ^[a-z][a-z0-9-]*$ ]]; then
  die "skill-name must be lowercase, start with a letter, and only contain letters/digits/hyphens (e.g. my-skill-name)"
fi

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
assets_dir="${script_dir}/../assets"

template_path=""
case "$mode" in
  minimal) template_path="${assets_dir}/template-minimal.md" ;;
  full) template_path="${assets_dir}/template-complete.md" ;;
  *) die "Internal error: unknown mode=$mode" ;;
esac

[[ -f "$template_path" ]] || die "Template not found: $template_path"

mkdir -p "$output_dir"

target_dir="${output_dir%/}/${skill_name}"

if [[ -e "$target_dir" && "$force" -ne 1 ]]; then
  die "Target already exists: $target_dir (use --force to overwrite)"
fi

mkdir -p "$target_dir"/{assets,scripts,references}

# ==================== Write Files ====================

render_template() {
  local src="$1"
  local dest="$2"
  sed "s/{{skill_name}}/${skill_name}/g" "$src" > "$dest"
}

render_template "$template_path" "$target_dir/SKILL.md"

cat > "$target_dir/references/index.md" <<EOF
# ${skill_name} Reference Index

## Quick Links

- Getting started: \`getting_started.md\`
- API/CLI/config: \`api.md\` (if applicable)
- Examples: \`examples.md\`
- Troubleshooting: \`troubleshooting.md\`

## Notes

- Put long-form content here: excerpts, evidence links, edge cases, FAQ
- Keep \`SKILL.md\` Quick Reference short and directly usable
EOF

if [[ "$mode" == "full" ]]; then
  cat > "$target_dir/references/getting_started.md" <<'EOF'
# Getting Started & Vocabulary

## Goals

- Define the 10 most important terms in this domain
- Provide the shortest path from zero to working
EOF

  cat > "$target_dir/references/api.md" <<'EOF'
# API / CLI / Config Reference (If Applicable)

## Suggested Structure

- Organize by use case, not alphabetically
- Key parameters: defaults, boundaries, common misuse
- Common errors: message -> cause -> fix steps
EOF

  cat > "$target_dir/references/examples.md" <<'EOF'
# Long Examples

Put examples longer than ~20 lines here, split by use case:

- Use case 1: ...
- Use case 2: ...
EOF

  cat > "$target_dir/references/troubleshooting.md" <<'EOF'
# Troubleshooting & Edge Cases

Write as: symptom -> likely causes -> diagnosis -> fix.
EOF
fi

# ==================== Summary ====================

echo ""
echo "OK: Skill generated: $target_dir/"
echo ""
echo "Layout:"
echo "  $target_dir/"
echo "  |-- SKILL.md"
echo "  |-- assets/"
echo "  |-- scripts/"
echo "  \\-- references/"
echo "      \\-- index.md"
echo ""
echo "Next steps:"
echo "  1) Edit $target_dir/SKILL.md (triggers/boundaries/quick reference/examples)"
echo "  2) Put long-form docs into $target_dir/references/ and update index.md"
