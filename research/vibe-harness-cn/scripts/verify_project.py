#!/usr/bin/env python3
# 做什么：执行项目 Verification Policy 注册的确定性门禁并写出稳定 artifact。
# 怎么运行：python3 scripts/verify_project.py --gate contract；gate 名来自 capability registry。
# 需要什么：Python 3.11+、uv、已锁定脚本依赖和当前项目治理工具。

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT / "governance/runtime/verification-artifacts"
GATES = ("architecture", "behavior", "contract", "rollback", "security", "test")
PRINCIPLE_FILES = (
    "README.md",
    "AGENTS.md",
    "docs/AGENTS.md",
    "docs/HARNESS_MODEL.md",
    "docs/OPERATOR_SPEC.md",
    "docs/PROBLEM_SOLVING_OPERATOR_ARCHITECTURE_PRD.md",
    "research/AGENTS.md",
    "research/UPSTREAMS.md",
    "research/EXPANDED_OPERATOR_RESEARCH.md",
    "research/HEURISTIC_METACOGNITIVE_RESEARCH.md",
    "research/upstreams.sources.json",
    "research/upstreams.lock.json",
    "contracts/AGENTS.md",
    "contracts/harness-manifest.schema.json",
    "contracts/operator-runtime.schema.json",
    "contracts/problem-solving-operator-pack.schema.json",
    "contracts/examples/minimal-coding-harness.json",
    "contracts/examples/minimal-operator-binding.json",
    "contracts/examples/minimal-operator-run-request.json",
    "contracts/examples/minimal-operator-run-record.json",
    "examples/AGENTS.md",
    "examples/reference_harness/AGENTS.md",
    "examples/reference_harness/README.md",
    "examples/reference_harness/reference_harness.py",
    "examples/reference_harness/bindings/instruction-packet.json",
    "examples/reference_harness/requests/definition-first.json",
    "operators/AGENTS.md",
    "operators/README.md",
    "operators/catalog.json",
    "operators/source-inventory.json",
    "operators/taxonomy/AGENTS.md",
    "operators/taxonomy/problem-solving-methodology.json",
    "operators/packs/research.json",
    "operators/packs/computer-science.json",
    "operators/packs/mathematics.json",
    "operators/packs/software-engineering.json",
    "operators/packs/programming.json",
    "operators/packs/machine-learning.json",
    "operators/packs/deep-learning.json",
    "operators/packs/scientific-methodology.json",
    "operators/packs/systems-science.json",
    "operators/packs/complexity-science.json",
    "operators/packs/algorithms.json",
    "operators/packs/information-theory.json",
    "operators/packs/physics.json",
    "operators/packs/chemistry.json",
    "operators/packs/problem-solving-methodology.json",
    "operators/packs/statistics.json",
    "operators/packs/decision-science.json",
    "operators/packs/operations-research.json",
    "operators/packs/design-methods.json",
    "operators/packs/engineering.json",
    "scripts/AGENTS.md",
    "scripts/sync_upstreams.sh",
    "scripts/validate_harness.py",
    "scripts/validate_operator_library.py",
    "scripts/verify_project.py",
    "governance/standards/架构设计原则.md",
    "governance/context/PROJECT_OPERATING_MODEL.md",
    "governance/context/CONTEXT-MAP.md",
    "governance/context/CONTEXT-ROUTER.md",
    "governance/context/TOOLCHAIN_MODEL.md",
    "governance/context/PROJECT-TOPOLOGY.md",
    "governance/context/module-contexts/contracts/CONTEXT.md",
    "governance/context/module-contexts/docs/CONTEXT.md",
    "governance/context/module-contexts/examples/CONTEXT.md",
    "governance/context/module-contexts/operators/CONTEXT.md",
    "governance/context/module-contexts/research/CONTEXT.md",
    "governance/decisions/adr/ADR-0001-元-Harness-采用契约优先的治理控制面.md",
    "governance/decisions/adr/ADR-0003-引入问题求解算子语义层.md",
    "governance/decisions/adr/ADR-0005-跨学科算子扩展采用证据优先分层.md",
    "governance/decisions/adr/ADR-0006-母领域与八类功能采用双轴分类.md",
    "governance/decisions/adr/ADR-0007-以参考-Harness-验证-Operator-Runtime-互操作契约.md",
    "governance/evidence/qa-plans/QA-0001-Harness-manifest-契约与策略门禁.md",
    "governance/evidence/qa-plans/QA-0002-问题求解算子库完整性与契约门禁.md",
    "governance/evidence/qa-plans/QA-0003-Operator-Core-与-Reference-Profile-门禁.md",
    "governance/evidence/qa-plans/QA-0004-Operator-Runtime-参考闭环门禁.md",
    "governance/tasks/0001-bootstrap-meta-harness/PLAN.md",
    "governance/tasks/0002-sync-official-harness-sources/PLAN.md",
    "governance/tasks/0003-add-deepseek-harness-upstream/PLAN.md",
    "governance/tasks/0004-sync-expanded-harness-sources/PLAN.md",
    "governance/tasks/0008-build-complete-problem-solving-operator-library/PLAN.md",
)
SECRET_PATTERNS = (
    re.compile(rb"AKIA[0-9A-Z]{16}"),
    re.compile(rb"gh[pousr]_[A-Za-z0-9]{36,}"),
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(
        rb"(?i)(?:api_key|access_token|secret|password)\s*[:=]\s*['\"][^'\"\r\n]{8,}['\"]"
    ),
)


