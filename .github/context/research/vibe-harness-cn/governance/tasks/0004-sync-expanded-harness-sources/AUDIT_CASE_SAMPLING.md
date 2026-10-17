# Audit Case Sampling Decision

- Source: governance/tasks/0004-sync-expanded-harness-sources
- Fixed Problem: 审查发现按 Claude Code 的 CLI 与 OpenHands 的 agent 产品形态分别创建“无核心源码”可见性枚举，会让元 Harness 类型系统围绕供应商形态持续增长。
- Decision: no-case
- Case ID: -
- Case Path: -
- Root Cause Class: product-shape-specific-visibility-taxonomy
- Trigger Signals: source visibility, CLI core, agent core, Harness core, enum proliferation
- Evidence: governance/tasks/0004-sync-expanded-harness-sources/REVIEW.md；research/upstreams.sources.json；tests/test_sync_upstreams.sh。
- No-Case Reason: 这是本项目 source registry 的首次局部 taxonomy 漂移，已在 owning registry 中统一为稳定 Harness core 状态并由精确集合回归覆盖；现有 wrong-concept-preservation 与 Ponytail review 已能提出同类审计问题，尚无第二个跨项目实例证明需要新增全局案例。

## Decision Values

- `case-created`
- `case-updated`
- `project-overlay`
- `promoted-to-gate`
- `no-case`

## Rule

每次问题修复后都必须填写采样判定。`no-case` 不是跳过；它必须给出明确理由。
