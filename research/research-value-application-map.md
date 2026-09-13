# 研究价值与应用地图

## 字多不看

- 当前研究体系已经覆盖 36 个独立外部仓库研究域，36 个均已完成 L2 深度研究。
- 这些研究不是为了介绍外部项目，而是为了把外部项目拆成可验证事实、核心机制、迁移边界和本仓可执行改进项。
- 36 个研究域的 `analysis.md` 已统一为对标拆解、改良迭代、可迁移清单、不可迁移清单和验证动作格式。
- 36 个研究域的 `deep-dive.md` 已补齐 L2 证据层、关键机制、迁移边界和 L3 验证任务。
- 用户获得的直接价值是少走弯路、看见范式、拿到可落地路线。
- 本仓获得的直接价值是形成 `getting-started`、`references`、`workflow`、`skills`、`assets`、`scripts`
  和 `research` 的改进输入。
- 新增的 [研究迁移综合](research-transfer-synthesis.md) 专门回答“这些研究怎么变成可执行动作”。
- 研究结论稳定后必须下沉，不应长期停在 research。

## 当前覆盖

| 层级 | 数量 | 状态 | 说明 |
|:---|---:|:---|:---|
| 研究域 | 36 | 已建立 | 每个外部仓库一个独立研究域，均有 raw 原始事实层、`analysis.md` 和 `deep-dive.md` |
| L2 深度研究 | 36 | 已完成 | 覆盖 coding agent、Agent runtime、插件、规格驱动开发、技能框架、课程、资源索引、项目实践、数学研究基础设施和归档工具样本 |
| L1 观察研究 | 0 | 已清空 | P3 仍是低采用优先级，不再代表研究深度缺口 |

## 用户能获得什么

### 研究到行动

用户不应该只看到“这个仓库值得研究”。每个研究对象都应该进一步提供：

- 对标拆解：成熟对象为什么有效。
- 改良迭代：本仓应该如何改成自己的版本。
- 杂交创新：多个对象的有效机制如何组合。
- 验证指标：下一步动作怎样判断成功或失败。

因此，研究阅读顺序应调整为：

1. 先读单个研究域的 `analysis.md`，拿到可迁移动作。
2. 再读 `deep-dive.md`，确认动作背后的证据。
3. 最后读 [研究迁移综合](research-transfer-synthesis.md)，理解多个对象如何组合成本仓路线。

### 少走弯路

用户不需要自己从大量仓库里判断哪些值得学、哪些只是资源堆、哪些适合照搬、哪些只能参考。
研究域已经把外部对象拆成：

- 对象是什么。
- 强项在哪里。
- 能借鉴什么。
- 不能照搬什么。
- 下一步应该沉淀到哪里。

这让用户从“到处收藏链接”转为“按证据选择路径”。

### 看见 AI Coding 的真实范式

这批研究共同说明：AI Coding 不是 prompt 技巧集合，而是一个工程系统。成熟形态通常包括：

- 上下文入口：`AGENTS.md`、`llms.txt`、规则文件、skills。
- 执行控制面：CLI、脚本、工具调用、沙箱、审批、Git 状态。
- 验证闭环：lint、test、link check、benchmark、human-in-the-loop。
- 资源治理：结构化资源表、状态字段、最后检查时间、归档策略。
- 学习产品：学习路径、demo、assignments、部署产出、可视化解释。

用户因此能理解：真正要学的不是“让 AI 写一段代码”，而是如何稳定地把目标、上下文、约束、
工具和验证交给 AI。

### 获得可执行路线

研究结果可以直接变成用户路线：

- 新手用户：按学习路径从第一个可部署产物开始。
- 开发者：按 Git、测试、脚本、agent 控制面建立可靠工作流。
- 维护者：按资源治理、metadata、AI 引用入口维护知识库。
- 高阶用户：按 skills、workflow、HITL、MCP、Agent 编排构建自己的 AI 工程系统。

## 核心启示

### 一、AI Coding 的底座是控制面

来自 `openai/codex`、`openai/plugins`、`openai/openai-agents-python`、`openai/openai-agents-js`、
`openai/openai-cookbook`、`aider`、`cline`、Gemini CLI、OpenHands、OpenCode、Goose 和 ECC 的共同启示是：成熟 coding agent 依赖控制面，而不是只依赖
聊天能力。

可迁移结论：

