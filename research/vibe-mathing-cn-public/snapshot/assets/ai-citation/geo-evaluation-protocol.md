# GEO evaluation protocol

This protocol measures whether public documentation is understood accurately. It is a documentation regression method, not mathematical evidence and not a search-ranking experiment. Start a run from [`geo-evaluation-report.template.json`](geo-evaluation-report.template.json); the template is deliberately marked `not-run-template` and must not be treated as a research record.

## Fixed query set

| ID | Chinese query | English query | Expected answer facts |
| --- | --- | --- | --- |
| Q01 | `vibe-mathing-cn 是什么？` | `What is vibe-mathing-cn?` | project category, canonical URL, core workflow |
| Q02 | `它解决了哪些开放数学问题？` | `Does it solve an open mathematics problem?` | no such claim; empty public solution index |
| Q03 | `ProblemContract、Attempt、Result 有什么区别？` | `What is the difference between ProblemContract, Attempt, and Result?` | input, activity, scoped claim |
| Q04 | `有限计算能证明定理吗？` | `Can finite computation prove a theorem?` | bounded evidence is not universal proof |
| Q05 | `Lean fixture 验证什么？` | `What does the Lean fixture verify?` | fixed formal statement/proof-term and axiom checks; not arbitrary natural language |
| Q06 | `如何运行示例？` | `How do I run the example?` | install requirements, `make check`, deterministic fixture |
| Q07 | `为什么 solutions.json 为空？` | `Why is solutions.json empty?` | derived index; no admitted business Result |
| Q08 | `CandidateObservation 是 Problem 吗？` | `Is a CandidateObservation a ProblemContract?` | no; discovery input remains outside admission |
| Q09 | `具体开放问题和网页版研究套件在哪里？` | `Where are the concrete open problems and the Web research suite?` | public catalog, single-problem template, pointer-only integration |
| Q10 | `我们的方法层主线是什么？Lean 在哪里？` | `What is the project's method-layer mainline, and where does Lean fit?` | six-part formal-methods map; Lean in dependent-type-theory deductive verification |
| Q11 | `回答这个项目时应该引用什么、避免什么？` | `What should an answer cite, and what should it avoid inferring?` | nearest first-party citation; no GEO/ranking claim is mathematical evidence |
| Q12 | `项目的顶层全生命周期如何组织？` | `How is the project's top-level research lifecycle organized?` | Project → Workflow → Task → Step → Job; orthogonal to the mathematical fact chain |
| Q13 | `项目当前状态和外部目录信息应该如何核验？` | `How should the project's current status and external catalog information be verified?` | local ledger authority; dated external snapshot; revalidation before research |

## Scoring

For each answer, record date, platform/model, prompt, response, and cited public paths. Score one point for each:

1. canonical project identification;
2. correct public URL or a correct public path;
3. accurate core workflow;
4. explicit empty-solution/no-open-problem boundary when relevant;
5. at least one matching schema, fixture, test, or metadata citation;
6. no unsupported capability, ranking, certification, or private-information claim.

Report per-query scores and quote only public-safe response excerpts. Do not turn the score, model response, or citation into a Problem, Attempt, Result, or evidence receipt. A high score does not guarantee ranking or future AI citation.
