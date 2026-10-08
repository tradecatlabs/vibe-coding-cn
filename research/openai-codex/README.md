# openai/codex 研究域

## 字多不看

- 本目录研究 `openai/codex` 这个外部仓库。
- 当前优先级：P1；研究角色：官方 coding agent 工具源码。
- GitHub 动态事实放在 `domain.yml`，观测日期为 2026-09-08；当前最新 release 为 `rust-v0.153.4`。

## 快速导航

| 文档 | 定位 |
|:---|:---|
| [domain.yml](domain.yml) | 仓库事实快照、研究方向、优先级和来源证据。 |
| [analysis.md](analysis.md) | 本研究域的结构化研究结果、可借鉴点、风险和下一轮任务。 |
| [deep-dive.md](deep-dive.md) | L2 源码/结构深度研究、关键机制和可迁移模式。 |
| [AGENTS.md](AGENTS.md) | 本研究域维护规则。 |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

### 细粒度目录

- [domain.yml](domain.yml) - 仓库事实快照、研究方向、优先级和来源证据。
- [analysis.md](analysis.md) - 本研究域的结构化研究结果、可借鉴点、风险和下一轮任务。
- [deep-dive.md](deep-dive.md) - L2 源码/结构深度研究、关键机制和可迁移模式。
- [AGENTS.md](AGENTS.md) - 本研究域维护规则。

</details>

## 使用方式

- 先读本 README 的判断，再读 `analysis.md` 和 `deep-dive.md` 的研究结论，最后读 `domain.yml`。
- 需要引用 stars、forks、release、归档状态时，先重新核验 GitHub。
- CLI 安装、认证、IDE、Skills 和 Plugins 的现行用法，以 [OpenAI Codex 文档](https://developers.openai.com/codex) 为准。
- 可复用方法、流程和模板正文归 `docs/gongfa/`，实例练习归 `docs/getting-started/`，执行能力按契约归 `skills/`；具体事实与验证证据仍留在本研究域。

## 正文

### 研究定位

`openai/codex` 的当前研究定位是：官方 coding agent 工具源码。

### 当前判断

适合作为 AI coding agent 工具实现、权限、沙箱和 CLI 交互研究对象。

### 观察字段

- GitHub URL：https://github.com/openai/codex
- 当前研究方向：`coding-agent-tooling`
- 当前优先级：P1
- 当前归档状态：`false`
- 主要语言：`Rust`
- 最新 release：`rust-v0.153.4`
- 本地源码快照：`raw/repository/`，commit `31ccaf40c2298bb3286c8fe274e1e21c498bb70a`

### 后续观察

- 官方 CLI、Skills、Plugins 和 IDE 入口是否继续保持清晰分层。
- 沙箱、执行策略、MCP、命令入口和可复用工作流是否继续保持稳定。
- 是否能反哺本仓库的[统一功法](../../docs/gongfa/README.md)、[入门练习](../../docs/getting-started/README.md)或[Skills 执行能力](../../skills/README.md)；具体观察仍留在本研究域。
- 是否存在许可证、归档状态、维护活跃度或生态迁移风险。
