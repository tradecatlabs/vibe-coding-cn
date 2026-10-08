# addyosmani/agent-skills 研究域

## 字多不看

- 本目录研究 Addy Osmani 的工程技能集合。
- 当前优先级：P1；研究角色：AI coding agent 的流程技能与质量门禁。
- 重点观察规格、计划、构建、测试、审查、简化和发布如何变成可执行技能。

## 快速导航

| 文档 | 定位 |
|:---|:---|
| [domain.yml](domain.yml) | 仓库事实快照、研究方向、优先级和来源证据。 |
| [analysis.md](analysis.md) | 工程技能集合的结构化研究结论和迁移边界。 |
| [deep-dive.md](deep-dive.md) | 命令、技能目录、安装方式和质量门禁的 L2 研究。 |
| [AGENTS.md](AGENTS.md) | 本研究域维护规则。 |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

### 细粒度目录

- [domain.yml](domain.yml) - 仓库事实快照、研究方向、优先级和来源证据。
- [analysis.md](analysis.md) - 工程技能集合的结构化研究结论和迁移边界。
- [deep-dive.md](deep-dive.md) - 命令、技能目录、安装方式和质量门禁的 L2 研究。
- [AGENTS.md](AGENTS.md) - 本研究域维护规则。

</details>

## 使用方式

- 先读本 README 的判断，再读 analysis.md 和 deep-dive.md。
- 需要当前安装或命令列表时，优先核验项目主页 https://skills.addy.ie 和 raw/ 快照。
- 只迁移流程契约和质量门禁思想，不复制未经审查的 skill 实现或共享依赖。

## 正文

### 研究定位

addyosmani/agent-skills 是面向 AI coding agent 的生产级工程技能集合，将开发生命周期拆成规格、计划、构建、测试、约束、审查、简化和发布等动作。

### 当前判断

它与本仓的[功法体系](../../docs/gongfa/README.md)和[Skills 执行能力](../../skills/README.md)职责高度相关，价值在于提供一套短命令到完整工程生命周期的映射。对本仓最值得借鉴的是“质量门禁跟随开发阶段”，而不是盲目增加更多 skill。

### 观察字段

- GitHub URL：https://github.com/addyosmani/agent-skills
- 当前研究方向：skill-governance
- 当前优先级：P1
- 当前归档状态：false
- 主要语言：JavaScript
- 最新 release：0.6.9
- 项目主页：https://skills.addy.ie

### 后续观察

- 单 skill 安装时共享 references 缺失的问题如何处理。
- Codex、Claude Code、Cursor、Copilot 和 Cline 之间的能力适配边界。
- /spec、/plan、/build、/test、/review 和 /ship 是否能映射成不重复的本仓入口。
