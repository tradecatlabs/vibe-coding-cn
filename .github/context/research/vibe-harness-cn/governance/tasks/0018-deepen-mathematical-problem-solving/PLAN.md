# Planning Summary
先完成权威来源核验和 55 项语义去重，再将 35 个缺口写入现有数学 pack，最后同步文档治理并完成确定性验证。
- 编译节点总数: 5
- 叶子执行项: 5
- 执行波次数: 5
- 当前任务必须遵守 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP`

# Lifecycle Gates
- 所有 required gate 必须按顺序执行，不得跳过 gate；独立审查缺失时保持 In Progress。
- SPEC：固定 55 项清单、20 reuse/35 add 和 reference-only 边界
- PLAN：固定权威来源、去重规则、停止条件和回滚
- BUILD：只新增可区分且有证据的静态 JSON/Markdown
- TEST：运行 Core/Profile、自测、项目和治理验证
- REVIEW：检查遗漏、重复、分类、证据等级和文档漂移
- SHIP：绑定 clean HEAD、新鲜证据和独立审查状态

# Simplest Path
复用现有 pack、inventory、catalog、taxonomy、研究矩阵和验证脚本；不新增领域、不改 Schema、不实现运行时。

# Split Strategy
按证据核验、逐项 crosswalk、内容入库、文档治理、验证收口五段串行推进。

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
- 全局预算: 优先复用五套经典/官方资料与既有 reference framework
- 全局预算: 35 个新增 source + 1 个 derived Method
- 全局预算: 只做公开资料、静态 JSON/Markdown 和确定性校验
- 全局停止条件: 55 项已全部映射且新增候选不再具有独立语义
- 全局停止条件: 候选只能靠收紧公共 Core 或实现 runtime 才能表达
- 全局停止条件: 权威来源不足或无法定义证据与失败边界
- 全局停止条件: 需要凭据、部署、外部写入、现实操作授权或破坏性操作
- 需要审批: 改变公共 Core Schema、运行时权限或外部服务
- 需要审批: 凭据、远端写入、删除或现实专业操作

# Next Executable Leaves
- TP-05 | Wave 5 | Depends On: TP-04 | Gate: clean-HEAD 任务级验证已通过；外部独立 reviewer receipt 仍待提供

# Dependency Graph
TP-01 -> TP-02
TP-02 -> TP-03
TP-03 -> TP-04
TP-04 -> TP-05

# Rollback Protocol
- 使用反向本地提交撤销本轮 mathematics pack、inventory、catalog、taxonomy、研究、文档和治理同步
- 不使用 reset、checkout、clean 或覆盖写整理工作树
- 不触碰其他任务目录、上游 registry、lock、同步器或 checkout
