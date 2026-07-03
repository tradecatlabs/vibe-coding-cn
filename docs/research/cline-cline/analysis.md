# cline/cline 研究分析

## 本轮结论

- Cline 是多表面 coding agent 产品，覆盖 VS Code Extension、CLI、Kanban、SDK 和 JetBrains Plugin。
- 它的研究重点不是单一模型调用，而是 agent 工具面、编辑器集成、规则/技能、评估和产品化分层。
- 本仓应重点吸收它的多入口架构、规则文件约定、evals 目录和 extension/webview 分离。

## 本地证据

- 研究对象：`cline/cline`
- 当前研究角色：IDE/SDK/CLI 自主编码 Agent
- 本轮成熟度：L1 初步理解
- 原始仓库：`raw/repository/`
- 原始来源清单：`raw/sources.yml`
- 事实摘要：`domain.yml`

## 结构观察

- 根目录包含 `.agents/`、`.claude/`、`.cline/`、`.clinerules/`、`apps/`、`sdk/`、`evals/` 和 `package.json`。
- `apps/` 和 `sdk/` 表明它已经从单一 VS Code 插件演化成多产品面。
- README 明确列出 CLI、Kanban、VS Code Extension、JetBrains Plugin、SDK、Plan and Act、Rules and Skills。

## 可借鉴点

- 把 Agent 能力拆成产品表面、SDK、规则、技能和评估，而不是把所有逻辑塞进一个入口。
- 规则文件和技能目录是让用户控制 agent 行为的关键资产。
- IDE agent 需要 plan/act 分离，降低自动执行的不可控风险。

## 风险和边界

- 产品面很多，架构复杂度高，直接模仿会带来过高维护成本。
- 前端、扩展宿主、模型工具调用和评估同时演进，研究需要分层拆解。
- 作为快速迭代项目，某些目录和命令可能频繁变化。

## 下一轮研究任务

- 拆读 `apps/`、`sdk/`、`evals/` 的边界，形成 IDE agent 架构图。
- 提炼 Cline 的 rules/skills 模式，和本仓 `skills/` 体系对照。

## 沉淀判断

- 本轮只完成 L1 理解，不直接迁入 concepts、references、workflow 或 skills。
- 只有经过 L2 源码阅读、实验验证或交叉对照后的结论，才进入稳定层。