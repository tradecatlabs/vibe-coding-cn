# shanraisshan/claude-code-best-practice 研究分析

## 本轮结论

- 这是 Agentic Engineering 方法论和 Claude Code 资产集合，属于 P1 对标对象。
- 它覆盖 concepts、development workflows、cross-model workflows、skill collections、agent collections、tips、orchestration 等层。
- 本仓应重点吸收其 agent/team/workflow/skill 的组织方式，同时保持本仓自己的中文主线和质量门禁。

## 本地证据

- 研究对象：`shanraisshan/claude-code-best-practice`
- 当前研究角色：Claude Code / Agentic Engineering 最强对标
- 本轮成熟度：L1 初步理解
- 原始仓库：`raw/repository/`
- 原始来源清单：`raw/sources.yml`
- 事实摘要：`domain.yml`

## 结构观察

- 根目录包含 `best-practice/`、`development-workflows/`、`orchestration-workflow/`、`agent-teams/`、`implementation/`、`tips/`、`tutorial/`、`reports/`。
- 存在 `.claude/`、`.codex/`、`.mcp.json`、`CLAUDE.md`，说明它同时面向多个 AI 工具运行环境。
- README 是大型导航页，入口多、概念密度高。

## 可借鉴点

- Agentic Engineering 需要把 workflow、agent team、skills、commands、MCP、tips 分层管理。
- 跨模型/跨工具工作流应该作为研究对象，而不是只绑定某一个产品。
- 大型方法论仓库需要强导航，否则会变成资料迷宫。

## 风险和边界

- 内容高度个人化，不能直接变成本仓标准。
- 覆盖面很宽，容易冲淡本仓“Vibe Coding 中文教程 + 工程治理”的定位。
- 需要区分 Claude Code 专属实践和通用 agent engineering 原则。

## 下一轮研究任务

- 重点拆读 `orchestration-workflow/`、`agent-teams/`、`development-workflows/`。
- 输出与本仓 `skills/`、`workflow/`、`research-domain-contract.md` 的差距清单。

## 沉淀判断

- 本轮只完成 L1 理解，不直接迁入 concepts、references、workflow 或 skills。
- 只有经过 L2 源码阅读、实验验证或交叉对照后的结论，才进入稳定层。