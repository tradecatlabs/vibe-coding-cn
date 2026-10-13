# obra/superpowers 研究域

## 字多不看

- 本目录研究 obra/superpowers 技能框架和软件开发方法论。
- 当前优先级：P1；研究角色：跨 Agent 的可复用技能与开发流程。
- 重点观察规格先行、测试驱动、技能触发、计划执行和多工具分发如何组合。

## 快速导航

| 文档 | 定位 |
|:---|:---|
| [domain.yml](domain.yml) | 仓库事实快照、研究方向、优先级和来源证据。 |
| [analysis.md](analysis.md) | 技能框架和开发方法论的结构化研究结论。 |
| [deep-dive.md](deep-dive.md) | 技能目录、插件适配和流程资产的 L2 研究。 |
| [AGENTS.md](AGENTS.md) | 本研究域维护规则。 |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

### 细粒度目录

- [domain.yml](domain.yml) - 仓库事实快照、研究方向、优先级和来源证据。
- [analysis.md](analysis.md) - 技能框架和开发方法论的结构化研究结论。
- [deep-dive.md](deep-dive.md) - 技能目录、插件适配和流程资产的 L2 研究。
- [AGENTS.md](AGENTS.md) - 本研究域维护规则。

</details>

## 使用方式

- 先读本 README 的判断，再读 analysis.md 和 deep-dive.md。
- 需要当前安装或集成方式时，优先核验上游仓库 https://github.com/obra/superpowers 和 raw/ 快照。
- 不直接复制外部 skill；先审查许可证、触发条件、命令副作用、权限和验证方式。

## 正文

### 研究定位

obra/superpowers 是一个面向多个 coding agent 的技能框架与软件开发方法论，试图把开发过程中的角色、步骤和质量要求封装为可加载能力。

### 当前判断

它是本仓“Prompt -> Skill -> Workflow”分层的强对标。最值得研究的是技能如何在任务开始前被发现、如何强制规格和测试、以及同一套方法如何适配 Codex、Claude Code、Cursor、Gemini CLI 和 OpenCode；不应直接照搬其产品化入口。

### 观察字段

- GitHub URL：https://github.com/obra/superpowers
- 当前研究方向：agent-workflow-methodology
- 当前优先级：P1
- 当前归档状态：false
- 主要语言：Shell
- 最新 release：v6.3.0

### 后续观察

- skill 触发和强制工作流是否有可验证的反例。
- Codex plugin、CLI、Cursor 和 OpenCode 适配是否保持同一能力边界。
- 哪些技能可以转为本仓的最小 owner skill，而不增加重复目录。
