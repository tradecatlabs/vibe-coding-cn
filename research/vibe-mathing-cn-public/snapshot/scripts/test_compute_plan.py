#!/usr/bin/env python3
# 做什么：回归验证 CPU/GPU 路由的规模估算、预算注入和失败语义。
# 怎么运行：python3 scripts/test_compute_plan.py
# 需要什么：Python 3 标准库；不需要真实 GPU。

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compute_plan  # noqa: E402


class ComputePlanTests(unittest.TestCase):
    def test_batch_search_uses_ops_per_sample(self) -> None:
        self.assertEqual(
            compute_plan.estimate_flops("batch-search", 1e8, None, 200),
            2e10,
        )

    def test_explicit_flops_override_estimate(self) -> None:
        self.assertEqual(
            compute_plan.estimate_flops("batch-search", 1e8, 1234, 200),
            1234,
        )

    def test_runtime_budget_controls_gpu_plan(self) -> None:
        plan = compute_plan.decide(
            kind="dense-numeric",
            n=4096,
            dtype="f64",
            flops=2e10,
            gpu_available=True,
            gpu_name="test-device",
            available_mb=32768,
            force_cpu=False,
            threads_max=2,
            memory_budget_gb=20,
            memory_headroom_gb=4,
        )
        self.assertEqual(plan["route"], "gpu")
        self.assertEqual(plan["memory_budget_mb"], 20 * 1024)
        self.assertTrue(plan["needs_gpu_lock"])

    def test_integer_batch_search_can_route_to_gpu(self) -> None:
        plan = compute_plan.decide(
            kind="batch-search",
            n=1e8,
            dtype="int8",
            flops=2e10,
            gpu_available=True,
            gpu_name="cuda-device",
            available_mb=32768,
            force_cpu=False,
            threads_max=1,
            memory_budget_gb=4,
            memory_headroom_gb=2,
        )
        self.assertEqual(plan["route"], "gpu")
        self.assertTrue(plan["needs_gpu_lock"])

    def test_small_integer_batch_stays_on_cpu(self) -> None:
        plan = compute_plan.decide(
            kind="batch-search",
            n=32,
            dtype="int8",
            flops=5120,
            gpu_available=True,
            gpu_name="cuda-device",
            available_mb=32768,
            force_cpu=False,
            threads_max=1,
            memory_budget_gb=4,
            memory_headroom_gb=2,
        )
        self.assertEqual(plan["route"], "cpu")

    def test_invalid_runtime_integer_fails(self) -> None:
        with patch.dict(os.environ, {"COMPUTE_THREADS_MAX": "invalid"}, clear=False):
            with self.assertRaisesRegex(ValueError, "COMPUTE_THREADS_MAX"):
                compute_plan.read_positive_int_env("COMPUTE_THREADS_MAX", 1)


if __name__ == "__main__":
    unittest.main()
