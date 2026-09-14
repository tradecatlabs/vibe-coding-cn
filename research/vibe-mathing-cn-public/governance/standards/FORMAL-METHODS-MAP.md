---
id: STD-FORMAL-METHODS-MAP
type: standard
status: current
owner: engineering
created: 2026-09-07
last_reviewed: 2026-09-07
review_cycle: P90D
version: 0.1
source: user-provided map reconciled with official public references
related_gates: [GATE-0002]
---

# 形式化方法技术地图与 Lean 定位

本文件冻结本项目的**方法层主线**。它是学习、工具选型和能力路由地图，不是 ISO/IEEE/AMS 标准，也不是任何工具或数学结果的认证。

## 一句话主线

> **规格与语义 → 演绎验证/定理证明 → 模型检查 → 抽象解释 → SAT/SMT/符号推理（含符号执行）/决策过程 → 精化与程序综合**

这是一张上位地图，不是要求每个问题依次经过六站的流水线。第一层回答“命题或程序到底是什么意思”；后面的验证范式回答“在什么假设、状态空间、逻辑和证据边界内可以检查它”。NASA 的 DO-333 形式化方法案例明确展示了 theorem proving、model checking 和 abstract interpretation 三类方法；SAT/SMT、符号执行、静态分析和综合是围绕这些方法展开的自动化与实现技术族。

## Formal Methods 六分法

| 核心类别 | 主要问题 | 代表性体系/来源 | 本项目定位 | 学习优先级 |
| --- | --- | --- | --- | --- |
| **① 形式化规格与程序语义** | 要证明的对象、状态、程序和性质究竟是什么意思？ | Floyd/Hoare、操作语义/指称语义、Software Foundations | `ProblemContract` 的 statement、domain、quantifiers、definitions、assumptions 和 acceptance 是这一层的工程落点 | 必学 ★★★ |
| **② 演绎验证 / 定理证明** | 从公理、定义和规格构造可检查的正确性证明 | Hoare Logic、Coq/Rocq、Isabelle、Lean、依赖类型理论 | `math-proof` 形成证明义务；`math-formalization` 将固定陈述与 proof term 交给 kernel 检查 | 必学 ★★★ |
| **③ 模型检查** | 自动遍历或符号探索状态空间，检查安全性、活性和时序性质 | Clarke–Emerson–Sifakis、SPIN、TLA+、NuSMV；Baier–Katoen | 横向理解状态空间与时序验证；当前公开垂直切片不等于已准入完整 model checker | 懂框架 ★★ |
| **④ 抽象解释 / 静态分析** | 用语义的安全过近似而非枚举全部状态，检查可达性、区间、数据流和不变量 | Patrick Cousot、Radhia Cousot、Frama-C 等 | 用来理解 sound over-approximation 与 false positive/precision trade-off；不把工具目录当运行证据 | 懂思想 ★★ |
| **⑤ SAT / SMT / 符号推理（含符号执行） / 决策过程** | 把证明义务、路径条件或程序约束转成可自动求解的逻辑问题 | SAT/SMT 社区、Z3、de Moura–Bjørner、rewriting/decision procedures | 当前公开 SMT-LRA fixture、有限计算和 canary 属于有界自动化证据；不能单独关闭一般数学命题 | 必学概念 ★★★ |
| **⑥ 精化、验证生成与程序综合** | 从规格逐步得到实现，或自动生成待验证实现/验证条件 | refinement calculus、B/Event-B、program synthesis、verification-condition generation | 当前作为后续扩展方向；不因模板、生成器或代码能运行就自动得到 Result | 后学 ★ |

分类之间不是互斥的：符号执行可能调用 SMT，模型检查可能使用抽象或 SAT，演绎验证也可能使用自动化决策过程。分类的作用是先固定“保证来自哪里”，再谈工具名称。

## Lean 的准确位置

**Lean ≠ 形式化方法的全部。** 它的主位置是：

```text
Formal Methods
├── Specification & Semantics
├── Verification Methods
│   └── Deductive Verification / Interactive Theorem Proving
│       └── Dependent-Type-Theory Proof Assistant
│           └── Lean  ← 本项目的形式化主战场
├── Model Checking
├── Abstract Interpretation
├── Symbolic Reasoning / Symbolic Execution / SAT / SMT
└── Refinement / Synthesis
```

Lean 官方参考手册将 Lean 定位为基于依赖类型理论的 interactive theorem prover，目标同时包括数学与 software verification；其 minimal kernel 检查 proof terms，tactic 产生的核心项最终仍由 kernel 检查。因此本项目坚持：**automation 找证明，kernel 验证明；kernel 检查不替代 statement-faithfulness 审查。**

Lean 与邻近方法有接口，但不应混称：

- `simp`、rewriting、arithmetic tactics 和 `grind` 是 Lean 内的自动化/决策过程，不等于 Lean 变成 model checker 或 abstract interpreter；
- SMT/符号执行可以产生候选、路径条件或辅助义务，但其结果是否足以支撑原命题取决于规格、覆盖范围、独立性和 verifier policy；
- Mathlib 是 Lean 的大型数学库，library engineering 和 API 搜索是形式化工作的重要组成部分；
- Lean 成功构造的 theorem 只说明**该 Lean 陈述**有被 kernel 接受的 proof term，仍需确认它忠实表达原始自然语言问题。

