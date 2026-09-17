<a id="learning-map"></a>
<a id="1-学习地图"></a>

# 学习地图

> 用一张地图把 `vibe-coding-cn` 的学习路线串起来：先从零开始跑通，再按目标进入 Prompt、Skill 或工程质量路线。

### 核心摘要

- 如果你是新手，先走“零基础路线”，目标是完成一次从想法到可运行项目的闭环。
- 如果你已经会编程，先走“开发者路线”，目标是把 AI 编程变成可复用、可验证、可维护的工程流程。
- 如果你要带团队，先走“团队路线”，目标是统一上下文、产物模板、任务拆解、审查和门禁。

### 路线总览

| 路线 | 适合谁 | 目标 | 首选入口 |
|:---|:---|:---|:---|
| 零基础路线 | 不会编程或刚开始 | 跑通从想法到项目的最小闭环 | [问题求解](../concepts/problem-solving.md) / [状态转移闭环](../concepts/vibe-coding-state-transition.md) |
| 开发者路线 | 已会写代码 | 建立 AI 结对编程工作流 | [Vibe Coding 经验](vibe-coding-experience.md) / [状态转移闭环](../concepts/vibe-coding-state-transition.md) |
| Prompt 路线 | 想提升提问质量 | 把需求表达成可执行指令 | [提示词库](../../prompts/README.md) |
| Skill 路线 | 想沉淀复用能力 | 把高频任务做成可重复调用的技能 | [Skills 技能大全](../../skills/README.md) |
| 质量门禁路线 | 担心 AI 乱写代码 | 用测试、CI、schema、清单约束 AI 输出 | [工程实践](../references/project-architecture-template.md) |

### 路线一：零基础路线

目标：完成一次“想法 -> 需求 -> 方案 -> 任务 -> AI 编码 -> 验证 -> Git 保存”的最小闭环。

1. [问题求解](../concepts/problem-solving.md)
   先学会把问题说清楚：目标、现状、差距、标准、约束、对象、路径。
2. [Vibe Coding 状态转移闭环](../concepts/vibe-coding-state-transition.md)
   再把目标、约束、行动、证据和版本串成一轮可验证、可回滚的状态转移。
3. [网络环境配置](network-environment.md)
   先解决访问 OpenAI、GitHub、文档和依赖源的问题。
4. [CLI 配置](cli-setup.md)
   配置并登录 Codex CLI，让本地 Agent 能在终端里执行工程动作。
5. [开发环境搭建](development-environment.md)
   优先交给 Codex Agent 主动检查和配置 Git、Node.js、Python、编辑器、项目依赖与测试命令。
6. [Vibe Coding 经验](vibe-coding-experience.md)
   学会人机分工、门禁、复盘和用 AI 审 AI。
7. [第一个项目](first-project.md)
   用本地待办清单走通需求、实现、运行、验收和 Git 保存。

完成标准：

- [ ] 能清楚描述一个项目目标
- [ ] 能让 AI 生成初版 PRD 或任务清单
- [ ] 能在本地打开项目目录
- [ ] 能用 AI CLI 执行一次修改
- [ ] 能按验收清单验证功能和边界
- [ ] 能用 Git 保存一次变更并记录提交号

### 路线二：开发者路线

目标：把 AI 从“临时助手”变成稳定的工程协作者。

1. [Vibe Coding 状态转移闭环](../concepts/vibe-coding-state-transition.md)
   先建立目标、约束、行动、证据和版本组成的总模型。
2. [Vibe Coding 经验](vibe-coding-experience.md)
   再建立人机分工和质量意识。
3. [拼好码](../concepts/glue-coding.md)
   优先复用成熟能力，把自研代码限制在连接、编排、适配和业务逻辑。
4. [工程实践](../references/project-architecture-template.md)
   在任务开始前写清楚目标、边界、禁止项、验收标准和门禁，并用底层程序逻辑检查项约束实现质量。

完成标准：

- [ ] 每个任务都有明确验收标准
- [ ] 每次 AI 输出都能被测试、脚本或清单验证
- [ ] 不让 AI 无依据重构或造轮子
- [ ] 能把一次失败整理成可复用经验

### 路线三：Prompt 路线

目标：把自然语言需求写成可执行、可检查、可复用的指令。

1. [提示词库入口](../../prompts/README.md)
2. [工程实践](../references/project-architecture-template.md)
3. [语言层要素](../concepts/language-layers.md)
4. [问题求解](../concepts/problem-solving.md)

练习方式：

- 把“我要做一个功能”改写成“目标、约束、输入、输出、验收标准”
- 把“帮我优化”改写成“按哪些指标优化、不能改什么、如何验证”
- 把“检查一下”改写成“按什么清单审查、输出什么格式、什么情况阻断”

### 路线四：Skill 路线

目标：把高频工作沉淀成可重复使用的能力。

1. [Skills 技能大全](../../skills/README.md)
2. [auto-skill](../../skills/auto-skill/SKILL.md)
3. [Claude 官方 Skills](../../skills/claude-official-skills/)

完成标准：

- [ ] 每个 Skill 都有清晰触发场景
- [ ] 每个 Skill 都说明输入、流程、输出和验证方式
- [ ] 复杂能力有 references、scripts 或 assets 支撑
- [ ] Skill 不只是长提示词，而是可执行工作流

### 路线五：团队路线

目标：让多个人和多个 AI Agent 使用同一套上下文和门禁。

优先阅读：

1. [AGENTS.md](../../AGENTS.md)
2. [工程实践](../references/project-architecture-template.md)

团队约束：

- 任务开始前必须写清目标、边界、验收标准
- 重要产出必须新开会话做 AI 审计
- 任何目录、命令、配置、工作流变化都要同步文档
- 任何自研偏离拼好码原则都要说明理由、风险和回滚路径

### 建议顺序

如果你不知道从哪里开始，按这个顺序：

```text
问题求解
  -> Vibe Coding 状态转移闭环
  -> 网络环境配置
  -> Codex / ChatGPT 订阅与登录准备
  -> Codex CLI 配置
  -> 让 Codex Agent 主动配置开发环境
  -> Vibe Coding 经验
  -> 第一个项目
  -> 拼好码
  -> 工程实践
  -> Skills 技能大全
```

### 下一步

- 新手：回到 [学习地图](learning-map.md)，从第 0 步开始；环境就绪后完成 [第一个项目](first-project.md)。
- 开发者：阅读 [Vibe Coding 经验](vibe-coding-experience.md)，再选择 Skill 或质量门禁路线。
- 团队：先统一 [AGENTS.md](../../AGENTS.md)、强前置条件和质量门禁。
