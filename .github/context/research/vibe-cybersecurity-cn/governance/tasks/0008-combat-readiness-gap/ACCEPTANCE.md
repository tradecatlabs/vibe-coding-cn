# Task-Level Acceptance

- 现状盘点表覆盖任务基线、工具链、靶场、验证控制面、skills 供应链，每项绑定真实证据。
- `governance/context/COMBAT_READINESS.md` 落盘：能力域评分、综合得分、P0/P1/P2
  差距清单、M1-M4 里程碑路径。
- 治理文档同步完成：拓扑、操作模型、上下文地图、README、任务索引、tasks/AGENTS.md。
- closeout 校验与 governance strict/health 全绿；无公网副作用。

# Validation Plan

```bash
python3 <CODEX_SKILLS>/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0008-combat-readiness-gap --phase closeout
python3 <CODEX_SKILLS>/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase closeout
python3 governance/tools/rebuild_governance_index.py --project-root .
python3 governance/tools/validate_governance_package.py --project-root . --strict
python3 governance/tools/governance_health_report.py --project-root . --strict
```

# Review Gate

- `PASS`：评分与差距清单绑定真实证据；治理文档无死链/占位；校验全绿。
- `WARN`：某项得分依据不足但已标注为推断，可接受并记录后续验证路径。
- `BLOCK`：证据与现状不符、占位符残留、strict/health 失败。

# Runtime Verification Gate

本任务为纯文档评估，无代码运行时；运行时验证为 `docs-only`。

# Ship Readiness

只交付本地文档与校验结果；不 push、不部署、不执行扫描工具。

# Task Package Acceptance

- TP-01：现状盘点表齐全，证据可溯源。
- TP-02：COMBAT_READINESS.md 含评分、差距清单、里程碑、触发条件与反事实。
- TP-03：6 个治理文档同步完成且无死链。
- TP-04：closeout 校验与 strict/health 全绿。

# Anti-Goals

- 不得修改 `governance/tasks/` 以外路径
- 不得虚构证据
- 不得越权补全未确认信息