Lean 4.22 release notes 记录了 SMT-style `grind` 的发布；这是版本历史和能力地图中的一个例子，不是本仓库当前安装状态或 verifier-admitted 证据。当前具体 toolchain 仍以 fixture 的 `lean-toolchain`、lockfile 和现场检查为准。

## Lean 六层栈

以后整理 Lean 资料时，按以下二级地图归档，而不是把教程章节直接当作领域地图：

1. **类型理论 / Kernel**：依赖类型理论、Curry–Howard、`Prop`/`Type`、归纳类型、递归、universes、definitional equality；
2. **Lean 语言与 elaboration**：函数式编程、dependent functions、structures、typeclasses、implicit arguments、coercions 和 elaboration；
3. **Proof Engineering**：proof term、`apply`、`rw`、induction、`simp`、`calc`、结构化证明和 lemma decomposition；
4. **自动化与决策过程**：rewriting、simplification、算术求解器、`grind` 及其他 tactics；
5. **Library Engineering**：Mathlib、API 搜索、typeclass hierarchy、canonical abstraction 和已有 lemma 复用；
6. **Formalization / Verification Applications**：数学形式化，以及程序、编译器、协议和算法验证。

项目 skill 的对应关系是：`math-proof` 主要覆盖证明义务和 proof engineering，`math-formalization` 覆盖 Lean 陈述、proof term、kernel/axiom/escape/faithfulness 分离，`math-computation` 覆盖有限计算与横向自动化，`math-discovery` 负责来源和语义边界，router 只选择当前最需要的一条路线。

## 本项目的映射

```text
规格与语义                 → ProblemContract
问题来源与语义审查          → math-discovery
证明义务与演绎论证          → math-proof
有限计算/反例/符号检查      → math-computation
SMT/决策过程               → 有界 fixture、canary、受限 adapter
形式化证明                  → math-formalization + Lean/Mathlib fixture
受信裁决                    → evidence capabilities + independent verification
派生事实                    → Result → ResearchBundle / Solution View
```

当前公共仓库直接展示的是固定 SymPy、SMT-LRA 和 Lean/Mathlib 工程切片；它没有因此声称具备完整 model checking、abstract interpretation 或 program synthesis 生产能力。工具成熟度 registry 的状态是证据/运行边界，不是安装清单；没有现场 evidence 的方法保持为 surveyed/source-locked。

## 推荐学习顺序

主干：

```text
数理逻辑 / Curry–Howard
        ↓
Lean dependent type theory + inductive types
        ↓
Lean 基本证明、induction、equality、simp
        ↓
形式语义、Hoare Logic、verification conditions
        ↓
Mathlib 与大型形式化工程
```

横向视野：

```text
SAT/SMT 与 Lean automation 的关系
        ↓
Model Checking 与 Abstract Interpretation
```

专业方向再从这里展开：Separation Logic、程序验证、验证编译器、精化和综合等。复杂 category theory、compiler internals、kernel 实现细节、高级 metaprogramming 和模型检查前沿算法都是地图上的区域，但不是入门入口。

## 对本项目的硬边界

- `ProblemContract` 是规格与语义层，不是随意 prompt；陈述、定义域和量词不清时不开始研究。
- 来源 catalog、CandidateObservation、Issue/PR、证明草稿、有限计算和工具标签都不是自动的 Result。
- Lean kernel check 只检查形式化陈述和 proof term；它不替代自然语言陈述忠实性、公理/逃逸、独立性和数学价值审查。
- Model checking、abstract interpretation、SMT 和 symbolic execution 的“能自动跑”不等于覆盖了原命题的全部量词。
- 只有通过当前 ProblemContract、独立验证、适用 evidence 能力和 statement-faithfulness 的 proof/counterexample Result，才能进入派生 Solution View。

## 权威起点

- [NASA NTRS: Formal Methods Case Studies for DO-333](https://ntrs.nasa.gov/citations/20140004055)：展示 theorem proving、model checking、abstract interpretation 三类案例；
- [Baier & Katoen, Principles of Model Checking](https://mitpress.mit.edu/9780262026499/principles-of-model-checking/)：模型检查经典教材入口；
- [Lean Language Reference](https://lean-lang.org/doc/reference/latest/)：Lean 的官方定位、依赖类型理论、kernel 与 tactic 边界；
- [Dependent Type Theory](https://lean-lang.org/theorem_proving_in_lean4/Dependent-Type-Theory/)：Lean 依赖类型理论基础；
- [Lean 4.22.0 release notes](https://lean-lang.org/doc/reference/latest/releases/v4.22.0/)：`grind` 等版本能力的历史记录；
- [Mathematics in Lean — Introduction](https://leanprover-community.github.io/mathematics_in_lean/C01_Introduction.html)：以 Mathlib 为基础的数学形式化学习入口；
- [Lean Learn](https://lean-lang.org/lean4/doc)：Lean 数学形式化与 software verification 的官方学习入口。

引用这些页面只能支持方法定位和学习地图，不能支持本项目已经解决任何数学问题的声明。
