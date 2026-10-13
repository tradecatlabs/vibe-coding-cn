# Task Overview

- Task ID: `0007`
- Slug: `vendor-project-skills`
- Objective: 把审计通过的 Web3/挖漏洞 skills 拉取为项目级 skill 供应链（vendored，不装全局），固定来源与许可。
- Status: `Done`

## In Scope

- 项目内 `skills/` 目录落地 vendored skills（2 个来源，13 个 skill）。
- `SKILLS_MANIFEST.json` 记录来源、固定 commit、许可、审计状态。
- AGENTS/README 同步项目级 skill 使用规则。

## Out of Scope

- 不安装任何 skill 到全局 全局 Codex skills 目录。
- 不纳入未审计/高敏感仓库（claude-pentest、communitytools 等）。

## Task Package Tree

```text
ROOT
├── TP-01 选择纳入范围
├── TP-02 vendored 落地与清单
├── TP-03 治理同步
└── TP-04 closeout
```

## Requirement Alignment

- 用户要求"拉取项目供应链，作为项目级 skill，不要全局"：
  以仓库内 `skills/` 目录承载，随项目分发，不污染全局环境。

## Reading Order

1. `skills/SKILLS_MANIFEST.json`
2. `skills/README.md`
3. `STATUS.md`

## Task Package Overview

| Node | Output | Acceptance |
|---|---|---|
| TP-01 | 纳入范围清单 | 仅审计通过且方向匹配 |
| TP-02 | `skills/` + manifest | 13 skill 落地、commit 固定 |
| TP-03 | AGENTS/README 同步 | 使用规则清楚 |
| TP-04 | closeout | 校验通过 |
