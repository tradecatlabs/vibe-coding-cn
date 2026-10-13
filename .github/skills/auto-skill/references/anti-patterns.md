# Anti-Patterns (And How to Fix Them)

This file documents common ways Skills fail in practice. Use it when refactoring existing Skills.

## 1) Documentation Dump in Quick Reference

**Symptom**
- Quick Reference contains paragraphs of text, pasted docs, or large excerpts.

**Why it fails**
- Users cannot scan or reuse it.
- The model treats it as "knowledge soup" rather than executable patterns.

**Fix**
- Move long text into `references/` (split by topic).
- Keep Quick Reference as <= 20 copy/paste patterns when possible.
- Add Examples for anything non-trivial.

## 2) Vague Triggers ("Helps with X")

**Symptom**
- `description` says "helps with databases" or similar.
- "When to Use" is a generic list with no tasks/inputs/goals.

**Why it fails**
- Activation becomes noisy and unpredictable.

**Fix**
- Rewrite `description` as: "What + when".
- In "When to Use", list decidable tasks:
  - "Writing migration SQL for PostgreSQL"
  - "Debugging a failing CCXT order placement"
- Add "Not For / Boundaries" to prevent misfires.

## 3) Missing Boundaries

**Symptom**
- The Skill never says what it will not do.

**Why it fails**
- The model over-promises and makes unsafe assumptions.
- The skill triggers in irrelevant contexts.

**Fix**
- Add `## Not For / Boundaries` with:
  - explicit out-of-scope items
  - required inputs and what questions to ask when missing

## 4) Non-reproducible Examples

**Symptom**
- Examples are pseudo-code, missing inputs, or missing expected outputs.

**Why it fails**
- Users cannot trust or validate the behavior.

**Fix**
- Each example should contain:
  - Input(s)
  - Steps
  - Expected output / acceptance criteria
- Prefer minimal reproducible examples over big "showcase" code.

## 5) One Giant File Syndrome

**Symptom**
- Everything is in `SKILL.md` (or one huge reference file).

**Why it fails**
- The entrypoint becomes unscannable and hard to maintain.

**Fix**
- Keep `SKILL.md` execution-focused (patterns + examples + boundaries).
- Split long content into `references/` and add `references/index.md`.

## 6) Invented Facts and Unverifiable Claims

**Symptom**
- The Skill claims API fields/flags/commands without citing sources.

**Why it fails**
- Incorrect guidance is worse than missing guidance.

**Fix**
- Add a "verification path": where/how to confirm in official docs or source code.
- Prefer statements backed by your material; mark assumptions explicitly.

## 7) Unsafe Defaults and Destructive Commands

**Symptom**
- The Skill suggests destructive commands as the default path.

**Why it fails**
- Users copy/paste and lose data.

**Fix**
- Put destructive actions behind explicit warnings and confirmation steps.
- Prefer read-only diagnostics first.

## 8) Inconsistent Terminology

**Symptom**
- Same concept has multiple names; different concepts share a name.

**Why it fails**
- Increases cognitive load and produces inconsistent outputs.

**Fix**
- Add a short glossary (in `references/getting_started.md` or similar).
- Use one concept, one name.
