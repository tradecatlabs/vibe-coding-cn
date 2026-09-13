---
id: GOV-PROJECT-OPERATING-MODEL
type: context
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-08-13
review_cycle: P90D
---

# Project Operating Model

本文件是 Vibe Mathing 的项目级操作模型。根 README 面向使用者说明项目，目录 README/AGENTS 管理局部事实，本文件维护跨模块真相源、变更路由和验收边界。

## 项目一句话定义

`vibe-mathing-cn` 是一个用非可信生成器产生候选，再由受信验证链把满足验收谓词的证明或反例派生到解空间的 AI 数学研究工作台。

## 顶层生命周期模型

项目的顶层组织采用五级结构：

```text
Project → Workflow → Task → Step → Job
```

`Project` 定完整目标，`Workflow` 定任务网络，`Task` 定输入/输出工作单元，`Step` 定具体操作，`Job` 是 Step 的一次有界执行实例。Job 不是 Task 的直接运行实例；重试创建新的 Job，恢复同一 Job 必须绑定已验证 checkpoint。

这五级结构描述目标如何组织和执行；`ProblemContract → Attempt → Result` 描述数学事实如何定义和裁决，二者正交。当前公共仓库把该模型作为架构与路由语言，尚未宣称拥有通用五级持久化 schema、DAG 调度器或多 Worker 生产能力。完整口径见 [`RESEARCH-LIFECYCLE-MODEL-v0.1.md`](../standards/RESEARCH-LIFECYCLE-MODEL-v0.1.md)。

## 业务模型

- 核心用户：使用 AI 做数学探索、计算、证明和形式化验证的研究者与工程师。
- 顶层组织：`Project`、`Workflow`、`Task`、`Step`、`Job`；分别负责目标、任务网络、工作单元、操作和有界执行。
- 数学事实对象：`Problem`、`Attempt`、`Result`，不被运行生命周期替代。
- 关键流程：来源记录 → canonical Problem → Workflow/Task/Step/Job → Attempt → candidate Result → trusted verification gate → solution view。
- 不属于本项目：保证自动解决开放问题、把有限实验当一般证明、把模型自评当独立验证、镜像未获授权的文献全文。

## 技术模型

- 主要运行形态：Git 管理的 Markdown、JSON/JSONL、JSON Schema、Python 单机 runtime/校验器、固定 Lean/Mathlib fixture 和项目级 Codex skills。
- 方法层主线：规格与语义 → 演绎验证/定理证明 → 模型检查 → 抽象解释 → SAT/SMT/符号推理（含符号执行）/决策过程 → 精化与程序综合；Lean 位于依赖类型理论型演绎验证/交互式定理证明，不等于整个形式化方法版图。完整地图见 `governance/standards/FORMAL-METHODS-MAP.md`。
- 数据事实源：来源记录在 `problem-library/records/problems.jsonl`；规范化问题在 `canonical-problems.jsonl`；研究与成果分别在 `research/records/` 和 `result-library/records/`。
- 派生视图：`result-library/indexes/solutions.json`，禁止绕过 Result 真相源直接录入。
- 外部依赖：公开问题来源、文献数据库、Python 数学/校验库、Lean/Mathlib；上游 skill 版本由 `vendor/sources.lock.json` 固定，形式工具链由 fixture 固定。
- 主要验证入口：`make check`；完整单机生产闭环为 `make check-production`；本机 ignored 材料加强验证为 `make check-full`。

## 工具链模型

工具链的命令、依赖、CI 边界、成本与回滚以 `context/TOOLCHAIN_MODEL.md` 为准。核心约束是：CI 只消费可版本化资产，本地 ignored 材料只进入 `make check-full`。

## 目录和真相源地图

