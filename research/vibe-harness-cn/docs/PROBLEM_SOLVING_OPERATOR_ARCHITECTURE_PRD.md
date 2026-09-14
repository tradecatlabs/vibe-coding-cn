# AI 问题求解算子库架构需求文档

- Working name：`Problem-Solving Operator Architecture`（PSOA）
- Document type：Product Requirements Document（PRD）
- Status：Active development
- Version：`0.3`
- Updated：2026-09-04

## 1. 一句话定义

PSOA 定义 Harness 内部的 Problem-Solving Operator Library：它把跨学科思维模型和方法论保存为
可发现、可组合、可执行、可验证、可追溯的 Operator，用来增强 LLM 的问题求解能力；共享规范
允许不同 Harness 在不共享内部运行时的前提下理解同一方法，并以各自的 Binding 执行。
换句话说，`Operator Library ⊂ Harness`，而 `Agent = LLM + Harness`。

## 2. 问题陈述

当前 AI 系统已经有模型、prompt、skill、tool、workflow、eval 和 trace，但缺少稳定的中间语义：

- `Debug`、`Falsify`、`Decompose`、`Ablate` 等方法常被写成自然语言提示，适用条件、状态变化、
  失败语义和证据要求无法机检。
- Tool 协议说明“可以调用什么”，却不说明“为什么现在应该调用、调用后应知道什么、什么证据
  足以继续”。
- Workflow 可以编排步骤，但往往把领域方法固化在单个实现中，难以跨模型和 Harness 迁移。
- 执行者容易把工具成功、自报完成或没有发现反例误判成任务成功。
- 方法来源分散在数学、计算机科学、软件工程、实验科学和机器学习中，缺少按问题求解职责组织的
  机器可读结构。

需要在 Harness 内建立明确的 Operator Library，把“领域知识是什么”与“遇到未知问题时应该
执行什么程序”分开。元 Harness 对共享规范、来源、版本、分发、conformance、eval 和生命周期
进行治理；具体 Harness 负责本地装载、选择、绑定、授权和执行。

## 3. 目标与成功定义

### 3.1 产品目标

1. 定义最小但完整的 Problem-Solving Operator 语义。
2. 定义 Operator 组合为 Method、Method 实例化为 Plan 的规则边界。
3. 表达现实状态、认知状态和治理状态的变化，而不把非确定性推理伪装成确定性指令。
4. 把证据、失败、预算、停止、权限和 provenance 变成一等契约。
5. 使同一 Operator/Method 可被不同模型、工具集和 Harness Binding 使用。
6. 为未来 JSON Schema、conformance suite、共享目录和 Harness 内 Operator Library 提供稳定需求基线。

### 3.2 核心成功信号

- 同一版本的 Operator 可以被两个独立 Harness 集成解析，并保持相同的前置条件、结果类型、
  证据和失败语义。
- Harness 可以在执行前确定 Operator 是否适用，在执行后产生结构化 Observation 和 Evidence。
- 每个 Harness 可以按版本装载自己的 Operator Library，并用本地 `OperatorBinding` 映射到模型、
  prompt、skill、tool 或 workflow，而不改变共享 `OperatorSpec` 的语义。
- Verifier 可以仅依据版本绑定的输入、结果和证据裁决 outcome，而不依赖执行者的自然语言自报。
- 一次运行可以被 provenance 记录完整重建：使用了什么、由谁执行、生成了什么、从何派生。
- 新增领域方法不要求修改核心运行时，只需新增合规 Operator/Method 定义及其本地 Binding。

## 4. 非目标

首版不负责：

- 训练或替代 LLM。
- 统一所有 Harness 的内部 agent loop、memory、tool API 或业务状态。
- 建设一个位于所有 Harness 之外、替它们选择和执行算子的中央运行时。
- 实现通用自动规划器、定理证明器、因果推断引擎或强化学习系统。
- 完整复制或宣称兼容 PDDL、HTN、BPMN、CMMN、DMN、Essence、W3C PROV。
- 把所有学科知识建设成 ontology 或百科全书。
- 让 Operator 定义授予权限、安装代码或绕过 Harness policy。
- 首版建设在线 registry service、数据库、Web UI、插件市场或多 agent 调度系统。
- 仅靠增加 operator 数量证明系统价值。

## 5. 用户与核心任务

| 用户 | 核心任务 | 期望收益 |
|---|---|---|
| Harness 平台工程师 | 让 Harness 查询、执行和报告标准 Operator | 减少每个运行时重复定义方法语义 |
| Operator 作者 | 把成熟方法提炼成可复用契约 | 方法可被发现、组合、测试和版本化 |
| Method/Workflow 设计者 | 把高层任务分解为 Operator 网络 | 组合逻辑不依赖单个 prompt 或模型 |
| Eval/TEVV 负责人 | 为结果定义证据与裁决规则 | 执行成功与问题解决明确分离 |
| 安全与治理负责人 | 审查权限、风险、来源和生命周期 | 算子不能借方法名逃逸运行时策略 |
| Agent 开发者 | 在任务状态上选择合适的方法 | 选择可解释、可回退、可观测 |

