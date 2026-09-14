#!/usr/bin/env python3
# 做什么：提供 ProblemContract 生命周期、研究运行和 ResearchBundle 导出的统一单机入口。
# 怎么运行：python3 scripts/vibe_mathing_cli.py <command> [options]
# 需要什么：Python 3、项目依赖与已注册 adapter；所有写入由 ResearchStore 完成。

from __future__ import annotations

import argparse
import json
import os
import stat
from datetime import datetime, timedelta, timezone
from pathlib import Path

from vibe_mathing.bundle import BundleError, derive_research_bundle
from vibe_mathing.pipeline import SYMPY_ADAPTER, run_sympy_pipeline
from vibe_mathing.runtime import cancel_run, load_run, now
from vibe_mathing.store import MAX_COLLECTION_BYTES, ResearchStore, StoreError


def read_problem_input(path: Path, root: Path) -> dict[str, object]:
    candidate = Path(os.path.abspath(path if path.is_absolute() else root / path))
    root = Path(os.path.abspath(root))
    try:
        relative = candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError("Problem 文件必须位于 project root 内") from exc
    current = root
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise ValueError("Problem 文件路径不能包含 symlink")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise ValueError("当前平台缺少 O_NOFOLLOW，拒绝读取 Problem 文件")
    descriptor = os.open(candidate, os.O_RDONLY | nofollow)
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode) or file_stat.st_size > MAX_COLLECTION_BYTES:
            raise ValueError("Problem 文件超过大小预算或不是普通文件")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, MAX_COLLECTION_BYTES - total + 1))
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_COLLECTION_BYTES:
                raise ValueError("Problem 文件超过大小预算")
            chunks.append(chunk)
    finally:
        os.close(descriptor)
    value = json.loads(
        b"".join(chunks).decode("utf-8"),
        parse_constant=lambda constant: (_ for _ in ()).throw(
            ValueError(f"JSON 常量非法：{constant}")
        ),
    )
    if not isinstance(value, dict):
        raise ValueError("Problem JSON 顶层必须是对象")
    return value


def next_timestamp(current: str) -> str:
    """生成严格晚于当前值的 UTC 秒级时间，避免同秒 lifecycle 转换漂移。"""
    candidate = now()
    if candidate > current:
        return candidate
    parsed = datetime.fromisoformat(current.replace("Z", "+00:00"))
    return (parsed + timedelta(seconds=1)).astimezone(timezone.utc).isoformat().replace(
        "+00:00", "Z"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Vibe Mathing 可信研究闭环")
    parser.add_argument("--project-root", default=".")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--problem-id", required=True)
    run_parser.add_argument("--adapter", default=SYMPY_ADAPTER, choices=[SYMPY_ADAPTER])
    run_parser.add_argument("--fail-after", choices=["candidate_ready", "result_written"])
    resume_parser = subparsers.add_parser("resume")
    resume_parser.add_argument("--run-id", required=True)
    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("--run-id", required=True)
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("--run-id", required=True)
    cancel_parser = subparsers.add_parser("cancel")
    cancel_parser.add_argument("--run-id", required=True)
    register_parser = subparsers.add_parser("register-problem")
    register_parser.add_argument("--file", required=True)
    bundle_parser = subparsers.add_parser("export-bundle")
    bundle_parser.add_argument("--problem-id", required=True)
    lifecycle_parser = subparsers.add_parser("set-problem-lifecycle")
    lifecycle_parser.add_argument("--problem-id", required=True)
    lifecycle_parser.add_argument("--lifecycle", required=True, choices=["active", "withdrawn"])
    args = parser.parse_args()
    root = Path(os.path.abspath(args.project_root))

    if args.command == "register-problem":
        source = Path(args.file)
        try:
            problem = read_problem_input(source, root)
        except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
            parser.error(f"无法读取 Problem JSON：{exc}")
        created = ResearchStore(root).upsert("problems", problem)
        print(json.dumps({"problem_id": problem.get("problem_id"), "created": created}, ensure_ascii=False))
        return 0
    if args.command == "export-bundle":
        try:
            bundle = derive_research_bundle(root, args.problem_id)
        except (BundleError, StoreError) as exc:
            parser.error(str(exc))
        print(json.dumps(bundle, ensure_ascii=False, sort_keys=True))
        return 0
    if args.command == "set-problem-lifecycle":
        store = ResearchStore(root)
        problem = next(
            (item for item in store.read("problems") if item["problem_id"] == args.problem_id),
            None,
        )
        if problem is None:
            parser.error(f"Problem 不存在：{args.problem_id}")
        changed = {
            **problem,
            "lifecycle": args.lifecycle,
            "updated_at": next_timestamp(problem["updated_at"]),
        }
        try:
            store.replace_problem(changed)
        except StoreError as exc:
            parser.error(str(exc))
        print(json.dumps({"problem_id": args.problem_id, "lifecycle": args.lifecycle}, ensure_ascii=False))
        return 0
    if args.command == "run":
        state = run_sympy_pipeline(root, args.problem_id, fail_after=args.fail_after)
    elif args.command == "resume":
        current = load_run(root, args.run_id)
        if current["adapter"] != SYMPY_ADAPTER:
            parser.error(f"不支持恢复 adapter={current['adapter']}")
        state = run_sympy_pipeline(root, current["problem_id"])
    elif args.command == "status":
        state = load_run(root, args.run_id)
    elif args.command == "verify":
        state = load_run(root, args.run_id)
        expected = f"result:{args.run_id.removeprefix('run:')}"
        solutions = ResearchStore(root).rebuild_solution_view()
        accepted = state["status"] == "accepted"
        if (expected in solutions) is not accepted:
            raise SystemExit("验证失败：run 终态与 Solution View 不一致")
    else:
        state = cancel_run(root, args.run_id)

    print(json.dumps(state, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
