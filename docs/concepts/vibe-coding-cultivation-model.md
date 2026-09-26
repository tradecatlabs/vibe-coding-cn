# Vibe Coding 修仙映射

## 字多不看

- V1 用修仙世界观描述 Vibe Coding 最基础的组成对象，只回答“有什么”。
- 人类修士对应 User / Operator；万魂幡是所有 AI 会话的集合；魂魄是其中一个会话，以 Session ID 标识。
- 修为对应 Model Capability / Intelligence；灵力对应 Token / Compute / Reasoning Budget。
- 功法对应 Harness / Rules / Skills / Workflow；法器对应 Tools / MCP / Browser / Shell / API。
- 七个对象可归纳为“人、魂、力、术与器”四层。

## V1 的目的

V1 用一套修仙世界观描述 AI 与 Vibe Coding 中最基础的组成对象。

它暂时不解释这些对象如何运行，也不讨论 Agent、任务执行或最终战力，只回答一个问题：

> 在 Vibe Coding 这套修仙世界里，最基础的东西分别是什么？

## 七个基础对象

| 修仙对象 | AI 对象 | 含义 |
|---|---|---|
| 人类修士 | User / Operator | 整个体系中的使用者和控制者。 |
| 万魂幡 | 全部 AI 会话的集合 | Pi、Claude Code、Codex 等工具中的全部 AI 会话。 |
| 魂魄 | 单个 Conversation / Session | 一个具体会话，以该会话的 Session ID 标识。 |
| 修为 | Model Capability / Intelligence | 模型本身在理解、推理、规划、生成和代码编写等方面的能力水平。 |
| 灵力 | Token / Compute / Reasoning Budget | AI 运行过程中可以投入的计算资源。 |
| 功法 | Harness / Rules / Skills / Workflow | 模型之外规定 AI 如何运行、如何思考和如何完成任务的方法体系。 |
| 法器 | Tools / MCP / Browser / Shell / API | AI 可以调用的外部工具。 |

### 人类修士

人类修士对应 User / Operator，代表 AI 系统之外的人类主体。

修士提出目标、选择模型、分配资源、配置功法、使用法器，并决定最终接受什么结果。

### 万魂幡

万魂幡对应**全部 AI 会话的总体集合**，包括 Pi、Claude Code、Codex 等工具中的会话。

万魂幡是集合，魂魄是集合中的基本单位。

### 魂魄

魂魄对应单个 Conversation / Session。当前 Pi 会话是一个魂魄，Claude Code 或 Codex 中的单个会话也各自是一个魂魄；每个会话以自己的 Session ID 标识。

不同魂魄拥有不同的历史，因此即使背后使用相同模型，也可能表现出完全不同的状态。

**这里的魂魄指单个会话，不指 Memory。**

### 修为

修为对应 Model Capability / Intelligence，表示模型本身在理解、推理、规划、生成、代码编写等方面能够达到的能力水平。

修为描述的是：

> 这个模型本身有多强。

不同模型即使拥有相同的灵力、功法和法器，也可能因为修为不同而产生不同表现。

### 灵力

灵力对应 Token、Compute 和 Reasoning Budget，代表 AI 运行过程中可以消耗的计算资源。

灵力描述的是：

> 能够投入多少计算资源。

因此，修为和灵力是两个不同维度：修为决定能力水平，灵力决定可以投入多少计算。

### 功法

功法对应 Harness、Rules、Skills 和 Workflow，代表模型之外、规定 AI 如何运行、如何思考和如何完成任务的一整套方法体系。

它可以包括：

- Harness
- System Rules
- Instructions
- Skills
- Workflow
- Orchestration

同样的模型，在不同功法下可以表现出完全不同的行为模式。

### 法器

法器对应 Tools、MCP、Browser、Shell、API、Database 和 Code Execution。

模型本身主要负责理解、推理和生成；法器让 AI 获得对外部世界进行操作的能力。

法器描述的是：

> AI 可以借助什么东西完成行动。

## V1 的四层结构

这七个基础对象可以进一步理解为四个层次：

| 层次 | 修仙对象 | 对应内容 |
|---|---|---|
| 人 | 人类修士 | 整个系统的使用者和控制者。 |
| 魂 | 万魂幡、魂魄 | 全部会话的集合，以及集合中的单个会话。 |
| 力 | 修为、灵力 | 模型能力与可以投入的计算资源。 |
| 术与器 | 功法、法器 | 模型之外的方法体系与外部工具。 |

> 人类修士执掌万魂幡，幡中藏有无数魂魄；魂有修为，运行需要灵力，并可借助功法与法器发挥能力。

## V1 的边界

V1 到这里为止，只定义“有什么”。至于这些对象如何运行，以及最终能够产生多大战力，留待后续版本讨论。
