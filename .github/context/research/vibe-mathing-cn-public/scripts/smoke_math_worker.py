#!/usr/bin/env python3
"""Bounded worker for the portable SymPy/mpmath smoke calculation."""

from __future__ import annotations

import json

import mpmath
import sympy as sp


def main() -> int:
    major_minor = tuple(int(part) for part in sp.__version__.split(".")[:2])
    if major_minor < (1, 14):
        raise RuntimeError(f"SymPy 版本过旧：{sp.__version__}")

    x = sp.symbols("x", real=True)
    identity = sp.trigsimp(sp.sin(x) ** 2 + sp.cos(x) ** 2)
    integral = sp.integrate(sp.exp(-(x**2)), (x, -sp.oo, sp.oo))
    with mpmath.workdps(80):
        numeric = mpmath.quad(
            lambda value: mpmath.exp(-(value**2)),
            [-mpmath.inf, mpmath.inf],
        )
        numeric_error = abs(numeric - mpmath.sqrt(mpmath.pi))

    if identity != 1 or integral != sp.sqrt(sp.pi) or numeric_error >= mpmath.mpf("1e-30"):
        raise RuntimeError("portable symbolic/numeric smoke assertion failed")

    print(
        json.dumps(
            {
                "status": "PASS",
                "sympy": sp.__version__,
                "identity": str(identity),
                "gaussian_integral": str(integral),
                "claim_level": "symbolically-checked",
                "kernel_checked": False,
            },
            ensure_ascii=False,
            indent=2,
            allow_nan=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
