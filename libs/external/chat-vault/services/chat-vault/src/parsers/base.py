#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class SessionData:
    """会话数据"""
    session_id: str
    source: str
    file_path: str
    file_mtime: float = 0
    cwd: str = None
    start_time: str = None  # 会话开始时间
    messages: List[Dict] = field(default_factory=list)  # [{"time", "role", "content"}]

class BaseParser(ABC):
    @abstractmethod
    def find_files(self, paths: list) -> list:
        pass
    
    @abstractmethod
    def parse_file(self, filepath: str) -> SessionData:
        pass
