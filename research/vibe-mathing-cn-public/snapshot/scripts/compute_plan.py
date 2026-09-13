#!/usr/bin/env python3
# 做什么：计算任务执行前的 GPU 可行性预检与资源预算路由，输出 CPU/GPU 决策。
# 怎么运行：python3 scripts/compute_plan.py --kind batch-search --n 1e8 --ops-per-sample 200 --dtype int8 [--json]
# 需要什么：Python 3 标准库；可选 CUDA 运行时 libcudart，无则自动回退 CPU。

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
from pathlib import Path

from vibe_mathing.runtime import RuntimeErrorBase, execute_bounded

# ==================== 可调参数（集中在此，按真实资源证据调整） ====================
GPU_FLOP_THRESHOLD = 1e9          # 估算浮点运算量达到该值才考虑 GPU
DENSE_MIN_N = 2048                # 稠密矩阵规模下限
DEFAULT_MEMORY_BUDGET_GB = 4       # 可移植保守默认；节点实际值由运行时注入
DEFAULT_MEMORY_HEADROOM_GB = 2     # 可移植保守默认；不表示节点容量
DEFAULT_THREADS_MAX = 1            # 可移植保守默认；多 worker 时避免线程叠加
# ================================================================================
GPU_PROBE_TIMEOUT_SECONDS = 5
GPU_PROBE_MEMORY_MB = 128
GPU_PROBE_OUTPUT_BYTES = 4096
MAX_GPU_PROBE_TIMEOUT_SECONDS = 300
MAX_SCALE = 1.0e18
MAX_FLOPS = 1.0e36
MAX_CONFIG_THREADS = 1024
MAX_CONFIG_MEMORY_GB = 1_048_576
PROJECT_ROOT = Path(__file__).resolve().parents[1]

KINDS = ("symbolic", "mpmath", "small-numeric", "dense-numeric", "batch-search")
GPUS_ROUTE_KINDS = ("dense-numeric", "batch-search")
FLOAT_DTYPES = ("f32", "f64")
BATCH_GPU_DTYPES = (*FLOAT_DTYPES, "int8", "int32", "int64")
DTYPES = (*BATCH_GPU_DTYPES, "exact")


def _reject_json_constant(value: str) -> object:
    raise ValueError(f"invalid JSON constant: {value}")


def probe_gpu(timeout_seconds: int = GPU_PROBE_TIMEOUT_SECONDS) -> tuple[bool, str]:
    """Run the CUDA probe in a disposable bounded process.

    A vendor runtime call can block or load native code.  It is therefore never
    executed in the planner process itself; failure, malformed output, and
    timeout all fail closed to CPU.
    """
    if (
        not isinstance(timeout_seconds, int)
        or isinstance(timeout_seconds, bool)
        or timeout_seconds <= 0
        or timeout_seconds > MAX_GPU_PROBE_TIMEOUT_SECONDS
    ):
        raise ValueError("GPU probe timeout must be a bounded positive integer")
    worker = PROJECT_ROOT / "scripts" / "gpu_probe_worker.py"
    if (
        worker.is_symlink()
        or worker.resolve() != worker
        or not worker.is_file()
        or not os.access(worker, os.R_OK)
    ):
        return False, "probe-worker-invalid"
    environment = {
        key: value
        for key, value in os.environ.items()
        if key in {"PATH", "HOME", "LANG", "LC_ALL", "TMPDIR"}
    }
    environment["PATH"] = environment.get("PATH", "/usr/local/bin:/usr/bin:/bin")
    try:
        completed = execute_bounded(
            [sys.executable, str(worker)],
            cwd=PROJECT_ROOT,
            timeout_seconds=timeout_seconds,
            max_output_bytes=GPU_PROBE_OUTPUT_BYTES,
            memory_budget_mb=GPU_PROBE_MEMORY_MB,
            threads_max=1,
            env=environment,
        )
    except RuntimeErrorBase:
        return False, "probe-failed"
    if not isinstance(completed, dict) or completed.get("exit_code") != 0:
        return False, "probe-error"
    stdout = completed.get("stdout")
    if not isinstance(stdout, str) or len(stdout.encode("utf-8")) > GPU_PROBE_OUTPUT_BYTES:
        return False, "probe-invalid"
    try:
        payload = json.loads(
            stdout,
            parse_constant=_reject_json_constant,
        )
    except (json.JSONDecodeError, ValueError):
        return False, "probe-invalid"
    if not isinstance(payload, dict):
        return False, "probe-invalid"
    available = payload.get("available")
    reason = payload.get("reason")
    if (
        not isinstance(available, bool)
        or not isinstance(reason, str)
        or not reason
        or len(reason) > 256
    ):
        return False, "probe-invalid"
    if not available:
        return False, reason
    return True, "cuda-device"


