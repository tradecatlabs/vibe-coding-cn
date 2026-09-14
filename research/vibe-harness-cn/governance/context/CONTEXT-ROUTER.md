---
id: GOV-CONTEXT-ROUTER
type: process
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-09-04
review_cycle: P90D
---

# Context Router

## 默认入口

所有任务先读：

1. `governance/INDEX.md`
2. `governance/context/PROJECT_OPERATING_MODEL.md`
3. `governance/context/PROJECT-TOPOLOGY.md`
4. `governance/context/CONTEXT-MAP.md`

## 任务类型路由

| 任务类型 | 必读文档 | 可选文档 | 必须产出 |
|---|---|---|---|
| 新功能 | 工程质量标准、未来最优解原则、Ponytail工程阶梯标准、非功能性需求标准、QA计划标准、代理协作协议 | 相关 ADR、术语表 | QA 计划或验证证据 |
| Bug 修复 | 劣质代码定义、本地工具与验证入口 | postmortems、lessons | 复现步骤、回归测试 |
| 性能优化 | 性能效率优化标准、门禁与护栏 | 历史性能复盘 | benchmark/profile 证据 |
| 架构变更 | 架构设计原则、ADR 索引、非功能性需求标准 | tech-debt | ADR 或 ADR 更新 |
| Review | auto-review module context、门禁与护栏 | lessons、agent-feedback | PASS/WARN/BLOCK finding |
| 复盘 | 文档治理规则、门禁与护栏 | postmortems/INDEX.md | 防复发动作 |
| 文档治理 | PROJECT_OPERATING_MODEL、DOCUMENT_DRIVEN_DEVELOPMENT、TOOLCHAIN_MODEL、CONTEXT-ROUTER | ADR、module context、任务 closeout | 文档同步证据或豁免理由 |
| 上游 Harness 研究 | `module-contexts/research/CONTEXT.md`、`research/UPSTREAMS.md`、revision lock | 领域模型、ADR-0001 | revision 绑定、源码可见性与研究限制 |
| Harness 契约 | 架构设计原则、非功能性需求标准、`module-contexts/contracts/CONTEXT.md` | ADR-0001、QA-0001、领域模型 | 正反例门禁与版本演进结论 |
| 问题求解算子库 | `module-contexts/operators/CONTEXT.md`、Operator Spec、PSOA PRD、ADR-0003/0004 | contracts/scripts context、QA 标准 | Core 格式、Profile 完整性、引用和负例证据 |
| Operator Runtime 协议 | `module-contexts/contracts/CONTEXT.md`、`module-contexts/examples/CONTEXT.md`、Operator Spec、ADR-0007 | operators/scripts context、QA-0004 | Runtime Core 正反例、参考 Harness 行为与职责边界证据 |
