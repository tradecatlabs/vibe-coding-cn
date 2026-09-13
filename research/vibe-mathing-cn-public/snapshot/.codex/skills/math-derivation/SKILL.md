---
name: math-derivation
description: "数学公式与理论线推导。用于整理散乱公式、固定不变量和记号、推导恒等式/近似/局部命题、检查隐藏假设，或把理论笔记变成可审计推导包。"
---

# Math Derivation

建立诚实、可检查的推导链；不把解释、近似或数值现象伪装成严格证明。

## Position in the Method Map

本 skill 连接“规格与语义”到“演绎验证/定理证明”：它先保持 ProblemContract 的定义和量词不变，再将论证拆成可复核的中间命题。它不是 Lean elaboration，也不是自动化求解器；需要形式化 proof term 时转交 `math-formalization`。地图总览见 [`FORMAL-METHODS-MAP.md`](../../../governance/standards/FORMAL-METHODS-MAP.md)。

## When to Use This Skill

- 用户要求推导公式、整理理论线或解释等式来源。
- 当前公式混用了不同对象、极限、尺度或适用域。
- 需要将全局量分解为可解释项，或从一般模型收敛到可验证特例。

## Not For / Boundaries

- CandidateObservation 未形成明确用户目标或 active ProblemContract 时回到 `math-discovery`；不得用推导文本替候选完成准入。
- 完整定理证明交给 `math-proof`。
- 具体符号/数值检查交给 `math-computation`，其结果只是证据层。
- 不静默增加假设、交换极限/积分、忽略收敛条件或改变目标对象。

## Quick Reference

```text
Target：要得到什么，角色是 identity / proposition / approximation / interpretation？
Invariant object：贯穿推导的唯一顶层对象是什么？
Assumptions：显式、隐藏、局部、渐近和正则性条件。
Notation：每个符号先定义，一物一名。
Map：中间恒等式/引理、每步所用假设、近似进入位置。
Checks：维度、定义域、边界、极限、特例、符号与数值反算。
Status：coherent / coherent-after-reframing / blocked。
```

## Examples

### Example 1：精确恒等式
- 输入：需要证明两个代数表达式等价。
- 动作：固定定义域和变量假设，逐步变形，再交给 SymPy 做差为零检查。
- 验收：区分纸面推导与 `symbolically-checked`，不标记 kernel-checked。

### Example 2：渐近近似
- 输入：推导大样本近似。
- 动作：标明极限变量、余项、均匀性和常数依赖。
- 验收：结论含适用域和误差阶，不把近似写成恒等式。

### Example 3：目标对象错误
- 输入：局部代理量被当作全局目标。
- 动作：指出对象切换，重构为“全局量 → 分解 → 局部切片”。
- 验收：状态为 `coherent-after-reframing` 并保留原目标差异。

## References

- `references/source-map.md`：推导方法来源和未吸收边界。
- `references/pressure-tests.md`：隐藏假设压力场景。

## Maintenance

- Sources：`kdense-scientific-skills` 与本项目 ProblemContract/证据分层规则；不依赖未发布本机来源。
- Last updated：2026-08-13。
- Verification：`python3 scripts/smoke_math.py` 只验证计算层；推导仍需逐步审计。
