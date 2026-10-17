# Review: 将问题求解算子库纳入 Harness

## Scope

- `target`: merge_gate
- `review_depth`: deep
- `selected_profiles`: agent-harness、architecture、build-release、correctness、operability、performance、ponytail-complexity、reliability、repo-hygiene、security
- `specialized_routes`: agent-harness-runtime、knowledge-assets-zone；reverse-engineering 经内容检查为关键词误路由，本任务不含二进制、样本、协议逆向或动态分析，因此标记 N/A
- `selected_audit_cases`: 无
- `base`: `5b8a191`
- `review mode`: 主 Codex 自审；只证明本地确定性门禁，不冒充外部独立 reviewer provenance

## Verdict

- `decision`: PASS
- `summary`: 算子库已被一致定位为 Harness 内部能力；共享规范治理、本地库存与 Binding、业务执行和验证职责边界清楚。未发现剩余 BLOCK/WARN。

## Findings

- 已修复：首次 principle scan 发现 PRD 与 ADR 缺少显式 Future-Optimal 证据字段；已补齐 Target end state、Real constraints、Inertia constraints、Kill list、Migration slice 和 Rejected short-term patches，复扫通过。
- 未发现剩余 BLOCK/WARN。

## Correctness And Architecture

- `Agent = LLM + Harness`；`Operator Library ⊂ Harness`，没有第二个中央业务执行 runtime。
- 元 Harness 只治理共享 Spec/Catalog、分发、conformance、evaluation 和 lifecycle；具体 Harness 拥有本地 Library、Binding、选择、权限、执行与业务状态。
- `MentalModelSpec`、`OperatorSpec`、`MethodSpec` 分别表达“怎么看”“做一次什么”“按什么顺序做”，纯概念不伪装成可执行动作。
- 共享 `OperatorSpec` 与 Harness-specific `OperatorBinding` 分离；Binding 可改变执行载体，不能改写前置条件、效果、证据和失败语义。
- Verifier 保持逻辑独立；Operator 不能授予权限，执行者不能凭自然语言自证成功。

## Scope And Simplicity

- 复用现有 PRD、ADR、领域模型和治理上下文，没有新增平行规格。
- 未修改 `contracts/`、`scripts/`、`tests/`，未引入 Schema、运行时、服务、数据库、UI 或依赖。
- 新增对象仅为 0007 任务证据；其存在由项目治理和用户纠正的可追踪要求证明。

## Security And Reliability

- 权限仍由具体 Harness policy fail closed 地裁决；算子只声明所需 capability 和风险。
- 一次运行绑定本地不可变库存快照、Spec 与 Binding 版本；远端目录变化不能静默改变运行中任务。
- Observation、Evidence、Outcome 和三类状态继续分离；失败、预算、重试、补偿、取消和 provenance 约束未弱化。
- 本轮不执行上游代码、不读取凭据、不产生运行时或外部系统副作用。

## Performance Audit

- `Complexity`: 本地 metadata 过滤目标近似 `O(n)`，`n` 为候选 Operator 数；不得默认把完整算子库送入模型上下文。
- `Hot path`: 本地候选预筛选、Binding materialization、模型/tool 调用与 Evidence/Provenance 写入；本轮仅改文档，没有运行时 hot path。
- `Immediate`: 实现阶段记录候选数量、上下文 token、模型/API/tool 调用数、p50/p95 时延、费用和证据体积。
- `Measure first`: 真实 10x/100x 规模退化出现前，不引入缓存、向量数据库、分布式队列或无界并发。

## Document Drift

- 已同步根 README/AGENTS、docs/AGENTS、HARNESS_MODEL、PRD、ADR-0003、ADR index、架构标准、PROJECT_OPERATING_MODEL、PROJECT-TOPOLOGY、docs module context、任务索引和 lessons。
- `contracts/`、`scripts/`、`tests/`、TOOLCHAIN_MODEL 和 DDD process 未更新：本轮没有字段级契约、命令、依赖、测试行为或开发流程变化。
- 已完成 audit-case 与 reuse sampling；不创建重复案例、Completion Exemplar 或 SOP。

## Unknowns And Evidence Boundary

- Schema、代表性 corpus、selector、Binding、Verifier 和双 Harness 互操作 proof 尚未实现，继续作为后续任务。
- 当前 PASS 只能证明需求与架构边界自洽，不证明算子库运行时、跨 Harness 互操作或生产就绪。
- 项目没有远端、CI、PR 或外部 reviewer provenance；本地自审不能替代独立审查。

## Verification Evidence

- `validate_governance_package.py --strict`: PASS，0 issues。
- `governance_health_report.py --strict`: PASS，127 Markdown、0 placeholder、0 stale。
- `scan_principle_gates.py --git-mode working --strict`: PASS，0 findings。
- `validate_task_docs.py --phase decompose`: PASS。
- `validate_tasks_tree.py --phase auto`: PASS，7/7 tasks valid。
- `validate_audit_case_sampling.py --strict`: PASS。
- `validate_reuse_sampling.py --strict`: PASS。
- `verify_project.py --gate architecture|behavior|contract|test`: 全部 PASS。
- 结构检查：FR=26、NFR=11、AC=8；目标术语齐全；`contracts/`、`scripts/`、`tests/` 无变更；`git diff --check` clean。

## Post-Commit Verification

- 已在 clean HEAD 上重新生成 repository input digest 与四个 required capability 结果；
  `validate_task_verification.py --strict` 返回 PASS。
- 无 remote，仅创建本地 commit；不声称已 push、PR、CI 或生产就绪。
