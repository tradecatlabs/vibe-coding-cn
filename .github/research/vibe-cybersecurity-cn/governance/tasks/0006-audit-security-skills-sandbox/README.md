# Task Overview

- Task ID: `0006`
- Slug: `audit-security-skills-sandbox`
- Objective: 拉取 cybersecurity/挖漏洞领域 skills 候选进入临时沙盒，执行供应链安全审计，输出准入评估。
- Status: `In Progress`

## In Scope

- 在隔离临时沙盒内浅克隆候选 skills 仓库（14 项）。
- 执行供应链安全审计：文件类型/大小、恶意模式、嵌入指令、许可、内容抽样。
- 输出审计报告与准入建议（进入候选 / 需整改 / 拒绝）。
- 审计结论落盘 0006 任务目录。

## Out of Scope

- 不把任何未审计内容安装进 Codex skills 目录。
- 不执行仓库内脚本、不运行"安装/一键部署"指令。
- 不 push、不部署。

## Task Package Tree

```text
ROOT
├── TP-01 沙盒建立与仓库拉取
├── TP-02 供应链安全审计
├── TP-03 审计报告与准入建议
└── TP-04 治理同步与 closeout
```

## Reading Order

1. `CONTEXT.md`
2. `SKILL_AUDIT_REPORT.md`
3. `STATUS.md`

## Task Package Overview

| Node | Output | Acceptance |
|---|---|---|
| TP-01 | 沙盒目录 + 14 个浅克隆 | 仓库真实存在且完整拉取 |
| TP-02 | 审计数据（统计+模式扫描） | 恶意模式/嵌入指令清单 |
| TP-03 | `SKILL_AUDIT_REPORT.md` | 逐仓库结论与准入建议 |
| TP-04 | 治理同步与 closeout | strict/health 通过 |

## Requirement Alignment

- 用户要求"拉取进入供应链，先建临时沙盒安全审计"：本任务以隔离沙盒 + 静态审计
  执行供应链准入前的安全检查。
- 项目供应链纪律：外部内容不可信，未审计不入候选。
