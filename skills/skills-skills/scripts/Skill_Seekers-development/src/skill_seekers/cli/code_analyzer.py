#!/usr/bin/env python3
"""
Code Analyzer for GitHub Repositories

Extracts code signatures at configurable depth levels:
- surface: File tree only (existing behavior)
- deep: Parse files for signatures, parameters, types
- full: Complete AST analysis (future enhancement)

Supports multiple languages with language-specific parsers.
"""

import ast
import re
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Parameter:
    """Represents a function parameter."""
    name: str
    type_hint: Optional[str] = None
    default: Optional[str] = None


@dataclass
class FunctionSignature:
    """Represents a function/method signature."""
    name: str
    parameters: List[Parameter]
    return_type: Optional[str] = None
    docstring: Optional[str] = None
    line_number: Optional[int] = None
    is_async: bool = False
    is_method: bool = False
    decorators: List[str] = None

    def __post_init__(self):
        if self.decorators is None:
            self.decorators = []


@dataclass
class ClassSignature:
    """Represents a class signature."""
    name: str
    base_classes: List[str]
    methods: List[FunctionSignature]
    docstring: Optional[str] = None
    line_number: Optional[int] = None


class CodeAnalyzer:
    """
    Analyzes code at different depth levels.
    """

    def __init__(self, depth: str = 'surface'):
        """
        Initialize code analyzer.

        Args:
            depth: Analysis depth ('surface', 'deep', 'full')
        """
        self.depth = depth

    def analyze_file(self, file_path: str, content: str, language: str) -> Dict[str, Any]:
        """
        Analyze a single file based on depth level.

        Args:
            file_path: Path to file in repository
            content: File content as string
            language: Programming language (Python, JavaScript, etc.)

        Returns:
            Dict containing extracted signatures
        """
        if self.depth == 'surface':
            return {}  # Surface level doesn't analyze individual files

        logger.debug(f"Analyzing {file_path} (language: {language}, depth: {self.depth})")

        try:
            if language == 'Python':
                return self._analyze_python(content, file_path)
            elif language in ['JavaScript', 'TypeScript']:
                return self._analyze_javascript(content, file_path)
            elif language in ['C', 'C++']:
                return self._analyze_cpp(content, file_path)
            else:
                logger.debug(f"No analyzer for language: {language}")
                return {}
        except Exception as e:
            logger.warning(f"Error analyzing {file_path}: {e}")
            return {}

    def _analyze_python(self, content: str, file_path: str) -> Dict[str, Any]:
        """Analyze Python file using AST."""
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            logger.debug(f"Syntax error in {file_path}: {e}")
            return {}

        classes = []
        functions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_sig = self._extract_python_class(node)
                classes.append(asdict(class_sig))
            elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                # Only top-level functions (not methods)
                # Fix AST parser to check isinstance(parent.body, list) before 'in' operator
                is_method = False
                try:
                    is_method = any(isinstance(parent, ast.ClassDef)
                                  for parent in ast.walk(tree)
                                  if hasattr(parent, 'body') and isinstance(parent.body, list) and node in parent.body)
                except (TypeError, AttributeError):
                    # If body is not iterable or check fails, assume it's a top-level function
                    is_method = False

                if not is_method:
                    func_sig = self._extract_python_function(node)
                    functions.append(asdict(func_sig))

        return {
            'classes': classes,
            'functions': functions
        }

    def _extract_python_class(self, node: ast.ClassDef) -> ClassSignature:
        """Extract class signature from AST node."""
        # Extract base classes
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(f"{base.value.id}.{base.attr}" if hasattr(base.value, 'id') else base.attr)

        # Extract methods
        methods = []
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                method_sig = self._extract_python_function(item, is_method=True)
                methods.append(method_sig)

        # Extract docstring
        docstring = ast.get_docstring(node)

        return ClassSignature(
            name=node.name,
            base_classes=bases,
            methods=methods,
            docstring=docstring,
            line_number=node.lineno
        )

    def _extract_python_function(self, node, is_method: bool = False) -> FunctionSignature:
        """Extract function signature from AST node."""
        # Extract parameters
        params = []
        for arg in node.args.args:
            param_type = None
            if arg.annotation:
                param_type = ast.unparse(arg.annotation) if hasattr(ast, 'unparse') else None

            params.append(Parameter(
                name=arg.arg,
                type_hint=param_type
            ))

        # Extract defaults
        defaults = node.args.defaults
        if defaults:
            # Defaults are aligned to the end of params
            num_no_default = len(params) - len(defaults)
            for i, default in enumerate(defaults):
                param_idx = num_no_default + i
                if param_idx < len(params):
                    try:
                        params[param_idx].default = ast.unparse(default) if hasattr(ast, 'unparse') else str(default)
                    except:
                        params[param_idx].default = "..."

        # Extract return type
        return_type = None
        if node.returns:
            try:
                return_type = ast.unparse(node.returns) if hasattr(ast, 'unparse') else None
            except:
                pass

        # Extract decorators
        decorators = []
        for decorator in node.decorator_list:
            try:
                if hasattr(ast, 'unparse'):
                    decorators.append(ast.unparse(decorator))
                elif isinstance(decorator, ast.Name):
                    decorators.append(decorator.id)
            except:
                pass

        # Extract docstring
        docstring = ast.get_docstring(node)

        return FunctionSignature(
            name=node.name,
            parameters=params,
            return_type=return_type,
            docstring=docstring,
            line_number=node.lineno,
            is_async=isinstance(node, ast.AsyncFunctionDef),
            is_method=is_method,
            decorators=decorators
        )

    def _analyze_javascript(self, content: str, file_path: str) -> Dict[str, Any]:
        """
        Analyze JavaScript/TypeScript file using regex patterns.

        Note: This is a simplified approach. For production, consider using
        a proper JS/TS parser like esprima or ts-morph.
        """
        classes = []
        functions = []

        # Extract class definitions
        class_pattern = r'class\s+(\w+)(?:\s+extends\s+(\w+))?\s*\{'
        for match in re.finditer(class_pattern, content):
            class_name = match.group(1)
            base_class = match.group(2) if match.group(2) else None

            # Try to extract methods (simplified)
            class_block_start = match.end()
            # This is a simplification - proper parsing would track braces
            class_block_end = content.find('}', class_block_start)
            if class_block_end != -1:
                class_body = content[class_block_start:class_block_end]
                methods = self._extract_js_methods(class_body)
            else:
                methods = []

            classes.append({
                'name': class_name,
                'base_classes': [base_class] if base_class else [],
                'methods': methods,
                'docstring': None,
                'line_number': content[:match.start()].count('\n') + 1
            })

        # Extract top-level functions
        func_pattern = r'(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)'
        for match in re.finditer(func_pattern, content):
            func_name = match.group(1)
            params_str = match.group(2)
            is_async = 'async' in match.group(0)

            params = self._parse_js_parameters(params_str)

            functions.append({
                'name': func_name,
                'parameters': params,
                'return_type': None,  # JS doesn't have type annotations (unless TS)
                'docstring': None,
                'line_number': content[:match.start()].count('\n') + 1,
                'is_async': is_async,
                'is_method': False,
                'decorators': []
            })

        # Extract arrow functions assigned to const/let
        arrow_pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\(([^)]*)\)\s*=>'
        for match in re.finditer(arrow_pattern, content):
            func_name = match.group(1)
            params_str = match.group(2)
            is_async = 'async' in match.group(0)

            params = self._parse_js_parameters(params_str)

            functions.append({
                'name': func_name,
                'parameters': params,
                'return_type': None,
                'docstring': None,
                'line_number': content[:match.start()].count('\n') + 1,
                'is_async': is_async,
                'is_method': False,
                'decorators': []
            })

        return {
            'classes': classes,
            'functions': functions
        }

    def _extract_js_methods(self, class_body: str) -> List[Dict]:
        """Extract method signatures from class body."""
        methods = []

        # Match method definitions
        method_pattern = r'(?:async\s+)?(\w+)\s*\(([^)]*)\)'
        for match in re.finditer(method_pattern, class_body):
            method_name = match.group(1)
            params_str = match.group(2)
            is_async = 'async' in match.group(0)

            # Skip constructor keyword detection
            if method_name in ['if', 'for', 'while', 'switch']:
                continue

            params = self._parse_js_parameters(params_str)

            methods.append({
                'name': method_name,
                'parameters': params,
                'return_type': None,
                'docstring': None,
                'line_number': None,
                'is_async': is_async,
                'is_method': True,
                'decorators': []
            })

        return methods

    def _parse_js_parameters(self, params_str: str) -> List[Dict]:
        """Parse JavaScript parameter string."""
        params = []

        if not params_str.strip():
            return params

        # Split by comma (simplified - doesn't handle complex default values)
        param_list = [p.strip() for p in params_str.split(',')]

        for param in param_list:
            if not param:
                continue

            # Check for default value
            if '=' in param:
                name, default = param.split('=', 1)
                name = name.strip()
                default = default.strip()
            else:
                name = param
                default = None

            # Check for type annotation (TypeScript)
            type_hint = None
            if ':' in name:
                name, type_hint = name.split(':', 1)
                name = name.strip()
                type_hint = type_hint.strip()

            params.append({
                'name': name,
                'type_hint': type_hint,
                'default': default
            })

        return params

    def _analyze_cpp(self, content: str, file_path: str) -> Dict[str, Any]:
        """
        Analyze C/C++ header file using regex patterns.

        Note: This is a simplified approach focusing on header files.
        For production, consider using libclang or similar.
        """
        classes = []
        functions = []

        # Extract class definitions (simplified - doesn't handle nested classes)
        class_pattern = r'class\s+(\w+)(?:\s*:\s*public\s+(\w+))?\s*\{'
        for match in re.finditer(class_pattern, content):
            class_name = match.group(1)
            base_class = match.group(2) if match.group(2) else None

            classes.append({
                'name': class_name,
                'base_classes': [base_class] if base_class else [],
                'methods': [],  # Simplified - would need to parse class body
                'docstring': None,
                'line_number': content[:match.start()].count('\n') + 1
            })

        # Extract function declarations
        func_pattern = r'(\w+(?:\s*\*|\s*&)?)\s+(\w+)\s*\(([^)]*)\)'
        for match in re.finditer(func_pattern, content):
            return_type = match.group(1).strip()
            func_name = match.group(2)
            params_str = match.group(3)

            # Skip common keywords
            if func_name in ['if', 'for', 'while', 'switch', 'return']:
                continue

            params = self._parse_cpp_parameters(params_str)

            functions.append({
                'name': func_name,
                'parameters': params,
                'return_type': return_type,
                'docstring': None,
                'line_number': content[:match.start()].count('\n') + 1,
                'is_async': False,
                'is_method': False,
                'decorators': []
            })

        return {
            'classes': classes,
            'functions': functions
        }

    def _parse_cpp_parameters(self, params_str: str) -> List[Dict]:
        """Parse C++ parameter string."""
        params = []

        if not params_str.strip() or params_str.strip() == 'void':
            return params

        # Split by comma (simplified)
        param_list = [p.strip() for p in params_str.split(',')]

        for param in param_list:
            if not param:
                continue

            # Check for default value
            default = None
            if '=' in param:
                param, default = param.rsplit('=', 1)
                param = param.strip()
                default = default.strip()

            # Extract type and name (simplified)
            # Format: "type name" or "type* name" or "type& name"
            parts = param.split()
            if len(parts) >= 2:
                param_type = ' '.join(parts[:-1])
                param_name = parts[-1]
            else:
                param_type = param
                param_name = "unknown"

            params.append({
                'name': param_name,
                'type_hint': param_type,
                'default': default
            })

        return params


if __name__ == '__main__':
    # Test the analyzer
    python_code = '''
class Node2D:
    """Base class for 2D nodes."""

    def move_local_x(self, delta: float, snap: bool = False) -> None:
        """Move node along local X axis."""
        pass

    async def tween_position(self, target: tuple, duration: float = 1.0):
        """Animate position to target."""
        pass

def create_sprite(texture: str) -> Node2D:
    """Create a new sprite node."""
    return Node2D()
'''

    analyzer = CodeAnalyzer(depth='deep')
    result = analyzer.analyze_file('test.py', python_code, 'Python')

    print("Analysis Result:")
    print(f"Classes: {len(result.get('classes', []))}")
    print(f"Functions: {len(result.get('functions', []))}")

    if result.get('classes'):
        cls = result['classes'][0]
        print(f"\nClass: {cls['name']}")
        print(f"  Methods: {len(cls['methods'])}")
        for method in cls['methods']:
            params = ', '.join([f"{p['name']}: {p['type_hint']}" + (f" = {p['default']}" if p.get('default') else "")
                               for p in method['parameters']])
            print(f"    {method['name']}({params}) -> {method['return_type']}")
