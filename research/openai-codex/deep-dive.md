# openai/codex 深度研究

## 研究级别

- 当前级别：L2 源码/结构深度研究。
- 研究对象：`openai/codex`。
- 证据来源：本目录 `raw/` 下的 GitHub 元数据、README 快照和本地仓库工作树。
- 观察日期：2026-07-03。

## L2 结论

`openai/codex` 不是简单的 CLI 包，而是一个以 Rust 工作区为核心的 coding agent
控制面。它把协议、配置、沙箱、工具、提示词、技能、TUI、CLI 包装和 MCP 服务拆成相对清晰的
边界，说明成熟 coding agent 的核心不是“会调用模型”，而是把模型能力放进可配置、可审计、
可限制、可交互的执行系统里。

对本仓最有价值的不是复制实现，而是学习它的边界设计：执行策略、沙箱策略、Agent 指令、
技能、配置和交互文档都被显式建模，避免把高风险行为藏在零散脚本或提示词里。

## 源码证据

- `raw/repository/codex-rs/protocol/`：协议层，说明 agent 运行时需要稳定消息边界。
- `raw/repository/codex-rs/config/`：配置层，承载运行参数、模型和权限相关配置。
- `raw/repository/codex-rs/sandboxing/`：跨平台沙箱抽象，说明执行权限是核心产品能力。
- `raw/repository/codex-rs/linux-sandbox/`：Linux 沙箱实现，说明本地命令执行必须有边界。
- `raw/repository/codex-rs/tools/`：工具层，说明 agent 能力通过显式工具接口接入。
- `raw/repository/codex-rs/skills/`：技能层，说明可复用操作经验被工程化为独立对象。
- `raw/repository/codex-rs/tui/`：终端交互层，承载人机协作的主要用户界面。
- `raw/repository/codex-cli/bin/codex.js`：npm 分发入口，本质上是对核心运行时的包装。
- `raw/repository/docs/exec.md`：命令执行文档，说明执行行为需要公开契约。
- `raw/repository/docs/execpolicy.md`：执行策略文档，说明权限策略需要独立表达。
- `raw/repository/docs/sandbox.md`：沙箱文档，说明安全边界不是实现细节。
- `raw/repository/docs/agents_md.md`：Agent 指令文档，说明项目级上下文是正式接口。
- `raw/repository/docs/skills.md`：技能文档，说明技能不是杂项 prompt，而是可治理能力单元。

## 关键机制

### 协议优先

Codex 将 agent 运行时拆成协议、客户端、服务和界面等层次。这个结构把“模型说了什么”与
“系统如何执行”分开，降低了 CLI、TUI、MCP 和未来其他入口之间互相污染的概率。

### 沙箱和审批是核心对象

本地 agent 的最大风险来自命令执行、文件写入、网络访问和外部工具调用。Codex 把 sandbox、
exec policy 和配置作为显式层，而不是把风险控制埋进一段提示词。这是企业级 agent 的底线：
风险必须是系统能力，不是靠模型自觉。

### 文档就是运行契约

`docs/exec.md`、`docs/execpolicy.md`、`docs/sandbox.md`、`docs/agents_md.md` 和
`docs/skills.md` 共同构成运行契约。它们不是营销文档，而是告诉使用者和贡献者：
哪些行为可执行，哪些行为受限，哪些上下文会被读取，技能如何介入系统。

### 分发壳和核心运行时分离

`codex-cli/` 更像分发入口，核心复杂度集中在 `codex-rs/`。这种结构适合长期维护：
包管理、安装体验和跨平台入口可以变化，但 agent 核心边界保持稳定。

## 可迁移模式

- 把 agent 执行相关内容分成 `config`、`sandbox`、`exec policy`、`tools`、`skills` 和
  `agent context` 六类，不混在一个 README 或提示词里。
- 对任何会执行命令、改文件或访问网络的脚本，增加风险等级、dry-run、审批策略和审计说明。
- 将 `AGENTS.md` 视为项目级上下文接口，而不是临时提示词。
- 将 skills 视为可复用能力单元，要求有触发条件、边界、输入输出和验证方式。
- 对本仓 `scripts/`、`skills/`、`research/` 建立类似的控制面文档。

## 对本仓的影响

本仓已经有 `AGENTS.md`、`skills/`、`scripts/`、`research/` 和 raw 事实层，下一步应把这些
对象之间的运行关系写得更明确：

- `scripts/` 是仓库控制面，不是杂物间。
- `skills/` 是 Agent 可复用能力层，不是提示词收藏夹。
- `research/` 是研究对象网络，不是外链列表。
- `AGENTS.md` 是 AI 协作的项目级接口，不是单纯贡献指南。

## 风险和待验证项

- Codex 是官方产品仓库，行为可能随版本快速变化；动态事实必须以 `domain.yml` 观测日为准。
- 本地源码只能说明公开实现和文档，不能完整代表云端模型、服务端策略或私有运行逻辑。
- 本轮没有运行 Codex 自身测试，结论只覆盖结构研究，不覆盖性能、稳定性或真实使用体验。

## 下一步 L3 验证任务

- 把本仓 `scripts/` 的风险分级和可执行入口整理成 `manifest.yml` 或等价登记表。
- 为高风险脚本补齐 dry-run、输入输出、owner、CI 状态和审计说明。
- 从 Codex 的 `exec policy` 和 `sandbox` 文档中抽象本仓可用的脚本治理检查清单。
- 在 `docs/references/` 沉淀“coding agent 控制面”模板，避免研究结论长期滞留在 research。
