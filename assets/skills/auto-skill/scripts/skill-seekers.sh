#!/usr/bin/env bash

set -euo pipefail

# ==================== Purpose ====================
# Run Skill Seekers from vendored source with a local venv.
#
# This script does NOT auto-install dependencies.
# Run skill-seekers-bootstrap.sh once if you see ImportError.

usage() {
  cat <<'EOF'
Usage:
  skill-seekers.sh [--venv <dir>] -- <skill-seekers args...>

Examples:
  ./skills/auto-skill/scripts/skill-seekers.sh -- --version
  ./skills/auto-skill/scripts/skill-seekers.sh -- scrape --config ./skills/auto-skill/scripts/Skill_Seekers-development/configs/react.json
  ./skills/auto-skill/scripts/skill-seekers.sh -- github --repo facebook/react --name react
EOF
}

die() {
  echo "Error: $*" >&2
  exit 1
}

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
tool_dir="${script_dir}/Skill_Seekers-development"
tool_src="${tool_dir}/src"
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
    *)
      die "Expected '--' before skill-seekers arguments (use --help)"
      ;;
  esac
done

[[ -d "$tool_src" ]] || die "Missing vendored source dir: $tool_src"

python_bin="python3"
if [[ -x "$venv_dir/bin/python" ]]; then
  python_bin="$venv_dir/bin/python"
fi

export PYTHONPATH="$tool_src${PYTHONPATH:+:$PYTHONPATH}"

exec "$python_bin" -m skill_seekers.cli.main "$@"
