# Task Overview
- Task ID: `0010`
- Slug: `expand-multidomain-operator-library`
- Objective: `深度调研并扩展来自数学、物理学、化学、计算机科学、科学方法、系统科学、复杂性科学、算法、软件工程、编程、机器学习、深度学习与科研等领域的问题求解算子库`
- Status: `Done`

## In Scope
- 以官方课程、标准、政府/学术机构资料为证据来源，提炼可执行问题求解算子
- 新增数学、物理、化学以及计算机科学、科学方法、系统科学、复杂性科学、算法、软件工程、编程、机器学习、深度学习与科研条目
- 更新 source inventory、packs、catalog、研究报告、目录文档和治理上下文
- 运行 Core/Profile、项目门禁、治理校验和任务级验证

## Out of Scope
- 实现物理/化学实验、仿真器、训练系统、selector、planner、runtime 或 Binding
- 修改公共 Core Schema 以强制某个学科的语义字段
- 声称新增条目已在真实 Harness、生产任务或实验中验证有效
- 读取凭据、部署、推送或执行破坏性 Git 操作

## Task Package Tree
- ROOT
  ├─ TP-01 [leaf] [P0] 建立跨学科证据矩阵
  ├─ TP-02 [leaf] [P0] 定义算子语义与领域边界
  ├─ TP-03 [leaf] [P0] 入库并同步目录文档
  └─ TP-04 [leaf] [P0] 验证、审查与交付收口

## Requirement Alignment
- 目标: 深度调研并扩展来自数学、物理学、化学、计算机科学、科学方法、系统科学、复杂性科学、算法、软件工程、编程、机器学习、深度学习与科研等领域的问题求解算子库
- approved plan 顶层步骤数: 4
- 编译后节点总数: 4
- 编译后叶子节点数: 4
- 对齐项: 用户要求深度调研并持续增加更多领域、更多学科的可调用思维模型和方法论算子
- 对齐项: 数学、物理、化学是第一优先级，其他点名领域必须得到可检索覆盖
- 对齐项: 现有库把内容与治理边界分开，新增领域应沿用该终态而不是扩大公共 Core
- 计划摘要: 先以一手资料建立跨学科证据矩阵，再筛出最小高价值算子，写入现有 Reference Profile，最后同步治理并以全量门禁收口。

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | documentation | Yes | - | 1 | Yes | No | 从一手资料提炼每个目标领域可执行、可证伪、可记录证据的候选方法 |
| TP-02 | ROOT | 1 | P0 | feature | Yes | TP-01 | 2 | No | No | 把候选方法写成 MentalModelSpec、OperatorSpec 或 MethodSpec，明确适用、证据、失败和恢复 |
| TP-03 | ROOT | 1 | P0 | feature | Yes | TP-02 | 3 | No | No | 更新 pack、catalog、计数、研究报告、README、模块上下文、ADR/QA 与 source-of-truth |
| TP-04 | ROOT | 1 | P0 | testing | Yes | TP-03 | 4 | No | No | 以全量门禁、治理检查、任务证据和 review 证明当前扩展可复核且可回滚 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
