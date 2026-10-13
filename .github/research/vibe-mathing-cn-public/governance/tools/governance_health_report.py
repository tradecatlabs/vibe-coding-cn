#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path

import sys

sys.dont_write_bytecode = True

from validate_governance_package import GOV_ROOT, parse_frontmatter, validate

DOCUMENT_DRIVEN_REQUIRED = [
    "context/PROJECT_OPERATING_MODEL.md",
    "processes/DOCUMENT_DRIVEN_DEVELOPMENT.md",
    "context/TOOLCHAIN_MODEL.md",
    "context/project_operating_model_contract.v1.yaml",
]


RECORD_DIRS = {
    "adr": ("ADR", Path("decisions/adr")),
    "review": ("REVIEW", Path("evidence/reviews")),
    "postmortem": ("POSTMORTEM", Path("evidence/postmortems")),
    "lesson": ("LESSON", Path("evidence/lessons")),
    "workorder": ("WO", Path("evidence/workorders")),
    "debt": ("DEBT", Path("evidence/tech-debt")),
    "gate": ("GATE", Path("architecture-gates/rules")),
    "qa": ("QA", Path("evidence/qa-plans")),
    "agent-feedback": ("AF", Path("agent-governance/agent-feedback")),
    "baseline": ("BASELINE", Path("evidence/baselines")),
    "control": ("CONTROL", Path("control-plane/controls")),
    "exception": ("EXCEPTION", Path("evidence/exceptions")),
    "risk": ("RISK", Path("risk-register")),
    "conformance": ("CONFORMANCE", Path("evidence/conformance")),
    "audit-export": ("AUDIT", Path("evidence/audit-exports")),
    "release": ("RELEASE", Path("evidence/releases")),
}


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def review_cycle_days(value: str | None) -> int:
    if not value:
        return 90
    match = re.fullmatch(r"P(\d+)D", value.strip())
    return int(match.group(1)) if match else 90


def markdown_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def record_counts(root: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    for kind, (prefix, rel_dir) in RECORD_DIRS.items():
        directory = root / rel_dir
        counts[kind] = len(list(directory.glob(f"{prefix}-*.md"))) if directory.exists() else 0
    return counts


def placeholder_docs(root: Path) -> list[str]:
    docs: list[str] = []
    for path in markdown_files(root):
        rel = path.relative_to(root)
        if rel.parts and rel.parts[0] == "templates":
            continue
        text = path.read_text(encoding="utf-8")
        if "待补充" in text:
            docs.append(str(rel))
    return docs


def stale_docs(root: Path, today: date) -> list[str]:
    stale: list[str] = []
    for path in markdown_files(root):
        rel = path.relative_to(root)
        if rel.parts and rel.parts[0] in {"templates", "archive"}:
            continue
        fm = parse_frontmatter(path.read_text(encoding="utf-8")) or {}
        last = parse_date(fm.get("last_reviewed"))
        if not last:
            continue
        cycle = review_cycle_days(fm.get("review_cycle"))
        if today - last > timedelta(days=cycle):
            stale.append(str(rel))
    return stale


def active_feedback(root: Path) -> list[str]:
    directory = root / "agent-governance" / "agent-feedback"
    if not directory.exists():
        return []
    open_items: list[str] = []
    for path in sorted(directory.glob("AF-*.md")):
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text) or {}
        status = fm.get("status", "").strip().lower()
        if status not in {"converted", "rejected", "archived", "deprecated"}:
            open_items.append(path.name)
    return open_items


def gate_quality(root: Path) -> dict[str, int]:
    directory = root / "architecture-gates" / "rules"
    total = 0
    auto_ready = 0
    if not directory.exists():
        return {"total": 0, "auto_ready": 0}
    for path in sorted(directory.glob("GATE-*.md")):
        total += 1
        fm = parse_frontmatter(path.read_text(encoding="utf-8")) or {}
        detectability = fm.get("detectability", "").lower()
        if any(token in detectability for token in ("test", "ci", "lint", "script", "auto")):
            auto_ready += 1
    return {"total": total, "auto_ready": auto_ready}


def document_driven_status(root: Path) -> dict[str, object]:
    existing = [rel for rel in DOCUMENT_DRIVEN_REQUIRED if (root / rel).exists()]
    missing = [rel for rel in DOCUMENT_DRIVEN_REQUIRED if rel not in existing]
    return {
        "enabled": bool(existing),
        "complete": bool(existing) and not missing,
        "existing": existing,
        "missing": missing,
    }


