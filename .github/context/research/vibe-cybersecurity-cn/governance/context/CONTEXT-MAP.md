---
id: GOV-CONTEXT-MAP
type: index
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-08-14
review_cycle: P90D
---

# Context Map

## 领域上下文

| 领域 | 代码目录 | 上下文文件 | 相关 ADR | 常用验证 |
|---|---|---|---|---|
| 项目根 | `.` | `context/PROJECT-TOPOLOGY.md` | `decisions/adr/INDEX.md` | governance strict validate |
| 治理包 | `governance/` | `context/AGENT-ENTRY.md` | `decisions/adr/INDEX.md` | governance health report |
| 任务容器 | `governance/tasks/` | `tasks/INDEX.md` | `decisions/adr/INDEX.md` | task tree validation |
| 网络安全领域与产品边界 | `.` | `context/CYBERSECURITY_LANDSCAPE.md` | `decisions/adr/ADR-0001-security-evidence-control-plane.md` | governance strict validate |
| 授权边界与 ScopeGrant 草案 | `governance/context/` | `context/AUTHORIZATION_BOUNDARIES.md` | `decisions/adr/ADR-0001-security-evidence-control-plane.md` | governance strict + P30D 复查 |
| Web3/EVM 审计闭环（本地靶场） | `web3-lab/` | `tasks/0004-web3-vertical-proof/CONTEXT.md`、`context/TOOLCHAIN_MODEL.md` | `decisions/adr/ADR-0001-security-evidence-control-plane.md` | `web3-lab/validate_lab_evidence.py`、`forge test` |
| Web3 工具准入与验证控制面 | `governance/tasks/0005-admit-web3-toolchain/` | `tasks/0005-*/CONTEXT.md`、`control-plane/verification-policy.v1.json` | `decisions/adr/ADR-0001-security-evidence-control-plane.md` | `validate_web3_admission.py`、`validate_task_verification.py` |
| 实战就绪度（授权协议 fork 级审计） | `governance/context/` | `context/COMBAT_READINESS.md` | `decisions/adr/ADR-0001-security-evidence-control-plane.md` | governance strict + P30D 复查 |

## 维护规则

- 不把模块上下文散落到代码目录。
- 模块上下文统一放在 `context/module-contexts/`。
- 原有模块 README 只被引用，不被治理包覆盖。
- 新增稳定模块后，再创建 `context/module-contexts/<module>/CONTEXT.md` 并更新本表。
