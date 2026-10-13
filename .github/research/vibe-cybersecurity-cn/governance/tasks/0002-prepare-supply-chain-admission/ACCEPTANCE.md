# Task-Level Acceptance

- 18 个研究 MVP 全部且仅一次进入准入目录。
- 所有候选默认禁用，具体版本和 digest 未经验证时保持空值/pending。
- active-high 或非 MVP 研究候选无法进入当前准入目录。
- `admitted` 状态必须要求固定版本和全部八个正式门禁通过；准入目录不拥有 `enabled` 状态。
- 人类可读表可由两个 JSON 真相源确定性重建。

# Validation Plan

```bash
python3 governance/tasks/0002-prepare-supply-chain-admission/validate_admission_candidates.py
python3 -m py_compile governance/tasks/0002-prepare-supply-chain-admission/validate_admission_candidates.py
python3 -m unittest governance/tasks/0002-prepare-supply-chain-admission/test_validate_admission_candidates.py
python3 <CODEX_SKILLS>/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0002-prepare-supply-chain-admission --phase closeout
python3 governance/tools/validate_governance_package.py --project-root . --strict
python3 governance/tools/governance_health_report.py --project-root . --strict
```

# Review Gate

`PASS` 仅表示候选表结构可交付；不得声称任何候选已经固定版本、本地复跑、正式纳入或启用。

# Runtime Verification Gate

`NOT_APPLICABLE`：本轮明确不改变运行时行为。替代证据是跨目录 JSON 校验、确定性表格摘要和原则/治理门禁；判断错误的风险是候选被误当成安装批准。

# Ship Readiness

- 文档和机器目录：Ready。
- 固定版本与实际供应链纳入：Not Ready，必须由后续逐项验证任务完成。
- 外部发布：未授权。

# Task Package Acceptance

## TP-01

- 状态机、八门禁、默认禁用、失效和恢复边界明确。

## TP-02

- 18 项全覆盖；每项有波次、职责、owner、风险配置、额外门禁和阻塞条件。

## TP-03

- 校验器从研究目录取事实，拒绝血缘漂移、越级状态、危险网络级别和伪固定版本。

## TP-04

- README、AGENTS、操作模型、工具链、拓扑和任务索引同步；治理 strict/health 通过。

# Anti-Goals

- 不安装或启用工具。
- 不猜测具体版本、摘要或许可证结论。
- 不新增业务运行时、数据库或插件框架。
