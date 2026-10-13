# Task Overview
- Task ID: `0018`
- Slug: `deepen-mathematical-problem-solving`
- Objective: `把数学家解决未知问题的八类方法地图逐项映射并沉淀为可审计算子`
- Status: `In Progress`

## In Scope
- 核验五套数学问题求解与证明资料
- 对用户点名的 55 个方法做完整 crosswalk
- 向现有 mathematics pack 增加 35 个独立 source 和 1 个 derived Method
- 同步 inventory、catalog、taxonomy、研究文档和治理记录
- 运行静态库、自测、项目和治理验证

## Out of Scope
- 建立数学知识百科或收录专门定理工具
- 实现 selector、planner、runtime、Binding、数据库、服务或 UI
- 改变公共 Core Schema 或权限边界
- 把静态内容宣称为真实 Agent 效果

## Task Package Tree
- ROOT
  ├─ TP-01 [leaf] [P0] 核验数学问题求解框架
  ├─ TP-02 [leaf] [P0] 逐项审计 55 个方法
  ├─ TP-03 [leaf] [P0] 沉淀数学算子与组合方法
  ├─ TP-04 [leaf] [P0] 同步文档与治理真相
  └─ TP-05 [leaf] [P0] 验证、审查与交付

## Requirement Alignment
- 目标: 把数学家解决未知问题的八类方法地图逐项映射并沉淀为可审计算子
- approved plan 顶层步骤数: 5
- 编译后节点总数: 5
- 编译后叶子节点数: 5
- 对齐项: 用户要求继续并完整沉淀其提供的数学思维模型地图
- 对齐项: 当前库已有 20 个可复用语义，本轮只新增 35 个独立缺口
- 对齐项: 数学方法按问题求解过程组织，而不是按代数、几何等知识分支组织
- 计划摘要: 先完成权威来源核验和 55 项语义去重，再将 35 个缺口写入现有数学 pack，最后同步文档治理并完成确定性验证。

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | action | Yes | - | 1 | No | No | 核验 Pólya、Schoenfeld、Mason–Burton–Stacey、NCTM 和 MIT 对问题求解、发现、控制与证明的支持边界 |
| TP-02 | ROOT | 1 | P0 | action | Yes | TP-01 | 2 | No | No | 与当前 432 个条目逐项去重并形成 20 reuse/35 add 的完整 crosswalk |
| TP-03 | ROOT | 1 | P0 | action | Yes | TP-02 | 3 | No | No | 将 35 个独立缺口和 1 个数学发现与证明循环写入现有 Reference Library |
| TP-04 | ROOT | 1 | P0 | action | Yes | TP-03 | 4 | No | No | 同步研究索引、目录职责、库快照、领域模型和任务证据 |
| TP-05 | ROOT | 1 | P0 | action | Yes | TP-04 | 5 | Yes | No | 运行全量库、自测、项目门禁、治理与任务级验证，记录独立审查状态 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