## 6. 全局定位与边界

```text
领域方法论
数学 / CS / 科研 / 软件工程 / ML
        │ 开采、归一化、评审
        ▼
Meta Harness Control Plane
Operator Specification / Catalog / Conformance / Evaluation / Lifecycle
        │ 发布版本、策略和验证结果
        ▼
Agent = LLM + Harness
              │
              └── Harness Runtime
                  ├── Instructions + Context / Memory
                  ├── Operator Library
                  │   ├── version-pinned MentalModelSpec / OperatorSpec / MethodSpec
                  │   ├── Harness-specific OperatorBinding
                  │   └── discovery / selection / materialization
                  ├── Tools + Permissions + Environment
                  ├── Loop / State / Planning
                  ├── Verification + Evidence
                  └── Observability + Provenance
        │ 上报声明、支持能力和版本绑定证据
        └──────────────────────────────> Meta Harness Control Plane
```

这里有四个不同对象，不能混用：

1. **Operator Specification**：跨 Harness 的公共语义和结构，由元 Harness 治理版本与 conformance。
2. **Operator Catalog**：可发布、检索、评测和淘汰的规范目录，是治理事实，不是业务执行状态。
3. **Operator Library**：某个 Harness 当前已装载、可供 Agent 使用的版本固定算子集合，属于该 Harness。
4. **OperatorBinding**：某个 Harness 如何把 Operator 落成 prompt、skill、模型调用、tool 或 workflow。

算子库保存的不只是提示词，而是完整的方法说明：来源、目标、适用与禁用条件、输入、步骤、预期
效果、结果类型、证据要求、失败与恢复、风险、预算、示例和反例。prompt/skill/tool 只是具体
Harness 的执行载体。

### 6.1 库内内容层级

```text
Operator Library
├── MentalModelSpec   如何观察和解释问题，例如不变量、二阶效应、偏差-方差
├── OperatorSpec      一次可调用动作，例如识别不变量、寻找反例、做消融
├── MethodSpec        多个 Operator 的组合，例如科学实验法、假设驱动调试
└── OperatorBinding   当前 Harness 如何把动作落成 prompt、skill、tool 或 workflow
```

不是所有思维模型都天然可执行。`MentalModelSpec` 是“怎么看”；`OperatorSpec` 是“现在做什么”；
`MethodSpec` 是“按什么顺序持续做”。只有带完整执行语义的 Operator/Method 才能直接进入计划；
思维模型必须通过显式 `apply_model` 关系被 Method 应用，或由具体 Operator Binding 显式引用后，
才能影响一次运行；它不能伪装成可执行 `use` 步骤。

### 6.2 相邻概念边界

| 概念 | 回答的问题 | 不拥有 |
|---|---|---|
| LLM | 如何生成、判断和推理？ | 权限、事实真相和完成裁决 |
| Tool | 可以对外部世界做什么？ | 方法适用性和任务成功语义 |
| Prompt | 如何向某个模型表达一次指令？ | 跨模型规范和生命周期 |
| Skill | 如何封装可触发的说明、资源和实现？ | 必然统一的状态转移和证据语义 |
| Operator | 当前可执行什么问题求解动作，它可能产生什么知识或状态？ | 自行授权和自证成功 |
| Method | 高层任务如何分解、约束和组合 Operator？ | 具体运行时调度状态 |
| Plan/Workflow | 本次问题实际按什么顺序执行？ | 可复用 Operator 的规范所有权 |
| Planner/Selector | 下一步选择哪个 Operator/Method？ | Operator 定义和执行权限 |
| Operator Library | 当前 Harness 已装载哪些思维模型和方法？ | 跨 Harness 的正式版本和治理结论 |
| Operator Catalog | 哪些共享规范可发布、支持、晋升或淘汰？ | 具体 Harness 的运行状态和本地 Binding |
| Harness | 如何装载算子、选择方法并安全执行？ | 跨 Harness 方法规范的治理真相 |
| Meta Harness | 如何统一规范、登记、分发、评测和治理 Harness/Operator？ | 具体业务任务和算子运行状态 |
| Verifier | 证据是否满足声明？ | 修改执行结果以制造 PASS |
| Provenance | 结果如何产生、从何派生？ | 对结果质量作最终判断 |

## 7. 设计原则

