# Review: AI 问题求解算子架构需求基线

## Scope

- `target`: merge_gate
- `review_depth`: deep
- `selected_profiles`: agent-harness、architecture、build-release、correctness、operability、performance、
  ponytail-complexity、reliability、repo-hygiene、security
- `specialized_routes`: agent-harness-runtime、knowledge-assets-zone；reverse-engineering 经内容检查为
  关键词误路由，本任务不含二进制、样本、协议逆向或动态分析，因此标记 N/A
- `files`: PSOA PRD、ADR-0003、docs module context、HARNESS_MODEL、根 README/AGENTS、项目操作模型、
  拓扑、上下文地图与 0006 任务证据
- `base`: `056f5ce`（项目重命名后的已提交基线）
- `review mode`: 主 Codex 自审；只证明本地确定性门禁，不冒充外部独立 reviewer provenance

## Verdict

- `decision`: PASS
- `summary`: PRD 已把 PSOA 定义为任务意图与 Harness 执行之间的供应商中立语义层，明确
  Operator Library、Planner、Harness、Verifier 与 Provenance 的所有权；需求可验收且未把
  Schema、planner、registry、executor 或 adapter 写成已实现能力。未发现剩余 BLOCK/WARN。

## Findings

- 无。

## Correctness And Architecture

- `world_state`、`knowledge_state`、`governance_state` 独立表达，避免把认知结果自动提升为现实事实。
- Observation、Evidence 与 Outcome 分层；执行成功不能替代 Verifier 裁决。
- Operator 只能声明 capability、风险和建议审批点，实际权限仍由 Harness policy 决定。
- Operator/Method 的未来机器契约独立于现有 Harness manifest；本轮未修改 `contracts/`。
- 核心 proof point 和 falsifier 均能由后续双 adapter prototype 直接检验。

## Scope And Simplicity

- 本轮只新增一个 PRD、一个 ADR、一个缺失的 docs module context 和必要导航/任务证据。
- 未引入代码、依赖、服务、数据库、UI、registry、缓存、队列或通用 planning runtime。
- 候选路径中已拒绝提示词库和完整平台；选择“语义规范 + 最小 conformance + 双 adapter proof”。
- 当前无需 `ponytail:` 技术债标注；MVP 天花板和升级触发已在 PRD 第 13 节明确记录。

## Security And Reliability

- 外部 Operator 定义按不可信输入处理；敏感值只能使用受控引用，不能内联进定义、Plan 或 provenance。
- 不支持 capability、前置条件缺失、证据陈旧和越权请求均要求 fail closed。
- 重试、补偿、预算耗尽、取消、部分失败和不可逆副作用均要求显式语义。
- 本轮没有执行上游、访问凭据、改变运行时、修改 manifest 或产生外部服务副作用。

## Performance Audit

- `Complexity`: 首版 metadata 过滤目标近似 `O(n)`，`n` 为候选 Operator 数；完整算子库不得默认进入
  模型上下文。
- `Hot path`: 候选预筛选、模型选择、Evidence/Provenance 写入；当前只有需求文档，无运行时 hot path。
- `Immediate`: 记录候选数量、token、模型/API/tool 调用数、时延、费用和证据体积。
- `Measure first`: 在真实 10x/100x 算子规模退化数据出现前，不引入缓存、向量数据库、分布式队列
  或无界并发。

## Document Drift

- 根 README/AGENTS、docs/AGENTS、HARNESS_MODEL、ADR-0003、docs module context、
  PROJECT_OPERATING_MODEL、PROJECT-TOPOLOGY、CONTEXT-MAP 与任务索引均已同步。
- TOOLCHAIN_MODEL、DDD process、现有 contract 与 Gate 未更新：本轮没有改变命令、依赖、流程、字段级
  契约或可机械阻断的新失败类别。
- `docs/PROBLEM_SOLVING_OPERATOR_ARCHITECTURE_PRD.md` 是需求真相源；字段级机器约束仍归未来
  `contracts/` 任务所有。

## Audit Case Consumption

- `route_review_scope.py` 未命中既有 audit case；本轮未修复 bug、审查 BLOCK/WARN、CI/测试漂移或
  可复发缺陷，因此不创建 `AUDIT_CASE_SAMPLING.md`。

## Unknowns And Evidence Boundary

- predicate/effect 表达、Method 图结构、Verifier 实现、PROV profile 和 registry ID 尚未由原型验证，
  已作为 PRD open questions 保留。
- PRD 的 `Draft v0.1` 只证明需求基线可供下游设计使用，不证明实现、互操作或生产就绪。
- 当前没有远端、CI、PR 或外部 reviewer provenance；PASS 仅表示本地自审和确定性门禁通过。

## Verification Evidence

- `validate_governance_package.py --strict`: PASS，0 issues。
- `governance_health_report.py --strict`: PASS，117 Markdown、0 placeholder、0 stale。
- `validate_task_docs.py --phase decompose`: PASS。
- `validate_tasks_tree.py --phase auto`: PASS，6/6 tasks valid。
- `scan_principle_gates.py --git-mode working --strict`: PASS，0 findings。
- `verify_project.py --gate architecture|behavior|contract|test`: 全部 PASS。
- PRD 结构检查：FR=23、NFR=10、AC=7；`contracts/` 无变更；placeholder=0；`git diff --check` clean。

## Required Post-Commit Verification

- 在最终 clean HEAD 上重新生成 repository input digest 和四个 required capability 的任务级结果，
  再由 `validate_task_verification.py --strict` 校验新鲜度。
- 无 remote，仅创建本地 commit；不声称已 push、PR、CI 或生产就绪。
