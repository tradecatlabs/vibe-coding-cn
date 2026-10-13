# Audit Case Sampling Decision

- Source: governance/tasks/0018-deepen-mathematical-problem-solving
- Fixed Problem: 任务生成器把 Anti-Goal 写成“不得修改任务目录外路径”，与已编译 Task Intent 的 `operators/`、`research/`、`docs/` 和治理范围矛盾；收口时已改回真实边界。
- Decision: no-case
- Case ID: CASE-0003
- Case Path: skills/workflow/modules/review/audit-cases/cases/CASE-0003-task-closeout-status-drift/CASE.md
- Root Cause Class: task-status-drift
- Trigger Signals: 任务范围、TODO、STATUS、验收清单或 closeout 与实际证据不一致。
- Evidence: 本任务的机器意图、验收文档、执行清单、状态表、验收清单和本地审查记录。
- No-Case Reason: 已有 CASE-0003 明确覆盖任务文档与真实范围/状态漂移，当前 validator 与人工 deep review 能直接发现；本轮没有新的根因类别、审计问题或机械检测缺口，因此不重复建案。

## Decision Values

- `case-created`
- `case-updated`
- `project-overlay`
- `promoted-to-gate`
- `no-case`
