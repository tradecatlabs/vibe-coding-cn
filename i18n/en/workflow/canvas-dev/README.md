# 🎨 Canvas Whiteboard-Driven Development Workflow

> Graphics are first-class citizens; code is the serialized form of the whiteboard

## Core Philosophy

```
Traditional Development: Code → Verbal Communication → Mental Architecture → Code Chaos
Canvas Approach: Code ⇄ Whiteboard ⇄ AI ⇄ Human (Whiteboard as Single Source of Truth)
```

| Pain Point | Solution |
|:-----------|:---------|
| 🤖 AI can't understand project structure | ✅ AI reads whiteboard JSON directly, instantly grasps architecture |
| 🧠 Humans can't remember complex dependencies | ✅ Clear connections, ripple effects visible at a glance |
| 💬 Team collaboration relies on verbal explanation | ✅ Point at the whiteboard, newcomers understand in 5 minutes |

## File Structure

```
canvas-dev/
├── README.md                 # This file - Workflow overview
├── workflow.md               # Complete workflow steps (linear process)
├── prompts/
│   ├── 01-architecture-analysis.md    # Prompt for generating whiteboard from code
│   ├── 02-whiteboard-driven-coding.md # Prompt for generating code from whiteboard
│   └── 03-whiteboard-sync-check.md    # Validate whiteboard-code consistency
├── templates/
│   ├── project.canvas        # Obsidian Canvas project template
│   └── module.canvas         # Single module whiteboard template
└── examples/
    └── demo-project.canvas   # Example project whiteboard
```

## Quick Start

### 1. Prepare Tools

- [Obsidian](https://obsidian.md/) - Free open-source whiteboard tool
- AI assistant (Claude/GPT-4, must support reading Canvas JSON)

### 2. Generate Project Architecture Whiteboard

```bash
# Provide project code path to AI, use architecture analysis prompt
# AI automatically generates .canvas file
```

### 3. Drive Development with Whiteboard

- Draw new modules and dependency relationships on the whiteboard
- Export whiteboard JSON and send to AI
- AI generates/modifies code based on the whiteboard

## Related Documentation

- [Canvas Whiteboard-Driven Development Guide](../../documents/02-methodology/Graphical AI Collaboration - Canvas Whiteboard-Driven Development.md)
- [Whiteboard-Driven Development System Prompt](../../prompts/01-system-prompts/AGENTS.md/12/AGENTS.md)
- [Glue Coding](../../documents/00-fundamentals/Glue Coding.md)
