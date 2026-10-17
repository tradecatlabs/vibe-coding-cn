# Review: 数学问题求解方法论深挖

## Scope

- `target`: merge_gate
- `review_depth`: deep
- `subject`: 用户点名的 55 个数学问题求解方法、35 个新增 source、1 个 derived Method，以及 inventory、catalog、taxonomy、研究和治理同步
- `base`: `edc38e2`（本轮开始时的 clean HEAD）
- `review mode`: 主 Codex 本地自审；只证明静态内容与确定性门禁，不冒充外部独立 reviewer provenance

## Verdict

- `decision`: PASS（本地范围审查）
- `summary`: 55 项均已逐项映射；20 项复用既有语义，35 项作为独立缺口进入 mathematics pack。新增内容具备前置条件、最小步骤、停止条件、证据和失败模式，并保持 `experimental`、`reference_only`、`harness_policy` 与 `verifier` 边界。外部独立 reviewer receipt 尚未提供，因此任务继续保持 `In Progress`。

## Findings

- 已处理：以现有 432 条基线做去重，不为凑数量复制 Definition First、Reduction、Analogy、Backtracking、Constructive Witness 等既有语义。
- 已处理：数学八组过程与项目八类 `functional_class` 分开；前者描述发现/证明生命周期，后者只记录主要问题空间作用。
- 已处理：计算实验、小规模样例、类比和反例搜索的证据等级被明确限制；经验支持不冒充一般证明，未找到反例不冒充定理成立。
- 已处理：新增组合 Method 是可跳过、可切换的参考流程，不是强制十步流水线；关键证据缺失或无进展时返回 `inconclusive` 或停止。
- 已修复：任务生成器写入了错误 Anti-Goal“不得修改任务目录外路径”，已按编译后的 Task Intent 改为真实边界，避免任务文档与实现范围互相矛盾。
- 未发现：本轮没有修改公共 Schema、selector、planner、runtime、Binding、数据库、服务、UI、凭据或上游 checkout。

## Selected Audit Case Consumption

- `CASE-0003 task-closeout-status-drift`：已核对 `TODO.md`、`STATUS.md`、`ACCEPTANCE_CHECKLIST.md` 与实际证据。TP-01 至 TP-04 记为 Done；TP-05 因 clean-HEAD 证据和外部独立审查尚未齐备而保持 In Progress，未提前关闭。
- 审查路由中由“库存、runtime、逆向”等文本触发的 concurrency/security/reverse-engineering 路径，经真实 diff 核对后均为不适用：变更只有静态 JSON/Markdown 与治理记录，无支付状态、运行时、样本或主动安全操作。

## Evidence And Boundaries

- `research/MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md` 保存经典框架、八组职责、55/55 crosswalk、证据等级和未验证项。
- `operators/catalog.json`、`operators/source-inventory.json`、mathematics pack 与 taxonomy 共同定义 `411 source + 57 derived = 468` 的当前快照。
- Reference Profile 输出为 `source_coverage=411/411 derived_methods=57/57 total=468`；自测中的无效样例仍被拒绝。
- 独立的只读 crosswalk 审计输出为 `crosswalk=55 reuse=20 add=35`、`targets=55 unique=55`，并确认全部引用可解析、taxonomy 解析一致、35 个新增条目语义字段完整、组合 Method 的 10 个步骤均可解析。
- clean-HEAD 任务级验证结果位于本任务 `runtime/verification/`；owner validator 返回 `verification_ready=true`、`closeout_ready=true`，四个 required gate 均无 issue，security 为 `NOT_APPLICABLE`。
- 权威来源支持母领域方法及框架，不证明迁移后的 Agent 效果；真实选择精度、成功率、成本和冲突处理仍需 Binding 与留出评测。

## Security, Reliability And Performance

- 本轮只读取公开资料和项目静态文件；未执行或安装上游代码，未读取凭据，未部署、远端写入或执行现实实验。
- 参考库校验保持对文件、条目和引用的线性扫描，复杂度可写为 `O(F + E + R)`，当前 `F=56`、`E=468`、`R=216`；它不处于 Agent 运行热路径，暂不需要数据库、缓存、并发或性能优化。
- 运行时选择、工具权限、实际副作用和最终结果仍由具体 Harness/Binding/verifier 负责。

## Document Drift

- 已同步根 README/AGENTS、operators README/AGENTS、research AGENTS/研究报告/矩阵、HARNESS_MODEL、OPERATOR_SPEC、PSOA PRD、项目操作模型、拓扑、工具链和 operators/research/docs module context。
- `contracts/problem-solving-operator-pack.schema.json` 无需修改：本轮只增加符合既有宽松 Core 与 Reference Profile 的内容，没有新增公共必填字段。
- `research/upstreams.sources.json`、lock、同步器和被忽略 checkout 未改变。

## Required Follow-up

- 当前 closeout validator 按预期 BLOCK：TP-05 未完成、Overall 仍为 `In Progress` 且存在外部 reviewer blocker；这是正确的 fail-closed 结果。
- 由真实 external_human reviewer 提供独立 receipt 后，才能关闭任务级独立审查门禁。
- 出现真实 Harness 消费方后，以固定任务集、正负例、留出集、重复运行、成本预算和恢复验证这些算子，再决定从 `experimental` 晋升。

## Rollback

- 通过反向本地提交移除本轮新增数学条目、组合 Method、计数和文档同步；不执行 reset、checkout 或 clean，不触碰上游 checkout。
