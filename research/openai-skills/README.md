# openai/skills 研究域

## 字多不看

- 本目录研究 OpenAI 官方公开的 Codex Skills Catalog 及其迁移到 Plugins 的过程。
- 当前优先级：P2；研究角色：Codex 技能目录的历史演进与迁移参照。
- 重点观察技能的目录形态、触发方式、渐进式加载、许可证和安装边界。

## 快速导航

| 文档 | 定位 |
|:---|:---|
| [domain.yml](domain.yml) | 仓库事实快照、研究方向、优先级和来源证据。 |
| [analysis.md](analysis.md) | 结构化研究结论、迁移边界和验证动作。 |
| [deep-dive.md](deep-dive.md) | 技能目录与 Codex 集成方式的 L2 研究。 |
| [AGENTS.md](AGENTS.md) | 本研究域维护规则。 |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

### 细粒度目录

- [domain.yml](domain.yml) - 仓库事实快照、研究方向、优先级和来源证据。
- [analysis.md](analysis.md) - 结构化研究结论、迁移边界和验证动作。
- [deep-dive.md](deep-dive.md) - 技能目录与 Codex 集成方式的 L2 研究。
- [AGENTS.md](AGENTS.md) - 本研究域维护规则。

</details>

## 使用方式

- 先读本 README 的当前判断，再读 `analysis.md` 和 `deep-dive.md`。
- 需要判断技能是否可复用时，再核验 `raw/` 的原始仓库材料和 `domain.yml` 的观测日期。
- 稳定结论下沉到本仓 `skills/` 或 `docs/gongfa/`，不要长期停在研究域。

## 正文

### 研究定位

`openai/skills` 是 OpenAI 公开的 Codex Skills Catalog，但当前仓库 README 已标注 deprecated，并把现行插件与 skill-only plugin 示例指向 `openai/plugins`。它现在更适合研究技能目录如何迁移到插件分发体系，而不是作为当前安装入口。

### 当前判断

它补齐了本仓现有 `skills/` 研究中“技能如何作为产品化分发单元”的官方历史对标。最值得借鉴的是目录发现、技能边界和渐进式上下文加载；当前使用应转向 `openai/plugins`，不应把已废弃目录当作安装入口，也不应直接把外部技能当作本仓规则执行。

### 观察字段

- GitHub URL：https://github.com/openai/skills
- 当前研究方向：`coding-agent-tooling`
- 当前优先级：P2
- 当前归档状态：`false`
- 主要语言：`Python`

### 后续观察

- `openai/plugins` 如何承接技能目录的元数据、版本和安装约定。
- Codex 官方文档如何定义技能、插件与权限的关系。
- 哪些技能机制可以转化为本仓的触发、输入输出和验证契约。
