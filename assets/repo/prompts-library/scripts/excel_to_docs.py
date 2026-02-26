#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
excel_to_docs.py

Thin wrapper that invokes the Excel → Documents converter implemented
in convert_local.py, keeping a clearer entrypoint name.

Usage:
  python prompt-library/scripts/excel_to_docs.py --excel "prompt (2).xlsx"
  # optional:
  # --category-name <fallback>  --config prompt-library/scripts/config.yaml
"""
from __future__ import annotations
import importlib.util
import sys
from pathlib import Path


def main() -> None:
    script = Path(__file__).resolve().parent / "convert_local.py"
    spec = importlib.util.spec_from_file_location("convert_local", str(script))
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load convert_local.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["convert_local"] = module
    spec.loader.exec_module(module)  # type: ignore
    # Delegate to its CLI
    module.main()  # type: ignore


if __name__ == "__main__":
    main()
