# auto-tmux Script Automation

`scripts/auto-tmux.sh` 是 `auto-tmux` 的安全执行层：把高频 tmux 操作封装为可审计命令，减少手写 `capture-pane` / `send-keys` 时的误控风险。

## 设计目标

- **先观察再控制**：所有发送动作都要求目标 pane 存在，并优先输出最近上下文。
- **默认脱敏**：读取 pane 输出时自动遮蔽常见 token、API key、password、Bearer token。
- **拒绝危险动作**：`rm -rf`、`git reset --hard`、`git clean -fd`、`tmux kill-server` 等命令默认拒绝，必须显式 `--force`。
- **批量动作可解释**：scan/rescue 都基于明确 session、pane、pattern 和 reply，不做无条件广播。
- **交接报告只读**：brief 汇总 doctor、topology、scan 和 state report，不发送按键、不改变 tmux 状态。
- **不改用户配置**：脚本只操作 tmux server，不写 `~/.tmux.conf`；oh-my-tmux 配置仍走 `assets/oh-my-tmux` 参考入口。

## 子命令总览

| 子命令 | 用途 | 风险控制 |
|:---|:---|:---|
| `doctor` | 检查 tmux、脚本、资产、session 健康状态 | 只读诊断 |
| `topology` | 列出 session/window/pane 拓扑 | 只读 |
| `capture` | 读取指定 pane 最近输出 | 默认脱敏，可保存到文件 |
| `send` | 向指定 pane 发送文本或按键 | 先打印上下文，危险文本需 `--force` |
| `broadcast` | 向指定 session 全部 pane 发送文本或按键 | 必须显式 session，支持 `--dry-run` |
| `rescue` | pattern 命中后发送确认 | 不命中不发送 |
| `scan` | 批量巡检 pane 输出 | 可按 session 限定范围 |
| `record` | 开启/停止 pane 输出审计日志 | 文件写入到显式目录 |
| `snapshot` | 导出拓扑和 pane 输出证据包 | 默认脱敏，写入显式目录 |
| `hub` | 初始化 AI 多终端工作台 | 已存在 session 不覆盖 |
| `wait` | 等待 pane 输出出现某个 pattern | 超时失败 |
| `swarm-brief.sh` | 生成只读交接报告 | 不发送按键，只汇总证据 |
| `swarm-watch.sh` | 有限轮次巡检 pane 输出和状态 | 不默认无限循环 |
| `swarm-dispatch.sh` | 渲染并可选下发提示词 | 默认只写文件，发送需 `--send` |
| `validate-auto-tmux.sh` | 执行技能专属质量门禁 | 覆盖脚本、文档索引、strict 和 smoke |

## 典型流程

### 0. 诊断环境

```bash
skills/auto-tmux/scripts/auto-tmux.sh doctor --session ai-hub
```

### 1. 建立 AI 工作台

```bash
skills/auto-tmux/scripts/auto-tmux.sh hub --session ai-hub --workers 3 --cmd "codex"
```

验收：

```bash
skills/auto-tmux/scripts/auto-tmux.sh topology --session ai-hub
```

### 2. 巡检全部 worker

```bash
skills/auto-tmux/scripts/auto-tmux.sh scan --session ai-hub -n 100
```

只看错误：

```bash
skills/auto-tmux/scripts/auto-tmux.sh scan --session ai-hub --pattern "ERROR|Traceback|failed"
```

保存巡检日志：

```bash
skills/auto-tmux/scripts/auto-tmux.sh scan --session ai-hub --save-dir /tmp/auto-tmux-scan
```

受控广播前先预览：

```bash
skills/auto-tmux/scripts/auto-tmux.sh broadcast --session ai-hub --text "pwd" --enter --dry-run
```

生成完整证据快照：

```bash
skills/auto-tmux/scripts/auto-tmux.sh snapshot --session ai-hub --dir /tmp/auto-tmux-snapshot -n 120
```

生成可交接的蜂群报告：

```bash
skills/auto-tmux/scripts/swarm-brief.sh --session ai-hub --swarm-dir /tmp/ai_swarm --out /tmp/auto-tmux-brief -n 80
```

采集连续巡检证据：

```bash
skills/auto-tmux/scripts/swarm-watch.sh --session ai-hub --swarm-dir /tmp/ai_swarm --iterations 3 --interval 10 -n 80
```

执行 auto-tmux 专属质量门禁：

```bash
skills/auto-tmux/scripts/validate-auto-tmux.sh
skills/auto-tmux/scripts/validate-auto-tmux.sh --no-smoke
```

渲染并预演下发 worker prompt：

```bash
target="$(tmux list-panes -t ai-hub:worker1 -F '#S:#I.#P' | head -n 1)"
skills/auto-tmux/scripts/swarm-dispatch.sh --role worker --target "$target" --task "只运行 make test" --send --dry-run
```

### 3. 安全发送命令

