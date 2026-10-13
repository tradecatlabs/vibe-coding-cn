# Planning Summary
先按六个母领域建立权威来源和证据缺口矩阵，再做语义去重、功能映射和 pack 入库，最后用全量库、治理与任务证据门禁收口。
- 编译节点总数: 11
- 叶子执行项: 10
- 执行波次数: 5
- 当前任务必须遵守 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP`

# Lifecycle Gates
- SPEC：固定六个领域、八类功能边界、来源优先级和 reference-only 约束；不得跳过 gate
- PLAN：固定证据矩阵、去重策略、变更边界、停止条件和回滚方式；不得跳过 gate
- BUILD：只写有来源支持的 pack、taxonomy、报告和文档切片；不得跳过 gate
- TEST：运行 Core/Profile、自测、引用/计数/结构和项目门禁；不得跳过 gate
- REVIEW：检查重复、分类漂移、专业误读、权限边界、证据缺口和文档漂移；不得跳过 gate
- SHIP：只在 clean HEAD 与新鲜任务验证证据绑定后交付；不得跳过 gate

# Simplest Path
复用现有研究报告、Reference Profile、inventory/catalog/pack、taxonomy 和验证脚本；只新增有来源且能形成独立语义的静态条目，不扩展运行时。

# Split Strategy
六个领域先分别完成证据抽取；缺口审计后串行执行去重提炼、目录同步、治理回写和验证收口。

# Execution Waves
- Wave 1: TP-01.01, TP-01.02, TP-01.03, TP-01.04, TP-01.05, TP-01.06
- Wave 2: TP-02
- Wave 3: TP-03
- Wave 4: TP-04
- Wave 5: TP-05

# Runtime Workflow Contract
- workflow artifact 必须存入任务目录，而不是只留在聊天上下文。
- worker 只能消费当前 packet 的最小上下文、允许工具、禁止动作、证据要求和停止条件。
- verifier / 自审必须独立挑战关键发现，不能把 worker 自评当作验收。
- integrator / closeout 必须报告 verified、rejected、unresolved、failed、not-covered。
- 全局预算: 每个领域优先 2–4 个一手/官方来源，必要时补 1 个独立交叉来源
- 全局预算: 每个领域形成 5 个 source 和 1 个 derived Method；证据不足则少于该数量并记录缺口
- 全局预算: 只做公开资料、静态 JSON/Markdown 和确定性校验
- 全局停止条件: 找不到支撑问题求解语义的权威来源
- 全局停止条件: 只能通过修改公共 Core 才能表达条目
- 全局停止条件: 条目与既有 source 重复或无法写出证据/失败契约
- 全局停止条件: required gate 失败且无新的修复证据
- 全局停止条件: 需要凭据、部署、现实操作授权、远端写入或破坏性操作
- 需要审批: 真实法律、伦理、教育、医疗或其他高影响决策
- 需要审批: 模型训练、部署、权限/凭据、远端写入、删除或外部副作用

# Next Executable Leaves
- TP-01.01 | Wave 1 | Depends On: 无 | Gate: 父步骤范围已确认: research-evidence
- TP-01.02 | Wave 1 | Depends On: 无 | Gate: 父步骤范围已确认: research-evidence
- TP-01.03 | Wave 1 | Depends On: 无 | Gate: 父步骤范围已确认: research-evidence
- TP-01.04 | Wave 1 | Depends On: 无 | Gate: 父步骤范围已确认: research-evidence
- TP-01.05 | Wave 1 | Depends On: 无 | Gate: 父步骤范围已确认: research-evidence
- TP-01.06 | Wave 1 | Depends On: 无 | Gate: 父步骤范围已确认: research-evidence

# Dependency Graph
TP-01.01 -> TP-02
TP-01.02 -> TP-02
TP-01.03 -> TP-02
TP-01.04 -> TP-02
TP-01.05 -> TP-02
TP-01.06 -> TP-02
TP-02 -> TP-03
TP-03 -> TP-04
TP-04 -> TP-05

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
