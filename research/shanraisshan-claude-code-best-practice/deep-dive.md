# shanraisshan/claude-code-best-practice 深度研究

## 研究级别

- 当前级别：L2 源码/结构深度研究。
- 研究对象：`shanraisshan/claude-code-best-practice`。
- 证据来源：本目录 `raw/` 下的 GitHub 元数据、README 快照和本地仓库工作树。
- 观察日期：2026-07-03。

## L2 结论

`shanraisshan/claude-code-best-practice` 更像一个 Claude Code / Agentic Engineering 方法操作系统，
不是单篇教程。它把最佳实践、实现文档、编排工作流、agent teams、reports、tips、videos、
Claude 配置、Codex 配置和 MCP 配置放在同一个研究对象内，重点展示“如何把 AI 工程经验变成
可复用操作资产”。

对本仓最重要的启发是：方法论必须落到文件、配置、工作流、示例输出和报告中，否则就只是口号。

## 源码证据

- `raw/repository/CLAUDE.md`：Claude 项目级上下文入口。
- `raw/repository/.mcp.json`：MCP 配置入口。
- `raw/repository/.claude/settings.json`：Claude 配置。
- `raw/repository/.codex/config.toml`：Codex 配置。
- `raw/repository/.codex/hooks.json`：Codex hooks 配置。
- `raw/repository/best-practice/claude-subagents.md`：subagents 最佳实践。
- `raw/repository/best-practice/claude-skills.md`：skills 最佳实践。
- `raw/repository/best-practice/claude-commands.md`：commands 最佳实践。
- `raw/repository/best-practice/claude-mcp.md`：MCP 最佳实践。
- `raw/repository/implementation/claude-subagents-implementation.md`：subagents 实现文档。
- `raw/repository/implementation/claude-goal-implementation.md`：goal 实现文档。
- `raw/repository/implementation/claude-skills-implementation.md`：skills 实现文档。
- `raw/repository/orchestration-workflow/orchestration-workflow.md`：编排工作流说明。
- `raw/repository/agent-teams/agent-teams-prompt.md`：agent teams prompt。
- `raw/repository/reports/why-harness-is-important.md`：Harness 重要性报告。

## 关键机制

### 方法论被文件系统化

这个仓库把 best practice、implementation、workflow、reports 和 tips 分开。它说明成熟经验不应该
只放在 README，而应按用途进入不同层：原则、实现、编排、案例、报告和配置。

### 配置是研究对象的一部分

`.claude/`、`.codex/` 和 `.mcp.json` 说明 AI 工程不是纯文档工作。模型入口、工具入口、hooks、
settings 和项目级上下文共同构成真实工作系统。

### Agentic Engineering 强调编排

`orchestration-workflow/` 和 `agent-teams/` 体现了从单 Agent 交互走向多角色、多步骤、可复用流程
的趋势。这里的关键不是“多 Agent 数量”，而是任务边界、上下文分发、验收标准和输出归档。

### 报告层提供反思和二次沉淀

`reports/` 把经验、问题和工具比较沉淀成独立材料。这对于本仓很重要：研究域的最终价值不是
收集资料，而是形成可复用判断。

## 可迁移模式

- 将经验分成 best-practice、implementation、workflow、reports 和 config 五层。
- 对每条方法论要求至少能落到一个文件、一个流程、一个示例或一个检查项。
- 将 hooks、settings、MCP 和项目上下文作为 AI 工程系统的一部分纳入治理。
- 对复杂任务使用 agent teams 或任务树时，必须先定义职责、边界、输入输出和验收标准。
- 重要结论需要有报告层，避免只在临时对话里消失。

## 对本仓的影响

本仓已经有 concepts、references、workflow、skills、research 和 governance 风格的资产雏形。
下一步应让这些层级更明确：

- principles 和 concepts 放底层认知。
- references 放可复用模板、清单和结构。
- workflow 放执行过程和门禁。
- skills 放 Agent 可执行能力。
- research 放未稳定的研究对象。
- reports 或 analysis 放研究判断和阶段复盘。

## 风险和待验证项

- 该仓库强烈绑定 Claude Code 生态，本仓不能直接照搬为通用事实。
- 个人方法论仓库容易混入偏好和风格判断，迁移时必须转成可验证契约。
- 本轮没有验证其中 hooks、MCP、agent teams 的真实运行效果。

## 下一步 L3 验证任务

- 在本仓补一份“方法论如何下沉到 concepts/references/workflow/skills”的分流规则。
- 对已有经验短句建立对应的可执行示例、检查项或技能入口。
- 把复杂研究任务的 agent teams 模式整理成本仓自己的任务编排契约。
- 将 Harness 相关结论与 `research/harness/` 做交叉审计。
