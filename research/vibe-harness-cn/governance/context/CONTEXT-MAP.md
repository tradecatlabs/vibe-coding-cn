---
id: GOV-CONTEXT-MAP
type: index
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-09-04
review_cycle: P90D
---

# Context Map

## 领域上下文

| 领域 | 代码目录 | 上下文文件 | 相关 ADR | 常用验证 |
|---|---|---|---|---|
| 项目根 | `.` | `context/PROJECT-TOPOLOGY.md` | `decisions/adr/INDEX.md` | governance strict validate |
| 治理包 | `governance/` | `context/AGENT-ENTRY.md` | `decisions/adr/INDEX.md` | governance health report |
| 任务容器 | `governance/tasks/` | `tasks/INDEX.md` | `decisions/adr/INDEX.md` | task tree validation |
| 上游研究 | `research` | `context/module-contexts/research/CONTEXT.md` | `decisions/adr/ADR-0001-元-Harness-采用契约优先的治理控制面.md` | `bash scripts/sync_upstreams.sh` |
| Harness 契约 | `contracts` | `context/module-contexts/contracts/CONTEXT.md` | `decisions/adr/ADR-0001-元-Harness-采用契约优先的治理控制面.md` | `uv run --locked --script scripts/validate_harness.py --self-test` |
| 问题求解算子库 | `operators` | `context/module-contexts/operators/CONTEXT.md` | `decisions/adr/ADR-0003-引入问题求解算子语义层.md`<br>`decisions/adr/ADR-0004-问题求解算子采用宽松核心与可选加严-Profile.md` | `uv run --locked --script scripts/validate_harness.py --operator-library operators/catalog.json` |
| 协议参考消费方 | `examples` | `context/module-contexts/examples/CONTEXT.md` | `decisions/adr/ADR-0007-以参考-Harness-验证-Operator-Runtime-互操作契约.md` | `python3 -m unittest tests.test_reference_operator_harness` |
| 验证脚本 | `scripts` | `context/module-contexts/scripts/CONTEXT.md` | `decisions/adr/ADR-0004-问题求解算子采用宽松核心与可选加严-Profile.md` | `uv run --locked --script scripts/validate_harness.py --self-test` |
| 领域与需求文档 | `docs` | `context/module-contexts/docs/CONTEXT.md` | `decisions/adr/ADR-0001-元-Harness-采用契约优先的治理控制面.md`<br>`decisions/adr/ADR-0003-引入问题求解算子语义层.md` | `python3 governance/tools/validate_governance_package.py --project-root . --strict` |

## 维护规则

- 不把模块上下文散落到代码目录。
- 模块上下文统一放在 `context/module-contexts/`。
- 原有模块 README 只被引用，不被治理包覆盖。
- 新增稳定模块后，再创建 `context/module-contexts/<module>/CONTEXT.md` 并更新本表。
