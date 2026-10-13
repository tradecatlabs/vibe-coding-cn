# Task Overview
- Task ID: `0012`
- Slug: `expand-next-domain-heuristics`
- Objective: `继续按八类功能深度研究更多母领域，并把可复用方法沉淀为可审计的 Harness 算子`
- Status: `In Progress`

## In Scope
- 继续维护八类功能的证据矩阵与母领域/功能双轴交叉索引
- 研究因果推断、经济与博弈、生态与生物、认知科学、人因可靠性、医学决策六个候选母领域
- 对既有信息论、复杂性科学和相关领域做缺口审计，去重后才新增条目
- 新增 source pack、derived Method、inventory、catalog、taxonomy、研究报告及治理同步

## Out of Scope
- 穷尽学科教材或建立无来源的百科清单
- 实现 selector、planner、runtime、Binding、数据库、在线 registry 或 UI
- 执行医疗、生态、生物、工程或其他现实实验与外部操作
- 改变公共 Core Schema 必填字段、权限模型或运行时状态机

## Task Package Tree
- ROOT
  ├─ TP-01 [branch] [P0] 六个新增母领域分别深度抓取证据
  │  ├─ TP-01.01 [leaf] [P0] 因果推断研究
  │  ├─ TP-01.02 [leaf] [P0] 经济与博弈研究
  │  ├─ TP-01.03 [leaf] [P0] 生态与生物研究
  │  ├─ TP-01.04 [leaf] [P0] 认知科学研究
  │  ├─ TP-01.05 [leaf] [P0] 人因可靠性研究
  │  └─ TP-01.06 [leaf] [P0] 医学决策研究
  ├─ TP-02 [leaf] [P0] 既有库缺口与重复审计
  ├─ TP-03 [leaf] [P0] 提炼新增算子与组合 Method
  ├─ TP-04 [leaf] [P0] 入库并同步目录文档
  └─ TP-05 [leaf] [P0] 验证、审查与交付收口

## Requirement Alignment
- 目标: 继续按八类功能深度研究更多问题求解母领域，并把可复用方法沉淀为可审计的 Harness 算子
- approved plan 顶层步骤数: 5
- 编译后节点总数: 11
- 编译后叶子节点数: 10
- 对齐项: 用户要求继续深度抓取并参考现有上下文，不把算子库停留在首批母领域
- 对齐项: 上一轮报告明确把因果推断、经济/博弈、生态/生物、认知科学、人因安全和医学决策列为后续矿山
- 对齐项: 任务开始时库有 20 个母领域、196 source、20 derived；本轮优先补充证据充分且不重复的缺口，当前形成 26 个母领域、226 source、26 derived
- 计划摘要: 先按候选母领域建立权威来源与证据缺口矩阵，再将反复出现的问题求解程序映射到八类功能，最后新增去重 pack 并用现有门禁收口。

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | documentation | No | - | - | No | No | 为候选母领域建立一手来源、反复使用的方法程序、可迁移问题、证据边界和未验证项，并映射到八类功能 |
| TP-01.01 | TP-01 | 2 | P0 | documentation | Yes | - | 1 | Yes | No | 研究反事实、因果图、干预、识别条件、混杂审计和敏感性分析如何支持受限结论 |
| TP-01.02 | TP-01 | 2 | P0 | documentation | Yes | - | 1 | Yes | No | 研究机会成本、边际分析、激励、均衡、机制设计和鲁棒策略中的问题求解程序 |
| TP-01.03 | TP-01 | 2 | P0 | documentation | Yes | - | 1 | Yes | No | 研究生态系统边界、种群动力学、适应、选择、网络关系、实验对照和多尺度推断 |
| TP-01.04 | TP-01 | 2 | P0 | documentation | Yes | - | 1 | Yes | No | 研究表征、类比、双过程、工作记忆、策略选择、认知负荷和元认知监控中的可迁移程序 |
| TP-01.05 | TP-01 | 2 | P0 | documentation | Yes | - | 1 | Yes | No | 研究情境意识、检查表、错误分类、工作负荷、冗余、恢复和安全关键决策中的方法 |
| TP-01.06 | TP-01 | 2 | P0 | documentation | Yes | - | 1 | Yes | No | 研究临床决策中的证据分层、诊断阈值、风险收益、共享决策和不确定性沟通，仅作参考方法 |
| TP-02 | ROOT | 1 | P0 | data | Yes | TP-01.01, TP-01.02, TP-01.03, TP-01.04, TP-01.05, TP-01.06 | 2 | No | No | 将新研究与现有 216 条目逐项比对，确定哪些方法是新语义、交叉索引或仅需报告补充 |
| TP-03 | ROOT | 1 | P0 | feature | Yes | TP-02 | 3 | No | No | 把通过缺口审计的方法写成 MentalModelSpec、OperatorSpec 或 MethodSpec，明确前提、步骤、证据、失败和恢复 |
| TP-04 | ROOT | 1 | P0 | feature | Yes | TP-03 | 4 | No | No | 更新 pack、catalog、计数、研究报告、README、模块上下文、ADR/QA 和任务证据 |
| TP-05 | ROOT | 1 | P0 | testing | Yes | TP-04 | 5 | No | No | 以全量库校验、项目门禁、治理检查、任务证据和 review 证明扩展可复核、可回滚且未越过运行时边界 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
