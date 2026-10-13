# Task-Level Acceptance

- 14 个候选仓库在隔离沙盒内完成浅克隆。
- 审计覆盖：文件统计、恶意模式扫描、嵌入指令扫描、许可核验、内容抽样。
- `SKILL_AUDIT_REPORT.md` 逐仓库给出结论（进入候选/需整改/拒绝）与证据。
- 未安装任何 skills 到 Codex 目录；无公网副作用。

# Validation Plan

```bash
ls .sandbox/skill-audit/                       # 沙盒内容
python3 governance/tasks/0006-audit-security-skills-sandbox/audit_skills.py
python3 <CODEX_SKILLS>/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0006-audit-security-skills-sandbox --phase closeout
python3 governance/tools/validate_governance_package.py --project-root . --strict
```

# Review Gate

- `PASS`：审计覆盖全部候选、结论有证据、未越权执行。
- `WARN`：低置信度恶意怀疑项，标记人工复核。
- `BLOCK`：发现高危投毒模式仍进入候选，或审计缺项。

# Runtime Verification Gate

本任务运行于本地沙盒；运行时验证为 `local-sandbox-only`。
未执行仓库内任何脚本，未安装任何 skill。

# Task Package Acceptance

- TP-01：14/14 仓库浅克隆成功。
- TP-02：审计扫描覆盖全部候选，命中清单完整。
- TP-03：逐仓库结论、风险分级、使用护栏齐备。
- TP-04：closeout 与治理 strict 通过。

# Ship Readiness

只交付本地审计报告；不安装、不部署、不 push。

# Anti-Goals

- 不执行仓库内任何脚本/安装器。
- 不把审计通过等同于内容可信。