def memory_available_mb() -> int:
    """取 /proc/meminfo 与 cgroup v2 限额中更保守的可用内存（MB）。"""
    meminfo_available = None
    cgroup_available = None
    try:
        for line in Path("/proc/meminfo").read_text(encoding="utf-8")[:1_000_000].splitlines():
            if line.startswith("MemAvailable:"):
                fields = line.split()
                if len(fields) >= 2:
                    parsed = int(fields[1])
                    if 0 <= parsed <= MAX_CONFIG_MEMORY_GB * 1024 * 1024:
                        meminfo_available = parsed // 1024
                break
    except (OSError, ValueError, IndexError):
        pass
    try:
        max_kb = int(Path("/sys/fs/cgroup/memory.max").read_text(encoding="utf-8").strip())
        cur_kb = int(Path("/sys/fs/cgroup/memory.current").read_text(encoding="utf-8").strip())
        if max_kb not in (0, -1) and cur_kb >= 0:
            cgroup_available = max(0, (max_kb - cur_kb)) // 1024
    except (OSError, ValueError, IndexError):
        pass
    candidates = [v for v in (meminfo_available, cgroup_available) if v is not None]
    return min(candidates) if candidates else 0


def cpu_count() -> int:
    try:
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError):
        return os.cpu_count() or 1


def read_positive_int_env(
    name: str, default: int, maximum: int | None = None
) -> int:
    """读取正整数运行时配置；非法或过大值显式失败。"""
    raw = os.environ.get(name)
    if raw is None:
        value = default
    else:
        try:
            value = int(raw)
        except ValueError as exc:
            raise ValueError(f"{name} 必须是正整数") from exc
    if value <= 0 or (maximum is not None and value > maximum):
        suffix = f" 且不超过 {maximum}" if maximum is not None else ""
        raise ValueError(f"{name} 必须是正整数{suffix}")
    return value


def _finite_number(value: object) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(value)
    except (OverflowError, TypeError):
        return False


def estimate_flops(
    kind: str,
    n: float,
    flops: float | None,
    ops_per_sample: float = 1.0,
) -> float:
    if not _finite_number(n) or n < 0 or n > MAX_SCALE:
        raise ValueError("n 必须是有限且在规模上限内的非负数")
    if (
        not _finite_number(ops_per_sample)
        or ops_per_sample <= 0
        or ops_per_sample > MAX_SCALE
    ):
        raise ValueError("ops_per_sample 必须是有限且在规模上限内的正数")
    if flops is not None:
        if not _finite_number(flops) or flops < 0 or flops > MAX_FLOPS:
            raise ValueError("flops 必须是有限且在预算上限内的非负数")
        return flops
    if kind == "dense-numeric":
        value = 2.0 * n**3  # 稠密矩阵乘下界
    elif kind == "batch-search":
        value = n * ops_per_sample
    else:
        value = 0.0
    if not _finite_number(value) or value > MAX_FLOPS:
        raise ValueError("估算 FLOP 超过有限预算")
    return value


