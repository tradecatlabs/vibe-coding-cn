# filipecalegario/awesome-vibe-coding 深度研究

## 研究级别

- 当前级别：L2 源码/结构深度研究。
- 研究对象：`filipecalegario/awesome-vibe-coding`。
- 证据来源：本目录 `raw/` 下的 GitHub 元数据、README 快照和本地仓库工作树。
- 观察日期：2026-07-03。

## L2 结论

`filipecalegario/awesome-vibe-coding` 是国际 Vibe Coding 生态雷达。它的价值不在深度评测，
而在给出工具、平台、社区、任务管理和 AI coding 文档的横向分类视图。

对本仓最有价值的是分类体系和候选研究对象发现；它不应被当作推荐结论本身，因为 awesome list
缺少采用标准、风险等级、最后验证时间和本地事实层。

## 源码证据

- `raw/repository/README.md`：英文主清单，包含概念、工具、社区和文档分类。
- `raw/repository/README-CN.md`：中文入口。
- `raw/repository/README-JP.md`：日文入口。
- `raw/repository/README-KR.md`：韩文入口。
- `raw/repository/README-PT.md`：葡萄牙文入口。
- `raw/repository/contributing.md`：贡献规则。
- `raw/repository/code-of-conduct.md`：社区行为准则。
- README 分类包含 Browser-based Tools、IDEs and Code Editors、Mobile Apps、Plugins and Extensions、
  Local Apps、Command Line Tools、Task Management for AI Coding、Documentation for AI Coding、
  Communities & Job Boards、News and Social Media。

## 关键机制

### 分类是主要价值

awesome list 的第一价值是让读者知道生态里有哪些类型，而不是判断哪个最好。它适合作为资源雷达，
不适合作为采购或采用决策。

### 多语言 README 承担传播

多语言 README 说明 Vibe Coding 已经不是单一英文社区话题。它可以帮助本仓观察术语翻译、
跨语境表达和中文语境下哪些词需要本地化。

### AI coding 文档成为独立分类

清单中单独列出 Documentation for AI Coding，说明 `AGENTS.md`、`llms.txt`、rules、prompt
template、design docs 等已经从辅助材料变成生态基础设施。

### 任务管理进入 Agent 生态

Task Management for AI Coding 分类说明，当 agent 能写代码后，下一层需求会变成任务拆分、
并行执行、进度可视化、工作树隔离和验收管理。

## 可迁移模式

- 本仓外部资源表应吸收其工具族分类，但必须补足状态、来源、最后检查和风险字段。
- `research/` 可以用该清单发现新的 P1/P2 候选研究对象。
- 关键词系统应吸收 browser tools、AI IDE、CLI agents、task management、AI coding docs 等分类。
- 对国际资源不直接翻译推荐，先做本地可用性、网络、支付、中文支持和维护状态验证。

## 对本仓的影响

本仓应把它定位为“资源发现层”，而不是“权威推荐层”：

- 发现新对象：进入 `assets/external-resources/` 或 `research/`。
- 验证对象：拉 raw，建研究域，写 analysis/deep-dive。
- 稳定对象：下沉到 concepts、references、workflow 或 skills。

这个三段流比直接复制 awesome list 更适合长期维护。

## 风险和待验证项

- 清单缺少结构化元数据，无法直接判断活跃度、许可证、风险和适配中文用户的程度。
- 部分工具可能已经更名、停更或商业策略变化，需要重新核验。
- 本轮没有逐条验证清单链接和工具可用性。

## 下一步 L3 验证任务

- 从清单中抽取 coding agent、task management、AI coding docs 三类候选资源。
- 将候选资源进入 `assets/external-resources/`，补齐状态和检查时间。
- 对高价值工具建立单独研究域，而不是继续堆在资源清单。
- 将国际术语映射到本仓关键词系统。
