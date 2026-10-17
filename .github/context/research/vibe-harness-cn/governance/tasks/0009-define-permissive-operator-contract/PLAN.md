# Planning Summary
先确定宽松核心与加严 Profile 的规范边界，再改 Schema/校验器和回归，最后同步长期项目真相并验证。
- 编译节点总数: 4
- 叶子执行项: 4
- 执行波次数: 4
- 当前任务必须遵守 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP`

# Lifecycle Gates
- SPEC：明确 Core MUST、Profile MAY/MUST 和扩展规则
- PLAN：固定最小变更面、兼容性和验证场景，所有 gate 不得跳过
- BUILD：调整 Schema、catalog 与薄 CLI
- TEST：Core 宽松正例和格式/安全负例、Reference exact-set 全部通过
- REVIEW：检查过严、过松、兼容性、复杂度和文档漂移
- SHIP：只在当前输入和 clean HEAD 上生成交付证据

# Simplest Path
保留现有 JSON Schema 与统一 CLI，只放宽公共 Schema并给现有 catalog 显式标注 Reference Profile，不新增服务或框架。

# Split Strategy
四个串行步骤；规范边界先于 Schema，Schema 先于测试，真实行为先于文档收口。

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
- 全局预算: 只实现静态规范、Schema、CLI 和回归，不扩展到运行时
- 全局停止条件: Schema 放宽需要破坏既有条目才能实现
- 全局停止条件: required gate 失败且没有新的修复证据
- 全局停止条件: 需要凭据、部署、远端写入或破坏性操作
- 需要审批: 外部发送
- 需要审批: 删除或破坏性操作
- 需要审批: 部署、发布、权限、凭据或远端状态变更

# Next Executable Leaves
- TP-01 | Wave 1 | Depends On: 无 | Gate: 任何字段强制项都能由互操作或安全必要性解释

# Dependency Graph
TP-01 -> TP-02
TP-02 -> TP-03
TP-03 -> TP-04

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
