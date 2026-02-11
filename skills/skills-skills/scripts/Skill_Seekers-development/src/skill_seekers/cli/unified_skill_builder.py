#!/usr/bin/env python3
"""
Unified Skill Builder

Generates final skill structure from merged multi-source data:
- SKILL.md with merged APIs and conflict warnings
- references/ with organized content by source
- Inline conflict markers (⚠️)
- Separate conflicts summary section

Supports mixed sources (documentation, GitHub, PDF) and highlights
discrepancies transparently.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UnifiedSkillBuilder:
    """
    Builds unified skill from multi-source data.
    """

    def __init__(self, config: Dict, scraped_data: Dict,
                 merged_data: Optional[Dict] = None, conflicts: Optional[List] = None):
        """
        Initialize skill builder.

        Args:
            config: Unified config dict
            scraped_data: Dict of scraped data by source type
            merged_data: Merged API data (if conflicts were resolved)
            conflicts: List of detected conflicts
        """
        self.config = config
        self.scraped_data = scraped_data
        self.merged_data = merged_data
        self.conflicts = conflicts or []

        self.name = config['name']
        self.description = config['description']
        self.skill_dir = f"output/{self.name}"

        # Create directories
        os.makedirs(self.skill_dir, exist_ok=True)
        os.makedirs(f"{self.skill_dir}/references", exist_ok=True)
        os.makedirs(f"{self.skill_dir}/scripts", exist_ok=True)
        os.makedirs(f"{self.skill_dir}/assets", exist_ok=True)

    def build(self):
        """Build complete skill structure."""
        logger.info(f"Building unified skill: {self.name}")

        # Generate main SKILL.md
        self._generate_skill_md()

        # Generate reference files by source
        self._generate_references()

        # Generate conflicts report (if any)
        if self.conflicts:
            self._generate_conflicts_report()

        logger.info(f"✅ Unified skill built: {self.skill_dir}/")

    def _generate_skill_md(self):
        """Generate main SKILL.md file."""
        skill_path = os.path.join(self.skill_dir, 'SKILL.md')

        # Generate skill name (lowercase, hyphens only, max 64 chars)
        skill_name = self.name.lower().replace('_', '-').replace(' ', '-')[:64]

        # Truncate description to 1024 chars if needed
        desc = self.description[:1024] if len(self.description) > 1024 else self.description

        content = f"""---
name: {skill_name}
description: {desc}
---

# {self.name.title()}

{self.description}

## 📚 Sources

This skill combines knowledge from multiple sources:

