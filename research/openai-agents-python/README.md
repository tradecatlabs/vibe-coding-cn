# openai/openai-agents-python 研究域

## 字多不看

- 本目录研究 OpenAI Agents SDK 的 Python 实现。
- 当前优先级：P1；研究角色：多 Agent 工作流与运行时编排框架。
- 重点观察 Agent、工具、handoff、guardrail、session 和 tracing 如何形成可验证闭环。

## 快速导航

| 文档 | 定位 |
|:---|:---|
| [domain.yml](domain.yml) | 仓库事实快照、研究方向、优先级和来源证据。 |
| [analysis.md](analysis.md) | Agent 工作流的结构化研究结论和迁移边界。 |
| [deep-dive.md](deep-dive.md) | SDK 运行时对象与验证机制的 L2 研究。 |
| [AGENTS.md](AGENTS.md) | 本研究域维护规则。 |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

### 细粒度目录

- [domain.yml](domain.yml) - 仓库事实快照、研究方向、优先级和来源证据。
- [analysis.md](analysis.md) - Agent 工作流的结构化研究结论和迁移边界。
- [deep-dive.md](deep-dive.md) - SDK 运行时对象与验证机制的 L2 研究。
- [AGENTS.md](AGENTS.md) - 本研究域维护规则。

</details>

## 使用方式

- 先读本 README 的当前判断，再读 `analysis.md` 和 `deep-dive.md`。
- 涉及 SDK 当前接口时，优先核验 OpenAI 官方文档和 `raw/` 中的仓库快照。
- 只迁移 Agent 编排与验证机制，不把 SDK 依赖当作本仓文档系统的必要前置。

## 正文

### 研究定位

`openai/openai-agents-python` 是一个轻量的多 Agent 工作流框架，适合研究模型、工具、handoff、guardrail、session 和 tracing 的组合方式。

### 当前判断

它与 `openai/codex` 互补：Codex 更接近本地 coding agent 的执行控制面，Agents SDK 更接近可编排 Agent 应用的运行时抽象。对本仓最有价值的是把“Agent 负责想什么、工具能做什么、结果如何被护栏和追踪验证”拆成清晰接口。

### 观察字段

- GitHub URL：https://github.com/openai/openai-agents-python
- 当前研究方向：`agent-runtime`
- 当前优先级：P1
- 当前归档状态：`false`
- 主要语言：`Python`

### 后续观察

- handoff 与多 Agent 编排是否能在复杂任务中降低上下文负担。
- guardrail、session 和 tracing 是否能形成可审计的行为证据。
- 哪些抽象能沉淀为本仓 `docs/gongfa/` 的通用方法或 `skills/` 的执行契约，哪些只适合运行时产品。
