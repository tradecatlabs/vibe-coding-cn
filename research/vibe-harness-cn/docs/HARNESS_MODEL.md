# Harness 领域模型与元 Harness 目标架构

## 结论

`Agent = LLM + Harness` 是一个有用的工程定义：LLM 提供概率性的理解、推理与决策候选，
harness 把这些能力约束成一个能读取上下文、调用工具、改变状态、验证结果并在边界内停止
的系统。模型决定能力上限，harness 决定能力以什么权限、成本和证据落地。

元 harness 不是“更大的 agent”，也不是所有 agent 的统一执行器。它是 harness 的治理
控制面：管理契约、能力、策略、评估、证据和生命周期，而具体 harness 仍拥有自己的
任务执行与业务状态。

## 1. 术语边界

### 1.1 LLM

输入上下文后产生文本、结构化输出或工具调用候选的概率模型。它不应拥有权限真相、
秘密真相、执行结果真相或完成状态真相。

### 1.2 Harness

把模型接入真实任务的工程系统，至少包括：

```text
instructions      指令层级、冲突决议、外部内容信任标签
context/memory    检索、上下文预算、压缩、持久记忆和恢复字段
operator library 思维模型、方法论、适用条件、步骤、证据与本地执行绑定
tools             工具 schema、协议、超时、幂等和结构化 observation
permissions       默认拒绝、风险分级、审批、沙箱和秘密注入
loop/state        plan-act-observe-adjust、预算、重试、checkpoint、停止条件
validation        成功判据、测试、eval、反事实和证据新鲜度
observability     trace、指标、审计、脱敏和成本
environment       文件、网络、进程、身份和外部系统边界
```

Anthropic 把 agent 描述为模型自主管理过程和工具使用的循环，并明确指出 agent 行为同时
受模型、harness、工具和环境影响；其 eval 指南进一步把 harness/scaffold 定义为处理
输入、编排工具调用并返回结果的系统。OpenAI 的 agent 构建能力也把 tools、guardrails、
orchestration 和 tracing 作为模型之外的一等原语。它们共同支持一个判断：生产 agent
的可靠性不能只靠 prompt 或模型能力声明。

### 1.3 Agent

本项目采用简写：

```text
Agent = LLM + Harness
```

为了避免把任务和环境藏掉，运行态使用更精确的表达：

```text
AgentRunResult = execute(LLM, HarnessVersion, Task, Environment, ExternalState)
```

因此，“同一个模型”在不同工具、权限、环境和验证策略下不是同一个 agent；“同一个
harness”更换模型后也必须重新评估，而不能继承旧的能力或安全结论。

### 1.4 Workflow 与 Agent

- workflow：代码预先决定主要路径，适合稳定、可枚举、需要确定性的流程。
- agent：模型动态决定下一步，适合路径无法预先硬编码的开放任务。

元 harness 必须同时治理两者，但不能强迫确定性 workflow 伪装成 agent。先使用能满足
需求的最简单形态；只有固定流程覆盖不了真实任务时，才增加自治。

## 2. Harness 的核心循环

```text
Task
  -> Context Builder
  -> Operator Discovery / Selection
  -> Applicability + Policy Decision
  -> Operator Binding / Context Materialization
  -> Model Invocation
  -> Proposed Action
  -> Schema Validation
  -> Permission / Approval Decision
  -> Tool Execution or Denial
  -> Structured Observation
  -> State + Evidence Update
  -> Stop / Pause / Retry / Continue
```

关键不变量：

1. 模型可以提出动作，不能授予自己权限。
2. 工具输出和外部内容默认是数据，不是高优先级指令。
3. 执行成功不等于任务完成；完成必须由独立于生成叙事的证据判定。
4. 每个 loop 都必须有步数、时间、token/成本预算和明确停止条件。
5. checkpoint 必须保存恢复所需的计划、审批状态、修改集合和验证证据，不能只保存聊天。
6. trace 默认记录元数据与脱敏结果；完整 prompt、工具参数和结果属于 opt-in 敏感数据。
7. 模型不能批准自己的动作；审批状态必须存在于 prompt 之外的运行控制面或外部系统。
8. 上下文压缩必须保留目标、活动计划、审批、已加载指令、修改集合、待处理动作和验证证据。

