"""Helpers for reading the repository taxonomy file.

The project intentionally keeps metadata in a small YAML subset so the quality
gate scripts can run without extra Python dependencies.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TAXONOMY = ROOT / "metadata/taxonomy.yml"


def strip_quotes(value: str) -> str:
    """Remove simple surrounding quotes from a taxonomy scalar."""
    return value.strip().strip("\"'")


def taxonomy_sections() -> dict[str, dict[str, str]]:
    """Return top-level taxonomy sections keyed by section id."""
    sections: dict[str, dict[str, str]] = {}
    current: str | None = None
    in_sections = False

    for line in TAXONOMY.read_text(encoding="utf-8").splitlines():
        if line == "sections:":
            in_sections = True
            continue
        if in_sections and line and not line.startswith(" "):
            break
        if not in_sections:
            continue

        section_match = re.match(r"^  ([A-Za-z0-9_-]+):\s*$", line)
        if section_match:
            current = section_match.group(1)
            sections[current] = {}
            continue
        field_match = re.match(r"^    (path|entry|agent_guide):\s*(.+?)\s*$", line)
        if current and field_match:
            sections[current][field_match.group(1)] = strip_quotes(field_match.group(2))

    return sections


def taxonomy_document_paths() -> list[str]:
    """Return document path entries from metadata/taxonomy.yml."""
    paths: list[str] = []
    in_documents = False

    for line in TAXONOMY.read_text(encoding="utf-8").splitlines():
        if line == "documents:":
            in_documents = True
            continue
        if in_documents and line and not line.startswith(" "):
            break
        if not in_documents:
            continue

        stripped = line.strip()
        if stripped.startswith("- path:"):
            _, value = stripped.split(":", 1)
            paths.append(strip_quotes(value))

    return paths


def doc_readmes_from_taxonomy() -> dict[Path, list[str]]:
    """Return docs README files and required main anchors from taxonomy."""
    readmes: dict[Path, list[str]] = {}

    for target in taxonomy_document_paths():
        path_part, _, anchor = target.partition("#")
        if not anchor or not path_part.startswith("docs/") or not path_part.endswith("/README.md"):
            continue
        readmes.setdefault(Path(path_part), []).append(anchor)

    return readmes