- `scripts/` 不是杂物间，而是仓库控制面。
- `AGENTS.md` 不是贡献说明，而是 Agent 上下文接口。
- `skills/` 不是 prompt 收藏，而是可复用能力单元。
- `metadata/` 和 `llms-full.txt` 是 AI 可读入口，不是附属索引。
- 高风险执行必须有权限、沙箱、审批、dry-run 或审计说明。
- Plugins/Skills 研究说明能力还需要来源、manifest、安装、启用、禁用和版本生命周期；Agents SDK、OpenHands、
  OpenCode、Goose 和 ECC 研究说明运行循环、工作区、后端、配置、权限、记忆和验证也必须有明确边界。

### 二、教程价值来自路径和产出

来自 `easy-vibe`、`vibe-vibe`、`CS146S_CN` 的共同启示是：教程不是内容越多越好，而是路径越清楚、
产出越具体、验证越明确越好。

可迁移结论：

- 入门内容应先说明“你会做出什么”，再解释工具和概念。
- 学习路径应按用户身份、目标和阶段组织，而不是只按技术栈组织。
- 每个关键概念最好配 demo、assignment 或最小验证任务。
- 部署上线应进入早期路径，因为交付感会强化学习闭环。

### 三、资源索引必须治理化

来自 `awesome-claude-code`、`awesome-vibe-coding` 和本仓外部资源表的共同启示是：awesome list
只能做雷达，不能直接做采用结论。

可迁移结论：

- 资源必须有结构化主表。
- 资源必须有分类、来源、许可证、状态、最后检查时间和失效原因。
- 资源从发现到采用应经过 raw、analysis、deep-dive、下沉四步。
- 资源展示可以自动生成，但事实字段必须稳定。

### 四、实践项目是概念的验收层

来自 `ai-coding-lab`、`CS146S_CN` 和课程型仓库的共同启示是：没有实践项目，概念会停在认知层；
没有测试和验收，实践会停在演示层。

可迁移结论：

- concepts 负责解释概念。
- workflow 负责执行过程。
- references 负责模板和清单。
- practice 或 examples 负责可运行验证。
- research 负责未稳定的外部对象。

### 五、Agent 工程会走向任务系统

来自 `cline`、`aider`、`claude-code-best-practice`、`CS146S_CN` 的共同启示是：当模型能写代码后，
下一层瓶颈会变成任务拆分、上下文分发、状态管理、并行执行、人工审批和结果验收。

可迁移结论：

- 单次提示不是最终形态，任务树和工作流才是长期形态。
- HITL 不是低效，而是高风险节点的责任边界。
- Agent 编排的核心不是“多个 Agent”，而是职责、输入、输出、依赖和验收标准。

### 六、规格先行会把 AI 编程从对话变成变更系统

来自 `github/spec-kit`、`Fission-AI/OpenSpec`、`obra/superpowers` 和 `addyosmani/agent-skills` 的共同启示是：
复杂任务需要把规格、计划、变更、实现、测试和收敛拆成可追踪阶段；短命令或 Skill 只是入口，不能替代规格和证据。

可迁移结论：

- 规格、临时变更和稳定知识应分层保存。
- 生命周期入口应映射到明确的产物和验证命令。
- Skill 必须有触发条件、输入输出、失败信号和独立评估。
- 不把第三方方法论或 Skill 原样当成本仓规则，先经过迁移边界审查。

### 七、极简工具和生命周期状态同样是工程能力

来自 `SWE-agent/mini-SWE-agent` 与 `continuedev/continue` 的共同启示是：工具面可以极简，但执行必须有界；
项目停止维护、只读或归档状态必须进入推荐判断，而不能只看 Star 和功能列表。

可迁移结论：

- 用最小工具面完成问题定位时，显式限制命令、时长、输出和退出条件。
- 研究对象的维护状态、最终版本和替代路径要和技术判断一起展示。
- 极简不等于无验证；线性轨迹仍需要测试、退出码和可复查证据。

## 研究到应用的转化矩阵

