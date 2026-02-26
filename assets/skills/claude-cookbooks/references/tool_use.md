# Tool Use with Claude

Source: anthropics/claude-cookbooks/tool_use

## Overview

Learn how to integrate Claude with external tools and functions to extend its capabilities.

## Key Examples

### Customer Service Agent
- **Location**: `tool_use/customer_service_agent.ipynb`
- **Description**: Build an intelligent customer service agent using Claude with tool integration
- **Key Concepts**: Function calling, state management, conversation flow

### Calculator Integration
- **Location**: `tool_use/calculator_tool.ipynb`
- **Description**: Integrate external calculation tools with Claude
- **Key Concepts**: Tool definitions, parameter passing, result handling

### Memory Demo
- **Location**: `tool_use/memory_demo/`
- **Description**: Implement persistent memory for Claude conversations
- **Key Concepts**: Context management, state persistence

## Best Practices

1. **Tool Definition**: Define clear, specific tool schemas
2. **Error Handling**: Implement robust error handling for tool calls
3. **Validation**: Validate tool inputs and outputs
4. **Context**: Maintain context across tool interactions

## Common Patterns

```python
# Tool definition example
tools = [{
    "name": "calculator",
    "description": "Performs basic arithmetic operations",
    "input_schema": {
        "type": "object",
        "properties": {
            "operation": {"type": "string"},
            "a": {"type": "number"},
            "b": {"type": "number"}
        },
        "required": ["operation", "a", "b"]
    }
}]
```

## Related Resources

- [Anthropic Tool Use Documentation](https://docs.claude.com/claude/docs/tool-use)
- [API Reference](https://docs.claude.com/claude/reference)
