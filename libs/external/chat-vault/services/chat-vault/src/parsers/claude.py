#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import hashlib
from datetime import datetime
from collections import defaultdict
from .base import BaseParser, SessionData

class ClaudeParser(BaseParser):
    def find_files(self, paths: list) -> list:
        files = []
        for base in paths:
            history = os.path.join(base, "history.jsonl")
            if os.path.exists(history):
                files.append(history)
        return files
    
    def parse_file(self, filepath: str) -> list:
        """返回多个 SessionData（按 project 分组）"""
        projects = defaultdict(list)
        file_mtime = os.path.getmtime(filepath)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                content = data.get('display', '')
                if not content:
                    continue
                
                project = data.get('project', 'unknown')
                ts_ms = data.get('timestamp', 0)
                ts = datetime.utcfromtimestamp(ts_ms / 1000).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z' if ts_ms else ''
                
                projects[project].append({
                    'time': ts,
                    'role': 'user',
                    'content': content
                })
        
        return [
            SessionData(
                session_id='claude-' + hashlib.md5(proj.encode()).hexdigest()[:12],
                source='claude',
                file_path=filepath,
                file_mtime=file_mtime,
                cwd=proj,
                start_time=msgs[0].get('time') if msgs else None,
                messages=msgs
            )
            for proj, msgs in projects.items()
        ]
