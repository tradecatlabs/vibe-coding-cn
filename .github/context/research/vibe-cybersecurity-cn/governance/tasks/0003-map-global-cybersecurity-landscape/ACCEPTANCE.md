# Task-Level Acceptance

- 长期景观同时解释资产面、威胁面、防御生命周期和证据标准。
- 产品边界区分直接建设、成熟集成和禁止自治。
- 0001 八类候选计数合计 46，并标明研究覆盖和真实空白。
- 所有动态框架版本有官方来源和检索截面。
- 没有扫描、安装、利用或生产可用声明。

# Validation Plan

```bash
jq '[.candidates | group_by(.category)[] | length] | add' governance/tasks/0001-survey-cybersecurity-supply-chain/supply-chain-candidates.json
python3 <CODEX_SKILLS>/auto-thinking/scripts/validate_task_intent.py --file governance/tasks/0003-map-global-cybersecurity-landscape/TASK_INTENT.json
python3 <CODEX_SKILLS>/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0003-map-global-cybersecurity-landscape --phase closeout
python3 governance/tools/rebuild_governance_index.py --project-root .
python3 governance/tools/validate_governance_package.py --project-root . --strict
python3 governance/tools/governance_health_report.py --project-root . --strict
```

# Review Gate

- `PASS`：概念职责清楚、版本有来源、候选数量一致、项目边界未越权、文档索引同步。
- `WARN`：市场分类或新兴标准可能变化，但有时点和复核条件。
- `BLOCK`：候选被声称为已运行、实证漏洞与扫描告警混淆，或核心文档/链接校验失败。

# Runtime Verification Gate

本任务不改变运行时行为，运行时验证为 `Not Applicable`。它不能证明任何扫描器效果或系统生产就绪。

# Ship Readiness

只允许交付本地研究与治理资产；不提交、不推送、不部署、不安装。

# Task Package Acceptance

- TP-01：至少覆盖治理、行为、应用、供应链、漏洞数据、情报交换和专项域权威来源。
- TP-02：景观和 ADR 相互引用但职责不重复。
- TP-03：八类计数与 0001 JSON 一致，空白有对接/延后原则。
- TP-04：任务 closeout 与治理 strict/health 新鲜通过。

# Anti-Goals

- 不修改 0001/0002 机器真相源。
- 不虚构工具运行、框架版本或验证结果。
- 不为填满景观而新增工具、依赖、运行时模块或供应链状态。

