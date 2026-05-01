#!/usr/bin/env bash

set -euo pipefail

# ==================== Purpose ====================
# Import Skill Seekers output/NAME/ into this repo's skills/NAME/.

usage() {
  cat <<'EOF'
Usage:
  skill-seekers-import.sh <skill-name> [--force]

Behavior:
  - Source: ./output/<skill-name>/
  - Dest:   ./skills/<skill-name>/
  - By default, refuses to overwrite an existing skills/<skill-name>/SKILL.md

Examples:
  ./skills/auto-skill/scripts/skill-seekers-import.sh react
  ./skills/auto-skill/scripts/skill-seekers-import.sh react --force
EOF
}

die() {
  echo "Error: $*" >&2
  exit 1
}

force=0
skill_name=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --force)
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
  die "skill-name must match ^[a-z][a-z0-9-]*$ (e.g. my-skill)"
fi

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../.." && pwd)"
src_dir="${repo_root}/output/${skill_name}"
dest_dir="${repo_root}/skills/${skill_name}"

[[ -d "$src_dir" ]] || die "Missing Skill Seekers output dir: $src_dir"
[[ -f "$src_dir/SKILL.md" ]] || die "Missing output SKILL.md: $src_dir/SKILL.md"

mkdir -p "$dest_dir"

if [[ -f "$dest_dir/SKILL.md" && "$force" -ne 1 ]]; then
  die "Refusing to overwrite existing: $dest_dir/SKILL.md (use --force)"
fi

rsync -a --delete "$src_dir"/ "$dest_dir"/

echo "OK: imported to: $dest_dir"
