---
id: GOV-CONTEXT-MAP
type: index
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-08-13
review_cycle: P90D
---

# Context Map

## 领域上下文

| 领域 | 代码目录 | 上下文文件 | 相关 ADR / Gate | 常用验证 |
|---|---|---|---|---|
| 项目根 | `.` | `PROJECT_OPERATING_MODEL.md` | ADR-0000 | `make check` |
| 问题空间 | `problem-library/` | `module-contexts/problem-library/CONTEXT.md` | ADR-0000 | portable/full problem validation |
| 研究空间 | `research/` | `module-contexts/research/CONTEXT.md` | ADR-0000 | research spaces validation |
| 成果/解空间 | `result-library/` | `module-contexts/result-library/CONTEXT.md` | ADR-0000、GATE-0002 | research spaces validation + negative tests |
| 文献空间 | `literature/` | `literature/README.md`、`literature/AGENTS.md` | - | portable/full literature validation |
| 形式化方法地图 | `governance/standards/FORMAL-METHODS-MAP.md` | `FORMAL-METHODS-MAP.md`、`.codex/skills/` | GATE-0002 | README/skill boundary checks + governance strict/health |
| 全生命周期模型 | `governance/standards/RESEARCH-LIFECYCLE-MODEL-v0.1.md` | `PROJECT_OPERATING_MODEL.md`、`PROJECT-TOPOLOGY.md`、`research/`、`result-library/` | GATE-0002 | lifecycle/identity/evidence boundary checks |
| 治理包 | `governance/` | `AGENT-ENTRY.md` | GATE-0000/0001 | governance strict/health |

## 维护规则

- 模块事实由局部 README/AGENTS 与治理 module context 共同表达，不互相替代。
- 新增稳定一级空间后，必须在本表、PROJECT-TOPOLOGY 和根 AGENTS 中登记。
- 所有相对路径均以 `governance/context/` 为上下文解释；代码目录仍以项目根为准。