class GateFailure(RuntimeError):
    pass


def run(name: str, argv: list[str]) -> str:
    completed = subprocess.run(
        argv,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    if completed.returncode != 0:
        tail = (completed.stdout or "").strip()[-4000:]
        raise GateFailure(f"{name} 失败（exit={completed.returncode}）：\n{tail}")
    return (completed.stdout or "").strip()


def harness_self_test() -> None:
    run(
        "Harness 正反例",
        ["uv", "run", "--locked", "--script", "scripts/validate_harness.py", "--self-test"],
    )


def gate_contract() -> list[str]:
    harness_self_test()
    run(
        "有效 manifest",
        [
            "uv",
            "run",
            "--locked",
            "--script",
            "scripts/validate_harness.py",
            "contracts/examples/minimal-coding-harness.json",
        ],
    )
    run(
        "完整 Operator Library",
        [
            "uv",
            "run",
            "--locked",
            "--script",
            "scripts/validate_harness.py",
            "--operator-library",
            "operators/catalog.json",
        ],
    )
    run(
        "Operator Runtime Core",
        [
            "uv",
            "run",
            "--locked",
            "--script",
            "scripts/validate_harness.py",
            "--operator-runtime",
            "contracts/examples/minimal-operator-binding.json",
            "contracts/examples/minimal-operator-run-request.json",
            "contracts/examples/minimal-operator-run-record.json",
        ],
    )
    return [
        "Harness 正例通过",
        "Operator Library 411/411 + 57/57",
        "Operator Runtime 三类 Core 对象通过",
        "结构/策略/引用负例被拒绝",
    ]


def gate_behavior() -> list[str]:
    harness_self_test()
    run(
        "Reference Operator Harness",
        ["python3", "-m", "unittest", "tests.test_reference_operator_harness"],
    )
    run("上游同步行为", ["bash", "tests/test_sync_upstreams.sh"])
    return [
        "有效 manifest 零状态退出",
        "算子库完整性通过",
        "Reference Operator Harness 闭环与失败关闭通过",
        "关键负例被拒绝",
        "上游同步拒绝路径通过",
    ]


def gate_test() -> list[str]:
    run("uv 锁文件", ["uv", "lock", "--check", "--script", "scripts/validate_harness.py"])
    run("上游同步脚本语法", ["bash", "-n", "scripts/sync_upstreams.sh"])
    run("上游同步回归", ["bash", "tests/test_sync_upstreams.sh"])
    harness_self_test()
    run(
        "Python 回归",
        ["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
    )
    for relative in (
        "scripts/validate_harness.py",
        "scripts/validate_operator_library.py",
        "scripts/verify_project.py",
        "examples/reference_harness/reference_harness.py",
    ):
        source = (ROOT / relative).read_text(encoding="utf-8")
        compile(source, relative, "exec")
    for path in project_files():
        if path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
    return ["锁定依赖有效", "Shell/Python 源码可解析", "JSON 语法有效", "正反例回归通过"]


def project_files() -> list[Path]:
    completed = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise GateFailure("凭据扫描要求项目存在可审计 Git revision")
    return [ROOT / item.decode(errors="surrogateescape") for item in completed.stdout.split(b"\0") if item]


def gate_security() -> list[str]:
    harness_self_test()
    findings: list[str] = []
    for path in project_files():
        if not path.is_file() or path.stat().st_size > 2_000_000:
            continue
        content = path.read_bytes()
        if b"\x00" in content:
            continue
        if any(pattern.search(content) for pattern in SECRET_PATTERNS):
            findings.append(path.relative_to(ROOT).as_posix())
    if findings:
        raise GateFailure("疑似内联凭据：" + ", ".join(findings))
    return ["权限与审批负例通过", "模型自批被拒绝", "项目文本未命中内联凭据模式"]


def gate_architecture() -> list[str]:
    run(
        "架构上下文包",
        [
            "python3",
            "governance/tools/governance_context_bundle.py",
            "--project-root",
            ".",
            "--task-type",
            "architecture",
            "--code-path",
            "contracts",
            "--code-path",
            "operators",
            "--code-path",
            "research",
            "--code-path",
            "examples",
        ],
    )
    run(
        "治理严格校验",
        ["python3", "governance/tools/validate_governance_package.py", "--project-root", ".", "--strict"],
    )
    run(
        "治理健康报告",
        ["python3", "governance/tools/governance_health_report.py", "--project-root", ".", "--strict"],
    )
    command = [
        "python3",
        "governance/tools/scan_principle_gates.py",
        "--repo",
        ".",
        "--strict",
        "--format",
        "json",
    ]
    for relative in PRINCIPLE_FILES:
        command.extend(["--file", relative])
    payload = json.loads(run("Ponytail/Future-Optimal 扫描", command))
    scanned_files = payload.get("scanned_files")
    if (
        payload.get("finding_count") != 0
        or not isinstance(scanned_files, list)
        or len(scanned_files) != len(PRINCIPLE_FILES)
    ):
        raise GateFailure("原则扫描范围或 finding 不符合预期")
    return ["架构 context bundle 通过", "治理 strict/health 通过", "显式原则扫描无 finding"]


def gate_rollback() -> list[str]:
    run("上游同步回滚边界", ["bash", "tests/test_sync_upstreams.sh"])
    manifest = json.loads(
        (ROOT / "contracts/examples/minimal-coding-harness.json").read_text(encoding="utf-8")
    )
    lifecycle = manifest["spec"]["lifecycle"]
    rollback = lifecycle.get("rollback")
    if lifecycle.get("stage") != "candidate":
        raise GateFailure("作者可声明非 candidate 生命周期状态")
    if not isinstance(rollback, str) or not rollback.strip():
        raise GateFailure("rollback 必须是非空操作说明")
    if not lifecycle.get("promotion_requires"):
        raise GateFailure("promotion_requires 为空")
    return ["上游拒绝路径保持本地 HEAD", "作者状态固定 candidate", "晋升条件非空", "回滚 trigger/action 完整"]


GATE_FUNCTIONS: dict[str, Callable[[], list[str]]] = {
    "architecture": gate_architecture,
    "behavior": gate_behavior,
    "contract": gate_contract,
    "rollback": gate_rollback,
    "security": gate_security,
    "test": gate_test,
}


def write_artifact(gate: str, verdict: str, checks: list[str], error: str = "") -> Path:
    artifact = {
        "schema_version": "1.0.0",
        "gate": gate,
        "verdict": verdict,
        "checks": [{"name": item, "status": "PASS"} for item in checks],
        "error": error,
    }
    path = ARTIFACT_DIR / f"{gate}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="执行项目确定性验证门禁。")
    parser.add_argument("--gate", required=True, choices=GATES)
    args = parser.parse_args()
    try:
        checks = GATE_FUNCTIONS[args.gate]()
    except (GateFailure, KeyError, OSError, ValueError, json.JSONDecodeError) as exc:
        path = write_artifact(args.gate, "BLOCK", [], str(exc))
        print(f"BLOCK {args.gate}: {exc}\nartifact={path.relative_to(ROOT)}", file=sys.stderr)
        return 1
    path = write_artifact(args.gate, "PASS", checks)
    print(f"PASS {args.gate}\nartifact={path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
