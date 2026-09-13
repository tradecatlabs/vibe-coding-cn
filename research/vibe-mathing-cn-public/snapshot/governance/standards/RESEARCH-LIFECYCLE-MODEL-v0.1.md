---
id: STD-RESEARCH-LIFECYCLE-MODEL-V0.1
type: standard
status: current
owner: engineering
created: 2026-09-07
last_reviewed: 2026-09-07
review_cycle: P90D
version: 0.1
source: sanitized public synthesis of lifecycle orchestration design
related_gates: [GATE-0002]
---

# 研究任务全生命周期与编排模型 v0.1 — PLFB F05 过程面

本文件定义项目唯一 [Point–Line–Face–Body 元模型](POINT-LINE-FACE-BODY-METAMODEL-v0.1.md)中 **F05 Process/PWTSJ** 面内的生命周期认识。它补充而不替代 `ProblemContract`、`Attempt`、Outcome Space、Evidence、`Result` schema 和数学证据准入规则。

PWTSJ 是 F05 面内模型，不是并列元模型根。OSPS 属于 F04：它维护 OutcomeNode、Obligation、候选分支和搜索前沿；PWTSJ 组织有界执行。二者必须通过显式跨面 Line 绑定。

它首先是一个公开的架构与术语模型，不是已实现的分布式调度器、OSPS orchestrator、Body runtime、统一 Observation Ledger、自动证明器、启动授权或能力认证。文档中出现的未来机制必须视为设计目标，不能当作当前运行能力。

## 一、F05 的五级结构

```text
Project
  └─ Workflow
      └─ Task
          └─ Step
              └─ Job
```

| 层级 | 定义 | 核心问题 | 生命周期职责 |
| --- | --- | --- | --- |
| **Project** | 一个完整目标及其边界 | 要完成什么目标？ | 绑定目标、问题契约和总预算 |
| **Workflow** | 为完成目标组织起来的任务网络 | 任务如何依赖、并行和汇聚？ | 管理研究路线、验证路线和整体进度 |
| **Task** | 有明确输入与输出的工作单元 | 这一单元要产出什么？ | 承担证明义务、来源审查或验证目标 |
| **Step** | Task 内可操作的细分动作 | 具体采用什么方法和工具？ | 定义方法、输入、验收条件和停止条件 |
| **Job** | Step 的一次有界执行实例 | 谁在何时何处执行了什么？ | 保存执行状态、资源消耗、产物摘要和回执 |

**硬约定：Job 是 Step 的实例，不是 Task 的直接运行实例。** 一个 Step 可以有多个 Job，用于参数变体、有限重试或独立验证；恢复同一个 Job 必须绑定已验证 checkpoint，重新执行则创建新 Job 并关联前次执行。

## 二、数学对象与五级结构正交

五级结构描述“目标如何被组织和执行”；数学对象描述“研究事实如何被定义和裁决”。二者不能合并成一条状态链，也不能用运行状态替代数学结论。

| 数学对象 | 绑定关系 |
| --- | --- |
| `ProblemContract` | Project 引用的数学问题身份与输入契约；不复制成第二份真相源 |
| `Attempt` / route | 一次研究尝试及其路线，通常关联 Workflow，可包含多个 Job |
| obligation graph | Task 承担的证明义务及依赖图；不等同于执行任务图 |
| candidate artifact | 生成 Job 产生的候选证明、代码、数据或反例材料 |
| evidence receipt | 验证 Job 针对指定候选、义务和陈述产生的可检查回执 |
| `Result` | 按既有准入规则记录的结构化主张，仍使用 `outcome × evidence` |
| `ResearchBundle` / `Solution View` | 从一致、已校验事实快照派生的只读视图，不单独保存数学真相 |

典型追踪关系是：

```text
Solution View
  → Result
      → 有效 Evidence
          → 验证 Job
              → Candidate Artifact
                  → 生成 Job → Step → Task → Workflow → Project
```

所有候选、证据和结论都必须绑定正确的 `ProblemContract`、`Attempt`、义务版本及输入摘要，防止换题、换假设或换产物后复用旧回执。

项目原有的数学事实链仍然是：

```text
ProblemContract → Attempt → candidate/evidence → Result → derived Solution View
```

## 三、标准研究生命周期

一个 Project 的典型 Workflow 可以展开为：

```text
问题契约化
  → 证明义务分解
  → AI/工具候选生成
  → 形式化与独立验证
  → 证据准入
  → Result 与视图派生
```

每个阶段都展开为 `Task → Step → Job`。例如，一个引理验证 Task 可以包含：

```text
Project：研究一个固定数学问题
  └─ Workflow：探索并验证一条证明路线
      └─ Task：验证引理 L
          ├─ Step：形式化候选引理
          │   └─ Job：在固定输入和预算内生成候选
          └─ Step：独立重建与公理审计
              └─ Job：注册 verifier 检查候选并生成回执
```

来源收集只能产生来源观察；只有已准入的 active `ProblemContract` 才能创建正式 `Attempt`。

## 四、五条相互独立的状态轴

