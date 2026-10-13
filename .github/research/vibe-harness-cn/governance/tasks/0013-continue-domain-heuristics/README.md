# Task Overview
- Task ID: `0013`
- Slug: `continue-domain-heuristics`
- Objective: `继续从更多母领域深度抓取问题求解方法，并将有证据的程序沉淀为可审计 Harness 算子`
- Status: `In Progress`

## In Scope
- 继续维护八类功能的证据矩阵与母领域/功能双轴交叉索引
- 研究法律推理、伦理与公共政策、教育与学习科学、语言学、历史推理、社会科学方法六个母领域
- 对既有 26 个母领域做缺口与重复审计，去重后才新增条目
- 新增 source pack、derived Method、inventory、catalog、taxonomy、研究报告及治理同步

## Out of Scope
- 穷尽学科教材或建立无来源的百科清单
- 实现 selector、planner、runtime、Binding、数据库、在线 registry 或 UI
- 提供法律意见、伦理批准、教育处方、语言规范裁决、历史事实裁定或社会政策授权
- 改变公共 Core Schema 必填字段、权限模型或运行时状态机

## Task Package Tree
- ROOT
  ├─ TP-01 [branch] [P0] 六个新增母领域分别深度抓取证据
  │  ├─ TP-01.01 [leaf] [P0] 法律推理研究
  │  ├─ TP-01.02 [leaf] [P0] 伦理与公共政策研究
  │  ├─ TP-01.03 [leaf] [P0] 教育与学习科学研究
  │  ├─ TP-01.04 [leaf] [P0] 语言学研究
  │  ├─ TP-01.05 [leaf] [P0] 历史推理研究
  │  └─ TP-01.06 [leaf] [P0] 社会科学方法研究
  ├─ TP-02 [leaf] [P0] 既有库缺口与重复审计
  ├─ TP-03 [leaf] [P0] 提炼新增算子与组合 Method
  ├─ TP-04 [leaf] [P0] 入库并同步目录文档
  └─ TP-05 [leaf] [P0] 验证、审查与交付收口

## Requirement Alignment
- 目标: 继续从更多母领域深度抓取问题求解方法，并将有证据的程序沉淀为可审计 Harness 算子
- approved plan 顶层步骤数: 5
- 编译后节点总数: 11
- 编译后叶子节点数: 10
- 对齐项: 用户要求继续深度抓取并参考上下文，不把算子库停留在既有 26 个母领域
- 对齐项: 既有研究明确要求把法律、伦理、教育、语言、历史和社会科学方法作为下一批证据矿山
- 对齐项: 当前库有 26 个母领域、226 source、26 derived；本轮只补语义独立且证据充分的缺口
- 计划摘要: 先按六个母领域建立权威来源和证据缺口矩阵，再做语义去重、功能映射和 pack 入库，最后用全量库、治理与任务证据门禁收口。

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | documentation | No | - | - | No | No | 为六个候选领域建立一手来源、反复使用的方法程序、可迁移问题、证据边界和未验证项，并映射到八类功能 |
| TP-01.01 | TP-01 | 2 | P0 | documentation | Yes | - | 1 | Yes | No | 研究争点识别、权威层级、先例类比/区分、证明标准和规则—事实适用如何支持受限结论 |
| TP-01.02 | TP-01 | 2 | P0 | documentation | Yes | - | 1 | Yes | No | 研究利益相关者、比例与不伤害、权利公平、影响评估、监督和责任分配中的问题求解程序 |
| TP-01.03 | TP-01 | 2 | P0 | documentation | Yes | - | 1 | Yes | No | 研究目标操作化、先备/误解诊断、提取应用、支架淡出和形成性反馈如何支持迁移学习 |
| TP-01.04 | TP-01 | 2 | P0 | documentation | Yes | - | 1 | Yes | No | 研究语料采样、最小对比、句法—语义—语用分层、篇章语境和歧义消解中的证据程序 |
| TP-01.05 | TP-01 | 2 | P0 | documentation | Yes | - | 1 | Yes | No | 研究来源出处批判、语境分期、交叉印证、史学视角和受约束反事实中的解释程序 |
| TP-01.06 | TP-01 | 2 | P0 | documentation | Yes | - | 1 | Yes | No | 研究构念操作化、抽样代表性、质性编码、混合方法和制度情境中的证据边界 |
| TP-02 | ROOT | 1 | P0 | data | Yes | TP-01.01, TP-01.02, TP-01.03, TP-01.04, TP-01.05, TP-01.06 | 2 | No | No | 将新研究与现有 226 条目逐项比对，确定哪些方法是新语义、交叉索引或仅需报告补充 |
| TP-03 | ROOT | 1 | P0 | feature | Yes | TP-02 | 3 | No | No | 把通过缺口审计的方法写成 MentalModelSpec、OperatorSpec 或 MethodSpec，明确前提、步骤、证据、失败和恢复 |
| TP-04 | ROOT | 1 | P0 | feature | Yes | TP-03 | 4 | No | No | 更新 pack、catalog、计数、研究报告、README、模块上下文、ADR 和任务证据 |
| TP-05 | ROOT | 1 | P0 | testing | Yes | TP-04 | 5 | No | No | 以全量库校验、项目门禁、治理检查、任务证据和 review 证明扩展可复核、可回滚且未越过运行时边界 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
