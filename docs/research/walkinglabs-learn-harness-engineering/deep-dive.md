# walkinglabs/learn-harness-engineering 深度研究

## 研究级别

- 当前级别：L2 结构深度研究。
- 研究对象：`walkinglabs/learn-harness-engineering`。
- 证据来源：本目录 `raw/` 下的 GitHub 元数据、README 快照和本地仓库工作树。
- 观察日期：2026-07-04。

## L2 结论

`walkinglabs/learn-harness-engineering` 的成熟点在于：它没有把 Harness Engineering
讲成“写更好的提示词”，而是讲成一套围绕 Agent 的工程控制系统。

它的结构从上到下是四层：

1. 课程叙事层：README、VitePress 首页、12 讲解释为什么 Agent 会失败。
2. 项目实验层：6 个递进项目在同一个 Electron 知识库应用上逐步增加 Harness 机制。
3. 资源模板层：`AGENTS.md`、`feature_list.json`、`init.sh`、进度、交接、评估表可直接复制。
4. 工具执行层：`skills/harness-creator` 和 `tools/audit-harness.sh` 把课程结论转成生成与审计能力。

这对本仓的启示是：研究报告不能只说“应该更可靠”，而要把可靠性拆成仓库 artifact、
状态机、门禁命令、评分表和会话交接。

## 源码证据

- `raw/repository/README.md`：主叙事入口，包含 Harness 五子系统、学习路径、12 讲、6 项目和资源库。
- `raw/repository/docs/en/index.md`：站点入口，把课程分成 lectures、projects 和 resource library。
- `raw/repository/docs/en/lectures/lecture-02-what-a-harness-actually-is/index.md`：定义五子系统模型。
- `raw/repository/docs/en/lectures/lecture-03-why-the-repository-must-become-the-system-of-record/index.md`：强调仓库是真相源。
- `raw/repository/docs/en/lectures/lecture-08-why-feature-lists-are-harness-primitives/index.md`：把 feature list 定义为 Harness 原语。
- `raw/repository/docs/en/lectures/lecture-10-why-end-to-end-testing-changes-results/index.md`：把全链路验证和可执行架构规则绑定。
- `raw/repository/docs/en/resources/templates/AGENTS.md`：给出启动流程、工作规则、完成定义和会话结束动作。
- `raw/repository/docs/en/resources/templates/feature_list.json`：提供带状态、验证和证据字段的功能状态机。
- `raw/repository/docs/en/resources/templates/init.sh`：统一安装、基线验证和启动命令。
- `raw/repository/docs/en/resources/templates/evaluator-rubric.md`：把产出验收转成评分表。
- `raw/repository/projects/project-06/solution/AGENTS.md`：完整项目末态的启动规则、边界、完成定义和清理要求。
- `raw/repository/projects/project-06/solution/feature_list.json`：完整项目用证据字段声明每个功能通过状态。
- `raw/repository/skills/harness-creator/SKILL.md`：将 Harness 创建、校验和报告生成封装成可复用 Skill。
- `raw/repository/tools/audit-harness.sh`：零依赖 shell 审计脚本，按五子系统检查现有仓库。
- `raw/repository/.github/workflows/deploy-pages.yml`：课程站点发布流程。
- `raw/repository/.github/workflows/release-course-pdfs.yml`：PDF 课程产物发布流程。

## 关键机制

### 五子系统把可靠性从感觉变成检查项

课程把 Harness 拆成 instructions、tools、environment、state、feedback。这个分法的价值是让“Agent
不可靠”不再是笼统抱怨，而能被定位成入口不清、工具不足、环境不可复现、状态不可恢复或反馈缺失。

对本仓而言，研究域可以沿用这个检查框架：

- Instructions：`AGENTS.md`、README、目录索引是否能让新 Agent 找到入口。
- Environment：依赖、版本、raw 拉取、Makefile 是否可复现。
- State：研究进度、任务状态和决策是否在仓库内。
- Feedback：`make test`、链接检查、结构检查是否足够表达完成标准。
- Tools：脚本、Skill 和 GitHub 流程是否被清楚登记。

### 仓库真相源减少跨会话猜测

Lecture 03 的核心不是“多写文档”，而是“把决策信息放到 Agent 能看到的位置”。它用 fresh session test
要求一个新会话仅凭仓库回答：系统是什么、如何组织、如何运行、如何验证、当前进度是什么。