1. **语义先于 JSON**：先定义对象、状态和不变量，再选择序列化结构。
2. **方法与领域知识分离**：Operator 表达求解程序；领域事实作为输入、约束或引用资源。
3. **声明与执行分离**：规范声明语义；Harness Binding 负责把语义落实为模型与工具动作。
4. **规范与本地库存分离**：元 Harness 治理共享 Spec/Catalog；具体 Harness 拥有本地 Library/Binding。
5. **执行与验证分离**：Operator 声明 evidence contract；Verifier 拥有 outcome 裁决。
6. **三类状态分离**：world、knowledge、governance 不得压成一个模糊 `state`。
7. **非确定性显式化**：探索失败、预算耗尽和“未发现反例”不得等价为相反命题成立。
8. **权限由 Harness 拥有**：Operator 只能声明所需 capability 和风险，不能扩大实际授权。
9. **版本绑定**：定义、binding、输入、证据和结果必须绑定可识别版本。
10. **组合优于继承**：Method 通过前置条件、数据流与控制关系组合 Operator，不建立深层类型树。
11. **标准借鉴而非标准拼盘**：复用成熟语义，首版不承担完整外部标准兼容成本。

## 8. 核心领域模型

### 8.1 三类状态

| 状态 | 内容 | 示例 |
|---|---|---|
| `world_state` | 外部系统和 artifact 的可观察事实 | 文件版本、测试状态、服务配置 |
| `knowledge_state` | 已知、未知、假设、置信和被排除解释 | 根因候选、反例、测量结果 |
| `governance_state` | 权限、审批、策略、证据充分度和生命周期 | 已审批、待验证、被策略拒绝 |

三类状态可以关联，但必须独立更新。例如一次只读诊断可能不改变 `world_state`，却减少
`knowledge_state` 的不确定性；一次高风险修复即使技术执行成功，也可能因缺少审批而不能推进
`governance_state`。

### 8.2 核心对象与所有权

| 对象 | 核心职责 | 生命周期 owner |
|---|---|---|
| `Problem` | 描述问题实例、当前状态、目标、约束和未知量 | 调用方 / Harness |
| `State` | 提供三类状态的版本化快照或引用 | 对应事实源 owner |
| `Goal` | 定义可验证的目标条件和停止边界 | 调用方 / Policy |
| `MentalModelSpec` | 定义观察视角、核心概念、假设、问题清单、适用边界和来源 | Meta Harness / Operator Catalog |
| `OperatorSpec` | 定义原子求解动作的共享稳定语义 | Meta Harness / Operator Catalog |
| `MethodSpec` | 定义 compound task 的共享分解方法 | Meta Harness / Operator Catalog |
| `OperatorLibrary` | 保存某个 Harness 已装载的 Spec、内容、版本和可用状态 | Harness Runtime |
| `OperatorBinding` | 将共享 Spec 映射为本地 prompt、skill、模型、tool 或 workflow | Harness Runtime |
| `Plan` | 把 Method/Operator 绑定到当前 Problem | Harness Planner / Selector |
| `OperatorRun` | 记录一次实际执行及其输入输出 | Harness Runtime |
| `Observation` | 描述执行中观察到的事实，不直接宣称结论 | Runtime / Sensor |
| `Evidence` | 将 Observation 与可检查声明绑定 | Verifier / Evidence store |
| `Outcome` | 对成功、失败、未知、阻塞等结果的结构化裁决 | Verifier |
| `ProvenanceRecord` | 记录 entity、activity、agent 和 derivation | Provenance owner |

### 8.3 最小生命周期

```text
Task -> Harness receives Problem + State + Goal
        │
        ▼
discover/select from local Operator Library
        │ applicability + policy/permission decision
        ▼
materialize Harness-specific OperatorBinding
        │ inject instructions/context and bind tools
        ▼
execute inside Harness loop
        │
        ▼
Observation + candidate Evidence
        │
        ▼
logically independent verification
   ┌────┼──────────┬─────────┐
success failure  unknown   blocked
   │       │         │         │
 next    compensate replan   approve/stop
        │
        ▼
state/provenance update + governance evidence report
```

Verifier 的“独立”是裁决职责独立，部署上可以是 Harness 内的隔离组件，也可以是外部评测服务；
它不能只复述执行模型的自评。元 Harness 消费版本绑定的声明与证据，不进入每次业务执行热路径。

## 9. Operator 语义需求

### 9.0 规范强度分层

本节描述成熟 Operator/Method 和运行时最终需要表达的能力，不等于这些内容全部是 Core JSON
Schema 的必填字段。字段强度分三层：

- **Core MUST**：稳定 envelope、字段类型、ID/version、`kind` 判别、`source_key` 条件、
  `extensions` 边界，以及权限/结果/sensitive owner 不可被内容作者改写。
- **Profile MAY/MUST**：特定库或场景可以要求来源、适用性、步骤、证据、失败、恢复、计数与词汇；
  Profile 必须显式命名和版本化，不能假装是公共 Core。
- **Runtime MUST**：装载、权限、预算、工具执行、Evidence 和 outcome 裁决由 Harness 强制；字段省略
  不能产生授权或成功结论。

因此，`draft` Core Pack 可以渐进补全语义；进入具体 Harness 执行或晋升前，再满足目标 Profile。
字段级规范见 [`OPERATOR_SPEC.md`](OPERATOR_SPEC.md)。

### FR-001 身份与版本

