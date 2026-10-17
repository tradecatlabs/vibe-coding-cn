# Planning Summary
先抓取六个领域的一手/权威来源，再做缺口审计、静态入库、文档治理和全量验证；不扩展运行时。
- 编译节点总数: 11
- 叶子执行项: 10
- 执行波次数: 5
- 当前任务必须遵守 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP`

# Lifecycle Gates
所有 gate 按顺序执行，不得跳过任何 gate。
- SPEC：固定六个领域、八类功能与 reference-only 边界
- PLAN：固定来源优先级、重复审计、停止条件和回滚
- BUILD：只写有来源支持的 JSON/Markdown
- TEST：运行 Core/Profile、自测、项目和治理验证
- REVIEW：检查重复、分类、专业误读、权限边界和文档漂移
- SHIP：绑定 clean HEAD、新鲜证据和未验证项

# Simplest Path
复用现有 research matrix、inventory/catalog/pack、taxonomy、治理模板和验证脚本，只新增独立语义。

# Split Strategy
六个领域证据并列准备，随后串行完成缺口审计、算子定义、目录同步和验证收口。

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
- 全局预算: 每个领域使用 2–4 个一手/官方来源，必要时补交叉来源
- 全局预算: 每个领域目标为 5 个 source + 1 个 derived Method
- 全局预算: 只做公开资料、静态 JSON/Markdown 和确定性校验
- 全局停止条件: 找不到支撑问题求解语义的权威来源
- 全局停止条件: 只能修改公共 Core 才能表达
- 全局停止条件: 候选与既有条目重复或无法写证据/失败契约
- 全局停止条件: 需要凭据、部署、现实操作授权、远端写入或破坏性操作
- 需要审批: 现实科学实验、材料/化学操作、仪器校准和高影响专业决策
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
