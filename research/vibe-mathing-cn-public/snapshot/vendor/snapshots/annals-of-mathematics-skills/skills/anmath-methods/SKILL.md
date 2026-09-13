---
name: anmath-methods
description: Use when laying out the proof strategy of a pure-mathematics manuscript for Annals of Mathematics — the architecture of the argument, the key lemmas and propositions, the novel technique, and where the difficulty lies. Designs and exposes the proof plan; does not check final correctness line-by-line (see anmath-referee-strategy).
---

# Proof Strategy and Architecture (anmath-methods)

## When to trigger

- The proof is essentially complete but its logical structure is not laid out for a reader
- A referee would not be able to see the plan before drowning in the details
- The key new idea is buried; it is not clear where the real difficulty is overcome
- The argument is monolithic and should be decomposed into named lemmas/propositions

## Architecture-first principle

For an Annals paper, an expert non-specialist should be able to read a **proof overview**
and understand *how* the theorem is proved before verifying *that* it is. The architecture
is part of the contribution.

1. **Proof outline up front.** After stating the Main Theorem, give a paragraph or short
   section sketching the strategy: the main steps, the key lemma(s), and the crux.
2. **Decompose into named results.** Break the argument into Lemmas, Propositions, and
   intermediate Theorems, each stated precisely and proved before it is used.
3. **Isolate the new idea.** Name explicitly which step is the genuinely new technique and
   why prior approaches failed there. This is what makes the paper publishable.
4. **Locate the difficulty.** Tell the reader where the hard part is and why it is hard;
   do not let the crux pass disguised as routine.

## Decomposition guidance

| Symptom | Action |
|---------|--------|
| A 10-page proof with no internal structure | Extract Lemmas/Propositions with clear statements |
| The same estimate reused three times | State it once as a Lemma and cite it |
| A self-contained technical computation interrupting the flow | Push to an appendix (anmath-supplementary) |
| Reliance on a deep external theorem | State it precisely with citation; do not paraphrase loosely |
| The crux step stated as "a calculation shows" | Expand fully — this is exactly what referees check |

## Handling the key technique

- State the **novel ingredient** as its own result when possible (a key Lemma or
  Proposition), so others can cite and reuse it — methods with reach justify Annals.
- Contrast with the **standard approach**: one or two sentences on why the obvious method
  does not work and how the new idea circumvents the obstruction.
- If the method is borrowed and adapted, **attribute it** and state precisely what is new
  in your adaptation.

## Dependence on external results

- Every external theorem you invoke must be **published and precisely cited**; quote the
  exact statement you use, not a vague version.
- Do **not** build an essential step on an unpublished or unverifiable claim; if
  unavoidable, isolate the dependence and flag it explicitly.

## Checklist

- [ ] A proof overview appears before the detailed argument
- [ ] The argument is decomposed into precisely stated lemmas/propositions
- [ ] Each auxiliary result is proved before it is used
- [ ] The genuinely new idea is named and explained as the crux
- [ ] Why the standard approach fails is stated explicitly
- [ ] Every external result invoked is published and precisely cited
- [ ] No essential step rests on an unpublished/unverifiable claim
- [ ] The crux is proved in full, not waved through as "a calculation"

## Anti-patterns

- A monolithic proof with no roadmap — the referee cannot navigate it
- Hiding the crux inside a step labeled "routine" or "standard"
- Restating a known method as if it were new without attribution
- Paraphrasing an external theorem loosely so the actual hypothesis is unclear
- Reusing the same estimate inline three times instead of stating it once
- Leaving the reader unable to say where the difficulty was overcome

## Output format

```
【Proof strategy, one paragraph】...
【Key lemmas/propositions】L1: ...; P1: ...; ...
【The new idea (crux)】...
【Why the standard approach fails】...
【External results relied on】author (year), Thm X — exact statement used
【Steps to push to appendix】... → anmath-supplementary
【Next step】anmath-figures (exposition & structure)
```
