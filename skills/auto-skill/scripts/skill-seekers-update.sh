#!/usr/bin/env bash

set -euo pipefail

# ==================== Purpose ====================
# Legacy updater for the old vendored Skill Seekers source snapshot.
#
# Notes:
# - Skill Seekers now lives under tools/external/Skill_Seekers-development.
# - The auto-skill scripts directory only exposes it through a relative symlink.
# - This script refuses to overwrite the linked repository; update tools/external directly instead.

usage() {
  cat <<'EOF'
Usage:
  skill-seekers-update.sh [--repo <owner/repo>] [--ref <git-ref>] [--dry-run]

Defaults:
  --repo yusufkaraaslan/Skill_Seekers
  --ref  main

Examples:
  ./skills/auto-skill/scripts/skill-seekers-update.sh --dry-run
EOF
}

die() {
  echo "Error: $*" >&2
  exit 1
}

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
target_dir="${script_dir}/Skill_Seekers-development"

repo="yusufkaraaslan/Skill_Seekers"
ref="main"
dry_run=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --repo)
      [[ $# -ge 2 ]] || die "--repo requires an argument like owner/repo"
      repo="$2"
      shift 2
      ;;
    --ref)
      [[ $# -ge 2 ]] || die "--ref requires a git ref (branch/tag/commit)"
      ref="$2"
      shift 2
      ;;
    --dry-run)
      dry_run=1
      shift
      ;;
    --)
      shift
      break
      ;;
    *)
      die "Unknown argument: $1 (use --help)"
      ;;
  esac
done

command -v curl >/dev/null 2>&1 || die "curl not found"
command -v tar >/dev/null 2>&1 || die "tar not found"
command -v rsync >/dev/null 2>&1 || die "rsync not found"

if [[ -L "$target_dir" && "$dry_run" -eq 0 ]]; then
  die "Skill_Seekers-development is linked to tools/external. Update tools/external/Skill_Seekers-development directly instead of overwriting through this legacy updater."
fi

tmp_dir="$(mktemp -d)"
cleanup() { rm -rf "$tmp_dir"; }
trap cleanup EXIT

archive_url="https://codeload.github.com/${repo}/tar.gz/${ref}"
archive_path="${tmp_dir}/skill-seekers.tgz"

curl -fsSL "$archive_url" -o "$archive_path"
tar -xzf "$archive_path" -C "$tmp_dir"

extracted_root="$(find "$tmp_dir" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
[[ -n "$extracted_root" ]] || die "Failed to locate extracted archive root"

if [[ "$dry_run" -eq 1 ]]; then
  echo "DRY RUN:"
  echo "  repo: $repo"
  echo "  ref:  $ref"
  echo "  from: $extracted_root"
  echo "  to:   $target_dir"
  if [[ -L "$target_dir" ]]; then
    echo "  note: target is a symlink; non-dry-run update is intentionally blocked"
  fi
  exit 0
fi

mkdir -p "$target_dir"

rsync -a --delete \
  --exclude '.git' \
  --exclude '*.md' \
  --exclude 'docs/' \
  --exclude 'tests/' \
  --exclude '.claude/' \
  --exclude '.gitignore' \
  --exclude 'CHANGELOG.md' \
  --exclude 'ROADMAP.md' \
  --exclude 'FUTURE_RELEASES.md' \
  --exclude 'ASYNC_SUPPORT.md' \
  --exclude 'STRUCTURE.md' \
  --exclude 'CONTRIBUTING.md' \
  --exclude 'QUICKSTART.md' \
  --exclude 'BULLETPROOF_QUICKSTART.md' \
  --exclude 'FLEXIBLE_ROADMAP.md' \
  "$extracted_root"/ \
  "$target_dir"/

echo "OK: updated source in: $target_dir"
