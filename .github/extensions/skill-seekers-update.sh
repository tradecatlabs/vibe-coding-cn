#!/usr/bin/env bash

set -euo pipefail

# ==================== Purpose ====================
# Guarded updater for the linked Skill Seekers source.
#
# Notes:
# - Skill Seekers位于本目录下的固定Git来源，不再经过旧scripts软引用。
# - 固定来源保护必须独立于它是否是软链接，不能因平铺变成可覆盖目录。
# - 本适配器拒绝非预览覆盖；来源更新应作为明确的Gitlink变更单独评审。

usage() {
  cat <<'EOF'
Usage:
  skill-seekers-update.sh [--repo <owner/repo>] [--ref <git-ref>] [--dry-run]

Defaults:
  --repo yusufkaraaslan/Skill_Seekers
  --ref  main

Examples:
  ./.github/extensions/skill-seekers-update.sh --dry-run
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

if [[ "$dry_run" -eq 0 ]]; then
  die "Skill_Seekers-development是固定来源；请单独评审Gitlink变更，不通过此适配器覆盖源码。"
fi

command -v curl >/dev/null 2>&1 || die "curl not found"
command -v tar >/dev/null 2>&1 || die "tar not found"

tmp_dir="$(mktemp -d)"
cleanup() { rm -rf "$tmp_dir"; }
trap cleanup EXIT

archive_url="https://codeload.github.com/${repo}/tar.gz/${ref}"
archive_path="${tmp_dir}/skill-seekers.tgz"

curl -fsSL "$archive_url" -o "$archive_path"
tar -xzf "$archive_path" -C "$tmp_dir"

extracted_root="$(find "$tmp_dir" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
[[ -n "$extracted_root" ]] || die "Failed to locate extracted archive root"

echo "DRY RUN:"
echo "  repo: $repo"
echo "  ref:  $ref"
echo "  from: $extracted_root"
echo "  to:   $target_dir"
echo "  note: 固定来源禁止非预览覆盖；预览仍会下载和解压临时归档，不是零I/O。"
