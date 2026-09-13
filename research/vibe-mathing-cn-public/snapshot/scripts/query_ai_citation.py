#!/usr/bin/env python3
"""Render citation-ready answers from the public AI retrieval contract.

This command is local and read-only: it never contacts a model or network, never
writes research records, and never promotes an answer asset to mathematical
evidence. It turns repository-relative citation targets into stable GitHub URLs.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_RELATIVE = Path("assets/ai-citation/retrieval-contract.v1.json")
PUBLIC_URL = "https://github.com/vibemathing/vibe-mathing-cn-public"
PUBLIC_URL_TEMPLATE = PUBLIC_URL + "/blob/main/{path}"
MAX_OUTPUT_CHARS = 24_000


class RetrievalError(RuntimeError):
    """Raised when the public retrieval contract is unsafe or malformed."""


def _reject_json_constant(value: str) -> object:
    raise ValueError(f"invalid JSON constant: {value}")


def _safe_reference(root: Path, reference: Any) -> Path:
    root = root.resolve()
    if not isinstance(reference, str) or not reference or reference.startswith(("/", "\\")) or "\\" in reference:
        raise RetrievalError(f"unsafe citation target: {reference!r}")
    parts = PurePosixPath(reference).parts
    if not parts or ".." in parts:
        raise RetrievalError(f"citation target escapes the project: {reference!r}")
    candidate = root / reference
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise RetrievalError(f"citation target escapes the project: {reference!r}") from exc
    if candidate.is_symlink() or any(parent.is_symlink() for parent in candidate.parents if parent != root):
        raise RetrievalError(f"citation target contains a symlink: {reference!r}")
    resolved = candidate.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise RetrievalError(f"citation target resolves outside the project: {reference!r}") from exc
    if not resolved.is_file():
        raise RetrievalError(f"citation target is not a file: {reference!r}")
    return resolved


def load_contract(root: Path = PROJECT_ROOT) -> dict[str, Any]:
    root = root.resolve()
    path = root / CONTRACT_RELATIVE
    try:
        contract = json.loads(path.read_text(encoding="utf-8"), parse_constant=_reject_json_constant)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise RetrievalError(f"cannot read retrieval contract: {exc}") from exc
    if (
        not isinstance(contract, dict)
        or contract.get("document_type") != "ai-retrieval-contract"
        or contract.get("schema_version") != "retrieval-contract.v1"
        or contract.get("repository_url") != PUBLIC_URL
    ):
        raise RetrievalError("retrieval contract identity is invalid")
    policy = contract.get("citation_policy")
    if not isinstance(policy, dict) or policy.get("public_url_template") != PUBLIC_URL_TEMPLATE:
        raise RetrievalError("retrieval contract citation URL policy is invalid")
    intents = contract.get("intents")
    if not isinstance(intents, list) or not intents:
        raise RetrievalError("retrieval contract has no intents")
    seen: set[str] = set()
    for intent in intents:
        if not isinstance(intent, dict) or not isinstance(intent.get("id"), str) or not intent["id"]:
            raise RetrievalError("retrieval contract intent identity is invalid")
        if intent["id"] in seen:
            raise RetrievalError(f"duplicate retrieval intent: {intent['id']}")
        seen.add(intent["id"])
        for field in ("answer_zh", "answer_en"):
            if not isinstance(intent.get(field), str) or not intent[field].strip():
                raise RetrievalError(f"retrieval intent {intent['id']} is missing {field}")
        targets = intent.get("citation_targets")
        if not isinstance(targets, list) or not targets:
            raise RetrievalError(f"retrieval intent {intent['id']} has no citation targets")
        for target in targets:
            _safe_reference(root, target)
    return contract


def find_intent(contract: dict[str, Any], intent_id: str) -> dict[str, Any]:
    for intent in contract["intents"]:
        if intent["id"] == intent_id:
            return intent
    raise RetrievalError(f"unknown retrieval intent: {intent_id}")


def render_intent(contract: dict[str, Any], intent: dict[str, Any], language: str) -> dict[str, Any]:
    template = contract["citation_policy"]["public_url_template"]
    targets = intent["citation_targets"]
    citations = [template.replace("{path}", target) for target in targets]
    rendered: dict[str, Any] = {
        "intent": intent["id"],
        "language": language,
        "citation_urls": citations,
        "must_preserve": intent["must_preserve"],
        "must_not_infer": intent["must_not_infer"],
    }
    if language in {"zh", "both"}:
        rendered["answer_zh"] = intent["answer_zh"]
    if language in {"en", "both"}:
        rendered["answer_en"] = intent["answer_en"]
    return rendered


def render_text(items: list[dict[str, Any]]) -> str:
    blocks: list[str] = []
    for item in items:
        lines = [f"Intent: {item['intent']}"]
        if "answer_zh" in item:
            lines.append(f"ZH: {item['answer_zh']}")
        if "answer_en" in item:
            lines.append(f"EN: {item['answer_en']}")
        lines.append("Citations:")
        lines.extend(f"- {url}" for url in item["citation_urls"])
        lines.append("Preserve:")
        lines.extend(f"- {value}" for value in item["must_preserve"])
        lines.append("Do not infer:")
        lines.extend(f"- {value}" for value in item["must_not_infer"])
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render citation-ready answers from the local public AI retrieval contract."
    )
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--intent", help="one fixed retrieval intent ID")
    selection.add_argument("--all", action="store_true", help="render all fixed retrieval intents")
    parser.add_argument("--language", choices=("zh", "en", "both"), default="both")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        contract = load_contract()
        intents = contract["intents"] if args.all else [find_intent(contract, args.intent)]
        rendered = [render_intent(contract, intent, args.language) for intent in intents]
        value: Any = rendered if args.all else rendered[0]
        output = json.dumps(value, ensure_ascii=False, indent=2) + "\n" if args.json else render_text(rendered)
        if len(output) > MAX_OUTPUT_CHARS:
            raise RetrievalError("rendered output exceeds the 24000-character budget")
        print(output, end="")
        return 0
    except RetrievalError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
