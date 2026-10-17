#!/usr/bin/env bash
# 做什么：从单一登记源浅克隆或 fast-forward 同步官方 Harness，并刷新 revision lock。
# 怎么运行：bash scripts/sync_upstreams.sh；可用 UPSTREAM_DEPTH/UPSTREAM_TIMEOUT_SECONDS 调整边界。
# 需要什么：git、python3、timeout、flock、可访问 github.com 的网络；不需要账号或凭据。
# 存在性：15 源必须由一份 registry 驱动；实测后再决定是否需要并发或更强 schema。

set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
UPSTREAM_DIR="$ROOT/research/upstreams"
LOCK_FILE="$ROOT/research/upstreams.lock.json"
SOURCE_FILE="$ROOT/research/upstreams.sources.json"
DEPTH=${UPSTREAM_DEPTH:-1}
DEEPEN_STEP=${UPSTREAM_DEEPEN_STEP:-32}
MAX_DEEPEN=${UPSTREAM_MAX_DEEPEN:-4096}
NETWORK_TIMEOUT=${UPSTREAM_TIMEOUT_SECONDS:-300}

for setting in DEPTH DEEPEN_STEP MAX_DEEPEN NETWORK_TIMEOUT; do
  value=${!setting}
  if [[ ! "$value" =~ ^[1-9][0-9]*$ ]]; then
    echo "BLOCK: $setting 必须是正整数" >&2
    exit 1
  fi
done

for command in timeout flock; do
  if ! command -v "$command" >/dev/null 2>&1; then
    echo "BLOCK: 缺少 $command 命令" >&2
    exit 1
  fi
done

run_git_network() {
  timeout --foreground "$NETWORK_TIMEOUT" git "$@"
}

update_checkout() {
  local name=$1
  local url=$2
  local target=$3
  local expected_branch=${4:-}

  if [[ ! -d "$target/.git" ]]; then
    if [[ -e "$target" ]]; then
      echo "BLOCK $name: 目标路径已存在但不是 Git checkout：$target" >&2
      return 1
    fi
    local target_parent
    target_parent=$(dirname "$target")
    mkdir -p "$target_parent"
    local staging
    staging=$(mktemp -d "$target_parent/.${name}.clone.XXXXXX")
    if [[ -n "$expected_branch" ]]; then
      if ! run_git_network clone --depth "$DEPTH" --branch "$expected_branch" --single-branch "$url" "$staging/repo"; then
        rm -rf "$staging"
        echo "BLOCK $name: clone 失败或超时" >&2
        return 1
      fi
    else
      if ! run_git_network clone --depth "$DEPTH" "$url" "$staging/repo"; then
        rm -rf "$staging"
        echo "BLOCK $name: clone 失败或超时" >&2
        return 1
      fi
    fi
    mv "$staging/repo" "$target"
    rmdir "$staging"
    return
  fi

  local actual_url
  actual_url=$(git -C "$target" remote get-url origin)
  if [[ "$actual_url" != "$url" ]]; then
    echo "BLOCK $name: origin 不匹配：$actual_url" >&2
    return 1
  fi

  if [[ -n "$(git -C "$target" status --porcelain --ignored=matching --untracked-files=all)" ]]; then
    echo "BLOCK $name: checkout 存在本地改动，拒绝同步以免覆盖研究现场" >&2
    return 1
  fi

  local branch
  branch=$(git -C "$target" symbolic-ref --quiet --short HEAD) || {
    echo "BLOCK $name: checkout 处于 detached HEAD，拒绝猜测同步目标" >&2
    return 1
  }
  if [[ -n "$expected_branch" && "$branch" != "$expected_branch" ]]; then
    echo "BLOCK $name: 当前分支 $branch 与登记分支 $expected_branch 不匹配" >&2
    return 1
  fi
  if ! run_git_network -C "$target" fetch --depth "$DEPTH" origin "$branch"; then
    echo "BLOCK $name: fetch 失败或超时" >&2
    return 1
  fi

  local deepened=0
  local step=$DEEPEN_STEP
  while ! git -C "$target" merge-base --is-ancestor HEAD FETCH_HEAD; do
    if [[ "$(git -C "$target" rev-parse --is-shallow-repository)" != "true" || $deepened -ge $MAX_DEEPEN ]]; then
      echo "BLOCK $name: 无法证明官方分支是本地 revision 的 fast-forward 后继" >&2
      return 1
    fi
    if (( step > MAX_DEEPEN - deepened )); then
      step=$((MAX_DEEPEN - deepened))
    fi
    if ! run_git_network -C "$target" fetch --deepen "$step" origin "$branch"; then
      echo "BLOCK $name: deepen fetch 失败或超时" >&2
      return 1
    fi
    deepened=$((deepened + step))
    step=$((step * 2))
  done
  git -C "$target" merge --ff-only FETCH_HEAD
}

sync_repo() {
  local name=$1
  local url=$2
  local branch=$3
  update_checkout "$name" "$url" "$UPSTREAM_DIR/$name" "$branch"
}

