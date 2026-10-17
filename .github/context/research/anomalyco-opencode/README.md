# anomalyco/opencode 研究域

## 字多不看

- 本目录研究当前规范仓库 `anomalyco/opencode`，也就是 OpenCode 开源 coding agent。
- 当前优先级：P1；研究角色：模型无关的终端与编辑器 coding agent。
- 重点观察提供商抽象、权限、工具、上下文、插件和多入口体验如何解耦。

## 快速导航

| 文档 | 定位 |
|:---|:---|
| [domain.yml](domain.yml) | 仓库事实快照、研究方向、优先级和来源证据。 |
| [analysis.md](analysis.md) | OpenCode 的结构化研究结论和迁移边界。 |
| [deep-dive.md](deep-dive.md) | 运行时边界、提供商和扩展机制的 L2 研究。 |
| [AGENTS.md](AGENTS.md) | 本研究域维护规则。 |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

### 细粒度目录

- [domain.yml](domain.yml) - 仓库事实快照、研究方向、优先级和来源证据。
- [analysis.md](analysis.md) - OpenCode 的结构化研究结论和迁移边界。
- [deep-dive.md](deep-dive.md) - 运行时边界、提供商和扩展机制的 L2 研究。
- [AGENTS.md](AGENTS.md) - 本研究域维护规则。

</details>

## 使用方式

- 先读本 README 的当前判断，再读 `analysis.md` 和 `deep-dive.md`。
- 与 `openai-codex` 对照阅读：前者强调开放提供商和可扩展 coding agent，后者强调 OpenAI 官方执行控制面。
- 使用 OpenCode 的当前命令、配置或订阅信息前，必须重新核验官方文档 https://opencode.ai/docs/。

## 正文

### 研究定位

`anomalyco/opencode` 是开源 coding agent，目标是在终端和其他开发入口中提供可替换模型、工具调用和项目协作能力。

### 当前判断

它是本仓已有 OpenCode 配置文档的直接研究对象。最值得借鉴的是把模型提供商、Agent 行为、工具权限和用户界面拆开；不能因为仓库规模大或社区关注度高，就把其完整运行时复制到本仓。

### 观察字段

- GitHub URL：https://github.com/anomalyco/opencode
- 项目主页：https://opencode.ai
- 当前研究方向：`coding-agent-tooling`
- 当前优先级：P1
- 当前归档状态：`false`
- 主要语言：`TypeScript`
- 默认分支：`dev`

### 后续观察

- `sst/opencode` 的历史路径和当前规范仓库是否继续保持可追溯重定向。
- 提供商、配置和权限模型是否保持稳定。
- 哪些开放模型接入经验能补充本仓的 CLI 配置与工具选择说明。
