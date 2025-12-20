#!/usr/bin/env python3
"""
Conflict Detector for Multi-Source Skills

Detects conflicts between documentation and code:
- missing_in_docs: API exists in code but not documented
- missing_in_code: API documented but doesn't exist in code
- signature_mismatch: Different parameters/types between docs and code
- description_mismatch: Docs say one thing, code comments say another

Used by unified scraper to identify discrepancies before merging.
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from difflib import SequenceMatcher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Conflict:
    """Represents a conflict between documentation and code."""
    type: str  # 'missing_in_docs', 'missing_in_code', 'signature_mismatch', 'description_mismatch'
    severity: str  # 'low', 'medium', 'high'
    api_name: str
    docs_info: Optional[Dict[str, Any]] = None
    code_info: Optional[Dict[str, Any]] = None
    difference: Optional[str] = None
    suggestion: Optional[str] = None


class ConflictDetector:
    """
    Detects conflicts between documentation and code sources.
    """

    def __init__(self, docs_data: Dict[str, Any], github_data: Dict[str, Any]):
        """
        Initialize conflict detector.

        Args:
            docs_data: Data from documentation scraper
            github_data: Data from GitHub scraper with code analysis
        """
        self.docs_data = docs_data
        self.github_data = github_data

        # Extract API information from both sources
        self.docs_apis = self._extract_docs_apis()
        self.code_apis = self._extract_code_apis()

        logger.info(f"Loaded {len(self.docs_apis)} APIs from documentation")
        logger.info(f"Loaded {len(self.code_apis)} APIs from code")

    def _extract_docs_apis(self) -> Dict[str, Dict[str, Any]]:
        """
        Extract API information from documentation data.

        Returns:
            Dict mapping API name to API info
        """
        apis = {}

        # Documentation structure varies, but typically has 'pages' or 'references'
        pages = self.docs_data.get('pages', {})

        # Handle both dict and list formats
        if isinstance(pages, dict):
            # Format: {url: page_data, ...}
            for url, page_data in pages.items():
                content = page_data.get('content', '')
                title = page_data.get('title', '')

                # Simple heuristic: if title or URL contains "api", "reference", "class", "function"
                # it might be an API page
                if any(keyword in title.lower() or keyword in url.lower()
                       for keyword in ['api', 'reference', 'class', 'function', 'method']):

                    # Extract API signatures from content (simplified)
                    extracted_apis = self._parse_doc_content_for_apis(content, url)
                    apis.update(extracted_apis)
        elif isinstance(pages, list):
            # Format: [{url: '...', apis: [...]}, ...]
            for page in pages:
                url = page.get('url', '')
                page_apis = page.get('apis', [])

                # If APIs are already extracted in the page data
                for api in page_apis:
                    api_name = api.get('name', '')
                    if api_name:
                        apis[api_name] = {
                            'parameters': api.get('parameters', []),
                            'return_type': api.get('return_type', 'Any'),
                            'source_url': url
                        }

        return apis

    def _parse_doc_content_for_apis(self, content: str, source_url: str) -> Dict[str, Dict]:
        """
        Parse documentation content to extract API signatures.

        This is a simplified approach - real implementation would need
        to understand the documentation format (Sphinx, JSDoc, etc.)
        """
        apis = {}

        # Look for function/method signatures in code blocks
        # Common patterns:
        # - function_name(param1, param2)
        # - ClassName.method_name(param1, param2)
        # - def function_name(param1: type, param2: type) -> return_type

        import re

        # Pattern for common API signatures
        patterns = [
            # Python style: def name(params) -> return
            r'def\s+(\w+)\s*\(([^)]*)\)(?:\s*->\s*(\w+))?',
            # JavaScript style: function name(params)
            r'function\s+(\w+)\s*\(([^)]*)\)',
            # C++ style: return_type name(params)
            r'(\w+)\s+(\w+)\s*\(([^)]*)\)',
            # Method style: ClassName.method_name(params)
            r'(\w+)\.(\w+)\s*\(([^)]*)\)'
        ]

        for pattern in patterns:
            for match in re.finditer(pattern, content):
                groups = match.groups()

                # Parse based on pattern matched
                if 'def' in pattern:
                    # Python function
                    name = groups[0]
                    params_str = groups[1]
                    return_type = groups[2] if len(groups) > 2 else None
                elif 'function' in pattern:
                    # JavaScript function
                    name = groups[0]
                    params_str = groups[1]
                    return_type = None
                elif '.' in pattern:
                    # Class method
                    class_name = groups[0]
                    method_name = groups[1]
                    name = f"{class_name}.{method_name}"
                    params_str = groups[2] if len(groups) > 2 else groups[1]
                    return_type = None
                else:
                    # C++ function
                    return_type = groups[0]
                    name = groups[1]
                    params_str = groups[2]

                # Parse parameters
                params = self._parse_param_string(params_str)

                apis[name] = {
                    'name': name,
                    'parameters': params,
                    'return_type': return_type,
                    'source': source_url,
                    'raw_signature': match.group(0)
                }

        return apis

    def _parse_param_string(self, params_str: str) -> List[Dict]:
        """Parse parameter string into list of parameter dicts."""
        if not params_str.strip():
            return []

        params = []
        for param in params_str.split(','):
            param = param.strip()
            if not param:
                continue

            # Try to extract name and type
            param_info = {'name': param, 'type': None, 'default': None}

            # Check for type annotation (: type)
            if ':' in param:
                parts = param.split(':', 1)
                param_info['name'] = parts[0].strip()
                type_part = parts[1].strip()

                # Check for default value (= value)
                if '=' in type_part:
                    type_str, default_str = type_part.split('=', 1)
                    param_info['type'] = type_str.strip()
                    param_info['default'] = default_str.strip()
                else:
                    param_info['type'] = type_part

            # Check for default without type (= value)
            elif '=' in param:
                parts = param.split('=', 1)
                param_info['name'] = parts[0].strip()
                param_info['default'] = parts[1].strip()

            params.append(param_info)

        return params

    def _extract_code_apis(self) -> Dict[str, Dict[str, Any]]:
        """
        Extract API information from GitHub code analysis.

        Returns:
            Dict mapping API name to API info
        """
        apis = {}

        code_analysis = self.github_data.get('code_analysis', {})
        if not code_analysis:
            return apis

        # Support both 'files' and 'analyzed_files' keys
        files = code_analysis.get('files', code_analysis.get('analyzed_files', []))

        for file_info in files:
            file_path = file_info.get('file', 'unknown')

            # Extract classes and their methods
            for class_info in file_info.get('classes', []):
                class_name = class_info['name']

                # Add class itself
                apis[class_name] = {
                    'name': class_name,
                    'type': 'class',
                    'source': file_path,
                    'line': class_info.get('line_number'),
                    'base_classes': class_info.get('base_classes', []),
                    'docstring': class_info.get('docstring')
                }

                # Add methods
                for method in class_info.get('methods', []):
                    method_name = f"{class_name}.{method['name']}"
                    apis[method_name] = {
                        'name': method_name,
                        'type': 'method',
                        'parameters': method.get('parameters', []),
                        'return_type': method.get('return_type'),
                        'source': file_path,
                        'line': method.get('line_number'),
                        'docstring': method.get('docstring'),
                        'is_async': method.get('is_async', False)
                    }

            # Extract standalone functions
            for func_info in file_info.get('functions', []):
                func_name = func_info['name']
                apis[func_name] = {
                    'name': func_name,
                    'type': 'function',
                    'parameters': func_info.get('parameters', []),
                    'return_type': func_info.get('return_type'),
                    'source': file_path,
                    'line': func_info.get('line_number'),
                    'docstring': func_info.get('docstring'),
                    'is_async': func_info.get('is_async', False)
                }

        return apis

    def detect_all_conflicts(self) -> List[Conflict]:
        """
        Detect all types of conflicts.

        Returns:
            List of Conflict objects
        """
        logger.info("Detecting conflicts between documentation and code...")

        conflicts = []

        # 1. Find APIs missing in documentation
        conflicts.extend(self._find_missing_in_docs())

        # 2. Find APIs missing in code
        conflicts.extend(self._find_missing_in_code())

        # 3. Find signature mismatches
        conflicts.extend(self._find_signature_mismatches())

        logger.info(f"Found {len(conflicts)} conflicts total")

        return conflicts

    def _find_missing_in_docs(self) -> List[Conflict]:
        """Find APIs that exist in code but not in documentation."""
        conflicts = []

        for api_name, code_info in self.code_apis.items():
            # Simple name matching (can be enhanced with fuzzy matching)
            if api_name not in self.docs_apis:
                # Check if it's a private/internal API (often not documented)
                is_private = api_name.startswith('_') or '__' in api_name
                severity = 'low' if is_private else 'medium'

                conflicts.append(Conflict(
                    type='missing_in_docs',
                    severity=severity,
                    api_name=api_name,
                    code_info=code_info,
                    difference=f"API exists in code ({code_info['source']}) but not found in documentation",
                    suggestion="Add documentation for this API" if not is_private else "Consider if this internal API should be documented"
                ))

        logger.info(f"Found {len(conflicts)} APIs missing in documentation")
        return conflicts

    def _find_missing_in_code(self) -> List[Conflict]:
        """Find APIs that are documented but don't exist in code."""
        conflicts = []

        for api_name, docs_info in self.docs_apis.items():
            if api_name not in self.code_apis:
                conflicts.append(Conflict(
                    type='missing_in_code',
                    severity='high',  # This is serious - documented but doesn't exist
                    api_name=api_name,
                    docs_info=docs_info,
                    difference=f"API documented ({docs_info.get('source', 'unknown')}) but not found in code",
                    suggestion="Update documentation to remove this API, or add it to codebase"
                ))

        logger.info(f"Found {len(conflicts)} APIs missing in code")
        return conflicts

    def _find_signature_mismatches(self) -> List[Conflict]:
        """Find APIs where signature differs between docs and code."""
        conflicts = []

        # Find APIs that exist in both
        common_apis = set(self.docs_apis.keys()) & set(self.code_apis.keys())

        for api_name in common_apis:
            docs_info = self.docs_apis[api_name]
            code_info = self.code_apis[api_name]

            # Compare signatures
            mismatch = self._compare_signatures(docs_info, code_info)

            if mismatch:
                conflicts.append(Conflict(
                    type='signature_mismatch',
                    severity=mismatch['severity'],
                    api_name=api_name,
                    docs_info=docs_info,
                    code_info=code_info,
                    difference=mismatch['difference'],
                    suggestion=mismatch['suggestion']
                ))

        logger.info(f"Found {len(conflicts)} signature mismatches")
        return conflicts

    def _compare_signatures(self, docs_info: Dict, code_info: Dict) -> Optional[Dict]:
        """
        Compare signatures between docs and code.

        Returns:
            Dict with mismatch details if conflict found, None otherwise
        """
        docs_params = docs_info.get('parameters', [])
        code_params = code_info.get('parameters', [])

        # Compare parameter counts
        if len(docs_params) != len(code_params):
            return {
                'severity': 'medium',
                'difference': f"Parameter count mismatch: docs has {len(docs_params)}, code has {len(code_params)}",
                'suggestion': f"Documentation shows {len(docs_params)} parameters, but code has {len(code_params)}"
            }

        # Compare parameter names and types
        for i, (doc_param, code_param) in enumerate(zip(docs_params, code_params)):
            doc_name = doc_param.get('name', '')
            code_name = code_param.get('name', '')

            # Parameter name mismatch
            if doc_name != code_name:
                # Use fuzzy matching for slight variations
                similarity = SequenceMatcher(None, doc_name, code_name).ratio()
                if similarity < 0.8:  # Not similar enough
                    return {
                        'severity': 'medium',
                        'difference': f"Parameter {i+1} name mismatch: '{doc_name}' in docs vs '{code_name}' in code",
                        'suggestion': f"Update documentation to use parameter name '{code_name}'"
                    }

            # Type mismatch
            doc_type = doc_param.get('type')
            code_type = code_param.get('type_hint')

            if doc_type and code_type and doc_type != code_type:
                return {
                    'severity': 'low',
                    'difference': f"Parameter '{doc_name}' type mismatch: '{doc_type}' in docs vs '{code_type}' in code",
                    'suggestion': f"Verify correct type for parameter '{doc_name}'"
                }

        # Compare return types if both have them
        docs_return = docs_info.get('return_type')
        code_return = code_info.get('return_type')

        if docs_return and code_return and docs_return != code_return:
            return {
                'severity': 'low',
                'difference': f"Return type mismatch: '{docs_return}' in docs vs '{code_return}' in code",
                'suggestion': "Verify correct return type"
            }

        return None

    def generate_summary(self, conflicts: List[Conflict]) -> Dict[str, Any]:
        """
        Generate summary statistics for conflicts.

        Args:
            conflicts: List of Conflict objects

        Returns:
            Summary dict with statistics
        """
        summary = {
            'total': len(conflicts),
            'by_type': {},
            'by_severity': {},
            'apis_affected': len(set(c.api_name for c in conflicts))
        }

        # Count by type
        for conflict_type in ['missing_in_docs', 'missing_in_code', 'signature_mismatch', 'description_mismatch']:
            count = sum(1 for c in conflicts if c.type == conflict_type)
            summary['by_type'][conflict_type] = count

        # Count by severity
        for severity in ['low', 'medium', 'high']:
            count = sum(1 for c in conflicts if c.severity == severity)
            summary['by_severity'][severity] = count

        return summary

    def save_conflicts(self, conflicts: List[Conflict], output_path: str):
        """
        Save conflicts to JSON file.

        Args:
            conflicts: List of Conflict objects
            output_path: Path to output JSON file
        """
        data = {
            'conflicts': [asdict(c) for c in conflicts],
            'summary': self.generate_summary(conflicts)
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"Conflicts saved to: {output_path}")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print("Usage: python conflict_detector.py <docs_data.json> <github_data.json>")
        sys.exit(1)

    docs_file = sys.argv[1]
    github_file = sys.argv[2]

    # Load data
    with open(docs_file, 'r') as f:
        docs_data = json.load(f)

    with open(github_file, 'r') as f:
        github_data = json.load(f)

    # Detect conflicts
    detector = ConflictDetector(docs_data, github_data)
    conflicts = detector.detect_all_conflicts()

    # Print summary
    summary = detector.generate_summary(conflicts)
    print("\n📊 Conflict Summary:")
    print(f"   Total conflicts: {summary['total']}")
    print(f"   APIs affected: {summary['apis_affected']}")
    print("\n   By Type:")
    for conflict_type, count in summary['by_type'].items():
        if count > 0:
            print(f"     {conflict_type}: {count}")
    print("\n   By Severity:")
    for severity, count in summary['by_severity'].items():
        if count > 0:
            emoji = '🔴' if severity == 'high' else '🟡' if severity == 'medium' else '🟢'
            print(f"     {emoji} {severity}: {count}")

    # Save to file
    output_file = 'conflicts.json'
    detector.save_conflicts(conflicts, output_file)
    print(f"\n✅ Full report saved to: {output_file}")
