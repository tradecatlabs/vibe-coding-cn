#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import glob
import json
from .base import BaseParser, SessionData

class GeminiParser(BaseParser):
    def find_files(self, paths: list) -> list:
        files = []
        for base in paths:
            if os.path.exists(base):
                files.extend(glob.glob(os.path.join(base, "*", "chats", "*.json")))
        return files
    
    def parse_file(self, filepath: str) -> SessionData:
        s = SessionData(
            session_id=os.path.basename(filepath).replace('.json', ''),
            source='gemini',
            file_path=filepath,
            file_mtime=os.path.getmtime(filepath)
        )
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        s.session_id = data.get('sessionId', s.session_id)
        s.start_time = data.get('startTime') or data.get('createTime') or data.get('timestamp')
        
        for msg in data.get('messages', []):
            if msg.get('type') not in ('user', 'gemini'):
                continue
            content = msg.get('content', '')
            if content:
                s.messages.append({
                    'time': msg.get('timestamp', ''),
                    'role': 'user' if msg.get('type') == 'user' else 'ai',
                    'content': content
                })
        
        return s
