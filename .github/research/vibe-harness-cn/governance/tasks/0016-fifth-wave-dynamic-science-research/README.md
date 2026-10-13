# Task Overview
- Task ID: `0016`
- Slug: `fifth-wave-dynamic-science-research`
- Objective: `继续深度抓取随机过程、微分方程与动力系统、经典力学、流体与连续介质、化学动力学、电化学方法，并沉淀为可审计算子`
- Status: `In Progress`

## In Scope
- 维护八类功能证据矩阵与母领域/功能双轴索引
- 研究六个新增母领域并建立五个 source 与一个 derived Method
- 同步 inventory、catalog、taxonomy、研究报告、文档和治理任务包
- 运行静态库、自测、项目门禁和治理校验

## Out of Scope
- 穷尽教材或建立百科
- 实现 selector、planner、runtime、Binding、数据库、在线 registry 或 UI
- 提供现实化学实验、电化学操作、材料制备、仪器设置、数值放行或专业决策
- 改变公共 Core Schema、权限模型或运行时状态机

## Task Package Tree
- ROOT
  ├─ TP-01 [branch] [P0] 六个动态科学领域深度抓取证据
  │  ├─ TP-01.01 [leaf] [P0] 随机过程与概率过程研究
  │  ├─ TP-01.02 [leaf] [P0] 微分方程与动力系统研究
  │  ├─ TP-01.03 [leaf] [P0] 经典力学与变分方法研究
  │  ├─ TP-01.04 [leaf] [P0] 流体与连续介质研究
  │  ├─ TP-01.05 [leaf] [P0] 化学动力学研究
  │  └─ TP-01.06 [leaf] [P0] 电化学与传质研究
  ├─ TP-02 [leaf] [P0] 既有库缺口与重复审计
  ├─ TP-03 [leaf] [P0] 提炼新增算子与组合 Method
  ├─ TP-04 [leaf] [P0] 入库并同步目录文档
  └─ TP-05 [leaf] [P0] 验证、审查与交付收口

## Requirement Alignment
- 目标: 继续深度抓取随机过程、微分方程与动力系统、经典力学、流体与连续介质、化学动力学、电化学方法，并沉淀为可审计算子
- approved plan 顶层步骤数: 5
- 编译后节点总数: 11
- 编译后叶子节点数: 10
- 对齐项: 用户要求继续深度抓取并参考历史上下文
- 对齐项: 本轮开始基线为 316 source、44 derived；本轮扩展到 346 source、50 derived，只补有证据且不重复的新语义
- 对齐项: 数学、物理、化学优先，补足动态系统、随机性、连续介质和测量链边界
- 计划摘要: 先抓取六个领域的一手/权威来源，再做缺口审计、静态入库、文档治理和全量验证；不扩展运行时。

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | No | 为随机过程、微分方程与动力系统、经典力学、流体与连续介质、化学动力学和电化学建立权威来源、方法程序、迁移边界和未验证项 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究状态转移、条件期望/鞅、停止时刻、集中界和耦合对问题求解的启发 |
| TP-01.02 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究适定性、初边值条件、相图、Lyapunov 稳定和分岔敏感性 |
| TP-01.03 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究作用量、Euler-Lagrange、对称守恒、Hamilton 状态空间和扰动分析 |
| TP-01.04 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究控制体守恒、无量纲相似、主导平衡、边界条件和降阶模型验证 |
| TP-01.05 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究速率律、机理候选、速率控制、稳态近似和参数敏感性 |
| TP-01.06 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究平衡电势、Nernst、界面动力学、扩散限制和测量交叉检查 |
| TP-02 | ROOT | 1 | P0 | action | Yes | TP-01.01, TP-01.02, TP-01.03, TP-01.04, TP-01.05, TP-01.06 | 2 | No | No | 将六个领域方法与当前 316 条目逐项比对，确定新增语义和交叉映射 |
| TP-03 | ROOT | 1 | P0 | action | Yes | TP-02 | 3 | No | No | 把独立语义写成五个 source 与一个 derived Method，保留前提、步骤、证据、失败和恢复 |
| TP-04 | ROOT | 1 | P0 | action | Yes | TP-03 | 4 | No | No | 同步 pack、inventory、catalog、taxonomy、研究报告、README、AGENTS、module context 和任务证据 |
| TP-05 | ROOT | 1 | P0 | action | Yes | TP-04 | 5 | No | No | 运行全量库、自测、项目门禁、治理校验和任务级证据检查 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
