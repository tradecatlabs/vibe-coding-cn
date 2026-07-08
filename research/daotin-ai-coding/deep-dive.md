# Daotin/ai-coding 深度研究

## 研究级别

- 当前级别：L2 结构深度研究。
- 研究对象：`Daotin/ai-coding`。
- 证据来源：本目录 `raw/` 下的 GitHub 元数据、README 快照、BACKUP 文章镜像和本地仓库工作树。
- 观察日期：2026-07-03。

## L2 结论

`Daotin/ai-coding` 的核心价值是中文 AI Coding 主题雷达。它把 Cursor、Claude Code、Codex、MCP、
AGENTS.md、OpenSkills、BMAD、Figma MCP、Prompt、UI 原型、验证技巧等实践话题集中在 README
和 BACKUP 文章镜像中，适合观察中文社区正在关心什么。

对本仓最重要的启发是：社区经验不能直接当标准，但可以作为关键词、问题清单和下沉任务的来源。
它的价值在“主题发现”，不在“工程规范定稿”。

## 本地证据

- `raw/repository/README.md`：按 AI 方法论、AI 工具、AI 经验、AI 科普、AI 实战、AI 思考、
  AI 提示词和 MCP 组织入口。
- `raw/repository/BACKUP/issue-18-ClaudeCode使用教程.md`：Claude Code 相关实践材料。
- `raw/repository/BACKUP/issue-26-Codex使用技巧.md`：Codex 使用技巧材料。
- `raw/repository/BACKUP/issue-41-一文搞懂MCP.md`：MCP 主题材料。
- `raw/repository/BACKUP/issue-44-AGENTS.md.md`：AGENTS.md 主题材料。
- `raw/repository/BACKUP/issue-45-MCP和AgentSkills的核心区别.md`：MCP 与 Agent Skills 对比材料。
- `raw/repository/BACKUP/issue-47-OpenSkills，AI编程助手的"Forge".md`：OpenSkills 主题材料。
- `domain.yml`：当前优先级为 P3，研究方向为 `workflow-methodology`。

## 关键机制

### Issue 到 README 的主题汇总

该仓库把分散文章和 issue 型内容汇总到 README。这个机制适合快速积累主题，但缺少版本化契约、
验证指标和稳定分类。

### 中文高频问题捕获

仓库覆盖了 MCP、AGENTS.md、Claude Code、Codex、BMAD、Figma MCP、Prompt 递归、AI 验证、
UI 原型等高频实践问题。这些主题可以反哺本仓的关键词系统和经验模块。

### 社区经验需要二次工程化

内容是经验集合，不是统一方法论。要进入本仓稳定层，必须重新拆成目的、对象、约束、输入、输出、
验证和失败条件。

## 可迁移模式

- 将 BACKUP 文章视为中文 AI Coding 关键词候选池。
- 把高频主题映射到 `docs/concepts/keyword-system.md`、`docs/workflow/` 和 `skills/`。
- 对 MCP、AGENTS.md、Skills、Codex、Claude Code 等主题建立“问题 -> 概念 -> 操作模板”链路。
- 将用户常见模糊需求整理为面试式 SPEC 生成流程。
- 将“告诉 AI 如何验证”类经验转成验证检查清单。

## 对本仓的影响

本仓可以从这个对象获得三类输入：

- 关键词输入：MCP、AGENTS.md、Agent Skills、BMAD、OpenSkills、Prompt 递归、验证。
- 流程输入：模糊需求访谈、AI 生成 SPEC、AI 自验证、UI 原型到实现。
- 资源输入：中文教程和工具文章候选资源。

这些输入应该进入研究域、关键词系统、资源候选表或 workflow 模板，而不是直接搬运为标准答案。

## 风险和待验证项

- 文章集合的质量不均，不能把单篇观点当作本仓规范。
- 部分主题变化很快，MCP、Codex、Claude Code 和 Skills 相关事实需要重新核验。
- README 聚合不等于治理，缺少状态字段、最后检查时间和验证记录。
- P3 定位应保留，除非某个主题在本仓形成明确采用需求。

## 下一步 L3 验证任务

- 从 BACKUP 中抽取 30 个高频关键词，和本仓关键词系统去重合并。
- 将“模糊需求让 AI 面试你形成 SPEC”整理为 workflow 候选模板。
- 为 MCP、AGENTS.md、Skills 三个主题建立概念边界说明，避免用户混用。
- 将 AI 验证技巧整理成一份最小 Debug 输入契约：预期、实际、最小复现、环境、验证命令。
