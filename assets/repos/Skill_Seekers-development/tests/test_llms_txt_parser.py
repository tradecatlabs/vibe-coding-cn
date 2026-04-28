import pytest
from skill_seekers.cli.llms_txt_parser import LlmsTxtParser

def test_parse_markdown_sections():
    """Test parsing markdown into page sections"""
    sample_content = """# Getting Started

Welcome to the docs.

## Installation

Run: npm install

## Usage

Import the library:

```javascript
import { app } from 'framework'
```

# API Reference

Main API documentation here.
"""

    parser = LlmsTxtParser(sample_content)
    pages = parser.parse()

    assert len(pages) >= 2
    assert pages[0]['title'] == 'Getting Started'
    assert pages[1]['title'] == 'API Reference'
    assert len(pages[0]['code_samples']) == 1
    assert pages[0]['code_samples'][0]['language'] == 'javascript'