def build_report(project_root: Path, strict: bool) -> dict[str, object]:
    root = project_root / GOV_ROOT
    validation = validate(project_root, strict)
    counts = record_counts(root)
    placeholders = placeholder_docs(root)
    stale = stale_docs(root, date.today())
    feedback = active_feedback(root)
    gate_stats = gate_quality(root)
    doc_driven = document_driven_status(root)
    markdown_count = len(markdown_files(root))

    decision = validation["decision"]
    if decision == "PASS" and (placeholders or stale or feedback):
        decision = "WARN"

    next_actions: list[str] = []
    if validation["decision"] == "BLOCK":
        next_actions.append("先修复 validate_governance_package.py 报出的 BLOCK。")
    if placeholders:
        next_actions.append("优先补齐含有“待补充”的当前标准、流程、gate 和模块上下文。")
    if feedback:
        next_actions.append("处理 open agent feedback：转成 lesson/gate，或明确 rejected/archived。")
    if stale:
        next_actions.append("复审过期文档并更新 last_reviewed。")
    if gate_stats["total"] and gate_stats["auto_ready"] == 0:
        next_actions.append("选择至少一个高价值 gate 转成 script/test/CI/agent 可检测护栏。")
    if doc_driven["enabled"] and not doc_driven["complete"]:
        next_actions.append("补齐 document-driven operating model：PROJECT_OPERATING_MODEL、DOCUMENT_DRIVEN_DEVELOPMENT、TOOLCHAIN_MODEL 和机器契约必须成套存在。")
    if not next_actions and decision == "PASS":
        next_actions.append("治理包健康，继续按事件增量维护。")

    return {
        "decision": decision,
        "root": str(root),
        "markdown_count": markdown_count,
        "record_counts": counts,
        "gate_quality": gate_stats,
        "document_driven": doc_driven,
        "placeholder_count": len(placeholders),
        "placeholder_examples": placeholders[:20],
        "stale_count": len(stale),
        "stale_examples": stale[:20],
        "open_agent_feedback_count": len(feedback),
        "open_agent_feedback_examples": feedback[:20],
        "validation": validation,
        "next_actions": next_actions,
    }


def render_markdown(report: dict[str, object]) -> str:
    counts = report["record_counts"]
    gates = report["gate_quality"]
    doc_driven = report["document_driven"]
    lines = [
        "# Governance Health Report",
        "",
        f"- `decision`: {report['decision']}",
        f"- `root`: {report['root']}",
        f"- `markdown_count`: {report['markdown_count']}",
        f"- `placeholder_count`: {report['placeholder_count']}",
        f"- `stale_count`: {report['stale_count']}",
        f"- `open_agent_feedback_count`: {report['open_agent_feedback_count']}",
        f"- `gate_auto_ready`: {gates['auto_ready']} / {gates['total']}",
        f"- `document_driven_operating_model`: {'enabled' if doc_driven['enabled'] else 'disabled'} / {'complete' if doc_driven['complete'] else 'incomplete'}",
        "",
        "## Record Counts",
        "",
    ]
    for kind, count in counts.items():
        lines.append(f"- `{kind}`: {count}")
    lines.extend(["", "## Placeholder Examples", ""])
    placeholders = report["placeholder_examples"]
    if placeholders:
        lines.extend(f"- `{item}`" for item in placeholders)
    else:
        lines.append("- none")
    lines.extend(["", "## Stale Examples", ""])
    stale = report["stale_examples"]
    if stale:
        lines.extend(f"- `{item}`" for item in stale)
    else:
        lines.append("- none")
    lines.extend(["", "## Document-Driven Operating Model", ""])
    if doc_driven["enabled"]:
        lines.append("- existing:")
        lines.extend(f"  - `{item}`" for item in doc_driven["existing"])
        lines.append("- missing:")
        if doc_driven["missing"]:
            lines.extend(f"  - `{item}`" for item in doc_driven["missing"])
        else:
            lines.append("  - none")
    else:
        lines.append("- disabled")
    lines.extend(["", "## Next Actions", ""])
    for item in report["next_actions"]:
        lines.append(f"- {item}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render an governance health report.")
    parser.add_argument("--project-root", default=".", help="Target project root.")
    parser.add_argument("--strict", action="store_true", help="Run strict structural validation inside the report.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report(Path(args.project_root).resolve(), args.strict)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report))
    return 1 if report["decision"] == "BLOCK" else 0


if __name__ == "__main__":
    raise SystemExit(main())
