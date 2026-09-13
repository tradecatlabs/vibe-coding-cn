---
name: vibe-mathing-router
description: "数学研究任务路由器。用户提出找问题、查文献、推公式、做计算、写证明或形式化验证，但当前瓶颈尚未明确时使用；每次只选择一个主 skill。"
---

# Vibe Mathing Router

识别当前数学研究瓶颈，只把任务交给一个 owner；不把整条研究链同时启动。

## Position in the Method Map

路由器先问“规格和语义是否已经冻结”，再区分演绎证明、模型检查、抽象解释、SAT/SMT/符号推理（含符号执行）或精化/综合的验证范式。Lean 是依赖类型理论型演绎验证的主战场，不是整张形式化方法地图。完整的上位/二级地图见 [`FORMAL-METHODS-MAP.md`](../../../governance/standards/FORMAL-METHODS-MAP.md)。顶层编排语言见 [`RESEARCH-LIFECYCLE-MODEL-v0.1.md`](../../../governance/standards/RESEARCH-LIFECYCLE-MODEL-v0.1.md)：路由器为 Step 选择 owner，不能把一次 Job 成功解释为数学结果。

## When to Use This Skill

- 用户提出开放式数学问题，但尚未说明需要检索、推导、计算还是证明。
- 输入混合了论文、公式、猜想和代码，需要先决定当前最短验证路径。
- 用户问“下一步该做什么”或“该用哪个数学 skill”。

## Not For / Boundaries

- 已明确要求符号计算、证明或 Lean 验证时，直接使用对应 owner。
- 不生成数学结论，不替代领域知识或机械验证。
- 不因输出文件类型选择路线；按当前阻塞选择。

## Quick Reference

```text
缺少问题边界/前人工作 -> math-discovery
公式对象、假设或近似不清 -> math-derivation
需要精确计算、数值实验、反例搜索 -> math-computation
需要定理证明、补步骤、攻击证明 -> math-proof
需要 Lean/内核级验证 -> math-formalization
```

路由输出必须包含：当前阶段、主 skill、选择理由、必需输入、停止条件、唯一下一步。

## Examples

### Example 1：开放问题
- 输入：“研究一下这个数列。”
- 动作：选择 `math-discovery`，先固定数列、已知项和检索边界。
- 验收：没有直接声称新定理，只给出可检索问题。

### Example 2：明确恒等式
- 输入：“检查这个积分恒等式。”
- 动作：选择 `math-computation`。
- 验收：产出可重跑计算和适用条件，不标记为一般性证明。

### Example 3：形式化请求
- 输入：“把这个证明写成 Lean。”
- 动作：选择 `math-formalization` 并先运行工具预检。
- 验收：Lean 缺失时状态为 blocked/calibration，不伪造 kernel-check。

## References

- `references/source-map.md`：项目 owner 映射来源。
- `references/pressure-tests.md`：路由误触发压力场景。

## Maintenance

- Sources：本项目 owner mapping 与供应链审计结果。
- Last updated：2026-09-07。
- Verification：`python3 scripts/validate_project.py`。