```text
契约生命周期   draft / active / withdrawn
执行生命周期   queued / running / succeeded / failed / timed_out / cancelled / ...
研究生命周期   以 Attempt schema 的生命周期为准
数学结果       undetermined / supported / established / refuted / inconclusive / withdrawn
证据能力       numeric_check / symbolic_check / kernel_check / ...
```

状态轴不得互相偷换：

```text
Job succeeded
  ≠ Step accepted
  ≠ Obligation closed
  ≠ OutcomeNode closed
  ≠ Result admitted
  ≠ Project solved
```

运行完成只说明一次活动结束。暂停、路线阻塞、预算耗尽和工具失败都不能自动改变数学 `outcome`；`Result` 当前结论必须由有效证据重新派生。

## 五、三个职责平面

| 平面 | 负责什么 | 不得做什么 |
| --- | --- | --- |
| **控制平面** | 契约、授权、规划、状态转换、调度、预算、恢复和停止 | 不直接把计划当作执行事实 |
| **执行平面** | AI、检索、计算、符号推理和形式化构造，产生候选产物 | 不自行签发数学闭合 |
| **验证平面** | 注册 verifier、证书/内核检查、公理审计、陈述忠实性和准入 | 不替生成者降低验收标准 |

验证操作同样通过 Job 执行，但必须隔离生成者与验证者的身份、权限和信任范围。

## 六、编排、预算与幂等

- **执行 DAG** 管理 Task/Step 的输入依赖、并行和汇聚；**证明义务 DAG** 管理引理、假设和结论依赖，二者不能混为一图。
- 外层状态机管理循环、换路、暂停、恢复和停止；修改图或契约会产生新版本，并重新评估受影响证据。
- 调度只能把已就绪且获授权的 Step 实例化为 Job；Worker 只能执行 Job，不能扩大授权或改变验收策略。
- 每个 Job 和其父级都必须有时间、内存、CPU、输出字节数、文件数、重试次数和累计预算；并行消耗也计入父级预算。
- 去重键、输入摘要和幂等写入用于防止重复发布；不能假定网络或进程天然提供 exactly-once。
- 同一 `ProblemContract` 的协调活动需要唯一持久身份；独立验证 Job 可以并行，但不能绕过 producer 配额或由生成者自签。

## 七、自动失败闭环

| 情况 | 生命周期动作 | 数学含义 |
| --- | --- | --- |
| 临时工具/网络故障 | 有限重试并保留每次 Job | 不改变 outcome |
| 证明失败、反例无效 | 保存候选和失败路线，重新规划 | 不能转成 refuted |
| 有限计算、局部结果 | 保存有界支持 | 不能外推全称命题 |
| 无进展、资源超额、授权不足 | 保存 checkpoint，暂停或停止 | 保持未解决状态 |
| 契约/义务改变 | 固定新版本，重验受影响证据 | 旧回执不能静默复用 |
| 证据失效 | 追加失效记录，重新派生视图 | 允许撤回结论 |
| 证明与反例同时闭合 | 阻断导出，转入冲突审计 | fail-closed，不任选一边 |

Job 至少应能追踪到五级 ID、运行关联 ID、定义/义务版本、输入输出摘要、执行器和工具链指纹、状态事件、消耗计量、回执及必要 checkpoint。大输出和运行日志留在受配额控制的运行区；公开仓库只保存合规的小型产物、摘要和索引。

## 八、验证与准入边界

形式化内核可以成为验证骨架，但只证明“编码后的命题在所用公理下有证明”。完整准入仍需检查：

1. 原问题与形式化陈述的对象、量词、范围和假设一致；
2. 证明依赖、公理和逃逸机制符合固定策略；
3. 外部计算具有适用的可检查证书或严格复现边界；
4. verifier 已注册、能力匹配且与生成者满足独立性；
5. 回执、底层产物和陈述摘要一致，且没有后续失效记录。

多模型赞同、有限扫描、数值趋势、退出码成功、Job 完成和完整溯源都不能替代数学证明。哈希绑定身份，不证明内容正确。

## 九、当前公开实现边界

当前公共仓库已经公开 `ProblemContract`、`Attempt`、`Result`、证据回执、受限运行时、固定 Fixture、验证器 registry 和派生 `ResearchBundle`/`Solution View` 的契约与检查。上述五级 Project/Workflow/Task/Step/Job 模型目前是顶层组织与未来编排的公共设计语言，**不是已经存在的五套持久化 schema、通用 DAG 调度器或多 Worker 生产能力**。

任何未来落地都必须通过兼容性设计、预算/恢复/幂等负例和公共边界审查；不得迁移或重写历史研究记录，也不得因为增加编排层就降低既有数学准入门槛。

## 十、公共验收口径

- 任一 Job 都可以追踪到 Project 及精确的 `ProblemContract`/义务版本；
- Job 成功不能绕过语义审查和证据门直接生成 `Solution View`；
- 重试和恢复不重复发布、不覆盖历史、不突破累计预算；
- 陈述漂移、证据摘要错误、自签验证和证明/反例冲突均 fail-closed；
- 无法验证时暂停、失败或保持未解决，不要求系统猜测答案。

> Project 定目标，Workflow 定流程，Task 定工作，Step 定操作，Job 记录执行；证据决定数学结论。
