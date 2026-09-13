#!/usr/bin/env python3
"""Validate public README, metadata, discovery links, claims, and empty-status truth."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

PUBLIC_URL = "https://github.com/vibemathing/vibe-mathing-cn-public"
PUBLIC_PROJECT_URL = "https://github.com/users/vibemathing/projects/1"
PUBLIC_BOUNTY_VIEW_URL = "https://github.com/users/vibemathing/projects/2/views/3"
BOUNTY_TOP146_PATH = "problem-library/BOUNTY_PROJECT_2_TOP146.md"
BOUNTY_TOP146_JSON_PATH = "problem-library/registry/bounty-project-2-top146.v1.json"
KEY_PROBLEM_REPOSITORIES = {
    "vibemathing/problem-millennium-riemann-hypothesis": "open-millennium-problem",
    "vibemathing/problem-millennium-p-vs-np": "open-millennium-problem",
    "vibemathing/problem-millennium-navier-stokes": "open-millennium-problem",
    "vibemathing/problem-millennium-yang-mills-mass-gap": "open-millennium-problem",
    "vibemathing/problem-millennium-hodge-conjecture": "open-millennium-problem",
    "vibemathing/problem-millennium-birch-swinnerton-dyer": "open-millennium-problem",
    "vibemathing/problem-secp256k1-ecdlog-polytime": "independent-key-problem",
}
REQUIRED_FILES = (
    "README.md",
    "README.en.md",
    "GEO.md",
    "llms.txt",
    "CITATION.cff",
    "codemeta.json",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "assets/README.md",
    "assets/architecture.svg",
    "assets/AGENTS.md",
    "assets/ai-citation/README.md",
    "assets/ai-citation/AGENTS.md",
    "assets/ai-citation/summary-short.md",
    "assets/ai-citation/summary-short.zh.md",
    "assets/ai-citation/summary-long.md",
    "assets/ai-citation/faq.md",
    "assets/ai-citation/comparison.md",
    "assets/ai-citation/recommended-answer.md",
    "assets/ai-citation/terminology.md",
    "assets/ai-citation/entity-card.v1.json",
    "assets/ai-citation/answer-matrix.v1.json",
    "assets/ai-citation/geo-evaluation-protocol.md",
    "assets/ai-citation/geo-evaluation-report.template.json",
    "assets/ai-citation/geo-readiness-checklist.md",
    "assets/ai-citation/schema-org-software.v1.json",
    "assets/ai-citation/llms-full.txt",
    "governance/publication/README.md",
    "governance/publication/AGENTS.md",
    "governance/publication/public-claims.v1.json",
    "governance/control-plane/plfb-metamodel.schema.json",
    "governance/control-plane/plfb-metamodel.v0.1.json",
    "governance/standards/POINT-LINE-FACE-BODY-METAMODEL-v0.1.md",
    "governance/standards/FORMAL-METHODS-MAP.md",
    "governance/standards/RESEARCH-LIFECYCLE-MODEL-v0.1.md",
    "problem-library/VIBEMATHING_PUBLIC_INDEX.md",
    "problem-library/BOUNTY_PROJECT_2_TOP146.md",
    "problem-library/registry/bounty-project-2-top146.v1.json",
    "problem-library/registry/vibemathing-public-source.v1.json",
    "problem-library/templates/README.md",
    "problem-library/templates/AGENTS.md",
    "problem-library/templates/problem-contract.template.json",
    "scripts/query_vibemathing_public.py",
    "scripts/query_ai_citation.py",
    "scripts/test_query_ai_citation.py",
    "scripts/audit_public_status.py",
    "scripts/test_audit_public_status.py",
    "scripts/validate_plfb_metamodel.py",
    "scripts/test_validate_plfb_metamodel.py",
)
SURFACE_FILES = (
    "README.md",
    "README.en.md",
    "GEO.md",
    "llms.txt",
    "assets/README.md",
    "assets/ai-citation/README.md",
    "assets/ai-citation/summary-short.md",
    "assets/ai-citation/summary-short.zh.md",
    "assets/ai-citation/summary-long.md",
    "assets/ai-citation/faq.md",
    "assets/ai-citation/comparison.md",
    "assets/ai-citation/recommended-answer.md",
    "assets/ai-citation/terminology.md",
    "assets/ai-citation/geo-evaluation-protocol.md",
    "assets/ai-citation/geo-readiness-checklist.md",
    "assets/ai-citation/llms-full.txt",
    "problem-library/VIBEMATHING_PUBLIC_INDEX.md",
    "problem-library/BOUNTY_PROJECT_2_TOP146.md",
)
REQUIRED_README_TERMS = (
    "ProblemContract",
    "Attempt",
    "Result",
    "ResearchBundle",
    "solutions.json",
    "open",
    "VIBEMATHING_PUBLIC_INDEX.md",
    "vibe-mathing-problem-library-public",
    "vibe-mathing-problem-public-template",
    "WEB_BOOTSTRAP",
    "POINT-LINE-FACE-BODY-METAMODEL-v0.1.md",
    "FORMAL-METHODS-MAP.md",
    "RESEARCH-LIFECYCLE-MODEL-v0.1.md",
    "Point–Line–Face–Body",
    "PWTSJ",
    "OSPS",
    "Project → Workflow → Task → Step → Job",
    "规格与语义",
    "Lean",
    "GEO.md",
)
REQUIRED_EN_TERMS = (
    "ProblemContract",
    "Attempt",
    "Result",
    "ResearchBundle",
    "solutions.json",
    "open mathematics problem",
    "VIBEMATHING_PUBLIC_INDEX.md",
    "vibe-mathing-problem-library-public",
    "vibe-mathing-problem-public-template",
    "WEB_BOOTSTRAP",
    "POINT-LINE-FACE-BODY-METAMODEL-v0.1.md",
    "FORMAL-METHODS-MAP.md",
    "RESEARCH-LIFECYCLE-MODEL-v0.1.md",
    "Point–Line–Face–Body",
    "PWTSJ",
    "OSPS",
    "Project → Workflow → Task → Step → Job",
    "Specification & Semantics",
    "Lean",
    "GEO.md",
)
FORBIDDEN_PUBLIC_IDENTIFIERS = (
    "vibe-mathing-cn-" + "internal",
    "vibemathing/vibe-mathing-cn-" + "internal",
    "\\\\wsl" + ".localhost",
)
PRIVATE_PATH_RE = re.compile(r"(?<![A-Za-z0-9_])/(?:home|root|srv)/[^\s`\"']+")
OLD_PUBLIC_URL_RE = re.compile(
    r"https://github\.com/tradecatlabs/vibe-mathing-cn(?:/|\.git|$|[\s`\"'?#])"
)
SECRET_ASSIGNMENT_RE = re.compile(
    r"(?i)\b(?:api[_-]?key|access[_-]?token|refresh[_-]?token|password|secret)\b\s*[:=]\s*[^\s`\"']+"
)
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)


class CheckError(RuntimeError):
    pass


def read_text(root: Path, relative: str) -> str:
    try:
        return (root / relative).read_text(encoding="utf-8")
    except OSError as exc:
        raise CheckError(f"cannot read {relative}: {exc}") from exc


def check_required_files(root: Path) -> None:
    missing = [relative for relative in REQUIRED_FILES if not (root / relative).is_file()]
    if missing:
        raise CheckError("missing public discovery files: " + ", ".join(missing))


def check_metadata(root: Path) -> None:
    cff = read_text(root, "CITATION.cff")
    for term in (
        "cff-version:",
        "title:",
        "type: software",
        "authors:",
        "license: MIT",
        f'repository-code: "{PUBLIC_URL}"',
    ):
        if term not in cff:
            raise CheckError(f"CITATION.cff is missing {term!r}")
    try:
        codemeta = json.loads(read_text(root, "codemeta.json"))
    except json.JSONDecodeError as exc:
        raise CheckError(f"codemeta.json is invalid: {exc}") from exc
    if codemeta.get("name") != "vibe-mathing-cn" or codemeta.get("url") != PUBLIC_URL:
        raise CheckError("codemeta identity must identify the public project")
    if codemeta.get("codeRepository") != PUBLIC_URL:
        raise CheckError("codemeta.codeRepository must identify the public repository")
    if codemeta.get("issueTracker") != PUBLIC_URL + "/issues":
        raise CheckError("codemeta.issueTracker must identify the public repository")
    if codemeta.get("license") != "https://spdx.org/licenses/MIT.html":
        raise CheckError("codemeta.license must identify MIT")


def check_architecture_asset(root: Path) -> None:
    path = root / "assets/architecture.svg"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise CheckError(f"cannot read assets/architecture.svg: {exc}") from exc
    required_markers = (
        "<svg",
        'xmlns="http://www.w3.org/2000/svg"',
        'role="img"',
        "<title",
        "<desc",
        "Point",
        "Line",
        "Face",
        "Body",
        "PWTSJ",
        "OSPS",
        "Project",
        "Workflow",
        "Task",
        "Step",
        "Job",
        "ProblemContract",
        "OutcomeNode",
        "Obligation",
        "Attempt",
        "Result",
        "mathematical proof",
    )
    missing = [marker for marker in required_markers if marker not in text]
    if missing:
        raise CheckError("architecture SVG is missing required markers: " + ", ".join(missing))
    if re.search(r"<(?:script|foreignObject|image|use)\b|(?:javascript:|on[a-z]+\s*=|(?:xlink:)?href\s*=)", text, re.IGNORECASE):
        raise CheckError("architecture SVG contains executable or external content")


def check_surfaces(root: Path) -> None:
    for relative in SURFACE_FILES:
        text = read_text(root, relative)
        for marker in FORBIDDEN_PUBLIC_IDENTIFIERS:
            if marker in text:
                raise CheckError(f"private identifier {marker!r} appears in {relative}")
        if PRIVATE_PATH_RE.search(text):
            raise CheckError(f"absolute private path appears in {relative}")
        if SECRET_ASSIGNMENT_RE.search(text):
            raise CheckError(f"secret-shaped assignment appears in {relative}")
        if OLD_PUBLIC_URL_RE.search(text):
            raise CheckError(f"old repository URL appears in {relative}")

    readme = read_text(root, "README.md")
    missing = [term for term in REQUIRED_README_TERMS if term not in readme]
    if missing:
        raise CheckError("README.md is missing required terms: " + ", ".join(missing))
    english = read_text(root, "README.en.md")
    missing = [term for term in REQUIRED_EN_TERMS if term not in english]
    if missing:
        raise CheckError("README.en.md is missing required terms: " + ", ".join(missing))
    llms = read_text(root, "llms.txt")
    for term in (
        PUBLIC_URL,
        "Current public status (verified 2026-09-09):",
        "Audience:",
        "Canonical vocabulary:",
        "solution index",
        "open mathematics problem",
        "Contribution guide:",
        "Problem catalog:",
        "Web research template:",
        "Start method:",
        "Method-layer mainline:",
        "Lean position:",
        "Single conceptual metamodel root:",
        "GEO guide:",
        "AI retrieval contract:",
        "Top-level lifecycle:",
        "Mathematical fact chain:",
        "Freshness authority:",
    ):
        if term not in llms:
            raise CheckError(f"llms.txt is missing {term!r}")

    try:
        solution_index = json.loads(read_text(root, "result-library/indexes/solutions.json"))
    except json.JSONDecodeError as exc:
        raise CheckError(f"solution index is invalid JSON: {exc}") from exc
    if not isinstance(solution_index, dict):
        raise CheckError("solution index must be a JSON object")
    if solution_index.get("result_ids") != []:
        raise CheckError("public documentation says the solution index is empty, but result_ids is not empty")
    for relative in (
        "problem-library/records/canonical-problems.jsonl",
        "research/records/attempts.jsonl",
        "result-library/records/results.jsonl",
    ):
        if read_text(root, relative).strip():
            raise CheckError(f"public documentation says canonical ledgers are empty, but {relative} has records")


def github_anchor(heading: str) -> str:
    value = re.sub(r"<[^>]+>", "", heading).strip().lower()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    return re.sub(r"\s+", "-", value).strip("-")


def check_links(root: Path) -> None:
    for relative in SURFACE_FILES:
        source = root / relative
        text = source.read_text(encoding="utf-8")
        anchors = {github_anchor(heading) for heading in HEADING_RE.findall(text)}
        for raw_target in MARKDOWN_LINK_RE.findall(text):
            target = raw_target.strip().strip("<>")
            if not target:
                continue
            if target.startswith("#"):
                if target[1:] not in anchors:
                    raise CheckError(f"broken public anchor: {relative} -> {target}")
                continue
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            target_path = target.split("#", 1)[0].split("?", 1)[0]
            if not target_path:
                continue
            candidate = (source.parent / target_path).resolve()
            try:
                candidate.relative_to(root.resolve())
            except ValueError as exc:
                raise CheckError(f"link escapes project: {relative} -> {target}") from exc
            if not candidate.exists():
                raise CheckError(f"broken public discovery link: {relative} -> {target}")


def check_external_problem_index(root: Path) -> None:
    try:
        registry = json.loads(read_text(root, "problem-library/registry/vibemathing-public-source.v1.json"))
    except json.JSONDecodeError as exc:
        raise CheckError(f"vibemathing source registry is invalid JSON: {exc}") from exc
    if not isinstance(registry, dict) or registry.get("schema_version") != "vibemathing-public-source.v1":
        raise CheckError("vibemathing source registry schema_version is invalid")
    namespace = registry.get("namespace")
    if (
        not isinstance(namespace, dict)
        or namespace.get("name") != "vibemathing"
        or namespace.get("url") != "https://github.com/vibemathing"
        or not isinstance(namespace.get("api_url"), str)
    ):
        raise CheckError("vibemathing source registry namespace is invalid")
    repositories = registry.get("repositories")
    expected_repositories = {
        "vibemathing/vibe-mathing-problem-library-public": "problem-library",
        "vibemathing/vibe-mathing-problem-public-template": "web-research-template",
    }
    if not isinstance(repositories, list):
        raise CheckError("vibemathing source registry repositories must be a list")
    by_name = {
        item.get("full_name"): item
        for item in repositories
        if isinstance(item, dict) and isinstance(item.get("full_name"), str)
    }
    for full_name, role in expected_repositories.items():
        item = by_name.get(full_name)
        if not isinstance(item, dict) or item.get("role") != role or not isinstance(item.get("url"), str):
            raise CheckError(f"vibemathing source registry is missing {full_name}")
    project_index = registry.get("project_index")
    if (
        not isinstance(project_index, dict)
        or project_index.get("owner") != "vibemathing"
        or project_index.get("number") != 1
        or project_index.get("url") != PUBLIC_PROJECT_URL
        or project_index.get("visibility") != "public"
    ):
        raise CheckError("vibemathing Project index identity is invalid")
    bounty_index = registry.get("bounty_project_index")
    bounty_view = bounty_index.get("view") if isinstance(bounty_index, dict) else None
    bounty_snapshot_meta = bounty_index.get("top146_snapshot") if isinstance(bounty_index, dict) else None
    if (
        not isinstance(bounty_index, dict)
        or bounty_index.get("owner") != "vibemathing"
        or bounty_index.get("number") != 2
        or bounty_index.get("url") != "https://github.com/users/vibemathing/projects/2"
        or not isinstance(bounty_view, dict)
        or bounty_view.get("number") != 3
        or bounty_view.get("url") != PUBLIC_BOUNTY_VIEW_URL
        or bounty_view.get("sort_by") != [
            {"field": "USD Equivalent", "direction": "DESC"},
            {"field": "Title", "direction": "ASC"},
        ]
        or not isinstance(bounty_snapshot_meta, dict)
        or bounty_snapshot_meta.get("path") != BOUNTY_TOP146_JSON_PATH
        or bounty_snapshot_meta.get("human_index_path") != BOUNTY_TOP146_PATH
        or bounty_snapshot_meta.get("unique_repositories") != 146
        or bounty_snapshot_meta.get("deduplication_key") != "repository_url"
    ):
        raise CheckError("vibemathing bounty Project index identity is invalid")
    try:
        bounty_snapshot = json.loads(read_text(root, BOUNTY_TOP146_JSON_PATH))
    except json.JSONDecodeError as exc:
        raise CheckError(f"bounty snapshot is invalid JSON: {exc}") from exc
    bounty_source = bounty_snapshot.get("source") if isinstance(bounty_snapshot, dict) else None
    bounty_selection = bounty_snapshot.get("selection") if isinstance(bounty_snapshot, dict) else None
    bounty_repositories = bounty_snapshot.get("repositories") if isinstance(bounty_snapshot, dict) else None
    if (
        not isinstance(bounty_snapshot, dict)
        or bounty_snapshot.get("schema_version") != "vibemathing-bounty-project-snapshot.v1"
        or not isinstance(bounty_source, dict)
        or bounty_source.get("view_url") != PUBLIC_BOUNTY_VIEW_URL
        or not isinstance(bounty_selection, dict)
        or bounty_selection.get("selected_unique_repositories") != 146
        or bounty_selection.get("deduplication_key") != "repository_url"
        or not isinstance(bounty_repositories, list)
        or len(bounty_repositories) != 146
        or [item.get("rank") for item in bounty_repositories] != list(range(1, 147))
        or len({item.get("repository_url") for item in bounty_repositories}) != 146
        or any(not isinstance(item.get("repository_url"), str) for item in bounty_repositories)
    ):
        raise CheckError("bounty Top-146 snapshot selection or deduplication is invalid")
    for key in (
        "repository_activity_is_evidence",
        "issue_pr_ci_checkpoint_is_evidence",
        "source_solved_or_claimed_status_is_result",
        "auto_admit_result_or_solution",
        "secp256k1_is_millennium_problem",
    ):
        boundary = bounty_snapshot.get("mathematical_boundary")
        if not isinstance(boundary, dict) or boundary.get(key) is not False:
            raise CheckError(f"bounty snapshot boundary is unsafe: {key}")
    key_repositories = registry.get("key_problem_repositories")
    if not isinstance(key_repositories, list) or len(key_repositories) != len(KEY_PROBLEM_REPOSITORIES):
        raise CheckError("vibemathing key problem repository index has the wrong size")
    key_by_name: dict[str, dict[str, Any]] = {}
    for item in key_repositories:
        if not isinstance(item, dict) or not isinstance(item.get("full_name"), str):
            raise CheckError("vibemathing key problem repository entry is invalid")
        full_name = item["full_name"]
        if full_name in key_by_name:
            raise CheckError(f"duplicate key problem repository: {full_name}")
        key_by_name[full_name] = item
    if set(key_by_name) != set(KEY_PROBLEM_REPOSITORIES):
        raise CheckError("vibemathing key problem repository identities drifted")
    for full_name, group in KEY_PROBLEM_REPOSITORIES.items():
        item = key_by_name[full_name]
        expected_url = f"https://github.com/{full_name}"
        if item.get("group") != group or item.get("url") != expected_url:
            raise CheckError(f"vibemathing key problem repository binding is invalid: {full_name}")
        for relative in ("README.md", "README.en.md", "problem-library/VIBEMATHING_PUBLIC_INDEX.md"):
            if expected_url not in read_text(root, relative):
                raise CheckError(f"key problem repository is missing from {relative}: {full_name}")
    key_policy = registry.get("key_problem_repository_policy")
    if (
        not isinstance(key_policy, dict)
        or key_policy.get("pointer_only") is not True
        or key_policy.get("auto_import_problem_contracts") is not False
        or key_policy.get("auto_clone_repositories") is not False
        or key_policy.get("repository_activity_is_mathematical_evidence") is not False
        or key_policy.get("repository_presence_is_solved_claim") is not False
        or key_policy.get("secp256k1_is_millennium_problem") is not False
    ):
        raise CheckError("vibemathing key problem repository policy is unsafe")
    for relative in ("README.md", "README.en.md", "problem-library/VIBEMATHING_PUBLIC_INDEX.md"):
        if PUBLIC_PROJECT_URL not in read_text(root, relative):
            raise CheckError(f"public Project index is missing from {relative}")
    snapshot = registry.get("canonical_catalog_snapshot")
    counts = snapshot.get("counts") if isinstance(snapshot, dict) else None
    if (
        not isinstance(snapshot, dict)
        or snapshot.get("index_path") != "catalog/canonical-index.json"
        or not isinstance(snapshot.get("index_url"), str)
        or not isinstance(counts, dict)
        or not {"canonical_problem_contracts", "draft_problem_contracts", "repository_locators"} <= set(counts)
        or any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in counts.values())
    ):
        raise CheckError("vibemathing catalog snapshot metadata is invalid")
    suite = registry.get("web_research_suite")
    if (
        not isinstance(suite, dict)
        or suite.get("template_repository") != "vibemathing/vibe-mathing-problem-public-template"
        or not isinstance(suite.get("required_start_files"), list)
        or not isinstance(suite.get("candidate_write_paths"), list)
    ):
        raise CheckError("vibemathing Web research suite metadata is invalid")
    try:
        template = json.loads(read_text(root, "problem-library/templates/problem-contract.template.json"))
    except json.JSONDecodeError as exc:
        raise CheckError(f"ProblemContract template is invalid JSON: {exc}") from exc
    policy = registry.get("integration_policy")
    if (
        not isinstance(policy, dict)
        or policy.get("mode") != "pointer-only until separately reviewed"
        or policy.get("remote_catalog_is_not_local_canonical") is not True
        or policy.get("auto_import_problem_contracts") is not False
        or policy.get("auto_clone_remote_repositories") is not False
        or policy.get("auto_admit_results") is not False
    ):
        raise CheckError("vibemathing source registry integration policy is unsafe")
    try:
        template = json.loads(read_text(root, "problem-library/templates/problem-contract.template.json"))
    except json.JSONDecodeError as exc:
        raise CheckError(f"ProblemContract template is invalid JSON: {exc}") from exc
    if (
        not isinstance(template, dict)
        or template.get("schema_version") != "1.0.0"
        or template.get("lifecycle") != "draft"
        or template.get("problem_id") != "problem:example-draft"
    ):
        raise CheckError("ProblemContract template must remain an explicit draft example")


def check_claims(root: Path) -> None:
    relative = "governance/publication/public-claims.v1.json"
    try:
        payload: dict[str, Any] = json.loads(read_text(root, relative))
    except json.JSONDecodeError as exc:
        raise CheckError(f"public claims JSON is invalid: {exc}") from exc
    if not isinstance(payload, dict):
        raise CheckError("public claims must be a JSON object")
    if payload.get("schema_version") != "public-claims.v1":
        raise CheckError("public claims schema_version is invalid")
    if payload.get("repository") != "vibemathing/vibe-mathing-cn-public":
        raise CheckError("public claims repository is invalid")
    verified_at = payload.get("last_verified")
    if not isinstance(verified_at, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", verified_at):
        raise CheckError("public claims last_verified must be an ISO date")
    claims = payload.get("claims")
    if not isinstance(claims, list) or not claims:
        raise CheckError("public claims must contain a non-empty claims list")
    seen: set[str] = set()
    allowed_surfaces = {"readme", "readme-en", "llms", "ai-citation", "metadata", "geo"}
    for item in claims:
        if not isinstance(item, dict):
            raise CheckError("each public claim must be an object")
        claim_id = item.get("claim_id")
        if not isinstance(claim_id, str) or not claim_id or claim_id in seen:
            raise CheckError("public claim IDs must be non-empty and unique")
        seen.add(claim_id)
        if item.get("status") != "current":
            raise CheckError(f"public claim {claim_id} is not current")
        if item.get("last_verified") != verified_at:
            raise CheckError(f"public claim {claim_id} has a stale verification date")
        surfaces = item.get("allowed_surfaces")
        if not isinstance(surfaces, list) or not surfaces or not set(surfaces) <= allowed_surfaces:
            raise CheckError(f"public claim {claim_id} has invalid allowed surfaces")
        evidence = item.get("evidence_refs")
        if not isinstance(evidence, list) or not evidence:
            raise CheckError(f"public claim {claim_id} has no evidence references")
        for reference in evidence:
            if (
                not isinstance(reference, str)
                or not reference
                or chr(0) in reference
                or "\\\\" in reference
            ):
                raise CheckError(f"public claim {claim_id} has an unsafe evidence reference")
            candidate = root / reference
            try:
                candidate.relative_to(root)
            except ValueError as exc:
                raise CheckError(f"public claim {claim_id} evidence escapes project") from exc
            if not candidate.exists():
                raise CheckError(f"public claim {claim_id} references missing path {reference}")
    required_claims = {
        "claim:identity",
        "claim:workflow",
        "claim:status",
        "claim:freshness-authority",
        "claim:fixtures",
        "claim:bounded-evidence",
        "claim:tool-maturity",
        "claim:problem-catalog",
        "claim:method-map",
        "claim:retrieval-contract",
        "claim:research-lifecycle",
        "claim:metamodel",
    }
    if not required_claims <= seen:
        raise CheckError("public claims are missing a required claim category")
    status_claim = next(item for item in claims if item.get("claim_id") == "claim:status")
    status_text = str(status_claim.get("text", "")).lower()
    if "empty" not in status_text or "does not claim" not in status_text:
        raise CheckError("claim:status must preserve the empty/no-solution boundary")
    freshness_claim = next(item for item in claims if item.get("claim_id") == "claim:freshness-authority")
    freshness_text = str(freshness_claim.get("text", "")).lower()
    if "dated" not in freshness_text or "revalidation" not in freshness_text:
        raise CheckError("claim:freshness-authority must preserve the snapshot/revalidation boundary")


def check_bounty_readme_tables(root: Path) -> None:
    expected_ranks = set(range(1, 147))
    rank_pattern = re.compile(r"^\|\s*(\d{1,3})\s*\|", re.MULTILINE)
    for relative, header in (
        ("README.md", "赏金（原币种；USD 等值）"),
        ("README.en.md", "Bounty (original; USD reference)"),
    ):
        text = read_text(root, relative)
        if header not in text:
            raise CheckError(f"{relative} is missing the inline bounty column")
        ranks = {int(value) for value in rank_pattern.findall(text) if 1 <= int(value) <= 146}
        if ranks != expected_ranks:
            raise CheckError(f"{relative} must contain inline Project #2 ranks 1..146")
        if "problem-secp256k1-ecdlog-polytime" not in text:
            raise CheckError(f"{relative} is missing the separate secp256k1 entry")
        table_lines = text.splitlines()
        header_index = next((index for index, line in enumerate(table_lines) if header in line), None)
        if header_index is None or header_index + 2 >= len(table_lines) or "secp256k1" not in table_lines[header_index + 2]:
            raise CheckError(f"{relative} must place secp256k1 in the first table row")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    try:
        check_required_files(root)
        check_architecture_asset(root)
        check_metadata(root)
        check_surfaces(root)
        check_bounty_readme_tables(root)
        check_links(root)
        check_external_problem_index(root)
        check_claims(root)
    except CheckError as exc:
        print(f"Public README/GEO check: BLOCK - {exc}")
        return 1
    print(f"Public README/GEO check: PASS surfaces={len(SURFACE_FILES)} claims=current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
