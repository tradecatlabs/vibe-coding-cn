# 知识库总索引

## 字多不看

- 新手先读 `getting-started/`，按 Vibe Coding 经验、学习地图、网络环境、CLI 配置和开发环境推进。
- 想理解 Vibe Coding 的底层概念，读 `concepts/`。
- 想补思维模型、软件工程常识和方法论，读 `philosophy/`。
- 想查工程模板、质量门禁、技术栈和常见坑，读 `references/`。
- 想记录新技术、优秀 repo 或工程趋势，读根目录 `research/`。
- 想按标准流程推进任务、提交和推送，读 `workflow/`。

## 快速导航

| 目录 | 定位 | 首选入口 |
|:---|:---|:---|
| [getting-started](./getting-started/) | 从零开始的入门教程 | [Vibe Coding 经验](./getting-started/vibe-coding-experience.md) / [学习地图](./getting-started/learning-map.md) |
| [concepts](./concepts/) | 核心概念、问题求解、关键词系统与工程思想 | [问题求解](./concepts/problem-solving.md) / [拼好码](./concepts/glue-coding.md) / [关键词系统](./concepts/keyword-system.md) |
| [philosophy](./philosophy/) | 哲学方法论、思维模型与底层认知模型 | [思维模型](./philosophy/thinking-models.md) / [方法论工具箱](./philosophy/methodology-toolbox.md) |
| [references](./references/) | 工程实践、技术栈、模板和检查清单 | [项目架构模板](./references/project-architecture-template.md) / [质量门禁](./references/quality-gates-and-pitfalls.md) |
| [research](../research/) | 根级研究域：新技术、优秀 repo 与工程范式研究 | [研究域治理契约](../research/research-domain-contract.md) / [研究迁移综合](../research/research-transfer-synthesis.md) |
| [workflow](./workflow/) | 开发流程、质量门禁和交付闭环 | [开发流程](./workflow/development-process.md) |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

### 全部文档索引

### getting-started

- [README](./getting-started/README.md) - 从零开始索引。
- [Vibe Coding 经验](./getting-started/vibe-coding-experience.md) - 通用语言能力、人机分工、机器门禁和入门铁律。
- [学习地图](./getting-started/learning-map.md) - 新手、开发者、团队、Prompt、Skill、质量门禁和 GEO/SEO 的路线选择。
- [网络环境配置](./getting-started/network-environment.md) - OpenAI、GitHub、文档和依赖源访问。
- [CLI 配置](./getting-started/cli-setup.md) - Codex CLI 默认路线与 OpenCode 备选路线。
- [开发环境搭建](./getting-started/development-environment.md) - 让 Agent 主动配置开发依赖、编辑器建议和测试命令。
- [AGENTS](./getting-started/AGENTS.md) - 入门教程目录操作规则。

### concepts

- [README](./concepts/README.md) - 核心概念索引。
- [问题求解](./concepts/problem-solving.md) - 用目标、现状、差距、标准、约束、对象和路径定义问题。
- [拼好码](./concepts/glue-coding.md) - 复用成熟能力，用胶水代码连接、编排、适配业务流程。
- [系统构建方法](./concepts/system-building.md) - 自顶向下、自底向上与分而治之的组合使用。
- [开发范式演进](./concepts/development-paradigms.md) - 软件工程组织方式的演进。
- [语言层要素](./concepts/language-layers.md) - 看懂代码所需的语言层要素。
- [关键词系统](./concepts/keyword-system.md) - Vibe Coding 与工程协作中的高频关键词。
- [递归自优化系统](./concepts/recursive-self-optimizing-system.md) - 递归自优化生成系统的形式化模型。
- [AGENTS](./concepts/AGENTS.md) - 核心概念目录操作规则。

### philosophy

