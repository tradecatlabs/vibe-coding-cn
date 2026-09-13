#!/usr/bin/env python3
"""Fixed exact-rational counterexample worker for the public pipeline."""

from __future__ import annotations

import json

import sympy as sp


def main() -> int:
    if sp.__version__ != "1.14.0":
        raise RuntimeError(f"SymPy version drift: {sp.__version__}")
    x = sp.Rational(1, 2)
    payload = {
        "backend": "sympy-exact-rational-v1",
        "x": str(x),
        "x_squared": str(x * x),
        "x_squared_lt_x": bool(x * x < x),
    }
    print(
        json.dumps(
            payload, sort_keys=True, separators=(",", ":"), allow_nan=False
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
