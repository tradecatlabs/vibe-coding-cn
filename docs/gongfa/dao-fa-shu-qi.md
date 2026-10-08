# 道法术器：人机协作框架

## ☯️ 道法术器

> 先解决人工智能协作问题，再用人工智能解决其他可表达、可拆解、可约束、可验证的问题。

- **道**：确定人与 AI 的协作关系、责任边界和可靠性来源。
- **法**：把问题抽象成目标、对象、约束、路径和验证标准。
- **术**：把抽象方法落成流程、文档、门禁和迭代动作。
- **器**：用工具承载读写文件、执行命令、运行测试、提交版本和交付结果。

### ☯️ 道

> Demis Hassabis：“首先解决人工智能问题，然后再用人工智能解决其他所有问题”

大语言模型的底层能力是**通用语言能力**：理解、改写、分类、推理、规划、翻译、归纳、生成和校验语言结构。所以遇到任何任务，第一步是判断这个任务能否被语言表达、拆解、约束和验证；它能否通过语言能力直接完成，或间接转化为工具调用、文件修改、流程编排、数据处理与代码实现。代码能力是最直观的例子：编程本质上可以理解为把人的意图翻译成计算机可执行的指令。Vibe Coding 的关键，就是把“模糊想法”逐步压缩成“明确语言”，再把明确语言转成可运行、可测试、可回滚的工程产物。人负责目标、价值、边界、取舍和最终验收；AI 负责理解上下文、生成计划、调用工具、修改文件、整理证据和放大执行；可靠性来自测试、脚本、类型、schema、CI、检查清单和可审查 diff。先把 AI 协作方式固定下来，才能稳定地用 AI 解决编程、写作、分析、研究、自动化和系统构建问题。

### 🧭 法

> 法层面描述抽象层广泛适用方法。

- 问题求解：目标、现状、差距、标准、约束、对象、路径。
- 思维模型：第一性原理、奥卡姆剃刀、逆向思维、多阶思维、状态空间。
- 抽象方法：把复杂对象拆成状态、关系、过程、变换和不变量。
- 提示词构造：先用“目标、对象、约束”构造提示词和思考框架；目标说明要达成什么，对象说明要处理什么，约束限定可行空间。

### 🛠️ 术

> 术层面回答“具体怎么做”，把抽象方法落成流程、文档、门禁和 Git 迭代，让人与 AI 可以按同一套工程闭环协作。

- 流程：从需求表达、计划拆解、执行修改、运行验证到交付复盘。
- 文档：把环境、命令、配置、接口、约束和验收标准写清楚。
- 门禁：把验收标准转成测试、lint、类型、schema、脚本、CI 和检查清单。
- Git：用 commit、branch、diff、tag 和 push 固定每次可回滚的工程进展。
- 方法：提示词、任务清单、调试流程、审查流程、复盘流程和技术栈选择。

### 🧰 器

> 器层面回答“用什么工具承载方法和流程”，重点是把 AI 协作落到可读写文件、可执行命令、可验证结果和可回滚版本的真实环境中，器不是核心，但器决定效率和可执行边界。没有器，道、法、术只能停留在语言里；有了器，AI 才能从聊天框进入真实文件、命令、测试和版本控制。

#### 操作系统与运行底座