每个 Core 条目必须具有稳定 ID、语义版本、kind、origin、状态和显示名称。owner、来源与兼容性
建议在成熟 Profile 中声明。显示名称不能作为机器身份；破坏性语义变化必须产生新版本。

### FR-002 目的与适用范围

成熟 Operator 应声明它减少哪类不确定性或产生哪类状态变化，并写明适用场景、非适用场景和
已知能力天花板；Core 允许草稿渐进补全。

### FR-003 参数与输入

Core 应允许 Profile 为输入补充类型、artifact 引用、事实源引用和敏感引用；执行型 Profile 再要求
输入可类型检查。Secret 不得以内联值进入 Operator 定义、Plan 或 provenance。

### FR-004 前置条件

执行型 Profile 应要求 Operator 声明可机检前置条件，包括所需状态、证据、capability、权限级别
和资源。运行时发现前置条件不满足时不得静默执行，应产生结构化结果。

### FR-005 状态效果

Operator 声明效果时，应标明 `world_state`、`knowledge_state`、`governance_state` 或 Profile
定义的扩展状态。预期效果是可验证声明，不是执行成功后的自动事实。

### FR-006 Observation 与可能结果

执行型 Profile 应要求 Operator 声明可能产生的 Observation 和 outcome 集合；推荐公共词汇包括：

- `succeeded`
- `failed`
- `inconclusive`
- `not_applicable`
- `blocked`
- `budget_exhausted`
- `cancelled`

具体 Operator 可以收窄或扩展，但不能改写公共词汇语义。

### FR-007 执行绑定

规范必须允许一个 Operator 对应多个 `OperatorBinding`。Binding 属于具体 Harness，声明本地模型、
prompt/skill、tool capability、环境和输入输出映射，但实现细节不能改变 Operator 的共享规范语义。

### FR-008 证据契约

可验证 Profile 应要求 outcome 声明主张、证据类型、来源、freshness、版本绑定、判定规则和证据
不足时的结果。Core 不以字段齐全冒充证据充分；自然语言总结也不能替代结构化证据。

### FR-009 失败、恢复与补偿

Core 允许 Operator 渐进声明可预期失败类别、重试条件、幂等性、可逆性、补偿动作、checkpoint
要求和不可恢复条件；有副作用的执行型 Profile 必须补齐相关项。重试不得默认无限，补偿不得
假装能够撤销现实世界中不可逆的副作用。

### FR-010 预算与停止

规范应支持由 Profile 或 Binding 声明时间、步骤、token、模型调用、外部调用、并发和费用预算，
以及正常停止、失败停止、人工介入和熔断条件；Core Pack 不要求每个条目重复填写全部预算维度。

### FR-011 风险与权限

Operator 只能声明最小所需 capability、资源范围、风险类别和建议审批点。最终允许、拒绝或审批
必须由 Harness policy 在运行时裁决；Operator 定义不能授予自己权限。

### FR-012 分类与发现

成熟 catalog 应优先按求解职责而非来源学科组织发现，并可支持以下检索维度；Core 的 `domain`
保持开放，不强制第三方采用本项目的分类树：

- 求解职责：表示、分解、搜索、构造、证伪、诊断、验证、优化、治理。
- 效果类型：world、knowledge、governance；执行控制属于 Plan/Harness 状态，不冒充 Operator 效果。
- 运行性质：确定性、随机性、幂等性、可逆性、交互性。
- 证据等级、风险等级、成本范围、成熟度和支持的 Harness/Binding。
- 来源领域作为 provenance 标签，而不是主目录层级。

## 10. Method、规划与控制需求

### FR-013 Method 分解

成熟 `MethodSpec` 应把 compound task 分解为更小的 Method 或 primitive Operator，并表达输入输出
绑定、前置条件、目标保持和终止条件。Core 允许 draft 无步骤；可执行 Profile 必须要求有限、
有向、可检查的结构。

### FR-014 控制关系

Method/Plan 必须能表达最小控制语义：顺序、选择、并行、循环上限、事件等待、重试、补偿、暂停、
取消和重新规划。首版不要求实现完整 BPMN/CMMN 图形语法。

### FR-015 选择可解释性

Planner/Selector 每次选择必须记录候选集合、适用性判断、选择依据、被淘汰路径和预算影响。
模型可以提出选择，但结构化 selector/policy 必须能够拒绝不适用或越权的候选。

### FR-016 数据与证据依赖

组合关系必须区分控制依赖、数据依赖和验证依赖。后续 Operator 只有在所需输入存在且上游证据
满足 freshness/quality 条件时才能进入 ready 状态。

### FR-017 重规划

当 Observation 推翻前提、结果不确定、预算不足或执行失败时，运行时必须能够保留已验证结果，
只使受影响计划子图失效，并选择补偿、替代 Method、人工介入或终止。

## 11. Harness、验证与 provenance 需求

### FR-018 Harness 算子库集成

