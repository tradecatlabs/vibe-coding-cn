# cline/cline 深度研究

## 研究级别

- 当前级别：L2 源码/结构深度研究。
- 研究对象：`cline/cline`。
- 证据来源：本目录 `raw/` 下的 GitHub 元数据、README 快照和本地仓库工作树。
- 观察日期：2026-07-03。

## L2 结论

`cline/cline` 已经不是单一 VS Code 插件，而是向多入口 agent 平台演化的代码库。它同时包含
VS Code 扩展、CLI、hub 服务、SDK、示例应用、规则系统、技能入口、测试平台和发布脚本。

对本仓最重要的启发是：当 AI coding 工具成熟后，产品边界会从“一个插件”扩展为
IDE、CLI、SDK、hooks、规则、技能、示例和测试平台组成的系统。也就是说，agent 能力必须被
平台化和契约化，不能只依赖单个入口。

## 源码证据

- `raw/repository/apps/vscode/src/extension.ts`：VS Code 扩展入口。
- `raw/repository/apps/vscode/webview-ui/`：前端交互界面。
- `raw/repository/apps/cli/src/main.ts`：CLI 入口。
- `raw/repository/apps/cli/src/index.ts`：CLI 对外模块入口。
- `raw/repository/apps/cline-hub/src/server.ts`：hub 服务入口。
- `raw/repository/apps/cline-hub/src/webview-protocol.ts`：webview 协议边界。
- `raw/repository/sdk/ARCHITECTURE.md`：SDK 架构说明。
- `raw/repository/sdk/AGENTS.md`：SDK 目录的 Agent 维护规则。
- `raw/repository/apps/examples/multi-agent/README.md`：多 agent 示例。
- `raw/repository/apps/examples/code-review-bot/README.md`：代码审查机器人示例。
- `raw/repository/.clinerules/general.md`：项目级规则示例。
- `raw/repository/.agents/skills/cline-sdk/SKILL.md`：技能化能力入口。

## 关键机制

### 多入口产品结构

Cline 同时维护 IDE、CLI、hub 和 SDK。这个结构说明 agent 产品的用户入口会多样化：
开发者可能在编辑器里交互，也可能在终端、自动化服务或自定义应用里调用同一套能力。

### SDK 化是生态扩展前提

`sdk/` 和 examples 表明 Cline 不只服务自己的 UI，还希望让外部开发者复用能力。成熟 agent
生态需要 SDK、示例、协议和测试，而不是只暴露一个不可组合的插件。

### 规则、技能和 hooks 承载操作边界

`.clinerules/`、`.agents/skills/` 和相关配置说明，agent 的行为边界需要显式文件承载。
这与本仓的 `AGENTS.md`、`skills/` 和治理文档方向一致。

### 测试平台和发布脚本是产品能力

当 agent 工具跨 IDE、CLI 和 SDK 后，测试与发布不再是附属流程，而是维持平台一致性的必要
控制面。没有测试平台，多入口很快会出现行为漂移。

## 可迁移模式

- 把本仓能力区分为人类阅读入口、AI 上下文入口、脚本入口和 skill 入口。
- 对每个入口说明协议、输入、输出、风险和验证方式。
- 为重要工作流提供 examples，而不是只写抽象原则。
- 把规则文件、skills、hooks、CLI 和文档索引视为同一套 agent 平台的不同表面。
- 长期考虑为本仓沉淀可复用 SDK/CLI 风格的读取与校验工具。

## 对本仓的影响

本仓已经有 `docs/`、`prompts/`、`skills/`、`scripts/`、`metadata/`、`assets/ai-citation/` 等多个入口。
Cline 的结构提醒我们：这些入口不能各自为政，应该用统一契约说明它们如何协同。

当前最值得推进的是：

- `metadata/` 继续作为机器索引事实源。
- `llms.txt` 和 `assets/ai-citation/llms-full.txt` 继续作为 AI 读取入口。
- `scripts/` 继续作为仓库控制面。
- `skills/` 继续作为 Agent 可复用能力层。
- `research/` 继续作为研究对象网络。

## 风险和待验证项

- Cline 代码库较大，且产品线较多；本轮没有验证所有 package 的构建和测试。
- 多入口平台化会带来复杂度，本仓不应为了“看起来平台化”提前增加不必要代码。
- 本仓当前仍以文档知识库为主，迁移时应优先吸收契约和治理模式，而非复制应用结构。

## 下一步 L3 验证任务

- 梳理本仓所有入口：人类入口、AI 入口、脚本入口、skill 入口、资源入口。
- 为每类入口写清输入、输出、owner、验证命令和更新策略。
- 在 `docs/references/` 中沉淀“多入口 agent 仓库结构模板”。
- 用 Cline examples 的思路，为本仓关键工作流增加最小可运行示例。
