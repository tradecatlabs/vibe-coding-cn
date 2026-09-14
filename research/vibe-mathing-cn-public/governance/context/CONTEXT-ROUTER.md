---
id: GOV-CONTEXT-ROUTER
type: process
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-08-13
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
| 形式化方法/工具选型 | `standards/FORMAL-METHODS-MAP.md`、`context/TOOLCHAIN_MODEL.md`、对应 active skill | math-tool maturity registry、fixtures、来源账本 | 方法定位、能力边界和可复跑验证证据 |
| 生命周期/编排设计 | `standards/RESEARCH-LIFECYCLE-MODEL-v0.1.md`、`context/PROJECT_OPERATING_MODEL.md`、相关 `research/`/`result-library/` README | schemas、runtime、GATE-0002、失败路线 | 五级关系、状态轴、预算/恢复边界和未实现项 |