Harness 必须把版本固定的 Operator/Method 装载进本地 Operator Library，并通过 `OperatorBinding`
完成规范对象与本地模型、tool、context、permission、state 之间的映射；必须报告不支持的
capability，不得用自由文本降级或假装兼容。

### FR-019 独立验证

执行者只能提交 Observation 和候选 Evidence。Verifier 根据 Operator 声明和项目 policy 产生
Outcome；高风险场景不得接受同一模型的无 provenance 自评作为独立验证。

### FR-020 Provenance

每次 Plan 和 OperatorRun 必须记录：使用的 entity、执行 activity、执行 agent/runtime、生成 entity、
派生关系、时间、版本和 digest。默认记录结构化元数据和脱敏引用，不强制保存完整 prompt 或工具结果。

### FR-021 生命周期

Operator/Method 至少支持 `draft`、`experimental`、`verified`、`deprecated`、`retired`。晋升必须绑定
conformance、eval、review 和兼容性证据；弃用必须给出替代项与迁移窗口。

### FR-022 Conformance

每个 Conformance Profile 必须提供与自身承诺匹配的正例和负例。Core 检查结构、类型与安全 owner；
执行型 Profile 再检查前置条件、效果、outcome、证据、权限、版本、provenance 和 fail-closed 行为。

### FR-023 扩展与供应商中立

实现可以在显式 `extensions` 对象中增加命名空间化扩展，但扩展不得改写核心字段含义或成为基础
conformance 的隐藏前提。多个真实消费者反复需要同一扩展时再推动规范升级。

### FR-024 本地库存与装载

每个 Harness 必须能够声明本地 Operator Library 当前装载的 Spec/Method 版本、Binding 版本、来源、
digest、信任状态和可用性。一次运行必须绑定不可变库存快照；远端目录变化不能静默改变进行中的任务。

### FR-025 治理同步边界

元 Harness 可以发布规范、目录元数据、conformance/eval 结果和生命周期决策；具体 Harness 决定何时
获取、验证、启用、回退或移除本地算子。同步失败不得让元 Harness 接管本地业务状态，也不得默认
把未验证的新版本放入执行热路径。

### FR-026 思维模型、算子与方法的归一化

来源材料进入库前必须被判定为领域事实、`MentalModelSpec`、`OperatorSpec` 或 `MethodSpec`：领域事实
只作为输入或引用资源；思维模型声明观察视角和适用边界；Operator 声明一次可执行动作；Method
组合多个 Operator。不得为了“全部算子化”而给纯概念伪造前置条件、效果或成功结论。

## 12. 非功能需求

| ID | 需求 |
|---|---|
| NFR-001 可移植性 | 核心语义不得绑定单一模型、prompt 格式、tool 协议或工作流引擎。 |
| NFR-002 可验证性 | 所有规范级 MUST 都应能映射到 Schema、validator、场景测试或明确人工检查。 |
| NFR-003 安全性 | 默认拒绝越权执行；外部定义与内容按不可信数据处理；敏感值只保留受控引用。 |
| NFR-004 可审计性 | 运行、证据和生命周期变化必须能够关联到版本与 digest。 |
| NFR-005 可演进性 | 破坏性变化有版本、迁移、弃用和回滚路径，不维护无期限双轨语义。 |
| NFR-006 可解释性 | Operator 目的、适用性、选择理由、outcome 和证据不足原因对人可读。 |
| NFR-007 可靠性 | 非确定性、超时、取消、重试、补偿和部分失败必须显式建模。 |
| NFR-008 效率 | 支持基于元数据的廉价预筛选；昂贵模型选择只处理已满足硬前置条件的候选。 |
| NFR-009 成本治理 | 每次运行可记录调用数、token、时延、费用、artifact/trace 体积和预算耗尽原因。 |
| NFR-010 隐私 | 证据与 provenance 默认最小披露，不要求复制完整输入、prompt、secret 或客户数据。 |
| NFR-011 运行独立性 | 已装载且验证通过的本地算子不应要求每次执行都在线调用元 Harness。 |

### 12.1 规模与性能验证

首版对本地 Operator Library 的 metadata 过滤目标应近似 `O(n)`，其中 `n` 是候选 Operator 数；
不能在每一步默认把完整算子库放入模型上下文。需要测量：

- 本地候选过滤和版本解析的 p50/p95 时延；
- 每次选择进入 LLM 上下文的候选数量与 token；
- 每次 OperatorRun 的模型/API/tool 调用数、总成本和完成时延；
- provenance 与 Evidence 的平均/峰值体积；
- 10x/100x 算子数量下检索、版本解析和计划验证的退化曲线。

没有上述数据前，不引入缓存、向量数据库、分布式队列或无界并发。

## 13. MVP 范围

### 13.1 必须交付

1. 规范性术语和对象模型。
2. `OperatorSpec`、`MethodSpec`、`Problem`、`Plan`、`OperatorRun`、`Evidence` 和 provenance 的
   JSON 表示与 Schema。
