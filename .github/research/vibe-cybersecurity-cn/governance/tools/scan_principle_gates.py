#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True


PONYTAIL_SPECULATIVE_PATTERNS = [
    r"\bjust in case\b",
    r"\bfuture[- ]proof\b",
    r"\bfor future use\b",
    r"\bfuture extension\b",
    r"\bextension point\b",
    r"\bmaybe later\b",
    r"\breserved for future\b",
    r"\bgeneric enough\b",
    r"\bextensible\b",
    r"为了以后",
    r"将来可能",
    r"预留",
    r"占位",
    r"扩展点",
    r"未来扩展",
]

PONYTAIL_OWNERSHIP_PATTERNS = [
    r"\binterface\b",
    r"\babstract class\b",
    r"\bclass\s+\w*(Factory|Builder|Manager|Registry|Adapter|Wrapper|Plugin|Provider|Strategy|Base)\b",
    r"\b(Factory|Builder|Manager|Registry|Adapter|Wrapper|Plugin|Provider|Strategy)\b",
    r"\bnew dependency\b",
    r"\bnew config\b",
    r"\bfeature flag\b",
    r"新增依赖",
    r"新增配置",
    r"新增抽象",
    r"新增文件",
    r"新增流程",
]

PONYTAIL_PROOF_MARKERS = [
    "existence",
    "current requirement",
    "current consumer",
    "lowest viable",
    "ladder",
    "owner",
    "verification",
    "delete trigger",
    "upgrade trigger",
    "ceiling",
    "ponytail",
    "存在性",
    "当前需求",
    "当前消费者",
    "最低阶梯",
    "负责人",
    "验证",
    "删除触发",
    "升级触发",
    "天花板",
]

FUTURE_DRIFT_PATTERNS = [
    r"\bshort[- ]term\b",
    r"\btemporary\b",
    r"\binterim\b",
    r"\bworkaround\b",
    r"\bband[- ]aid\b",
    r"\bcompatibility\b",
    r"\bbackward[- ]compatible\b",
    r"\blegacy[- ]alias\b",
    r"\bcompat[- ]shim\b",
    r"\bshim\b",
    r"\bfor now\b",
    r"\bkeep old\b",
    r"\bmigration fear\b",
    r"短期",
    r"临时",
    r"过渡",
    r"兼容",
    r"旧别名",
    r"旧概念",
    r"暂时",
    r"先这样",
    r"以后再",
]

FUTURE_EVIDENCE_MARKERS = {
    "target_end_state": ["target end state", "end-state", "目标终态", "终态"],
    "real_constraints": ["real constraints", "真实约束"],
    "inertia_constraints": ["inertia constraints", "惯性约束"],
    "kill_list": ["kill list", "kill-list", "删除清单", "停止存在"],
    "proof_point": ["proof point", "证明点"],
    "falsifier": ["falsifier", "falsification", "推翻条件", "证伪"],
    "migration_slice": ["migration slice", "迁移切片"],
}

TEXT_SUFFIXES = {
    ".adoc",
    ".cfg",
    ".conf",
    ".css",
    ".go",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".mjs",
    ".py",
    ".rs",
    ".sh",
    ".sql",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}


def should_skip_path(path: str) -> bool:
    rel = Path(path)
    lowered_parts = {part.lower() for part in rel.parts}
    name = rel.name.lower()
    path_text = rel.as_posix().lower()
    return (
        "__pycache__" in lowered_parts
        or "node_modules" in lowered_parts
        or "tests" in lowered_parts
        or name.startswith("test-")
        or name == "changelog.md"
        or name == "skill.md" and path_text.startswith("skills/")
        or name == "index.md"
        or name == "gate-index.md"
        or name == "门禁与护栏.md"
        or name.startswith("gate-")
        or path_text == "scripts/check-codex-health.sh"
        or "/references/" in path_text and (
            "future-optimal" in name
            or "ponytail" in name
            or name.endswith("-review.md")
            or name.endswith("-patterns.md")
        )
        or "/standards/" in path_text and (
            "未来最优解" in name
            or "ponytail" in name
        )
        or name.endswith(".test.py")
        or name.endswith(".spec.py")
        or name.endswith(".test.ts")
        or name.endswith(".spec.ts")
        or name.endswith(".test.js")
        or name.endswith(".spec.js")
    )


