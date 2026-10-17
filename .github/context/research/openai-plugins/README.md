# openai/plugins 研究域

## 字多不看

- 本目录研究 OpenAI 官方公开的 Codex 插件仓库。
- 当前优先级：P1；研究角色：插件与 skill-only plugin 的能力分发入口。
- 重点观察插件边界、技能打包、发现方式、权限和第三方集成的治理方式。

## 快速导航

| 文档 | 定位 |
|:---|:---|
| [domain.yml](domain.yml) | 仓库事实快照、研究方向、优先级和来源证据。 |
| [analysis.md](analysis.md) | 插件分发与 Codex 集成的结构化研究结论。 |
| [deep-dive.md](deep-dive.md) | 插件目录与技能打包边界的 L2 研究。 |
| [AGENTS.md](AGENTS.md) | 本研究域维护规则。 |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

### 细粒度目录

- [domain.yml](domain.yml) - 仓库事实快照、研究方向、优先级和来源证据。
- [analysis.md](analysis.md) - 插件分发与 Codex 集成的结构化研究结论。
- [deep-dive.md](deep-dive.md) - 插件目录与技能打包边界的 L2 研究。
- [AGENTS.md](AGENTS.md) - 本研究域维护规则。

</details>

## 使用方式

- 先读本 README 的当前判断，再读 `analysis.md` 和 `deep-dive.md`。
- 当前插件格式和安装方式以 OpenAI 官方 Codex 文档为准：<https://developers.openai.com/codex/plugins>。
- 外部插件必须先审查来源、权限、许可证和执行副作用，不能因为插件可发现就默认可信。

## 正文

### 研究定位

`openai/plugins` 是 OpenAI 官方公开的插件仓库，面向 Codex 插件与 skill-only plugin 的示例、目录和分发实践。

### 当前判断

它承接了已废弃的 `openai/skills` 目录，是理解 Codex 如何把可复用技能提升为可安装插件的重要一手对象。对本仓最有价值的是“能力包 + 元数据 + 安装边界”的组织方式，而不是复制某个插件内容。

### 观察字段

- GitHub URL：https://github.com/openai/plugins
- 当前研究方向：`coding-agent-tooling`
- 当前优先级：P1
- 当前归档状态：`false`
- 主要语言：`JavaScript`

### 后续观察

- 插件 manifest、技能目录和依赖声明是否形成稳定规范。
- 插件权限、网络访问和工具调用是否有可审查的安全边界。
- 哪些结构能迁移到本仓 `.github/skills/`，并通过本仓自己的验证门禁。
