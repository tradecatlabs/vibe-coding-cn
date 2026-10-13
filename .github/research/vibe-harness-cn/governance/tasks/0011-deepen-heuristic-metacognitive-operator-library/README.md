# Task Overview
- Task ID: `0011`
- Slug: `deepen-heuristic-metacognitive-operator-library`
- Objective: `按八类功能分类深度研究问题求解启发式与元认知，并覆盖数学、计算机科学、科学方法、软件调试、软件设计、统计学、机器学习、工程学、系统思维、决策科学、运筹学、设计方法等母领域，补充可审计算子与研究报告`
- Status: `Done`

## In Scope
- 以权威理论与官方资料为证据，分别研究 Representation、Decomposition、Transformation、Search、Construction、Verification/Falsification、Diagnosis/Revision、Control/Metacognition 八类功能
- 补齐统计学、决策科学、运筹学、设计方法和上位问题求解方法论等母领域，并去重扩展既有领域
- 新增缺口 operator packs、八类交叉索引、来源台账、研究报告和领域文档
- 运行 Core/Profile、项目门禁、治理校验和任务级验证

## Out of Scope
- 穷尽所有学科或实现完整求解器、仿真器、实验室自动化、训练平台
- 实现 selector、planner、runtime、Binding、数据库、在线 registry 或 UI
- 修改公共 Core Schema 以强制学科字段或功能分类字段
- 执行上游代码、模型训练、物理/化学实验、部署、凭据读取、远端写入或破坏性操作

## Task Package Tree
- ROOT
  ├─ TP-01 [branch] [P0] 八类功能分别深度抓取证据
  │  ├─ TP-01.01 [leaf] [P0] Representation 表征研究
  │  ├─ TP-01.02 [leaf] [P0] Decomposition 分解研究
  │  ├─ TP-01.03 [leaf] [P0] Transformation 变换研究
  │  ├─ TP-01.04 [leaf] [P0] Search 搜索研究
  │  ├─ TP-01.05 [leaf] [P0] Construction 构造研究
  │  ├─ TP-01.06 [leaf] [P0] Verification/Falsification 验证证伪研究
  │  ├─ TP-01.07 [leaf] [P0] Diagnosis/Revision 诊断修正研究
  │  └─ TP-01.08 [leaf] [P0] Control/Metacognition 控制元认知研究
  ├─ TP-02 [leaf] [P0] 提炼母领域算子与双轴分类
  ├─ TP-03 [leaf] [P0] 入库并同步交叉索引与文档
  └─ TP-04 [leaf] [P0] 验证、审查与交付收口

## Requirement Alignment
- 目标: 按八类功能分类深度研究通用问题求解启发式与元认知，并从数学问题求解、计算机科学算法思维、科学方法、软件调试、软件设计、统计学、机器学习、工程学、系统思维、决策科学、运筹学、设计方法及既有科研领域提炼可调用算子
- approved plan 顶层步骤数: 4
- 编译后节点总数: 12
- 编译后叶子节点数: 11
- 对齐项: 用户要求按八类功能单独深度抓取问题求解启发式与元认知
- 对齐项: 用户补充数学、计算机科学、科学方法、软件调试、软件设计、统计学、机器学习、工程学、系统思维、决策科学、运筹学、设计方法等母领域
- 对齐项: 现有库已覆盖部分母领域，本轮优先补缺并建立功能交叉视图，不重复堆叠同名条目
- 计划摘要: 先分别抓取八类功能的上位理论与各母领域的操作程序，再去重提炼算子和交叉索引，最后用现有 Profile/治理门禁收口。

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | documentation | No | - | - | No | No | 为八类功能各自建立权威来源、核心动作、适用边界、失败方向和迁移推断 |
| TP-01.01 | TP-01 | 2 | P0 | documentation | Yes | - | 1 | Yes | No | 抓取重述、抽象、图示、模型选择和问题表征变换的权威证据 |
| TP-01.02 | TP-01 | 2 | P0 | documentation | Yes | - | 1 | Yes | No | 抓取子目标、分治、模块化、依赖拆解和 means-ends 方法的权威证据 |
| TP-01.03 | TP-01 | 2 | P0 | documentation | Yes | - | 1 | Yes | No | 抓取类比、归约、反向工作、松弛、特化/推广和等价变换的权威证据 |
| TP-01.04 | TP-01 | 2 | P0 | documentation | Yes | - | 1 | Yes | No | 抓取系统枚举、贪心、回溯、分支定界、探索/利用和启发式搜索证据 |
| TP-01.05 | TP-01 | 2 | P0 | documentation | Yes | - | 1 | Yes | No | 抓取构造性证明、原型、模拟、生成检验、约束满足和迭代精化证据 |
| TP-01.06 | TP-01 | 2 | P0 | documentation | Yes | - | 1 | Yes | No | 抓取证明、反例、实验、复现、不变量、独立审查和校准证据 |
| TP-01.07 | TP-01 | 2 | P0 | documentation | Yes | - | 1 | Yes | No | 抓取复现、定位、二分、根因、误差分解、差分比较和反思修正证据 |
| TP-01.08 | TP-01 | 2 | P0 | documentation | Yes | - | 1 | Yes | No | 抓取策略选择、监控、停止、预算分配、切换、回溯和 look-back 证据 |
| TP-02 | ROOT | 1 | P0 | feature | Yes | TP-01.01, TP-01.02, TP-01.03, TP-01.04, TP-01.05, TP-01.06, TP-01.07, TP-01.08 | 2 | No | No | 从统计学、决策科学、运筹学、设计方法及其他母领域筛出不重复的可执行算子，并建立功能分类交叉索引 |
| TP-03 | ROOT | 1 | P0 | feature | Yes | TP-02 | 3 | No | No | 更新 packs、inventory、catalog、taxonomy、研究报告、README、领域文档、ADR/QA 和模块上下文 |
| TP-04 | ROOT | 1 | P0 | testing | Yes | TP-03 | 4 | No | No | 用全量门禁、治理检查、任务证据、review 和回滚说明证明本轮扩展可复核 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
