# Aider-AI/aider 深度研究

## 研究级别

- 当前级别：L2 源码/结构深度研究。
- 研究对象：`Aider-AI/aider`。
- 证据来源：本目录 `raw/` 下的 GitHub 元数据、README 快照和本地仓库工作树。
- 观察日期：2026-07-03。

## L2 结论

`Aider-AI/aider` 的核心不是“聊天式写代码”，而是终端里的 Git 驱动编辑循环。它把仓库状态、
代码上下文、编辑格式、命令执行、lint/test、模型配置和用户交互拆成独立模块，让 agent 的每次
修改都尽量落在可 diff、可回滚、可验证的 Git 工作流中。

对本仓最重要的启发是：AI 编码工具的质量边界，主要由编辑协议、仓库上下文选择、验证门禁和
Git 状态管理决定，而不是由提示词长短决定。

## 源码证据

- `raw/repository/aider/main.py`：CLI 主入口，负责把参数、模型、仓库和交互流程组装起来。
- `raw/repository/aider/args.py`：参数层，说明用户可控配置是产品接口的一部分。
- `raw/repository/aider/repo.py`：Git 仓库状态层，承载 diff、commit、dirty state 等行为。
- `raw/repository/aider/repomap.py`：仓库地图层，负责从代码库中压缩可用上下文。
- `raw/repository/aider/commands.py`：命令系统，承载终端内的人机交互入口。
- `raw/repository/aider/run_cmd.py`：本地命令执行层，连接 AI 建议和真实环境。
- `raw/repository/aider/linter.py`：lint 反馈层，把工具结果变成修复循环的一部分。
- `raw/repository/aider/models.py`：模型配置层，说明多模型支持需要独立治理。
- `raw/repository/aider/sendchat.py`：模型调用层，连接上下文、消息和模型响应。
- `raw/repository/aider/coders/base_coder.py`：coder 抽象基类，定义编辑策略共同边界。
- `raw/repository/aider/coders/architect_coder.py`：架构/规划型 coder。
- `raw/repository/aider/coders/editblock_coder.py`：基于 edit block 的局部编辑策略。
- `raw/repository/aider/coders/udiff_coder.py`：基于 unified diff 的编辑策略。
- `raw/repository/aider/coders/patch_coder.py`：基于 patch 的编辑策略。
- `raw/repository/tests/`：测试层，覆盖命令、仓库、lint、repo map 和核心工作流。

## 关键机制

### Git 是工作流中心

Aider 把 Git 状态放在核心位置。它不是让 AI 随意改文件，而是围绕当前仓库、diff、commit、
脏工作树和可回滚状态组织工作。这一点适合所有 coding agent：写代码只是动作，Git 才是
工程协作的事实边界。

### 编辑格式是产品接口

`coders/` 中存在多种 coder：whole file、edit block、unified diff、patch、architect 等。
这说明“AI 如何表达修改”不是实现细节，而是影响可靠性、可审查性和失败模式的产品接口。

### repo map 是上下文压缩层

`repomap.py` 体现了一个关键设计：大仓库不能简单把所有文件塞进上下文，必须有面向任务的结构化
摘要和检索策略。上下文质量决定修改质量，垃圾上下文会直接制造垃圾结果。

### lint/test 是反馈回路

`linter.py`、`run_cmd.py` 和测试目录说明 Aider 将工具反馈接入循环。成熟 agent 不只是生成补丁，
还要能读取失败、缩小范围、再次修复。

## 可迁移模式

- 将“编辑格式”视为正式协议：全文件、diff、patch、结构化 block 的适用边界要写清楚。
- 将 Git 状态作为 AI 修改的事实源：修改前检查 dirty state，修改后保留 diff 和验证证据。
- 为大文档/大仓库建立 repo map 或文档 map，而不是让 AI 盲读整个仓库。
- 把 lint、test、link check 和脚本校验结果作为修复循环输入。
- 对不同任务区分规划型、编辑型、审查型和问答型 agent 行为。

## 对本仓的影响

本仓现在已经有 Markdown 门禁、链接检查、raw 研究域和 AI 引用入口。Aider 的模式提醒我们：

- 文档修改也需要 Git 状态意识，避免把用户未提交修改误当作自己的改动。
- 大量 Markdown 文档需要“文档地图”，否则索引和引用会漂移。
- 研究域 L2/L3 产物应当可 diff、可审查、可回滚，而不是只在对话里口头总结。
- 提交前门禁应继续保持 `make test` 的统一入口。

## 风险和待验证项

- 本轮只做源码结构研究，没有运行 Aider 的测试套件或交互流程。
- Aider 的 Python 实现细节不应被本仓直接复制；本仓主要迁移工作流和治理边界。
- 不同编辑格式的真实成功率需要通过任务集 benchmark 验证，不能只靠结构判断。

## 下一步 L3 验证任务

- 为本仓建立“文档地图/研究地图”的生成或校验机制，降低长文档索引漂移。
- 把 Git dirty state、门禁命令和验证证据纳入研究域 closeout 模板。
- 在 `docs/workflow/` 沉淀“AI 修改 -> diff 审查 -> 门禁 -> 提交”的最小闭环。
- 对本仓常见 Markdown 修改任务设计小型 benchmark，比较全文件编辑和局部 patch 的稳定性。