## 3. 元 Harness 应治理什么

### 3.1 单一真相源

每个受管 harness 提交版本化 `Harness` manifest，声明：

- 身份、owner、来源 revision；
- 领域、排除项、风险等级和自治级别；
- 模型选择策略与 fallback；
- 指令、上下文、记忆、工具和环境边界；
- 权限、审批、预算、重试、checkpoint 和停止条件；
- 工具输入/输出/错误 Schema、结果大小、重试与审批绑定；
- 验证、可观测、发布、晋升和回滚策略。

manifest 是 candidate 声明真相，不是运行成功或正式批准的证明。`v1alpha1` 禁止作者自报
`approved`；正式生命周期状态必须由元 harness 根据 trace、eval result、审批记录、部署记录
和当前 artifact digest 派生并拥有。

### 3.2 控制面能力

目标终态由六个正交能力组成：

| 能力 | 职责 | 不拥有 |
|---|---|---|
| Registry | 版本、owner、来源、状态和依赖登记 | 业务任务状态 |
| Policy | 组织规则与 manifest 的确定性准入 | 模型主观自报豁免 |
| Conformance | Schema、静态规则和适配器能力检查 | 生产效果结论 |
| Evaluation | 数据集、runner、指标、回归和晋升证据 | harness 实现代码 |
| Evidence | trace、成本、审批、验证和 provenance 关联 | 未脱敏秘密与内容仓库 |
| Lifecycle | candidate、approved、paused、retired 与回滚 | 业务部署编排细节 |

### 3.3 控制面与数据面

```text
                    Meta Harness Control Plane
 manifest/operator spec -> registry -> policy -> conformance -> eval -> promotion
                           |                         |
                           +------ evidence <-------+
                                      ^
                                      |
                    stable adapter / trace envelope
                                      |
        +-----------------------------+----------------------------+
        |                             |                            |
 Coding Harness Runtime     Support Harness Runtime     Research Harness Runtime
```

控制面不得通过共享数据库直接接管所有运行时内部状态。适配器只交换稳定的声明、命令、
状态摘要和证据 envelope，避免把元 harness 变成所有系统的单点故障与耦合中心。

### 3.4 Harness 内的问题求解算子库

Harness 不只负责调用模型和工具，还应给 Agent 提供“如何解决问题”的能力。`Debug`、`Falsify`、
`Decompose`、`Ablate` 等思维模型和方法论被保存进 Harness 内的 Operator Library，回答“何时适用、
怎么做、改变什么认知、产生什么证据、失败后如何继续”。这套架构称为 Problem-Solving Operator
Architecture（PSOA），详细需求见
[`PROBLEM_SOLVING_OPERATOR_ARCHITECTURE_PRD.md`](PROBLEM_SOLVING_OPERATOR_ARCHITECTURE_PRD.md)，
公共交换格式与 Profile 分层见 [`OPERATOR_SPEC.md`](OPERATOR_SPEC.md)。

正确边界是 `Operator Library ⊂ Harness`，而不是在所有 Harness 外再造一个 Operator Runtime：

- 元 Harness 管共享 `OperatorSpec`/`MethodSpec`、目录、版本、分发、conformance、eval 和生命周期。
- 具体 Harness 管本地 Operator Library、`OperatorBinding`、选择、上下文注入、权限、执行和业务状态。
- 库内区分 `MentalModelSpec`（怎么看）、`OperatorSpec`（做一次什么）和 `MethodSpec`（按什么顺序做）；
  纯概念不能伪装成带成功条件的可执行动作。
- Binding 可以使用 prompt、skill、模型调用、tool 或 workflow，但不能改写共享方法语义。
- Verifier 在职责上独立裁决 Evidence 是否足以支持 outcome；它可以部署在 Harness 内或外部，
  但不能接受执行者无 provenance 的自评作为通过依据。
