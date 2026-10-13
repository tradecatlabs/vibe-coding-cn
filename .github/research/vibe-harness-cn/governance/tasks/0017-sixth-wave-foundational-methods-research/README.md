# Task Overview
- Task ID: `0017`
- Slug: `sixth-wave-foundational-methods-research`
- Objective: `继续深度抓取线性代数谱方法、拓扑几何、电磁场方法、量子算子方法、溶液热力学相平衡和光谱结构解析，并沉淀为可审计算子`
- Status: `In Progress`

## In Scope
- 维护八类功能证据矩阵与母领域/功能双轴索引
- 研究六个新增母领域并分别建立五个 source 与一个 derived Method
- 同步 inventory、catalog、taxonomy、研究报告、文档和治理任务包
- 运行静态库、自测、项目门禁和治理校验

## Out of Scope
- 穷尽教材或建立百科
- 实现 selector、planner、runtime、Binding、数据库、在线 registry 或 UI
- 提供现实物理或化学实验、仪器设置、数值放行或专业决策
- 改变公共 Core Schema、权限模型或运行时状态机

## Task Package Tree
- ROOT
  ├─ TP-01 [branch] [P0] 六个基础领域深度抓取证据
  │  ├─ TP-01.01 [leaf] [P0] 线性代数与谱方法研究
  │  ├─ TP-01.02 [leaf] [P0] 拓扑与几何研究
  │  ├─ TP-01.03 [leaf] [P0] 电磁场方法研究
  │  ├─ TP-01.04 [leaf] [P0] 量子算子方法研究
  │  ├─ TP-01.05 [leaf] [P0] 溶液热力学与相平衡研究
  │  └─ TP-01.06 [leaf] [P0] 光谱结构解析研究
  ├─ TP-02 [leaf] [P0] 既有库缺口与重复审计
  ├─ TP-03 [leaf] [P0] 提炼新增算子与组合 Method
  ├─ TP-04 [leaf] [P0] 入库并同步目录文档
  └─ TP-05 [leaf] [P0] 验证、审查与交付收口

## Requirement Alignment
- 目标: 继续深度抓取线性代数谱方法、拓扑几何、电磁场方法、量子算子方法、溶液热力学相平衡和光谱结构解析，并沉淀为可审计算子
- approved plan 顶层步骤数: 5
- 编译后节点总数: 11
- 编译后叶子节点数: 10
- 对齐项: 用户要求继续深度抓取并参考历史上下文
- 对齐项: 当前库 346 source、50 derived；本轮只补有证据且不重复的新语义
- 对齐项: 数学、物理、化学优先，补足结构、场、算子、相平衡和证据汇合方法
- 计划摘要: 先完成六个领域的一手来源核验和语义缺口审计，再做静态入库、文档治理和全量验证；不扩展运行时。

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | No | 为线性代数谱方法、拓扑几何、电磁场方法、量子算子方法、溶液热力学相平衡和光谱结构解析建立权威来源、方法程序、迁移边界和未验证项 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究秩与零空间、基选择、正交投影、谱分解和低秩残差 |
| TP-01.02 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究连续性、连通性、紧致性、同伦不变量和局部到整体障碍 |
| TP-01.03 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究源场建模、对称面、叠加、势与边值问题和能流守恒 |
| TP-01.04 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究状态与可观测量、对易性、基表示、变分与微扰近似及概率归一 |
| TP-01.05 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究相律、化学势、活度逸度、相稳定和 Gibbs-Duhem 一致性 |
| TP-01.06 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 研究分子式约束、正交谱特征、片段连接、全证据一致性和参考条件审计 |
| TP-02 | ROOT | 1 | P0 | action | Yes | TP-01.01, TP-01.02, TP-01.03, TP-01.04, TP-01.05, TP-01.06 | 2 | No | No | 将六个领域方法与当前 396 个条目逐项比对，确定新增语义和交叉映射 |
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
