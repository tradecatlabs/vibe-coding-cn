# Task Overview
- Task ID: `0008`
- Slug: `combat-readiness-gap`
- Objective: `梳理项目现状，量化实战（真实授权协议 fork 级审计）就绪度，产出差距清单与里程碑路径`
- Status: `Done`

## In Scope
- 盘点 0001-0007 交付物与工具链、靶场、验证控制面、skills 供应链现状。
- 量化"对真实授权协议做 fork 级审计"的综合就绪度（0-100）与能力域得分。
- 产出 P0/P1/P2 差距清单与 M1-M4 里程碑路径，落盘 `governance/context/COMBAT_READINESS.md`。
- 同步治理文档（拓扑、操作模型、上下文地图、README、任务索引、AGENTS）。

## Out of Scope
- 不选择或拉取任何真实协议仓库（等待用户指定授权目标）。
- 不实现端到端审计管线代码（属于 M1 工程任务）。
- 不接入 RPC、情报源、报告模板（P1/P2 工程任务）。
- 不把靶场结论外推为真实协议审计结论。

## Task Package Tree
```text
ROOT
├── TP-01 现状盘点与证据核实
├── TP-02 就绪度评分与差距清单
├── TP-03 治理同步
└── TP-04 closeout 校验
```

## Requirement Alignment
- 用户要求"开始整理和梳理项目，距离实战还差多少"：本任务输出量化就绪度、
  差距清单与可执行里程碑，作为 M1 启动前的决策依据。
- 实战定义：给定协议仓库 + 书面授权，产出候选漏洞 -> 独立复现 -> 证据归档 ->
  审计报告的端到端流程，且结论可复查。

## Task Package Overview
| Node | Output | Acceptance |
|---|---|---|
| TP-01 | 现状盘点表（任务/工具/靶场/控制面/skills） | 每项绑定真实证据 |
| TP-02 | `COMBAT_READINESS.md` | 评分、差距清单、里程碑齐全 |
| TP-03 | 治理文档同步 | 拓扑/操作模型/context-map/README/INDEX/AGENTS 更新 |
| TP-04 | closeout 校验 | task docs + governance strict/health 全绿 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
