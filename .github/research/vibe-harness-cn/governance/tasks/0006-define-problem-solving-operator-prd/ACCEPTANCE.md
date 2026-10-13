# Task-Level Acceptance
- `docs/PROBLEM_SOLVING_OPERATOR_ARCHITECTURE_PRD.md` 包含问题、用户、目标、非目标、系统边界、
  核心对象、功能需求、非功能需求、MVP、验收、风险、待决策项和路线图。
- PRD 明确三类状态以及 Operator 与 Tool/Prompt/Skill/Workflow/Planner/Harness/Verifier 的边界。
- ADR-0003 记录独立语义层、独立契约和双 adapter proof 的长期架构取舍。
- README、两级 AGENTS、HARNESS_MODEL、PROJECT_OPERATING_MODEL、PROJECT-TOPOLOGY、CONTEXT-MAP
  和 docs module context 可以一致导航到需求真相源。
- 任务文档、governance strict/health、原则扫描和项目 required gates 全部在当前输入上通过。

# Validation Plan
- 结构检查：PRD 必需章节、FR/NFR/AC 标识、无待填占位符。
- 边界检查：Harness manifest 未改变，PSOA 只作为需求与架构文档出现。
- 文档检查：治理索引重建、strict validator、health report、docs context bundle。
- 项目门禁：执行 Verification Plan 中 required capability。
- Git 检查：只选择性 stage 本任务文件；确认无凭据和无意外运行产物。

# Review Gate
- correctness：需求、状态、outcome 和 evidence 语义不互相矛盾。
- readability：读者可从问题到边界、需求、MVP、验收顺序理解，不依赖聊天上下文。
- architecture：Operator Library、Planner、Harness、Verifier、Provenance owner 清楚且依赖单向。
- security：Operator 不授权、不自证成功；secret 和外部内容边界明确。
- performance：规定 metadata 预筛选、预算指标和 10x/100x 测量，不提前引入缓存/服务。
- document drift：所有长期真相源已更新或有具体豁免。

# Runtime Verification Gate
- Task Intent 与 Verification Plan 必须保持 `READY`。
- required capability 缺失、ERROR、非 PASS 或 stale evidence 时 fail closed。
- 本地自审和确定性门禁不得冒充外部独立 reviewer 或生产级 TEVV。

# Ship Readiness
- 选择性 stage PRD、相关导航/治理文件和 0006 任务证据。
- 提交前检查 branch、diff、未跟踪文件、secret、runtime 路径和文档链接。
- 本地 commit 后重新生成任务级新鲜验证证据；无 remote 不 push。

# Task Package Acceptance
## TP-01
- Verify：检查 PRD 第 2–20 节及 FR-001..023、NFR-001..010、AC-001..007。
- Gate：需求可供后续 prototype/Schema 任务直接消费，未把规划写成已实现能力。

## TP-02
- Verify：检查 ADR-0003、docs context、README/AGENTS、HARNESS_MODEL、操作模型和拓扑链接。
- Gate：PSOA 需求 owner 清楚；Harness manifest 与工具链行为保持不变。

## TP-03
- Verify：task docs、governance strict/health、principle scan、required project gates 和 Git diff。
- Gate：当前输入无 BLOCK；提交只包含本任务所有文件。

# Anti-Goals
- 不得把 PRD 当成实现完成证明。
- 不得为满足“完整”而实现 Schema、服务或大规模算子库。
- 不得修改现有 Harness manifest 或测试行为。
- 不得虚构外部标准兼容性、运行结果或独立评审。
