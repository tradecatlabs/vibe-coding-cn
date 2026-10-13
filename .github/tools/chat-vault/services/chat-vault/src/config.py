#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
配置模块 - 智能路径识别
支持: Linux 原生路径、WSL 路径 (\\wsl.localhost\Ubuntu\...)
"""
import os
import re
from dotenv import load_dotenv

# 项目目录
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")

load_dotenv(os.path.join(PROJECT_DIR, ".env"))

def convert_wsl_path(path: str) -> str:
    match = re.match(r'^\\\\wsl[.\$]?[^\\]*\\[^\\]+\\(.+)$', path, re.IGNORECASE)
    if match:
        return '/' + match.group(1).replace('\\', '/')
    return path

def normalize_path(path: str) -> str:
    path = path.strip()
    path = convert_wsl_path(path)
    return os.path.expanduser(path)

def get_paths(env_key: str) -> list:
    val = os.getenv(env_key, "")
    if not val:
        return []
    return [normalize_path(p) for p in val.split(",") if p.strip()]

def auto_detect_paths() -> dict:
    home = os.path.expanduser("~")
    kiro_db = os.path.join(home, ".local", "share", "kiro-cli")
    candidates = {
        "codex_paths": [os.path.join(home, ".codex", "sessions"), os.path.join(home, ".codex")],
        "kiro_paths": [kiro_db] if os.path.exists(kiro_db) else [],
        "gemini_paths": [os.path.join(home, ".gemini", "tmp"), os.path.join(home, ".gemini")],
        "claude_paths": [os.path.join(home, ".claude")],
    }
    detected = {}
    for key, paths in candidates.items():
        for p in paths:
            if os.path.exists(p):
                detected[key] = [p]
                break
        if key not in detected:
            detected[key] = []
    return detected

def load_config() -> dict:
    auto = auto_detect_paths()
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "logs"), exist_ok=True)
    
    return {
        "codex_paths": get_paths("CODEX_PATHS") or auto.get("codex_paths", []),
        "kiro_paths": get_paths("KIRO_PATHS") or auto.get("kiro_paths", []),
        "gemini_paths": get_paths("GEMINI_PATHS") or auto.get("gemini_paths", []),
        "claude_paths": get_paths("CLAUDE_PATHS") or auto.get("claude_paths", []),
        "output_dir": OUTPUT_DIR,
        "log_dir": os.path.join(OUTPUT_DIR, "logs"),
        "db_path": os.path.join(OUTPUT_DIR, "chat_history.db"),
    }

CONFIG = load_config()
