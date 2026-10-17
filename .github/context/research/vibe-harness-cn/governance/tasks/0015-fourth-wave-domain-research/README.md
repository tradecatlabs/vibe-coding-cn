# Task Overview
- Task ID: `0015`
- Slug: `fourth-wave-domain-research`
- Objective: `继续深度抓取控制论、数值分析、离散组合数学、热力学/统计物理、有机化学与分析化学方法，并沉淀为可审计算子`
- Status: `In Progress`

## In Scope
- 维护八类功能证据矩阵与母领域/功能双轴索引
- 研究六个新增母领域并建立五个 source 与一个 derived Method
- 同步 inventory、catalog、taxonomy、研究报告、文档和治理任务包
- 运行静态库、Core、自测、项目门禁和治理校验

## Out of Scope
- 穷尽教材或建立百科
- 实现 selector、planner、runtime、Binding、数据库、在线 registry 或 UI
- 提供现实实验、仪器校准、材料制备、控制系统操作或专业放行意见
- 改变公共 Core Schema、权限模型或运行时状态机

## Task Package Tree
- ROOT
  ├─ TP-01 [branch] [P0] 六个新增母领域深度抓取证据
  │  ├─ TP-01.01 [leaf] [P0] 控制论与反馈系统研究
  │  ├─ TP-01.02 [leaf] [P0] 数值分析与科学计算研究
  │  ├─ TP-01.03 [leaf] [P0] 离散组合数学研究
  │  ├─ TP-01.04 [leaf] [P0] 热力学与统计物理研究
  │  ├─ TP-01.05 [leaf] [P0] 有机化学反应设计研究
  │  └─ TP-01.06 [leaf] [P0] 分析化学与计量学研究
  ├─ TP-02 [leaf] [P0] 既有库缺口与重复审计
  ├─ TP-03 [leaf] [P0] 提炼新增算子与组合 Method
  ├─ TP-04 [leaf] [P0] 入库并同步目录文档
  └─ TP-05 [leaf] [P0] 验证、审查与交付收口

## Requirement Alignment
- 目标: 继续深度抓取控制论、数值分析、离散组合数学、热力学/统计物理、有机化学与分析化学方法，并沉淀为可审计算子
- approved plan 顶层步骤数: 5
- 编译后节点总数: 11
- 编译后叶子节点数: 10
- 对齐项: 用户要求继续深度抓取并参考历史上下文
- 对齐项: 本轮开始基线为 286 source、38 derived；当前库已扩展为 316 source、44 derived，只纳入有证据且不重复的新语义
- 对齐项: 数学、物理、化学优先，同时补 Harness 控制和数值误差边界
- 计划摘要: 先抓取六个领域的一手/权威来源，再做缺口审计、静态入库、文档治理和全量验证；不扩展运行时。

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | No | 为控制论、数值分析、离散组合数学、热力学/统计物理、有机化学和分析化学建立权威来源、方法程序、迁移边界和未验证项 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究状态空间、可控/可观测、反馈、稳定裕度和滚动重规划 |
| TP-01.02 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究条件性/稳定性、收敛、误差控制、残差和复现 |
| TP-01.03 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究双射、抽屉、容斥、递推/生成函数和极值界 |
| TP-01.04 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究系统边界、熵、自由能、扰动响应和系综采样 |
| TP-01.05 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究化学/区域/立体选择性、保护基代价、机理和复现审查 |
| TP-01.06 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究校准、检出限、基质干扰、方法验证和不确定度 |
| TP-02 | ROOT | 1 | P0 | action | Yes | TP-01.01, TP-01.02, TP-01.03, TP-01.04, TP-01.05, TP-01.06 | 2 | No | No | 将六个领域方法与当前 286 条目逐项比对，确定新增语义和交叉映射 |
| TP-03 | ROOT | 1 | P0 | action | Yes | TP-02 | 3 | No | No | 把独立语义写成五个 source 与一个 derived Method，保留前提、步骤、证据、失败和恢复 |
| TP-04 | ROOT | 1 | P0 | action | Yes | TP-03 | 4 | No | No | 同步 pack、inventory、catalog、taxonomy、研究报告、README、AGENTS、module context 和任务证据 |
| TP-05 | ROOT | 1 | P0 | action | Yes | TP-04 | 5 | No | No | 运行全量库、Core、自测、项目门禁、治理校验和任务级证据检查 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
