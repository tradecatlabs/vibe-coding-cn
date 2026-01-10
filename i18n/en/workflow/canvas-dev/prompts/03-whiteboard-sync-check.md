# 03-Whiteboard Sync Check Prompt

> Validate consistency between whiteboard and actual code

## Use Cases

- Check if whiteboard needs updating before PR/MR merge
- Periodic audit of architecture documentation accuracy
- Discover implicit dependencies in code

## Prompt

```markdown
You are a code and architecture consistency checking expert. Please compare the following whiteboard and code to find inconsistencies.

## Input

Canvas whiteboard JSON:
```json
{CANVAS_JSON}
```

Project code path: {PROJECT_PATH}

## Check Items

1. **Node Completeness**
   - Do all nodes in the whiteboard have corresponding code files/classes?
   - Are there important modules in code not recorded in whiteboard?

2. **Edge Accuracy**
   - Do whiteboard edges reflect real import/call relationships?
   - Are there dependencies in code not marked in whiteboard?

3. **Group Correctness**
   - Is whiteboard grouping consistent with directory structure?
   - Are there abnormal cross-group dependencies?

## Output Format

### 🔴 Severe Inconsistencies (Must Fix)
| Type | Whiteboard | Code | Suggestion |
|:-----|:-----------|:-----|:-----------|
| Missing node | - | UserService.py | Add to whiteboard |
| Wrong edge | A→B | A doesn't call B | Remove edge |

### 🟡 Minor Inconsistencies (Recommend Fix)
| Type | Whiteboard | Code | Suggestion |
|:-----|:-----------|:-----|:-----------|
| Naming inconsistency | user_service | UserService | Unify naming |

### 🟢 Good Consistency
- Node coverage: {X}%
- Edge accuracy: {Y}%

### 📋 Fix Suggestions
1. {specific fix step}
2. {specific fix step}
```

## Automation Script (Optional)

```python
#!/usr/bin/env python3
"""
canvas_sync_check.py - Whiteboard and code consistency check script

Usage: python canvas_sync_check.py project.canvas /path/to/project
"""

import json
import ast
import os
from pathlib import Path

def load_canvas(canvas_path):
    with open(canvas_path) as f:
        return json.load(f)

def extract_imports(py_file):
    """Extract import relationships from Python file"""
    with open(py_file) as f:
        tree = ast.parse(f.read())
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    return imports

def check_consistency(canvas, project_path):
    """Compare whiteboard nodes with actual files"""
    canvas_nodes = {n['text'].split('\n')[0].strip('# ') 
                    for n in canvas.get('nodes', [])}
    
    actual_files = set()
    for py_file in Path(project_path).rglob('*.py'):
        actual_files.add(py_file.stem)
    
    missing_in_canvas = actual_files - canvas_nodes
    missing_in_code = canvas_nodes - actual_files
    
    return {
        'missing_in_canvas': missing_in_canvas,
        'missing_in_code': missing_in_code,
        'coverage': len(canvas_nodes & actual_files) / len(actual_files) * 100
    }

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python canvas_sync_check.py <canvas_file> <project_path>")
        sys.exit(1)
    
    canvas = load_canvas(sys.argv[1])
    result = check_consistency(canvas, sys.argv[2])
    
    print(f"Coverage: {result['coverage']:.1f}%")
    if result['missing_in_canvas']:
        print(f"Missing in whiteboard: {result['missing_in_canvas']}")
    if result['missing_in_code']:
        print(f"Missing in code: {result['missing_in_code']}")
```

## CI/CD Integration

```yaml
# .github/workflows/canvas-check.yml
name: Canvas Sync Check

on:
  pull_request:
    paths:
      - '**.py'
      - '**.canvas'

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check canvas consistency
        run: python scripts/canvas_sync_check.py docs/architecture.canvas src/
```
