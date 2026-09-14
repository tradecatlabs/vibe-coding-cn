# FAQ

## Does vibe-mathing-cn solve the Riemann Hypothesis, P versus NP, or another open problem?

No. The canonical Problem, Attempt, and Result ledgers are empty, the public solution index has no result IDs, and the repository makes no claim to solve an open mathematics problem.

## What is the project?

It is a trusted AI mathematics research and verification workbench. It organizes work as ProblemContract -> Attempt -> candidate/evidence -> Result -> derived Solution View.

## What is a ProblemContract?

A versioned input contract that freezes the exact statement, domain, quantifiers, definitions, assumptions, sources, acceptance policy, and bounded runtime constraints.

## What is the difference between CandidateObservation, Attempt, and Result?

A CandidateObservation is a source-discovery record and remains outside research admission. An Attempt records a research activity. A Result is a scoped claim with an outcome and evidence record; a generated draft is not automatically a Result.

## Why is an AI-generated proof not automatically a Result?

The agent is a candidate generator. The proposed proof must be checked against the exact statement, scope, evidence, independence requirements, and statement-faithfulness boundary before it can qualify.

## What does a finite computation or passing test show?

It shows only that a bounded input or engineering condition passed a check. It does not establish a universal mathematical statement without a separate argument covering the full claim.

## What does the Lean fixture show?

It shows that a fixed Lean/Mathlib fixture can be built and audited for proof-term and axiom properties. It does not automatically validate an arbitrary natural-language theorem.

## What is the project's method-layer mainline, and where does Lean fit?

The map is Specification & Semantics -> Deductive Verification/Theorem Proving -> Model Checking -> Abstract Interpretation -> SAT/SMT/Symbolic Reasoning (including Symbolic Execution)/Decision Procedures -> Refinement/Synthesis. Lean is in the dependent-type-theory deductive-verification branch, not the whole formal-methods field. See [`FORMAL-METHODS-MAP.md`](../../governance/standards/FORMAL-METHODS-MAP.md).

## What is the project's single conceptual metamodel root?

Point-Line-Face-Body (PLFB) is the single conceptual root. Stable objects map to Points, typed directed relationships to Lines, bounded knowledge or operation dimensions to Faces, and cross-face compositions to reference-only Bodies. PWTSJ is Face F05 and OSPS is Face F04; they are not parallel roots. This is a conceptual standard, not a claim that a PLFB registry service, Body runtime, OSPS orchestrator, general scheduler, or unified Observation Ledger is implemented.

## What is the top-level research lifecycle?

Inside F05, the architecture language is Project -> Workflow -> Task -> Step -> Job. Project defines the goal, Workflow the task network, Task the work unit, Step the operation, and Job one bounded execution. F04/OSPS maintains OutcomeNodes, Obligations, alternatives, and the search frontier. `Job succeeded != Step accepted != Obligation closed != OutcomeNode closed != Result admitted != Project solved`.

## How should current status and external catalog information be checked?

Use the three canonical ledgers and `solutions.json` for this repository's status. Treat external catalog counts and repository states as dated snapshots; re-read the remote contract, index, repository identity, lifecycle, and digest before starting research. A verification date does not guarantee that a remote snapshot is still current.

## Why is `solutions.json` empty?

The index is derived only from qualifying proof or counterexample Results. It is empty because no business Result currently satisfies every admission gate; it is not a manually filled answer table.

## Where are the concrete open problems and the Web research suite?

Use [`problem-library/VIBEMATHING_PUBLIC_INDEX.md`](../../problem-library/VIBEMATHING_PUBLIC_INDEX.md). It points to the public vibemathing ProblemContract catalog, concrete `problem-*` repositories, and the fixed `vibe-mathing-problem-public-template`. Re-read the remote contract and `WEB_BOOTSTRAP.md` before research; remote entries remain outside local admission.

## How can I run the public example?

Install `requirements.txt`, run `make check`, then use the deterministic SymPy commands in `README.md`. The fixture demonstrates the engineering path and does not create a claim about an open problem.