| 事实类型 | 真相源 | 备注 |
|---|---|---|
| 项目定位与使用入口 | `README.md` | 面向使用者 |
| Agent 运行边界 | `AGENTS.md` | 数学真实性与目录维护规则 |
| 来源问题观察 | `problem-library/records/problems.jsonl` | 不等于 canonical Problem |
| 规范化问题 | `problem-library/records/canonical-problems.jsonl` | 版本化陈述、稳定来源 URL 与可选本地来源记录 ID |
| 研究尝试 | `research/records/attempts.jsonl` | Attempt lifecycle 不表达数学结论 |
| 运行 checkpoint | `research/runs/` | Git ignored；schema 化状态、预算、恢复与取消 |
| verifier 信任策略 | `research/verifiers.json` | role、trust domain、capability、output policy |
| 验证产物与回执 | `research/artifacts/` | 可信根、现场 SHA-256、禁止 symlink/覆盖 |
| 研究成果 | `result-library/records/results.jsonl` | `outcome × evidence` 二维状态与追加证据账本 |
| 完整解视图 | `result-library/indexes/solutions.json` | 从 Result 派生 |
| 文献书目 | `literature/catalog/*.jsonl` | 电子书二进制保持本地忽略 |
| 研究方法 | `.codex/skills/` | 只保存 active owner skills |
| Vibe-Mathing 核心规范 | `governance/standards/VIBE-MATHING-SPEC-v0.1.md` | 三条基本法则及操作层要求 |
| 形式化方法地图 | `governance/standards/FORMAL-METHODS-MAP.md` | 方法层主线、Lean 定位、Lean 六层栈与学习顺序 |
| 全生命周期模型 | `governance/standards/RESEARCH-LIFECYCLE-MODEL-v0.1.md` | Project → Workflow → Task → Step → Job；数学对象与执行层正交 |
| 供应链版本 | `vendor/sources.lock.json` | URL、commit、许可和导入映射 |
| 项目治理 | `governance/` | 标准、ADR、Gate 和任务证据 |
| CI 入口 | `.github/workflows/ci.yml` | portable 与固定 Lean production-loop 双门 |

## 不可违反的边界

1. 来源记录不自动成为 canonical Problem。
2. Attempt 不自动成为 Result，Result 不自动成为 Solution。
3. 数值/符号证据、局部/条件结果和失败路径不能关闭原问题。
4. 完整解必须是 `proof + established` 或 `counterexample + refuted`，并具备当前有效的独立直接验证和 statement faithfulness `accept`。
5. proof assistant 成功只证明形式化陈述，仍需审计其是否忠实表达原问题。
6. 证据能力按集合偏序表达；不得把 outcome 与 numeric/human/kernel 压成单一等级。
7. Result 与 Attempt 必须引用同一个 Problem；独立性由 registry trust domain 派生，准入证据必须位于可信根、现场摘要匹配且满足 verifier output policy。
8. CI 不访问外部来源、不上传本地文献、不修改研究真相源。
9. UnsolvedMath 未明确许可的目录内容只作为本地可重建数据，不进入公开 Git。

上述研究闭环的规范真相源是 `standards/VIBE-MATHING-SPEC-v0.1.md`；本文件只维护项目级摘要和导航，不复制第二套规范。

## 变更入口

- 改对象字段：同步修改 owner schema、局部 README/AGENTS、校验器与回归测试。
- 改晋升规则：同步修改 Result schema、校验器、负例、GATE-0002 和 ADR。
- 改工具/CI：同步修改 `Makefile`、`scripts/check.sh`、`.github/workflows/ci.yml` 与 `TOOLCHAIN_MODEL.md`。
- 改方法层地图：同步修改 `FORMAL-METHODS-MAP.md`、相关 skill 的职责边界、工具目录和 README 的定位摘要；不得把教学地图写成运行能力或数学证据。
- 改生命周期模型：同步修改 `RESEARCH-LIFECYCLE-MODEL-v0.1.md`、Project Operating Model、README、research/result 边界和 GEO 事实资产；不得把设计目标写成已实现调度能力。
- 新增目录或重划职责：同步根与目标目录 README/AGENTS、PROJECT-TOPOLOGY 和 module context。

## 验证入口

```bash
make check
make check-production
make check-full
python3 governance/tools/governance_context_bundle.py --project-root . --task-type docs
```

## 最近一次 review

- 日期：2026-08-13
- 结论：单机 runtime、唯一 writer、可信回执、SymPy E2E 与固定 Lean fixture 已建立；数学业务记录仍为空。
- 后续动作：接入真实外部 reviewer attestation，并用公开非开放定理校准自然语言到 Lean 的人工 statement faithfulness。
