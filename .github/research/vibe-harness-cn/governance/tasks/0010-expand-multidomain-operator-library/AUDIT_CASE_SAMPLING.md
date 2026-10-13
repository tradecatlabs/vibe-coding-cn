# Audit Case Sampling Decision

- Source: governance/tasks/0010-expand-multidomain-operator-library
- Fixed Problem: 原则扫描器把跨学科算子说明中的领域词汇误识别为短期降级信号，导致 architecture/test gate 首次 BLOCK。
- Decision: no-case
- Case ID: -
- Case Path: -
- Root Cause Class: lexical-principle-scanner-false-positive
- Trigger Signals: future-optimal-drift、兼容、暂时、临时、原则扫描误报
- Evidence: governance/tasks/0010-expand-multidomain-operator-library/REVIEW.md；governance/tools/scan_principle_gates.py；本轮扫描输出。
- No-Case Reason: 本轮仅对既有词法门禁的单次误报做语义等价改写；没有改变扫描器规则，也没有出现新的设计缺陷。项目已有原则 gate 和历史任务的误报处理方式足以承载该模式，暂不足以形成独立跨项目案例；若同类误报再次阻断真实语义，应更新 scanner 的词法边界或晋升审计案例。

## Decision Values

- `case-created`
- `case-updated`
- `project-overlay`
- `promoted-to-gate`
- `no-case`

## Rule

每次问题修复后都必须填写采样判定。`no-case` 不是跳过；它必须给出明确理由。
