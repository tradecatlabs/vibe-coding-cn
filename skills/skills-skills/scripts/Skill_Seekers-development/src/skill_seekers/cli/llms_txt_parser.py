"""ABOUTME: Parses llms.txt markdown content into structured page data"""
"""ABOUTME: Extracts titles, content, code samples, and headings from markdown"""

import re
from typing import List, Dict

class LlmsTxtParser:
    """Parse llms.txt markdown content into page structures"""

    def __init__(self, content: str):
        self.content = content

    def parse(self) -> List[Dict]:
        """
        Parse markdown content into page structures.

        Returns:
            List of page dicts with title, content, code_samples, headings
        """
        pages = []

        # Split by h1 headers (# Title)
        sections = re.split(r'\n# ', self.content)

        for section in sections:
            if not section.strip():
                continue

            # First line is title
            lines = section.split('\n')
            title = lines[0].strip('#').strip()

            # Parse content
            page = self._parse_section('\n'.join(lines[1:]), title)
            pages.append(page)

        return pages

    def _parse_section(self, content: str, title: str) -> Dict:
        """Parse a single section into page structure"""
        page = {
            'title': title,
            'content': '',
            'code_samples': [],
            'headings': [],
            'url': f'llms-txt#{title.lower().replace(" ", "-")}',
            'links': []
        }

        # Extract code blocks
        code_blocks = re.findall(r'```(\w+)?\n(.*?)```', content, re.DOTALL)
        for lang, code in code_blocks:
            page['code_samples'].append({
                'code': code.strip(),
                'language': lang or 'unknown'
            })

        # Extract h2/h3 headings
        headings = re.findall(r'^(#{2,3})\s+(.+)$', content, re.MULTILINE)
        for level_markers, text in headings:
            page['headings'].append({
                'level': f'h{len(level_markers)}',
                'text': text.strip(),
                'id': text.lower().replace(' ', '-')
            })

        # Remove code blocks from content for plain text
        content_no_code = re.sub(r'```.*?```', '', content, flags=re.DOTALL)

        # Extract paragraphs
        paragraphs = [p.strip() for p in content_no_code.split('\n\n') if len(p.strip()) > 20]
        page['content'] = '\n\n'.join(paragraphs)

        return page
