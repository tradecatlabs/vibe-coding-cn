---
name: math-proof
description: "严格自然语言数学证明。用于证明或审查 theorem/lemma/proposition、补齐证明草稿、构建证明义务与依赖图、寻找反例、检查量词/常数/边界情况，或判断命题是否必须削弱。"
---

# Math Proof

产出可审计的证明包；命题不成立或条件不足时，优先反驳或修正，不制造漂亮假证明。

## Position in the Method Map

本 skill 位于“演绎验证 / 定理证明”的 proof-engineering 阶段，前置是 [`FORMAL-METHODS-MAP.md`](../../../governance/standards/FORMAL-METHODS-MAP.md) 所定义的规格与语义边界。证明草稿、引理图和自然语言审查不会自动等同于 Lean kernel check；需要形式化时交给 `math-formalization`，需要有限反例或 SMT 路径时交给 `math-computation`。

## When to Use This Skill

- 用户要求证明、补全或检查一个数学命题。
- 当前证明含“显然”“类似”“标准论证”等可能隐藏缺口的跳步。
- 需要将大结论拆成引理、证明义务和依赖图。
- 需要从边界值、退化情形或量词顺序寻找反例。

## Not For / Boundaries

- 候选库条目必须先形成精确用户请求或 active ProblemContract；来源状态、目录题面或 candidate formal file 不能触发研究证明或 Result 晋升。
- 自然语言证明只能达到 `proof-drafted` 或经真实人工审查后的 `human-reviewed`。
- `kernel-checked` 只由 `math-formalization` 的真实 proof assistant 成功证据产生。
- 不静默强化假设、缩小定义域或改变结论量词。
- 引用标准定理时必须说明名称、版本/来源和为何满足前提。
- 证明义务图出现重复 ID、未知依赖、循环或未闭合节点时必须 fail-closed，不能 warning 后继续。
- 子引理被反驳只否定当前证明路线；除非反例直接满足原命题的否定，不能把原命题标记 `refuted`。

## Quick Reference

```text
Claim：精确陈述与量词顺序。
Status：provable-as-stated / repaired / refuted / blocked。
Assumptions：显式、隐藏和最小必要条件。
Proof obligations：每个非平凡蕴含一个义务。
Dependency map：结论 -> 引理 -> 外部定理 -> 假设。
Graph gate：节点 ID 唯一、依赖存在、无环、所有终点可追溯到 Claim。
Attack pass：边界、退化、极端尺度、量词交换、等号条件。
Proof：编号步骤，每步绑定义务或已验证结果。
Open gaps：任何未闭合项都会阻止完成声明。
Route status：open / blocked / refuted / closed，与 Claim status 分开记录。
```

## Examples

### Example 1：命题为假
- 输入：一个全称不等式。
- 动作：先检查边界和小规模反例，再决定证明策略。
- 验收：找到反例后停止写证明，输出最小反例和可能修正版。

### Example 2：缺少紧致性
- 输入：证明草稿在极值存在性处跳步。
- 动作：隔离存在性义务，核查连续性、闭性和有界性。
- 验收：条件不足时状态为 repaired/blocked，不写“显然存在”。

### Example 3：完整证明草稿
- 输入：陈述、假设与若干已知引理。
- 动作：建立依赖图，逐项闭合证明义务并做反例攻击。
- 验收：statement 与实际证明完全一致，仍标记 `proof-drafted` 而非 kernel-checked。

### Example 4：路线引理为假
- 输入：某条证明路线依赖一个可被反例推翻的辅助引理。
- 动作：将该 route 标记 refuted，检查反例是否也反驳原 Claim，并保留其他独立路线。
- 验收：没有原命题反例时，Claim 仍为 blocked/open，而不是 refuted。

## References

- `references/source-map.md`：证明、审稿、proof DAG 与批判性思考来源映射。
- `references/pressure-tests.md`：错误命题、DAG 完整性、路线状态与隐藏缺口压力场景。

## Maintenance

- Sources：`annals-of-mathematics-skills`、`kdense-scientific-skills`、`proofflow`、`leanprover-skills`；上游图与 skill 只作方法/反例来源，不代表本项目已安装或验证。
- Last updated：2026-08-26。
- Verification：项目结构校验；数学正确性需要人工或 proof assistant 证据。