read_source_rows() {
  local source_file=${1:-$SOURCE_FILE}
  python3 - "$source_file" <<'PY'
from __future__ import annotations

import json
from pathlib import Path, PurePosixPath
import re
import sys


source_file = Path(sys.argv[1]).resolve()
try:
    registry = json.loads(source_file.read_text(encoding="utf-8"))
except FileNotFoundError:
    raise SystemExit(f"source registry missing: {source_file}")
except (json.JSONDecodeError, OSError) as exc:
    raise SystemExit(f"source registry unreadable: {exc}")

if registry.get("schema_version") != "1.0.0":
    raise SystemExit("source registry schema_version must be 1.0.0")
sources = registry.get("sources")
if not isinstance(sources, list) or not sources:
    raise SystemExit("source registry sources must be a non-empty list")

required_strings = (
    "name",
    "git_url",
    "branch",
    "license",
    "license_path",
    "license_marker",
    "source_visibility",
    "visibility_assessment",
    "visibility_assessment_commit",
    "limitation",
)
allowed_visibility = {
    "core-source-public",
    "public-repository-without-harness-core-source",
}
allowed_assessments = {"validated-core-paths", "manual-negative-assessment"}
seen_names: set[str] = set()
seen_urls: set[str] = set()


def validate_relative_path(name: str, field: str, value: object) -> str:
    if not isinstance(value, str) or not value:
        raise SystemExit(f"{name}: {field} entries must be non-empty strings")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        raise SystemExit(f"{name}: unsafe {field} path: {value}")
    return value


for index, spec in enumerate(sources):
    if not isinstance(spec, dict):
        raise SystemExit(f"source registry entry {index} must be an object")
    for field in required_strings:
        if not isinstance(spec.get(field), str):
            raise SystemExit(f"source registry entry {index}: {field} must be a string")
    name = spec["name"]
    git_url = spec["git_url"]
    branch = spec["branch"]
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
        raise SystemExit(f"unsafe source name: {name}")
    if name in seen_names:
        raise SystemExit(f"duplicate source name: {name}")
    if not re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\.git", git_url):
        raise SystemExit(f"{name}: git_url must be an official GitHub HTTPS clone URL")
    if git_url in seen_urls:
        raise SystemExit(f"duplicate source git_url: {git_url}")
    if not branch or branch.strip() != branch or any(char in branch for char in "\x00\r\n"):
        raise SystemExit(f"{name}: invalid branch")
    if spec["source_visibility"] not in allowed_visibility:
        raise SystemExit(f"{name}: unsupported source_visibility")
    if spec["visibility_assessment"] not in allowed_assessments:
        raise SystemExit(f"{name}: unsupported visibility_assessment")
    assessed_commit = spec["visibility_assessment_commit"]
    if assessed_commit and not re.fullmatch(r"[0-9a-f]{40}", assessed_commit):
        raise SystemExit(f"{name}: visibility_assessment_commit must be a full commit")
    for field in ("core_paths", "public_paths"):
        values = spec.get(field)
        if not isinstance(values, list):
            raise SystemExit(f"{name}: {field} must be a list")
        for value in values:
            validate_relative_path(name, field, value)
    validate_relative_path(name, "license_path", spec["license_path"])
    if spec["visibility_assessment"] == "validated-core-paths" and not spec["core_paths"]:
        raise SystemExit(f"{name}: validated-core-paths requires core_paths")
    if spec["visibility_assessment"] == "manual-negative-assessment" and not assessed_commit:
        raise SystemExit(f"{name}: manual-negative-assessment requires a bound commit")
    seen_names.add(name)
    seen_urls.add(git_url)
    for value in (name, git_url, branch):
        sys.stdout.buffer.write(value.encode("utf-8") + b"\0")
PY
}

