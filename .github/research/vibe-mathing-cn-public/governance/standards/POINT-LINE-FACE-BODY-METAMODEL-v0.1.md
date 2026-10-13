---
id: GOV-STANDARD-PLFB-METAMODEL-001
type: standard
status: current
owner: engineering
created: 2026-09-07
last_reviewed: 2026-09-07
review_cycle: P90D
---

# Point–Line–Face–Body Metamodel v0.1

## 1. Purpose

Vibe Math uses **Point–Line–Face–Body (PLFB)** as its single conceptual metamodel root.

- **Point**: a stable, addressable object with identity and type.
- **Line**: a typed, directed relationship between Points.
- **Face**: a bounded knowledge or operation dimension that owns allowed Point and Line types.
- **Body**: a reference-only composition of multiple Faces and cross-face Lines for one declared scope.

PWTSJ, OSPS, Formal Methods, ProblemContract, Evidence, and Result are not parallel roots. They are Faces or models inside Faces.

## 2. Root invariants

1. Every stable domain object maps to exactly one declared Point type.
2. Every stable relationship maps to exactly one declared Line type with source and target types.
3. Every Point and Line type has one owner Face.
4. Cross-face Lines must declare their source Face, target Face, direction, and binding rule.
5. A Body references owner truth sources; it does not copy or rewrite their records.
6. Operational, mathematical, evidence, and publication states remain separate axes.
7. No lower-level success may silently close a higher-level mathematical claim.

## 3. Face map

| Face | Scope | Representative Points |
|---|---|---|
| F01 Identity & Scope | object identity, revisions, digests, and composition scope | Body, Snapshot, Repository |
| F02 Source & Literature | source observations, citations, and literature identity | Source, SourceObservation, Citation, LiteratureRecord |
| F03 Semantics & Problem | frozen statement, domain, quantifiers, assumptions, and acceptance | ProblemContract, Definition, Statement, Assumption |
| F04 Outcome Space / OSPS | dynamic outcome graph and search frontier | OutcomeNode, OutcomeFrontier, Obstruction |
| F05 Process / PWTSJ | execution decomposition | Project, Workflow, Task, Step, Job, Checkpoint |
| F06 Method & Representation | mathematical methods, representations, strategies, and invariants | Method, Representation, ToolPlan, Invariant |
| F07 Research Route & Obligation | attempts, routes, obligations, dependencies, and failed routes | Attempt, Route, ObligationGraph, Obligation, FailedRoute |
| F08 Candidate & Artifact | immutable untrusted candidates and checkable artifacts | CandidateArtifact, ProgramArtifact, DatasetArtifact, Certificate |
| F09 Evidence & Verification | verifiers, receipts, evidence links, reviews, and invalidation | Verifier, EvidenceReceipt, EvidenceLink, SemanticReview |
| F10 Result & Solution View | admitted scoped claims and derived views | Claim, Result, ResearchBundle, SolutionView |
| F11 Observation, Feedback & Learning | observable events, decisions, lessons, and next obligations | Observation, StateDelta, Decision, Lesson |
| F12 Capability, Resource & Governance | agents, tools, runtimes, budgets, authorization, policy, gates, and risk | Agent, Tool, Runtime, Budget, Policy, Gate |
| F13 Portfolio, Publication & Projection | portfolio composition and gated public projections | PortfolioItem, ProjectCard, WikiPage, PublicClaim |

The table is a public conceptual map. It is not a claim that every listed Point has a dedicated persistent schema or runtime service.

## 4. F05: PWTSJ process face

The public execution vocabulary remains:

```text
Project → Workflow → Task → Step → Job
```

- **Project** declares a goal, scope, authority, and completion boundary.
- **Workflow** organizes Tasks and dependencies.
- **Task** is an accountable work unit with acceptance criteria.
- **Step** is an ordered or dependency-bound operation.
- **Job** is one bounded execution of a Step.

This vocabulary belongs to Face F05. It is architecture and routing language, not proof that a general scheduler, five independent persistent ledgers, or a multi-worker production system exists.

## 5. F04: OSPS outcome-space face

OSPS is the Outcome Space model inside Face F04. Its conceptual chain is:

```text
Source → ProblemContract → OutcomeNode → Obligation → CandidateArtifact → EvidenceLink → Result
```

An **OutcomeNode** represents a scoped possible outcome or intermediate state. An **Obligation** states what must be discharged before that node can close. A **CandidateArtifact** is untrusted research output. An **EvidenceLink** binds a candidate or claim to verifier-scoped evidence. A **Result** is an admitted, scoped mathematical claim.

OSPS maintains outcome alternatives, dependencies, blockers, and a search frontier. It does not create Jobs, issue evidence, or admit Results by itself. This document defines the conceptual model; it does not claim that an OSPS orchestrator or Outcome Graph runtime is implemented.

## 6. Cross-face binding

PWTSJ and OSPS are orthogonal but may be linked explicitly:

```text
F05 Task/Step --targets--> F04 OutcomeNode and F07 Obligation
F05 Job --produces--> F08 CandidateArtifact
F08 CandidateArtifact --supported-by--> F09 EvidenceLink
F09 EvidenceLink --evaluates--> F10 Result
```

Every binding must preserve ProblemContract identity and any required revision or content digest. A process object cannot become mathematical evidence merely because it completed successfully.

The minimum non-propagation rule is:

```text
Job succeeded
≠ Step accepted
≠ Obligation closed
≠ OutcomeNode closed
≠ Result admitted
≠ Project solved
```

Likewise, repository, Issue, pull request, CI, merge, checkpoint, publication, or model self-assessment is not by itself mathematical Evidence or a Result.

## 7. Four graphs and one ledger

Implementations should keep these views distinct:

1. **Semantic Graph** — definitions, assumptions, statements, and equivalence claims.
2. **Outcome Graph** — outcome nodes, obligations, alternatives, dependencies, and blockers.
3. **Process Graph** — Project, Workflow, Task, Step, Job, and their execution dependencies.
4. **Evidence Graph** — candidates, verifier receipts, reviews, EvidenceLinks, and Result support.
5. **Observation Ledger** — append-only externally observable events and status changes.

An Observation Ledger records observable process and artifact facts. It must not request, reconstruct, or publish hidden chain-of-thought.

## 8. Body contract

A Body manifest may compose multiple Faces only by reference. Each reference should identify:

- the owner Face and object type;
- the owner record locator;
- an immutable revision or content digest when required;
- the binding type and direction;
- the verification or freshness condition applicable to that reference.

A Body manifest must not duplicate ProblemContract, Attempt, CandidateArtifact, EvidenceLink, Result, or other owner-ledger records as a second truth source. A Body status is a projection over referenced states, not a replacement for them.

## 9. Status and evidence boundary

Process state, outcome state, evidence capability, Result outcome, and publication state are separate axes. In particular:

- finite enumeration can support only its declared finite scope;
- symbolic or numerical checks do not automatically become kernel checks;
- kernel checking validates a formal proof term but does not replace statement-faithfulness review;
- source labels such as `answered`, `resolved`, `solved`, or `open` do not become Result outcomes;
- public projections cannot write back into mathematical truth sources.

For the executable public research contract, see [VIBE-MATHING-SPEC-v0.1.md](VIBE-MATHING-SPEC-v0.1.md). For the F05 lifecycle vocabulary, see [RESEARCH-LIFECYCLE-MODEL-v0.1.md](RESEARCH-LIFECYCLE-MODEL-v0.1.md). For method positioning, see [FORMAL-METHODS-MAP.md](FORMAL-METHODS-MAP.md).

## 10. Public machine contract and implementation boundary

The public machine contract is [`../control-plane/plfb-metamodel.v0.1.json`](../control-plane/plfb-metamodel.v0.1.json), validated by [`../../scripts/validate_plfb_metamodel.py`](../../scripts/validate_plfb_metamodel.py). It enumerates 61 Point types, 58 Line types, F01–F13, and B0–B4. These entries are conceptual types only: the registry contains no Problem, Attempt, CandidateArtifact, EvidenceLink, Result, or other business instance.

This public release establishes a conceptual standard, schema, validator, and discovery contract only. It does not claim a universal solver, a deployed PLFB registry service, a Body runtime, a general PWTSJ scheduler, an OSPS orchestrator, a unified Observation Ledger, or a solved open problem.
