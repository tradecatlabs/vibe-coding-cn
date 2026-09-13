# 研究

## 字多不看

- 本目录记录新技术、优秀 repo、工程范式和工具趋势的研究对象。
- 当前包含 36 个外部仓库研究域，另有两个内部工程研究项目、Harness 与 tmux 主题研究对象；外部研究域均保留 raw、analysis 和 deep-dive 证据层。
- 新增或重构长期研究对象时，先遵循研究域治理契约，并拉取 raw 原始事实层。
- 长期研究对象优先使用独立目录，短篇观察可先用单文件承载。
- 外部仓库研究对象采用“一仓库一研究域”，不再使用聚合目录承载多个仓库。
- 成熟后可沉淀到 concepts、references、workflow 或 skills。

## 快速导航

| 文档 | 定位 |
|:---|:---|
| <a id="research-domain-contract"></a>[研究域治理契约](research-domain-contract.md) | 研究域的结构、raw 原始事实层、成熟度、证据、沉淀和归档规则。 |
| <a id="research-value-application-map"></a>[研究价值与应用地图](research-value-application-map.md) | 研究体系给用户带来的价值、核心启示、应用位置和下沉路线。 |
| <a id="research-transfer-synthesis"></a>[研究迁移综合](research-transfer-synthesis.md) | 将对标拆解、改良迭代和杂交创新转成可执行研究路线。 |
| <a id="research-harness-engineering"></a>[Harness 研究对象](harness/) | 工程控制、评估器、反馈闭环与 AI 生成系统可靠性。 |
| <a id="research-walkinglabs-learn-harness-engineering"></a>[walkinglabs/learn-harness-engineering 研究域](walkinglabs-learn-harness-engineering/) | Harness Engineering 课程、模板、Skill 与审计工具。 |
| <a id="research-mindfold-ai-trellis"></a>[mindfold-ai/Trellis 研究域](mindfold-ai-trellis/) | 跨平台 Agent Harness、任务规格与会话记忆系统。 |
| <a id="research-vibe-cybersecurity-cn"></a>[vibe-cybersecurity-cn](vibe-cybersecurity-cn/) | 授权边界内的 Agent 网络安全自动化研究与工程项目。 |
| <a id="research-vibe-harness-cn"></a>[vibe-harness-cn](vibe-harness-cn/) | 治理 Agent Harness 与问题求解算子库的元 Harness 项目。 |
| <a id="research-vibe-mathing-cn-public"></a>[vibemathing/vibe-mathing-cn-public 研究域](vibe-mathing-cn-public/) | 数学研究、证据闭环与可信验证工作台。 |
| <a id="research-tmux-ai-swarm"></a>[tmux 蜂群协作](tmux-ai-swarm.md) | 用 tmux 让多个 AI 终端可感知、可调度、可救援的实验性协作范式。 |
| <a id="research-aider-ai-aider"></a>[Aider-AI/aider 研究域](aider-ai-aider/) | 终端 AI 结对编程工具。 |
| <a id="research-cline-cline"></a>[cline/cline 研究域](cline-cline/) | IDE/SDK/CLI 自主编码 Agent。 |
| <a id="research-hesreallyhim-awesome-claude-code"></a>[hesreallyhim/awesome-claude-code 研究域](hesreallyhim-awesome-claude-code/) | Claude Code 生态索引。 |
| <a id="research-openai-codex"></a>[openai/codex 研究域](openai-codex/) | 官方 coding agent 工具源码。 |
| <a id="research-openai-plugins"></a>[openai/plugins 研究域](openai-plugins/) | Codex 插件、marketplace 与 skill-only plugin 分发。 |
| <a id="research-openai-skills"></a>[openai/skills 研究域](openai-skills/) | 已 deprecated 的 Codex Skills Catalog 与插件迁移参照。 |
| <a id="research-openai-agents-python"></a>[openai/openai-agents-python 研究域](openai-agents-python/) | Agent、工具、handoff、guardrail、session 与 tracing 运行时。 |
| <a id="research-openai-agents-js"></a>[openai/openai-agents-js 研究域](openai-agents-js/) | 官方 TypeScript/JavaScript Agent 运行时。 |
| <a id="research-openai-cookbook"></a>[openai/openai-cookbook 研究域](openai-cookbook/) | OpenAI API、Codex、Agent、评估与安全示例库。 |
| <a id="research-github-spec-kit"></a>[github/spec-kit 研究域](github-spec-kit/) | GitHub 官方规格驱动开发工具包。 |
| <a id="research-fission-ai-openspec"></a>[Fission-AI/OpenSpec 研究域](fission-ai-openspec/) | 面向 AI coding assistant 的规格驱动开发工具。 |
| <a id="research-google-gemini-gemini-cli"></a>[google-gemini/gemini-cli 研究域](google-gemini-gemini-cli/) | 终端 coding agent、MCP、扩展与安全评估。 |
| <a id="research-openhands-openhands"></a>[OpenHands/OpenHands 研究域](openhands-openhands/) | Agent Canvas、工作区、后端与自动化控制中心。 |
| <a id="research-anomalyco-opencode"></a>[anomalyco/opencode 研究域](anomalyco-opencode/) | 模型无关的终端与编辑器 coding agent。 |
| <a id="research-obra-superpowers"></a>[obra/superpowers 研究域](obra-superpowers/) | 跨 coding agent 的技能框架与开发方法论。 |
| <a id="research-addyosmani-agent-skills"></a>[addyosmani/agent-skills 研究域](addyosmani-agent-skills/) | 面向 coding agent 的生命周期技能与质量门禁。 |
| <a id="research-aaif-goose-goose"></a>[aaif-goose/goose 研究域](aaif-goose-goose/) | 跨模型、跨平台的开源 AI Agent。 |
| <a id="research-continuedev-continue"></a>[continuedev/continue 研究域](continuedev-continue/) | 已停止主动维护的 IDE/CLI Agent 历史对标。 |
| <a id="research-swe-agent-mini-swe-agent"></a>[SWE-agent/mini-SWE-agent 研究域](swe-agent-mini-swe-agent/) | 面向 issue 和命令行任务的极简软件工程 Agent。 |
| <a id="research-affaan-m-ecc"></a>[affaan-m/ECC 研究域](affaan-m-ecc/) | 多种 coding agent 的 Harness、技能与质量实践集合。 |
| <a id="research-shanraisshan-claude-code-best-practice"></a>[shanraisshan/claude-code-best-practice 研究域](shanraisshan-claude-code-best-practice/) | Claude Code / Agentic Engineering 最强对标。 |
| <a id="research-tradecatlabs-vibe-coding-cn"></a>[tradecatlabs/vibe-coding-cn 研究域](tradecatlabs-vibe-coding-cn/) | 中文主线工程化工作流。 |
| <a id="research-datawhalechina-easy-vibe"></a>[datawhalechina/easy-vibe 研究域](datawhalechina-easy-vibe/) | 中文分阶段交互式课程。 |
| <a id="research-datawhalechina-vibe-vibe"></a>[datawhalechina/vibe-vibe 研究域](datawhalechina-vibe-vibe/) | 中文零基础系统教程。 |
| <a id="research-filipecalegario-awesome-vibe-coding"></a>[filipecalegario/awesome-vibe-coding 研究域](filipecalegario-awesome-vibe-coding/) | 国际 Vibe Coding 索引。 |
| <a id="research-luzhenqian-ai-coding-lab"></a>[luzhenqian/ai-coding-lab 研究域](luzhenqian-ai-coding-lab/) | AI Coding 项目实验室。 |
| <a id="research-shouzhengai-cs146s-cn"></a>[ShouZhengAI/CS146S_CN 研究域](shouzhengai-cs146s-cn/) | 中文课程与 assignments。 |
| <a id="research-ai-for-developers-awesome-vibe-coding"></a>[ai-for-developers/awesome-vibe-coding 研究域](ai-for-developers-awesome-vibe-coding/) | 精选 Vibe Coding 资料清单。 |
| <a id="research-daotin-ai-coding"></a>[Daotin/ai-coding 研究域](daotin-ai-coding/) | AI Coding 经验汇总。 |
| <a id="research-earyantle-vibe-coding-skill"></a>[earyantLe/vibe-coding-skill 研究域](earyantle-vibe-coding-skill/) | Vibe Coding Skill / SOP 化。 |
| <a id="research-liyupi-ai-guide"></a>[liyupi/ai-guide 研究域](liyupi-ai-guide/) | AI 资源大全与产品实用路线。 |
| <a id="research-roocodeinc-roo-code"></a>[RooCodeInc/Roo-Code 研究域](roocodeinc-roo-code/) | 已归档多 Agent 编辑器工具；当前已归档，仅作参考。 |
| <a id="research-wendy7756-vibe-coding-guide"></a>[wendy7756/vibe-coding-guide 研究域](wendy7756-vibe-coding-guide/) | 非程序员自然语言编程指南。 |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

