# auto-tmux Iteration Roadmap

本文件用于追踪 `auto-tmux` 的多轮迭代，避免后续重复补同一类能力。每轮迭代必须同时满足：脚本或文档有明确增量、`auto-tmux` 专属门禁通过、`auto-skill --strict` 通过、全仓 `make test` 通过。

## 已完成能力

| 轮次 | 提交 | 能力层 | 交付物 |
|:---|:---|:---|:---|
| 1 | `843fe5f` | 技能创建 | 初始 `auto-tmux` skill |
| 2 | `dd97365` | 自动化入口 | `auto-tmux.sh` 基础自动化 |
| 3 | `55555c2` | 蜂群工具 | `swarm-state.sh` 与协作脚本雏形 |
| 4 | `feb6baf` | prompt 工具 | commander / worker / reviewer prompt 渲染 |
| 5 | `f072055` | 交接报告 | `swarm-brief.sh`、`task-next`、`task-block`、`task-fail` |
| 6 | `11fbb2a` | 质量门禁 | `validate-auto-tmux.sh` |
| 7 | `04f3ffc` | prompt 下发 | `swarm-dispatch.sh` |
| 8 | `bc332b3` | 连续巡检 | `swarm-watch.sh` |
| 9 | `bec9b77` | 锁治理 | `lock-prune --older-than` |
| 10 | `3f5b0fb` | 状态校验 | `swarm-state.sh validate` |
| 11 | `ce8a2a7` | 任务导入 | `task-import --file` |
| 12 | `84a0139` | 任务重试 | `task-list --status/--owner`、`task-reopen` |
| 13 | `7f5fc7a` | 状态度量 | `swarm-state.sh metrics` |
| 14 | `b8e77f6` | pane 取证 | `auto-tmux.sh inspect` |
| 15 | `bc37fc1` | 长文本粘贴 | `auto-tmux.sh paste --file` |
| 16 | `075a803` | session 清理 | `auto-tmux.sh cleanup --session` |
| 17 | `dc59ee2` | 任务依赖 | `task-depend`、`task-ready` |
| 18 | `42bca78` | 结果归档 | `swarm-archive.sh` |
| 19 | `07ac877` | 安全策略 | `safety-check.sh`、`safety-policy.md` |
| 20 | `6d46748` | 状态可视化 | `swarm-board.sh` |
| 21 | `d8e7d31` | 依赖领取一致性 | `task-next` 尊重 `blocked-by` |
| 22 | `cc69865` | worker 分配 | `swarm-assign.sh` |
| 23 | `004d942` | replay 审计 | `record-summary.sh` |
| 24 | `16afbee` | 健康检查 | `swarm-health.sh` |
| 25 | `38ccefe` | shell completion | `completion.bash` |
| 26 | `9e33018` | 依赖可视化 | `swarm-deps-graph.sh` |
| 27 | `f98841d` | 机器可读导出 | `swarm-export.sh` |
| 28 | `c6eeb1f` | 状态时间线 | `swarm-timeline.sh` |
| 29 | `本轮` | 阻塞报告 | `swarm-blockers.sh` |

## 后续候选方向

| 优先级 | 方向 | 说明 |
|:---|:---|:---|
| P3 | 远程 session | SSH 场景下的只读拓扑和安全边界 |

## 每轮验收清单

```bash
skills/auto-tmux/scripts/validate-auto-tmux.sh
skills/auto-skill/scripts/validate-skill.sh skills/auto-tmux --strict
git diff --check
make test
```

## 维护规则

- 新增脚本必须接入 `validate-auto-tmux.sh` 或 `auto-tmux-smoke-test.sh`。
- 新增状态字段必须同步更新 `swarm-state.md`、`automation.md` 和 smoke test。
- 新增 prompt 或协作协议必须同步更新 `prompt-templates.md` 或 `ai-swarm-collaboration.md`。
- 迭代完成后追加本文件的已完成能力表，避免重复实现。
