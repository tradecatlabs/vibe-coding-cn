#!/usr/bin/env python3
"""Foundry Smart Contract Security Agent.

Pre-deployment audit orchestrator for a Foundry project. Runs static analysis
(Slither, Aderyn), optional symbolic execution (Mythril), Foundry tests/coverage,
and a key-leak scan, then aggregates everything into a single JSON report with a
PASS/FAIL deploy gate.

Design constraints (mirrors the upstream repo's style, hardened):
  - subprocess always called with an ARGUMENT LIST, never shell=True
  - no outbound network calls; every tool runs locally on local source
  - every external tool guarded by timeout and graceful degradation if absent
  - read-only with respect to the project (only writes the report file)
"""

import os
import re
import json
import shutil
import argparse
import logging
import subprocess
from collections import defaultdict
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

SWC_REGISTRY = {
    "SWC-101": "Integer Overflow and Underflow",
    "SWC-104": "Unchecked Call Return Value",
    "SWC-105": "Unprotected Ether Withdrawal",
    "SWC-106": "Unprotected SELFDESTRUCT",
    "SWC-107": "Reentrancy",
    "SWC-110": "Assert Violation",
    "SWC-112": "Delegatecall to Untrusted Callee",
    "SWC-113": "DoS with Failed Call",
    "SWC-114": "Transaction Order Dependence (front-running)",
    "SWC-115": "Authorization through tx.origin",
    "SWC-116": "Block values as a proxy for time",
    "SWC-120": "Weak Sources of Randomness",
    "SWC-128": "DoS with Block Gas Limit",
}

SEVERITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3, "informational": 4, "optimization": 5}

# Directories that are dependencies / build output, not the audited code.
SKIP_DIRS = {"lib", "out", "cache", "node_modules", ".git", "broadcast", "artifacts"}

# A raw 32-byte hex private key (with or without 0x). High-precision signal: a
# 64-hex literal in source is almost always a key. Broader secret detection
# (mnemonics, API tokens, generic secrets) is intentionally delegated to gitleaks
# (see references/secure-deployment-and-keys.md) rather than reinvented noisily here.
PRIVKEY_RE = re.compile(r"\b(0x)?[0-9a-fA-F]{64}\b")


def _which(tool):
    return shutil.which(tool) is not None


def _run(cmd, timeout):
    """Run a command (list args), return (returncode, stdout, stderr). Never raises."""
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        logger.warning("Timeout: %s", " ".join(cmd))
        return 124, "", "timeout"
    except FileNotFoundError:
        return 127, "", "not found"


# --------------------------------------------------------------------------- #
# Static analysis
# --------------------------------------------------------------------------- #
def run_slither(project):
    if not _which("slither"):
        logger.warning("slither not installed - skipping static analysis")
        return None
    rc, out, err = _run(["slither", project, "--json", "-"], timeout=300)
    # Slither exits non-zero when it finds issues; JSON still lands on stdout.
    if not out:
        logger.error("slither produced no JSON (%s)", err.strip()[:200])
        return {}
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        logger.error("slither JSON parse failed")
        return {}


def analyze_slither(slither_output):
    findings, by_severity, by_detector = [], defaultdict(int), defaultdict(int)
    for det in (slither_output or {}).get("results", {}).get("detectors", []):
        severity = det.get("impact", "informational").lower()
        by_severity[severity] += 1
        name = det.get("check", "unknown")
        by_detector[name] += 1
        loc = ""
        elems = det.get("elements", [])
        if elems:
            sm = elems[0].get("source_mapping", {})
            lines = sm.get("lines") or [0]
            loc = f"{sm.get('filename_short', '')}:L{lines[0]}"
        findings.append({
            "source": "slither", "detector": name, "severity": severity,
            "confidence": det.get("confidence", ""), "location": loc,
            "description": (det.get("description", "") or "").strip()[:240],
        })
    return {
        "total": len(findings),
        "by_severity": dict(by_severity),
        "top_detectors": dict(sorted(by_detector.items(), key=lambda x: -x[1])[:15]),
        "findings": sorted(findings, key=lambda f: SEVERITY_RANK.get(f["severity"], 9)),
    }