### 细粒度目录

- [研究域治理契约](research-domain-contract.md) - 研究域的结构、raw 原始事实层、成熟度、证据、沉淀和归档规则。
- [研究价值与应用地图](research-value-application-map.md) - 研究体系给用户带来的价值、核心启示、应用位置和下沉路线。
- [研究迁移综合](research-transfer-synthesis.md) - 将对标拆解、改良迭代和杂交创新转成可执行研究路线。
- [Harness 研究对象](harness/README.md) - 工程控制、评估器、反馈闭环与 AI 生成系统可靠性。
- [Harness 工程解析](harness/harness-engineering.md) - Harness Engineering 的工程控制、评估器与反馈闭环解析。
- [walkinglabs/learn-harness-engineering 研究域](walkinglabs-learn-harness-engineering/README.md) - Harness Engineering 课程、模板、Skill 与审计工具。
- [walkinglabs/learn-harness-engineering 研究分析](walkinglabs-learn-harness-engineering/analysis.md) - Harness 课程、控制面和验证闭环的结构化研究。
- [walkinglabs/learn-harness-engineering 深度研究](walkinglabs-learn-harness-engineering/deep-dive.md) - Harness 结构、工具链和可迁移机制的 L2 研究。
- [mindfold-ai/Trellis 研究域](mindfold-ai-trellis/README.md) - 跨平台 Agent Harness、任务规格与会话记忆系统。
- [mindfold-ai/Trellis 研究分析](mindfold-ai-trellis/analysis.md) - 任务控制面、规格注入和多平台适配的结构化研究。
- [mindfold-ai/Trellis 深度研究](mindfold-ai-trellis/deep-dive.md) - Harness 架构、CLI 和记忆系统的 L2 研究。
- [vibe-cybersecurity-cn](vibe-cybersecurity-cn/README.md) - 授权边界内的 Agent 网络安全自动化研究与工程项目。
- [vibe-harness-cn](vibe-harness-cn/README.md) - 治理 Agent Harness 与问题求解算子库的元 Harness 项目。
- [vibemathing/vibe-mathing-cn-public 研究域](vibe-mathing-cn-public/README.md) - 数学研究、证据闭环与可信验证工作台。
- [vibemathing/vibe-mathing-cn-public 研究分析](vibe-mathing-cn-public/analysis.md) - 数学研究工作流、迁移价值和采用边界的结构化研究。
- [vibemathing/vibe-mathing-cn-public 深度研究](vibe-mathing-cn-public/deep-dive.md) - 证据闭环、有界运行时和公共边界的 L2 研究。
- [tmux 蜂群协作](tmux-ai-swarm.md) - 用 tmux 让多个 AI 终端可感知、可调度、可救援的实验性协作范式。
- [Aider-AI/aider 研究域](aider-ai-aider/README.md) - 终端 AI 结对编程工具。
- [Aider-AI/aider 研究分析](aider-ai-aider/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [Aider-AI/aider 深度研究](aider-ai-aider/deep-dive.md) - L2 源码/结构深度研究、关键机制和可迁移模式。
- [cline/cline 研究域](cline-cline/README.md) - IDE/SDK/CLI 自主编码 Agent。
- [cline/cline 研究分析](cline-cline/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [cline/cline 深度研究](cline-cline/deep-dive.md) - L2 源码/结构深度研究、关键机制和可迁移模式。
- [hesreallyhim/awesome-claude-code 研究域](hesreallyhim-awesome-claude-code/README.md) - Claude Code 生态索引。
- [hesreallyhim/awesome-claude-code 研究分析](hesreallyhim-awesome-claude-code/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [hesreallyhim/awesome-claude-code 深度研究](hesreallyhim-awesome-claude-code/deep-dive.md) - L2 源码/结构深度研究、关键机制和可迁移模式。
- [openai/codex 研究域](openai-codex/README.md) - 官方 coding agent 工具源码。
- [openai/codex 研究分析](openai-codex/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [openai/codex 深度研究](openai-codex/deep-dive.md) - L2 源码/结构深度研究、关键机制和可迁移模式。
- [openai/plugins 研究域](openai-plugins/README.md) - Codex 插件、marketplace 与 skill-only plugin 分发。
- [openai/plugins 研究分析](openai-plugins/analysis.md) - 插件能力包、发现和权限边界的结构化研究。
- [openai/plugins 深度研究](openai-plugins/deep-dive.md) - manifest、marketplace 和验证资产的 L2 研究。
- [openai/skills 研究域](openai-skills/README.md) - 已 deprecated 的 Codex Skills Catalog 与插件迁移参照。
- [openai/skills 研究分析](openai-skills/analysis.md) - 技能目录生命周期和迁移边界的结构化研究。
- [openai/skills 深度研究](openai-skills/deep-dive.md) - 技能目录、能力包和渐进加载的 L2 研究。
- [openai/openai-agents-python 研究域](openai-agents-python/README.md) - Agent 运行时与多 Agent 工作流编排。
- [openai/openai-agents-python 研究分析](openai-agents-python/analysis.md) - Agent、工具、护栏和追踪的结构化研究。
- [openai/openai-agents-python 深度研究](openai-agents-python/deep-dive.md) - SDK 运行时对象与验证机制的 L2 研究。
- [openai/openai-agents-js 研究域](openai-agents-js/README.md) - 官方 TypeScript/JavaScript Agent 运行时。
- [openai/openai-agents-js 研究分析](openai-agents-js/analysis.md) - TypeScript Agent 运行时的结构化研究。
- [openai/openai-agents-js 深度研究](openai-agents-js/deep-dive.md) - SDK 包结构、sandbox 与验证机制的 L2 研究。
- [openai/openai-cookbook 研究域](openai-cookbook/README.md) - OpenAI API、Codex、Agent、评估与安全示例库。
- [openai/openai-cookbook 研究分析](openai-cookbook/analysis.md) - 官方示例、登记表和可复现产物的结构化研究。
- [openai/openai-cookbook 深度研究](openai-cookbook/deep-dive.md) - registry、Codex 示例、Agent 示例与风险边界的 L2 研究。
- [github/spec-kit 研究域](github-spec-kit/README.md) - GitHub 官方规格驱动开发工具包。
- [github/spec-kit 研究分析](github-spec-kit/analysis.md) - 规格驱动流程和测试分层的结构化研究。
- [github/spec-kit 深度研究](github-spec-kit/deep-dive.md) - `.specify`、命令模板、扩展和测试结构的 L2 研究。
- [Fission-AI/OpenSpec 研究域](fission-ai-openspec/README.md) - 面向 AI coding assistant 的规格驱动开发工具。
- [Fission-AI/OpenSpec 研究分析](fission-ai-openspec/analysis.md) - 变更提案、规格资产和 CLI/Skill 边界的结构化研究。
- [Fission-AI/OpenSpec 深度研究](fission-ai-openspec/deep-dive.md) - changes、specs、schema、skills 与命令的 L2 研究。
- [google-gemini/gemini-cli 研究域](google-gemini-gemini-cli/README.md) - 终端 coding agent、MCP 和扩展。
- [google-gemini/gemini-cli 研究分析](google-gemini-gemini-cli/analysis.md) - 上下文、工具、权限和安全评估的结构化研究。
- [google-gemini/gemini-cli 深度研究](google-gemini-gemini-cli/deep-dive.md) - CLI、扩展、checkpoint 和负例评估的 L2 研究。
- [OpenHands/OpenHands 研究域](openhands-openhands/README.md) - Agent Canvas、工作区和后端控制中心。
- [OpenHands/OpenHands 研究分析](openhands-openhands/analysis.md) - Agent 编排、工作区和自动化的结构化研究。
- [OpenHands/OpenHands 深度研究](openhands-openhands/deep-dive.md) - Agent Server、适配层和状态边界的 L2 研究。
- [anomalyco/opencode 研究域](anomalyco-opencode/README.md) - 模型无关的终端与编辑器 coding agent。
- [anomalyco/opencode 研究分析](anomalyco-opencode/analysis.md) - provider、权限、插件和配置生命周期的结构化研究。
- [anomalyco/opencode 深度研究](anomalyco-opencode/deep-dive.md) - plan/build、策略、插件 reload 和 v2 spec 的 L2 研究。
- [obra/superpowers 研究域](obra-superpowers/README.md) - 跨 coding agent 的技能框架与开发方法论。
- [obra/superpowers 研究分析](obra-superpowers/analysis.md) - 技能触发、TDD、审查和插件分发的结构化研究。
- [obra/superpowers 深度研究](obra-superpowers/deep-dive.md) - 技能组合、阶段门禁和跨 harness 分发的 L2 研究。
- [addyosmani/agent-skills 研究域](addyosmani-agent-skills/README.md) - 面向 coding agent 的生命周期技能与质量门禁。
- [addyosmani/agent-skills 研究分析](addyosmani-agent-skills/analysis.md) - 生命周期命令、上下文层级和技能评估的结构化研究。
- [addyosmani/agent-skills 深度研究](addyosmani-agent-skills/deep-dive.md) - commands、skills、references 和 evals 的 L2 研究。
- [aaif-goose/goose 研究域](aaif-goose-goose/README.md) - 跨模型、跨平台的开源 AI Agent。
- [aaif-goose/goose 研究分析](aaif-goose-goose/analysis.md) - provider、MCP、工作区和评估资产的结构化研究。
- [aaif-goose/goose 深度研究](aaif-goose-goose/deep-dive.md) - Rust workspace、上下文管理和 workflow recipe 的 L2 研究。
- [continuedev/continue 研究域](continuedev-continue/README.md) - 已停止主动维护的 IDE/CLI Agent 历史对标。
- [continuedev/continue 研究分析](continuedev-continue/analysis.md) - 只读生命周期、上下文分层和迁移边界的结构化研究。
- [continuedev/continue 深度研究](continuedev-continue/deep-dive.md) - IDE/CLI、配置、上下文和生命周期的 L2 研究。
- [SWE-agent/mini-SWE-agent 研究域](swe-agent-mini-swe-agent/README.md) - 面向 issue 和命令行任务的极简软件工程 Agent。
- [SWE-agent/mini-SWE-agent 研究分析](swe-agent-mini-swe-agent/analysis.md) - 极简工具面、有界执行和问题修复闭环研究。
- [SWE-agent/mini-SWE-agent 深度研究](swe-agent-mini-swe-agent/deep-dive.md) - Bash 工具、轨迹、环境适配和评估边界的 L2 研究。
- [affaan-m/ECC 研究域](affaan-m-ecc/README.md) - 多种 coding agent 的 Harness、技能与质量实践集合。
- [affaan-m/ECC 研究分析](affaan-m-ecc/analysis.md) - Harness、记忆、安全和技能治理的结构化研究。
- [affaan-m/ECC 深度研究](affaan-m-ecc/deep-dive.md) - `.codex`、manifests、hooks 和评估技能的 L2 研究。
- [shanraisshan/claude-code-best-practice 研究域](shanraisshan-claude-code-best-practice/README.md) - Claude Code / Agentic Engineering 最强对标。
- [shanraisshan/claude-code-best-practice 研究分析](shanraisshan-claude-code-best-practice/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [shanraisshan/claude-code-best-practice 深度研究](shanraisshan-claude-code-best-practice/deep-dive.md) - L2 源码/结构深度研究、关键机制和可迁移模式。
- [tradecatlabs/vibe-coding-cn 研究域](tradecatlabs-vibe-coding-cn/README.md) - 中文主线工程化工作流。
- [tradecatlabs/vibe-coding-cn 研究分析](tradecatlabs-vibe-coding-cn/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [tradecatlabs/vibe-coding-cn 深度研究](tradecatlabs-vibe-coding-cn/deep-dive.md) - L2 源码/结构深度研究、关键机制和可迁移模式。
- [datawhalechina/easy-vibe 研究域](datawhalechina-easy-vibe/README.md) - 中文分阶段交互式课程。
- [datawhalechina/easy-vibe 研究分析](datawhalechina-easy-vibe/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [datawhalechina/easy-vibe 深度研究](datawhalechina-easy-vibe/deep-dive.md) - L2 源码/结构深度研究、关键机制和可迁移模式。
- [datawhalechina/vibe-vibe 研究域](datawhalechina-vibe-vibe/README.md) - 中文零基础系统教程。
- [datawhalechina/vibe-vibe 研究分析](datawhalechina-vibe-vibe/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [datawhalechina/vibe-vibe 深度研究](datawhalechina-vibe-vibe/deep-dive.md) - L2 源码/结构深度研究、关键机制和可迁移模式。
- [filipecalegario/awesome-vibe-coding 研究域](filipecalegario-awesome-vibe-coding/README.md) - 国际 Vibe Coding 索引。
- [filipecalegario/awesome-vibe-coding 研究分析](filipecalegario-awesome-vibe-coding/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [filipecalegario/awesome-vibe-coding 深度研究](filipecalegario-awesome-vibe-coding/deep-dive.md) - L2 源码/结构深度研究、关键机制和可迁移模式。
- [luzhenqian/ai-coding-lab 研究域](luzhenqian-ai-coding-lab/README.md) - AI Coding 项目实验室。
- [luzhenqian/ai-coding-lab 研究分析](luzhenqian-ai-coding-lab/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [luzhenqian/ai-coding-lab 深度研究](luzhenqian-ai-coding-lab/deep-dive.md) - L2 源码/结构深度研究、关键机制和可迁移模式。
- [ShouZhengAI/CS146S_CN 研究域](shouzhengai-cs146s-cn/README.md) - 中文课程与 assignments。
- [ShouZhengAI/CS146S_CN 研究分析](shouzhengai-cs146s-cn/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [ShouZhengAI/CS146S_CN 深度研究](shouzhengai-cs146s-cn/deep-dive.md) - L2 源码/结构深度研究、关键机制和可迁移模式。
- [ai-for-developers/awesome-vibe-coding 研究域](ai-for-developers-awesome-vibe-coding/README.md) - 精选 Vibe Coding 资料清单。
- [ai-for-developers/awesome-vibe-coding 研究分析](ai-for-developers-awesome-vibe-coding/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [ai-for-developers/awesome-vibe-coding 深度研究](ai-for-developers-awesome-vibe-coding/deep-dive.md) - L2 结构深度研究、关键机制、迁移边界和验证任务。
- [Daotin/ai-coding 研究域](daotin-ai-coding/README.md) - AI Coding 经验汇总。
- [Daotin/ai-coding 研究分析](daotin-ai-coding/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [Daotin/ai-coding 深度研究](daotin-ai-coding/deep-dive.md) - L2 结构深度研究、关键机制、迁移边界和验证任务。
- [earyantLe/vibe-coding-skill 研究域](earyantle-vibe-coding-skill/README.md) - Vibe Coding Skill / SOP 化。
- [earyantLe/vibe-coding-skill 研究分析](earyantle-vibe-coding-skill/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [earyantLe/vibe-coding-skill 深度研究](earyantle-vibe-coding-skill/deep-dive.md) - L2 结构深度研究、关键机制、迁移边界和验证任务。
- [liyupi/ai-guide 研究域](liyupi-ai-guide/README.md) - AI 资源大全与产品实用路线。
- [liyupi/ai-guide 研究分析](liyupi-ai-guide/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [liyupi/ai-guide 深度研究](liyupi-ai-guide/deep-dive.md) - L2 结构深度研究、关键机制、迁移边界和验证任务。
- [RooCodeInc/Roo-Code 研究域](roocodeinc-roo-code/README.md) - 已归档多 Agent 编辑器工具；当前已归档，仅作参考。
- [RooCodeInc/Roo-Code 研究分析](roocodeinc-roo-code/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [RooCodeInc/Roo-Code 深度研究](roocodeinc-roo-code/deep-dive.md) - L2 结构深度研究、关键机制、迁移边界和验证任务。
- [wendy7756/vibe-coding-guide 研究域](wendy7756-vibe-coding-guide/README.md) - 非程序员自然语言编程指南。
- [wendy7756/vibe-coding-guide 研究分析](wendy7756-vibe-coding-guide/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [wendy7756/vibe-coding-guide 深度研究](wendy7756-vibe-coding-guide/deep-dive.md) - L2 结构深度研究、关键机制、迁移边界和验证任务。

</details>

## 使用方式

- 评估新技术、优秀 repo 或工程范式时，先写 research。
- 新增长期研究对象前，先按研究域治理契约判断它是否应该成为独立研究域，并用 `scripts/fetch-research-raw.py` 拉取原始材料。
- 外部仓库默认一仓库一研究域；横向比较只能放在索引或单独对比文档中。
- 对象会持续演化时，优先放入独立对象目录。
- 确认成熟后，再迁入更稳定的概念、参考或技能文档。

## 正文

正文已拆分到上方独立文档；本 README 只保留索引、旧锚点兼容入口和阅读顺序。
