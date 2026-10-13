# obra/superpowers 深度研究

## 研究级别

- 当前级别：L2 技能框架与开发方法论研究。
- 研究对象：obra/superpowers。
- 证据来源：本目录 raw/ 下的 README、skills、插件 manifest、docs 和 tests。
- 观察日期：2026-09-08。

## L2 结论

Superpowers 的工作流顺序是 brainstorming -> using-git-worktrees -> writing-plans -> executing/subagent development -> TDD -> requesting review -> finishing branch。其核心不是把所有任务自动化，而是把阶段责任和质量门禁写成可触发的 skill。Codex plugin manifest 让同一能力具备可发现、可安装的分发边界。

## 关键机制

### 方法论作为能力包

.github/skills/ 下每个目录拥有独立 SKILL.md，覆盖一个清晰动作。技能文本、插件入口和行为测试分离，便于跨 harness 适配。

### 阶段而非巨型提示词

头脑风暴、计划、实现、测试、审查和收尾不是一段长 prompt，而是连续的小型契约。这降低了上下文负担，也让失败可以停在一个明确阶段。

### 跨 harness 分发

.codex-plugin、.claude-plugin、.cursor-plugin、.opencode 等目录将能力本体与平台适配分离。通用方法保持一份，平台入口单独维护。

### 验证前置

verification-before-completion 和 tests/ 说明完成声明必须有证据。这个原则与本仓“质量门禁高于口头保证”一致。

## 可迁移模式

- 为本仓已有 auto-* skill 补最小触发和完成契约，不新增同义技能。
- 将 workflow 的阶段输出设计成可被下一个阶段直接读取的文档。
- 对插件、软链接或安装脚本标注副作用和撤销路径。
- 为关键 skill 添加至少一个负例：何时不该触发、何时必须停。

## 迁移边界

- 本仓遵循单 Agent 主路径；外部 subagent 方案仅作为对标。
- worktree、插件 marketplace 和自动安装不是本仓研究门禁的前置。
- 外部技能许可证允许使用不等于允许无审查复制其指令。

## L3 验证任务

1. 抽样 auto-review、auto-debug 和 auto-skill，比较触发/输出/验证契约完整度。
2. 为其中一个 skill 写最小负例并接入现有目录检查。
3. 评估是否能通过一个现有 skill 覆盖需求，避免新增重复能力。
