#!/usr/bin/env bash
# 做什么：验证上游登记源、浅克隆前进同步与脏工作树拒绝行为。
# 怎么运行：bash tests/test_sync_upstreams.sh。
# 需要什么：bash、git、mktemp；不访问网络，不读取凭据。

set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
source "$ROOT/scripts/sync_upstreams.sh"
PROJECT_SOURCE_FILE=$SOURCE_FILE

TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

SOURCE_ROWS="$TMP_DIR/source-rows"
read_source_rows >"$SOURCE_ROWS"
python3 - "$PROJECT_SOURCE_FILE" "$SOURCE_ROWS" <<'PY'
import json
from pathlib import Path
import sys


registry = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
sources = registry["sources"]
expected = {
    "opencode": ("https://github.com/anomalyco/opencode.git", "dev"),
    "codex": ("https://github.com/openai/codex.git", "main"),
    "claude-code": ("https://github.com/anthropics/claude-code.git", "main"),
    "deepseek-harness": ("https://github.com/deepseek-ai/deepseek-harness.git", "master"),
    "pi": ("https://github.com/earendil-works/pi.git", "main"),
    "openclaw": ("https://github.com/openclaw/openclaw.git", "main"),
    "goose": ("https://github.com/aaif-goose/goose.git", "main"),
    "gemini-cli": ("https://github.com/google-gemini/gemini-cli.git", "main"),
    "cline": ("https://github.com/cline/cline.git", "main"),
    "qwen-code": ("https://github.com/QwenLM/qwen-code.git", "main"),
    "kimi-code": ("https://github.com/MoonshotAI/kimi-code.git", "main"),
    "crush": ("https://github.com/charmbracelet/crush.git", "main"),
    "mistral-vibe": ("https://github.com/mistralai/mistral-vibe.git", "main"),
    "openhands": ("https://github.com/OpenHands/OpenHands.git", "main"),
    "hermes-agent": ("https://github.com/NousResearch/hermes-agent.git", "main"),
}
assert len(sources) == len(expected), (
    f"expected {len(expected)} official sources, got {len(sources)}"
)
actual = {source["name"]: (source["git_url"], source["branch"]) for source in sources}
assert actual == expected
assert len({source["git_url"] for source in sources}) == len(sources)
for source in sources:
    assert source["license"]
    if source["visibility_assessment"] == "validated-core-paths":
        assert source["core_paths"]
openhands = next(source for source in sources if source["name"] == "openhands")
assert openhands["source_visibility"] == "public-repository-without-harness-core-source"
assert openhands["visibility_assessment"] == "manual-negative-assessment"
assert openhands["visibility_assessment_commit"]
crush = next(source for source in sources if source["name"] == "crush")
assert crush["license"] == "FSL-1.1-MIT"
rows = Path(sys.argv[2]).read_bytes().split(b"\0")
assert rows[-1] == b""
assert len(rows[:-1]) == len(sources) * 3
PY

python3 - "$PROJECT_SOURCE_FILE" "$TMP_DIR" <<'PY'
import json
from pathlib import Path
import sys


registry = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
output_dir = Path(sys.argv[2])

duplicate = json.loads(json.dumps(registry))
duplicate["sources"].append(dict(duplicate["sources"][0]))
(output_dir / "invalid-duplicate.json").write_text(json.dumps(duplicate), encoding="utf-8")

non_github = json.loads(json.dumps(registry))
non_github["sources"][0]["git_url"] = "file:///tmp/not-official.git"
(output_dir / "invalid-url.json").write_text(json.dumps(non_github), encoding="utf-8")

unsafe_path = json.loads(json.dumps(registry))
unsafe_path["sources"][0]["core_paths"] = ["../outside"]
(output_dir / "invalid-path.json").write_text(json.dumps(unsafe_path), encoding="utf-8")
PY
for invalid_registry in \
  "$TMP_DIR/invalid-duplicate.json" \
  "$TMP_DIR/invalid-url.json" \
  "$TMP_DIR/invalid-path.json"; do
  SOURCE_FILE=$invalid_registry
  if read_source_rows >"$TMP_DIR/invalid-rows" 2>/dev/null; then
    echo "FAIL: 非法 source registry 未被拒绝：$invalid_registry" >&2
    exit 1
  fi
done
SOURCE_FILE=$PROJECT_SOURCE_FILE

ORIGIN="$TMP_DIR/origin.git"
AUTHOR="$TMP_DIR/author"
CHECKOUT="$TMP_DIR/checkout"

