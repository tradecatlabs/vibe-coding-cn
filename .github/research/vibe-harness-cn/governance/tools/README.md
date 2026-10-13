---
id: TOOLS-GOVERNANCE
type: tooling
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-08-13
review_cycle: P90D
---

# Governance Tools

这里放治理包自身维护脚本或接入说明。默认不修改项目外部 CI、lint 或 hook。

默认内置工具：

- `init_governance_package.py`：初始化或补齐治理包。
- `new_governance_record.py`：新增 ADR/Gate/QA/Postmortem/Lesson/Agent Feedback 等编号记录。
- `new_module_context.py`：新增治理包内模块上下文，并更新 `CONTEXT-MAP.md`。
- `rebuild_governance_index.py`：重建根索引、记录索引、`architecture-gates/rules/INDEX.md` 和 `GATE-INDEX.md`。
- `validate_governance_package.py`：校验治理包结构、frontmatter 和 gate 必填项。
- `governance_health_report.py`：输出治理包健康度、占位内容、过期文档、open feedback 和下一步动作。
- `governance_context_bundle.py`：按任务类型输出 agent 本次应读取的治理文档、模块上下文和必须产出。

这些脚本只写入 `governance/` 内部；外部 CI、lint、hook 接入必须单独 opt-in。
