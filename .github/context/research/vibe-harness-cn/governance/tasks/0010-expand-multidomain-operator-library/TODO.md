# Execution Checklist
[x] TP-01 | P0 | 建立跨学科证据矩阵 | Verify: 检查研究报告、来源台账、候选清单、局限和未验证项 | Gate: 每个核心候选都有可追溯权威来源，事实、推断和未知分开 | Parallelizable: No
[x] TP-02 | P0 | 定义算子语义与领域边界 | Verify: 检查每个 entry 的类型、语义字段、治理 owner、source_refs 和状态 | Gate: 新增算子不越过 Core/Profile、安全 owner 和 reference-only 边界 | Parallelizable: No
[x] TP-03 | P0 | 入库并同步目录文档 | Verify: 运行 JSON 结构检查与 Reference Profile 校验，并核对文档中的规模与边界 | Gate: inventory/catalog/packs 精确一致，文档没有遗留 75+7 的过期事实 | Parallelizable: No
[x] TP-04 | P0 | 验证、审查与交付收口 | Verify: 运行 operator self-test、project gates、governance strict/health/principle 和任务 docs validator | Gate: 所有 required gate 绑定当前输入、策略和真实产物；失败项明确记录 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
