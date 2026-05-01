---
name: claude-code-guide
description: "Claude Code guide skill: CLI workflows, project context, tool permissions, slash commands, hooks, MCP, large-file analysis, debugging, and advanced coding-agent operating patterns."
---

# claude-code-guide Skill

Use this skill to answer Claude Code workflow questions and to turn the long Chinese guide in `references/README.md` into focused operating steps.

## When to Use This Skill

Trigger when any of these applies:
- Learning or explaining Claude Code CLI workflows, command habits, or project-context handling.
- Designing slash commands, hooks, MCP integrations, memory/context conventions, or task workflows.
- Debugging Claude Code permission, tool-use, file analysis, or large-context problems.
- Comparing interactive coding-agent patterns such as explore-plan-edit-verify, review loops, or multi-agent coordination.
- Extracting a compact answer from the full Claude Code guide in `references/README.md`.

## Not For / Boundaries

- Not the source of truth for current Claude product availability, pricing, or model names; verify those with official Anthropic docs when exact current behavior matters.
- Not for bypassing tool permissions, sandbox rules, repository policies, or higher-priority system/developer instructions.
- Do not treat the long guide as automatically correct for every Claude Code version; use it as local project reference material.
- Required inputs: target workflow, OS/shell, Claude Code version if relevant, current repository constraints, and the exact error or behavior observed.
- If a command may mutate files or external systems, identify the blast radius and validation path before recommending it.

## Quick Reference

### Common Patterns

**Start with project context**
```text
Read README/AGENTS/CONTRIBUTING, inspect git status, then search for local patterns before editing.
```

**Large-file triage**
```bash
wc -l path/to/file.md
rg -n '^#{1,6} ' path/to/file.md
sed -n '1,120p' path/to/file.md
```

**Slash command authoring shape**
```text
.claude/commands/<command-name>.md
```

**Hook design checklist**
```text
event -> allowed command -> timeout -> logging -> rollback/disable path
```

**MCP integration checklist**
```text
server name -> command/env -> auth source -> minimal permission -> smoke test
```

**Debug a Claude Code failure**
```text
Capture: command, working directory, permission mode, exact error, relevant config, and smallest reproduction.
```

**Context hygiene rule**
```text
Keep entry prompts short; move long references to files and load only the needed section.
```

## Examples

### Example 1: Add a Custom Slash Command

- Input: user wants a repeatable `/review-pr` workflow.
- Steps:
  1. Create or update `.claude/commands/review-pr.md` with scope, required inputs, and output format.
  2. Reference repository review rules instead of duplicating stale policy text.
  3. Test the command on a small diff and refine ambiguous steps.
- Expected output / acceptance: command is discoverable, deterministic, and does not bypass repo review constraints.

### Example 2: Diagnose a Permission Problem

- Input: Claude Code refuses to run or edit a file.
- Steps:
  1. Identify whether the blocker is tool permission, filesystem sandbox, repository policy, or OS permissions.
  2. Capture the exact path, command, and error.
  3. Propose the least-permissive fix and a smoke test.
- Expected output / acceptance: user gets a concrete unblock path without granting broad unnecessary access.

### Example 3: Summarize a Long Guide Section

- Input: need the MCP section from `references/README.md`.
- Steps:
  1. Use heading search to locate the section.
  2. Read only the relevant slice.
  3. Return a short operator checklist plus links back to the local reference file.
- Expected output / acceptance: answer is actionable and avoids dumping the full long document.

## References

- `references/index.md`: structured navigation for the guide.
- `references/README.md`: long-form Claude Code Chinese guide.

## Maintenance

- Sources: local `references/README.md` and `references/index.md`.
- Last updated: 2026-04-28
- Known limits: Claude Code behavior can change; verify current CLI flags, hooks, and MCP details against official docs when precision matters.
