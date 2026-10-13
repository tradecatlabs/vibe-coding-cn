---
id: TOOLS-GOVERNANCE
type: tooling
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-09-01
review_cycle: P90D
---

# Governance Tools

这里放治理包自身维护脚本或接入说明。默认不修改项目外部 CI、lint 或 hook。

默认内置工具：

方法层入口：先读 `governance/standards/FORMAL-METHODS-MAP.md` 确定规格、验证范式和 Lean 的位置，再用下列工具检查实际能力；工具目录不替代方法地图或证据门禁。

公开能力边界：`MATH_TOOL_CATALOG.md` 使用严格两列（工具族 | 解释与说明）；`math-tool-maturity.v1.json` 是 41 个工具族的机器注册表，不能被解释为某台机器的安装或运行报告。

问题库候选工具（候选永不直接准入）：

- `scripts/build_candidate_observations.py`：从本地 inventory 与解析器生成带摘要的 CandidateObservation snapshot。
- `scripts/validate_candidate_problem_library.py`：校验来源、parser、artifact、digest、路径和 `research_eligible=false`。
- `scripts/audit_candidate_admission.py`：只读输出来源级审计，不写 SourceRecord、ProblemContract、Attempt、Result 或 Solution。
- `scripts/query_problem_library.py`：默认 admitted；候选必须显式 collection。

数学工具契约：

- `scripts/validate_math_tool_maturity.py`：校验成熟度与 runtime route 不越权。
- `scripts/check_math_tools.py`：有 timeout 的现场探针，稳定标签不泄漏可执行路径。
- `scripts/run_math_tool_canaries.py`：有界正例、反例、错误和 timeout canary；不访问网络、不写研究记录。
- `scripts/validate_math_tool_canaries.py`：校验显式提供的 canary 报告；公开仓不携带运行报告。


- `init_governance_package.py`：初始化或补齐治理包。
- `new_governance_record.py`：新增 ADR/Gate/QA/Postmortem/Lesson/Agent Feedback 等编号记录。
- `new_module_context.py`：新增治理包内模块上下文，并更新 `CONTEXT-MAP.md`。
- `rebuild_governance_index.py`：重建根索引、记录索引、`architecture-gates/rules/INDEX.md` 和 `GATE-INDEX.md`。
- `validate_governance_package.py`：校验治理包结构、frontmatter 和 gate 必填项。
- `governance_health_report.py`：输出治理包健康度、占位内容、过期文档、open feedback 和下一步动作。
- `governance_context_bundle.py`：按任务类型输出 agent 本次应读取的治理文档、模块上下文和必须产出。

这些脚本只写入 `governance/` 内部；外部 CI、lint、hook 接入必须单独 opt-in。
