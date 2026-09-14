# 数学工具生态与公开能力边界

> 本文是公开仓的可移植说明，不是当前主机、容器或研究 worker 的运行报告。
> 方法层分类不按教程目录展开，统一以 [`governance/standards/FORMAL-METHODS-MAP.md`](../../standards/FORMAL-METHODS-MAP.md) 的 Formal Methods 六分法和 Lean 六层栈为上位地图。

## 观察框架

工具族按以下状态机管理：`surveyed → source_locked → installed → smoke_checked → evidence_capable → verifier_admitted`。
状态是证据能力边界，不是“工具数量”或“安装清单”。固定 commit、下载源码、模型自评和一次成功命令都不能自动提升状态。

公开仓维护 41 个工具族的机器注册表，并将每个条目锚定到 `governance/tools/MATH_TOOL_CATALOG.md#T01` 至 `#T41`。
这取代了对未发布内部盘点文件的依赖；缺少公开证据的条目明确保持为调研分类。

## 当前公开准入

- **SymPy**：只准入固定的符号/精确算术 vertical slice，证据能力上限是有限 `symbolic_check` 或相应运行回执。
- **Lean 4/Mathlib**：只准入固定 fixture 的 kernel 检查，同时保留 axiom、逃逸和 statement-faithfulness 审计。
- **SAT/SMT、数值库、图论库和其他 CAS**：目录、可选依赖和 canary 契约可以公开；没有公开且可复核的运行证据时，不进入 evidence/verifier route。

## 运行规则

1. 研究前先固定 ProblemContract 的 `allowed_adapters`、方法和 runtime 预算。
2. 每个外部命令/solver/CAS 都必须有 timeout、输出上限、停止条件和失败语义。
3. GPU 或并行粗筛的结果只能作为有限候选；精确裁决必须走已审查的 CPU/形式化路径。
4. canary 只验证运行时协议（正例、反例、错误、timeout），不创建 Problem、Attempt、Result 或 Solution。
5. 工具来源通过 `vendor/sources.lock.json` 固定；reference-only 缓存不等于安装、激活或验证器准入。

## 入口

- 机器注册表：`governance/control-plane/math-tool-maturity.v1.json`
- schema：`governance/control-plane/math-tool-maturity.schema.json`
- 目录：`governance/tools/MATH_TOOL_CATALOG.md`
- 探针：`scripts/check_math_tools.py --profile <profile> --strict`
- canary：先设置 `MATH_CANARY_SOURCE_SHA256` 为 runner 的 sha256，再运行 `scripts/run_math_tool_canaries.py --tools T13,T15,T16 --json --strict`

任何新增工具都必须同时补充 owner、来源、可复核测试、证据上限和失败语义；否则保持 `surveyed`。
