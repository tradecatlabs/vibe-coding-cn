# 12Factor.me - Four Phases × Twelve Principles Methodology

Source: https://www.12factor.me/

> Methodology for 10x engineering efficiency improvement in the AI collaboration era

---

## Phase 1: Preparation

*Establish clear information architecture and context environment*

### 1. Single Source of Truth

**Core Concept**: Scattered information leads to context confusion, easily causing misjudgment by both humans and machines.

**Recommended Practices**:
- Centralize all requirements, designs, and context in a unified document center (e.g., Notion / Confluence / GitHub Wiki).
- When collaborating with AI, directly reference this "source of truth" rather than randomly copying and pasting information.

**Anti-patterns**:
- Team members each maintain different versions of documents, leading to inconsistent AI responses and suggestions.

### 2. Prompt First

**Core Concept**: Treat prompts as the new generation of design documents.

**Recommended Practices**:
- Before starting a task, prioritize writing prompts to clarify inputs, outputs, styles, and constraints.
- Reuse validated and optimized prompt templates within the team.

**Anti-patterns**:
- Directly asking AI to write code without planning, leading to wrong direction and unnecessary rework.

### 3. Context Hygiene

**Core Concept**: Clean context enables more precise AI responses.

**Recommended Practices**:
- Start a new session for each new task to avoid old content interference
- Regularly summarize the current situation in one sentence to help AI "align context"

**Anti-patterns**:
- Mixing conversations from three days ago with today's tasks

---

## Phase 2: Execution

*Efficiently collaborate to complete specific tasks*

### 4. Human-in-the-Loop

**Core Concept**: AI produces fast, but only humans can grasp direction and business judgment.

**Recommended Practices**:
- AI provides initial drafts, humans responsible for key decisions and risk control
- For important features, perform logic verification before merging code

**Anti-patterns**:
- Accepting AI output wholesale without any review

### 5. Chunked Work

**Core Concept**: Break large tasks into small chunks, easier to iterate and correct.

**Recommended Practices**:
- Keep tasks completable within 10-30 minutes
- Verify results immediately after each chunk

**Anti-patterns**:
- Having AI write 5000 lines at once, impossible to debug

### 6. Parallel Flow

**Core Concept**: While AI works, humans do low-context-switch side tasks to maintain rhythm.

**Recommended Practices**:
- Prepare a "side task list" including document organization, small fixes, code reviews, etc.
- While waiting for AI, don't take on high cognitive load new tasks to avoid excessive switching costs

**Anti-patterns**:
- Scrolling social media while waiting for AI, breaking the rhythm

---

## Phase 3: Collaboration

*Manage cognitive load and workflow during collaboration*

### 7. Cognitive Load Budget

**Core Concept**: Human attention is a scarce resource.

**Recommended Practices**:
- Set daily time limits for AI collaboration
- Schedule deep review tasks during peak mental periods

**Anti-patterns**:
- Working with AI all day, completely exhausted by evening

### 8. Flow Protection

**Core Concept**: Once high-focus flow is interrupted, recovery cost is extremely high.

**Recommended Practices**:
- Set focus periods (e.g., 90 minutes), block notifications and interruptions
- AI interactions also done in batches during focus flow, not scattered triggers

**Anti-patterns**:
- Writing code while replying to messages while watching AI output, cliff-like efficiency drop

### 9. Reproducible Sessions

**Core Concept**: Collaboration process must be traceable for continuous optimization.

**Recommended Practices**:
- Save prompts, AI versions, change reasons to codebase or knowledge base
- When bugs occur, can replay the generation process

**Anti-patterns**:
- No record of AI generation history, can't trace causes when errors occur

---

## Phase 4: Iteration

*Continuous learning and improving collaboration patterns*

### 10. Rest & Reflection

**Core Concept**: Retrospect after sprints to run faster.

**Recommended Practices**:
- After sprint ends, spend 5 minutes reflecting on AI output vs expectations
- Update prompt templates, accumulate "pitfall records"

**Anti-patterns**:
- Continuous sprints, accumulating errors without summary

### 11. Skill Parity

**Core Concept**: AI is a magnifier, amplifying abilities and also weaknesses.

**Recommended Practices**:
- Continuously learn domain knowledge and code review skills
- Maintain independent judgment on AI output

**Anti-patterns**:
- Completely relying on AI, losing manual skills and technical insight

### 12. Culture of Curiosity

**Core Concept**: Curiosity drives exploration, avoiding "blind trust in AI".

**Recommended Practices**:
- When facing AI answers, first ask "why", then ask "can it be better"
- Team shares AI usage experiences and improvement ideas

**Anti-patterns**:
- Accepting AI solutions without question

---

*Generated from [12Factor.me](https://12factor.me)*
*License: MIT*