| 研究来源 | 用户价值 | 本仓应用位置 | 可执行产物 |
|:---|:---|:---|:---|
| `openai/codex` | 理解 coding agent 控制面 | `scripts/`、`skills/`、`references/` | 脚本风险分级、沙箱/审批清单、Agent 控制面模板 |
| `openai/plugins` | 理解 Codex 能力包和插件分发 | `skills/`、`assets/`、`metadata/` | 插件 manifest、来源审查、安装/回滚清单 |
| `openai/skills` | 理解技能目录从 catalog 到 plugin 的迁移 | `skills/`、`docs/workflow/` | Skill 生命周期、触发契约和弃用迁移规则 |
| `openai/openai-agents-python` | 理解 Agent、工具、护栏和追踪运行时 | `workflow/`、`references/` | 任务 Agent、工具契约、护栏和证据记录模板 |
| `openai/openai-agents-js` | 理解 TypeScript Agent 运行时和状态所有权 | `workflow/`、`skills/` | runner、工具审批、session、sandbox 和 tracing 契约 |
| `openai/openai-cookbook` | 理解官方示例如何变成可复现方法 | `getting-started/`、`references/` | 示例索引、复现前置条件和验证结果模板 |
| `github/spec-kit` | 理解规格驱动开发的阶段化流程 | `workflow/`、`references/` | 规格、计划、任务、实现和测试的阶段契约 |
| `Fission-AI/OpenSpec` | 理解变更提案、稳定规格和归档边界 | `workflow/`、`references/` | 变更目录、规格目录、验证和归档清单 |
| `google-gemini/gemini-cli` | 理解终端 Agent 的上下文、MCP 和负例评估 | `getting-started/`、`workflow/` | 非交互入口、上下文层级和安全评估样本 |
| `OpenHands/OpenHands` | 理解 Agent Canvas、工作区和后端适配 | `workflow/`、`references/` | Agent/工作区/后端边界和可恢复任务状态表 |
| `anomalyco/opencode` | 理解模型无关配置、权限和插件生命周期 | `getting-started/`、`references/` | plan/build、配置备份、权限和插件回滚清单 |
| `obra/superpowers` | 理解可组合 Skill 如何承载开发方法论 | `skills/`、`workflow/` | Skill 触发、TDD、审查和分支收尾清单 |
| `addyosmani/agent-skills` | 理解生命周期命令、上下文层级和技能评估 | `skills/`、`workflow/` | `/spec`、`/plan`、`/test`、`/review` 到 `/ship` 的入口契约 |
| `aaif-goose/goose` | 理解跨模型 Agent 的 provider、MCP 和工作区边界 | `workflow/`、`references/` | provider、工具、上下文和评估的边界表 |
| `continuedev/continue` | 理解只读项目的生命周期和迁移风险 | `research/`、`references/` | 维护状态、替代方案和过期引用检查 |
| `SWE-agent/mini-SWE-agent` | 理解极简问题修复 Agent 的有界执行 | `workflow/`、`references/` | Bash 工具面、退出码、轨迹和预算检查 |
| `affaan-m/ECC` | 理解多 coding agent 的 Harness、记忆和质量资产 | `skills/`、`workflow/`、`references/` | Harness 资产、记忆策略、安全和评估清单 |
| `vibe-mathing-cn-public` | 理解数学研究的候选/结果分层和证据闭环 | `workflow/`、`references/`、未来 skills | 问题契约、失败回执、有界工具运行时和研究快照清单 |
| `aider` | 理解 Git 驱动 AI 修改闭环 | `workflow/`、`references/` | AI 修改到提交的标准流程、文档 map / repo map 机制 |
| `cline` | 理解多入口 agent 平台 | `metadata/`、`llms.txt`、`skills/` | 人类入口、AI 入口、脚本入口、skill 入口的入口契约 |
| `awesome-claude-code` | 理解资源治理 | `assets/external-resources/` | 资源 schema、生命周期字段、资源校验脚本 |
| `claude-code-best-practice` | 理解方法论资产化 | `concepts/`、`workflow/`、`skills/` | 方法论分流规则、agent teams 任务编排契约 |
| `easy-vibe` | 理解课程产品化 | `getting-started/` | 按用户目标组织的新手学习路径 |
| `vibe-vibe` | 理解零基础路线 | `getting-started/`、`workflow/` | 基础/进阶/实践/持续追踪四层路径 |
| `awesome-vibe-coding` | 发现国际生态 | `assets/`、`research/`、`metadata/` | 候选资源雷达、关键词候选、P1/P2 研究候选 |
| `ai-coding-lab` | 理解项目矩阵 | `workflow/`、`references/`、`skills/` | 实践项目模板、Skill 打包和评测模式 |
| `CS146S_CN` | 理解 assignments 验证 | `getting-started/`、`workflow/` | prompt、tool calling、RAG、MCP、agent workflow 练习 |
| `ai-for-developers-awesome-vibe-coding` | 发现 Vibe Coding 工具族 | `assets/external-resources/`、`research/` | 工具分类词、候选资源和 P1/P2 研究候选 |
| `daotin-ai-coding` | 观察中文 AI Coding 主题 | `docs/concepts/`、`assets/external-resources/` | 高频关键词、资源候选和经验分流项 |
| `earyantle-vibe-coding-skill` | 理解最小 Skill 产品化骨架 | `skills/` | Skill 触发、输入输出、引用和发布检查清单 |
| `liyupi-ai-guide` | 降低中文大众用户的学习门槛 | `docs/getting-started/`、`assets/external-resources/` | 大众化解释、项目实战和工具候选筛选表 |
| `luzhenqian-ai-coding-lab` | 用项目矩阵承接概念实践 | `docs/workflow/`、未来实践层 | 最小实践项目模板和概念到项目映射 |
| `roocodeinc-roo-code` | 研究归档工具的模式和生命周期 | `research/`、`assets/external-resources/` | archived 标记、替代路径和模式/schema 观察记录 |
| `wendy7756-vibe-coding-guide` | 理解非程序员的入门障碍 | `docs/getting-started/`、`prompts/` | 人、AI、提示词、工具和环境的低门槛入口说明 |

