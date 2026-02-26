#!/usr/bin/env python3
"""
Quality Checker for Claude Skills
Validates skill quality, checks links, and generates quality reports.

Usage:
    python3 quality_checker.py output/react/
    python3 quality_checker.py output/godot/ --verbose
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class QualityIssue:
    """Represents a quality issue found during validation."""
    level: str  # 'error', 'warning', 'info'
    category: str  # 'enhancement', 'content', 'links', 'structure'
    message: str
    file: Optional[str] = None
    line: Optional[int] = None


@dataclass
class QualityReport:
    """Complete quality report for a skill."""
    skill_name: str
    skill_path: Path
    errors: List[QualityIssue] = field(default_factory=list)
    warnings: List[QualityIssue] = field(default_factory=list)
    info: List[QualityIssue] = field(default_factory=list)

    def add_error(self, category: str, message: str, file: str = None, line: int = None):
        """Add an error to the report."""
        self.errors.append(QualityIssue('error', category, message, file, line))

    def add_warning(self, category: str, message: str, file: str = None, line: int = None):
        """Add a warning to the report."""
        self.warnings.append(QualityIssue('warning', category, message, file, line))

    def add_info(self, category: str, message: str, file: str = None, line: int = None):
        """Add info to the report."""
        self.info.append(QualityIssue('info', category, message, file, line))

    @property
    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return len(self.warnings) > 0

    @property
    def is_excellent(self) -> bool:
        """Check if quality is excellent (no errors, no warnings)."""
        return not self.has_errors and not self.has_warnings

    @property
    def quality_score(self) -> float:
        """Calculate quality score (0-100)."""
        # Start with perfect score
        score = 100.0

        # Deduct points for issues
        score -= len(self.errors) * 15  # -15 per error
        score -= len(self.warnings) * 5  # -5 per warning

        # Never go below 0
        return max(0.0, score)

    @property
    def quality_grade(self) -> str:
        """Get quality grade (A-F)."""
        score = self.quality_score
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'


class SkillQualityChecker:
    """Validates skill quality and generates reports."""

    def __init__(self, skill_dir: Path):
        """Initialize quality checker.

        Args:
            skill_dir: Path to skill directory
        """
        self.skill_dir = Path(skill_dir)
        self.skill_md_path = self.skill_dir / "SKILL.md"
        self.references_dir = self.skill_dir / "references"
        self.report = QualityReport(
            skill_name=self.skill_dir.name,
            skill_path=self.skill_dir
        )

    def check_all(self) -> QualityReport:
        """Run all quality checks and return report.

        Returns:
            QualityReport: Complete quality report
        """
        # Basic structure checks
        self._check_skill_structure()

        # Enhancement verification
        self._check_enhancement_quality()

        # Content quality checks
        self._check_content_quality()

        # Link validation
        self._check_links()

        return self.report

    def _check_skill_structure(self):
        """Check basic skill structure."""
        # Check SKILL.md exists
        if not self.skill_md_path.exists():
            self.report.add_error(
                'structure',
                'SKILL.md file not found',
                str(self.skill_md_path)
            )
            return

        # Check references directory exists
        if not self.references_dir.exists():
            self.report.add_warning(
                'structure',
                'references/ directory not found - skill may be incomplete',
                str(self.references_dir)
            )
        elif not list(self.references_dir.glob('*.md')):
            self.report.add_warning(
                'structure',
                'references/ directory is empty - no reference documentation found',
                str(self.references_dir)
            )

    def _check_enhancement_quality(self):
        """Check if SKILL.md was properly enhanced."""
        if not self.skill_md_path.exists():
            return

        content = self.skill_md_path.read_text(encoding='utf-8')

        # Check for template indicators (signs it wasn't enhanced)
        template_indicators = [
            "TODO:",
            "[Add description]",
            "[Framework specific tips]",
            "coming soon",
        ]

        for indicator in template_indicators:
            if indicator.lower() in content.lower():
                self.report.add_warning(
                    'enhancement',
                    f'Found template placeholder: "{indicator}" - SKILL.md may not be enhanced',
                    'SKILL.md'
                )

        # Check for good signs of enhancement
        enhancement_indicators = {
            'code_examples': re.compile(r'```[\w-]+\n', re.MULTILINE),
            'real_examples': re.compile(r'Example:', re.IGNORECASE),
            'sections': re.compile(r'^## .+', re.MULTILINE),
        }

        code_blocks = len(enhancement_indicators['code_examples'].findall(content))
        real_examples = len(enhancement_indicators['real_examples'].findall(content))
        sections = len(enhancement_indicators['sections'].findall(content))

        # Quality thresholds
        if code_blocks == 0:
            self.report.add_warning(
                'enhancement',
                'No code examples found in SKILL.md - consider enhancing',
                'SKILL.md'
            )
        elif code_blocks < 3:
            self.report.add_info(
                'enhancement',
                f'Only {code_blocks} code examples found - more examples would improve quality',
                'SKILL.md'
            )
        else:
            self.report.add_info(
                'enhancement',
                f'✓ Found {code_blocks} code examples',
                'SKILL.md'
            )

        if sections < 4:
            self.report.add_warning(
                'enhancement',
                f'Only {sections} sections found - SKILL.md may be too basic',
                'SKILL.md'
            )
        else:
            self.report.add_info(
                'enhancement',
                f'✓ Found {sections} sections',
                'SKILL.md'
            )

    def _check_content_quality(self):
        """Check content quality."""
        if not self.skill_md_path.exists():
            return

        content = self.skill_md_path.read_text(encoding='utf-8')

        # Check YAML frontmatter
        if not content.startswith('---'):
            self.report.add_error(
                'content',
                'Missing YAML frontmatter - SKILL.md must start with ---',
                'SKILL.md',
                1
            )
        else:
            # Extract frontmatter
            try:
                frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
                if frontmatter_match:
                    frontmatter = frontmatter_match.group(1)

                    # Check for required fields
                    if 'name:' not in frontmatter:
                        self.report.add_error(
                            'content',
                            'Missing "name:" field in YAML frontmatter',
                            'SKILL.md',
                            2
                        )

                    # Check for description
                    if 'description:' in frontmatter:
                        self.report.add_info(
                            'content',
                            '✓ YAML frontmatter includes description',
                            'SKILL.md'
                        )
                else:
                    self.report.add_error(
                        'content',
                        'Invalid YAML frontmatter format',
                        'SKILL.md',
                        1
                    )
            except Exception as e:
                self.report.add_error(
                    'content',
                    f'Error parsing YAML frontmatter: {e}',
                    'SKILL.md',
                    1
                )

        # Check code block language tags
        code_blocks_without_lang = re.findall(r'```\n[^`]', content)
        if code_blocks_without_lang:
            self.report.add_warning(
                'content',
                f'Found {len(code_blocks_without_lang)} code blocks without language tags',
                'SKILL.md'
            )

        # Check for "When to Use" section
        if 'when to use' not in content.lower():
            self.report.add_warning(
                'content',
                'Missing "When to Use This Skill" section',
                'SKILL.md'
            )
        else:
            self.report.add_info(
                'content',
                '✓ Found "When to Use" section',
                'SKILL.md'
            )

        # Check reference files
        if self.references_dir.exists():
            ref_files = list(self.references_dir.glob('*.md'))
            if ref_files:
                self.report.add_info(
                    'content',
                    f'✓ Found {len(ref_files)} reference files',
                    'references/'
                )

                # Check if references are mentioned in SKILL.md
                mentioned_refs = 0
                for ref_file in ref_files:
                    if ref_file.name in content:
                        mentioned_refs += 1

                if mentioned_refs == 0:
                    self.report.add_warning(
                        'content',
                        'Reference files exist but none are mentioned in SKILL.md',
                        'SKILL.md'
                    )

    def _check_links(self):
        """Check internal markdown links."""
        if not self.skill_md_path.exists():
            return

        content = self.skill_md_path.read_text(encoding='utf-8')

        # Find all markdown links [text](path)
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        links = link_pattern.findall(content)

        broken_links = []

        for text, link in links:
            # Skip external links (http/https)
            if link.startswith('http://') or link.startswith('https://'):
                continue

            # Skip anchor links
            if link.startswith('#'):
                continue

            # Check if file exists (relative to SKILL.md)
            link_path = self.skill_dir / link
            if not link_path.exists():
                broken_links.append((text, link))

        if broken_links:
            for text, link in broken_links:
                self.report.add_warning(
                    'links',
                    f'Broken link: [{text}]({link})',
                    'SKILL.md'
                )
        else:
            if links:
                internal_links = [l for t, l in links if not l.startswith('http')]
                if internal_links:
                    self.report.add_info(
                        'links',
                        f'✓ All {len(internal_links)} internal links are valid',
                        'SKILL.md'
                    )


def print_report(report: QualityReport, verbose: bool = False):
    """Print quality report to console.

    Args:
        report: Quality report to print
        verbose: Show all info messages
    """
    print("\n" + "=" * 60)
    print(f"QUALITY REPORT: {report.skill_name}")
    print("=" * 60)
    print()

    # Quality score
    print(f"Quality Score: {report.quality_score:.1f}/100 (Grade: {report.quality_grade})")
    print()

    # Errors
    if report.errors:
        print(f"❌ ERRORS ({len(report.errors)}):")
        for issue in report.errors:
            location = f" ({issue.file}:{issue.line})" if issue.file and issue.line else f" ({issue.file})" if issue.file else ""
            print(f"   [{issue.category}] {issue.message}{location}")
        print()

    # Warnings
    if report.warnings:
        print(f"⚠️  WARNINGS ({len(report.warnings)}):")
        for issue in report.warnings:
            location = f" ({issue.file}:{issue.line})" if issue.file and issue.line else f" ({issue.file})" if issue.file else ""
            print(f"   [{issue.category}] {issue.message}{location}")
        print()

    # Info (only in verbose mode)
    if verbose and report.info:
        print(f"ℹ️  INFO ({len(report.info)}):")
        for issue in report.info:
            location = f" ({issue.file})" if issue.file else ""
            print(f"   [{issue.category}] {issue.message}{location}")
        print()

    # Summary
    if report.is_excellent:
        print("✅ EXCELLENT! No issues found.")
    elif not report.has_errors:
        print("✓ GOOD! No errors, but some warnings to review.")
    else:
        print("❌ NEEDS IMPROVEMENT! Please fix errors before packaging.")

    print()


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Check skill quality and generate report",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic quality check
  python3 quality_checker.py output/react/

  # Verbose mode (show all info)
  python3 quality_checker.py output/godot/ --verbose

  # Exit with error code if issues found
  python3 quality_checker.py output/django/ --strict
"""
    )

    parser.add_argument(
        'skill_directory',
        help='Path to skill directory (e.g., output/react/)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show all info messages'
    )

    parser.add_argument(
        '--strict',
        action='store_true',
        help='Exit with error code if any warnings or errors found'
    )

    args = parser.parse_args()

    # Check if directory exists
    skill_dir = Path(args.skill_directory)
    if not skill_dir.exists():
        print(f"❌ Directory not found: {skill_dir}")
        sys.exit(1)

    # Run quality checks
    checker = SkillQualityChecker(skill_dir)
    report = checker.check_all()

    # Print report
    print_report(report, verbose=args.verbose)

    # Exit code
    if args.strict and (report.has_errors or report.has_warnings):
        sys.exit(1)
    elif report.has_errors:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
