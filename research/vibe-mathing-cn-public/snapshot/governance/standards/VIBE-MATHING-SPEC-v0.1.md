---
id: STD-VIBE-MATHING-SPEC-V0.1
type: standard
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-09-07
review_cycle: P90D
version: 0.1
source: ADR-0000
related_gates: [GATE-0002]
---

# VIBE-MATHING-SPEC v0.1

本规范定义 `vibe-mathing-cn` 的最小可信研究闭环。它是项目级规范，不声称是 ISO、IEEE、AMS 或数学共同体统一标准。顶层任务编排的公共语言是 `Project → Workflow → Task → Step → Job`；其定义、状态轴和当前未实现边界见 [`RESEARCH-LIFECYCLE-MODEL-v0.1.md`](RESEARCH-LIFECYCLE-MODEL-v0.1.md)。

## 目标

从问题库出发，由非可信 Agent 探索候选，由受信验证链裁决；只有完整、保真、可独立复核并带有效证据的证明或反例进入解库派生视图。

## 方法层主线

本项目采用以下 Formal Methods 上位地图指导规格、验证方法和工具路由：

> **规格与语义 → 演绎验证/定理证明 → 模型检查 → 抽象解释 → SAT/SMT/符号推理（含符号执行）/决策过程 → 精化与程序综合**

它是方法地图而不是强制流水线：不同问题可以在不同层闭合或保持 open，但必须说明覆盖范围和证据边界。Lean 位于依赖类型理论型演绎验证/交互式定理证明；Lean 的六层栈是类型理论与 Kernel、语言与 elaboration、Proof Engineering、自动化与决策过程、Library Engineering、应用形式化/验证。完整分类和学习顺序见 [`FORMAL-METHODS-MAP.md`](FORMAL-METHODS-MAP.md)。

这一区分不能被弱化：SMT 或有限计算不是一般性定理证明，模型检查不是 Lean kernel check，工具可运行或自动化成功也不是数学 Result。项目的运行闭环仍然是 `Problem → Attempt → Result → Verification Artifacts`，方法地图与运行闭环是两个正交层次；五级任务生命周期与数学结果状态也必须保持正交。

## 规范词

- `MUST` / 必须：不满足即违反规范。
- `MUST NOT` / 禁止：出现即违反规范。
- `SHOULD` / 应当：默认遵守；偏离时必须记录理由和风险。

## 对象

- `Problem`：规范化、版本化的研究问题，回答“研究什么”。
- `Attempt`：一次 ResearchRun 的机器对象，回答“做过什么”。
- `Result`：一项原子数学主张及其证据账本，回答“真正知道了什么”。
- `Solution View`：从合格 Result 派生的只读解库视图，不是可独立写入的真相源。
- `Verification Artifact`：可复查的计算记录、审查记录、证明证书、内核输出或忠实性审计产物。

## 三条基本法则

### R1 — 候选隔离

系统事实链必须是：

```text
Problem → Attempt → Result
```

- Agent 只能创建 Attempt 和候选 Result，禁止自行宣布问题已解决。
- Result 必须引用产生它的 Attempt，Attempt 必须引用同一个 Problem。
- Solution View 必须从合格 Result 派生，禁止成为第二套人工维护的真相源。

### R2 — 验证准入

只有独立验证链可以改变系统“真正知道什么”。Result 必须分开记录：

```text
outcome × evidence
```

证据是能力集合，不是 `numeric < symbolic < human < kernel` 的线性等级。至少区分：

```text
numeric_check
symbolic_check
human_review
kernel_check
counterexample_check
axiom_escape_audit
statement_faithfulness
prior_art_review
```

Solution View 只允许两种闭合结果：

```text
proof + established
counterexample + refuted
```

两者都必须具备当前有效的独立直接验证与 `statement_faithfulness=accept`。`kernel_check` 只证明形式化陈述及证明项通过内核检查，不能替代陈述忠实性、新颖性、可读性或数学价值审查。

### R3 — 证据守恒

每项可晋升结论必须形成完整链条：

```text
Problem → Attempt → Result → Verification Artifacts
```

- 证据记录和失效记录必须只追加、不可覆盖历史。
- 当前结论和 Solution View 必须由当前有效证据重新派生。
- 新证据可以使结论晋升，也可以使其变为 `inconclusive`、`withdrawn` 或 `refuted`。
- Agent 自评不是独立证据；来源、引用、验证产物或陈述忠实性断链时，Result 必须退出 Solution View。

## 操作层要求

以下要求落实三条基本法则，但不是新的基本法则：

1. **Problem Contract**：冻结原陈述、量词、定义、来源、版本和允许公理。
2. **Tool Disclosure**：记录模型、版本、工具、输入摘要、日期、计算资源和人类干预。
3. **Balanced Search**：应当同时搜索证明、反例、变体、边界条件和既有文献。
4. **Versioned Repair**：保存证明稿版本和 obligation ledger；局部修补后重验受影响依赖。
5. **Independent Closure**：最终验证必须来自独立工具或领域专家；同模型、同信任域的新会话只能承担对抗性审稿，不能单独授予 `established`。
6. **Fail-Closed Formalization**：固定 proof-assistant 与库版本，扫描逃逸机制，检查使用公理，并独立审查 statement faithfulness。
7. **Append-Only Invalidation**：发现错误时追加失效记录，不删除或覆盖原证据。

## 当前机器实现

- 对象契约：`problem-library/schema/canonical-problem.schema.json`、`research/schema/attempt.schema.json`、`result-library/schema/result.schema.json`。
- 准入裁决：`scripts/validate_research_spaces.py`。
- 负例验证：`scripts/test_research_spaces.py`。
- 治理门禁：`governance/architecture-gates/rules/GATE-0002-数学成果晋升必须有充分证据和独立验证.md`。
- 架构依据：`governance/decisions/adr/ADR-0000-问题空间到解空间的最小闭环.md`。
- 方法地图：`governance/standards/FORMAL-METHODS-MAP.md`，只负责方法层定位，不授予工具能力或 Result 状态。

## 成熟度边界

本规范从 v0.1 起是当前项目规则；现有 schema、校验器和负例覆盖核心准入不变量，并要求 kernel 直接验证与公理/逃逸审计组合使用。Lean 工具链和代表性外部案例尚未完成固定版本本地复跑，因此不得声称“完整工具链认证”或“外部标准符合性认证”。

## 一句话

> Agent 产生候选，验证链建立事实，证据账本保存事实。
