# affaan-m/ECC 研究域

## 字多不看

- 本目录研究 ECC 的 Agent Harness 性能优化、技能、记忆、安全和研究优先实践。
- 当前优先级：P1；研究角色：面向 Codex、Claude Code、OpenCode、Cursor 等工具的 Harness 资产。
- 重点观察上下文压缩、持久记忆、技能组织、验证和安全护栏如何组合。

## 快速导航

| 文档 | 定位 |
|:---|:---|
| [domain.yml](domain.yml) | 仓库事实快照、研究方向、优先级和来源证据。 |
| [analysis.md](analysis.md) | Harness 资产的结构化研究结论、风险和迁移边界。 |
| [deep-dive.md](deep-dive.md) | 技能、记忆、钩子和多 Agent 适配的 L2 研究。 |
| [AGENTS.md](AGENTS.md) | 本研究域维护规则。 |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

### 细粒度目录

- [domain.yml](domain.yml) - 仓库事实快照、研究方向、优先级和来源证据。
- [analysis.md](analysis.md) - Harness 资产的结构化研究结论、风险和迁移边界。
- [deep-dive.md](deep-dive.md) - 技能、记忆、钩子和多 Agent 适配的 L2 研究。
- [AGENTS.md](AGENTS.md) - 本研究域维护规则。

</details>

## 使用方式

- 先读本 README 的判断，再读 analysis.md 和 deep-dive.md。
- 需要当前安装、skill 或配置方式时，优先核验 ECC 官方入口 https://ecc.tools 和 raw/ 快照。
- 只吸收经过审查的 Harness 机制；不把外部命令、钩子、权限扩大或模型特定配置直接复制到本仓。

## 正文

### 研究定位

affaan-m/ECC 是一个面向多种 coding agent 的 Harness 资产集合，关注技能、记忆、安全、研究优先和上下文/性能优化。

### 当前判断

它是本仓 Harness Engineering 研究的补充对标。最有价值的是把 Agent 体验问题拆成上下文、记忆、技能、验证和安全几个可观察面；风险在于外部配置和钩子可能改变本机行为，任何迁移都必须先做来源和副作用审查。

### 观察字段

- GitHub URL：https://github.com/affaan-m/ECC
- 当前研究方向：harness-engineering
- 当前优先级：P1
- 当前归档状态：false
- 主要语言：JavaScript
- 最新 release：v2.2.0
- 项目主页：https://ecc.tools

### 后续观察

- 技能、instinct、memory、security 和 research-first 资产的真实边界。
- Codex、Claude Code、OpenCode、Cursor 之间哪些内容是通用机制，哪些是适配层。
- token/上下文优化是否有 benchmark、失败样本和反 Goodhart 证据。
