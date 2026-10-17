# Task Overview
- Task ID: `0014`
- Slug: `third-wave-domain-research`
- Objective: `继续从更多母领域深度抓取问题求解方法，并将有证据的程序沉淀为可审计 Harness 算子`
- Status: `In Progress`

## In Scope
- 维护八类功能的证据矩阵与母领域/功能双轴交叉索引
- 研究形式逻辑与自动推理、哲学与科学认识论、地球科学、天文学与天体物理、材料科学、信息与知识科学六个母领域
- 对既有 32 个母领域做缺口与重复审计，只有有证据的新语义才入库
- 新增 source pack、derived Method、source inventory、catalog、taxonomy crosswalk 和研究报告
- 同步领域文档、目录自述、治理 ADR、module context、任务证据和验证结果

## Out of Scope
- 穷尽学科教材、建立百科或收集未经来源支持的 mental-model 清单
- 实现 selector、planner、runtime、Binding、数据库、在线 registry 或 UI
- 提供数学证明、地质解释、天文观测结论、材料设计处方、知识检索授权或任何现实专业意见
- 改变公共 Core Schema 必填字段、权限模型或运行时状态机

## Task Package Tree
- ROOT
  ├─ TP-01 [branch] [P0] 六个新增母领域分别深度抓取证据
  │  ├─ TP-01.01 [leaf] [P0] 形式逻辑与自动推理研究
  │  ├─ TP-01.02 [leaf] [P0] 哲学与科学认识论研究
  │  ├─ TP-01.03 [leaf] [P0] 地球科学与地学研究
  │  ├─ TP-01.04 [leaf] [P0] 天文学与天体物理研究
  │  ├─ TP-01.05 [leaf] [P0] 材料科学研究
  │  └─ TP-01.06 [leaf] [P0] 信息与知识科学研究
  ├─ TP-02 [leaf] [P0] 既有库缺口与重复审计
  ├─ TP-03 [leaf] [P0] 提炼新增算子与组合 Method
  ├─ TP-04 [leaf] [P0] 入库并同步目录文档
  └─ TP-05 [leaf] [P0] 验证、审查与交付收口

## Requirement Alignment
- 目标: 继续从更多母领域深度抓取问题求解方法，并将有证据的程序沉淀为可审计 Harness 算子
- approved plan 顶层步骤数: 5
- 编译后节点总数: 11
- 编译后叶子节点数: 10
- 对齐项: 用户要求继续深度抓取并参考上下文，研究范围从既有 32 个母领域继续扩展
- 对齐项: 历史研究把形式逻辑、认识论、地学、天文、材料和信息知识列为可补的证据矿山
- 对齐项: 当前库有 32 个母领域、256 source、32 derived；本轮只补语义独立且证据充分的缺口
- 计划摘要: 先分别深挖六个母领域的一手或权威资料，再做语义去重、功能映射、静态入库和全量验证；不扩展运行时。

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | No | 为六个候选领域建立权威来源、反复使用的方法程序、可迁移问题、证据边界和未验证项，并映射到八类功能 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究规格化、语法语义分离、可满足性反例、证明状态分解和内核检查如何约束推理 |
| TP-01.02 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究观察与解释分离、最佳解释推断、辅助假设审计、欠定性分支和区分性证据设计 |
| TP-01.03 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究观测误差、地层相对时序、地图剖面、质量守恒和遥感地面真值如何支持跨尺度推断 |
| TP-01.04 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究观测模型分离、信号背景区分、尺度检查、光变/光谱拟合和独立观测确认 |
| TP-01.05 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究加工—结构—性能映射、计量溯源、微观结构表征、数据质量和资格校准 |
| TP-01.06 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究信息需求表达、查询扩展、来源权威与 provenance、精确率召回率审计和元数据公平性检查 |
| TP-02 | ROOT | 1 | P0 | action | Yes | TP-01.01, TP-01.02, TP-01.03, TP-01.04, TP-01.05, TP-01.06 | 2 | No | No | 将新研究与现有 256 条目逐项比对，确定哪些方法是新语义、交叉索引或仅需报告补充 |
| TP-03 | ROOT | 1 | P0 | action | Yes | TP-02 | 3 | No | No | 把通过缺口审计的方法写成 MentalModelSpec、OperatorSpec 或 MethodSpec，明确前提、步骤、证据、失败和恢复 |
| TP-04 | ROOT | 1 | P0 | action | Yes | TP-03 | 4 | No | No | 更新 pack、inventory、catalog、taxonomy、研究报告、README、模块上下文和 ADR，保持单一真相源一致 |
| TP-05 | ROOT | 1 | P0 | action | Yes | TP-04 | 5 | No | No | 运行全量库、Core、自测、项目门禁、治理校验和任务证据检查，绑定 clean HEAD 与未验证项 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
