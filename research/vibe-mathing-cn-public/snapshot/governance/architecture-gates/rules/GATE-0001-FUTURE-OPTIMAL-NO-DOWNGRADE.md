---
id: GATE-0001
type: gate
status: active
owner: engineering
created: 2026-08-13
last_reviewed: 2026-08-13
review_cycle: P90D
severity: BLOCK
detectability: agent+script+manual
source: STD-FUTURE-OPTIMAL
---

# 非平凡方案不得主动降级成短期补丁

## 阻止条件

非平凡方案、架构、重构、任务拆分或治理规则没有说明 target end state、real constraints、inertia constraints、kill list、proof point、falsifier 和 migration slice，或者因实现成本、迁移恐惧、内部调用方成本、旧命名/旧目录惯性而主动降级成不通向终态的短期补丁。

## 原因

代码编写成本不是默认约束。真正昂贵的是错误概念、错误边界、缺失测试、缺失门禁、缺失迁移路径和长期质量债。

## 检查方式

- Script：`python3 governance/tools/scan_principle_gates.py --repo . --git-mode working --strict`。
- Agent review：使用 `auto-review` 的 `future-optimal-drift` profile。
- 人工审查：检查真实约束与惯性约束是否混写，短期切片是否通向目标终态。
- 治理审查：涉及架构或治理决策时，ADR 必须包含 target end state、rejected short-term patches 和 migration path。

## 可操作错误提示

你给出了能跑的短期方案，但没有证明它通向长期正确结构。请先写清目标终态、真实约束、惯性约束、kill list、proof point、falsifier 和本轮迁移切片；如果保留兼容层，请说明真实 contract、移除条件和后续任务。

## 最小修复

- 把短期补丁改成本轮可验证迁移切片；或
- 证明兼容层有真实外部 contract 并记录移除条件；或
- 明确 blocker，停止声明该目标已完成。
