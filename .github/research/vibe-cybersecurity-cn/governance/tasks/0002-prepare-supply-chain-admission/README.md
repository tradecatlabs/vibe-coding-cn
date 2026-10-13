# Task Overview

- Task ID: `0002`
- Slug: `prepare-supply-chain-admission`
- Objective: 把 0001 研究候选收敛为分波次、可审计、可验证且默认不执行的供应链准入候选表。
- Status: `Done`

## In Scope

- 读取 0001 的 18 个 MVP 候选，不复制上游事实。
- 定义准入生命周期、八个正式门禁、风险配置和实施波次。
- 建立机器准入目录、跨目录校验器和自动生成表格。
- 同步项目操作模型、工具链和目录拓扑。

## Out of Scope

- 选择具体 release、commit、镜像或数据快照。
- 下载、安装、拉取镜像、访问远程 API 或执行扫描。
- 把任何候选标为 `verified`、`admitted` 或 `enabled`。
- 把当前排序包装成实验胜出或生产批准。

## Task Package Tree

```text
ROOT
├── TP-01 准入状态与门禁契约
├── TP-02 首批候选与波次编排
├── TP-03 机器校验与自动视图
└── TP-04 项目文档同步与 closeout
```

## Requirement Alignment

用户要求开始制作准备纳入供应链的候选表。本任务交付的是“准入队列”，不是“安装清单”：18 个研究 MVP 全部进入候选队列，但不授予具体任务运行权，正式纳入必须逐项完成固定版本和八个门禁。

## Task Package Overview

| ID | Parent | Depth | Priority | Type | Leaf | Depends On | Ready | Objective |
|---|---|---:|---|---|---|---|---|---|
| TP-01 | ROOT | 1 | P1 | security-contract | Yes | - | No | 定义生命周期、门禁和 fail-closed 语义 |
| TP-02 | ROOT | 1 | P1 | catalog | Yes | TP-01 | No | 编制 18 项候选和四个波次 |
| TP-03 | ROOT | 1 | P1 | validation | Yes | TP-02 | No | 校验研究血缘、状态和准入条件 |
| TP-04 | ROOT | 1 | P1 | governance | Yes | TP-03 | No | 同步项目真相源并完成验证 |

## Reading Order

1. `ADMISSION_POLICY.md`
2. `ADMISSION_CANDIDATE_TABLE.md`
3. `admission-candidates.json`
4. `STATUS.md`
5. `ACCEPTANCE.md`
6. `REVIEW.md`