- 状态效果区分现实、认知和治理三类，避免把“未发现反例”误写成“命题已证明”。
- 现有 Harness manifest 未来只登记支持的规范版本、本地库存摘要和 Binding capability，不复制全部定义。

当前已实现静态契约和首个运行协议证明：Operator Pack 宽松 Core Schema 只约束稳定字段、类型判别、显式扩展和安全 owner；
本仓库 `vibe-harness-cn/reference-library-v1` Profile 再用独立 source inventory 固定 411 个跨学科
原始条目，五十六个 JSON pack 保存这些条目和 57 个显式派生 Method。离线 validator 检查 Core
格式，以及 Profile 的精确覆盖、唯一 ID、计数、来源、Method 引用、路径与治理不变量。
`contracts/operator-runtime.schema.json` 进一步定义 `OperatorBinding`、`OperatorRunRequest` 与
`OperatorRunRecord` 的宽松交换信封；`examples/reference_harness/` 作为具体 Harness 的参考消费方，
以 `O(n)` 元数据扫描、受预算的 Method 展开、Verifier 重算和摘要 provenance 完成无副作用闭环。

这次 `completed/accepted` 只证明 instruction packet 被正确物化，不证明问题已解决。全部内容仍为
`experimental`；尚未实现真实 LLM/tool execution、第二个独立 Binding 或生产 eval。核心互操作 proof 仍是同一
Operator 被两个不同 Harness 装入各自本地库，通过不同 Binding 执行并产生可比较证据；若第二个
实现必须改写核心语义才能接入，则应修改抽象，而不是增加兼容层。

### 3.5 跨学科算子扩展

本轮按“算子出生领域”和“在问题求解系统中的职责”分开：数学提供定义、界、更新和反例；物理学提供
量纲、守恒、极限、稳定性和不确定度检查；化学提供物料/电荷/电子平衡、平衡/动力学、机理与安全筛选；
算法、科学方法论、系统科学、复杂性科学、软件工程、编程、机器学习和深度学习分别补足搜索、实验、反馈、
跨尺度、演化、调试、泛化和训练稳定性。详细证据矩阵见
[`research/EXPANDED_OPERATOR_RESEARCH.md`](../research/EXPANDED_OPERATOR_RESEARCH.md)。这些条目仍是
参考内容，不是完整教材、专家替代品或自动执行权限。

### 3.6 上位问题求解方法论与双轴分类

算子库的来源域和功能类必须分开。来源域回答“这个方法从哪个成熟领域开采”，功能类回答“它主要改变问题
空间的哪一部分”。当前八类功能是表征、分解、变换、搜索、构造、验证/证伪、诊断/修正、控制/元认知；
它们由 Schoenfeld 的启发式/控制区分、Pólya 的理解—计划—执行—回看循环和 Newell–Simon 的问题空间/算子
视角综合而来。当前已覆盖 56 个母领域；在统计、决策科学、运筹学、设计方法和工程学之后，又加入因果推断、
经济学/博弈论、生态/生物学、认知科学、人因可靠性、医学决策、法律推理、伦理与公共政策、教育与学习科学、语言学、历史推理、社会科学方法、形式逻辑与自动推理、哲学与科学认识论、地球科学、天文学与天体物理、材料科学、信息与知识科学。统计抽样、信息价值、运筹松弛、工程压力、
因果识别、战略响应、观测误差、认知负荷、人因恢复与医学证据分级均保留为可审查参考动作。

