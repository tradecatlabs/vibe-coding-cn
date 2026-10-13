# 数学工具目录

本目录描述公开项目可以如何使用数学工具；它不是某台机器的安装报告。“可用”只表示相应 bounded route 通过公开契约，不能表示能解决开放问题。

工具族按 `surveyed → source_locked → installed → smoke_checked → evidence_capable → verifier_admitted` 管理。41 个工具族的保守状态见 `governance/control-plane/math-tool-maturity.v1.json`；未达到所需状态的工具不得被 Router 当作运行能力。

## 工具族与证据上限

| 工具族 | 解释与说明 |
|:---|:---|
| SymPy | 精确代数、微积分、方程和矩阵；入口为项目 Python。证据上限是指定输入切片的 `symbolic_check`，不是一般证明。 |
| mpmath | 任意精度积分、根和常数核对；使用显式工作精度和 timeout。证据上限是 `numeric_check`。 |
| NumPy 与 SciPy | 数值线性代数、稀疏求解、积分和优化；记录残差、精度、输入规模和停止条件。证据上限是有限数值检查。 |
| python-flint、Arb 与 gmpy2 | 整数、多项式、球算术和可靠误差界；只有对应 runtime probe 通过才可运行。不能由包名推断安装。 |
| SageMath | 数论、椭圆曲线、组合和代数几何桥接；通过受限 `sage -c` 入口并设置 timeout。证据上限是计算或符号切片。 |
| PARI/GP | 整数分解、代数数论和椭圆曲线；通过 `gp -fq` 的有界输入。证据上限是编码对象的计算证据。 |
| GAP | 有限群、表示和组合结构；通过 `gap -q` 的有限对象 smoke test。证据上限是有限对象计算证据。 |
| Singular 与 Macaulay2 | Gröbner 基、理想、模和代数簇；只运行固定输入文件，设置输出预算和 timeout。证据上限是符号证据。 |
| polymake、4ti2 与 TOPCOM | 多面体、整数代数、点配置和三角剖分；只接受固定版本和有界枚举，不能把未穷尽搜索当作定理。 |
| NetworkX 与 igraph | 图构造、算法原型和性质扫描；记录图规模、算法和覆盖范围。证据上限是有限计算证据。 |
| nauty 与 Traces | 同构消重、规范标号和图枚举；枚举必须有规模上限、timeout 和停止回执。 |
| Z3、cvc5 与 SMT-LIB | 有界逻辑公式和模型/反例搜索；必须记录编码、solver 版本、timeout 和结果。solver 判定的是编码公式，不自动判定原题。 |
| PySAT、MiniSat 与 CaDiCaL | CNF 组合搜索和受限 SAT 协议；输入、退出码、输出上限和 proof/反例解释必须分开记录。 |
| FEniCSx、PETSc、SLEPc、MPI 与 UFL | PDE/FEM、稀疏线性系统、谱计算和有界并行；只提供 `numeric_check` 或运行能力，不能证明 Navier–Stokes 全局正则性。 |
| Lean、Lake 与 Mathlib | 固定 fixture 的定义、引理和 kernel check；使用 `lake env lean`。kernel check 仍需 axiom/escape 和 statement-faithfulness 审计。 |
| OEIS、LMFDB、DLMF 与 TPTP | 公开资料和索引的 discovery/reference 入口；来源、版本和归属必须记录，不把网页标签当作数学结果。 |
| Gappa 与区间算术 | 有界浮点/区间证书；必须固定舍入、输入范围和验证器，不替代完整数学证明。 |
| Alethe、Carcara、SMTCoq、Dedukti、LFSC 与 OpenMath | proof exchange 或证书生态的调研/source-lock 入口；没有公开 runtime 证据时保持 `source_locked` 或 `surveyed`。 |
| 其他 proof assistant | Mizar、HOL、Isabelle、Rocq、Metamath、ACL2、Agda、PVS、Nuprl 和 MetaPRL 目前只作调研分类；不声明已安装或 verifier-admitted。 |
| 商业 CAS | Mathematica、Maple、Magma 等需要用户单独授权；公开仓不伪装为可重建依赖，也不把商业输出直接晋升 Result。 |

## 运行约束

```bash
python3 scripts/check_math_tools.py --profile portable --strict
python3 scripts/validate_math_tool_maturity.py
```

所有 solver、CAS、外部命令和批量计算都必须有 timeout、资源预算、停止条件、输出上限和终止回执。GPU 或并行粗筛只能产生有限候选；精确裁决必须回到已审查的 CPU 或形式化路径。工具成功、固定 commit、有限枚举和模型自评不能单独改变 `Result.outcome`。
