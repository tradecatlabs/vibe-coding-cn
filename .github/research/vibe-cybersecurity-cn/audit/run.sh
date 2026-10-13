#!/usr/bin/env bash
# run.sh - S0 审计管线骨架（M1）：克隆/本地目标 -> 固定 commit -> 编译 -> Slither 候选 -> forge test -> 证据摘要
# 用法: audit/run.sh --path <本地独立克隆>|--repo <git-url> --commit <sha> [--out <输出根>] [--test-match <forge 过滤器>]
# 需要: git, forge (>=1.7), slither (>=0.11), jq；目标必须是可以自由改动的独立工作区
set -euo pipefail

# ============ 工具解析（PATH 优先，回退项目 venv） ============
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
detect_tool() {
  local name="$1"
  if command -v "$name" >/dev/null 2>&1; then
    command -v "$name"
    return 0
  fi
  if [[ -x "$REPO_ROOT/.venv-web3/bin/$name" ]]; then
    echo "$REPO_ROOT/.venv-web3/bin/$name"
    return 0
  fi
  return 1
}

FORGE_BIN="$(detect_tool forge)" || { echo "缺少 forge（请先安装 Foundry）" >&2; exit 4; }
SLITHER_BIN="$(detect_tool slither)" || { echo "缺少 slither（请安装到 PATH 或 .venv-web3/bin）" >&2; exit 4; }
SOLC_BIN="$(detect_tool solc || true)"
TOOL_BIN_DIR="$(dirname "$SLITHER_BIN")"
export PATH="$TOOL_BIN_DIR:$PATH"

# ============ 运行参数（也可用环境变量覆盖） ============
OUT_ROOT="${AUDIT_OUT_ROOT:-audit/out}"
TEST_MATCH=""
REPO_URL=""
TARGET_PATH=""
TARGET_COMMIT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo) REPO_URL="$2"; shift 2 ;;
    --path) TARGET_PATH="$2"; shift 2 ;;
    --commit) TARGET_COMMIT="$2"; shift 2 ;;
    --out) OUT_ROOT="$2"; shift 2 ;;
    --test-match) TEST_MATCH="$2"; shift 2 ;;
    -h|--help)
      sed -n '2,4p' "$0"
      exit 0
      ;;
    *) echo "未知参数: $1" >&2; exit 2 ;;
  esac
done

[[ -n "$TARGET_COMMIT" ]] || { echo "缺少 --commit <sha>" >&2; exit 2; }
[[ -n "$REPO_URL" || -n "$TARGET_PATH" ]] || { echo "缺少 --repo <url> 或 --path <目录>" >&2; exit 2; }

# 输出根转绝对路径：必须在 cd 目标工程之前解析，避免证据落入目标目录
OUT_ROOT="$(realpath -m "$OUT_ROOT")"
RUN_DIR="${OUT_ROOT}/run-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$RUN_DIR"

# ============ 目标工作区准备 ============
if [[ -n "$REPO_URL" ]]; then
  WS_ROOT="${OUT_ROOT}/workspace"
  mkdir -p "$WS_ROOT"
  WS_DIR="${WS_ROOT}/$(basename "$REPO_URL" .git)"
  if [[ ! -d "$WS_DIR/.git" ]]; then
    git clone --quiet --no-checkout --filter=blob:none "$REPO_URL" "$WS_DIR"
  fi
  git -C "$WS_DIR" checkout --quiet "$TARGET_COMMIT"
  git -C "$WS_DIR" submodule update --init --depth 1 --quiet
  TARGET_PATH="$WS_DIR"
else
  [[ -d "$TARGET_PATH/.git" ]] || { echo "--path 必须是 git 仓库" >&2; exit 2; }
  HEAD_COMMIT="$(git -C "$TARGET_PATH" rev-parse HEAD)"
  if [[ "$HEAD_COMMIT" != "$TARGET_COMMIT" ]]; then
    # 保护用户工作区：只有干净工作树才允许切换 commit
    [[ -z "$(git -C "$TARGET_PATH" status --porcelain)" ]] || { echo "目标工作树非干净，拒绝 checkout（请用独立克隆）" >&2; exit 2; }
    git -C "$TARGET_PATH" checkout --quiet "$TARGET_COMMIT"
  fi
fi

cd "$TARGET_PATH"
REAL_COMMIT="$(git rev-parse HEAD)"
[[ "$REAL_COMMIT" == "$TARGET_COMMIT" ]] || { echo "commit 不匹配: $REAL_COMMIT != $TARGET_COMMIT" >&2; exit 2; }