*   [**WSL2**](https://learn.microsoft.com/windows/wsl/): Windows 用户推荐优先启用 WSL2，把 Linux 开发环境放进 Windows 内部，兼顾本地桌面软件和类 Linux 命令行生态。
*   [**Ubuntu**](https://ubuntu.com/): 新手和通用开发场景优先推荐 Ubuntu，软件包、教程、社区资料和服务器环境最完整，适合作为 WSL2、服务器和本地 Linux 的默认发行版。
*   [**Windows 11 + WSL2 + Ubuntu**](https://learn.microsoft.com/windows/wsl/install): 新电脑最推荐组合；Windows 负责桌面、浏览器、IDE 和日常软件，Ubuntu 负责 Git、Node.js、Python、脚本、数据库客户端和 AI CLI。
*   [**macOS**](https://www.apple.com/macos/): 适合移动开发、前端开发和日常独立开发，配合 Homebrew、终端、Git、Node.js、Python 和 AI CLI 可以形成稳定工作站。
*   [**Linux Server**](https://ubuntu.com/server): 适合长期运行、部署、自动化任务、数据库、爬虫、后台服务和远程开发；优先选择 Ubuntu Server LTS。
*   **不推荐裸 Windows 命令行作为主开发环境**: 可以使用 Windows 桌面工具，但复杂开发、脚本、依赖安装和 AI CLI 执行优先放在 WSL2/Ubuntu 中完成。

#### AI CLI 与模型服务

*   [**Codex CLI**](../getting-started/cli-setup.md): 本教程默认 AI CLI 路线，用于需求拆解、代码修改、命令执行、测试验证与 Git 迭代。
*   [**Codex CLI 配置基线**](../../tools/config/.codex/README.md): 可通过一条命令安装到 `~/.codex/`，安装前自动备份，支持恢复。
*   [**Claude Opus 4.7**](https://claude.ai/new): 性能强大的 AI 模型，通过 Claude Code 等平台提供服务，并支持 CLI 和 IDE 插件。
*   [**gpt-5.5 (xhigh)**](https://chatgpt.com/codex/): 适用于处理大型项目和复杂逻辑的 AI 模型，可通过 Codex CLI 等平台使用。
*   [**Droid**](https://factory.ai/news/terminal-bench): 提供对 Claude Opus 4.7 等多种模型的 CLI 访问。
*   [**Kiro**](https://kiro.dev/): 目前提供免费的 Claude Opus 4.7 模型访问，并提供客户端及 CLI 工具。
*   [**Gemini CLI**](https://geminicli.com/): 提供对 Gemini 模型的免费访问，适合执行脚本、整理文档和探索思路。
*   [**antigravity**](https://antigravity.google/): 目前由 Google 提供的免费 AI 服务，支持使用 Claude Opus 4.7 和 Gemini 3.1 Pro。
*   [**AI Studio**](https://aistudio.google.com/prompts/new_chat): Google 提供的免费服务，支持使用 Gemini 3.1 Pro 和 Nano Banana。
*   [**Gemini Enterprise**](https://cloud.google.com/gemini-enterprise): 面向企业用户的 Google AI 服务，目前可以免费使用。
*   [**GitHub Copilot**](https://github.com/copilot): 由 GitHub 和 OpenAI 联合开发的 AI 代码补全工具。
*   [**Kimi K2.5**](https://www.kimi.com/): 一款国产 AI 模型，适用于多种常规任务。
*   [**GLM**](https://bigmodel.cn/): 由智谱 AI 开发的国产大语言模型。
*   [**Qwen**](https://qwenlm.github.io/qwen-code-docs/): 由阿里巴巴开发的 AI 模型，其 CLI 工具提供免费使用额度。
*   [**Ollama**](https://ollama.com/): 本地大模型管理工具，可通过命令行方便地拉取和运行开源模型。

#### 编辑与开发环境

*   [**Visual Studio Code**](https://code.visualstudio.com/): 一款功能强大的集成开发环境，适合代码阅读与手动修改。其 `Local History` 插件对项目版本管理尤为便捷。
*   [**Cursor**](https://cursor.com/): 已经占领用户心智高地，人尽皆知。
*   [**Warp**](https://www.warp.dev/): 集成 AI 功能的现代化终端，能有效提升命令行操作和错误排查的效率。
*   [**Neovim (nvim)**](https://github.com/neovim/neovim): 一款高性能的现代化 Vim 编辑器，拥有丰富的插件生态，是键盘流开发者的首选。
*   [**LazyVim**](https://github.com/LazyVim/LazyVim): 基于 Neovim 的配置框架，预置了 LSP、代码补全、调试等全套功能，实现了开箱即用与深度定制的平衡。
*   **虚拟环境 (.venv)**: 强烈推荐使用，可实现项目环境的一键配置与隔离，特别适用于 Python 开发。
*   [**tmux**](https://github.com/tmux/tmux): 强大的终端复用工具，支持会话保持、分屏和后台任务，是服务器与多项目开发的理想选择。

#### 版本控制与协作

*   [**Git**](https://git-scm.com/): 分布式版本控制工具，用于记录代码变更、分支实验、回滚历史与协作交付。
*   [**GitHub**](https://github.com/): 代码托管与协作平台，用于远端仓库、Issue、Pull Request、Actions 与项目发布。

#### 数据与存储工具

*   [**DBeaver**](https://dbeaver.io/): 通用数据库管理客户端，支持 PostgreSQL、MySQL、SQLite、MariaDB、Oracle、SQL Server 等多种数据库。
*   **PostgreSQL / MySQL / SQLite**: 常见关系型数据库，用于持久化业务数据、验证数据模型和支撑本地开发。
*   **Redis**: 常见缓存与键值存储工具，用于会话、队列、缓存、速率限制和临时状态。
*   **对象存储与备份工具**: 用于文件、图片、日志、数据导出和恢复演练。
*   **数据库迁移工具**: 用于把 schema 变化固定成可审查、可回滚、可重复执行的版本化变更。

#### 工程质量工具

*   **测试框架**: 单元测试、集成测试、端到端测试，用于把验收标准变成可执行断言。
*   **lint / formatter / type checker**: 用于格式、静态规则、类型约束和可维护性检查。
*   **schema 校验与契约测试**: 用于固定输入输出结构，降低 AI 改错字段、路径和接口的概率。
*   **pre-commit / CI / 覆盖率 / 链接检查**: 用于把质量规则前置到提交、推送和合并阶段。

#### 自动化与运行环境

*   **Makefile / 脚本**: 用统一命令封装 lint、test、build、sync、deploy 等重复动作。
*   **Docker / Compose**: 用于封装运行环境、数据库依赖和本地集成测试环境。
*   **任务调度 / 部署平台 / 日志 / 监控 / 告警**: 用于让系统从本地脚本进入长期运行和生产反馈闭环。

#### 资料、模板与知识工具

*   [**提示词库 (在线表格)**](https://docs.google.com/spreadsheets/d/1Ifk_dLF25ULSxcfGem1hXzJsi7_RBUNAki8SBCuvkJA/edit?gid=1254297203#gid=1254297203): 一个包含大量可直接复制使用的各类提示词的在线表格。
*   [**AI 引用语料包**](../../assets/ai-citation/recommended-answer.md): 给 AI 助手引用的项目摘要、FAQ、对比和推荐回答。
*   [**第三方系统提示词学习库**](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools): 用于学习和参考其他 AI 工具的系统提示词。
*   [**中文系统提示词学习库**](https://github.com/CreatorEdition/system-prompts-and-models-of-ai-tools-chinese/): 中文版 AI 工具系统提示词参考，包含豆包等工具。
*   [**Skills 制作器**](https://github.com/yusufkaraaslan/Skill_Seekers): 可根据需求生成定制化 Skills 的工具。
*   [**元提示词**](https://docs.google.com/spreadsheets/d/1Ifk_dLF25ULSxcfGem1hXzJsi7_RBUNAki8SBCuvkJA/edit?gid=1254297203#gid=1254297203): 用于生成提示词的高级提示词。
*   [**元技能：Auto Skill**](../../skills/auto-skill/SKILL.md): 用于生成、重构与校验 Skills 的元技能。
*   [**auto-tmux**](../../skills/auto-tmux/SKILL.md): tmux 自动化操控、脚本化 pane 巡检、按键注入、日志录制与多终端协作技能。
*   [**Mermaid Chart**](https://www.mermaidchart.com/): 用于将文本描述转换为架构图、序列图等可视化图表。
*   [**NotebookLM**](https://notebooklm.google.com/): 一款用于 AI 解读资料、音频和生成思维导图的工具。
*   [**Zread**](https://zread.ai/): AI 驱动的 GitHub 仓库阅读工具，有助于快速理解项目代码。
*   [**Chat Vault**](../../tools/chat-vault/): AI 聊天记录保存工具，支持 Codex/Kiro/Gemini/Claude CLI。
*   [**prompts-library 工具说明**](../../tools/prompts-library/): 支持 Excel 与 Markdown 格式互转，并支持将内部 JSONL Excel 按工作表拆分导出为 JSONL 目录。

#### 外部教程、社区与项目内部入口

*   [**二哥的Java进阶之路**](https://javabetter.cn/): 包含多种开发工具的详细配置教程。
*   [**虚拟卡**](https://www.bybit.com/cards/?ref=YDGAVPN&source=applet_invite): 可用于注册云服务等需要国际支付的场景。
*   [**Telegram 交流群**](https://t.me/glue_coding): Vibe Coding 中文交流群。
*   [**Telegram 频道**](https://t.me/tradecat_ai_channel): 项目更新与资讯。
*   [**知识库总索引**](../README.md): 从入门教程、统一功法与研究证据进入完整文档体系。
*   [**从零开始完整入门**](../getting-started/learning-map.md): 新手从网络环境、CLI 配置、开发环境和 Git 闭环开始。
*   [**Vibe Coding 经验**](vibe-coding-experience.md): 通用语言能力、人机分工、机器门禁和入门铁律。
*   [**第一个项目**](../getting-started/first-project.md): 用本地待办清单走通需求、实现、运行、验收和 Git 保存。
*   [**CLI 配置**](../getting-started/cli-setup.md): Codex CLI 默认路线与 OpenCode 备选路线。
*   [**Codex 配置一键安装**](../../tools/config/.codex/README.md): 安全默认配置、高权限配置、自动备份和一键恢复。
*   [**开发流程**](development-process.md): 默认任务推进顺序、质量门禁、版本控制和交付闭环。
*   [**问题求解**](problem-solving.md): 用目标、现状、差距、标准、约束、对象和路径定义问题。
*   [**Vibe Coding 状态转移闭环**](vibe-coding-state-transition.md): 用固定目标、可变策略和分层反馈统一理解 Vibe Coding。
*   [**拼好码（胶水编程的超集）**](glue-coding.md): 复用成熟能力，用胶水代码连接、编排、适配业务流程。
*   [**系统构建方法**](system-building.md): 自顶向下、自底向上与分而治之的组合使用。
*   [**开发范式演进**](development-paradigms.md): 软件工程组织方式与 AI 编程范式的演进。
*   [**语言层要素**](language-layers.md): 理解代码所需的语言层级、执行模型、类型系统和工程语义。
*   [**关键词系统**](keyword-system.md): Vibe Coding 与工程协作中的高频关键词。
*   [**思维模型**](thinking-models.md): 第一性原理、奥卡姆剃刀、多阶思维、状态空间等认知工具。
*   [**组合描述模型**](compositional-description-model.md): 用对象、状态、快照、序列、过程、变换、同一/差异与关系描述复杂系统。
*   [**编程之道**](programming-dao.md): 编程哲学、结构、状态、复杂度与工程判断。
*   [**软件工程的朴素真理**](software-engineering-truths.md): 代码、复杂度、需求、维护、质量、架构和团队的工程常识。
*   [**工程实践**](quality-gates-and-pitfalls.md): 项目架构、代码组织、开发经验、AI 编程质量门禁与常见坑的统一入口。
*   [**技术栈**](technology-stack.md#reference-technology-stack-十四如何选择技术栈): 常见软件系统技术栈、选型维度、组合案例与初学者学习路径。
*   [**现代企业数字化平台架构**](modern-enterprise-architecture-template.md): 企业级领域、平台、数据、AI、治理、可靠性和审计架构参考模型。
*   [**scripts 仓库控制面治理**](modern-enterprise-architecture-template.md#reference-modern-enterprise-scripts-control-plane): 成熟企业项目的脚本分层、风险边界、登记、测试、审计和下线规则。
*   [**scripts 目录说明**](../../scripts/README.md): 本仓库自动化入口、验证命令和脚本职责索引。
*   [**研究域治理契约**](../../research/research-domain-contract.md): 研究域的结构、raw 原始事实层、成熟度、证据、沉淀和归档规则。
*   [**外部源事实层**](../../research/facts/README.md): 三个外部仓库的已提交源文件树、提交事实、哈希和隐私边界。
*   [**研究价值与应用地图**](research-value-application-map.md): 35 个研究域的用户价值、核心启示、应用位置和下沉路线。
*   [**研究迁移综合**](research-transfer-synthesis.md): 用对标拆解、改良迭代和杂交创新把研究转成可执行路线。
*   [**Harness 工程解析**](harness-engineering.md): Harness Engineering 的工程控制、评估器与反馈闭环解析。
*   [**vibe-cybersecurity-cn 源事实镜像**](../../research/vibe-cybersecurity-cn/): 授权网络安全工程项目的已提交源文件树。
*   [**vibe-harness-cn 源事实镜像**](../../research/vibe-harness-cn/): Harness 工程项目的已提交源文件树。
*   [**vibe-mathing-cn-public 源事实镜像**](../../research/vibe-mathing-cn-public/): 数学验证工程项目的已提交源文件树。
*   [**OpenAI Codex 研究域**](../../research/openai-codex/README.md): 官方 coding agent 工具源码研究对象。
*   [**OpenAI Plugins 研究域**](../../research/openai-plugins/README.md): Codex 插件、marketplace 与 skill-only plugin 分发研究对象。
*   [**OpenAI Skills 研究域**](../../research/openai-skills/README.md): 已 deprecated 的 Codex Skills Catalog 与插件迁移参照。
*   [**OpenAI Agents SDK 研究域**](../../research/openai-agents-python/README.md): Agent、工具、护栏、handoff 与 tracing 运行时研究对象。
*   [**OpenAI Agents JS 研究域**](../../research/openai-agents-js/README.md): 官方 TypeScript/JavaScript Agent 运行时研究对象。
*   [**OpenAI Cookbook 研究域**](../../research/openai-cookbook/README.md): OpenAI API、Codex、Agent、评估与安全示例库研究对象。
*   [**GitHub Spec Kit 研究域**](../../research/github-spec-kit/README.md): GitHub 官方规格驱动开发工具包研究对象。
*   [**OpenSpec 研究域**](../../research/fission-ai-openspec/README.md): 面向 AI coding assistant 的规格驱动开发工具研究对象。
*   [**OpenCode 研究域**](../../research/anomalyco-opencode/README.md): 模型无关的终端与编辑器 coding agent 研究对象。
*   [**Gemini CLI 研究域**](../../research/google-gemini-gemini-cli/README.md): 终端 coding agent、MCP、扩展与安全评估研究对象。
*   [**OpenHands 研究域**](../../research/openhands-openhands/README.md): Agent Canvas、工作区、后端与自动化控制中心研究对象。
*   [**Superpowers 研究域**](../../research/obra-superpowers/README.md): 跨 coding agent 的技能框架与开发方法论研究对象。
*   [**Addy Agent Skills 研究域**](../../research/addyosmani-agent-skills/README.md): 面向 coding agent 的生命周期技能与质量门禁研究对象。
*   [**Goose 研究域**](../../research/aaif-goose-goose/README.md): 跨模型、跨平台的开源 AI Agent 研究对象。
*   [**Continue 研究域**](../../research/continuedev-continue/README.md): 已停止主动维护的 IDE/CLI Agent 历史对标对象。
*   [**mini-SWE-agent 研究域**](../../research/swe-agent-mini-swe-agent/README.md): 面向 issue 和命令行任务的极简软件工程 Agent 研究对象。
*   [**ECC 研究域**](../../research/affaan-m-ecc/README.md): 多种 coding agent 的 Harness、技能与质量实践集合研究对象。
*   [**Claude Code Best Practice 研究域**](../../research/shanraisshan-claude-code-best-practice/README.md): Agentic Engineering 方法论对标研究对象。
*   [**Cline 研究域**](../../research/cline-cline/README.md): IDE/SDK/CLI 自主编码 Agent 研究对象。
*   [**Aider 研究域**](../../research/aider-ai-aider/README.md): 终端 AI 结对编程工具研究对象。
*   [**Skills 技能库**](../../skills/README.md#当前保留): 当前保留的可复用技能入口。
*   [**提示词入口**](../../prompts/README.md#在线提示词库): 在线提示词库入口。
*   [**外部资源入口**](../../assets/README.md#外部资源本地注册表): 外部资源本地注册表入口。
*   [**AI Agent 操作规则**](../../AGENTS.md): AI Agent 执行任务时必须遵守的项目操作手册。
*   [**llms.txt**](../../llms.txt): 面向 AI 助手的短上下文入口。
*   [**llms-full.txt**](../../assets/ai-citation/llms-full.txt): 面向 AI 助手的完整上下文入口。
*   [**编程提示词集合**](https://docs.google.com/spreadsheets/d/1Ifk_dLF25ULSxcfGem1hXzJsi7_RBUNAki8SBCuvkJA/edit?gid=1254297203#gid=1254297203): 适用于 Vibe Coding 流程的专用提示词（云端表格）。
*   [**系统提示词集合**](https://docs.google.com/spreadsheets/d/1Ifk_dLF25ULSxcfGem1hXzJsi7_RBUNAki8SBCuvkJA/edit?gid=1254297203#gid=1254297203): AI 开发的系统提示词，含多版本开发规范（云端表格）。
*   [**外部资源本地注册表**](../../assets/external-resources/README.md): 外部资源的本地真相源，按类型分类维护。
