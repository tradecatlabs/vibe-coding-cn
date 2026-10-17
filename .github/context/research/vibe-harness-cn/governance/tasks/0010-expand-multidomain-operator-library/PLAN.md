# Planning Summary
先以一手资料建立跨学科证据矩阵，再筛出最小高价值算子，写入现有 Reference Profile，最后同步治理并以全量门禁收口。
- 编译节点总数: 4
- 叶子执行项: 4
- 执行波次数: 4
- 当前任务必须遵守 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP`

# Lifecycle Gates
- 所有 lifecycle gates 均为 required，不得跳过；失败必须 fail-closed
- SPEC：明确来源、学科边界、算子提炼规则和实验性声明
- PLAN：固定新增 domain、条目集合、变更边界和证据要求
- BUILD：更新 inventory、packs、catalog 和报告
- TEST：运行 Core/Profile、自测、项目 gates 与结构检查
- REVIEW：检查重复、过度简化、权限误读、引用漂移、文档漂移和复杂度
- SHIP：只在 clean HEAD 与新鲜验证证据上形成交付

# Simplest Path
复用现有 JSON Schema、Reference Profile validator、inventory/catalog/packs 和治理命令，只新增内容与必要文档，不增加运行时服务或依赖。

# Split Strategy
四个串行阶段：研究证据→算子定义→入库与文档→验证与交付；先完成证据和命名，再批量写 JSON。

# Execution Waves
- Wave 1: TP-01
- Wave 2: TP-02
- Wave 3: TP-03
- Wave 4: TP-04

# Runtime Workflow Contract
- workflow artifact 必须存入任务目录，而不是只留在聊天上下文。
- worker 只能消费当前 packet 的最小上下文、允许工具、禁止动作、证据要求和停止条件。
- verifier / 自审必须独立挑战关键发现，不能把 worker 自评当作验收。
- integrator / closeout 必须报告 verified、rejected、unresolved、failed、not-covered。
- 全局预算: 只新增静态研究内容、契约引用和治理文档，不运行上游代码/实验/模型训练
- 全局停止条件: 无法找到足以支撑核心算子语义的权威来源
- 全局停止条件: 新增内容需要修改公共 Core 才能表达
- 全局停止条件: required gate 失败且没有新的修复证据
- 全局停止条件: 需要凭据、部署、远端写入或破坏性操作
- 需要审批: 真实物理/化学实验、模型训练或外部副作用
- 需要审批: 部署、发布、权限、凭据、删除和远端状态变更

# Next Executable Leaves
- TP-01 | Wave 1 | Depends On: 无 | Gate: 每个核心候选都有可追溯权威来源，事实、推断和未知分开

# Dependency Graph
TP-01 -> TP-02
TP-02 -> TP-03
TP-03 -> TP-04

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