3. 覆盖 `MentalModelSpec → OperatorSpec → MethodSpec` 关系，以及认知、现实和治理效果的代表性
   corpus；数量服从覆盖率，不以堆数量为目标。
4. 至少两个 compound Method，证明分解、选择、失败和重规划语义。
5. 一个离线 conformance validator，包含正例与关键负例。
6. 两个彼此独立的 Harness 集成：各自装载本地 Operator Library，以不同 Binding 执行同一 Operator。
7. 一个端到端 proof：Task → Harness/Operator Library → Binding → LLM/Tools → Observation/Evidence →
   Verifier → Provenance。

### 13.2 MVP 不包含

- 在线 registry/API、数据库、UI、marketplace。
- 通用最优 planner 或全自动 operator 生成。
- 自动修改已验证 Operator。
- 完整图形化流程编辑器。
- 大规模 ontology、RDF store 或完整外部标准兼容层。
- 生产级权限系统、sandbox 或 secret manager；MVP 只定义并验证集成边界。

### 13.3 升级触发

- 离线文件无法满足真实并发查询、版本解析或权限隔离时，再评估 registry service。
- 两个以上 Harness Binding 重复同一映射逻辑时，再提取共享 Binding SDK。
- 规则选择在真实 eval 中明显输给受控 planning 时，再引入更复杂 planner。
- JSON 引用与图查询无法支持真实 provenance 审计时，再评估 PROV/RDF 映射。

### 13.4 当前实现切片

当前交付覆盖静态内容、conformance 与首个无副作用运行协议证明，不等于完整 MVP：

- `operators/source-inventory.json` 独立固定当前跨学科清单的 411 个原始条目；每个 domain 的精确数量与条目身份直接保存在该 inventory，文档不复制第二份长计数序列。
- 五十六个 `operators/packs/*.json` 精确覆盖 411/411，并额外提供 57 个明确标记为 `derived` 的领域组合
  Method，总计 468 个条目；在前一阶段补齐通用问题求解、统计、决策科学、运筹学、设计方法和工程学后，
  本阶段再加入因果推断、经济学/博弈论、生态/生物学、认知科学、人因可靠性、医学决策、法律推理、伦理与公共政策、教育与学习科学、语言学、历史推理、社会科学方法、形式逻辑与自动推理、哲学与科学认识论、地球科学、天文学与天体物理、材料科学、信息与知识科学，并用双轴 taxonomy
  分开母领域与功能类；第四阶段加入控制论、数值分析、离散组合数学、热力学/统计物理、有机化学反应设计和分析化学与计量学；第五阶段加入随机过程、微分方程与动力系统、经典力学与变分方法、流体与连续介质、化学动力学、电化学与传质；第六阶段加入线性代数谱方法、拓扑几何、电磁场方法、量子算子方法、溶液热力学相平衡和光谱结构解析；数学专项再对 55 个求解方法完成 20 reuse/35 add crosswalk，并补充 1 个 derived 发现与证明循环。
- `contracts/problem-solving-operator-pack.schema.json` 以宽松 Core 区分 `MentalModelSpec`、
  `OperatorSpec` 和 `MethodSpec`；只强制稳定字段形状、类型判别和安全 owner，不保存 Binding。
- `operators/catalog.json` 显式声明 `vibe-harness-cn/reference-library-v1`，当前为 56 个 pack；
  `scripts/validate_operator_library.py` 在 Core 之上检查安全相对路径、完整内容、精确清单、唯一
  ID/source key、声明计数、来源引用、Method 引用和权限/裁决/敏感值边界。
- canonical 库与缺项、重复 ID、坏引用、类型伪装、错误思维模型边、Method 循环、权限 owner
  改写、路径逃逸负例，以及最小自定义领域 Core Pack、空 Pack、显式扩展、未知字段和错误类型，
  由统一 `--self-test` 重跑。
- `contracts/operator-runtime.schema.json` 定义宽松的 `OperatorBinding`、`OperatorRunRequest` 和
  `OperatorRunRecord`；`examples/reference_harness/` 以 Harness 本地 Binding 完成确定性选择、三种
  Spec 的受限物化、Verifier 重算和摘要 provenance。
- 参考 Harness 的唯一效果范围是 `none`；它不调用模型或工具。`completed/accepted` 的 claim scope
  固定为 `instruction_materialization_only`，不得解释为问题已解决或方法有效。

尚未交付：通用 Problem/Plan/Evidence 模型、planner、Binding SDK、真实 LLM/tool execution、第二个
独立 Harness、双 Harness 互操作 proof 和生产 eval。因此所有库条目保持 `experimental`。

## 14. 用户故事

### US-001 Operator 作者发布方法

作为 Operator 作者，我希望提交带来源、前置条件、outcome、证据和失败语义的定义，并通过
conformance 后进入 `experimental`，以便 Harness 能安全发现它。

### US-002 Planner 选择下一步

