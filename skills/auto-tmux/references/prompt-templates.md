# Swarm Prompt Templates

`scripts/render-swarm-prompt.sh` 用于渲染 tmux 蜂群协作的 commander、worker、reviewer，以及单 worker Codex Pilot Mode 的 `codex-worker` 提示词。它把常用协作协议固化成可复制模板，避免每次手写时遗漏边界、状态、锁和验收要求。

## 子命令

| 角色 | 命令 | 用途 |
|:---|:---|:---|
| commander | `render-swarm-prompt.sh commander` | 任务拆分、巡检、救援、验收 |
| worker | `render-swarm-prompt.sh worker` | 执行单一子任务并回报证据 |
| reviewer | `render-swarm-prompt.sh reviewer` | 独立审查 worker 产出 |
| codex-worker | `render-swarm-prompt.sh codex-worker` | Codex Pilot Mode 中的持久化交互式 worker Codex |

## Commander Prompt

```bash
bash skills/auto-tmux/scripts/render-swarm-prompt.sh commander \
  --session ai-hub \
  --swarm-dir /tmp/ai_swarm \
  --task "重构 README 实验性方法入口"
```

适用场景：

- 开始一个多 worker 协作任务。
- 需要统一任务拆分、锁、巡检和验收。
- 需要让 commander 只做调度，不直接混入 worker 实现。

## Worker Prompt

先获取 worker target：

```bash
target="$(tmux list-panes -t ai-hub:worker1 -F '#S:#I.#P' | head -n 1)"
```

渲染 worker 提示词：

```bash
bash skills/auto-tmux/scripts/render-swarm-prompt.sh worker \
  --session ai-hub \
  --target "$target" \
  --swarm-dir /tmp/ai_swarm \
  --task "只检查 docs/research/README.md 的链接和锚点"
```

适用场景：

- 给某个 worker 下发边界清晰的单一任务。
- 需要强制 worker 在修改前加锁，完成后写状态和结果。
- 需要让 worker 汇报修改文件、验证结果、风险和下一步。

## Reviewer Prompt

```bash
bash skills/auto-tmux/scripts/render-swarm-prompt.sh reviewer \
  --session ai-hub \
  --swarm-dir /tmp/ai_swarm \
  --task "审查本轮 auto-tmux 脚本和文档改动"
```

适用场景：

- worker 完成后，需要另一个 AI 做独立审查。
- 需要重点检查 correctness、越界修改、缺失测试、文档不同步。
- 需要避免同一上下文自我确认。

## Codex Worker Prompt

`codex-worker` 用于单 worker 的 Codex Pilot Mode：主 Codex 控制一个持久化、交互式、对人类可见的 worker Codex pane。

```bash
bash skills/auto-tmux/scripts/render-swarm-prompt.sh codex-worker \
  --session codex-pilot \
  --target codex-pilot:worker.0 \
  --task "进入持久 worker 待命状态，等待主 Codex 后续分派任务"
```

适用场景：

- 你只想让主 Codex 控制一个可旁观的交互式子 Codex。
- 需要主 Codex 做上下文治理、提示词工程、过程监督和最终验收。
- 需要 worker Codex 保持在 tmux pane 中持久运行，而不是用无头 `codex exec`。

## 推荐下发方式

优先使用封装脚本渲染并预演：

```bash
bash skills/auto-tmux/scripts/swarm-dispatch.sh \
  --role worker \
  --target "$target" \
  --task "运行 make test 并分析失败" \
  --send \
  --dry-run
```

Codex Pilot Mode 下发示例：

```bash
bash skills/auto-tmux/scripts/swarm-dispatch.sh \
  --role codex-worker \
  --target codex-pilot:worker.0 \
  --session codex-pilot \
  --task "进入持久 worker 待命状态，等待主 Codex 后续分派任务" \
  --send \
  --dry-run
```

渲染到临时文件：

```bash
bash skills/auto-tmux/scripts/render-swarm-prompt.sh worker \
  --target "$target" \
  --task "运行 make test 并分析失败" \
  > /tmp/worker-prompt.md
```

发送到 worker：

```bash
bash skills/auto-tmux/scripts/auto-tmux.sh send \
  -t "$target" \
  --text "$(cat /tmp/worker-prompt.md)" \
  --enter
```

长 prompt 可以用 tmux buffer 粘贴：

```bash
bash skills/auto-tmux/scripts/auto-tmux.sh paste \
  -t "$target" \
  --file /tmp/worker-prompt.md \
  --enter \
  --dry-run
```

## 注意事项

- Prompt 只定义职责和边界，不替代测试、lint、diff、CI 等硬门禁。
- commander、worker、reviewer 应使用不同 pane，避免角色混淆。
- Codex Pilot Mode 默认只使用一个 `codex-worker` pane；不要扩展成多 worker，除非用户明确要求。
- 长任务必须配合 `record`、`snapshot` 或 `swarm-brief.sh` 保留证据。
- 多 worker 修改同一资源前必须配合 `swarm-state.sh lock-acquire`。
