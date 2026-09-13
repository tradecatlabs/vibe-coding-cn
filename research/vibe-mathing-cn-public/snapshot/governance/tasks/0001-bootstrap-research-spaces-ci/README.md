# Task Overview

- Task ID: `0001`
- Slug: `bootstrap-research-spaces-ci`
- Objective: 搭建问题空间到解空间的最小研究闭环、CI 和 GitHub 交付。
- Status: `in-progress`

## In Scope

- canonical Problem、Attempt、Result 三个机器契约及空真相源。
- research/result-library 一级空间、解库派生索引和晋升负例。
- 最小 governance、ADR、数学成果晋升 Gate 和模块上下文。
- `make check`、`make check-full`、GitHub Actions 与公开仓库卫生。
- 初始化 Git，安全推送空远端 `vibemathing/vibe-mathing-cn` 并核验 CI。

## Out of Scope

- 自动归一化 6012 条来源记录。
- 生成任何数学“解”、训练模型或实现通用求解 Agent。
- 引入数据库、知识图谱、向量检索、多 Agent 或部署服务。
- 公开分发本地 PDF、动态网页快照、可重建来源数据和许可未知的本机 skill snapshot。

## Task Package Tree

- TP-01：冻结 Problem/Attempt/Result 契约与派生边界。
- TP-02：建立研究空间、成果空间、治理和文档。
- TP-03：建立可移植/完整两级质量门和 GitHub CI。
- TP-04：公开仓库审查、Git 提交、推送和远端 CI 核验。

## Requirement Alignment

用户明确要求搭建空间、CI 和相关能力，并推送到指定 GitHub 仓库。结构遵循此前确认的“问题库 → Agent 研究 → 验证 → 解库”。

## Task Package Overview

| ID | Parent | Depth | Priority | Type | Leaf | Depends On | Ready | Objective |
|---|---|---:|---|---|---|---|---|---|
| TP-01 | ROOT | 1 | P0 | contract | Yes | - | No | 固定三个核心对象与解库晋升规则 |
| TP-02 | ROOT | 1 | P0 | architecture | Yes | TP-01 | No | 创建空间、治理和局部文档 |
| TP-03 | ROOT | 1 | P0 | ci | Yes | TP-02 | No | 创建统一检查和 GitHub Actions |
| TP-04 | ROOT | 1 | P0 | delivery | Yes | TP-03 | Yes | Git 初始化、推送和远端核验 |

## Reading Order

1. `CONTEXT.md`
2. `PLAN.md`
3. `ACCEPTANCE.md`
4. `ACCEPTANCE_CHECKLIST.md`
5. `TODO.md`
6. `STATUS.md`
