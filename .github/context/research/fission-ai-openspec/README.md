# Fission-AI/OpenSpec 研究域

## 字多不看

- 本目录研究 Fission-AI 的 OpenSpec。
- 当前优先级：P1；研究角色：面向 AI coding assistant 的规格驱动开发工具。
- 重点观察规格、变更提案、实现任务和验证资产如何形成闭环。

## 快速导航

| 文档 | 定位 |
|:---|:---|
| [domain.yml](domain.yml) | 仓库事实快照、研究方向、优先级和来源证据。 |
| [analysis.md](analysis.md) | OpenSpec 工作流的结构化研究结论和迁移边界。 |
| [deep-dive.md](deep-dive.md) | schema、CLI、模板和多工具集成的 L2 研究。 |
| [AGENTS.md](AGENTS.md) | 本研究域维护规则。 |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

### 细粒度目录

- [domain.yml](domain.yml) - 仓库事实快照、研究方向、优先级和来源证据。
- [analysis.md](analysis.md) - OpenSpec 工作流的结构化研究结论和迁移边界。
- [deep-dive.md](deep-dive.md) - schema、CLI、模板和多工具集成的 L2 研究。
- [AGENTS.md](AGENTS.md) - 本研究域维护规则。

</details>

## 使用方式

- 先读本 README 的判断，再读 analysis.md 和 deep-dive.md。
- 需要当前命令、schema 或集成方式时，优先核验 OpenSpec 官网 https://openspec.dev/ 与 raw/ 快照。
- 将它作为 Spec Kit 的独立对标，不直接复制脚本、模板或外部 Agent 指令。

## 正文

### 研究定位

Fission-AI/OpenSpec 是面向 AI coding assistant 的规格驱动开发工具，目标是让需求变化先形成可审查的规格和实施资产，再进入代码修改。

### 当前判断

它与 github/spec-kit 处在相近问题域，但研究重点不同：OpenSpec 更适合观察“变化提案、规格资产和多工具适配”如何落地。对本仓的价值是提供另一种把自然语言需求转成可审查中间产物的实现参照。

### 观察字段

- GitHub URL：https://github.com/Fission-AI/OpenSpec
- 当前研究方向：spec-driven-development
- 当前优先级：P1
- 当前归档状态：false
- 主要语言：TypeScript
- 最新 release：v1.12.0
- 项目主页：https://openspec.dev/

### 后续观察

- 规格与变更提案是否有明确的状态转换和完成判定。
- schema、模板和 CLI 是否能降低不同 Agent 入口之间的语义漂移。
- 哪些结构可以与本仓的任务、质量门禁和 Git 交付闭环组合。
