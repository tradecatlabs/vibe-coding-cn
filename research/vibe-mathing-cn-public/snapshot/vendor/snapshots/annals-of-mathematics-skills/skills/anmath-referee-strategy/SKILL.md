---
name: anmath-referee-strategy
description: Use when anticipating how an expert Annals of Mathematics referee will verify a proof — stress-testing the argument for gaps, checking external dependencies, and pre-empting the questions a careful reader will ask. Hardens the manuscript before submission; does not write the rebuttal (anmath-revision).
---

# Referee Strategy (anmath-referee-strategy)

## When to trigger

- The manuscript is essentially final and you want to pre-empt referee objections
- You want an adversarial read of your own proof before an expert does it for you
- You are unsure which steps a careful referee will distrust
- You want to decide what to make easier to verify before sending

## How Annals referees read

Expect a referee who is an **expert and verifies proofs in detail**, often over a long
period (a year or more is common). They do not skim; they reconstruct each step. Their
implicit questions:

1. **Is it important enough?** Significance is judged again at the report stage.
2. **Is every step actually valid?** They will probe exactly the steps you find hardest.
3. **Do the external results say what you claim?** They will check the cited statement.
4. **Does the theorem match the proof?** Any over-claim is caught here.
5. **Is anything hidden behind "clearly"?** Softening words attract scrutiny, not less.

## Self-adversarial pass

| Probe | What to do before they do |
|-------|---------------------------|
| Where is the crux? | Make sure it is fully spelled out and easy to locate |
| Which step is weakest? | Strengthen or expand it; do not hope it is overlooked |
| Every "clearly"/"standard" | Resolve or cite it (see anmath-writing-style) |
| Every external theorem | Re-read the cited source; confirm hypotheses match your use |
| Quantifiers / constants | Confirm order and dependence are stated and correct |
| Special / boundary cases | Check the degenerate cases the main argument might miss |
| Computer-assisted steps | Confirm code/data are archived and the claim is reproducible |

## Make verification easy

- A clear **proof overview** and named lemmas let a referee navigate and check piece by
  piece — this speeds a long review and reduces the chance of misreading.
- **Precise citations** (exact theorem number and statement) save the referee from hunting
  and remove a common source of objections.
- **Isolate any dependence on unpublished work** so the referee can see exactly what rests
  on it; reduce or remove such dependence where possible.

## Suggested / opposed referees

- If the portal allows suggestions, propose genuine experts without conflicts of interest;
  do not pack the list with close collaborators.
- Declare conflicts honestly. Editors decide; transparency builds trust.

## Checklist

- [ ] The crux is fully spelled out and easy to find
- [ ] The weakest step has been strengthened or expanded, not hidden
- [ ] Every "clearly"/"standard" is resolved or precisely cited
- [ ] Every external theorem's hypotheses match your use (re-checked at source)
- [ ] Quantifier order and constant dependence verified
- [ ] Degenerate/boundary cases handled
- [ ] Computer-assisted steps reproducible (archived code/data)
- [ ] Suggested referees are genuine, conflict-free experts; conflicts declared

## Anti-patterns

- Hoping a referee will not check the step you yourself are unsure about
- Citing an external theorem without re-reading its exact hypotheses
- Leaving the crux hard to locate in a long, unstructured proof
- Suggesting only close collaborators as referees
- Treating significance as settled at submission — it is re-judged in the report
- Relying on "it is easy to see" to get past a careful reader (it will not)

## Output format

```
【Crux locatable & complete】yes / fix: ...
【Weakest step】... → strengthened / expanded
【External-citation re-check】hypotheses match use: yes / fix: ...
【Boundary cases】covered / add: ...
【Computer-assisted reproducible】n/a / yes
【Suggested referees】names (conflict-free); conflicts declared: ...
【Residual risks to flag to editor】...
【Next step】submit, then await report → anmath-revision
```
