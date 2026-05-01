---
name: claude-cookbooks
description: "Claude cookbooks skill: Claude API examples for messages, tool use, vision, RAG, summarization, text-to-SQL, prompt caching, agents, multimodal workflows, and third-party integrations."
---

# claude-cookbooks Skill

Use this skill to turn cookbook material into runnable Claude API integration patterns while keeping model/version assumptions explicit.

## When to Use This Skill

Trigger when any of these applies:
- Building applications that call the Claude API.
- Implementing tool use/function calling, structured outputs, RAG, summarization, classification, or text-to-SQL.
- Working with multimodal inputs such as images and document extraction.
- Exploring prompt caching, agents, sub-agent patterns, or third-party integrations.
- Looking up cookbook examples stored in `references/` and adapting them to a project.

## Not For / Boundaries

- Not the source of truth for latest Anthropic models, pricing, limits, or API changes; verify current API details with official docs when exact current behavior matters.
- Do not hard-code API keys or leak prompts containing private user data.
- Cookbook examples are starting points, not production architecture; add retries, timeouts, observability, evals, and security checks.
- Required inputs: language/runtime, use case, model policy from the project, data sensitivity, expected output schema, and failure handling requirements.
- If local references conflict with current official docs, prefer the official docs and update the reference notes.

## Quick Reference

### Common Patterns

**Basic Messages API shape**
```python
import anthropic

client = anthropic.Anthropic(api_key="YOUR_API_KEY")
response = client.messages.create(
    model="YOUR_APPROVED_MODEL",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
)
```

**Tool definition shape**
```python
tools = [{
    "name": "get_weather",
    "description": "Get current weather for a location.",
    "input_schema": {
        "type": "object",
        "properties": {"location": {"type": "string"}},
        "required": ["location"],
    },
}]
```

**Vision content shape**
```python
content = [
    {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": base64_image}},
    {"type": "text", "text": "Describe the image."},
]
```

**Prompt caching shape**
```python
system = [{
    "type": "text",
    "text": "Large stable system prompt...",
    "cache_control": {"type": "ephemeral"},
}]
```

**RAG pipeline skeleton**
```text
ingest -> chunk -> embed/index -> retrieve -> rerank/filter -> answer with citations -> evaluate
```

**Production hardening checklist**
```text
timeouts, retries, redaction, structured logging, eval set, cost guard, rate-limit handling
```

## Examples

### Example 1: Add Tool Use to an App

- Input: user asks for weather lookup through Claude.
- Steps:
  1. Define a JSON schema for `get_weather`.
  2. Send the user request with the tool definition.
  3. Execute only validated tool calls and return tool results to the model.
- Expected output / acceptance: tool arguments pass schema validation and no unapproved function is called.

### Example 2: Build a RAG Answerer

- Input: local product docs and user questions.
- Steps:
  1. Chunk and index documents with stable IDs.
  2. Retrieve relevant chunks for each question.
  3. Ask Claude to answer only from retrieved evidence and cite chunk IDs.
- Expected output / acceptance: unsupported claims are refused or marked unknown, and answers include source references.

### Example 3: Vision Extraction

- Input: screenshot or document image.
- Steps:
  1. Convert image to supported media type and base64.
  2. Send image plus extraction instructions.
  3. Validate returned fields against the expected schema.
- Expected output / acceptance: extracted data is structured, missing fields are explicit, and raw sensitive images are not logged.

## References

- `references/index.md`: navigation for cookbook topics.
- `references/main_readme.md` and `references/README.md`: upstream overview material.
- `references/tool_use.md`: tool-use examples.
- `references/capabilities.md`: classification, RAG, summarization, and text-to-SQL.
- `references/multimodal.md`: image and multimodal examples.
- `references/patterns.md`: agents, caching, and advanced patterns.
- `references/third_party.md`: vector DB and external integrations.
- `scripts/memory_tool.py`: local helper script retained from the cookbook material.

## Maintenance

- Sources: local `references/` extracted from Anthropic cookbook material.
- Last updated: 2026-04-28
- Known limits: examples may carry older model names; replace with the project-approved current model before use.
