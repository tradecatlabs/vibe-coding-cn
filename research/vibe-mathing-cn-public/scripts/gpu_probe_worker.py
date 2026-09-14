#!/usr/bin/env python3
"""Minimal native CUDA runtime probe; invoked only inside a bounded worker."""

from __future__ import annotations

import ctypes
import json
import os
import stat
from pathlib import Path


MAX_RUNTIME_BYTES = 256_000_000
CUDART_CANDIDATES = (
    "/usr/local/cuda/lib64/libcudart.so",
    "/usr/lib/aarch64-linux-gnu/libcudart.so",
    "/usr/lib/x86_64-linux-gnu/libcudart.so",
)


def main() -> int:
    loaded = None
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        print(json.dumps({"available": False, "reason": "unsafe-platform"}, allow_nan=False))
        return 0
    for candidate in CUDART_CANDIDATES:
        candidate_path = Path(candidate)
        if candidate_path.is_symlink():
            continue
        try:
            descriptor = os.open(candidate_path, os.O_RDONLY | nofollow)
        except OSError:
            continue
        try:
            file_stat = os.fstat(descriptor)
            if not stat.S_ISREG(file_stat.st_mode) or file_stat.st_size > MAX_RUNTIME_BYTES:
                continue
        finally:
            os.close(descriptor)
        try:
            if candidate_path.resolve() != candidate_path:
                continue
            loaded = ctypes.CDLL(candidate)
            break
        except OSError:
            continue
    if loaded is None:
        print(json.dumps({"available": False, "reason": "no-cudart"}, allow_nan=False))
        return 0
    count = ctypes.c_int(-1)
    try:
        rc = loaded.cudaGetDeviceCount(ctypes.byref(count))
    except AttributeError:
        print(json.dumps({"available": False, "reason": "cudart-incomplete"}, allow_nan=False))
        return 0
    if rc != 0 or count.value <= 0:
        print(json.dumps({"available": False, "reason": f"cuda-rc={rc}"}, allow_nan=False))
        return 0
    print(json.dumps({"available": True, "reason": "cuda-device"}, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