- [README](./philosophy/README.md) - 哲学方法论索引。
- [思维模型](./philosophy/thinking-models.md) - 可复用思维模型索引。
- [组合描述模型](./philosophy/compositional-description-model.md) - 用对象、状态、快照、序列、过程、变换、同一/差异与关系描述复杂系统。
- [编程之道](./philosophy/programming-dao.md) - 编程哲学与工程判断。
- [软件工程的朴素真理](./philosophy/software-engineering-truths.md) - 代码、复杂度、需求、维护、质量、架构和团队的工程常识。
- [方法论工具箱](./philosophy/methodology-toolbox.md) - 现象学还原、正反合、可证伪主义、形式化方法等提效工具。
- [AGENTS](./philosophy/AGENTS.md) - 哲学方法论目录操作规则。

### references

- [README](./references/README.md) - 参考资料索引。
- [项目架构模板](./references/project-architecture-template.md) - 常见项目结构、架构设计原则、最低门禁和检查清单。
- [通用 Python 项目骨架](./references/python-project-skeleton.md) - Python 应用、服务、脚本工具和库项目的通用骨架。
- [企业级架构模板](./references/enterprise-architecture-template.md) - 中大型工程组织、平台工程和多产品线参考模型。
- [现代企业数字化平台架构](./references/modern-enterprise-architecture-template.md) - 面向领域产品网络、微服务容器 GitOps 边界、AI 原生能力、微调治理、AI 事件响应、内部平台、数据产品、供应链安全、FinOps 成本治理、版本治理、版本控制面、基线版本策略、发布通道、兼容性与冻结控制总账、基线生产变更、发布编排、变更冲突与失败恢复总账、基线事故、问题、纠正行动与复发防止总账、基线数据产品质量、契约违约、运行血缘与可观测性总账、基线工程质量、测试证据、缺陷与发布验证总账、基线人员能力、培训、职责履职与职责分离总账、基线业务结果、价值实现与组合收益总账、基线价值流、关键旅程与端到端流程总账、基线架构视图、运行拓扑与依赖影响总账、基线质量属性、架构驱动与权衡决策总账、基线架构原则、约束、反模式与例外执行总账、基线安全配置、加固姿态与配置漂移修复总账、基线漏洞、暴露面与修复验证总账、基线威胁建模、攻击面与安全风险总账、基线容量、性能、弹性伸缩与成本效率总账、基线服务可靠性、SLO、错误预算与可观测性总账、基线备份、恢复、灾备与可恢复性验证总账、基线密码材料、密钥、证书与秘密生命周期总账、基线资产关键性、数据分类与风险分级总账、基线身份权限、特权访问与工作负载身份总账、基线处理活动、个人数据清单与 RoPA 覆盖总账、基线隐私权利请求、同意偏好与合法基础执行总账、基线记录留存、法律保全与可防御删除总账、基线监管与合规义务可追溯总账、基线运营韧性与重要业务服务影响容忍总账、基线第三方与关键供应商风险总账、基线数据驻留与跨境处理总账、基线共享责任与继承控制总账、基线独立控制保证抽样总账、基线连续控制监测总账、基线运行时准入决策总账、基线运行时准入回执、基线长期验签回执、基线证据不可变归档回执、干净环境基线重建回执、私有制品托管交接清单、审计导出排除清单、本地私有制品边界、基线迁移执行回执、基线迁移工作单、基线消费锁定文件、基线准入执行策略、基线撤销与隔离记录、基线发布事务回执、基线门禁执行报告、基线证据追踪图、基线会审裁决记录、基线 EOL 退役证书、基线状态对账报告、基线生命周期状态机、基线就绪评分卡、基线例外总账、基线回滚验证记录、基线通知确认总账、基线验证环境锁定、基线制品清单、基线发布证据、基线兼容性总账、基线采纳总账、基线支持矩阵、基线发布列车、基线符合性声明、外部标准版本锁定、可执行标准、执行控制面、门禁决策、RACI 决策权、可靠性分级、仓库拓扑、迁移弃用、审计证据、联邦治理和行业对标矩阵的完整说明文档。
- [常识](./references/common-sense.md) - AI 编程和工程交付前的最低判断线。
- [Dataset First 数据服务](./references/dataset-first-data-service.md) - 数据服务模板。
- [代码组织](./references/code-organization.md) - 模块化、命名、注释、格式化、文档和工具。
- [开发经验](./references/development-experience.md) - 编码规范、架构原则和常见基础设施经验。
- [AI 编程质量门禁与常见坑](./references/quality-gates-and-pitfalls.md) - 系统提示词、强前置条件、常见坑和硬门禁。
- [底层程序逻辑设计与工程优化项](./references/low-level-program-logic.md) - 运行模型、并发模型、数据模型、性能模型和工程交付检查清单。
- [技术栈](./references/technology-stack.md) - 技术栈选型、组合案例与初学者学习路径。
- [AGENTS](./references/AGENTS.md) - 参考资料目录操作规则。

