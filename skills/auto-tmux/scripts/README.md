# auto-tmux scripts

`scripts/` 存放 `auto-tmux` 的可执行辅助脚本，把常见 tmux 操作封装成安全、可复用、可审计的命令。

## 入口

- [`auto-tmux.sh`](./auto-tmux.sh) - 统一命令入口，支持拓扑、读取、发送、巡检、救援、录制、等待和 AI 工作台初始化。
- [`swarm-state.sh`](./swarm-state.sh) - 蜂群状态、任务、锁和报告管理。
- [`swarm-brief.sh`](./swarm-brief.sh) - 只读生成蜂群交接报告，汇总 doctor、topology、pane 输出和状态报告。
- [`swarm-watch.sh`](./swarm-watch.sh) - 有限轮次巡检蜂群 pane 输出和状态报告，形成连续证据。
- [`swarm-archive.sh`](./swarm-archive.sh) - 打包 brief、snapshot 和 swarm state，生成可交接归档。
- [`safety-check.sh`](./safety-check.sh) - 发送、粘贴或分发前检查危险命令、敏感信息和过大 payload。
- [`render-swarm-prompt.sh`](./render-swarm-prompt.sh) - commander、worker、reviewer 提示词渲染。
- [`swarm-dispatch.sh`](./swarm-dispatch.sh) - 渲染提示词并可选发送到指定 pane，默认只写文件。
- [`auto-tmux-smoke-test.sh`](./auto-tmux-smoke-test.sh) - 创建临时 tmux 会话，端到端验证脚本能力。
- [`validate-auto-tmux.sh`](./validate-auto-tmux.sh) - 汇总脚本权限、语法、help、文档索引、strict 和 smoke 门禁。

## 常用命令

```bash
# 查看帮助
skills/auto-tmux/scripts/auto-tmux.sh help

# 查看 tmux 拓扑
skills/auto-tmux/scripts/auto-tmux.sh topology
skills/auto-tmux/scripts/auto-tmux.sh cleanup --session ai-hub --dry-run

# 诊断环境
skills/auto-tmux/scripts/auto-tmux.sh doctor --session ai-hub

target="$(tmux list-panes -t ai-hub:worker1 -F '#S:#I.#P' | head -n 1)"

# 读取指定 pane 最近 80 行
skills/auto-tmux/scripts/auto-tmux.sh inspect -t "$target" -n 40
skills/auto-tmux/scripts/auto-tmux.sh capture -t "$target" -n 80

# 发送命令并回车
skills/auto-tmux/scripts/safety-check.sh --text "make test"
skills/auto-tmux/scripts/auto-tmux.sh send -t "$target" --text "make test" --enter
skills/auto-tmux/scripts/safety-check.sh --file /tmp/prompt.md --strict
skills/auto-tmux/scripts/auto-tmux.sh paste -t "$target" --file /tmp/prompt.md --enter --dry-run

# 扫描某个 session 的错误
skills/auto-tmux/scripts/auto-tmux.sh scan --session ai-hub --pattern "ERROR|Traceback"

# 受控广播，先 dry-run
skills/auto-tmux/scripts/auto-tmux.sh broadcast --session ai-hub --text "pwd" --enter --dry-run

# 生成证据快照
skills/auto-tmux/scripts/auto-tmux.sh snapshot --session ai-hub --dir /tmp/auto-tmux-snapshot

# 生成蜂群交接报告
skills/auto-tmux/scripts/swarm-brief.sh --session ai-hub --swarm-dir /tmp/ai_swarm --out /tmp/auto-tmux-brief

# 采集 3 轮蜂群巡检证据
skills/auto-tmux/scripts/swarm-watch.sh --session ai-hub --swarm-dir /tmp/ai_swarm --iterations 3 --interval 10

# 打包交接归档
skills/auto-tmux/scripts/swarm-archive.sh --session ai-hub --swarm-dir /tmp/ai_swarm --out /tmp/ai-hub-handoff.tar.gz

# 初始化蜂群状态并添加任务
skills/auto-tmux/scripts/swarm-state.sh init --dir /tmp/ai_swarm
skills/auto-tmux/scripts/swarm-state.sh task-add --id task-001 --text "检查 README 链接"
skills/auto-tmux/scripts/swarm-state.sh task-import --file /tmp/tasks.txt --prefix batch --dir /tmp/ai_swarm
skills/auto-tmux/scripts/swarm-state.sh task-depend --id task-002 --blocked-by task-001 --dir /tmp/ai_swarm
skills/auto-tmux/scripts/swarm-state.sh task-ready --dir /tmp/ai_swarm
skills/auto-tmux/scripts/swarm-state.sh task-next --owner "$target" --dir /tmp/ai_swarm
skills/auto-tmux/scripts/swarm-state.sh lock-prune --older-than 3600 --dry-run --dir /tmp/ai_swarm
skills/auto-tmux/scripts/swarm-state.sh task-block --id task-001 --owner "$target" --reason "等待输入" --dir /tmp/ai_swarm
skills/auto-tmux/scripts/swarm-state.sh task-fail --id task-001 --owner "$target" --reason "测试失败" --dir /tmp/ai_swarm
skills/auto-tmux/scripts/swarm-state.sh task-list --status FAIL --dir /tmp/ai_swarm
skills/auto-tmux/scripts/swarm-state.sh metrics --dir /tmp/ai_swarm
skills/auto-tmux/scripts/swarm-state.sh task-reopen --id task-001 --owner "$target" --reason "重新执行" --dir /tmp/ai_swarm
skills/auto-tmux/scripts/swarm-state.sh validate --dir /tmp/ai_swarm
skills/auto-tmux/scripts/swarm-state.sh report --dir /tmp/ai_swarm

# 端到端自测
skills/auto-tmux/scripts/auto-tmux-smoke-test.sh

# auto-tmux 专属质量门禁
skills/auto-tmux/scripts/validate-auto-tmux.sh

# 渲染 worker prompt
skills/auto-tmux/scripts/render-swarm-prompt.sh worker --target "$target" --task "只运行 make test"

# 渲染并预演下发 worker prompt
skills/auto-tmux/scripts/swarm-dispatch.sh --role worker --target "$target" --task "只运行 make test" --send --dry-run
```

## 安全约束

- 默认对捕获输出做密钥脱敏。
- `send` 会先打印目标 pane 最近上下文，再发送按键。
- 危险命令默认拒绝，必须显式 `--force`。
- 长 prompt、文件粘贴和 prompt 下发前先运行 `safety-check.sh`。
- 批量操作必须使用明确的 session/window/pane 目标。
- 批量广播必须先 `--dry-run`，确认目标列表后再真实发送。
- 多 worker 协作时用 `swarm-state.sh lock-acquire` 声明文件、目录或服务锁。
