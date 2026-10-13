# Changelog

## 0.4.0

- CandidateObservation 未形成 active ProblemContract 时禁止启动研究计算。
- 工具能力按 surveyed/source_locked/installed/smoke_checked/evidence_capable/verifier_admitted 分层。
- solver、CAS、枚举和外部命令强制 wall-time、线程/内存预算与终止回执。

## 0.3.1 - 2026-08-29

- 支持为 Sage、FEniCSx、Lean/Lake 显式绑定独立运行时，非交互执行不再依赖登录 shell 的 PATH。
- FEniCSx 探针适配 DOLFINx 0.11 `create_unit_square` API，并增加 conda-forge 环境幂等部署脚本。

## 0.3.0 - 2026-08-16

- 新增按领域划分的数学工具目录、独立运行时边界和 evidence 上限。
- 要求任务启动前使用 `check_math_tools.py` 对实际行为做 fail-closed 探测。

## 0.2.0 - 2026-08-15

- 强制 GPU 可行性预检：新增计算类型路由决策表与 `scripts/compute_plan.py` 入口；GPU 只做粗筛，精确裁决回 CPU。

## 0.1.0 - 2026-08-13

- 建立 SymPy/NumPy/SciPy/mpmath/OEIS 计算证据契约和复杂度边界。
