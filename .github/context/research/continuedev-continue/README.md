# continuedev/continue 研究域

## 字多不看

- 本目录研究 Continue 开源 coding agent。
- 当前优先级：P2；研究角色：IDE/CLI、模型配置、上下文和 Agent 工具链。
- 维护状态：官方 README 标注仓库不再主动维护，当前仅作历史架构与迁移对标。
- 重点观察同一项目如何承载编辑器辅助、终端 Agent、上下文索引和模型适配。

## 快速导航

| 文档 | 定位 |
|:---|:---|
| [domain.yml](domain.yml) | 仓库事实快照、研究方向、优先级和来源证据。 |
| [analysis.md](analysis.md) | Continue coding agent 的结构化研究结论和迁移边界。 |
| [deep-dive.md](deep-dive.md) | IDE、CLI、上下文和扩展架构的 L2 研究。 |
| [AGENTS.md](AGENTS.md) | 本研究域维护规则。 |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

### 细粒度目录

- [domain.yml](domain.yml) - 仓库事实快照、研究方向、优先级和来源证据。
- [analysis.md](analysis.md) - Continue coding agent 的结构化研究结论和迁移边界。
- [deep-dive.md](deep-dive.md) - IDE、CLI、上下文和扩展架构的 L2 研究。
- [AGENTS.md](AGENTS.md) - 本研究域维护规则。

</details>

## 使用方式

- 先读本 README 的判断，再读 analysis.md 和 deep-dive.md。
- 需要当前安装、配置或模型适配时，优先核验 Continue 文档 https://docs.continue.dev/ 和 raw/ 快照。
- 只迁移上下文边界、配置发现和评估思路，不把 IDE 插件依赖当作本仓 CLI 主线。

## 正文

### 研究定位

continuedev/continue 是开源 coding agent 项目，覆盖 IDE、CLI、模型配置、上下文和扩展等开发入口。

### 当前判断

它适合作为“IDE 入口和 Agent 入口如何共用能力层”的对标对象。对本仓的价值主要在于上下文来源、模型配置、扩展边界和用户入口的分离；不应把 IDE 产品形态与本仓教程的文档职责混淆。

### 观察字段

- GitHub URL：https://github.com/continuedev/continue
- 当前研究方向：coding-agent-tooling
- 当前优先级：P2
- 当前归档状态：false
- 主要语言：TypeScript
- 最新 release：v2.0.0-vscode
- 项目主页：https://continue.dev

### 后续观察

- .continue/、core/、extensions/、gui/、binary/ 和 .github/skills/ 的边界是否稳定。
- 上下文索引、模型配置和 Agent 工具是否有清晰的验证路径。
- 哪些 IDE/CLI 组合经验可以反哺本仓的开发环境和工具选择入口。