作为 Harness 的 Planner/Selector，我希望先从本地 Operator Library 按硬前置条件、权限和预算筛选，
再对剩余候选作启发式或模型选择，并记录淘汰理由，以便选择可解释且可复现。

### US-003 Harness 执行标准 Operator

作为 Harness 开发者，我希望装载共享 OperatorSpec 并只实现本地 Binding，不重新发明 `Debug` 或
`Falsify` 的成功语义，以便不同 Harness 的运行结果可比较。

### US-004 Verifier 拒绝伪完成

作为 TEVV 负责人，我希望在证据缺失、陈旧或版本不匹配时返回 `inconclusive/blocked`，而不是接受
执行者的 PASS 文案。

### US-005 治理负责人审计运行

作为治理负责人，我希望从 Outcome 反向追溯 Operator、Method、Plan、Binding、模型、工具、输入和
证据版本，以便复现、问责、回滚或弃用。

## 15. 验收场景

### AC-001 跨 Harness 语义一致

Given 同一版本 OperatorSpec 和同一测试 Problem 已装载进两个 Harness 的本地库，When 两个独立
Binding 执行，Then 二者可以使用不同模型或工具，但必须输出同一 outcome vocabulary、证据字段
和 provenance 必填项。

### AC-002 前置条件 fail closed

Given 所需 baseline 或权限缺失，When Harness 尝试执行 `Ablate`，Then 执行被阻止并返回结构化
`not_applicable` 或 `blocked`，不得调用破坏性工具。

### AC-003 认知结果不被误判

Given `CounterexampleSearch` 在预算内未发现反例，When Verifier 裁决，Then 结果为
`inconclusive` 或规范定义的有限结论，不得自动宣称原命题为真。

### AC-004 证据版本绑定

Given Evidence 来自旧 artifact 或旧 Operator 版本，When Verifier 校验新运行，Then Evidence 被判
stale 并阻止成功 outcome。

### AC-005 失败后局部重规划

Given Plan 中一个节点失败，When runtime 重规划，Then 保留未受影响且仍新鲜的已验证节点，只使
失败节点及其依赖后代失效。

### AC-006 Provenance 可重建

Given 任一 OperatorRun，When 审计者读取记录，Then 能定位输入、定义版本、Binding、执行者、输出、
证据和派生链；敏感内容可以是受控引用而非明文副本。

### AC-007 不支持能力明确失败

Given Harness Binding 不支持 Operator 要求的 capability，When 做 conformance/plan 检查，Then 在
执行前返回明确缺口，不允许自由文本降级。

### AC-008 非程序性思维模型不伪装成动作

Given 一个只提供观察视角、没有明确状态效果的思维模型，When 作者将其加入库，Then 它被保存为
`MentalModelSpec` 并由 Operator 引用，而不是伪造一个可执行 Operator 和虚假成功条件。

## 16. 候选架构路径与决策

| 路径 | 核心思路 | 结论 |
|---|---|---|
| A：JSON Prompt Library | 把方法只写成模板和标签 | 拒绝；无法稳定表达状态、失败、证据和权限 |
| B：外部 Operator Runtime | 中央服务替所有 Harness 选择并执行算子 | 拒绝；产生双运行时 owner 和热路径耦合 |
| C：Harness 内结构化算子库 + 共享治理规范 | 本地执行、中央治理，以两个 Binding 验证 | 选择；归属正确且能证伪互操作假设 |
| D：完整 Planning/Workflow 平台 | 首版直接实现 planner、runtime、registry 和 UI | 拒绝；边界过大，且与现有 Harness 重复 |

### Target end state

PSOA 成为 Harness 内问题求解能力的共享架构：MentalModelSpec、OperatorSpec 和 MethodSpec 保持
供应商中立；每个 Harness 拥有自己的 Operator Library、Binding、选择、执行、权限和运行状态；
Verifier 拥有结果裁决，
Provenance owner 拥有审计链；Vibe Harness CN 负责规范、目录、分发、conformance、evaluation 和
lifecycle 治理。

### Real constraints

- 具体 Harness 必须继续拥有权限、业务副作用和运行状态。
- Operator 不能授予自己权限，执行者不能只靠自然语言自证成功。
- 同一规范必须能被异构 Harness 使用，运行和证据必须绑定确定版本。

### Inertia constraints

- 现有“外部独立语义层”表述不是公共 API、持久数据或外部承诺，不能决定目标架构。
- PRD 文件名和 PSOA 工作名可以保留，但不得保留错误的外部执行平面含义。

### Kill list

- 删除位于所有 Harness 外部的统一 Operator Runtime 概念。
- 删除元 Harness 与具体 Harness 共同拥有算子运行状态的双 owner 模型。
- 删除把中央 Catalog、本地 Library 和 Harness-specific Binding 混成一个对象的表达。

### Migration slice

本轮只纠正需求、领域模型和 ADR；下一轮以代表性 MentalModel/Operator/Method 验证本地库存语义，
再冻结 Schema，最后用两个 Harness 的不同 Binding 完成互操作 proof。

