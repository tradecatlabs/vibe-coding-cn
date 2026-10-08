# openai/openai-agents-js 研究域

## 字多不看

- 本目录研究 OpenAI 官方 JavaScript/TypeScript Agents SDK。
- 当前优先级：P1；研究角色：Agent 运行时与多 Agent 工作流编排。
- 重点观察工具、handoff、guardrail、session、sandbox 和 tracing 如何形成可验证闭环。

## 快速导航

| 文档 | 定位 |
|:---|:---|
| [domain.yml](domain.yml) | 仓库事实快照、研究方向、优先级和来源证据。 |
| [analysis.md](analysis.md) | TypeScript Agent 运行时的结构化研究结论和迁移边界。 |
| [deep-dive.md](deep-dive.md) | SDK 包结构、sandbox 与验证机制的 L2 研究。 |
| [AGENTS.md](AGENTS.md) | 本研究域维护规则。 |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

### 细粒度目录

- [domain.yml](domain.yml) - 仓库事实快照、研究方向、优先级和来源证据。
- [analysis.md](analysis.md) - TypeScript Agent 运行时的结构化研究结论和迁移边界。
- [deep-dive.md](deep-dive.md) - SDK 包结构、sandbox 与验证机制的 L2 研究。
- [AGENTS.md](AGENTS.md) - 本研究域维护规则。

</details>

## 使用方式

- 先读本 README 的当前判断，再读 analysis.md 和 deep-dive.md。
- 涉及当前接口时，优先核验官方文档 https://openai.github.io/openai-agents-js/ 和 raw/ 中的仓库快照。
- 不把 SDK 依赖当作本仓文档系统的必要前置；只迁移清晰的运行时边界和验证契约。

## 正文

### 研究定位

openai/openai-agents-js 是 OpenAI 官方的 JavaScript/TypeScript Agents SDK，面向多 Agent 工作流、工具调用和可追踪的 Agent 应用。

### 当前判断

它与 openai/openai-agents-python 互补：本研究域关注 TypeScript 生态中的 Agent 编排、工具、护栏、沙箱和 tracing；对本仓最有价值的是把“模型意图”和“运行时执行”分成可以验证的接口。

### 观察字段

- GitHub URL：https://github.com/openai/openai-agents-js
- 当前研究方向：agent-runtime
- 当前优先级：P1
- 当前归档状态：false
- 主要语言：TypeScript
- 最新 release：v0.17.1

### 后续观察

- sandbox agent 是否形成稳定的文件系统、命令执行和权限边界。
- guardrail、session 和 tracing 是否能提供跨轮次的可审计证据。
- 哪些运行时概念可以沉淀为本仓 `docs/gongfa/` 的通用方法或 `skills/` 的执行契约。
