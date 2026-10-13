---
id: GOV-CONTEXT-ROUTER
type: process
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-08-14
review_cycle: P90D
---

# Context Router

## 默认入口

所有任务先读：

1. `governance/INDEX.md`
2. `governance/context/PROJECT_OPERATING_MODEL.md`
3. `governance/context/PROJECT-TOPOLOGY.md`
4. `governance/context/CONTEXT-MAP.md`

涉及安全能力边界、工具选型或产品覆盖时，再读 `governance/context/CYBERSECURITY_LANDSCAPE.md`。
涉及什么动作需要授权、ScopeGrant 导入或主动交互时，再读 `governance/context/AUTHORIZATION_BOUNDARIES.md`。

## 任务类型路由

| 任务类型 | 必读文档 | 可选文档 | 必须产出 |
|---|---|---|---|
| 新功能 | 工程质量标准、未来最优解原则、Ponytail工程阶梯标准、非功能性需求标准、QA计划标准、代理协作协议 | 相关 ADR、术语表 | QA 计划或验证证据 |
| Bug 修复 | 劣质代码定义、本地工具与验证入口 | postmortems、lessons | 复现步骤、回归测试 |
| 性能优化 | 性能效率优化标准、门禁与护栏 | 历史性能复盘 | benchmark/profile 证据 |
| 架构变更 | 架构设计原则、网络安全全局景观、ADR 索引、非功能性需求标准 | tech-debt | ADR 或 ADR 更新 |
| Review | auto-review module context、门禁与护栏 | lessons、agent-feedback | PASS/WARN/BLOCK finding |
| 复盘 | 文档治理规则、门禁与护栏 | postmortems/INDEX.md | 防复发动作 |
| 文档治理 | PROJECT_OPERATING_MODEL、DOCUMENT_DRIVEN_DEVELOPMENT、TOOLCHAIN_MODEL、CONTEXT-ROUTER | ADR、module context、任务 closeout | 文档同步证据或豁免理由 |
| Web3/EVM 审计 | 0004 任务包、TOOLCHAIN_MODEL、web3-lab/README、AUTHORIZATION_BOUNDARIES、门禁与护栏 | CYBERSECURITY_LANDSCAPE、ADR-0001 | 候选 JSON + 证据账本 + 独立验证 artifact |
| Web3 工具准入/验证门禁 | 0005 任务包、control-plane verification policy、TOOLCHAIN_MODEL | 0002 准入模型、0004 候选表 | 准入校验 + 验证门禁结果 |