### Rejected short-term patches

- 不在旧外部语义层外再加一层“嵌入式适配器”掩盖归属错误。
- 不同时维护外部算子执行和 Harness 内算子执行两条路径。
- 不因尚未实现 Schema 而把算子退化成无状态、无证据的 prompt 模板。

### Proof point

同一 Operator 定义被两个不同 Harness 装入各自本地库，并通过不同 Binding 正确执行和验证。

### Falsifier

若第二个 Harness 必须改写核心 Operator 语义、隐藏状态或绕过证据契约才能接入，则当前抽象边界
错误，应修改领域模型，而不是增加供应商特例。

## 17. 风险与缓解

| 风险 | 影响 | 缓解 |
|---|---|---|
| 把方法库做成提示词市场 | 无法验证与组合 | 核心 conformance 必须覆盖状态、outcome、evidence |
| 把算子库放到 Harness 外部 | 双运行时 owner、延迟和单点故障 | 本地库执行；元 Harness 只交换规范和证据 |
| 中央目录与本地库存混为一谈 | 版本漂移、运行不可复现 | 每次运行绑定本地不可变库存快照 |
| 过度照搬 PDDL/BPMN | 规范复杂、落地困难 | 只吸收当前 proof 所需语义 |
| 把非确定性写成确定效果 | 产生错误成功结论 | Observation、Outcome、Verifier 分层 |
| Operator 与 Tool 混淆 | 方法不可移植、权限失控 | Tool 只作为 Binding capability |
| 自由文本扩展泛滥 | 供应商特例成为事实标准 | 命名空间扩展、typed core、触发规范升级 |
| 自证成功 | Goodhart、虚假完成 | 独立 evidence contract 与 verifier owner |
| provenance 过度采集 | 泄密与存储膨胀 | 默认元数据、digest、受控引用和保留策略 |
| 算子数量驱动 | 质量和可发现性下降 | 以覆盖、复用、eval 与生命周期晋升衡量 |

## 18. 待决策问题

以下问题不阻塞需求基线，但必须在 Schema/原型阶段用实现证据裁决：

1. 前置条件和效果采用受限 predicate DSL、CEL/JSON Logic 类表达，还是 typed JSON 组合。
2. `knowledge_state` 如何表达置信度、未知和证据冲突，而不制造伪精确概率。
3. Operator 是纯声明，还是允许引用签名/隔离后的 executable Binding package。
4. Method 首版采用树、DAG，还是同时允许受限循环；循环如何证明有界。
5. Verifier 规则中哪些必须确定性执行，哪些允许统计或模型辅助判断。
6. Provenance 首版使用轻量 JSON 映射，还是直接提供 W3C PROV 兼容 profile。
7. Registry 的 canonical ID、依赖解析、签名和供应链信任模型。
8. 并发 Operator 对同一 world/knowledge/governance state 的冲突检测与提交协议。
9. Operator package 如何把规范、说明、示例、Binding 引用和 eval 资产打包，同时保持签名与最小披露。
10. Harness 何时同步、启用和回退算子版本；离线运行与紧急撤回如何权衡。

## 19. 演进路线

1. **Requirements**：冻结本 PRD、术语、边界、proof point 与 falsifier。
2. **Semantic Prototype**：已用完整 411 项内容和 57 个组合 Method 验证类型、outcome、evidence 与本地库存结构。
3. **Contract v0**：已发布 Operator Pack 与 Runtime Core JSON Schema、精确覆盖和离线 conformance；
   通用 Problem/Plan/Evidence 仍待补齐。
4. **Composition**：参考 Harness 已证明 Method 受预算递归物化；Plan、失败恢复和局部重规划仍待实现。
5. **Interoperability**：由两个 Harness 装载同一 Spec，并通过不同 Binding 执行同一 conformance corpus。
6. **Evaluation**：建立开发集、密封留出集、成本/质量指标和晋升门禁。
7. **Registry/Lifecycle**：只在真实查询、协作和版本治理需求出现后服务化。

## 20. 设计依据（非规范性）

这些框架提供可借鉴语义，但不自动成为 PSOA 的合规依赖：

- STRIPS/PDDL：state、goal、preconditions、effects 与 domain/problem 分离。
- HTN Planning：primitive/compound task 与 method decomposition。
- BPMN/CMMN：控制流、事件、异常、补偿与 adaptive case。
- DMN：可复用决策和 selector 规则。
- NIST TEVV、ISO/IEC/IEEE 29119、ACM SIGSOFT Empirical Standards：验证、实验和证据要求。
- W3C PROV：Entity、Activity、Agent 和 derivation。
- OMG Essence：Practice/Method 的模块化描述。
- SWEBOK、数学、计算机科学、实验科学、机器学习和深度学习：Operator 的持续来源。

以上来源只决定“从哪里学习”，不决定 PSOA 顶层分类；进入库后的主分类取决于 Operator 在问题
求解系统中的职责。
