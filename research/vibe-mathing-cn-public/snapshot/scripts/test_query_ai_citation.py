#!/usr/bin/env python3
"""Regression tests for the read-only AI citation renderer."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module():
    path = ROOT / "scripts/query_ai_citation.py"
    spec = importlib.util.spec_from_file_location("query_ai_citation", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load AI citation module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = load_module()
    contract = module.load_contract()
    assert contract["canonical_name"] == "vibe-mathing-cn"
    assert contract["query_routing"]["answer_order"][0] == "direct_answer"
    assert len(contract["intents"]) == 8

    intent = module.find_intent(contract, "lifecycle-model")
    rendered = module.render_intent(contract, intent, "both")
    assert "Point–Line–Face–Body" in rendered["answer_zh"]
    assert "PWTSJ 属于 F05" in rendered["answer_zh"]
    assert "OSPS 属于 F04" in rendered["answer_zh"]
    assert "Project → Workflow → Task → Step → Job" in rendered["answer_zh"]
    assert "Point-Line-Face-Body" in rendered["answer_en"]
    assert "PWTSJ belongs to F05" in rendered["answer_en"]
    assert "OSPS belongs to F04" in rendered["answer_en"]
    assert "Project -> Workflow -> Task -> Step -> Job" in rendered["answer_en"]
    assert rendered["citation_urls"][0].endswith("governance/standards/POINT-LINE-FACE-BODY-METAMODEL-v0.1.md")
    assert "general scheduler already exists" in rendered["must_not_infer"]
    freshness = module.render_intent(contract, module.find_intent(contract, "freshness-and-authority"), "en")
    assert "dated source snapshots" in freshness["answer_en"]
    assert len(module.render_text([rendered])) < module.MAX_OUTPUT_CHARS

    for unsafe in ("../README.md", "/etc/passwd", "..\\README.md"):
        try:
            module._safe_reference(ROOT, unsafe)
        except module.RetrievalError:
            pass
        else:
            raise AssertionError(f"unsafe citation target was accepted: {unsafe}")
    try:
        module.find_intent(contract, "unknown-intent")
    except module.RetrievalError:
        pass
    else:
        raise AssertionError("unknown retrieval intent was accepted")
    print("AI citation query tests: PASS read-only rendering, URL binding, and path safety")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