def regex_found(patterns: list[str], text: str) -> list[str]:
    found: list[str] = []
    for pattern in patterns:
        if re.search(pattern, text, flags=re.IGNORECASE):
            found.append(pattern)
    return found


def marker_present(markers: list[str], lowered_text: str) -> bool:
    return any(marker.lower() in lowered_text for marker in markers)


def line_for_pattern(patterns: list[str], lines: list[str]) -> tuple[int | None, str | None]:
    for index, line in enumerate(lines, start=1):
        if regex_found(patterns, line):
            return index, line.strip()
    return None, None


def safe_read_text(path: Path, max_bytes: int) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return None
    try:
        if path.stat().st_size > max_bytes:
            return None
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def load_files_from_git(repo: Path, mode: str) -> list[str]:
    commands = {
        "working": ["git", "diff", "--name-only", "-z", "HEAD"],
        "staged": ["git", "diff", "--cached", "--name-only", "-z"],
        "all": ["git", "ls-files", "-z"],
    }
    result = subprocess.run(
        commands[mode],
        cwd=repo,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        return []
    return [os.fsdecode(item) for item in result.stdout.split(b"\0") if item]


def load_file_args(args: argparse.Namespace) -> list[str]:
    files: list[str] = []
    files.extend(args.file or [])
    if args.files_from:
        files.extend(
            line.strip()
            for line in Path(args.files_from).read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        )
    if not files:
        files.extend(load_files_from_git(Path(args.repo).resolve(), args.git_mode))
    return sorted(dict.fromkeys(files))


def scan_ponytail(path: str, text: str) -> list[dict[str, object]]:
    lowered = text.lower()
    lines = text.splitlines()
    findings: list[dict[str, object]] = []
    speculative = regex_found(PONYTAIL_SPECULATIVE_PATTERNS, text)
    ownership = regex_found(PONYTAIL_OWNERSHIP_PATTERNS, text)
    has_proof = marker_present(PONYTAIL_PROOF_MARKERS, lowered)

    if speculative and not has_proof:
        line_number, evidence = line_for_pattern(PONYTAIL_SPECULATIVE_PATTERNS, lines)
        findings.append(
            {
                "gate_id": "GATE-0000",
                "profile": "ponytail-complexity",
                "severity": "BLOCK",
                "label": "yagni",
                "path": path,
                "line": line_number,
                "evidence": evidence or speculative[0],
                "reason": "发现面向未来的扩展/占位信号，但没有存在性理由、当前消费者、最低工程阶梯、天花板或验证路径。",
                "minimal_fix": "删除/合并/内联该对象，或补充当前存在性理由、owner、验证方式、天花板和升级/删除触发条件。",
                "verification": "重新运行 scan_principle_gates.py，并确认 `ponytail-complexity` 无 BLOCK finding。",
            }
        )
    elif ownership and not has_proof:
        line_number, evidence = line_for_pattern(PONYTAIL_OWNERSHIP_PATTERNS, lines)
        findings.append(
            {
                "gate_id": "GATE-0000",
                "profile": "ponytail-complexity",
                "severity": "WARN",
                "label": "ownership-surface",
                "path": path,
                "line": line_number,
                "evidence": evidence or ownership[0],
                "reason": "发现新增/扩展所有权面信号，但没有足够证据证明对象现在必须存在。",
                "minimal_fix": "优先使用标准库、平台原生、项目既有能力；若保留，补 existence check、最低阶梯和验证路径。",
                "verification": "补齐存在性证明后重新扫描；必要时交给 `auto-review` 的 `ponytail-complexity` 深审。",
            }
        )
    return findings


def scan_future_optimal(path: str, text: str) -> list[dict[str, object]]:
    lowered = text.lower()
    lines = text.splitlines()
    drift = regex_found(FUTURE_DRIFT_PATTERNS, text)
    if not drift:
        return []

    missing = [
        key
        for key, markers in FUTURE_EVIDENCE_MARKERS.items()
        if not marker_present(markers, lowered)
    ]
    if not missing:
        return []

    line_number, evidence = line_for_pattern(FUTURE_DRIFT_PATTERNS, lines)
    severity = "BLOCK" if len(missing) >= 4 else "WARN"
    return [
        {
            "gate_id": "GATE-0001",
            "profile": "future-optimal-drift",
            "severity": severity,
            "label": "target-downgrade",
            "path": path,
            "line": line_number,
            "evidence": evidence or drift[0],
            "reason": "发现短期补丁、兼容层、旧概念或迁移恐惧信号，但 Future-Optimal 证据不完整。",
            "missing": missing,
            "minimal_fix": "补齐目标终态、真实约束、惯性约束、kill list、proof point、falsifier 和 migration slice；或删除不通向终态的兼容/临时路径。",
            "verification": "重新运行 scan_principle_gates.py，并确认 `future-optimal-drift` 无 BLOCK finding。",
        }
    ]


def scan_files(repo: Path, files: list[str], max_bytes: int) -> dict[str, object]:
    scanned: list[str] = []
    skipped: list[str] = []
    findings: list[dict[str, object]] = []
    for file_name in files:
        if should_skip_path(file_name):
            skipped.append(file_name)
            continue
        path = (repo / file_name).resolve()
        try:
            rel = path.relative_to(repo)
        except ValueError:
            skipped.append(file_name)
            continue
        text = safe_read_text(path, max_bytes)
        if text is None:
            skipped.append(str(rel))
            continue
        scanned.append(str(rel))
        findings.extend(scan_ponytail(str(rel), text))
        findings.extend(scan_future_optimal(str(rel), text))

    decision = "PASS"
    if any(item["severity"] == "BLOCK" for item in findings):
        decision = "BLOCK"
    elif findings:
        decision = "WARN"

    return {
        "decision": decision,
        "scanned_files": scanned,
        "skipped_files": skipped,
        "finding_count": len(findings),
        "findings": findings,
    }


def render_markdown(payload: dict[str, object]) -> str:
    lines = [
        "# Principle Gate Scan",
        "",
        f"- `decision`: {payload['decision']}",
        f"- `scanned_files`: {len(payload['scanned_files'])}",
        f"- `skipped_files`: {len(payload['skipped_files'])}",
        f"- `finding_count`: {payload['finding_count']}",
        "",
        "## Findings",
        "",
    ]
    findings = payload["findings"]
    if not findings:
        lines.append("- none")
    else:
        for item in findings:
            line = item.get("line")
            location = f"{item['path']}:{line}" if line else str(item["path"])
            lines.extend(
                [
                    f"### {item['severity']} `{item['profile']}` `{item['label']}`",
                    "",
                    f"- gate: `{item['gate_id']}`",
                    f"- location: `{location}`",
                    f"- evidence: {item['evidence']}",
                    f"- reason: {item['reason']}",
                ]
            )
            if item.get("missing"):
                lines.append(f"- missing: {', '.join(item['missing'])}")
            lines.extend(
                [
                    f"- minimal_fix: {item['minimal_fix']}",
                    f"- verification: {item['verification']}",
                    "",
                ]
            )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan files for Ponytail complexity and Future-Optimal drift gate signals."
    )
    parser.add_argument("--repo", default=".", help="Repository root.")
    parser.add_argument("--file", action="append", default=[], help="File to scan. Repeatable.")
    parser.add_argument("--files-from", help="Read files from a newline-delimited list.")
    parser.add_argument(
        "--git-mode",
        choices=("working", "staged", "all"),
        default="working",
        help="When no files are provided, scan files from this git source.",
    )
    parser.add_argument("--max-bytes", type=int, default=500_000, help="Skip files larger than this size.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when BLOCK findings exist.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = Path(args.repo).resolve()
    files = load_file_args(args)
    payload = scan_files(repo, files, args.max_bytes)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(payload))
    return 1 if args.strict and payload["decision"] == "BLOCK" else 0


if __name__ == "__main__":
    raise SystemExit(main())
