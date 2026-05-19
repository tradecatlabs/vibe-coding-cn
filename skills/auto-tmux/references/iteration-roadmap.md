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
| 29 | `4417e87` | 阻塞报告 | `swarm-blockers.sh` |
| 30 | `0cabf50` | 报告包 | `swarm-report-pack.sh` |
| 31 | `565352b` | 远程只读采集 | `remote-readonly.sh` |
| 32 | `4a35cbc` | session 安全策略 | `session-safety.md` |
| 33 | `ff8cd86` | 远程证据包增强 | `remote-readonly.sh` 输出 `metadata.jsonl`，validator 覆盖 fake SSH |
| 34 | `5677df3` | 报告附件索引 | `swarm-report-pack.sh --attach` |
| 35 | `7a2ff13` | 报告包 manifest | `swarm-report-pack.sh` 输出根级 `manifest.json` |
| 36 | `9eac52f` | 报告包压缩 | `swarm-report-pack.sh --tar` |
| 37 | `ab6d8f2` | worker 结果收敛 | `swarm-results.sh` |
| 38 | `3b10fb6` | 结果摘要导出 | `swarm-results.sh --jsonl` |
| 39 | `842cd2d` | JSONL 字段门禁 | `check-jsonl.sh` |
| 40 | `2824c06` | JSONL 格式治理 | `jsonl-schema.md` |
| 41 | `a74be2c` | 交付包审计清单 | `review-checklist.sh` |
| 42 | `01b4a6f` | 审计清单结果门禁 | `review-checklist.sh --strict` |
| 43 | `82486a7` | report pack 自检命令 | `verify-report-pack.sh` |
| 44 | `d448fdb` | report pack 自检文档 | `report-pack-review.md` |
| 45 | `63d7831` | 文档摘要索引 | `reading-paths.md` |
| 46 | `07d4850` | 操作事故 runbook | `incident-runbook.md` |
| 47 | `d6a309f` | 事故报告脚本 | `incident-report.sh` |
| 48 | `1ac2ee4` | 脚本清单速查 | `script-cheatsheet.md` |
| 49 | `022d812` | 包一致性审计 | `audit-package.sh` |
| 50 | `2b96f6e` | 迭代收尾说明 | `iteration-closeout.md` |

## 后续候选方向

| 优先级 | 方向 | 说明 |
|:---|:---|:---|
| P3 | 示例包 | 增加最小可复制的 `/tmp/ai_swarm` 示例数据，方便演示报告链路 |

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
