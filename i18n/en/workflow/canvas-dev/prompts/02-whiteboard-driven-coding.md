# 02-Whiteboard-Driven Coding Prompt

> Generate/modify code based on Canvas whiteboard architecture diagram

## Use Cases

- New feature development: Draw whiteboard first, then generate code
- Architecture refactoring: Modify whiteboard connections, AI syncs code refactoring
- Module splitting: Split nodes on whiteboard, AI generates new files

## Prompt

```markdown
You are an expert at generating code from architecture whiteboards. Please generate corresponding code implementation based on the following Obsidian Canvas whiteboard JSON.

## Input
Canvas JSON:
```json
{CANVAS_JSON}
```

Tech stack: {TECH_STACK}
Target directory: {TARGET_DIR}

## Parsing Rules

1. **Node → File/Class**
   - Title in node text → filename/classname
   - List items in node text → methods/functions
   - Node color/group → module affiliation

2. **Edge → Dependency Relationship**
   - fromNode → toNode = import/call relationship
   - Edge label determines relationship type:
     - "calls" → function call
     - "extends" → class extends
     - "depends" → import
     - "data flow" → parameter passing

3. **Group → Directory Structure**
   - Nodes in the same group go in the same directory
   - Group name → directory name

## Output Requirements

1. Generate complete file structure
2. Each file contains:
   - Correct import statements (based on edges)
   - Class/function definitions (based on node content)
   - Call relationship implementation (based on edge direction)
3. Add necessary type annotations and comments
4. Follow tech stack best practices

## Output Format

```
File: {file_path}
```{language}
{code_content}
```
```

## Usage Example

```
Generate Python FastAPI project code based on the following whiteboard:

{paste .canvas file content}

Tech stack: Python 3.11 + FastAPI + SQLAlchemy
Target directory: /home/user/my-api
```

## Incremental Update Mode

When whiteboard is modified, use the following prompt:

```markdown
Whiteboard has been updated, please compare old and new versions, only modify changed parts:

Old whiteboard: {OLD_CANVAS_JSON}
New whiteboard: {NEW_CANVAS_JSON}

Output:
1. Files to add
2. Files to modify (output only diff)
3. Files to delete
```