详细证据、来源链接和抽取边界见 [`research/HEURISTIC_METACOGNITIVE_RESEARCH.md`](../research/HEURISTIC_METACOGNITIVE_RESEARCH.md)，
三十六个新增母领域的证据缺口见 [`research/DOMAIN_EVIDENCE_MATRIX.md`](../research/DOMAIN_EVIDENCE_MATRIX.md)，
机器分类视图见 [`operators/taxonomy/problem-solving-methodology.json`](../operators/taxonomy/problem-solving-methodology.json)。
第四波加入控制论、数值分析、离散组合数学、热力学/统计物理、有机化学反应设计、分析化学与计量学；第五波加入随机过程、微分方程与动力系统、经典力学与变分方法、流体与连续介质、化学动力学、电化学与传质；第六波再加入线性代数谱方法、拓扑几何、电磁场方法、量子算子方法、溶液热力学相平衡和光谱结构解析，补足结构空间、连续变形、源场边界、算子相容性、多相约束和多谱证据汇合。功能映射是项目推断，不是母学科官方分类；它不实现 selector、planner、权限或结果裁决。

数学专项不新增母领域，而是把 55 个问题求解方法按定义与表征、特化与实验、模式与猜想、变换与归约、构造与搜索、证明与界定、反例与压力检查、元认知控制与复盘逐项审计。20 项复用既有跨领域语义，35 项补入 mathematics pack，并增加一个数学发现与证明组合循环；详细 crosswalk 见 [`research/MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md`](../research/MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md)。

## 4. 首版选择与被拒绝路径

### 路径 A：契约优先的治理控制面（选择）

先建立领域模型、Schema、正反例和 validator。优点是供应商中立、可机检、可逐步接入；
当前切片不提供集中查询和在线策略服务；这两项没有当前消费方，也不是契约 proof point 的前置条件。

### 路径 B：先造统一运行时（拒绝）

统一封装模型调用、工具循环和状态机。它会过早把所有 harness 压成同一种执行模型，
并让控制面拥有不该拥有的业务状态；在没有真实适配对象前无法证明抽象正确。

### 路径 C：先接入现成多 agent / workflow 框架（拒绝）

成熟框架适合实现具体 harness，但不天然提供跨框架的治理真相。现在选择任一框架都会
把产品 API 误当领域模型。后续实现适配器时应优先复用 OpenAI Agents SDK、MCP、
OpenTelemetry 或具体业务已有框架，而不是重造模型调用、协议和 tracing。

### Ponytail 存在性结论

- 应存在：manifest、Schema、正反例、validator、领域文档和 ADR；它们直接证明统一治理可行。
- 暂不应存在：Web UI、数据库、队列、插件系统、在线 policy server、多 agent 调度器。
- 升级触发：接入第二个真实 runtime adapter；单文件 registry 无法支持查询/并发；离线策略无法满足
  发布门禁；跨运行时证据无法用现有 envelope 表达。
- 不可简化：默认拒绝、权限边界、停止条件、秘密治理、验证证据、脱敏和回滚。

### Future-Optimal 证据

- Target end state / 目标终态：Registry、Policy、Conformance、Evaluation、Evidence、Lifecycle
  六项正交控制面能力，通过稳定声明和证据边界治理异构 runtime。
- Real constraints / 真实约束：权限必须 fail closed；证据必须绑定 revision；控制面不能拥有业务状态。
- Inertia constraints / 惯性约束：空仓库没有旧 API、存量数据、部署或外部承诺需要兼容。
- Kill list：统一 runtime、首版数据库、首版 Web UI、首版队列、多 agent 调度器和无第二实现的插件系统。
- Proof point：有效 manifest PASS，结构/权限/版本/观测负例被确定性拒绝。
- Falsifier：第二类真实 harness 必须依赖自由文本特例才能表达关键治理边界。
- Migration slice：领域模型 -> v1alpha1 manifest -> 正反例 validator -> 首个真实 harness 接入。
- Short-term patches rejected：不以统一框架 wrapper、兼容壳或在线服务空架子替代当前契约切片。
- Ceiling / 升级触发：`v1alpha1` 只接受 `never/always` 审批；出现可解析、可版本化的真实
  条件策略注册表和第二个消费方后，再引入 conditional approval，不能先放悬空 policy URI。

## 5. 首版 Proof Point 与 Falsifier

