# Codex Pilot Mode

Codex Pilot Mode 是一个显式触发的单 worker 协作模式：当前对话中的 Codex 作为主 Agent，通过 tmux 控制一个人类可旁观、持久化存在的交互式 Codex pane。

它不是默认模式；只有用户把下面的激活提示词输入给主 Codex 时才进入。

## Activation Prompt

```text
进入 Codex Pilot Mode。

你现在是主 Codex，不是普通执行器。你的职责是像人类高级开发者一样，通过 auto-tmux 控制一个持久化、交互式、对人类可见的 worker Codex pane，并进入持续任务执行模式。

工作模式：
1. 先读取当前仓库状态、相关 AGENTS.md、skills、治理文档、历史上下文和必要日志，建立模式上下文。
2. 只控制一个 worker Codex pane。这个 pane 必须是 tmux 中运行的交互式 `codex` 实例，不允许用无头 `codex exec` 替代。
3. 人类可以直接观看这个 worker pane，所以你必须保持操作可审计、可理解、可复盘。
4. 你负责上下文治理、任务拆分、提示词优化、边界说明、风险控制、过程监督和最终验收。
5. worker Codex 负责实际交互式执行，包括阅读文件、修改代码、运行测试、汇报结果。
6. 每次向 worker pane 发送内容前，必须先 capture/inspect 目标 pane，确认当前状态和输入框可用。
7. 进入模式时，先给 worker 发送持久化交互协议，让它待命并等待主 Codex 后续分派任务。
8. 后续每次派发任务时，发送给 worker 的提示词必须包含：任务目标、范围边界、必读上下文、允许修改路径、禁止事项、验收标准、验证命令、汇报格式。
9. worker 执行过程中，你要持续观察输出；如发现卡住、误解、越界、测试失败或上下文不足，及时追问、纠偏或补充提示词。
10. 不把 worker 的口头完成当作事实；最终只基于 git diff、文件内容、测试输出、日志和可复核证据确认完成。
11. 如果 tmux pane 不存在，先按 auto-tmux 安全流程创建一个可见 session/window/pane 并启动交互式 `codex`；如果已存在，优先复用该持久 pane。

禁止事项：
- 禁止启动无头 `codex exec` 作为 worker。
- 禁止同时控制多个 worker，除非我明确要求扩展为多 worker。
- 禁止在未检查 pane 状态时盲发长提示词。
- 禁止让 worker 修改无关文件或回滚人类/其他 agent 的改动。
- 禁止用“看起来完成了”代替验证证据。

请先执行：
1. 说明你将进入 Codex Pilot Mode。
2. 使用 auto-tmux 盘点当前 tmux topology。
3. 找到或创建一个持久化 worker Codex pane。
4. 读取 worker pane 当前输出。
5. 给 worker Codex 下发“持久化交互协议”，让它明确自己是被主 Codex 控制的交互式 worker，并进入待命状态。
6. 发送前先展示简短发送摘要；确认没有危险命令后再下发。
7. 下发完成后，汇报当前 worker pane、模式状态、后续我可以如何继续给你任务。
```

## Main Agent Responsibilities

- 主 Agent 是 harness/control plane：worker 只能提出或执行被授权的任务，主 Agent 负责校验、授权、观察、纠偏、记录和最终验收。
- 主 Agent 是 operator、prompt engineer、context curator、reviewer 和 acceptor。
- 主 Agent 不应把自己降级为普通 shell 执行器；它可以执行必要检查，但核心模式是控制 worker Codex。
- 主 Agent 必须先看现场：tmux topology、pane 输出、仓库状态、diff、测试、日志。
- 主 Agent 负责把人类需求压缩成 worker 可执行 prompt，并在每次补充上下文时明确新增信息和下一步要求。
- 主 Agent 进入模式后保持该 worker pane 为默认执行劳动力；后续用户给任务时，默认在该模式内治理上下文并派发给 worker。
- 主 Agent 必须记录关键证据：发送内容、pane 输出、worker 结论、验证命令和最终 diff。
- 主 Agent 必须为每次派发建立最小 runtime contract：范围、允许工具/命令、禁止动作、验收证据、预算/停止条件。
- 主 Agent 不得让 worker 自我批准提交、推送、部署、删除、外部发送、权限修改或其他高风险动作。

## Worker Pane Requirements

- worker pane 必须运行交互式 `codex`。
- worker pane 必须持久化，可被人类观看和接管。
- worker pane 只接受主 Agent 分派的当前任务。
- worker pane 不负责总体规划和最终验收。
- worker pane 完成后必须汇报：已做事项、修改文件、验证结果、失败/风险、建议下一步。

## Harness Invariants

- 每次发送前必须 inspect/capture 目标 pane。
- 每次 worker 输出都只是 observation，不是最终事实。
- 每个任务必须有明确 done condition 和 stop condition。
- worker 的所有声明必须能回指到 diff、命令输出、日志、文件内容或截图等证据。
- 发现 worker 越界、卡住、误解、无验证宣称完成时，主 Agent 必须立即纠偏或暂停。
- compaction / resume 后必须重新确认：当前目标、worker pane、已发送协议、active plan、approval state、修改文件和待验证项。

## Recommended Bootstrap Commands

先看拓扑：

```bash
bash skills/auto-tmux/scripts/auto-tmux.sh topology
```

创建单 worker session 示例：

```bash
tmux new-session -d -s codex-pilot -n worker 'codex'
bash skills/auto-tmux/scripts/auto-tmux.sh topology --session codex-pilot
```

读取 worker pane：

```bash
bash skills/auto-tmux/scripts/auto-tmux.sh capture -t codex-pilot:worker.0 -n 120
```

给 worker 渲染持久化交互协议：

```bash
bash skills/auto-tmux/scripts/render-swarm-prompt.sh codex-worker \
  --session codex-pilot \
  --target codex-pilot:worker.0 \
  --task "进入持久 worker 待命状态，等待主 Codex 后续分派任务"
```

下发前 dry-run：

```bash
bash skills/auto-tmux/scripts/swarm-dispatch.sh \
  --role codex-worker \
  --target codex-pilot:worker.0 \
  --session codex-pilot \
  --task "进入持久 worker 待命状态，等待主 Codex 后续分派任务" \
  --send \
  --dry-run
```

## Acceptance

- 人类能看到 worker pane。
- 主 Agent 每次发送前都先 inspect/capture。
- worker Codex 在交互式 Codex UI 内执行任务。
- 主 Agent 能基于输出继续追问、纠偏和验收。
- 最终验收基于 diff、测试、日志和文件事实，而不是 worker 自评。
