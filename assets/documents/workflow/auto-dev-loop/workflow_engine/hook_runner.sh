#!/bin/bash
# workflow_engine/hook_runner.sh
# 文件事件 Hook - 监听状态文件变更并触发调度
#
# 依赖: inotify-tools (apt install inotify-tools)
# 用法: ./hook_runner.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STATE_FILE="$SCRIPT_DIR/state/current_step.json"
RUNNER="$SCRIPT_DIR/runner.py"

echo "[HOOK] 启动监听: $STATE_FILE"
echo "[HOOK] 按 Ctrl+C 停止"

# 检查依赖
if ! command -v inotifywait &> /dev/null; then
    echo "[ERROR] 需要安装 inotify-tools: sudo apt install inotify-tools"
    exit 1
fi

# 确保状态文件存在
mkdir -p "$(dirname "$STATE_FILE")"
[ -f "$STATE_FILE" ] || echo '{"status":"idle"}' > "$STATE_FILE"

# 监听文件修改事件
inotifywait -m -e modify "$STATE_FILE" 2>/dev/null | while read -r directory event filename; do
    echo "[HOOK] $(date '+%H:%M:%S') 检测到状态变更"
    
    # 读取 target_step
    target=$(python3 -c "import json; print(json.load(open('$STATE_FILE')).get('target_step',''))" 2>/dev/null)
    
    if [ "$target" = "done" ]; then
        echo "[HOOK] 工作流已完成"
    elif [ -n "$target" ] && [ "$target" != "null" ]; then
        echo "[HOOK] 触发调度 -> $target"
        python3 "$RUNNER" dispatch
    fi
done
