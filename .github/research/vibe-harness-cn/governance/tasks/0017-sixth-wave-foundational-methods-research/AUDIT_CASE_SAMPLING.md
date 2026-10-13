# Audit Case Sampling Decision

- Source: governance/tasks/0017-sixth-wave-foundational-methods-research
- Fixed Problem: 首轮静态校验发现新增来源记录与既有 `ref:nist-chemistry-webbook` 重复，随后复用已有 reference ID 并重新通过全库校验。
- Decision: no-case
- Case ID: -
- Case Path: -
- Root Cause Class: duplicated-reference-registration
- Trigger Signals: 新增 pack 后 Reference Profile 对 reference ID 做全库唯一性检查并 BLOCK。
- Evidence: REVIEW.md；operators/source-inventory.json；operator library validator 的重复引用 BLOCK 与修复后 PASS。
- No-Case Reason: 现有 validator 已确定性覆盖该模式且失败信息直接定位重复 ID；本轮没有发现需要新增规则、脚本或跨项目审计案例的检测缺口。若未来出现通过同步删除 inventory/pack 绕过检测，再建立单独案例。

## Decision Values

- `case-created`
- `case-updated`
- `project-overlay`
- `promoted-to-gate`
- `no-case`
