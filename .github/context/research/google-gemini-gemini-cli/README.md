# google-gemini/gemini-cli 研究域

## 字多不看

- 本目录研究 Google 的开源终端 AI Agent `gemini-cli`。
- 当前优先级：P1；研究角色：面向终端的开源 coding agent 与 MCP 客户端。
- 重点观察上下文、工具调用、扩展、MCP、沙箱和交互式 CLI 的组合方式。

## 快速导航

| 文档 | 定位 |
|:---|:---|
| [domain.yml](domain.yml) | 仓库事实快照、研究方向、优先级和来源证据。 |
| [analysis.md](analysis.md) | 终端 Agent 的结构化研究结论和迁移边界。 |
| [deep-dive.md](deep-dive.md) | CLI、扩展和工具边界的 L2 研究。 |
| [AGENTS.md](AGENTS.md) | 本研究域维护规则。 |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

### 细粒度目录

- [domain.yml](domain.yml) - 仓库事实快照、研究方向、优先级和来源证据。
- [analysis.md](analysis.md) - 终端 Agent 的结构化研究结论和迁移边界。
- [deep-dive.md](deep-dive.md) - CLI、扩展和工具边界的 L2 研究。
- [AGENTS.md](AGENTS.md) - 本研究域维护规则。

</details>

## 使用方式

- 先读本 README 的当前判断，再读 `analysis.md` 和 `deep-dive.md`。
- 需要比较终端 Agent 时，结合 `openai-codex`、Aider、Cline 和 OpenCode 研究域阅读。
- 只迁移可验证的上下文、扩展和工具边界，不复制特定模型或供应商账号流程。

## 正文

### 研究定位

`google-gemini/gemini-cli` 是 Google 维护的开源终端 AI Agent，提供 CLI 交互、工具使用、MCP 和扩展能力。

### 当前判断

它是本仓研究矩阵中重要的“模型厂商开源 CLI”对标，能帮助区分模型能力和 Harness 能力。最值得观察的是终端入口如何把上下文、工具、扩展与用户确认组织成一条可持续执行链。

### 观察字段

- GitHub URL：https://github.com/google-gemini/gemini-cli
- 项目主页：https://geminicli.com
- 当前研究方向：`coding-agent-tooling`
- 当前优先级：P1
- 当前归档状态：`false`
- 主要语言：`TypeScript`

### 后续观察

- 扩展和 MCP 的边界是否保持清晰、可安装和可审计。
- 工具权限、沙箱与用户确认是否能覆盖高风险命令。
- 哪些终端工作流可转化为本仓的 CLI 配置、workflow 和质量门禁文档。
