---
id: MATH-TOOL-CATALOG
type: tooling
status: current
owner: engineering
created: 2026-09-01
last_reviewed: 2026-09-01
review_cycle: P90D
---

# 数学工具族目录

本目录是公开仓的能力边界与证据上限，不是某台机器的安装清单。`surveyed` 只表示已分类；
`source_locked` 只表示来源固定；`installed`、`smoke_checked`、`evidence_capable` 和
`verifier_admitted` 必须由对应的公开校验器和可复核产物支持。公开仓当前只把 SymPy 的有限
证据切片和 Lean fixture 的内核验证作为高等级入口；其余工具族不能越权进入证明或验证路由。

工具 canary 的 schema、runner 和测试逻辑可复用，但没有公开运行报告就不宣称运行时已安装；
GPU、宿主机、容器、模型和凭据不属于本目录。结果仍需绑定 ProblemContract、Attempt、
Result 与 evidence receipt。

| 工具族 | 解释与说明 |
|:---|:---|
| <a id="T01"></a>`T01` · 算筹、算盘、对数表、机械计算器 | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T02"></a>`T02` · FORTRAN、BLAS/LINPACK 传统 | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T03"></a>`T03` · Logic Theorist、resolution、Davis–Putnam | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T04"></a>`T04` · REDUCE、Macsyma/Maxima | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T05"></a>`T05` · Automath、LCF、NQTHM | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T06"></a>`T06` · Mizar、HOL、Isabelle、Coq/Rocq | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T07"></a>`T07` · Maple、Mathematica | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T08"></a>`T08` · PARI/GP、FLINT/Arb | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T09"></a>`T09` · GAP | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T10"></a>`T10` · Singular、Macaulay2 | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T11"></a>`T11` · SageMath | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T12"></a>`T12` · SymPy | `evidence_capable` / route=`evidence`；公开仓准入 `evidence_capable`；只覆盖固定 SymPy 精确算术/符号 vertical slice，不能替代通用证明器。 |
| <a id="T13"></a>`T13` · mpmath、python-flint | `surveyed` / route=`none`；公开仓仅发布 `surveyed` 分类和有界 canary 契约；没有公开运行报告，不提供 runtime route。 |
| <a id="T14"></a>`T14` · NumPy、SciPy、Julia | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T15"></a>`T15` · Z3、cvc5、SMT-LIB | `surveyed` / route=`none`；公开仓仅发布 `surveyed` 分类和有界 canary 契约；没有公开运行报告，不提供 runtime route。 |
| <a id="T16"></a>`T16` · MiniSat、CaDiCaL | `surveyed` / route=`none`；公开仓仅发布 `surveyed` 分类和有界 canary 契约；没有公开运行报告，不提供 runtime route。 |
| <a id="T17"></a>`T17` · E、Vampire、Prover9、TPTP | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T18"></a>`T18` · Lean 4/Mathlib | `verifier_admitted` / route=`verifier`；公开仓准入 `verifier_admitted`；只覆盖固定 Lean/Mathlib fixture 的 kernel、axiom 与 faithfulness 门。 |
| <a id="T19"></a>`T19` · HOL Light、Isabelle、Rocq、Metamath、ACL2 | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T20"></a>`T20` · polymake、4ti2、TOPCOM | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T21"></a>`T21` · nauty/Traces、NetworkX、igraph | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T22"></a>`T22` · OEIS、LMFDB、DLMF、TPTP | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T23"></a>`T23` · Gappa、区间算术与浮点证书 | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T24"></a>`T24` · Alethe/Eunoia、CPC、Carcara、SMTCoq | `source_locked` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T25"></a>`T25` · Isabelle/HOL + LLM prover（Isabellm） | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T26"></a>`T26` · OpenTheory / proof exchange packages | `source_locked` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T27"></a>`T27` · LeanDojo-v2 / TorchLean / ITPEval 生态 | `source_locked` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T28"></a>`T28` · Axiom / FriCAS | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T29"></a>`T29` · Macaulay2 / Singular | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T30"></a>`T30` · GAP / SageMath | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T31"></a>`T31` · ACL2 / TPTP-SZS | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T32"></a>`T32` · FLINT / Arb | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T33"></a>`T33` · OSCAR.jl | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T34"></a>`T34` · Dedukti | `source_locked` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T35"></a>`T35` · Agda | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T36"></a>`T36` · LFSC | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T37"></a>`T37` · PVS | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T38"></a>`T38` · Nuprl / MetaPRL | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T39"></a>`T39` · Maude | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T40"></a>`T40` · OpenMath | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |
| <a id="T41"></a>`T41` · SMT-LIB / SMT-LIB-db | `surveyed` / route=`none`；仅作公开调研分类；没有安装、运行或独立验证器准入声明。 |

## 可复核入口

- 能力分类：`governance/control-plane/math-tool-maturity.v1.json`。
- 结构校验：`scripts/validate_math_tool_maturity.py`。
- 可移植测试：`scripts/test_validate_math_tool_maturity.py`、`scripts/test_check_math_tools.py`。
- 受限 canary：`scripts/run_math_tool_canaries.py`；只在显式配置的运行时中执行，所有子进程有 timeout，输出不进入研究记录。
- 证据上限：有限数值/符号输出只能支持对应切片；`kernel_check` 仍不替代自然语言陈述忠实性审查。
