#!/usr/bin/env python3
"""
Demo: Conflict Detection and Reporting

This demonstrates the unified scraper's ability to detect and report
conflicts between documentation and code implementation.
"""

import sys
import json
from pathlib import Path

# Add CLI to path
sys.path.insert(0, str(Path(__file__).parent / 'cli'))

from conflict_detector import ConflictDetector

print("=" * 70)
print("UNIFIED SCRAPER - CONFLICT DETECTION DEMO")
print("=" * 70)
print()

# Load test data
print("📂 Loading test data...")
print("   - Documentation APIs from example docs")
print("   - Code APIs from example repository")
print()

with open('cli/conflicts.json', 'r') as f:
    conflicts_data = json.load(f)

conflicts = conflicts_data['conflicts']
summary = conflicts_data['summary']

print(f"✅ Loaded {summary['total']} conflicts")
print()

# Display summary
print("=" * 70)
print("CONFLICT SUMMARY")
print("=" * 70)
print()

print(f"📊 **Total Conflicts**: {summary['total']}")
print()

print("**By Type:**")
for conflict_type, count in summary['by_type'].items():
    if count > 0:
        emoji = "📖" if conflict_type == "missing_in_docs" else "💻" if conflict_type == "missing_in_code" else "⚠️"
        print(f"   {emoji} {conflict_type}: {count}")
print()

print("**By Severity:**")
for severity, count in summary['by_severity'].items():
    if count > 0:
        emoji = "🔴" if severity == "high" else "🟡" if severity == "medium" else "🟢"
        print(f"   {emoji} {severity.upper()}: {count}")
print()

# Display detailed conflicts
print("=" * 70)
print("DETAILED CONFLICT REPORTS")
print("=" * 70)
print()

# Group by severity
high = [c for c in conflicts if c['severity'] == 'high']
medium = [c for c in conflicts if c['severity'] == 'medium']
low = [c for c in conflicts if c['severity'] == 'low']

# Show high severity first
if high:
    print("🔴 **HIGH SEVERITY CONFLICTS** (Requires immediate attention)")
    print("-" * 70)
    for conflict in high:
        print()
        print(f"**API**: `{conflict['api_name']}`")
        print(f"**Type**: {conflict['type']}")
        print(f"**Issue**: {conflict['difference']}")
        print(f"**Suggestion**: {conflict['suggestion']}")

        if conflict['docs_info']:
            print(f"\n**Documented as**:")
            print(f"  Signature: {conflict['docs_info'].get('raw_signature', 'N/A')}")

        if conflict['code_info']:
            print(f"\n**Implemented as**:")
            params = conflict['code_info'].get('parameters', [])
            param_str = ', '.join(f"{p['name']}: {p.get('type_hint', 'Any')}" for p in params if p['name'] != 'self')
            print(f"  Signature: {conflict['code_info']['name']}({param_str})")
            print(f"  Return type: {conflict['code_info'].get('return_type', 'None')}")
            print(f"  Location: {conflict['code_info'].get('source', 'N/A')}:{conflict['code_info'].get('line', '?')}")
    print()

# Show medium severity
if medium:
    print("🟡 **MEDIUM SEVERITY CONFLICTS** (Review recommended)")
    print("-" * 70)
    for conflict in medium[:3]:  # Show first 3
        print()
        print(f"**API**: `{conflict['api_name']}`")
        print(f"**Type**: {conflict['type']}")
        print(f"**Issue**: {conflict['difference']}")

        if conflict['code_info']:
            print(f"**Location**: {conflict['code_info'].get('source', 'N/A')}")

    if len(medium) > 3:
        print(f"\n   ... and {len(medium) - 3} more medium severity conflicts")
    print()

# Example: How conflicts appear in final skill
print("=" * 70)
print("HOW CONFLICTS APPEAR IN SKILL.MD")
print("=" * 70)
print()

example_conflict = high[0] if high else medium[0] if medium else conflicts[0]

print("```markdown")
print("## 🔧 API Reference")
print()
print("### ⚠️ APIs with Conflicts")
print()
print(f"#### `{example_conflict['api_name']}`")
print()
print(f"⚠️ **Conflict**: {example_conflict['difference']}")
print()

if example_conflict.get('docs_info'):
    print("**Documentation says:**")
    print("```")
    print(example_conflict['docs_info'].get('raw_signature', 'N/A'))
    print("```")
    print()

if example_conflict.get('code_info'):
    print("**Code implementation:**")
    print("```python")
    params = example_conflict['code_info'].get('parameters', [])
    param_strs = []
    for p in params:
        if p['name'] == 'self':
            continue
        param_str = p['name']
        if p.get('type_hint'):
            param_str += f": {p['type_hint']}"
        if p.get('default'):
            param_str += f" = {p['default']}"
        param_strs.append(param_str)

    sig = f"def {example_conflict['code_info']['name']}({', '.join(param_strs)})"
    if example_conflict['code_info'].get('return_type'):
        sig += f" -> {example_conflict['code_info']['return_type']}"

    print(sig)
    print("```")
print()

print("*Source: both (conflict)*")
print("```")
print()

# Key takeaways
print("=" * 70)
print("KEY TAKEAWAYS")
print("=" * 70)
print()

print("✅ **What the Unified Scraper Does:**")
print("   1. Extracts APIs from both documentation and code")
print("   2. Compares them to detect discrepancies")
print("   3. Classifies conflicts by type and severity")
print("   4. Provides actionable suggestions")
print("   5. Shows both versions transparently in the skill")
print()

print("⚠️ **Common Conflict Types:**")
print("   - **Missing in docs**: Undocumented features in code")
print("   - **Missing in code**: Documented but not implemented")
print("   - **Signature mismatch**: Different parameters/types")
print("   - **Description mismatch**: Different explanations")
print()

print("🎯 **Value:**")
print("   - Identifies documentation gaps")
print("   - Catches outdated documentation")
print("   - Highlights implementation differences")
print("   - Creates single source of truth showing reality")
print()

print("=" * 70)
print("END OF DEMO")
print("=" * 70)