"""

        # List sources
        for source in self.config.get('sources', []):
            source_type = source['type']
            if source_type == 'documentation':
                content += f"- ✅ **Documentation**: {source.get('base_url', 'N/A')}\n"
                content += f"  - Pages: {source.get('max_pages', 'unlimited')}\n"
            elif source_type == 'github':
                content += f"- ✅ **GitHub Repository**: {source.get('repo', 'N/A')}\n"
                content += f"  - Code Analysis: {source.get('code_analysis_depth', 'surface')}\n"
                content += f"  - Issues: {source.get('max_issues', 0)}\n"
            elif source_type == 'pdf':
                content += f"- ✅ **PDF Document**: {source.get('path', 'N/A')}\n"

        # Data quality section
        if self.conflicts:
            content += f"\n## ⚠️ Data Quality\n\n"
            content += f"**{len(self.conflicts)} conflicts detected** between sources.\n\n"

            # Count by type
            by_type = {}
            for conflict in self.conflicts:
                ctype = conflict.type if hasattr(conflict, 'type') else conflict.get('type', 'unknown')
                by_type[ctype] = by_type.get(ctype, 0) + 1

            content += "**Conflict Breakdown:**\n"
            for ctype, count in by_type.items():
                content += f"- {ctype}: {count}\n"

            content += f"\nSee `references/conflicts.md` for detailed conflict information.\n"

        # Merged API section (if available)
        if self.merged_data:
            content += self._format_merged_apis()

        # Quick reference from each source
        content += "\n## 📖 Reference Documentation\n\n"
        content += "Organized by source:\n\n"

        for source in self.config.get('sources', []):
            source_type = source['type']
            content += f"- [{source_type.title()}](references/{source_type}/)\n"

        # When to use this skill
        content += f"\n## 💡 When to Use This Skill\n\n"
        content += f"Use this skill when you need to:\n"
        content += f"- Understand how to use {self.name}\n"
        content += f"- Look up API documentation\n"
        content += f"- Find usage examples\n"

        if 'github' in self.scraped_data:
            content += f"- Check for known issues or recent changes\n"
            content += f"- Review release history\n"

        content += "\n---\n\n"
        content += "*Generated by Skill Seeker's unified multi-source scraper*\n"

        with open(skill_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Created SKILL.md")

    def _format_merged_apis(self) -> str:
        """Format merged APIs section with inline conflict warnings."""
        if not self.merged_data:
            return ""

        content = "\n## 🔧 API Reference\n\n"
        content += "*Merged from documentation and code analysis*\n\n"

        apis = self.merged_data.get('apis', {})

        if not apis:
            return content + "*No APIs to display*\n"

        # Group APIs by status
        matched = {k: v for k, v in apis.items() if v.get('status') == 'matched'}
        conflicts = {k: v for k, v in apis.items() if v.get('status') == 'conflict'}
        docs_only = {k: v for k, v in apis.items() if v.get('status') == 'docs_only'}
        code_only = {k: v for k, v in apis.items() if v.get('status') == 'code_only'}

        # Show matched APIs first
        if matched:
            content += "### ✅ Verified APIs\n\n"
            content += "*Documentation and code agree*\n\n"
            for api_name, api_data in list(matched.items())[:10]:  # Limit to first 10
                content += self._format_api_entry(api_data, inline_conflict=False)

        # Show conflicting APIs with warnings
        if conflicts:
            content += "\n### ⚠️ APIs with Conflicts\n\n"
            content += "*Documentation and code differ*\n\n"
            for api_name, api_data in list(conflicts.items())[:10]:
                content += self._format_api_entry(api_data, inline_conflict=True)

        # Show undocumented APIs
        if code_only:
            content += f"\n### 💻 Undocumented APIs\n\n"
            content += f"*Found in code but not in documentation ({len(code_only)} total)*\n\n"
            for api_name, api_data in list(code_only.items())[:5]:
                content += self._format_api_entry(api_data, inline_conflict=False)

        # Show removed/missing APIs
        if docs_only:
            content += f"\n### 📖 Documentation-Only APIs\n\n"
            content += f"*Documented but not found in code ({len(docs_only)} total)*\n\n"
            for api_name, api_data in list(docs_only.items())[:5]:
                content += self._format_api_entry(api_data, inline_conflict=False)

        content += f"\n*See references/api/ for complete API documentation*\n"

        return content

    def _format_api_entry(self, api_data: Dict, inline_conflict: bool = False) -> str:
        """Format a single API entry."""
        name = api_data.get('name', 'Unknown')
        signature = api_data.get('merged_signature', name)
        description = api_data.get('merged_description', '')
        warning = api_data.get('warning', '')

        entry = f"#### `{signature}`\n\n"

        if description:
            entry += f"{description}\n\n"

        # Add inline conflict warning
        if inline_conflict and warning:
            entry += f"⚠️ **Conflict**: {warning}\n\n"

            # Show both versions if available
            conflict = api_data.get('conflict', {})
            if conflict:
                docs_info = conflict.get('docs_info')
                code_info = conflict.get('code_info')

                if docs_info and code_info:
                    entry += "**Documentation says:**\n"
                    entry += f"```\n{docs_info.get('raw_signature', 'N/A')}\n```\n\n"
                    entry += "**Code implementation:**\n"
                    entry += f"```\n{self._format_code_signature(code_info)}\n```\n\n"

        # Add source info
        source = api_data.get('source', 'unknown')
        entry += f"*Source: {source}*\n\n"

        entry += "---\n\n"

        return entry

    def _format_code_signature(self, code_info: Dict) -> str:
        """Format code signature for display."""
        name = code_info.get('name', '')
        params = code_info.get('parameters', [])
        return_type = code_info.get('return_type')

        param_strs = []
        for param in params:
            param_str = param.get('name', '')
            if param.get('type_hint'):
                param_str += f": {param['type_hint']}"
            if param.get('default'):
                param_str += f" = {param['default']}"
            param_strs.append(param_str)

        sig = f"{name}({', '.join(param_strs)})"
        if return_type:
            sig += f" -> {return_type}"

        return sig

    def _generate_references(self):
        """Generate reference files organized by source."""
        logger.info("Generating reference files...")

        # Generate references for each source type
        if 'documentation' in self.scraped_data:
            self._generate_docs_references()

        if 'github' in self.scraped_data:
            self._generate_github_references()

        if 'pdf' in self.scraped_data:
            self._generate_pdf_references()

        # Generate merged API reference if available
        if self.merged_data:
            self._generate_merged_api_reference()

    def _generate_docs_references(self):
        """Generate references from documentation source."""
        docs_dir = os.path.join(self.skill_dir, 'references', 'documentation')
        os.makedirs(docs_dir, exist_ok=True)

        # Create index
        index_path = os.path.join(docs_dir, 'index.md')
        with open(index_path, 'w') as f:
            f.write("# Documentation\n\n")
            f.write("Reference from official documentation.\n\n")

        logger.info("Created documentation references")

    def _generate_github_references(self):
        """Generate references from GitHub source."""
        github_dir = os.path.join(self.skill_dir, 'references', 'github')
        os.makedirs(github_dir, exist_ok=True)

        github_data = self.scraped_data['github']['data']

        # Create README reference
        if github_data.get('readme'):
            readme_path = os.path.join(github_dir, 'README.md')
            with open(readme_path, 'w') as f:
                f.write("# Repository README\n\n")
                f.write(github_data['readme'])

        # Create issues reference
        if github_data.get('issues'):
            issues_path = os.path.join(github_dir, 'issues.md')
            with open(issues_path, 'w') as f:
                f.write("# GitHub Issues\n\n")
                f.write(f"{len(github_data['issues'])} recent issues.\n\n")

                for issue in github_data['issues'][:20]:
                    f.write(f"## #{issue['number']}: {issue['title']}\n\n")
                    f.write(f"**State**: {issue['state']}\n")
                    if issue.get('labels'):
                        f.write(f"**Labels**: {', '.join(issue['labels'])}\n")
                    f.write(f"**URL**: {issue.get('url', 'N/A')}\n\n")

        # Create releases reference
        if github_data.get('releases'):
            releases_path = os.path.join(github_dir, 'releases.md')
            with open(releases_path, 'w') as f:
                f.write("# Releases\n\n")

                for release in github_data['releases'][:10]:
                    f.write(f"## {release['tag_name']}: {release.get('name', 'N/A')}\n\n")
                    f.write(f"**Published**: {release.get('published_at', 'N/A')[:10]}\n\n")
                    if release.get('body'):
                        f.write(release['body'][:500])
                        f.write("\n\n")

        logger.info("Created GitHub references")

    def _generate_pdf_references(self):
        """Generate references from PDF source."""
        pdf_dir = os.path.join(self.skill_dir, 'references', 'pdf')
        os.makedirs(pdf_dir, exist_ok=True)

        # Create index
        index_path = os.path.join(pdf_dir, 'index.md')
        with open(index_path, 'w') as f:
            f.write("# PDF Documentation\n\n")
            f.write("Reference from PDF document.\n\n")

        logger.info("Created PDF references")

    def _generate_merged_api_reference(self):
        """Generate merged API reference file."""
        api_dir = os.path.join(self.skill_dir, 'references', 'api')
        os.makedirs(api_dir, exist_ok=True)

        api_path = os.path.join(api_dir, 'merged_api.md')

        with open(api_path, 'w') as f:
            f.write("# Merged API Reference\n\n")
            f.write("*Combined from documentation and code analysis*\n\n")

            apis = self.merged_data.get('apis', {})

            for api_name in sorted(apis.keys()):
                api_data = apis[api_name]
                entry = self._format_api_entry(api_data, inline_conflict=True)
                f.write(entry)

        logger.info(f"Created merged API reference ({len(apis)} APIs)")

    def _generate_conflicts_report(self):
        """Generate detailed conflicts report."""
        conflicts_path = os.path.join(self.skill_dir, 'references', 'conflicts.md')

        with open(conflicts_path, 'w') as f:
            f.write("# Conflict Report\n\n")
            f.write(f"Found **{len(self.conflicts)}** conflicts between sources.\n\n")

            # Group by severity
            high = [c for c in self.conflicts if (hasattr(c, 'severity') and c.severity == 'high') or c.get('severity') == 'high']
            medium = [c for c in self.conflicts if (hasattr(c, 'severity') and c.severity == 'medium') or c.get('severity') == 'medium']
            low = [c for c in self.conflicts if (hasattr(c, 'severity') and c.severity == 'low') or c.get('severity') == 'low']

            f.write("## Severity Breakdown\n\n")
            f.write(f"- 🔴 **High**: {len(high)} (action required)\n")
            f.write(f"- 🟡 **Medium**: {len(medium)} (review recommended)\n")
            f.write(f"- 🟢 **Low**: {len(low)} (informational)\n\n")

            # List high severity conflicts
            if high:
                f.write("## 🔴 High Severity\n\n")
                f.write("*These conflicts require immediate attention*\n\n")

                for conflict in high:
                    api_name = conflict.api_name if hasattr(conflict, 'api_name') else conflict.get('api_name', 'Unknown')
                    diff = conflict.difference if hasattr(conflict, 'difference') else conflict.get('difference', 'N/A')

                    f.write(f"### {api_name}\n\n")
                    f.write(f"**Issue**: {diff}\n\n")

            # List medium severity
            if medium:
                f.write("## 🟡 Medium Severity\n\n")

                for conflict in medium[:20]:  # Limit to 20
                    api_name = conflict.api_name if hasattr(conflict, 'api_name') else conflict.get('api_name', 'Unknown')
                    diff = conflict.difference if hasattr(conflict, 'difference') else conflict.get('difference', 'N/A')

                    f.write(f"### {api_name}\n\n")
                    f.write(f"{diff}\n\n")

        logger.info(f"Created conflicts report")


if __name__ == '__main__':
    # Test with mock data
    import sys

    if len(sys.argv) < 2:
        print("Usage: python unified_skill_builder.py <config.json>")
        sys.exit(1)

    config_path = sys.argv[1]

    with open(config_path, 'r') as f:
        config = json.load(f)

    # Mock scraped data
    scraped_data = {
        'github': {
            'data': {
                'readme': '# Test Repository',
                'issues': [],
                'releases': []
            }
        }
    }

    builder = UnifiedSkillBuilder(config, scraped_data)
    builder.build()

    print(f"\n✅ Test skill built in: output/{config['name']}/")
