# OpenHands/OpenHands 研究域

## 字多不看

- 本目录研究 OpenHands 的 AI 驱动开发平台与 Agent 运行方式。
- 当前优先级：P1；研究角色：端到端软件开发 Agent 与执行环境。
- 重点观察任务状态、工具调用、运行环境、评估、回放和人机接管边界。

## 快速导航

| 文档 | 定位 |
|:---|:---|
| [domain.yml](domain.yml) | 仓库事实快照、研究方向、优先级和来源证据。 |
| [analysis.md](analysis.md) | AI 驱动开发平台的结构化研究结论和迁移边界。 |
| [deep-dive.md](deep-dive.md) | Agent、运行环境和评估机制的 L2 研究。 |
| [AGENTS.md](AGENTS.md) | 本研究域维护规则。 |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

### 细粒度目录

- [domain.yml](domain.yml) - 仓库事实快照、研究方向、优先级和来源证据。
- [analysis.md](analysis.md) - AI 驱动开发平台的结构化研究结论和迁移边界。
- [deep-dive.md](deep-dive.md) - Agent、运行环境和评估机制的 L2 研究。
- [AGENTS.md](AGENTS.md) - 本研究域维护规则。

</details>

## 使用方式

- 先读本 README 的当前判断，再读 `analysis.md` 和 `deep-dive.md`。
- 将它作为“完整开发环境 + Agent 执行循环”的对标对象，不把平台级能力等同于本仓教程必须提供的功能。
- 稳定结论优先下沉到本仓 `docs/gongfa/` 或 `skills/`。

## 正文

### 研究定位

`OpenHands/OpenHands` 是一个 AI 驱动开发项目，面向从任务描述到代码修改、命令执行和结果交付的完整开发过程。

### 当前判断

它适合研究“coding agent 如何从聊天工具变成开发执行环境”。相较只关注 CLI 命令的项目，它更能暴露任务状态、工作区隔离、执行回放和评估体系对可靠性的影响。

### 观察字段

- GitHub URL：https://github.com/OpenHands/OpenHands
- 当前研究方向：`agent-runtime`
- 当前优先级：P1
- 当前归档状态：`false`
- 主要语言：`TypeScript`

### 后续观察

- Agent 执行环境与宿主机权限如何隔离。
- 任务回放、评估和人工接管是否能提供可复现证据。
- 哪些平台能力适合转化为本仓的质量门禁，而不是继续增加文档体积。