# ============ 工程探测 ============
ENGINE="unknown"
if [[ -f foundry.toml ]]; then ENGINE="foundry"; fi
if [[ -f hardhat.config.ts || -f hardhat.config.js ]]; then ENGINE="hardhat"; fi
if [[ "$ENGINE" == "unknown" ]]; then
  echo "M1: 未识别的工程类型（仅支持 foundry / hardhat）" >&2
  exit 3
fi
if [[ "$ENGINE" == "hardhat" ]]; then
  echo "M1: Hardhat/Node 路径未启用（Node v22 环境待验证），请提供 Foundry 工程" >&2
  exit 3
fi

# ============ 工具版本 ============
FORGE_VERSION="$("$FORGE_BIN" --version 2>/dev/null | head -1 || echo unknown)"
SLITHER_VERSION="$("$SLITHER_BIN" --version 2>/dev/null || echo unknown)"
SOLC_VERSION="$("${SOLC_BIN:-solc}" --version 2>/dev/null | tail -1 || echo unknown)"

echo "[1/4] 固定 commit: $REAL_COMMIT (engine=$ENGINE)"
echo "[2/4] forge build -> $RUN_DIR/out"
FOUNDRY_OUT="$RUN_DIR/out" "$FORGE_BIN" build --root . --quiet
ABI_COUNT="$(find "$RUN_DIR/out" -name '*.json' -not -name '*.metadata.json' 2>/dev/null | wc -l)"

echo "[3/4] slither 候选 -> $RUN_DIR/slither.json"
set +e
"$SLITHER_BIN" . --json "$RUN_DIR/slither.json" > "$RUN_DIR/slither.log" 2>&1
SLITHER_EXIT=$?
set -e
SLITHER_SUCCESS="$(jq -r '.success // false' "$RUN_DIR/slither.json" 2>/dev/null || echo false)"
SLITHER_DETECTORS="$(jq '.results.detectors | length' "$RUN_DIR/slither.json" 2>/dev/null || echo 0)"
if [[ "$SLITHER_SUCCESS" != "true" ]]; then
  echo "slither 未产出有效 JSON（退出码 $SLITHER_EXIT），视为失败" >&2
  SLITHER_FAILED="yes"
elif [[ $SLITHER_EXIT -ne 0 ]]; then
  echo "slither JSON 有效但退出码 $SLITHER_EXIT（清理阶段异常），记为 warning" >&2
fi

echo "[4/4] forge test 空跑"
TEST_FILTER_ARGS=()
[[ -n "$TEST_MATCH" ]] && TEST_FILTER_ARGS=(--match-test "$TEST_MATCH")
TEST_OUTPUT="$(FOUNDRY_OUT="$RUN_DIR/out" "$FORGE_BIN" test --root . "${TEST_FILTER_ARGS[@]}" 2>&1 || true)"
TEST_SUMMARY="$(echo "$TEST_OUTPUT" | grep -E 'Suite result|Ran .* test suites' | tail -4 || echo "$TEST_OUTPUT" | tail -5)"
echo "$TEST_OUTPUT" > "$RUN_DIR/forge-test.log"

# ============ 证据摘要 ============
RUN_DIR_REL="${RUN_DIR#"$REPO_ROOT"/}"
jq -n \
  --arg schema "s0-audit-run/v1" \
  --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --arg target "$(basename "$TARGET_PATH")" \
  --arg commit "$REAL_COMMIT" \
  --arg engine "$ENGINE" \
  --arg forge "$FORGE_VERSION" \
  --arg slither "$SLITHER_VERSION" \
  --arg solc "$SOLC_VERSION" \
  --argjson abi_count "${ABI_COUNT:-0}" \
  --argjson detectors "${SLITHER_DETECTORS:-0}" \
  --arg test_summary "$TEST_SUMMARY" \
  --arg slither_failed "${SLITHER_FAILED:-no}" \
  --argjson slither_exit "${SLITHER_EXIT:-0}" \
  --arg slither_success "$SLITHER_SUCCESS" \
  --arg run_dir "$RUN_DIR_REL" \
  '{schema: $schema, timestamp: $ts, target: {name: $target, commit: $commit, engine: $engine},
    tools: {forge: $forge, slither: $slither, solc: $solc},
    artifacts: {abi_artifacts: $abi_count, slither_detectors: $detectors, forge_test: $test_summary},
    flags: {slither_failed: $slither_failed, slither_exit: $slither_exit, slither_success: $slither_success}, run_dir: $run_dir}' \
  | tee "$RUN_DIR/evidence.json"

echo
echo "证据目录: $RUN_DIR"