Proof point：一个实际 coding harness runtime adapter 能被供应商中立 manifest 完整描述，正例通过 Schema
和项目策略，缺失停止条件的负例被确定性拒绝，且整个验证可用一条命令重跑。

Falsifier：接入第二个不同领域 harness 时，必须绕过 Schema 或把关键运行边界塞进自由文本；
若出现该情况，应修改领域模型并升级契约，而不是在 validator 中堆特例。

## 6. 风险模型

元 harness 最危险的失败不是“页面不可用”，而是错误地给出治理通过结论：

- manifest 合规被误当成效果和安全已经通过；
- 陈旧 eval 或 trace 被绑定到新 harness/model revision；
- 高风险工具绕过默认拒绝或审批；
- 外部内容借 prompt injection 提升为指令；
- 采集完整 prompt、参数、结果导致秘密和隐私泄露；
- 元 harness 自己成为特权执行入口或全局单点故障。

因此晋升决策必须绑定 harness revision、model identity、policy version、eval suite version、
artifact digest 和证据时间；缺失 required capability 时 fail closed。

## 7. 效率与扩展判断

首版 validator 对每个 manifest 做一次 Schema 遍历与少量跨字段规则检查，时间和空间复杂度
均为 `O(n)`，其中 `n` 是 manifest 节点数。当前 hot path 是人类评审和契约演进，不是计算。

- 立即值得做：离线确定性验证、结构化错误路径、正反例回归。
- 需要数据后再做：registry 索引、并行 eval、trace 存储、缓存和增量验证。
- 暂不值得做：数据库、分布式队列、无界并发和自研 tracing。

10x harness 数量下可继续批量离线验证；100x 且带大规模 eval 时，瓶颈会转向模型/API 成本、
外部 I/O、trace 体积和 rate limit，而非 Schema 校验。届时应基于 p95/p99 验证时延、每次晋升
模型调用数、token/API 成本、trace 字节数和队列等待时间决定 batch、缓存与并发上限。

## 8. 路线图

1. Contract：冻结 `v1alpha1` 最小字段，接入第一个真实 runtime adapter。
2. Adapters：定义供应商中立的 conformance/evidence envelope，接入第二类 runtime adapter。
3. Evaluation：建立 baseline、开发集、密封留出集和版本绑定的晋升门禁。
4. Registry：只有查询、并发和历史规模证明需要时，引入持久存储与 API。
5. Operations：接入 OpenTelemetry、审批系统和部署平台，形成可暂停、可回滚的生命周期。

每一步的扩权都必须由前一步失败数据或明确消费需求触发。

## 9. 源码调研：11 个新增 Harness

在既有 15 源 revision lock 之上，本项目已完成第一轮批量源码级调研：Pi、OpenClaw、Goose、
Gemini CLI、Cline、Qwen Code、Kimi Code、Crush、Mistral Vibe、OpenHands、Hermes Agent。
逐仓档案与证据路径见
[`research/HARNESS_RESEARCH.md`](../research/HARNESS_RESEARCH.md)。下面是回写领域模型的
横向结论；它们是研究输入和契约演进候选，不是控制面已实现能力。

### 9.1 Agent loop 已收敛，元 Harness 不必再造循环

11 个 Harness 都有“模型调用 → 工具执行 → 结果回填 → 上下文管理”的 attempt/reply 循环，
且多数有独立 loop 模块（Pi/OpenClaw `agent-loop.ts`、Goose `agent.rs`、Gemini
`agent-session.ts`、Cline `ClineCore.ts`、Kimi `loop/`、Crush `coordinator.go`、Mistral
`agent_loop/_loop.py`、Hermes `conversation_loop.py`）。元 Harness 治理的是循环的边界事实
（版本、工具面、权限、预算、停止条件、证据），而不是循环实现。

### 9.2 权限语义高度异质，登记必须表达语义类别

- 声明式：Gemini TOML 策略文件、Goose permission.yaml 三级权限。
- 代码链：Kimi 19 policy/11 维度责任链、Qwen 分类器 + 危险规则、OpenClaw tool policy、
  Mistral PermissionStore、Crush permission service。
