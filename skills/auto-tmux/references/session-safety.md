# auto-tmux Session Safety

本文件定义 `auto-tmux` 在本地 session、远程 SSH session 和多 AI 蜂群协作中的安全边界。核心原则：先只读取证，再决定是否控制；远程默认只读，控制必须回到明确 pane、明确命令、明确验收的本地执行路径。

## 分层安全模型

| 层级 | 典型动作 | 默认策略 | 允许升级条件 |
|:---|:---|:---|:---|
| 只读观察 | `topology`、`inspect`、`capture`、`scan`、`snapshot`、`remote-readonly.sh` | 允许 | 不需要升级 |
| 本地单 pane 控制 | `send`、`paste`、`rescue` | 谨慎允许 | 已确认 target、上下文和 payload |
| 本地批量控制 | `broadcast`、`swarm-dispatch --send` | 默认 dry-run | 白名单、dry-run、payload 安全检查通过 |
| session 清理 | `cleanup` | 默认 dry-run | 明确 session 且显式 `--force` |
| 远程控制 | SSH 后发送按键、执行写操作、清理远端 session | 禁止作为默认路径 | 另行人工确认，不由 `remote-readonly.sh` 执行 |

## 远程只读规则

`scripts/remote-readonly.sh` 只用于采集远端 tmux 证据。它的远端动作必须限定为：

- `tmux has-session`
- `tmux list-sessions`
- `tmux list-windows`
- `tmux list-panes`
- `tmux capture-pane`

禁止把它扩展为：

- `tmux send-keys`
- `tmux kill-session`
- `tmux kill-server`
- 修改远端 `~/.tmux.conf` 或 shell 配置
- 执行 `git reset`、`rm`、`docker`、数据库写入等非 tmux 只读命令

## 发送前检查

任何会改变 pane 状态的动作，必须满足：

1. target 使用 `<session>:<window>.<pane>` 绝对定位。
2. 先通过 `inspect` 或 `capture` 查看最近输出。
3. 对长文本、文件和 prompt 运行 `scripts/safety-check.sh`。
4. 批量发送先 `--dry-run`，确认目标集合后再执行。
5. 发送后立刻 capture 保存结果，不能只相信命令返回值。

推荐流程：

```bash
target="ai-hub:1.0"
skills/auto-tmux/scripts/auto-tmux.sh inspect -t "$target" -n 40
skills/auto-tmux/scripts/safety-check.sh --text "make test"
skills/auto-tmux/scripts/auto-tmux.sh send -t "$target" --text "make test" --enter
skills/auto-tmux/scripts/auto-tmux.sh capture -t "$target" -n 80
```

## 敏感信息处理

- 输出证据默认脱敏；发现 token、API key、password、Bearer、`sk-` 等内容时不在报告中原样保留。
- 远程采集结果写入显式输出目录，避免混入仓库。
- 不把 `/tmp/auto-tmux-*` 证据包直接提交到 Git。
- 需要分享证据时，优先分享摘要、状态、错误类型和可复现命令，不分享完整 pane 历史。

## 多 Agent 协作边界

多 Agent 共用 tmux 时，安全问题通常来自“误控”和“重复写”。执行前必须先区分：

- commander：分配任务、巡检、验收、归档。
- worker：只处理分配给自己的任务。
- reviewer：只读审查 worker 产出。

并发写同一文件、目录或服务前，必须使用 `swarm-state.sh lock-acquire` 声明锁；发现锁冲突时不继续发送任务。

## 回滚与复盘

出现误发送、误广播或错误清理风险时：

1. 立即停止继续发送。
2. `capture` 保存目标 pane 的当前输出。
3. `swarm-blockers.sh` 记录阻塞或失败。
4. `swarm-archive.sh` 打包证据。
5. 在任务记录中写明误操作范围、已执行命令、影响对象、修复动作和防复发规则。

## 验收

```bash
skills/auto-tmux/scripts/remote-readonly.sh --host example.com --session ai-hub --dry-run
skills/auto-tmux/scripts/safety-check.sh --text "make test"
skills/auto-tmux/scripts/validate-auto-tmux.sh
```