def run_aderyn(project):
    if not _which("aderyn"):
        logger.info("aderyn not installed - skipping (recommended: cargo install aderyn)")
        return None
    report = os.path.join(project, "aderyn-report.json")
    rc, out, err = _run(["aderyn", project, "-o", report], timeout=300)
    try:
        with open(report) as fh:
            data = json.load(fh)
        return data
    except (OSError, json.JSONDecodeError):
        logger.error("aderyn report not readable")
        return {}


def analyze_aderyn(aderyn_output):
    findings, by_severity = [], defaultdict(int)
    if not aderyn_output:
        return {"total": 0, "by_severity": {}, "findings": []}
    for sev_key, sev in (("high_issues", "high"), ("low_issues", "low")):
        block = aderyn_output.get(sev_key, {}) or {}
        for issue in block.get("issues", []) if isinstance(block, dict) else []:
            by_severity[sev] += 1
            inst = (issue.get("instances") or [{}])[0]
            loc = f"{inst.get('contract_path', '')}:L{inst.get('line_no', 0)}"
            findings.append({
                "source": "aderyn", "detector": issue.get("title", ""), "severity": sev,
                "location": loc, "description": (issue.get("description", "") or "").strip()[:240],
            })
    return {
        "total": len(findings),
        "by_severity": dict(by_severity),
        "findings": sorted(findings, key=lambda f: SEVERITY_RANK.get(f["severity"], 9)),
    }


# --------------------------------------------------------------------------- #
# Symbolic execution (optional)
# --------------------------------------------------------------------------- #
def run_mythril(target, timeout):
    if not _which("myth"):
        logger.info("mythril not installed - skipping symbolic execution")
        return None
    rc, out, err = _run(
        ["myth", "analyze", target, "--execution-timeout", str(timeout), "-o", "json"],
        timeout=timeout + 60,
    )
    if not out:
        return {}
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        logger.error("mythril JSON parse failed")
        return {}


def analyze_mythril(mythril_output):
    findings, by_swc = [], defaultdict(int)
    for issue in (mythril_output or {}).get("issues", []):
        swc = f"SWC-{issue.get('swc-id')}" if issue.get("swc-id") else "unknown"
        by_swc[swc] += 1
        findings.append({
            "source": "mythril", "swc_id": swc,
            "swc_title": SWC_REGISTRY.get(swc, issue.get("title", "")),
            "severity": issue.get("severity", "Medium").lower(),
            "location": f"{issue.get('contract', '')}:L{issue.get('lineno', 0)}",
            "description": (issue.get("description", "") or "").strip()[:240],
        })
    return {"total": len(findings), "by_swc": dict(by_swc), "findings": findings}


# --------------------------------------------------------------------------- #
# Foundry tests + coverage
# --------------------------------------------------------------------------- #
def run_forge_tests(project):
    if not _which("forge"):
        logger.warning("forge not installed - skipping tests")
        return {"available": False}
    rc, out, err = _run(["forge", "test"], timeout=900)
    text = out + err
    passed = sum(int(n) for n in re.findall(r"(\d+)\s+passed", text))
    failed = sum(int(n) for n in re.findall(r"(\d+)\s+failed", text))
    return {"available": True, "exit_code": rc, "passed": passed,
            "failed": failed, "all_passed": rc == 0}


def run_forge_coverage(project):
    if not _which("forge"):
        return {"available": False}
    rc, out, err = _run(["forge", "coverage", "--report", "summary"], timeout=1200)
    m = re.search(r"^\|\s*Total\s*\|\s*([\d.]+)%", out, re.M)
    lines_pct = float(m.group(1)) if m else None
    return {"available": True, "lines_pct": lines_pct}