write_lock() {
  local source_file=${1:-$SOURCE_FILE}
  python3 - "$UPSTREAM_DIR" "$LOCK_FILE" "$source_file" <<'PY'
from __future__ import annotations

from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys


upstream_dir = Path(sys.argv[1]).resolve()
lock_file = Path(sys.argv[2]).resolve()
source_file = Path(sys.argv[3]).resolve()
source_bytes = source_file.read_bytes()
registry = json.loads(source_bytes)
source_specs = registry["sources"]


def git_value(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(completed.stderr.strip() or f"git {' '.join(args)} failed: {repo}")
    return completed.stdout.strip()


def tracked_file_count(repo: Path, paths: list[str] | None = None) -> int:
    command = ["git", "-C", str(repo), "ls-files", "-z"]
    if paths:
        command.extend(["--", *paths])
    completed = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(completed.stderr.decode(errors="replace").strip())
    return sum(1 for item in completed.stdout.split(b"\0") if item)


def validate_source_layout(repo: Path, spec: dict[str, object]) -> None:
    license_path = repo / str(spec["license_path"])
    if not license_path.is_file():
        raise SystemExit(f"license file missing for {spec['name']}: {spec['license_path']}")
    license_text = license_path.read_text(encoding="utf-8", errors="replace")
    if str(spec["license_marker"]) not in license_text:
        raise SystemExit(f"license marker changed for {spec['name']}; manual review required")
    for field in ("core_paths", "public_paths"):
        for relative in spec[field]:
            if not (repo / relative).exists():
                raise SystemExit(f"declared {field} path missing for {spec['name']}: {relative}")


sources = []
for spec in source_specs:
    name = spec["name"]
    expected_url = spec["git_url"]
    repo = upstream_dir / name
    actual_url = git_value(repo, "remote", "get-url", "origin")
    if actual_url != expected_url:
        raise SystemExit(f"origin mismatch for {name}: {actual_url}")
    validate_source_layout(repo, spec)
    branch = git_value(repo, "symbolic-ref", "--quiet", "--short", "HEAD")
    if branch != spec["branch"]:
        raise SystemExit(f"branch mismatch for {name}: {branch}")
    commit = git_value(repo, "rev-parse", "HEAD")
    assessed_commit = str(spec["visibility_assessment_commit"]) or commit
    visibility = str(spec["source_visibility"])
    limitation = str(spec["limitation"])
    if spec["visibility_assessment"] == "manual-negative-assessment" and commit != assessed_commit:
        visibility = "requires-manual-review"
        limitation = "上游 revision 已变化；不得继承上一 revision 的核心源码可见性结论，必须重新检查。"
    core_file_count = tracked_file_count(repo, spec["core_paths"]) if spec["core_paths"] else 0
    if spec["core_paths"] and core_file_count == 0:
        raise SystemExit(f"declared core paths contain no tracked files for {name}")
    sources.append(
        {
            "name": name,
            "github_url": expected_url.removesuffix(".git"),
            "checkout": f"research/upstreams/{name}",
            "branch": branch,
            "commit": commit,
            "commit_time": git_value(repo, "show", "-s", "--format=%cI", "HEAD"),
            "shallow": git_value(repo, "rev-parse", "--is-shallow-repository") == "true",
            "license": spec["license"],
            "license_path": spec["license_path"],
            "source_visibility": visibility,
            "visibility_assessment": spec["visibility_assessment"],
            "visibility_assessment_commit": assessed_commit,
            "core_paths": spec["core_paths"],
            "public_paths": spec["public_paths"],
            "tracked_file_count": tracked_file_count(repo),
            "core_file_count": core_file_count,
            "limitation": limitation,
        }
    )

source_registry_digest = f"sha256:{hashlib.sha256(source_bytes).hexdigest()}"
generated_at = datetime.now().astimezone().isoformat(timespec="seconds")
if lock_file.is_file():
    try:
        previous = json.loads(lock_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        previous = {}
    if (
        previous.get("sources") == sources
        and previous.get("source_registry_digest") == source_registry_digest
        and isinstance(previous.get("generated_at"), str)
    ):
        generated_at = previous["generated_at"]

payload = {
    "schema_version": "1.0.0",
    "generated_at": generated_at,
    "source_registry": "research/upstreams.sources.json",
    "source_registry_digest": source_registry_digest,
    "sources": sources,
}
rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
if not lock_file.is_file() or lock_file.read_text(encoding="utf-8") != rendered:
    lock_file.write_text(rendered, encoding="utf-8")
PY
}

main() {
  mkdir -p "$UPSTREAM_DIR"
  exec 9>"$UPSTREAM_DIR/.sync.lock"
  if ! flock --exclusive --nonblock 9; then
    echo "BLOCK: 已有上游同步进程运行中" >&2
    return 1
  fi
  local rows_file source_snapshot_file
  rows_file=$(mktemp)
  source_snapshot_file=$(mktemp)
  if ! cp -- "$SOURCE_FILE" "$source_snapshot_file"; then
    rm -f "$rows_file" "$source_snapshot_file"
    echo "BLOCK: 无法读取上游 source registry" >&2
    return 1
  fi
  if ! read_source_rows "$source_snapshot_file" >"$rows_file"; then
    rm -f "$rows_file" "$source_snapshot_file"
    echo "BLOCK: 上游 source registry 无效" >&2
    return 1
  fi
  local name url branch
  local source_count=0
  local sync_failed=0
  while IFS= read -r -d '' name; do
    if ! IFS= read -r -d '' url || ! IFS= read -r -d '' branch; then
      echo "BLOCK: 上游 source registry 输出不完整" >&2
      sync_failed=1
      break
    fi
    if ! git check-ref-format --branch "$branch" >/dev/null 2>&1; then
      echo "BLOCK $name: 登记分支不是合法 Git branch：$branch" >&2
      sync_failed=1
      break
    fi
    if ! sync_repo "$name" "$url" "$branch"; then
      sync_failed=1
      break
    fi
    source_count=$((source_count + 1))
  done <"$rows_file"
  rm -f "$rows_file"
  if (( sync_failed != 0 || source_count == 0 )); then
    rm -f "$source_snapshot_file"
    return 1
  fi
  if ! write_lock "$source_snapshot_file"; then
    rm -f "$source_snapshot_file"
    return 1
  fi
  rm -f "$source_snapshot_file"

  echo "PASS: 官方上游已同步，revision lock 已刷新"
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
fi
