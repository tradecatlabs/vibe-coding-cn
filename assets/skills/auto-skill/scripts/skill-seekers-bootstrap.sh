#!/usr/bin/env bash

set -euo pipefail

# ==================== Purpose ====================
# Bootstraps a local venv for the vendored Skill Seekers source code.
#
# Output:
# - Creates: skills/auto-skill/scripts/.venv-skill-seekers/

usage() {
  cat <<'EOF'
Usage:
  skill-seekers-bootstrap.sh [--venv <dir>]

Examples:
  ./skills/auto-skill/scripts/skill-seekers-bootstrap.sh
  ./skills/auto-skill/scripts/skill-seekers-bootstrap.sh --venv ./skills/auto-skill/scripts/.venv-skill-seekers
EOF
}

die() {
  echo "Error: $*" >&2
  exit 1
}

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
tool_dir="${script_dir}/Skill_Seekers-development"
default_venv="${script_dir}/.venv-skill-seekers"

venv_dir="$default_venv"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --venv)
      [[ $# -ge 2 ]] || die "--venv requires a directory argument"
      venv_dir="$2"
      shift 2
      ;;
    --)
      shift
      break
      ;;
    -*)
      die "Unknown argument: $1 (use --help)"
      ;;
    *)
      die "Unexpected positional argument: $1 (use --help)"
      ;;
  esac
done

[[ -d "$tool_dir" ]] || die "Missing vendored tool dir: $tool_dir"
[[ -f "$tool_dir/requirements.txt" ]] || die "Missing requirements.txt: $tool_dir/requirements.txt"
command -v python3 >/dev/null 2>&1 || die "python3 not found"

if [[ ! -d "$venv_dir" ]]; then
  python3 -m venv "$venv_dir"
fi

"$venv_dir/bin/python" -m pip install --upgrade pip >/dev/null
"$venv_dir/bin/pip" install -r "$tool_dir/requirements.txt"

echo "OK: venv ready: $venv_dir"
