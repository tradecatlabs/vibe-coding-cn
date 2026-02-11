#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  validate-skill.sh <skill-dir> [--strict]

What it does:
  - Validates SKILL.md YAML frontmatter (name/description)
  - Performs lightweight structural checks
  - In --strict mode, enforces the recommended section layout

Examples:
  ./skills/claude-skills/scripts/validate-skill.sh skills/postgresql
  ./skills/claude-skills/scripts/validate-skill.sh skills/my-skill --strict
EOF
}

die() {
  echo "Error: $*" >&2
  exit 1
}

warn() {
  echo "Warning: $*" >&2
}

strict=0
skill_dir=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --strict)
      strict=1
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
      if [[ -z "$skill_dir" ]]; then
        skill_dir="$1"
        shift
      else
        die "Extra argument: $1 (only one <skill-dir> is allowed)"
      fi
      ;;
  esac
done

[[ -n "$skill_dir" ]] || { usage; exit 1; }
[[ -d "$skill_dir" ]] || die "Not a directory: $skill_dir"

skill_md="$skill_dir/SKILL.md"
[[ -f "$skill_md" ]] || die "Missing SKILL.md: $skill_md"

base_name="$(basename -- "${skill_dir%/}")"

# -------------------- Parse YAML frontmatter --------------------

frontmatter=""
if frontmatter="$(
  awk '
    BEGIN { in_fm=0; closed=0 }
    NR==1 {
      if ($0 != "---") exit 2
      in_fm=1
      next
    }
    in_fm==1 {
      if ($0 == "---") { closed=1; exit 0 }
      print
      next
    }
    END {
      if (closed == 0) exit 3
    }
  ' "$skill_md"
)"; then
  :
else
  rc=$?
  case "$rc" in
    2) die "SKILL.md must start with YAML frontmatter (--- as the first line)" ;;
    3) die "YAML frontmatter is not closed (missing ---)" ;;
    *) die "Failed to parse YAML frontmatter (awk exit=$rc)" ;;
  esac
fi

name="$(
  printf "%s\n" "$frontmatter" | awk -F: '
    tolower($1) ~ /^name$/ {
      sub(/^[^:]*:[[:space:]]*/, "", $0)
      gsub(/[[:space:]]+$/, "", $0)
      print
      exit
    }
  '
)"

description="$(
  printf "%s\n" "$frontmatter" | awk -F: '
    tolower($1) ~ /^description$/ {
      sub(/^[^:]*:[[:space:]]*/, "", $0)
      gsub(/[[:space:]]+$/, "", $0)
      print
      exit
    }
  '
)"

[[ -n "$name" ]] || die "Missing frontmatter field: name"
[[ -n "$description" ]] || die "Missing frontmatter field: description"

if [[ ! "$name" =~ ^[a-z][a-z0-9-]*$ ]]; then
  die "Invalid name: '$name' (expected ^[a-z][a-z0-9-]*$)"
fi

if [[ "$strict" -eq 1 && "$name" != "$base_name" ]]; then
  die "Strict mode: frontmatter name ('$name') must match directory name ('$base_name')"
fi

# -------------------- Strip fenced code blocks for section checks --------------------

filtered_md="$(mktemp)"
trap 'rm -f "$filtered_md"' EXIT

awk '
  BEGIN { in_fence=0 }
  /^[[:space:]]*```/ { in_fence = !in_fence; next }
  in_fence==0 { print }
' "$skill_md" > "$filtered_md"

# -------------------- Structural checks --------------------

required_h2=(
  "When to Use This Skill"
  "Not For / Boundaries"
  "Quick Reference"
  "Examples"
  "References"
  "Maintenance"
)

for title in "${required_h2[@]}"; do
  if ! grep -Eq "^##[[:space:]]+${title}([[:space:]]*)$" "$filtered_md"; then
    if [[ "$strict" -eq 1 ]]; then
      die "Strict mode: missing required section heading: '## ${title}'"
    fi
    warn "Missing recommended section heading: '## ${title}'"
  fi
done

# references/index.md presence (only enforced in strict mode when references/ exists)
if [[ -d "$skill_dir/references" && "$strict" -eq 1 && ! -f "$skill_dir/references/index.md" ]]; then
  die "Strict mode: references/ exists but references/index.md is missing"
fi

# -------------------- Heuristics: Quick Reference size --------------------

quick_start="$(awk 'match($0, /^##[[:space:]]+Quick Reference([[:space:]]*)$/){print NR; exit}' "$filtered_md" || true)"
if [[ -n "$quick_start" ]]; then
  quick_end="$(awk -v s="$quick_start" 'NR>s && match($0, /^##[[:space:]]+/){print NR; exit}' "$filtered_md" || true)"
  total_lines="$(wc -l < "$filtered_md" | tr -d ' ')"
  if [[ -z "$quick_end" ]]; then
    quick_end="$((total_lines + 1))"
  fi
  quick_len="$((quick_end - quick_start - 1))"
  if [[ "$quick_len" -gt 250 ]]; then
    if [[ "$strict" -eq 1 ]]; then
      die "Strict mode: Quick Reference section is too long (${quick_len} lines). Move long-form text into references/."
    fi
    warn "Quick Reference section is large (${quick_len} lines). Consider moving long-form text into references/."
  fi
fi

# -------------------- Heuristics: Examples count --------------------

examples_start="$(awk 'match($0, /^##[[:space:]]+Examples([[:space:]]*)$/){print NR; exit}' "$filtered_md" || true)"
if [[ -n "$examples_start" ]]; then
  examples_end="$(awk -v s="$examples_start" 'NR>s && match($0, /^##[[:space:]]+/){print NR; exit}' "$filtered_md" || true)"
  total_lines="$(wc -l < "$filtered_md" | tr -d ' ')"
  if [[ -z "$examples_end" ]]; then
    examples_end="$((total_lines + 1))"
  fi

  example_count="$(
    awk -v s="$examples_start" -v e="$examples_end" '
      NR>s && NR<e && match($0, /^###[[:space:]]+Example([[:space:]]|$)/) { c++ }
      END { print c+0 }
    ' "$filtered_md"
  )"

  if [[ "$example_count" -lt 3 ]]; then
    if [[ "$strict" -eq 1 ]]; then
      die "Strict mode: expected >= 3 examples (found ${example_count})."
    fi
    warn "Recommended: >= 3 examples (found ${example_count})."
  fi
fi

echo "OK: $skill_dir"
