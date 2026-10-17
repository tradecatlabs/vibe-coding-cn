# Planning Summary
目标终态是让 PSOA 成为模型与 Harness 无关的问题求解中间表示：Operator Library 拥有方法语义，
Harness 拥有权限和执行，Verifier 拥有结果裁决，Provenance owner 拥有审计链。当前迁移切片只
冻结 PRD 与架构边界，不把未经 prototype 验证的字段直接固化成机器契约。

# Lifecycle Gates
- `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP` 必须按序闭合，不得跳过 gate。
- SPEC：从用户材料和项目事实冻结 Problem Statement、目标、非目标、术语与边界。
- PLAN：比较提示词库、完整平台和独立语义层三条路径，选择可证伪的最小路径。
- BUILD：完成 PRD、ADR、module context 和入口同步。
- TEST：运行任务文档、治理、原则和项目 capability 门禁。
- REVIEW：执行 correctness、architecture、document-drift、security、performance 自审。
- SHIP：选择性本地 commit；无 remote 不 push。

# Simplest Path
- Existence check：独立 PRD 应存在；HARNESS_MODEL 无法同时承担总体领域模型和详细组件需求。
- Selected ladder rung：优先使用项目既有 Markdown、ADR、module context 和验证工具，零新依赖。
- Why lower rungs failed：只改 HARNESS_MODEL 会使需求、路线图和验收失去清晰 owner；任务聊天不能
  成为长期真相源。
- Skipped scope：Schema、parser、planner、operator corpus、adapter 和在线 registry。
- Ceiling / upgrade path：PRD 通过评审后，用 semantic prototype 决定字段，再进入 Contract v0。
- Do-not-simplify：三类状态、非确定性 outcome、权限边界、独立验证、版本绑定与 provenance。
- Minimal runnable check：治理 strict/health、任务 closeout validator、项目 architecture gate。

### 候选路径

| 路径 | 差异 | 结论 |
|---|---|---|
| A：只扩写 HARNESS_MODEL | 文件少，但组件需求与总体模型耦合 | 拒绝 |
| B：把 PRD 只放进 governance | 治理集中，但违反本项目 `docs/` 领域/目标架构 owner | 拒绝 |
| C：独立 docs PRD + ADR/context 导航 | 真相边界清楚，可供后续 contract 消费 | 选择 |

# Split Strategy
- TP-01 只拥有需求语义，避免在写 PRD 时顺手实现 Schema。
- TP-02 只负责长期项目真相同步，保证架构和导航不漂移。
- TP-03 只负责审查、验证和交付，不在门禁阶段继续扩充需求。

# Execution Waves
- Wave 1：TP-01。
- Wave 2：TP-02（依赖 TP-01）。
- Wave 3：TP-03（依赖 TP-02）。

# Runtime Workflow Contract
- 允许：读取项目文档、编辑当前范围文件、运行本地文档/治理/项目门禁、选择性 Git 交付。
- 禁止：实现运行时或 Schema、执行上游、安装依赖、访问凭据、原生子代理、push/部署、破坏性 Git。
- 预算：保持一个 PRD、一个 ADR、一个 module context；不扩张为百科或完整外部标准映射。
- 停止条件：出现会改变核心 owner/公共契约的未决选择时保留为 open question，不猜测实现。

# Next Executable Leaves
- TP-03 已进入执行：完成 review、严格校验与交付。

# Dependency Graph
```text
TP-01 -> TP-02 -> TP-03
```

# Rollback Protocol
- 使用反向提交撤销 PRD、ADR、module context、导航和任务文件，不覆盖并行改动。
- 本轮没有 Schema、运行时或持久数据变化，无需兼容层或数据迁移。
- 不使用 reset、clean、stash、强制 checkout 或未经确认的文件删除。

# Document-Driven Change Preflight
- Operating model update：`updated`；登记 PSOA 作为新语义层需求。
- Toolchain model update：`not needed`；没有新增或修改命令、依赖、构建、发布和回滚入口。
- Process update：`not needed`；文档驱动流程本身未改变。
- Source-of-truth updates：PSOA PRD、HARNESS_MODEL、ADR-0003、docs module context、项目入口与拓扑。
- Local README/AGENTS impact：`updated`；新增文档和依赖方向已登记。
- Contract/catalog/schema impact：`not needed`；本轮明确不实现字段级契约。
- ADR/Gate/module-context impact：ADR-0003 与 docs context 新增；无可机械阻断的新失败类，不新增 Gate。
- Documentation exemption reason：仅 Toolchain Model、DDD process、contracts/Gate 豁免，理由如上。
- Validation evidence：governance strict/health、principle scan、task validator、project gates。
