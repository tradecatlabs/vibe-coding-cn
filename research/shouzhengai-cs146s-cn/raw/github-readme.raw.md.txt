<div align="center">
  <img src="teaser.png" width="100%" height="auto">
</div>

<h1 align="center">📚CS146S中文版课程 Vibe Coding Together</h1>
🌟 付费赞助广告位：联系邮箱szwang.scholar@gmail.com，在文档内展示您的品牌和产品。

![Visitors](https://api.visitorbadge.io/api/visitors?path=https://github.com/ShouZhengAI/CS146S_CN&label=Total%20Visitors&labelColor=%232ccce4&countColor=%23d9e3f0)

**欢迎加入 动手学CS146S 交流群一起讨论**:
<div align="center">
  <img src="group6-2.png" width="20%" height="auto">
</div>

> 本项目长期维护，希望能帮到各位入门 vibe coding 的朋友，欢迎Star，分享与提PR🌟~  
> 正在积极维护高质量 Assignments 中，每周天发布哦~



## 课程简介

近几年来，大型语言模型（LLM）为软件开发带来了革命性的新范式。传统的软件开发生命周期正在被人工智能的自动化能力渗透和重塑，这引发了一个关键问题：下一代软件工程师应如何利用这些进步，将工作效率提升十倍（10x），并为未来的职业生涯做好准备？

本课程将证明，现代人工智能工具不仅能大幅提高开发人员的生产力，还能让更广泛的受众更容易接触和从事软件工程工作。我们将展示，软件开发已经从“从零开始”（0-1）的代码编写，演变为一个迭代工作流程：规划、利用AI生成、修改，然后重复。学生将深入掌握传统软件工程挑战背后的理论，以及当前解决这些问题的尖端AI驱动工具。

通过动手实践的工程任务，以及来自行业先驱（这些革命性工具的开发者）的讲座，你将获得以下方面的实战经验：AI辅助开发、自动化测试、智能文档生成和安全漏洞检测。学完本课程后，你将对如何将最先进的LLM模型整合到复杂的开发工作流程中并避免常见陷阱有一个清晰而透彻的理解。


**先决条件**：具备相当于 CS111 级别的编程经验。推荐具备 CS221/229 课程知识。

**形式**：每周讲座、动手编码实践课，以及行业嘉宾演讲。期末项目要求展示现代开发实践。

**目标**：掌握现代开发工具、理解 AI 辅助编程、学习自动化测试和部署、探索新兴软件趋势。

**评分**：期末项目 80%，每周作业 15%，课堂参与 5%

**作业截止日期**：
![calender](./Resource/imgs/PixPin_2025-12-16_17-10-42.png)

* [教学大纲](#教学大纲)
    * [第 1 周：编码 LLM 和 AI 开发简介](#第-1-周编码-llm-和-ai-开发简介)
    * [第 2 周：编码智能体剖析](#第-2-周编码智能体剖析)
    * [第 3 周：AI 集成开发环境（IDE）](#第-3-周ai-集成开发环境ide)
    * [第 4 周：编码智能体模式](#第-4-周编码智能体模式)
    * [第 5 周：现代终端](#第-5-周现代终端)
    * [第 6 周：AI 测试与安全](#第-6-周ai-测试与安全)
    * [第 7 周：现代软件支持](#第-7-周现代软件支持)
    * [第 8 周：自动化 UI 和应用程序构建](#第-8-周自动化-ui-和应用程序构建)
    * [第 9 周：智能体部署后](#第-9-周智能体部署后)
    * [第 10 周：AI 软件工程的未来展望](#第-10-周ai-软件工程的未来展望)
* [本地ai应用](#本地应用)
* [vibe coding命令行工具](#命令行工具)
* [国产编程平台](#国产编程平台)
* [FAQ 常见问题](#常见问题)
* [相关资源-vibe coding项目](#相关项目资源)
---
- [x] week1 Assignments
- [ ] week2 Assignments
- [ ] week3 Assignments
- [ ] week4 Assignments
- [ ] week5 Assignments
- [ ] week6 Assignments
- [ ] week7 Assignments
- [ ] week8 Assignments  
- [ ] week9 Assignments
- [ ] week0 Assignments
---
## 教学大纲

### 第 1 周：编码 LLM 和 AI 开发简介

**主题**

  - 课程安排
  - LLM 到底是什么
  - 如何有效进行 Prompt

**阅读材料**

  - [深入探究 LLM: Deep Dive into LLMs](https://www.youtube.com/watch?v=7xTGNNLPyMI)
    - [b站中文版](https://www.bilibili.com/video/BV16cNEeXEer)
  - [提示工程概述: Prompt Engineering Overview](https://cloud.google.com/discover/what-is-prompt-engineering)
    - [提示词工程概述中文版](https://www.yuque.com/wangjiandong/gwcyhv/uw3b7we9pmdubdig)
  - [提示工程指南: Prompt Engineering Guide](https://www.promptingguide.ai/techniques)
    - [提示词工程指南中文版](https://www.yuque.com/wangjiandong/gwcyhv/ziny243nwrodmew3)
  - [AI 提示工程：深度探究: AI Prompt Engineering: A Deep Dive](https://www.youtube.com/watch?v=T9aRN5JkmL8)
    - [b站中文版](https://www.bilibili.com/video/BV18ukBYzEQG)
  - [OpenAI 如何使用 Codex: How OpenAI Uses Codex](https://cdn.openai.com/pdf/6a2631dc-783e-479b-b1a4-af0cfbd38630/how-openai-uses-codex.pdf)

**课后作业**

  - [LLM 提示词实践平台: LLM Prompting Playground](./Assignments/week1/README.md)

**9 月 22 日（周一）：** 简介及 LLM 原理 - [Slides](./Resource/pdfs/1_1%20Introduction%20and%20how%20an%20LLM%20is%20made.pdf) [中文PPT](./Resource/pdfs/1_1%20Introduction%20and%20how%20an%20LLM%20is%20made_CN.pdf)

**9 月 26 日（周五）：** LLM 的高效提示 - [Slides](./Resource/pdfs/1_2%20Power%20prompting%20for%20LLMs.pdf) [中文PPT](./Resource/pdfs/1_2%20Power%20prompting%20for%20LLMs_CN.pdf)

### 第 2 周：编码智能体剖析

**主题**

  - 智能体架构和组件
  - 工具使用和函数调用
  - MCP (模型上下文协议)

**阅读材料**

  - [MCP 简介: MCP Introduction](https://stytch.com/blog/model-context-protocol-introduction/)
  - [MCP 服务器实现示例: Sample MCP Server Implementations](https://github.com/modelcontextprotocol/servers)
  - [MCP 服务器认证: MCP Server Authentication](https://developers.cloudflare.com/agents/guides/remote-mcp-server/#add-authentication)
  - [MCP 服务器 SDK: MCP Server SDK](https://github.com/modelcontextprotocol/typescript-sdk/tree/main?tab=readme-ov-file#server)
  - [MCP 注册中心: MCP Registry](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/)
  - [关于 MCP 的思考: MCP Food-for-Thought](https://www.reillywood.com/blog/apis-dont-make-good-mcp-tools/)

**课后作业**

  - [AI IDE 初探: First Steps in the AI IDE](./Assignments/week2/assignment.md)

**9 月 29 日（周一）：** 从零开始构建一个编码智能体 - [Slides](./Resource/pdfs/2_1%20Building%20a%20coding%20agent%20from%20scratch.pdf), [已完成的练习: Completed Exercise](./Resource/completed/coding_agent_from_scratch_lecture.py)

**10 月 3 日（周五）：** 构建一个自定义 MCP 服务器 - [Slides](./Resource/pdfs/2_2%20Building%20a%20coding%20agent%20from%20scratch.pdf), [已完成的练习: Completed Exercise](./Resource/completed/simple_mcp.py)

### 第 3 周：AI 集成开发环境（IDE）

**主题**

  - 上下文管理和代码理解
  - 智能体的产品需求文档（PRD）
  - IDE 集成和扩展

**阅读材料**

  - [规范即新的源代码: Specs Are the New Source Code](https://blog.ravi-mehta.com/p/specs-are-the-new-source-code)
  - [长上下文如何失效及修复方法: How Long Contexts Fail](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html)
  - [Devin：编码智能体 101: Devin: Coding Agents 101](https://devin.ai/agents101#introduction)
  - [让 AI 在复杂代码库中工作: Getting AI to Work In Complex Codebases](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md)
  - [FAANG 是如何进行 Vibe Coding 的: How FAANG Vibe Codes](https://x.com/rohanpaul_ai/status/1959414096589422619)
  - [为智能体编写高效工具: Writing Effective Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)

**课后作业**

  - [构建一个自定义 MCP 服务器: Build a Custom MCP Server](https://github.com/mihail911/modern-software-dev-assignments/blob/master/week3/assignment.md)

**10 月 6 日（周一）：** 从首次提示到最佳 IDE 设置 - [Slides](./Resource/pdfs/3_1%20Building%20a%20coding%20agent%20from%20scratch.pdf), [设计文档模板: Design Doc Template](./Resource/completed/design_doc_template.md)

**10 月 10 日（周五）：** [Silas Alberti](https://www.linkedin.com/in/silasalberti/) ([Cognition](https://cognition.ai/) 研究负责人) - [Slides](./Resource/pdfs/3_2%20Silas%20Alberti,%20Head%20of%20Research.pdf)

### 第 4 周：编码智能体模式

**主题**

  - 管理智能体自治级别
  - 人与智能体协作模式

**阅读材料**

  - [Anthropic 如何使用 Claude Code: How Anthropic Uses Claude Code](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf)
  - [Claude 最佳实践: Claude Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
  - [精选 Claude 智能体: Awesome Claude Agents](https://github.com/vijaythecoder/awesome-claude-agents)
  - [Super Claude](https://github.com/SuperClaude-Org/SuperClaude_Framework): Super Claude
  - [好的上下文，好的代码: Good Context Good Code](https://blog.stockapp.com/good-context-good-code/)
  - [窥探 Claude Code 的内部机制: Peeking Under the Hood of Claude Code](https://medium.com/@outsightai/peeking-under-the-hood-of-claude-code-70f5a94a9a62)

**课后作业**

  - [使用 Claude Code 编码: Coding with Claude Code](https://github.com/mihail911/modern-software-dev-assignments/blob/master/week4/assignment.md)

**10 月 13 日（周一）：** 如何成为一名智能体管理者 - [Slides](https://docs.google.com/presentation/d/19mgkwAnJDc7JuJy0zhhoY0ZC15DiNpxL8kchPDnRkRQ/edit?usp=sharing)

**10 月 17 日（周五）：** [Boris Cherney](https://www.linkedin.com/in/bcherny/) ([Claude Code](https://www.anthropic.com/claude-code) 创建者) - [Slides](https://docs.google.com/presentation/d/1bv7Zozn6z45CAh-IyX99dMPMyXCHC7zj95UfwErBYQ8/edit?usp=sharing)

### 第 5 周：现代终端

**主题**

  - AI 增强的命令行界面
  - 终端自动化和脚本编写

**阅读材料**

  - [Warp 大学: Warp University](https://www.warp.dev/university?slug=university)
  - [Warp 对比 Claude Code: Warp vs Claude Code](https://www.warp.dev/university/getting-started/warp-vs-claude-code)
  - [Warp 如何使用 Warp 来构建 Warp: How Warp Uses Warp to Build Warp](https://notion.warp.dev/How-Warp-uses-Warp-to-build-Warp-21643263616d81a6b9e3e63fd8a7380c)

**课后作业**

  - [使用 Warp 进行智能体开发: Agentic Development with Warp](https://github.com/mihail911/modern-software-dev-assignments/tree/master/week5)

**10 月 20 日（周一）：** 如何打造一款爆款 AI 开发者产品 - [Slides](https://docs.google.com/presentation/d/1Djd4eBLBbRkma8rFnJAWMT0ptct_UGB8hipmoqFVkxQ/edit?usp=sharing)

**10 月 24 日（周五）：** [Zach Lloyd](https://www.linkedin.com/in/zachlloyd/) ([Warp](https://www.warp.dev/) 首席执行官) - [Slides](https://www.figma.com/slides/kwbcmtqTFQMfUhiMH8BiEx/Warp---Stanford--Copy-?node-id=9-116&t=oBWBCk8mjg2l2NR5-1)

### 第 6 周：AI 测试与安全

**主题**

  - 安全的 Vibe coding
  - 漏洞检测的历史
  - AI 生成的测试套件

**阅读材料**

  - [SAST 对比 DAST: SAST vs DAST](https://www.splunk.com/en_us/blog/learn/sast-vs-dast.html)
  - [通过提示注入实现 Copilot 远程代码执行: Copilot Remote Code Execution via Prompt Injection](https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/)
  - [使用 Claude Code 和 OpenAI Codex 发现现代 Web 应用程序中的漏洞: Finding Vulnerabilities in Modern Web Apps Using Claude Code and OpenAI Codex](https://semgrep.dev/blog/2025/finding-vulnerabilities-in-modern-web-apps-using-claude-code-and-openai-codex/)
  - [智能体 AI 威胁：身份欺骗和冒充风险: Agentic AI Threats: Identity Spoofing and Impersonation Risks](https://www.google.com/search?q=https://unit42.paloaltonetworks.com/agentic-ai-threats/%23:~:text%3DIdentity%2520spoofing%2520and%2520impersonation:%2520Attackers,accurate%2520information%2520exchange%2520are%2520critical.)
  - [OWASP Top Ten：主要的 Web 应用程序安全风险: OWASP Top Ten: The Leading Web Application Security Risks](https://owasp.org/www-project-top-ten/)
  - [上下文腐烂：理解 AI 上下文窗口的退化: Context Rot: Understanding Degradation in AI Context Windows](https://research.trychroma.com/context-rot)
  - [使用 O3 进行漏洞提示分析: Vulnerability Prompt Analysis with O3](https://github.com/SeanHeelan/o3_finds_cve-2025-37899/blob/master/system_prompt_uafs.prompt)

**课后作业**

  - [编写安全的 AI 代码: Writing Secure AI Code](https://github.com/mihail911/modern-software-dev-assignments/blob/master/week6/assignment.md)

**10 月 27 日（周一）：** AI QA、SAST、DAST 及未来 - [Slides](https://docs.google.com/presentation/d/1C05bCLasMDigBbkwdWbiz4WrXibzi6ua4hQQbTod_8c/edit?usp=sharing)

**10 月 31 日（周五）：** [Isaac Evans](https://www.linkedin.com/in/isaacevans/) ([Semgrep](https://semgrep.dev/) 首席执行官)

### 第 7 周：现代软件支持

**主题**

  - 我们可以信任哪些 AI 代码系统
  - 调试与诊断
  - 智能文档生成

**阅读材料**

  - [代码审查：做就对了: Code Reviews: Just Do It](https://blog.codinghorror.com/code-reviews-just-do-it/)
  - [如何有效进行代码审查: How to Review Code Effectively](https://github.blog/developer-skills/github/how-to-review-code-effectively-a-github-staff-engineers-philosophy/)
  - [现代代码审查中 AI 辅助的编码实践评估: AI-Assisted Assessment of Coding Practices in Modern Code Review](https://arxiv.org/pdf/2405.13565)
  - [AI 代码审查实施最佳实践: AI Code Review Implementation Best Practices](https://graphite.dev/guides/ai-code-review-implementation-best-practices)
  - [软件团队的代码审查要点: Code Review Essentials for Software Teams](https://blakesmith.me/2015/02/09/code-review-essentials-for-software-teams.html)
  - [从数百万次 AI 代码审查中汲取的经验: Lessons from millions of AI code reviews](https://www.youtube.com/watch?v=TswQeKftnaw)
    - [欢迎提供中文版视频]

**课后作业**

  - [代码审查练习: Code Review Reps](https://github.com/mihail911/modern-software-dev-assignments/tree/master/week7)

**11 月 3 日（周一）：** AI 代码审查 - [Slides](https://docs.google.com/presentation/d/1NkPzpuSQt6Esbnr2-EnxM9007TL6ebSPFwITyVY-QxU/edit?usp=sharing)

**11 月 7 日（周五）：** [Tomas Reimers](https://www.linkedin.com/in/tomasreimers/) ([Graphite](https://graphite.dev/) 首席产品官) - [Slides](https://drive.google.com/file/d/1hwF-RIkOJ_OFy17BKhzFyCtxSS7Pcf7p/view?usp=drive_link)

### 第 8 周：自动化 UI 和应用程序构建

**主题**

  - 面向所有人的设计和前端开发
  - 快速 UI/UX 原型设计和迭代

**课后作业**

  - [多技术栈 Web 应用程序构建: Multi-stack Web App Builds](https://github.com/mihail911/modern-software-dev-assignments/tree/master/week8)

**11 月 10 日（周一）：** 通过单个提示词实现端到端应用程序 - [Slides](https://docs.google.com/presentation/d/1GrVLsfMFIXMiGjIW9D7EJIyLYh_-3ReHHNd_vRfZUoo/edit?usp=sharing)

**11 月 14 日（周五）：** [Gaspar Garcia](https://www.linkedin.com/in/gaspargarcia/) ([Vercel](https://vercel.com/) AI 研究负责人) - [Slides](https://docs.google.com/presentation/d/1Jf2aN5zIChd5tT86rZWWqY-iDWbxgR-uynKJxBR7E9E/edit?usp=sharing)

### 第 9 周：智能体部署后

**主题**

  - AI 系统的监控和可观测性
  - 自动化事件响应
  - 分诊和调试

**阅读材料**

  - [网站可靠性工程 (SRE) 简介: Introduction to Site Reliability Engineering](https://sre.google/sre-book/introduction/)
  - [你应该了解的可观测性基础知识: Observability Basics You Should Know](https://last9.io/blog/traces-spans-observability-basics/)
  - [使用 AI 进行 Kubernetes 故障排除: Kubernetes Troubleshooting with AI](https://resolve.ai/blog/kubernetes-troubleshooting-in-resolve-ai)
  - [你的新自主队友: Your New Autonomous Teammate](https://resolve.ai/blog/product-deep-dive)
  - [多智能体系统在使软件工程师具备 AI 原生能力中的作用: Role of Multi Agent Systems in Making Software Engineers AI-native](https://resolve.ai/blog/role-of-multi-agent-systems-AI-native-engineering)
  - [智能体 AI 在待命工程中的优势: Benefits of Agentic AI in On-call Engineering](https://resolve.ai/blog/Top-5-Benefits)

**11 月 17 日（周一）：** 事件响应和 DevOps - [Slides](https://docs.google.com/presentation/d/1Mfe-auWAsg9URCujneKnHr0AbO8O-_U4QXBVOlO4qp0/edit?usp=sharing)

**11 月 21 日（周五）：** [Mayank Agarwal](https://www.linkedin.com/in/mayank-ag/) ([Resolve](https://resolve.ai/) 首席技术官) 和 [Milind Ganjoo](https://www.linkedin.com/in/mganjoo/) ([Resolve](https://resolve.ai/) 技术人员) - [Slides](https://drive.google.com/file/d/11WnEbMGc9kny_WBpMN10I8oP8XsiQOnM/view?usp=sharing)

### 第 10 周：AI 软件工程的未来展望

**主题**

  - 软件开发角色的未来
  - 新兴的 AI 编码范式
  - 行业趋势与预测

**12 月 1 日（周一）：** 十年后的软件开发

**12 月 5 日（周五）：** [Martin Casado](https://a16z.com/author/martin-casado/) ([a16z](https://a16z.com/) 普通合伙人)

---


## 本地应用
- [Dyad](https://www.dyad.sh/) - 免费、本地、开源的AI应用构建器

## 命令行工具

- [anthropics/claude-code](https://github.com/anthropics/claude-code) - 理解你的代码库、自动化任务、解释代码和管理git的编程代理，全部通过自然语言。
- [aider](https://aider.chat/) - 在终端中进行AI结对编程。
- [codename goose](https://block.github.io/goose/) - 本地机器AI代理，允许你使用任何LLM并添加任何MCP服务器作为扩展
- [MyCoder.ai](https://github.com/drivecore/mycoder) - 开源AI驱动的编程助手，具有Git和GitHub集成，支持并行执行和自修改功能。
- [ai-christianson/RA.Aid](https://github.com/ai-christianson/RA.Aid) - 基于LangGraph代理任务执行框架构建的独立编程代理
- [CodeSelect](https://github.com/maynetee/codeselect) - 基于Python的命令行工具，高效地将项目源代码传达给AI。
- [OpenAI Codex CLI](https://github.com/openai/codex) - OpenAI的轻量级编程代理，在终端中运行
- [Gemini CLI](https://github.com/google-gemini/gemini-cli) - 谷歌开源的AI代理，将 Gemini 的强大功能直接带入您的终端。
- [vibe-cli](https://github.com/Jinjos/vibe-cli) - 氛围编程工作流的命令行界面。
- [langchain-code](https://github.com/zamalali/langchain-code) - 基于LangChain的编程代理，用于AI辅助开发。
- [kimi-cli](https://github.com/MoonshotAI/kimi-cli) - Kimi官方命令行界面，一个帮助编程任务和开发工作流的AI助手。

## 国产编程平台


| 国产编程模型                | 定位                          | 个人最低订阅价                                                                                                                          | CLI & IDE                                                                                                                                                | 其他                                                          |
| --------------------- | --------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| **GLM-4.6 Coding**    | 智谱「通用+编程」双模长上下文             | [20 元/月（Coding Plan）](https://docs.bigmodel.cn/cn/guide/models/text/glm-4.6)<br>季付 54 元≈18 元/月                                   | – [GLM-CLI（官方）](https://github.com/xqsit94/glm)<br>– Claude Code / Roo Code / Cline 等 10+ 第三方已适配                                                         | [iFlow（开源流程编排）](https://github.com/OSCC-Project/iFlow)      |
| **Kimi K2 Thinking**  | 月之暗面「推理+代码」长思考模型            | [49 元/月（K2 会员）](https://kimi-k2.org/zh/blog/15-kimi-k2-thinking-zh)<br>放量 199 元/月                                                | – Kimi-Code-CLI（内测）<br>– 继续用 Claude Code，自定义 base-url 切到 K2                                                                                              | [Qwencode（阿里开源轻量 CLI）](https://github.com/alibaba/qwencode) |
| **Doubao-Seed-Code**  | 字节「Agentic 编程」专用模型，256k 上下文 | [Lite：首月 9.9 元，续费 40 元/月](https://www.volcengine.com/docs/82354/1639499)<br>Pro：首月 49.9 元，续费 200 元/月                             | – [veCLI（火山引擎）](https://www.volcengine.com/docs/82354/1639499)<br>– [Trae（字节官方 AI IDE）](https://www.trae.ai/)<br>– 兼容 Anthropic API，Claude Code 一行配置即可切换 | [CodeBuddy（腾讯开源）](https://github.com/Tencent/CodeBuddy)     |
| **DeepSeek-Coder**    | 深度求索开源系列，可本地部署              | 模型开源免费<br>[API 按量：输入 1 元 / 百万 tokens，输出 2 元 / 百万 tokens](https://platform.deepseek.com/)                                         | – [DeepSeek-Coder-CLI（官方）](https://coder.deepseek.com/)<br>– continue.dev / OpenCoder 插件                                                                 | 同上                                                          |
| **Qwen3-Coder-Flash** | 阿里通义「甜品级」开源编程模型             | 模型开源免费<br>[API 按量：输入≈0.8 元 / 百万 tokens，输出≈1.5 元 / 百万 tokens](https://www.modelscope.cn/models/Qwen/Qwen3-Coder-30B-A3B-Instruct) | – [Qwen-Code-CLI（官方）](https://github.com/QwenLM/Qwen-Code-CLI)<br>– [Qoder（阿里 AI IDE）](https://qoder.aliyun.com/)<br>– Claude Code + 自定义 endpoint        | 同上                                                          |


## 常见问题
<details>

### 本课程将使用哪些编程语言？

* 本课程不局限于特定的语言，重点是学习适用于不同编程语言的工具和实践。不过，课程示例将主要使用 Python、JavaScript，并在适当情况下使用一些系统编程语言。重点在于理解**现代开发实践**，而非精通特定语言。

### 我是否需要具备使用 GitHub Copilot 等 AI 工具的经验？

* 不需要具备 AI 开发工具的经验。本课程将从基础知识开始，循序渐进地过渡到更高级的应用。然而，扎实的编程基础（相当于 CS111 及以上水平）是必不可少的。

### 本课程会取代传统的软件工程课程吗？

* 本课程是传统软件工程课程的有力补充，重点关注现代工具和 AI 辅助开发。它假定你已具备软件工程的基础知识，并在此基础上教授最新的实践。

### 本课程需要投入多少时间？

* 预计每周投入约 10-12 小时，包括听课、完成作业和项目工作。本课程侧重实践，需要时间来尝试新的工具和技术。

### 是否有特殊的软硬件要求？

* 学生需要使用一台能够运行现代开发工具的计算机。某些基于云的服务可能需要订阅（如 GitHub Copilot 等），但课程将尽可能提供访问权限或替代方案。可靠的互联网连接对于使用基于云的工具至关重要。

### 课程内容的时效性如何？

* 课程内容设计具有高度时效性，将每周更新，以反映 AI 辅助开发这一快速变化的领域。来自行业领先公司的嘉宾讲者将确保学生学到最新的行业实践和新兴工具。

### 我可以旁听本课程吗？

* 我们欢迎斯坦福大学的学生和教职员工申请旁听。旁听者可以参加所有讲座，但我们无法批改您的作业或就期末项目提供建议。

</details>

---



# 相关项目资源

| 名称 | 简要 | 链接 |
|----------|----------|------|
| datawhalechina/vibe-vibe | 首个系统化 Vibe Coding 开源教程，从零基础到全栈实战，让人人都能用 AI 开发产品。在线阅读地址：www.vibevibe.cn | [link](https://github.com/datawhalechina/vibe-vibe) |
| tukuaiai/vibe-coding-cn | Vibe Coding 的中文翻译版本 + 个人开发经验 + 提示词库，构建成一个综合的 vibecoding 工作站，包含工作流程、工具配置和最佳实践 | [link](https://github.com/tukuaiai/vibe-coding-cn) |
| EnzeD/vibe-coding | 《Ultimate Guide to Vibe Coding V1.2》，系统化的 AI 驱动开发指南，强调结构化规划、记忆库管理和迭代测试，避免 AI 失控，实现高效模块化的 Vibe Coding，适用于游戏和应用开发 | [link](https://github.com/EnzeD/vibe-coding) |
| Doloffer Guide优惠价GPT  claude会员充值 | 正版订阅 售后无忧，https://doloffer.com 9折优惠码：AI8888 https://github.com/Doloffer-g/guide/blob/main/README.md | [link](https://doloffer.com) |

## 🙏 Acknowledgement
* [Awesome Vibe Coding](https://github.com/filipecalegario/awesome-vibe-coding) ：一个精选的vibe coding参考列表，专注于通过AI协作编写代码，包括工具、概念和提示工程指南。



# 许可证

本项目采用 MIT 许可证 - 详情请见 `LICENSE` 文件。
## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ShouZhengAI/CS146S_CN&type=Timeline)](https://star-history.com/#ShouZhengAI/CS146S_CN&Timeline)
