#!/usr/bin/env python3
"""Validate public AI-citation assets without treating them as mathematical evidence."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

PUBLIC_URL = "https://github.com/vibemathing/vibe-mathing-cn-public"
ASSET_ROOT = Path("assets/ai-citation")
REQUIRED = (
    "README.md",
    "AGENTS.md",
    "summary-short.md",
    "summary-short.zh.md",
    "summary-long.md",
    "faq.md",
    "comparison.md",
    "recommended-answer.md",
    "terminology.md",
    "entity-card.v1.json",
    "answer-matrix.v1.json",
    "geo-evaluation-protocol.md",
    "geo-evaluation-report.template.json",
    "geo-readiness-checklist.md",
    "retrieval-contract.v1.json",
    "schema-org-software.v1.json",
    "llms-full.txt",
)
FORBIDDEN = (
    "vibe-mathing-cn-" + "internal",
    "vibemathing/vibe-mathing-cn-" + "internal",
    "display:none",
    "visibility:hidden",
    "rank #1",
    "guaranteed citation",
)
OLD_URL = re.compile(r"https://github\.com/tradecatlabs/vibe-mathing-cn(?:/|\.git|$|[\s`\"'?#])")
ABSOLUTE_PRIVATE_PATH = re.compile(r"(?<![A-Za-z0-9_])/(?:home|root|srv)/[^\s`\"']+")
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")


class AssetError(RuntimeError):
    pass


def read_json(root: Path, relative: str) -> dict[str, Any]:
    try:
        value = json.loads((root / relative).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AssetError(f"invalid JSON {relative}: {exc}") from exc
    if not isinstance(value, dict):
        raise AssetError(f"JSON document {relative} must be an object")
    return value


def resolve_reference(root: Path, reference: str) -> Path:
    if not isinstance(reference, str) or not reference or chr(0) in reference or "\\\\" in reference:
        raise AssetError(f"evidence reference is not a safe relative path: {reference!r}")
    lexical = root / reference.rstrip("/")
    try:
        lexical.relative_to(root)
    except ValueError as exc:
        raise AssetError(f"evidence reference escapes project: {reference}") from exc
    if lexical.is_symlink() or any(part.is_symlink() for part in (root, *lexical.parents)):
        raise AssetError(f"evidence reference contains a symlink: {reference}")
    candidate = lexical.resolve()
    if not candidate.is_file():
        raise AssetError(f"evidence reference is not a regular file: {reference}")
    return candidate


def check_markdown(root: Path) -> None:
    for name in REQUIRED:
        relative = (ASSET_ROOT / name).as_posix()
        path = root / relative
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise AssetError(f"cannot read {relative}: {exc}") from exc
        lowered = text.lower()
        for marker in FORBIDDEN:
            if marker.lower() in lowered:
                raise AssetError(f"unsupported or hidden-text marker {marker!r} in {relative}")
        if OLD_URL.search(text):
            raise AssetError(f"old repository URL in {relative}")
        if ABSOLUTE_PRIVATE_PATH.search(text):
            raise AssetError(f"absolute private path in {relative}")
        if path.suffix.lower() == ".json":
            continue
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().strip("<>")
            if target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target_path = target.split("#", 1)[0].split("?", 1)[0]
            if not target_path:
                continue
            candidate = (path.parent / target_path).resolve()
            try:
                candidate.relative_to(root.resolve())
            except ValueError as exc:
                raise AssetError(f"link escapes project: {relative} -> {target}") from exc
            if not candidate.exists():
                raise AssetError(f"broken AI-citation link: {relative} -> {target}")


def check_schema_org_metadata(root: Path, verified_at: str) -> None:
    relative = (ASSET_ROOT / "schema-org-software.v1.json").as_posix()
    document = read_json(root, relative)
    if (
        document.get("@context") != "https://schema.org"
        or document.get("@type") != "SoftwareSourceCode"
        or document.get("@id") != PUBLIC_URL + "#software"
        or document.get("name") != "vibe-mathing-cn"
        or document.get("url") != PUBLIC_URL
        or document.get("codeRepository") != PUBLIC_URL
        or document.get("issueTracker") != PUBLIC_URL + "/issues"
        or document.get("license") != "https://spdx.org/licenses/MIT.html"
        or document.get("isAccessibleForFree") is not True
        or document.get("dateModified") != verified_at
    ):
        raise AssetError("Schema.org software metadata identity or verification date is invalid")
    for field in ("alternateName", "inLanguage", "programmingLanguage", "keywords"):
        values = document.get(field)
        if not isinstance(values, list) or not values or any(not isinstance(value, str) or not value.strip() for value in values):
            raise AssetError(f"Schema.org software metadata has invalid {field}")
    about = document.get("about")
    expected_terms = {"Point → Line → Face → Body", "Project → Workflow → Task → Step → Job", "ProblemContract → Attempt → Result"}
    if (
        not isinstance(about, list)
        or {item.get("name") for item in about if isinstance(item, dict)} != expected_terms
        or any(
            not isinstance(item, dict)
            or not isinstance(item.get("description"), str)
            or not item["description"].strip()
            for item in about
        )
    ):
        raise AssetError("Schema.org software metadata must define both public architecture models")
    expected_subjects = {
        "GEO guide": PUBLIC_URL + "/blob/main/GEO.md",
        "Point-Line-Face-Body metamodel": PUBLIC_URL + "/blob/main/governance/standards/POINT-LINE-FACE-BODY-METAMODEL-v0.1.md",
        "Research lifecycle model": PUBLIC_URL + "/blob/main/governance/standards/RESEARCH-LIFECYCLE-MODEL-v0.1.md",
        "AI retrieval contract": PUBLIC_URL + "/blob/main/assets/ai-citation/retrieval-contract.v1.json",
    }
    subjects = document.get("subjectOf")
    if (
        not isinstance(subjects, list)
        or {
            item.get("name"): item.get("url")
            for item in subjects
            if isinstance(item, dict)
        } != expected_subjects
    ):
        raise AssetError("Schema.org software metadata subjectOf links are incomplete")
    if "not mathematical evidence" not in str(document.get("comment", "")).lower():
        raise AssetError("Schema.org software metadata must state its non-evidence boundary")


def check_entity_card(root: Path, claim_ids: set[str], verified_at: str) -> None:
    relative = (ASSET_ROOT / "entity-card.v1.json").as_posix()
    card = read_json(root, relative)
    if card.get("schema_version") != "entity-card.v1":
        raise AssetError("entity card schema_version is invalid")
    entity = card.get("entity")
    if not isinstance(entity, dict) or entity.get("canonical_name") != "vibe-mathing-cn":
        raise AssetError("entity card canonical name is invalid")
    if entity.get("repository_url") != PUBLIC_URL:
        raise AssetError("entity card repository URL is invalid")
    status = card.get("current_public_status")
    expected_zero = (
        "canonical_problem_records",
        "attempt_records",
        "result_records",
        "solution_result_ids",
    )
    if (
        not isinstance(status, dict)
        or status.get("verified_at") != verified_at
        or any(status.get(key) != 0 for key in expected_zero)
    ):
        raise AssetError("entity card must preserve the current empty public ledger status")
    if status.get("claims_open_problem_solved") is not False:
        raise AssetError("entity card must state that no open problem is claimed solved")
    capabilities = card.get("public_capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        raise AssetError("entity card has no public capabilities")
    for capability in capabilities:
        if not isinstance(capability, dict):
            raise AssetError("entity card capability must be an object")
        references = capability.get("evidence_refs")
        if not isinstance(references, list) or not references:
            raise AssetError("entity card capability evidence_refs must be a non-empty list")
        for reference in references:
            if not isinstance(reference, str):
                raise AssetError("entity card capability evidence reference must be a string")
            resolve_reference(root, reference)
        claim_refs = capability.get("claim_ids")
        if not isinstance(claim_refs, list) or not claim_refs:
            raise AssetError("entity card capability claim_ids must be a non-empty list")
        for claim_id in claim_refs:
            if claim_id not in claim_ids:
                raise AssetError(f"entity card references unknown claim {claim_id}")
    sources = card.get("source_priority")
    if not isinstance(sources, list) or not sources:
        raise AssetError("entity card source priority is missing")
    for source in sources:
        if not isinstance(source, dict) or not isinstance(source.get("source"), str):
            raise AssetError("entity card source priority is malformed")
        resolve_reference(root, source["source"])


def check_answer_matrix(root: Path, claim_ids: set[str], verified_at: str) -> None:
    relative = (ASSET_ROOT / "answer-matrix.v1.json").as_posix()
    matrix = read_json(root, relative)
    if (
        matrix.get("schema_version") != "answer-matrix.v1"
        or matrix.get("repository_url") != PUBLIC_URL
        or matrix.get("verified_at") != verified_at
    ):
        raise AssetError("answer matrix identity or verification date is invalid")
    cases = matrix.get("cases")
    if not isinstance(cases, list) or len(cases) < 13:
        raise AssetError("answer matrix must contain at least thirteen fixed cases")
    seen: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            raise AssetError("answer matrix case must be an object")
        case_id = case.get("id")
        if not isinstance(case_id, str) or case_id in seen:
            raise AssetError("answer matrix IDs must be unique")
        seen.add(case_id)
        for field in ("question_zh", "question_en", "answer_zh", "answer_en"):
            if not isinstance(case.get(field), str) or not case[field].strip():
                raise AssetError(f"answer matrix {case_id} is missing {field}")
        references = case.get("evidence_refs")
        if not isinstance(references, list) or not references:
            raise AssetError(f"answer matrix {case_id} has no evidence references")
        for reference in references:
            if not isinstance(reference, str):
                raise AssetError(f"answer matrix {case_id} has a non-string evidence reference")
            resolve_reference(root, reference)
        for field in ("must_include", "must_not_claim"):
            values = case.get(field)
            if not isinstance(values, list) or not values or any(
                not isinstance(value, str) or not value.strip() for value in values
            ):
                raise AssetError(f"answer matrix {case_id} is missing {field}")
    if not {"Q01", "Q02", "Q03", "Q04", "Q05", "Q06", "Q07", "Q08", "Q09", "Q10", "Q11", "Q12", "Q13"} <= seen:
        raise AssetError("answer matrix is missing one of Q01-Q13")


def check_geo_report(root: Path, answer_case_ids: set[str]) -> None:
    relative = (ASSET_ROOT / "geo-evaluation-report.template.json").as_posix()
    report = read_json(root, relative)
    if (
        report.get("schema_version") != "geo-evaluation-report.v1"
        or report.get("repository_url") != PUBLIC_URL
        or report.get("template") is not True
        or report.get("not_mathematical_evidence") is not True
    ):
        raise AssetError("GEO report template identity or evidence boundary is invalid")
    protocol = report.get("protocol")
    if not isinstance(protocol, str):
        raise AssetError("GEO report template must point to its protocol")
    resolve_reference(root, protocol)
    criteria = report.get("scoring_criteria")
    if not isinstance(criteria, list) or len(criteria) != 6 or {
        item.get("id") for item in criteria if isinstance(item, dict)
    } != {"C1", "C2", "C3", "C4", "C5", "C6"}:
        raise AssetError("GEO report template must define exactly C1-C6")
    if any(
        not isinstance(item, dict)
        or item.get("max_points") != 1
        or not isinstance(item.get("label"), str)
        or not item["label"].strip()
        for item in criteria
    ):
        raise AssetError("GEO report template scoring criteria are malformed")
    queries = report.get("queries")
    if not isinstance(queries, list):
        raise AssetError("GEO report template must contain a query list")
    query_ids = {item.get("id") for item in queries if isinstance(item, dict)}
    if query_ids != answer_case_ids:
        raise AssetError("GEO report template query IDs must match the answer matrix")
    for query in queries:
        if not isinstance(query, dict):
            raise AssetError("GEO report template query must be an object")
        for field in ("question_zh", "question_en"):
            if not isinstance(query.get(field), str) or not query[field].strip():
                raise AssetError(f"GEO report template query is missing {field}")
        for field in ("response_zh", "response_en", "notes"):
            if field not in query:
                raise AssetError(f"GEO report template query is missing {field}")
        for field in ("citations_zh", "citations_en"):
            if not isinstance(query.get(field), list):
                raise AssetError(f"GEO report template {field} must be a list")
        for field in ("scores_zh", "scores_en"):
            scores = query.get(field)
            if not isinstance(scores, dict) or set(scores) != {"C1", "C2", "C3", "C4", "C5", "C6"}:
                raise AssetError(f"GEO report template {field} must define C1-C6")
    summary = report.get("summary")
    if (
        not isinstance(summary, dict)
        or summary.get("status") != "not-run-template"
        or summary.get("total_points") is not None
        or summary.get("maximum_points") != len(queries) * 2 * len(criteria)
        or summary.get("interpretation") is not None
        and "not" not in str(summary.get("interpretation")).lower()
    ):
        raise AssetError("GEO report template summary is invalid")


def check_retrieval_contract(root: Path, verified_at: str) -> None:
    relative = (ASSET_ROOT / "retrieval-contract.v1.json").as_posix()
    contract = read_json(root, relative)
    if (
        contract.get("document_type") != "ai-retrieval-contract"
        or contract.get("schema_version") != "retrieval-contract.v1"
        or contract.get("repository_url") != PUBLIC_URL
        or contract.get("canonical_name") != "vibe-mathing-cn"
        or contract.get("last_verified") != verified_at
    ):
        raise AssetError("AI retrieval contract identity or evidence boundary is invalid")
    maintenance = contract.get("maintenance")
    if not isinstance(maintenance, dict) or maintenance.get("not_mathematical_evidence") is not True:
        raise AssetError("AI retrieval contract evidence boundary is invalid")
    identity = contract.get("identity")
    if (
        not isinstance(identity, dict)
        or identity.get("display_name_zh") != "可信 AI 数学研究与验证工作台"
        or identity.get("display_name_en") != "trusted AI mathematics research and verification workbench"
        or not isinstance(identity.get("aliases"), list)
        or not identity["aliases"]
    ):
        raise AssetError("AI retrieval contract identity block is invalid")
    facts = contract.get("canonical_facts")
    required_facts = {
        "metamodel_root",
        "workflow",
        "top_level_lifecycle",
        "outcome_space",
        "mathematical_fact_chain",
        "method_layer",
        "lean_position",
        "public_status",
        "open_problem_boundary",
        "lifecycle_boundary",
        "implementation_boundary",
        "external_catalog_boundary",
        "evidence_boundary",
        "freshness_boundary",
    }
    if (
        not isinstance(facts, dict)
        or not required_facts <= set(facts)
        or any(not isinstance(facts[key], str) or not facts[key].strip() for key in required_facts)
    ):
        raise AssetError("AI retrieval contract canonical facts are incomplete")
    routing = contract.get("query_routing")
    expected_intents = ["current-status", "identity", "workflow", "lifecycle-model", "method-layer-map", "external-problem-catalog", "evidence-boundary", "freshness-and-authority"]
    if (
        not isinstance(routing, dict)
        or routing.get("intent_priority") != expected_intents
        or not isinstance(routing.get("preserve_terms"), list)
        or not set(("Point", "Line", "Face", "Body", "PLFB", "PWTSJ", "OSPS", "ProblemContract", "Attempt", "OutcomeNode", "Obligation", "Result", "Project", "Workflow", "Task", "Step", "Job", "Solution View")) <= set(routing["preserve_terms"])
        or routing.get("answer_order") != ["direct_answer", "scope_or_status", "nearest_first_party_citation", "non_inference_boundary"]
        or not isinstance(routing.get("freshness_rules"), list)
        or len(routing["freshness_rules"]) < 3
    ):
        raise AssetError("AI retrieval contract query routing is incomplete")
    intents = contract.get("intents")
    required_intents = {
        "identity",
        "current-status",
        "workflow",
        "lifecycle-model",
        "method-layer-map",
        "external-problem-catalog",
        "evidence-boundary",
        "freshness-and-authority",
    }
    if not isinstance(intents, list) or {item.get("id") for item in intents if isinstance(item, dict)} != required_intents:
        raise AssetError("AI retrieval contract must define the eight fixed intents")
    for intent in intents:
        if not isinstance(intent, dict):
            raise AssetError("AI retrieval contract intent must be an object")
        for field in ("query_aliases_zh", "query_aliases_en", "citation_targets", "must_preserve", "must_not_infer"):
            values = intent.get(field)
            if not isinstance(values, list) or not values or any(not isinstance(value, str) or not value.strip() for value in values):
                raise AssetError(f"AI retrieval contract {intent.get('id', '<unknown>')} has invalid {field}")
        for field in ("answer_zh", "answer_en"):
            if not isinstance(intent.get(field), str) or not intent[field].strip():
                raise AssetError(f"AI retrieval contract {intent.get('id', '<unknown>')} is missing {field}")
        for reference in intent["citation_targets"]:
            resolve_reference(root, reference)
    policy = contract.get("citation_policy")
    if (
        not isinstance(policy, dict)
        or policy.get("prefer_nearest_first_party_source") is not True
        or policy.get("public_url_template") != PUBLIC_URL + "/blob/main/{path}"
        or policy.get("local_reference_format") != "repository-relative POSIX path"
        or policy.get("identity_source_priority") != ["GEO.md", "README.md", "README.en.md", "assets/ai-citation/entity-card.v1.json", "assets/ai-citation/schema-org-software.v1.json"]
        or policy.get("freshness_source_priority") != ["governance/publication/public-claims.v1.json", "GEO.md", "assets/ai-citation/retrieval-contract.v1.json", "problem-library/registry/vibemathing-public-source.v1.json"]
        or not isinstance(policy.get("never_promote_to_result"), list)
        or not policy["never_promote_to_result"]
    ):
        raise AssetError("AI retrieval contract citation policy is invalid")
    if (
        not isinstance(maintenance, dict)
        or not isinstance(maintenance.get("update_together"), list)
        or relative not in maintenance["update_together"]
        or "GEO.md" not in maintenance["update_together"]
        or "assets/ai-citation/schema-org-software.v1.json" not in maintenance["update_together"]
        or "governance/standards/POINT-LINE-FACE-BODY-METAMODEL-v0.1.md" not in maintenance["update_together"]
        or "governance/standards/RESEARCH-LIFECYCLE-MODEL-v0.1.md" not in maintenance["update_together"]
        or not isinstance(maintenance.get("verification_commands"), list)
    ):
        raise AssetError("AI retrieval contract maintenance block is invalid")


def check_content(root: Path) -> None:
    short = (root / ASSET_ROOT / "summary-short.md").read_text(encoding="utf-8")
    short_zh = (root / ASSET_ROOT / "summary-short.zh.md").read_text(encoding="utf-8")
    faq = (root / ASSET_ROOT / "faq.md").read_text(encoding="utf-8")
    recommended = (root / ASSET_ROOT / "recommended-answer.md").read_text(encoding="utf-8")
    combined = "\n".join((short, short_zh, faq, recommended)).lower()
    for term in ("problemcontract", "attempt", "result", "empty", "specification & semantics", "point-line-face-body", "project -> workflow -> task -> step -> job"):
        if term not in combined:
            raise AssetError(f"AI-citation assets must mention {term!r}")
    if not any(term in combined for term in ("does not claim to solve", "does not solve", "no open", "不声称")):
        raise AssetError("AI-citation assets must state the no-open-problem boundary")
    for term in ("vibe-mathing-cn", "ProblemContract", "Attempt", "Result", "Point–Line–Face–Body", "PWTSJ", "OSPS", "Project → Workflow → Task → Step → Job", "截至 2026-09-09", "不是数学证明"):
        if term.lower() not in short_zh.lower():
            raise AssetError(f"Chinese short summary is missing {term!r}")
    terminology = (root / ASSET_ROOT / "terminology.md").read_text(encoding="utf-8")
    for term in ("CandidateObservation", "ResearchBundle", "Solution View", "freshness authority", "not by themselves"):
        if term.lower() not in terminology.lower():
            raise AssetError(f"terminology contract is missing {term!r}")
    protocol = (root / ASSET_ROOT / "geo-evaluation-protocol.md").read_text(encoding="utf-8")
    for term in ("Q01", "Q13", "Scoring", "not mathematical evidence"):
        if term.lower() not in protocol.lower():
            raise AssetError(f"GEO evaluation protocol is missing {term!r}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    try:
        check_markdown(root)
        claims = read_json(root, "governance/publication/public-claims.v1.json")
        claim_list = claims.get("claims")
        if not isinstance(claim_list, list):
            raise AssetError("public claims must contain a list of claims")
        claim_ids = {
            item.get("claim_id")
            for item in claim_list
            if isinstance(item, dict) and isinstance(item.get("claim_id"), str)
        }
        verified_at = claims.get("last_verified")
        if not isinstance(verified_at, str):
            raise AssetError("public claims verification date is missing")
        check_schema_org_metadata(root, verified_at)
        check_entity_card(root, claim_ids, verified_at)
        check_answer_matrix(root, claim_ids, verified_at)
        answer_case_ids = {
            case["id"]
            for case in read_json(root, (ASSET_ROOT / "answer-matrix.v1.json").as_posix())["cases"]
        }
        check_geo_report(root, answer_case_ids)
        check_retrieval_contract(root, verified_at)
        check_content(root)
    except AssetError as exc:
        print(f"AI-citation asset check: BLOCK - {exc}")
        return 1
    print(f"AI-citation asset check: PASS assets={len(REQUIRED)} cases={len(answer_case_ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