def decide(
    kind: str,
    n: float,
    dtype: str,
    flops: float,
    gpu_available: bool,
    gpu_name: str,
    available_mb: int,
    force_cpu: bool,
    threads_max: int,
    memory_budget_gb: int,
    memory_headroom_gb: int,
) -> dict:
    if (
        not isinstance(kind, str)
        or len(kind) > 64
        or not isinstance(dtype, str)
        or len(dtype) > 64
        or not isinstance(gpu_available, bool)
        or not isinstance(gpu_name, str)
        or len(gpu_name) > 256
        or not isinstance(force_cpu, bool)
        or not isinstance(available_mb, int)
        or isinstance(available_mb, bool)
        or available_mb < 0
        or available_mb > MAX_CONFIG_MEMORY_GB * 1024
        or not isinstance(threads_max, int)
        or isinstance(threads_max, bool)
        or threads_max <= 0
        or threads_max > MAX_CONFIG_THREADS
        or not isinstance(memory_budget_gb, int)
        or isinstance(memory_budget_gb, bool)
        or memory_budget_gb <= 0
        or memory_budget_gb > MAX_CONFIG_MEMORY_GB
        or not isinstance(memory_headroom_gb, int)
        or isinstance(memory_headroom_gb, bool)
        or memory_headroom_gb <= 0
        or memory_headroom_gb > MAX_CONFIG_MEMORY_GB
        or not isinstance(n, (int, float))
        or isinstance(n, bool)
        or not _finite_number(n)
        or n < 0
        or n > MAX_SCALE
        or not isinstance(flops, (int, float))
        or isinstance(flops, bool)
        or not _finite_number(flops)
        or flops < 0
        or flops > MAX_FLOPS
    ):
        raise ValueError("compute plan inputs are invalid or exceed budget")
    reasons: list[str] = []
    route = "cpu"

    if force_cpu:
        reasons.append("COMPUTE_FORCE_CPU=1 强制 CPU")
    elif kind in ("symbolic", "mpmath"):
        route = "cpu"
        reasons.append(f"{kind} 固定走 CPU：符号/任意精度计算无 GPU 后端")
    elif kind == "small-numeric":
        route = "cpu"
        reasons.append("small-numeric 固定走 CPU：小规模任务 GPU 无收益")
    elif kind in GPUS_ROUTE_KINDS:
        threshold_ok = flops >= GPU_FLOP_THRESHOLD
        dense_ok = kind == "dense-numeric" and n >= DENSE_MIN_N
        if not gpu_available:
            reasons.append(f"GPU 不可用（{gpu_name}），回退 CPU")
        elif kind == "dense-numeric" and dtype not in FLOAT_DTYPES:
            reasons.append(f"稠密数值精度 {dtype} 无准入 GPU 后端，回退 CPU")
        elif kind == "batch-search" and dtype not in BATCH_GPU_DTYPES:
            reasons.append(f"批量搜索精度 {dtype} 无准入 GPU 后端，回退 CPU")
        elif not (threshold_ok or dense_ok):
            reasons.append(
                f"估算运算量 {flops:.3g} FLOP 低于阈值 {GPU_FLOP_THRESHOLD:.3g}"
                f"（稠密另需 n>={DENSE_MIN_N}），CPU 更优"
            )
        elif available_mb < (memory_budget_gb + memory_headroom_gb) * 1024:
            reasons.append(
                f"可用内存 {available_mb} MiB 低于预算+余量"
                f"（{memory_budget_gb + memory_headroom_gb} GiB），排队或回退 CPU"
            )
        else:
            route = "gpu"
            reasons.append(
                f"运算量 {flops:.3g} FLOP 达阈值且 GPU 可用，走 GPU 粗筛"
            )
    else:  # 未知类型不应到达，防御性分支
        reasons.append(f"未知计算类型 {kind}，回退 CPU")

    memory_budget_mb = 0
    needs_lock = False
    if route == "gpu":
        memory_budget_mb = min(
            memory_budget_gb * 1024,
            available_mb - memory_headroom_gb * 1024,
        )
        needs_lock = True

    return {
        "route": route,
        "kind": kind,
        "n": n,
        "dtype": dtype,
        "flops_estimate": flops,
        "gpu_available": gpu_available,
        "gpu_name": gpu_name,
        "memory_available_mb": available_mb,
        "memory_budget_mb": memory_budget_mb,
        "threads_max": threads_max,
        "memory_budget_config_gb": memory_budget_gb,
        "memory_headroom_config_gb": memory_headroom_gb,
        "needs_gpu_lock": needs_lock,
        "reasons": reasons,
        "evidence_rule": "GPU 结果仅限 numeric-check；精确裁决必须回 CPU 的 SymPy/mpmath/FP64 路径",
        "engine": "scripts/compute_plan.py",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="计算任务 GPU 可行性预检：输出 CPU/GPU 路由与资源预算。"
    )
    parser.add_argument("--kind", required=True, choices=KINDS, help="计算类型")
    parser.add_argument("--n", type=float, default=0.0,
                        help="规模（矩阵阶数/样本数/项数）；符号任务可省略")
    parser.add_argument("--dtype", default="f64", choices=DTYPES,
                        help="数值精度；exact/symbolic 走 CPU；整数批量搜索可用 int8/int32/int64")
    parser.add_argument("--flops", type=float, default=None,
                        help="可选：调用方给出的估算浮点运算量；缺省按类型与 n 推算")
    parser.add_argument("--ops-per-sample", type=float, default=1.0,
                        help="batch-search 每样本估算操作数；--flops 优先级更高")
    parser.add_argument("--json", action="store_true", help="只输出 JSON")
    args = parser.parse_args()

    if not math.isfinite(args.n):
        parser.error("--n 必须是有限数")
    if args.kind in ("small-numeric", "dense-numeric", "batch-search") and args.n <= 0:
        parser.error(f"{args.kind} 要求 --n > 0")
    if not math.isfinite(args.ops_per_sample) or args.ops_per_sample <= 0:
        parser.error("--ops-per-sample 必须是有限正数")
    if args.flops is not None and (not math.isfinite(args.flops) or args.flops < 0):
        parser.error("--flops 必须是有限非负数")

    try:
        threads_max = read_positive_int_env(
            "COMPUTE_THREADS_MAX", DEFAULT_THREADS_MAX, MAX_CONFIG_THREADS
        )
        memory_budget_gb = read_positive_int_env(
            "COMPUTE_MEMORY_BUDGET_GB", DEFAULT_MEMORY_BUDGET_GB, MAX_CONFIG_MEMORY_GB
        )
        memory_headroom_gb = read_positive_int_env(
            "COMPUTE_MEMORY_HEADROOM_GB", DEFAULT_MEMORY_HEADROOM_GB, MAX_CONFIG_MEMORY_GB
        )
    except ValueError as exc:
        parser.error(str(exc))

    gpu_available, gpu_name = probe_gpu()
    available_mb = memory_available_mb()
    force_cpu = os.environ.get("COMPUTE_FORCE_CPU", "") == "1"
    try:
        flops = estimate_flops(args.kind, args.n, args.flops, args.ops_per_sample)
    except ValueError as exc:
        parser.error(str(exc))

    plan = decide(
        kind=args.kind,
        n=args.n,
        dtype=args.dtype,
        flops=flops,
        gpu_available=gpu_available,
        gpu_name=gpu_name,
        available_mb=available_mb,
        force_cpu=force_cpu,
        threads_max=threads_max,
        memory_budget_gb=memory_budget_gb,
        memory_headroom_gb=memory_headroom_gb,
    )
    plan["cpu_count"] = cpu_count()

    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2, allow_nan=False))
    else:
        print(f"route           : {plan['route']}")
        print(f"kind            : {plan['kind']}  n={plan['n']:g}  dtype={plan['dtype']}")
        print(f"flops_estimate  : {plan['flops_estimate']:.3g}")
        print(f"gpu             : available={plan['gpu_available']}  {plan['gpu_name']}")
        print(f"memory          : available={plan['memory_available_mb']} MiB  budget={plan['memory_budget_mb']} MiB")
        print(f"threads_max     : {plan['threads_max']}  needs_gpu_lock={plan['needs_gpu_lock']}")
        for reason in plan["reasons"]:
            print(f"reason          : {reason}")
        print(f"evidence_rule   : {plan['evidence_rule']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