- 审批流：Cline auto-approve、Hermes approval modes、Kimi approval service、OpenClaw
  gateway-question/native-hook-relay。
- 硬约束 vs 可豁免：Kimi 明确区分“harness 约束（硬 deny，无 ask 通道）”与“权限
  （可豁免 ask/deny）”，这是治理模型的关键二分。

结论：权限治理应登记“权限语义类别 + 默认姿态”并做一致性审计，而不是统一实现权限引擎。

### 9.3 Sandbox 能力存在 ≠ 默认安全

Pi 无内建权限/沙箱（文档给容器化模式）；OpenClaw sandbox 默认 `off`（mode/scope/elevated）；
Goose 只有 security inspector 无沙箱本体；Hermes 声明七种执行后端；Gemini 平台 sandbox +
默认策略文件；其余仓库未在源码中定位明确实现。registry 必须逐 revision 分开记录
“能力存在”与“默认姿态”两个事实。

### 9.4 证据与契约机制可借鉴

Pi telemetry conformance 测试、Kimi v2 config/state/wire contract manifests + import boundary
检查、OpenClaw 原子 model runtime generation、Qwen goal evidence/checkpoint、Hermes ACP
provenance + lifecycle ledger、Gemini evals/memory-tests/perf-tests。证据层应借鉴
“契约 manifest + conformance 测试 + 原子快照 + 可审计行为记录”的组合。

### 9.5 ACP 是跨 harness 控制协议的第一候选

OpenHands、Kimi、Goose、Cline、Mistral、Hermes 都提供或消费 ACP；Gemini 用 A2A。控制面
适配器应把 ACP 视为第一候选协议，同时保留对原生协议（如 Codex app-server、Claude Code
插件面）的登记。

### 9.6 技能/插件治理是跨 harness 通用需求

Hermes 技能自改进、Qwen auto-skills、Pi skills/packages、OpenClaw skills、Kimi skills、
Mistral skills：skill 是跨 harness 的通用资产类型，需要版本、来源、信任级别、自动更新
元数据与失效机制（Goose 的 extension malware check 是安全边界实例）。

### 9.7 对当前契约的候选影响（不立即实施）

- `Harness` manifest 未来可增加：权限语义类别与默认姿态、sandbox 能力与默认姿态、
  控制协议（ACP/A2A/原生）登记、goal/budget 治理字段。
- 任何字段新增都必须走“Schema + 正例 + 负例 + 文档 + ADR + api_version 升级”的既有变更规则。
- OpenHands Agent Canvas 与 Claw 等“控制中心形态”仓库证明多 agent backend registry 形态
  可行，但元 Harness 只借鉴 backend registry 与 ACP 集成边界，不复制其运行态所有权。

## 10. 一手资料

15 个目标 Harness 的官方 GitHub revision 与源码可见性已经固定在
[`research/upstreams.lock.json`](../research/upstreams.lock.json)，研究边界见
[`research/UPSTREAMS.md`](../research/UPSTREAMS.md)。其中 13 个 checkout 可做核心源码级比较；
Claude Code 官方仓库未公开 CLI 核心实现，当前 OpenHands 仓库是 Agent Canvas 而不含 agent core，
两者只能按公开扩展面、客户端或协议行为做有限比较。DeepSeek Harness 仍是 developer preview，
OpenClaw sandbox 默认关闭，Crush 当前采用 FSL-1.1-MIT；源码公开不能自动推出稳定、默认安全或
当前 permissive open-source 许可。这些都是 revision 绑定的证据边界，不应由推断补齐。

- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [Anthropic: Trustworthy agents in practice](https://www.anthropic.com/research/trustworthy-agents)
- [OpenAI: New tools for building agents](https://openai.com/index/new-tools-for-building-agents/)
- [Model Context Protocol: Server primitives](https://modelcontextprotocol.io/specification/2025-06-18/server/index)
- [OpenTelemetry: GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
