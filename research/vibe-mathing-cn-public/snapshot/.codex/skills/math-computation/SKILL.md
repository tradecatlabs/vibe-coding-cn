---
name: math-computation
description: "可重跑的数学计算与反例实验。用于 SymPy 精确代数/微积分/方程/矩阵、NumPy/SciPy 数值方法、mpmath 高精度交叉检查、OEIS 序列识别、有限范围反例搜索和计算证据记录。"
---

# Math Computation

用成熟计算库生成可重跑证据；计算用于发现、反驳和核对，不越权成为一般性证明。

## Position in the Method Map

本 skill 覆盖形式化方法地图中的“SAT/SMT、符号执行和决策过程”横向自动化，以及有限的数值/符号实验；它不替代规格与语义、演绎证明、模型检查或抽象解释。需要 Lean proof term 和 kernel 检查时转交 `math-formalization`，需要精确定义和来源时先转交 `math-discovery`。完整地图见 [`FORMAL-METHODS-MAP.md`](../../../governance/standards/FORMAL-METHODS-MAP.md)。

## When to Use This Skill

- 需要精确化简、求解、积分、极限、级数、矩阵或多项式计算。
- 需要高精度数值交叉检查、参数扫描或有限范围反例搜索。
- 需要识别整数序列、测试猜想小规模实例或生成图表数据。
- 需要为数论、有限代数、图论、SAT/SMT、代数几何或 PDE 实验选择成熟工具。

## Not For / Boundaries

- 只有明确用户计算请求或 active ProblemContract 才能启动研究计算；CandidateObservation 必须先回到 `math-discovery` 完成准入。
- 工具只有达到 `smoke_checked` 才可生成计算证据，只有独立 verifier adapter 达到 `verifier_admitted` 才可作为验证器；survey 文档和固定源码不算运行能力。
- 浮点相等不是数学恒等；优先 exact arithmetic。
- SymPy 返回结果可能带分支、条件或未求值对象，必须检查。
- 有限枚举“未发现反例”不证明全称命题。
- 大规模矩阵/扫描必须先估算复杂度、内存和停止条件；任何计算、外部命令、solver、枚举或 Lean/CAS 子任务必须有 wall-time、内存/线程/输出预算、可登记的终止回执，禁止裸 `solve()` 或无 timeout heredoc。

## GPU 可行性预检（强制）

任何计算动手前，先运行 `python3 scripts/compute_plan.py --kind <类型> --n <规模> --dtype <精度>`，批量搜索还必须提供 `--ops-per-sample` 或 `--flops`；按输出 `route` 选择 CPU 或 GPU，并把路由决策与原因写入执行记录：

| 工具族 | 解释与说明 |
| --- | --- |
| `symbolic` 与 `mpmath` | 固定走 CPU；精确或任意精度计算没有本项目 GPU route。 |
| `small-numeric` | 固定走 CPU；单次小规模任务的 GPU 无收益。 |
| `dense-numeric` | 只有规模/运算量达阈值、精度为 f32/f64 且 GPU 可用时才考虑 GPU；否则回退 CPU。 |
| `batch-search` | 只有运算量达阈值且 GPU 可用时才考虑 GPU；GPU 只做粗筛，精确复核回 CPU。 |

- GPU 不可用、GPU 队列忙或可用内存不足时回退 CPU，并在执行记录标注原因；`COMPUTE_FORCE_CPU=1` 可强制走 CPU，节点预算由 `COMPUTE_MEMORY_BUDGET_GB` / `COMPUTE_MEMORY_HEADROOM_GB` / `COMPUTE_THREADS_MAX` 运行时注入。
- GPU 只做粗筛/预筛；结果只能作为 `numeric-check` 支持，不得提升证据等级；候选必须回 CPU 用 SymPy/mpmath/FP64 精确复核。
- 多 Agent 并行时遵守项目 AGENTS.md「计算资源与 GPU 路由（强制）」：线程上限、GPU 全局串行锁、内存水位门禁。

## Quick Reference

先按问题域运行能力探针；不得只凭包名、PATH 或 Agent 自报认定工具可用：

```bash
python3 scripts/check_math_tools.py --profile <profile> --strict
```

profile 与具体工具入口见 `references/tool-catalog.md`。项目 `.venv`、系统 Python、Sage 和 Lean 是独立运行时，禁止跨运行时猜测 import。

```python
import sympy as sp
x = sp.symbols("x", real=True)
delta = sp.simplify(lhs - rhs)
status = "symbolically-checked" if delta == 0 else "not-verified"
```

执行记录至少包含：输入表达式、假设、库版本、精确/近似模式、命令或脚本、输出、失败条件、claim level。

性能口径：符号表达式可能发生组合爆炸；矩阵稠密求解通常为 O(n^3)/O(n^2) 内存；批量数值优先 `lambdify`/向量化、稀疏结构和有界采样。

## Examples

### Example 1：恒等式检查
- 输入：`lhs = sin(x)^2 + cos(x)^2`，`rhs = 1`。
- 动作：使用实变量假设和 `trigsimp/simplify`。
- 验收：记录 SymPy 版本与差值；状态最多 `symbolically-checked`。

### Example 2：数值反例
- 输入：带参数的不等式猜想。
- 动作：先定义域，再用确定性网格与边界采样，保存首个反例。
- 验收：找到反例即 `refuted-for-stated-domain`；未找到只报告覆盖范围。

### Example 3：大矩阵
- 输入：求解大型稀疏线性系统。
- 动作：识别稀疏性和条件数，优先 SciPy sparse solver，记录残差。
- 验收：没有构造不必要的稠密副本，报告时间/内存规模变量。

### Example 4：GPU 预检与批量反例搜索
- 输入：对 10^8 个格点批量验证数值不等式猜想。
- 动作：先运行 `python3 scripts/compute_plan.py --kind batch-search --n 1e8 --ops-per-sample 200 --dtype f32`，按 `route` 选择 GPU 或 CPU；GPU 命中候选后用 SymPy/mpmath 精确复核。
- 验收：执行记录含路由决策、库版本、命中样本与复核结果；GPU 结果只标 `numeric-check`。

## References

- `references/source-map.md`：CAS、数值方法和 OEIS 来源映射。
- `references/tool-catalog.md`：数学工具、运行时、用法、profile 与证据边界。
- `references/pressure-tests.md`：数值/符号证据越权压力场景。

## Maintenance

- Sources：`wentor-research-plugins` 数学技能、`kdense-scientific-skills` 的 SymPy skill。
- Last updated：2026-08-16。
- Verification：`python3 scripts/smoke_math.py` 与 `python3 scripts/check_math_tools.py --profile <profile> --strict`；库 API 以当前官方文档和实测为准。
