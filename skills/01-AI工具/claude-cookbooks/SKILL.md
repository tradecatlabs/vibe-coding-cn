---
name: claude-cookbooks
description: Claude AI cookbooks - code examples, tutorials, and best practices for using Claude API. Use when learning Claude API integration, building Claude-powered applications, or exploring Claude capabilities.
---

# Claude Cookbooks Skill

Comprehensive code examples and guides for building with Claude AI, sourced from the official Anthropic cookbooks repository.

## When to Use This Skill

This skill should be triggered when:
- Learning how to use Claude API
- Implementing Claude integrations
- Building applications with Claude
- Working with tool use and function calling
- Implementing multimodal features (vision, image analysis)
- Setting up RAG (Retrieval Augmented Generation)
- Integrating Claude with third-party services
- Building AI agents with Claude
- Optimizing prompts for Claude
- Implementing advanced patterns (caching, sub-agents, etc.)

## Quick Reference

### Basic API Usage

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

# Simple message
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "Hello, Claude!"
    }]
)
```

### Tool Use (Function Calling)

```python
# Define a tool
tools = [{
    "name": "get_weather",
    "description": "Get current weather for a location",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City name"}
        },
        "required": ["location"]
    }
}]

# Use the tool
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in San Francisco?"}]
)
```

### Vision (Image Analysis)

```python
# Analyze an image
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": base64_image
                }
            },
            {"type": "text", "text": "Describe this image"}
        ]
    }]
)
```

### Prompt Caching

```python
# Use prompt caching for efficiency
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system=[{
        "type": "text",
        "text": "Large system prompt here...",
        "cache_control": {"type": "ephemeral"}
    }],
    messages=[{"role": "user", "content": "Your question"}]
)
```

## Key Capabilities Covered

### 1. Classification
- Text classification techniques
- Sentiment analysis
- Content categorization
- Multi-label classification

### 2. Retrieval Augmented Generation (RAG)
- Vector database integration
- Semantic search
- Context retrieval
- Knowledge base queries

### 3. Summarization
- Document summarization
- Meeting notes
- Article condensing
- Multi-document synthesis

### 4. Text-to-SQL
- Natural language to SQL queries
- Database schema understanding
- Query optimization
- Result interpretation

### 5. Tool Use & Function Calling
- Tool definition and schema
- Parameter validation
- Multi-tool workflows
- Error handling

### 6. Multimodal
- Image analysis and OCR
- Chart/graph interpretation
- Visual question answering
- Image generation integration

### 7. Advanced Patterns
- Agent architectures
- Sub-agent delegation
- Prompt optimization
- Cost optimization with caching

## Repository Structure

The cookbooks are organized into these main categories:

- **capabilities/** - Core AI capabilities (classification, RAG, summarization, text-to-SQL)
- **tool_use/** - Function calling and tool integration examples
- **multimodal/** - Vision and image-related examples
- **patterns/** - Advanced patterns like agents and workflows
- **third_party/** - Integrations with external services (Pinecone, LlamaIndex, etc.)
- **claude_agent_sdk/** - Agent SDK examples and templates
- **misc/** - Additional utilities (PDF upload, JSON mode, evaluations, etc.)

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **main_readme.md** - Main repository overview
- **capabilities.md** - Core capabilities documentation
- **tool_use.md** - Tool use and function calling guides
- **multimodal.md** - Vision and multimodal capabilities
- **third_party.md** - Third-party integrations
- **patterns.md** - Advanced patterns and agents
- **index.md** - Complete reference index

## Common Use Cases

### Building a Customer Service Agent
1. Define tools for CRM access, ticket creation, knowledge base search
2. Use tool use API to handle function calls
3. Implement conversation memory
4. Add fallback mechanisms

See: `references/tool_use.md#customer-service`

### Implementing RAG
1. Create embeddings of your documents
2. Store in vector database (Pinecone, etc.)
3. Retrieve relevant context on query
4. Augment Claude's response with context

See: `references/capabilities.md#rag`

### Processing Documents with Vision
1. Convert document to images or PDF
2. Use vision API to extract content
3. Structure the extracted data
4. Validate and post-process

See: `references/multimodal.md#vision`

### Building Multi-Agent Systems
1. Define specialized agents for different tasks
2. Implement routing logic
3. Use sub-agents for delegation
4. Aggregate results

See: `references/patterns.md#agents`

## Best Practices

### API Usage
- Use appropriate model for task (Sonnet for balance, Haiku for speed, Opus for complex tasks)
- Implement retry logic with exponential backoff
- Handle rate limits gracefully
- Monitor token usage for cost optimization

### Prompt Engineering
- Be specific and clear in instructions
- Provide examples when needed
- Use system prompts for consistent behavior
- Structure outputs with JSON mode when needed

### Tool Use
- Define clear, specific tool schemas
- Validate inputs and outputs
- Handle errors gracefully
- Keep tool descriptions concise but informative

### Multimodal
- Use high-quality images (higher resolution = better results)
- Be specific about what to extract/analyze
- Respect size limits (5MB per image)
- Use appropriate image formats (JPEG, PNG, GIF, WebP)

## Performance Optimization

### Prompt Caching
- Cache large system prompts
- Cache frequently used context
- Monitor cache hit rates
- Balance caching vs. fresh content

### Cost Optimization
- Use Haiku for simple tasks
- Implement prompt caching for repeated context
- Set appropriate max_tokens
- Batch similar requests

### Latency Optimization
- Use streaming for long responses
- Minimize message history
- Optimize image sizes
- Use appropriate timeout values

## Resources

### Official Documentation
- [Anthropic Developer Docs](https://docs.claude.com)
- [API Reference](https://docs.claude.com/claude/reference)
- [Anthropic Support](https://support.anthropic.com)

### Community
- [Anthropic Discord](https://www.anthropic.com/discord)
- [GitHub Cookbooks Repo](https://github.com/anthropics/claude-cookbooks)

### Learning Resources
- [Claude API Fundamentals Course](https://github.com/anthropics/courses/tree/master/anthropic_api_fundamentals)
- [Prompt Engineering Guide](https://docs.claude.com/claude/docs/guide-to-anthropics-prompt-engineering-resources)

## Working with This Skill

### For Beginners
Start with `references/main_readme.md` and explore basic examples in `references/capabilities.md`

### For Specific Features
- Tool use → `references/tool_use.md`
- Vision → `references/multimodal.md`
- RAG → `references/capabilities.md#rag`
- Agents → `references/patterns.md#agents`

### For Code Examples
Each reference file contains practical, copy-pasteable code examples

## Examples Available

The cookbook includes 50+ practical examples including:
- Customer service chatbot with tool use
- RAG with Pinecone vector database
- Document summarization
- Image analysis and OCR
- Chart/graph interpretation
- Natural language to SQL
- Content moderation filter
- Automated evaluations
- Multi-agent systems
- Prompt caching optimization

## Notes

- All examples use official Anthropic Python SDK
- Code is production-ready with error handling
- Examples follow current API best practices
- Regular updates from Anthropic team
- Community contributions welcome

## Skill Source

This skill was created from the official Anthropic Claude Cookbooks repository:
https://github.com/anthropics/claude-cookbooks

Repository cloned and processed on: 2025-10-29
