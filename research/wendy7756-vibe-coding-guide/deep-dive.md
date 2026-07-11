# wendy7756/vibe-coding-guide 深度研究

## 研究级别

- 当前级别：L2 结构深度研究。
- 研究对象：`wendy7756/vibe-coding-guide`。
- 证据来源：本目录 `raw/` 下的 GitHub 元数据、双语 README、模型文档、Prompt 文档和经验记录。
- 观察日期：2026-07-03。

## L2 结论

`wendy7756/vibe-coding-guide` 的核心价值是非程序员视角下的自然语言编程入口。它把 IDE/工具、
LLM、Prompt 和个人实践经验分开组织，并提供中英文内容，说明 Vibe Coding 的入门障碍首先不是
代码语法，而是用户能否把目的、模型、工具和提示词说清楚。

对本仓最重要的启发是：关键词和概念是进入系统的门。用户不理解模型、工具、Prompt、部署和反馈，
就无法稳定触达 Vibe Coding 的真实能力。

## 本地证据

- `raw/repository/README.md` 和 `raw/repository/README_EN.md`：中英文入口。
- `raw/repository/LLMs/abstract.md`：模型说明入口。
- `raw/repository/LLMs/claude-sonnet-4.md`、`raw/repository/LLMs/gpt-4.1.md`、
  `raw/repository/LLMs/gemini-2.5-pro.md`、`raw/repository/LLMs/o3.md`：模型分项说明。
- `raw/repository/Prompts/NLP-guide.md`：自然语言提示词指南。
- `raw/repository/my-experience/web-experience.md`：Web 实践记录。
- `raw/repository/my-experience/ios-app-experience.md`：iOS 实践记录。
- `raw/repository/my-experience/verceldeploy.md`：部署经验记录。
- `domain.yml`：当前优先级为 P3，研究方向为 `cn-onboarding`。

## 关键机制

### 模型、工具、Prompt 分层

仓库把 LLM 文档、Prompt 指南和实践经验分开。这个分层适合新手理解：模型是能力边界，工具是执行
环境，Prompt 是表达接口，项目经验是反馈闭环。

### 非程序员表达优先

该对象的阅读对象不是传统开发者。它强调自然语言、工具选择和实践经验，说明入门内容不能默认用户
已经掌握工程术语。

### 双语入口降低传播门槛

README 和部分文档提供中英文版本，适合让内容在更大范围内被理解。对本仓而言，双语不是当前硬需求，
但“术语可解释、概念可翻译”是长期优势。

## 可迁移模式

- 在 `getting-started/` 中补充非程序员入口：目的、工具、模型、Prompt、反馈、部署。
- 把模型、工具、提示词、项目经验作为不同层级讲解，避免用户混为一谈。
- 将“自然语言如何表达需求”连接到本仓关键词系统。
- Debug 输入继续压成“预期 vs 实际 + 最小复现 + 环境 + 验证命令”。
- 对非开发者内容强调结果和验证，不把他们提前拉进实现细节。

## 对本仓的影响

该对象能帮助本仓回答一个关键问题：不会编程的人怎么开始？

- 先让用户描述结果，而不是学习全部工程概念。
- 再让用户区分模型、工具和提示词，避免把所有失败都归因于 AI 不行。
- 最后引入最小复现、部署和验证，完成从表达需求到交付结果的闭环。
- 关键词系统应承担“概念入口”的角色，不理解关键词就难以触摸对象。

## 风险和待验证项

- 个人经验文档不能直接上升为普适方法论。
- 模型版本和能力变化很快，具体模型评价必须重新核验。
- 非程序员路径不能牺牲验证门槛，结果仍需测试、预览或部署证据。
- 本仓不应变成工具评测站，工具和模型只作为任务路径的一部分。

## 下一步 L3 验证任务

- 为非程序员新增一条最小路径：描述结果、选择工具、生成、验证、修正、发布。
- 将模型、工具、Prompt、部署、反馈整理进关键词系统的入门概念组。
- 抽取个人实践中的失败场景，改写成本仓 Debug 最小输入模板。
- 设计一个“只描述结果”的入门练习，验证用户能否用 AI 产出可检查作品。
