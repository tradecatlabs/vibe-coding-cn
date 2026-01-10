# 01-Architecture Analysis Prompt

> Automatically generate Obsidian Canvas architecture whiteboard from existing code

## Use Cases

- Taking over a new project, quickly understand architecture
- Create visual documentation for existing projects
- Prepare for Code Review or technical presentations

## Prompt

```markdown
You are a code architecture analysis expert. Please analyze the following project structure and generate an architecture whiteboard in Obsidian Canvas format.

## Input
Project path: {PROJECT_PATH}
Analysis granularity: {GRANULARITY} (file/class/service)

## Output Requirements
Generate a .canvas file conforming to Obsidian Canvas JSON format, including:

1. **Nodes**:
   - Each module/file/class as a node
   - Node contains: id, type, x, y, width, height, text
   - Layout by functional zones (e.g., API layer on left, data layer on right)

2. **Edges**:
   - Represent dependency/call relationships between modules
   - Contains: id, fromNode, toNode, fromSide, toSide, label
   - Label indicates relationship type (call/inheritance/dependency/data flow)

3. **Groups**:
   - Group by functional domain (e.g., user module, payment module)
   - Use colors to distinguish different layers

## Canvas JSON Structure Example
```json
{
  "nodes": [
    {
      "id": "node1",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 200,
      "height": 100,
      "text": "# UserService\n- createUser()\n- getUser()"
    }
  ],
  "edges": [
    {
      "id": "edge1",
      "fromNode": "node1",
      "toNode": "node2",
      "fromSide": "right",
      "toSide": "left",
      "label": "calls"
    }
  ]
}
```

## Analysis Steps
1. Scan project directory structure
2. Identify entry files and core modules
3. Analyze import/require statements to extract dependency relationships
4. Identify database operations, API calls, external services
5. Layout node positions by call hierarchy
6. Generate complete .canvas JSON
```

## Usage Example

```
Please analyze the /home/user/my-project project and generate a file-level architecture whiteboard.
Focus on:
- API routes and handler functions
- Database models and operations
- External service calls
```

## Output File

The generated `.canvas` file can be directly opened and edited in Obsidian.
