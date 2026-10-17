# addyosmani/agent-skills 深度研究

## 研究级别

- 当前级别：L2 生命周期技能与评估研究。
- 研究对象：addyosmani/agent-skills。
- 证据来源：本目录 raw/ 下的 README、skills、commands、agents、references、evals 和 plugin 入口。
- 观察日期：2026-09-08。

## L2 结论

该仓库把技能分成 Meta、Define、Plan、Build、Verify、Review 和 Ship 等阶段，并通过 context hierarchy 约束加载顺序。它还把同一套 skill 适配到 Codex、Claude Code、OpenCode、Gemini CLI 和其他工具。最有价值的结构是“阶段入口 + 共享检查清单 + 行为评估”，而不是技能数量。

## 关键机制

### 生命周期命令是导航层

/spec、/plan、/build、/test、/review 和 /ship 把复杂技能库压缩成可记忆入口。用户先描述正在做什么，再由入口选择专业 skill。

### 上下文层级

context-engineering 将规则文件、规格/架构、相关源码、错误输出和对话历史分层，强调既不能缺上下文，也不能把整份规格全部塞给 Agent。

### 共享 references 的可移植性问题

README 明确提示单 skill 安装可能缺少仓库级 references。这是一个真实的分发风险：能力本体和共享资料若没有绑定，安装结果可能“看似成功、实际不完整”。

### Evals 作为独立证据

evals/ 将技能行为和 fixture 分离出来，允许验证技能是否改变行为，避免只看 skill 文案。

## 可迁移模式

- 为本仓 docs、prompts、skills 建立任务到入口的映射表。
- 对共享 references 做路径存在和覆盖检查。
- 让重要 skill 有正例、负例和结果判定。
- 把验证、审查和发布保持为独立阶段。

## 迁移边界

- 本仓不需要迁入多平台插件目录。
- 不把外部仓库的“25 skills”数字写成质量指标。
- 自动执行仍受本仓 AGENTS、权限和真实证据约束。

## L3 验证任务

1. 检查本仓 .github/skills/README.md 是否能按目标找到 owner skill。
2. 为一个高风险 skill 增加共享资源覆盖和路径门禁。
3. 用一个小型行为 fixture 验证 skill 的输出是否满足契约。