git init --quiet --bare "$ORIGIN"
git init --quiet --initial-branch=main "$AUTHOR"
git -C "$AUTHOR" config user.name "Harness Test"
git -C "$AUTHOR" config user.email "harness-test@example.invalid"
printf 'one\n' >"$AUTHOR/revision.txt"
git -C "$AUTHOR" add revision.txt
git -C "$AUTHOR" commit --quiet -m "first"
git -C "$AUTHOR" remote add origin "file://$ORIGIN"
git -C "$AUTHOR" push --quiet --set-upstream origin main
git --git-dir="$ORIGIN" symbolic-ref HEAD refs/heads/main
update_checkout fixture "file://$ORIGIN" "$CHECKOUT" main
[[ -d "$CHECKOUT/.git" ]] || {
  echo "FAIL: 首次 clone 未原子落位" >&2
  exit 1
}
FAILED_CHECKOUT="$TMP_DIR/failed-checkout"
if update_checkout missing "file://$TMP_DIR/missing.git" "$FAILED_CHECKOUT" main 2>/dev/null; then
  echo "FAIL: 不存在的 origin 未被拒绝" >&2
  exit 1
fi
[[ ! -e "$FAILED_CHECKOUT" ]] || {
  echo "FAIL: clone 失败后遗留目标目录" >&2
  exit 1
}
if compgen -G "$TMP_DIR/.missing.clone.*" >/dev/null; then
  echo "FAIL: clone 失败后遗留 staging 目录" >&2
  exit 1
fi

UPSTREAM_DIR="$TMP_DIR/sync-root"
LOCK_FILE="$TMP_DIR/sync-lock.json"
mkdir -p "$UPSTREAM_DIR"
exec 8>"$UPSTREAM_DIR/.sync.lock"
flock --exclusive 8
if main 2>/dev/null; then
  echo "FAIL: 并发同步锁未被拒绝" >&2
  exit 1
fi
flock --unlock 8
exec 8>&-

printf 'two\n' >>"$AUTHOR/revision.txt"
git -C "$AUTHOR" commit --quiet -am "second"
git -C "$AUTHOR" push --quiet
EXPECTED=$(git -C "$AUTHOR" rev-parse HEAD)

update_checkout fixture "file://$ORIGIN" "$CHECKOUT"
ACTUAL=$(git -C "$CHECKOUT" rev-parse HEAD)
[[ "$ACTUAL" == "$EXPECTED" ]] || {
  echo "FAIL: 浅克隆没有前进到官方 tip" >&2
  exit 1
}

touch "$CHECKOUT/local-note"
if update_checkout fixture "file://$ORIGIN" "$CHECKOUT" 2>/dev/null; then
  echo "FAIL: 脏工作树未被拒绝" >&2
  exit 1
fi
[[ "$(git -C "$CHECKOUT" rev-parse HEAD)" == "$EXPECTED" ]] || {
  echo "FAIL: 拒绝路径改变了 checkout" >&2
  exit 1
}

rm "$CHECKOUT/local-note"
printf 'ignored-local/\n' >>"$CHECKOUT/.git/info/exclude"
mkdir "$CHECKOUT/ignored-local"
touch "$CHECKOUT/ignored-local/note"
if update_checkout fixture "file://$ORIGIN" "$CHECKOUT" 2>/dev/null; then
  echo "FAIL: 被忽略的本地研究文件未被拒绝" >&2
  exit 1
fi
rm -rf "$CHECKOUT/ignored-local"
git -C "$CHECKOUT" switch --quiet -c local-branch
if update_checkout fixture "file://$ORIGIN" "$CHECKOUT" main 2>/dev/null; then
  echo "FAIL: 非登记分支未被拒绝" >&2
  exit 1
fi
git -C "$CHECKOUT" switch --quiet main
PRE_REWRITE=$(git -C "$CHECKOUT" rev-parse HEAD)
printf 'rewritten\n' >>"$AUTHOR/revision.txt"
git -C "$AUTHOR" commit --quiet --amend -am "rewritten second"
git -C "$AUTHOR" push --quiet --force origin main
if update_checkout fixture "file://$ORIGIN" "$CHECKOUT" 2>/dev/null; then
  echo "FAIL: 无法证明 fast-forward 的远端改写未被拒绝" >&2
  exit 1
fi
[[ "$(git -C "$CHECKOUT" rev-parse HEAD)" == "$PRE_REWRITE" ]] || {
  echo "FAIL: 远端改写拒绝路径改变了 checkout" >&2
  exit 1
}

echo "PASS: 十五源登记、原子 clone、浅克隆前进、互斥、分支/脏树/忽略文件与远端改写拒绝行为正确"
