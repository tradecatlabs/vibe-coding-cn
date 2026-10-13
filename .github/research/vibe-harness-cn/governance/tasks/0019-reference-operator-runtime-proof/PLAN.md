# Planning Summary
先冻结共享运行时信封与 Harness 本地职责，再做单文件参考 Harness，随后用反例和摘要重算证明 fail-closed，最后同步文档治理并运行项目门禁。
- 编译节点总数: 5
- 叶子执行项: 5
- 执行波次数: 5
- 当前任务必须遵守 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP`

# Lifecycle Gates
- SPEC：固定共享信封、本地 Binding、verdict 语义和隐私边界
- PLAN：确认无中央运行时、无外部副作用、O(n) 选择预算
- BUILD：实现最小可运行路径并保持静态库不变
- TEST：正例与 fail-closed 反例均可自动重跑
- REVIEW：检查职责越界、权限扩大、自证成功和敏感信息泄漏
- SHIP：绑定 clean HEAD、新鲜门禁结果与独立审查状态
- 上述 gate 必须按顺序完成，不得跳过 gate 或用自报结果替代证据

# Simplest Path
复用 Python 标准库、现有 jsonschema 锁和静态目录；只新增一个可执行参考模块、一个本地 binding、三个运行时样例和必要测试。

# Split Strategy
按契约、参考执行、反例验证、文档治理、收口五段串行推进。

# Execution Waves
- Wave 1: TP-01
- Wave 2: TP-02
- Wave 3: TP-03
- Wave 4: TP-04
- Wave 5: TP-05

# Runtime Workflow Contract
- workflow artifact 必须存入任务目录，而不是只留在聊天上下文。
- worker 只能消费当前 packet 的最小上下文、允许工具、禁止动作、证据要求和停止条件。
- verifier / 自审必须独立挑战关键发现，不能把 worker 自评当作验收。
- integrator / closeout 必须报告 verified、rejected、unresolved、failed、not-covered。
- 全局预算: 一个 reference Harness 模块，不新增长期服务或基础设施
- 全局预算: Selector 单次 O(n) 扫描；Method 展开受 max_steps 限制
- 全局预算: 只写本地 JSON/Markdown/Python 与忽略的验证证据
- 全局停止条件: 需求需要真实模型、工具、远端服务或生产凭据
- 全局停止条件: 实现开始演化成通用 Planner、中央 runtime 或插件框架
- 全局停止条件: 现有目录内容无法提供确定性选择或展开所需的稳定字段
- 全局停止条件: Schema 必须收紧内容语义才可表达第一版闭环
- 需要审批: 真实模型或工具执行、远端写入、生产 Harness 集成
- 需要审批: 新增服务、数据库、长期运行进程或破坏性操作

# Next Executable Leaves
- TP-01 | Wave 1 | Depends On: 无 | Gate: 任务目标与上下文已确认

# Dependency Graph
TP-01 -> TP-02
TP-02 -> TP-03
TP-03 -> TP-04
TP-04 -> TP-05

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
