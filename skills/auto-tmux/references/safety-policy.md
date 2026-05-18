# auto-tmux Safety Policy

本文件定义 `auto-tmux` 的安全边界：什么时候只能观察，什么时候必须 dry-run，什么时候需要 `--force`，以及哪些信息不能进入共享 pane、归档或交接报告。

## 安全分层

| 层级 | 动作 | 默认策略 |
|:---|:---|:---|
| 只读观察 | `doctor`、`topology`、`inspect`、`capture`、`scan`、`snapshot`、`swarm-brief.sh`、`swarm-watch.sh`、`swarm-archive.sh` | 允许执行，输出默认脱敏 |
| 受控写入 | `send`、`paste`、`rescue`、`broadcast`、`swarm-dispatch.sh --send` | 先观察目标上下文；批量或长文本先 dry-run |
| 破坏性动作 | `cleanup --force`、危险命令文本、强制释放他人锁 | 必须显式 `--force`，并保留上下文证据 |
| 禁止自动化 | 密码输入、生产数据库变更、真实凭证分发、未知 pane 里的破坏性命令 | 交给人工确认，不由脚本静默执行 |

## 发送前检查

发送文本、粘贴文件或分发 prompt 前，先做三件事：

1. `inspect` 目标 pane，确认它是预期 session/window/pane。
2. 对 payload 运行 `scripts/safety-check.sh`。
3. 对批量发送、长 prompt 或跨 worker 下发先使用 `--dry-run`。

示例：

```bash
target="ai-hub:2.1"
skills/auto-tmux/scripts/auto-tmux.sh inspect -t "$target" -n 40
skills/auto-tmux/scripts/safety-check.sh --file /tmp/prompt.md --strict
skills/auto-tmux/scripts/auto-tmux.sh paste -t "$target" --file /tmp/prompt.md --enter --dry-run
```

## 敏感信息策略

- `capture`、`inspect`、`scan` 和 `snapshot` 默认遮蔽常见 API key、Bearer token、password、secret。
- 除非排查必须，不使用 `--no-redact`；使用后不得把原始输出写入公开文档或共享交接包。
- `swarm-state.sh` 的任务文本、结果和阻塞原因会做基础清洗，但仍不应写入真实凭证。
- `swarm-archive.sh` 会复制 state、brief 和 snapshot；归档前应确认 state 目录没有真实密钥、cookie、token 或私有用户数据。

## 危险命令策略

以下文本默认视为危险，需要显式 `--force` 或人工处理：

- `rm -rf`
- `mkfs`
- `dd if=`
- `shutdown` / `reboot` / `halt` / `poweroff`
- `tmux kill-server`
- `git reset --hard`
- `git clean -fd`
- `DROP DATABASE` / `DROP TABLE`

如果危险命令确实是任务目标，必须先说明：

1. 目标 pane 是什么。
2. 为什么必须执行。
3. 影响范围是什么。
4. 如何验证和回滚。

## 广播与分发策略

- `broadcast` 必须显式指定 `--session`，不能对全部 tmux server 盲发。
- `swarm-dispatch.sh` 默认只渲染文件；只有带 `--send` 才会下发。
- 指挥者应优先按 worker 单点下发任务，只有环境检查、状态查询等低风险命令才考虑广播。
- 广播前必须 dry-run，并确认目标 pane 列表。

## 清理与锁策略

- `cleanup` 默认只做 dry-run；真实 kill session 必须 `--force`。
- 如果 session attached，脚本会警告；仍要继续时必须由操作者承担上下文确认责任。
- `lock-release` 默认只允许 owner 释放自己的锁；释放他人锁必须 `--force`。
- `lock-prune` 先 dry-run，再真实清理过期锁。

## 交接与归档策略

- `swarm-brief.sh`、`swarm-watch.sh`、`swarm-archive.sh` 必须保持只读。
- 交接包用于恢复现场，不是长期公开材料。
- 交接包发布前至少检查：
  - 是否含真实 token、cookie、password。
  - 是否含用户隐私、私有路径或生产数据。
  - 是否含未脱敏日志。
  - 是否含不应公开的任务细节。

## 最小安全清单

```text
[ ] 已确认 target 是预期 pane。
[ ] 已 capture/inspect 最近输出。
[ ] 已对长文本或文件运行 safety-check。
[ ] 批量动作已 dry-run。
[ ] 危险动作有 force 理由、影响范围和回滚路径。
[ ] 交接包已检查敏感信息。
```
