# Planning Summary
先把模糊的“治理所有 harness”收敛为供应商中立控制面，再以 manifest + validator 证明统一
治理的最小可能切片；项目当前没有既有 runtime 或公共契约，因此无需兼容壳或迁移双轨。

- Target end state / 目标终态：六项正交控制面能力，具体 runtime 继续拥有业务状态。
- Real constraints / 真实约束：权限 fail closed、证据绑定 revision、控制面/数据面分离。
- Inertia constraints / 惯性约束：空仓库没有旧 API、存量数据或外部承诺。
- Kill list：统一 runtime、首版 DB/UI/队列、多 agent 调度和无第二实现的插件系统。
- Proof point：有效 manifest 通过，结构/策略负例被拒绝。
- Falsifier：第二类 harness 只能靠自由文本特例表达关键边界。
- Migration slice：领域模型 -> v1alpha1 契约 -> validator -> 首个真实 harness。

# Lifecycle Gates
`SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP` 全部必须有真实证据，禁止跳过任何 gate。
- SPEC：Task Intent、领域定义、目标终态与边界。
- PLAN：四个语义叶子、依赖、验证和回滚。
- BUILD：文档、契约、validator、治理资产。
- TEST：正反例、JSON/Python、治理与任务文档校验。
- REVIEW：agent harness、contract/security、Ponytail、future-optimal、document drift。
- SHIP：仅本地文件交付；不声称发布、部署或生产就绪。

# Simplest Path
使用 JSON Schema 表达结构、jsonschema 执行成熟校验、薄 Python 处理少量跨字段规则；不建
服务和存储。它是当前唯一同时满足可机检、可扩展、可回滚和低所有权成本的路径。

# Split Strategy
- TP-01 先稳定概念，避免从框架 API 反推领域。
- TP-02 与 TP-03 都依赖 TP-01，可分别落契约和治理真相。
- TP-04 等待两者完成后统一验证，防止文档/契约漂移。

# Execution Waves
- Wave 1：TP-01。
- Wave 2：TP-02、TP-03（语义上可并行；本次按单 agent 串行执行）。
- Wave 3：TP-04。

# Runtime Workflow Contract
- Graph mode：语义任务树；不创建原子执行图，原因是每个叶子输入完整、无共享生产副作用。
- 允许工具：本地文件读写、非交互 shell、官方资料检索。
- 禁止动作：子代理、发布、push、部署、凭据搜寻与生产写入。
- 输出：项目文件和结构化验证结果；失败非零退出并保留首个可操作错误。

# Next Executable Leaves
- TP-04：执行最终新鲜验证、审查和任务状态收口。

# Dependency Graph
```text
TP-01 -> TP-02 -> TP-04
   \----> TP-03 ----^
```

# Rollback Protocol
- 该目录初始不是 Git 仓库，不能虚构 Git rollback。
- 删除新增项目文件可回到空目录；治理/契约单文件修改可按变更清单人工恢复。
- 未来已有使用方后，Schema 只能通过版本升级与旧版保留窗口回滚。
- 不影响任何外部系统，因为本轮没有部署、push 或网络写入。