本仓已经有 `AGENTS.md`、`llms.txt`、`assets/ai-citation/llms-full.txt` 和 docs 索引。缺口在于：
部分研究结论仍是散文式表达，尚未都转成可恢复状态和可执行验证。

### Feature list 是任务完成定义的机器接口

Lecture 08 把 feature list 从备忘录提升为 Harness 原语。核心不是 JSON 格式，而是四件事：

- 每个条目有可观察行为。
- 每个条目有验证命令或验证步骤。
- 每个条目有状态。
- 状态升级必须附带证据。

这比普通 TODO 更适合 AI 协作，因为 Agent 可以读取、选择、执行、验证、写回，而不是靠自然语言猜测
“差不多完成”。

### 全链路验证改变 Agent 行为

Lecture 10 的关键判断是：只跑单元测试会遗漏组件边界问题，完整管线验证会反过来约束 Agent 的实现方式。
它还强调把架构规则变成可执行检查，并把失败信息写成 Agent 能按步骤修复的反馈。

本仓当前 `make test` 已经包含 Markdown lint、链接、折叠块、docs 结构、metadata、AI 引用和 starter kit
检查。这是文档仓库的全链路验证雏形。下一步可以把研究域 raw 层、新研究域索引、目录 AGENTS 覆盖也纳入
更强的结构性检查。

### Skill 与审计脚本让课程可执行

`skills/harness-creator/SKILL.md` 说明这个仓库不满足于讲课。它提供创建、校验、报告、benchmark 的工具入口。
`tools/audit-harness.sh` 则从 shell 层给出五子系统审计。

这说明成熟研究对象应该至少有一条“从文章到工具”的路径。对本仓来说，Harness 研究成熟后应沉淀到：

- `docs/research/harness/`：概念、机制、对标与判断。
- `docs/workflow/`：日常执行流程和质量门禁。
- `scripts/`：可自动检查的规则。
- `skills/`：可复用的 Agent 操作能力。

## 可迁移模式

- 用五子系统表审计所有 Agent 协作入口。
- 用 fresh session test 检查新会话能否从仓库恢复上下文。
- 用 `feature_list.json` 的思想重构任务包和研究域进度，而不是复制固定文件名。
- 用 `init.sh` 的思想保持“一条命令得到基线状态”，本仓对应 `make test`。
- 用 `evaluator-rubric.md` 的思想要求重要产出必须有正确性、验证、范围、可靠性、维护性和交接评分。
- 用 `audit-harness.sh` 的思想把可重复的 review feedback 晋升为自动门禁。

## 对本仓的影响

本仓当前强项是中文知识库、研究域治理、索引、质量门禁和 AI 引用入口；该仓强项是把 Harness
讲成课程、练习、模板、Skill 和脚本。

两者结合后的方向应该是：

- `docs/research/harness/` 继续承载 Harness Engineering 概念与外部论文/文章对齐。
- `docs/research/walkinglabs-learn-harness-engineering/` 承载该课程仓库的一手研究。
- `docs/workflow/` 承载本仓实际如何使用 Harness 控制 AI 协作。
- `scripts/` 或 `skills/` 只在检查逻辑稳定后再接管自动化。

关键取舍是：吸收控制面和验证闭环，不复制其课程站点和多语言工程复杂度。

## 风险和待验证项

- 本轮没有运行外部仓库的 VitePress 构建、PDF 构建、Skill 脚本和审计脚本。
- 该仓库 star、fork、updated、topics 属动态事实，引用前必须重新核验。
- 其模板默认面向代码项目，本仓是 Markdown 知识库，迁移时必须改成文档治理和研究域治理语言。
- `skills/harness-creator` 作为外部 Skill 引入前需要单独做安全、依赖、许可证和维护成本评估。

## 下一步 L3 验证任务

- 在 `docs/research/harness/` 新增一份“最小 Harness 检查表”，用五子系统审计本仓。
- 为一个真实研究域试写 `id / behavior / verification / status / evidence` 状态表。
- 把一次重复出现的文档审查问题转成可执行脚本或 `make` 门禁。
- 抽样运行 `raw/repository/tools/audit-harness.sh` 对本仓评分，并记录哪些检查项需要为 Markdown 知识库改写。
