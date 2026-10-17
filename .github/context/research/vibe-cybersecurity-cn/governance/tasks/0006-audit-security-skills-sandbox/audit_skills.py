#!/usr/bin/env python3
"""供应链安全审计：统计、恶意模式、嵌入指令、许可核验。
运行：python3 governance/tasks/0006-audit-security-skills-sandbox/audit_skills.py
依赖：Python 3.10+ 标准库；需要 .sandbox/skill-audit/ 下已克隆的仓库。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


SANDBOX = Path(__file__).resolve().parents[3] / ".sandbox" / "skill-audit"
OUT = Path(__file__).resolve().parent / "AUDIT_DATA.json"

# 高危/中危恶意模式（正则，大小写不敏感）
HIGH_PATTERNS = [
    (r"curl[^\n]*\|\s*(ba)?sh", "curl-pipe-shell"),
    (r"wget[^\n]*\|\s*(ba)?sh", "wget-pipe-shell"),
    (r"iwr[^\n]*\|\s*iex", "powershell-download-execute"),
    (r"Invoke-WebRequest[^\n]*Invoke-Expression", "pwsh-download-execute"),
    (r"base64\s*-d[^\n]*\|\s*(ba)?sh", "base64-pipe-shell"),
    (r"eval\s*\(\s*subprocess", "python-eval-subprocess"),
    (r"os\.system\s*\(\s*['\"]rm\s+-rf", "destructive-rm"),
    (r"shutil\.rmtree\s*\(\s*['\"]/", "destructive-rmtree"),
]
MEDIUM_PATTERNS = [
    (r"eval\s*\(", "eval"),
    (r"exec\s*\(", "exec"),
    (r"BEGIN\s*\{[^}]*system\(", "perl-system"),
    (r"\.ssh[\\/](id_rsa|id_ed25519|authorized_keys)", "ssh-key-reference"),
    (r"AKIA[0-9A-Z]{16}", "aws-key-lookalike"),
    (r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----", "private-key-block"),
    (r"sk-ant-[A-Za-z0-9_-]{20,}", "anthropic-key-lookalike"),
    (r"ghp_[A-Za-z0-9]{30,}", "github-pat-lookalike"),
    (r"sk-[A-Za-z0-9]{30,}", "openai-key-lookalike"),
]
# 嵌入指令模式：仅标记为数据，绝不执行
EMBEDDED_INSTRUCTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"disregard\s+(all\s+)?previous",
    r"you\s+must\s+(now\s+)?(ignore|forget|override)",
    r"system\s+prompt\s*:",
    r"<system>",
]
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".py", ".sh", ".js", ".ts", ".sol", ".rst"}


def scan_repo(repo_dir: Path) -> dict:
    files = [p for p in repo_dir.rglob("*") if p.is_file()]
    total_bytes = sum(p.stat().st_size for p in files)
    by_ext: dict[str, int] = {}
    for p in files:
        ext = p.suffix.lower() or "(none)"
        by_ext[ext] = by_ext.get(ext, 0) + 1
    top_exts = sorted(by_ext.items(), key=lambda kv: -kv[1])[:8]

    high_hits: list[dict] = []
    medium_hits: list[dict] = []
    embedded_hits: list[dict] = []
    binary_files: list[str] = []
    suspicious_binaries: list[str] = []
    license_files: list[str] = []
    seen_text_bytes = 0

    for p in files:
        rel = str(p.relative_to(repo_dir))
        if p.name.lower() in {"license", "license.md", "license.txt", "copying", "copying.md"}:
            license_files.append(p.name)
        # 二进制检测
        try:
            head = p.read_bytes()[:4096]
        except OSError:
            continue
        is_binary = b"\x00" in head
        if is_binary:
            binary_files.append(rel)
            # ELF/Mach-O/PE 可执行
            if head.startswith(b"\x7fELF") or head[:2] in {b"MZ", b"\xcf\xfa\xed\xfe"}:
                suspicious_binaries.append(rel)
            continue
        if p.suffix.lower() not in TEXT_SUFFIXES and p.name not in {"LICENSE", "LICENSE.md", "README.md", "SKILL.md"}:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        seen_text_bytes += len(text)
        for pattern, label in HIGH_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                high_hits.append({"file": rel, "pattern": label})
        for pattern, label in MEDIUM_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                medium_hits.append({"file": rel, "pattern": label})
        for pattern in EMBEDDED_INSTRUCTION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                embedded_hits.append({"file": rel, "pattern": pattern})

    # 去重
    high_hits = {f"{h['file']}:{h['pattern']}": h for h in high_hits}.values()
    medium_hits = {f"{h['file']}:{h['pattern']}": h for h in medium_hits}.values()
    embedded_hits = {f"{h['file']}:{h['pattern']}": h for h in embedded_hits}.values()

    # 顶层结构抽样
    top_level = sorted(p.name for p in repo_dir.iterdir())

    verdict = "pass"
    if high_hits:
        verdict = "high-risk"
    elif suspicious_binaries or any(h["pattern"].startswith("ssh-key") or "key-lookalike" in h["pattern"] or "private-key" in h["pattern"] for h in medium_hits):
        verdict = "review"

    return {
        "files": len(files),
        "total_bytes": total_bytes,
        "top_exts": dict(top_exts),
        "high_hits": list(high_hits)[:20],
        "medium_hits": list(medium_hits)[:30],
        "embedded_hits": list(embedded_hits)[:20],
        "binary_files": len(binary_files),
        "suspicious_binaries": suspicious_binaries[:10],
        "licenses": sorted(set(license_files)),
        "top_level": top_level[:15],
        "verdict": verdict,
    }


def main() -> int:
    if not SANDBOX.is_dir():
        print(f"BLOCK: 沙盒不存在 {SANDBOX}", file=sys.stderr)
        return 1
    results: dict[str, dict] = {}
    for repo_dir in sorted(SANDBOX.iterdir()):
        if not repo_dir.is_dir():
            continue
        results[repo_dir.name] = scan_repo(repo_dir)
    payload = {
        "schema_version": "1.0.0",
        "snapshot_date": "2026-08-14",
        "sandbox": str(SANDBOX),
        "repos": results,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"PASS: {len(results)} repos audited -> {OUT.name}")
    for name, r in results.items():
        print(f"  {name}: files={r['files']} bytes={r['total_bytes']} high={len(r['high_hits'])} "
              f"medium={len(r['medium_hits'])} embedded={len(r['embedded_hits'])} bins={r['binary_files']} "
              f"verdict={r['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