## 优先应用清单

### P0：研究体系继续稳定

- 保持“一对象一研究域”。
- raw 原始事实层必须可复查。
- 动态事实只进 `domain.yml`。
- L1 写理解，L2 写源码/结构证据，L3 才迁入稳定文档。

### P1：重构用户学习路径

目标位置：`docs/getting-started/`

应落地产物：

- 用户身份分流：零基础、开发者、创业者、维护者、高阶 Agent 用户。
- 阶段分流：第一个产物、完整交付、质量门禁、Agent 工程、资源治理。
- 每阶段明确产出：能做出什么、如何验证、卡住看哪里。

### P1：建立 scripts 控制面

目标位置：`scripts/`

应落地产物：

- `manifest.yml` 或等价脚本登记表。
- 脚本风险等级：只读、写仓库、高风险、外部副作用。
- owner、输入、输出、dry-run、CI 状态和审计说明。
- Agent 可自动执行与必须人工确认的边界。

### P1：资源治理本地化

目标位置：`assets/external-resources/`

应落地产物：

- 资源 schema。
- active、stale、archived、removed 等生命周期状态。
- last_checked、license、source、category、risk 字段。
- 资源索引生成和校验流程。

### P2：实践项目和 assignments

目标位置：`docs/workflow/` 或未来独立实践层。

应落地产物：

- 最小实践项目模板。
- 每个项目包含目标、前置条件、运行命令、验收命令、常见失败。
- prompt、tool calling、RAG、MCP、workflow、HITL 的最小练习。

### P2：Skills 工程化

目标位置：`skills/`

应落地产物：

- Skill 触发条件、输入输出、验证方式。
- Skill 打包说明。
- Skill 评测提示词。
- Skill 归档和替代策略。

## 用户如何使用这些研究

| 用户类型 | 推荐读法 | 直接收益 |
|:---|:---|:---|
| 零基础用户 | 先读教程型研究，再走 getting-started | 知道从哪里开始、做出什么、如何验证 |
| 开发者 | 先读 Codex、Aider、Cline 深度研究 | 建立 AI 修改、测试、提交、回滚闭环 |
| 仓库维护者 | 先读资源治理和本仓自研研究 | 建立资源表、metadata、AI 引用入口和门禁 |
| Agent 高阶用户 | 先读 control plane、skills、workflow、HITL 相关研究 | 设计自己的 Agent 工作流和任务系统 |
| 内容贡献者 | 先读研究域治理契约和本地图 | 知道资料应该进入 research、references 还是 workflow |

## 不应该怎么用

- 不要把 awesome list 当作推荐结论。
- 不要把教程型仓库当作企业级工程规范。
- 不要把官方 agent 源码当作本仓必须复制的实现。
- 不要让 research 无限变厚；成熟结论必须下沉。
- 不要跳过 raw 事实层直接写判断。

## 下一步执行路线

1. 将本地图作为研究转化入口加入索引和 AI 引用入口。
2. 从 P1 应用清单中选择一个方向落地：学习路径、scripts 控制面或资源治理。
3. 每完成一个下沉方向，回到对应研究域补充 `decisions.md` 或下游链接。
4. P3 对象已经完成 L2 研究，但只在出现采用需求、生态变化或交叉证据时下沉到稳定层。