```bash
target="$(tmux list-panes -t ai-hub:worker1 -F '#S:#I.#P' | head -n 1)"
skills/auto-tmux/scripts/auto-tmux.sh send -t "$target" --text "make test" --enter
```

如果要清空当前输入行后发送：

```bash
target="$(tmux list-panes -t ai-hub:worker1 -F '#S:#I.#P' | head -n 1)"
skills/auto-tmux/scripts/auto-tmux.sh send -t "$target" --clear --text "make lint" --enter
```

### 4. 自动救援等待确认的 pane

```bash
target="$(tmux list-panes -t ai-hub:worker1 -F '#S:#I.#P' | head -n 1)"
skills/auto-tmux/scripts/auto-tmux.sh rescue -t "$target" --pattern "(y/n)" --reply y
```

先演练不发送：

```bash
target="$(tmux list-panes -t ai-hub:worker1 -F '#S:#I.#P' | head -n 1)"
skills/auto-tmux/scripts/auto-tmux.sh rescue -t "$target" --pattern "(y/n)" --reply y --dry-run
```

### 5. 等待任务完成信号

```bash
target="$(tmux list-panes -t ai-hub:worker1 -F '#S:#I.#P' | head -n 1)"
skills/auto-tmux/scripts/auto-tmux.sh wait -t "$target" --pattern "BUILD SUCCESS|Tests passed" --timeout 300
```

### 6. 开启审计日志

```bash
target="$(tmux list-panes -t ai-hub:worker1 -F '#S:#I.#P' | head -n 1)"
skills/auto-tmux/scripts/auto-tmux.sh record start -t "$target" --dir /tmp/auto-tmux-records
```

停止：

```bash
target="$(tmux list-panes -t ai-hub:worker1 -F '#S:#I.#P' | head -n 1)"
skills/auto-tmux/scripts/auto-tmux.sh record stop -t "$target"
```

## AI 蜂群协作建议

推荐结构：

```text
ai-hub
├── commander  # 人类或主 Agent：分配任务、巡检、验收、回收证据
├── worker1    # 子任务 1
├── worker2    # 子任务 2
└── worker3    # 子任务 3
```

最小协议：

1. commander 只通过明确 pane 目标发送任务，不盲发广播。
2. worker 输出完成状态、失败原因、修改文件和验证结果。
3. commander 用 `scan` 收集状态，用 `capture` 保留证据。
4. 需要确认输入时，用 `rescue --dry-run` 先验证 pattern，再真实发送。
5. 长任务用 `record start` 留日志，结束后 `record stop`。
6. 多 worker 修改同一文件、目录或服务前，用 `swarm-state.sh lock-acquire` 声明锁。

## 状态与锁脚本

初始化状态目录：

```bash
skills/auto-tmux/scripts/swarm-state.sh init --dir /tmp/ai_swarm
```

添加并认领任务：

```bash
skills/auto-tmux/scripts/swarm-state.sh task-add --id task-001 --text "检查 README 链接"
skills/auto-tmux/scripts/swarm-state.sh task-claim --id task-001 --owner "ai-hub:2.1"
skills/auto-tmux/scripts/swarm-state.sh task-next --owner "ai-hub:2.1"
```

标记阻塞或失败：

```bash
skills/auto-tmux/scripts/swarm-state.sh task-block --id task-001 --owner "ai-hub:2.1" --reason "等待用户确认"
skills/auto-tmux/scripts/swarm-state.sh task-fail --id task-001 --owner "ai-hub:2.1" --reason "make test failed"
```

获取文件锁：

```bash
skills/auto-tmux/scripts/swarm-state.sh lock-acquire --name README.md --owner "ai-hub:2.1"
```

完成任务并生成报告：

```bash
skills/auto-tmux/scripts/swarm-state.sh task-done --id task-001 --owner "ai-hub:2.1" --result "make test passed"
skills/auto-tmux/scripts/swarm-state.sh report
```

## 验证命令

```bash
bash -n skills/auto-tmux/scripts/auto-tmux.sh
bash -n skills/auto-tmux/scripts/swarm-state.sh
bash -n skills/auto-tmux/scripts/swarm-brief.sh
bash -n skills/auto-tmux/scripts/swarm-watch.sh
bash -n skills/auto-tmux/scripts/render-swarm-prompt.sh
bash -n skills/auto-tmux/scripts/swarm-dispatch.sh
bash -n skills/auto-tmux/scripts/validate-auto-tmux.sh
skills/auto-tmux/scripts/auto-tmux.sh help
skills/auto-tmux/scripts/swarm-state.sh help
skills/auto-tmux/scripts/swarm-brief.sh --help
skills/auto-tmux/scripts/validate-auto-tmux.sh --no-smoke
skills/auto-tmux/scripts/render-swarm-prompt.sh commander --session ai-hub --task "smoke"
skills/auto-tmux/scripts/auto-tmux-smoke-test.sh
skills/auto-skill/scripts/validate-skill.sh skills/auto-tmux --strict
```
