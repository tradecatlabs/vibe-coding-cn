# auto-tmux Iteration Closeout

本文件记录 `auto-tmux` 50 轮迭代后的收尾状态，用于后续维护者快速判断能力边界、验证路径和继续优化方向。

## 最终能力层

| 能力层 | 当前状态 | 主要入口 |
|:---|:---|:---|
| tmux 观察 | 已覆盖本地 topology、capture、inspect、scan、snapshot | `auto-tmux.sh` |
| tmux 控制 | 已覆盖 send、paste、broadcast、rescue，并接入安全预检 | `auto-tmux.sh`、`safety-check.sh` |
| 蜂群状态 | 已覆盖任务、依赖、锁、状态日志、指标和报告 | `swarm-state.sh` |
| 蜂群协作 | 已覆盖 prompt 渲染、dry-run 下发、分配建议、健康检查 | `render-swarm-prompt.sh`、`swarm-dispatch.sh`、`swarm-assign.sh`、`swarm-health.sh` |
| 只读取证 | 已覆盖本地 brief/watch/archive 和远程 SSH 只读采集 | `swarm-brief.sh`、`swarm-watch.sh`、`swarm-archive.sh`、`remote-readonly.sh` |
| 交付报告 | 已覆盖 board、deps、timeline、blockers、results、report pack、manifest、tar | `swarm-report-pack.sh` |
| 审计门禁 | 已覆盖 JSONL 字段、review checklist、report pack 验证和 package consistency | `check-jsonl.sh`、`review-checklist.sh`、`verify-report-pack.sh`、`audit-package.sh` |
| 事故复盘 | 已覆盖误发送、误广播、远程采集失败和敏感信息风险模板 | `incident-report.sh`、`incident-runbook.md` |

## 验证链路

每次修改 `skills/auto-tmux` 后，至少运行：

```bash
skills/auto-tmux/scripts/validate-auto-tmux.sh
skills/auto-skill/scripts/validate-skill.sh skills/auto-tmux --strict
git diff --check
make test
```

其中 `validate-auto-tmux.sh` 已经内置：

- Bash 语法和可执行权限检查。
- 主要脚本 `--help` 检查。
- report pack、JSONL、review checklist、incident report 和远程 fake SSH 最小验证。
- `audit-package.sh` 包索引一致性审计。
- auto-skill strict 验证。
- tmux smoke test。

## 维护边界

- 默认只读优先：观察、取证、健康检查、报告包和远程采集不得升级为隐式控制。
- 控制动作必须显式目标：send、paste、broadcast、rescue 和 dispatch 必须明确 session/window/pane 或明确 dry-run。
- 远程默认只读：`remote-readonly.sh` 不允许出现 `send-keys`、`kill-*`、配置写入或状态修改。
- 新增脚本必须同步更新 `SKILL.md`、`scripts/README.md`、`scripts/AGENTS.md`、`validate-auto-tmux.sh` 和 `script-cheatsheet.md`。
- 新增 reference 必须同步更新 `references/README.md`、`references/index.md` 和 `SKILL.md`。
- 新增机器可读输出必须同步更新 `jsonl-schema.md`，并接入 `check-jsonl.sh` 或等价门禁。

## 下一阶段候选

| 方向 | 说明 |
|:---|:---|
| 回放能力 | 从 `record-summary.sh` 产物中生成可审计 replay 摘要，但不能自动重放危险输入。 |
| CI 分层 | 把慢 smoke test 和静态包审计拆成 fast/slow 两档，便于 CI 和本地快速检查。 |
| 示例包 | 增加最小可复制的 `/tmp/ai_swarm` 示例数据，方便验证 board、timeline 和 report pack。 |
| 文档压缩 | 将长脚本清单收敛成角色化阅读路径，避免 SKILL 入口继续膨胀。 |

## 收尾结论

`auto-tmux` 已从单一 tmux 辅助脚本扩展为可观察、可控制、可协作、可取证、可审计、可复盘的 tmux 自动化技能包。后续优化应优先保持安全边界和门禁完整性，而不是继续堆叠无约束的控制能力。