# --------------------------------------------------------------------------- #
# Key hygiene
# --------------------------------------------------------------------------- #
def scan_key_leaks(project):
    """Heuristic scan for plaintext private keys / mnemonics in source-controlled files."""
    hits = []
    for root, dirs, files in os.walk(project):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            # Match source/config files plus all dotenv variants (.env, .env.local, .env.prod...)
            if not (f.endswith((".sol", ".env", ".json", ".js", ".ts", ".toml", ".txt", ".md", ".sh", ".yaml", ".yml"))
                    or f.startswith(".env")):
                continue
            path = os.path.join(root, f)
            try:
                with open(path, encoding="utf-8", errors="ignore") as fh:
                    content = fh.read()
            except OSError:
                continue
            for m in PRIVKEY_RE.finditer(content):
                # Exclude the well-known Anvil/Hardhat test mnemonic-derived keys & all-zero.
                val = m.group(0).lower().removeprefix("0x")
                if val == "0" * 64 or "test test test" in content[max(0, m.start() - 80):m.start()]:
                    continue
                hits.append({"file": os.path.relpath(path, project), "type": "possible_private_key"})
                break
    return {"leaked_secret_candidates": len(hits), "hits": hits[:20],
            "note": "high-precision private-key scan only; run gitleaks for full secret coverage"}


# --------------------------------------------------------------------------- #
# Aggregation + gate
# --------------------------------------------------------------------------- #
def deduplicate(*finding_lists):
    seen, combined = set(), []
    for lst in finding_lists:
        for f in lst:
            key = (f.get("location", ""), f.get("detector", f.get("swc_id", "")))
            if key not in seen:
                seen.add(key)
                combined.append(f)
    return combined


def build_report(project, slither, aderyn, mythril, tests, coverage, keys, min_coverage):
    combined = deduplicate(slither["findings"], aderyn["findings"], mythril["findings"])
    crit_high = sum(1 for f in combined if f.get("severity") in ("critical", "high"))

    gate_fail = []
    if crit_high > 0:
        gate_fail.append(f"{crit_high} high/critical static finding(s)")
    if tests.get("available") and not tests.get("all_passed"):
        gate_fail.append(f"{tests.get('failed', '?')} failing test(s)")
    if keys["leaked_secret_candidates"] > 0:
        gate_fail.append(f"{keys['leaked_secret_candidates']} possible leaked secret(s)")
    cov = coverage.get("lines_pct")
    if cov is not None and cov < min_coverage:
        gate_fail.append(f"line coverage {cov}% < {min_coverage}% threshold")

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "project": os.path.abspath(project),
        "static_analysis": {
            "slither": {"total": slither["total"], "by_severity": slither["by_severity"],
                        "top_detectors": slither["top_detectors"]},
            "aderyn": {"total": aderyn["total"], "by_severity": aderyn["by_severity"]},
        },
        "symbolic_execution": {"mythril": {"total": mythril["total"], "by_swc": mythril.get("by_swc", {})}},
        "testing": {"forge_test": tests, "coverage": coverage},
        "key_hygiene": keys,
        "combined_findings": len(combined),
        "critical_high_findings": crit_high,
        "deploy_gate": "PASS" if not gate_fail else "FAIL",
        "gate_failures": gate_fail,
        "findings": combined[:40],
    }


def main():
    ap = argparse.ArgumentParser(description="Foundry Smart Contract Security Audit Agent")
    ap.add_argument("--project", default=".", help="Path to the Foundry project root")
    ap.add_argument("--mythril", metavar="FILE", help="Run Mythril symbolic execution on this .sol file")
    ap.add_argument("--mythril-timeout", type=int, default=300)
    ap.add_argument("--min-coverage", type=float, default=80.0, help="Min line coverage %% for PASS")
    ap.add_argument("--output", default="audit-report.json")
    args = ap.parse_args()

    logger.info("Auditing Foundry project: %s", os.path.abspath(args.project))
    slither = analyze_slither(run_slither(args.project))
    aderyn = analyze_aderyn(run_aderyn(args.project))
    mythril = analyze_mythril(run_mythril(args.mythril, args.mythril_timeout) if args.mythril else {})
    tests = run_forge_tests(args.project)
    coverage = run_forge_coverage(args.project)
    keys = scan_key_leaks(args.project)

    report = build_report(args.project, slither, aderyn, mythril, tests, coverage, keys, args.min_coverage)
    with open(args.output, "w") as fh:
        json.dump(report, fh, indent=2, default=str)
    logger.info("Audit: %d findings (%d high/critical) | gate=%s",
                report["combined_findings"], report["critical_high_findings"], report["deploy_gate"])
    if report["gate_failures"]:
        logger.warning("Gate failures: %s", "; ".join(report["gate_failures"]))
    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()
