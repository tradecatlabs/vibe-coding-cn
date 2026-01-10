### Phenomenological Reduction (Suspension of Assumptions) for Vibe Coding

**Core Purpose**
Strip "what I think the requirement is" from the conversation, leaving only observable, reproducible, and verifiable facts and experience structures, allowing the model to produce usable code with fewer assumptions.

---

## 1) Key Methods (Understanding in Engineering Context)

* **Epoché (Suspension)**: Temporarily withhold any "causal explanations/business inferences/best practice preferences."
  Only record: what happened, what is expected, what are the constraints.

* **Reduction**: Reduce the problem to the minimal structure of "given input → process → output."
  Don't discuss architecture, patterns, or tech stack elegance first.

* **Intentionality**: Clarify "who this feature is for, in what context, to achieve what experience."
  Not "make a login," but "users can complete login within 2 seconds even on weak networks and get clear feedback."

---

## 2) Applicable Scenarios

* Requirements descriptions full of abstract words: fast, stable, like something, intelligent, smooth.
* Model starts "bringing its own assumptions": filling in product logic, randomly selecting frameworks, adding complexity on its own.
* Hard to reproduce bugs: intermittent, environment-related, unclear input boundaries.

---

## 3) Operating Procedure (Can Follow Directly)

### A. First "Clear Explanations," Keep Only Phenomena

Describe using four elements:

1. **Phenomenon**: Actual result (including errors/screenshots/log fragments).
2. **Intent**: Desired result (observable criteria).
3. **Context**: Environment and preconditions (version, platform, network, permissions, data scale).
4. **Boundaries**: What not to do/not to assume (don't change interface, don't introduce new dependencies, don't change database structure, etc.).

### B. Produce "Minimal Reproducible Example" (MRE)

* Minimal input sample (shortest JSON/smallest table/smallest request)
* Minimal code snippet (remove unrelated modules)
* Clear reproduction steps (1, 2, 3)
* Expected vs. Actual (comparison table)

### C. Reduce "Abstract Words" to Testable Metrics

* "Fast" → P95 latency < X, cold start < Y, throughput >= Z
* "Stable" → Error rate < 0.1%, retry strategy, circuit breaker conditions
* "User-friendly" → Interaction feedback, error messages, undo/recovery capability

---

## 4) Prompt Templates for Models (Can Copy Directly)

**Template 1: Reduce Problem (No Speculation)**

```
Please first do "phenomenological reduction": don't speculate on causes, don't introduce extra features.
Based only on the information I provide, output:
1) Phenomenon (observable facts)
2) Intent (observable result I want)
3) Context (environment/constraints)
4) Undetermined items (minimum information that must be clarified or I need to provide)
5) Minimal reproducible steps (MRE)
Then provide the minimal fix solution and corresponding tests.
```

**Template 2: Abstract Requirements to Testable Specs**

```
Apply "suspension of assumptions" to the following requirements: remove all abstract words, convert to verifiable specs:
- Clear input/output
- Clear success/failure criteria
- Clear performance/resource metrics (if needed)
- Clear what NOT to do
Finally provide acceptance test case list.
Requirements: <paste>
```

---

## 5) Concrete Implementation in Vibe Coding (Building Habits)

* **Write "phenomenon card" before each work session** (2 minutes): phenomenon/intent/context/boundaries.
* **Have the model restate first**: require it to only restate facts and gaps, no solutions allowed.
* **Then enter generation**: solutions must be tied to "observable acceptance" and "falsifiable tests."

---

## 6) Common Pitfalls and Countermeasures

* **Pitfall: Treating explanations as facts** ("Might be caused by cache")
  Countermeasure: Move "might" to "hypothesis list," each hypothesis with verification steps.

* **Pitfall: Requirements piled with adjectives**
  Countermeasure: Force conversion to metrics and test cases; no writing code if not "testable."

* **Pitfall: Model self-selecting tech stack**
  Countermeasure: Lock in boundaries: language/framework/dependencies/interfaces cannot change.

---

## 7) One-Sentence Mantra (Easy to Put in Toolbox Card)

**First suspend explanations, then fix phenomena; first write acceptance criteria, then let model write implementation.**