### research

- [README](../research/README.md) - 研究笔记索引。
- [研究域治理契约](../research/research-domain-contract.md) - 研究域的结构、raw 原始事实层、成熟度、证据、沉淀和归档规则。
- [研究价值与应用地图](../research/research-value-application-map.md) - 研究体系给用户带来的价值、核心启示、应用位置和下沉路线。
- [研究迁移综合](../research/research-transfer-synthesis.md) - 将对标拆解、改良迭代和杂交创新转成可执行研究路线。
- [Harness 研究对象](../research/harness/README.md) - Harness Engineering 的工程控制、评估器与反馈闭环研究对象。
- [Harness 工程解析](../research/harness/harness-engineering.md) - Harness Engineering 的工程控制、评估器与反馈闭环解析。
- [walkinglabs/learn-harness-engineering 研究域](../research/walkinglabs-learn-harness-engineering/README.md) - Harness Engineering 课程、模板、Skill 与审计工具。
- [mindfold-ai/Trellis 研究域](../research/mindfold-ai-trellis/README.md) - 跨平台 Agent Harness、任务规格与会话记忆系统。
- [外部源事实层](../research/facts/README.md) - 三个外部仓库的已提交源文件树、提交事实、哈希和隐私边界。
- [tmux 蜂群协作](../research/tmux-ai-swarm.md) - 用 tmux 让多个 AI 终端可感知、可调度、可救援的实验性协作范式。
- [Aider-AI/aider 研究域](../research/aider-ai-aider/README.md) - 终端 AI 结对编程工具。
- [Aider-AI/aider 研究分析](../research/aider-ai-aider/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [Aider-AI/aider 深度研究](../research/aider-ai-aider/deep-dive.md) - L2 源码/结构深度研究、关键机制和可迁移模式。
- [cline/cline 研究域](../research/cline-cline/README.md) - IDE/SDK/CLI 自主编码 Agent。
- [cline/cline 研究分析](../research/cline-cline/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [cline/cline 深度研究](../research/cline-cline/deep-dive.md) - L2 源码/结构深度研究、关键机制和可迁移模式。
- [hesreallyhim/awesome-claude-code 研究域](../research/hesreallyhim-awesome-claude-code/README.md) - Claude Code 生态索引。
- [hesreallyhim/awesome-claude-code 研究分析](../research/hesreallyhim-awesome-claude-code/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [hesreallyhim/awesome-claude-code 深度研究](../research/hesreallyhim-awesome-claude-code/deep-dive.md) - L2 源码/结构深度研究、关键机制和可迁移模式。
- [openai/codex 研究域](../research/openai-codex/README.md) - 官方 coding agent 工具源码。
- [openai/codex 研究分析](../research/openai-codex/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [openai/codex 深度研究](../research/openai-codex/deep-dive.md) - L2 源码/结构深度研究、关键机制和可迁移模式。
- [openai/plugins 研究域](../research/openai-plugins/README.md) - Codex 插件、marketplace 与 skill-only plugin 分发。
- [openai/plugins 研究分析](../research/openai-plugins/analysis.md) - 插件能力包、发现和权限边界的结构化研究。
- [openai/plugins 深度研究](../research/openai-plugins/deep-dive.md) - manifest、marketplace 和验证资产的 L2 研究。
- [openai/skills 研究域](../research/openai-skills/README.md) - 已 deprecated 的 Codex Skills Catalog 与插件迁移参照。
- [openai/skills 研究分析](../research/openai-skills/analysis.md) - 技能目录生命周期和迁移边界的结构化研究。
- [openai/skills 深度研究](../research/openai-skills/deep-dive.md) - 技能目录、能力包和渐进加载的 L2 研究。
- [openai/openai-agents-python 研究域](../research/openai-agents-python/README.md) - Agent 运行时与多 Agent 工作流编排。
- [openai/openai-agents-python 研究分析](../research/openai-agents-python/analysis.md) - Agent、工具、护栏和追踪的结构化研究。
- [openai/openai-agents-python 深度研究](../research/openai-agents-python/deep-dive.md) - SDK 运行时对象与验证机制的 L2 研究。
- [openai/openai-agents-js 研究域](../research/openai-agents-js/README.md) - 官方 TypeScript/JavaScript Agent 运行时。
- [openai/openai-agents-js 研究分析](../research/openai-agents-js/analysis.md) - TypeScript Agent 运行时的结构化研究。
- [openai/openai-agents-js 深度研究](../research/openai-agents-js/deep-dive.md) - SDK 包结构、sandbox 与验证机制的 L2 研究。
- [openai/openai-cookbook 研究域](../research/openai-cookbook/README.md) - OpenAI API、Codex、Agent、评估与安全示例库。
- [openai/openai-cookbook 研究分析](../research/openai-cookbook/analysis.md) - 官方示例、登记表和可复现产物的结构化研究。
- [openai/openai-cookbook 深度研究](../research/openai-cookbook/deep-dive.md) - registry、Codex 示例、Agent 示例与风险边界的 L2 研究。
- [github/spec-kit 研究域](../research/github-spec-kit/README.md) - GitHub 官方规格驱动开发工具包。
- [github/spec-kit 研究分析](../research/github-spec-kit/analysis.md) - 规格驱动流程和测试分层的结构化研究。
- [github/spec-kit 深度研究](../research/github-spec-kit/deep-dive.md) - `.specify`、命令模板、扩展和测试结构的 L2 研究。
- [Fission-AI/OpenSpec 研究域](../research/fission-ai-openspec/README.md) - 面向 AI coding assistant 的规格驱动开发工具。
- [Fission-AI/OpenSpec 研究分析](../research/fission-ai-openspec/analysis.md) - 变更提案、规格资产和 CLI/Skill 边界的结构化研究。
- [Fission-AI/OpenSpec 深度研究](../research/fission-ai-openspec/deep-dive.md) - changes、specs、schema、skills 与命令的 L2 研究。
- [google-gemini/gemini-cli 研究域](../research/google-gemini-gemini-cli/README.md) - 终端 coding agent、MCP 和扩展。
- [google-gemini/gemini-cli 研究分析](../research/google-gemini-gemini-cli/analysis.md) - 上下文、工具、权限和安全评估的结构化研究。
- [google-gemini/gemini-cli 深度研究](../research/google-gemini-gemini-cli/deep-dive.md) - CLI、扩展、checkpoint 和负例评估的 L2 研究。
- [OpenHands/OpenHands 研究域](../research/openhands-openhands/README.md) - Agent Canvas、工作区和后端控制中心。
- [OpenHands/OpenHands 研究分析](../research/openhands-openhands/analysis.md) - Agent 编排、工作区和自动化的结构化研究。
- [OpenHands/OpenHands 深度研究](../research/openhands-openhands/deep-dive.md) - Agent Server、适配层和状态边界的 L2 研究。
- [anomalyco/opencode 研究域](../research/anomalyco-opencode/README.md) - 模型无关的终端与编辑器 coding agent。
- [anomalyco/opencode 研究分析](../research/anomalyco-opencode/analysis.md) - provider、权限、插件和配置生命周期的结构化研究。
- [anomalyco/opencode 深度研究](../research/anomalyco-opencode/deep-dive.md) - plan/build、策略、插件 reload 和 v2 spec 的 L2 研究。
- [obra/superpowers 研究域](../research/obra-superpowers/README.md) - 跨 coding agent 的技能框架与开发方法论。
- [obra/superpowers 研究分析](../research/obra-superpowers/analysis.md) - 技能触发、TDD、审查和插件分发的结构化研究。
- [obra/superpowers 深度研究](../research/obra-superpowers/deep-dive.md) - 技能组合、阶段门禁和跨 harness 分发的 L2 研究。
- [addyosmani/agent-skills 研究域](../research/addyosmani-agent-skills/README.md) - 面向 coding agent 的生命周期技能与质量门禁。
- [addyosmani/agent-skills 研究分析](../research/addyosmani-agent-skills/analysis.md) - 生命周期命令、上下文层级和技能评估的结构化研究。
- [addyosmani/agent-skills 深度研究](../research/addyosmani-agent-skills/deep-dive.md) - commands、skills、references 和 evals 的 L2 研究。
- [aaif-goose/goose 研究域](../research/aaif-goose-goose/README.md) - 跨模型、跨平台的开源 AI Agent。
- [aaif-goose/goose 研究分析](../research/aaif-goose-goose/analysis.md) - provider、MCP、工作区和评估资产的结构化研究。
- [aaif-goose/goose 深度研究](../research/aaif-goose-goose/deep-dive.md) - Rust workspace、上下文管理和 workflow recipe 的 L2 研究。
- [continuedev/continue 研究域](../research/continuedev-continue/README.md) - 已停止主动维护的 IDE/CLI Agent 历史对标。
- [continuedev/continue 研究分析](../research/continuedev-continue/analysis.md) - 只读生命周期、上下文分层和迁移边界的结构化研究。
- [continuedev/continue 深度研究](../research/continuedev-continue/deep-dive.md) - IDE/CLI、配置、上下文和生命周期的 L2 研究。
- [SWE-agent/mini-SWE-agent 研究域](../research/swe-agent-mini-swe-agent/README.md) - 面向 issue 和命令行任务的极简软件工程 Agent。
- [SWE-agent/mini-SWE-agent 研究分析](../research/swe-agent-mini-swe-agent/analysis.md) - 极简工具面、有界执行和问题修复闭环研究。
- [SWE-agent/mini-SWE-agent 深度研究](../research/swe-agent-mini-swe-agent/deep-dive.md) - Bash 工具、轨迹、环境适配和评估边界的 L2 研究。
- [affaan-m/ECC 研究域](../research/affaan-m-ecc/README.md) - 多种 coding agent 的 Harness、技能与质量实践集合。
- [affaan-m/ECC 研究分析](../research/affaan-m-ecc/analysis.md) - Harness、记忆、安全和技能治理的结构化研究。
- [affaan-m/ECC 深度研究](../research/affaan-m-ecc/deep-dive.md) - `.codex`、manifests、hooks 和评估技能的 L2 研究。
- [shanraisshan/claude-code-best-practice 研究域](../research/shanraisshan-claude-code-best-practice/README.md) - Claude Code / Agentic Engineering 最强对标。
- [shanraisshan/claude-code-best-practice 研究分析](../research/shanraisshan-claude-code-best-practice/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [shanraisshan/claude-code-best-practice 深度研究](../research/shanraisshan-claude-code-best-practice/deep-dive.md) - L2 源码/结构深度研究、关键机制和可迁移模式。
- [tradecatlabs/vibe-coding-cn 研究域](../research/tradecatlabs-vibe-coding-cn/README.md) - 中文主线工程化工作流。
- [tradecatlabs/vibe-coding-cn 研究分析](../research/tradecatlabs-vibe-coding-cn/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [tradecatlabs/vibe-coding-cn 深度研究](../research/tradecatlabs-vibe-coding-cn/deep-dive.md) - L2 源码/结构深度研究、关键机制和可迁移模式。
- [datawhalechina/easy-vibe 研究域](../research/datawhalechina-easy-vibe/README.md) - 中文分阶段交互式课程。
- [datawhalechina/easy-vibe 研究分析](../research/datawhalechina-easy-vibe/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [datawhalechina/easy-vibe 深度研究](../research/datawhalechina-easy-vibe/deep-dive.md) - L2 源码/结构深度研究、关键机制和可迁移模式。
- [datawhalechina/vibe-vibe 研究域](../research/datawhalechina-vibe-vibe/README.md) - 中文零基础系统教程。
- [datawhalechina/vibe-vibe 研究分析](../research/datawhalechina-vibe-vibe/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [datawhalechina/vibe-vibe 深度研究](../research/datawhalechina-vibe-vibe/deep-dive.md) - L2 源码/结构深度研究、关键机制和可迁移模式。
- [filipecalegario/awesome-vibe-coding 研究域](../research/filipecalegario-awesome-vibe-coding/README.md) - 国际 Vibe Coding 索引。
- [filipecalegario/awesome-vibe-coding 研究分析](../research/filipecalegario-awesome-vibe-coding/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [filipecalegario/awesome-vibe-coding 深度研究](../research/filipecalegario-awesome-vibe-coding/deep-dive.md) - L2 源码/结构深度研究、关键机制和可迁移模式。
- [luzhenqian/ai-coding-lab 研究域](../research/luzhenqian-ai-coding-lab/README.md) - AI Coding 项目实验室。
- [luzhenqian/ai-coding-lab 研究分析](../research/luzhenqian-ai-coding-lab/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [luzhenqian/ai-coding-lab 深度研究](../research/luzhenqian-ai-coding-lab/deep-dive.md) - L2 源码/结构深度研究、关键机制和可迁移模式。
- [ShouZhengAI/CS146S_CN 研究域](../research/shouzhengai-cs146s-cn/README.md) - 中文课程与 assignments。
- [ShouZhengAI/CS146S_CN 研究分析](../research/shouzhengai-cs146s-cn/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [ShouZhengAI/CS146S_CN 深度研究](../research/shouzhengai-cs146s-cn/deep-dive.md) - L2 源码/结构深度研究、关键机制和可迁移模式。
- [ai-for-developers/awesome-vibe-coding 研究域](../research/ai-for-developers-awesome-vibe-coding/README.md) - 精选 Vibe Coding 资料清单。
- [ai-for-developers/awesome-vibe-coding 研究分析](../research/ai-for-developers-awesome-vibe-coding/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [ai-for-developers/awesome-vibe-coding 深度研究](../research/ai-for-developers-awesome-vibe-coding/deep-dive.md) - L2 结构深度研究、关键机制、迁移边界和验证任务。
- [Daotin/ai-coding 研究域](../research/daotin-ai-coding/README.md) - AI Coding 经验汇总。
- [Daotin/ai-coding 研究分析](../research/daotin-ai-coding/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [Daotin/ai-coding 深度研究](../research/daotin-ai-coding/deep-dive.md) - L2 结构深度研究、关键机制、迁移边界和验证任务。
- [earyantLe/vibe-coding-skill 研究域](../research/earyantle-vibe-coding-skill/README.md) - Vibe Coding Skill / SOP 化。
- [earyantLe/vibe-coding-skill 研究分析](../research/earyantle-vibe-coding-skill/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [earyantLe/vibe-coding-skill 深度研究](../research/earyantle-vibe-coding-skill/deep-dive.md) - L2 结构深度研究、关键机制、迁移边界和验证任务。
- [liyupi/ai-guide 研究域](../research/liyupi-ai-guide/README.md) - AI 资源大全与产品实用路线。
- [liyupi/ai-guide 研究分析](../research/liyupi-ai-guide/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [liyupi/ai-guide 深度研究](../research/liyupi-ai-guide/deep-dive.md) - L2 结构深度研究、关键机制、迁移边界和验证任务。
- [RooCodeInc/Roo-Code 研究域](../research/roocodeinc-roo-code/README.md) - 已归档多 Agent 编辑器工具。
- [RooCodeInc/Roo-Code 研究分析](../research/roocodeinc-roo-code/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [RooCodeInc/Roo-Code 深度研究](../research/roocodeinc-roo-code/deep-dive.md) - L2 结构深度研究、关键机制、迁移边界和验证任务。
- [wendy7756/vibe-coding-guide 研究域](../research/wendy7756-vibe-coding-guide/README.md) - 非程序员自然语言编程指南。
- [wendy7756/vibe-coding-guide 研究分析](../research/wendy7756-vibe-coding-guide/analysis.md) - 结构化研究结论、可借鉴点、风险和下一轮任务。
- [wendy7756/vibe-coding-guide 深度研究](../research/wendy7756-vibe-coding-guide/deep-dive.md) - L2 结构深度研究、关键机制、迁移边界和验证任务。
- [AGENTS](../research/AGENTS.md) - 研究笔记目录操作规则。


### workflow

- [README](./workflow/README.md) - 开发流程索引。
- [开发流程](./workflow/development-process.md) - 默认任务推进顺序、质量门禁和交付闭环。
- [AGENTS](./workflow/AGENTS.md) - 开发流程目录操作规则。

</details>

## 使用方式

- 只想快速开始：从 [getting-started](./getting-started/README.md) 进入。
- 已经有项目问题：先读 [问题求解](./concepts/problem-solving.md)，再读 [质量门禁与常见坑](./references/quality-gates-and-pitfalls.md)。
- 需要给 AI Agent 上下文：先给它 [AGENTS](./AGENTS.md)，再给它当前任务对应目录的 README 和具体正文文档。
- 需要规范执行顺序：读 [开发流程](./workflow/development-process.md)。
- 新增内容时，先判断它属于教程、概念、哲学、参考还是研究；研究内容进入根目录 `research/`。

## 正文

### 推荐阅读路径

#### 新手路径

1. [Vibe Coding 经验](./getting-started/vibe-coding-experience.md)
2. [学习地图](./getting-started/learning-map.md)
3. [问题求解](./concepts/problem-solving.md)
4. [拼好码](./concepts/glue-coding.md)
5. [质量门禁与常见坑](./references/quality-gates-and-pitfalls.md)

#### 开发者路径

1. [拼好码](./concepts/glue-coding.md)
2. [系统构建方法](./concepts/system-building.md)
3. [技术栈](./references/technology-stack.md)
4. [项目架构模板](./references/project-architecture-template.md)

#### 思维模型路径

1. [思维模型](./philosophy/thinking-models.md)
2. [组合描述模型](./philosophy/compositional-description-model.md)
3. [编程之道](./philosophy/programming-dao.md)
4. [软件工程的朴素真理](./philosophy/software-engineering-truths.md)
5. [递归自优化系统](./concepts/recursive-self-optimizing-system.md)

#### AI Agent 读取路径

1. [根目录 AGENTS](../AGENTS.md)
2. [docs 目录 AGENTS](./AGENTS.md)
3. [开发流程](./workflow/development-process.md)
4. [Vibe Coding 经验](./getting-started/vibe-coding-experience.md)
5. [项目架构模板](./references/project-architecture-template.md)
6. [质量门禁与常见坑](./references/quality-gates-and-pitfalls.md)
7. [AI 引用语料](../assets/ai-citation/README.md)
