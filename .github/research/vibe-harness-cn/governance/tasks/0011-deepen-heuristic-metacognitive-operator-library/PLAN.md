# Planning Summary
先分别抓取八类功能的上位理论与各母领域的操作程序，再去重提炼算子和交叉索引，最后用现有 Profile/治理门禁收口。
- 编译节点总数: 12
- 叶子执行项: 11
- 执行波次数: 4
- 当前任务必须遵守 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP`

# Lifecycle Gates
- SPEC：固定双轴模型、八类边界、来源层级和不把知识当授权的约束；不得跳过 gate
- PLAN：固定母领域覆盖、去重策略、变更边界和证据要求；不得跳过 gate
- BUILD：更新缺口 packs、inventory、catalog、taxonomy crosswalk、研究报告和文档
- TEST：运行 Core/Profile、自测、项目 gates、结构和引用检查
- REVIEW：检查分类漂移、重复、过度简化、权限误读、引用/计数/文档漂移和维护成本
- SHIP：只在 clean HEAD 与当前输入绑定的新鲜验证证据上形成交付；任一 required gate 失败则停止

# Simplest Path
复用现有 JSON Schema、Reference Profile validator、inventory/catalog/packs 与研究文档格式；新增缺口 pack 和独立 taxonomy crosswalk，不扩张运行时或公共 Core。

# Split Strategy
四阶段串行：八类证据抓取→母领域去重与算子定义→入库/交叉索引/文档→全量验证与收口；八类研究在第一阶段分别记录。

# Execution Waves
- Wave 1: TP-01.01, TP-01.02, TP-01.03, TP-01.04, TP-01.05, TP-01.06, TP-01.07, TP-01.08
- Wave 2: TP-02
- Wave 3: TP-03
- Wave 4: TP-04

# Runtime Workflow Contract
- workflow artifact 必须存入任务目录，而不是只留在聊天上下文。
- worker 只能消费当前 packet 的最小上下文、允许工具、禁止动作、证据要求和停止条件。
- verifier / 自审必须独立挑战关键发现，不能把 worker 自评当作验收。
- integrator / closeout 必须报告 verified、rejected、unresolved、failed、not-covered。
- 全局预算: 只做公开资料抓取、静态 JSON/Markdown 更新和确定性校验，不运行上游代码或现实实验
- 全局停止条件: 八类中某类找不到能支撑核心语义的权威来源
- 全局停止条件: 只能通过修改公共 Core 才能表达分类或条目
- 全局停止条件: required gate 失败且没有新的修复证据
- 全局停止条件: 需要凭据、部署、远端写入、实验授权或破坏性操作
- 需要审批: 真实物理/化学实验、模型训练、在线检索写入或外部副作用
- 需要审批: 部署、发布、权限、凭据、删除和远端状态变更

# Next Executable Leaves
- TP-01.01 | Wave 1 | Depends On: 无 | Gate: 父步骤范围已确认: research-evidence
- TP-01.02 | Wave 1 | Depends On: 无 | Gate: 父步骤范围已确认: research-evidence
- TP-01.03 | Wave 1 | Depends On: 无 | Gate: 父步骤范围已确认: research-evidence
- TP-01.04 | Wave 1 | Depends On: 无 | Gate: 父步骤范围已确认: research-evidence
- TP-01.05 | Wave 1 | Depends On: 无 | Gate: 父步骤范围已确认: research-evidence
- TP-01.06 | Wave 1 | Depends On: 无 | Gate: 父步骤范围已确认: research-evidence
- TP-01.07 | Wave 1 | Depends On: 无 | Gate: 父步骤范围已确认: research-evidence
- TP-01.08 | Wave 1 | Depends On: 无 | Gate: 父步骤范围已确认: research-evidence

# Dependency Graph
TP-01.01 -> TP-02
TP-01.02 -> TP-02
TP-01.03 -> TP-02
TP-01.04 -> TP-02
TP-01.05 -> TP-02
TP-01.06 -> TP-02
TP-01.07 -> TP-02
TP-01.08 -> TP-02
TP-02 -> TP-03
TP-03 -> TP-04

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
