#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import re
from .base import BaseParser, SessionData

class CodexParser(BaseParser):
    def __init__(self, source: str = 'codex'):
        self.source = source
    
    def find_files(self, paths: list) -> list:
        files = []
        for base in paths:
            if not os.path.exists(base):
                continue
            for root, _, names in os.walk(base):
                for f in names:
                    if f.endswith('.jsonl') and f != 'history.jsonl':
                        files.append(os.path.join(root, f))
        return files
    
    def _extract_id(self, filepath: str) -> str:
        match = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', 
                          os.path.basename(filepath))
        return match.group(1) if match else os.path.basename(filepath).replace('.jsonl', '')
    
    def parse_file(self, filepath: str) -> SessionData:
        s = SessionData(
            session_id=self._extract_id(filepath),
            source=self.source,
            file_path=filepath,
            file_mtime=os.path.getmtime(filepath)
        )
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line or line[0] != '{':
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue
                
                if data.get('type') == 'session_meta':
                    p = data.get('payload', {})
                    s.cwd = p.get('cwd')
                    s.session_id = p.get('id', s.session_id)
                    s.start_time = p.get('timestamp') or data.get('timestamp')
                    continue
                
                if data.get('type') != 'response_item':
                    continue
                payload = data.get('payload', {})
                if payload.get('type') != 'message':
                    continue
                role = payload.get('role')
                if role not in ('user', 'assistant'):
                    continue
                
                parts = [item.get('text', '') for item in payload.get('content', [])
                         if isinstance(item, dict) and item.get('type') in ('input_text', 'output_text', 'text')]
                if parts:
                    s.messages.append({
                        'time': data.get('timestamp', ''),
                        'role': 'user' if role == 'user' else 'ai',
                        'content': ' '.join(parts)
                    })
        
        return s
