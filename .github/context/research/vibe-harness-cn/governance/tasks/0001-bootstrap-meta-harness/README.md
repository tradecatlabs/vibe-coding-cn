# Task Overview
- Task ID: `0001`
- Slug: `bootstrap-meta-harness`
- Objective: `建立元 harness 项目的领域模型、治理边界、机器契约与最小验证入口`
- Status: `Done`

## In Scope
- Harness 与 Agent 的领域定义。
- 元 harness 控制面边界与 ADR。
- Harness manifest v1alpha1 Schema、有效样例与负例。
- 可重跑 validator、治理包和本轮审查证据。

## Out of Scope
- 具体模型调用、统一 agent runtime 和业务任务状态。
- Web UI、数据库、消息队列、在线 registry 和多 agent 调度。
- 远端、push、PR、部署或外部通信。

## Task Package Tree
```text
ROOT
├── TP-01 研究并定义 Harness 领域模型
├── TP-02 落地 manifest 契约与 validator（依赖 TP-01）
├── TP-03 建立项目治理与架构记忆（依赖 TP-01）
└── TP-04 执行验证与风险审查（依赖 TP-02、TP-03）
```

## Requirement Alignment
- 用户的“agent = llm + harness”由 TP-01 形成可检验工程定义。
- “负责治理所有 harness”由 TP-01/TP-03 定义控制面而非统一 runtime。
- “开始搭建项目”由 TP-02 提供首个可运行 proof point。
- “开始调研汇报”由 `docs/HARNESS_MODEL.md` 和最终汇报完成。
- 本地 Git revision 只用于 owner-controlled input digest 与 RED/GREEN 证据，不代表远端交付。

## Task Package Overview
| Node | Objective | Depends On | Deliverables |
|---|---|---|---|
| TP-01 | 定义 Harness 领域模型与终态 | - | `docs/HARNESS_MODEL.md`、根 README/AGENTS |
| TP-02 | 建立可机检声明契约 | TP-01 | Schema、正反例、validator |
| TP-03 | 建立项目工程记忆与边界 | TP-01 | operating model、架构原则、ADR、QA、module context |
| TP-04 | 证明门禁有效并审查风险 | TP-02, TP-03 | self-test、governance validation、review evidence |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
8. REVIEW.md
9. DEBUG.md / REGRESSION_EVIDENCE.json
10. VERIFICATION_PLAN.json / runtime/verification
11. REUSE_SAMPLING.json / REUSE_ASSET_HANDOFF.json / exemplar/
